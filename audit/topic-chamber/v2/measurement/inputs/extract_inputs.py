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
        raise ValueError('CHAMBER_MEASUREMENT_REJECT: ' + message)


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
            fontname = str(font.get('/BaseFont', font.get('/Name',''))) if font else ''
            pieces.append(text)
            local.extend([str(font.get('/BaseFont', font.get('/Name',''))) if font else ''] * len(text))

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
    if key in ('L008','N016'):
        events, _ = actual_event_alignment(pdf, raw, fonts, pages)
    calibrated = calibrate(raw, row, fonts, key, events)
    return raw, selected(raw, row), selected(calibrated, row), fonts, events


def read_type1(data):
    """Read literal Type1 bytes, allowing absent unused Subrs/array slots.

    Some 2005 subset fonts omit Subrs altogether or leave unused Encoding
    entries as PostScript nulls. The standard FontTools convenience parser
    assumes both structures are populated. No used glyph is substituted.
    """
    from fontTools.misc import psLib,psCharStrings,eexec
    original=psLib.unpack_item
    def sparse(item):
        return None if item is None else original(item)
    try:
        psLib.unpack_item=sparse
        face=psLib.suckfont(data,'ascii')
    finally: psLib.unpack_item=original
    subrs=face['Private'].get('Subrs',[]);lenIV=face['Private'].get('lenIV',4)
    need(lenIV>=0,'nonnegative Type1 lenIV')
    for name,raw in face['CharStrings'].items():
        clear,_=eexec.decrypt(raw,4330)
        face['CharStrings'][name]=psCharStrings.T1CharString(clear[lenIV:],subrs=subrs)
    for i,raw in enumerate(subrs):
        if raw is not None:
            clear,_=eexec.decrypt(raw,4330);subrs[i]=psCharStrings.T1CharString(clear[lenIV:],subrs=subrs)
    return face


def embedded(font):
    """Read the actual Type1 program, with the PDF's encoding differences."""
    if font.get('/Subtype') == '/Type3':
        encoding=font['/Encoding'].get_object();mapping={};index=0
        for item in encoding['/Differences']:
            if isinstance(item,int):index=item
            else:mapping[index]=str(item).lstrip('/');index+=1
        strings={str(k).lstrip('/'):dict(type3_character_program=v.get_object().get_data()) for k,v in font['/CharProcs'].items()}
        return None,mapping,strings
    need(font.get('/Subtype') == '/Type1', 'one-byte source Type1 or literal Type3 font')
    descriptor=font.get('/FontDescriptor')
    if descriptor is None:
        need(str(font['/BaseFont']) == '/Times-Roman' and str(font.get('/Encoding')) == '/WinAnsiEncoding',
             'only the explicitly WinAnsi standard identification-banner font is unembedded')
        from fontTools.agl import UV2AGL
        return None, {i:UV2AGL.get(ord(bytes([i]).decode('cp1252',errors='replace')),'.notdef') for i in range(256)}, None
    descriptor=descriptor.get_object()
    need('/FontFile' in descriptor or '/FontFile3' in descriptor, 'embedded source font program')
    if '/FontFile' in descriptor:
        data=descriptor['/FontFile'].get_object().get_data()
        face=read_type1(data)
        encoding,strings=face['Encoding'],face['CharStrings']
    else:
        data=descriptor['/FontFile3'].get_object().get_data()
        face=CFFFontSet();face.decompile(BytesIO(data),None)
        top=face[face.fontNames[0]];encoding,strings=top.Encoding,top.CharStrings
    if isinstance(encoding,str):
        need(encoding=='StandardEncoding','known CFF named encoding')
        from fontTools.encodings.StandardEncoding import StandardEncoding
        encoding=StandardEncoding
    mapping=dict(enumerate(encoding))
    override=font.get('/Encoding')
    if override is not None: override=override.get_object()
    base_override = override.get('/BaseEncoding') if override and not isinstance(override,str) else override
    if base_override == '/StandardEncoding':
        from fontTools.encodings.StandardEncoding import StandardEncoding
        mapping=dict(enumerate(StandardEncoding))
    elif base_override is not None and base_override != '/WinAnsiEncoding':
        raise ValueError('Unsupported explicit BaseEncoding '+str(base_override))
    if base_override == '/WinAnsiEncoding':
        from fontTools.agl import UV2AGL
        mapping={i:UV2AGL.get(ord(bytes([i]).decode('cp1252',errors='replace')),'.notdef') for i in range(256)}
    if override and not isinstance(override,str):
        for item in override.get('/Differences',[]):
            if isinstance(item,int): index=item
            else: mapping[index]=str(item).lstrip('/'); index+=1
    return sha(data),mapping,strings


