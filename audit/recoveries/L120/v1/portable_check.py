"""Public-only restoration and bounded replay of the accepted L120 synthesis.

All upstream articles and their raster/text copies remain explicit hash-only
attribution. Complete acquired proof/certificate packets are restored unchanged.
Existing public admissions are retained boundaries, not new mathematical claims.
"""
import sys
if sys.flags.optimize:raise RuntimeError('Unoptimized Python required')
from pathlib import Path,PurePosixPath
import argparse,collections,copy,gzip,hashlib,json,os,shutil,subprocess,time
BASE='audit/recoveries/L120/v1'
HISTORICAL='/Users/sasha/medusa/research/leemans/'
PUBLIC='/Users/sasha/medusa/math_compression/'
AUTHOR='corpus106_L120_principal_v2/manifest.json'
AUTHOR_HASH='b5860c241cb773ae005ba412237f5b30220f7c045f5c90e21a35f2f133cc7831'
REVIEW='corpus106_L120_principal_root_review/manifest.json'
REVIEW_HASH='2478f1609c3ff05aec7ca856c44190042bafcaf169b118266a2f9bea40e09543'
def need(c,m):
 if not c:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def child(root,name):
 need(isinstance(name,str)and name,'Empty relative path');q=PurePosixPath(name);need(not q.is_absolute()and'..'not in q.parts,'Unsafe relative path');p=(root/q).resolve();need(p.is_relative_to(root.resolve()),'Path escapes root');return p
def structure(t,policy):
 for k in('whole_original_credit','new_measurements','new_question_credit','new_Lean'):need(t[k]==0,'Transport cannot self-admit '+k)
 need(t['logical_files']==len(t['files'])==9979,'Exact logical inventory')
 keys=[(r['origin'],r['path'])for r in t['files']];need(len(keys)==len(set(keys)),'Duplicate logical file')
 need({x['origin']for x in t['files']}<={'study','public','repo','local_software_documentation'},'Unexpected namespace')
 omitted={(r['origin'],r['path'],r['bytes'],r['sha256'])for r in t['files']if r['transport'].endswith('HASH_ONLY')}
 expected={(r['origin'],r['path'],r['bytes'],r['sha256'])for r in policy['primary_sources_hash_only']}
 need(omitted==expected and t['primary_sources_hash_only']==policy['primary_sources_hash_only']and len(omitted)==61,'Exact documentary omissions')
 need(len(t['packets'])==503 and len({(p['origin'],p['path'])for p in t['packets']})==503,'Whole packet inventory')
 pm={(p['origin'],p['path']):p['sha256']for p in t['packets']}
 for p,h in[(AUTHOR,AUTHOR_HASH),(REVIEW,REVIEW_HASH)]:need(pm.get(('study',p))==h,'Required principal/review chain')
 for key in('legacy_common_aliases','historical_documentary_exceptions','relative_locator_resolutions','inherited_relative_locators','predecessor_transports'):
  need(t[key]==policy[key],'Exact documented boundary '+key)
 need(len(t['relative_locator_resolutions'])==460 and len(t['inherited_relative_locators'])==42,'Exact relative locators')
 need(sum(len(r['bindings'])for r in t['legacy_common_aliases'])==21,'Exact common aliases')
 need(collections.Counter(e['kind']for e in t['historical_documentary_exceptions'])=={'HISTORICAL_NATIVE_RENDER_CACHE_HASH_ONLY':169,'HISTORICAL_PRIMARY_SOURCE_RENDER_HASH_ONLY':51,'EXTERNAL_SOFTWARE_HASH_ONLY':22,'HISTORICAL_TYPESETTING_LOG_HASH_ONLY':1},'Exact historical exceptions')
 for r in t['files']:
  need(not r.get('public_path','').endswith('.md'),'Markdown restored only into temporary working tree')
  if not r['transport'].endswith('HASH_ONLY'):
   need(r['transport']in('EXISTING_PUBLIC','NEW_FROZEN_FILE'),'Unknown transport');need(r['encoding']in('identity','gzip'),'Unknown encoding');child(Path('/logical'),r['path']);child(Path('/public'),r['public_path'])
