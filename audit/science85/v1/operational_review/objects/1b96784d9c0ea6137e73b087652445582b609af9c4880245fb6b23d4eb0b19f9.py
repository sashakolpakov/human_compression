"""Restore exact L041 public evidence and run bounded, unchanged controls."""
import sys
if sys.flags.optimize:raise RuntimeError('Unoptimized Python required')
sys.dont_write_bytecode=True
from pathlib import Path,PurePosixPath
import argparse,copy,gzip,hashlib,json,os,subprocess,time
B='audit/recoveries/L041/v1'
AUTHOR='corpus106_L041_decorated_geometry_v2'
AUTHOR_HASH='6f7221a6784c479748786ca2497df0a32f1162cd995e93acb3d9f58dc1665877'
def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def child(root,name):
 need(isinstance(name,str)and name,'Nonempty relative path');p=PurePosixPath(name);need(not p.is_absolute()and'..'not in p.parts,'Safe relative path');q=(root/p).resolve();need(q.is_relative_to(root.resolve()),'No escaping path');return q
def structure(t,policy):
 for k in ['whole_original_credit','new_measurements','new_question_credit','new_Lean']:need(t[k]==0,'No credit from transport')
 for k in policy:need(t[k]==policy[k],'Exact immutable policy '+k)
 need(len(t['files'])==policy['logical_files'],'Complete logical inventory')
 keys=[(r['origin'],r['path'])for r in t['files']];need(len(keys)==len(set(keys)),'Unique logical paths')
 need(len(t['packets'])==policy['private_packets']and sum(p['exports']for p in t['packets'])==policy['complete_private_exports'],'Complete private manifests')
 pm={(p['origin'],p['path']):p['sha256']for p in t['packets']};need(len(pm)==len(t['packets']),'Unique private manifests')
 need(pm.get(('study',AUTHOR+'/manifest.json'))==AUTHOR_HASH,'Exact frozen author')
 for name,h in policy['entry_roots']:need(pm.get(('study',name+'/manifest.json'))==h,'Exact declared entry chain')
 omitted={(r['origin'],r['path'],r['bytes'],r['sha256'],r['transport'])for r in t['files']if r['transport'].endswith('HASH_ONLY')}
 expected={(r['origin'],r['path'],r['bytes'],r['sha256'],r['reason'])for r in policy['documentary_assets']+policy['runtime_identities']}
 need(omitted==expected,'Exact documentary and runtime boundary')
 need(len(policy['runtime_identities'])==1,'One historical Python runtime identity')
 runtime=policy['runtime_identities'][0];need(runtime['origin']=='runtime'and runtime['path'].startswith('/opt/homebrew/Cellar/python@3.14/')and runtime['reason']=='RUNTIME_IDENTITY_HASH_ONLY','Literal historical runtime namespace')
 for r in t['files']:
  need(r['origin']in ['study','public','runtime'],'Declared namespaces')
  if r['origin']=='runtime':need(r['transport']=='RUNTIME_IDENTITY_HASH_ONLY','Runtime cannot masquerade as scientific file');continue
  child(Path('/logical'),r['path'])
  if r['transport'].endswith('HASH_ONLY'):continue
  need(r['transport']in ['NEW_FROZEN_FILE','EXISTING_PUBLIC']and r['encoding']in ['identity','gzip'],'Lossless public transport');child(Path('/public'),r['public_path'])
  if r['transport']=='NEW_FROZEN_FILE':need(not r['public_path'].endswith(('.md','.pyc')),'No Markdown or bytecode destination')
 rows={(r['origin'],r['path']):r for r in t['files']}
 tex=rows['study',AUTHOR+'/decorated_points.tex'];table=rows['study',AUTHOR+'/tetrahedra_section.tex']
 need(tex['encoding']==table['encoding']=='identity'and Path(tex['public_path']).parent/ 'tetrahedra_section.tex'==Path(table['public_path']),'Exact adjacent literal TeX input')
 reused={(r['public_path'],r['stored_bytes'],r['stored_sha256'])for r in t['files']if r['transport']=='EXISTING_PUBLIC'}
 need(reused=={(r['path'],r['bytes'],r['sha256'])for r in t['tracked_public_reuse']},'Complete tracked reuse inventory')
