"""Restore the exact L036 proof/review closure using public payloads only."""
import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path,PurePosixPath
import argparse,copy,gzip,hashlib,json,os,subprocess,time
B='corrections/rudvalis-rank-two/v1'
def need(v,m):
 if not v:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,j):p.write_text(json.dumps(j,indent=2)+'\n')
def child(root,name):
 need(isinstance(name,str)and name,'Nonempty relative path');p=PurePosixPath(name);need(not p.is_absolute()and'..'not in p.parts,'Safe relative path');q=(root/p).resolve();need(q.is_relative_to(root.resolve()),'No escape');return q
def structure(t,policy):
 for k,v in policy.items():need(t[k]==v,'Exact policy '+k)
 for k in ['whole_original_credit','new_measurements','new_question_credit','new_Lean']:need(t[k]==0,'No transport credit')
 need(t['tracked_public_reuse']==[],'No undeclared checkout dependency')
 rows={(r['origin'],r['path']):r for r in t['files']};need(len(rows)==len(t['files'])==policy['logical_files'],'Unique complete inventory')
 packets={(r['origin'],r['path']):r for r in t['packets']};need(len(packets)==len(t['packets'])==policy['private_manifest_records']==3,'Three complete accepted packets')
 need(sum(p['exports']for p in t['packets'])==policy['complete_private_exports']==16,'All sixteen accepted exports')
 need(len(policy['components'])==1 and policy['components'][0]['source_ids']==['L036'],'Exactly L036')
 c=policy['components'][0];need(c['accepted_mathematics']is True and c['public_credit']==0,'Private accepted scope')
 roots=[]
 for role in ['author','distinct_review','root_adoption']:
  x=c[role];k=('study',x['packet']+'/manifest.json');roots.append([x['packet'],x['sha256']]);need(k in packets and packets[k]['sha256']==x['sha256']and rows[k]['sha256']==x['sha256']and rows[k]['bytes']==x['bytes'],'Exact acceptance '+role)
 need(roots==policy['entry_roots'],'Complete acceptance chain')
 for ext in ['.tex','.pdf']:
  r=rows['study',c['author']['packet']+'/orbit_bound'+ext];need(r['transport']=='NEW_FROZEN_FILE'and r['encoding']=='identity'and r['public_path']==B+'/proof/orbit_bound'+ext,'Stable native entry')
 for name in c['scientific_programs']:
  r=rows['study',c['author']['packet']+'/'+name];need(r['transport']=='NEW_FROZEN_FILE'and r['encoding']=='identity'and r['public_path']==B+'/programs/'+name,'Stable unchanged program')
 omitted={(x['origin'],x['path'],x['bytes'],x['sha256'],x['transport'])for x in rows.values()if x['transport'].endswith('HASH_ONLY')}
 expected={(x['origin'],x['path'],x['bytes'],x['sha256'],x['reason'])for x in policy['documentary_assets']}
 need(omitted==expected and len(expected)==6,'Exact documentary exclusions');need(policy['runtime_identities']==[]and policy['provenance_leaves']==[],'No undeclared omission')
 need(policy['native_inputs']==[dict(source_ids=['L036'],tex=B+'/proof/orbit_bound.tex',pdf=B+'/proof/orbit_bound.pdf',tex_inputs=[],physical_pages=2)],'Complete native inputs')
 for r in rows.values():
  need(r['origin']=='study','Declared namespace');child(Path('/logical'),r['path'])
  if r['transport'].endswith('HASH_ONLY'):continue
  need(r['transport']=='NEW_FROZEN_FILE'and r['encoding']in ['identity','gzip'],'Declared lossless storage');child(Path('/public'),r['public_path']);need(not r['public_path'].endswith(('.md','.pyc')),'Explicit stored suffix')
