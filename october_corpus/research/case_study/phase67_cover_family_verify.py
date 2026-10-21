#!/usr/bin/env python3
"""Replay eight reviewed cover-family diagnostics with stock GAP in fresh output.

Only the distributed program, theorem and review are required. The all-parameter
theorem is a written proof; this runner checks eight exact finite cases.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import subprocess
import time

BOUND = {
    'phase49_cover_family_check.g': '999a878716810ab4ce476ea2a45c6986d36ef9530a7d02ef3a3871074dab3cfe',
    'phase49_cover_family_theorem.md': '769ddbf891597c3c0d6246ad3f93b354dd02226e02d90cff1eaa250b7bbd4725',
    'phase59_cover_family_recent_audit.json': 'efb1466200ba01263dba5532cee6c64379128088d104314208cb4181fb9a82c6',
}
LOG_SHA = 'e89d679dc4de9be0c049002235ccee4bef8548ef7ac3c8ab2197a584e8f77a77'
PARAMETERS = [(3, 2, 1), (3, 2, 2), (3, 3, 1), (3, 3, 2)] + [(5, 2, k) for k in range(1, 5)]


def digest(data):
    return sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--gap', default='gap')
    parser.add_argument('--timeout', type=float, default=900)
    args = parser.parse_args()
    output = args.output_dir.absolute()
    if output.exists() or output.is_symlink():
        parser.error('output path exists; refusing to overwrite')
    if args.timeout <= 0:
        parser.error('timeout must be positive')
    for name, expected in BOUND.items():
        if digest((args.input_root / name).read_bytes()) != expected:
            raise ValueError('Reviewed input changed: ' + name)
    gap = shutil.which(args.gap)
    if gap is None:
        raise RuntimeError('Stock GAP executable unavailable')
    output.mkdir(parents=True, exist_ok=False)
    local = output / 'certificate.g'
    local.write_bytes((args.input_root / 'phase49_cover_family_check.g').read_bytes())
    command = [gap, '-q', local.name]
    started = time.monotonic()
    timed_out = False
    try:
        run = subprocess.run(command, cwd=output, capture_output=True, timeout=args.timeout)
        stdout, stderr, exit_code = run.stdout, run.stderr, run.returncode
    except subprocess.TimeoutExpired as exc:
        stdout, stderr, exit_code = exc.stdout or b'', exc.stderr or b'', None
        timed_out = True
    seconds = time.monotonic() - started
    (output / 'stdout.log').write_bytes(stdout)
    (output / 'stderr.log').write_bytes(stderr)
    canonical = stdout.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')
    (output / 'canonical_stdout.log').write_text(canonical)
    flat = re.sub(r'\s+', ' ', canonical.replace('\\\n', ''))
    rows = re.findall(r'PARAM_PASS \[ (\d+), (\d+), (\d+) \] orders \[ ([\d, ]+) \]', flat)
    parameters = [tuple(map(int, row[:3])) for row in rows]
    cases, valid_orders = [], True
    for row in rows:
        p, alpha, k = map(int, row[:3])
        q = p ** alpha
        orders = list(map(int, row[3].replace(' ', '').split(',')))
        expected = [4*p*p*q, 4*p**3*q, 4*p*p*q, 4*p**4*q, 4*p**4*q, 4*p**5*q]
        valid_orders = valid_orders and orders == expected
        cases.append(dict(p=p, alpha=alpha, k=k, orders_P_R_T_Q_Qdual_H=orders))
    version = re.search(r'PASS GAP (\S+) eight exact finite diagnostics; all-parameter theorem is written', flat)
    unchanged = all(digest((args.input_root / name).read_bytes()) == expected for name, expected in BOUND.items())
    unchanged = unchanged and digest(local.read_bytes()) == BOUND['phase49_cover_family_check.g']
    passed = (not timed_out and exit_code == 0 and not stderr and parameters == PARAMETERS
              and valid_orders and version is not None and version.group(1) == '4.15.1'
              and digest(canonical.encode()) == LOG_SHA and unchanged
              and not re.search(r'FAIL|Error,|Syntax error', canonical))
    report = {
        'date': '2026-10-10', 'status': 'PASS' if passed else 'FAIL',
        'command': command, 'exit_code': exit_code, 'timed_out': timed_out,
        'elapsed_seconds': seconds, 'runner_sha256': digest(Path(__file__).read_bytes()),
        'GAP_version': version.group(1) if version else None,
        'bound_inputs': BOUND, 'all_bound_inputs_and_executed_copy_unchanged': unchanged,
        'stdout_sha256': digest(stdout), 'stderr_sha256': digest(stderr),
        'canonical_stdout_sha256': digest(canonical.encode()),
        'canonicalization': 'UTF-8 decode; only CRLF and bare CR converted to LF, matching the original text-mode run.',
        'exact_previous_log_match': digest(canonical.encode()) == LOG_SHA,
        'cases': cases,
        'scope': 'Eight exact finite diagnostics from bare presentations. The all-parameter result relies on the separately reviewed written proof.',
        'retained_computational_input': 'Stock GAP 4.15.1 exact finite-presentation and permutation-group algorithms; no source catalogue or primary capture is needed by this runner.',
        'new_Lean_build': False, 'historical_priority_claim': False,
        'general_conjecture_claim': False,
    }
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if passed else 1)


if __name__ == '__main__':
    main()
