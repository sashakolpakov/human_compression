#!/usr/bin/env python3
"""Replay the frozen author packet and independent source-incidence checks."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
AUTHOR = 'cbbb953e5565ef1dd36286fe245c12c81fd1f854be5d887a544361055d97a24b'


def require(ok, why):
    if not ok:
        raise ValueError(why)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output-dir',type=Path,required=True)
    p.add_argument('--gap',default='/opt/homebrew/bin/gap')
    p.add_argument('--lean',default='/Users/sasha/.elan/bin/lean')
    p.add_argument('--packages',default='/Users/sasha/bogachev/formal/.lake/packages')
    args = p.parse_args()
    out = args.output_dir.absolute()
    require(not out.exists(), 'fresh output directory required')
    require(digest(ROOT/'phase186_export.json') == AUTHOR, 'author manifest changed')
    manifest = json.loads((ROOT/'phase186_export.json').read_text())
    rows = manifest['exports']+manifest['retained_inputs']
    def verify():
        for row in rows:
            file = ROOT/row['path']
            require(file.stat().st_size == row['bytes'] and digest(file) == row['sha256'],
                    'author binding changed: '+row['path'])
    verify()
    local = ['phase199_review.py','phase199_hermitian_literal.g','phase199_path_length.py']
    inputs = {name:digest(ROOT/name) for name in local}
    out.mkdir(parents=True)
    def command(label, argv, marker=None, expected_success=True):
        r = subprocess.run(argv,cwd=ROOT,text=True,capture_output=True,timeout=300)
        text = r.stdout+r.stderr
        (out/(label+'.log')).write_text(text)
        if expected_success:
            require(r.returncode == 0 and 'Error,' not in text, label+' command failed')
            if marker:
                require(marker in text, label+' acceptance marker absent')
        else:
            require('Error,' in text and (not marker or marker not in text), label+' mutation survived')
        return text
    command('author_replay',[sys.executable,'-B',str(ROOT/'phase186_check.py'),'--out',
            str(out/'author'),'--gap',args.gap,'--lean',args.lean,'--packages',args.packages])
    command('literal_hermitian',[args.gap,'-q','-b',str(ROOT/'phase199_hermitian_literal.g')],
            'P199_LITERAL_HERMITIAN_PASS')
    command('retained_mathieu_fibers',[args.gap,'-q','-b',str(ROOT/'phase182_mathieu_fibers.g')],
            'P182_MATHIEU_EXTENSION_FIBERS_PASS')
    path_report = json.loads(command('path_length',[sys.executable,'-B',str(ROOT/'phase199_path_length.py')]))
    require(path_report['status']=='PASS', 'path check failed')
    original = (ROOT/'phase199_hermitian_literal.g').read_text()
    old = 'return x in flag[2] and x<>flag[1];'
    require(original.count(old)==1, 'source-incidence mutation site is not unique')
    mutant = out/'wrong_flag_incidence.g'
    mutant.write_text(original.replace(old,'return not x in flag[2] and x<>flag[1];'))
    command('wrong_flag_incidence',[args.gap,'-q','-b',str(mutant)],
            'P199_LITERAL_HERMITIAN_PASS',False)
    author = json.loads((out/'author/phase186_build.json').read_text())
    witness = json.loads((out/'author/phase186_witt_witness.json').read_text())
    require(digest(out/'author/phase186_witt_witness.json') ==
            manifest['replay']['artifact_hashes']['phase186_witt_witness.json'],
            'fresh exact Witt witness differs')
    verify()
    require(inputs == {name:digest(ROOT/name) for name in local},'review code changed during run')
    report = dict(status='PASS',author_manifest_sha256=AUTHOR,review_inputs=inputs,
        author_finite_cases=author['finite_cases'],author_new_Lean_reports=author['new_Lean_axiom_reports'],
        author_retained_Lean_reports=author['retained_dependency_axiom_reports'],
        author_Lean_negative_controls=author['Lean_negative_controls'],
        independent_literal_Hermitian_q=[3,4,5],independent_path_length=path_report,
        independent_source_incidence_mutation='REJECTED',retained_Mathieu_fibers_freshly_passed=True,
        GAP_version=witness['gap_version'],DESIGN_version=witness['design_version'],
        GRAPE_version=witness['grape_version'],mathlib_revision=author['mathlib_revision'],
        complete_Witt_witness_byte_identical=True,
        scope='Scientific acceptance and limitations are in phase199_L092_review.md; finite replay does not formalize the uniform proofs.',
        public_edits=False,new_open_conjecture_credit=0)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('PHASE199_REVIEW_PASS',digest(out/'report.json'))


if __name__ == '__main__':
    main()
