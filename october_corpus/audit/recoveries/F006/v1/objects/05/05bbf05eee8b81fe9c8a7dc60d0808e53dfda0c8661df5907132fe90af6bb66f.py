"""Validate retained exceptional censuses, without repeating enumeration."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import time

S = Path('/Users/sasha/medusa/research/leemans')
W = S / 'reboot_20261013'
models = S / 'corpus106_F006_exceptional_work'
out = W / 'F006_other_full_IP01'
source = S / 'corpus106_L071_remaining_censuses_v1/validate.py'
spec = importlib.util.spec_from_file_location('retained_literals', source)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


CODE = r'''Read("model.g");;Read("checks.g");;Read("records.g");;
if Size(G)<>expectedOrder then Error("model order");fi;
if Set(ivs)<>Set(Concatenation(List(Filtered(ConjugacyClasses(G),
 c->Order(Representative(c))=2),AsList))) then Error("involution domain");fi;
aut:=AutomorphismGroup(G);;
if innerAction then
 if Size(G)/Size(Centre(G))<>Size(aut) then Error("full inner action");fi;
 A:=G;;
else
 A:=Image(ActionHomomorphism(aut,ivs,OnPoints));;
 if Size(A)<>Size(aut) then Error("full involution action");fi;
fi;
limit:=0;;while 2^(limit+1)<=Size(G) do limit:=limit+1;od;
if Length(recordedIds)<>limit then Error("rank limit");fi;
total:=0;;pairs:=0;;firstTuple:=fail;;
for rank in [1..limit] do
 self:=0;;connected:=0;;connectedSelf:=0;;types:=[];;
 for ids in recordedIds[rank] do
  if Length(ids)<>rank or not ForAll(ids,i->i in [1..Length(ivs)]) then Error("indices");fi;
  t:=List(ids,i->ivs[i]);;
  if not ForAll(t,x->Order(x)=2 and x in G) then Error("marks");fi;
  for i in [1..rank] do for j in [i+2..rank] do
   if Comm(t[i],t[j])<>() then Error("string");fi;
  od;od;
  if Group(t)<>G then Error("generation");fi;
  if not FullIP(t) then Error("full subset intersection property");fi;
  pairs:=pairs+4^rank;
  typ:=List([1..rank-1],j->Order(t[j]*t[j+1]));;Add(types,typ);
  if innerAction then sd:=RepresentativeAction(A,t,Reversed(t),OnTuples)<>fail;
  else sd:=RepresentativeAction(A,ids,Reversed(ids),OnTuples)<>fail;fi;
  conn:=ForAll(typ,x->x>2);;
  if sd then self:=self+1;fi;
  if conn then connected:=connected+1;if sd then connectedSelf:=connectedSelf+1;fi;fi;
  total:=total+1;
  if firstTuple=fail and rank>=3 then firstTuple:=t;fi;
 od;
 got:=[Length(recordedIds[rank]),self,(Length(recordedIds[rank])+self)/2,
       connected,connectedSelf,(connected+connectedSelf)/2];;
 if got<>reportedCounts[rank] then Error("rank/self-duality/connected count");fi;
 Print("VERIFIED_RANK ",rank," ",got,"\n");
 Print("VERIFIED_TYPE_COUNTS ",rank," ",Collected(types),"\n");
od;
if firstTuple<>fail and FullIP([firstTuple[1],firstTuple[2],firstTuple[1]]) then
 Error("repetition control");fi;
Print("VALIDATED_MODEL ",modelName," TUPLES ",total," SUBSET_PAIRS ",pairs,"\n");
Print("COMPLETE_EXCEPTIONAL_ROW_VALIDATION\n");QUIT;
'''

out.mkdir(exist_ok=False)
reports = []
for name, run_name, limit in [('F4', 'F006_F4_restored01', 10),
                              ('H4', 'F006_H4_restored01', 13),
                              ('E7', 'F006_E7_inner_restart01', 21)]:
    run = W / run_name
    receipt = json.loads((run / 'report.json').read_text())
    need(receipt['status'] == 'EXITED' and receipt['returncode'] == 0 and
         receipt['complete_marker'] and receipt['unchanged'], 'completed census')
    for pin in receipt['pins']:
        need(sha(models / pin['path']) == pin['sha256'], 'census input changed')
    need((run / 'stderr.log').read_bytes() == b'', 'census stderr')
    raw = (run / 'stdout.log').read_text()
    need(raw.count('COMPLETE_EXHAUSTION') == 1, 'complete census')
    ranks = list(map(int, re.findall(r'COMPLETE_MARKS_RANK_(\d+) ', raw)))
    need(ranks == list(range(1, limit + 1)), 'all ranks')
    pattern = (r'RANK\s+(\d+)\s+ordered\s+(\d+)\s+self\s+(\d+)\s+dual_classes\s+(\d+)'
               r'\s+connected_ordered\s+(\d+)\s+connected_self\s+(\d+)\s+connected_dual\s+(\d+)')
    rows = [list(map(int, x)) for x in re.findall(pattern, raw)]
    need([r[0] for r in rows] == ranks, 'complete summary')
    dest = out / name
    dest.mkdir()
    text = 'ivs:=' + module.literal(raw, 'INVOLUTIONS_LITERAL ') + ';;\nrecordedIds:=[];;\n'
    for rank in ranks:
        text += f'recordedIds[{rank}]:=' + module.literal(raw, f'COMPLETE_MARKS_RANK_{rank} ') + ';;\n'
    text += 'reportedCounts:=' + json.dumps([r[1:] for r in rows]) + ';;\n'
    text += 'innerAction:=' + ('true' if name == 'E7' else 'false') + ';;\n'
    (dest / 'records.g').write_text(text)
    (dest / 'validate.g').write_text(CODE)
    shutil.copyfile(models / (name + '_model.g'), dest / 'model.g')
    shutil.copyfile(S / 'corpus106_F002_recovery_v1/checks.g', dest / 'checks.g')
    paths = [Path(__file__), source, run / 'report.json', run / 'stdout.log',
             run / 'stderr.log'] + sorted(dest.iterdir())
    pins = [dict(path=str(p), bytes=p.stat().st_size, sha256=sha(p)) for p in paths]
    (dest / 'input.json').write_text(json.dumps(dict(pins=pins, counts=rows), indent=2)+'\n')
    start = time.monotonic()
    with (dest / 'stdout.log').open('wb') as so, (dest / 'stderr.log').open('wb') as se:
        child = subprocess.Popen(['/opt/homebrew/bin/gap', '-q', '-b', 'validate.g'],
                                 cwd=dest, stdout=so, stderr=se)
        current = dict(status='RUNNING', name=name, pid=child.pid, owner='root',
                       started_utc=datetime.now(timezone.utc).isoformat(), seconds_limit=3600)
        (out / 'current_job.json').write_text(json.dumps(current, indent=2)+'\n')
        print(json.dumps(current), flush=True)
        try:
            rc = child.wait(timeout=3600)
            status = 'EXITED'
        except subprocess.TimeoutExpired:
            child.kill(); child.wait(); rc = None; status = 'TIMEOUT_NO_CERTIFICATE'
    complete = (dest / 'stdout.log').read_text().count('COMPLETE_EXCEPTIONAL_ROW_VALIDATION') == 1
    unchanged = all(sha(Path(p['path'])) == p['sha256'] for p in pins)
    if status == 'EXITED' and not (rc == 0 and complete and unchanged and
                                   (dest / 'stderr.log').read_bytes() == b''):
        status = 'FAILED_NO_CERTIFICATE'
    report = dict(name=name, status=status, returncode=rc, seconds=time.monotonic()-start,
                  complete_marker=complete, unchanged=unchanged, pins=pins,
                  all_subset_intersections_checked=(status == 'EXITED'),
                  rank_limit=limit, recorded_tuples=sum(r[1] for r in rows),
                  distinct_review_pending=True, whole_original_credit=0)
    (dest / 'report.json').write_text(json.dumps(report, indent=2)+'\n')
    reports.append(report)
    (out / 'batch_progress.json').write_text(json.dumps(reports, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='pins'}), flush=True)
(out / 'current_job.json').write_text(json.dumps(dict(status='BATCH_TERMINAL',
    complete=sum(r['status']=='EXITED' for r in reports), total=len(reports)))+'\n')
