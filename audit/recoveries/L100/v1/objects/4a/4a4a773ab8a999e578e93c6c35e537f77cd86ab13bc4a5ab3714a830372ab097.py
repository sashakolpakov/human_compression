import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,hashlib,json,os,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent

def verify(p,r):
 b=p.read_bytes();assert len(b)==r['bytes']and hashlib.sha256(b).hexdigest()==r['sha256'],str(p)
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();out=a.out.absolute();assert not out.exists()
 m=json.loads((P/'manifest.json').read_text());deps=json.loads((P/'dependencies.json').read_text())
 for r in m['exports']:verify(P/r['path'],r)
 for r in deps:verify(Path(r['path']),r)
 out.mkdir(parents=True);cmd=[sys.executable,str(P/'repair.py'),'--out',str(out/'fresh')]
 q=subprocess.run(cmd,capture_output=True,timeout=120);(out/'stdout').write_bytes(q.stdout);(out/'stderr').write_bytes(q.stderr);assert q.returncode==0 and not q.stderr
 for p in (P/'derived').glob('*.json'):assert p.read_bytes()==(out/'fresh/decoded'/p.name).read_bytes()
 guards=[]
 for script in ['decode.py','structural.py','repair.py','check.py']:
  for mode in ['argument','environment']:
   denied=out/('DENIED_'+script+'_'+mode);env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
   if mode=='environment':env['PYTHONOPTIMIZE']='1'
   cmd=[sys.executable]+(['-O']if mode=='argument'else[])+[str(P/script),'--out',str(denied)];r=subprocess.run(cmd,capture_output=True,env=env,timeout=5)
   assert r.returncode!=0 and b'normal Python required'in r.stderr and not denied.exists();guards.append([script,mode])
 for r in m['exports']:verify(P/r['path'],r)
 for r in deps:verify(Path(r['path']),r)
 report=dict(status='PASS_FROZEN_PALETTE_SERIALIZATION_REPAIR',exports=len(m['exports']),dependencies=len(deps),guards=guards,scientific_files=61,graph_runs=0,source_credit=0);(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
