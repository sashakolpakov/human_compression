"""Edition/native checks and supplementary examples, not a formal proof checker."""
import sys
if sys.flags.optimize:raise RuntimeError('Normal Python is required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,json,hashlib,subprocess,os,shutil
from commutators import run,need
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');a=p.parse_args()
 P=Path(__file__).resolve().parent;O=a.out.resolve();need(not O.exists() and not O.is_relative_to(P),'fresh external output')
 manifest=json.loads((P/'manifest.json').read_text());deps=json.loads((P/'dependencies.json').read_text())
 for r in manifest['exports']:
  data=(P/r['path']).read_bytes();need(len(data)==r['bytes']and hashlib.sha256(data).hexdigest()==r['sha256'],'changed export')
 for r in deps:
  data=Path(r['path']).read_bytes();need(len(data)==r['bytes']and hashlib.sha256(data).hexdigest()==r['sha256'],'changed dependency')
 O.mkdir(parents=True);result=run();need(result==json.loads((P/'commutators.json').read_text()),'example agreement')
 (O/'commutators.json').write_text(json.dumps(result,indent=2)+'\n')
 guards=[]
 for name in ['check.py','commutators.py']:
  for mode in ['argument','environment']:
   env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
   if mode=='environment':env['PYTHONOPTIMIZE']='1'
   cmd=[sys.executable]+(['-O']if mode=='argument'else[])+[str(P/name)]
   x=subprocess.run(cmd,env=env,capture_output=True,timeout=10);(O/(name+'_'+mode+'.stderr')).write_bytes(x.stderr)
   need(x.returncode!=0 and b'Normal Python is required'in x.stderr,'optimization guard');guards.append([name,mode])
 native=None
 if a.render:
  from pypdf import PdfReader
  N=O/'native';N.mkdir();shutil.copyfile(P/'translation_kernel.tex',N/'translation_kernel.tex')
  for i in range(2):
   x=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','translation_kernel.tex'],cwd=N,capture_output=True,timeout=60)
   (N/f'build{i}.stdout').write_bytes(x.stdout);(N/f'build{i}.stderr').write_bytes(x.stderr);need(x.returncode==0 and not x.stderr,'native build')
  need(not any(t in (N/'translation_kernel.log').read_text()for t in ['Overfull','Underfull','Warning']),'clean native')
  old=[p.extract_text()for p in PdfReader(P/'translation_kernel.pdf').pages];new=[p.extract_text()for p in PdfReader(N/'translation_kernel.pdf').pages];need(old==new and len(new)==3,'complete native text')
  x=subprocess.run(['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png','translation_kernel.pdf'],cwd=N,capture_output=True,timeout=60);(N/'render.stderr').write_bytes(x.stderr);need(x.returncode==0 and not x.stderr,'native render');native=3
 out=dict(status='PASS_L033_TRANSLATION_KERNEL_COMPONENT',exports=len(manifest['exports']),dependencies=len(deps),supplementary_examples=result,optimization_guards=guards,native_pages=native,written_uniform_proof_requires_distinct_review=True,whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None)
 (O/'report.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
