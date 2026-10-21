#!/usr/bin/env python3
"""Independent input review: no author extractor, calibration or metric imports."""
import argparse, collections, hashlib, io, json, pathlib, unicodedata
import pypdf
import fontTools
from pypdf.generic import ContentStream, TextStringObject, ByteStringObject
from pypdf import _cmap
from fontTools import t1Lib, agl
from fontTools.cffLib import CFFFontSet

PIN='0dfc2fce16d8c532a1cdd9b8f61c1d9391c15099091e795cbba56bde30501620'
def digest(b): return hashlib.sha256(b).hexdigest()
def require(b,s):
    if not b: raise ValueError(s)
def read(p): return json.loads(p.read_text())
def metrics(text,form):
    text=unicodedata.normalize(form,text); words=0; alpha=0; w=False; a=False; out=[]; pending=False
    for c in text:
        cw=not c.isspace(); ca=c.isalnum()
        if cw and not w: words+=1
        if ca and not a: alpha+=1
        w,a=cw,ca
        if not cw:
            if out: pending=True
        else:
            if pending: out.append(' ')
            out.append(c);pending=False
    clean=''.join(out)
    return dict(whitespace_tokens=words,alphanumeric_units=alpha,characters_without_whitespace=sum(not c.isspace() for c in text),characters_with_collapsed_whitespace=len(clean),utf8_bytes_with_collapsed_whitespace=len(clean.encode()),collapsed_text_sha256=digest(clean.encode()))

# Values classified by reading the actual source pages and embedded glyph outlines.
ALIAS={('CMSY10','P'):'𝒫',('MSBM10','Z'):'ℤ',('MSBM10','N'):'ℕ',('MSBM10','F'):'𝔽',
 ('CMEX10','bracketlefttp'):'⎡',('CMEX10','bracketleftex'):'⎢',('CMEX10','bracketleftbt'):'⎣',
 ('CMEX10','bracketrighttp'):'⎤',('CMEX10','bracketrightex'):'⎥',('CMEX10','bracketrightbt'):'⎦',('MSAM10','triangleleft'):'⊲'}
# Non-AGL/variant names whose extraction was visually checked, without substituting it.
NAMES={'multicloseright':'⋊','negationslash':'̸','mapsto':'↦','floorleft':'⌊','floorright':'⌋','angbracketleft':'⟨','angbracketright':'⟩','parenleftbig':'(','parenrightbig':')','bracketleftBigg':'[','bracketrightBigg':']','bracketleftBig':'[','bracketrightBig':']','braceleftBigg':'{','summationtext':'∑','producttext':'∏','summationdisplay':'∑','productdisplay':'∏','prime':'′','square':'□','triangleleftequal':'⊴'}

def face(font):
    name=str(font['/BaseFont']);d=font.get('/FontDescriptor')
    if d is None:
        require(name=='/Times-Roman','undeclared unembedded font');return None,{32:'space'}
    d=d.get_object();ref=d.get('/FontFile') or d.get('/FontFile3');data=ref.get_object().get_data()
    if '/FontFile' in d:
        f=t1Lib.T1Font.__new__(t1Lib.T1Font);f.data=data;f.encoding='ascii';f.parse();enc=f.font['Encoding']
    else:
        f=CFFFontSet();f.decompile(io.BytesIO(data),None);enc=f[f.fontNames[0]].Encoding
    enc=dict(enumerate(enc));over=font.get('/Encoding')
    if over and not isinstance(over,str):
        for v in over.get('/Differences',[]):
            if isinstance(v,int): at=v
            else: enc[at]=str(v)[1:];at+=1
    return digest(data),enc

