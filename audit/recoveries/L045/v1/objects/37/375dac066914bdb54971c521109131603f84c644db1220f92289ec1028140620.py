"""Bound the finite controls and rebuild the complete torus manuscript."""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess


def need(value, message):
    if not value:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--study', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--render', action='store_true')
    args = parser.parse_args()
    packet = Path(__file__).resolve().parent
    study = args.study.resolve()
    out = args.out.resolve()
    need(not out.exists(), 'fresh output required')
    dependencies = json.loads((packet / 'dependencies.json').read_text())
    for row in dependencies:
        data = (study / row['path']).read_bytes()
        need(len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'], 'exact primary dependency')
    exports = []
    if (packet / 'manifest.json').is_file():
        exports = json.loads((packet / 'manifest.json').read_text())['exports']
        for row in exports:
            data = (packet / row['path']).read_bytes()
            need(len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'], 'exact frozen export')
    out.mkdir(parents=True)
    env = os.environ.copy()
    env.pop('PYTHONOPTIMIZE', None)

    def run(name, command, cap, cwd=None):
        result = subprocess.run(command, capture_output=True, timeout=cap, env=env, cwd=cwd)
        (out / (name + '.stdout')).write_bytes(result.stdout)
        (out / (name + '.stderr')).write_bytes(result.stderr)
        need(result.returncode == 0 and not result.stderr, 'clean completion ' + name)
        return result.stdout

    stdout = run('controls', ['/opt/homebrew/bin/gap', '-q', '-T', str(packet / 'tori_controls.g')], 60)
    need(stdout == (packet / 'expected_stdout.txt').read_bytes(), 'exact full finite controls')
    lines = [line.strip() for line in stdout.decode().splitlines() if line.strip()]
    need(len(lines) == 37 and lines[-1] == 'COMPLETE_TORI_CONTROLS', 'complete case roster')
    need(sum(s.startswith('TORUS|') for s in lines) == 12, 'twelve finite-field matrix cases')
    need(sum(s.startswith('PAIR|') for s in lines) == 24, 'twenty-four paired scalar cases')
    for mode in ('argument', 'environment'):
        command = [sys.executable]
        guard_env = env.copy()
        if mode == 'argument':
            command.append('-O')
        else:
            guard_env['PYTHONOPTIMIZE'] = '1'
        target = out / ('forbidden_' + mode)
        result = subprocess.run(command + [str(packet / 'check.py'), '--out', str(target)],
                                capture_output=True, timeout=10, env=guard_env)
        (out / (mode + '.stderr')).write_bytes(result.stderr)
        need(result.returncode != 0 and b'unoptimized execution required' in result.stderr and not target.exists(), 'optimization guard')
    native = out / 'native'
    native.mkdir()
    shutil.copy2(packet / 'tori.tex', native / 'tori.tex')
    for number in range(2):
        run('native' + str(number), ['/opt/homebrew/bin/pdflatex', '-halt-on-error', '-interaction=nonstopmode', 'tori.tex'], 45, native)
    log = (native / 'tori.log').read_text()
    need(not any(s in log for s in ['Overfull', 'Underfull', 'LaTeX Warning', 'Package rerunfilecheck Warning']), 'clean native manuscript')
    from pypdf import PdfReader
    pdf = PdfReader(native / 'tori.pdf')
    need(len(pdf.pages) == 3, 'complete three-page manuscript')
    native_text = '\n'.join(p.extract_text() or '' for p in pdf.pages)
    (native / 'text.txt').write_text(native_text)
    if (packet / 'expected_text.txt').is_file():
        need(native_text == (packet / 'expected_text.txt').read_text(), 'exact native text')
    if args.render:
        run('render', ['/opt/homebrew/bin/gs', '-dSAFER', '-dBATCH', '-dNOPAUSE', '-sDEVICE=png16m', '-r110', '-sOutputFile=page-%02d.png', 'tori.pdf'], 45, native)
    report = dict(status='PASS_ORTHOGONAL_TORI_CONTROLS', exports=len(exports), dependencies=len(dependencies),
                  matrix_cases=12, paired_order_cases=24, native_pages=3, optimization_guards=2,
                  whole_original_credit=0, new_question_credit=0, Lean_credit=0)
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
