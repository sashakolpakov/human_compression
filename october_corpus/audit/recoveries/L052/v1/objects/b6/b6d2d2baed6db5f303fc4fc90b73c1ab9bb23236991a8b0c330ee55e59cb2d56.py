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
    need(scope['source_id'] == 'L052' and scope['written_pages'] == 8, 'Written source scope')
    expected = ['2.1','2.2','3.1','3.2','3.3','3.4','3.5','4.1','4.2','4.3',
                '4.6','5.1','5.2','6.1','6.2','7.1','7.2','8.1','8.2']
    need([r['source_clause'] for r in scope['clauses']] == expected, 'Exact nineteen clauses')
    need(scope['retained_source_theorems'] == ['5.1: marked string C-group correspondence'],
         'Retained source theorem remains explicit')
    need(scope['two_chamber_orbits_assumed'] and scope['faithfulness_qualification_explicit'],
         'Necessary geometric hypotheses')
    need(all(scope[k] == 0 for k in ['whole_original_credit','new_question_credit',
                                   'new_Lean_declarations','new_measurements']), 'Component boundary')
    out.mkdir(parents=True)
    native = None
    if a.render:
        from pypdf import PdfReader
        shutil.copy2(base/'residue_theory.tex', out/'residue_theory.tex')
        for n in [1,2]:
            p = subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',
                                'residue_theory.tex'], cwd=out, capture_output=True, timeout=45)
            (out/f'native{n}.stdout').write_bytes(p.stdout)
            (out/f'native{n}.stderr').write_bytes(p.stderr)
            need(p.returncode == 0, 'Native build failed')
        text = lambda p: [page.extract_text() for page in PdfReader(p).pages]
        got = text(out/'residue_theory.pdf')
        need(len(got) == 8 and got == text(base/'residue_theory.pdf'), 'Exact native text and pages')
        log = (out/'residue_theory.log').read_text()
        need(not any(t in log for t in ['Overfull','LaTeX Warning:','undefined references']),
             'Native layout or reference warning')
        subprocess.run(['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100',
                        '-sOutputFile='+str(out/'page-%02d.png'),str(out/'residue_theory.pdf')],
                       check=True, capture_output=True, timeout=45)
        native = dict(pages=8, text_identical=True, direct_visual_review_still_required=True)
    report = dict(status='PASS_L052_WRITTEN_COMPONENT_BINDINGS', dependencies=len(dependencies),
                  exports=len(manifest['exports']), source_clauses=19, native=native,
                  mathematical_proof_checked_by_this_program=False,
                  retained_proof_replays_repeated=False, new_Lean_declarations=0,
                  whole_original_credit=0, new_question_credit=0, new_measurements=0)
    (out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))

if __name__ == '__main__':
    main()
