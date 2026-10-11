#!/usr/bin/env python3
"""Portable full-document counts and declared font calibration; no factors."""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import re
import unicodedata
import pypdf
import fontTools
from calibration import glyph_alias
from pypdf import _cmap
from fontTools import t1Lib
from fontTools.cffLib import CFFFontSet
from io import BytesIO
from fontTools.pens.recordingPen import RecordingPen
from collections import Counter
from pypdf.generic import ContentStream, TextStringObject, ByteStringObject

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError('TOPIC_F_MEASUREMENT_REJECT: ' + message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def metrics(text, form):
    text = unicodedata.normalize(form, text)
    collapsed = ' '.join(text.split())
    return dict(whitespace_tokens=len(collapsed.split()),
        alphanumeric_units=len(re.findall(r'[^\W_]+', text)),
        characters_without_whitespace=sum(not c.isspace() for c in text),
        characters_with_collapsed_whitespace=len(collapsed),
        utf8_bytes_with_collapsed_whitespace=len(collapsed.encode()),
        collapsed_text_sha256=sha(collapsed.encode()))


def selected(raw, row):
    parts = []
    for span in row['included_spans']:
        start = span['start']
        for f in row['excluded_furniture']:
            if span['start'] <= f['start'] < f['end'] <= span['end']:
                parts.append(raw[start:f['start']])
                start = f['end']
        parts.append(raw[start:span['end']])
    return '\n'.join(parts)


def calibrate(raw, row, fonts, key, events):
    chars, seen = list(raw), set()
    for glyph in row['glyph_substitutions']:
        at = glyph['offset']
        need(at not in seen, 'no repeated substitution')
        seen.add(at)
        original = chr(int(glyph['input_codepoint'][2:], 16))
        need(raw[at] == original and fonts[at] == glyph['input_font'], 'actual source font/glyph')
        need(at in events and glyph.get('pdf_event') == events[at], 'exact original PDF text event and byte')
        expected = glyph_alias(key, original, fonts[at], events[at])
        need('visitor_event_location' not in glyph, 'no invented whitespace glyph event')
        need(len(glyph['output']) == 1 and glyph['output'] == expected,
             'one authorized visible Unicode glyph; no deletion')
        page = row['page_bindings'][glyph['page'] - 1]
        need(at == page['start'] + glyph['page_offset'] and page['start'] <= at < page['end'],
             'glyph physical-page locator')
        a, b = glyph['context_start'], glyph['context_end']
        need(a <= at < b and sha(raw[a:b].encode()) == glyph['context_sha256'], 'exact context')
        chars[at] = glyph['output']
    for i, c in enumerate(raw):
        bad = ((unicodedata.category(c) == 'Cc' and c not in '\n\r\t') or
               unicodedata.category(c) == 'Co' or c == '\ufffd')
        need(not bad or i in seen, 'every control/private-use glyph classified')
        if glyph_alias(key, c, fonts[i], events.get(i)) is not None:
            need(i in seen, 'every declared printable or whitespace glyph alias classified')
    return ''.join(chars)


def document(study, key, row):
    pdf = study / row['path']
    need(sha(pdf.read_bytes()) == row['pdf_sha256'], 'bound PDF ' + key)
    pages, texts, fonts, events = [], [], [], {}
    at = 0
    for number, page in enumerate(pypdf.PdfReader(pdf).pages, 1):
        pieces, local = [], []

        def visitor(text, cm, tm, font, size):
            fontname = str(font.get('/BaseFont', '')) if font else ''
            pieces.append(text)
            local.extend([str(font.get('/BaseFont', '')) if font else ''] * len(text))

        text = page.extract_text(visitor_text=visitor) or ''
        need(text == ''.join(pieces) and len(text) == len(local), 'font alignment ' + key)
        pages.append(dict(page=number, start=at, end=at + len(text),
                          sha256=sha(text.encode()), empty_extraction=not text))
        at += len(text) + 1
        texts.append(text)
        fonts.extend(local)
        fonts.append('')
    raw = '\n'.join(texts)
    fonts = fonts[:-1]
    need(len(pages) == row['pages'] and pages == row['page_bindings'], 'all physical pages ' + key)
    need(sha(raw.encode()) == row['extraction_sha256'], 'full extraction ' + key)
    need(row['included_spans'] == [dict(start=0, end=len(raw), sha256=sha(raw.encode()),
         role=row['included_spans'][0]['role'])], 'complete-document selection ' + key)
    previous = 0
    for f in row['excluded_furniture']:
        a, b = f['start'], f['end']
        need(previous <= a < b <= len(raw), 'ordered furniture')
        previous = b
        need(raw[a:b] == f['literal'] and sha(raw[a:b].encode()) == f['sha256'],
             'exact declared furniture ' + key)
    if key == 'L014':
        events, _ = actual_event_alignment(pdf, raw, fonts, pages)
    calibrated = calibrate(raw, row, fonts, key, events)
    return raw, selected(raw, row), selected(calibrated, row), fonts, events


def embedded(font):
    """Read the actual Type1 program, with the PDF's encoding differences."""
    need(font.get('/Subtype') == '/Type1', 'one-byte source Type1 font')
    descriptor=font.get('/FontDescriptor')
    if descriptor is None:
        need(str(font['/BaseFont']) == '/Times-Roman' and not font.get('/Encoding'),
             'only the standard banner font is unembedded')
        return None, {32:'space'}, None
    descriptor=descriptor.get_object()
    need('/FontFile' in descriptor or '/FontFile3' in descriptor, 'embedded source font program')
    if '/FontFile' in descriptor:
        data=descriptor['/FontFile'].get_object().get_data()
        face=t1Lib.T1Font.__new__(t1Lib.T1Font)
        face.data=data; face.encoding='ascii'; face.parse()
        encoding,strings=face.font['Encoding'],face.font['CharStrings']
    else:
        data=descriptor['/FontFile3'].get_object().get_data()
        face=CFFFontSet();face.decompile(BytesIO(data),None)
        top=face[face.fontNames[0]];encoding,strings=top.Encoding,top.CharStrings
    mapping=dict(enumerate(encoding))
    override=font.get('/Encoding')
    if override and not isinstance(override,str):
        for item in override.get('/Differences',[]):
            if isinstance(item,int): index=item
            else: mapping[index]=str(item).lstrip('/'); index+=1
    return sha(data),mapping,strings


def actual_event_alignment(path, raw, fonts, pages):
    """Align every printed nonspace source character to an actual text byte.

    Genuine space bytes are allowed only when they are the standard Times-Roman
    space in the banner. All layout and actual whitespace stays in extraction.
    Inline one-pixel image rules are inventoried separately; no form XObject is
    silently skipped. The underlying pypdf decoder is a declared dependency.
    """
    reader=pypdf.PdfReader(path);result={};faces={};uses=Counter();spaces=[];page_data=[]
    for pno,page in enumerate(reader.pages,1):
        need(not page['/Resources'].get('/XObject'),'no unvisited source form XObjects')
        pb=pages[pno-1];offsets=[i for i in range(pb['start'],pb['end']) if not raw[i].isspace()]
        cursor=0;font=None;resource=None;stack=[]
        for oi,(operands,op) in enumerate(ContentStream(page.get_contents(),reader).operations):
            if op==b'q': stack.append((font,resource))
            elif op==b'Q': font,resource=stack.pop()
            elif op==b'Tf':
                resource=str(operands[0]);font=page['/Resources']['/Font'][operands[0]].get_object()
            if op not in (b'Tj',b'TJ',b"'",b'"'): continue
            need(font is not None and font.get('/Subtype')=='/Type1','source Type1 text')
            name=str(font['/BaseFont'])
            if name not in faces: faces[name]=embedded(font)
            stream,mapping,strings=faces[name];encoding,cmap=_cmap.get_encoding(font)
            parts=operands[0] if op==b'TJ' else [operands[-1]]
            for pi,part in enumerate(parts):
                if not isinstance(part,(TextStringObject,ByteStringObject)): continue
                data=part.original_bytes if hasattr(part,'original_bytes') else bytes(part)
                for bi,byte in enumerate(data):
                    decoded=encoding.get(byte,chr(byte)) if isinstance(encoding,dict) else bytes([byte]).decode(encoding)
                    decoded=''.join(cmap.get(c,c) for c in decoded)
                    need(len(decoded)==1,'one decoded character per actual source glyph')
                    glyph=mapping.get(byte,'standard_'+decoded if stream is None else '')
                    need(bool(glyph),'actual embedded encoding resolves every glyph')
                    event=dict(page=pno,operator_index=oi,operator=op.decode('ascii'),part_index=pi,
                        byte_index=bi,encoded_byte=byte,font_resource=resource,font=name,
                        text_part_sha256=sha(data),decoded_codepoint=f'U+{ord(decoded):04X}',glyph_name=glyph,
                        font_stream_sha256=stream)
                    uses[name,byte,decoded,glyph]+=1
                    if decoded.isspace():
                        need(name=='/Times-Roman' and byte==32 and glyph=='space' and pno==1,
                             'actual whitespace glyph is the reviewed standard banner space')
                        spaces.append(event);continue
                    need(cursor<len(offsets),'no excess actual glyphs')
                    at=offsets[cursor]
                    need(raw[at]==decoded and fonts[at]==name,'actual byte/font versus extraction')
                    result[at]=event;cursor+=1
        need(cursor==len(offsets),'every nonspace extracted source glyph has an original event')
        page_data.append(dict(page=pno,aligned_characters=cursor))
    classes=[]
    for (name,byte,c,glyph),count in sorted(uses.items()):
        stream,mapping,strings=faces[name];outline=None
        if strings is not None:
            pen=RecordingPen();strings[glyph].draw(pen);outline=sha(json.dumps(pen.value).encode())
        classes.append(dict(font=name,encoded_byte=byte,decoded_codepoint=f'U+{ord(c):04X}',glyph_name=glyph,
            occurrences=count,font_stream_sha256=stream,outline_sha256=outline))
    audit=dict(all_nonspace_source_characters_aligned=True,pages=page_data,
        actual_space_events=spaces,space_policy='Standard banner spaces preserved; generated whitespace also preserved.',
        font_streams=[dict(font=k,sha256=v[0],embedded=v[0] is not None) for k,v in sorted(faces.items())],
        encoded_glyph_classes=classes,primary_font_bytes_exported=False)
    return result,audit


VALIDATION = {'phase236_models.py', 'phase236_finite_check.g', 'phase248_presentation_check.g'}
DRIVERS = {'phase236_check.py', 'phase248_check.py'}


def program_boundary(replacement):
    rows = replacement['complete_validation_programs']
    need(len(rows) == 3 and {Path(r['path']).name for r in rows} == VALIDATION,
         'three whole validation programs')
    need(all(r['classification'] == 'validation' and r['uniform_written_proof_premise'] is False
             for r in rows), 'validation scope, not a required finite proof')
    drivers = replacement['complete_operational_drivers']
    need(len(drivers) == 2 and {Path(r['path']).name for r in drivers} == DRIVERS,
         'both full archival operational drivers')
    need(all(r['uniform_written_proof_premise'] is False for r in drivers), 'drivers are operational')
    formal = replacement['complete_formal_files']
    need(len(formal) == 1 and Path(formal[0]['path']).name == 'OddKernelIntersection.lean'
         and len(formal[0]['declarations']) == 5, 'five scoped declarations in one whole file')
    need(replacement['retained_external_cost'] is None and replacement['graphics_cost'] is None,
         'unpriced external and graphic costs remain unknown')


def contract_boundary(scope, contract):
    need(scope['source_ids'] == ['L014'] and len(scope['contracts']) == 25, 'all 25 L014 source rows')
    need(contract['source_rows'] == scope['contracts'] and contract['proof_spans'] == scope['proof_spans'],
         'unchanged accepted source and proof scope')
    need(contract['retained_remote_primary'] == scope['retained_remote_primary']
         and contract['retained_classical'] == scope['retained_classical'], 'retained external inputs')
    need(contract['missing_CP_fulltext_cost'] is None and contract['graphics_cost'] is None,
         'missing CP and graphics not assigned zero cost')
    need(scope['validation_boundary']['uniform_written_proof_depends_on_finite_results'] is False,
         'uniform written proofs independent of finite validation')


def full_files(study, rows):
    report = {}
    for row in rows:
        data = (study / row['path']).read_bytes()
        need(len(data) == row['bytes'] and sha(data) == row['sha256'], 'whole raw file ' + row['path'])
        report[Path(row['path']).name] = dict(sha256=sha(data), bytes=len(data), role=row['role'],
            metrics={form: metrics(data.decode('utf-8'), form) for form in ('NFC', 'NFKC')})
    return report


def appendix_boundary(study, replacement):
    row = replacement['appendix_tex']; data = (study / row['path']).read_bytes()
    need(sha(data) == row['sha256'], 'complete appendix TeX')
    inclusions = re.findall(r'\\VerbatimInput\[[^\]]*\]\{([^}]+)\}', data.decode())
    need(len(inclusions) == 3 and {Path(p).name for p in inclusions} == VALIDATION,
         'all three full verbatim inputs exactly once')
    need(all(p.startswith('programs/') for p in inclusions), 'actual full-file inputs')
    need(not re.search(r'firstline|lastline|firstnumber|lastnumber', data.decode()), 'no truncated program listings')
    return dict(tex_sha256=sha(data), full_file_inclusions=inclusions, all_complete=True,
        pdf_render_trust='The bound four-page appendix is the independently accepted full render; this input replay does not rerender it.')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--study-root', type=Path, default=HERE.parent)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(), 'fresh output directory')
    args.out.mkdir(parents=True)
    protocol = json.loads((HERE / 'protocol.json').read_text()); specs = {}
    for name in ('policy', 'source_input_spec', 'replacement_input_spec', 'publication_binding', 'source_contract_boundary', 'graphic_inventory'):
        data = (HERE / (name + '.json')).read_bytes()
        need(sha(data) == protocol[name + '_sha256'], 'frozen ' + name)
        specs[name] = json.loads(data)
    need(sha((HERE / 'calibration.py').read_bytes()) == protocol['calibration_sha256'], 'frozen calibration')
    policy = specs['policy']; source = specs['source_input_spec']; replacement = specs['replacement_input_spec']
    need(pypdf.__version__ == source['pypdf_version'] == replacement['pypdf_version'] == '6.13.0', 'pinned extraction')
    need(fontTools.__version__ == protocol['fonttools_version'] == '4.63.0', 'pinned font parser')
    need(set(source['sources']) == {'L014'} and set(replacement['ours']) == {'U_F', 'F1', 'CODE'}, 'complete four-document boundary')
    for key in ('author', 'independent_review', 'root_adoption', 'accepted_scope'):
        row = policy[key]; data = (args.study_root / row['path']).read_bytes()
        need(len(data) == row['bytes'] and sha(data) == row['sha256'], 'accepted ' + key)
    program_boundary(replacement)
    scope = json.loads((args.study_root / policy['accepted_scope']['path']).read_text())
    contract_boundary(scope, specs['source_contract_boundary'])
    docs = {}; cache = {}; font_audit = {}
    for key, row in (source['sources'] | replacement['ours']).items():
        raw, before, after, fonts, events = document(args.study_root, key, row)
        cache[key] = (raw, fonts, events)
        if key == 'L014':
            _, font_audit[key] = actual_event_alignment(args.study_root / row['path'], raw, fonts, row['page_bindings'])
        variants = {v: {n: metrics(t, n) for n in ('NFC', 'NFKC')}
                    for v, t in [('raw_untrimmed', raw), ('raw_selected', before), ('calibrated_selected', after)]}
        docs[key] = dict(pdf_sha256=row['pdf_sha256'], pages=row['pages'], calibrations=len(row['glyph_substitutions']),
            furniture_occurrences=len(row['excluded_furniture']), variants=variants)
    programs = full_files(args.study_root, replacement['complete_validation_programs'])
    drivers = full_files(args.study_root, replacement['complete_operational_drivers'])
    formal = full_files(args.study_root, replacement['complete_formal_files'])
    appendix = appendix_boundary(args.study_root, replacement)
    controls = []
    def reject(name, function):
        try: function()
        except (ValueError, KeyError, IndexError):
            controls.append(dict(name=name, rejected=True)); return
        raise ValueError('control did not reject: ' + name)
    bad = copy.deepcopy(replacement); bad['complete_validation_programs'].pop()
    reject('omit one validation program', lambda: program_boundary(bad))
    bad = copy.deepcopy(replacement); bad['complete_validation_programs'][0]['classification'] = 'required'
    reject('silently change validation to a required finite premise', lambda: program_boundary(bad))
    bad = copy.deepcopy(replacement); bad['complete_operational_drivers'].pop()
    reject('omit an archival driver', lambda: program_boundary(bad))
    bad = copy.deepcopy(replacement); bad['complete_formal_files'][0]['declarations'].pop()
    reject('omit a scoped formal declaration', lambda: program_boundary(bad))
    bad = copy.deepcopy(replacement); bad['retained_external_cost'] = 0
    reject('replace unknown retained proof cost by zero', lambda: program_boundary(bad))
    bad = copy.deepcopy(specs['source_contract_boundary']); bad['missing_CP_fulltext_cost'] = 0
    reject('replace unavailable CP cost by zero', lambda: contract_boundary(scope, bad))
    raw, fonts, events = cache['L014']; row = source['sources']['L014']
    for name, change in [
        ('delete a calibration', lambda r: r['glyph_substitutions'].pop()),
        ('replace a visible glyph incorrectly', lambda r: r['glyph_substitutions'][0].update(output='x')),
        ('erase a visible glyph', lambda r: r['glyph_substitutions'][0].update(output='')),
        ('change an encoded event', lambda r: r['glyph_substitutions'][0]['pdf_event'].update(encoded_byte=255)),
        ('change a font', lambda r: r['glyph_substitutions'][0].update(input_font='/Unknown')),
        ('change an occurrence context', lambda r: r['glyph_substitutions'][0].update(context_sha256='0'*64)),
        ('reverse the visible normality sign', lambda r: next(x for x in r['glyph_substitutions'] if x['output']=='⊲').update(output='⊳'))]:
        bad = copy.deepcopy(row); change(bad)
        reject(name, lambda bad=bad: calibrate(raw, bad, fonts, 'L014', events))
    bad = copy.deepcopy(row); bad['included_spans'][0]['start'] = 1
    reject('body-only source selection', lambda: document(args.study_root, 'L014', bad))
    bad = copy.deepcopy(row); bad['excluded_furniture'][0]['literal'] = 'invented'
    reject('invented furniture', lambda: document(args.study_root, 'L014', bad))
    report = dict(status='PASS_PROPOSED_INPUT_REPLAY_NOT_NUMERICAL_ADMISSION',
        protocol_sha256=sha((HERE / 'protocol.json').read_bytes()),
        documents=docs, complete_validation_programs=programs, complete_operational_drivers=drivers, complete_formal_files=formal,
        appendix=appendix, controls=controls, source_contract_rows=25, principal_contracts=1, new_source_credit=0, new_question_credit=0,
        pdf_metric_cells=120, raw_validation_program_metric_cells=30, raw_driver_metric_cells=20, raw_formal_metric_cells=10,
        ratios=None, primary_text_exported=False)
    (args.out / 'report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    (args.out / 'font_audit.json').write_text(json.dumps(font_audit, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(dict(status=report['status'], pdf_metric_cells=120, validation_program_metric_cells=30,
                         driver_metric_cells=20, controls=len(controls), ratio=None)))


if __name__ == '__main__':
    main()
