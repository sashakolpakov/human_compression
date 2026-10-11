#!/usr/bin/env python3
"""Independent whole-page selection and state-machine counts; no author imports."""
from pathlib import Path
import argparse, hashlib, json, unicodedata
import pypdf

PIN='77ca6e548a9a87aae502697fa5a4ec91a3a68818c363f7bc3d879e84f639e259'
def sha(b): return hashlib.sha256(b).hexdigest()
def need(c,m):
    if not c: raise ValueError(m)
def read(p): return json.loads(p.read_text())
def measure(text,form):
    text=unicodedata.normalize(form,text)
    tokens=alnum=nonspace=0; in_token=in_alnum=False; out=[]; pending=False
    for ch in text:
        space=ch.isspace(); a=ch.isalnum()
        if a and not in_alnum: alnum+=1
        in_alnum=a
        if space:
            in_token=False
            if out: pending=True
        else:
            if not in_token: tokens+=1
            in_token=True; nonspace+=1
            if pending: out.append(' '); pending=False
            out.append(ch)
    collapsed=''.join(out)
    return dict(whitespace_tokens=tokens,alphanumeric_units=alnum,characters_without_whitespace=nonspace,
                characters_with_collapsed_whitespace=len(collapsed),utf8_bytes_with_collapsed_whitespace=len(collapsed.encode()),collapsed_text_sha256=sha(collapsed.encode()))
def binding(row,roots):
    p=Path(row['path']);need(not p.is_absolute() and '..' not in p.parts,'relative input path')
    f=roots[row['root']]/p;b=f.read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'binding '+str(f));return f,b
def changes(raw,ops):
    # Character mask/output insertions, independently of author's slice builder.
    mask=bytearray(len(raw)); insert={}
    for a,b,s in ops:
        need(0<=a<b<=len(raw) and not any(mask[a:b]),'disjoint full character ranges')
        mask[a:b]=b'\1'*(b-a);insert[a]=s
    out=[]
    for i,c in enumerate(raw):
        if i in insert:out.append(insert[i])
        if not mask[i]:out.append(c)
    return ''.join(out)
def selection(key,pages,spec):
    raw='\n'.join(pages);need(sha(raw.encode())==spec['extraction_sha256'],'literal extraction')
    page_rows=[];cut_rows=[];pos=0
    for n,t in enumerate(pages,1):
        page_rows.append(dict(page=n,start=pos,end=pos+len(t),sha256=sha(t.encode()),empty_extraction=not bool(t)))
        a=b=None
        if key=='L040' and n==1:
            pass
        elif key=='L040' and n>=3:
            j=n-1
            lit=(str(j)+' MARIA ELISA FERNANDES AND DIMITRI LEEMANS\n') if j%2==0 else ('C-GROUPS OF HIGH RANK FOR THE SYMMETRIC GROUPS '+str(j)+'\n')
            need(t.startswith(lit),'literal accepted-source running header');a,b=0,len(lit)
        else:
            number=1 if key=='L040' else n
            z=len(t)
            while z and t[z-1].isspace():z-=1
            a=z-len(str(number));b=len(t)
            need(t[a:z]==str(number) and (a==0 or t[a-1]=='\n'),'isolated physical page footer')
        if a is not None:
            cut_rows.append(dict(page=n,start=pos+a,end=pos+b,literal=t[a:b],sha256=sha(t[a:b].encode())))
        pos+=len(t)+1
    need(page_rows==spec['page_bindings'],'all physical pages and exact boundaries')
    need(cut_rows==spec['excluded_furniture'],'independently identified furniture only')
    need(spec['included_spans']==[dict(start=0,end=len(raw),sha256=sha(raw.encode()))],'complete source inclusion')
    ops=[(r['start'],r['end'],'\n') for r in cut_rows]
    raw_selected=changes(raw,ops);repairs=[]
    for r in spec['glyph_substitutions']:
        a,b=r['start'],r['end'];need(raw[a:b]==r['input'],'whole decoded glyph span')
        ev=r['pdf_events'];need(len(ev)==b-a and ev[0]['decoded_text']==r['input'],'one original glyph')
        same={k:v for k,v in ev[0].items() if k!='decoded_character_index'}
        for j,e in enumerate(ev):
            need(e['decoded_character_index']==j and {k:v for k,v in e.items() if k!='decoded_character_index'}==same,'single encoded event, consecutive decoded indices')
        need(len(r['output'])==1,'single observed output symbol')
        repairs.append((a,b,r['output']))
    full=dict(raw_untrimmed=raw,raw_selected=raw_selected,calibrated_selected=changes(raw,ops+repairs))
    article=None
    if key=='L040':
        offset=len(pages[0])+1
        need(spec['article_only_span']==dict(start=offset,end=len(raw),physical_pages=list(range(2,22)),sha256=sha(raw[offset:].encode())),'exact twenty-page article span')
        text='\n'.join(pages[1:]);need(text==raw[offset:],'direct article extraction')
        need(not any(a<offset for a,b,v in ops+repairs),'no cover discarded in calibrated primary')
        ao=[(a-offset,b-offset,v) for a,b,v in ops];ar=[(a-offset,b-offset,v) for a,b,v in repairs]
        article=dict(raw_untrimmed=text,raw_selected=changes(text,ao),calibrated_selected=changes(text,ao+ar))
    return full,article
