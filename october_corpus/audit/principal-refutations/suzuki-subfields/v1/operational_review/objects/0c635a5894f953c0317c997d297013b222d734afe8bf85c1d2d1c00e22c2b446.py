"""Restore complete Suzuki correction evidence and run unchanged small controls."""
import sys
if sys.flags.optimize:raise RuntimeError('Unoptimized Python required')
sys.dont_write_bytecode=True
from pathlib import Path,PurePosixPath
import argparse,copy,gzip,hashlib,json,os,subprocess,time
B='corrections/suzuki-subfields/v1'
PROVENANCE={'phase8_suzuki_subfields.md','phase8_suzuki_subfields_independent_audit.md',
 'phase8_suzuki_subfields_intake.json','phase8_suzuki_subfields_check.py',
 'phase8_suzuki_subfields_check.json','phase8_suzuki_subfields_independent_run.json',
 'phase6_suzuki_realization.md','phase6_suzuki_counterexample_audit.md',
 'phase6_suzuki_counterexample_audit.json','phase6_suzuki_counterexample_audit_run.json',
 'phase6_suzuki_torus_check.py','phase6_suzuki_torus_check.json',
 'phase5_suzuki_check.py','phase5_suzuki_higher_check.py'}
def need(v,m):
 if not v:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def child(root,name):
 need(isinstance(name,str)and name,'Nonempty relative path');p=PurePosixPath(name)
 need(not p.is_absolute()and'..'not in p.parts,'Safe relative path');q=(root/p).resolve()
 need(q.is_relative_to(root.resolve()),'No escaping path');return q
def structure(t,policy):
 for k in ['whole_original_credit','new_measurements','new_question_credit','new_Lean']:need(t[k]==0,'No credit from transport')
 for k in policy:need(t[k]==policy[k],'Exact policy '+k)
 need(len(t['files'])==policy['logical_files'],'Complete inventory')
 keys=[(r['origin'],r['path'])for r in t['files']];need(len(keys)==len(set(keys)),'Unique logical paths')
 rows={(r['origin'],r['path']):r for r in t['files']}
 pm={(p['origin'],p['path']):p for p in t['packets']};need(len(pm)==len(t['packets']),'Unique manifest paths')
 need(len(pm)==policy['private_manifest_records']and sum(p['exports']for p in pm.values())==policy['complete_private_exports'],'Complete manifest/export inventory')
 ids=[c['source_id']for c in policy['components']];need(len(ids)==len(set(ids))and set(ids)=={'L110','L114','L115'},'Exact separate original coverage')
 expected_roots=[]
 for c in policy['components']:
  need(c['public_credit']==0 and c['accepted_mathematics']is True,'Private mathematical acceptance only')
  for role in ['author','distinct_review','root_adoption']:
   z=c[role];key=('study',z['packet']+'/manifest.json');expected_roots.append([z['packet'],z['sha256']])
   need(key in pm and pm[key]['sha256']==z['sha256']and rows[key]['sha256']==z['sha256']and rows[key]['bytes']==z['bytes'],'Exact component '+role)
  A=c['author']['packet'];base=B+'/'+c['public_subdir'];stem=c['manuscript_stem']
  for ext in ['.tex','.pdf']:
   r=rows['study',A+'/'+stem+ext];need(r.get('encoding')=='identity'and r.get('public_path')==base+'/proof/'+stem+ext,'Stable complete native route')
  for name in [c['program'],c['expected']]+c['extra_program_inputs']:
   r=rows['study',A+'/'+name];need(r.get('encoding')=='identity'and r.get('public_path')==base+'/programs/'+name,'Stable unchanged program route')
 need(expected_roots==policy['entry_roots'],'Declared acceptance chain')
 omitted={(r['origin'],r['path'],r['bytes'],r['sha256'],r['transport'])for r in rows.values()if r['transport'].endswith('HASH_ONLY')}
 expected={(r['origin'],r['path'],r['bytes'],r['sha256'],r['reason'])for r in policy['documentary_assets']}
 need(omitted==expected and len(expected)==24 and policy['runtime_identities']==[],'Exact documentary/runtime boundary')
 need({r['path']for r in policy['provenance_leaves']}==PROVENANCE,'Exact provenance-only boundary')
 for leaf in policy['provenance_leaves']:
  r=rows.get((leaf['origin'],leaf['path']));need(r is not None and all(r[k]==leaf[k]for k in ['bytes','sha256'])and not r['transport'].endswith('HASH_ONLY'),'Historical provenance retained verbatim')
 for r in rows.values():
  need(r['origin']in ['study','public'],'Declared namespace');child(Path('/logical'),r['path'])
  if r['transport'].endswith('HASH_ONLY'):continue
  need(r['transport']in ['NEW_FROZEN_FILE','EXISTING_PUBLIC']and r['encoding']in ['identity','gzip'],'Lossless storage');child(Path('/public'),r['public_path'])
  if r['transport']=='NEW_FROZEN_FILE':need(not r['public_path'].endswith(('.md','.pyc')),'Explicit storage suffix')
 need({(r['public_path'],r['stored_bytes'],r['stored_sha256'])for r in rows.values()if r['transport']=='EXISTING_PUBLIC'}=={(r['path'],r['bytes'],r['sha256'])for r in t['tracked_public_reuse']},'Complete tracked reuse inventory')
