"""Check frozen bytes and run bounded incremental controls; no L100 fusion."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
if not __debug__:raise SystemExit('optimized execution forbidden')
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
def require(v,msg):
 if not v:raise ValueError(msg)
def verify(row,root=None):
 p=Path(row['path'])
 if root is not None:
  require(not p.is_absolute() and '..' not in p.parts,'safe export');p=root/p
 b=p.read_bytes();require(len(b)==row['bytes']and hashlib.sha256(b).hexdigest()==row['sha256'],'changed binding '+str(p))
def main():
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);ns=a.parse_args();out=ns.out.absolute()
 manifest=json.loads((HERE/'manifest.json').read_text())
 for r in manifest['exports']:verify(r,HERE)
 deps=json.loads((HERE/'dependencies.json').read_text())
 for r in deps:verify(r)
 out.mkdir(parents=True,exist_ok=False)
 cmd=[sys.executable,str(HERE/'controls.py'),'--out',str(out/'bounded')]
 with(out/'stdout').open('wb')as so,(out/'stderr').open('wb')as se:
  p=subprocess.run(cmd,stdout=so,stderr=se,timeout=90)
 require(p.returncode==0 and not(out/'stderr').read_bytes(),'clean bounded controls')
 r=json.loads((out/'bounded/report.json').read_text());require(r['status']=='PASS_INCREMENTAL_FUSION_CONTROLS_NO_L100_POSTPROCESSING','control status')
 report=dict(status='PASS_INCREMENTAL_FUSION_INTERFACE_REPLAY',exports=len(manifest['exports']),dependencies=len(deps),child='bounded/report.json',target_census_runs=0,L100_postprocessing_runs=0)
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
