"""Explicit public L041 adapter; original scientific controls remain unchanged."""
import sys
if sys.flags.optimize:raise RuntimeError('Unoptimized Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,json,os,shutil,subprocess,time
def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();P=a.author.resolve();O=a.out.resolve()
 need(not O.exists()and not O.is_relative_to(P),'Fresh external output');O.mkdir(parents=True);start=time.monotonic();env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
 p=subprocess.run([sys.executable,'-B',str(P/'check_decorations.py')],capture_output=True,env=env,timeout=180);(O/'finite.stdout').write_bytes(p.stdout);(O/'finite.stderr').write_bytes(p.stderr)
 need(p.returncode==0 and not p.stderr,'Unchanged finite controls');finite=json.loads(p.stdout.splitlines()[-1]);need(finite==load(P/'finite_expected.json'),'Exact five-field control output')
 guards=[]
 for file in [P/'check.py',P/'check_decorations.py',Path(__file__).resolve()]:
  for mode in ['argument','environment']:
   target=O/(file.stem+'_'+mode);e=dict(env)
   if mode=='environment':e['PYTHONOPTIMIZE']='1'
   q=subprocess.run([sys.executable]+(['-O']if mode=='argument'else[])+[str(file),'--out',str(target)],capture_output=True,env=e,timeout=15);(O/(file.stem+'_'+mode+'.stderr')).write_bytes(q.stderr)
   need(q.returncode!=0 and b'Python'in q.stderr and not target.exists(),'Pre-output optimization guard');guards.append([file.name,mode])
 from pypdf import PdfReader
 def texts(p):return [page.extract_text()for page in PdfReader(p).pages]
 expected=texts(P/'decorated_points.pdf');need(len(expected)==8,'Complete eight-page manuscript')
 N=O/'native';N.mkdir()
 for name in ['decorated_points.tex','tetrahedra_section.tex']:shutil.copyfile(P/name,N/name)
 for k in [1,2]:
  q=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','decorated_points.tex'],cwd=N,env=env,capture_output=True,timeout=60);(N/f'build{k}.stdout').write_bytes(q.stdout);(N/f'build{k}.stderr').write_bytes(q.stderr);need(q.returncode==0 and not q.stderr,'Native build')
 need(texts(N/'decorated_points.pdf')==expected,'All eight native page texts identical');log=(N/'decorated_points.log').read_text();need(not any(s in log for s in ['Warning','Overfull','Underfull']),'Clean native log')
 q=subprocess.run(['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png','decorated_points.pdf'],cwd=N,env=env,capture_output=True,timeout=60);(N/'render.stdout').write_bytes(q.stdout);(N/'render.stderr').write_bytes(q.stderr);need(q.returncode==0 and not q.stderr and len(list(N.glob('page-*.png')))==8,'Eight native rasters')
 report=dict(status='PASS_PUBLIC_L041_APPLICATION',finite_fields=[r['q']for r in finite['cases']],finite_exact=True,optimization_guards=guards,native_pages=8,native_text_identical=True,author_scientific_code_unchanged=True,runtime_text_patching=False,original_documentary_assets_read=False,acquired_censuses_repeated=False,Lean_repeated=False,general_proof_verified_by_program=False,whole_original_credit=0,new_question_credit=0,new_Lean=0,new_measurements=0,seconds=time.monotonic()-start)
 (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
