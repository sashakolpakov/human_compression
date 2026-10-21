#!/usr/bin/env python3
"""Independent document selection and character-state recount, no author imports."""
import argparse, collections, hashlib, json, pathlib, unicodedata, copy
import pypdf, fontTools
from fontTools import agl
from font_events import inspect

def sha(b):return hashlib.sha256(b).hexdigest()
def need(b,s):
    if not b:raise ValueError(s)
def read(p):return json.loads(p.read_text())
def metrics(s,form):
    s=unicodedata.normalize(form,s);words=alpha=nonspace=0;w=a=False;out=[];pending=False
    for c in s:
        cw=not c.isspace();ca=c.isalnum()
        words+=int(cw and not w);alpha+=int(ca and not a);w,a=cw,ca;nonspace+=cw
        if cw:
            if pending:out.append(' ')
            out.append(c);pending=False
        elif out:pending=True
    t=''.join(out)
    return dict(whitespace_tokens=words,alphanumeric_units=alpha,characters_without_whitespace=nonspace,characters_with_collapsed_whitespace=len(t),utf8_bytes_with_collapsed_whitespace=len(t.encode()),collapsed_text_sha256=sha(t.encode()))
def variants(raw,before,after):return {k:{f:metrics(s,f) for f in ['NFC','NFKC']} for k,s in [('raw_untrimmed',raw),('raw_selected',before),('calibrated_selected',after)]}
def selection(s,row):
    parts=[];at=0
    for f in row['excluded_furniture']:parts.append(s[at:f['start']]);at=f['end']
    parts.append(s[at:]);return '\n'.join(parts)
ALIASES={('LMMathExtension10-Regular','bracelefttp'):'⎧',('LMMathExtension10-Regular','braceleftbt'):'⎩',('LMMathExtension10-Regular','braceleftmid'):'⎨',('LMMathExtension10-Regular','braceex'):'⎪',('MSBM10','F'):'𝔽',('MSBM10','Z'):'ℤ',('LASY10','a50'):'□',('LINE10','a34'):'╱',('LINE10','a98'):'╲',('LCIRCLE10','a116'):'●'}
ALIASES.update({('LMMathSymbols10-Regular',x):y for x,y in dict(D='𝒟',L='ℒ',P='𝒫',Q='𝒬',T='𝒯').items()})
ALIASES.update({('CMSY10',x):y for x,y in dict(A='𝒜',B='ℬ',F='ℱ',H='ℋ',L='ℒ',P='𝒫',S='𝒮').items()})

