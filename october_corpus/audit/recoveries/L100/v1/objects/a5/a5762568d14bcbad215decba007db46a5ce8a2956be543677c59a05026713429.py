"""Small private execution receipt; every deadline/failure is retained."""
import argparse, hashlib, json, pathlib, subprocess, time
if not __debug__:
    raise SystemExit("optimized execution forbidden")
def pin(p):
    p=pathlib.Path(p).resolve(); b=p.read_bytes()
    return dict(path=str(p), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
def main():
    a=argparse.ArgumentParser(); a.add_argument('--script',type=pathlib.Path,required=True)
    a.add_argument('--out',type=pathlib.Path,required=True); a.add_argument('--seconds',type=int,required=True)
    args=a.parse_args()
    if not 1<=args.seconds<=60: raise SystemExit('small control cap must be 1..60')
    args.out.mkdir(parents=True,exist_ok=False)
    command=['/opt/homebrew/bin/gap','-q','-b',str(args.script.resolve())]
    record=dict(status='RUNNING', command=command, cap_seconds=args.seconds,
                input=pin(args.script), target_census=False)
    dest=args.out/'receipt.json'; dest.write_text(json.dumps(record,indent=2)+'\n')
    start=time.monotonic()
    with (args.out/'stdout').open('wb') as so,(args.out/'stderr').open('wb') as se:
        try:
            p=subprocess.run(command,stdout=so,stderr=se,timeout=args.seconds)
            record.update(returncode=p.returncode,status='RETURNED' if p.returncode==0 else 'FAILED')
        except subprocess.TimeoutExpired:
            record.update(status='DEADLINE',returncode=None)
    record.update(elapsed=time.monotonic()-start,stdout=pin(args.out/'stdout'),stderr=pin(args.out/'stderr'))
    if pin(args.script)!=record['input']: record['status']='INPUT_CHANGED'
    dest.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2))
    return 0 if record['status']=='RETURNED' and not (args.out/'stderr').read_bytes() else 1
if __name__=='__main__': raise SystemExit(main())