def events(reader, texts, fontchars):
    faces={};classes=collections.Counter();byoffset={};space=0;absolute=0
    for pn,(page,text,seenfonts) in enumerate(zip(reader.pages,texts,fontchars),1):
        require(not page['/Resources'].get('/XObject'),'unvisited XObject');tokens=[];current=None;stack=[]
        for oi,(args,op) in enumerate(ContentStream(page.get_contents(),reader).operations):
            if op==b'q':stack.append(current)
            elif op==b'Q':current=stack.pop()
            elif op==b'Tf':current=(str(args[0]),page['/Resources']['/Font'][args[0]].get_object())
            if op not in [b'TJ',b'Tj',b"'",b'"']:continue
            resource,font=current;name=str(font['/BaseFont']);require(font['/Subtype']=='/Type1','source font type')
            if name not in faces:faces[name]=face(font)
            stream,mapping=faces[name];enc,cm=_cmap.get_encoding(font)
            parts=args[0] if op==b'TJ' else [args[-1]]
            for pi,part in enumerate(parts):
                if not isinstance(part,(TextStringObject,ByteStringObject)):continue
                raw=part.original_bytes
                for bi,b in enumerate(raw):
                    c=enc.get(b,chr(b)) if isinstance(enc,dict) else bytes([b]).decode(enc)
                    c=''.join(cm.get(k,k) for k in c);require(len(c)==1,'multi-character glyph')
                    gn=mapping.get(b,'standard_'+c if stream is None else '')
                    require(gn,'empty embedded name');classes[name,b,c,gn,stream]+=1
                    ev=dict(page=pn,operator_index=oi,operator=op.decode(),part_index=pi,byte_index=bi,encoded_byte=b,font_resource=resource,font=name,text_part_sha256=digest(raw),decoded_codepoint=f'U+{ord(c):04X}',glyph_name=gn,font_stream_sha256=stream)
                    if c.isspace():
                        require(pn==1 and name=='/Times-Roman' and b==32 and gn=='space','unreviewed true space');space+=1
                    else:tokens.append((c,name,ev))
        positions=[i for i,c in enumerate(text) if not c.isspace()]
        require(len(tokens)==len(positions),'byte/text length')
        for i,(c,name,ev) in zip(positions,tokens):
            require(text[i]==c and seenfonts[i]==name,'byte/text/font alignment');byoffset[absolute+i]=ev
        absolute+=len(text)+1
    require(space==6,'banner spaces')
    audit=[]
    for (name,b,c,gn,stream),n in sorted(classes.items()):
        family=name.split('+')[-1];alias=ALIAS.get((family,gn))
        if alias is None:
            expected=NAMES.get(gn,agl.toUnicode(gn) or (c if stream is None else None))
            require(c==expected,f'Unclassified glyph {name} {b} {gn}: {c!r} vs {expected!r}')
        audit.append(dict(font=name,encoded_byte=b,decoded_codepoint=f'U+{ord(c):04X}',glyph_name=gn,occurrences=n,font_stream_sha256=stream))
    return byoffset,audit,faces

def selection(text,row):
    chunks=[];pos=0
    for cut in row['excluded_furniture']:
        chunks.append(text[pos:cut['start']]);pos=cut['end']
    chunks.append(text[pos:]);return '\n'.join(chunks)

