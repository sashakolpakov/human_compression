"""Supplementary field controls and native build for the Suzuki subspace proof."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Use ordinary Python')
sys.dont_write_bytecode = True
from pathlib import Path
import argparse, hashlib, importlib.util, json, os, shutil, subprocess, time
from pypdf import PdfReader

P = Path(__file__).resolve().parent
def need(ok, message):
    if not ok:
        raise ValueError(message)
def pin(p):
    b = p.read_bytes()
    return dict(bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    O = a.out.resolve()
    need(not O.exists(), 'Fresh output required')
    m = json.loads((P/'manifest.json').read_text())
    for row in m['exports']:
        need(pin(P/row['path']) == {k:row[k] for k in ('bytes','sha256')}, 'Exact export')
    for row in json.loads((P/'dependencies.json').read_text()):
        need(pin(Path(row['path'])) == {k:row[k] for k in ('bytes','sha256')}, 'Exact retained source or provenance')
    O.mkdir(parents=True)
    env = dict(os.environ)
    env.pop('PYTHONOPTIMIZE', None)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    commands = []
    def run(label, cmd, cap=30, cwd=None):
        start = time.monotonic()
        r = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, timeout=cap)
        (O/(label+'.stdout')).write_bytes(r.stdout)
        (O/(label+'.stderr')).write_bytes(r.stderr)
        commands.append(dict(label=label, command=cmd, exit_code=r.returncode, seconds=time.monotonic()-start))
        need(r.returncode == 0 and not r.stderr, 'Clean completed call '+label)
        return r
    run('fields', [sys.executable, str(P/'center_orbits.py'), str(O/'fields.json')])
    fields = json.loads((O/'fields.json').read_text())
    need(fields == json.loads((P/'expected.json').read_text()), 'Exact supplementary field counts')
    spec = importlib.util.spec_from_file_location('field_control', P/'center_orbits.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    damages = []
    for n, f in [(9,(1<<9)|1),(15,(1<<15)|1)]:
        try:
            module.run(n,f)
        except ValueError as exc:
            need(str(exc) in ['Frobenius identity','Rabin irreducibility'], 'Polynomial rejected at field construction')
            damages.append(dict(n=n, modulus=f, rejection=str(exc)))
        else:
            raise ValueError('Reducible polynomial accepted')
    N = O/'native'
    N.mkdir()
    shutil.copy2(P/'central_covers.tex', N/'central_covers.tex')
    for i in (1,2):
        run('latex'+str(i), ['pdflatex','-halt-on-error','-interaction=nonstopmode','central_covers.tex'], cwd=N)
    log = (N/'central_covers.log').read_text()
    need(not any(s in log for s in ['Warning','Overfull','Underfull']), 'Clean native log')
    texts = lambda p: [page.extract_text() for page in PdfReader(p).pages]
    need(len(texts(N/'central_covers.pdf')) == 4, 'Complete four-page proof')
    need(texts(N/'central_covers.pdf') == texts(P/'central_covers.pdf'), 'Exact native page texts')
    run('render', ['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png','central_covers.pdf'], cwd=N)
    guards = []
    for name in ['check.py','center_orbits.py']:
        for mode in ['argument','environment']:
            target = O/(name+'_'+mode)
            cmd = [sys.executable]
            ee = dict(env)
            if mode == 'argument':
                cmd.append('-O')
            else:
                ee['PYTHONOPTIMIZE'] = '1'
            r = subprocess.run(cmd+[str(P/name),'--out',str(target)], env=ee, capture_output=True, timeout=10)
            need(r.returncode != 0 and b'Use ordinary Python' in r.stderr and not target.exists(), 'Pre-output optimization guard')
            guards.append([name, mode])
    report = dict(status='PASS_L115_SCALAR_SUBSPACE_COMPONENT', fields=[r['q'] for r in fields['cases']],
                  scalar_subspaces=[9,585], automorphism_orbits=[1,41], polynomial_damages=damages,
                  guards=guards, native_pages=4, commands=commands, whole_original_credit=0,
                  new_question_credit=0, new_Lean=0, measurement=None,
                  general_proof_verified_by_program=False, old_matrix_census_repeated=False)
    (O/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))
if __name__ == '__main__':
    main()
