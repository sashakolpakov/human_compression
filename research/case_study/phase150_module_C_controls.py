#!/usr/bin/env python3
"""Isolated structural, mutation and output-refusal checks for Module C.

No GAP or Lean theorem/census execution occurs. This audits portability and
bindings, not mathematical correctness. Existing output directories are refused.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent


def require(test, message):
    if not test:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    require(not os.path.lexists(args.output_dir), 'Refusing existing output path')
    manifest_path = ROOT / 'phase150_module_C_manifest.json'
    manifest = json.loads(manifest_path.read_text())
    records = manifest['files'] + manifest['required_shared_inputs']
    for record in records:
        require(sha(ROOT / record['path']) == record['sha256'], 'Changed input before controls')
    cases = []
    with tempfile.TemporaryDirectory(prefix='module-C-portable-') as temporary:
        scratch = Path(temporary)
        public = scratch / 'research' / 'case_study'
        for record in records:
            src = ROOT / record['path']; dest = public / record['path']
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dest)
        shutil.copyfile(manifest_path, public / manifest_path.name)
        require(not (public / 'sources').exists(), 'Private source material copied')
        verifier = public / 'phase150_module_C_verify.py'
        runner = public / 'phase150_module_C_run.py'

        def run(case, argv, success, needle=None, output=None):
            process = subprocess.run([sys.executable, '-O', *map(str, argv)],
                                     cwd=scratch, capture_output=True, text=True, timeout=40)
            require((process.returncode == 0) == success, 'Unexpected result: ' + case)
            if needle:
                require(needle in process.stdout + process.stderr, 'Wrong refusal: ' + case)
            if output and not success:
                require(not os.path.lexists(output), 'Rejected operation created output: ' + case)
            cases.append({'case': case, 'returncode': process.returncode,
                          'expected_success': success, 'expected_diagnostic': needle,
                          'stdout': process.stdout, 'stderr': process.stderr})

        result = scratch / 'portable.json'
        run('public layout without primary files', [verifier, '--output', result], True,
            'MODULE_C_STRUCTURAL_BINDINGS_PASS')
        portable = json.loads(result.read_text())
        changed = ['phase150_module_C_manuscript.md', 'phase138_umbrella_v3.md',
                   'phase40_compress_operations_check.g', 'phase40_compress_operations_exhaustive.g',
                   'phase150_module_C_ledger.json', 'phase150_module_C_costs.json',
                   'phase150_module_C_render/application.pdf',
                   'phase150_module_C_render/render_report.json',
                   'phase150_module_C_visual_review.json']
        for number, name in enumerate(changed):
            path = public / name; old = path.read_bytes(); path.write_bytes(old + b'\n')
            output = scratch / ('changed-%d.json' % number)
            run('changed input: ' + name, [verifier, '--output', output], False,
                'Changed package input', output)
            path.write_bytes(old)

        # Rebind a bad span at the package layer, so this tests the semantic span
        # check rather than merely a changed-file digest.
        lp = public / 'phase150_module_C_ledger.json'; old_ledger = lp.read_bytes()
        mp = public / manifest_path.name; old_manifest = mp.read_bytes()
        ledger = json.loads(old_ledger)
        ledger['proof_legs']['C.Petrial']['binding']['end_char'] -= 1
        lp.write_text(json.dumps(ledger, indent=2) + '\n')
        altered_manifest = json.loads(old_manifest)
        for record in altered_manifest['files']:
            if record['path'] == lp.name:
                record['sha256'] = sha(lp); record['bytes'] = lp.stat().st_size
        mp.write_text(json.dumps(altered_manifest, indent=2) + '\n')
        output = scratch / 'bad-span.json'
        run('rebound but incorrect full proof span', [verifier, '--output', output], False,
            'Incorrect full proof binding', output)
        lp.write_bytes(old_ledger); mp.write_bytes(old_manifest)

        for kind in ['file', 'directory', 'dangling symlink']:
            existing = scratch / ('existing-' + kind.replace(' ', '-'))
            if kind == 'file': existing.write_bytes(b'preserve this sentinel')
            elif kind == 'directory': existing.mkdir()
            else: existing.symlink_to(scratch / 'nonexistent-target')
            run('verifier refuses ' + kind, [verifier, '--output', existing], False,
                'Refusing existing output path')
            run('runner refuses ' + kind, [runner, '--output-dir', existing], False,
                'Refusing existing output path')
            if kind == 'file':
                require(existing.read_bytes() == b'preserve this sentinel', 'Output was clobbered')
            elif kind == 'directory':
                require(not list(existing.iterdir()), 'Existing directory was modified')
            else:
                require(existing.is_symlink(), 'Symlink was removed')

        for number, name in enumerate(changed[2:4]):
            path = public / name; old = path.read_bytes(); path.write_bytes(old + b'\n')
            output = scratch / ('runner-changed-%d' % number)
            run('runner rejects changed program before GAP: ' + name,
                [runner, '--output-dir', output, '--gap', '/GAP-MUST-NOT-BE-INVOKED'],
                False, 'Changed required program', output)
            path.write_bytes(old)
        run('runner command interface', [runner, '--help'], True)
        final = scratch / 'portable-final.json'
        run('public inputs restored', [verifier, '--output', final], True,
            'MODULE_C_STRUCTURAL_BINDINGS_PASS')
        require(json.loads(final.read_text()) == portable, 'Restored replay differs')
        for record in records:
            require(sha(public / record['path']) == record['sha256'], 'Control left altered input')
    args.output_dir.mkdir(parents=True)
    report = {'status': 'PASS_STRUCTURAL_CONTROLS', 'manifest_sha256_at_execution': sha(manifest_path),
              'controls_script_sha256': sha(Path(__file__)), 'cases': cases,
              'case_count': len(cases), 'portable_replay': portable,
              'private_sources_copied': False, 'fresh_GAP_execution': False,
              'fresh_Lean_execution': False, 'mathematical_correctness_proved': False,
              'final_seal_note': 'When evidence is added to the final manifest after this run, its new hash differs. All computational input hashes remain bound here and are rechecked after sealing.',
              'checked_bindings': records}
    (args.output_dir / 'phase150_module_C_controls_report.json').write_text(
        json.dumps(report, indent=2, sort_keys=True) + '\n')
    print('MODULE_C_STRUCTURAL_CONTROLS_PASS', len(cases))


if __name__ == '__main__':
    main()
