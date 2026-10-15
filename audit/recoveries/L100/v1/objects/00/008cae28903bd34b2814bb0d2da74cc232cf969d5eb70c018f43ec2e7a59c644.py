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
            p=Path(r['path']);verify(p if p.is_absolute() else S/p,r)
    rehash();O.mkdir(parents=True)
    def run(name,cmd,cap=60,cwd=None):
        start=time.monotonic();code=None;deadline=False
        with (O/(name+'.stdout')).open('wb')as out,(O/(name+'.stderr')).open('wb')as err:
            try:q=subprocess.run(cmd,stdout=out,stderr=err,timeout=cap,cwd=cwd);code=q.returncode
            except subprocess.TimeoutExpired:deadline=True
        (O/(name+'.receipt.json')).write_text(json.dumps(dict(command=cmd,exit_code=code,deadline=deadline,cap_seconds=cap,seconds=time.monotonic()-start),indent=2)+'\n');need(code==0 and not (O/(name+'.stderr')).stat().st_size,'clean '+name)
    for name in ['replay','controls']:run(name,[sys.executable,str(P/(name+'.py')),'--out',str(O/name)])
    for r in read(P/'input_aliases.json'):verify(Path(r['original']),r);verify(P/r['copy'],r)
    first=read(P/'history/objects01/receipt.json');need(first['status']=='FAILED_PRESERVED'and first['exit_code']==1 and first['inputs_unchanged'],'exact weaker-definition uniqueness failure preserved')
    for name,status in [('objects02','COMPLETE_LITERAL_OBJECTS'),('recipes01','COMPLETE_LITERAL_MAPS'),('ovals01','COMPLETE_LITERAL_MAPS')]:
        r=read(P/'history'/name/'receipt.json');need(r['status']==status and r['exit_code']==0 and r['inputs_unchanged'],'exact complete finite construction receipt')
    guards=[]
    for script in ['objects','objects_v2','recipes','ovals','replay','controls','check']:
        for mode in ['argument','environment']:
            out=O/(script+'_'+mode+'_DENIED');env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
            if mode=='environment':env['PYTHONOPTIMIZE']='1'
            cmd=[sys.executable]+(['-O']if mode=='argument'else[])+[str(P/(script+'.py')),'--out',str(out)];q=subprocess.run(cmd,capture_output=True,env=env,timeout=5)
            need(q.returncode!=0 and b'normal Python required'in q.stderr and not out.exists(),'pre-output optimization guard');guards.append([script,mode])
    native=None
    if a.render:
        from pypdf import PdfReader
        N=O/'native';N.mkdir()
        for i in range(2):run('native'+str(i+1),['/opt/homebrew/bin/pdflatex','-halt-on-error','-interaction=nonstopmode','-output-directory',str(N),str(P/'constructions.tex')],30,P)
        log=(N/'constructions.log').read_text();need(not any(x in log for x in ['Warning','Overfull','Underfull']),'clean native log')
        old=PdfReader(P/'constructions.pdf');new=PdfReader(N/'constructions.pdf');need(len(old.pages)==len(new.pages)==4,'four full manuscript pages');need([p.extract_text()for p in old.pages]==[p.extract_text()for p in new.pages],'exact native page text');native=dict(pages=4,text_identical=True)
    rehash();r=dict(status='PASS_L100_BUTTERFLY_OVAL_COMPONENT',exports=len(M['exports']),dependencies=len(deps),replay=read(O/'replay/report.json'),controls=read(O/'controls/report.json'),optimization_guards=len(guards),native=native,new_censuses=0,whole_source_credit=0)
    (O/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
if __name__=='__main__':main()
