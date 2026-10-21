import sys
if sys.flags.optimize:raise SystemExit('normal Python required')
import argparse,hashlib,json,os,shutil,subprocess
from pathlib import Path
from pypdf import PdfReader
P=Path(__file__).resolve().parent
def need(ok,msg):
 if not ok:raise ValueError(msg)
def pin(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);arg=ap.parse_args();out=arg.out.resolve()
 need(not out.exists() and P not in out.parents,'fresh external output')
 manifest=json.loads((P/'manifest.json').read_text());deps=json.loads((P/'dependencies.json').read_text())
 for x in manifest['exports']:need(pin(P/x['path'])=={k:x[k]for k in ('bytes','sha256')},'export')
 for x in deps:need(pin(Path(x['path']))=={k:x[k]for k in ('bytes','sha256')},'dependency')
 out.mkdir(parents=True);env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
 def run(label,cmd,cwd=None):
  r=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,timeout=30);(out/(label+'.stdout')).write_bytes(r.stdout);(out/(label+'.stderr')).write_bytes(r.stderr);need(r.returncode==0,'command '+label);return r
 run('table',[sys.executable,str(P/'table_one.py'),'--out',str(out/'table.json')]);need(json.loads((out/'table.json').read_text())==json.loads((P/'expected.json').read_text()),'exact nine-row table')
 guards=[]
 for script in ['check.py','table_one.py']:
  for mode in ['argument','environment']:
   ee=dict(env);cmd=[sys.executable];target=out/(script+mode)
   if mode=='argument':cmd.append('-O')
   else:ee['PYTHONOPTIMIZE']='1'
   r=subprocess.run([*cmd,str(P/script),'--out',str(target)],env=ee,capture_output=True,timeout=5)
   need(r.returncode!=0 and b'normal Python required' in r.stderr and not target.exists(),'optimization rejected');guards.append([script,mode])
 native=out/'native';native.mkdir();shutil.copy2(P/'table_one.tex',native/'table_one.tex')
 for i in [1,2]:run('latex'+str(i),['/opt/homebrew/bin/pdflatex','-halt-on-error','-interaction=nonstopmode','table_one.tex'],native)
 need(not any(x in (native/'table_one.log').read_text() for x in ['Warning','Overfull','Underfull']),'clean native')
 txt=lambda p:[q.extract_text() for q in PdfReader(p).pages]
 need(txt(P/'table_one.pdf')==txt(native/'table_one.pdf'),'native text identity')
 run('render',['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r90','-sOutputFile=page-%02d.png','table_one.pdf'],native)
 result=dict(status='PASS_L027_TABLE_ONE',exports=len(manifest['exports']),dependencies=len(deps),rows=9,characteristic_polynomials=3,guards=guards,native_pages=len(txt(native/'table_one.pdf')),scope='Necessary parameter arithmetic, no IP classification inferred',whole_original_credit=0)
 (out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
