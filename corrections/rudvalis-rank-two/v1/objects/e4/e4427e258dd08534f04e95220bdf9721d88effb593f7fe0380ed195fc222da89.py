import sys
if sys.flags.optimize:
    raise SystemExit('Ordinary Python required')
import argparse,hashlib,json,os,shutil,subprocess,time
from pathlib import Path
from pypdf import PdfReader
P=Path(__file__).resolve().parent
def need(ok,msg):
    if not ok:raise ValueError(msg)
def pin(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();o=a.out.resolve()
    need(not o.exists()and P not in o.parents,'fresh external output')
    m=json.loads((P/'manifest.json').read_text());deps=json.loads((P/'dependencies.json').read_text())
    for x in m['exports']:need(pin(P/x['path'])=={k:x[k]for k in ['bytes','sha256']},'frozen export')
    for x in deps:need(pin(Path(x['path']))=={k:x[k]for k in ['bytes','sha256']},'frozen source')
    o.mkdir(parents=True);env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);commands=[]
    def run(label,cmd,cwd=None):
        start=time.monotonic();r=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,timeout=45)
        (o/(label+'.stdout')).write_bytes(r.stdout);(o/(label+'.stderr')).write_bytes(r.stderr)
        commands.append(dict(label=label,command=cmd,returncode=r.returncode,seconds=time.monotonic()-start))
        need(r.returncode==0 and not r.stderr,'clean '+label)
    run('arithmetic',[sys.executable,'-B',str(P/'arithmetic.py'),'--out',str(o/'arithmetic.json')])
    need(json.loads((o/'arithmetic.json').read_text())==json.loads((P/'expected.json').read_text()),'complete exact result')
    guards=[]
    for program in ['check.py','arithmetic.py']:
        for mode in ['argument','environment']:
            ee=dict(env);target=o/(program+'_'+mode);cmd=[sys.executable]
            if mode=='argument':cmd.append('-O')
            else:ee['PYTHONOPTIMIZE']='1'
            r=subprocess.run(cmd+[str(P/program),'--out',str(target)],env=ee,capture_output=True,timeout=10)
            need(r.returncode!=0 and b'Ordinary Python required'in r.stderr and not target.exists(),'optimization guard');guards.append([program,mode])
    n=o/'native';n.mkdir();shutil.copyfile(P/'orbit_bound.tex',n/'orbit_bound.tex')
    for i in [1,2]:run('latex'+str(i),['pdflatex','-halt-on-error','-interaction=nonstopmode','orbit_bound.tex'],n)
    need(not any(s in(n/'orbit_bound.log').read_text()for s in ['Warning','Overfull','Underfull']),'clean native')
    texts=lambda f:[p.extract_text()for p in PdfReader(f).pages]
    need(texts(n/'orbit_bound.pdf')==texts(P/'orbit_bound.pdf'),'exact native text')
    run('render',['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png','orbit_bound.pdf'],n)
    result=dict(status='PASS_L036_PRINCIPAL_BOUND',exports=len(m['exports']),dependencies=len(deps),native_pages=len(texts(n/'orbit_bound.pdf')),guards=guards,commands=commands,lower_bound=50669,refuted_fixed_total=1511,whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None)
    (o/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
