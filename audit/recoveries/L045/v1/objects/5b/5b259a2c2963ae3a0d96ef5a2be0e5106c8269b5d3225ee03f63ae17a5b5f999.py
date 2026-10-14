"""Bounded arithmetic and native verification for two written arguments."""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
import argparse,hashlib,json,os,shutil,subprocess,time
from pathlib import Path

def need(ok,msg):
    if not ok:raise ValueError(msg)

def pin(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true')
    a=ap.parse_args();P=Path(__file__).resolve().parent;O=a.out.resolve()
    need(not O.exists(),'fresh output required')
    exports=[]
    if(P/'manifest.json').exists():
        exports=json.loads((P/'manifest.json').read_text())['exports']
        for r in exports:need(pin(P/r['path'])=={k:r[k]for k in ('bytes','sha256')},'changed export '+r['path'])
    deps=json.loads((P/'dependencies.json').read_text())
    for r in deps:
        p=Path(r['path']);p=p if p.is_absolute()else a.study/p
        need(pin(p)=={k:r[k]for k in ('bytes','sha256')},'changed dependency '+str(p))
    O.mkdir(parents=True);env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
    receipts=[]
    def run(name,cmd,cwd,timeout=60):
        t=time.monotonic();z=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,timeout=timeout)
        (O/(name+'.stdout')).write_bytes(z.stdout);(O/(name+'.stderr')).write_bytes(z.stderr)
        r=dict(name=name,command=cmd,returncode=z.returncode,seconds=time.monotonic()-t,
               stdout=pin(O/(name+'.stdout')),stderr=pin(O/(name+'.stderr')))
        receipts.append(r);need(z.returncode==0 and not z.stderr,'clean '+name);return z
    z=run('arithmetic',[sys.executable,str(P/'check_bounds.py')],P)
    report=json.loads(z.stdout);need(report==json.loads((P/'arithmetic_expected.json').read_text()),'exact finite arithmetic record')
    native=[]
    for stem in ['triality','overgroups']:
        N=O/stem;N.mkdir();shutil.copy2(P/(stem+'.tex'),N/(stem+'.tex'))
        for i in range(2):run(stem+'_native'+str(i),['pdflatex','-halt-on-error','-interaction=nonstopmode',stem+'.tex'],N)
        log=(N/(stem+'.log')).read_text();need('Overfull'not in log and 'LaTeX Warning'not in log,'native layout/references '+stem)
        from pypdf import PdfReader
        pdf=PdfReader(N/(stem+'.pdf'));text='\n'.join(p.extract_text()or''for p in pdf.pages);(N/'text.txt').write_text(text)
        if(P/(stem+'_expected.txt')).exists():need(text==(P/(stem+'_expected.txt')).read_text(),'exact final text '+stem)
        if a.render:run(stem+'_render',['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r105','-sOutputFile=page-%02d.png',stem+'.pdf'],N)
        native.append(dict(manuscript=stem,pages=len(pdf.pages)))
    guards=[]
    for f in ['check.py','check_bounds.py']:
        for mode in ['argument','environment']:
            e=env.copy();cmd=[sys.executable]
            if mode=='argument':cmd.append('-O')
            else:e['PYTHONOPTIMIZE']='1'
            cmd.append(str(P/f));cmd+=['--study',str(a.study),'--out',str(O/'forbidden')]
            z=subprocess.run(cmd,env=e,capture_output=True,timeout=10)
            need(z.returncode!=0 and b'unoptimized execution required'in z.stderr and not(O/'forbidden').exists(),'early optimization guard')
            guards.append(dict(script=f,mode=mode,rejected=True))
    out=dict(status='PASS_ORTHOGONAL_COUNTING_COMPONENT',exports=len(exports),dependencies=len(deps),arithmetic=report,native=native,guards=guards,receipts=receipts,whole_original_credit=0,new_question_credit=0,new_Lean_credit=0,new_measurements=0,conditional_interface='Plus dimension eight still requires its complete maximal-overgroup cover; no finite control supplies that classification.')
    (O/'report.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items()if k not in ('arithmetic','receipts')}))

if __name__=='__main__':main()
