#!/usr/bin/env python3
"""Independent whole-page extraction and state-machine counts; no author imports."""
from pathlib import Path
import argparse, hashlib, json, unicodedata
import pypdf
PIN='fb6b56fa264b35faec3ac8151023cf5ad083d25e5e9eed0ffce68f5e0ce9e439'
PAGES={'L020':19,'U':5,'A1':3,'COUNTER':3,'CODE':3}
CLASSES={('L020','/ZSYTRN+CMSY10',71):('G','G','𝒢',111),('L020','/GEHQPJ+MSBM10',78):('N','N','ℕ',1)}
def need(b,m):
 if not b:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text())
def bound(root,row):
 p=Path(row['path']);need(not p.is_absolute() and '..' not in p.parts,'safe relative path');p=root/p;b=p.read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'exact file '+str(p));return p,b
def measure(s,form):
 s=unicodedata.normalize(form,s);words=alnum=nonspace=0;inword=inalnum=False;pending=False;out=[]
 for c in s:
  a=c.isalnum()
  if a and not inalnum:alnum+=1
  inalnum=a
  if c.isspace():
   inword=False
   if out:pending=True
  else:
   if not inword:words+=1
   inword=True;nonspace+=1
   if pending:out.append(' ');pending=False
   out.append(c)
 t=''.join(out)
 return dict(whitespace_tokens=words,alphanumeric_units=alnum,characters_without_whitespace=nonspace,characters_with_collapsed_whitespace=len(t),utf8_bytes_with_collapsed_whitespace=len(t.encode()),normalized_text_sha256=sha(s.encode()),collapsed_text_sha256=sha(t.encode()))
def edit(s,ops):
 mask=bytearray(len(s));insert={}
 for a,b,value in ops:
  need(0<=a<b<=len(s) and not any(mask[a:b]),'disjoint visible edits');mask[a:b]=b'\1'*(b-a);insert[a]=value
 return ''.join(insert.get(i,'')+('' if mask[i] else c) for i,c in enumerate(s))
def boundary(p):
 need({k:r['pages'] for k,r in p['documents'].items()}==PAGES,'all thirty-three pages')
 need(p['source_ids']==['L020'] and p['original_count']==1 and p['source_dispositions']==19,'one exact original, nineteen dispositions')
 need(p['whole_common']==['U'] and p['written_documents']==['U','A1','COUNTER'],'whole five-page common')
 need(p['applications']=={'L020':['A1','COUNTER']},'both full three-page local papers')
 need(p['programme_printed_alternative']==['CODE'] and p['old_two_page_program_appendix']=='replaced, not added','complete appendix replaces predecessor')
 need(len(p['programs'])==3 and sum(r['bytes'] for r in p['programs'])==11533 and all(r['whole_file'] for r in p['programs']),'three entire programs')
 need([r['logical_role'] for r in p['programs']]==['required_finite_certificates_for_three_source_examples','bounded_validation_not_uniform_premise','transparent_S18_certificate_supporting_complete_written_proof'],'separate actual program roles')
 need(len(p['operational_drivers'])==3 and sum(r['bytes'] for r in p['operational_drivers'])==15947,'three separate full drivers')
 need(len(p['formal_files'])==2 and sum(r['bytes'] for r in p['formal_files'])==6855 and sum(r['declarations'] for r in p['formal_files'])==p['formal_declarations']==15,'two full partial formal files')
 need(not p['cross_topic_discount'] and not p['old_Topic_B_common_free_premise'] and not p['factors_permitted'] and p['ratio'] is None,'no free umbrella or factors')
 need(all(x is None for x in p['unknown_costs'].values()),'external costs remain unknown')
 need(p['primary_coordinate']==dict(variant='raw_untrimmed',normalization='NFC',unit='characters_without_whitespace'),'raw untrimmed primary')
 need(p['variants']==['raw_untrimmed','raw_selected','calibrated_selected'] and p['normalizations']==['NFC','NFKC'],'all thirty PDF coordinates')
 need('entire5page common' in p['conditional_policy'] and 'all three complete' in p['conditional_policy'] and 'AND complete3page counterproof' in p['conditional_policy'],'full conditional acquisition')
 need('case3 false' in p['source_correction'] and 'literal claims' in p['source_correction'],'source correction not rewritten in extraction')
 need(p['new_source_credit']==p['new_question_credit']==0,'no new credit')
