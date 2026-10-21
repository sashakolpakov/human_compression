"""Verify exact review closure; optionally repeat the independent small control."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Use ordinary Python')
sys.dont_write_bytecode = True
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess

P = Path(__file__).resolve().parent

def need(ok, why):
    if not ok:
        raise ValueError(why)

def pin(path):
    b = path.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--study', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--replay-independent', action='store_true')
    a = ap.parse_args()
    s, out = a.study.resolve(), a.out.resolve()
    need(not out.exists(), 'Fresh output required')
    m = json.loads((P/'manifest.json').read_text())
    for row in m['exports']:
        need(pin(P/row['path']) == {k: row[k] for k in ('bytes','sha256')}, 'Exact export')
    dependencies = json.loads((P/'dependencies.json').read_text())
    for row in dependencies:
        need(pin(s/row['path']) == {k: row[k] for k in ('bytes','sha256')}, 'Exact dependency '+row['path'])
    r = json.loads((P/'review.json').read_text())
    need(r['status'] == 'ACCEPTED_L114_COMPATIBLE_TORI_COMPONENT', 'Review status')
    need(r['author_manifest']['sha256'] == 'fb18e3f0f489141c4728e115eb576cb019c4c0bae8fa9d4fb187eef9d473cf26', 'Reviewed edition')
    need(json.loads((P/'fresh_report.json').read_text())['status'] == 'PASS_L114_COMPATIBLE_TORI_NOTE', 'Fresh author checker')
    need(json.loads((P/'independent_report.json').read_text())['status'] == 'PASS', 'Independent terminal control')
    need(not (P/'independent.stderr').read_bytes(), 'Clean independent stderr')
    need((P/'independent.stdout').read_bytes().rstrip().endswith(b'PASS_INDEPENDENT_L114_WITNESS'), 'Complete independent control')
    out.mkdir(parents=True)
    replay = None
    if a.replay_independent:
        env = dict(os.environ)
        env.pop('PYTHONOPTIMIZE', None)
        cmd = ['/opt/homebrew/bin/gap','-q','-b',str(P/'independent_witness.g')]
        try:
            c = subprocess.run(cmd, env=env, capture_output=True, timeout=60)
        except subprocess.TimeoutExpired as e:
            (out/'independent.stdout').write_bytes(e.stdout or b'')
            (out/'independent.stderr').write_bytes(e.stderr or b'')
            raise
        (out/'independent.stdout').write_bytes(c.stdout)
        (out/'independent.stderr').write_bytes(c.stderr)
        need(c.returncode == 0 and not c.stderr and c.stdout == (P/'independent.stdout').read_bytes(), 'Independent replay exact output')
        replay = {'command': cmd, 'exit_code': c.returncode, 'stdout': pin(out/'independent.stdout')}
    report = {'status': 'PASS_L114_DISTINCT_REVIEW_CLOSURE', 'exports': len(m['exports']),
              'dependencies': len(dependencies), 'independent_replay': replay,
              'mathematical_proof_verified_by_program': False, 'whole_original_credit': 0}
    (out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))

if __name__ == '__main__':
    main()
