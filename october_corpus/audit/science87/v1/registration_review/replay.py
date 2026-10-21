from pathlib import Path
import hashlib,json,subprocess,time
W=Path('/Users/sasha/medusa/research/leemans/reboot_20261013');A=W/'combined_dispositions_publication_work';O=W/'science87_distinct_review_work/fresh01';O.mkdir(exist_ok=False)
py='/Users/sasha/.venvs/global/bin/python'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(A/'ready_v3.json')=='c5f1dc132133b2d59ca98927d86f85ce0268e03757c6396d09f05f27c424176f'
assert sha(A/'handoff_v3_manifest.json')=='8f2b8284c9e76aa86bdef4ec21636c62b1944f63133f5ff9b6980d953551d354'
prior=json.loads((W/'science87_distinct_review_work/independent01/receipt.json').read_text())
for x in prior['inputs']:
 p=A/'trial02'/x['path'];assert p.stat().st_size==x['bytes']and sha(p)==x['sha256'],x['path']
commands=[('handoff',[py,str(A/'verify_handoff.py'),'--candidate',str(A/'trial02')]),('preflight',[py,str(A/'trial02/scripts/check_science87.py'),'--repo',str(A/'trial02'),'--preflight'])]
receipts=[]
for name,cmd in commands:
 t=time.monotonic();result=subprocess.run(cmd,cwd=A,capture_output=True,timeout=300)
 (O/(name+'.stdout')).write_bytes(result.stdout);(O/(name+'.stderr')).write_bytes(result.stderr)
 rec=dict(name=name,command=cmd,cwd=str(A),returncode=result.returncode,seconds=time.monotonic()-t,stdout_sha256=sha(O/(name+'.stdout')),stderr_sha256=sha(O/(name+'.stderr')))
 receipts.append(rec);(O/'receipt.json').write_text(json.dumps(dict(status='RUNNING',steps=receipts),indent=2)+'\n')
 if result.returncode or result.stderr:raise RuntimeError(rec)
 print(name,result.stdout.decode().strip(),flush=True)
for x in prior['inputs']:
 p=A/'trial02'/x['path'];assert p.stat().st_size==x['bytes']and sha(p)==x['sha256'],x['path']
(O/'receipt.json').write_text(json.dumps(dict(status='PASS_FROZEN_SCIENCE87_REGISTRATION_REPLAY',steps=receipts,prior_independent_inputs_unchanged=True,no_mathematical_replay=True,no_public_writes=True),indent=2)+'\n')
