"""Replay the source join and native manuscript, without acquired censuses."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Optimized Python is not supported')
sys.dont_write_bytecode = True
import argparse
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

def need(condition, message):
    if not condition:
        raise ValueError(message)

def load(path):
    return json.loads(path.read_text())

def verify(base, row):
    p = (base / row['path']).resolve()
    need(p.is_relative_to(base) and p.is_file(), 'Unsafe or missing exact file')
    b = p.read_bytes()
    need(len(b) == row['bytes'] and hashlib.sha256(b).hexdigest() == row['sha256'], 'Changed exact file ' + row['path'])
    return p

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--study', type=Path, required=True)
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--render', action='store_true')
    a = ap.parse_args()
    P = Path(__file__).resolve().parent
    S, R, O = a.study.resolve(), a.repo.resolve(), a.out.resolve()
    need(not O.exists() and not O.is_relative_to(P), 'Fresh external output required')
    manifest = load(P / 'manifest.json')
    need(manifest['original'] == 'L052', 'Exact original')
    need(len({r['path'] for r in manifest['exports']}) == len(manifest['exports']), 'Distinct exports')
    for row in manifest['exports']:
        verify(P, row)
    for row in load(P / 'acquired_packets.json')['packets']:
        verify(S, row['manifest'])
    O.mkdir(parents=True)
    env = os.environ.copy()
    env.pop('PYTHONOPTIMIZE', None)
    commands = []
    def run(name, argv):
        result = subprocess.run(list(map(str, argv)), cwd=O, env=env, capture_output=True, timeout=120)
        (O / (name + '.stdout')).write_bytes(result.stdout)
        (O / (name + '.stderr')).write_bytes(result.stderr)
        commands.append(dict(name=name, argv=list(map(str, argv)), returncode=result.returncode))
        need(result.returncode == 0, 'Failed child ' + name)
        return result
    run('register', [sys.executable, P/'check_register.py', '--study', S, '--repo', R, '--out', O/'register'])
    report = load(O/'register/report.json')
    need(report['status'] == 'PASS_COMPLETE_L052_SOURCE_JOIN', 'Complete source join')
    from pypdf import PdfReader
    def pages(path):
        return [p.extract_text() for p in PdfReader(path).pages]
    combined = pages(P/'principal.pdf')
    need(len(combined) == 5, 'Five complete synthesis pages')
    expected = '\n\f\n'.join(combined)
    need(expected == (P/'principal_expected.txt').read_text(), 'Exact synthesis text')
    inventory = load(P/'acquired_manuscripts.json')
    need([x['pages'] for x in inventory['manuscripts']] == [8, 5], 'Both complete acquired manuscripts')
    for row in inventory['manuscripts']:
        verify(S, row['tex'])
        acquired = pages(verify(S, row['pdf']))
        need(len(acquired) == row['pages'], 'Complete acquired page range')
        combined.extend(acquired)
    need(len(combined) == 18 and pages(P/'complete_proof.pdf') == combined, 'Exact eighteen-page reading volume')
    guards = []
    for entry in ['check.py', 'check_register.py']:
        for mode in ['argument', 'environment']:
            e = env.copy()
            cmd = [sys.executable]
            if mode == 'argument':
                cmd.append('-O')
            else:
                e['PYTHONOPTIMIZE'] = '1'
            target = O / ('rejected_' + entry + '_' + mode)
            cmd += [str(P/entry), '--study', str(S), '--repo', str(R), '--out', str(target)]
            r = subprocess.run(cmd, env=e, capture_output=True, timeout=15)
            (O / ('guard_' + entry + '_' + mode + '.stderr')).write_bytes(r.stderr)
            need(r.returncode != 0 and b'Optimized Python is not supported' in r.stderr and not target.exists(), 'Pre-output optimization guard')
            guards.append(dict(entry=entry, mode=mode))
    native = None
    if a.render:
        N = O/'native'
        N.mkdir()
        shutil.copyfile(P/'principal.tex', N/'principal.tex')
        for i in range(2):
            run('native' + str(i+1), ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', '-output-directory='+str(N), N/'principal.tex'])
        need('\n\f\n'.join(pages(N/'principal.pdf')) == expected, 'Fresh native text and page identity')
        log = (N/'principal.log').read_text()
        need(not any(x in log for x in ['Overfull', 'Underfull', 'LaTeX Warning:', 'undefined references']), 'Clean final native log')
        run('raster', ['gs', '-q', '-dBATCH', '-dNOPAUSE', '-sDEVICE=png16m', '-r100', '-sOutputFile='+str(N/'page-%02d.png'), N/'principal.pdf'])
        need(len(list(N.glob('page-*.png'))) == 5, 'All five native rasters')
        native = dict(pages=5, text_identical=True, clean_log=True)
    final = dict(status='PASS_L052_PRINCIPAL_ASSEMBLY', exports=len(manifest['exports']),
        direct_bindings=report['bindings'], counts=report['counts'], acquired_components=2,
        acquired_manifests=5, acquired_pages=13, synthesis_pages=5, full_reading_volume_pages=18,
        damaged_controls=report['damaged_controls'], optimization_guards=guards,
        commands=commands, native=native, mathematical_census_repeated=False,
        whole_original_credit=0, new_question_credit=0, new_measurements=0, new_Lean_declarations=0)
    (O/'report.json').write_text(json.dumps(final, indent=2)+'\n')
    print(json.dumps(final))

if __name__ == '__main__':
    main()
