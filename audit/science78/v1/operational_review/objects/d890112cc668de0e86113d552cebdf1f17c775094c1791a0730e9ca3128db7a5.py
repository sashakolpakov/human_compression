"""Restore and replay the exact public L059 proof/certificate package.

Historical article/data-source files are identified explicitly by hash. The
bounded numerical inputs used by this replay are included in full. No private
study path is read, and no mathematical acceptance is inferred from hashes.
"""
import sys
if sys.flags.optimize:raise RuntimeError('Optimized Python is not supported')
from pathlib import Path,PurePosixPath
import argparse,collections,copy,gzip,hashlib,json,os,shutil,subprocess,time
BASE='audit/recoveries/L059/v1'
HISTORICAL='/Users/sasha/medusa/research/leemans/'
PUBLIC_HISTORICAL='/Users/sasha/medusa/math_compression/'
COMPANIONS={'portable_integrity.py': '166862f8ef759abdeef968aed972389f8edf9d0b042621d443da93cc55af36ca', 'named_examples_portable.g': '931e870ec52ca372d7735362ed1565f960de92e5251353ef8f2f263825a3881c', 'method_controls_portable.g': 'caef6bdd7f89488a1b4fa7e897c48fd5853cc933a24170ce21015ad797c3451e'}
REQUIRED={
 'corpus106_L059_principal_v2/manifest.json':'7bd69a403767f78a4b4702aa7b110b8eabf6d8d128c9cf4c31141f9b389d21d9',
 'corpus106_L059_principal_independent_review/manifest.json':'6fc27eab72de943d831eb7397c52609c1c8572726f9e1f62a5d0d05bf72fd738',
 'corpus106_L059_principal_root_adoption/manifest.json':'26b8489176d5a05454d9ce99991eedce9a67ce19b90fea3db99f0c040621a8ba',
 'reboot_20261013/L059_publication_inputs/manifest.json':'e570fb5412b7f39a29b7c9d0d79da023bb9cc279bbb65f4195291ec63b421320'}
PRIMARY_NAMES=['C4_FinalFull.mgm','CAT_lcf.txt','CSS_lcf.txt','Wilson_Potocnik_census_coverage.pdf','c4_index.html','c4_index_20110130.html','c4_table.html','c4_table_20080505.html','c4_table_20141228.html','final_and_foster_web_receipt.json','final_edition_scope_web_receipt.json','foster_primary.html','sage_smallgraphs_source.py','source_tables_01.png','source_tables_02.png','Wilson_Potocnik_coverage_page2.png']
PRIMARY={('study','reboot_20261013/L059_recovery_work/'+x) for x in PRIMARY_NAMES}
PRIMARY|={('study','sources/catalogue_L059.pdf'),('study','reboot_20261013/L059_principal_distinct/source-1.png'),('study','reboot_20261013/L059_principal_distinct/source-2.png')}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def child(root,name):
 q=PurePosixPath(name);need(name and not q.is_absolute() and '..' not in q.parts,'Unsafe relative path')
 p=(root/q).resolve();need(p.is_relative_to(root.resolve()),'Path escapes root');return p
def structure(t):
 need(t['whole_original_credit']==0,'Transport cannot self-admit')
 need(t['logical_files']==len(t['files'])==10573,'Exact logical inventory')
 keys=[(r['origin'],r['path']) for r in t['files']];need(len(keys)==len(set(keys)),'Duplicate logical record')
 need({r['origin'] for r in t['files']}<={'study','public'},'Unexpected namespace')
 omitted={(r['origin'],r['path']) for r in t['files'] if r['transport'].endswith('HASH_ONLY')}
 need(omitted==PRIMARY=={(r['origin'],r['path']) for r in t['primary_sources_hash_only']},'Exact documentary exclusions')
 need(len(t['packets'])==9 and len({(r['origin'],r['path']) for r in t['packets']})==9,'Whole packets')
 manifests={r['path']:r['sha256'] for r in t['packets']}
 for p,h in REQUIRED.items():need(manifests.get(p)==h,'Required acceptance/input edition')
 need(len(t['relative_locator_resolutions'])==20,'Exact historical locators')
 need(not t['historical_documentary_exceptions'],'No unexplained historical omissions')
 for r in t['files']:
  child(Path('/logical'),r['path'])
  if not r['transport'].endswith('HASH_ONLY'):
   need(r['transport'] in ['EXISTING_PUBLIC','NEW_FROZEN_FILE'],'Transport kind')
   need(r['encoding'] in ['identity','gzip'],'Lossless encoding')
   child(Path('/public'),r['public_path'])
