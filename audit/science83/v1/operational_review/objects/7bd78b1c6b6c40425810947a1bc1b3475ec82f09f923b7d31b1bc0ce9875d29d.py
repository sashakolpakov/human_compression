"""Public-only exact L052 closure and bounded assembly replay.

Documentary originals are hash-only. Every scientific proof, numerical input,
program, receipt and review is restored from exact public bytes. No private
filesystem or text-patched author program is used by the replay.
"""
import sys
if sys.flags.optimize:raise RuntimeError('Unoptimized Python required')
sys.dont_write_bytecode=True
from pathlib import Path,PurePosixPath
import argparse,copy,gzip,hashlib,json,os,shutil,subprocess,time
BASE='audit/recoveries/L052/v1'
ACCEPT={'corpus106_L052_principal_v1/manifest.json': 'b049a901a2bd38852fad99b636a70575617306c8aee3c5c37c1bda5d91f4ae1d', 'corpus106_L052_principal_independent_review/manifest.json': '9a8105bfe4e0b0a26c8acd02f6778ab01f584c55f091eeb86371dc4d6dfe1cc6', 'corpus106_L052_principal_root_adoption/manifest.json': '1eb788b4facfdcdd3d0bebd8e43669fde6c599e73f7cb38eddd2cf29f336f687'}
def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def child(root,name):
 need(isinstance(name,str)and name,'Empty relative name');n=PurePosixPath(name);need(not n.is_absolute()and'..'not in n.parts,'Unsafe relative name');p=(root/n).resolve();need(p.is_relative_to(root.resolve()),'Escaping path');return p
def structure(t,policy):
 for k in ['whole_original_credit','new_measurements','new_question_credit','new_Lean']:need(t[k]==0,'No credit from transport')
 need(t['logical_files']==len(t['files'])==policy['logical_files'],'Exact logical closure')
 keys=[(r['origin'],r['path'])for r in t['files']];need(len(set(keys))==len(keys),'Unique logical identities')
 need(len(t['packets'])==policy['packets'] and sum(p['exports']for p in t['packets'])==policy['complete_manifest_exports'],'Complete manifests')
 pm={(p['origin'],p['path']):p['sha256']for p in t['packets']};need(len(pm)==len(t['packets']),'Unique packets')
 for p,h in ACCEPT.items():need(pm.get(('study',p))==h,'Exact accepted author/review/adoption')
 for k in ['primary_sources_hash_only','relative_locator_resolutions','historical_documentary_exceptions','legacy_common_aliases','inherited_relative_locators','predecessor_transports','historical_absolute_roots','mathematical_acceptance']:need(t[k]==policy[k],'Exact declared policy '+k)
 omitted={(r['origin'],r['path'],r['bytes'],r['sha256'],r['transport'])for r in t['files']if r['transport'].endswith('HASH_ONLY')};expected={(r['origin'],r['path'],r['bytes'],r['sha256'],r['reason'])for r in policy['primary_sources_hash_only']};need(omitted==expected and len(omitted)==14,'Only exact documentary assets omitted')
 for r in t['files']:
  need(r['origin']in ['study','public','gap'],'Explicit namespace');child(Path('/logical'),r['path'])
  if r['transport'].endswith('HASH_ONLY'):continue
  need(r['transport']in ['EXISTING_PUBLIC','NEW_FROZEN_FILE']and r['encoding']in ['identity','gzip'],'Exact transport mode');child(Path('/public'),r['public_path']);need(not r['public_path'].endswith(('.md','.pyc')),'No new public Markdown/bytecode path')
