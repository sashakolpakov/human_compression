"""Replay the explicit hypermap counterexample and its fixed native manuscript."""
import sys
if sys.flags.optimize:raise RuntimeError('unoptimized execution required')
import argparse,hashlib,json,os,shutil,subprocess
from pathlib import Path
from verify import need,verify
P=Path(__file__).resolve().parent
def pin(p,x):
 b=p.read_bytes();need(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],'binding '+str(p))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 m=json.loads((P/'manifest.json').read_text())
 for x in m['exports']:pin(P/x['path'],x)
 deps=json.loads((P/'dependencies.json').read_text())
 for x in deps:pin(a.study/x['path'],x)
 result=json.loads(json.dumps(verify()));need(result==json.loads((P/'expected.json').read_text()),'literal complete report')
 env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
 guards=[]
 for f in ['verify.py','check.py']:
  z=subprocess.run([sys.executable,'-O',str(P/f)],env=env,capture_output=True,text=True,timeout=10)
  (a.out/(f+'.guard.stderr')).write_text(z.stderr);need(z.returncode!=0 and 'unoptimized execution required' in z.stderr,'optimization guard');guards.append(f)
 if a.render:
  from pypdf import PdfReader
  d=a.out/'native';d.mkdir();shutil.copy2(P/'hypermap.tex',d/'hypermap.tex')
  for i in range(2):
   z=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','hypermap.tex'],cwd=d,env=env,capture_output=True,text=True,timeout=60)
   (d/f'pass{i}.stdout').write_text(z.stdout);(d/f'pass{i}.stderr').write_text(z.stderr);need(z.returncode==0,'native build')
  need('undefined' not in z.stdout.lower() and 'Overfull' not in z.stdout,'native warnings')
  src=PdfReader(P/'hypermap.pdf');out=PdfReader(d/'hypermap.pdf');need(len(src.pages)==len(out.pages)==2,'native pages');need([p.extract_text()for p in src.pages]==[p.extract_text()for p in out.pages],'native text')
  z=subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile=page-%02d.png','hypermap.pdf'],cwd=d,capture_output=True,timeout=60);need(z.returncode==0,'native raster')
 report={'status':'PASS','exports':len(m['exports']),'bindings':len(deps),'literal':result,'optimization_guards':guards,'native_pages':2 if a.render else None,'whole_original_credit':0,'named_conjecture_credit':0}
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
