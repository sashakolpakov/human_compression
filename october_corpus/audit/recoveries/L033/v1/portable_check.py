"""Restore the complete L033 proof closure from public payloads only."""
import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,copy,gzip,hashlib,json,os,subprocess,time
from pathlib import Path,PurePosixPath
B='audit/recoveries/L033/v1';A='algebra/coxeter_quotients/principal_v1';REVIEW='algebra/coxeter_quotients/principal_review_v1/manifest.json'
ROOTS=[(A+'/manifest.json','3e72fe3b8bcaad6c315a9cf9c32cd64dd3b5e101b9024889cebf99c738d9cbfc'),(REVIEW,'cfde0cdbf82f655eeda8cf9ccb6a036cf3f0293f02cb616a6c493f984863e25b')]
def need(x,s):
 if not x:raise ValueError(s)
def read(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def child(root,relative):
 p=PurePosixPath(relative);need(relative and not p.is_absolute() and '..' not in p.parts,'Unsafe relative path');q=(root/relative).resolve();need(q.is_relative_to(root.resolve()),'Escaping path');return q
def structure(t,p):
 need(t['logical_files']==len(t['files'])==p['logical_files']==2928,'Exact inventory')
 keys=[(r['origin'],r['path']) for r in t['files']];need(len(set(keys))==len(keys),'Duplicate logical name')
 need(len(t['packets'])==p['packets']==43 and sum(x['exports'] for x in t['packets'])==p['exports'],'Complete packet inventory')
 for k in ('roots','relative_locators','public_boundaries','documentary_boundaries','historical_roots','git_baseline','documentary_and_runtime_hash_only'):need(t[k]==p[k],'Exact policy '+k)
 need(t['roots']==[list(x) for x in ROOTS],'Exact acceptance roots')
 pm={(r['origin'],r['path']):r['sha256'] for r in t['packets']}
 for path,h in ROOTS:need(pm.get(('study',path))==h,'Exact complete principal/review')
 need(all(t[k]==0 for k in ('whole_original_credit','new_measurements','new_question_credit','new_Lean')),'No transport credit')
 omitted=[{k:r[k] for k in ('origin','path','bytes','sha256','transport')} for r in t['files'] if r['transport'].endswith('HASH_ONLY')];need(omitted==p['documentary_and_runtime_hash_only'] and len(omitted)==103,'Exact documentary/runtime boundary')
 for r in t['files']:
  need(r['origin'] in ('study','public','runtime'),'Known namespace');child(Path('/safe'),r['path'].lstrip('/') if r['origin']=='runtime' else r['path'])
  if r['transport'].endswith('HASH_ONLY'):continue
  need(r['transport'] in ('EXISTING_PUBLIC','NEW_FROZEN_FILE') and r['encoding'] in ('identity','gzip'),'Exact storage kind');child(Path('/safe'),r['public_path']);need(not r['public_path'].endswith(('.md','.pyc')),'Safe public file extension')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--payload',type=Path);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--expected-transport',required=True);ap.add_argument('--expected-policy',required=True);ap.add_argument('--expected-adapter',required=True);a=ap.parse_args();repo=a.repo.resolve();payload=(a.payload or a.repo).resolve();O=a.out.resolve();tp=child(payload,B+'/transport.json');pp=child(payload,B+'/portable_policy.json');adapter=child(payload,B+'/application_replay.py')
 need(sha(tp)==a.expected_transport and sha(pp)==a.expected_policy and sha(adapter)==a.expected_adapter,'Exact operational bytes');t=read(tp);p=read(pp);structure(t,p)
 damages=[]
 changes=[('duplicate',lambda x:x['files'].__setitem__(1,copy.deepcopy(x['files'][0]))),('credit',lambda x:x.__setitem__('whole_original_credit',1)),('missing_packet',lambda x:x['packets'].pop()),('wrong_review',lambda x:next(z for z in x['packets'] if z['path']==REVIEW).__setitem__('sha256','0'*64)),('omitted_proof',lambda x:next(z for z in x['files'] if z['path']==A+'/principal.tex').__setitem__('transport','DOCUMENTARY_SOURCE_HASH_ONLY')),('missing_locator',lambda x:x['relative_locators'].pop()),('missing_boundary',lambda x:x['public_boundaries'].pop()),('missing_provenance',lambda x:x['documentary_boundaries'].pop()),('runtime_omission',lambda x:x['documentary_and_runtime_hash_only'].pop()),('unsafe_path',lambda x:next(z for z in x['files'] if z['origin']=='study').__setitem__('path','../escape')),('namespace',lambda x:x['files'][0].__setitem__('origin','private')),('unsafe_storage',lambda x:next(z for z in x['files'] if 'public_path' in z).__setitem__('public_path','../escape'))]
 for label,fn in changes:
  v=copy.deepcopy(t);fn(v)
  try:structure(v,p)
  except (ValueError,KeyError):damages.append(label)
  else:raise ValueError('Malformed transport accepted '+label)
 need(not O.exists(),'Fresh output');O.mkdir(parents=True);start=time.monotonic();roots={k:O/'restored'/k for k in ('study','public','runtime')}
 for q in roots.values():q.mkdir(parents=True)
 def logical(origin,name):return child(roots[origin],name.lstrip('/') if origin=='runtime' else name)
 tracked=set(subprocess.check_output(['git','-C',str(repo),'ls-files','-z']).decode().split('\0'))
 bykey={(r['origin'],r['path']):r for r in t['files']};seen={};decoded={};stored={};cache=O/'decoded';cache.mkdir()
 for r in t['files']:
  if r['transport'].endswith('HASH_ONLY'):continue
  if r['transport']=='EXISTING_PUBLIC':need(r['public_path'] in tracked,'Reused payload must exist in a clean checkout')
  src=child(repo if r['transport']=='EXISTING_PUBLIC' else payload,r['public_path']);ident=(r['bytes'],r['sha256'])
  if str(src) not in stored:need(src.stat().st_size==r['stored_bytes'] and sha(src)==r['stored_sha256'],'Stored public payload');stored[str(src)]=(r['stored_bytes'],r['stored_sha256'])
  else:need(stored[str(src)]==(r['stored_bytes'],r['stored_sha256']),'Conflicting stored identity')
  if ident not in decoded:
   b=src.read_bytes();b=gzip.decompress(b) if r['encoding']=='gzip' else b;need((len(b),hashlib.sha256(b).hexdigest())==ident,'Decoded exact bytes');q=cache/r['sha256'];q.write_bytes(b);decoded[ident]=q
  dest=logical(r['origin'],r['path']);dest.parent.mkdir(parents=True,exist_ok=True);os.link(decoded[ident],dest);seen[r['origin'],r['path']]=dest
 print('RESTORED',len(seen),'UNIQUE',len(decoded),flush=True)
 def identity(name,namespace=None,context=None):
  if name.startswith(p['historical_roots']['study']):return [('study',name[len(p['historical_roots']['study']):])]
  if name.startswith(p['historical_roots']['public']):return [('public',name[len(p['historical_roots']['public']):])]
  if Path(name).is_absolute():return [('runtime',name)]
  choices=[]
  if namespace=='absolute':return identity('/'+name,context=context)
  if namespace in ('study','public','repo','runtime'):choices.append(('public' if namespace=='repo' else namespace,name))
  choices.extend([('study',name),('public',name)])
  if context:choices.append(('study',str(PurePosixPath(context).parent/name)))
  return choices
 locators={(x['context'].removeprefix(p['historical_roots']['study']),x['historical_pin']['path'],x['historical_pin']['sha256']):x for x in t['relative_locators']}
 counts=[0,0]
 def verify_pin(row,context=None):
  name=row['path'];h=row['sha256']
  for key in identity(name,row.get('namespace',row.get('origin')),context):
   z=bykey.get(key)
   if z and z['sha256']==h and z['bytes']==row.get('bytes',z['bytes']):counts[0]+=1;counts[1]+=z['transport'].endswith('HASH_ONLY');return
  loc=locators.get((context,name,h))
  if loc:
   z=bykey[loc['resolved_origin'],loc['resolved_path']];need(z['sha256']==h and z['bytes']==row.get('bytes',z['bytes']),'Literal historical alias');counts[0]+=1;return
  raise ValueError('Unresolved literal pin '+str(context)+' -> '+name)
 exports=0
 for pk in t['packets']:
  q=logical(pk['origin'],pk['path']);need(sha(q)==pk['sha256'],'Packet identity');m=read(q);need(len(m['exports'])==pk['exports'],'Complete packet exports')
  for row in m['exports']:
   name=row['path'];name=name if Path(name).is_absolute() else str(PurePosixPath(pk['path']).parent/name);verify_pin(dict(row,path=name),pk['path']);exports+=1
 principal=roots['study']/A;deps=read(principal/'dependencies.json');need(len(deps)==2391,'Exact principal closure')
 for r in deps:verify_pin(r,A+'/dependencies.json')
 boundary={(r.get('origin','public'),r['path'],r['sha256']) for r in t['public_boundaries']}
 special={(r['context'].removeprefix(p['historical_roots']['study']),r['field']):r for r in t['documentary_boundaries']}
 def walk(x,context):
  if isinstance(x,dict):
   if isinstance(x.get('path'),str) and isinstance(x.get('sha256'),str) and len(x['sha256'])==64 and all(c in '0123456789abcdef' for c in x['sha256']):verify_pin(x,context)
   for k,v in x.items():
    if k=='exports':continue
    if (context,k) in special:need(v==special[context,k]['value'],'Exact incidental checkpoint field');continue
    if isinstance(k,str) and k.startswith('/') and isinstance(v,str) and len(v)==64:verify_pin(dict(path=k,sha256=v),context)
    walk(v,context)
  elif isinstance(x,list):
   for v in x:walk(v,context)
 audited=[]
 for key,q in seen.items():
  r=bykey[key]
  if key[0]!='study' or q.suffix!='.json' or (*key,r['sha256']) in boundary:continue
  try:x=read(q)
  except (ValueError,UnicodeError):continue
  walk(x,key[1]);audited.append(key[1])
 save(O/'metadata_audit.json',dict(files=audited,pins=counts[0],documentary_or_runtime_pins=counts[1],previous_public_boundaries=len(boundary)))
 volume=child(payload,p['reading_volume']['path']);need(volume.stat().st_size==p['reading_volume']['bytes'] and sha(volume)==p['reading_volume']['sha256'],'Exact complete reading volume')
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1';cmd=[sys.executable,str(adapter),'--study',str(roots['study']),'--out',str(O/'application'),'--policy',str(pp),'--volume',str(volume)]
 with (O/'application.stdout').open('wb') as out,(O/'application.stderr').open('wb') as err:
  rc=None;deadline=False
  try:r=subprocess.run(cmd,stdout=out,stderr=err,env=env,timeout=180,cwd=O);rc=r.returncode
  except subprocess.TimeoutExpired:deadline=True
 save(O/'application.receipt.json',dict(command=cmd,cap_seconds=180,returncode=rc,deadline=deadline));need(rc==0 and not deadline and not (O/'application.stderr').stat().st_size,'Clean application replay; retain failure outputs')
 app=read(O/'application/report.json');need(app['status']=='PASS_PUBLIC_L033_PRINCIPAL_APPLICATION','Complete application')
 guards=[]
 for mode in ('argument','environment'):
  e=env.copy();cmd=[sys.executable]
  if mode=='argument':cmd.append('-O')
  else:e['PYTHONOPTIMIZE']='1'
  cmd.append(str(Path(__file__).resolve()));r=subprocess.run(cmd,capture_output=True,env=e,timeout=10);need(r.returncode!=0 and b'normal Python required' in r.stderr,'Portable guard');guards.append(mode)
 for (n,h),q in decoded.items():need(q.stat().st_size==n and sha(q)==h,'Restored inputs unchanged')
 result=dict(status='PASS_PUBLIC_L033_COMPLETE_CLOSURE',logical_records=len(t['files']),restored_files=len(seen),unique_decoded=len(decoded),stored_payloads=len(stored),complete_packets=len(t['packets']),complete_exports=exports,principal_dependency_pins=2391,metadata_pins=counts[0],documentary_runtime_pins=counts[1],omitted_documentary_runtime=len(t['documentary_and_runtime_hash_only']),malformed_controls=damages,portable_guards=guards,application=app,git_tracked_reuse=True,target_censuses=0,new_measurements=0,new_Lean=0,new_question_credit=0,whole_original_credit=0,seconds=time.monotonic()-start)
 save(O/'report.json',result);print(json.dumps(result))
if __name__=='__main__':main()
