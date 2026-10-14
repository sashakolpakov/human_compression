from pathlib import Path
import datetime,hashlib,json,os,signal,subprocess,time
W=Path(__file__).resolve().parent;S=W.parents[1]
env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def dump(p,data):p.write_text(json.dumps(data,indent=2)+'\n')
for n,limit in [(15,7)]:
    V=W/'a15_interval_validation'
    if (V/'validation.stdout').exists():raise RuntimeError('fresh receipt required')
    inputs=[pin(V/x)for x in ['input.g','driver.g','validate.g','canonical.py']]
    inputs.append(pin(S/'corpus106_L120_interval_validator_v1/intervals.g'))
    started=time.monotonic()
    with (V/'validation.stdout').open('wb')as out,(V/'validation.stderr').open('wb')as err:
        p=subprocess.Popen(['/opt/homebrew/bin/gap','-q','-T',str(V/'driver.g')],stdout=out,stderr=err,env=env,start_new_session=True)
        dump(V/'running.json',dict(status='RUNNING',pid=p.pid,start_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),deadline_unix=time.time()+600,cap_seconds=600,inputs=inputs,role='Positive A15 validation; interval method root accepted ab10c8c1.'))
        try:ret=p.wait(timeout=600)
        except subprocess.TimeoutExpired:
            os.killpg(p.pid,signal.SIGTERM)
            try:p.wait(timeout=5)
            except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
            ret=124
    text=(V/'validation.stdout').read_text();good=ret==0 and not(V/'validation.stderr').read_bytes()and text.rstrip().endswith('COMPLETE_ALTERNATING_INTERVAL_VALIDATION')
    result=dict(status='PASS_ACTUAL_INTERVAL_VALIDATION'if good else'INCOMPLETE_OR_FAILED',returncode=ret,seconds=time.monotonic()-started,inputs=inputs,stdout=pin(V/'validation.stdout'),stderr=pin(V/'validation.stderr'),new_credit=0)
    dump(V/'validation_receipt.json',result)
    if not good:raise RuntimeError('validation stopped')
    cp=subprocess.run(['/Users/sasha/.venvs/global/bin/python',str(V/'canonical.py'),'--degree',str(n),'--rank-limit',str(limit),'--input',str(V/'validation.stdout'),'--out',str(V/'canonical_report.json')],env=env,capture_output=True,timeout=180)
    (V/'canonical.stdout').write_bytes(cp.stdout);(V/'canonical.stderr').write_bytes(cp.stderr)
    if cp.returncode or cp.stderr:raise RuntimeError('literal fusion failed')
    report=json.loads((V/'canonical_report.json').read_text());enum=json.loads((W/'finite_rows_work'/'a15_enumeration_summary01.json').read_text())
    for row in report['rows']:
        if any(row[k]!=enum['counts'][str(row['rank'])][k]for k in ['ordered','self_dual','with_duality']):raise RuntimeError('independent enumeration/fusion discrepancy')
    result.update(status='PASS_ACTUAL_INTERVALS_AND_LITERAL_FUSION',canonical=pin(V/'canonical_report.json'),total_seconds=time.monotonic()-started)
    dump(V/'receipt.json',result);print(json.dumps(dict(degree=n,status=result['status'],tuples=report['tuples'],interval_checks=report['interval_checks'],seconds=result['total_seconds'])),flush=True)
