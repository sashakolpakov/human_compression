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
ALIASES={('CMEX10','parenleftbig'):'(',('CMEX10','parenrightbig'):')',('CMEX10','braceleftbig'):'{',('CMEX10','bracerightbig'):'}',('CMEX10','braceleftBigg'):'{',('CMEX10','bracelefttp'):'⎧',('CMEX10','braceleftbt'):'⎩',('CMEX10','braceleftmid'):'⎨',('CMEX10','braceex'):'⎪',('CMEX10','unionsqdisplay'):'⨆',('CMEX10','tildewide'):'˜',('CMEX7','tildewide'):'˜',('CMSY10','mapsto'):'∣',('CMSY10','G'):'𝒢'}

def document(study,key,row):
    path=study/row['path'];need(sha(path.read_bytes())==row['pdf_sha256'],'PDF binding '+key)
    reader=pypdf.PdfReader(path);texts=[];fontchars=[];pages=[];at=0;images=[];skips=0
    for pn,p in enumerate(reader.pages,1):
        pieces=[];fs=[]
        def visit(t,cm,tm,font,size):
            nonlocal skips
            
            pieces.append(t);fs.extend([str(font.get('/BaseFont','')) if font else '']*len(t))
        s=p.extract_text(visitor_text=visit) or '';need(s==''.join(pieces),'visitor duplicate exception exact')
        texts.append(s);fontchars.append(fs);pages.append(dict(page=pn,start=at,end=at+len(s),sha256=sha(s.encode()),empty_extraction=not s));at+=len(s)+1
        for image in p.images:images.append(dict(page=pn,name=image.name,width=image.image.width,height=image.image.height,sha256=sha(image.data)))
    need(skips==0,'no skipped visitor callback')
    raw='\n'.join(texts);need(pages==row['page_bindings'] and len(pages)==row['pages'],'all page hashes/bounds')
    need(sha(raw.encode())==row['extraction_sha256'],'full extraction')
    inc=row['included_spans'];need(len(inc)==1 and inc[0]['start']==0 and inc[0]['end']==len(raw) and inc[0]['sha256']==sha(raw.encode()),'entire document')
    cuts=collections.defaultdict(list)
    for c in row['excluded_furniture']:
        a,b=c['start'],c['end'];need(raw[a:b]==c['literal'] and sha(raw[a:b].encode())==c['sha256'],'furniture bytes');cuts[c['page']].append(c)
    need(set(cuts)==set(range(1,len(pages)+1)),'all and only page furniture')
    for pn,cs in cuts.items():
        p=pages[pn-1];s=texts[pn-1];need(len(cs)==1,'one furniture cut per page');f=cs[0]
        if key=='F010' and pn==1:
            i=s.rfind('\n1\n')+1
            need(i>0 and f['start']==i and f['end']==i+2 and f['literal']=='1\n','first-page numeral only')
            need('arXiv:2511.02410v2' in s[i+2:] and '16 Dec 2025' in s[i+2:],'identification banner retained')
        elif key=='F010':
            need(f['start']==p['start'] and f['end']==p['start']+s.index('\n')+1,'exact first-line header')
            need(str(pn) in f['literal'] and ('ANTONIO' in f['literal'] if pn%2==0 else 'FINITE GROUPS REPRESENTED BY FINITE INCIDENCE GEOMETRIES' in f['literal']),'running author/title line')
        else:
            need(f['end']==p['end'] and f['start']==p['end']-len(str(pn)) and f['literal']==str(pn),'only final page number')
    events={};audit={}
    if key=='F010':events,audit=inspect(path,texts,fontchars)
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
    if key=='F010':
        need(sum(raw[i]=='\t' for i in wanted)==3,'all three visible tab-coded braces calibrated')
        need(audit['visible_whitespace_characters']==3,'actual nonempty outlines for all tabs')
    return d,audit,images

def run(study,packet):
    need(pypdf.__version__=='6.13.0' and fontTools.__version__=='4.63.0','pinned parsers')
    manifest=read(packet/'manifest.json')
    for r in manifest['exports']:
        b=(packet/r['path']).read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'frozen export '+r['path'])
    src=read(packet/'source_input_spec.json');repl=read(packet/'replacement_input_spec.json');counts=read(packet/'author_counts.json');graphics=read(packet/'graphic_inventory.json')
    docs={};audits={};img={}
    for k,row in {**src['sources'],**repl['ours']}.items():
        docs[k],audits[k],img[k]=document(study,k,row)
        want=[{z:r[z] for z in ['page','name','width','height','sha256']} for r in graphics['documents'][k]['raster_images']];need(img[k]==want,'complete raster inventory '+k)
    need(docs==counts['documents'],'all120 independent metric cells/24 hashes')
    raw={}
    for key in ['complete_validation_programs','complete_operational_drivers','complete_formal_files']:
        raw[key]={}
        for r in repl[key]:
            b=(study/r['path']).read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'full rawfile')
            raw[key][pathlib.Path(r['path']).name]=dict(sha256=sha(b),bytes=len(b),role=r['role'],metrics={f:metrics(b.decode(),f) for f in ['NFC','NFKC']})
        need(raw[key]==counts[key],'independent whole-file cells '+key)
    report=dict(status='PASS_INDEPENDENT_COUNTS_PENDING_FONT_EVIDENCE_RECONCILIATION',packet_sha256=sha((packet/'manifest.json').read_bytes()),pdf_metric_cells=120,raw_metric_cells=60,documents=docs,raw_files=raw,font_audit=audits,images=img,factors=None,primary_text_exported=False)
    return report
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=pathlib.Path,required=True);ap.add_argument('--packet',type=pathlib.Path,required=True);ap.add_argument('--out',type=pathlib.Path,required=True);a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output');r=run(a.study_root,a.packet);a.out.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ['documents','raw_files','font_audit','images']}))
