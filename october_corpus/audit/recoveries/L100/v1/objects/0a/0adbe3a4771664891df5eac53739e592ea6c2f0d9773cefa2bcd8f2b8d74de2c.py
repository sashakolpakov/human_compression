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
    b=p.read_bytes();need(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],str(p))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args();O=a.out.absolute();need(not O.exists(),'fresh output')
    manifest=read(P/'manifest.json');deps=read(P/'dependencies.json')
    def rehash():
        for r in manifest['exports']:verify(P/r['path'],r)
        for r in deps:verify(Path(r['path']),r)
    rehash();O.mkdir(parents=True);receipts=[]
    def run(name,cmd,timeout=60,cwd=None):
        start=time.monotonic();q=subprocess.run(cmd,capture_output=True,timeout=timeout,cwd=cwd)
        (O/(name+'.stdout')).write_bytes(q.stdout);(O/(name+'.stderr')).write_bytes(q.stderr)
        r=dict(command=cmd,exit_code=q.returncode,elapsed_seconds=time.monotonic()-start)
        (O/(name+'.receipt.json')).write_text(json.dumps(r,indent=2)+'\n');receipts.append(r)
        need(q.returncode==0 and not q.stderr,'clean '+name);return q
    for name in ['literal_diagrams','construction_join','named_residues','transcribe_diagrams','controls']:
        run(name,[sys.executable,str(P/(name+'.py')),'--out',str(O/name)])
    need(read(O/'literal_diagrams/diagrams.json')['records']==read(P/'literal_diagrams01/diagrams.json')['records'],'all29 fresh literal residue tables')
    joins=read(O/'construction_join/joins.json');oldjoins=read(P/'construction_join03/joins.json')
    need(joins['routes']==oldjoins['routes'] and joins['duality']==oldjoins['duality'],'ten exact fresh construction maps')
    need(read(O/'named_residues/named_residues.json')['records']==read(P/'named_residues02/named_residues.json')['records'],'all52 exact fresh named/polarity maps')
    for name in ['diagram_inventory02','diagram_comparison01']:
        old=read(P/(name+'.json'))['rows'];fresh=read(O/'transcribe_diagrams'/(name+'.json'))['rows']
        if name=='diagram_inventory02':
            old=[{k:v for k,v in q.items()if k!='native_inputs'}for q in old];fresh=[{k:v for k,v in q.items()if k!='native_inputs'}for q in fresh]
        need(old==fresh,'fresh transcription/comparison '+name)
    guards=[]
    for script in ['literal_diagrams','construction_join','named_residues','transcribe_diagrams','controls','check']:
        for mode in ['argument','environment']:
            denied=O/(script+'_'+mode+'_DENIED');env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
            if mode=='environment':env['PYTHONOPTIMIZE']='1'
            cmd=[sys.executable]+(['-O']if mode=='argument'else[])+[str(P/(script+'.py')),'--out',str(denied)]
            q=subprocess.run(cmd,capture_output=True,env=env,timeout=5)
            need(q.returncode!=0 and b'normal Python required'in q.stderr and not denied.exists(),'optimization pre-output guard');guards.append([script,mode])
    native=None
    if a.render:
        from pypdf import PdfReader
        N=O/'native';N.mkdir()
        for i in range(2):run('native'+str(i+1),['/opt/homebrew/bin/pdflatex','-halt-on-error','-interaction=nonstopmode','-output-directory',str(N),str(P/'source_joins.tex')],30,P)
        log=(N/'source_joins.log').read_text();need(not any(x in log for x in ['Warning','Overfull','Underfull']),'clean final native log')
        original=PdfReader(P/'source_joins.pdf');new=PdfReader(N/'source_joins.pdf')
        need(len(original.pages)==len(new.pages)==2,'two native pages')
        need([p.extract_text()for p in original.pages]==[p.extract_text()for p in new.pages],'exact native page text');native=dict(pages=2,exact_page_text=True)
    rehash()
    report=dict(status='PASS_L100_SOURCE_DIAGRAM_JOIN_COMPONENT',exports=len(manifest['exports']),dependencies=len(deps),literal_models=29,
                named_residue_maps=52,construction_maps=10,controls=read(O/'controls/report.json'),guards=guards,native=native,
                target_runs=0,graph_classification_runs=0,source_credit=0)
    (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
