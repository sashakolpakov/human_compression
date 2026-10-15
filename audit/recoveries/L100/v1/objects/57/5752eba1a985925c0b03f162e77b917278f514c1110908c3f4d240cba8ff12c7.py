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
    b=p.read_bytes();need(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'exact binding '+str(p))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,default=P.parents[2]);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args();S=a.study.resolve();O=a.out.resolve();need(not O.exists(),'fresh output')
    m=read(P/'manifest.json');deps=read(P/'dependencies.json')
    def rehash():
        for r in m['exports']:verify(P/r['path'],r)
        for r in deps:
            p=Path(r['path']);verify(p if p.is_absolute() else S/p,r)
    rehash();O.mkdir(parents=True);runs=[]
    def run(name,cmd,cap=30,cwd=None):
        start=time.monotonic();q=subprocess.run(cmd,capture_output=True,timeout=cap,cwd=cwd)
        (O/(name+'.stdout')).write_bytes(q.stdout);(O/(name+'.stderr')).write_bytes(q.stderr)
        r=dict(command=cmd,exit_code=q.returncode,seconds=time.monotonic()-start)
        (O/(name+'.receipt.json')).write_text(json.dumps(r,indent=2)+'\n');runs.append(r);need(q.returncode==0 and not q.stderr,'clean '+name)
    roots=read(P/'acquired_roots.json')
    for r in roots:verify(S/r['path'],r)
    for r in read(P/'input_aliases.json'):
        original=Path(r['original']);verify(original,r);verify(P/r['copy'],r)
    for name in ['verify','controls']:run(name,[sys.executable,str(P/(name+'.py')),'--out',str(O/name)])
    # The adapted verifier imports the exact probe helper, not an edited predicate.
    need((P/'probe_engine.py').read_bytes()==(P/'history/certificate_v3.py').read_bytes(),'unchanged successful probe helper')
    receipt=read(P/'history/probe02_receipt/receipt.json')
    need(receipt['status']=='COMPLETE_LITERAL_CONSTRUCTION_PROBE' and receipt['returncode']==0 and receipt['inputs_unchanged'],'clean changed probe receipt')
    failed=read(P/'history/probe01_receipt/receipt.json')
    need(failed['status']=='FAILED_NO_COMPLETE_CERTIFICATE' and failed['returncode']!=0,'uncorrected failed join preserved')
    guards=[]
    for script in ['verify','controls','check','probe_engine']:
        for mode in ['argument','environment']:
            denied=O/(script+'_'+mode+'_DENIED');env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
            if mode=='environment':env['PYTHONOPTIMIZE']='1'
            cmd=[sys.executable]+(['-O']if mode=='argument'else[])+[str(P/(script+'.py')),'--out',str(denied)]
            q=subprocess.run(cmd,capture_output=True,env=env,timeout=5)
            need(q.returncode!=0 and b'normal Python required' in q.stderr and not denied.exists(),'optimization pre-output guard');guards.append([script,mode])
    native=None
    if a.render:
        from pypdf import PdfReader
        N=O/'native';N.mkdir()
        for i in range(2):run('native'+str(i+1),['/opt/homebrew/bin/pdflatex','-halt-on-error','-interaction=nonstopmode','-output-directory',str(N),str(P/'baer.tex')],30,P)
        log=(N/'baer.log').read_text();need(not any(x in log for x in ['Warning','Overfull','Underfull']),'clean native log')
        old=PdfReader(P/'baer.pdf');new=PdfReader(N/'baer.pdf');need(len(old.pages)==len(new.pages)==3,'three complete proof pages')
        need([p.extract_text()for p in old.pages]==[p.extract_text()for p in new.pages],'exact native page text');native=dict(pages=3,text_identical=True)
    rehash();report=dict(status='PASS_L100_BAER_CORRECTION_COMPONENT',exports=len(m['exports']),dependencies=len(deps),literal=read(O/'verify/report.json'),controls=read(O/'controls/report.json'),optimization_guards=len(guards),native=native,target_runs=0,subset_enumerations=0,whole_source_credit=0)
    (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
