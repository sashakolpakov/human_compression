"""Public-only L019 closure restoration, integrity, and bounded finite replay.

No private study is read. Documentary source bytes and historical render caches
are explicitly outside the runnable proof closure. Mathematical reviews remain
separate; this checker does not infer mathematical validity from hashes.
"""
import sys
if sys.flags.optimize:raise RuntimeError('Optimized Python is not supported')
from pathlib import Path,PurePosixPath
import argparse,collections,copy,gzip,hashlib,json,os,shutil,subprocess,time
BASE='audit/recoveries/L019/v1'
HISTORICAL='/Users/sasha/medusa/research/leemans/'
AUTHOR='corpus106_L019_principal_v1/manifest.json'
AUTHOR_HASH='bf7b464283603675a940bc6de5f628275ac5e4263ab4e227704e56fa4e4fc370'
REVIEW='corpus106_L019_principal_independent_review/manifest.json'
REVIEW_HASH='c326425c80536b4bbedf94083b70890b01af3cc8482d81ca8d4d6664a18c5813'
ROOT='corpus106_L019_principal_root_adoption/manifest.json'
ROOT_HASH='e7799bfbc3ccfb86073c771988a82bb6551eb942e382ff9c6d747ca2fbfbf618'
PRIMARY={('study', 'reboot_20261013/L019_section9_contract_work/source_page_39.txt'), ('study', 'reboot_20261013/L019_endpoint_anchors_distinct/source35.png'), ('study', 'reboot_20261013/L019_section9_contract_work/source_42.png'), ('study', 'reboot_20261013/L019_balanced_pairs_distinct/source-02.png'), ('study', 'sources/alternating2019.txt'), ('study', 'reboot_20261013/L019_split_inheritance_distinct/source35.png'), ('study', 'reboot_20261013/L019_balanced_pairs_distinct/source-01.png'), ('study', 'reboot_20261013/L019_trivial_factor_distinct_v2/source35.png'), ('study', 'reboot_20261013/L019_section9_contract_work/source_page_40.txt'), ('study', 'sources/catalogue_L071.txt'), ('study', 'sources/stability2024.pdf'), ('study', 'reboot_20261013/L019_recovery_work/source_page_02.txt'), ('study', 'reboot_20261013/L019_endpoint_anchors_distinct/source36.png'), ('study', 'sources/g2_even2026.pdf'), ('study', 'reboot_20261013/L019_trivial_factor_distinct/source35.png'), ('study', 'reboot_20261013/L019_balanced_pairs_distinct/source-03.png'), ('study', 'reboot_20261013/L044_principal_distinct/source-1.png'), ('study', 'reboot_20261013/L044_principal_distinct/source-2.png'), ('study', 'sources/alternating2019.pdf'), ('study', 'reboot_20261013/L019_orbit_budgets_distinct_v2/source17.png'), ('study', 'sources/catalogue_L044.txt'), ('study', 'reboot_20261013/L019_initial_fracture_distinct/source10.png'), ('study', 'reboot_20261013/L019_section9_contract_work/source_page_37.txt'), ('study', 'reboot_20261013/L044_general_imprimitive_root_work/source_7_9.txt'), ('study', 'reboot_20261013/L019_recovery_work/source_page07.png'), ('study', 'reboot_20261013/L019_trivial_factor_distinct/source36.png'), ('local_software_documentation', '/opt/homebrew/Cellar/gap/4.15.1/share/gap/doc/ref/chap79.txt'), ('study', 'reboot_20261013/L019_section9_contract_work/source_page_38.txt'), ('study', 'reboot_20261013/L019_split_inheritance_distinct/source36.png'), ('study', 'reboot_20261013/L019_orbit_budgets_distinct/source17.png'), ('study', 'reboot_20261013/L019_actual_wings_distinct/source17.png'), ('study', 'reboot_20261013/L044_principal_distinct/source_required_pages.pdf'), ('study', 'reboot_20261013/L019_orbit_budgets_distinct_v2/source18.png'), ('study', 'reboot_20261013/L019_recovery_work/SnJanuary2023.tex'), ('study', 'reboot_20261013/L019_recovery_work/source_page_01.txt'), ('study', 'reboot_20261013/L019_faithful_augmentation_distinct02/source35.png'), ('study', 'reboot_20261013/L019_section9_contract_work/source_page_42.txt'), ('study', 'reboot_20261013/L019_trivial_factor_distinct_v2/source36.png'), ('study', 'sources/catalogue_L044.pdf'), ('study', 'reboot_20261013/L019_section9_contract_work/source_page_41.txt'), ('study', 'reboot_20261013/L019_section9_contract_work/source_41.png'), ('study', 'sources/catalogue_L071.pdf'), ('study', 'reboot_20261013/L019_orbit_budgets_distinct/source18.png'), ('study', 'reboot_20261013/L019_initial_fracture_distinct/source9.png'), ('study', 'reboot_20261013/L019_section9_contract_work/source_38.png')}
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
 need(t['logical_files']==len(t['files'])==6652,'Exact logical inventory')
 keys=[(r['origin'],r['path'])for r in t['files']];need(len(keys)==len(set(keys)),'Duplicate logical file')
 need({x['origin']for x in t['files']}<={'study','public','local_software_documentation'},'Unexpected namespace')
 omitted={(r['origin'],r['path'])for r in t['files']if r['transport'].endswith('HASH_ONLY')}
 need(omitted==PRIMARY=={(r['origin'],r['path'])for r in t['primary_sources_hash_only']},'Exact documentary omissions')
 need(len(t['packets'])==439 and len({(p['origin'],p['path'])for p in t['packets']})==439,'Whole packet inventory')
 pm={p['path']:p['sha256']for p in t['packets']}
 for p,h in [(AUTHOR,AUTHOR_HASH),(REVIEW,REVIEW_HASH),(ROOT,ROOT_HASH)]:need(pm.get(p)==h,'Required complete principal/review chain')
 need(len(t['legacy_common_aliases']['bindings'])==21,'Exact common aliases')
 need(len(t['relative_locator_resolutions'])==42,'Exact relative locators')
 ec=collections.Counter(e['kind']for e in t['historical_documentary_exceptions'])
 need(ec=={'HISTORICAL_NATIVE_RENDER_CACHE_HASH_ONLY':169,'HISTORICAL_PRIMARY_SOURCE_RENDER_HASH_ONLY':51,'EXTERNAL_SOFTWARE_HASH_ONLY':22,'HISTORICAL_TYPESETTING_LOG_HASH_ONLY':1},'Exact historical exceptions')
 for r in t['files']:
  need(not r.get('public_path','').endswith('.md'),'Markdown provenance must use explicit .txt public object')
  if not r['transport'].endswith('HASH_ONLY'):
   need(r['transport']in ['EXISTING_PUBLIC','NEW_FROZEN_FILE'],'Unknown transport')
   need(r['encoding']in ['identity','gzip'],'Unknown encoding')
   child(Path('/logical'),r['path']);child(Path('/public'),r['public_path'])
