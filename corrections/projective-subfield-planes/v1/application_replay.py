"""Relocatable replay adapter; all acquired scientific programs remain literal."""
import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,hashlib,importlib.util,json,os,re,shutil,subprocess,time
def need(v,m):
 if not v:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--replay-independent',action='store_true');a=ap.parse_args()
 S=a.study.resolve();O=a.out.resolve();need(not O.exists()and not O.is_relative_to(S),'Fresh external output')
 A=S/'corpus106_PSL2_subfield_planes_v1';V=S/'corpus106_PSL2_subfield_planes_independent_review'
 old=V/'independent.stdout';receipt=load(V/'independent_receipt.json');code=V/'independent.g'
 need(receipt['status']=='PASS'and receipt['returncode']==0 and receipt['unchanged']is True and receipt['seconds']<receipt['deadline_seconds']==60,'Complete acquired witness execution')
 need(sha(code)==receipt['script']['sha256']and code.stat().st_size==receipt['script']['bytes'],'Exact executed independent script')
 need(not(V/'independent.stderr').read_bytes(),'Clean independent execution')
 normalize=lambda b:re.sub(rb'\s+',b'',b.replace(b'\\\n',b''))
 marker=b'PASS INDEPENDENT_GAP_GF512 orders=[134217216,504,448,56] intersection=56 local_degrees=[9,8] kernels=[1,8] ordered_pair_orbits=[72,56] planes=9'
 need(normalize(old.read_bytes())==normalize(marker),'Exact retained witness result')
 need(load(V/'fresh01/report.json')['status']=='PASS_PROJECTIVE_SUBFIELD_PLANES_COMPONENT','Accepted finite execution')
 O.mkdir(parents=True);env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1';commands=[];start=time.monotonic()
 def run(label,cmd,cwd=None,cap=60):
  t=time.monotonic()
  try:p=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,timeout=cap)
  except subprocess.TimeoutExpired as e:
   (O/(label+'.stdout')).write_bytes(e.stdout or b'');(O/(label+'.stderr')).write_bytes(e.stderr or b'');raise
  (O/(label+'.stdout')).write_bytes(p.stdout);(O/(label+'.stderr')).write_bytes(p.stderr)
  commands.append(dict(label=label,command=cmd,returncode=p.returncode,seconds=time.monotonic()-t));need(p.returncode==0 and not p.stderr,'Clean '+label);return p
 run('finite',[sys.executable,'-B',str(A/'finite.py'),'--out',str(O/'finite.json')])
 got=load(O/'finite.json');need(got==load(A/'expected.json'),'Exact four finite models')
 if a.replay_independent:
  gap=shutil.which('gap');need(gap,'GAP on PATH');p=run('independent',[gap,'-q','-T',str(code)]);need(normalize(p.stdout)==normalize(old.read_bytes()),'Same exact independent witness')
 spec=importlib.util.spec_from_file_location('unchanged_projective_plane_fields',A/'finite.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);damages=[]
 for q,f in [(4,5),(8,9)]:
  try:module.field(q,f)
  except AssertionError:damages.append(dict(q=q,polynomial=f,rejected=True))
  else:raise ValueError('Reducible polynomial accepted')
 guards=[]
 for program in [A/'check.py',A/'finite.py',Path(__file__).resolve()]:
  for mode in ['argument','environment']:
   target=O/(program.stem+'_'+mode);ee=dict(env)
   if mode=='environment':ee['PYTHONOPTIMIZE']='1'
   p=subprocess.run([sys.executable]+(['-O']if mode=='argument'else[])+[str(program),'--out',str(target)],env=ee,capture_output=True,timeout=15)
   (O/(program.stem+'_'+mode+'.stderr')).write_bytes(p.stderr);need(p.returncode!=0 and b'Ordinary Python required'in p.stderr and not target.exists(),'Pre-output optimization guard');guards.append([program.name,mode])
 from pypdf import PdfReader
 texts=lambda p:[page.extract_text()for page in PdfReader(p).pages]
 N=O/'native';N.mkdir();shutil.copyfile(A/'subfield_planes.tex',N/'subfield_planes.tex')
 need(not re.findall(r'\\(?:input|include)\s*\{([^}]+)\}',(N/'subfield_planes.tex').read_text()),'Complete native input inventory')
 for i in [1,2]:run('latex'+str(i),['pdflatex','-interaction=nonstopmode','-halt-on-error','subfield_planes.tex'],N)
 need(texts(N/'subfield_planes.pdf')==texts(A/'subfield_planes.pdf')and len(texts(N/'subfield_planes.pdf'))==3,'Complete native text')
 need(not any(x in(N/'subfield_planes.log').read_text()for x in ['Warning','Overfull','Underfull']),'Clean native')
 run('render',['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=pnggray','-r105','-sOutputFile=page-%02d.png','subfield_planes.pdf'],N)
 pages=sorted(N.glob('page-*.png'));need(len(pages)==3,'All native pages')
 need(all(sha(p)==sha(V/'fresh01/native'/p.name)for p in pages),'All rasters equal directly viewed distinct-review edition')
 report=dict(status='PASS_PUBLIC_PSL2_PLANES_APPLICATION',finite_replayed=True,independent_replayed=a.replay_independent,acquired_independent_execution=not a.replay_independent,independent_receipt_sha256=sha(V/'independent_receipt.json'),independent_stdout_sha256=sha(old),finite_sha256=sha(O/'finite.json'),finite_models=4,reducible_polynomial_controls=damages,optimization_guards=guards,native_pages=3,native_text_identical=True,native_rasters_equal_review=True,native_raster_sha256=[sha(p)for p in pages],commands=commands,author_scientific_code_unchanged=True,runtime_text_patching=False,private_fallback=False,general_proofs_verified_by_program=False,geometry_class_count_claimed=False,independent_mathematical_defects=1,source_ids=['L063','L064'],whole_original_credit=0,new_measurements=0,new_question_credit=0,new_Lean=0,seconds=time.monotonic()-start)
 (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