def document(k,path,spec):
 pages=[pg.extract_text() or '' for pg in pypdf.PdfReader(path).pages];need(len(pages)==PAGES[k],'all physical pages '+k)
 raw='\n'.join(pages);need(sha(raw.encode())==spec['extraction_sha256'],'raw exact extraction');cuts=[];pbs=[];pos=0
 for n,t in enumerate(pages,1):
  pbs.append(dict(page=n,start=pos,end=pos+len(t),sha256=sha(t.encode()),empty_extraction=not bool(t)))
  if k=='L020' and n>1:
   header=(f'{n} JULIE DE SAEDELEER, DIMITRI LEEMANS, AND JESSICA MULPAS\n' if n%2==0 else f'RANK AUGMENTATION THEOREM FROM RANK 3 TO RANK 4 {n}\n')
   need(t.startswith(header),'literal running header');a=0;b=len(header)
  else:
   need(t.endswith('\n'+str(n)),'isolated terminal page number');a=len(t)-len(str(n));b=len(t)
  cuts.append(dict(page=n,start=pos+a,end=pos+b,literal=t[a:b],sha256=sha(t[a:b].encode())));pos+=len(t)+1
 need(pbs==spec['page_bindings'] and cuts==spec['excluded_furniture'],'exact complete pages/furniture')
 need(spec['included_spans']==[dict(start=0,end=len(raw),sha256=sha(raw.encode()))],'every body character included')
 ops=[(r['start'],r['end'],'\n') for r in cuts];rep=[];classes={}
 for r in spec['glyph_substitutions']:
  i=r['offset'];e=r['pdf_event'];key=(k,e['font'],e['encoded_byte']);need(key in CLASSES,'only reviewed glyph class');g,c,v,n=CLASSES[key]
  need(e['glyph_name']==g and raw[i]==c and r['output']==v and r['kind']=='actual_visible_mathematical_alphabet','actual reviewed symbol, no mathematical emendation')
  need(r['input_codepoint']==f'U+{ord(c):04X}' and e['decoded_text']==c,'raw literal character')
  pb=pbs[r['page']-1];need(r['page_offset']==i-pb['start'],'physical offset')
  a,b=r['context_start'],r['context_end'];need(pb['start']<=a<=i<b<=pb['end'] and sha(raw[a:b].encode())==r['context_sha256'],'exact local context')
  rep.append((i,i+1,v));classes[key]=classes.get(key,0)+1
 need(classes=={key:v[3] for key,v in CLASSES.items() if key[0]==k},'complete repair multiplicities')
 if k=='L020':need(raw.count('arXiv:2212.12563v1  [math.GR]  23 Dec 2022')==1,'whole banner once')
 return {v:{n:measure(t,n) for n in ['NFC','NFKC']} for v,t in dict(raw_untrimmed=raw,raw_selected=edit(raw,ops),calibrated_selected=edit(raw,ops+rep)).items()},raw

def audit(packet,study):
 need(sha((packet/'manifest.json').read_bytes())==PIN,'frozen author manifest')
 for r in read(packet/'manifest.json')['exports']:bound(packet,r)
 p=read(packet/'policy.json');spec=read(packet/'input_spec.json');wanted=read(packet/'author_counts.json');boundary(p)
 protocol=read(packet/'protocol.json');need(protocol['positive_root_review_sha256']=='7432603519e9e854f5044de3349e6b2707685110f889bdfe4e1e249e6e751504' and protocol['appendix_distinct_review_sha256']=='8a7a1728b5f6809e77d13f516f682f0f8902c1a26fd44e115c0b48c382194d03','distinct science and appendix acceptances')
 need(protocol['primary_coordinate']==p['primary_coordinate'] and not protocol['primary_material_exported'] and not protocol['factors_permitted'],'protocol boundary')
 for r in protocol['local_bindings']:bound(packet,r)
 for r in p['scientific_bindings']:bound(study,r)
 for folder,status in [('topic_B_L020_positive_root_review','PASS_DISTINCT_ROOT_CORRECTED_PRINCIPAL_L020'),('topic_B_L020_case_three_root_review','PASS_DISTINCT_ROOT_WRITTEN_AND_SCOPED_FORMAL_REVIEW'),('topic_B_L020_complete_programs_independent_review','ACCEPTED_UNCHANGED_COMPLETE_PROGRAM_APPENDIX')]:
  rootreview=study/folder
  for r in read(rootreview/'manifest.json')['exports']:bound(rootreview,r)
  need(read(rootreview/'review.json')['status']==status,'actual distinct review status')
 docs={};texts={}
 for k,r in p['documents'].items():
  path,_=bound(study,r);need(all(spec[k][f]==r[f] for f in r),'same spec PDF');met,raw=document(k,path,spec[k]);need(met==wanted['documents'][k]['metrics'],'all independent coordinates '+k);docs[k]=dict(pages=PAGES[k],pdf_sha256=r['sha256'],metrics=met);texts[k]=raw
 rawfiles={}
 for cat in ['programs','operational_drivers','formal_files']:
  rawfiles[cat]={}
  for r in p[cat]:
   _,b=bound(study,r);met={n:measure(b.decode(),n) for n in ['NFC','NFKC']};need(met==wanted['raw_files'][cat][r['path']]['metrics'],'whole raw counts '+r['path']);rawfiles[cat][r['path']]=dict(bytes=len(b),sha256=sha(b),metrics=met)
 tex=(study/'topic_B_L020_complete_programs/programs.tex').read_text()
 need(tex.count('\\VerbatimInput')==3 and not any(x in tex for x in ['firstline','lastline','linerange']),'three complete VerbatimInputs')
 pack=lambda t:''.join(c for c in unicodedata.normalize('NFKC',t) if not c.isspace())
 code=pack(edit(texts['CODE'],[(x['start'],x['end'],'\n') for x in spec['CODE']['excluded_furniture']]))
 for r in p['programs']:
  path,b=bound(study,r);name=path.name
  need(sum(chunk.split('\n',1)[0].endswith('{'+name+'}') for chunk in tex.split('\\VerbatimInput')[1:])==1 and code.count(pack(b.decode()))==1,'whole program represented once')
 return dict(status='PASS',author_manifest_sha256=PIN,pdf_metric_cells=150,raw_metric_cells=80,normalized_and_collapsed_text_hashes=92,pages=33,documents=docs,raw_files=rawfiles,whole_programs=3,whole_program_bytes=11533,drivers_separate_bytes=15947,formal_separate_bytes=6855,partial_formal_declarations=15,all_whole_code_inclusion=True,scientific_programs_executed=False,factors_computed=False,author_python_imported=False,unknown_costs=p['unknown_costs'])
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');r=audit(a.packet,a.study_root);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print('PASS 150 PDF + 80 raw cells;92 hashes')
if __name__=='__main__':main()
