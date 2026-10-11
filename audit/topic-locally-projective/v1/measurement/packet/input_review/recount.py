#!/usr/bin/env python3
"""Independent whole-page extraction and state-machine counts; no author imports."""
from pathlib import Path
import argparse, hashlib, json, unicodedata
import pypdf
PIN='396355b0cc7fac4c1c0af5a18af4a148195b8abebdbd49699a10c7cfdf21cb74'
PAGES={'L084':2,'L095':15,'U':7,'TABLES':5,'A1':2,'A2':3,'CODE':6}
CLASSES={('L084','/CMSY10',80):('P','P','𝒫',4),('L084','/MarVoSym',66):('B','B','✉',1),('L095','/OIWWDJ+LASY10',50):('a50','✷','□',2),('L095','/SXXWVZ+CMSY10',55):('mapsto','↦','⊢',4),('L095','/SXXWVZ+CMSY10',75):('K','K','𝒦',4),('L095','/SXXWVZ+CMSY10',76):('L','L','ℒ',4),('L095','/SXXWVZ+CMSY10',80):('P','P','𝒫',40),('L095','/SXXWVZ+CMSY10',81):('Q','Q','𝒬',2)}
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
 return dict(whitespace_tokens=words,alphanumeric_units=alnum,characters_without_whitespace=nonspace,characters_with_collapsed_whitespace=len(t),utf8_bytes_with_collapsed_whitespace=len(t.encode()),collapsed_text_sha256=sha(t.encode()))
def edit(s,ops):
 mask=bytearray(len(s));insert={}
 for a,b,value in ops:
  need(0<=a<b<=len(s) and not any(mask[a:b]),'disjoint visible edits');mask[a:b]=b'\1'*(b-a);insert[a]=value
 return ''.join(insert.get(i,'')+('' if mask[i] else c) for i,c in enumerate(s))
def boundary(p):
 need({k:r['pages'] for k,r in p['documents'].items()}==PAGES,'all forty pages')
 need(p['source_ids']==['L084','L095'] and p['original_count']==2,'two original editions')
 need(p['whole_common']==['U','TABLES'] and p['written_documents']==['U','TABLES','A1','A2'],'whole twelve-page common acquisition')
 need(p['applications']=={'L084':['A1'],'L095':['A2']},'separate full applications')
 need(p['programme_printed_alternative']==['CODE'],'whole printed programme alternative')
 need(len(p['programs'])==6 and sum(r['bytes'] for r in p['programs'])==24255 and all(r['whole_file'] and r['logical_role']=='required_finite_computation' for r in p['programs']),'six whole required programmes')
 need(len(p['required_data'])==1 and p['required_data'][0]['bytes']==39150 and p['required_data'][0]['sha256']=='11b552c06a0f5ce753f1dd1c2c47a7131aa70570236c7aa7631e3b7e509e07a4','entire mandatory historical table data')
 need(len(p['output_data'])==11 and sum(r['bytes'] for r in p['output_data'])==3470182,'whole generated outputs separately')
 need(len(p['operational_drivers'])==3 and sum(r['bytes'] for r in p['operational_drivers'])==32220 and not p['formal_files'],'drivers separately; no formal files')
 need(not p['cross_topic_discount'] and not p['factors_permitted'] and p['ratio'] is None,'no free umbrella or factors')
 need(all(x is None for x in p['unknown_costs'].values()),'external costs unknown')
 need('whole raw required source_tables.json' in p['programme_policy'] and 'same whole raw source_tables.json' in p['programme_policy'],'mandatory data in both code alternatives')
 need('entire common proof+tables' in p['conditional_policy'] and 'full required historical comparison data' in p['conditional_policy'],'conditional full acquisition')
def document(k,path,spec):
 pages=[pg.extract_text() or '' for pg in pypdf.PdfReader(path).pages];need(len(pages)==PAGES[k],'all physical pages '+k)
 raw='\n'.join(pages);need(sha(raw.encode())==spec['extraction_sha256'],'raw exact extraction');cuts=[];pbs=[];pos=0
 for n,t in enumerate(pages,1):
  pbs.append(dict(page=n,start=pos,end=pos+len(t),sha256=sha(t.encode()),empty_extraction=not bool(t)))
  if k=='L084':
   if n==1:pos+=len(t)+1;continue
   header='434 M.I. Hartley, D. Leemans\n';need(t.startswith(header),'actual erratum running header');a=0;b=len(header)
  else:
   z=len(t)
   while z and t[z-1].isspace():z-=1
   a=z-len(str(n));b=len(t);need(t[a:z]==str(n) and (a==0 or t[a-1]=='\n'),'isolated page footer')
  cuts.append(dict(page=n,start=pos+a,end=pos+b,literal=t[a:b],sha256=sha(t[a:b].encode())));pos+=len(t)+1
 need(pbs==spec['page_bindings'] and cuts==spec['excluded_furniture'],'exact complete pages/furniture')
 need(spec['included_spans']==[dict(start=0,end=len(raw),sha256=sha(raw.encode()))],'every body character included')
 ops=[(r['start'],r['end'],'\n') for r in cuts];rep=[];classes={}
 for r in spec['glyph_substitutions']:
  i=r['offset'];e=r['pdf_event'];key=(k,e['font'],e['encoded_byte']);need(key in CLASSES,'only reviewed glyph class');g,c,v,n=CLASSES[key]
  need(e['glyph_name']==g and raw[i]==c and r['output']==v and r['kind']=='visible_symbol','actual reviewed symbol, no mathematical emendation')
  need(r['input_codepoint']==f'U+{ord(c):04X}' and e['decoded_text']==c,'raw literal character')
  pb=pbs[r['page']-1];need(r['page_offset']==i-pb['start'],'physical offset')
  a,b=r['context_start'],r['context_end'];need(pb['start']<=a<=i<b<=pb['end'] and sha(raw[a:b].encode())==r['context_sha256'],'exact local context')
  rep.append((i,i+1,v));classes[key]=classes.get(key,0)+1
 need(classes=={key:v[3] for key,v in CLASSES.items() if key[0]==k},'complete repair multiplicities')
 if k=='L095':need(raw.count('arXiv:math/0307075v1  [math.GR]  5 Jul 2003')==1,'whole banner once')
 return {v:{n:measure(t,n) for n in ['NFC','NFKC']} for v,t in dict(raw_untrimmed=raw,raw_selected=edit(raw,ops),calibrated_selected=edit(raw,ops+rep)).items()},raw