def glyph_evidence(strings,glyph):
    if strings is None:
        return dict(kind='unembedded_standard_glyph',visible=glyph!='space',outline_sha256=None)
    obj=strings[glyph]
    if isinstance(obj,dict) and 'type3_character_program' in obj:
        b=obj['type3_character_program']
        need(b'BI' in b and b'/IM true' in b and b'/W 38' in b and b'/H 38' in b,'literal Type3 bitmap glyph format')
        return dict(kind='Type3_image_mask_character_program',visible=True,character_program_sha256=sha(b),character_program_bytes=len(b),bitmap_dimensions=[38,38],image_mask=True,outline_sha256=None)
    pen=RecordingPen();obj.draw(pen)
    return dict(kind='embedded_Type1_outline',visible=any(op not in ('endPath','closePath') for op,args in pen.value),outline_sha256=sha(json.dumps(pen.value).encode()))


def font_identity(font):
    """Bind the actual PDF dictionary separately from its shared embedded stream."""
    data=BytesIO();font.write_to_stream(data)
    ref=getattr(font,'indirect_reference',None)
    object_id=None if ref is None else dict(idnum=ref.idnum,generation=ref.generation)
    declaration=font.get('/Encoding')
    if declaration is not None: declaration=declaration.get_object()
    def plain(value):
        value=value.get_object() if hasattr(value,'get_object') else value
        if isinstance(value,dict):return {str(k):plain(v) for k,v in sorted(value.items())}
        if isinstance(value,list):return [plain(v) for v in value]
        if value is None or isinstance(value,(bool,int,float)):return value
        return str(value)
    info=dict(font_dictionary_object=object_id,font_dictionary_sha256=sha(data.getvalue()),
              pdf_encoding_declaration=plain(declaration))
    return sha(json.dumps(info,sort_keys=True).encode()),info