def document(study,key,row,fontaudit,graphics):
    p=study/row['path'];require(digest(p.read_bytes())==row['pdf_sha256'],'PDF binding')
    reader=pypdf.PdfReader(p);texts=[];fonts=[];pages=[];at=0;imgs=[]
    for no,page in enumerate(reader.pages,1):
        chunks=[];fs=[]
        def visit(t,cm,tm,font,size):
            chunks.append(t);fs.extend([str(font.get('/BaseFont','')) if font else '']*len(t))
        s=page.extract_text(visitor_text=visit) or '';require(s==''.join(chunks),'visitor/extraction agreement')
        texts.append(s);fonts.append(fs);pages.append(dict(page=no,start=at,end=at+len(s),sha256=digest(s.encode()),empty_extraction=not s));at+=len(s)+1
        for im in page.images:imgs.append((no,im.name,im.image.width,im.image.height,digest(im.data)))
    require(imgs==[(x['page'],x['name'],x['width'],x['height'],x['sha256']) for x in graphics['documents'][key]],'full image inventory')
    require(all(x[2:4]==(1,1) for x in imgs),'unclassified raster text')
    raw='\n'.join(texts);require(len(texts)==row['pages'] and pages==row['page_bindings'],'page bindings')
    require(digest(raw.encode())==row['extraction_sha256'],'extraction binding')
    require(len(row['included_spans'])==1,'full document inclusion');inc=row['included_spans'][0]
    require(inc['start']==0 and inc['end']==len(raw) and inc['sha256']==digest(raw.encode()),'all text retained')
    require(len(row['excluded_furniture'])==len(pages),'one furniture cut/page')
    for n,(pb,cut) in enumerate(zip(pages,row['excluded_furniture']),1):
        s=texts[n-1];a,b=cut['start'],cut['end'];require(cut['page']==n and raw[a:b]==cut['literal'] and digest(raw[a:b].encode())==cut['sha256'],'furniture binding')
        if key=='L014' and n>1:
            expected=s[:s.index('\n')+1];require(a==pb['start'] and b==a+len(expected),'source prefix furniture only')
            require(('STRING C-GROUPS OF ORDER 4 pm' in expected if n%2 else 'DONG-DONG HOU, YAN-QUAN FENG' in expected),'actual running header')
        else: require(a==pb['end']-len(str(n)) and b==pb['end'] and raw[a:b]==str(n),'only trailing page number')
    ev={};classes=[]
    if key=='L014':
        ev,classes,faces=events(reader,texts,fonts)
        original=fontaudit['L014']['encoded_glyph_classes']
        require(classes==[{k:r[k] for k in classes[0]} for r in original],'all encoded glyph classes')
        require(len(classes)==595 and len(ev)==25574 and len(faces)==22,'font census')
    wanted={i:ALIAS[(e['font'].split('+')[-1],e['glyph_name'])] for i,e in ev.items() if (e['font'].split('+')[-1],e['glyph_name']) in ALIAS}
    changes=row['glyph_substitutions'];require(len(changes)==len(wanted) and {r['offset'] for r in changes}==set(wanted),'exact alias occurrence inventory')
    calibrated=list(raw)
    for r in changes:
        i=r['offset'];require(r['pdf_event']==ev[i] and r['output']==wanted[i] and r['input_font']==ev[i]['font'],'visible glyph and actual event')
        require(r['input_codepoint']==f'U+{ord(raw[i]):04X}','input character')
        require(digest(raw[r['context_start']:r['context_end']].encode())==r['context_sha256'],'glyph context')
        pb=pages[r['page']-1];require(pb['start']+r['page_offset']==i and pb['start']<=i<pb['end'],'physical glyph locator');calibrated[i]=r['output']
    calibrated=''.join(calibrated)
    require(not any(unicodedata.category(c)=='Co' or c=='\ufffd' or unicodedata.category(c)=='Cc' and c not in '\n\r\t' for c in calibrated),'unresolved glyph')
    return dict(pdf_sha256=row['pdf_sha256'],pages=len(texts),calibrations=len(changes),furniture_occurrences=len(pages),variants={k:{f:metrics(v,f) for f in ['NFC','NFKC']} for k,v in [('raw_untrimmed',raw),('raw_selected',selection(raw,row)),('calibrated_selected',selection(calibrated,row))]}),dict(images=len(imgs),classes=len(classes),aligned_nonspace=len(ev)),calibrated

def boundary(replacement):
    expected=[('complete_validation_programs',{'phase236_models.py','phase236_finite_check.g','phase248_presentation_check.g'}),('complete_operational_drivers',{'phase236_check.py','phase248_check.py'}),('complete_formal_files',{'OddKernelIntersection.lean'})]
    for k,names in expected: require({pathlib.Path(r['path']).name for r in replacement[k]}==names and len(replacement[k])==len(names),'complete raw inventory '+k)
    require(all(r['classification']=='validation' and r['uniform_written_proof_premise'] is False for r in replacement['complete_validation_programs']),'validation/proof distinction')
    require(replacement['retained_external_cost'] is None and replacement['graphics_cost'] is None,'unknown costs')

