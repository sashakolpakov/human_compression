"""Portable bounded review replay; supplied author packet remains immutable."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from independent_oracle import source_oracle, a5_oracle
from literal_checks import check as literal_check

HERE = Path(__file__).resolve().parent
AUTHOR_SHA = '591169a4e8e2625a2c85b217a59c13758554ffd85cbd5624bf048e01e6b667a9'


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def bindings(base, manifest):
    rows = json.loads(manifest.read_text())['exports']
    for row in rows:
        p = base/row['path']
        need(p.stat().st_size == row['bytes'] and sha(p) == row['sha256'], row['path'])
    return len(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--author', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--rerun-author', action='store_true')
    args = parser.parse_args()
    need(not args.out.exists(), 'fresh output')
    args.out.mkdir(parents=True)
    need(sha(args.author/'manifest.json') == AUTHOR_SHA, 'exact author freeze')
    author_files = bindings(args.author, args.author/'manifest.json')
    review_files = bindings(HERE, HERE/'manifest.json') if (HERE/'manifest.json').exists() else None
    review = json.loads((HERE/'review.json').read_text())
    need(review['status'] == 'ACCEPTED_COMPLETE_PRINCIPAL_CONTRACT', 'scope status')
    need(review['no_literal_theorem_set_equivalence'] and review['new_Lean_credit'] == 0 and review['new_conjecture_credit'] == 0, 'limited credit')
    scope = json.loads((args.author/'source_map.json').read_text())
    need(len(scope['rows']) == 40 and len({r['id'] for r in scope['rows']}) == 40, 'whole source dispositions')
    need(next(r for r in scope['rows'] if r['id']=='5.3')['status'] == 'ANCILLARY_SOURCE_PROOF_ROUTE_NOT_INDEPENDENTLY_RECOVERED', 'appendix boundary')
    inv = json.loads((args.author/'program_inventory.json').read_text())
    need(len(inv['whole_files']) == 7 and inv['source_software_cost'] is None and inv['no_software_inclusive_factor'], 'program scope')
    for r in inv['whole_files']:
        p = args.author/r['path']
        need(p.stat().st_size == r['bytes'] and sha(p) == r['sha256'], 'program binding')
    retained = json.loads((args.author/'retained_projective.json').read_text())['whole_files']
    need(len(retained) == 380, 'full retained closure')
    for r in retained:
        need(sha(args.author/r['path']) == r['sha256'], 'retained binding')
    independent = json.loads(json.dumps({'status':'PASS','source':source_oracle(),'small_exhaustion':a5_oracle()}))
    need(independent == json.loads((HERE/'evidence/independent_oracle.json').read_text()), 'independent coordinate replay')
    oracle_file = args.out/'independent_oracle.json'
    oracle_file.write_text(json.dumps(independent,indent=2)+'\n')
    result = literal_check(args.author/'generated_markings.g',args.author/'source_markings.g',
                           HERE/'evidence/a5.stdout',oracle_file)
    need(json.loads(json.dumps(result)) == json.loads((HERE/'evidence/literal_checks.json').read_text()), 'whole literal replay')
    small_receipt = json.loads((HERE/'evidence/a5_author_report.json').read_text())
    for r in small_receipt['pins']:
        need(sha(args.author/r['path']) == r['sha256'], 'small run uses exact frozen code')
    need(small_receipt['returncode'] == 0 and small_receipt['complete_marker'] and small_receipt['unchanged'], 'complete small run')
    controls = []
    with tempfile.TemporaryDirectory(dir=args.out) as tmp:
        root = Path(tmp)
        good = (args.author/'generated_markings.g').read_text()
        source = (args.author/'source_markings.g').read_text()
        small = (HERE/'evidence/a5.stdout').read_text()
        mutations = [
            ('delete even involution', good.replace('( 8, 9)(10,11), ', '', 1), source, small),
            ('duplicate even involution', good.replace('( 8,10)( 9,11)', '( 8, 9)(10,11)', 1), source, small),
            ('corrupt required source edge', good, source.replace('(2,3)', '(2,4)',1), small),
            ('delete rank-four record', re.sub(r'recordedMarks\[4\]:=.*?;;', 'recordedMarks[4]:=[];;', good, flags=re.S), source, small),
            ('delete small exhaustive class', good, source, small.replace('[ [ 1, 4, 2 ], [ 1, 5, 2 ], [ 1, 5, 3 ] ]','[ [ 1, 4, 2 ], [ 1, 5, 2 ] ]')),
            ('duplicate source class', good, source.replace('(1,2)(3,4)(8,9)(10,11)','(1,2)(3,4)(6,7)(8,9)',1), small),
        ]
        for name,g,s,l in mutations:
            need((g,s,l) != (good,source,small), 'active mutation '+name)
            (root/'g.g').write_text(g);(root/'s.g').write_text(s);(root/'small.txt').write_text(l)
            rejected = False
            try:
                literal_check(root/'g.g',root/'s.g',root/'small.txt',oracle_file)
            except (ValueError,IndexError):
                rejected = True
            need(rejected, 'mutation accepted '+name)
            controls.append(name)
    controls += independent['source']['controls']
    if args.rerun_author:
        p=subprocess.run([sys.executable,'-B','-O',str(args.author/'check.py'),'--out',str(args.out/'author_replay'),'--render'],capture_output=True,text=True)
        (args.out/'author.stdout').write_text(p.stdout);(args.out/'author.stderr').write_text(p.stderr)
        need(p.returncode==0, 'fresh author replay')
    report = dict(status='PASS',author_exports=author_files,review_exports=review_files,retained_files=380,
                  source_dispositions=40,involutions=18315,source_rows=5,source_orbit_cells=10,
                  a5_orbit_counts={'3':3,'4':0,'5':0},literal_matches=10,independent_controls=controls,
                  author_rerun=args.rerun_author,new_Lean_credit=0,new_conjecture_credit=0,new_compression_factor=None)
    (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