def document(study,key,row):
    path=study/row['path'];need(sha(path.read_bytes())==row['pdf_sha256'],'PDF binding '+key)
    reader=pypdf.PdfReader(path);texts=[];fontchars=[];pages=[];at=0;images=[];skips=0
    for pn,p in enumerate(reader.pages,1):
        pieces=[];fs=[]
        def visit(t,cm,tm,font,size):
            nonlocal skips
            if key=='L009' and pn==1 and font is None and t=='ALGEBRAIC\n COMBINATORICS':skips+=1;return
            pieces.append(t);fs.extend([str(font.get('/BaseFont','')) if font else '']*len(t))
        s=p.extract_text(visitor_text=visit) or '';need(s==''.join(pieces),'visitor duplicate exception exact')
        texts.append(s);fontchars.append(fs);pages.append(dict(page=pn,start=at,end=at+len(s),sha256=sha(s.encode()),empty_extraction=not s));at+=len(s)+1
        for image in p.images:images.append(dict(page=pn,name=image.name,width=image.image.width,height=image.image.height,sha256=sha(image.data)))
    need(skips==(1 if key=='L009' else 0),'exact duplicate Form count')
    raw='\n'.join(texts);need(pages==row['page_bindings'] and len(pages)==row['pages'],'all page hashes/bounds')
    need(sha(raw.encode())==row['extraction_sha256'],'full extraction')
    inc=row['included_spans'];need(len(inc)==1 and inc[0]['start']==0 and inc[0]['end']==len(raw) and inc[0]['sha256']==sha(raw.encode()),'entire document')
    cuts=collections.defaultdict(list)
    for c in row['excluded_furniture']:
        a,b=c['start'],c['end'];need(raw[a:b]==c['literal'] and sha(raw[a:b].encode())==c['sha256'],'furniture bytes');cuts[c['page']].append(c)
    expected=set(range(3,26)) if key=='L009' else set(range(2,15)) if key=='L092' else set(range(1,len(pages)+1))
    need(set(cuts)==expected,'only repeated pages')
    for pn,cs in cuts.items():
        p=pages[pn-1];s=texts[pn-1]
        if key=='L009':
            need(len(cs)==2,'both source header/footer');h,f=cs
            need(h['start']==p['start'] and h['end']==p['start']+s.index('\n')+1,'only first-line header')
            need(('Remi Delaby' in h['literal'] if pn%2 else 'Geometries with trialities arising from linear spaces' in h['literal']),'actual running title')
            need(f['end']==p['end'] and f['literal'].startswith('Algebraic Combinatorics , Vol. 9 #2 (2026) ') and f['literal'].endswith(str(pn+377)),'only journal footer')
        elif key=='L092':
            need(len(cs)==1,'one header');h=cs[0]
            need(h['start']==p['start'] and h['end']==p['start']+s.index('\n')+1 and 'D. Leemans: A Generalization of a Construction due to Van Nypelseer' in h['literal'] and str(pn+560) in h['literal'],'only source running line')
        else:
            need(len(cs)==1,'one page number');f=cs[0]
            need(f['end']==p['end'] and f['start']==p['end']-len(str(pn)) and f['literal']==str(pn),'only final page number')
    events={};audit={}
    if key in ('L009','L092'):events,audit=inspect(path,texts,fontchars)
    if key=='L009':
        changed={429:{0,1},433:{0,1,3,22},434:{0,1,3}}
        audit['cache_repair_occurrences']=[]
        for i,e in events.items():
            ev=e['event'];obj=e['font_dictionary']
            if ev['encoded_byte'] in changed.get(obj[0],set()):
                audit['cache_repair_occurrences'].append(dict(source=key,offset=i,page=ev['page'],font=ev['font'],encoded_byte=ev['encoded_byte'],decoded_text=ev['decoded_text'],old_glyph='.notdef',new_glyph=ev['glyph_name'],font_dictionary_object=dict(idnum=obj[0],generation=obj[1]),effective_encoding_sha256=e['effective_encoding_sha256']))
    wanted={i:ALIASES[(e['event']['font'].split('+')[-1],e['event']['glyph_name'])] for i,e in events.items() if (e['event']['font'].split('+')[-1],e['event']['glyph_name']) in ALIASES}
    subs=row['glyph_substitutions'];need(len(subs)==len(wanted) and {r['offset'] for r in subs}==set(wanted),'all actual alias occurrences, no extra replacements')
    result=list(raw)
    for r in subs:
        i=r['offset'];ev=events[i]['event'];need(r['output']==wanted[i] and len(r['output'])==1,'actual visible alias')
        need(r['input_codepoint']==f'U+{ord(raw[i]):04X}' and r['input_font']==ev['font'],'source glyph/font')
        need(all(r['pdf_event'][k]==v for k,v in ev.items()),'full literal PDF event')
        if 'font_dictionary_object' in r['pdf_event']:
            obj=r['pdf_event']['font_dictionary_object'];need([obj['idnum'],obj['generation']]==events[i]['font_dictionary'],'actual font dictionary')
            need(all(r['pdf_event'][k]==events[i][k] for k in ['effective_encoding_sha256','font_dictionary_sha256']),'actual font dictionary/encoding hashes')
        p=pages[r['page']-1];need(p['start']<=i<p['end'] and p['start']+r['page_offset']==i,'glyph physical locator')
        need(sha(raw[r['context_start']:r['context_end']].encode())==r['context_sha256'],'glyph context');result[i]=r['output']
    calibrated=''.join(result);need(not any(c=='\ufffd' or unicodedata.category(c)=='Co' or unicodedata.category(c)=='Cc' and c not in '\n\r\t' for c in calibrated),'all unresolved characters')
    before=selection(raw,row);after=selection(calibrated,row)
    d=dict(pdf_sha256=row['pdf_sha256'],pages=len(pages),calibrations=len(subs),furniture_occurrences=len(row['excluded_furniture']),variants=variants(raw,before,after))
    sensitivity=None
    if key=='L009':
        end=pages[0]['end'];sensitivity=dict(physical_page=1,in_primary_coordinate=True,role='publisher identification cover, distinct from the 24 article pages',metrics={f:metrics(texts[0],f) for f in ['NFC','NFKC']},article_only=variants(raw[end:],before[end:],after[end:]),raster_logo_lettering_cost=None,no_factor=True)
    return d,audit,images,sensitivity

def run(study,packet):
    need(pypdf.__version__=='6.13.0' and fontTools.__version__=='4.63.0','pinned parsers')
    manifest=read(packet/'manifest.json')
    for r in manifest['exports']:
        b=(packet/r['path']).read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'frozen export '+r['path'])
    src=read(packet/'source_input_spec.json');repl=read(packet/'replacement_input_spec.json');counts=read(packet/'author_counts.json');graphics=read(packet/'graphic_inventory.json')
    docs={};audits={};img={}
    for k,row in {**src['sources'],**repl['ours']}.items():
        docs[k],audits[k],img[k],sensitivity=document(study,k,row)
        want=[{z:r[z] for z in ['page','name','width','height','sha256']} for r in graphics['raster_objects'][k]];need(img[k]==want,'complete raster inventory '+k)
        if sensitivity:need(sensitivity==counts['identification_cover_sensitivity'],'cover/article variants')
    need(docs==counts['documents'],'all180 independent metric cells/36 hashes')
    raw={}
    for key in ['complete_programs','complete_operational_drivers','complete_formal_files']:
        raw[key]={}
        for r in repl[key]:
            b=(study/r['path']).read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'full rawfile')
            raw[key][pathlib.Path(r['path']).name]=dict(sha256=sha(b),bytes=len(b),role=r['role'],metrics={f:metrics(b.decode(),f) for f in ['NFC','NFKC']})
        need(raw[key]==counts[key],'independent whole-file cells '+key)
    report=dict(status='PASS_INDEPENDENT_COUNTS_PENDING_FONT_EVIDENCE_RECONCILIATION',packet_sha256=sha((packet/'manifest.json').read_bytes()),pdf_metric_cells=180,raw_metric_cells=220,documents=docs,raw_files=raw,font_audit=audits,images=img,factors=None,primary_text_exported=False)
    return report
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=pathlib.Path,required=True);ap.add_argument('--packet',type=pathlib.Path,required=True);ap.add_argument('--out',type=pathlib.Path,required=True);a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output');r=run(a.study_root,a.packet);a.out.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ['documents','raw_files','font_audit','images']}))