def main(a):
 start=time.monotonic();R=a.repo.resolve();P=a.payload.resolve()if a.payload else R
 tp=child(P,B+'/transport.json');pp=child(P,B+'/portable_policy.json');adapter=child(P,B+'/application_replay.py')
 need(sha(tp)==a.expected_transport and sha(pp)==a.expected_policy and sha(adapter)==a.expected_adapter,'Exact transport/policy/adapter identities')
 t=load(tp);policy=load(pp);structure(t,policy)
 cases=[('duplicate',lambda x:x['files'].__setitem__(1,copy.deepcopy(x['files'][0]))),('credit',lambda x:x.__setitem__('whole_original_credit',1)),('missing_packet',lambda x:x['packets'].pop()),('wrong_author',lambda x:next(p for p in x['packets']if p['path']==AUTHOR+'/manifest.json').__setitem__('sha256','0'*64)),('proof_as_document',lambda x:next(r for r in x['files']if r['path']==AUTHOR+'/decorated_points.tex').__setitem__('transport','DOCUMENTARY_ASSET_HASH_ONLY')),('lost_runtime_boundary',lambda x:x['runtime_identities'].clear()),('runtime_as_study',lambda x:next(r for r in x['files']if r['origin']=='runtime').__setitem__('origin','study')),('unsafe_path',lambda x:x['files'][0].__setitem__('path','../escape')),('lost_native_input',lambda x:x['files'].remove(next(r for r in x['files']if r['path']==AUTHOR+'/tetrahedra_section.tex'))),('nonadjacent_input',lambda x:next(r for r in x['files']if r['path']==AUTHOR+'/tetrahedra_section.tex').__setitem__('public_path',B+'/wrong.tex')),('lost_tracked_reuse',lambda x:x['tracked_public_reuse'].pop())]
 controls=[]
 for name,change in cases:
  bad=copy.deepcopy(t);change(bad)
  try:structure(bad,policy)
  except(ValueError,KeyError):controls.append(name)
  else:raise ValueError('Damaged transport accepted '+name)
 tracked=set(subprocess.check_output(['git','-C',str(R),'ls-files','-z']).decode().split('\0'))
 for r in t['tracked_public_reuse']:need(r['path']in tracked,'Every reused object must be Git tracked')
 need(not a.out.exists(),'Fresh external output');O=a.out.resolve();O.mkdir(parents=True);roots={ns:O/'restored'/ns for ns in ['study','public']}
 for root in roots.values():root.mkdir(parents=True)
 cache=O/'payloads';cache.mkdir();rows={(r['origin'],r['path']):r for r in t['files']};seen={};stored={};decoded={}
 for key,r in rows.items():
  if r['transport'].endswith('HASH_ONLY'):continue
  p=child(R if r['transport']=='EXISTING_PUBLIC'else P,r['public_path']);want=r['stored_bytes'],r['stored_sha256']
  if p not in stored:need(p.is_file()and(p.stat().st_size,sha(p))==want,'Exact stored public bytes '+str(p));stored[p]=want
  else:need(stored[p]==want,'Consistent stored identity')
  ident=r['bytes'],r['sha256']
  if ident not in decoded:
   data=p.read_bytes();data=gzip.decompress(data)if r['encoding']=='gzip'else data;need((len(data),hashlib.sha256(data).hexdigest())==ident,'Exact decoded scientific bytes');q=cache/r['sha256'];q.write_bytes(data);decoded[ident]=q
  q=child(roots[r['origin']],r['path']);q.parent.mkdir(parents=True,exist_ok=True);os.link(decoded[ident],q);seen[key]=q
 def matches(r,x):return r['sha256']==x['sha256']and x.get('bytes',r['bytes'])==r['bytes']
 def direct(key,x):
  r=rows.get(key);need(r is not None and matches(r,x),'Exact direct pin '+str(key));need(r['transport'].endswith('HASH_ONLY')or key in seen,'Restored scientific input');return r
 exports=0
 for pk in t['packets']:
  p=seen[pk['origin'],pk['path']];need(sha(p)==pk['sha256'],'Exact private manifest');m=load(p);need(len(m['exports'])==pk['exports'],'All manifest exports')
  for x in m['exports']:direct((pk['origin'],str(PurePosixPath(pk['path']).parent/x['path'])),x);exports+=1
 audit=[];unresolved=[]
 def resolve(x,ctx):
  name=x.get('path');h=x.get('sha256')
  if not isinstance(name,str)or not isinstance(h,str)or len(h)!=64:return
  candidates=[]
  for ns,prefix in policy['historical_absolute_roots'].items():
   if name.startswith(prefix):candidates.append((ns,name[len(prefix):]))
  if Path(name).is_absolute():candidates.append(('runtime',name))
  else:
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
  if key[0]=='study'and p.suffix=='.json':
   try:j=load(p)
   except(ValueError,UnicodeError):continue
   walk(j,key[1])
 save(O/'metadata_binding_audit.json',dict(resolved=audit,unresolved=unresolved));need(not unresolved,'Every exact metadata pin resolves')
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
 cmd=[sys.executable,str(adapter),'--author',str(roots['study']/AUTHOR),'--out',str(O/'application')]
 with(O/'application.stdout').open('wb')as so,(O/'application.stderr').open('wb')as se:
  p=subprocess.Popen(cmd,env=env,cwd=O,stdout=so,stderr=se);save(O/'active.json',dict(status='RUNNING',pid=p.pid,cap_seconds=240))
  try:code=p.wait(timeout=240)
  except subprocess.TimeoutExpired:p.kill();p.wait();save(O/'active.json',dict(status='TERMINAL_TIMEOUT_NO_CERTIFICATE'));raise ValueError('Capped application incomplete')
 save(O/'active.json',dict(status='TERMINAL',returncode=code));need(code==0 and not(O/'application.stderr').read_bytes(),'Application succeeded with retained clean receipt')
 application=load(O/'application/report.json');need(application['status']=='PASS_PUBLIC_L041_APPLICATION'and application['finite_fields']==[4,7,13,19,25]and application['native_pages']==8 and len(application['optimization_guards'])==6,'Exact application scope')
 guards=[]
 for mode in ['argument','environment']:
  e=dict(env);target=O/('bad_'+mode)
  if mode=='environment':e['PYTHONOPTIMIZE']='1'
  p=subprocess.run([sys.executable]+(['-O']if mode=='argument'else[])+[str(Path(__file__).resolve()),'--out',str(target)],env=e,capture_output=True,timeout=15);need(p.returncode!=0 and b'Unoptimized Python required'in p.stderr and not target.exists(),'Pre-output portable guard');guards.append(mode)
 for key,p in seen.items():need((p.stat().st_size,sha(p))==(rows[key]['bytes'],rows[key]['sha256']),'Restored bytes unchanged after replay')
 report=dict(status='PASS_PUBLIC_L041_CLOSURE',checker_sha256=sha(Path(__file__)),transport_sha256=sha(tp),policy_sha256=sha(pp),adapter_sha256=sha(adapter),logical_files=len(rows),restored_files=len(seen),decoded_objects=len(decoded),stored_objects=len(stored),private_packets=len(t['packets']),complete_exports=exports,metadata_pins=len(audit),documentary_assets=len(policy['documentary_assets']),runtime_identities=len(policy['runtime_identities']),tracked_reused_objects=len(t['tracked_public_reuse']),malformed_transport_controls=controls,optimization_guards=guards,application=application,application_stdout_sha256=sha(O/'application.stdout'),application_stderr_empty=True,principal_review_pending=policy['principal_review_pending'],no_private_fallback=True,acquired_censuses_repeated=False,new_measurements=0,new_question_credit=0,new_Lean=0,whole_original_credit=0,seconds=time.monotonic()-start)
 save(O/'report.json',report);print(json.dumps(report))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--payload',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--expected-transport',required=True);p.add_argument('--expected-policy',required=True);p.add_argument('--expected-adapter',required=True);main(p.parse_args())