def main(a):
 start=time.monotonic();repo=a.repo.resolve();payload=a.payload.resolve() if a.payload else repo
 for name,digest in COMPANIONS.items():need(sha(Path(__file__).resolve().parent/name)==digest,'Exact companion program '+name)
 tp=child(payload,BASE+'/transport.json');need(sha(tp)==a.expected_transport,'Exact transport hash');t=json.loads(tp.read_text());structure(t)
 controls=[]
 mutations=[('duplicate',lambda x:x['files'].__setitem__(1,copy.deepcopy(x['files'][0]))),('credit',lambda x:x.__setitem__('whole_original_credit',1)),('omit_proof',lambda x:next(r for r in x['files'] if r['path']=='corpus106_L059_principal_v2/faithful_markings.tex').__setitem__('transport','PRIVATE_PRIMARY_SOURCE_HASH_ONLY')),('missing_packet',lambda x:x['packets'].pop()),('changed_root',lambda x:next(r for r in x['packets'] if r['path']=='corpus106_L059_principal_root_adoption/manifest.json').__setitem__('sha256','0'*64)),('unsafe_path',lambda x:x['files'][0].__setitem__('path','../escape')),('bad_encoding',lambda x:next(r for r in x['files'] if 'encoding' in r).__setitem__('encoding','pickle')),('omitted_locator',lambda x:x['relative_locator_resolutions'].pop())]
 for name,fn in mutations:
  bad=copy.deepcopy(t);fn(bad)
  try:structure(bad)
  except (ValueError,KeyError):controls.append(name)
  else:raise ValueError('Malformed transport accepted: '+name)
 need(not a.out.exists(),'Fresh output required');out=a.out.resolve();out.mkdir(parents=True)
 study=out/'restored/study';public=out/'restored/repo';cache=out/'payloads'
 for p in [study,public,cache]:p.mkdir(parents=True)
 roots={'study':study,'public':public};decoded={};seen={};rowmap={(r['origin'],r['path']):r for r in t['files']}
 for r in t['files']:
  if r['transport'].endswith('HASH_ONLY'):continue
  key=(r['bytes'],r['sha256']);dest=child(roots[r['origin']],r['path'])
  if key not in decoded:
   src=child(repo if r['transport']=='EXISTING_PUBLIC' else payload,r['public_path'])
   need(src.stat().st_size==r['stored_bytes'] and sha(src)==r['stored_sha256'],'Changed stored payload')
   target=cache/r['sha256'];opener=gzip.open if r['encoding']=='gzip' else open
   with opener(src,'rb') as inf,target.open('wb') as outf:shutil.copyfileobj(inf,outf)
   need(target.stat().st_size==r['bytes'] and sha(target)==r['sha256'],'Changed decoded bytes');decoded[key]=target
  dest.parent.mkdir(parents=True,exist_ok=True);os.link(decoded[key],dest);seen[(r['origin'],r['path'])]=dest
 exports=0
 for packet in t['packets']:
  p=seen[(packet['origin'],packet['path'])];need(sha(p)==packet['sha256'],'Manifest pin');m=json.loads(p.read_text());need(len(m['exports'])==packet['exports'],'Complete packet exports')
  for r in m['exports']:
   q=child(p.parent,r['path']);need(q.is_file() and q.stat().st_size==r['bytes'] and sha(q)==r['sha256'],'Complete manifest export');exports+=1
 # Resolve pinned dependency objects to declared public bytes, preserving
 # historical absolute paths as metadata without ever opening those paths.
 literal_count=0
 def literal(x,context):
  nonlocal literal_count
  name=x.get('path');h=x.get('sha256')
  if not isinstance(name,str) or not isinstance(h,str) or len(h)!=64:return
  if name.startswith(HISTORICAL):keys=[('study',name[len(HISTORICAL):])]
  elif name.startswith(PUBLIC_HISTORICAL):keys=[('public',name[len(PUBLIC_HISTORICAL):])]
  elif not Path(name).is_absolute():keys=[('study',name),('public',name),('study',str(PurePosixPath(context).parent/name)),('study','reboot_20261013/L059_recovery_work/'+name),('study','reboot_20261013/L059_publication_inputs/'+name)]
  else:keys=[]
  for key in keys:
   r=rowmap.get(key)
   if r and r['sha256']==h and r['bytes']==x.get('bytes',r['bytes']):literal_count+=1;return
  raise ValueError('Unresolved exact pin '+context+' -> '+name)
 def walk(x,context):
  if isinstance(x,dict):
   literal(x,context)
   for k,v in x.items():
    if isinstance(k,str) and k.startswith(HISTORICAL) and isinstance(v,str) and len(v)==64:literal({'path':k,'sha256':v},context)
    if k!='exports':walk(v,context)
  elif isinstance(x,list):
   for y in x:walk(y,context)
 for (origin,rel),p in seen.items():
  if origin=='study' and p.suffix=='.json' and ('L059' in PurePosixPath(rel).parts[0] or rel.startswith('reboot_20261013/L059_publication_inputs/')):walk(json.loads(p.read_text()),rel)
 principal=study/'corpus106_L059_principal_v2';working=study/'reboot_20261013/L059_recovery_work';inputs=study/'reboot_20261013/L059_publication_inputs'
 toolroot=Path(__file__).resolve().parent;env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);runs=[]
 def execute(label,cmd,cwd,cap):
  with (out/(label+'.stdout')).open('wb') as stdout,(out/(label+'.stderr')).open('wb') as stderr:
   p=subprocess.Popen(cmd,cwd=cwd,env=env,stdout=stdout,stderr=stderr)
   (out/'active.json').write_text(json.dumps({'status':'RUNNING','label':label,'pid':p.pid,'cap_seconds':cap})+'\n')
   try:code=p.wait(timeout=cap)
   except subprocess.TimeoutExpired:p.kill();p.wait();raise ValueError(label+' capped without a certificate')
  need(code==0 and not (out/(label+'.stderr')).read_bytes(),'Replay failed: '+label)
  runs.append(dict(label=label,returncode=code,stdout_sha256=sha(out/(label+'.stdout')),stderr_empty=True))
 execute('principal',[sys.executable,str(toolroot/'portable_integrity.py'),'--sources',str(working),'--study',str(study),'--packet',str(principal),'--transport',str(tp),'--replay',str(out/'principal'),'--replay-named','--gap',a.gap],out,180)
 principal_report=json.loads((out/'principal/report.json').read_text());need(principal_report['faithful_markings']==4254 and principal_report['graphs']==1950,'Principal totals')
 execute('numeric_inputs',[sys.executable,str(inputs/'replay_numeric_inputs.py'),'--derived',str(working),'--output',str(out/'numeric_inputs.json')],out,180)
 numeric=json.loads((out/'numeric_inputs.json').read_text());old_numeric=json.loads((working/'cubic_source_verification.json').read_text());need(numeric['status']=='PASS_PUBLIC_NUMERIC_INPUTS_839_REUSE_261' and numeric['graphs']==old_numeric['graphs'],'All exact primary input records')
 execute('method_controls',[a.gap,'-q','-b','-T',str(toolroot/'method_controls_portable.g')],working,60)
 need('PASS_METHOD_CONTROLS' in (out/'method_controls.stdout').read_text(),'Method control completion')
 from pypdf import PdfReader
 native=[]
 for folder,name,pages in [('corpus106_L059_principal_v2','faithful_markings',10),('corpus106_L059_historical_quartic_v1','historical_quartic',3),('corpus106_L059_subdivision_actual_actions_v1','actual_actions',2)]:
  target=out/'native'/name;target.mkdir(parents=True);source=study/folder
  for tex in source.glob('*.tex'):shutil.copyfile(tex,target/tex.name)
  for number in [1,2]:
   r=subprocess.run([a.pdflatex,'-interaction=nonstopmode','-halt-on-error',name+'.tex'],cwd=target,env=env,capture_output=True,timeout=60)
   (target/f'pass{number}.stdout').write_bytes(r.stdout);(target/f'pass{number}.stderr').write_bytes(r.stderr);need(r.returncode==0 and not r.stderr,'Native build '+name)
  fresh=[p.extract_text() for p in PdfReader(target/(name+'.pdf')).pages];old=[p.extract_text() for p in PdfReader(source/(name+'.pdf')).pages]
  need(len(fresh)==pages and fresh==old and 'Overfull' not in (target/(name+'.log')).read_text(),'Native text/overflow '+name);native.append(dict(name=name,pages=pages,text_identical=True))
 for key,p in seen.items():need(sha(p)==rowmap[key]['sha256'],'Restored input mutated')
 report=dict(status='PASS_PUBLIC_L059_COMPLETE_CLOSURE',checker_sha256=sha(Path(__file__)),companion_sha256=COMPANIONS,transport_sha256=sha(tp),logical_files=len(t['files']),restored_files=len(seen),unique_decoded_payloads=len(decoded),packets=len(t['packets']),exports=exports,exact_metadata_pins=literal_count,documentary_hash_only=len(PRIMARY),relative_locator_records=20,malformed_controls=controls,runs=runs,graphs=1950,faithful_markings=4254,printed_cells=39,numeric_inputs=839,explicit_reuse_isomorphisms=261,method_control_graphs=5,native=native,source_completeness='Retained external catalogue and software premises; not newly proved by replay.',full_census_repeated=False,private_runtime_fallback=False,whole_original_credit=0,new_question_credit=0,new_formal_declarations=0,new_measurements=0,seconds=time.monotonic()-start)
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');(out/'active.json').write_text(json.dumps({'status':'TERMINAL','returncode':0})+'\n');print(json.dumps(report))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--payload',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--expected-transport',required=True);p.add_argument('--gap',default='/opt/homebrew/bin/gap');p.add_argument('--pdflatex',default='/opt/homebrew/bin/pdflatex');main(p.parse_args())
