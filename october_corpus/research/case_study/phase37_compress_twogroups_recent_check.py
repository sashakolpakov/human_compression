"""Independent runner and output validation for the charged order-256 census.

It executes the author's unchanged GAP program in a temporary working directory.
The finite classification still retains GAP and SmallGroups; this is not an
independent group-arithmetic implementation or an all-parameter proof.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import time


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    p.add_argument('--gap', default=shutil.which('gap'))
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--log', type=Path, required=True)
    a = p.parse_args()
    if not a.gap:
        p.error('GAP is required')
    if a.output.exists() or a.log.exists():
        p.error('output or log already exists')
    script = a.root.resolve() / 'phase37_compress_twogroups_census.g'
    initial = sha(script.read_bytes())
    assert initial == '0a1e993362b263c9ef23e8fca5103c3a2b766a937a2f9af7608fbca8252d2752'
    start = time.monotonic()
    with tempfile.TemporaryDirectory(prefix='compress_B_review_') as scratch:
        result = subprocess.run([a.gap, '-q', str(script)], cwd=scratch,
                                capture_output=True, text=True, timeout=300)
    elapsed = time.monotonic() - start
    assert sha(script.read_bytes()) == initial, 'author source changed during execution'
    assert result.returncode == 0, (result.returncode, result.stderr)
    assert not result.stderr.strip(), result.stderr
    assert not re.search(r'UNEXPECTED|Error,|Syntax error', result.stdout)
    header = re.search(r'GAP (\S+) SmallGroups (\S+) eligible_groups=(\d+)', result.stdout)
    assert header
    counts = re.search(r'PASS groups=(\d+) active=(\d+) triples=(\d+)\s+pattern_counts=\[\s*(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\s*\]', result.stdout)
    assert counts
    values = list(map(int, counts.groups()))
    assert values == [1651, 1641, 92, 64, 4, 16, 8], values
    hits = re.findall(r'HIT \[\s*256,\s*(\d+)\s*\] patterns=\[\s*([^\]]+)\]', result.stdout)
    hits = [(int(g), list(map(int, re.findall(r'\d+', patterns)))) for g, patterns in hits]
    assert hits == [(5078, [1]), (6661, [3]), (6665, [2, 4])], hits
    cpu = re.findall(r'ms=(\d+)', result.stdout)
    with a.log.open('x') as f:
        f.write(result.stdout)
    report = {
        'date': '2026-10-10', 'status': 'PASS',
        'scope': 'Fresh unchanged author census execution plus independent exact output assertions. GAP/SmallGroups arithmetic and catalogue completeness retained.',
        'review_runner_sha256': sha(Path(__file__).read_bytes()),
        'executed_script': script.name, 'executed_script_sha256': initial,
        'executed_source_unchanged': True, 'exit_code': result.returncode,
        'GAP_version': header.group(1), 'SmallGroups_version': header.group(2),
        'eligible_groups': values[0], 'active_groups': values[1],
        'anchored_valid_triples': values[2], 'pattern_counts': values[3:],
        'group_pattern_hits': hits,
        'wall_seconds': elapsed, 'author_cpu_ms': int(cpu[-1]),
        'log_filename': a.log.name, 'log_sha256': sha(a.log.read_bytes()),
        'working_directory': 'disposable temporary directory',
        'historical_and_author_reports_overwritten': False,
        'all_parameter_classification_verified_by_this_execution': False,
    }
    with a.output.open('x') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(json.dumps({k: report[k] for k in ['status', 'eligible_groups', 'anchored_valid_triples', 'pattern_counts', 'wall_seconds']}))


if __name__ == '__main__':
    main()
