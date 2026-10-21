import sys
if sys.flags.optimize:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,hashlib,json,subprocess,time,os
from pathlib import Path
P=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def need(v,m):
    if not v:raise ValueError(m)
def exact(r,p=None):
    b=Path(p or r['path']).read_bytes();need(len(b)==r['bytes']and hashlib.sha256(b).hexdigest()==r['sha256'],'exact binding '+str(p or r['path']))
def main():
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--render',action='store_true');v=a.parse_args();O=v.out;need(O.is_absolute()and not O.exists(),'fresh absolute output');M=read(P/'manifest.json');D=read(P/'dependencies.json')
    def rehash():
        for r in M['exports']:
            q=Path(r['path']);need(not q.is_absolute()and '..'not in q.parts,'safe packet export');exact(r,P/q)
        for r in D:exact(r)
    rehash();O.mkdir()
    def run(name,cmd,cap=30,cwd=None):
        t=time.monotonic();rc=None;deadline=False
        with(O/(name+'.stdout')).open('wb')as f,(O/(name+'.stderr')).open('wb')as e:
            try:rc=subprocess.run(cmd,stdout=f,stderr=e,cwd=cwd,timeout=cap).returncode
            except subprocess.TimeoutExpired:deadline=True
        r=dict(command=cmd,cap_seconds=cap,exit_code=rc,deadline=deadline,seconds=time.monotonic()-t,target_census=False)
        (O/(name+'.receipt.json')).write_text(json.dumps(r,indent=2)+'\n');need(rc==0 and not deadline and not(O/(name+'.stderr')).stat().st_size,'clean bounded call '+name)
    run('join',[sys.executable,str(P/'prepare.py'),'--out',str(O/'join')])
    for n in ['components.json','claim_register.json','bibliography_routes.json','named_rows.json','minima.json','report.json']:
        need(read(O/'join'/n)==read(P/'expected'/n),'exact acquired source join '+n)
    for n in ['named_table.tex','minimum_table.tex']:need((O/'join'/n).read_bytes()==(P/n).read_bytes(),'literal native input '+n)
    run('small',[sys.executable,str(P/'joins.py'),'--out',str(O/'small')]);need(read(O/'small/report.json')==read(P/'small_report.json'),'small elementary controls')
    run('contract',[sys.executable,str(P/'validate.py'),'--join',str(O/'join'),'--out',str(O/'contract')]);need(read(O/'contract/report.json')['damage_controls']==18,'18 actual ledger damages')
    guards=[]
    for name in ['check','prepare','joins','validate']:
        for envmode in [False,True]:
            dst=O/(name+('_env'if envmode else'_arg')+'_DENIED');env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
            if envmode:env['PYTHONOPTIMIZE']='1'
            cmd=[sys.executable]+([]if envmode else['-O'])+[str(P/(name+'.py')),'--out',str(dst)]
            if name=='validate':cmd+=['--join',str(O/'join')]
            r=subprocess.run(cmd,capture_output=True,timeout=5,env=env);need(r.returncode!=0 and b'normal Python required'in r.stderr and not dst.exists(),'optimization guard');guards.append([name,envmode])
    from pypdf import PdfReader
    vol=read(P/'volume.json');pages=[];streams=[]
    for entry in vol['entries']:
        p=P/'principal.pdf'if entry['component']=='principal'else Path(entry['input']['path']);exact(entry['input'],p);z=PdfReader(p)
        need(len(z.pages)==entry['pages']and entry['first_page']==len(pages)+1,'volume page route');pages.extend(t.extract_text()for t in z.pages);streams.extend(t.get_contents().get_data()for t in z.pages)
    actual=PdfReader(P/'complete_proofs.pdf');need(len(pages)==vol['pages']and [x.extract_text()for x in actual.pages]==pages and [x.get_contents().get_data()for x in actual.pages]==streams,'full reading volume text/content identity')
    native=None
    if v.render:
        N=O/'native';N.mkdir()
        for i in range(2):run('native'+str(i+1),['/opt/homebrew/bin/pdflatex','-halt-on-error','-interaction=nonstopmode','-output-directory',str(N),str(P/'principal.tex')],30,P)
        log=(N/'principal.log').read_text();need(not any(x in log for x in ['Warning','Overfull','Underfull','Infinite glue']),'clean native log')
        a=PdfReader(P/'principal.pdf');b=PdfReader(N/'principal.pdf');need(len(a.pages)==len(b.pages)==9 and [x.extract_text()for x in a.pages]==[x.extract_text()for x in b.pages],'nine exact native pages')
        run('raster',['/opt/homebrew/bin/gs','-q','-dNOPAUSE','-dBATCH','-sDEVICE=png16m','-r100','-sOutputFile='+str(N/'page-%02d.png'),str(N/'principal.pdf')])
        need(all((N/('page-%02d.png'%i)).read_bytes()==(P/'native_author'/('page-%02d.png'%i)).read_bytes()for i in range(1,10)),'all9 native raster identities');native=dict(pages=9,text_identical=True,rasters_identical=True)
    rehash();r=dict(status='PASS_L033_COMPLETE_SOURCE_SYNTHESIS',exports=len(M['exports']),dependencies=len(D),source_clauses=109,component_manuscripts=12,complete_proof_pages=vol['pages'],source_named_positives=22,excluded_rows=4,minimum_interfaces=9,retained_premises=8,correction_groups=7,bibliography_entries=29,damage_controls=18,optimization_guards=len(guards),native=native,new_target_censuses=0,new_Lean=0,new_measurements=0,new_question_credit=0,public_admission=False)
    (O/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
if __name__=='__main__':main()
