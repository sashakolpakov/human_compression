from pathlib import Path
import hashlib, json, os, subprocess, sys, time
if sys.flags.optimize:
    raise RuntimeError('optimized Python unsupported')
W=Path(__file__).resolve().parent
d=W/'nonbipartite_retry01'
name='CAT_2024_9'
old=W/'nonbipartite_subdivisions'/(name+'.receipt.json')
if json.loads(old.read_text())['status']!='TIME_LIMIT_NO_CONCLUSION':
    raise ValueError('retry requires the recorded capped attempt')
if (d/(name+'.receipt.json')).exists():
    raise ValueError('retry already has a disposition')
start=time.time()
env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
with (d/'stdout.log').open('wb') as so,(d/'stderr.log').open('wb') as se:
    child=subprocess.Popen(['/opt/homebrew/bin/gap','-q','-b','-T',str(d/'worker.g')],
                           cwd=W,env=env,stdout=so,stderr=se)
    active=dict(name=name,runner_pid=os.getpid(),child_pid=child.pid,start_unix=start,deadline_seconds=180)
    (d/'active.json').write_text(json.dumps(active,indent=2)+'\n')
    try:
        rc=child.wait(timeout=180);cap=False
    except subprocess.TimeoutExpired:
        child.terminate()
        try:rc=child.wait(timeout=5)
        except subprocess.TimeoutExpired:child.kill();rc=child.wait()
        cap=True
stdout=(d/'stdout.log').read_text();stderr=(d/'stderr.log').read_text()
status='TIME_LIMIT_NO_CONCLUSION' if cap else ('PASS' if rc==0 and not stderr.strip()
    and 'L059_NONBIPARTITE_RETRY_COMPLETE '+name+' ' in stdout else 'FAILED')
digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=active|dict(status=status,returncode=rc,elapsed_seconds=time.time()-start,
              method='exact nauty generators and actual graph actions',
              prior_capped_receipt_sha256=digest(old),script_sha256=digest(d/'worker.g'),
              oracle_sha256=digest(d/'oracle.json'),stdout_sha256=digest(d/'stdout.log'),
              stderr_sha256=digest(d/'stderr.log'),
              library_sha256={n:digest(W/n) for n in ['subdivision_markings.g','subdivision_actual_actions.g','maximal_descent_arcs.g']})
if status=='PASS':r['witness_sha256']=digest(d/(name+'.g'))
(d/(name+'.receipt.json')).write_text(json.dumps(r,indent=2)+'\n')
(d/'active.json').write_text(json.dumps(dict(runner_pid=os.getpid(),child_pid=None,status='COMPLETE',disposition=status),indent=2)+'\n')
print(name,status,round(time.time()-start,2),flush=True)
