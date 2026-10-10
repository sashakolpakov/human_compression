#!/usr/bin/env python3
"""Replay the independent kernel-action check on actual voltage permutations."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--voltage', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--gap', default='/opt/homebrew/bin/gap')
    a = p.parse_args()
    if a.out.exists():
        raise ValueError('fresh output directory required')
    a.out.mkdir(parents=True)
    model = json.loads(a.voltage.read_text())
    def marks(generators):
        return '['+','.join('PermList('+str(g)+')' for g in generators)+']'
    check = Path(__file__).with_name('phase255_kernel_action.g')
    script = a.out/'literal_kernel_action.g'
    script.write_text('HMarks:='+marks(model['generators'])+';;\nGMarks:='+
                      marks(model['base_generators'])+';;\n'+check.read_text())
    r = subprocess.run([a.gap,'-q','-T',str(script)],text=True,capture_output=True,timeout=300)
    (a.out/'stdout').write_text(r.stdout)
    (a.out/'stderr').write_text(r.stderr)
    if r.returncode or r.stderr or 'PHASE255_PASS' not in r.stdout:
        raise ValueError('independent kernel check failed')
    report = {'status':'PASS','input_sha256':hashlib.sha256(a.voltage.read_bytes()).hexdigest(),
              'checker_sha256':hashlib.sha256(check.read_bytes()).hexdigest(),
              'stdout':r.stdout,'scope':'Actual generated permutation cover; independent conjugation action on its three kernel lines.'}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(r.stdout,end='')


if __name__=='__main__':
    main()
