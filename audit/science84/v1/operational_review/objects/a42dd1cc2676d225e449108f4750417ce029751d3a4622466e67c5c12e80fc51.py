"""Restore exact public N010 evidence and replay the bounded source join."""
import sys
if sys.flags.optimize:raise RuntimeError('Unoptimized Python required')
sys.dont_write_bytecode=True
import argparse,copy,gzip,hashlib,json,os,subprocess,time
from pathlib import Path,PurePosixPath
B='audit/recoveries/N010/v1'
ACCEPT={'corpus106_N010_principal_v2/manifest.json':'ba06d64f5d5e08ff25df0e1fdb98e04362c6d7055ad489b14bbe40c625f8c271',
 'corpus106_N010_principal_independent_review/manifest.json':'9679450e6c769404889f873a00f624e60a9c6ab3c47a09ec6e5d30943b40fa35',
 'corpus106_N010_principal_root_adoption/manifest.json':'56c02b706f9c999fd370dca79c38c93464dd79d19dc456e5cd9f62a16addd486'}
def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def child(root,name):
 need(isinstance(name,str)and name,'Nonempty relative path');n=PurePosixPath(name);need(not n.is_absolute()and'..'not in n.parts,'Safe relative path');p=(root/n).resolve();need(p.is_relative_to(root.resolve()),'No escaping path');return p
def structure(t,policy):
 for k in ['whole_original_credit','new_measurements','new_question_credit','new_Lean']:need(t[k]==0,'No credit from transport')
 for k in policy:need(t[k]==policy[k],'Exact policy '+k)
 need(t['logical_files']==len(t['files'])==5962,'Exact complete logical closure')
 keys=[(r['origin'],r['path'])for r in t['files']];need(len(set(keys))==len(keys),'Unique logical paths')
 need(len(t['packets'])==policy['private_packets']==25 and sum(r['exports']for r in t['packets'])==policy['complete_private_exports']==215,'Complete private manifest inventory')
 pm={(r['origin'],r['path']):r['sha256']for r in t['packets']};need(len(pm)==25,'Unique private packets')
 for p,h in ACCEPT.items():need(pm.get(('study',p))==h,'Accepted exact principal chain')
 omitted={(r['origin'],r['path'],r['bytes'],r['sha256'],r['transport'])for r in t['files']if r['transport'].endswith('HASH_ONLY')}
 expected={(r['origin'],r['path'],r['bytes'],r['sha256'],r['reason'])for r in policy['primary_sources_hash_only']}
 need(omitted==expected and len(omitted)==15,'Exact direct documentary omissions')
 need(len(policy['inherited_documentary_exclusions'])==3 and len(policy['complete_published_collections'])==6,'Exact inherited complete collections')
 for r in t['files']:
  need(r['origin']in ['study','public'],'Exact namespace');child(Path('/logical'),r['path'])
  if r['transport'].endswith('HASH_ONLY'):continue
  need(r['transport']in ['EXISTING_PUBLIC','NEW_FROZEN_FILE']and r['encoding']in ['identity','gzip'],'Exact lossless mode');child(Path('/public'),r['public_path'])
  if r['transport']=='NEW_FROZEN_FILE':need(not r['public_path'].endswith(('.md','.pyc')),'No new Markdown or bytecode path')
