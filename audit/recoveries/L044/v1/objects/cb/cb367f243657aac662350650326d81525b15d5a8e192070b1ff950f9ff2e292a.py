#!/usr/bin/env python3
"""Whole required finite census and exact coloured-graph source correspondence.

No author census receipt is used as a substitute for running the required GAP
programs. The literal source graph data is mandatory mathematical input.
"""
from pathlib import Path
import argparse, ast, hashlib, json, shutil, subprocess, tempfile, time

ROOT = Path(__file__).resolve().parent

def need(value, message):
    if not value:
        raise ValueError(message)

def conjugacy(a, b):
    """All rooted deterministic coloured graph maps; fixed points are included."""
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        return None
    n = len(a[0])
    for image in range(n):
        f, queue, ok = {0: image}, [0], True
        for x in queue:
            for aa, bb in zip(a, b):
                y, z = aa[x] - 1, bb[f[x]] - 1
                if y in f:
                    if f[y] != z:
                        ok = False
                        break
                elif z in f.values():
                    ok = False
                    break
                else:
                    f[y] = z
                    queue.append(y)
            if not ok:
                break
        if ok and len(f) == n:
            return [f[x] + 1 for x in range(n)]
    return None

def source_rows(path):
    data = json.loads(path.read_text())
    rows = data['rows']
    need([r['source_row'] for r in rows] == list(range(1,17)), 'literal sixteen rows')
    for r in rows:
        n, d = r['degree'], r['rank']
        gs = [list(range(1,n+1)) for _ in range(d)]
        for a,b,c in r['edges']:
            need(1 <= a <= n and 1 <= b <= n and 0 <= c < d and a != b, 'edge range')
            need(gs[c][a-1] == a and gs[c][b-1] == b, 'same-colour matching')
            gs[c][a-1], gs[c][b-1] = b,a
        need(gs == r['generators'], 'literal edges/permutations differ')
    for i,a in enumerate(rows):
        for b in rows[i+1:]:
            need(not conjugacy(a['generators'], b['generators']) and
                 not conjugacy(a['generators'], b['generators'][::-1]), 'duplicate source class')
    return rows

def compare(log, rows):
    roster, solutions, complete, named = [], [], None, []
    for line in log.splitlines():
        if line.startswith('ROSTER|'):
            s=line.split('|');roster.append({'degree':int(s[1]),'id':int(s[2]),'order':int(s[3]),'status':s[4]})
        elif line.startswith('SOLUTION|'):
            _,n,id,types,gens=line.split('|')
            solutions.append({'degree':int(n),'id':int(id),'types':ast.literal_eval(types),'generators':ast.literal_eval(gens)})
        elif line.startswith('COMPLETE|'):
            complete=[int(x) for x in line.split('|')[1:]]
        elif line.startswith('NAMED|'):
            named.append(line)
    need(complete is not None, 'complete GAP terminator absent')
    need(complete == [len(roster),sum(r['status']=='CENSUS' for r in roster),len(solutions)],'roster completeness mismatch')
    need(len({(r['degree'],r['id']) for r in roster}) == len(roster),'duplicate action')
    matches=[];covered=set()
    for s in solutions:
        found=[]
        for r in rows:
            for dual in (False,True):
                target=r['generators'][::-1] if dual else r['generators']
                f=conjugacy(s['generators'],target)
                if f:
                    found.append({'row':r['source_row'],'dual':dual,'vertex_map':f})
                    covered.add(r['source_row'])
        need(found,'computed marking missing from literal source table')
        need(len({f['row'] for f in found})==1,'ambiguous source row')
        matches.append(dict(s, source_matches=found))
    need(covered==set(range(1,17)),'source row not attained by complete census')
    for i,a in enumerate(solutions):
        for b in solutions[i+1:]:
            need(not conjugacy(a['generators'],b['generators']),'duplicate ordered class')
    need(complete[1:]==[17,27],'changed finite result')
    need(len(named)==5,'named-group checks absent')
    return {'catalogue_actions':len(roster),'searched_actions':17,'ordered_classes':27,
            'source_duality_classes':16,'roster':roster,'named_checks':named,'matches':matches}

def controls(log, rows):
    checks=[]
    fixtures=[('missing_completion',log.replace('COMPLETE|','INCOMPLETE|'),rows),
              ('missing_source_row',log,rows[:-1]),
              ('missing_marking','\n'.join(x for x in log.splitlines() if not x.startswith('SOLUTION|5|')),rows)]
    for name,bad,rr in fixtures:
        try: compare(bad,rr)
        except ValueError: checks.append(name)
        else: raise ValueError('control accepted: '+name)
    damaged=json.loads(json.dumps(rows));damaged[3]['generators'][0]=list(range(1,10))
    try:compare(log,damaged)
    except ValueError:checks.append('changed_source_colour')
    else:raise ValueError('changed source colour accepted')
    a=[[2,1,3],[1,3,2]];b=[[1,3,2],[2,1,3]]
    need(conjugacy(a,b) is not None,'positive conjugacy fixture')
    need(conjugacy(a,[[1,2,3],b[1]]) is None,'fixed-point mismatch fixture')
    checks.extend(['positive_conjugacy_fixture','fixed_point_mismatch_fixture'])
    return checks

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path)
    p.add_argument('--gap',default='/opt/homebrew/bin/gap');p.add_argument('--render',action='store_true')
    p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=False)
    manifest=ROOT/'manifest.json'
    if manifest.exists():
        for r in json.loads(manifest.read_text())['exports']:
            raw=(ROOT/r['path']).read_bytes()
            need(len(raw)==r['bytes'] and hashlib.sha256(raw).hexdigest()==r['sha256'],'export '+r['path'])
    started=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='L044_table2_') as tmp:
        tmp=Path(tmp)
        for name in ('census.g','run.g'):shutil.copyfile(ROOT/name,tmp/name)
        run=subprocess.run([a.gap,'-q','-b','run.g'],cwd=tmp,capture_output=True,timeout=60)
    log=(run.stdout+run.stderr).decode(errors='replace');(a.out/'census.log').write_text(log)
    need(run.returncode==0 and 'Error,' not in log and 'Syntax error' not in log,'GAP execution failed')
    rows=source_rows(ROOT/'source_table2.json');result=compare(log,rows)
    (a.out/'correspondence.json').write_text(json.dumps(result,indent=2)+'\n')
    render=None
    if a.render:
        from pypdf import PdfReader
        tmp=a.out/'render';tmp.mkdir();shutil.copyfile(ROOT/'small_primitive.tex',tmp/'small_primitive.tex')
        for k in range(2):
            run=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','small_primitive.tex'],cwd=tmp,capture_output=True,timeout=45)
            (a.out/f'render{k}.log').write_bytes(run.stdout+run.stderr);need(run.returncode==0,'render failed')
        old=[p.extract_text() for p in PdfReader(ROOT/'small_primitive.pdf').pages]
        new=[p.extract_text() for p in PdfReader(tmp/'small_primitive.pdf').pages]
        need(old==new,'rendered page texts differ');render={'pages':len(new),'all_page_texts_equal':True}
    report={'status':'PASS','role':'required finite census, exact source graph correspondence; no whole-source admission',
            'catalogue_actions':result['catalogue_actions'],'searched_actions':17,'ordered_classes':27,
            'source_duality_classes':16,'controls':controls(log,rows),'render':render,
            'elapsed_seconds':time.monotonic()-started,'no_new_Lean':True}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':main()
