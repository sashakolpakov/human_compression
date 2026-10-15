"""Exact finite companion and complete native text, not a formal proof checker."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Normal Python is required')
sys.dont_write_bytecode=True
import argparse,hashlib,json,os,shutil,subprocess
from pathlib import Path

def need(ok,message):
    if not ok:raise ValueError(message)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--render',action='store_true');a=ap.parse_args()
    P=Path(__file__).resolve().parent;O=a.out.resolve()
    need(not O.exists() and not O.is_relative_to(P),'Fresh external output')
    m=json.loads((P/'manifest.json').read_text())
    def check(p,row):
        b=p.read_bytes();need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'Changed input '+str(p))
    for r in m['exports']:check(P/r['path'],r)
    deps=json.loads((P/'dependencies.json').read_text())
    for r in deps:check(Path(r['path']),r)
    O.mkdir(parents=True);env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
    p=subprocess.run([sys.executable,str(P/'affine_quotient.py'),str(O/'literal.json')],capture_output=True,env=env,timeout=30)
    (O/'literal.stdout').write_bytes(p.stdout);(O/'literal.stderr').write_bytes(p.stderr)
    need(p.returncode==0 and not p.stderr,'Fresh exact matrix calculation')
    need(json.loads((O/'literal.json').read_text())==json.loads((P/'literal01.json').read_text()),'Exact certificate agreement')
    guards=[]
    for script in ['check.py','affine_quotient.py']:
        p=subprocess.run([sys.executable,'-O',str(P/script)],capture_output=True,timeout=15)
        need(p.returncode!=0 and b'Normal Python is required' in p.stderr,'Optimization guard')
        guards.append(script)
    from pypdf import PdfReader
    expected=[p.extract_text() for p in PdfReader(P/'quotient_kernels.pdf').pages]
    need(len(expected)==3,'Full three-page note')
    native=False
    if a.render:
        N=O/'native';N.mkdir();shutil.copy2(P/'quotient_kernels.tex',N/'quotient_kernels.tex')
        for k in range(2):
            p=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','quotient_kernels.tex'],cwd=N,capture_output=True,timeout=60)
            (N/f'build{k}.stdout').write_bytes(p.stdout);(N/f'build{k}.stderr').write_bytes(p.stderr)
            need(p.returncode==0 and not p.stderr,'Complete native compilation')
        log=(N/'quotient_kernels.log').read_text()
        need(not any(x in log for x in ['Overfull','Underfull','LaTeX Warning']),'Clean native layout')
        need([p.extract_text() for p in PdfReader(N/'quotient_kernels.pdf').pages]==expected,'Exact full native text')
        p=subprocess.run(['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r90','-sOutputFile=page-%02d.png','quotient_kernels.pdf'],cwd=N,capture_output=True,timeout=60)
        (N/'render.stderr').write_bytes(p.stderr)
        need(p.returncode==0 and not p.stderr and len(list(N.glob('page-*.png')))==3,'Three rendered pages')
        native=True
    report=dict(status='PASS_L033_AFFINE_QUOTIENT_COMPONENT',exports=len(m['exports']),dependencies=len(deps),matrix_certificate=True,native_pages=3 if native else None,optimization_guards=guards,whole_original_credit=0,new_question_credit=0,new_Lean_declarations=0,infinite_geometry_requires_written_proof=True)
    (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':main()