def main(a):
 start=time.monotonic();repo=a.repo.resolve();payload=a.payload.resolve()if a.payload else repo
 tp=child(payload,BASE+'/transport.json');need(sha(tp)==a.expected_transport,'Frozen transport mismatch');t=json.loads(tp.read_text());structure(t)
 controls=[]
 mutators=[('duplicate',lambda x:x['files'].__setitem__(1,copy.deepcopy(x['files'][0]))),('credit',lambda x:x.__setitem__('whole_original_credit',1)),('omit_proof',lambda x:next(r for r in x['files']if r['path']=='corpus106_L019_principal_v1/principal.tex').__setitem__('transport','PRIVATE_PRIMARY_SOURCE_HASH_ONLY')),('packet_missing',lambda x:x['packets'].pop()),('root_changed',lambda x:next(p for p in x['packets']if p['path']==ROOT).__setitem__('sha256','0'*64)),('namespace',lambda x:x['files'][0].__setitem__('origin','private_fallback')),('alias_missing',lambda x:x['legacy_common_aliases']['bindings'].pop()),('exception_missing',lambda x:x['historical_documentary_exceptions'].pop()),('locator_missing',lambda x:x['relative_locator_resolutions'].pop()),('unsafe_path',lambda x:x['files'][0].__setitem__('path','../escape'))]
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
 principal=study/'corpus106_L019_principal_v1';deps=json.loads((principal/'dependencies.json').read_text())
 if isinstance(deps,dict):deps=deps['bindings']
 for row in deps:verify(study,row)
 acquired=json.loads((principal/'acquired_packets.json').read_text())
 if isinstance(acquired,dict):acquired=acquired['packets']
 need(len(acquired)==13,'Immediate mathematical roots')
 for r in t['relative_locator_resolutions']:
  target=seen[(r['resolved_origin'],r['resolved_path'])];p=r['historical_pin'];need(sha(target)==p['sha256']and p.get('bytes',target.stat().st_size)==target.stat().st_size,'Relative locator changed')
 for r in t['legacy_common_aliases']['bindings']:
  p=child(study,r['expected']);need(p.is_file()and sha(p)==r['sha256'],'Retained common alias missing')
 # Independently resolve every exact pin in all transported L019 JSON
 # metadata. Documentary exceptions and historical relative roots are explicit.
 exception_map={}
 for item in t['historical_documentary_exceptions']:
  rec=item['record'];exception_map[(rec.get('context',rec.get('ref')),rec.get('pin',{}).get('path',rec.get('path')))]=item
 locator_map={(r['context'].removeprefix(HISTORICAL),r['historical_pin']['path'],r['historical_pin']['sha256']):r for r in t['relative_locator_resolutions']}
 literal_checks=[0,0]
 def literal_pin(obj,context):
  name=obj.get('path');h=obj.get('sha256')
  if not isinstance(name,str)or not isinstance(h,str)or len(h)!=64:return
  candidates=[]
  if name.startswith(HISTORICAL):candidates.append(('study',name[len(HISTORICAL):]))
  elif name.startswith('/Users/sasha/medusa/math_compression/'):
   candidates.append(('public',name.removeprefix('/Users/sasha/medusa/math_compression/')))
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
  raise ValueError('Unresolved exact L019 metadata pin: '+context+' -> '+name)
 def audit_json(obj,context):
  if isinstance(obj,dict):
   literal_pin(obj,context)
   for k,v in obj.items():
    if isinstance(k,str)and k.startswith(HISTORICAL)and isinstance(v,str)and len(v)==64:literal_pin({'path':k,'sha256':v},context)
    if k!='exports':audit_json(v,context)
  elif isinstance(obj,list):
   for v in obj:audit_json(v,context)
 for (origin,rel),p in seen.items():
  if origin=='study'and ('L019'in PurePosixPath(rel).parts[0]or PurePosixPath(rel).parts[0].startswith('topic_B_rank_extension_repair'))and p.suffix=='.json':audit_json(json.loads(p.read_text()),rel)
 # The earlier complete L044 closure is an exact acquired boundary. Do not
 # reinterpret unrelated historical catalogue metadata as new L019 premises.
 prior_path=public/'audit/recoveries/L044/v1/transport.json'
 need(sha(prior_path)=='507bf6343f589b1fd87b722cfdbf54645cf745e6256f97346d4fb47289b66599','Acquired L044 transport')
 prior=json.loads(prior_path.read_text())
 for r in prior['files']:
  old=rowmap[(r['origin'],r['path'])];need((r['sha256'],r['bytes'])==(old['sha256'],old['bytes']),'Prior logical bytes preserved')
 need(t['historical_documentary_exceptions']==prior['historical_documentary_exceptions'],'Acquired documentary exceptions unchanged')
 need(t['legacy_common_aliases']==prior['legacy_common_aliases'],'Acquired aliases unchanged')
 need(t['relative_locator_resolutions'][:26]==prior['relative_locator_resolutions'],'Acquired exact locators unchanged')
 need(all(r in t['packets']for r in prior['packets']),'Whole prior packet closure')
 routes=json.loads((principal/'source_map.json').read_text())
 need(routes['original']=='L019'and len(routes['principal_contract'])==3 and len(routes['retained_auxiliary_corrections'])==4,'Complete exact source contract')
 # Explicit portable replay companion: mathematical helpers and engines below
 # are unchanged. The original author wrapper checks the article PDF, which is
 # documentary hash-only; this wrapper instead verifies its exact metadata pin.
 env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);runs=[]
 def execute(label,cmd,cwd,cap):
  with (out/(label+'.stdout')).open('wb')as stdout,(out/(label+'.stderr')).open('wb')as stderr:
   proc=subprocess.Popen(cmd,cwd=cwd,env=env,stdout=stdout,stderr=stderr)
   (out/'active.json').write_text(json.dumps({'status':'RUNNING','label':label,'pid':proc.pid,'cap_seconds':cap})+'\n')
   try:code=proc.wait(timeout=cap)
   except subprocess.TimeoutExpired:proc.kill();proc.wait();raise ValueError(label+' timed out; no certificate')
  need(code==0 and not (out/(label+'.stderr')).read_bytes(),'Finite replay failed: '+label)
  runs.append({'label':label,'returncode':code,'stdout_sha256':sha(out/(label+'.stdout')),'stderr_empty':True})
  return (out/(label+'.stdout')).read_bytes()
 guards=[]
 for label,cmd,e in [('argument',[sys.executable,'-O',str(Path(__file__).resolve())],env),('environment',[sys.executable,str(Path(__file__).resolve())],dict(env,PYTHONOPTIMIZE='1'))]:
  result=subprocess.run(cmd,env=e,capture_output=True,timeout=15)
  need(result.returncode!=0 and b'Optimized Python is not supported'in result.stderr,'Optimization guard')
  (out/(label+'.stderr')).write_bytes(result.stderr);guards.append(label)
 import ast,importlib.util
 balanced=study/'topic_B_L019_balanced_pairs_v1';work=out/'finite';work.mkdir()
 for n in range(2,13,2):
  name=f'n{n}_run03'if n==12 else f'n{n}_run01';shutil.copytree(balanced/name,work/name)
 for name in ['verify_arrays.py','prepare_positive_checks.py','positive_checks.g','small_independent_v2.g']:shutil.copyfile(balanced/name,work/name)
 execute('arrays',[sys.executable,'verify_arrays.py'],work,120)
 fresh=json.loads((work/'arrays_report.json').read_text());need(fresh==json.loads((balanced/'arrays_report.json').read_text()),'Exact literal arrays')
 execute('positive_inputs',[sys.executable,'prepare_positive_checks.py'],work,30)
 need((work/'positive_inputs.g').read_bytes()==(balanced/'positive_inputs.g').read_bytes(),'Exact generated positive inputs')
 b=execute('positive',[a.gap,'-q','-T','positive_checks.g'],work,120)
 need(b.count(b'COMPLETE_POSITIVE_CHECKS|41|101|')==1,'All positive completions')
 b=execute('labelled',[a.gap,'-q','-T','small_independent_v2.g'],work,120)
 need(b.count(b'COMPLETE_LABELLED|')==1,'Independent labelled completion')
 spec=importlib.util.spec_from_file_location('arrays',work/'verify_arrays.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
 def tuples(data,tag):return [tuple(tuple(x-1 for x in g)for g in ast.literal_eval(line.split('|',1)[1]))for line in data.decode().splitlines()if line.startswith(tag+'|')]
 labelled=tuples(b,'LABELLED');need(len(labelled)==720 and {v.canon(x,0)for x in labelled}=={v.canon(x,0)for x in v.load_run(work,6)},'Independent degree-six classes')
 damaged=0
 for x in [((0,0),),((1,0,2),(0,2,1),(2,1,0)),((1,0,2,3),)]:
  try:v.canon(x,0)
  except ValueError:damaged+=1
 need(damaged==3,'Malformed literal controls')
 censuses=[]
 for n in range(2,13,2):
  cw=out/f'census{n}';cw.mkdir();(cw/'parameters.g').write_text(f'n:={n};;\n');shutil.copyfile(balanced/'enumerate_v3.g',cw/'enumerate.g')
  b=execute(f'census{n}',[a.gap,'-q','-T','enumerate.g'],cw,600)
  need(b.count(b'COMPLETE_ANCHORED_CRITICAL_WINGS|')==1,'Complete census marker')
  ts=tuples(b,'SOLUTION');codes={v.canon(x,0)for x in ts};need(len(codes)==len(ts)and codes=={v.canon(x,0)for x in v.load_run(work,n)},'Exact fresh rooted census classes')
  censuses.append({'degree':n,'wings':len(ts)})
 from pypdf import PdfReader
 native=[]
 for folder,name,pages in [('corpus106_L019_principal_v1','principal',2),('topic_B_L019_pure_bijection_v1','pure_bijection',4),('topic_B_L019_balanced_pairs_v1','balanced_pairs',3)]:
  source=study/folder;target=out/'native'/name;target.mkdir(parents=True);shutil.copyfile(source/(name+'.tex'),target/(name+'.tex'))
  for i in [1,2]:
   r=subprocess.run([a.pdflatex,'-interaction=nonstopmode','-halt-on-error',name+'.tex'],cwd=target,env=env,capture_output=True,timeout=60)
   (target/f'pass{i}.stdout').write_bytes(r.stdout);(target/f'pass{i}.stderr').write_bytes(r.stderr);need(r.returncode==0 and not r.stderr,'Native build')
  texts=[p.extract_text()for p in PdfReader(target/(name+'.pdf')).pages];need(len(texts)==pages and texts==[p.extract_text()for p in PdfReader(source/(name+'.pdf')).pages],'Native text identity')
  need(not any(x in (target/(name+'.log')).read_text()for x in ['Overfull','LaTeX Warning']),'Native warning');native.append({'name':name,'pages':pages,'text_identical':True})
 # Rehash restored inputs after programs execute; all source trees are immutable.
 for key,p in seen.items():need(sha(p)==rowmap[key]['sha256'],'Restored input mutated')
 result=dict(status='PASS_PUBLIC_L019_COMPLETE_CLOSURE',checker_sha256=sha(Path(__file__)),transport_sha256=sha(tp),logical_records=len(t['files']),restored_files=len(seen),distinct_payloads=len(decoded),acquired_packets=len(t['packets']),acquired_exports=exports,immediate_mathematical_roots=13,principal_claims=3,auxiliary_corrections=4,exact_metadata_pins_checked=literal_checks[0],documentary_metadata_pins_acquired=literal_checks[1],historical_exceptions=len(t['historical_documentary_exceptions']),documentary_omissions=len(PRIMARY),relative_locators=42,malformed_controls=controls,optimization_guards=guards,malformed_literal_controls=damaged,finite_runs=runs,fresh_complete_censuses=censuses,wing_counts=fresh['wing_counts'],boundary_counts=fresh['boundary_counts'],independent_labelled_degree6=720,positive_wings=41,positive_glued_markings=101,native=native,private_proof_fallback=False,unrelated_group_censuses_repeated=False,mathematical_review_replaced_by_hashes=False,new_formal_declarations=0,new_measurements=0,new_question_credit=0,whole_original_credit=0,seconds=time.monotonic()-start)
 (out/'report.json').write_text(json.dumps(result,indent=2)+'\n');(out/'active.json').write_text(json.dumps({'status':'TERMINAL','returncode':0})+'\n');print(json.dumps(result))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--payload',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--expected-transport',required=True);p.add_argument('--gap',default='/opt/homebrew/bin/gap');p.add_argument('--pdflatex',default='/opt/homebrew/bin/pdflatex');main(p.parse_args())
