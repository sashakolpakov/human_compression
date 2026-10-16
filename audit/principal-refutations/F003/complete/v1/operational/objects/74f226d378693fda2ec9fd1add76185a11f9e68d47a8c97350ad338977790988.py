from pathlib import Path
import subprocess,json,hashlib,time
W=Path(__file__).resolve().parent
P=W/'independent.g';digest=hashlib.sha256(P.read_bytes()).hexdigest();out=W/'gap01';out.mkdir(exist_ok=False)
start=time.monotonic()
with (out/'stdout.log').open('wb') as so,(out/'stderr.log').open('wb') as se:
    proc=subprocess.Popen(['/opt/homebrew/bin/gap','-q','-b',str(P)],cwd=W,stdout=so,stderr=se)
    (out/'pid').write_text(str(proc.pid)+'\n')
    try:rc=proc.wait(timeout=120);status='EXITED'
    except subprocess.TimeoutExpired:proc.kill();proc.wait();rc=None;status='TIMEOUT_NO_CERTIFICATE'
same=hashlib.sha256(P.read_bytes()).hexdigest()==digest
complete=(out/'stdout.log').read_text().count('COMPLETE_INDEPENDENT_GAP_RECONSTRUCTION')==1
if status=='EXITED' and not(rc==0 and complete and same and not(out/'stderr.log').read_bytes()):status='FAILED_NO_CERTIFICATE'
report=dict(status=status,returncode=rc,seconds=time.monotonic()-start,seconds_limit=120,code_sha256=digest,unchanged=same,complete=complete)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
