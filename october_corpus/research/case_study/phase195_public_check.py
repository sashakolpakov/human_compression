#!/usr/bin/env python3
"""Public replay of the reviewed phase187 gluing contract (phase195 adapter).

The independent GAP source neither imports the author Python program nor reads
its output. Only after both finish does this driver compare their invariants.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--gap', type=Path, default=Path('/opt/homebrew/bin/gap'))
    parser.add_argument('--lean', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    out = args.output_dir.absolute()
    require(not out.exists() and not out.is_symlink(), 'fresh output directory required')
    out.mkdir(parents=True)
    manifest = root / 'phase187_manifest.json'
    require(sha(manifest) == '5506e0c10b748e74c3554fbcfb29e0c7d1ea6f5bd103204cfd8ffd0c1426189d',
            'author freeze identity changed')
    # The historical freeze also binds primary PDFs, unrelated screening notes
    # and compiled artifacts. Public replay needs only these distributed inputs.
    names = {'phase187_parallel_gluing.md', 'phase187_parallel_gluing_check.py',
             'phase187_run.py', 'phase187_formal/SimultaneousMatching.lean',
             'phase187_author_replay/replay.json', 'phase138_umbrella_v3.md'}
    bindings = [b for b in json.loads(manifest.read_text())['bindings']
                if b['path'] in names]
    require({b['path'] for b in bindings} == names, 'public binding set changed')
    fixed = {
        'phase191_independent_gluing.g':
            '0965e2a54146b21ac53822ac497d0879e0a7478bf4f490a393d71fbae566f0df',
        'phase191_parallel_gluing_review.md':
            'de1298ede87bcf566055b1cf654bbbf068ed66ec2a1753370ffa80e34c84fa01',
        'phase191_source_contract.json':
            'f1ff5de32eb4e40c1a1f5f89d1fa86b4db8ddc16ab0eb287c4659d2515465e19',
    }
    for name, expected in fixed.items():
        require(sha(root / name) == expected, 'review input changed: ' + name)
    gap_version = subprocess.run([str(args.gap.absolute()), '-q', '-b'],
        input='Print(GAPInfo.Version, "\\n"); QUIT_GAP(0);\n',
        capture_output=True, text=True, check=True, timeout=30).stdout.strip()
    require(gap_version == '4.15.1', 'reviewed GAP version required')
    for binding in bindings:
        path = root / binding['path']
        require(sha(path) == binding['sha256'] and path.stat().st_size == binding['bytes'],
                'author binding mismatch: ' + binding['path'])
    independent = root / 'phase191_independent_gluing.g'
    reviewer_binding = sha(independent)
    environment = dict(os.environ)
    environment.pop('PYTHONOPTIMIZE', None)
    r = subprocess.run([sys.executable, '-B', str(root / 'phase187_run.py'),
                        '--output-dir', str(out / 'author'), '--lean', str(args.lean.absolute())],
                       capture_output=True, text=True, cwd=root, env=environment, timeout=180)
    (out / 'author_driver.log').write_text(r.stdout + r.stderr)
    require(r.returncode == 0 and 'PHASE187_REPLAY_PASS' in r.stdout,
            'fresh author replay failed')
    author = json.loads((out / 'author/replay.json').read_text())
    require(sha(out / 'author/replay.json') == sha(root / 'phase187_author_replay/replay.json'),
            'fresh author replay differs from bound author output')
    scenarios = [
        ('native', None, None, None),
        ('reverse_matching_composition', 'beta := [(),s,t*a];;', 'beta := [(),s,a*t];;',
         'literal common lift cosets'),
        ('omit_point_line_incidences', 'for u in lines[q][j] do',
         'for u in Difference(lines[q][j],[1]) do', 'residual connectivity'),
    ]
    controls = []
    native = None
    for name, old, new, rejection in scenarios:
        text = independent.read_text()
        if old is not None:
            require(text.count(old) == 1, 'nonunique mutation anchor: ' + name)
            text = text.replace(old, new)
        staged = out / (name + '.g')
        staged.write_text(text)
        if old is None:
            require(sha(staged) == reviewer_binding, 'native stage changed')
        r = subprocess.run([str(args.gap.absolute()), '-q', '-b', str(staged)],
                           capture_output=True, text=True, cwd=out, timeout=120)
        log = r.stdout + r.stderr
        (out / (name + '.log')).write_text(log)
        if rejection:
            require(r.returncode != 0 and 'PHASE191_REJECT: ' + rejection in log
                    and 'PHASE191_NATIVE_GAP_PASS' not in log,
                    'negative control did not fail closed: ' + name)
            controls.append({'name': name, 'rejected': True, 'reason': rejection})
        else:
            require(r.returncode == 0 and 'PHASE191_NATIVE_GAP_PASS' in log
                    and 'Error,' not in log and 'Syntax warning' not in log,
                    'native GAP reconstruction failed')
            native = json.loads(log.split('PHASE191_JSON_BEGIN\n', 1)[1].split(
                '\nPHASE191_JSON_END', 1)[0])
    for label in ('alpha', 'beta'):
        expected = author['geometry']['gluing_' + label]
        actual = native[label]
        require(actual['object_counts'] == expected['object_counts'], 'object census differs')
        require(actual['line_counts'] == [expected['line_counts_by_direction'][str(i)]
                                         for i in range(4)], 'direction census differs')
        require(actual['flag_counts'] == expected['flag_counts'], 'flag census differs')
        require(actual['connected_by_flag_size'] ==
                [expected['connected_residues_by_rank'][str(r)] for r in (4, 3, 2)],
                'residue census differs')
        require(actual['panel_counts'] == [[int(k), v] for k, v in sorted(
            expected['panel_completion_distribution'].items(), key=lambda item: int(item[0]))],
            'panel distribution differs')
    require(sha(independent) == reviewer_binding, 'reviewer source changed during replay')
    for binding in bindings:
        require(sha(root / binding['path']) == binding['sha256'], 'author input changed during replay')
    for name, expected in fixed.items():
        require(sha(root / name) == expected, 'review input changed during replay')
    report = {
        'status': 'PASS',
        'public_adapter': 'phase195',
        'GAP_version': gap_version,
        'reviewed_input_hashes': fixed,
        'primary_PDFs_required_for_execution': False,
        'author_manifest_sha256': sha(manifest),
        'verified_author_bindings': len(bindings),
        'reviewer_GAP_sha256': reviewer_binding,
        'author_replay_byte_identical': True,
        'independent_native_GAP': native,
        'reviewer_negative_controls': controls,
        'author_negative_controls': author['negative_controls'],
        'Lean': author['Lean'],
        'source_lemma_literal_counterexample': True,
        'positive_written_theorem_requires_human_review': True,
        'full_geometric_Lean_certificate': False,
        'whole_source_principal_credit': 0,
        'open_conjecture_credit': 0,
        'priority_claim': False,
    }
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print('PHASE195_PUBLIC_REPLAY_PASS', sha(out / 'report.json'))


if __name__ == '__main__':
    main()
