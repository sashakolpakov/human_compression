"""Bounded exact replay of the first critical symmetric factors."""
import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
import argparse,ast,hashlib,json,os,shutil,subprocess,time
from pathlib import Path
def need(x,m):
 if not x:raise ValueError(m)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args();here=Path(__file__).resolve().parent;out=a.out.resolve();need(not out.exists(),'fresh output');out.mkdir(parents=True)
 m=json.loads((here/'manifest.json').read_text());d=json.loads((here/'dependencies.json').read_text())
 for base,rows in [(here,m['exports']),(a.study,d)]:
  for r in rows:
   p=base/r['path'];v=p.read_bytes();need(len(v)==r['bytes']and hashlib.sha256(v).hexdigest()==r['sha256'],'binding '+str(p))
 env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);receipts=[]
 def run(name,args,cwd=out,success=True):
  start=time.monotonic()
  try:r=subprocess.run(args,cwd=cwd,env=env,capture_output=True,timeout=45)
  except subprocess.TimeoutExpired as e:
   for ext,v in [('stdout',e.stdout),('stderr',e.stderr)]: (out/(name+'.'+ext)).write_bytes(v or b'')
   (out/(name+'_timeout.json')).write_text(json.dumps({'status':'TIMEOUT_NO_CERTIFICATE','args':args,'cap':45})+'\n');raise
  for ext,v in [('stdout',r.stdout),('stderr',r.stderr)]: (out/(name+'.'+ext)).write_bytes(v)
  receipts.append({'name':name,'args':args,'returncode':r.returncode,'seconds':time.monotonic()-start,'cap':45});(out/'receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
  need((r.returncode==0 and not r.stderr)if success else r.returncode!=0,'run '+name)
  return r.stdout.decode().replace('\r','')
 for name,marker in [('six','SUMMARY all=32 fractured=24 bad=0'),('eight','COMPLETE_ANCHORED_CRITICAL_SYMMETRIC|')]:
  text=run(name,['/opt/homebrew/bin/gap','-q','-T',str(here/(name+'.g'))]);need(text==(here/(name+'.stdout')).read_bytes().decode().replace('\r','')and text.count(marker)==1,'complete exact census '+name)
  if name=='eight':
   rows=[ast.literal_eval(line.split('|',4)[4])for line in text.splitlines()if line.startswith('SOLUTION|')];need(rows==json.loads((here/'eight_tuples.json').read_text()),'literal arrays from full census')
 run('literal',[sys.executable,str(here/'verify_eight.py'),'--out',str(out/'literal.json')]);need(json.loads((out/'literal.json').read_text())==json.loads((here/'direct_report.json').read_text()),'literal result')
 for mode in ['-O','-OO']:run('reject'+mode,[sys.executable,mode,str(here/'verify_eight.py'),'--out',str(out/(mode+'.json'))],success=False)
 run('reject_missing',[sys.executable,str(here/'verify_eight.py'),'--input',str(out/'absent.json'),'--out',str(out/'missing.json')],success=False)
 (out/'truncated.json').write_text('[]\n');run('reject_truncated',[sys.executable,str(here/'verify_eight.py'),'--input',str(out/'truncated.json'),'--out',str(out/'truncated_result.json')],success=False)
 if a.render:
  native=out/'native';native.mkdir()
  for name in ['build.py','small_symmetric.tex']:shutil.copy2(here/name,native/name)
  run('native',[sys.executable,str(native/'build.py')],native)
 report={'status':'PASS_SMALL_SYMMETRIC_BOUNDARY','exports':len(m['exports']),'dependencies':len(d),'S6_terminals':32,'S6_fractured_sufficient':24,'S8_natural_tuples':9,'S8_fractured':8,'S8_pure_first':6,'S8_even_kernel_obstructions':2,'negative_controls':4,'whole_original_credit':0};(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
