#!/usr/bin/env python3
"""Independent full-PDF recount; no imports from the author's measurement code."""
import argparse
import collections
import copy
import hashlib
import io
import json
import re
import unicodedata
from pathlib import Path

import pypdf
from fontTools.cffLib import CFFFontSet
from fontTools import agl
from pypdf._cmap import get_encoding

FORMS = ('NFC', 'NFKC')
UNITS = ('whitespace_tokens', 'alphanumeric_units', 'characters_without_whitespace',
         'characters_with_collapsed_whitespace', 'utf8_bytes_with_collapsed_whitespace')
GLYPHS = dict(braceleft='{', braceright='}', comma=',', fi='ﬁ', fl='ﬂ', Gamma='Γ',
              multiply='×', quotedblleft='“', quotedblright='”', quoteright='’',
              asteriskmath='∗', arrowright='→', element='∈', backslash='\\',
              intersection='∩', negationslash='̸', emptyset='∅', reflexsubset='⊆',
              angbracketleft='⟨', angbracketright='⟩', sigma='σ', bar='|', similar='∼',
              union='∪', omega='ω', tau='τ', greaterequal='≥', lessequal='≤', slash='/',
              mu='μ', nu='ν', prime='′', eta='η', endash='–', grave='`', a105='○',
              a0='╱', a64='╲', angbracketleftbig='⟨', angbracketleftbigg='⟨',
              angbracketrightbig='⟩', angbracketrightbigg='⟩', braceleftbig='{', bracerightbig='}',
              bracketleftbigg='[', bracketrightbigg=']', bracketleftbt='⎣', bracketleftex='⎢',
              bracketlefttp='⎡', bracketrightbt='⎦', bracketrightex='⎥', bracketrighttp='⎤',
              parenleftBig='(', parenleftBigg='(', parenleftbig='(', parenrightBig=')',
              parenrightBigg=')', parenrightbig=')', summationdisplay='∑', summationtext='∑',
              vextendsingle='⎪', mapsto='∣')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text())


def count(text, form):
    text = unicodedata.normalize(form, text)
    tokens = alphanumeric = nonspace = 0
    was_word = was_alpha = False
    collapsed = []
    space = False
    for c in text:
        white, alpha = c.isspace(), c.isalnum()
        alphanumeric += int(alpha and not was_alpha)
        was_alpha = alpha
        if white:
            was_word = False
            space = bool(collapsed)
            continue
        tokens += int(not was_word)
        nonspace += 1
        was_word = True
        if space:
            collapsed.append(' ')
        space = False
        collapsed.append(c)
    value = ''.join(collapsed)
    return dict(whitespace_tokens=tokens, alphanumeric_units=alphanumeric,
                characters_without_whitespace=nonspace, characters_with_collapsed_whitespace=len(value),
                utf8_bytes_with_collapsed_whitespace=len(value.encode()), collapsed_text_sha256=sha(value.encode()))


def font_evidence(reader, key, groups):
    fonts = {}
    for page in reader.pages:
        for ref in page['/Resources']['/Font'].values():
            font = ref.get_object()
            fonts[str(font.get('/BaseFont'))] = font
    verified = []
    for group in groups:
        name = group['font']
        font = fonts[name]
        descriptor = font['/FontDescriptor']
        char = chr(int(group['input_codepoint'][2:], 16))
        if key == 'L088':
            raw = descriptor['/FontFile3'].get_data()
            cff = CFFFontSet()
            cff.decompile(io.BytesIO(raw), None)
            encoding = cff[cff.fontNames[0]].Encoding
            require(sha(raw) == group['embedded_cff']['cff_sha256'], 'embedded CFF edition')
            for row in group['embedded_cff']['encoding']:
                require(encoding[row['byte']] == row['glyph_name'], 'CFF glyph evidence')
            code = ord(char)
            # The three TeX zero aliases are separately checked on rendered pages.
            if code == 0 and encoding[0] == '.notdef':
                require(name in ('/PYRHTW+CMR10','/RWOQWQ+CMBX12','/GEQKXG+LINE10'), 'undeclared zero alias')
                code = 161
            glyph = encoding[code]
        else:
            raw = descriptor['/FontFile'].get_data()
            header = raw.split(b'currentfile eexec')[0].decode('latin1')
            encoding = {int(code):glyph for code,glyph in re.findall(r'dup (\d+) /([^\s]+) put',header)}
            base, cmap = get_encoding(font)
            require(base == 'charmap', 'adopted Type 1 byte encoding')
            candidates = [glyph for code,glyph in encoding.items() if cmap.get(chr(code),chr(code))==char]
            require(len(candidates)==1, 'unique Type 1 glyph for extracted character')
            glyph = candidates[0]
        require(GLYPHS[glyph] == group['visible_output'], 'visible glyph identity')
        verified.append(dict(document=key,font=name,input_codepoint=group['input_codepoint'],
                             glyph_name=glyph,output=GLYPHS[glyph],font_stream_sha256=sha(raw)))
    return verified


