from pathlib import Path
import subprocess,os,json,time,hashlib,sys
if sys.flags.optimize:raise RuntimeError('optimized Python unsupported')
W=Path(__file__).resolve().parent;os.chdir(W)
out=W/'current_c4_descent';queue=json.loads((W/'descent_queue.json').read_text())
env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
limit=180
for name in queue:
    receipt=out/(name+'.receipt.json')
    if receipt.exists():continue
    script=W/'descent_workers'/(name+'.g')
    start=time.time()
    with (out/(name+'.stdout')).open('wb') as so,(out/(name+'.stderr')).open('wb') as se:
        child=subprocess.Popen(['/opt/homebrew/bin/gap','-q','-b','-T',str(script)],stdout=so,stderr=se,env=env)
        active={'runner_pid':os.getpid(),'child_pid':child.pid,'name':name,'deadline_seconds':limit,'start_unix':start}
        (W/'active_descent.json').write_text(json.dumps(active,indent=2)+'\n')
        try:rc=child.wait(timeout=limit);cap=False
        except subprocess.TimeoutExpired:
            child.terminate()
            try:rc=child.wait(timeout=5)
            except subprocess.TimeoutExpired:child.kill();rc=child.wait()
            cap=True
    stdout=(out/(name+'.stdout')).read_text();stderr=(out/(name+'.stderr')).read_text()
    status='TIME_LIMIT_NO_CONCLUSION' if cap else ('PASS' if rc==0 and 'L059_DESCENT_COMPLETE '+name+' ' in stdout and not stderr.strip() else 'FAILED')
    result=active|{'status':status,'returncode':rc,'elapsed_seconds':time.time()-start,'script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'stdout_sha256':hashlib.sha256((out/(name+'.stdout')).read_bytes()).hexdigest(),'stderr_sha256':hashlib.sha256((out/(name+'.stderr')).read_bytes()).hexdigest()}
    if status=='PASS':result['witness_sha256']=hashlib.sha256((out/(name+'.g')).read_bytes()).hexdigest()
    receipt.write_text(json.dumps(result,indent=2)+'\n')
    print(name,status,round(result['elapsed_seconds'],2),flush=True)
(W/'active_descent.json').write_text(json.dumps({'runner_pid':os.getpid(),'status':'COMPLETE_QUEUE','owned_child':None},indent=2)+'\n')
print('DESCENT_QUEUE_COMPLETE',flush=True)
