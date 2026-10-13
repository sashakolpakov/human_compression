from pathlib import Path
import subprocess,os,json,time,hashlib,sys
if sys.flags.optimize:raise RuntimeError('optimized Python unsupported')
W=Path(__file__).resolve().parent;os.chdir(W)
out=W/'cubic_2048_markings';queue=json.loads((out/'queue.json').read_text())
env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
for name in queue:
    receipt=out/(name+'.receipt.json')
    if receipt.exists():continue
    script=W/'cubic_2048_fast_workers'/(name+'.g');start=time.time()
    with (out/(name+'.stdout')).open('wb') as so,(out/(name+'.stderr')).open('wb') as se:
        child=subprocess.Popen(['/opt/homebrew/bin/gap','-q','-b','-T',str(script)],stdout=so,stderr=se,env=env)
        active={'runner_pid':os.getpid(),'child_pid':child.pid,'name':name,'deadline_seconds':180,'start_unix':start}
        (out/'active.json').write_text(json.dumps(active,indent=2)+'\n')
        try:rc=child.wait(timeout=180);cap=False
        except subprocess.TimeoutExpired:
            child.terminate()
            try:rc=child.wait(timeout=5)
            except subprocess.TimeoutExpired:child.kill();rc=child.wait()
            cap=True
    stdout=(out/(name+'.stdout')).read_text();stderr=(out/(name+'.stderr')).read_text()
    status='TIME_LIMIT_NO_CONCLUSION' if cap else ('PASS' if rc==0 and 'L059_CUBIC2048_COMPLETE '+name+' ' in stdout and not stderr.strip() else 'FAILED')
    result=active|{'status':status,'returncode':rc,'elapsed_seconds':time.time()-start,'automorphism_oracle':'pynauty.autgrp','nauty_input_sha256':hashlib.sha256((W/'cubic_2048_nauty'/(name+'.json')).read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'stdout_sha256':hashlib.sha256((out/(name+'.stdout')).read_bytes()).hexdigest(),'stderr_sha256':hashlib.sha256((out/(name+'.stderr')).read_bytes()).hexdigest()}
    if status=='PASS':result['witness_sha256']=hashlib.sha256((out/(name+'.g')).read_bytes()).hexdigest()
    receipt.write_text(json.dumps(result,indent=2)+'\n');print(name,status,round(time.time()-start,2),flush=True)
(out/'active.json').write_text(json.dumps({'runner_pid':os.getpid(),'status':'COMPLETE_QUEUE','child_pid':None},indent=2)+'\n')
print('CUBIC2048_MARKING_QUEUE_COMPLETE',flush=True)
