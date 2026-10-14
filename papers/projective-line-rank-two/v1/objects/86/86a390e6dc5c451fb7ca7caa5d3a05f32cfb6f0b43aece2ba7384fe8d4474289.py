"""Exact review closure; the general mathematics remains a written review."""
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
        need(pin(P/row['path']) == {k: row[k] for k in ('bytes','sha256')}, 'Exact export '+row['path'])
    dependencies = json.loads((P/'dependencies.json').read_text())
    for row in dependencies:
        need(pin(s/row['path']) == {k: row[k] for k in ('bytes','sha256')}, 'Exact dependency '+row['path'])
    r = json.loads((P/'review.json').read_text())
    need(r['status'] == 'ACCEPTED_L076_PROJECTIVE_LINE_CLASSIFICATION', 'Review status')
    need(r['author_manifest']['sha256'] == '87504d5ba922c8a79ca7312203b717d34cbda001ece95437d677d892e8b8653d', 'Reviewed edition')
    fresh = json.loads((P/'fresh_report.json').read_text())
    need(fresh['status'] == 'PASS_L076_CLASSIFICATION_COMPONENT', 'Fresh checker completed')
    need((fresh['finite_fields'],fresh['torus_cases'],fresh['geometry_representatives']) == (14,28,19), 'Complete finite inventory')
    need(fresh['native'] == {'pages':6,'text_identical':True}, 'Native consistency')
    old = json.loads((P/'independent_report.json').read_text())
    need(old['status'] == 'PASS_INDEPENDENT_L076_GLOBAL_ORBITS_AND_MODELS', 'Independent controls')
    source = s/r['independent_input']['path']
    need(pin(source) == {k:r['independent_input'][k] for k in ('bytes','sha256')}, 'Exact independent input')
    need(old['input_sha256'] == pin(source)['sha256'], 'Independent input bridge')
    need(not (source.parent/'finite.stderr').read_bytes(), 'Clean finite stderr')
    need(source.read_bytes().rstrip().endswith(b'PASS_COMPLETE_L076_FINITE_CLASSIFICATION'), 'Complete finite marker')
    out.mkdir(parents=True)
    replay = None
    if a.replay_independent:
        env = dict(os.environ)
        env.pop('PYTHONOPTIMIZE', None)
        cmd = [sys.executable,'-B',str(P/'independent.py'),'--input',str(source),'--out',str(out/'independent.json')]
        try:
            c = subprocess.run(cmd, env=env, capture_output=True, timeout=90)
        except subprocess.TimeoutExpired as e:
            (out/'independent.stdout').write_bytes(e.stdout or b'')
            (out/'independent.stderr').write_bytes(e.stderr or b'')
            raise
        (out/'independent.stdout').write_bytes(c.stdout)
        (out/'independent.stderr').write_bytes(c.stderr)
        need(c.returncode == 0 and not c.stderr, 'Clean independent replay')
        need(json.loads((out/'independent.json').read_text()) == old, 'Exact independent semantic result')
        replay = {'command': cmd, 'exit_code': c.returncode, 'report': pin(out/'independent.json')}
    report = {'status':'PASS_L076_DISTINCT_REVIEW_CLOSURE','exports':len(m['exports']),
              'dependencies':len(dependencies),'independent_replay':replay,
              'mathematical_proof_verified_by_program':False,'whole_original_credit':0}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__ == '__main__':
    main()
