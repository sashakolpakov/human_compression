from pathlib import Path
import json,subprocess,time,sys,os,hashlib
if sys.flags.optimize:raise RuntimeError('optimized Python unsupported')
W=Path(__file__).resolve().parent;out=W/'cubic_filter';queue=json.loads((out/'queue.json').read_text())
env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
for name in queue:
    receipt=out/(name+'.receipt.json')
    if receipt.exists():continue
    start=time.time()
    with (out/(name+'.stdout')).open('wb') as so,(out/(name+'.stderr')).open('wb') as se:
        p=subprocess.Popen([sys.executable,str(W/'cubic_filter_worker.py'),name],stdout=so,stderr=se,env=env)
        active={'runner_pid':os.getpid(),'child_pid':p.pid,'chunk':name,'deadline_seconds':180,'start_unix':start}
        (out/'active.json').write_text(json.dumps(active,indent=2)+'\n')
        try:rc=p.wait(timeout=180);cap=False
        except subprocess.TimeoutExpired:
            p.terminate()
            try:rc=p.wait(timeout=5)
            except subprocess.TimeoutExpired:p.kill();rc=p.wait()
            cap=True
    good=rc==0 and 'CUBIC_FILTER_COMPLETE '+name+' ' in (out/(name+'.stdout')).read_text() and not (out/(name+'.stderr')).read_text().strip()
    status='TIME_LIMIT_NO_CONCLUSION' if cap else 'PASS' if good else 'FAILED'
    receipt.write_text(json.dumps(active|{'status':status,'returncode':rc,'elapsed_seconds':time.time()-start},indent=2)+'\n')
    print(name,status,round(time.time()-start,2),flush=True)
(out/'active.json').write_text(json.dumps({'runner_pid':os.getpid(),'status':'COMPLETE_QUEUE','child_pid':None},indent=2)+'\n')
print('CUBIC_FILTER_QUEUE_COMPLETE',flush=True)