def audit(packet,public,sources):
    need(sha((packet/'manifest.json').read_bytes())==PIN,'exact author freeze')
    m=read(packet/'manifest.json')
    for r in m['exports']:
        b=(packet/r['path']).read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'author export '+r['path'])
    roots=dict(packet=packet,public=public,sources=sources);p=read(packet/'policy.json');s=read(packet/'input_spec.json');expected=read(packet/'author_counts.json')
    docs={};rows=[];cells=hashes=0;article=None
    for key,r in s.items():
        path,_=binding(r,roots);pages=[pg.extract_text() or '' for pg in pypdf.PdfReader(path).pages]
        need(len(pages)==r['pages'],'complete page count')
        ts,article_text=selection(key,pages,r);met={v:{n:measure(t,n) for n in ('NFC','NFKC')} for v,t in ts.items()}
        need(met==expected['documents'][key]['metrics'],'independent document metrics '+key)
        docs[key]=dict(pdf_sha256=r['sha256'],pages=len(pages),metrics=met)
        rows.append(dict(document=key,all_pages=True,whole_frontmatter_references_preserved=True,furniture_cuts=len(r['excluded_furniture']),glyph_spans=len(r['glyph_substitutions'])))
        cells+=30;hashes+=6
        if article_text is not None:
            article={v:{n:measure(t,n) for n in ('NFC','NFKC')} for v,t in article_text.items()}
            need(article==expected['source_article_only']['metrics'],'independent direct article-only counts')
            cells+=30;hashes+=6
    raw={}
    for cat,rs in [('programs',p['programs']),('drivers',p['drivers']),('formal',p['formal'])]:
        raw[cat]={}
        for r in rs:
            _,b=binding(r,roots);met={n:measure(b.decode(),n) for n in ('NFC','NFKC')}
            need(met==expected['raw_files'][cat][r['path']]['metrics'],'independent whole file metrics')
            raw[cat][r['path']]=dict(bytes=len(b),sha256=sha(b),metrics=met);cells+=10;hashes+=2
    # Existing complete bundle and scientific documents are input bindings, not re-proofs.
    bound=[]
    for cat in ('scientific_bindings','retained_numerical_inputs'):
        for r in p[cat]:binding(r,roots);bound.append(dict(category=cat,**r))
    binding(p['retained_old_common'],roots);bound.append(dict(category='retained_old_common',**p['retained_old_common']))
    return dict(status='PASS',role='Independent selection and arithmetic; accepted calibration meanings and actual-font audit reviewed separately',author_manifest_sha256=PIN,pdf_metric_cells=120,source_article_only_cells=30,raw_metric_cells=70,total_cells=cells,text_hashes=hashes,pages=49,documents=docs,source_article_only=article,raw_files=raw,selection_review=rows,retained_bindings=bound,scientific_programs_executed=False,ratio=None)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists(),'fresh report');r=audit(a.packet,a.public_root,a.sources_root);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print('PASS',r['total_cells'],'cells',r['text_hashes'],'hashes')
if __name__=='__main__':main()
