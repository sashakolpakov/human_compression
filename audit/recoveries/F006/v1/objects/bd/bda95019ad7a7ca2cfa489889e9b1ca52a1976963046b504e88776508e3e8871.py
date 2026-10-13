"""Validate the completed E8 census using the retained full-subset checker."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import time

S=Path('/Users/sasha/medusa/research/leemans')
W=S/'reboot_20261013'
run=W/'central_marks_E8_01'
models=S/'corpus106_central_marks_work'
out=W/'F006_E8_full_IP01'
source=S/'corpus106_L071_remaining_censuses_v1/validate.py'

def need(ok,message):
    if not ok:raise ValueError(message)

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

receipt=json.loads((run/'report.json').read_text())
need(receipt['status']=='EXITED' and receipt['returncode']==0 and
     receipt['complete_marker'] and receipt['unchanged'],'completed census required')
for row in receipt['pins']:need(sha(models/row['path'])==row['sha256'],'census input changed')
need((run/'stderr.log').read_bytes()==b'','census stderr')
raw=(run/'stdout.log').read_text()
need(raw.count('COMPLETE_EXHAUSTION')==1,'one complete exhaustion marker')
ranks=list(map(int,re.findall(r'COMPLETE_TUPLES_RANK_(\d+) ',raw)))
need(ranks==list(range(1,30)),'full rank bound')
pattern=r'RANK\s+(\d+)\s+ordered\s+(\d+)\s+self\s+(\d+)\s+dual_classes\s+(\d+)\s+connected_ordered\s+(\d+)\s+connected_self\s+(\d+)\s+connected_dual\s+(\d+)'
rows=[list(map(int,x)) for x in re.findall(pattern,raw)]
need([x[0] for x in rows]==ranks,'all rank summaries')
spec=importlib.util.spec_from_file_location('retained_full_validation',source)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
out.mkdir(exist_ok=False)
text='recordedMarks:=[];;\n'
for rank in ranks:
    text+=f'recordedMarks[{rank}]:='+module.literal(raw,f'COMPLETE_TUPLES_RANK_{rank} ')+';;\n'
text+='reportedCounts:='+json.dumps([x[1] for x in rows])+';;\n'
(out/'records.g').write_text(text)
shutil.copyfile(models/'E8_model.g',out/'model.g')
shutil.copyfile(S/'corpus106_F002_recovery_v1/checks.g',out/'checks.g')
(out/'validate.g').write_text(module.CODE)
paths=[Path(__file__),source,run/'report.json',run/'stdout.log',run/'stderr.log',
       out/'records.g',out/'model.g',out/'checks.g',out/'validate.g']
pins=[dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p)) for p in paths]
(out/'input.json').write_text(json.dumps(dict(status='VALIDATING_COMPLETED_E8_CENSUS',
    pins=pins,rank_counts=rows,retained_CODE_used_verbatim=True,
    whole_original_credit=0,seconds_limit=3600),indent=2)+'\n')
start=time.monotonic()
with (out/'stdout.log').open('wb') as so,(out/'stderr.log').open('wb') as se:
    child=subprocess.Popen(['/opt/homebrew/bin/gap','-q','-b','validate.g'],cwd=out,stdout=so,stderr=se)
    (out/'pid').write_text(str(child.pid)+'\n')
    (out/'current_job.json').write_text(json.dumps(dict(status='RUNNING',pid=child.pid,
        owner='root',seconds_limit=3600,started_utc=datetime.now(timezone.utc).isoformat()),indent=2)+'\n')
    print(json.dumps(dict(started='E8 full subset IP',pid=child.pid,recorded_tuples=sum(x[1] for x in rows))),flush=True)
    try:rc=child.wait(timeout=3600);status='EXITED'
    except subprocess.TimeoutExpired:
        child.kill();child.wait();rc=None;status='TIMEOUT_NO_CERTIFICATE'
complete=(out/'stdout.log').read_text().count('COMPLETE_REMAINING_MODEL_VALIDATION')==1
unchanged=all(sha(Path(x['path']))==x['sha256'] for x in pins)
if status=='EXITED' and not(rc==0 and complete and unchanged and (out/'stderr.log').read_bytes()==b''):
    status='FAILED_NO_CERTIFICATE'
report=dict(status=status,returncode=rc,complete_marker=complete,unchanged=unchanged,
    seconds=time.monotonic()-start,pins=pins,recorded_tuples=sum(x[1] for x in rows),
    rank_limit=29,all_subset_intersections_checked=complete and status=='EXITED',
    distinct_review_pending=True,whole_original_credit=0)
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
(out/'current_job.json').write_text(json.dumps(dict(status=status,pid=child.pid))+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='pins'}))