def extract(pdf, spec):
    require(sha(pdf.read_bytes())==spec['pdf_sha256'], 'bound PDF')
    reader=pypdf.PdfReader(pdf)
    texts,fonts,callbacks,pages=[],[],{},[]
    offset=0
    for number,page in enumerate(reader.pages,1):
        fragments=[]
        local_fonts=[]
        at=offset
        def visit(text, cm, tm, font, size):
            nonlocal at
            name=str(font.get('/BaseFont','')) if font else ''
            if text:
                callbacks[at]=dict(text=text,font=name,location=[number,round(tm[-2],1),round(tm[-1],1)])
            fragments.append(text)
            local_fonts.extend([name]*len(text))
            at+=len(text)
        text=page.extract_text(visitor_text=visit) or ''
        require(text==''.join(fragments) and len(text)==len(local_fonts), 'visitor alignment')
        pages.append(dict(page=number,start=offset,end=offset+len(text),sha256=sha(text.encode()),empty_extraction=not text))
        texts.append(text); fonts.extend(local_fonts+['']); offset+=len(text)+1
    raw='\n'.join(texts)
    require(pages==spec['page_bindings'] and len(pages)==spec['pages'] and
            sha(raw.encode())==spec['extraction_sha256'], 'full extraction and page bindings')
    return reader,raw,fonts[:-1],callbacks


def variants(key, spec, raw, fonts, callbacks, group_rows):
    spans=spec['included_spans']
    require(len(spans)==1 and spans[0]['start']==0 and spans[0]['end']==len(raw) and
            spans[0]['sha256']==sha(raw.encode()), 'complete input boundary')
    omit={}
    previous=0
    for f in spec['excluded_furniture']:
        a,b=f['start'],f['end']
        require(previous<=a<b<=len(raw) and raw[a:b]==f['literal'] and
                sha(raw[a:b].encode())==f['sha256'], 'exact furniture')
        page=spec['page_bindings'][f['page']-1]
        require(page['start']<=a<b<=page['end'], 'furniture on declared page')
        omit[a]=b; previous=b
    allowed={(g['font'],g['input_codepoint']):g for g in group_rows}
    substitutions={}
    observed=collections.Counter()
    for row in spec['glyph_substitutions']:
        at=row['offset']
        require(at not in substitutions and 0<=at<len(raw), 'unique glyph occurrence')
        require(ord(raw[at])==int(row['input_codepoint'][2:],16) and fonts[at]==row['input_font'], 'actual glyph/font')
        group=allowed[(row['input_font'],row['input_codepoint'])]
        require(len(row['output'])==1 and row['output']==group['visible_output'], 'no glyph deletion or rewording')
        page=spec['page_bindings'][row['page']-1]
        require(page['start']<=at<page['end'] and at-page['start']==row['page_offset'], 'glyph page and offset')
        a,b=row['context_start'],row['context_end']
        require(a<=at<b and sha(raw[a:b].encode())==row['context_sha256'], 'glyph occurrence context')
        if 'visitor_event_location' in row:
            event=callbacks.get(at)
            require(event and event['text']==raw[at] and event['font']==row['input_font'] and
                    event['location']==row['visitor_event_location'], 'whitespace glyph callback')
        if key=='F014' and raw[at] in (' ','\n'):
            require('visitor_event_location' in row, 'generated whitespace cannot be reinterpreted')
        substitutions[at]=row['output']
        observed[(row['input_font'],row['input_codepoint'])]+=1
    require(observed==collections.Counter({pair:g['count'] for pair,g in allowed.items()}), 'all glyph group occurrences')
    for at,c in enumerate(raw):
        if unicodedata.category(c) in ('Cc','Co') and c not in '\n\r\t' or c=='\ufffd':
            require(at in substitutions, 'unclassified nontext glyph')
        pair=(fonts[at],'U+%04X'%ord(c))
        if pair in allowed and c not in (' ','\n'):
            require(at in substitutions, 'omitted printable glyph alias')
    before,after=[],[]
    at=0
    while at<len(raw):
        if at in omit:
            before.append('\n'); after.append('\n'); at=omit[at]
        else:
            before.append(raw[at]); after.append(substitutions.get(at,raw[at])); at+=1
    return {'raw_untrimmed':raw,'raw_selected':''.join(before),'calibrated_selected':''.join(after)}