def main(a):
 started=time.monotonic();R=a.repo.resolve();P=a.payload.resolve()if a.payload else R
 tp=child(P,B+'/transport.json');pp=child(P,B+'/portable_policy.json');adapter=child(P,B+'/application_replay.py')
 need(sha(tp)==a.expected_transport and sha(pp)==a.expected_policy and sha(adapter)==a.expected_adapter,'Pinned transport,policy,adapter')
 t=load(tp);policy=load(pp);structure(t,policy)
 cases=[('duplicate',lambda x:x['files'].__setitem__(1,copy.deepcopy(x['files'][0]))),
  ('credit',lambda x:x.__setitem__('whole_original_credit',1)),('missing_packet',lambda x:x['packets'].pop()),
  ('wrong_author',lambda x:x['packets'][0].__setitem__('sha256','0'*64)),
  ('proof_as_document',lambda x:next(r for r in x['files']if r['path'].endswith('/subfield_boundary.tex')).__setitem__('transport','DOCUMENTARY_ASSET_HASH_ONLY')),
  ('missing_provenance',lambda x:x['provenance_leaves'].pop()),('changed_provenance',lambda x:x['provenance_leaves'][0].__setitem__('sha256','0'*64)),
  ('unsafe_path',lambda x:x['files'][0].__setitem__('path','../escape')),
  ('missing_program',lambda x:x['files'].remove(next(r for r in x['files']if r['path'].endswith('/center_orbits.py')))),
  ('lost_reuse',lambda x:x['tracked_public_reuse'].clear()),
  ('cross_original_review',lambda x:x['components'][0].__setitem__('distinct_review',x['components'][1]['distinct_review'])),
  ('invented_credit',lambda x:x['components'][0].__setitem__('public_credit',1)),
  ('lost_original',lambda x:x['components'].pop()),
  ('native_pages',lambda x:x['components'][0].__setitem__('manuscript_pages',1))]
 damaged=[]
 for name,change in cases:
  bad=copy.deepcopy(t);change(bad)
  try:structure(bad,policy)
  except(ValueError,KeyError):damaged.append(name)
  else:raise ValueError('Damaged transport accepted '+name)
 tracked=set(subprocess.check_output(['git','-C',str(R),'ls-files','-z']).decode().split('\0'))
 for r in t['tracked_public_reuse']:need(r['path']in tracked,'Reused bytes are Git tracked')
 O=a.out.resolve();need(not O.exists(),'Fresh external output');O.mkdir(parents=True)
 roots={ns:O/'restored'/ns for ns in ['study','public']}
 for p in roots.values():p.mkdir(parents=True)
 cache=O/'payloads';cache.mkdir();rows={(r['origin'],r['path']):r for r in t['files']};seen={};stored={};decoded={}
 for key,r in rows.items():
  if r['transport'].endswith('HASH_ONLY'):continue
  p=child(R if r['transport']=='EXISTING_PUBLIC'else P,r['public_path']);want=(r['stored_bytes'],r['stored_sha256'])
  if p not in stored:need(p.is_file()and(p.stat().st_size,sha(p))==want,'Exact stored public bytes '+str(p));stored[p]=want
  else:need(stored[p]==want,'Consistent stored identity')
  ident=r['bytes'],r['sha256']
  if ident not in decoded:
   raw=p.read_bytes();raw=gzip.decompress(raw)if r['encoding']=='gzip'else raw
   need((len(raw),hashlib.sha256(raw).hexdigest())==ident,'Exact lossless decoding');q=cache/r['sha256'];q.write_bytes(raw);decoded[ident]=q
  q=child(roots[r['origin']],r['path']);q.parent.mkdir(parents=True,exist_ok=True);os.link(decoded[ident],q);seen[key]=q
 def matches(r,x):return r['sha256']==x['sha256']and x.get('bytes',r['bytes'])==r['bytes']
 def direct(key,x):
  r=rows.get(key);need(r is not None and matches(r,x),'Exact direct binding '+str(key));need(r['transport'].endswith('HASH_ONLY')or key in seen,'Restored scientific input');return r
 exports=0
 for pk in t['packets']:
  p=seen[pk['origin'],pk['path']];need(sha(p)==pk['sha256'],'Frozen manifest');m=load(p);need(len(m['exports'])==pk['exports'],'All exports')
  for x in m['exports']:direct((pk['origin'],str(PurePosixPath(pk['path']).parent/x['path'])),x);exports+=1
 audit=[];unresolved=[]
 def resolve(x,ctx):
  name=x.get('path');h=x.get('sha256')
  if not isinstance(name,str)or not isinstance(h,str)or len(h)!=64:return
  candidates=[]
  for ns,prefix in policy['historical_absolute_roots'].items():
   if name.startswith(prefix):candidates.append((ns,name[len(prefix):]))
  if not Path(name).is_absolute():
   ns=x.get('namespace',x.get('origin'))
   if ns in ['study','public']:candidates.append((ns,name))
   candidates.extend([(ns,name)for ns in ['study','public']]);candidates.append(('study',str(PurePosixPath(ctx).parent/name)))
  for key in candidates:
   r=rows.get(key)
   if r and matches(r,x):direct(key,x);audit.append(dict(context=ctx,path=name,sha256=h,route=r['transport']));return
  unresolved.append(dict(context=ctx,pin=x))
 def walk(x,ctx):
  if isinstance(x,dict):
   resolve(x,ctx)
   for k,v in x.items():
    if isinstance(k,str)and k.startswith('/')and isinstance(v,str)and len(v)==64:resolve(dict(path=k,sha256=v),ctx)
    if k!='exports':walk(v,ctx)
  elif isinstance(x,list):
   for v in x:walk(v,ctx)
 for key,p in seen.items():
  if key[0]=='study'and p.suffix=='.json'and key[1]not in PROVENANCE:
   try:j=load(p)
   except(ValueError,UnicodeError):continue
   walk(j,key[1])
 save(O/'metadata_binding_audit.json',dict(resolved=audit,unresolved=unresolved,provenance_only_leaves=policy['provenance_leaves']))
 need(not unresolved,'Every acquiring metadata pin resolves')
 independent=[]
 for c in policy['components']:
  V=roots['study']/c['distinct_review']['packet'];receipt=load(V/'independent_report.json');need(receipt['status']=='PASS'and receipt['exit_code']==0 and not(V/'independent.stderr').read_bytes(),'Clean completed independent GAP evidence')
  name=c['independent_program'];marker=c['independent_marker'].encode();executed=receipt[c['independent_receipt_pin']]
  need(sha(V/name)==executed['sha256']and(V/name).stat().st_size==executed['bytes'],'Exact independent executed input')
  need((V/'independent.stdout').read_bytes().rstrip().endswith(marker),'Complete independent marker');independent.append(c['source_id'])
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
 cmd=[sys.executable,str(adapter),'--study',str(roots['study']),'--policy',str(pp),'--out',str(O/'application')]
 with(O/'application.stdout').open('wb')as so,(O/'application.stderr').open('wb')as se:
  p=subprocess.Popen(cmd,cwd=O,env=env,stdout=so,stderr=se);save(O/'active.json',dict(status='RUNNING',pid=p.pid,cap_seconds=240))
  try:code=p.wait(timeout=240)
  except subprocess.TimeoutExpired:p.kill();p.wait();save(O/'active.json',dict(status='TERMINAL_TIMEOUT_NO_CERTIFICATE'));raise ValueError('Application incomplete')
 save(O/'active.json',dict(status='TERMINAL',returncode=code));need(code==0 and not(O/'application.stderr').read_bytes(),'Clean complete public application')
 app=load(O/'application/report.json');need(app['status']=='PASS_PUBLIC_SUZUKI_APPLICATION'and app['native_pages']==sum(c['manuscript_pages']for c in policy['components']),'Exact application scope')
 need([c['source_id']for c in app['components']]==[c['source_id']for c in policy['components']],'Every original replayed separately')
 guards=[]
 for mode in ['argument','environment']:
  ee=dict(env);target=O/('bad_'+mode)
  if mode=='environment':ee['PYTHONOPTIMIZE']='1'
  p=subprocess.run([sys.executable]+(['-O']if mode=='argument'else[])+[str(Path(__file__).resolve()),'--out',str(target)],env=ee,capture_output=True,timeout=15)
  need(p.returncode!=0 and b'Unoptimized Python required'in p.stderr and not target.exists(),'Portable pre-output guard');guards.append(mode)
 for key,p in seen.items():need((p.stat().st_size,sha(p))==(rows[key]['bytes'],rows[key]['sha256']),'Restored scientific bytes unchanged')
 report=dict(status='PASS_PUBLIC_SUZUKI_CLOSURE',checker_sha256=sha(Path(__file__)),transport_sha256=sha(tp),policy_sha256=sha(pp),adapter_sha256=sha(adapter),logical_files=len(rows),restored_files=len(seen),decoded_objects=len(decoded),stored_objects=len(stored),private_packets=len(t['packets']),complete_exports=exports,metadata_pins=len(audit),documentary_assets=len(policy['documentary_assets']),provenance_only_leaves=len(PROVENANCE),tracked_reused_objects=len(t['tracked_public_reuse']),malformed_transport_controls=damaged,optimization_guards=guards,acquired_independent_GAP_calls=independent,application=app,application_stdout_sha256=sha(O/'application.stdout'),application_stderr_empty=True,no_private_fallback=True,acquired_censuses_repeated=False,whole_original_credit=0,new_measurements=0,new_question_credit=0,new_Lean=0,seconds=time.monotonic()-started)
 save(O/'report.json',report);print(json.dumps(report))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--payload',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--expected-transport',required=True);p.add_argument('--expected-policy',required=True);p.add_argument('--expected-adapter',required=True);main(p.parse_args())
