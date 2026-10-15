"""Edition and native verification; the mathematical proof needs a distinct reader."""
import sys
if sys.flags.optimize:raise RuntimeError('Normal Python is required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,json,hashlib,subprocess,shutil,os

def need(ok,message):
 if not ok:raise ValueError(message)
def h(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');a=p.parse_args()
 P=Path(__file__).resolve().parent;O=a.out.resolve();need(not O.exists() and not O.is_relative_to(P),'fresh external output')
 M=json.loads((P/'manifest.json').read_text());D=json.loads((P/'dependencies.json').read_text())
 for x in M['exports']:need(h(P/x['path'])=={k:x[k]for k in ['bytes','sha256']},'changed export')
 for x in D:need(h(Path(x['path']))=={k:x[k]for k in ['bytes','sha256']},'changed dependency')
 O.mkdir(parents=True);guards=[]
 for mode in ['argument','environment']:
  env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
  if mode=='environment':env['PYTHONOPTIMIZE']='1'
  x=subprocess.run([sys.executable]+(['-O']if mode=='argument'else[])+[str(P/'check.py')],env=env,capture_output=True,timeout=10)
  (O/f'guard_{mode}.stderr').write_bytes(x.stderr);need(x.returncode!=0 and b'Normal Python is required'in x.stderr,'optimization guard');guards.append(mode)
 pages=None
 if a.render:
  from pypdf import PdfReader
  N=O/'native';N.mkdir();shutil.copyfile(P/'finite_quotients.tex',N/'finite_quotients.tex')
  for i in range(2):
   x=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','finite_quotients.tex'],cwd=N,capture_output=True,timeout=60)
   (N/f'build{i}.stdout').write_bytes(x.stdout);(N/f'build{i}.stderr').write_bytes(x.stderr);need(x.returncode==0 and not x.stderr,'native build')
  need(not any(t in (N/'finite_quotients.log').read_text()for t in ['Warning','Overfull','Underfull']),'clean native')
  old=[p.extract_text()for p in PdfReader(P/'finite_quotients.pdf').pages];new=[p.extract_text()for p in PdfReader(N/'finite_quotients.pdf').pages]
  need(old==new and len(new)==4,'complete native text');pages=4
  x=subprocess.run(['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png','finite_quotients.pdf'],cwd=N,capture_output=True,timeout=60);need(x.returncode==0 and not x.stderr,'native render')
 report=dict(status='PASS_L033_FINITE_QUOTIENTS_EDITION',exports=len(M['exports']),dependencies=len(D),optimization_guards=guards,native_pages=pages,mathematical_certificate=False,whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None)
 (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
