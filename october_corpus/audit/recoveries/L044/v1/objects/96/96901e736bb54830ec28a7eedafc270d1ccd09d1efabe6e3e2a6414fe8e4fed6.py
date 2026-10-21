import sys
if sys.flags.optimize:
    raise SystemExit('Optimized Python is not permitted')

from pathlib import Path
import argparse
import hashlib
import json
import math
import os
import subprocess
import time


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bracket(text, marker):
    need(text.count(marker) == 1, 'Nonunique record marker: ' + marker)
    start = text.index('[', text.index(marker) + len(marker))
    depth = 0
    for end in range(start, len(text)):
        if text[end] == '[':
            depth += 1
        elif text[end] == ']':
            depth -= 1
        if depth == 0:
            return text[start:end + 1]
    raise ValueError('Unclosed record array')


parser = argparse.ArgumentParser()
parser.add_argument('--out', type=Path, required=True)
parser.add_argument('--recorded-runs', type=Path,
                    help='Acquire complete existing author runs; omit to replay enumeration')
parser.add_argument('--gap', default='/opt/homebrew/bin/gap')
parser.add_argument('--seconds', type=int, default=3600)
args = parser.parse_args()
root = Path(__file__).resolve().parent
need(args.seconds > 0, 'Invalid time allowance')
need(not args.out.exists(), 'Output directory already exists')
pins = {name: digest(root / name) for name in ['check.py', 'checks.g', 'enumerate_even.g']}
args.out.mkdir(parents=True)
env = dict(os.environ)
env.pop('PYTHONOPTIMIZE', None)


def run_gap(code, cwd, stem):
    start = time.monotonic()
    command = [args.gap, '-q', '-b', '-c', code]
    with (cwd / (stem + '.stdout')).open('wb') as out, (cwd / (stem + '.stderr')).open('wb') as err:
        proc = subprocess.Popen(command, cwd=cwd, stdout=out, stderr=err, env=env)
        (cwd / (stem + '.pid')).write_text(str(proc.pid) + '\n')
        try:
            rc = proc.wait(timeout=args.seconds)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
            (cwd / (stem + '.status.json')).write_text(json.dumps({'status': 'TIMEOUT_NO_CERTIFICATE', 'seconds': time.monotonic() - start}) + '\n')
            raise ValueError('Incomplete GAP execution: ' + stem)
    stderr = (cwd / (stem + '.stderr')).read_text()
    stdout = (cwd / (stem + '.stdout')).read_text()
    need(rc == 0 and not stderr.strip() and 'Error,' not in stdout, 'GAP execution failed: ' + stem)
    return stdout, {'returncode': rc, 'seconds': time.monotonic() - start, 'command': command}