def actual_event_alignment(path, raw, fonts, pages):
    """Replay actual Type1 glyph events keyed by PDF dictionary, not BaseFont.

    Identically named fonts can have different PDF Encoding/Differences. The
    cache key binds the actual dictionary/object. Shared font-program streams
    remain separately identified; they never merge effective encodings.
    """
    reader=pypdf.PdfReader(path);result={};faces={};identities={};uses=Counter();spaces=[];page_data=[];forms=[]
    for pno,page in enumerate(reader.pages,1):
        pb=pages[pno-1];cursor=0
        def stream_events(content,resources,route,initial_font=None,initial_resource=None):
            font=initial_font;resource=initial_resource;stack=[]
            for oi,(operands,op) in enumerate(ContentStream(content,reader).operations):
                if op==b'q': stack.append((font,resource))
                elif op==b'Q': font,resource=stack.pop()
                elif op==b'Tf':
                    resource=str(operands[0]);font=resources['/Font'][operands[0]].get_object()
                elif op==b'Do':
                    name=operands[0];obj=resources['/XObject'][name].get_object()
                    if obj.get('/Subtype')=='/Form':
                        subroute=route+[dict(operator_index=oi,resource=str(name),stream_sha256=sha(obj.get_data()))]
                        forms.append(dict(page=pno,route=subroute))
                        yield from stream_events(obj,obj.get('/Resources',resources),subroute,font,resource)
                if op not in (b'Tj',b'TJ',b"'",b'"'): continue
                need(font is not None and font.get('/Subtype') in ('/Type1','/Type3'),'source Type1 or Type3 text')
                name=str(font.get('/BaseFont',font.get('/Name','')));fid,identity=font_identity(font)
                if fid not in faces:
                    faces[fid]=embedded(font)
                    effective=faces[fid][1]
                    identities[fid]=dict(identity,font=name,pdf_subtype=str(font['/Subtype']),effective_encoding_sha256=sha(json.dumps(effective,sort_keys=True).encode()),
                        effective_encoding={str(k):v for k,v in sorted(effective.items())})
                stream,mapping,strings=faces[fid];encoding,cmap=_cmap.get_encoding(font)
                parts=operands[0] if op==b'TJ' else [operands[-1]]
                for pi,part in enumerate(parts):
                    if not isinstance(part,(TextStringObject,ByteStringObject)): continue
                    data=part.original_bytes if hasattr(part,'original_bytes') else bytes(part)
                    for bi,byte in enumerate(data):
                        decoded=encoding.get(byte,chr(byte)) if isinstance(encoding,dict) else bytes([byte]).decode(encoding)
                        decoded=''.join(cmap.get(c,c) for c in decoded)
                        need(bool(decoded),'nonempty decoded glyph text')
                        glyph=mapping.get(byte,'standard_'+decoded if stream is None else '')
                        need(bool(glyph) and glyph!='.notdef','actual embedded encoding resolves every used glyph')
                        event=dict(page=pno,form_route=route,operator_index=oi,operator=op.decode('ascii'),part_index=pi,
                            byte_index=bi,encoded_byte=byte,font_resource=resource,font=name,
                            font_identity=fid,**{k:v for k,v in identities[fid].items() if k not in ('font','effective_encoding','pdf_encoding_declaration')},
                            text_part_sha256=sha(data),decoded_text=decoded,decoded_codepoints=[f'U+{ord(c):04X}' for c in decoded],glyph_name=glyph,
                            font_stream_sha256=stream)
                        uses[fid,byte,decoded,glyph]+=1
                        for di,c in enumerate(decoded):
                            yield c,dict(event,decoded_character_index=di)
        actual=list(stream_events(page.get_contents(),page['/Resources'],[]))
        visible_spaces=set()
        for decoded,event in actual:
            if not decoded.isspace():continue
            _,_,strings=faces[event['font_identity']]
            evidence=glyph_evidence(strings,event['glyph_name'])
            spaces.append(dict(event,visible_outline=evidence['visible'],glyph_evidence=evidence))
            if evidence['visible']:visible_spaces.add((decoded,event['font']))
        offsets=[i for i in range(pb['start'],pb['end']) if not raw[i].isspace() or (raw[i],fonts[i]) in visible_spaces]
        for decoded,event in actual:
            name=event['font'];stream,mapping,strings=faces[event['font_identity']]
            if decoded.isspace() and not glyph_evidence(strings,event['glyph_name'])['visible']:continue
            need(cursor<len(offsets),'no excess actual glyphs')
            at=offsets[cursor]
            need(raw[at]==decoded and fonts[at]==name,f'actual byte/font versus extraction page{pno} offset{at}: {repr(decoded)} vs {repr(raw[at])}')
            result[at]=event;cursor+=1
        need(cursor==len(offsets),'every nonspace extracted source glyph has an original event')
        page_data.append(dict(page=pno,aligned_characters=cursor))
    classes=[]
    for (fid,byte,c,glyph),count in sorted(uses.items()):
        stream,mapping,strings=faces[fid];evidence=glyph_evidence(strings,glyph)
        classes.append(dict(font=identities[fid]['font'],font_identity=fid,
            font_dictionary_object=identities[fid]['font_dictionary_object'],font_dictionary_sha256=identities[fid]['font_dictionary_sha256'],
            effective_encoding_sha256=identities[fid]['effective_encoding_sha256'],encoded_byte=byte,decoded_text=c,
            decoded_codepoints=[f'U+{ord(d):04X}' for d in c],glyph_name=glyph,
            occurrences=count,font_stream_sha256=stream,glyph_evidence=evidence))
    audit=dict(all_nonspace_source_characters_aligned=True,pages=page_data,
        actual_space_events=spaces,space_policy='All actual visible whitespace-decoded glyphs are aligned and counted with exact source byte/dictionary evidence; empty-outline spaces and generated whitespace remain unchanged. Ambiguous alignment fails closed.',
        form_xobjects_visited=forms,
        font_dictionaries=[dict(font_identity=fid,**info,font_stream_sha256=faces[fid][0]) for fid,info in sorted(identities.items())],
        font_streams=[dict(sha256=s,embedded=s is not None,dictionary_identities=sorted(fid for fid in faces if faces[fid][0]==s)) for s in sorted({f[0] for f in faces.values()},key=lambda x:x or '')],
        encoded_glyph_classes=classes,cache_key='actual PDF dictionary object plus dictionary bytes; effective encoding hash bound separately',primary_font_bytes_exported=False,font_stream_scope='font_streams inventories embedded Type1 programs only; Type3 character programs have separate glyph_evidence hashes and are not claimed to be absent ink.')
    return result,audit



