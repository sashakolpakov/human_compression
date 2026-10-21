"""Check the frozen written component and its acquired editions; no group search."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Normal Python is required')
sys.dont_write_bytecode = True
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

STUDY = Path('/Users/sasha/medusa/research/leemans')
REPO = Path('/Users/sasha/medusa/math_compression')

def need(ok, message):
    if not ok:
        raise ValueError(message)

def pin_ok(path, row):
    raw = path.read_bytes()
    need(len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'],
         'Changed acquired edition: ' + str(path))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--study', type=Path, required=True)
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--render', action='store_true')
    a = ap.parse_args()
    base = Path(__file__).resolve().parent
    out = a.out.resolve()
    need(not out.exists() and not out.is_relative_to(base), 'Fresh external output required')
    manifest = json.loads((base/'manifest.json').read_text())
    for row in manifest['exports']:
        p = (base/row['path']).resolve()
        need(p.is_relative_to(base), 'Unsafe export path')
        pin_ok(p, row)
    dependencies = json.loads((base/'dependencies.json').read_text())
    for row in dependencies:
        p = Path(row['path'])
        if p.is_relative_to(STUDY):
            p = a.study.resolve()/p.relative_to(STUDY)
        elif p.is_relative_to(REPO):
            p = a.repo.resolve()/p.relative_to(REPO)
        else:
            raise ValueError('Unregistered dependency root: ' + str(p))
        pin_ok(p, row)
    scope = json.loads((base/'scope.json').read_text())
    need(scope['original_id'] == 'N010' and scope['written_pages'] == 2, 'Written source scope')
    need(scope['source_section'] == [2,4,5] and len(scope['claims']) == 2, 'Chamber word component scope')
    need(all(scope[k] == 0 for k in ['whole_original_credit','new_question_credit',
                                   'new_Lean_declarations','new_measurements']), 'Component boundary')
    out.mkdir(parents=True)
    env = dict(__import__('os').environ)
    env.pop('PYTHONOPTIMIZE', None)
    p = subprocess.run([sys.executable, str(base/'check_amalgamations.py'), '--out', str(out/'finite')], capture_output=True, timeout=75, env=env)
    (out/'finite.stdout').write_bytes(p.stdout)
    (out/'finite.stderr').write_bytes(p.stderr)
    need(p.returncode == 0 and not p.stderr, 'Full finite calculation')
    finite = json.loads((out/'finite/report.json').read_text())
    need(finite['status'] == 'PASS_TWO_EXACT_ORIENTED_AMALGAMATIONS', 'Complete finite report')
    need([x['order'] for x in finite['cases']] == [2000,960], 'Both exact source orders')
    native = None
    if a.render:
        from pypdf import PdfReader
        shutil.copy2(base/'oriented_examples.tex', out/'oriented_examples.tex')
        for n in [1,2]:
            p = subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',
                                'oriented_examples.tex'], cwd=out, capture_output=True, timeout=45)
            (out/f'native{n}.stdout').write_bytes(p.stdout)
            (out/f'native{n}.stderr').write_bytes(p.stderr)
            need(p.returncode == 0, 'Native build failed')
        text = lambda p: [page.extract_text() for page in PdfReader(p).pages]
        got = text(out/'oriented_examples.pdf')
        need(len(got) == 2 and got == text(base/'oriented_examples.pdf'), 'Exact native text and pages')
        log = (out/'oriented_examples.log').read_text()
        need(not any(t in log for t in ['Overfull','LaTeX Warning:','undefined references']),
             'Native layout or reference warning')
        subprocess.run(['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100',
                        '-sOutputFile='+str(out/'page-%02d.png'),str(out/'oriented_examples.pdf')],
                       check=True, capture_output=True, timeout=45)
        native = dict(pages=2, text_identical=True, direct_visual_review_still_required=True)
    report = dict(status='PASS_N010_ORIENTED_EXAMPLES', dependencies=len(dependencies),
                  exports=len(manifest['exports']), source_section=[2,4,5], native=native, finite=finite,
                  mathematical_proof_checked_by_this_program=False,
                  retained_proof_replays_repeated=False, new_Lean_declarations=0,
                  whole_original_credit=0, new_question_credit=0, new_measurements=0)
    (out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))

if __name__ == '__main__':
    main()
