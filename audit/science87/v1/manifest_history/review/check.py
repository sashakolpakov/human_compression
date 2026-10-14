import sys
if sys.flags.optimize: raise RuntimeError("Ordinary Python required")
import argparse,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--study',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);a=p.parse_args();here=Path(__file__).resolve().parent
def verify(base,r):
 q=base/r['path'];raw=q.read_bytes()
 if len(raw)!=r['bytes'] or hashlib.sha256(raw).hexdigest()!=r['sha256']:raise ValueError('Changed binding '+str(q))
m=json.loads((here/'manifest.json').read_text())
for r in m['exports']:verify(here,r)
d=json.loads((here/'dependencies.json').read_text())
for r in d:verify(a.repo if r['namespace']=='public' else a.study,r)
print(json.dumps(dict(status='PASS',exports=len(m['exports']),dependencies=len(d),no_mathematical_replay=True)))
