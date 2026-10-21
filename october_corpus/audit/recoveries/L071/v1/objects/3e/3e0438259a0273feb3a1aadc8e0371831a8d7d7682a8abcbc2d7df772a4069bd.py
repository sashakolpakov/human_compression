"""Match each author's sporadic marking to one independently enumerated orbit.

The source program is parsed as restricted data; it is never executed.
The original archive has no role in the exhaustion search.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse
import json
import re
import shutil
import subprocess
import time
from validate import literal, sha, need

W = Path(__file__).resolve().parent
S = W.parent
SOURCE = S / 'reboot_20261013/L071_census_preparation/source_sporpolys/sporpolys'
NAMES = {'M11':'m11', 'M12':'m12', 'J1':'j1', 'M22':'m22', 'J2':'j2',
         'M23':'m23', 'HS':'hs', 'M24':'m24', 'McL':'mcl', 'Tits':'ti',
         'He':'he', 'J3':'j3'}


def source_data(path, variable):
    chunks = [s.strip() for s in path.read_text().split(';;') if s.strip()]
    need(chunks[:2] == ['gens := []', variable + ' := []'], 'literal source header')
    gens, tuples = [], []
    for chunk in chunks[2:]:
        if chunk.startswith('Add(gens,'):
            m = re.fullmatch(r'Add\(gens,([\s\d,()]+)\)', chunk)
            need(m is not None, 'literal source permutation')
            gens.append(m[1])
        else:
            m = re.fullmatch(r'Add\(' + re.escape(variable) +
                             r',\[(gens\[\d+\](?:,gens\[\d+\])*)\]\)', chunk)
            need(m is not None, 'literal source tuple')
            indices = list(map(int, re.findall(r'gens\[(\d+)\]', m[1])))
            need(all(1 <= i <= len(gens) for i in indices), 'source generator indices')
            tuples.append(indices)
    code = 'sourceGens:=[' + ','.join(gens) + '];;\nsourceTuples:=['
    code += ','.join('[' + ','.join(f'sourceGens[{i}]' for i in t) + ']' for t in tuples)
    return code + '];;\n', len(gens), len(tuples)


CODE = r'''Read("model.g");;Read("records.g");;Read("source.g");;
if Size(G)<>expectedOrder or not IsNormal(A,G) then Error("model");fi;
if Size(A)/Size(Centralizer(A,G))<>Size(AutomorphismGroup(G)) then
 Error("full automorphism action");fi;
root:=rec(marks:=[],children:=[],leaf:=fail);;
allCount:=0;;
for rank in [1..Length(recordedMarks)] do
 for index in [1..Length(recordedMarks[rank])] do
  t:=recordedMarks[rank][index];;node:=root;;
  for x in t do
   pos:=Position(node.marks,x);;
   if pos=fail then
    Add(node.marks,x);Add(node.children,rec(marks:=[],children:=[],leaf:=fail));
    pos:=Length(node.marks);
   fi;
   node:=node.children[pos];;
  od;
  if node.leaf<>fail then Error("duplicate literal recorded tuple");fi;
  node.leaf:=[rank,index];;allCount:=allCount+1;
 od;
od;
if Length(sourceTuples)<>allCount then Error("source cardinality");fi;
matched:=[];;
if Length(sourceTuples)>0 then
 H:=Group(sourceTuples[1]);;
 if Size(H)<>expectedOrder or not ForAll(sourceGens,x->x in H) then
  Error("source group consistency");fi;
 iso:=IsomorphismGroups(H,G);;
 if iso=fail or not IsBijective(iso) then Error("source model isomorphism");fi;
 Print("SOURCE_MODEL_GENERATORS ",GeneratorsOfGroup(H),"\n");
 Print("SOURCE_MODEL_IMAGES ",List(GeneratorsOfGroup(H),x->Image(iso,x)),"\n");
 sourceImages:=List(sourceGens,x->Image(iso,x));;
 Print("ALL_SOURCE_GENERATOR_IMAGES ",sourceImages,"\n");
 for sourceIndex in [1..Length(sourceTuples)] do
  original:=List(sourceTuples[sourceIndex],x->sourceImages[Position(sourceGens,x)]);;
  t:=ShallowCopy(original);;node:=root;;St:=A;;transporter:=One(A);;
  for i in [1..Length(t)] do
   found:=fail;;
   for j in [1..Length(node.marks)] do
    h:=RepresentativeAction(St,t[i],node.marks[j]);;
    if h<>fail then found:=[j,h];break;fi;
   od;
   if found=fail then Error("no matching orbit");fi;
   j:=found[1];;h:=found[2];;
   if not h in St or t[i]^h<>node.marks[j] then Error("transporter");fi;
   t:=List(t,x->x^h);;transporter:=transporter*h;;
   St:=Centralizer(St,node.marks[j]);;node:=node.children[j];;
  od;
  if node.leaf=fail or node.leaf in matched then Error("missing or repeated leaf");fi;
  if not transporter in A or List(original,x->x^transporter)<>
      recordedMarks[node.leaf[1]][node.leaf[2]] then Error("literal tuple match");fi;
  Add(matched,ShallowCopy(node.leaf));
  Print("SOURCE_MATCH ",sourceIndex," LEAF ",node.leaf," TRANSPORTER ",transporter,"\n");
 od;
fi;
if Length(matched)<>allCount then Error("not a bijection");fi;
Print("COMPLETE_SOURCE_ORBIT_BIJECTION ",modelName," CLASSES ",allCount,"\n");QUIT;
'''


def main(args):
    args.out.mkdir(parents=True, exist_ok=False)
    queue = json.loads((W / 'queue.json').read_text())
    rows = [r for r in queue['models'] if r['name'] in NAMES]
    if args.names:
        names = args.names.split(',')
        need(set(names) <= set(NAMES), 'unknown comparison name')
        rows = [r for r in rows if r['name'] in names]
    reports = []
    for row in rows:
        name = row['name']
        run = args.run / name
        receipt = json.loads((run / 'report.json').read_text())
        need(receipt['status'] == 'EXITED' and receipt['returncode'] == 0 and
             receipt['complete_marker'] and receipt['unchanged'], 'completed census')
        for pin in receipt['pins']:
            need(sha(Path(pin['path'])) == pin['sha256'], 'census pin')
        raw = (run / 'stdout.log').read_text()
        need(raw.count('COMPLETE_EXHAUSTION') == 1, 'completed full stream')
        ranks = list(map(int, re.findall(r'COMPLETE_TUPLES_RANK_(\d+) ', raw)))
        need(ranks == list(range(1, row['order'].bit_length())), 'complete rank range')
        out = args.out / name
        out.mkdir()
        text = 'recordedMarks:=[];;\n'
        for rank in ranks:
            text += f'recordedMarks[{rank}]:=' + literal(raw, f'COMPLETE_TUPLES_RANK_{rank} ') + ';;\n'
        (out / 'records.g').write_text(text)
        source = SOURCE / (NAMES[name] + '.gap')
        text, gen_count, tuple_count = source_data(source, NAMES[name])
        (out / 'source.g').write_text(text)
        shutil.copy2(W / row['model'], out / 'model.g')
        if name == 'J3':
            for ext in ('g1', 'g2'):
                shutil.copy2(W / f'J3.{ext}', out / f'J3.{ext}')
        (out / 'compare.g').write_text(CODE)
        paths = [Path(__file__), W / 'validate.py', W / 'queue.json',
                 source, SOURCE.parent.parent / 'sporpolys_download.json',
                 run / 'report.json', run / 'stdout.log'] + list(out.iterdir())
        pins = [dict(path=str(p), sha256=sha(p)) for p in paths]
        started = time.monotonic()
        with (out / 'stdout.log').open('wb') as so, (out / 'stderr.log').open('wb') as se:
            child = subprocess.Popen(['/opt/homebrew/bin/gap', '-q', '-b', 'compare.g'],
                                     cwd=out, stdout=so, stderr=se)
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
        complete = (out / 'stdout.log').read_text().count('COMPLETE_SOURCE_ORBIT_BIJECTION') == 1
        unchanged = all(sha(Path(pin['path'])) == pin['sha256'] for pin in pins)
        if status == 'EXITED' and not (rc == 0 and complete and unchanged and
                                       (out / 'stderr.log').read_bytes() == b''):
            status = 'FAILED_NO_CERTIFICATE'
        report = dict(name=name, status=status, returncode=rc, complete_marker=complete,
                      unchanged=unchanged, seconds=time.monotonic() - started, pins=pins,
                      source_generators=gen_count, source_markings=tuple_count,
                      source_used_only_after_census=True, distinct_review_pending=True,
                      whole_original_credit=0)
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
    p.add_argument('--seconds', type=int, default=1800)
    main(p.parse_args())