def run(study,packet):
    require(pypdf.__version__=='6.13.0' and fontTools.__version__=='4.63.0','declared parser versions')
    man=read(packet/'manifest.json');require(digest((packet/'manifest.json').read_bytes())==PIN,'manifest pin')
    for row in man['exports']:
        b=(packet/row['path']).read_bytes();require(len(b)==row['bytes'] and digest(b)==row['sha256'],'export '+row['path'])
    for row in man['immutable_inputs']:
        b=(study/row['path']).read_bytes();require(len(b)==row['bytes'] and digest(b)==row['sha256'],'immutable input '+row['path'])
    source=read(packet/'source_input_spec.json');replacement=read(packet/'replacement_input_spec.json');counts=read(packet/'author_counts.json');fa=read(packet/'font_audit.json');graphics=read(packet/'graphic_inventory.json')
    scope=read(study/'topic_F_volume/scope.json');sb=read(packet/'source_contract_boundary.json');policy=read(packet/'policy.json')
    require(sb['source_rows']==scope['contracts'] and sb['row_count']==25 and sb['proof_spans']==scope['proof_spans'],'unchanged accepted source/proof scope')
    require(sb['retained_remote_primary']==scope['retained_remote_primary'] and policy['retained_CP']['full_text_cost'] is None and sb['missing_CP_fulltext_cost'] is None,'retained CP input and unknown cost')
    require(graphics['graphic_cost'] is None and graphics['raster_text_cost'] is None and source['historical_program_cost'] is None,'unmeasured graphics and old programs')
    boundary(replacement);docs={};inventories={}
    for key,row in {**source['sources'],**replacement['ours']}.items():
        docs[key],inventories[key],_=document(study,key,row,fa,graphics)
    require(docs==counts['documents'],'all independent PDF coordinates/hash records')
    raw={}
    for k in ['complete_validation_programs','complete_operational_drivers','complete_formal_files']:
        raw[k]={}
        for row in replacement[k]:
            b=(study/row['path']).read_bytes();require(digest(b)==row['sha256'] and len(b)==row['bytes'],'raw file binding')
            r=dict(sha256=digest(b),bytes=len(b),role=row['role'],metrics={f:metrics(b.decode(),f) for f in ['NFC','NFKC']});raw[k][pathlib.Path(row['path']).name]=r
        require(raw[k]==counts[k],'raw independent coordinates '+k)
    tex=(study/replacement['appendix_tex']['path']).read_text();need=[pathlib.Path(r['path']).name for r in replacement['complete_validation_programs']]
    require(tex.count('\\VerbatimInput')==3 and 'firstline' not in tex and 'lastline' not in tex,'complete appendix inputs')
    require(all('{programs/'+n+'}' in tex for n in need),'all three full programs printed')
    require(counts['ratios'] is None and counts['new_source_credit']==0 and counts['new_question_credit']==0,'input only')
    return dict(status='PASS_INDEPENDENT_INPUT_RECOUNT',author_manifest_sha256=PIN,pdf_metric_cells=120,pdf_hashes=24,raw_program_metric_cells=30,raw_driver_metric_cells=20,raw_formal_metric_cells=10,raw_hashes=12,documents=docs,raw_files=raw,inventories=inventories,factors=None,primary_text_exported=False)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=pathlib.Path,required=True);ap.add_argument('--packet',type=pathlib.Path);ap.add_argument('--out',type=pathlib.Path,required=True);a=ap.parse_args();p=a.packet or a.study_root/'topic_F_measurement_inputs'
    require(not a.out.exists(),'fresh output');r=run(a.study_root,p);a.out.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ['documents','raw_files','inventories']}))
