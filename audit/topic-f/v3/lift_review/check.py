#!/usr/bin/env python3
"""Bind the reviewed cyclic lift and compile its exact inherited Lean module."""
import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path

FRAGMENT = '8aeb15004912bed2cb6728e643f0bb4b0405e81d91228b757c81976a7ef230b5'
FORMAL = 'd8429bd867cbc8ea29c6af9768d93df49c5be027328f2b25fa32102cbc3009d7'
DEPENDENCIES = '4c716f4ff0ea4940311014c9853c0b8e5aaab8250f8cefdf9f8003845cfb02e3'


def need(value, message):
    if not value:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--fragment', type=Path, required=True)
    p.add_argument('--formal', type=Path, required=True)
    p.add_argument('--dependencies', type=Path, required=True)
    p.add_argument('--packages', type=Path, required=True)
    p.add_argument('--lean', required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    need(not a.out.exists(), 'fresh output required')
    a.out.mkdir(parents=True)
    need(sha(a.fragment) == FRAGMENT and sha(a.formal) == FORMAL
         and sha(a.dependencies) == DEPENDENCIES, 'changed reviewed proof input')
    dependencies = []
    for row in json.loads(a.dependencies.read_text())['packages']:
        directory = a.packages / row['name']
        rev = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=directory, text=True).strip()
        dirty = subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=no'],
                                        cwd=directory, text=True)
        need(rev == row['rev'] and not dirty, 'changed Lean source dependency')
        dependencies.append(dict(name=row['name'], revision=rev, tracked_clean=True))
    env = os.environ.copy()
    env['LEAN_PATH'] = ':'.join(str(d / '.lake/build/lib/lean') for d in a.packages.iterdir()
                               if (d / '.lake/build/lib/lean').is_dir())
    result = subprocess.run([a.lean, str(a.formal.resolve())], cwd=a.out, env=env,
                            capture_output=True, text=True, timeout=60)
    (a.out / 'lean.stdout').write_text(result.stdout)
    (a.out / 'lean.stderr').write_text(result.stderr)
    expected = ["'LeemansLift." + name +
                "' depends on axioms: [propext, Classical.choice, Quot.sound]" for name in
                ['reversing_preserves_power_subgroup', 'noReverser_of_cyclic_kernel',
                 'cyclic_intersection_transfer', 'intersection_of_image_and_kernel']]
    need(result.returncode == 0 and result.stderr == '' and result.stdout.strip().splitlines() == expected,
         'Lean declarations or axiom scope differ')
    report = dict(status='PASS_ROOT_CYCLIC_LIFT_INTERFACE', fragment_sha256=FRAGMENT,
                  formal_sha256=FORMAL, compiled_declarations=4, used_by_cyclic_lift=3,
                  new_declarations=0, axioms='standard only', dependencies=dependencies,
                  compiled_dependencies_trusted=True, finite_model_construction_formalized=False,
                  source_parameter_family_formalized=False, geometric_correspondence_formalized=False,
                  full_original_credit=0, new_question_credit=0)
    (a.out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
