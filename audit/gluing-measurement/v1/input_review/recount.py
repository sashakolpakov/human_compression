#!/usr/bin/env python3
"""Independent whole-page selection and state-machine counts; no author imports."""
from pathlib import Path
import argparse, hashlib, json, unicodedata
import pypdf

PIN='7f7cc0dc06b772ca150535d53d0a4d20799255da6e447dffa8e88a25f32d5306'
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
        if key=='L010' and n>=2:
            lit=(str(n)+' DIMITRI LEEMANS AND JESSICA MULPAS\n') if n%2==0 else ('GLUING METHODS FOR STRING C-GROUPS '+str(n)+'\n')
            need(t.startswith(lit),'literal source running header');a,b=0,len(lit)
        else:
            number=n;z=len(t)
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
        need(key=='L010','only source aliases calibrated')
        allowed={55:('mapsto','↦','⊢'),66:('B','B','ℬ'),67:('C','C','𝒞'),71:('G','G','𝒢'),72:('H','H','ℋ'),79:('O','O','𝒪')}
        e=ev[0];need((e['glyph_name'],r['input'],r['output'])==allowed[e['encoded_byte']],'reviewed literal glyph class')
        need(e['font_identity']=='effc9f182edef25b04bc3dfcad785cd8bf95ac7b573d5613d56a951da3d8ba6c','actual font dictionary identity')
        need(e['font_dictionary_sha256']=='42cb19573dc5ca37e1f0c8793d8fd8ab1056fb2d634e4f8357448bea0ed51b02','font dictionary bytes')
        need(e['effective_encoding_sha256']=='a4e8992adf2497c66d7410796affb36443c6791b05336be4a700b00254392efb','effective encoding')
        need(e['font_stream_sha256']=='9e909caca89de137ec6f60954d194e36d3e6782bd7568367dca54ed2bb8c31cf','embedded stream')
        need(sha(raw[r['context_start']:r['context_end']].encode())==r['context_sha256'],'literal glyph context')
        need(len(r['output'])==1,'single observed output symbol')
        repairs.append((a,b,r['output']))
    full=dict(raw_untrimmed=raw,raw_selected=raw_selected,calibrated_selected=changes(raw,ops+repairs))
    return full,None

def boundary(p):
    need(set(p['replacements'])=={'U1','U2','A1','CODE'},'both complete common papers, application and code')
    need([p['source']['pages']]+[p['replacements'][k]['pages'] for k in ('U1','U2','A1','CODE')]==[15,5,6,5,4],'whole PDF page boundary')
    need(p['source_id']=='L010' and p['source_rows']==23 and p['original_manuscripts']==1,'one fixed accepted contract')
    need(len(p['programs'])==3 and len(p['drivers'])==3 and len(p['formal'])==2,'complete eight raw files')
    need(all(x['role']=='finite_validation' and x['uniform_mathematical_premise'] is False for x in p['programs']),'diagnostics are not uniform premises')
    need(p['principal_required_programs']==0 and p['validation_programs']==3,'exact code roles')
    for key in ('whole_common_papers_charged','existing_B_common_is_not_a_prerequisite','all_declared_code_prepurchased_for_conditional_results','raw_and_printed_code_are_alternatives'):
        need(p[key] is True,key)
    need(p['cross_topic_discount'] is False and p['partial_formal_declarations']==10 and p['whole_source_formalized'] is False,'no unpaid umbrella or inflated formal scope')
    need(p['unknown_costs']==dict(full_graphics=None,historical_software=None,retained_external_proofs=None,full_formalization=None),'unknown costs stay null')
    need(p['factors_permitted'] is False and p['ratio'] is None and p['new_scientific_credit']==0,'inputs only')
def code_inclusion(packet,policy,roots):
    # In this fixed appendix the actual program text uses Type0 Menlo. The
    # three Type1 classes are solely printed wrap signs, inspected separately.
    # This representation check has no effect on any measured coordinate.
    parts=[]
    for n,page in enumerate(pypdf.PdfReader(packet/'programs.pdf').pages,1):
        pieces=[]
        def visitor(text,cm,tm,font,size):
            if font and font.get('/Subtype')=='/Type0':pieces.append(text)
        page.extract_text(visitor_text=visitor);text=''.join(pieces).rstrip()
        need(text.endswith('\n'+str(n)),'code isolated footer')
        parts.append(text[:-(len(str(n))+1)])
    packed=''.join(ch for ch in ''.join(parts) if not ch.isspace())
    tex=(packet/'programs.tex').read_text();names=[]
    for row in policy['programs']:
        _,raw=binding(row,roots);need((packet/row['printed_path']).read_bytes()==raw,'whole printed code copy')
        need(''.join(ch for ch in raw.decode() if not ch.isspace()) in packed,'entire literal program in PDF')
        need(tex.count('{'+row['printed_path']+'}')==1,'each complete verbatim input once')
        names.append(row['path'])
    need(tex.count('\\VerbatimInput')==3 and not any(s in tex for s in ('firstline','lastline','firstnumber','linerange')),'no code slicing')
    return dict(full_files=names,whole_verbatim_bytes=True,complete_PDF_program_text=True,wrap_signs_ignored_only_for_inclusion=True)
def audit(packet,public,sources):
    need(sha((packet/'manifest.json').read_bytes())==PIN,'exact author freeze')
    m=read(packet/'manifest.json')
    for r in m['exports']:
        b=(packet/r['path']).read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'author export '+r['path'])
    roots=dict(packet=packet,public=public,sources=sources);p=read(packet/'policy.json');s=read(packet/'input_spec.json');expected=read(packet/'author_counts.json')
    boundary(p)
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
    for cat in ('scientific_bindings',):
        for r in p[cat]:binding(r,roots);bound.append(dict(category=cat,**r))
    return dict(status='PASS',role='Independent selection and arithmetic; accepted calibration meanings and actual-font audit reviewed separately',author_manifest_sha256=PIN,pdf_metric_cells=150,source_article_only_cells=0,raw_metric_cells=80,total_cells=cells,text_hashes=hashes,pages=35,documents=docs,source_article_only=article,raw_files=raw,selection_review=rows,retained_bindings=bound,program_inclusion=code_inclusion(packet,p,roots),scientific_programs_executed=False,ratio=None)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists(),'fresh report');r=audit(a.packet,a.public_root,a.sources_root);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print('PASS',r['total_cells'],'cells',r['text_hashes'],'hashes')
if __name__=='__main__':main()
