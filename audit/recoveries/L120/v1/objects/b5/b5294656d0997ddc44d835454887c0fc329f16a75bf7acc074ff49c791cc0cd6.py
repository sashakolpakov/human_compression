"""Small complete controls and literal six-point fusion; no large census."""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
import argparse, hashlib, json, os, re, shutil, subprocess
from pathlib import Path

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--study', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--render', action='store_true')
    args = parser.parse_args()
    S, P, O = args.study.resolve(), Path(__file__).resolve().parent, args.out.resolve()
    need(not O.exists(), 'fresh output')
    bindings = json.loads((P/'dependencies.json').read_text())
    for row in bindings:
        data = (S/row['path']).read_bytes()
        need(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'], 'dependency '+row['path'])
    exports = []
    if (P/'manifest.json').exists():
        exports = json.loads((P/'manifest.json').read_text())['exports']
        for row in exports:
            data = (P/row['path']).read_bytes()
            need(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'], 'frozen export '+row['path'])
    O.mkdir(parents=True)
    env = os.environ.copy()
    env.pop('PYTHONOPTIMIZE', None)
    def run(name, command, cap, cwd=None):
        cp = subprocess.run(command, cwd=cwd, env=env, capture_output=True, timeout=cap)
        (O/(name+'.stdout')).write_bytes(cp.stdout)
        (O/(name+'.stderr')).write_bytes(cp.stderr)
        need(cp.returncode==0 and not cp.stderr, 'clean complete '+name)
        return cp.stdout.decode()
    # No fixed large-row plan is accessible through this checker.
    run('controls', [sys.executable, str(P/'run_pool.py'), '--plan', str(P/'pool_control_plan01.json'), '--out', str(O/'controls')], 100)
    plan = json.loads((P/'pool_control_plan01.json').read_text())
    reference = json.loads((P/'control_references.json').read_text())
    need(len(plan['runs'])==len(reference)==9, 'nine complete controls')
    for row, ref in zip(plan['runs'], reference):
        D = O/'controls'/row['name']
        receipt = json.loads((D/'report.json').read_text())
        need(receipt['status']=='COMPLETE_FIXED_BRANCH', 'complete branch required')
        need(json.loads((D/'result.json').read_text())==json.loads((S/ref['path']).read_text()), 'full literal control equivalence')
    # Derive the full S6 input from fresh completed enumerations, not a target count.
    involutions, ids = None, []
    for branch in [1,2,3]:
        D = O/'controls'/('pool_connected6_part'+str(branch))
        text = (D/'stdout.log').read_text()
        match = re.search(r'INVOLUTIONS_LITERAL\s+(\[.*?\])\s+DIRECT_INITIAL_CHILD', text, re.S)
        need(match is not None, 'literal involution list')
        literal = match.group(1)
        if involutions is None:
            involutions = literal
        else:
            need(involutions==literal, 'identical fresh sorted involutions')
        result = json.loads((D/'result.json').read_text())
        ids.extend(row['ids'] for row in result['marks'] if row['order']==720)
    need(len(ids)==len(set(map(tuple, ids))), 'no repeated target tuple across initial classes')
    (O/'six_input.g').write_text('ivs:='+involutions+';;\nids:='+json.dumps(ids)+';;\n')
    (O/'six_driver.g').write_text('inputFile:='+json.dumps(str(O/'six_input.g'))+';;\nRead('+json.dumps(str(P/'six.g'))+');\n')
    output = run('six', ['/opt/homebrew/bin/gap','-q','-T',str(O/'six_driver.g')], 60)
    pattern = r'RANK\s+(\d+)\s+POINT_CLASSES\s+(\d+)\s+OUTER\s+(\[.*?\])\s+REVERSE\s+(\[.*?\])\s+FULL_AUT\s+(\d+)\s+WITH_DUAL\s+(\d+)'
    rows = [dict(rank=int(r), point_classes=int(n), outer_permutation=json.loads(a), reversal_permutation=json.loads(b), full_aut_classes=int(c), with_duality=int(d)) for r,n,a,b,c,d in re.findall(pattern, output, re.S)]
    expected = json.loads((P/'six_expected.json').read_text())
    need(rows==expected['rows'], 'actual full automorphism and reversal orbits')
    need(output.count('TERMINAL_S6_FUSION')==1 and 'SUBSET_PAIRS 6016' in output, 'complete independent subset verification')
    # The guards fail before producing an output directory.
    guards = 0
    for name in ['check.py','run_pool.py']:
        for mode in ['argument','environment']:
            command = [sys.executable]
            e = env.copy()
            if mode=='argument': command.append('-O')
            else: e['PYTHONOPTIMIZE']='1'
            target = O/(name+'_'+mode+'_forbidden')
            cp = subprocess.run(command+[str(P/name),'--study',str(S),'--out',str(target)], env=e, capture_output=True, timeout=10)
            (O/(name+'_'+mode+'.stderr')).write_bytes(cp.stderr)
            need(cp.returncode!=0 and b'unoptimized execution required' in cp.stderr and not target.exists(), 'optimization guard')
            guards += 1
    pages = None
    if args.render:
        N = O/'native';N.mkdir();shutil.copyfile(P/'search.tex',N/'search.tex')
        for i in range(2): run('native'+str(i),['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','search.tex'],45,N)
        from pypdf import PdfReader
        pages=len(PdfReader(N/'search.pdf').pages)
        need(pages<=6 and pages>=3,'full native manuscript')
        run('raster',['/opt/homebrew/bin/gs','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png','search.pdf'],45,N)
        need('Overfull' not in (N/'search.log').read_text(),'native width')
    report=dict(status='PASS_FINITE_METHOD_AND_S6',exports=len(exports),dependencies=len(bindings),complete_controls=9,
                subset_pairs=6016,six_rows=rows,optimization_guards=guards,native_pages=pages,
                new_survey_numeric_cells=1,large_rows_complete=False,whole_original_credit=0)
    (O/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__=='__main__':main()
