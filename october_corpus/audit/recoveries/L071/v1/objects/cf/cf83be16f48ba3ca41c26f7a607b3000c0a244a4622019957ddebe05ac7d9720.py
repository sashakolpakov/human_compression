"""Check every recorded tuple and every printed Co3 table cell.

Completeness is supplied by the separately reviewed enumeration proof and
its completed execution, not by this checker or by agreement of totals.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import time

p = argparse.ArgumentParser()
p.add_argument('--run', type=Path, required=True)
p.add_argument('--out', type=Path, required=True)
p.add_argument('--seconds', type=int, default=3600)
a = p.parse_args()
W = Path(__file__).resolve().parent
S = W.parent
E = S / 'corpus106_double_coset_work'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def literal(raw, marker):
    need(raw.count(marker) == 1, 'unique tuple marker ' + marker)
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


run = json.loads((a.run / 'report.json').read_text())
need(run['status'] == 'EXITED' and run['returncode'] == 0 and
     run['complete_marker'] and run['unchanged'], 'completed enumeration')
for pin in run['pins']:
    need(sha(E / pin['path']) == pin['sha256'], 'enumeration pin')
raw = (a.run / 'stdout.log').read_text()
need(raw.count('COMPLETE_EXHAUSTION') == 1, 'one completed enumeration')
ranks = list(map(int, re.findall(r'COMPLETE_TUPLES_RANK_(\d+) ', raw)))
need(ranks == list(range(1, 39)), 'complete rank range through log2 group order')
source = json.loads((W / 'co3_source_tables.json').read_text())
need(source['source_pdf_sha256'] == sha(S / 'sources/catalogue_L071.pdf'), 'source PDF')
need(source['source_text_sha256'] == sha(S / 'sources/catalogue_L071.txt'), 'source text')
a.out.mkdir(parents=True, exist_ok=False)
lines = ['recordedMarks:=[];;']
for rank in ranks:
    lines.append(f'recordedMarks[{rank}]:=' + literal(raw, f'COMPLETE_TUPLES_RANK_{rank} ') + ';;')
(a.out / 'records.g').write_text('\n'.join(lines) + '\n')
expected = []
for rank in (3, 4, 5):
    rows = source['rows'][str(rank)]
    need(len({tuple(row['type']) for row in rows}) == len(rows), 'unique source types')
    need(all(len(row['type']) == rank - 1 and row['count'] >= 0 for row in rows), 'source shape')
    expected.extend([[rank, row['type'], row['count']] for row in rows])
(a.out / 'expected.g').write_text('expected:=' + json.dumps(expected) + ';;\n')
shutil.copy2(E / 'Co3_model.g', a.out / 'model.g')
shutil.copy2(S / 'corpus106_F002_recovery_v1/checks.g', a.out / 'checks.g')
code = r'''Read("model.g");;Read("checks.g");;Read("records.g");;Read("expected.g");;
if Size(G)<>495766656000 or not IsSimpleGroup(G) then Error("Co3 model");fi;
if not (2^38<=Size(G) and Size(G)<2^39) then Error("rank limit");fi;
total:=0;;actual:=[];;
for rank in [1..38] do
 types:=[];;
 for t in recordedMarks[rank] do
  if Length(t)<>rank or not ForAll(t,x->Order(x)=2 and x in G) then Error("marks");fi;
  for i in [1..rank] do for j in [i+2..rank] do
   if Comm(t[i],t[j])<>() then Error("string");fi;
  od;od;
  if Group(t)<>G then Error("generation");fi;
  if not FullIP(t) then Error("full subset intersection property");fi;
  Add(types,List([1..rank-1],j->Order(t[j]*t[j+1])));
  total:=total+1;
  if total mod 500=0 then Print("VALIDATION_PROGRESS ",total,"\n");fi;
 od;
 cells:=Collected(types);;
 Print("VERIFIED_TYPE_COUNTS ",rank," ",cells,"\n");
 for cell in cells do Add(actual,[rank,cell[1],cell[2]]);od;
od;
for row in expected do
 matches:=Filtered(actual,x->x[1]=row[1] and x[2]=row[2]);;
 if row[3]=0 then
  if Length(matches)<>0 then Error("printed zero cell");fi;
 elif Length(matches)<>1 or matches[1][3]<>row[3] then Error("printed positive cell");fi;
od;
for row in actual do
 if not row in expected then Error("unlisted type or rank occurred");fi;
od;
if total<>22908 or Length(expected)<>824 then Error("literal coverage count");fi;
if FullIP([recordedMarks[3][1][1],recordedMarks[3][1][2],recordedMarks[3][1][1]]) then
 Error("repetition control");fi;
Print("ALL_CO3_TABLE_CELLS_AND_FULL_IP_PASS TUPLES ",total," PRINTED_CELLS ",Length(expected),"\n");
Print("COMPLETE_CO3_VALIDATION\n");QUIT;
'''
(a.out / 'validate.g').write_text(code)
paths = [Path(__file__), a.run / 'report.json', a.run / 'stdout.log',
         W / 'co3_source_tables.json', W / 'co3_source_visual.json']
paths.extend(a.out / name for name in ('records.g', 'expected.g', 'model.g', 'checks.g', 'validate.g'))
pins = [{'path': str(path.resolve()), 'sha256': sha(path)} for path in paths]
start = time.monotonic()
with (a.out / 'stdout.log').open('wb') as so, (a.out / 'stderr.log').open('wb') as se:
    q = subprocess.Popen(['/opt/homebrew/bin/gap', '-q', '-b', 'validate.g'],
                         cwd=a.out, stdout=so, stderr=se)
    (a.out / 'pid').write_text(str(q.pid) + '\n')
    try:
        rc = q.wait(timeout=a.seconds)
        status = 'EXITED'
    except subprocess.TimeoutExpired:
        q.kill()
        q.wait()
        rc = None
        status = 'TIMEOUT_NO_CERTIFICATE'
result = {'status': status, 'returncode': rc, 'seconds': time.monotonic() - start,
          'complete_marker': 'COMPLETE_CO3_VALIDATION' in (a.out / 'stdout.log').read_text(),
          'pins': pins, 'unchanged': all(sha(Path(row['path'])) == row['sha256'] for row in pins),
          'software_premises': 'Exact GAP group operations and the named Co3 library model',
          'whole_original_credit': 0, 'distinct_review_pending': True}
(a.out / 'report.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({key: value for key, value in result.items() if key != 'pins'}))
