"""Public-only L044 closure restoration, integrity, and bounded finite replay.

No private study is read. Documentary source bytes and historical render caches
are explicitly outside the runnable proof closure. Mathematical reviews remain
separate; this checker does not infer mathematical validity from hashes.
"""
import sys
if sys.flags.optimize:raise RuntimeError('Optimized Python is not supported')
from pathlib import Path,PurePosixPath
import argparse,collections,copy,gzip,hashlib,json,os,shutil,subprocess,time
BASE='audit/recoveries/L044/v1'
HISTORICAL='/Users/sasha/medusa/research/leemans/'
AUTHOR='corpus106_L044_principal_v1/manifest.json'
AUTHOR_HASH='1d28ce85d74f3f19fcc8c13f433c46500e2dd441993041093f45b759fac7563f'
REVIEW='corpus106_L044_principal_independent_review/manifest.json'
REVIEW_HASH='a38fcf1add536e43c4fe1c9d15e237b8a98cc87445cc2c490007c17b63a35a09'
ROOT='corpus106_L044_principal_root_adoption/manifest.json'
ROOT_HASH='85a42d5d77a891e7264c054d7f689fd85c9f5b40c485fd9a582bb8ea140ada51'
PRIMARY={('local_software_documentation','/opt/homebrew/Cellar/gap/4.15.1/share/gap/doc/ref/chap79.txt'),('study','reboot_20261013/L044_general_imprimitive_root_work/source_7_9.txt'),('study','reboot_20261013/L044_principal_distinct/source-1.png'),('study','reboot_20261013/L044_principal_distinct/source-2.png'),('study','reboot_20261013/L044_principal_distinct/source_required_pages.pdf')}
PRIMARY|={('study','sources/'+x)for x in ['alternating2019.pdf','alternating2019.txt','catalogue_L044.pdf','catalogue_L044.txt','catalogue_L071.pdf','catalogue_L071.txt','g2_even2026.pdf']}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def child(root,name):
 q=PurePosixPath(name);need(name and not q.is_absolute()and'..'not in q.parts,'Unsafe relative path');p=(root/q).resolve();need(p.is_relative_to(root.resolve()),'Path escapes root');return p
def structure(t):
 need(t['whole_original_credit']==0,'Transport cannot self-admit')
 need(t['logical_files']==len(t['files'])==4285,'Exact logical inventory')
 keys=[(r['origin'],r['path'])for r in t['files']];need(len(keys)==len(set(keys)),'Duplicate logical file')
 need({x['origin']for x in t['files']}<={'study','public','local_software_documentation'},'Unexpected namespace')
 omitted={(r['origin'],r['path'])for r in t['files']if r['transport'].endswith('HASH_ONLY')}
 need(omitted==PRIMARY=={(r['origin'],r['path'])for r in t['primary_sources_hash_only']},'Exact documentary omissions')
 need(len(t['packets'])==349 and len({(p['origin'],p['path'])for p in t['packets']})==349,'Whole packet inventory')
 pm={p['path']:p['sha256']for p in t['packets']}
 for p,h in [(AUTHOR,AUTHOR_HASH),(REVIEW,REVIEW_HASH),(ROOT,ROOT_HASH)]:need(pm.get(p)==h,'Required complete principal/review chain')
 need(len(t['legacy_common_aliases']['bindings'])==21,'Exact common aliases')
 need(len(t['relative_locator_resolutions'])==26,'Exact relative locators')
 ec=collections.Counter(e['kind']for e in t['historical_documentary_exceptions'])
 need(ec=={'HISTORICAL_NATIVE_RENDER_CACHE_HASH_ONLY':169,'HISTORICAL_PRIMARY_SOURCE_RENDER_HASH_ONLY':51,'EXTERNAL_SOFTWARE_HASH_ONLY':22,'HISTORICAL_TYPESETTING_LOG_HASH_ONLY':1},'Exact historical exceptions')
 for r in t['files']:
  need(not r['path'].endswith('.md'),'Working Markdown not public proof')
  if not r['transport'].endswith('HASH_ONLY'):
   need(r['transport']in ['EXISTING_PUBLIC','NEW_FROZEN_FILE'],'Unknown transport')
   need(r['encoding']in ['identity','gzip'],'Unknown encoding')
