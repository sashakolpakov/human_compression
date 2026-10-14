"""Replay the complete survey's interfaces and native manuscript."""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
import argparse,copy,hashlib,json,os,shutil,subprocess,time
from pathlib import Path
from verify_contract import verify,need,check_marking,source_check
P=Path(__file__).resolve().parent

def load(p):return json.loads(p.read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def pin(p):
    h=hashlib.sha256();size=0
    with p.open('rb')as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b);size+=len(b)
    return dict(bytes=size,sha256=h.hexdigest())
def checkpin(p,x):need(pin(p)=={k:x[k]for k in ('bytes','sha256')},'exact input '+str(p))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path,required=True);ap.add_argument('--repo',type=Path);ap.add_argument('--gap-root',type=Path);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--source-tex',type=Path);ap.add_argument('--render',action='store_true');a=ap.parse_args()
    S=a.study.resolve();R=(a.repo or S.parents[1]/'math_compression').resolve();O=a.out.resolve();need(not O.exists(),'fresh output required')
    roots={'study':S,'public':R,'gap':(a.gap_root or Path('/opt/homebrew/bin/gap').resolve().parent.parent).resolve()}
    exports=[]
    if(P/'manifest.json').exists():
        exports=load(P/'manifest.json')['exports']
        for x in exports:checkpin(P/x['path'],x)
    deps=load(P/'dependencies.json')['files']
    for x in deps:checkpin(roots[x['namespace']]/x['path'],x)
    O.mkdir(parents=True);env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
    result=verify(P,S,source_tex=a.source_tex)
    expected=load(P/'expected.json');need({k:v for k,v in result.items()if k!='source_replay'}=={k:v for k,v in expected.items()if k!='source_replay'},'complete interface result')
    save(O/'interfaces.json',result)
    scope=load(P/'survey_table_scope09.json');clauses=load(P/'named_clause_register03.json');figure=load(P/'survey_figure_records01.json');bad=[]
    x=copy.deepcopy(scope);x['rows'].pop();bad.append(('missing_source_cell',lambda:verify(P,S,scope=x)))
    y=copy.deepcopy(scope);y['rows'][0]['comparison_value']+=1;bad.append(('changed_acquired_count',lambda:verify(P,S,scope=y)))
    z=copy.deepcopy(scope);next(r for r in z['rows']if r['disposition']=='retained_independent_published_classification')['disposition']='acquired_project_result';bad.append(('promoted_retained_classification',lambda:verify(P,S,scope=z)))
    c=copy.deepcopy(clauses);c['clauses'].pop();bad.append(('missing_source_question',lambda:verify(P,S,clauses=c)))
    f=copy.deepcopy(figure);f['records'][0]['to_model']['point_map'][0],f['records'][0]['to_model']['point_map'][1]=f['records'][0]['to_model']['point_map'][1],f['records'][0]['to_model']['point_map'][0];bad.append(('wrong_diagram_transport',lambda:verify(P,S,figure=f)))
    m=copy.deepcopy(load(P/'table_interfaces01.json')['table4_literal_controls'][0]);m['marks'][0][0]=999;bad.append(('invalid_construction_literal',lambda:check_marking(m['marks'],m['degree'],m['type'])))
    negative=[]
    for name,action in bad:
        try:action()
        except ValueError as e:negative.append(dict(case=name,rejected=True,message=str(e)))
        else:raise ValueError('damaged interface passed '+name)
    save(O/'negative_controls.json',negative)
    guards=[]
    for script in ('check.py','verify_contract.py'):
        for mode in ('argument','environment'):
            e=env.copy();cmd=[sys.executable]
            if mode=='argument':cmd.append('-O')
            else:e['PYTHONOPTIMIZE']='1'
            dest=O/(script+'_'+mode+'_forbidden');cmd.extend([str(P/script),'--out',str(dest)]);z=subprocess.run(cmd,capture_output=True,timeout=10,env=e)
            (O/(script+'_'+mode+'.stderr')).write_bytes(z.stderr);need(z.returncode!=0 and b'unoptimized execution required'in z.stderr and not dest.exists(),'optimization pre-output rejection');guards.append(dict(script=script,mode=mode,rejected=True))
    save(O/'optimization_guards.json',guards)
    pages=None
    if a.render:
        N=O/'native';N.mkdir();shutil.copy2(P/'survey.tex',N/'survey.tex')
        for i in range(2):
            cmd=['pdflatex','-halt-on-error','-interaction=nonstopmode','survey.tex'];start=time.monotonic();z=subprocess.run(cmd,cwd=N,env=env,capture_output=True,timeout=60);(N/f'build{i}.stdout').write_bytes(z.stdout);(N/f'build{i}.stderr').write_bytes(z.stderr);save(N/f'build{i}.json',dict(command=cmd,returncode=z.returncode,seconds=time.monotonic()-start));need(z.returncode==0 and not z.stderr,'native build')
        log=(N/'survey.log').read_text();need('Overfull'not in log and 'LaTeX Warning'not in log,'native layout/reference warnings')
        from pypdf import PdfReader
        pdf=PdfReader(N/'survey.pdf');pages=len(pdf.pages);text='\n'.join(p.extract_text()or''for p in pdf.pages);(N/'text.txt').write_text(text)
        if(P/'native_expected.txt').exists():need(text==(P/'native_expected.txt').read_text(),'exact final native text')
        z=subprocess.run(['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r105','-sOutputFile=page-%02d.png','survey.pdf'],cwd=N,capture_output=True,timeout=60);need(z.returncode==0,'native rendering')
    report=dict(status='PASS_L120_PRINCIPAL_ASSEMBLY',exports=len(exports),dependencies=len(deps),interfaces=result,damaged_controls=len(negative),optimization_guards=len(guards),native_pages=pages,new_census=False,whole_original_credit=0,new_question_credit=0,new_Lean_credit=0,new_measurements=0)
    save(O/'report.json',report);print(json.dumps(report))
if __name__=='__main__':main()
