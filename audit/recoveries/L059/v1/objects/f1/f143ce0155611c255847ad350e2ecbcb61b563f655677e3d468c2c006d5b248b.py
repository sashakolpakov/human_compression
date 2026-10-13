from pathlib import Path
import subprocess, os, json, time, hashlib, sys
if sys.flags.optimize:
    raise RuntimeError('optimized Python unsupported')
W = Path(__file__).resolve().parent
os.chdir(W)
out = W / 'subdivision_markings'
owned = W / 'subdivision_second_owner'
queue = json.loads((owned / 'queue.json').read_text())
bases = json.loads((out / 'basis.json').read_text())
env = os.environ.copy()
env.pop('PYTHONOPTIMIZE', None)
for name in queue:
    receipt = out / (name + '.receipt.json')
    reservation = json.loads(receipt.read_text())
    if reservation['status'] == 'PASS':
        continue
    if reservation['status'] != 'RESERVED_FOR_SECOND_RUNNER' or reservation['owner'] != 'L059_subdivision_second':
        raise ValueError('not an owned reservation: ' + name)
    basis = W / bases[name]
    br = json.loads(basis.with_suffix('.receipt.json').read_text())
    if br['status'] != 'PASS' or hashlib.sha256(basis.read_bytes()).hexdigest() != br['witness_sha256']:
        raise ValueError('unaccepted basis: ' + name)
    script = W / 'subdivision_workers' / (name + '.g')
    start = time.time()
    with (out / (name + '.stdout')).open('wb') as so, (out / (name + '.stderr')).open('wb') as se:
        child = subprocess.Popen(['/opt/homebrew/bin/gap', '-q', '-b', '-T', str(script)], stdout=so, stderr=se, env=env)
        active = dict(runner_pid=os.getpid(), child_pid=child.pid, name=name, deadline_seconds=180, start_unix=start)
        (owned / 'active.json').write_text(json.dumps(active, indent=2) + '\n')
        try:
            rc = child.wait(timeout=180)
            cap = False
        except subprocess.TimeoutExpired:
            child.terminate()
            try:
                rc = child.wait(timeout=5)
            except subprocess.TimeoutExpired:
                child.kill()
                rc = child.wait()
            cap = True
    stdout = (out / (name + '.stdout')).read_text()
    stderr = (out / (name + '.stderr')).read_text()
    status = ('TIME_LIMIT_NO_CONCLUSION' if cap else
              'PASS' if rc == 0 and 'L059_SUBDIVISION_COMPLETE ' + name + ' ' in stdout and not stderr.strip()
              else 'FAILED')
    result = active | dict(status=status, owner='L059_subdivision_second', returncode=rc,
                           elapsed_seconds=time.time()-start,
                           basis_sha256=hashlib.sha256(basis.read_bytes()).hexdigest(),
                           script_sha256=hashlib.sha256(script.read_bytes()).hexdigest(),
                           stdout_sha256=hashlib.sha256((out/(name+'.stdout')).read_bytes()).hexdigest(),
                           stderr_sha256=hashlib.sha256((out/(name+'.stderr')).read_bytes()).hexdigest())
    if status == 'PASS':
        result['witness_sha256'] = hashlib.sha256((out / (name + '.g')).read_bytes()).hexdigest()
    temporary = receipt.with_suffix('.new')
    temporary.write_text(json.dumps(result, indent=2) + '\n')
    temporary.replace(receipt)
    print(name, status, round(time.time()-start, 2), flush=True)
(owned / 'active.json').write_text(json.dumps(dict(runner_pid=os.getpid(), child_pid=None,
                                                  status='COMPLETE_RESERVED_QUEUE'), indent=2)+'\n')
print('SUBDIVISION_RESERVED_QUEUE_COMPLETE', flush=True)
