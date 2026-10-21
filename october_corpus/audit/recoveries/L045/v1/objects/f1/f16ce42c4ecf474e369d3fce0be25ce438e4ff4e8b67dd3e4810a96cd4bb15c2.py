"""Replay the exact principal assembly, without rerunning acquired censuses."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Optimized Python is not supported')
sys.dont_write_bytecode = True
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
from pathlib import Path

def need(ok, message):
    if not ok:
        raise ValueError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--study', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--render', action='store_true')
    a = ap.parse_args()
    P = Path(__file__).resolve().parent
    S, O = a.study.resolve(), a.out.resolve()
    need(not O.exists() and not O.is_relative_to(P), 'Fresh external output required')
    manifest = json.loads((P / 'manifest.json').read_text())
    for row in manifest['exports']:
        p = (P / row['path']).resolve()
        need(p.is_relative_to(P) and p.is_file(), 'Unsafe/missing packet export')
        need(p.stat().st_size == row['bytes'] and sha(p) == row['sha256'], 'Changed packet export ' + row['path'])
    # The scientific checker verifies all literal source routes and every
    # complete acquired author/review-manifest export, not sampled proofs.
    O.mkdir(parents=True)
    env = os.environ.copy(); env.pop('PYTHONOPTIMIZE', None)
    commands = []
    def run(name, argv):
        p = subprocess.run(argv, cwd=O, env=env, capture_output=True, timeout=120)
        (O / (name + '.stdout')).write_bytes(p.stdout)
        (O / (name + '.stderr')).write_bytes(p.stderr)
        commands.append(dict(name=name, argv=list(map(str, argv)), returncode=p.returncode))
        need(p.returncode == 0, 'Failed child ' + name)
        return p
    run('register', [sys.executable, str(P/'check_register.py'), '--study', str(S), '--out', str(O/'register'), '--require-complete'])
    register = json.loads((O/'register/report.json').read_text())
    need(register['status'] == 'PASS_COMPLETE_POSITIVE_PRINCIPAL_REGISTER' and not register['pending'], 'Complete principal contract')
    inventory = json.loads((P/'acquired_manuscripts.json').read_text())
    from pypdf import PdfReader
    def texts(pdf):
        return [page.extract_text() for page in PdfReader(pdf).pages]
    ordered = [dict(path='principal.pdf', pages=7, origin='packet')]
    combined = texts(P/'principal.pdf')
    for row in inventory['manuscripts']:
        for key in ['tex','pdf']:
            path = S / row[key]['path']
            need(path.is_file() and path.stat().st_size == row[key]['bytes'] and sha(path) == row[key]['sha256'], 'Acquired native edition')
        extracted = texts(S/row['pdf']['path'])
        need(len(extracted) == row['pages'], 'Complete acquired page range')
        combined.extend(extracted)
        ordered.append(dict(path=row['pdf']['path'], pages=row['pages'], origin='study'))
    need(len(ordered) == 15 and len(combined) == 58, 'Seven synthesis plus 51 complete acquired pages')
    need(texts(P/'complete_proof.pdf') == combined, 'Exact page-for-page complete reading volume')
    guards = []
    for mode in ['argument', 'environment']:
        e = env.copy()
        cmd = [sys.executable]
        if mode == 'argument': cmd.append('-O')
        else: e['PYTHONOPTIMIZE'] = '1'
        target = O / ('rejected_' + mode)
        cmd += [str(P/'check.py'), '--study', str(S), '--out', str(target)]
        r = subprocess.run(cmd, env=e, capture_output=True, timeout=15)
        (O / ('guard_' + mode + '.stderr')).write_bytes(r.stderr)
        need(r.returncode != 0 and b'Optimized Python is not supported' in r.stderr and not target.exists(), 'Pre-output optimization guard')
        guards.append(mode)
    native = None
    if a.render:
        N = O/'native'; N.mkdir(); shutil.copyfile(P/'principal.tex', N/'principal.tex')
        for i in range(2):
            run('native' + str(i+1), ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', '-output-directory='+str(N), str(N/'principal.tex')])
        pages = texts(N/'principal.pdf')
        expected = (P/'principal_expected.txt').read_text()
        need('\n\f\n'.join(pages) == expected and len(pages) == 7, 'Fresh native text/page identity')
        log = (N/'principal.log').read_text()
        need(not any(token in log for token in ['Overfull', 'Underfull', 'LaTeX Warning:', 'undefined references']), 'Clean final native log')
        run('raster', ['gs','-q','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile='+str(N/'page-%02d.png'),str(N/'principal.pdf')])
        need(len(list(N.glob('page-*.png'))) == 7, 'All native rasters')
        native = dict(pages=7, text_identical=True, clean_log=True)
    report = dict(status='PASS_L045_POSITIVE_PRINCIPAL_ASSEMBLY', exports=len(manifest['exports']),
        direct_bindings=register['bindings'], source_clauses=36, finite_parameter_entries=35,
        sporadic_groups=26, acquired_roots=13, acquired_manuscripts=14, acquired_pages=51,
        synthesis_pages=7, full_reading_volume_pages=58, damaged_controls=register['damaged_controls'],
        optimization_guards=guards, native=native, commands=commands, mathematical_census_repeated=False,
        whole_original_credit=0, new_question_credit=0, new_measurements=0, new_Lean_declarations=0)
    (O/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))

if __name__ == '__main__':
    main()
