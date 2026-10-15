"""Rehash the packet then run only bounded small-model and preparation controls."""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
if not __debug__:raise SystemExit('optimized execution forbidden')
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
def main():
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);ns=a.parse_args();out=ns.out.absolute();out.mkdir(parents=True,exist_ok=False)
 for row in json.loads((HERE/'manifest.json').read_text())['exports']:
  p=Path(row['path']);assert not p.is_absolute() and '..' not in p.parts
  b=(HERE/p).read_bytes();assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
 for name,folder in [('controls.py','bounded'),('caller_control.py','tiny_caller')]:
  cmd=[sys.executable,str(HERE/name),'--out',str(out/folder)]
  with (out/(folder+'.stdout')).open('wb') as so,(out/(folder+'.stderr')).open('wb') as se:
   r=subprocess.run(cmd,stdout=so,stderr=se,timeout=65)
  assert r.returncode==0 and not (out/(folder+'.stderr')).read_bytes()
 (out/'report.json').write_text(json.dumps(dict(status='PASS_PARTIAL_FUSION_INTERFACE_REPLAY',target_census_runs=0,L100_postprocessing_runs=0,children=['bounded/report.json','tiny_caller/report.json']),indent=2)+'\n')
 print('PASS_PARTIAL_FUSION_INTERFACE_REPLAY')
if __name__=='__main__':main()