def check_complete_cff_inventory(reader, spec, raw, fonts):
    """Check also printable source glyphs absent from the proposed corrections."""
    encodings={}
    for page in reader.pages:
        for ref in page['/Resources']['/Font'].values():
            font=ref.get_object(); name=str(font.get('/BaseFont'))
            if name in encodings:
                continue
            cff=CFFFontSet()
            cff.decompile(io.BytesIO(font['/FontDescriptor']['/FontFile3'].get_data()),None)
            encodings[name]=cff[cff.fontNames[0]].Encoding
    corrections={r['offset']:r['output'] for r in spec['glyph_substitutions']}
    checked=0
    for i,(char,font) in enumerate(zip(raw,fonts)):
        if char.isspace() or not font or any(f['start']<=i<f['end'] for f in spec['excluded_furniture']):
            continue
        require(ord(char)<=255,'unexpected CFF extraction outside byte alphabet')
        name=encodings[font][ord(char)]
        if name=='.notdef' and char=='\0':
            name=encodings[font][161]
        unicode=GLYPHS.get(name) or agl.toUnicode(name)
        require(bool(unicode) and unicode==corrections.get(i,char), 'uncalibrated printable CFF glyph')
        checked+=1
    return dict(selected_nonwhitespace_occurrences=checked,unmapped_glyphs=0,additional_discrepancies=0)


