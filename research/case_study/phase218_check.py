#!/usr/bin/env python3
"""Independent finite and scoped Lean review of frozen phase211."""
import argparse
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent
AUTHOR_MANIFEST_SHA = '636bb448db55668c72d684971eb0d452ef6c3ce415bd11e7d929e5130280a8a4'
RETAINED = {
    'phase109_cover_families_generalization_model.json':
        '3299bad80e6880a7e45000662dc981bc54c623bf581676a9829912b7bea06715',
    'phase109_cover_families_generalization_theorem.md':
        'ecc09bbf395aa45a5830ba385eb7588e825f7c7b6a074ac5a2345e0d89876a9e',
    'phase112_cover_families_review_audit.md':
        'e896441e08de339d7f1b0ddbe0c4a4a98dcf43238b224c3b38862a72fc0953f3',
}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def command(args, expected=0, timeout=240):
    start = time.monotonic()
    result = subprocess.run(args, cwd=ROOT, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            timeout=timeout)
    require(result.returncode == expected,
            f'command returned {result.returncode}, expected {expected}: {args}\n{result.stdout}')
    return dict(returncode=result.returncode, output=result.stdout,
                seconds=round(time.monotonic()-start, 6))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=pathlib.Path, required=True)
    ap.add_argument('--gap', default=shutil.which('gap') or '/opt/homebrew/bin/gap')
    ap.add_argument('--lean', default='/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean')
    ap.add_argument('--packages', default='/Users/sasha/bogachev/formal/.lake/packages')
    args = ap.parse_args()
    require(not args.out.exists() and not args.out.is_symlink(), 'fresh output path required')
    manifest = ROOT / 'phase211_export.json'
    require(sha(manifest) == AUTHOR_MANIFEST_SHA, 'author manifest binding mismatch')
    bound = json.loads(manifest.read_text())['files']
    for name, record in bound.items():
        p = ROOT / name
        require(p.stat().st_size == record['bytes'] and sha(p) == record['sha256'],
                f'author binding mismatch: {name}')
    for name, digest in RETAINED.items():
        require(sha(ROOT/name) == digest, f'retained binding mismatch: {name}')
    native_source = (ROOT / 'phase218_independent.g').read_text()
    match = re.search(r'Dmarks:=List\((\[[\s\S]+?\]),PermList\);;', native_source)
    require(match is not None, 'native source model declaration missing')
    require(json.loads(match[1]) == json.loads((ROOT /
        'phase109_cover_families_generalization_model.json').read_text())['generators'],
        'native D marking differs from retained literal model')
    out = args.out.resolve()
    out.mkdir(parents=True)
    author = command([sys.executable, '-B', '-O', str(ROOT/'phase211_check.py'),
                      '--out', str(out/'author'), '--lean', args.lean,
                      '--packages', args.packages])
    (out/'author_driver.log').write_text(author['output'])
    author_report = json.loads((out/'author/report.json').read_text())
    require(author_report['status'] == 'PASS' and author_report['Lean_theorems'] == 6,
            'author replay did not establish its declared scope')
    native = out/'independent.g'
    native.write_text(native_source)
    independent = command([args.gap, '-q', str(native)])
    require('P218_INDEPENDENT_PASS' in independent['output'] and
            'Syntax warning' not in independent['output'] and 'Error,' not in independent['output'],
            'independent native calculation did not complete cleanly')
    (out/'independent.log').write_text(independent['output'])
    controls = []
    mutations = [
        ('identity_mark', 'Surface("D256",Dmarks);;',
         'Dmarks[1]:=();; Surface("D256",Dmarks);;', 'REJECT distinct involutions'),
        ('one_orientation_constraint', 'whole:=solve([],[]);',
         'es[1][1]:=-es[1][1]; whole:=solve([],[]);', 'REJECT D closed surface'),
        ('omit_second_facet_type',
         'faces[4]:=Concatenation(faces[4],faces[5]);Unbind(faces[5]);',
         'Unbind(faces[5]);', 'REJECT complete incidence flag enumeration'),
    ]
    for name, old, new, reason in mutations:
        require(native_source.count(old) == 1, f'mutation anchor changed: {name}')
        p = out/f'control_{name}.g'
        p.write_text(native_source.replace(old, new))
        result = command([args.gap, '-q', str(p)], expected=1)
        require(reason in result['output'] and 'P218_INDEPENDENT_PASS' not in result['output'],
                f'negative control rejected for unexpected reason: {name}')
        (out/f'control_{name}.log').write_text(result['output'])
        controls.append(dict(name=name, reason=reason, **result))
    # Confirm that the original frozen files were not modified by any replay.
    for name, record in bound.items():
        require(sha(ROOT/name) == record['sha256'], f'author file changed: {name}')
    require(sha(manifest) == AUTHOR_MANIFEST_SHA, 'author manifest changed')
    report = dict(status='PASS', author_manifest_sha256=AUTHOR_MANIFEST_SHA,
                  author_binding_count=len(bound), retained_bindings=RETAINED,
                  native_source_sha256=sha(ROOT/'phase218_independent.g'),
                  author=author, independent=independent, independent_controls=controls,
                  author_Lean_theorems=6, author_Lean_axioms=author_report['Lean_axioms'],
                  author_controls='two finite controls and one Lean weakening control passed',
                  native_results={
                      'D256': {'cells': [256,512,224], 'orientable': True,
                               'complements': [[178,True],[223,True],[223,True]],
                               'end_cells': [64,96,24], 'end_boundary_cycles': [8]*8},
                      'Tomotope': {'automorphism_order': 96, 'all_incidence_flags': 192,
                                   'monodromy_order': 18432, 'cells': [18432,36864,14592],
                                   'orientable': False,
                                   'complements': [[14090,False],[14591,False],[14591,False]]}},
                  written_scope='Review separately accepts the homological intersection, surface criterion, all-prime construction, retained-source family transport, and infinite minimal-descendant argument. These are not established by finite replay or all formalized in Lean.',
                  exclusions=['No resolution of the arbitrary-polytope conjecture.',
                              'No newly solved Tomotope multiplicity question.',
                              'No whole-source or compression-ratio credit.',
                              'No historical-priority claim.'])
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','independent_controls':len(controls),
                      'Lean_theorems':6,'report':str(out/'report.json')}))


if __name__ == '__main__':
    main()
