#!/usr/bin/env python3
"""Review controls on isolated nonprimary copies; no rendering or GAP execution."""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--base', type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument('--output-dir', type=Path, required=True)
    a = ap.parse_args()
    out = a.output_dir.absolute()
    require(not os.path.lexists(out), 'Fresh output directory required')
    manifest_path = a.base / 'phase98_twelve_measurement_manifest.json'
    require(digest(manifest_path) == '7477a91be128f4c0fb953e4a7f4b9d422bd70a371367de1fcee2db0cd59b229d', 'Author freeze changed')
    m = json.loads(manifest_path.read_text())
    bindings = dict(m['files'])
    bindings.update(m['retained_nonprimary_inputs'])
    bindings[manifest_path.name] = {'sha256': digest(manifest_path)}
    require(all(not n.startswith('sources/') and '_sources/' not in n for n in bindings), 'Primary asset in portable tree')
    out.mkdir()
    tree = out / 'portable-nonprimary'
    tree.mkdir()
    for name, b in bindings.items():
        src, dst = a.base / name, tree / name
        require(digest(src) == b['sha256'], 'Bad input: ' + name)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
    counter = a.base / 'phase103_twelve_measurement_review_count.py'
    shutil.copyfile(counter, tree / counter.name)
    command = [sys.executable, '-O', str(tree / counter.name), '--base', str(tree), '--replacement-only']
    def invoke(target):
        return subprocess.run(command + ['--output', str(target)], text=True, capture_output=True)
    good = out / 'portable-count.json'
    result = invoke(good)
    (out / 'portable.stdout.txt').write_text(result.stdout)
    (out / 'portable.stderr.txt').write_text(result.stderr)
    require(result.returncode == 0 and json.loads(good.read_text())['status'] == 'PASS', 'Isolated replacement verification failed')
    controls = []
    good_sha = digest(good)
    for label in ['file', 'directory', 'dangling-symlink']:
        target = good if label == 'file' else out / label
        if label == 'directory':
            target.mkdir()
        elif label == 'dangling-symlink':
            target.symlink_to(out / 'absent-target')
        result = invoke(target)
        require(result.returncode != 0 and 'Output exists' in result.stderr, 'Output refusal failed: ' + label)
        require(digest(good) == good_sha, 'Existing result changed')
        if label == 'directory':
            require(list(target.iterdir()) == [], 'Existing directory changed')
        elif label == 'dangling-symlink':
            require(target.is_symlink() and not target.exists(), 'Dangling link changed')
        controls.append({'case': label, 'rejected': True, 'returncode': result.returncode, 'stderr': result.stderr})
    mutations = [
        ('protocol', 'phase98_twelve_measurement_protocol.json'),
        ('manuscript', 'phase78_n009_integration_manuscript.md'),
        ('data', 'phase78_n009_integration_data.g'),
        ('rendered-pdf', 'phase98_twelve_measurement_render/replacement.pdf'),
        ('last-page-raster', 'phase98_twelve_measurement_render/page-83.png'),
    ]
    for label, name in mutations:
        target = tree / name
        original = target.read_bytes()
        target.write_bytes(original + b'\nINDEPENDENT_REVIEW_MUTATION\n')
        output = out / ('rejected-' + label + '.json')
        result = invoke(output)
        require(result.returncode != 0 and 'Hash mismatch' in result.stderr, 'Mutation refusal failed: ' + label)
        require(not os.path.lexists(output), 'Mutation created result')
        target.write_bytes(original)
        controls.append({'case': label, 'input': name, 'rejected': True, 'returncode': result.returncode, 'output_created': False, 'stderr': result.stderr})
    for name, b in bindings.items():
        require(digest(tree / name) == b['sha256'] == digest(a.base / name), 'Input changed: ' + name)
    report = {'status': 'PASS', 'portable_nonprimary_files': len(bindings),
        'portable_full_replacement_recount': True, 'private_source_assets_in_snapshot': False,
        'all_original_and_copied_inputs_unchanged': True, 'no_clobber_cases': 3,
        'mutation_cases': 5, 'controls': controls,
        'counter_sha256': digest(counter), 'portable_result_sha256': digest(good),
        'scope': 'Own independent counter; portable nonprimary replacement-only mode. Complete source recount is a separate private-input run. No proof or GAP replay.'}
    (out / 'controls.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'portable_nonprimary_files': len(bindings), 'no_clobber_cases': 3, 'mutation_cases': 5}))


if __name__ == '__main__':
    main()