def main():
    ap=argparse.ArgumentParser()
    for name in ('study-root','public-root','proposal','out'):
        ap.add_argument('--'+name,type=Path,required=True)
    args=ap.parse_args()
    require(not args.out.exists(), 'fresh output directory')
    args.out.mkdir(parents=True)
    require(pypdf.__version__=='6.13.0','pinned parser')
    proposal=args.proposal
    for row in read(proposal/'manifest.json')['exports']:
        data=(proposal/row['path']).read_bytes()
        require(sha(data)==row['sha256'] and len(data)==row['bytes'], 'frozen proposal export')
    sources=read(proposal/'source_input_spec.json')
    replacements=read(proposal/'replacement_input_spec.json')
    publication=read(proposal/'publication_binding.json')
    require(sha((args.public_root/publication['admission']['path']).read_bytes())==publication['admission']['sha256'], 'accepted proof edition')
    require(set(sources['sources'])=={'L088','N013','F014'} and
            set(replacements['ours'])=={'U_C','C1','C2','C3','C4','CODE'}, 'full document inventory')
    require(sources['missing_source_pdf']['L108']['pdf_cost'] is None,'unknown L108')
    scope=read(args.public_root/'papers/topic-c/v2/scope.json')
    require([r['id'] for r in scope['sources']]==['L088','N013','L108','F014'], 'accepted source scope')
    for source in scope['sources']:
        primary=source['primary']
        data=(args.study_root/primary['path']).read_bytes()
        require(sha(data)==primary['sha256'] and len(data)==primary['bytes'], 'accepted primary edition')
        if source['id']=='L108':
            browser=sources['missing_source_pdf']['L108']['available_representation']
            require(browser['path']==primary['path'] and browser['sha256']==primary['sha256'], 'browser bound but not counted')
        else:
            spec=sources['sources'][source['id']]
            require(spec['path']==primary['path'] and spec['pdf_sha256']==primary['sha256'], 'measured source matches proof source')
    evidence=read(proposal/'glyph_evidence.json')['groups']
    documents={};checked_fonts=[];cached={};cff_inventory=None
    for key,spec in (sources['sources']|replacements['ours']).items():
        pdf=(args.public_root/publication['scientific_documents'][key]['public_path'] if key in replacements['ours']
             else args.study_root/spec['path'])
        reader,raw,fonts,callbacks=extract(pdf,spec)
        groups=[g for g in evidence if g['document']==key]
        checked_fonts+=font_evidence(reader,key,groups)
        texts=variants(key,spec,raw,fonts,callbacks,groups)
        if key=='L088':
            cff_inventory=check_complete_cff_inventory(reader,spec,raw,fonts)
        cached[key]=(spec,raw,fonts,callbacks,groups)
        values={name:{form:count(text,form) for form in FORMS} for name,text in texts.items()}
        documents[key]=dict(pdf_sha256=spec['pdf_sha256'],pages=spec['pages'],calibrated_occurrences=len(spec['glyph_substitutions']),
                            variants=values,calibrated_minus_raw={form:{unit:values['calibrated_selected'][form][unit]-
                            values['raw_selected'][form][unit] for unit in UNITS} for form in FORMS})
    programs={}
    require(len(replacements['required_mathematical_programs'])==2, 'both complete required programs')
    for row in replacements['required_mathematical_programs']:
        raw=(args.public_root/row['public_path']).read_bytes()
        require(sha(raw)==row['sha256'] and len(raw)==row['bytes'], 'complete raw program edition')
        programs[Path(row['path']).name]=dict(sha256=sha(raw),bytes=len(raw),variants={f:count(raw.decode(),f) for f in FORMS})
    author=read(proposal/'author_counts.json')
    require(documents==author['documents'] and programs==author['raw_program_alternative'], 'independent full recount differs')
    controls=[]
    for mode in ('drop_page','drop_document_prefix','delete_glyph','change_glyph','wrong_font','wrong_context',
                 'omit_alias','wrong_whitespace_location','invent_whitespace','trim_nonfurniture'):
        key='F014' if 'whitespace' in mode else 'L088'
        spec,raw,fonts,callbacks,groups=cached[key]
        spec=copy.deepcopy(spec)
        if mode=='drop_page':spec['included_spans'][0]['end']-=100
        elif mode=='drop_document_prefix':spec['included_spans'][0]['start']=10
        elif mode=='delete_glyph':spec['glyph_substitutions'][0]['output']=''
        elif mode=='change_glyph':spec['glyph_substitutions'][0]['output']='?'
        elif mode=='wrong_font':spec['glyph_substitutions'][0]['input_font']='/wrong'
        elif mode=='wrong_context':spec['glyph_substitutions'][0]['context_sha256']='0'*64
        elif mode=='omit_alias':spec['glyph_substitutions'].pop()
        elif mode=='wrong_whitespace_location':next(r for r in spec['glyph_substitutions'] if 'visitor_event_location' in r)['visitor_event_location'][1]+=1
        elif mode=='invent_whitespace':next(r for r in spec['glyph_substitutions'] if 'visitor_event_location' in r).pop('visitor_event_location')
        else:spec['excluded_furniture'][0]['end']+=1
        try:variants(key,spec,raw,fonts,callbacks,groups)
        except (ValueError,KeyError):controls.append(dict(name=mode,rejected=True))
        else:raise ValueError('corruption accepted: '+mode)
    result=dict(status='PASS_INDEPENDENT_COMPLETE_INPUT_RECOUNT',proposal_manifest_sha256=sha((proposal/'manifest.json').read_bytes()),
                checker_sha256=sha(Path(__file__).read_bytes()),documents=documents,raw_program_alternative=programs,
                metric_cells=270,normalized_text_hashes=54,raw_program_metric_cells=20,embedded_font_groups=checked_fonts,
                complete_L088_printable_font_inventory=cff_inventory,
                negative_controls=controls,source_pdf_metrics_unknown={'L108':None},ratio=None,
                independent_code=True,shared_pdf_parser='pypdf 6.13.0',new_source_credit=0,new_question_credit=0)
    (args.out/'recount.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:result[k] for k in ('status','metric_cells','normalized_text_hashes','raw_program_metric_cells','ratio')}))


if __name__=='__main__':
    main()