def main(a):
 start=time.monotonic();repo=a.repo.resolve();payload=a.payload.resolve()if a.payload else repo
 tp=child(payload,B+'/transport.json');pp=child(payload,B+'/portable_policy.json');adapter=child(payload,B+'/application_replay.py')
 need(sha(tp)==a.expected_transport and sha(pp)==a.expected_policy and sha(adapter)==a.expected_adapter,'Exact transport/policy/adapter pins')
 t=load(tp);policy=load(pp);structure(t,policy)
 mutations=[('duplicate',lambda x:x['files'].__setitem__(1,copy.deepcopy(x['files'][0]))),
 ('credit',lambda x:x.__setitem__('whole_original_credit',1)),('missing_packet',lambda x:x['packets'].pop()),
 ('wrong_author',lambda x:next(p for p in x['packets']if p['path']=='corpus106_N010_principal_v2/manifest.json').__setitem__('sha256','0'*64)),
 ('proof_as_document',lambda x:next(r for r in x['files']if r['path']=='corpus106_N010_principal_v2/principal.tex').__setitem__('transport','DOCUMENTARY_ASSET_HASH_ONLY')),
 ('lost_inherited_boundary',lambda x:x['inherited_documentary_exclusions'].pop()),
 ('lost_document',lambda x:x['primary_sources_hash_only'].pop()),
 ('unsafe_path',lambda x:x['files'][0].__setitem__('path','../escape')),
 ('private_fallback',lambda x:x['files'][0].__setitem__('origin','private')),
 ('lost_table',lambda x:x['files'].remove(next(r for r in x['files']if r['path']=='corpus106_N010_principal_v2/context_table.tex')))]
 controls=[]
 for name,fn in mutations:
  bad=copy.deepcopy(t);fn(bad)
  try:structure(bad,policy)
  except(ValueError,KeyError):controls.append(name)
  else:raise ValueError('Damaged transport accepted '+name)
 need(not a.out.exists(),'Fresh external output');out=a.out.resolve();out.mkdir(parents=True)
 roots={k:out/'restored'/k for k in ['study','public']}
 for root in roots.values():root.mkdir(parents=True)
 cache=out/'payloads';cache.mkdir();rows={(r['origin'],r['path']):r for r in t['files']};decoded={};stored={};seen={}
 for key,r in rows.items():
  if r['transport'].endswith('HASH_ONLY'):continue
  p=child(repo if r['transport']=='EXISTING_PUBLIC'else payload,r['public_path']);wanted=r['stored_bytes'],r['stored_sha256']
  if p not in stored:need(p.is_file()and(p.stat().st_size,sha(p))==wanted,'Exact stored public bytes '+str(p));stored[p]=wanted
  else:need(stored[p]==wanted,'Consistent public storage pin')
  ident=r['bytes'],r['sha256']
  if ident not in decoded:
   data=p.read_bytes();data=gzip.decompress(data)if r['encoding']=='gzip'else data
   need((len(data),hashlib.sha256(data).hexdigest())==ident,'Exact decoded payload');q=cache/r['sha256'];q.write_bytes(data);decoded[ident]=q
  q=child(roots[r['origin']],r['path']);q.parent.mkdir(parents=True,exist_ok=True);os.link(decoded[ident],q);seen[key]=q
 print('RESTORED',len(seen),len(decoded),flush=True)
 def matches(r,x):return r['sha256']==x['sha256']and x.get('bytes',r['bytes'])==r['bytes']
 def direct(key,x):
  r=rows.get(key);need(r is not None and matches(r,x),'Exact direct pin '+str(key))
  need(r['transport'].endswith('HASH_ONLY')or key in seen,'Restored direct scientific pin');return r
 exports=0
 for pk in t['packets']:
  p=seen[pk['origin'],pk['path']];need(sha(p)==pk['sha256'],'Exact private manifest');m=load(p);need(len(m['exports'])==pk['exports'],'All private exports')
  for row in m['exports']:
   direct((pk['origin'],str(PurePosixPath(pk['path']).parent/row['path'])),row);exports+=1
 # Every old published transport is retained exactly. Decode all its scientific
 # objects once; documentary rows stay literal inherited exemptions. This avoids
 # guessing that an old omitted GAP manual is a newly missing scientific input.
 legacy={};legacy_decoded={};legacy_rows=0;legacy_documents=0;legacy_literals={};legacy_locators={}
 prefixes=dict(policy['historical_absolute_roots'])
 for item in policy['inherited_documentary_exclusions']:
  p=seen['public',item['transport']['path']];need(sha(p)==item['transport']['sha256'],'Exact inherited transport');old=load(p)
  docs=[r for r in old['files']if r['transport'].endswith('HASH_ONLY')]
  need(docs==item['documentary_rows']==item['exact_declared_omissions'],'Unchanged full inherited documentary list')
  for ns,prefix in old.get('historical_absolute_roots',{}).items():
   need(ns not in prefixes or prefixes[ns]==prefix,'Consistent inherited absolute root');prefixes[ns]=prefix
  for loc in old.get('relative_locator_resolutions',[]):
   key=loc['context'],loc['historical_pin']['path'],loc['historical_pin']['sha256']
   legacy_locators[key]=loc
  for r in old['files']:
   legacy[(r['origin'],r['path'],r['sha256'])]=r;legacy_rows+=1
   if Path(r['path']).is_absolute():legacy_literals[r['path'],r['sha256']]=r
   if r['transport'].endswith('HASH_ONLY'):legacy_documents+=1;continue
   storedkey=('public',r['public_path']);q=seen.get(storedkey);need(q is not None,'Complete stored inherited proof object')
   direct(storedkey,dict(bytes=r['stored_bytes'],sha256=r['stored_sha256']))
   ident=r['bytes'],r['sha256']
   if ident not in legacy_decoded:
    data=q.read_bytes();need(r['encoding']in ['identity','gzip'],'Inherited exact encoding');data=gzip.decompress(data)if r['encoding']=='gzip'else data
    need((len(data),hashlib.sha256(data).hexdigest())==ident,'All inherited scientific bytes decoded exactly');legacy_decoded[ident]=True
 print('INHERITED',legacy_rows,len(legacy_decoded),legacy_documents,flush=True)
 audit=[];unresolved=[]
 def resolve(x,context):
  name=x.get('path');h=x.get('sha256')
  if not isinstance(name,str)or not isinstance(h,str)or len(h)!=64:return
  candidates=[]
  for ns,prefix in prefixes.items():
   if name.startswith(prefix):candidates.append((ns,name[len(prefix):]))
  if name.startswith('PUBLIC:'):candidates.append(('public',name[7:]))
  if not Path(name).is_absolute():
   ns=x.get('namespace',x.get('origin'))
   if ns in ['study','public','gap']:candidates.append((ns,name))
   candidates.extend([(ns,name)for ns in ['study','public','gap']]);candidates.append(('study',str(PurePosixPath(context).parent/name)))
  for key in candidates:
   r=rows.get(key)
   if r and matches(r,x):direct(key,x);audit.append(dict(context=context,path=name,sha256=h,route='direct',documentary=r['transport'].endswith('HASH_ONLY')));return
  for key in candidates:
   r=legacy.get((*key,h))
   if r and matches(r,x):audit.append(dict(context=context,path=name,sha256=h,route='inherited_complete_public_transport',documentary=r['transport'].endswith('HASH_ONLY')));return
  r=legacy_literals.get((name,h))
  if r and matches(r,x):audit.append(dict(context=context,path=name,sha256=h,route='inherited_literal_documentary_namespace',documentary=r['transport'].endswith('HASH_ONLY')));return
  loc=legacy_locators.get((context,name,h))
  if loc:
   r=legacy.get((loc['resolved_origin'],loc['resolved_path'],h))
   need(r is not None and matches(r,x),'Exact inherited historical locator target')
   audit.append(dict(context=context,path=name,sha256=h,route='inherited_explicit_locator',documentary=r['transport'].endswith('HASH_ONLY')));return
  unresolved.append(dict(context=context,pin=x))
 def walk(x,context):
  if isinstance(x,dict):
   resolve(x,context)
   for k,v in x.items():
    if isinstance(k,str)and k.startswith('/')and isinstance(v,str)and len(v)==64:resolve(dict(path=k,sha256=v),context)
    if k!='exports':walk(v,context)
  elif isinstance(x,list):
   for v in x:walk(v,context)
 for key,p in seen.items():
  if key[0]=='study'and p.suffix=='.json':
   try:j=load(p)
   except(ValueError,UnicodeError):continue
   walk(j,key[1])
 save(out/'metadata_binding_audit.json',dict(resolved=audit,unresolved=unresolved));need(not unresolved,'Unresolved exact metadata; inspect retained audit')
 principal=roots['study']/'corpus106_N010_principal_v2';bindings=load(principal/'dependencies.json');need(len(bindings)==5777,'Complete principal direct bindings')
 for r in bindings:direct((r['namespace'],r['path']),r)
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
 cmd=[sys.executable,str(adapter),'--study',str(roots['study']),'--author',str(principal),'--out',str(out/'application')]
 with(out/'application.stdout').open('wb')as so,(out/'application.stderr').open('wb')as se:
  p=subprocess.Popen(cmd,cwd=out,env=env,stdout=so,stderr=se);save(out/'active.json',dict(status='RUNNING',pid=p.pid,cap_seconds=120))
  try:code=p.wait(timeout=120)
  except subprocess.TimeoutExpired:p.kill();p.wait();save(out/'active.json',dict(status='TERMINAL_TIMEOUT_NO_CERTIFICATE'));raise ValueError('Capped application incomplete')
 save(out/'active.json',dict(status='TERMINAL',returncode=code));need(code==0 and not(out/'application.stderr').read_bytes(),'Application failed; exact stdout/stderr retained')
 application=load(out/'application/report.json');need(application['status']=='PASS_PUBLIC_N010_APPLICATION'and len(application['damaged_controls'])==17 and len(application['optimization_guards'])==4 and application['native_pages']==11 and application['full_reading_volume_pages']==22,'Complete exact application scope')
 guards=[]
 for mode in ['argument','environment']:
  e=dict(env);cmd=[sys.executable]+(['-O']if mode=='argument'else[])+[str(Path(__file__).resolve())]
  if mode=='environment':e['PYTHONOPTIMIZE']='1'
  p=subprocess.run(cmd,env=e,capture_output=True,timeout=15);need(p.returncode!=0 and b'Unoptimized Python required'in p.stderr,'Pre-output portable guard');guards.append(mode)
 final={}
 for key,p in seen.items():
  ident=p.stat().st_ino
  if ident not in final:final[ident]=p.stat().st_size,sha(p)
  need(final[ident]==(rows[key]['bytes'],rows[key]['sha256']),'Restored scientific bytes remain unchanged')
 report=dict(status='PASS_PUBLIC_N010_COMPLETE_SURVEY_CLOSURE',checker_sha256=sha(Path(__file__)),transport_sha256=sha(tp),policy_sha256=sha(pp),adapter_sha256=sha(adapter),
 logical_records=len(rows),restored_files=len(seen),distinct_decoded_payloads=len(decoded),stored_payloads_verified=len(stored),private_packets=len(t['packets']),private_exports=exports,
 inherited_logical_records=legacy_rows,inherited_decoded_payloads=len(legacy_decoded),inherited_documentary_records=legacy_documents,principal_dependency_pins=len(bindings),
 metadata_pins_checked=len(audit),metadata_documentary_pins=sum(r['documentary']for r in audit),direct_documentary_omissions=15,
 malformed_transport_controls=controls,portable_optimization_guards=guards,application=application,
 application_stdout_sha256=sha(out/'application.stdout'),application_stderr_empty=True,native_pages=11,private_proof_fallback=False,
 acquired_censuses_repeated=False,mathematical_review_replaced_by_hashes=False,new_Lean=0,new_measurements=0,new_question_credit=0,whole_original_credit=0,seconds=time.monotonic()-start)
 save(out/'report.json',report);print(json.dumps(report))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--payload',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--expected-transport',required=True);p.add_argument('--expected-policy',required=True);p.add_argument('--expected-adapter',required=True);main(p.parse_args())
