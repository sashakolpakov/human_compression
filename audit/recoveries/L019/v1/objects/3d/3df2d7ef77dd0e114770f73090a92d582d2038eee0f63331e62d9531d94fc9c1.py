"""Replay the finite ten-point component, with explicit failure receipts."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):
    raise RuntimeError('normal Python required')
HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--study', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--render', action='store_true')
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    deps = json.loads((HERE / 'dependencies.json').read_text())
    exports = json.loads((HERE / 'manifest.json').read_text())['exports']
    for base, rows in [(HERE, exports), (args.study, deps)]:
        for row in rows:
            path = base / row['path']
            data = path.read_bytes()
            need(len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'], 'binding ' + str(path))
    env = os.environ.copy()
    env.pop('PYTHONOPTIMIZE', None)
    receipts = []

    def run(name, command, cwd=out, negative=False, chosen_env=env):
        start = time.monotonic()
        try:
            result = subprocess.run(command, cwd=cwd, env=chosen_env, capture_output=True, timeout=45)
        except subprocess.TimeoutExpired as exc:
            (out / (name + '.stdout')).write_bytes(exc.stdout or b'')
            (out / (name + '.stderr')).write_bytes(exc.stderr or b'')
            (out / (name + '_timeout.json')).write_text(json.dumps({'status': 'TIMEOUT_NO_CERTIFICATE', 'cap_seconds': 45}) + '\n')
            raise
        (out / (name + '.stdout')).write_bytes(result.stdout)
        (out / (name + '.stderr')).write_bytes(result.stderr)
        receipts.append({'name': name, 'command': command, 'returncode': result.returncode,
                         'seconds': time.monotonic() - start, 'cap_seconds': 45})
        (out / 'receipts.json').write_text(json.dumps(receipts, indent=2) + '\n')
        if negative:
            need(result.returncode != 0 and b'normal Python required' in result.stderr, 'guard ' + name)
        else:
            need(result.returncode == 0 and not result.stderr, 'execution ' + name)
        return result.stdout.decode().replace('\r', '')

    text = run('census', ['/opt/homebrew/bin/gap', '-q', '-T', str(HERE / 'enumerate.g')])
    need(text == (HERE / 'stdout.log').read_bytes().decode().replace('\r', ''), 'exact complete census')
    need(text.count('COMPLETE_FRACTURED_CRITICAL_SYMMETRIC|') == 1 and
         text.count('TERMINAL_GROUPS|') == 1 and 'SOLUTION|' not in text, 'completion and negative result')
    positive = run('positive', ['/opt/homebrew/bin/gap', '-q', '-T', str(HERE / 'positive.g')])
    need(positive.strip() == 'PASS_PURE_FIRST_POSITIVE|3628800|6|2080_subset_pairs', 'positive marking')
    run('small', [sys.executable, str(HERE / 'small_controls.py'), '--out', str(out / 'small.json')])
    need(json.loads((out / 'small.json').read_text()) == json.loads((HERE / 'small_controls.json').read_text()), 'literal small controls')
    run('reject_argument', [sys.executable, '-O', str(HERE / 'check.py')], negative=True)
    badenv = dict(env, PYTHONOPTIMIZE='1')
    run('reject_environment', [sys.executable, str(HERE / 'check.py')], negative=True, chosen_env=badenv)
    if args.render:
        shutil.copy2(HERE / 'degree_ten.tex', out / 'degree_ten.tex')
        for i in [1, 2]:
            run('native' + str(i), ['/opt/homebrew/bin/pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'degree_ten.tex'])
        log = (out / 'degree_ten.log').read_text()
        need('Overfull' not in log and 'LaTeX Warning:' not in log, 'native content')
    report = {'status': 'PASS_TEN_POINT_SYMMETRIC_COMPONENT', 'exports': len(exports),
              'dependencies': len(deps), 'all_involutions': 9495, 'anchor_fixing_involutions': 2619,
              'nodes': [1, 4, 197, 1775, 645, 208, 18], 'S10_nonpure_candidates': 0,
              'terminal_full_subset_oracles': 18, 'positive_control': True,
              'small_literal_subset_intersections': 16587, 'optimization_guards': 2,
              'whole_original_credit': 0, 'new_Lean': 0}
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
