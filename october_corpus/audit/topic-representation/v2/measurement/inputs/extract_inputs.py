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
        raise ValueError('REPRESENTATION_MEASUREMENT_REJECT: ' + message)


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
    if key == 'F010':
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
    need(font.get('/Subtype') == '/Type1', 'one-byte source Type1 font')
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
        pb=pages[pno-1];offsets=[i for i in range(pb['start'],pb['end']) if not raw[i].isspace() or (raw[i]=='\t' and fonts[i]=='/AYZVIA+CMEX10')]
        cursor=0
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
                need(font is not None and font.get('/Subtype')=='/Type1','source Type1 text')
                name=str(font['/BaseFont']);fid,identity=font_identity(font)
                if fid not in faces:
                    faces[fid]=embedded(font)
                    effective=faces[fid][1]
                    identities[fid]=dict(identity,font=name,effective_encoding_sha256=sha(json.dumps(effective,sort_keys=True).encode()),
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
        for decoded,event in stream_events(page.get_contents(),page['/Resources'],[]):
            name=event['font'];stream,mapping,strings=faces[event['font_identity']]
            if decoded.isspace():
                visible=False
                if strings is not None:
                    pen=RecordingPen();strings[event['glyph_name']].draw(pen)
                    visible=any(op not in ('endPath','closePath') for op,args in pen.value)
                else: need(event['glyph_name']=='space','unembedded whitespace is standard space')
                spaces.append(dict(event,visible_outline=visible))
                if not visible: continue
                need(decoded=='\t' and name=='/AYZVIA+CMEX10' and event['encoded_byte']==9 and event['glyph_name']=='bracerightbig', 'exact visible whitespace alias')
            need(cursor<len(offsets),'no excess actual glyphs')
            at=offsets[cursor]
            need(raw[at]==decoded and fonts[at]==name,f'actual byte/font versus extraction page{pno} offset{at}: {repr(decoded)} vs {repr(raw[at])}')
            result[at]=event;cursor+=1
        need(cursor==len(offsets),'every nonspace extracted source glyph has an original event')
        page_data.append(dict(page=pno,aligned_characters=cursor))
    classes=[]
    for (fid,byte,c,glyph),count in sorted(uses.items()):
        stream,mapping,strings=faces[fid];outline=None
        if strings is not None:
            pen=RecordingPen();strings[glyph].draw(pen);outline=sha(json.dumps(pen.value).encode())
        classes.append(dict(font=identities[fid]['font'],font_identity=fid,
            font_dictionary_object=identities[fid]['font_dictionary_object'],font_dictionary_sha256=identities[fid]['font_dictionary_sha256'],
            effective_encoding_sha256=identities[fid]['effective_encoding_sha256'],encoded_byte=byte,decoded_text=c,
            decoded_codepoints=[f'U+{ord(d):04X}' for d in c],glyph_name=glyph,
            occurrences=count,font_stream_sha256=stream,outline_sha256=outline))
    audit=dict(all_nonspace_source_characters_aligned=True,pages=page_data,
        actual_space_events=spaces,space_policy='Actual empty-outline spaces and all generated whitespace are preserved; the exact CMEX10 byte9 decoded tab has a visible right-brace outline and is separately occurrence-bound.',
        form_xobjects_visited=forms,
        font_dictionaries=[dict(font_identity=fid,**info,font_stream_sha256=faces[fid][0]) for fid,info in sorted(identities.items())],
        font_streams=[dict(sha256=s,embedded=s is not None,dictionary_identities=sorted(fid for fid in faces if faces[fid][0]==s)) for s in sorted({f[0] for f in faces.values()},key=lambda x:x or '')],
        encoded_glyph_classes=classes,cache_key='actual PDF dictionary object plus dictionary bytes; effective encoding hash bound separately',primary_font_bytes_exported=False)
    return result,audit


PROGRAMS={'phase177_hexagon_check.g','phase188_gadget_check.g'}
DRIVERS={'phase188_verify.py','phase193_public_check.py'}
FORMAL={'RecognizableRestriction.lean':8,'CompletedHexagonCounterexample.lean':4}

def program_boundary(r):
    p=r['complete_validation_programs'];d=r['complete_operational_drivers'];f=r['complete_formal_files']
    need(len(p)==2 and {Path(x['path']).name for x in p}==PROGRAMS,'both full validation programs')
    need(all(x['role']=='finite_validation' and x['complete_original_file'] and not x['uniform_written_proof_premise'] for x in p),'validation is not uniform proof')
    need(len(d)==2 and {Path(x['path']).name for x in d}==DRIVERS and all(x['role']=='historical_operational_driver' for x in d),'two full drivers separate')
    need(len(f)==2 and {Path(x['path']).name:len(x['declarations']) for x in f}==FORMAL,'two formal files, eight plus four statements')
    need(r['retained_external_cost'] is None and r['graphics_cost'] is None,'unknown retained/graphic costs')
    need(r['program_representation']['primary']=='whole four-page CODE appendix: both complete validation programs' and not r['program_representation']['pruning'],'whole appendix boundary')

def contract_boundary(scope,c):
    need(c['row_count']==len(c['source_rows'])==6 and len(c['proof_spans'])==13,'six source blocks/thirteen contexts')
    for key in ['inherited_source_block_order','proof_spans','precise_hypotheses','source_qualifications','exclusions','validation_boundary']:
        need(c[key]==scope[key],'exact accepted '+key)
    need(c['source_rows']==scope['contracts'] and c['attribution']==scope['source'],'all exact inherited source rows and authors')
    need(c['new_question_credit']==0 and c['new_source_credit']==0 and c['retained_external_cost'] is None and c['graphics_cost'] is None,'no new credit or zero unknown cost')

def full_files(study,rows):
    result={}
    for r in rows:
        b=(study/r['path']).read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'whole raw file '+r['path'])
        result[Path(r['path']).name]=dict(sha256=sha(b),bytes=len(b),role=r['role'],metrics={n:metrics(b.decode(),n) for n in ('NFC','NFKC')})
    return result

