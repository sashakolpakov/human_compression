"""Validate all tuples in completed censuses; completeness is a separate proof.

No source count directs enumeration. This program only reads its completed
outputs, validates the actual markings, and records their type distributions.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import time

W = Path(__file__).resolve().parent
S = W.parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def literal(raw, marker):
    need(raw.count(marker) == 1, 'unique tuple marker: ' + marker)
    start = raw.index('[', raw.index(marker) + len(marker))
    depth = 0
    for end in range(start, len(raw)):
        if raw[end] == '[':
            depth += 1
        elif raw[end] == ']':
            depth -= 1
        if depth == 0:
            result = raw[start:end + 1]
            need(re.fullmatch(r'[\s\d,()\[\]]+', result) is not None,
                 'literal permutations only')
            return result
    raise ValueError('unclosed tuple list')


CODE = r'''Read("model.g");;Read("checks.g");;Read("records.g");;
if Size(G)<>expectedOrder or not IsNormal(A,G) then Error("model");fi;
if Size(A)/Size(Centralizer(A,G))<>Size(AutomorphismGroup(G)) then
 Error("full automorphism action");fi;
limit:=0;;while 2^(limit+1)<=Size(G) do limit:=limit+1;od;
if Length(recordedMarks)<>limit then Error("full rank bound");fi;
total:=0;;firstTuple:=fail;;
for rank in [1..limit] do
 types:=[];;
 for t in recordedMarks[rank] do
  if Length(t)<>rank or not ForAll(t,x->Order(x)=2 and x in G) then
   Error("marks");fi;
  for i in [1..rank] do for j in [i+2..rank] do
   if Comm(t[i],t[j])<>() then Error("string");fi;
  od;od;
  if Group(t)<>G then Error("generation");fi;
  if not FullIP(t) then Error("full subset intersection property");fi;
  Add(types,List([1..rank-1],j->Order(t[j]*t[j+1])));
  if firstTuple=fail and rank>=3 then firstTuple:=t;fi;
  total:=total+1;
 od;
 if Length(recordedMarks[rank])<>reportedCounts[rank] then
  Error("reported rank count");fi;
 Print("VERIFIED_TYPE_COUNTS ",rank," ",Collected(types),"\n");
od;
if firstTuple<>fail and FullIP([firstTuple[1],firstTuple[2],firstTuple[1]]) then
 Error("repetition control");fi;
Print("VALIDATED_MODEL ",modelName," TUPLES ",total," RANK_LIMIT ",limit,"\n");
Print("COMPLETE_REMAINING_MODEL_VALIDATION\n");QUIT;
'''


def main(args):
    args.out.mkdir(parents=True, exist_ok=False)
    queue = json.loads((W / 'queue.json').read_text())
    rows = queue['models']
    if args.names:
        names = args.names.split(',')
        need(set(names) <= {row['name'] for row in rows}, 'unknown model')
        rows = [row for row in rows if row['name'] in names]
    else:
        rows = [row for row in rows if (args.run / row['name'] / 'report.json').exists()]
    need(rows, 'no completed inputs')
    reports = []
    for row in rows:
        name = row['name']
        run = args.run / name
        receipt = json.loads((run / 'report.json').read_text())
        need(receipt['status'] == 'EXITED' and receipt['returncode'] == 0 and
             receipt['complete_marker'] and receipt['unchanged'], 'completed census: ' + name)
        for pin in receipt['pins']:
            need(sha(Path(pin['path'])) == pin['sha256'], 'census pin: ' + pin['path'])
        raw = (run / 'stdout.log').read_text()
        need(raw.count('COMPLETE_EXHAUSTION') == 1, 'single complete exhaustion')
        need((run / 'stderr.log').read_bytes() == b'', 'empty census stderr')
        limit = row['order'].bit_length() - 1
        ranks = list(map(int, re.findall(r'COMPLETE_TUPLES_RANK_(\d+) ', raw)))
        need(ranks == list(range(1, limit + 1)), 'all ranks: ' + name)
        totals = re.findall(r'RANK\s+(\d+)\s+ordered\s+(\d+)\s+self\s+(\d+)\s+dual_classes\s+(\d+)\s+connected_ordered\s+(\d+)\s+connected_self\s+(\d+)\s+connected_dual\s+(\d+)', raw)
        need([int(x[0]) for x in totals] == ranks, 'rank summaries')
        out = args.out / name
        out.mkdir()
        text = 'recordedMarks:=[];;\n'
        for rank in ranks:
            text += f'recordedMarks[{rank}]:=' + literal(raw, f'COMPLETE_TUPLES_RANK_{rank} ') + ';;\n'
        text += 'reportedCounts:=' + json.dumps([int(x[1]) for x in totals]) + ';;\n'
        (out / 'records.g').write_text(text)
        shutil.copy2(W / row['model'], out / 'model.g')
        if name == 'J3':
            for ext in ('g1', 'g2'):
                shutil.copy2(W / f'J3.{ext}', out / f'J3.{ext}')
        shutil.copy2(S / 'corpus106_F002_recovery_v1/checks.g', out / 'checks.g')
        (out / 'validate.g').write_text(CODE)
        paths = [Path(__file__), W / 'queue.json', run / 'report.json',
                 run / 'stdout.log', run / 'stderr.log'] + list(out.iterdir())
        pins = [dict(path=str(p), sha256=sha(p)) for p in paths]
        started = time.monotonic()
        with (out / 'stdout.log').open('wb') as so, (out / 'stderr.log').open('wb') as se:
            child = subprocess.Popen(['/opt/homebrew/bin/gap', '-q', '-b', 'validate.g'],
                                     cwd=out, stdout=so, stderr=se)
            (out / 'pid').write_text(str(child.pid) + '\n')
            current = dict(name=name, pid=child.pid, owner='root', seconds_limit=args.seconds,
                           started_utc=datetime.now(timezone.utc).isoformat())
            (args.out / 'current_job.json').write_text(json.dumps(current, indent=2) + '\n')
            print(json.dumps(dict(started=name, pid=child.pid)), flush=True)
            try:
                rc = child.wait(timeout=args.seconds)
                status = 'EXITED'
            except subprocess.TimeoutExpired:
                child.kill()
                child.wait()
                rc = None
                status = 'TIMEOUT_NO_CERTIFICATE'
        complete = (out / 'stdout.log').read_text().count('COMPLETE_REMAINING_MODEL_VALIDATION') == 1
        unchanged = all(sha(Path(pin['path'])) == pin['sha256'] for pin in pins)
        if status == 'EXITED' and not (rc == 0 and complete and unchanged and
                                       (out / 'stderr.log').read_bytes() == b''):
            status = 'FAILED_NO_CERTIFICATE'
        report = dict(name=name, status=status, returncode=rc, complete_marker=complete,
                      unchanged=unchanged, seconds=time.monotonic() - started, pins=pins,
                      all_subset_intersections_checked=True, rank_limit=limit,
                      recorded_tuples=sum(int(x[1]) for x in totals),
                      distinct_review_pending=True, whole_original_credit=0)
        (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
        reports.append(report)
        (args.out / 'batch_progress.json').write_text(json.dumps(reports, indent=2) + '\n')
        print(json.dumps({k:v for k,v in report.items() if k != 'pins'}), flush=True)
    (args.out / 'current_job.json').write_text(json.dumps(dict(status='BATCH_TERMINAL', total=len(reports),
        complete=sum(r['status'] == 'EXITED' for r in reports)), indent=2) + '\n')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--run', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--names')
    p.add_argument('--seconds', type=int, default=1200)
    main(p.parse_args())
