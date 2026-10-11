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
        raise ValueError('TOPIC_AFFINE_MEASUREMENT_REJECT: ' + message)


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
    if key == 'L012':
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
        actual_space_events=spaces,space_policy='Six standard banner spaces preserved; generated whitespace also preserved.',
        font_streams=[dict(font=k,sha256=v[0],embedded=v[0] is not None) for k,v in sorted(faces.items())],
        encoded_glyph_classes=classes,primary_font_bytes_exported=False)
    return result,audit


REQUIRED={'phase250_affine64_kernel.g','phase250_affine_check.py','phase250_base384_census.g',
    'phase250_fixed_groups.g','phase2_cubic_kernel_check.g','phase2_cubic_lattice_check.py'}
AUXILIARY={'check.py','integrity_controls.py','controls.py'}

def program_boundary(replacement):
    rows=replacement['complete_mathematical_programs']
    need(len(rows)==6 and {Path(r['path']).name for r in rows}==REQUIRED,'six whole required programs')
    need(all(r['classification']=='required' for r in rows),'no required program demotion')
    aux=replacement['complete_auxiliary_scripts']
    need(len(aux)==3 and {Path(r['path']).name for r in aux}==AUXILIARY,'all three separate auxiliary scripts')


def full_files(study,public,rows):
    report={}
    for row in rows:
        path=public/row['public_path'] if public else study/row['path']
        data=path.read_bytes();need(len(data)==row['bytes'] and sha(data)==row['sha256'],'whole raw file '+row['path'])
        text=data.decode('utf-8')
        report[Path(row['path']).name]=dict(sha256=sha(data),bytes=len(data),role=row['role'],
            metrics={form:metrics(text,form) for form in ('NFC','NFKC')})
    return report


