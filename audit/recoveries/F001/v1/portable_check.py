"""Restore F001 using public paths alone; replay its finite and native checks.

Uniform written proofs and their distinct reviews remain separate evidence.
The primary-source exemption authenticates documentary hashes only.
"""
from pathlib import Path, PurePosixPath
import argparse, contextlib, gzip, hashlib, importlib.util, json, os, shutil, sys
BASE='audit/recoveries/F001/v1'
PRIMARY={'sources/symplectic_ranks2020.pdf','sources/symplectic_ranks2020.txt','sources/psl2_chiral2017.pdf','sources/psl2_chiral2017.txt','sources/monson_symmetric_polytopes_course.pdf'}
def need(ok,s):
 if not ok: raise ValueError(s)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def child(root,name):
 p=PurePosixPath(name);need(name and not p.is_absolute() and '..' not in p.parts,'unsafe logical path');q=(root/p).resolve();need(q.is_relative_to(root.resolve()),'path escapes');return q
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def main(a):
 need(__debug__,'optimized Python unsupported');need(not a.out.exists(),'fresh output required')
 os.environ.pop('PYTHONOPTIMIZE',None)
 repo=a.repo.resolve();payload=a.payload.resolve() if a.payload else repo
 tp=child(payload,BASE+'/transport.json');need(sha(tp)==a.expected_transport,'frozen transport changed');tr=json.loads(tp.read_text())
 need(len(tr['files'])==tr['logical_files'],'logical inventory')
 a.out.mkdir(parents=True);study=a.out.resolve()/'restored/study';study.mkdir(parents=True);cache=a.out.resolve()/'payloads';cache.mkdir()
 seen=set();decoded={};primary={}
 for row in tr['files']:
  need(row['origin']=='study' and row['path'] not in seen,'duplicate or unknown logical origin');seen.add(row['path']);dest=child(study,row['path'])
  if row['transport'].endswith('HASH_ONLY'):
   need(row['transport']=='PRIVATE_PRIMARY_SOURCE_HASH_ONLY' and row['path'] in PRIMARY,'undeclared omission');primary[row['path']]=row;continue
  key=(row['bytes'],row['sha256'])
  if key not in decoded:
   need(row['transport'] in ['EXISTING_PUBLIC','NEW_FROZEN_FILE'],'unknown transport');base=repo if row['transport']=='EXISTING_PUBLIC' else payload;src=child(base,row['public_path'])
   need(src.stat().st_size==row['stored_bytes'] and sha(src)==row['stored_sha256'],'stored evidence changed');need(row['encoding'] in ['identity','gzip'],'unknown encoding')
   target=cache/row['sha256'];opener=gzip.open if row['encoding']=='gzip' else open
   with opener(src,'rb') as inf,target.open('wb') as outf: shutil.copyfileobj(inf,outf)
   need(target.stat().st_size==row['bytes'] and sha(target)==row['sha256'],'decoded evidence changed');decoded[key]=target
  dest.parent.mkdir(parents=True,exist_ok=True);os.link(decoded[key],dest)
 need(set(primary)==PRIMARY==set(tr['primary_sources_hash_only']),'exact primary omissions')
 packets={p['path']:p for p in tr['packets']};need(len(packets)==len(tr['packets']),'duplicate packet')
 needed=set(json.loads((study/'corpus106_F001_principal_v1/dependencies.json').read_text())['required_acquired_manifests'])
 needed.update(n+'/manifest.json' for n in ['corpus106_F001_principal_v1','corpus106_F006_Dn_v2','corpus106_F006_Dn_independent_review','corpus106_F006_complete_root_adoption'])
 need(needed<=set(packets) and len(packets)==len(needed)+1,'complete author/components plus one whole-principal acceptance')
 extra=(set(packets)-needed).pop();need(extra.startswith('corpus106_F001_principal_') and extra.endswith('/manifest.json'),'whole-principal acceptance route')
 exports=0
 for relative,pin in packets.items():
  mp=child(study,relative);need(sha(mp)==pin['sha256'],'packet manifest changed');m=json.loads(mp.read_text());need(len(m['exports'])==pin['exports'],'complete acquired exports')
  for row in m['exports']:
   p=child(mp.parent,row['path']);need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'missing acquired export');exports+=1
 completed=[]
 for stem,bind_name,gap in [('odd_existence','bind',True),('reflection_bound','binding',False),('mixed_bound','binding',False),('principal','bind',False),('rank_bound',None,True)]:
  p=study/('corpus106_F001_'+stem+'_v1');author=module('f001_'+stem+'_restored',p/'check.py')
  if bind_name:
   original=getattr(author,bind_name)
   def restored_bind(root,row,original=original):
    target=(root/row['path']).resolve();need(target.is_relative_to(study),'binding leaves restored study')
    if root.resolve()==study and row['path'] in primary:
     pin=primary[row['path']];need(row['bytes']==pin['bytes'] and row['sha256']==pin['sha256'],'source identity changed');return
    original(root,row)
   setattr(author,bind_name,restored_bind)
  args=[str(p/'check.py'),'--out',str(a.out.resolve()/stem)]
  if bind_name:args+=['--study-root',str(study)]
  # The auxiliary check's only --study-root reads are its two source PDFs/text
  # hashes, already authenticated above; it has no mathematical fallback.
  if gap:args+=['--gap',a.gap]
  if a.render:args+=['--render']
  prior=sys.argv;sys.argv=args
  try:
   with (a.out/(stem+'.stdout')).open('w') as stream,contextlib.redirect_stdout(stream):author.main()
  finally:sys.argv=prior
  result=json.loads((a.out/stem/'report.json').read_text());need(result['status']=='PASS','restored component failed');completed.append(dict(component=stem,report=result))
 odd=completed[0]['report'];need(odd['finite_subset_pairs']==4096 and odd['q3_prefix_counts']==[2,13,121,20,2] and odd['q3_generating_markings']==0,'complete odd finite premises')
 mixed=completed[2]['report'];need(mixed.get('identities')==53 or mixed.get('symbolic_identities')==53,'all mixed identities')
 principal=completed[3]['report'];need(principal['claim_routes']==14 and principal['acquired_export_records']==175,'whole principal acquisition')
 aux=completed[4]['report'];need(aux['group_orders']==[5040,5040] and aux['full_subset_intersection_pairs_per_marking']==4096,'auxiliary correction evidence')
 report=dict(status='PASS_PUBLIC_F001_RESTORATION_AND_FINITE_PREMISES',transport_sha256=sha(tp),logical_records=len(seen),restored_files=len(seen)-len(primary),distinct_payloads=len(decoded),acquired_packets=len(packets),acquired_exports=exports,documentary_primary_only=sorted(primary),checks=completed,private_proof_fallback=False,source_content_reread=False,new_native_page_review=False,mathematical_review_replaced_by_hashes=False,whole_original_credit=0)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='checks'}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--payload',type=Path);p.add_argument('--expected-transport',required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--gap',default='gap');p.add_argument('--render',action='store_true');main(p.parse_args())
