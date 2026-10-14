#!/usr/bin/env python3
"""Read-only identity check for this private handoff, not scientific acceptance."""
import argparse,hashlib,json,pathlib
if not __debug__: raise SystemExit('Optimized execution is not allowed')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--candidate',type=pathlib.Path);a=ap.parse_args()
 root=pathlib.Path(__file__).resolve().parent
 def load(p):return json.loads(p.read_text())
 def check(base,row):
  rel=pathlib.Path(row['path'])
  if rel.is_absolute() or '..' in rel.parts:raise RuntimeError('Unsafe relative path')
  p=base/rel;b=p.read_bytes()
  if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:raise RuntimeError('Identity mismatch: '+str(p))
 ready=load(root/'ready_v3.json');check(root,ready['manifest'])
 m=load(root/ready['manifest']['path'])
 for r in m['files']:check(root,r)
 aliases=load(root/'historical_aliases_v3.json')['aliases']
 for x in aliases:check(root,dict(path=x['retained_exact_file'],bytes=x['bytes'],sha256=x['sha256']))
 n=0
 if a.candidate:
  for r in load(root/'candidate_manifest_v3.json')['files']:check(a.candidate,r);n+=1
 print(json.dumps(dict(status='PASS_EXACT_HANDOFF_IDENTITIES',handoff_files=len(m['files']),historical_aliases=len(aliases),candidate_files=n,public_writes=False)))
if __name__=='__main__':main()
