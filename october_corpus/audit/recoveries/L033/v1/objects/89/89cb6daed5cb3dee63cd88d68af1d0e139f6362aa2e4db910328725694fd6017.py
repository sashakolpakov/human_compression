"""Replay finite certificates and complete native manuscript.

The geometric proof is mathematical text requiring a distinct reader.
This program does not claim to be a formal proof checker.
"""
import sys
if sys.flags.optimize:
    raise RuntimeError('Normal Python is required')
sys.dont_write_bytecode = True
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
from compute_spherical import compute
from verify_weights import require


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--render', action='store_true')
    args = parser.parse_args()
    packet = Path(__file__).resolve().parent
    output = args.out.resolve()
    require(not output.exists() and not output.is_relative_to(packet), 'fresh external output')
    manifest = json.loads((packet / 'manifest.json').read_text())
    dependencies = json.loads((packet / 'dependencies.json').read_text())

    def bound(path, row):
        data = path.read_bytes()
        require(len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'],
                'changed input ' + str(path))

    for row in manifest['exports']:
        bound(packet / row['path'], row)
    for row in dependencies:
        bound(Path(row['path']), row)
    output.mkdir(parents=True)
    result = compute(output / 'finite')
    expected = json.loads((packet / 'finite_report.json').read_text())
    require(result == expected, 'complete finite agreement')
    require((output / 'finite/central_matrices.json').read_bytes() ==
            (packet / 'central_matrices.json').read_bytes(), 'central matrix agreement')
    for row in result['orbits']:
        name = 'E%d_%d.txt.gz' % (row['rank'], row['vertex_type'])
        require((packet / 'certificates' / name).read_bytes() ==
                (output / 'finite' / name).read_bytes(), 'full certificate agreement ' + name)
    from pypdf import PdfReader
    expected_text = [p.extract_text() for p in PdfReader(packet / 'spherical_quotients.pdf').pages]
    require(len(expected_text) == 6, 'complete six-page manuscript')
    native_pages = None
    if args.render:
        native = output / 'native'
        native.mkdir()
        shutil.copy2(packet / 'spherical_quotients.tex', native / 'spherical_quotients.tex')
        for pass_number in range(2):
            child = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error',
                                    'spherical_quotients.tex'], cwd=native, capture_output=True, timeout=60)
            (native / f'build{pass_number}.stdout').write_bytes(child.stdout)
            (native / f'build{pass_number}.stderr').write_bytes(child.stderr)
            require(child.returncode == 0 and not child.stderr, 'native compilation')
        log = (native / 'spherical_quotients.log').read_text()
        require(not any(x in log for x in ['Overfull', 'Underfull', 'Warning']), 'clean native layout')
        require([p.extract_text() for p in PdfReader(native / 'spherical_quotients.pdf').pages] == expected_text,
                'complete native text')
        child = subprocess.run(['gs', '-q', '-dSAFER', '-dBATCH', '-dNOPAUSE', '-sDEVICE=png16m',
                                '-r90', '-sOutputFile=page-%02d.png', 'spherical_quotients.pdf'],
                               cwd=native, capture_output=True, timeout=60)
        (native / 'render.stderr').write_bytes(child.stderr)
        require(child.returncode == 0 and not child.stderr and len(list(native.glob('page-*.png'))) == 6,
                'six rendered pages')
        native_pages = 6
    guards = []
    for mode in ['argument', 'environment']:
        command = [sys.executable] + (['-O'] if mode == 'argument' else []) + [str(packet / 'check.py')]
        environment = dict(os.environ)
        if mode == 'environment':
            environment['PYTHONOPTIMIZE'] = '1'
        child = subprocess.run(command, env=environment, capture_output=True, timeout=15)
        require(child.returncode != 0 and b'Normal Python is required' in child.stderr, 'optimization guard')
        guards.append(mode)
    report = {'status': 'PASS_L033_SPHERICAL_COMPONENT', 'exports': len(manifest['exports']),
              'dependencies': len(dependencies), 'orbits': len(result['orbits']),
              'vectors': result['vectors'], 'reflection_checks': result['reflection_checks'],
              'central_matrix_types': result['central_matrix_types'],
              'damaged_controls': result['damaged_controls'], 'optimization_guards': guards,
              'native_pages': native_pages, 'whole_original_credit': 0, 'new_question_credit': 0,
              'new_Lean': 0, 'compression_factor': None, 'written_proof_requires_distinct_review': True}
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
