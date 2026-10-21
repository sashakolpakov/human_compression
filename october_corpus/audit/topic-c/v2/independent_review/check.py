#!/usr/bin/env python3
"""Replay the independent review's bindings and finite interface controls.

The default does not recompile Lean or repeat the full Janko census. Use --full
to request the author packet's complete fresh render/formal/census replay too.
The mathematical review remains a written human-readable artifact.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def bind(base, row):
    path = base / row['path']
    data = path.read_bytes()
    need(len(data) == row['bytes'] and sha(data) == row['sha256'],
         'Changed bound artifact: ' + str(path))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--author-root', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--study-root', type=Path)
    parser.add_argument('--public-root', type=Path)
    parser.add_argument('--full', action='store_true')
    args = parser.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(), 'Use a fresh output path')
    out = args.out.resolve()
    out.mkdir(parents=True)
    record = json.loads((ROOT / 'review.json').read_text())
    bind(args.author_root, record['author_manifest'])
    manifest = json.loads((args.author_root / record['author_manifest']['path']).read_text())
    for row in manifest['exports']:
        bind(args.author_root, row)
    for row in record['review_exports_before_freeze']:
        bind(ROOT, row)

    # An independent transcription of the forty-row boundary. Repeated proof
    # references are checked as bindings, not interpreted as exclusive costs.
    scope = json.loads((args.author_root / 'scope.json').read_text())
    expected = {f'{prefix}{i}' for prefix, count in [('J', 11), ('N', 16), ('P', 8), ('F', 5)]
                for i in range(1, count + 1)}
    rows = scope['source_result_rows']
    need(len(rows) == 40 and {r['id'] for r in rows} == expected, 'Changed historical contract')
    by_id = {r['id']: r for r in rows}
    need(all(by_id[k]['coverage'] == 'excluded_auxiliary' for k in ['N14', 'N15']), 'Lost exclusion')
    need(all(by_id[k]['coverage'] == 'corrected_or_qualified_assertion'
             for k in ['J10', 'N13', 'P4', 'P7', 'P8']), 'Lost literal correction')
    need(by_id['J9']['required_programs'] == ['program.construction', 'program.census'],
         'Census proof program omitted')
    checked_spans = 0
    for region in list(scope['proof_regions'].values()) + [
            item['binding'] for item in scope['proof_statements_and_context'].values()]:
        text = (args.author_root / region['file']).read_text()
        a, b = region['start_char'], region['end_char']
        need(0 <= a < b <= len(text), 'Invalid theorem span')
        raw = text[a:b].encode()
        need(len(raw) == region['bytes'] and sha(raw) == region['sha256'], 'Changed theorem span')
        need(text[:a].count('\n') + 1 == region['start_line'] and
             text[:b].count('\n') + 1 == region['end_line'], 'Changed theorem locator')
        checked_spans += 1
    sources_checked = 0
    if args.study_root:
        for item in record['primary_sources_read']:
            bind(args.study_root, item['binding'])
            sources_checked += 1

    env = dict(os.environ)
    for name in ['PYTHONOPTIMIZE', 'LEAN_PATH', 'LEAN_SRC_PATH']:
        env.pop(name, None)
    proc = subprocess.run([sys.executable, '-B', '-E', ROOT / 'recognition_controls.py',
                           '--out', out / 'interface_controls'],
                          env=env, text=True, capture_output=True)
    (out / 'interface_controls.log').write_text(proc.stdout + proc.stderr)
    need(proc.returncode == 0, 'Independent interface controls failed')
    full_report = None
    if args.full:
        command = [sys.executable, '-B', '-E', args.author_root / 'check.py',
                   '--out', out / 'full_author_replay', '--render', '--formal', '--census']
        if args.study_root:
            command += ['--study-root', args.study_root]
        if args.public_root:
            command += ['--public-root', args.public_root]
        proc = subprocess.run(command, env=env, capture_output=True, text=True)
        (out / 'full_author_replay.log').write_text(proc.stdout + proc.stderr)
        need(proc.returncode == 0, 'Full fresh author replay failed')
        full_report = json.loads((out / 'full_author_replay' / 'report.json').read_text())
        need(full_report['fresh_scoped_formal'] and full_report['fresh_Janko_census'],
             'Incomplete full replay')
    report = dict(status='PASS', author_exports=len(manifest['exports']),
                  historical_contract_rows=40, proof_spans=checked_spans,
                  primary_bindings_checked=sources_checked,
                  fresh_independent_interface_controls=True,
                  fresh_formal_render_and_census=args.full,
                  full_replay=full_report,
                  mathematical_acceptance='See the bound independent written review; not inferred from this script.',
                  source_credit_increment=0, question_credit_increment=0, ratio=None)
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k:v for k,v in report.items() if k != 'full_replay'}))


if __name__ == '__main__':
    main()