def appendix_boundary(study,public,replacement):
    row=replacement['appendix_tex'];path=public/row['public_path'] if public else study/row['path']
    data=path.read_bytes();need(sha(data)==row['sha256'],'exact complete appendix TeX')
    inclusions=re.findall(r'\\VerbatimInput\[[^\]]*\]\{([^}]+)\}',data.decode())
    need(len(inclusions)==6 and {Path(p).name for p in inclusions}==REQUIRED,'all six full verbatim inputs exactly once')
    need(all(p.startswith('programs/') and Path(p).name in REQUIRED for p in inclusions),'actual full-file inputs')
    need(not re.search(r'firstline|lastline|firstnumber|lastnumber',data.decode()),'no truncated program listings')
    return dict(tex_sha256=sha(data),full_file_inclusions=inclusions,all_complete=True,
        pdf_render_trust='The bound eight-page appendix is byte-identical to the independently reviewed publication; this input replay does not rerender it.')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,default=HERE.parent)
    ap.add_argument('--public-root',type=Path);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();need(not args.out.exists() and not args.out.is_symlink(),'fresh output directory')
    args.out.mkdir(parents=True)
    protocol=json.loads((HERE/'protocol.json').read_text());specs={}
    for name in ('policy','source_input_spec','replacement_input_spec','publication_binding','source_contract_boundary','graphic_inventory'):
        b=(HERE/(name+'.json')).read_bytes();need(sha(b)==protocol[name+'_sha256'],'frozen '+name);specs[name]=json.loads(b)
    need(sha((HERE/'calibration.py').read_bytes())==protocol['calibration_sha256'],'frozen calibration')
    source,replacement,pub=specs['source_input_spec'],specs['replacement_input_spec'],specs['publication_binding']
    need(pypdf.__version__==source['pypdf_version']==replacement['pypdf_version']=='6.13.0','pinned extraction')
    need(fontTools.__version__==protocol['fonttools_version']=='4.63.0','pinned font parser')
    need(set(source['sources'])=={'L012'} and set(replacement['ours'])=={'U_Affine','AF1','CODE'},'exact complete document boundary')
    program_boundary(replacement)
    scope_binding=replacement['accepted_scope']
    scope_path=args.public_root/'papers/topic-affine/v2/scope.json' if args.public_root else args.study_root/scope_binding['path']
    need(sha(scope_path.read_bytes())==scope_binding['sha256'],'exact admitted mathematical scope')
    scope=json.loads(scope_path.read_text());contract=specs['source_contract_boundary']
    need(scope['source']=='L012' and scope['ledger_rows']==33 and len(scope['source_rows'])==33,'exact source and all 33 rows')
    need(contract['source_rows']==scope['source_rows'] and contract['exclusions']==scope['exclusions'],'complete unchanged admitted source clauses')
    need(scope['formal_scope']['new']==2 and scope['formal_scope']['reused']==7 and not scope['formal_scope']['end_to_end'],'nine scoped declarations only')
    docs={};cache={};font_audit={} 
    for key,row in (source['sources']|replacement['ours']).items():
        base,actual=args.study_root,row
        if args.public_root and key in replacement['ours']:
            mapped=pub['documents'][key]
            need(mapped['private_path']==row['path'] and mapped['sha256']==row['pdf_sha256'],'exact publication route')
            base,actual=args.public_root,dict(row,path=mapped['public_path'])
        raw,before,after,fonts,events=document(base,key,actual);cache[key]=(raw,fonts,events)
        if key=='L012':
            _,font_audit[key]=actual_event_alignment(base/actual['path'],raw,fonts,row['page_bindings'])
        variants={v:{n:metrics(t,n) for n in ('NFC','NFKC')} for v,t in [('raw_untrimmed',raw),('raw_selected',before),('calibrated_selected',after)]}
        docs[key]=dict(pdf_sha256=row['pdf_sha256'],pages=row['pages'],calibrations=len(row['glyph_substitutions']),
            furniture_occurrences=len(row['excluded_furniture']),variants=variants)
    programs=full_files(args.study_root,args.public_root,replacement['complete_mathematical_programs'])
    auxiliary=full_files(args.study_root,args.public_root,replacement['complete_auxiliary_scripts'])
    formal=full_files(args.study_root,args.public_root,replacement['complete_formal_files'])
    appendix=appendix_boundary(args.study_root,args.public_root,replacement)
    controls=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError):controls.append(dict(name=name,rejected=True));return
        raise ValueError('control did not reject: '+name)
    r=copy.deepcopy(replacement);r['complete_mathematical_programs'].pop();reject('omit required program',lambda:program_boundary(r))
    r=copy.deepcopy(replacement);r['complete_mathematical_programs'][0]['classification']='diagnostic';reject('demote required program',lambda:program_boundary(r))
    r=copy.deepcopy(replacement);r['complete_auxiliary_scripts'].pop();reject('omit auxiliary discrepancy union',lambda:program_boundary(r))
    raw,fonts,events=cache['L012'];row=source['sources']['L012']
    for label,change in [
        ('delete calibration',lambda r:r['glyph_substitutions'].pop()),
        ('replace visible glyph incorrectly',lambda r:r['glyph_substitutions'][0].update(output='x')),
        ('erase visible glyph',lambda r:r['glyph_substitutions'][0].update(output='')),
        ('wrong encoded event',lambda r:r['glyph_substitutions'][0]['pdf_event'].update(encoded_byte=255)),
        ('wrong font',lambda r:r['glyph_substitutions'][0].update(input_font='/Unknown')),
        ('wrong occurrence context',lambda r:r['glyph_substitutions'][0].update(context_sha256='0'*64))]:
        bad=copy.deepcopy(row);change(bad);reject(label,lambda bad=bad:calibrate(raw,bad,fonts,'L012',events))
    bad=copy.deepcopy(row);bad['included_spans'][0]['start']=1
    reject('body-only source boundary',lambda:document(args.study_root,'L012',bad))
    bad=copy.deepcopy(row);bad['excluded_furniture'][0]['literal']='invented'
    reject('wrong furniture',lambda:document(args.study_root,'L012',bad))
    report=dict(status='PASS_PROPOSED_INPUT_REPLAY_NOT_NUMERICAL_ADMISSION',protocol_sha256=sha((HERE/'protocol.json').read_bytes()),
        documents=docs,complete_programs=programs,complete_auxiliary_scripts=auxiliary,complete_formal_files=formal,
        appendix=appendix,controls=controls,source_contract_rows=33,principal_contracts=1,project_total_preserved=27,
        pdf_metric_cells=4*3*2*5,raw_program_metric_cells=6*2*5,ratios=None,primary_text_exported=False)
    (args.out/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    (args.out/'font_audit.json').write_text(json.dumps(font_audit,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(dict(status=report['status'],pdf_metric_cells=120,raw_program_metric_cells=60,controls=len(controls),ratio=None)))

if __name__=='__main__':main()
