#!/usr/bin/env python3
"""Replay the reviewed locally faithful cover certificates without primary PDFs."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
PINS = {
    'phase246_manifest.json': 'c418955a364b691a3339eeb7d04b97300dfc691686deb9a1cc3184e74b899185',
    'phase255_manifest.json': '832dce997f2098e17cf3eff9de9f7da359b05256ab1ba26dd427978482821aee',
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def need(condition, message):
    if not condition:
        raise RuntimeError('PHASE260_REJECT ' + message)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['out', 'gap', 'lean', 'packages']:
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(), 'fresh output')
    out = args.out.resolve()
    need(not out.exists(), 'fresh resolved output')
    out.mkdir(parents=True)
    start = time.monotonic()
    checked = 0
    for name, pin in PINS.items():
        need(sha(ROOT / name) == pin, 'frozen manifest ' + name)
        manifest = json.loads((ROOT / name).read_text())
        for row in manifest.get('files', manifest.get('exports', [])) + manifest['retained']:
            rel = Path(row['path'])
            need(not rel.is_absolute() and '..' not in rel.parts, 'relative frozen path')
            if rel.parts[0] == 'sources':
                continue
            path = ROOT / rel
            need(path.stat().st_size == row['bytes'] and sha(path) == row['sha256'],
                 'frozen artifact ' + str(rel))
            checked += 1
    executions = []
    def run(label, command):
        tick = time.monotonic()
        result = subprocess.run([str(x) for x in command], cwd=out,
                                text=True, capture_output=True, timeout=360)
        stdout, stderr = out / (label + '.stdout'), out / (label + '.stderr')
        stdout.write_text(result.stdout)
        stderr.write_text(result.stderr)
        executions.append(dict(label=label, returncode=result.returncode,
            seconds=round(time.monotonic()-tick, 3),
            stdout_sha256=sha(stdout), stderr_sha256=sha(stderr)))
        need(result.returncode == 0, label + ' exit status')
        return result
    run('author', [sys.executable, '-B', '-O', ROOT / 'phase246_check.py',
        '--out', out / 'author', '--gap', args.gap, '--lean', args.lean,
        '--packages', args.packages])
    author = json.loads((out / 'author/report.json').read_text())
    need(author['status'] == 'PASS' and len(author['axiom_reports']) == 3,
         'author and scoped formal replay')
    run('independent_complex', [sys.executable, '-B', '-O',
        ROOT / 'phase255_native_complex.py', '--out', out / 'native', '--gap', args.gap])
    run('independent_integer', [sys.executable, '-B', '-O',
        ROOT / 'phase245_tomotope_integral.py', '--input', out / 'native/complex.json',
        '--out', out / 'native_integral_report.json'])
    kernel = run('independent_kernel', [sys.executable, '-B', '-O',
        ROOT / 'phase255_run_kernel.py', '--out', out / 'kernel', '--gap', args.gap,
        '--voltage', out / 'author/Tomotope_voltage.json'])
    need('PHASE255_PASS' in kernel.stdout and
         not re.search(r'Error|warning', kernel.stdout + kernel.stderr),
         'actual independent kernel action')
    report = dict(status='PASS', seconds=round(time.monotonic()-start, 3),
        frozen_public_bindings_checked=checked, primary_full_texts_distributed=False,
        lean_declarations=3, actual_cover_order=73728, minimal_abelian_cover_order=36864,
        executions=executions,
        scope='General locally faithful abelian criterion and restricted Tomotope classification; no general finite multiplicity solution or full Lean claim.')
    (out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))

if __name__ == '__main__':
    main()