def audit(packet,study):
 need(sha((packet/'manifest.json').read_bytes())==PIN,'frozen author manifest')
 for r in read(packet/'manifest.json')['exports']:bound(packet,r)
 p=read(packet/'policy.json');spec=read(packet/'input_spec.json');wanted=read(packet/'author_counts.json');boundary(p)
 protocol=read(packet/'protocol.json');need(protocol['science_review_sha256']=='b7535f010d143e18e13c3eb27acd1d0ac2f7b6a4a83b2ed22e464c85038b52c5','distinct root science authority')
 need(protocol['primary_coordinate']==dict(variant='calibrated_selected',normalization='NFC',unit='characters_without_whitespace'),'declared primary input coordinate')
 for cat,root in [('local_bindings',packet),('scientific_bindings',study)]:
  for r in protocol[cat]:bound(root,r)
 rootreview=study/'topic_LocallyProjective_volume_root_review'
 for r in read(rootreview/'manifest.json')['exports']:bound(rootreview,r)
 need(read(rootreview/'review.json')['status']=='PASS_DISTINCT_ROOT_MODULAR_MIGRATION','distinct modular acceptance status')
 docs={};texts={}
 for k,r in p['documents'].items():
  path,_=bound(study,r);need(all(spec[k][f]==r[f] for f in r),'same spec PDF');met,raw=document(k,path,spec[k]);need(met==wanted['documents'][k]['metrics'],'all independent coordinates '+k);docs[k]=dict(pages=PAGES[k],pdf_sha256=r['sha256'],metrics=met);texts[k]=raw
 rawfiles={}
 for cat in ['programs','required_data','operational_drivers']:
  rawfiles[cat]={}
  for r in p[cat]:
   _,b=bound(study,r);met={n:measure(b.decode(),n) for n in ['NFC','NFKC']};need(met==wanted['raw_files'][cat][r['path']]['metrics'],'whole raw counts '+r['path']);rawfiles[cat][r['path']]=dict(bytes=len(b),sha256=sha(b),metrics=met)
 for r in p['output_data']:bound(study,r)
 historical=read(study/p['required_data'][0]['path']);need(len(historical)==145 and sorted(r['label'] for r in historical)==list(range(1,146)),'all literal historical labels, including corrected/deleted rows')
 runtime=read(packet/'scientific_computational_inputs.json');need(runtime['selected_file_count']==len(runtime['selected_file_pins'])==13 and runtime['selected_bytes']==sum(r['bytes'] for r in runtime['selected_file_pins']) and runtime['complete_installation_cost'] is None and runtime['complete_algorithm_proof_cost'] is None,'selected runtime pins do not imply full runtime cost')
 tex=(study/'topic_LocallyProjective_volume/required-programs.tex').read_text()
 need(tex.count('\\VerbatimInput')==6 and not any(x in tex for x in ['firstline','lastline','linerange']),'six complete VerbatimInputs')
 # One normalization solely for printed-code inclusion, never for measurements.
 pack=lambda t:''.join(c for c in unicodedata.normalize('NFKC',t) if not c.isspace()).replace('↪','').replace('⌋','')
 for r in p['programs']:
  path,b=bound(study,r);relative=r['path'].split('topic_LocallyProjective_volume/')[1]
  need(sum(chunk.split('\n',1)[0].endswith('{'+relative+'}') for chunk in tex.split('\\VerbatimInput')[1:])==1 and pack(b.decode()) in pack(edit(texts['CODE'],[(x['start'],x['end'],'\n') for x in spec['CODE']['excluded_furniture']])),'full programme represented once')
 need('source_tables.json' not in [x.split('}')[0] for x in tex.split('\\VerbatimInput{')[1:]],'no claim of printed full historical data')
 return dict(status='PASS',author_manifest_sha256=PIN,pdf_metric_cells=210,raw_metric_cells=100,collapsed_text_hashes=62,pages=40,documents=docs,raw_files=rawfiles,required_programs=6,required_program_bytes=24255,required_raw_data_bytes=39150,outputs_separate_bytes=3470182,drivers_separate_bytes=32220,all_whole_code_inclusion=True,scientific_programs_executed=False,factors_computed=False,author_python_imported=False,unknown_costs=p['unknown_costs'])
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');r=audit(a.packet,a.study_root);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print('PASS 210 PDF + 100 raw cells;62 hashes')
if __name__=='__main__':main()