def main(a):
 start=time.monotonic();repo=a.repo.resolve();payload=a.payload.resolve()if a.payload else repo;tp=child(payload,BASE+'/transport.json');pp=child(payload,BASE+'/portable_policy.json');need(sha(tp)==a.expected_transport and sha(pp)==a.expected_policy,'Exact transport/policy');t=load(tp);policy=load(pp);structure(t,policy)
 mutations=[('duplicate',lambda x:x['files'].__setitem__(1,copy.deepcopy(x['files'][0]))),('credit',lambda x:x.__setitem__('whole_original_credit',1)),('missing_packet',lambda x:x['packets'].pop()),('review_pin',lambda x:next(p for p in x['packets']if p['path']=='corpus106_L052_principal_v1/manifest.json').__setitem__('sha256','0'*64)),('proof_as_document',lambda x:next(r for r in x['files']if r['path']=='corpus106_L052_principal_v1/principal.tex').__setitem__('transport','PRIMARY_SOURCE_HASH_ONLY')),('missing_locator',lambda x:x['relative_locator_resolutions'].pop()),('missing_document',lambda x:x['primary_sources_hash_only'].pop()),('unsafe_path',lambda x:x['files'][0].__setitem__('path','../escape')),('private_namespace',lambda x:x['files'][0].__setitem__('origin','private'))]
 controls=[]
 for n,fn in mutations:
  bad=copy.deepcopy(t);fn(bad)
  try:structure(bad,policy)
  except(ValueError,KeyError):controls.append(n)
  else:raise ValueError('Malformed transport accepted '+n)
 need(not a.out.exists(),'Fresh external output');a.out.mkdir(parents=True);out=a.out.resolve();roots={k:out/'restored'/k for k in ['study','public','gap']};cache=out/'payloads';cache.mkdir()
 for p in roots.values():p.mkdir(parents=True)
 rows={(r['origin'],r['path']):r for r in t['files']};seen={};decoded={};stored={}
 for key,r in rows.items():
  if r['transport'].endswith('HASH_ONLY'):continue
  source=child(repo if r['transport']=='EXISTING_PUBLIC'else payload,r['public_path']);identity=r['bytes'],r['sha256'];wanted=r['stored_bytes'],r['stored_sha256']
  if source not in stored:need(source.is_file()and(source.stat().st_size,sha(source))==wanted,'Stored bytes '+str(source));stored[source]=wanted
  else:need(stored[source]==wanted,'Conflicting storage identity')
  if identity not in decoded:
   q=cache/r['sha256'];data=source.read_bytes();data=gzip.decompress(data)if r['encoding']=='gzip'else data;need((len(data),hashlib.sha256(data).hexdigest())==identity,'Exact decoded scientific bytes');q.write_bytes(data);decoded[identity]=q
  p=child(roots[r['origin']],r['path']);p.parent.mkdir(parents=True,exist_ok=True);os.link(decoded[identity],p);seen[key]=p
 print('RESTORED',len(seen),len(decoded),flush=True)
 def verify_key(key,row):
  if Path(key[1]).is_absolute():
   hits=[(k,key[1][len(prefix):])for k,prefix in t['historical_absolute_roots'].items()if key[1].startswith(prefix)]
   need(len(hits)==1,'Unknown absolute historical export');key=hits[0]
  r=rows.get(key);need(r is not None and r['sha256']==row['sha256']and row.get('bytes',r['bytes'])==r['bytes'],'Missing/changed logical binding '+str(key))
  if not r['transport'].endswith('HASH_ONLY'):need(key in seen,'Not restored')
 locators={(r['context'],r['historical_pin']['path'],r['historical_pin']['sha256']):r for r in t['relative_locator_resolutions']}
 exports=0
 for pk in t['packets']:
  key=pk['origin'],pk['path'];p=seen[key];need(sha(p)==pk['sha256'],'Exact packet manifest');m=load(p);need(len(m['exports'])==pk['exports'],'Complete packet exports')
  for row in m['exports']:
   literal_key=(pk['origin'],str(PurePosixPath(pk['path']).parent/PurePosixPath(row['path'])))
   actual=rows.get(literal_key)
   if actual and actual['sha256']==row['sha256'] and row.get('bytes',actual['bytes'])==actual['bytes']:verify_key(literal_key,row)
   else:
    loc=locators.get((pk['path'],row['path'],row['sha256']));need(loc is not None,'Historical export needs explicit exact locator');verify_key((loc['resolved_origin'],loc['resolved_path']),row)
   exports+=1
 locators={(r['context'],r['historical_pin']['path'],r['historical_pin']['sha256']):r for r in t['relative_locator_resolutions']};counts=[0,0];audited=[]
 def literal(x,context):
  name=x.get('path');h=x.get('sha256')
  if not isinstance(name,str)or not isinstance(h,str)or len(h)!=64:return
  candidates=[]
  for k,prefix in t['historical_absolute_roots'].items():
   if name.startswith(prefix):candidates.append((k,name[len(prefix):]))
  if not Path(name).is_absolute():
   ns=x.get('namespace',x.get('origin'))
   if ns in roots:candidates.append((ns,name))
   candidates.extend([(k,name)for k in roots]);candidates.append(('study',str(PurePosixPath(context).parent/PurePosixPath(name))))
  for key in candidates:
   r=rows.get(key)
   if r and r['sha256']==h and x.get('bytes',r['bytes'])==r['bytes']:verify_key(key,x);counts[0]+=1;counts[1]+=r['transport'].endswith('HASH_ONLY');return
  loc=locators.get((context,name,h))
  if loc:verify_key((loc['resolved_origin'],loc['resolved_path']),x);counts[0]+=1;return
  raise ValueError('Unresolved exact metadata '+context+' -> '+name)
 def walk(x,context):
  if isinstance(x,dict):
   literal(x,context)
   for k,v in x.items():
    if isinstance(k,str)and k.startswith('/')and isinstance(v,str)and len(v)==64:literal(dict(path=k,sha256=v),context)
    if k!='exports':walk(v,context)
  elif isinstance(x,list):
   for v in x:walk(v,context)
 for key,p in seen.items():
  if key[0]=='study'and p.suffix=='.json':
   try:j=load(p)
   except(ValueError,UnicodeError):continue
   walk(j,key[1]);audited.append(key[1])
 principal=roots['study']/'corpus106_L052_principal_v1';bindings=load(principal/'dependencies.json');need(len(bindings)==644,'Complete principal bindings')
 for r in bindings:verify_key((r['namespace'],r['path']),r)
 for r in t['relative_locator_resolutions']:verify_key((r['resolved_origin'],r['resolved_path']),r['historical_pin'])
 save(out/'new_metadata_audit.json',dict(files=audited,literal_pins=counts[0],documentary_pins=counts[1]))
 adapter=child(payload,BASE+'/application_replay.py');need(sha(adapter)==a.expected_adapter,'Exact explicit adapter');env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1';cmd=[sys.executable,str(adapter),'--study',str(roots['study']),'--author',str(principal),'--out',str(out/'application')]
 with(out/'application.stdout').open('wb')as so,(out/'application.stderr').open('wb')as se:
  p=subprocess.Popen(cmd,cwd=out,env=env,stdout=so,stderr=se);save(out/'active.json',dict(status='RUNNING',pid=p.pid,cap_seconds=120))
  try:code=p.wait(timeout=120)
  except subprocess.TimeoutExpired:p.kill();p.wait();raise ValueError('Application deadline without certificate')
 need(code==0 and not(out/'application.stderr').read_bytes(),'Fresh application failed; retained stdout/stderr');application=load(out/'application/report.json');need(application['status']=='PASS_PUBLIC_L052_APPLICATION'and len(application['damaged_controls'])==13 and len(application['optimization_guards'])==6 and application['native_pages']==5 and application['full_reading_volume_pages']==18,'Exact complete application scope')
 guards=[]
 for mode in ['argument','environment']:
  e=dict(env);cmd=[sys.executable]+(['-O']if mode=='argument'else[])+[str(Path(__file__).resolve())]
  if mode=='environment':e['PYTHONOPTIMIZE']='1'
  p=subprocess.run(cmd,env=e,capture_output=True,timeout=15);need(p.returncode!=0 and b'Unoptimized Python required'in p.stderr,'Portable optimization guard');guards.append(mode)
 final={}
 for key,p in seen.items():
  k=p.stat().st_ino
  if k not in final:final[k]=p.stat().st_size,sha(p)
  need(final[k]==(rows[key]['bytes'],rows[key]['sha256']),'Restored scientific bytes mutated')
 result=dict(status='PASS_PUBLIC_L052_COMPLETE_CLOSURE',checker_sha256=sha(Path(__file__)),transport_sha256=sha(tp),policy_sha256=sha(pp),adapter_sha256=sha(adapter),logical_records=len(rows),restored_files=len(seen),distinct_decoded_payloads=len(decoded),stored_payloads_verified=len(stored),acquired_packets=len(t['packets']),acquired_exports=exports,principal_dependency_pins=len(bindings),exact_metadata_pins_checked=counts[0],documentary_metadata_pins_acquired=counts[1],documentary_omissions=14,relative_locators=len(t['relative_locator_resolutions']),malformed_transport_controls=controls,portable_optimization_guards=guards,application=application,application_stdout_sha256=sha(out/'application.stdout'),application_stderr_empty=True,native_pages=5,native_text_identical=True,private_proof_fallback=False,mathematical_census_repeated=False,mathematical_review_replaced_by_hashes=False,new_Lean=0,new_measurements=0,new_question_credit=0,whole_original_credit=0,seconds=time.monotonic()-start)
 save(out/'report.json',result);save(out/'active.json',dict(status='TERMINAL',returncode=0));print(json.dumps(result))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--payload',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--expected-transport',required=True);p.add_argument('--expected-policy',required=True);p.add_argument('--expected-adapter',required=True);main(p.parse_args())
