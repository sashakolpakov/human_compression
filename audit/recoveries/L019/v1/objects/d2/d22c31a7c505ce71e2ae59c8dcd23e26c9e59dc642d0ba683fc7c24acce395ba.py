"""Directory-local bounded verification; leaves author inputs untouched."""
from pathlib import Path
import argparse,json,os,subprocess,sys,time,hashlib,shutil
if sys.flags.optimize:raise SystemExit('optimized Python is unsupported')
def need(x,m):
 if not x:raise ValueError(m)
def pin(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();w=Path(__file__).resolve().parent;out=args.out.resolve();need(not out.exists(),'fresh directory required');out.mkdir(parents=True)
 env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1';receipts=[]
 def run(name,cmd,inputs,good=True,childenv=env):
  before=[pin(p) for p in inputs];st=time.monotonic();v=subprocess.run(cmd,cwd=out,env=childenv,capture_output=True,timeout=45);(out/(name+'.stdout')).write_bytes(v.stdout);(out/(name+'.stderr')).write_bytes(v.stderr);need(before==[pin(p) for p in inputs],'changed input');receipts.append({'name':name,'command':cmd,'input_pins':before,'returncode':v.returncode,'deadline_seconds':45,'seconds':time.monotonic()-st});(out/'receipts.json').write_text(json.dumps(receipts,indent=2)+'\n');need((v.returncode==0)==good,'wrong exit '+name)
  if good:need(not v.stderr,'stderr '+name)
  return v
 a=run('direct',[sys.executable,'-B',str(w/'check_a10.py'),'--out',str(out/'direct_report.json')],[w/'check_a10.py',w/'permutation_library.py',w/'a10_inputs.json']);need(b'PASS_A10_ATTACHMENT_OBSTRUCTIONS' in a.stdout,'direct completion')
 b=run('gap',['/opt/homebrew/bin/gap','-q','-T',str(w/'a10_gap.g')],[w/'a10_gap.g']);need(b'PASS_A10_GAP' in b.stdout,'gap completion')
 data=json.loads((w/'a10_inputs.json').read_text())
 for name in ['missing','damaged']:
  d=json.loads(json.dumps(data))
  if name=='missing':d['representatives'].pop()
  else:d['representatives'][0]['permutations'][0][0]=0
  p=out/(name+'.json');p.write_text(json.dumps(d));run(name,[sys.executable,'-B',str(w/'check_a10.py'),'--input',str(p),'--out',str(out/(name+'_forbidden.json'))],[p,w/'check_a10.py',w/'permutation_library.py'],good=False);need(not (out/(name+'_forbidden.json')).exists(),'damaged accepted')
 for mode in ['flag','environment']:
  cmd=[sys.executable,'-B']+(['-O'] if mode=='flag' else [])+[str(w/'check_a10.py'),'--out',str(out/(mode+'_forbidden.json'))]
  run(mode,cmd,[w/'check_a10.py'],good=False,childenv=dict(env,PYTHONOPTIMIZE='1') if mode=='environment' else env);need(not (out/(mode+'_forbidden.json')).exists(),'optimized accepted')
 report={'status':'PASS_EXACT_A10_ATTACHMENT_FILTER','rows':10,'orientations':20,'index_six_obstructions':4,'rejection_controls':4,'new_census':False,'whole_original_credit':0}
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
