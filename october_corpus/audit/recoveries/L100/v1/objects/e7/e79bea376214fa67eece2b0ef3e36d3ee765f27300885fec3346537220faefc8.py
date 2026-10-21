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
    b=p.read_bytes();need((len(b),hashlib.sha256(b).hexdigest())==(r['bytes'],r['sha256']),'exact input '+str(p))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,default=P.parents[2]);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args();S=a.study.resolve();O=a.out.resolve();need(not O.exists(),'fresh output')
    M=read(P/'manifest.json');deps=read(P/'dependencies.json')
    def rehash():
        for r in M['exports']:verify(P/r['path'],r)
        for r in deps:
            p=Path(r['path']);verify(p if p.is_absolute()else S/p,r)
    rehash();O.mkdir(parents=True)
    def run(name,cmd,cap=30,cwd=None):
        t=time.monotonic();rc=None;deadline=False
        with(O/(name+'.stdout')).open('wb')as out,(O/(name+'.stderr')).open('wb')as err:
            try:r=subprocess.run(cmd,stdout=out,stderr=err,timeout=cap,cwd=cwd);rc=r.returncode
            except subprocess.TimeoutExpired:deadline=True
        (O/(name+'.receipt.json')).write_text(json.dumps(dict(command=cmd,cap_seconds=cap,exit_code=rc,deadline=deadline,seconds=time.monotonic()-t),indent=2)+'\n');need(rc==0 and not deadline and not(O/(name+'.stderr')).stat().st_size,'clean bounded '+name)
    run('assemble',[sys.executable,str(P/'assemble.py'),'--out',str(O/'join')])
    for n in ['claim_register.json','catalogue.json','execution_join.json','bibliography_routes.json','report.json']:
        need(read(O/'join'/n)==read(P/'expected'/n),'exact accepted interface join '+n)
    need((O/'join/catalogue.tex').read_bytes()==(P/'catalogue.tex').read_bytes(),'literal immediate native table')
    guards=[]
    for name in ['assemble','check']:
        for mode in ['argument','environment']:
            dst=O/(name+'_'+mode+'_DENIED');env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
            if mode=='environment':env['PYTHONOPTIMIZE']='1'
            cmd=[sys.executable]+(['-O']if mode=='argument'else[])+[str(P/(name+'.py')),'--out',str(dst)]
            r=subprocess.run(cmd,capture_output=True,env=env,timeout=5);need(r.returncode!=0 and b'normal Python required'in r.stderr and not dst.exists(),'pre-output optimization guard');guards.append([name,mode])
    native=None
    if a.render:
        from pypdf import PdfReader
        N=O/'native';N.mkdir()
        for i in range(2):run('native'+str(i+1),['/opt/homebrew/bin/pdflatex','-halt-on-error','-interaction=nonstopmode','-output-directory',str(N),str(P/'principal.tex')],30,P)
        log=(N/'principal.log').read_text();need(not any(x in log for x in ['Warning','Overfull','Underfull']),'clean native log');old=PdfReader(P/'principal.pdf');new=PdfReader(N/'principal.pdf');need(len(old.pages)==len(new.pages)==7,'seven proof pages');need([p.extract_text()for p in old.pages]==[p.extract_text()for p in new.pages],'exact full native texts');native=dict(pages=7,text_identical=True)
    rehash();out=dict(status='PASS_L100_PRINCIPAL_SYNTHESIS',exports=len(M['exports']),dependencies=len(deps),original_clauses=55,models=29,anchors=95,inner_families=145,corrections=6,retained_inputs=8,bibliography_attributions=47,damage_controls=16,optimization_guards=len(guards),native=native,target_censuses=0,new_measurements=0,new_Lean=0,new_question_credit=0,administrative_source_credit=0);(O/'report.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
