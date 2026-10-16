"""One root-reviewed 30-second library export, held unless 4 GiB is free."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import signal
import subprocess
import time

HERE=Path(__file__).resolve().parent


def need(ok,message):
    if not ok:raise ValueError(message)


def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(2**20),b''):h.update(b)
    return h.hexdigest()


def main(a):
    req=json.loads((HERE/'request.json').read_text())
    need(sha(HERE/'request.json')==a.expected_request,'Exact reviewed request')
    for row in req['bindings']:
        p=Path(row['path'])
        need(p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'Exact request binding '+str(p))
    need(a.out.is_absolute() and not a.out.exists(),'Fresh absolute output')
    need(a.authorized_once,'Explicit root authorization required')
    free=shutil.disk_usage(a.out.parent).free
    if free < req['launch_reserve_bytes']+req['output_cap_bytes']:
        print(json.dumps(dict(status='HOLD_L036_CHARACTER_EXPORT_DISK_RESERVE',free_bytes=free,target_launched=False)))
        return
    a.out.mkdir()
    started=time.monotonic()
    reason='completed'
    with (a.out/'stdout').open('wb') as out,(a.out/'stderr').open('wb') as err:
        child=subprocess.Popen(req['command'],cwd=HERE,stdout=out,stderr=err,start_new_session=True)
        while child.poll() is None:
            elapsed=time.monotonic()-started
            total=sum(p.stat().st_size for p in [a.out/'stdout',a.out/'stderr'])
            free=shutil.disk_usage(a.out).free
            if elapsed>req['deadline_seconds'] or total>req['output_cap_bytes'] or free<req['emergency_floor_bytes']:
                reason='deadline' if elapsed>req['deadline_seconds'] else 'output_cap' if total>req['output_cap_bytes'] else 'disk_floor'
                os.killpg(child.pid,signal.SIGTERM)
                try:child.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    os.killpg(child.pid,signal.SIGKILL);child.wait()
                break
            time.sleep(0.1)
    result=dict(status='L036_CHARACTER_EXPORT_TERMINAL',reason=reason,returncode=child.returncode,
                seconds=time.monotonic()-started,request_sha256=a.expected_request,target_launched=True,
                science_accepted=False,outputs=[dict(path=p.name,bytes=p.stat().st_size,sha256=sha(p)) for p in [a.out/'stdout',a.out/'stderr']])
    (a.out/'receipt.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--expected-request',required=True)
    p.add_argument('--out',type=Path,required=True)
    p.add_argument('--authorized-once',action='store_true')
    main(p.parse_args())
