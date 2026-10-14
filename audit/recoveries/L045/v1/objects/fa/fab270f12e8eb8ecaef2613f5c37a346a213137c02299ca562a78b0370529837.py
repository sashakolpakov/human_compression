"""Fresh bounded finite controls for the full-rank even orthogonal theorem."""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
from verify_report import need, validate


def pin(path):
    data = path.read_bytes()
    return dict(path=str(path), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--study', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--render', action='store_true')
    args = parser.parse_args()
    packet, study, out = Path(__file__).resolve().parent, args.study.resolve(), args.out.resolve()
    need(not out.exists(), 'fresh output required')
    dependencies = json.loads((packet / 'dependencies.json').read_text())
    for row in dependencies:
        actual = pin(study / row['path'])
        need(all(actual[k] == row[k] for k in ('bytes', 'sha256')), 'exact dependency ' + row['path'])
    exports = []
    if (packet / 'manifest.json').exists():
        exports = json.loads((packet / 'manifest.json').read_text())['exports']
        for row in exports:
            actual = pin(packet / row['path'])
            need(all(actual[k] == row[k] for k in ('bytes', 'sha256')), 'exact export ' + row['path'])
    historical_pins = 0
    if (packet / 'execution_aliases.json').exists():
        aliases = json.loads((packet / 'execution_aliases.json').read_text())
        for receipt_path in sorted((packet / 'author_replay').glob('*.receipt.json')):
            receipt = json.loads(receipt_path.read_text())
            need(receipt['exit_code'] == 0, 'retained clean execution')
            for row in receipt['inputs'] + [receipt['stdout'], receipt['stderr']]:
                need(row['path'] in aliases, 'complete retained execution closure')
                actual = pin(packet / aliases[row['path']])
                need(all(actual[k] == row[k] for k in ('bytes', 'sha256')), 'literal retained execution pin')
                historical_pins += 1
    out.mkdir(parents=True)
    env = os.environ.copy()
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    receipts = []

    def run(name, command, inputs, cap=60, cwd=None):
        start = time.monotonic()
        before = [pin(p) for p in inputs]
        try:
            result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, timeout=cap)
        except subprocess.TimeoutExpired as error:
            (out / (name + '.stdout')).write_bytes(error.stdout or b'')
            (out / (name + '.stderr')).write_bytes(error.stderr or b'')
            (out / (name + '.receipt.json')).write_text(json.dumps(dict(status='TIMEOUT_NO_CERTIFICATE',
                command=command, inputs=before, cap=cap), indent=2) + '\n')
            raise
        stdout, stderr = out / (name + '.stdout'), out / (name + '.stderr')
        stdout.write_bytes(result.stdout)
        stderr.write_bytes(result.stderr)
        receipt = dict(command=command, cwd=str(cwd) if cwd else None, inputs=before,
                       exit_code=result.returncode, elapsed=time.monotonic() - start,
                       stdout=pin(stdout), stderr=pin(stderr), cap=cap)
        (out / (name + '.receipt.json')).write_text(json.dumps(receipt, indent=2) + '\n')
        receipts.append(name)
        need(before == [pin(p) for p in inputs], 'unchanged actual inputs')
        need(result.returncode == 0 and not result.stderr, 'clean terminal execution: ' + name)
        return result.stdout

    compiler = shutil.which('clang++')
    need(compiler is not None, 'C++ compiler')
    source = packet / 'matrix_controls.cpp'
    outputs = []
    for mode in ('plain', 'sanitized'):
        binary = out / ('matrix_' + mode)
        flags = ['-O2'] if mode == 'plain' else ['-O1', '-g', '-fsanitize=address,undefined', '-fno-omit-frame-pointer']
        run(mode + '_compile', [compiler, '-std=c++17', '-Wall', '-Wextra', '-pedantic'] + flags + [str(source), '-o', str(binary)], [source])
        stdout = run(mode, [str(binary)], [binary, source], cap=90)
        report = json.loads(stdout)
        validate(report)
        need(report == json.loads((packet / 'expected_matrix.json').read_text()), 'exact finite matrix output')
        outputs.append(stdout)
    need(outputs[0] == outputs[1], 'ordinary and sanitized output equality')
    actual = packet / 'actual_controls.g'
    stdout = run('actual_groups', ['/opt/homebrew/bin/gap', '-q', '-T', str(actual)], [actual], cap=60)
    need(stdout == (packet / 'expected_gap.txt').read_bytes(), 'exact independent named groups and trace controls')
    lines = [line.strip() for line in stdout.decode().splitlines() if line.strip()]
    need(len(lines) == 12 and lines[-1] == 'COMPLETE_EVEN_FIXED_CONTROLS', 'complete eleven-control GAP roster')

    report = json.loads(outputs[0])
    damages = []
    for label in ('factor_two', 'missing_fibre', 'duplicate_frame', 'wrong_nu', 'wrong_bound', 'wrong_total'):
        bad = copy.deepcopy(report)
        if label == 'factor_two': bad['fibres'][3]['omega_kernel'] *= 2
        elif label == 'missing_fibre': bad['fibres'].pop()
        elif label == 'duplicate_frame': bad['frames'][-1] = bad['frames'][-2]
        elif label == 'wrong_nu': bad['centralizers'][4]['nu2'] += 1
        elif label == 'wrong_bound': bad['centralizers'][4]['bound'] *= 2
        else: bad['literal_centralizer_matrices'] -= 1
        try:
            validate(bad)
        except ValueError:
            damages.append(label)
        else:
            raise ValueError('accepted damaged report: ' + label)
    (out / 'damaged_controls.json').write_text(json.dumps(damages, indent=2) + '\n')
    guards = []
    for script in ('check.py', 'verify_report.py'):
        for mode in ('argument', 'environment'):
            target = out / ('forbidden_' + script + '_' + mode)
            command = [sys.executable]
            guard_env = env.copy()
            if mode == 'argument': command.append('-O')
            else: guard_env['PYTHONOPTIMIZE'] = '1'
            result = subprocess.run(command + [str(packet / script), '--out', str(target)], env=guard_env, capture_output=True, timeout=10)
            need(result.returncode != 0 and b'unoptimized execution required' in result.stderr and not target.exists(), 'pre-output optimization rejection')
            guards.append(dict(script=script, mode=mode, exit_code=result.returncode, stderr=result.stderr.decode()))
    (out / 'optimization_controls.json').write_text(json.dumps(guards, indent=2) + '\n')

    native = out / 'native'
    native.mkdir()
    tex = native / 'even_fixed.tex'
    shutil.copy2(packet / 'even_fixed.tex', tex)
    for i in range(2):
        run('native' + str(i), ['/opt/homebrew/bin/pdflatex', '-halt-on-error', '-interaction=nonstopmode', tex.name], [tex], cwd=native)
    log = (native / 'even_fixed.log').read_text()
    need(not any(x in log for x in ('Overfull', 'Underfull', 'LaTeX Warning')), 'clean native output')
    from pypdf import PdfReader
    pdf = PdfReader(native / 'even_fixed.pdf')
    text = '\n'.join(page.extract_text() or '' for page in pdf.pages)
    (native / 'text.txt').write_text(text)
    need(len(pdf.pages) == 3, 'complete three-page proof')
    if (packet / 'expected_text.txt').exists():
        need(text == (packet / 'expected_text.txt').read_text(), 'exact native text')
    if args.render:
        run('render', ['/opt/homebrew/bin/gs', '-dSAFER', '-dBATCH', '-dNOPAUSE', '-sDEVICE=png16m', '-r110', '-sOutputFile=page-%02d.png', 'even_fixed.pdf'], [native / 'even_fixed.pdf'], cwd=native)
    final = dict(status='PASS_EVEN_ORTHOGONAL_FIXED', exports=len(exports), dependencies=len(dependencies),
        matrix_controls=validate(report), actual_group_cases=4, trace_families=7, trace_inverters=121,
        sanitized_exact=True, damaged_controls=6, optimization_guards=4, native_pages=3,
        historical_execution_pins=historical_pins,
        completed_receipts=receipts, whole_original_credit=0, source_row_credit=0)
    (out / 'report.json').write_text(json.dumps(final, indent=2) + '\n')
    print(json.dumps(final))


if __name__ == '__main__':
    main()
