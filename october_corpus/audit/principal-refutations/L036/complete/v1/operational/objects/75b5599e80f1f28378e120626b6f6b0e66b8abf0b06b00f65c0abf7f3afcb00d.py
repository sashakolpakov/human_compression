"""Replay the finite arithmetic and fixed-source joins; never invoke GAP."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode = True
from pathlib import Path
from pypdf import PdfReader
import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
P = HERE.parent
SOURCE = P.parents[1] / 'sources/catalogue_L036.pdf'
RAW = P / 'table_execution01/stdout'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load(path):
    return json.loads(path.read_text())


def pin(path):
    data = path.read_bytes()
    return dict(path=str(path), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())


def module(name):
    spec = importlib.util.spec_from_file_location(name, HERE / (name + '.py'))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def texts(path):
    return [p.extract_text() for p in PdfReader(path).pages]


def main(args):
    need(args.out.is_absolute() and not args.out.exists(), 'Fresh absolute replay directory')
    deps = load(HERE / 'dependencies.json')
    for row in deps:
        need(pin(Path(row['path'])) == row, 'Exact input: ' + row['path'])
    receipt = load(P / 'table_execution01/receipt.json')
    need(receipt['reason'] == 'completed' and receipt['returncode'] == 0 and receipt['child_reaped'] and
         receipt['final_request_unchanged'] and not receipt['final_binding_failures'] and
         not receipt['final_boundary_failures'] and receipt['final_bindings_checked'] == 201,
         'Actual single acquisition completed within reviewed limits')
    need((P / 'table_execution01/stderr').read_bytes() == b'', 'No acquisition stderr')
    raw = RAW.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == receipt['outputs'][0]['sha256'], 'Exact actual output')
    need(load(P / 'table_request02_root_review/manifest.json')['status'].startswith('ACCEPTED'),
         'Distinct input-request acceptance')
    a = module('arithmetic')
    data, intervals = a.parse(raw)
    result = a.calculate(data)
    result.update(literal_GAP_interval_adapter=intervals, input_sha256=hashlib.sha256(raw).hexdigest())
    need(result == load(HERE / 'results.json'), 'Exact independently recomputed arithmetic')
    source, pages = module('source_tables').extract(SOURCE)
    need(source == load(HERE / 'printed01/tables.json'), 'Every printed source cell retained exactly')
    comparison = module('join').compare(source, result, load(P / 'character_application/arithmetic01.json'))
    need(comparison == load(HERE / 'source_join.json'), 'Exact source comparison and label correction')
    controls = module('controls').run(data, source, result)
    need(controls == load(HERE / 'controls01.json'), 'Exact mathematical controls')
    need((HERE / 'theory.tex').read_bytes() == (P / 'character_application/theory.tex').read_bytes() and
         (HERE / 'theory.pdf').read_bytes() == (P / 'character_application/theory.pdf').read_bytes(),
         'Unchanged accepted common proof')
    collisions = {r['name']: r['equal_maximal_character_positions'] for r in result['suborbits']}
    need(collisions == dict(M11=[], M12=[], M22=[[3, 4]], M23=[[2, 3]], J1=[]),
         'Exactly the character ambiguities stated in the proof')
    args.out.mkdir()
    save(args.out / 'arithmetic.json', result)
    save(args.out / 'source_join.json', comparison)
    save(args.out / 'controls.json', controls)
    guards = []
    for flag in ['-O', '-OO']:
        proc = subprocess.run([sys.executable, flag, str(HERE / 'arithmetic.py'), '--help'],
                              capture_output=True, timeout=5)
        need(proc.returncode != 0 and b'Ordinary Python required' in proc.stderr,
             'Optimization must reject execution')
        guards.append(flag)
    native = []
    if args.render:
        shutil.copyfile(HERE / 'applications.tex', args.out / 'applications.tex')
        for i in [1, 2]:
            proc = subprocess.run(['/opt/homebrew/bin/pdflatex', '-interaction=nonstopmode',
                                   '-halt-on-error', 'applications.tex'], cwd=args.out,
                                  capture_output=True, timeout=30)
            (args.out / ('tex%d.stdout' % i)).write_bytes(proc.stdout)
            (args.out / ('tex%d.stderr' % i)).write_bytes(proc.stderr)
            need(proc.returncode == 0, 'Native TeX build')
        need('Overfull' not in (args.out / 'applications.log').read_text(), 'Clean proof layout')
        need(texts(args.out / 'applications.pdf') == texts(HERE / 'applications.pdf'), 'Exact fresh proof text')
        proc = subprocess.run(['/opt/homebrew/bin/gs', '-q', '-dSAFER', '-dBATCH', '-dNOPAUSE',
                               '-sDEVICE=png16m', '-r100', '-sOutputFile=proof-%02d.png',
                               'applications.pdf'], cwd=args.out, capture_output=True, timeout=30)
        need(proc.returncode == 0, 'Native raster generation')
        for i in range(1, len(texts(HERE / 'applications.pdf')) + 1):
            name = 'proof-%02d.png' % i
            need((args.out / name).read_bytes() == (HERE / ('final-%02d.png' % i)).read_bytes(),
                 'Exact fresh native proof page')
            native.append(name)
    report = dict(status='PASS_L036_SIX_OUTER_TOTALS_AND_SUBORBIT_TABLES', dependency_bindings=len(deps),
                  stored_mark_tables=11, printed_numeric_cells=308, numeric_cell_changes=0,
                  M23_row_label_corrections=2, preliminary_upper_counts=dict(M11=38, M12=268),
                  controls=controls, optimization_guards=guards, native_pages=native,
                  GAP_launched=False, whole_source_accepted=False)
    save(args.out / 'report.json', report)
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--render', action='store_true')
    main(parser.parse_args())
