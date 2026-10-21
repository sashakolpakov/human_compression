#!/usr/bin/env python3
"""Isolated controls for the additive phase116 ledger correction."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
P = 'phase110_commuting_pairs_integration_'
PROGRAM = 'phase116_commuting_pairs_correction.py'
LEDGER = 'phase116_commuting_pairs_corrected_ledger.json'


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-dir', type=Path, required=True)
    args = ap.parse_args()
    need(not os.path.lexists(args.output_dir), 'Fresh controls output required')
    args.output_dir.mkdir(parents=True)
    manifest = json.loads((ROOT / (P + 'manifest.json')).read_text())
    intake = json.loads((ROOT / (P + 'intake.json')).read_text())
    names = set(manifest['export_allowlist']) | {r['path'] for r in intake['retained_input_bindings']}
    names |= {PROGRAM, LEDGER}
    snap = args.output_dir / 'public-inputs'
    snap.mkdir()
    for name in sorted(names):
        need(not name.startswith('sources/') and not name.endswith(('.pdf', '.png')), 'Primary file in copy')
        target = snap / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    before = {n: sha(snap / n) for n in names}

    def run(*arguments):
        return subprocess.run([sys.executable, '-B', '-O', str((snap / PROGRAM).resolve()), *map(str, arguments)],
                              cwd=args.output_dir.parent, capture_output=True, text=True)

    successful = args.output_dir / 'fresh.json'
    fresh = run('--output', successful)
    need(fresh.returncode == 0, 'Public-only replay failed: ' + fresh.stderr)
    successful_hash = sha(successful)
    text = (snap / (P + 'manuscript.md')).read_text()
    ledger = json.loads((snap / LEDGER).read_text())
    cases = []
    original = snap / (P + 'ledger.json')
    for name, data in [('original_truncated_ledger', original.read_bytes()),
                       ('single_hash', None), ('missing_exception_body', None)]:
        if data is None:
            damaged = copy.deepcopy(ledger)
            row = next(r for r in damaged['contracts'] if r['integration_id'] == 'L066.1')
            span = row['integrated_proof_span']
            end = span['start_codepoint'] + 1 if name == 'single_hash' else text.index('### 25.3.') + 1
            span['end_codepoint_exclusive'] = end
            span['sha256_utf8'] = hashlib.sha256(text[span['start_codepoint']:end].encode()).hexdigest()
            data = (json.dumps(damaged, indent=2, ensure_ascii=False) + '\n').encode()
        candidate = args.output_dir / (name + '.json')
        candidate.write_bytes(data)
        output = args.output_dir / (name + '-result.json')
        result = run('--expected-ledger', candidate, '--output', output)
        need(result.returncode != 0 and 'Corrected proof ledger mismatch' in result.stderr
             and not os.path.lexists(output), 'Bad span accepted: ' + name)
        cases.append(dict(name=name, rejected=True, output_absent=True,
                          internal_span_hashes_consistent=True))
    occupied_file = args.output_dir / 'occupied-file'
    occupied_file.write_text('preserve\n')
    occupied_dir = args.output_dir / 'occupied-directory'
    occupied_dir.mkdir()
    occupied_link = args.output_dir / 'occupied-link'
    occupied_link.symlink_to(args.output_dir / 'absent')
    refusals = []
    for mode in ['--output', '--build-dir']:
        for kind, path in [('file', occupied_file), ('directory', occupied_dir), ('dangling_symlink', occupied_link)]:
            result = run(mode, path)
            need(result.returncode != 0 and 'Fresh output required' in result.stderr, 'Occupied output accepted')
            refusals.append(dict(mode=mode, kind=kind))
    need(before == {n: sha(snap / n) for n in names}, 'Copied inputs changed')
    need(sha(successful) == successful_hash and occupied_file.read_text() == 'preserve\n'
         and occupied_link.is_symlink() and list(occupied_dir.iterdir()) == [], 'Output changed')
    report = dict(status='PASS', public_only_replay=True, copied_inputs=before,
                  arithmetic_or_mathematical_review=False, primary_assets_copied=False,
                  negative_controls=cases, no_clobber=refusals,
                  successful_report_sha256=successful_hash, all_inputs_and_successful_outputs_unchanged=True,
                  program_sha256=sha(ROOT / PROGRAM), controls_sha256=sha(Path(__file__)))
    (args.output_dir / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status='PASS', public_files=len(names), rejected_ledgers=len(cases), no_clobber=len(refusals))))


if __name__ == '__main__':
    main()
