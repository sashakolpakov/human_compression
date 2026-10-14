"""Explicit public adapter: unchanged finite certificate and complete native proof."""
import sys
if sys.flags.optimize:raise RuntimeError('Unoptimized Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,json,os,shutil,subprocess,time
def need(v,m):
 if not v:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();P=a.author.resolve();O=a.out.resolve()
 need(not O.exists()and not O.is_relative_to(P),'Fresh external output');O.mkdir(parents=True);start=time.monotonic();env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
 cmd=[sys.executable,'-B',str(P/'finite.py'),'--out',str(O/'finite.json')]
 q=subprocess.run(cmd,env=env,capture_output=True,timeout=60);(O/'finite.stdout').write_bytes(q.stdout);(O/'finite.stderr').write_bytes(q.stderr);need(q.returncode==0 and not q.stderr,'Unchanged finite certificate');finite=load(O/'finite.json');need(finite==load(P/'expected.json'),'Exact finite output')
 damage=[]
 for mode in ['mark','edge','local_pattern']:
  q=subprocess.run([sys.executable,'-B',str(P/'finite.py'),'--out',str(O/('bad_'+mode+'.json')),'--damage',mode],env=env,capture_output=True,timeout=60);(O/f'damage_{mode}.stderr').write_bytes(q.stderr);need(q.returncode!=0 and b'ValueError'in q.stderr,'Damaged example rejected');damage.append(mode)
 guards=[]
 for f in [P/'check.py',P/'finite.py',Path(__file__).resolve()]:
  for mode in ['argument','environment']:
   target=O/(f.stem+'_'+mode);e=dict(env)
   if mode=='environment':e['PYTHONOPTIMIZE']='1'
   q=subprocess.run([sys.executable]+(['-O']if mode=='argument'else[])+[str(f),'--out',str(target)],env=e,capture_output=True,timeout=15);(O/(f.stem+'_'+mode+'.stderr')).write_bytes(q.stderr);need(q.returncode!=0 and (b'optimized execution is unsupported'in q.stderr or b'Unoptimized Python required'in q.stderr)and not target.exists(),'Pre-output optimization guard');guards.append([f.name,mode])
 from pypdf import PdfReader
 def texts(p):return [page.extract_text()for page in PdfReader(p).pages]
 expected=texts(P/'counterexample.pdf');need(len(expected)==5,'Complete five-page proof');N=O/'native';N.mkdir();shutil.copyfile(P/'counterexample.tex',N/'counterexample.tex')
 for i in range(2):
  q=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','counterexample.tex'],cwd=N,env=env,capture_output=True,timeout=60);(N/f'build{i}.stdout').write_bytes(q.stdout);(N/f'build{i}.stderr').write_bytes(q.stderr);need(q.returncode==0 and not q.stderr,'Native build')
 need(texts(N/'counterexample.pdf')==expected,'All five page texts identical');need(not any(x in(N/'counterexample.log').read_text()for x in ['Warning','Overfull','Underfull']),'Clean native log')
 q=subprocess.run(['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png','counterexample.pdf'],cwd=N,env=env,capture_output=True,timeout=60);(N/'render.stdout').write_bytes(q.stdout);(N/'render.stderr').write_bytes(q.stderr);need(q.returncode==0 and not q.stderr and len(list(N.glob('page-*.png')))==5,'Five native rasters')
 report=dict(status='PASS_PUBLIC_L029_APPLICATION',vertices=finite['vertices'],objects=112,chambers=finite['chambers'],specified_group_order=finite['G_order'],full_group_order=finite['full_matrix_action_order'],subset_intersections=finite['subset_intersections_checked'],actual_panels=finite['actual_panels_checked'],residue_component_sizes=[len(c)for c in finite['actual_residue_components']],finite_exact=True,damage_controls=damage,optimization_guards=guards,native_pages=5,native_text_identical=True,author_scientific_code_unchanged=True,runtime_text_patching=False,original_documentary_assets_read=False,acquired_censuses_repeated=False,independent_GAP_repeated=False,Lean_repeated=False,general_proof_verified_by_program=False,whole_original_credit=0,new_measurements=0,new_question_credit=0,new_Lean=0,seconds=time.monotonic()-start)
 (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
