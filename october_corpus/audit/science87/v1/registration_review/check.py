"""Read-only exact review binding check; no mathematical or target replay."""
import sys
if sys.flags.optimize:raise SystemExit('Ordinary Python required')
from pathlib import Path
import argparse,hashlib,json
p=argparse.ArgumentParser();p.add_argument('--study',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);a=p.parse_args();root=Path(__file__).resolve().parent
m=json.loads((root/'manifest.json').read_text())
def check(base,r):
 rel=Path(r['path'])
 if rel.is_absolute()or'..'in rel.parts:raise ValueError('Unsafe relative input')
 raw=(base/rel).read_bytes()
 if len(raw)!=r['bytes']or hashlib.sha256(raw).hexdigest()!=r['sha256']:raise ValueError(str(base/rel))
for r in m['exports']:check(root,r)
d=json.loads((root/'dependencies.json').read_text())
for r in d:check(a.study if r['namespace']=='study'else a.repo,r)
print(json.dumps(dict(status='PASS_EXACT_SCIENCE87_REGISTRATION_REVIEW_BINDINGS',exports=len(m['exports']),dependencies=len(d),no_public_writes=True)))