results = []
for degree in [7, 8, 10]:
    order = math.factorial(degree) // 2
    rank_limit = order.bit_length() - 1
    work = args.out / ('A' + str(degree))
    work.mkdir()
    for name in ['checks.g', 'enumerate_even.g']:
        (work / name).write_bytes((root / name).read_bytes())
    if args.recorded_runs:
        previous = args.recorded_runs / ('small_maxima_A%d_run01' % degree)
        report = json.loads((previous / 'report.json').read_text())
        need(report['status'] == 'EXITED' and report['returncode'] == 0
             and report['complete_marker'] and report['unchanged'], 'Incomplete retained run')
        need(report['degree'] == degree and report['rank_limit'] == rank_limit,
             'Retained run has wrong parameters')
        engine_pins = [p for p in report['pins'] if p['path'] == 'enumerate_even.g']
        need(len(engine_pins) == 1 and engine_pins[0]['sha256'] == pins['enumerate_even.g'],
             'Retained run uses different enumeration engine')
        source = (previous / 'stdout.log').read_text()
        need(not (previous / 'stderr.log').read_text().strip(), 'Retained GAP error output')
        (work / 'enumeration.stdout').write_text(source)
        (work / 'enumeration.stderr').write_text('')
        (work / 'retained_report.json').write_bytes((previous / 'report.json').read_bytes())
        execution = {'mode': 'ACQUIRED_COMPLETE_AUTHOR_RUN',
                     'input_stdout_sha256': digest(previous / 'stdout.log'),
                     'input_report_sha256': digest(previous / 'report.json')}
    else:
        source, execution = run_gap('degree:=%d;rankLimit:=%d;Read("enumerate_even.g");' % (degree, rank_limit), work, 'enumeration')
        execution['mode'] = 'FRESH_COMPLETE_ENUMERATION'
    need(source.count('COMPLETE_EXHAUSTION') == 1 and 'Error,' not in source,
         'Missing or invalid exhaustion record')
    need('DEGREE %d RANK_LIMIT %d GROUP_ORDER %d' % (degree, rank_limit, order) in source,
         'Enumeration header mismatch')
    lines = ['recordedInvolutions:=' + bracket(source, 'INVOLUTIONS_LITERAL') + ';;', 'recordedMarks:=[];;']
    for rank in range(3, rank_limit + 1):
        lines.append('recordedMarks[%d]:=' % rank + bracket(source, 'COMPLETE_MARKS_RANK_%d ' % rank) + ';;')
    (work / 'records.g').write_text('\n'.join(lines) + '\n')
    validation = '''Read("checks.g");;Read("records.g");;
Ambient:=AlternatingGroup(degree);;total:=0;;altTotal:=0;;altCounts:=[];;
if 2^(rankLimit+1)<=Size(Ambient) then Error("incomplete rank cutoff");fi;
for rank in [3..rankLimit] do
 altCount:=0;;orders:=[];;
 for ids in recordedMarks[rank] do
  t:=List(ids,i->recordedInvolutions[i]);;
  if Length(t)<>rank or not ForAll(t,x->Order(x)=2 and x in Ambient) then Error("invalid marks");fi;
  for i in [1..rank] do for j in [i+2..rank] do
   if Comm(t[i],t[j])<>() then Error("string commutation");fi;
  od;od;
  if not FullIP(t) then Error("full subset IP");fi;
  H:=Group(t);;
  if not IsTransitive(H,[1..degree]) then Error("record is not transitive");fi;
  total:=total+1;Add(orders,Size(H));
  if H=Ambient then altCount:=altCount+1;altTotal:=altTotal+1;fi;
 od;
 Add(altCounts,altCount);
 Print("VALIDATED_RANK ",rank," ALTERNATING ",altCount," GROUP_ORDERS ",Collected(orders),"\\n");
od;
if FullIP([recordedInvolutions[1],recordedInvolutions[2],recordedInvolutions[1]]) then Error("repetition negative control");fi;
Print("ALT_COUNTS ",altCounts,"\\n");
Print("ALL_RECORDS_FULL_SUBSET_IP_PASS DEGREE ",degree," TOTAL ",total," ALTERNATING ",altTotal,"\\n");
Print("COMPLETE_VALIDATION\\n");QUIT;
'''
    (work / 'validate.g').write_text(validation)
    output, validation_execution = run_gap('degree:=%d;rankLimit:=%d;Read("validate.g");' % (degree, rank_limit), work, 'validation')
    need(output.count('COMPLETE_VALIDATION') == 1, 'Incomplete full-IP validation')
    counts = json.loads(bracket(output, 'ALT_COUNTS '))
    need(len(counts) == rank_limit - 2 and all(isinstance(c, int) and c >= 0 for c in counts), 'Invalid rank counts')
    maximum = max([0] + [rank for rank, count in enumerate(counts, 3) if count])
    need(maximum == (5 if degree == 10 else 0), 'Claimed maximum does not follow from census')
    result = {'degree': degree, 'group_order': order, 'rank_limit': rank_limit,
              'counts_by_rank_3_up': counts, 'maximum_rank_3_up': maximum,
              'enumeration': execution, 'validation': validation_execution,
              'source_sha256': digest(work / 'enumeration.stdout'),
              'validation_sha256': digest(work / 'validation.stdout')}
    (work / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    results.append(result)
need(all(digest(root / name) == sha for name, sha in pins.items()), 'Input changed during execution')
report = {'status': 'COMPLETE_SMALL_MAXIMA', 'input_pins': pins, 'results': results,
          'scope': 'Complete exact n7/n8/n10 enumeration through subgroup-doubling cutoff; lower ranks1/2 excluded by separate elementary proof.',
          'whole_original_credit': 0, 'GAP_exact_operations_are_software_premises': True}
(args.out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'status': report['status'], 'maxima': {r['degree']: r['maximum_rank_3_up'] for r in results}}))
