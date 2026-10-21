"""Integrity and native replay for a uniform mathematical component."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):
    raise RuntimeError('normal Python required')
HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--study', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--render', action='store_true')
    a = p.parse_args()
    out = a.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    exports = json.loads((HERE / 'manifest.json').read_text())['exports']
    deps = json.loads((HERE / 'dependencies.json').read_text())
    for base, rows in [(HERE, exports), (a.study, deps)]:
        for row in rows:
            path = base / row['path']
            data = path.read_bytes()
            need(len(data) == row['bytes'] and
                 hashlib.sha256(data).hexdigest() == row['sha256'],
                 'binding ' + str(path))
    env = os.environ.copy()
    env.pop('PYTHONOPTIMIZE', None)
    for name, command, childenv in [
        ('argument', [sys.executable, '-O', str(HERE / 'check.py')], env),
        ('environment', [sys.executable, str(HERE / 'check.py')], dict(env, PYTHONOPTIMIZE='1')),
    ]:
        r = subprocess.run(command, capture_output=True, env=childenv, timeout=15)
        (out / ('guard_' + name + '.stdout')).write_bytes(r.stdout)
        (out / ('guard_' + name + '.stderr')).write_bytes(r.stderr)
        need(r.returncode != 0 and b'normal Python required' in r.stderr, 'optimization guard')
    if a.render:
        shutil.copy2(HERE / 'anchor_deletion.tex', out / 'anchor_deletion.tex')
        for i in [1, 2]:
            r = subprocess.run(['/opt/homebrew/bin/pdflatex', '-interaction=nonstopmode',
                                '-halt-on-error', 'anchor_deletion.tex'], cwd=out,
                               env=env, capture_output=True, timeout=30)
            (out / f'native{i}.stdout').write_bytes(r.stdout)
            (out / f'native{i}.stderr').write_bytes(r.stderr)
            need(r.returncode == 0 and not r.stderr, 'native execution')
        log = (out / 'anchor_deletion.log').read_text()
        need('Overfull' not in log and 'LaTeX Warning:' not in log, 'native content')
    report = {'status': 'PASS_ANCHOR_DELETION_BINDINGS_AND_NATIVE',
              'exports': len(exports), 'dependencies': len(deps),
              'optimization_guards': 2, 'finite_mathematical_premise': False,
              'mathematical_review': 'separate', 'whole_original_credit': 0}
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
