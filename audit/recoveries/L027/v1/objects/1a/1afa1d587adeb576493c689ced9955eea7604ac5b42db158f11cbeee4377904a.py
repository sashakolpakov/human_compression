import sys
if sys.flags.optimize:raise SystemExit('normal Python required')
import argparse,hashlib,json,os,re,shutil,subprocess,time
from pathlib import Path
from pypdf import PdfReader
P=Path(__file__).resolve().parent
def need(ok,msg):
 if not ok:raise ValueError(msg)
def pin(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def verify(p,x):need(pin(p)=={k:x[k] for k in ('bytes','sha256')},'changed input '+str(p))
def parse(b):
 lines=b.decode().replace('\r','').splitlines()
 need(len(lines)==68 and lines[-1]=='PASS_ALL_ODD_THREE_CONTROLS','complete finite receipt')
 need(sum(t.startswith('GENERIC ') for t in lines)==50,'exact affine roster')
 need(sum(t.startswith('TRIANGULAR ') for t in lines)==9,'exact triangular roster')
 need(sum(t.startswith('CONIC ') for t in lines)==4,'exact conic roster')
 need(sum(t.startswith('UNIPOTENT ') for t in lines)==4,'exact unipotent roster')
 for t in lines[:-1]:need(t.endswith(' PASS'),'explicit successful receipt')
 return lines

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);arg=ap.parse_args();out=arg.out.resolve()
 need(not out.exists() and out!=P and P not in out.parents,'fresh external output')
 manifest=json.loads((P/'manifest.json').read_text());deps=json.loads((P/'dependencies.json').read_text())
 for x in manifest['exports']:verify(P/x['path'],x)
 for x in deps:verify(Path(x['path']),x)
 out.mkdir(parents=True);env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);commands=[]
 def run(label,cmd,cap,cwd=None):
  start=time.monotonic();r=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,timeout=cap)
  (out/(label+'.stdout')).write_bytes(r.stdout);(out/(label+'.stderr')).write_bytes(r.stderr)
  commands.append(dict(label=label,command=cmd,returncode=r.returncode,seconds=time.monotonic()-start))
  need(r.returncode==0,'command '+label);return r
 run('literal',[sys.executable,str(P/'literal.py'),'--out',str(out/'literal.json')],30)
 literal=json.loads((out/'literal.json').read_text());need(literal==json.loads((P/'literal_expected.json').read_text()),'literal identities')
 r=run('finite',['/opt/homebrew/bin/gap','-q','-b',str(P/'finite.g')],120)
 need(not r.stderr,'finite clean stderr');lines=parse(r.stdout);need(lines==json.loads((P/'finite_expected.json').read_text()),'exact controls')
 guards=[]
 for mode in ['argument','environment']:
  ee=dict(env);cmd=[sys.executable];target=out/('optimized_'+mode)
  if mode=='argument':cmd.append('-O')
  else:ee['PYTHONOPTIMIZE']='1'
  r=subprocess.run([*cmd,str(P/'check.py'),'--out',str(target)],env=ee,capture_output=True,timeout=10)
  need(r.returncode!=0 and b'normal Python required' in r.stderr and not target.exists(),'optimization rejected');guards.append(mode)
 native=out/'native';native.mkdir();shutil.copy2(P/'odd_three.tex',native/'odd_three.tex')
 for i in [1,2]:run('latex'+str(i),['/opt/homebrew/bin/pdflatex','-halt-on-error','-interaction=nonstopmode','odd_three.tex'],30,native)
 log=(native/'odd_three.log').read_text();need(all(t not in log for t in ['Warning','Overfull','Underfull']),'clean native')
 texts=lambda p:[q.extract_text() for q in PdfReader(p).pages]
 need(texts(native/'odd_three.pdf')==texts(P/'odd_three.pdf'),'native text identity')
 run('render',['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png','odd_three.pdf'],30,native)
 result=dict(status='PASS_L027_ODD_THREE_CONTROLS',exports=len(manifest['exports']),dependencies=len(deps),identities=literal['count'],affine_models=50,triangular_models=9,conic_markings=4,actual_subset_pairs=11584,unipotent_fields=4,guards=guards,native_pages=len(texts(native/'odd_three.pdf')),commands=commands,proof_status='Uniform written proof, bounded controls only',whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None)
 (out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
