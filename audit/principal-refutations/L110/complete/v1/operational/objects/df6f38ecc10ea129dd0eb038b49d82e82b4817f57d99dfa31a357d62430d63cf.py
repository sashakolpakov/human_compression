"""Read-only bindings and fresh TeX replay; no group or discovery process."""
from pathlib import Path
import argparse,hashlib,json,subprocess,shutil,sys,time
from pypdf import PdfReader
if not __debug__:raise SystemExit('optimization is not admitted')
C=Path(__file__).resolve().parent
def need(x,s):
 if not x:raise ValueError(s)
def pin(p,base=None):
 b=p.read_bytes();return dict(path=str(p.relative_to(base) if base else p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def verify(row,base=None):
 p=Path(row['path']) if base is None else base/row['path'];need(pin(p,base)==row,'binding mismatch '+str(p))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);ap.add_argument('--render',action='store_true');a=ap.parse_args();o=a.out.resolve();need(not o.exists(),'fresh output required');o.mkdir(parents=True);t=time.monotonic()
 deps=json.loads((C/'dependencies.json').read_text());mf=json.loads((C/'manifest.json').read_text())
 for r in deps:verify(r)
 for r in mf['exports']:verify(r,C)
 old=[]
 for source,review,key in [('phase7_suzuki_descent.md','phase7_suzuki_audit.json','reviewed_hashes'),('phase7_suzuki_torus_families.md','phase7_suzuki_families_audit.json','reviewed_hashes'),('phase8_suzuki_subfields.md','phase8_suzuki_subfields_independent_audit.json','sha256')]:
  src=next(Path(r['path']) for r in deps if Path(r['path']).name==source);rev=next(Path(r['path']) for r in deps if Path(r['path']).name==review)
  need(pin(src)['sha256']==json.loads(rev.read_text())[key][source],'old reviewed proof differs');old.append(source)
 parts=json.loads((C/'parts.json').read_text());native=[]
 for part in parts:
  s=part['stem'];shutil.copyfile(C/(s+'.tex'),o/(s+'.tex'))
  for run in [1,2]:
   p=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error',s+'.tex'],cwd=o,capture_output=True)
   (o/f'{s}_build{run}.stdout').write_bytes(p.stdout);(o/f'{s}_build{run}.stderr').write_bytes(p.stderr);need(p.returncode==0,'native build '+s)
  x,y=PdfReader(C/(s+'.pdf')),PdfReader(o/(s+'.pdf'));need(len(x.pages)==len(y.pages)==part['pages'],'page count '+s)
  for p,q in zip(x.pages,y.pages):need(''.join(p.extract_text().split())==''.join(q.extract_text().split()),'native text '+s)
  if a.render:
   p=subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=pnggray','-r90',f'-sOutputFile={s}-%02d.png',s+'.pdf'],cwd=o,capture_output=True)
   (o/f'{s}_render.stdout').write_bytes(p.stdout);(o/f'{s}_render.stderr').write_bytes(p.stderr);need(p.returncode==0,'native render '+s)
  native.append(part)
 # Reader damage controls, without changing any acquired input.
 controls=[]
 for field,value in [('bytes',deps[0]['bytes']+1),('sha256','0'*64)]:
  r=dict(deps[0]);r[field]=value
  try:verify(r)
  except ValueError:controls.append('reject changed '+field)
  else:raise ValueError('damaged binding accepted')
 for flag in ['-O','-OO']:
  p=subprocess.run([sys.executable,flag,str(C/'check.py'),'--out',str(o/('forbidden'+flag))],capture_output=True)
  need(p.returncode!=0 and b'optimization is not admitted' in p.stderr,'optimization guard');controls.append(flag+' rejected')
 report=dict(status='PASS',dependency_bindings=len(deps),export_bindings=len(mf['exports']),old_reviewed_proofs=old,native=native,controls=controls,target_calls=0,elapsed_seconds=time.monotonic()-t,scope='Native assembly and exact old evidence acquisition; mathematical claims require distinct written review.')
 (o/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
