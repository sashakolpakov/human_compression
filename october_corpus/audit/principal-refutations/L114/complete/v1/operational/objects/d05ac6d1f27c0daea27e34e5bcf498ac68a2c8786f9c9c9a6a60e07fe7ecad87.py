"""Replay the supplementary identities and complete native L110 boundary note."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Use ordinary Python')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess
from pypdf import PdfReader
P=Path(__file__).resolve().parent
def need(ok,message):
    if not ok:raise ValueError(message)
def verify(p,row):
    b=p.read_bytes()
    need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'Exact bound input '+str(p))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();O=a.out.resolve()
    need(not O.exists(),'Fresh output')
    for row in json.loads((P/'manifest.json').read_text())['exports']:verify(P/row['path'],row)
    for row in json.loads((P/'dependencies.json').read_text()):verify(Path(row['path']),row)
    O.mkdir(parents=True);env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
    def run(label,cmd,cwd=None):
        r=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,timeout=30)
        (O/(label+'.stdout')).write_bytes(r.stdout);(O/(label+'.stderr')).write_bytes(r.stderr)
        need(r.returncode==0 and not r.stderr,'Clean completed '+label)
    run('controls',[sys.executable,str(P/'controls.py'),str(O/'controls.json')])
    need(json.loads((O/'controls.json').read_text())==json.loads((P/'expected.json').read_text()),'Exact identities and arithmetic')
    N=O/'native';N.mkdir();shutil.copy2(P/'subfield_boundary.tex',N/'subfield_boundary.tex')
    for i in (1,2):run('latex'+str(i),['pdflatex','-halt-on-error','-interaction=nonstopmode','subfield_boundary.tex'],N)
    need(not any(s in (N/'subfield_boundary.log').read_text() for s in ['Warning','Overfull','Underfull']),'Clean native log')
    texts=lambda p:[page.extract_text() for page in PdfReader(p).pages]
    need(len(texts(N/'subfield_boundary.pdf'))==3 and texts(N/'subfield_boundary.pdf')==texts(P/'subfield_boundary.pdf'),'Complete native page identity')
    run('render',['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png','subfield_boundary.pdf'],N)
    guards=[]
    for f in ['check.py','controls.py']:
        for mode in ['argument','environment']:
            target=O/(f+'_'+mode);ee=dict(env);cmd=[sys.executable]
            if mode=='argument':cmd.append('-O')
            else:ee['PYTHONOPTIMIZE']='1'
            r=subprocess.run(cmd+[str(P/f),'--out',str(target)],capture_output=True,env=ee,timeout=10)
            need(r.returncode!=0 and b'Use ordinary Python' in r.stderr and not target.exists(),'Optimization guard');guards.append([f,mode])
    report=dict(status='PASS_L110_BOUNDARY_NOTE',native_pages=3,symbolic_identities=8,lattice_vertices=16,lattice_edges=32,field_meets=256,optimization_guards=guards,whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None,old_computations_repeated=False,group_enumerated=False)
    (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
