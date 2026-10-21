"""Replay the finite supplement and bind the complete written argument."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse, hashlib, json, os, shutil, subprocess
from pypdf import PdfReader
P=Path(__file__).resolve().parent
def pin(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args()
    out=a.out.resolve();assert not out.exists()
    manifest=json.loads((P/'manifest.json').read_text())
    for r in manifest['exports']:assert pin(P/r['path'])=={k:r[k]for k in ['bytes','sha256']}
    deps=json.loads((P/'dependencies.json').read_text())
    for r in deps:assert pin(a.study/r['path'])=={k:r[k]for k in ['bytes','sha256']}
    out.mkdir(parents=True)
    def run(name,cmd,cwd=None):
        p=subprocess.run(cmd,cwd=cwd,capture_output=True,timeout=30)
        (out/(name+'.stdout')).write_bytes(p.stdout);(out/(name+'.stderr')).write_bytes(p.stderr)
        assert p.returncode==0 and not p.stderr
        return p
    run('finite',[sys.executable,'-B',str(P/'finite.py'),'--out',str(out/'finite.json')])
    got=json.loads((out/'finite.json').read_text());assert got==json.loads((P/'expected.json').read_text())
    guards=[]
    for script in ['check.py','finite.py']:
        for mode in ['argument','environment']:
            env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);cmd=[sys.executable]
            if mode=='argument':cmd+=['-O']
            else:env['PYTHONOPTIMIZE']='1'
            p=subprocess.run(cmd+[str(P/script)],env=env,capture_output=True,timeout=10)
            assert p.returncode!=0 and b'Ordinary Python required'in p.stderr and not p.stdout
            guards.append([script,mode])
    native=None
    if a.render:
        nd=out/'native';nd.mkdir();shutil.copyfile(P/'subfield_planes.tex',nd/'subfield_planes.tex')
        for i in [1,2]:run('latex'+str(i),['pdflatex','-interaction=nonstopmode','-halt-on-error','subfield_planes.tex'],nd)
        log=(nd/'subfield_planes.log').read_text()
        assert all(x not in log for x in ['Warning','Overfull','Underfull'])
        pages=PdfReader(nd/'subfield_planes.pdf').pages;old=PdfReader(P/'subfield_planes.pdf').pages
        assert len(pages)==len(old)==3
        assert [x.extract_text()for x in pages]==[x.extract_text()for x in old]
        run('images',['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=pnggray','-r105','-sOutputFile=page-%02d.png','subfield_planes.pdf'],nd)
        native=dict(pages=3,text_identical=True)
    report=dict(status='PASS_PROJECTIVE_SUBFIELD_PLANES_COMPONENT',finite_models=len(got['models']),
        exports=len(manifest['exports']),dependencies=len(deps),native=native,optimization_guards=guards,
        general_proof_verified_by_program=False,whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
