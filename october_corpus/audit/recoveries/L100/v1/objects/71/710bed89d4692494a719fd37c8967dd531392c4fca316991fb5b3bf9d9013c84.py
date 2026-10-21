import argparse,hashlib,json,os,subprocess,sys
from pathlib import Path
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
def verify(p,r):
 b=p.read_bytes();assert len(b)==r['bytes']and hashlib.sha256(b).hexdigest()==r['sha256'],str(p)
def main():
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);x=a.parse_args()
 manifest=json.loads((P/'manifest.json').read_text());deps=json.loads((P/'dependencies.json').read_text())
 for r in manifest['exports']:verify(P/r['path'],r)
 for r in deps:verify(Path(r['path']),r)
 out=x.out.absolute();assert not out.exists();out.mkdir(parents=True)
 cmd=[sys.executable,str(P/'bounded_controls.py'),'--out',str(out/'bounded')];p=subprocess.run(cmd,capture_output=True,timeout=120);(out/'stdout').write_bytes(p.stdout);(out/'stderr').write_bytes(p.stderr);assert p.returncode==0 and not p.stderr
 guards=[]
 for script in ['bounded_controls.py','check.py','literal_oracle.py']:
  for mode in ['argument','environment']:
   denied=out/('DENIED_'+script+'_'+mode);env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
   if mode=='environment':env['PYTHONOPTIMIZE']='1'
   cmd=[sys.executable]+(['-O']if mode=='argument'else[])+[str(P/script),'--out',str(denied)];q=subprocess.run(cmd,capture_output=True,env=env,timeout=5);assert q.returncode!=0 and b'normal Python required'in q.stderr and not denied.exists();guards.append([script,mode])
 report=dict(status='PASS_FROZEN_LITERAL_PALETTE_INTERFACE',exports=len(manifest['exports']),dependencies=len(deps),guards=guards,target_census_runs=0,L100_postprocessing_runs=0);(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
