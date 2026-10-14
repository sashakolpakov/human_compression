"""Replay one complete L027 component without claiming the whole original."""
import sys
if sys.flags.optimize:
    raise SystemExit('normal Python required')
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,time
from pypdf import PdfReader

P=Path(__file__).resolve().parent
def need(ok,message):
    if not ok:raise ValueError(message)
def digest(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def verify(p,row):
    need(digest(p)=={k:row[k] for k in ('bytes','sha256')},'changed input '+str(p))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();O=a.out.resolve()
    need(not O.exists(),'fresh output')
    manifest=json.loads((P/'manifest.json').read_text())
    for row in manifest['exports']:verify(P/row['path'],row)
    for row in json.loads((P/'dependencies.json').read_text()):verify(Path(row['path']),row)
    O.mkdir(parents=True);env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);records=[]
    def run(label,cmd,cap,cwd=None):
        start=time.monotonic();r=subprocess.run(cmd,cwd=cwd,capture_output=True,timeout=cap,env=env)
        (O/(label+'.stdout')).write_bytes(r.stdout);(O/(label+'.stderr')).write_bytes(r.stderr)
        row=dict(label=label,command=cmd,returncode=r.returncode,seconds=time.monotonic()-start)
        records.append(row);need(r.returncode==0,'execution '+label);return r
    run('symbolic',[sys.executable,str(P/'check_rank_four.py'),'--out',str(O/'symbolic.json')],30)
    need(json.loads((O/'symbolic.json').read_text())==json.loads((P/'symbolic_expected.json').read_text()),'exact symbolic controls')
    r=run('finite',['/opt/homebrew/bin/gap','-q','-b',str(P/'finite_rank_four.g')],120)
    need(not r.stderr,'clean GAP stderr');lines=[s.strip() for s in r.stdout.decode().splitlines() if s.strip()]
    need(lines==json.loads((P/'finite_expected.json').read_text()),'complete finite controls')
    N=O/'native';N.mkdir();shutil.copy2(P/'rank_four.tex',N/'rank_four.tex')
    for i in (1,2):run('latex'+str(i),['pdflatex','-halt-on-error','-interaction=nonstopmode','rank_four.tex'],30,N)
    log=(N/'rank_four.log').read_text();need(all(s not in log for s in ['Warning','Overfull','Underfull']),'clean native build')
    texts=lambda p:[page.extract_text() for page in PdfReader(p).pages]
    need(texts(N/'rank_four.pdf')==texts(P/'rank_four.pdf'),'native text identity')
    run('render',['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png','rank_four.pdf'],30,N)
    guards=[]
    for name in ['check.py','check_rank_four.py']:
        for mode in ['argument','environment']:
            ee=dict(env);cmd=[sys.executable];out=O/(name+'_'+mode)
            if mode=='argument':cmd+=['-O']
            else:ee['PYTHONOPTIMIZE']='1'
            r=subprocess.run([*cmd,str(P/name),'--out',str(out)],capture_output=True,env=ee,timeout=10)
            need(r.returncode!=0 and b'normal Python required' in r.stderr and not out.exists(),'optimization guard')
            guards.append([name,mode])
    report=dict(status='PASS_L027_RANK_FOUR_COMPONENT',exports=len(manifest['exports']),symbolic_identities=25,
                finite_fields=[5,7,8,9,13],guards=guards,native_pages=len(texts(N/'rank_four.pdf')),
                commands=records,whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None)
    (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