PROGRAMS={'chiral_cover.g':'required finite premise','reflection_models.py':'diagnostic'}
FORMAL={'LiftCertificate.lean':4,'ChamberOrbit.lean':3,'TwoOrbitReflection.lean':7}

def bound(root,row):
    data=(root/row['path']).read_bytes()
    need(len(data)==row['bytes'] and sha(data)==row['sha256'],'bound complete file '+row['path'])
    return data

def program_boundary(r):
    programs=r['complete_mathematical_programs'];drivers=r['complete_operational_drivers'];formal=r['complete_formal_files']
    need(len(programs)==2 and {Path(x['path']).name for x in programs}==set(PROGRAMS),'whole required and diagnostic programs')
    need(all(x['complete_original_file'] for x in programs),'no program pruning')
    need(programs[0]['classification']=='required' and programs[0]['required_mathematical_premise'] is True and programs[1]['classification']=='diagnostic' and programs[1]['required_mathematical_premise'] is False ,'exact distinct program roles')
    need(len(drivers)==3 and {Path(x['path']).name for x in drivers}=={'archived_author_driver.py','archived_review_driver.py','check.py'},'three full drivers separate')
    need(len(formal)==3 and {Path(x['path']).name:x['reports'] for x in formal}==FORMAL,'three scoped modules and fourteen declarations')
    need(r['program_representation']['primary']=='whole3-page CODE appendix: complete required GAP plus complete diagnostic Python' and r['program_representation']['pruning'] is False and r['program_representation']['drivers_in_appendix'] is False,'whole program boundary')
    need(r['retained_external_cost'] is None and r['graphics_cost'] is None,'unknown cost not zero')

def contract_boundary(scope,question,formal,c):
    need(c['row_count']==len(c['source_rows'])==27 and len(c['proof_spans'])==22,'all 27 source rows/22 proof contexts')
    for key,sourcekey in [('source_rows','rows'),('proof_spans','proof_spans'),('source_bindings','source_bindings'),('principal_contracts','principal_contracts')]:
        need(c[key]==scope[sourcekey],'exact accepted '+key)
    need(c['question_map']==question and c['formal_scope']==formal,'separate question/formal boundaries')
    need(c['new_source_credit']==c['new_question_credit']==0 and c['whole_manuscript_all_assertions_claim'] is False,'no new credit or all-assertions claim')
    need(all(c[k] is None for k in ('retained_external_cost','graphics_cost','historical_software_cost','ratio')),'unknown costs not zero and no factors')

def full_files(root,rows):
    output={}
    for row in rows:
        data=bound(root,row)
        output[Path(row['path']).name]=dict(sha256=sha(data),bytes=len(data),role=row['role'],metrics={form:metrics(data.decode(),form) for form in ('NFC','NFKC')})
    return output

