"""One finite, capped invocation, with literal files and terminal status retained."""
import sys
if not __debug__: raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse, hashlib, json, subprocess, time
from pathlib import Path
def pin(p):
    p=Path(p).resolve();b=p.read_bytes()
    return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--cap',type=int,required=True);ap.add_argument('--inputs',type=Path,required=True);ap.add_argument('command',nargs=argparse.REMAINDER);a=ap.parse_args()
    if not 1<=a.cap<=120:raise ValueError('finite 1..120 second cap')
    O=a.out.resolve()
    if O.exists():raise ValueError('fresh output required')
    cmd=a.command[1:] if a.command[:1]==['--'] else a.command
    if not cmd:raise ValueError('literal command required')
    paths=json.loads(a.inputs.read_text())+[str(Path(__file__).resolve()),str(a.inputs.resolve())]
    inputs=[pin(p) for p in sorted(set(paths))];O.mkdir(parents=True)
    (O/'inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
    start=time.monotonic();rc=None;deadline=False;error=None
    (O/'active.json').write_text(json.dumps(dict(command=cmd,cap_seconds=a.cap,inputs=inputs),indent=2)+'\n')
    with (O/'stdout').open('wb') as so,(O/'stderr').open('wb') as se:
        try:rc=subprocess.run(cmd,stdin=subprocess.DEVNULL,stdout=so,stderr=se,timeout=a.cap).returncode
        except subprocess.TimeoutExpired:deadline=True
        except OSError as e:error=repr(e)
    try:unchanged=all(pin(r['path'])==r for r in inputs)
    except OSError:unchanged=False
    clean=(O/'stderr').stat().st_size==0
    outputs=[pin(p) for p in sorted(O.rglob('*')) if p.is_file()]
    passed=rc==0 and not deadline and error is None and unchanged and clean
    report=dict(status='CLEAN_FINITE_RETURN' if passed else 'FAILED_NO_CERTIFICATE',command=cmd,cap_seconds=a.cap,returncode=rc,deadline=deadline,error=error,seconds=time.monotonic()-start,inputs_unchanged=unchanged,stderr_empty=clean,outputs=outputs,target_census=False,whole_original_credit=0)
    (O/'receipt.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));raise SystemExit(0 if passed else 1)
if __name__=='__main__':main()
