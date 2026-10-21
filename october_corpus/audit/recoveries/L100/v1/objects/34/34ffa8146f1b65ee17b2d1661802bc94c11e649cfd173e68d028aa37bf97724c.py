import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,hashlib,json,os,subprocess,time
from pathlib import Path
P=Path(__file__).resolve().parent
def need(v,s):
    if not v:raise ValueError(s)
def read(p):return json.loads(p.read_text())
def verify(p,r):
    b=p.read_bytes();need((len(b),hashlib.sha256(b).hexdigest())==(r['bytes'],r['sha256']),'exact binding '+str(p))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,default=P.parents[2]);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args();S=a.study.resolve();O=a.out.resolve();need(not O.exists(),'fresh output');M=read(P/'manifest.json');deps=read(P/'dependencies.json')
    def rehash():
        for r in M['exports']:verify(P/r['path'],r)
        for r in deps:
            p=Path(r['path']);verify(p if p.is_absolute()else S/p,r)
    rehash();O.mkdir(parents=True)
    def run(name,cmd,cap=60,cwd=None):
        t=time.monotonic();rc=None;deadline=False
        with(O/(name+'.stdout')).open('wb')as out,(O/(name+'.stderr')).open('wb')as err:
            try:r=subprocess.run(cmd,stdout=out,stderr=err,timeout=cap,cwd=cwd);rc=r.returncode
            except subprocess.TimeoutExpired:deadline=True
        (O/(name+'.receipt.json')).write_text(json.dumps(dict(command=cmd,cap_seconds=cap,exit_code=rc,deadline=deadline,seconds=time.monotonic()-t),indent=2)+'\n');need(rc==0 and not deadline and not(O/(name+'.stderr')).stat().st_size,'clean bounded '+name)
    def equal_timed(actual,expected):
        x=read(actual);y=read(expected);x.pop('seconds',None);y.pop('seconds',None);need(x==y,'exact scientific result '+str(actual))
    run('inventory',[sys.executable,str(P/'inventory.py'),'--out',str(O/'inventory')]);equal_timed(O/'inventory/inventory.json',P/'input01/inventory.json')
    run('atoms',[sys.executable,str(P/'atoms_v3.py'),'--out',str(O/'atoms')]);equal_timed(O/'atoms/report.json',P/'expected/atoms.json')
    run('kernels',[sys.executable,str(P/'kernels.py'),'--atoms',str(O/'atoms/report.json'),'--out',str(O/'kernels')]);equal_timed(O/'kernels/report.json',P/'expected/kernels.json')
    run('validate',[sys.executable,str(P/'validate.py'),'--atoms',str(O/'atoms/report.json'),'--kernels',str(O/'kernels/report.json'),'--out',str(O/'validate')]);need(read(O/'validate/report.json')==read(P/'expected/validation.json'),'literal witness controls')
    run('source_names',[sys.executable,str(P/'source_names.py'),'--atoms',str(O/'atoms/report.json'),'--kernels',str(O/'kernels/report.json'),'--out',str(O/'source_names.json')]);need(read(O/'source_names.json')==read(P/'source_names.json'),'complete native-source structural join')
    guards=[]
    for name in ['inventory','atoms_v3','kernels','validate','source_names','check']:
        for mode in ['argument','environment']:
            dst=O/(name+'_'+mode+'_DENIED');env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
            if mode=='environment':env['PYTHONOPTIMIZE']='1'
            cmd=[sys.executable]+(['-O']if mode=='argument'else[])+[str(P/(name+'.py')),'--out',str(dst)]
            r=subprocess.run(cmd,capture_output=True,env=env,timeout=5);need(r.returncode!=0 and b'normal Python required'in r.stderr and not dst.exists(),'pre-output optimization guard');guards.append([name,mode])
    native=None
    if a.render:
        from pypdf import PdfReader
        N=O/'native';N.mkdir()
        for i in range(2):run('native'+str(i+1),['/opt/homebrew/bin/pdflatex','-halt-on-error','-interaction=nonstopmode','-output-directory',str(N),str(P/'parabolics.tex')],30,P)
        log=(N/'parabolics.log').read_text();need(not any(x in log for x in ['Warning','Overfull','Underfull']),'clean native log');old=PdfReader(P/'parabolics.pdf');new=PdfReader(N/'parabolics.pdf');need(len(old.pages)==len(new.pages)==3,'three proof pages');need([p.extract_text()for p in old.pages]==[p.extract_text()for p in new.pages],'exact complete native texts');native=dict(pages=3,text_identical=True)
    rehash();r=dict(status='PASS_L100_PARABOLIC_KERNEL_COMPONENT',exports=len(M['exports']),dependencies=len(deps),atoms=77,parabolics=99,kernels=99,borels=29,kernel_certificates=61,damage_controls=len(read(O/'validate/report.json')['damage_controls'])+len(read(O/'source_names.json')['damage_controls']),optimization_guards=len(guards),native=native,target_censuses=0,whole_source_credit=0);(O/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r),flush=True)
if __name__=='__main__':main()