def appendix_boundary(root,r):
    data=bound(root,r['appendix_tex']);text=data.decode()
    inputs=re.findall(r'\\VerbatimInput\[[^\]]*\]\{([^}]+)\}',text)
    need(len(inputs)==2 and {Path(x).name for x in inputs}==set(PROGRAMS) and all(x.startswith('programs/') for x in inputs),'whole program inclusions exactly once')
    need(not re.search(r'firstline|lastline|firstnumber|lastnumber',text),'no printed program pruning')
    return dict(tex_sha256=sha(data),whole_file_inclusions=inputs,all_complete=True,render_scope='The exact accepted three-page scientific appendix is measured; this input replay does not rebuild or rerun its programs.')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True)
    ap.add_argument('--sources-root',type=Path);ap.add_argument('--source-L008',dest='source_L008',type=Path);ap.add_argument('--source-N016',dest='source_N016',type=Path)
    ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'fresh output');a.out.mkdir(parents=True)
    if (HERE/'manifest.json').exists():
        for binding in json.loads((HERE/'manifest.json').read_text())['exports']:
            relative=Path(binding['path']);need(not relative.is_absolute() and '..' not in relative.parts,'safe export path')
            bound(HERE,binding)
    protocol=json.loads((HERE/'protocol.json').read_text());specs={}
    for name in ['policy','source_input_spec','replacement_input_spec','publication_binding','source_contract_boundary','graphic_inventory','font_audit','glyph_reconciliation','visual_review']:
        data=(HERE/(name+'.json')).read_bytes();need(sha(data)==protocol[name+'_sha256'],'fixed '+name);specs[name]=json.loads(data)
    need(sha((HERE/'calibration.py').read_bytes())==protocol['calibration_sha256'],'fixed glyph calibration')
    need(protocol['factors_permitted'] is False and protocol['ratio'] is None,'input proposal only')
    source=specs['source_input_spec'];replacement=specs['replacement_input_spec'];publication=specs['publication_binding']
    need(pypdf.__version__==source['pypdf_version']==replacement['pypdf_version']=='6.13.0' and fontTools.__version__==protocol['fonttools_version']=='4.63.0','exact parser versions')
    need(set(source['sources'])=={'L008','N016'} and set(replacement['ours'])=={'U_H','H1','H2','CODE'},'all six full documents')
    need(source['N016_publisher_pdf_available'] is False,'author edition, not publisher version')
    public_files={key:bound(a.public_root,row) for key,row in publication['bindings'].items()}
    scope=json.loads(public_files['accepted_scope']);question=json.loads(public_files['question_map'])
    formal=json.loads((a.public_root/'papers/topic-chamber/v2/formal/scope.json').read_text())
    program_boundary(replacement);contract_boundary(scope,question,formal,specs['source_contract_boundary'])
    docs={};cache={};audits={};paths={}
    for key,row in (source['sources']|replacement['ours']).items():
        if key in source['sources']:
            path=getattr(a,'source_'+key) or ((a.sources_root/row['path']) if a.sources_root else None)
            need(path is not None,'supply both original PDFs or --sources-root')
        else:path=a.public_root/row['path']
        paths[key]=path;resolved=dict(row,path=str(path.resolve()))
        raw,before,after,fonts,events=document(Path('/'),key,resolved);cache[key]=(raw,fonts,events,resolved)
        if key in source['sources']:_,audits[key]=actual_event_alignment(path,raw,fonts,row['page_bindings'])
        variants={variant:{form:metrics(text,form) for form in ('NFC','NFKC')} for variant,text in [('raw_untrimmed',raw),('raw_selected',before),('calibrated_selected',after)]}
        docs[key]=dict(pdf_sha256=row['pdf_sha256'],pages=row['pages'],calibrations=len(row['glyph_substitutions']),furniture_occurrences=len(row['excluded_furniture']),variants=variants)
        if key in replacement['ours']:need(publication['documents'][key]==dict(path=row['path'],sha256=row['pdf_sha256']),'exact published PDF binding')
    need(audits==specs['font_audit'],'all actual font dictionary/encoding/outline evidence')
    from reconcile import reconcile
    need(reconcile(audits)==specs['glyph_reconciliation'],'all glyph class identifications')
    programs=full_files(a.public_root,replacement['complete_mathematical_programs']);drivers=full_files(a.public_root,replacement['complete_operational_drivers']);formals=full_files(a.public_root,replacement['complete_formal_files']);appendix=appendix_boundary(a.public_root,replacement)
    controls=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError):controls.append(dict(name=name,rejected=True));return
        raise RuntimeError('mutation accepted: '+name)
    for name,change in [('omit required program',lambda x:x['complete_mathematical_programs'].pop(0)),('omit diagnostic',lambda x:x['complete_mathematical_programs'].pop()),('promote diagnostic to proof',lambda x:x['complete_mathematical_programs'][1].update(required_mathematical_premise=True)),('prune program',lambda x:x['complete_mathematical_programs'][0].update(complete_original_file=False)),('omit driver',lambda x:x['complete_operational_drivers'].pop()),('omit Lean declaration',lambda x:x['complete_formal_files'][0].update(reports=3)),('zero graphic cost',lambda x:x.update(graphics_cost=0))]:
        b=copy.deepcopy(replacement);change(b);reject(name,lambda b=b:program_boundary(b))
    for name,change in [('omit source clause',lambda x:x['source_rows'].pop()),('omit proof context',lambda x:x['proof_spans'].pop(next(iter(x['proof_spans'])))),('claim new question',lambda x:x.update(new_question_credit=1)),('claim all assertions',lambda x:x.update(whole_manuscript_all_assertions_claim=True)),('change all-rank finite status',lambda x:x['question_map'].update(invented_all_rank_solution=True)),('claim full formalization',lambda x:x['formal_scope'].update(full_application_verified=True))]:
        b=copy.deepcopy(specs['source_contract_boundary']);change(b);reject(name,lambda b=b:contract_boundary(scope,question,formal,b))
    for key in ('L008','N016'):
        raw,fonts,events,row=cache[key]
        changes=[('omit alias',lambda x:x['glyph_substitutions'].pop()),('alter glyph',lambda x:x['glyph_substitutions'][0].update(output='x')),('erase glyph',lambda x:x['glyph_substitutions'][0].update(output='')),('wrong font',lambda x:x['glyph_substitutions'][0].update(input_font='/Wrong')),('wrong context',lambda x:x['glyph_substitutions'][0].update(context_sha256='0'*64)),('wrong actual byte',lambda x:x['glyph_substitutions'][0]['pdf_event'].update(encoded_byte=255)),('wrong font dictionary',lambda x:x['glyph_substitutions'][0]['pdf_event']['font_dictionary_object'].update(idnum=0)),('wrong effective encoding',lambda x:x['glyph_substitutions'][0]['pdf_event'].update(effective_encoding_sha256='0'*64))]
        if key=='L008':changes.append(('lose visible formfeed as whitespace',lambda x:next(g for g in x['glyph_substitutions'] if g['input_codepoint']=='U+000C').update(output=' ')))
        else:changes.append(('lose Type3 bitmap bullet',lambda x:next(g for g in x['glyph_substitutions'] if g['input_codepoint']=='U+0088').update(output=' ')))
        for name,change in changes:
            b=copy.deepcopy(row);change(b);reject(key+' '+name,lambda b=b:calibrate(raw,b,fonts,key,events))
        b=copy.deepcopy(row);b['included_spans'][0]['start']=1;reject(key+' drop first character',lambda b=b:document(Path('/'),key,b))
        b=copy.deepcopy(row);b['excluded_furniture'][0]['literal']='invented';reject(key+' invent furniture',lambda b=b:document(Path('/'),key,b))
    b=copy.deepcopy(audits);b['N016']['encoded_glyph_classes'][0]['glyph_name']='.notdef';reject('falsify actual outline audit',lambda:need(b==audits,'actual glyph audit'))
    report=dict(status='PASS_PROPOSED_INPUT_REPLAY_NOT_NUMERICAL_ADMISSION',protocol_sha256=sha((HERE/'protocol.json').read_bytes()),publication_commit=publication['commit'],documents=docs,complete_mathematical_programs=programs,complete_operational_drivers=drivers,complete_formal_files=formals,appendix=appendix,controls=controls,source_contract_rows=27,proof_contexts=22,principal_contracts=2,new_source_credit=0,new_question_credit=0,pdf_metric_cells=180,raw_program_metric_cells=20,raw_driver_metric_cells=30,raw_formal_metric_cells=30,public_provenance_bindings=len(public_files),ratios=None,primary_text_exported=False)
    (a.out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(a.out/'font_audit.json').write_text(json.dumps(audits,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(status=report['status'],documents=6,pages=36,pdf_metric_cells=180,raw_metric_cells=80,controls=len(controls),ratio=None)))
if __name__=='__main__':main()
