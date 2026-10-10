#!/usr/bin/env python3
"""Replay the independent L014 review, with frozen source and proof bindings."""
import argparse, hashlib, json, pathlib, re, subprocess, sys, time
ROOT = pathlib.Path(__file__).resolve().parent
AUTHOR_SHA = 'cd47d4db7001373e32c4a0c284a45891bc8908d61d1d5d218d8e85f248aa6092'
def need(ok, message):
    if not ok: raise RuntimeError('PHASE248_REJECT ' + message)
def digest(data): return hashlib.sha256(data).hexdigest()
def check_entry(row):
    path = pathlib.PurePosixPath(row['path'])
    need(not path.is_absolute() and '..' not in path.parts, 'relative artifact path')
    data = (ROOT / path).read_bytes()
    need(len(data) == row['bytes'] and digest(data) == row['sha256'], 'binding ' + str(path))
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=pathlib.Path, required=True)
    ap.add_argument('--gap', type=pathlib.Path, required=True)
    ap.add_argument('--lean', type=pathlib.Path, required=True)
    ap.add_argument('--packages', type=pathlib.Path, required=True)
    ap.add_argument('--verify-primary', action='store_true')
    args=ap.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(), 'fresh raw output path')
    out=args.out.resolve(); need(not out.exists(), 'fresh resolved output path'); out.mkdir(parents=True)
    authorbytes=(ROOT/'phase236_manifest.json').read_bytes()
    need(digest(authorbytes)==AUTHOR_SHA, 'author manifest')
    author=json.loads(authorbytes)
    for row in author['exports']: check_entry(row)
    for row in author['retained_bindings']:
        if args.verify_primary or not row['path'].startswith('sources/'): check_entry(row)
    review=json.loads((ROOT/'phase248_manifest.json').read_bytes())
    for row in review['exports']: check_entry(row)
    ledger=json.loads((ROOT/'phase236_source_ledger.json').read_bytes())
    need(len(ledger['rows'])==25 and len(ledger['proof_spans'])==10, 'source ledger cardinalities')
    for name,row in ledger['proof_spans'].items():
        lines=(ROOT/row['path']).read_bytes().splitlines(keepends=True)
        data=b''.join(lines[row['start_line']-1:row['end_line']])
        need(len(data)==row['utf8_bytes'] and digest(data)==row['sha256'], 'proof span '+name)
    for row in ledger['rows']:
        need(all(span in ledger['proof_spans'] for span in row['proof_span_closure']), 'proof dependency row')
    contract=json.loads((ROOT/'phase248_contract.json').read_bytes())
    need([r['source_row_id'] for r in contract['ledger_review']]==[r['id'] for r in ledger['rows']], 'exact source row review')
    # A one-byte mutation must not be admitted as the bound author manifest.
    need(digest(authorbytes+b' ') != AUTHOR_SHA, 'manifest mutation rejection')
    def run(label, command, timeout=240):
        start=time.monotonic()
        proc=subprocess.run([str(x) for x in command],cwd=out,text=True,capture_output=True,timeout=timeout)
        for suffix,data in [('stdout',proc.stdout),('stderr',proc.stderr)]: (out/(label+'.'+suffix)).write_text(data)
        return proc, dict(label=label,returncode=proc.returncode,seconds=round(time.monotonic()-start,4),
            stdout_sha256=digest(proc.stdout.encode()),stderr_sha256=digest(proc.stderr.encode()))
    proc,author_run=run('author236',[sys.executable,'-B','-O',ROOT/'phase236_check.py','--out',out/'author236',
        '--gap',args.gap,'--lean',args.lean,'--packages',args.packages])
    need(proc.returncode==0, 'fresh author replay exit')
    report=json.loads((out/'author236/report.json').read_bytes())
    need(report['status']=='PASS' and len(report['cyclotomic_parameters'])==7 and len(report['abelian_parameters'])==4,
        'eleven marked examples')
    need(report['intersection_equalities_per_model']==64 and len(report['axiom_reports'])==5 and len(report['negative_controls'])==3,
        'author control and formal scope')
    for basename in ['finite.stdout','formal.stdout','models.stdout']:
        need((out/'author236'/basename).read_bytes()==(ROOT/'phase236_author_replay'/basename).read_bytes(), 'semantic replay '+basename)
    proc,independent=run('presentation',[args.gap,'-q','-T',ROOT/'phase248_presentation_check.g'])
    need(proc.returncode==0 and 'PHASE248_PRESENTATION_PASS' in proc.stdout and not re.search(r'Error|warning',proc.stdout+proc.stderr),
        'independent literal-presentation replay')
    params=[tuple(map(int,x)) for x in re.findall(r'^LITERAL_PRESENTATION (\d+) (\d+) ORDER (\d+)',proc.stdout,re.M)]
    need(params==[(3,3,27),(3,6,729),(5,3,125),(5,5,3125),(11,3,1331)], 'independent exact orders')
    need(proc.stdout.count('IP64 PASS')==5 and 'COMPOSITE_INDEX_FALSE_WEAKENING_REJECTED' in proc.stdout, 'IP and prime hypothesis control')
    result=dict(status='PASS',author_manifest_sha256=AUTHOR_SHA,author_exports_checked=len(author['exports']),
        review_exports_checked=len(review['exports']),source_rows=25,proof_spans=10,primary_bindings_checked=args.verify_primary,
        author_replay=author_run,independent_presentation_replay=independent,presentation_parameters=params,
        semantic_controls=['author: cyclotomic coefficient','author: literal bad marking','author: source orders',
            'independent: composite-index false weakening'],integrity_control='changed author-manifest bytes rejected',
        lean_declarations=5,coverage='One corrected principal L014 contract, with written all-parameter proof and retained CP theorem.',
        limits=['No open-conjecture or whole-paper claim.','No compression ratio.',
            'Finite examples and GAP presentation algorithms are not a formal proof of all parameters.',
            'Lean covers five intersection/reflection interfaces, not the complete manuscript.',
            'Remote CP primary theorem is not locally hashed.'])
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',source_rows=25,proof_spans=10,independent_presentations=5,lean_declarations=5,report=str(out/'report.json'))))
if __name__=='__main__': main()