def main(a):
 start=time.monotonic();repo=a.repo.resolve();payload=a.payload.resolve()if a.payload else repo
 tp=child(payload,BASE+'/transport.json');need(sha(tp)==a.expected_transport,'Exact frozen transport');t=load(tp)
 policy_path=child(payload,BASE+'/portable_policy.json');need(sha(policy_path)==a.expected_policy,'Exact source and historical boundary policy');policy=load(policy_path);structure(t,policy)
 controls=[]
 mutations=[('duplicate',lambda x:x['files'].__setitem__(1,copy.deepcopy(x['files'][0]))),('credit',lambda x:x.__setitem__('whole_original_credit',1)),('omit_proof',lambda x:next(r for r in x['files']if r['path']=='corpus106_L120_principal_v2/survey.tex').__setitem__('transport','PRIVATE_PRIMARY_SOURCE_HASH_ONLY')),('packet_missing',lambda x:x['packets'].pop()),('review_changed',lambda x:next(p for p in x['packets']if p['path']==REVIEW).__setitem__('sha256','0'*64)),('namespace',lambda x:x['files'][0].__setitem__('origin','private_fallback')),('alias_missing',lambda x:x['legacy_common_aliases'][0]['bindings'].pop()),('exception_missing',lambda x:x['historical_documentary_exceptions'].pop()),('locator_missing',lambda x:x['relative_locator_resolutions'].pop()),('unsafe_path',lambda x:next(r for r in x['files']if not r['transport'].endswith('HASH_ONLY')).__setitem__('path','../escape')),('source_omission_changed',lambda x:x['primary_sources_hash_only'].pop())]
 for name,fn in mutations:
  v=copy.deepcopy(t);fn(v)
  try:structure(v,policy)
  except(ValueError,KeyError):controls.append(name)
  else:raise ValueError('Malformed transport accepted '+name)
 need(not a.out.exists(),'Fresh output directory');a.out.mkdir(parents=True);out=a.out.resolve();study=out/'restored/study';public=out/'restored/repo';cache=out/'payloads';study.mkdir(parents=True);public.mkdir();cache.mkdir()
 rowmap={(r['origin'],r['path']):r for r in t['files']};roots={'study':study,'public':public,'repo':public};seen={};decoded={};stored_verified={}
 for r in t['files']:
  key=(r['origin'],r['path'])
  if r['transport'].endswith('HASH_ONLY'):continue
  source=child(repo if r['transport']=='EXISTING_PUBLIC'else payload,r['public_path']);stored=(r['stored_bytes'],r['stored_sha256'])
  if source not in stored_verified:need(source.is_file()and source.stat().st_size==stored[0]and sha(source)==stored[1],'Stored payload changed '+str(source));stored_verified[source]=stored
  else:need(stored_verified[source]==stored,'Conflicting public payload')
  identity=(r['bytes'],r['sha256']);dest=child(roots[r['origin']],r['path'])
  if identity not in decoded:
   target=cache/r['sha256'];opener=gzip.open if r['encoding']=='gzip'else open
   with opener(source,'rb')as inf,target.open('wb')as outf:shutil.copyfileobj(inf,outf)
   need(target.stat().st_size==r['bytes']and sha(target)==r['sha256'],'Decoded payload changed');decoded[identity]=target
  dest.parent.mkdir(parents=True,exist_ok=True)
  if dest.exists():need(dest.stat().st_size==r['bytes']and sha(dest)==r['sha256'],'Namespace collision differs')
  else:os.link(decoded[identity],dest)
  seen[key]=dest
 print('RESTORED',len(seen),len(decoded),flush=True)
 omitted={(r['origin'],r['path']):r for r in t['primary_sources_hash_only']}
 def verify_path(p,row):
  origin='study'if p.is_relative_to(study)else'public'if p.is_relative_to(public)else None
  need(origin is not None,'Pinned path outside restored namespaces');relative=str(p.relative_to(study if origin=='study'else public));key=(origin,relative)
  if key in omitted:
   old=omitted[key];need(row['sha256']==old['sha256']and row.get('bytes',old['bytes'])==old['bytes'],'Documentary binding changed');return
  need(p.is_file()and sha(p)==row['sha256']and row.get('bytes',p.stat().st_size)==p.stat().st_size,'Pinned file missing or changed '+str(p))
 exports=0
 for pk in t['packets']:
  p=child(roots[pk['origin']],pk['path']);need(sha(p)==pk['sha256'],'Packet manifest changed');m=load(p);need(len(m['exports'])==pk['exports'],'Complete exports')
  for row in m['exports']:verify_path(child(p.parent,row['path']),row);exports+=1
 principal=study/'corpus106_L120_principal_v2';deps=load(principal/'dependencies.json')['files'];need(len(deps)==4306,'Complete principal dependency list')
 for row in deps:verify_path(child(roots[row['namespace']],row['path']),row)
 acquired=load(principal/'acquired_roots.json');need(len(acquired)==38,'Immediate mathematical roots')
 locators=t['inherited_relative_locators']+t['relative_locator_resolutions']
 for r in locators:
  target=seen[(r['resolved_origin'],r['resolved_path'])];old=r['historical_pin'];need(sha(target)==old['sha256']and old.get('bytes',target.stat().st_size)==target.stat().st_size,'Relative locator changed')
 for alias in t['legacy_common_aliases']:
  for r in alias['bindings']:
   p=child(study,r['expected']);need(p.is_file()and sha(p)==r['sha256'],'Exact common alias')
 # Every predecessor logical identity and packet is preserved. No former
 # mathematical census is rerun or re-admitted by this packaging operation.
 prior_keys=set();prior_packets=set()
 for predecessor in t['predecessor_transports']:
  p=child(public,predecessor['path']);verify_path(p,predecessor);old=load(p)
  for r in old['files']:
   key=(r['origin'],r['path']);now=rowmap[key];need((r['sha256'],r['bytes'])==(now['sha256'],now['bytes']),'Prior logical bytes preserved');prior_keys.add(key)
  for r in old['packets']:need(r in t['packets'],'Whole prior packet closure');prior_packets.add((r['origin'],r['path']))
 # Literal dependency references in all newly acquired private JSON are paid
 # by their actual logical identity or an explicit same-byte locator. Already
 # accepted public metadata is an explicit boundary, not a recursive audit of
 # unrelated former catalogue/measurement snapshots.
 locator_map={(r['context'].removeprefix(HISTORICAL),r['historical_pin']['path'],r['historical_pin']['sha256']):r for r in locators}
 counts=[0,0];audited=[]
 def literal_pin(obj,context):
  name=obj.get('path');h=obj.get('sha256')
  if not isinstance(name,str)or not isinstance(h,str)or len(h)!=64:return
  candidates=[]
  if name.startswith(HISTORICAL):candidates.append(('study',name.removeprefix(HISTORICAL)))
  elif name.startswith(PUBLIC):candidates.extend([('public',name.removeprefix(PUBLIC)),('repo',name.removeprefix(PUBLIC))])
  elif not Path(name).is_absolute():
   origin=obj.get('namespace',obj.get('origin'))
   if origin in('study','public','repo'):candidates.append((origin,name))
   candidates.extend([('study',name),('public',name),('repo',name),('study',str(PurePosixPath(context).parent/PurePosixPath(name)))])
  for key in candidates:
   r=rowmap.get(key)
   if r and r['sha256']==h and obj.get('bytes',r['bytes'])==r['bytes']:counts[0]+=1;counts[1]+=r['transport'].endswith('HASH_ONLY');return
  locator=locator_map.get((context,name,h))
  if locator:
   q=seen[(locator['resolved_origin'],locator['resolved_path'])];need(sha(q)==h and obj.get('bytes',q.stat().st_size)==q.stat().st_size,'Historical exact locator changed');counts[0]+=1;return
  raise ValueError('Unresolved new exact metadata pin '+context+' -> '+name)
 def audit_json(obj,context):
  if isinstance(obj,dict):
   literal_pin(obj,context)
   for k,v in obj.items():
    if isinstance(k,str)and k.startswith('/')and isinstance(v,str)and len(v)==64:literal_pin({'path':k,'sha256':v},context)
    if k!='exports':audit_json(v,context)
  elif isinstance(obj,list):
   for v in obj:audit_json(v,context)
 for key,p in seen.items():
  if key[0]=='study'and key not in prior_keys and p.suffix=='.json':
   try:j=load(p)
   except(ValueError,UnicodeError):continue
   audit_json(j,key[1]);audited.append(key[1])
 save(out/'new_metadata_audit.json',{'files':audited,'literal_pins':counts[0],'documentary_pins':counts[1]})
 routes=load(principal/'source_map.json');need(routes['original']=='L120'and len(routes['retained_assertions'])==7 and len(routes['acquired_or_corrected_assertions'])==25 and len(routes['corrections'])==8,'Exact source contract')
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
 adapter=child(payload,BASE+'/application_replay.py');need(sha(adapter)==a.expected_adapter,'Explicit frozen adapter')
 cmd=[sys.executable,str(adapter),'--study',str(study),'--author',str(principal),'--out',str(out/'application')]
 with(out/'application.stdout').open('wb')as stdout,(out/'application.stderr').open('wb')as stderr:
  proc=subprocess.Popen(cmd,cwd=out,env=env,stdout=stdout,stderr=stderr);save(out/'active.json',{'status':'RUNNING','label':'unchanged_mathematical_code_explicit_public_adapter','pid':proc.pid,'cap_seconds':120})
  try:code=proc.wait(timeout=120)
  except subprocess.TimeoutExpired:proc.kill();proc.wait();raise ValueError('Application capped without certificate')
 need(code==0 and not(out/'application.stderr').read_bytes(),'Fresh application replay; inspect retained stdout/stderr')
 application=load(out/'application/report.json');need(application['status']=='PASS_PUBLIC_L120_APPLICATION'and application['damaged_controls']==6 and application['optimization_guards']==6 and application['native_pages']==9,'Exact application scope')
 need(not application['primary_source_replayed']and not application['new_census'],'No private source or census fallback')
 guards=[]
 for label,cmd,e in [('argument',[sys.executable,'-O',str(Path(__file__).resolve())],env),('environment',[sys.executable,str(Path(__file__).resolve())],dict(env,PYTHONOPTIMIZE='1'))]:
  r=subprocess.run(cmd,env=e,capture_output=True,timeout=15);need(r.returncode!=0 and b'Unoptimized Python required'in r.stderr,'Portable optimization guard');guards.append(label)
 # Hard-linked identities are rehashed once after application execution; every
 # logical restored name must retain its precise identity.
 final_hashes={}
 for key,p in seen.items():
  ident=(p.stat().st_dev,p.stat().st_ino)
  if ident not in final_hashes:final_hashes[ident]=(p.stat().st_size,sha(p))
  need(final_hashes[ident]==(rowmap[key]['bytes'],rowmap[key]['sha256']),'Restored input mutated')
 result=dict(status='PASS_PUBLIC_L120_COMPLETE_CLOSURE',checker_sha256=sha(Path(__file__)),transport_sha256=sha(tp),policy_sha256=sha(policy_path),adapter_sha256=sha(adapter),logical_records=len(t['files']),restored_files=len(seen),distinct_decoded_payloads=len(decoded),stored_payloads_verified=len(stored_verified),acquired_packets=len(t['packets']),acquired_exports=exports,immediate_mathematical_roots=len(acquired),new_metadata_json=len(audited),exact_metadata_pins_checked=counts[0],documentary_metadata_pins_acquired=counts[1],historical_exceptions=len(t['historical_documentary_exceptions']),documentary_omissions=len(omitted),relative_locators=len(locators),malformed_transport_controls=controls,portable_optimization_guards=guards,application=application,application_stdout_sha256=sha(out/'application.stdout'),application_stderr_empty=True,native_pages=9,native_text_identical=True,private_proof_fallback=False,mathematical_census_repeated=False,mathematical_review_replaced_by_hashes=False,new_Lean=0,new_measurements=0,new_question_credit=0,whole_original_credit=0,seconds=time.monotonic()-start)
 save(out/'report.json',result);save(out/'active.json',{'status':'TERMINAL','returncode':0});print(json.dumps(result))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--payload',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--expected-transport',required=True);p.add_argument('--expected-policy',required=True);p.add_argument('--expected-adapter',required=True);main(p.parse_args())
