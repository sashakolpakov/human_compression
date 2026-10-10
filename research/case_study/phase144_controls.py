#!/usr/bin/env python3
"""Isolated portability, changed-input and no-clobber controls for phase144."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-dir', type=Path, required=True)
    a = ap.parse_args()
    if os.path.lexists(a.output_dir):
        raise FileExistsError('Refusing existing control output directory')
    out = a.output_dir.absolute(); out.mkdir()
    manifest = json.loads((ROOT / 'phase144_manifest.json').read_text())
    public = out / 'math_compression/research/case_study'; public.mkdir(parents=True)
    names = {b['path'] for b in manifest['files'] + manifest['required_shared_inputs']}
    names.add('phase144_manifest.json')
    for name in names:
        target = public / name; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, target)
    rows = []

    def invoke(label, argv, ok, message=None):
        r = subprocess.run(argv, capture_output=True, text=True)
        (out / (label + '.stdout')).write_text(r.stdout)
        (out / (label + '.stderr')).write_text(r.stderr)
        passed = (r.returncode == 0) if ok else (r.returncode != 0 and message in r.stderr)
        if not passed:
            raise RuntimeError(label + ' unexpected outcome')
        rows.append(dict(name=label, passed=True, returncode=r.returncode))

    base = [sys.executable, '-B', '-O', str(public / 'phase144_recount.py')]
    invoke('portable-positive', base + ['--output', str(out / 'portable.json')], True)
    invoke('private-primary-recount', [sys.executable, '-B', '-O', str(ROOT / 'phase144_recount.py'),
        '--primary-check', '--output', str(out / 'primary.json')], True)
    mutations = ['phase138_umbrella_v3.md', 'phase138_module_A_v2.md',
        'phase78_n009_integration_census.g', 'phase78_n009_integration_finite.g',
        'phase78_n009_integration_data.g', 'phase78_n009_integration_run.py',
        'phase144_render/replacement.pdf', 'phase144_measurement_protocol.json']
    for i, name in enumerate(mutations, 1):
        p = public / name; original = p.read_bytes()
        try:
            p.write_bytes(original + b'\nMUTATION\n')
            invoke('mutation-' + str(i), base + ['--output', str(out / ('mutation-' + str(i) + '.json'))], False, 'Binding changed:')
        finally:
            p.write_bytes(original)
    runner = [sys.executable, '-B', '-O', str(public / 'phase144_measurement.py')]
    occupied = out / 'occupied'; occupied.write_text('preserve')
    directory = out / 'occupied-dir'; directory.mkdir()
    symlink = out / 'occupied-link'; symlink.symlink_to(occupied)
    dangling = out / 'dangling-link'; dangling.symlink_to(out / 'never-created')
    for i, path in enumerate([occupied, directory, symlink, dangling], 1):
        invoke('no-clobber-' + str(i), runner + ['--output-dir', str(path)], False, 'Refusing existing output directory:')
    source = public / 'sources/catalogue_L032.pdf'; source.parent.mkdir()
    source.write_bytes((ROOT / 'sources/catalogue_L032.pdf').read_bytes() + b'\nMUTATION\n')
    invoke('primary-PDF-mutation', runner + ['--output-dir', str(out / 'must-not-create')], False, 'Bound input changed: sources/catalogue_L032.pdf')
    if (out / 'must-not-create').exists() or occupied.read_text() != 'preserve':
        raise RuntimeError('A refusal modified an output')
    result = dict(status='PASS', cases=rows, case_count=len(rows),
        public_layout='math_compression/research/case_study', primary_files_needed_for_public_recount=False,
        mathematical_programs_or_Lean_executed=False)
    (out / 'controls.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
