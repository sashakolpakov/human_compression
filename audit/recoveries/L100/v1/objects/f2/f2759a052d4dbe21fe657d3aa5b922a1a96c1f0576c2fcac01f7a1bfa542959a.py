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
    ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,default=P.parents[2]);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args();S=a.study.resolve();O=a.out.resolve();need(not O.exists(),'fresh output')
    M=read(P/'manifest.json');deps=read(P/'dependencies.json')
    def rehash():
        for r in M['exports']:verify(P/r['path'],r)
        for r in deps:
            p=Path(r['path']);verify(p if p.is_absolute()else S/p,r)
    rehash();O.mkdir(parents=True)
    def run(name,cmd,cap=60,cwd=None):
        start=time.monotonic();code=None;deadline=False
        with(O/(name+'.stdout')).open('wb')as out,(O/(name+'.stderr')).open('wb')as err:
            try:r=subprocess.run(cmd,stdout=out,stderr=err,timeout=cap,cwd=cwd);code=r.returncode
            except subprocess.TimeoutExpired:deadline=True
        (O/(name+'.receipt.json')).write_text(json.dumps(dict(command=cmd,cap_seconds=cap,exit_code=code,deadline=deadline,seconds=time.monotonic()-start),indent=2)+'\n');need(code==0 and not deadline and not(O/(name+'.stderr')).stat().st_size,'clean bounded '+name)
    models=','.join(str(i)for i in range(1,30))
    run('structures',[sys.executable,str(P/'automorphism_names.py'),'--out',str(O/'structures'),'--models',models])
    for i in range(1,30):need(read(O/f'structures/model{i}.json')==read(P/f'expected/model{i}.json'),'exact literal structure witness')
    run('validate',[sys.executable,str(P/'validate.py'),'--results',str(O/'structures'),'--out',str(O/'validate')])
    need(read(O/'validate/report.json')==read(P/'expected/validation.json'),'exact independent-witness controls and invariants')
    run('source_join',[sys.executable,str(P/'source_names.py'),'--results',str(O/'structures'),'--out',str(O/'source_names.json')])
    actual=read(O/'source_names.json');expected=read(P/'source_names.json');actual.pop('inputs');expected.pop('inputs');need(actual==expected,'exact full source name join')
    guards=[]
    for name in ['automorphism_names','validate','source_names','check']:
        for mode in ['argument','environment']:
            dst=O/(name+'_'+mode+'_DENIED');env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
            if mode=='environment':env['PYTHONOPTIMIZE']='1'
            cmd=[sys.executable]+(['-O']if mode=='argument'else[])+[str(P/(name+'.py')),'--out',str(dst)]
            r=subprocess.run(cmd,capture_output=True,env=env,timeout=5);need(r.returncode!=0 and b'normal Python required'in r.stderr and not dst.exists(),'pre-output guard');guards.append([name,mode])
    native=None
    if a.render:
        from pypdf import PdfReader
        N=O/'native';N.mkdir()
        for i in range(2):run('native'+str(i+1),['/opt/homebrew/bin/pdflatex','-halt-on-error','-interaction=nonstopmode','-output-directory',str(N),str(P/'structures.tex')],30,P)
        log=(N/'structures.log').read_text();need(not any(x in log for x in ['Warning','Overfull','Underfull']),'clean native log')
        old=PdfReader(P/'structures.pdf');new=PdfReader(N/'structures.pdf');need(len(old.pages)==len(new.pages)==3,'three complete proof pages');need([p.extract_text()for p in old.pages]==[p.extract_text()for p in new.pages],'exact native page texts');native=dict(pages=3,text_identical=True)
    rehash();r=dict(status='PASS_L100_AUT_COR_STRUCTURE_COMPONENT',exports=len(M['exports']),dependencies=len(deps),models=29,groups=58,split_central_factors=5,validation=read(O/'validate/report.json'),optimization_guards=len(guards),native=native,target_censuses=0,whole_source_credit=0)
    (O/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r),flush=True)
if __name__=='__main__':main()