def main(a):
 start=time.monotonic();R=a.repo.resolve();P=a.payload.resolve()if a.payload else R;tp=child(P,B+'/transport.json');pp=child(P,B+'/portable_policy.json');adapter=child(P,B+'/application_replay.py')
 need(sha(tp)==a.expected_transport and sha(pp)==a.expected_policy and sha(adapter)==a.expected_adapter,'Exact transport, policy and adapter')
 t=load(tp);policy=load(pp);structure(t,policy);damages=[]
 changes=[('duplicate',lambda x:x['files'].__setitem__(1,copy.deepcopy(x['files'][0]))),('credit',lambda x:x.__setitem__('whole_original_credit',1)),('missing_packet',lambda x:x['packets'].pop()),('wrong_author',lambda x:x['packets'][0].__setitem__('sha256','0'*64)),('proof_omitted',lambda x:next(r for r in x['files']if r['path'].endswith('/orbit_bound.tex')).__setitem__('transport','DOCUMENTARY_ASSET_HASH_ONLY')),('unsafe_path',lambda x:x['files'][0].__setitem__('path','../escape')),('missing_program',lambda x:x['files'].remove(next(r for r in x['files']if r['path'].endswith('/arithmetic.py')))),('invented_public_credit',lambda x:x['components'][0].__setitem__('public_credit',1)),('native_pages',lambda x:x['native_inputs'][0].__setitem__('physical_pages',1)),('untracked_reuse',lambda x:x['tracked_public_reuse'].append(dict(path='untracked.pyc')))]
 for label,change in changes:
  bad=copy.deepcopy(t);change(bad)
  try:structure(bad,policy)
  except(ValueError,KeyError):damages.append(label)
  else:raise ValueError('Damaged structure accepted '+label)
 O=a.out.resolve();need(not O.exists(),'Fresh external output');O.mkdir(parents=True);S=O/'restored/study';S.mkdir(parents=True);cache=O/'payloads';cache.mkdir();rows={(r['origin'],r['path']):r for r in t['files']};seen={};stored={};decoded={}
 for key,r in rows.items():
  if r['transport'].endswith('HASH_ONLY'):continue
  p=child(P,r['public_path']);wanted=r['stored_bytes'],r['stored_sha256']
  if p not in stored:need(p.is_file()and(p.stat().st_size,sha(p))==wanted,'Exact public object '+str(p));stored[p]=wanted
  else:need(stored[p]==wanted,'Consistent stored identity')
  ident=r['bytes'],r['sha256']
  if ident not in decoded:
   raw=p.read_bytes();raw=gzip.decompress(raw)if r['encoding']=='gzip'else raw;need((len(raw),hashlib.sha256(raw).hexdigest())==ident,'Exact decoded identity');q=cache/r['sha256'];q.write_bytes(raw);decoded[ident]=q
  q=child(S,r['path']);q.parent.mkdir(parents=True,exist_ok=True);os.link(decoded[ident],q);seen[key]=q
 def direct(key,x):
  r=rows.get(key);need(r is not None and r['sha256']==x['sha256']and r['bytes']==x.get('bytes',r['bytes']),'Exact direct binding '+str(key));need(r['transport'].endswith('HASH_ONLY')or key in seen,'Scientific file restored');return r
 exports=0
 for pk in t['packets']:
  p=seen[pk['origin'],pk['path']];need(sha(p)==pk['sha256'],'Exact manifest');m=load(p);need(len(m['exports'])==pk['exports'],'Complete exports')
  for x in m['exports']:direct((pk['origin'],str(PurePosixPath(pk['path']).parent/x['path'])),x);exports+=1
 audit=[];unresolved=[]
 def resolve(x,ctx):
  name=x.get('path');h=x.get('sha256')
  if not isinstance(name,str)or not isinstance(h,str)or len(h)!=64:return
  candidates=[]
  for ns,prefix in policy['historical_absolute_roots'].items():
   if name.startswith(prefix):candidates.append((ns,name[len(prefix):]))
  if not Path(name).is_absolute():candidates += [('study',name),('study',str(PurePosixPath(ctx).parent/name))]
  for key in candidates:
   r=rows.get(key)
   if r and r['sha256']==h and r['bytes']==x.get('bytes',r['bytes']):direct(key,x);audit.append(dict(context=ctx,path=name,sha256=h,route=r['transport']));return
  unresolved.append(dict(context=ctx,pin=x))
 def walk(x,ctx):
  if isinstance(x,dict):
   resolve(x,ctx)
   for k,v in x.items():
    if k!='exports':walk(v,ctx)
  elif isinstance(x,list):
   for v in x:walk(v,ctx)
 for key,p in seen.items():
  if p.suffix=='.json':walk(load(p),key[1])
 save(O/'metadata_binding_audit.json',dict(resolved=audit,unresolved=unresolved));need(not unresolved,'All acquiring metadata locators resolve')
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1';cmd=[sys.executable,'-B',str(adapter),'--study',str(S),'--out',str(O/'application')]
 with(O/'application.stdout').open('wb')as so,(O/'application.stderr').open('wb')as se:
  p=subprocess.Popen(cmd,cwd=O,env=env,stdout=so,stderr=se);save(O/'active.json',dict(status='RUNNING',pid=p.pid,cap_seconds=240))
  try:code=p.wait(timeout=240)
  except subprocess.TimeoutExpired:p.kill();p.wait();save(O/'active.json',dict(status='TERMINAL_TIMEOUT_NO_CERTIFICATE'));raise ValueError('Incomplete application')
 save(O/'active.json',dict(status='TERMINAL',returncode=code));need(code==0 and not(O/'application.stderr').read_bytes(),'Clean application completion');app=load(O/'application/report.json');need(app['status']=='PASS_PUBLIC_L036_APPLICATION'and app['native_pages']==2 ,'Complete application')
 guards=[]
 for mode in ['argument','environment']:
  ee=dict(env);target=O/('bad_'+mode)
  if mode=='environment':ee['PYTHONOPTIMIZE']='1'
  p=subprocess.run([sys.executable]+(['-O']if mode=='argument'else[])+[str(Path(__file__).resolve()),'--out',str(target)],env=ee,capture_output=True,timeout=15)
  need(p.returncode!=0 and b'Ordinary Python required'in p.stderr and not target.exists(),'Pre-output guard');guards.append(mode)
 for key,p in seen.items():need((p.stat().st_size,sha(p))==(rows[key]['bytes'],rows[key]['sha256']),'Scientific bytes unchanged')
 report=dict(status='PASS_PUBLIC_L036_CLOSURE',checker_sha256=sha(Path(__file__)),transport_sha256=sha(tp),policy_sha256=sha(pp),adapter_sha256=sha(adapter),logical_files=len(rows),restored_files=len(seen),decoded_objects=len(decoded),stored_objects=len(stored),private_packets=len(t['packets']),complete_exports=exports,metadata_pins=len(audit),documentary_assets=6,tracked_reused_objects=0,malformed_transport_controls=damages,optimization_guards=guards,application=app,application_stdout_sha256=sha(O/'application.stdout'),application_stderr_empty=True,no_private_fallback=True,acquired_censuses_repeated=False,independent_controls_replayed=False,whole_original_credit=0,new_measurements=0,new_question_credit=0,new_Lean=0,seconds=time.monotonic()-start)
 save(O/'report.json',report);print(json.dumps(report))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--payload',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--expected-transport',required=True);p.add_argument('--expected-policy',required=True);p.add_argument('--expected-adapter',required=True);main(p.parse_args())