def main(a):
 start=time.monotonic();repo=a.repo.resolve();payload=a.payload.resolve()if a.payload else repo
 tp=child(payload,BASE+'/transport.json');need(sha(tp)==a.expected_transport,'Frozen transport mismatch');t=json.loads(tp.read_text());structure(t)
 controls=[]
 mutators=[('duplicate',lambda x:x['files'].__setitem__(1,copy.deepcopy(x['files'][0]))),('credit',lambda x:x.__setitem__('whole_original_credit',1)),('omit_proof',lambda x:next(r for r in x['files']if r['path']=='corpus106_L044_principal_v1/principal.tex').__setitem__('transport','PRIVATE_PRIMARY_SOURCE_HASH_ONLY')),('packet_missing',lambda x:x['packets'].pop()),('root_changed',lambda x:next(p for p in x['packets']if p['path']==ROOT).__setitem__('sha256','0'*64)),('namespace',lambda x:x['files'][0].__setitem__('origin','private_fallback')),('alias_missing',lambda x:x['legacy_common_aliases']['bindings'].pop()),('exception_missing',lambda x:x['historical_documentary_exceptions'].pop())]
 for name,fn in mutators:
  v=copy.deepcopy(t);fn(v)
  try:structure(v)
  except (ValueError,KeyError):controls.append(name)
  else:raise ValueError('Malformed control accepted: '+name)
 need(not a.out.exists(),'Fresh output directory');a.out.mkdir(parents=True);out=a.out.resolve();study=out/'restored/study';public=out/'restored/repo';cache=out/'payloads';study.mkdir(parents=True);public.mkdir();cache.mkdir()
 seen={};decoded={};roots={'study':study,'public':public,'repo':public};rowmap={(r['origin'],r['path']):r for r in t['files']}
 for r in t['files']:
  key=(r['origin'],r['path'])
  if r['transport'].endswith('HASH_ONLY'):continue
  identity=(r['bytes'],r['sha256']);dest=child(roots[r['origin']],r['path'])
  if identity not in decoded:
   source=child(repo if r['transport']=='EXISTING_PUBLIC'else payload,r['public_path']);need(source.stat().st_size==r['stored_bytes']and sha(source)==r['stored_sha256'],'Stored payload changed')
   target=cache/r['sha256'];opener=gzip.open if r['encoding']=='gzip'else open
   with opener(source,'rb')as inf,target.open('wb')as outf:shutil.copyfileobj(inf,outf)
   need(target.stat().st_size==r['bytes']and sha(target)==r['sha256'],'Decoded payload changed');decoded[identity]=target
  dest.parent.mkdir(parents=True,exist_ok=True);os.link(decoded[identity],dest);seen[key]=dest
 def verify(root,row):
  p=child(root,row['path']);origin='study'if root==study else'public'if root==public else None
  key=(origin,row['path'])
  if key in PRIMARY:
   old=rowmap[key];need(row['sha256']==old['sha256']and row.get('bytes',old['bytes'])==old['bytes'],'Documentary binding changed');return
  need(p.is_file()and sha(p)==row['sha256']and row.get('bytes',p.stat().st_size)==p.stat().st_size,'Pinned file missing or changed: '+str(p))
 exports=0
 for pk in t['packets']:
  p=child(roots[pk['origin']],pk['path']);need(sha(p)==pk['sha256'],'Packet manifest changed');m=json.loads(p.read_text());need(len(m['exports'])==pk['exports'],'Complete exports')
  for row in m['exports']:verify(p.parent,row);exports+=1
 principal=study/'corpus106_L044_principal_v1';deps=json.loads((principal/'dependencies.json').read_text())['bindings']
 for row in deps:verify(study,row)
 acquired=json.loads((principal/'acquired_packets.json').read_text())['packets'];need(len(acquired)==13,'Immediate mathematical roots')
 for item in acquired:
  verify(study,item['author_manifest'])
  for row in item['review_manifests']:verify(study,row)
 for r in t['relative_locator_resolutions']:
  target=seen[(r['resolved_origin'],r['resolved_path'])];p=r['historical_pin'];need(sha(target)==p['sha256']and p.get('bytes',target.stat().st_size)==target.stat().st_size,'Relative locator changed')
 for r in t['legacy_common_aliases']['bindings']:
  p=child(study,r['expected']);need(p.is_file()and sha(p)==r['sha256'],'Retained common alias missing')
 # Independently resolve every exact pin in all transported L044 JSON
 # metadata. Documentary exceptions and historical relative roots are explicit.
 exception_map={}
 for item in t['historical_documentary_exceptions']:
  rec=item['record'];exception_map[(rec.get('context',rec.get('ref')),rec.get('pin',{}).get('path',rec.get('path')))]=item
 locator_map={(r['context'],r['historical_pin']['path'],r['historical_pin']['sha256']):r for r in t['relative_locator_resolutions']}
 literal_checks=[0,0]
 def literal_pin(obj,context):
  name=obj.get('path');h=obj.get('sha256')
  if not isinstance(name,str)or not isinstance(h,str)or len(h)!=64:return
  candidates=[]
  if name.startswith(HISTORICAL):candidates.append(('study',name[len(HISTORICAL):]))
  elif not Path(name).is_absolute():
   candidates.extend([('study',name),('public',name)])
   candidates.append(('study',str(PurePosixPath(context).parent/PurePosixPath(name))))
  for key in candidates:
   r=rowmap.get(key)
   if r and r['sha256']==h and obj.get('bytes',r['bytes'])==r['bytes']:
    literal_checks[0]+=1;return
  locator=locator_map.get((context,name,h))
  if locator:
   q=seen[(locator['resolved_origin'],locator['resolved_path'])];need(sha(q)==h,'Relative exact pin changed');literal_checks[0]+=1;return
  exception=exception_map.get((context,name))
  if exception:
   old=exception['record'].get('pin')
   if old:need(old['sha256']==h and old.get('bytes')==obj.get('bytes'),'Historical documentary pin mismatch')
   literal_checks[1]+=1;return
  raise ValueError('Unresolved exact L044 metadata pin: '+context+' -> '+name)
 def audit_json(obj,context):
  if isinstance(obj,dict):
   literal_pin(obj,context)
   for k,v in obj.items():
    if isinstance(k,str)and k.startswith(HISTORICAL)and isinstance(v,str)and len(v)==64:literal_pin({'path':k,'sha256':v},context)
    if k!='exports':audit_json(v,context)
  elif isinstance(obj,list):
   for v in obj:audit_json(v,context)
 for (origin,rel),p in seen.items():
  if origin=='study'and 'L044'in PurePosixPath(rel).parts[0]and p.suffix=='.json':audit_json(json.loads(p.read_text()),rel)
 routes=json.loads((principal/'claim_routes.json').read_text());need(routes['original']=='L044'and len(routes['routes'])==11,'Complete source routes')
 # These are exact known short standalone finite interfaces. Their unchanged
 # code is run only in the restored tree; no private-source import or patch.
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);runs=[]
 def execute(label,cmd,cap):
  with (out/(label+'.stdout')).open('wb')as stdout,(out/(label+'.stderr')).open('wb')as stderr:
   p=subprocess.Popen(cmd,cwd=out,env=env,stdout=stdout,stderr=stderr)
   (out/'active.json').write_text(json.dumps({'label':label,'pid':p.pid,'command':cmd,'cap_seconds':cap})+'\n')
   try:code=p.wait(timeout=cap)
   except subprocess.TimeoutExpired:p.kill();p.wait();raise ValueError(label+' timed out; no certificate')
  need(code==0 and not (out/(label+'.stderr')).read_bytes(),'Finite replay failed: '+label)
  runs.append({'label':label,'returncode':code,'stdout_sha256':sha(out/(label+'.stdout')),'stderr_empty':True})
 execute('degree16',[sys.executable,str(study/'topic_B_L044_degree_sixteen_v1/check.py'),str(out/'degree16')],300)
 deg=json.loads((out/'degree16/report.json').read_text());need(deg['status']=='PASS'and deg['census']['reference_pairs']==5413998,'Complete degree16 reference decisions')
 execute('small_maxima',[sys.executable,str(study/'topic_B_L044_small_maxima_v1/check.py'),'--out',str(out/'small_maxima'),'--recorded-runs',str(study/'topic_B_L044_small_maxima_v1/author_first_runs'),'--gap',a.gap,'--seconds','120'],180)
 small=json.loads((out/'small_maxima/report.json').read_text());need(small['status']=='COMPLETE_SMALL_MAXIMA','Small boundary receipt')
 # Native assembly replay preserves exact frozen mathematical text.
 from pypdf import PdfReader
 n=out/'native';n.mkdir();shutil.copyfile(principal/'principal.tex',n/'principal.tex')
 for i in [1,2]:
  p=subprocess.run([a.pdflatex,'-interaction=nonstopmode','-halt-on-error','principal.tex'],cwd=n,env=env,capture_output=True,timeout=60);(n/f'pass{i}.stdout').write_bytes(p.stdout);(n/f'pass{i}.stderr').write_bytes(p.stderr);need(p.returncode==0 and not p.stderr,'Native build')
 pages=[p.extract_text()for p in PdfReader(n/'principal.pdf').pages];need(len(pages)==2 and pages==[p.extract_text()for p in PdfReader(principal/'principal.pdf').pages],'Native assembly text changed');need(not any(x in (n/'principal.log').read_text()for x in ['Overfull','LaTeX Warning']),'Native warning')
 # Rehash restored inputs after programs execute; all source trees are immutable.
 for key,p in seen.items():need(sha(p)==rowmap[key]['sha256'],'Restored input mutated')
 result=dict(status='PASS_PUBLIC_L044_COMPLETE_CLOSURE',transport_sha256=sha(tp),logical_records=len(t['files']),restored_files=len(seen),distinct_payloads=len(decoded),acquired_packets=len(t['packets']),acquired_exports=exports,immediate_mathematical_roots=13,source_routes=11,exact_metadata_pins_checked=literal_checks[0],documentary_metadata_pins_acquired=literal_checks[1],historical_exceptions=len(t['historical_documentary_exceptions']),documentary_omissions=len(PRIMARY),malformed_controls=controls,finite_runs=runs,degree16_full_subset_pairs=5413998,small_maxima_recorded_exhaustions_reused=True,native_pages=2,private_proof_fallback=False,large_group_censuses_repeated=False,mathematical_review_replaced_by_hashes=False,new_formal_declarations=0,whole_original_credit=0,seconds=time.monotonic()-start)
 (out/'report.json').write_text(json.dumps(result,indent=2)+'\n');(out/'active.json').write_text(json.dumps({'status':'TERMINAL','returncode':0})+'\n');print(json.dumps(result))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--payload',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--expected-transport',required=True);p.add_argument('--gap',default='/opt/homebrew/bin/gap');p.add_argument('--pdflatex',default='/opt/homebrew/bin/pdflatex');main(p.parse_args())