def appendix_boundary(study,r):
    row=r['appendix_tex'];b=(study/row['path']).read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'exact complete-code TeX')
    inputs=re.findall(r'\\VerbatimInput\[[^\]]*\]\{([^}]+)\}',b.decode())
    need(len(inputs)==2 and {Path(x).name for x in inputs}==PROGRAMS and all(x.startswith('programs/') for x in inputs),'whole code inputs exactly once')
    need(not re.search(r'firstline|lastline|firstnumber|lastnumber',b.decode()),'no code pruning')
    return dict(tex_sha256=sha(b),full_file_inclusions=inputs,all_complete=True,pdf_render_trust='Exact four-page full-code PDF was accepted with the scientific edition; this measurement does not repeat that build.')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,default=HERE.parent);ap.add_argument('--public-root',type=Path);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'fresh output');a.out.mkdir(parents=True)
    protocol=json.loads((HERE/'protocol.json').read_text());specs={}
    for name in ['policy','source_input_spec','replacement_input_spec','publication_binding','source_contract_boundary','graphic_inventory','font_audit']:
        b=(HERE/(name+'.json')).read_bytes();need(sha(b)==protocol[name+'_sha256'],'fixed '+name);specs[name]=json.loads(b)
    need(sha((HERE/'calibration.py').read_bytes())==protocol['calibration_sha256'],'fixed visible-glyph calibration')
    source=specs['source_input_spec'];replacement=specs['replacement_input_spec'];policy=specs['policy']
    need(pypdf.__version__==source['pypdf_version']==replacement['pypdf_version']=='6.13.0' and fontTools.__version__==protocol['fonttools_version']=='4.63.0','pinned parser versions')
    need(set(source['sources'])=={'F010'} and set(replacement['ours'])=={'U_R','R1','CODE'},'all four complete PDFs')
    for key in ['author','independent_review','role_delta','root_adoption','accepted_scope']:
        r=policy[key];b=(a.study_root/r['path']).read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'accepted binding '+key)
    program_boundary(replacement);scope=json.loads((a.study_root/policy['accepted_scope']['path']).read_text());contract_boundary(scope,specs['source_contract_boundary'])
    docs={};cache={};audits={}
    for key,row in (source['sources']|replacement['ours']).items():
        raw,before,after,fonts,events=document(a.study_root,key,row);cache[key]=(raw,fonts,events)
        if key in source['sources']:_,audits[key]=actual_event_alignment(a.study_root/row['path'],raw,fonts,row['page_bindings'])
        variants={v:{n:metrics(t,n) for n in ('NFC','NFKC')} for v,t in [('raw_untrimmed',raw),('raw_selected',before),('calibrated_selected',after)]}
        docs[key]=dict(pdf_sha256=row['pdf_sha256'],pages=row['pages'],calibrations=len(row['glyph_substitutions']),furniture_occurrences=len(row['excluded_furniture']),variants=variants)
    need(audits==specs['font_audit'],'all actual dictionary/encoding/outline evidence')
    programs=full_files(a.study_root,replacement['complete_validation_programs']);drivers=full_files(a.study_root,replacement['complete_operational_drivers']);formal=full_files(a.study_root,replacement['complete_formal_files']);appendix=appendix_boundary(a.study_root,replacement)
    checked=[]
    if a.public_root:
        pub=specs['publication_binding'];r=pub['admission'];need(sha((a.public_root/r['path']).read_bytes())==r['sha256'],'exact public scientific admission')
        for key,row in pub['documents'].items():
            need(sha((a.public_root/row['public_path']).read_bytes())==row['sha256'],'public mathematical copy '+key);checked.append(row['public_path'])
    controls=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError):controls.append(dict(name=name,rejected=True));return
        raise RuntimeError('mutation accepted: '+name)
    for name,change in [
        ('omit complete validation program',lambda x:x['complete_validation_programs'].pop()),
        ('promote samples to uniform premise',lambda x:x['complete_validation_programs'][0].update(uniform_written_proof_premise=True)),
        ('prune whole program',lambda x:x['complete_validation_programs'][0].update(complete_original_file=False)),
        ('omit complete driver',lambda x:x['complete_operational_drivers'].pop()),
        ('omit formal declaration',lambda x:x['complete_formal_files'][0]['declarations'].pop()),
        ('zero unknown cost',lambda x:x.update(graphics_cost=0))]:
        b=copy.deepcopy(replacement);change(b);reject(name,lambda b=b:program_boundary(b))
    for name,change in [('omit principal clause',lambda x:x['source_rows'].pop()),('erase degree correction',lambda x:x['source_qualifications'].pop(0)),('claim source question answer as new',lambda x:x.update(new_question_credit=1)),('drop normality',lambda x:x['precise_hypotheses'].update(normal_subgroup_required=False))]:
        b=copy.deepcopy(specs['source_contract_boundary']);change(b);reject(name,lambda b=b:contract_boundary(scope,b))
    raw,fonts,events=cache['F010'];row=source['sources']['F010']
    for name,change in [('omit alias',lambda x:x['glyph_substitutions'].pop()),('alter visible glyph',lambda x:x['glyph_substitutions'][0].update(output='x')),('erase visible glyph',lambda x:x['glyph_substitutions'][0].update(output='')),('wrong font',lambda x:x['glyph_substitutions'][0].update(input_font='/Wrong')),('wrong context',lambda x:x['glyph_substitutions'][0].update(context_sha256='0'*64)),('wrong actual byte',lambda x:x['glyph_substitutions'][0]['pdf_event'].update(encoded_byte=255)),('wrong font dictionary',lambda x:x['glyph_substitutions'][0]['pdf_event']['font_dictionary_object'].update(idnum=0)),('wrong effective encoding',lambda x:x['glyph_substitutions'][0]['pdf_event'].update(effective_encoding_sha256='0'*64)),('lose right brace as whitespace',lambda x:next(g for g in x['glyph_substitutions'] if g['input_codepoint']=='U+0009').update(output=' ')),('combine mapsto and arrow',lambda x:next(g for g in x['glyph_substitutions'] if g['pdf_event']['glyph_name']=='mapsto').update(output='↦'))]:
        b=copy.deepcopy(row);change(b);reject(name,lambda b=b:calibrate(raw,b,fonts,'F010',events))
    b=copy.deepcopy(row);b['included_spans'][0]['start']=1;reject('drop first source character',lambda:document(a.study_root,'F010',b))
    b=copy.deepcopy(row);b['excluded_furniture'][0]['literal']='invented';reject('invent running furniture',lambda:document(a.study_root,'F010',b))
    b=copy.deepcopy(audits);b['F010']['encoded_glyph_classes'][0]['glyph_name']='.notdef';reject('wrong outline evidence',lambda:need(b==audits,'actual glyph audit'))
    report=dict(status='PASS_PROPOSED_INPUT_REPLAY_NOT_NUMERICAL_ADMISSION',protocol_sha256=sha((HERE/'protocol.json').read_bytes()),documents=docs,complete_validation_programs=programs,complete_operational_drivers=drivers,complete_formal_files=formal,appendix=appendix,controls=controls,source_contract_rows=6,principal_contracts=1,new_source_credit=0,new_question_credit=0,pdf_metric_cells=120,raw_program_metric_cells=20,raw_driver_metric_cells=20,raw_formal_metric_cells=20,public_exact_documents_checked=checked,ratios=None,primary_text_exported=False)
    (a.out/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');(a.out/'font_audit.json').write_text(json.dumps(audits,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(status=report['status'],pdf_metric_cells=120,raw_program_metric_cells=20,driver_metric_cells=20,formal_metric_cells=20,controls=len(controls),ratio=None)))
if __name__=='__main__':main()
