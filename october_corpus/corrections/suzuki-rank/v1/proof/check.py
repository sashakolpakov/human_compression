#!/usr/bin/env python3
"""Replay the fixed construction, source bindings and native manuscript."""
import argparse,copy,hashlib,json,shutil,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent

def require(ok,message):
    if not ok:raise ValueError(message)

def load(name):return json.loads((HERE/name).read_text())
def binding(root,row):
    data=(root/row['path']).read_bytes()
    require(len(data)==row['bytes'],'byte count '+row['path'])
    require(hashlib.sha256(data).hexdigest()==row['sha256'],'hash '+row['path'])

def scope_check(s):
    require(s['whole_original_accepted'] is False,'author packet cannot accept itself')
    for key in ['new_original_credit','new_conjecture_credit','new_Lean','new_measurement']:
        require(s[key]==0,'credit overclaim '+key)
    require(s['finite_ambient_group_census_premises']==[],'ambient census premise')
    require(s['source_edition']=='arXiv:2010.04080v1, 8 October 2020','edition overclaim')
    require(s['group']=='Sz(32768)' and s['type']==[31,31,25],'construction scope')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--study-root',type=Path);ap.add_argument('--render',action='store_true');a=ap.parse_args()
    a.out.mkdir(parents=True,exist_ok=False)
    man=load('manifest.json')
    for row in man['exports']:binding(HERE,row)
    scope=load('scope.json');scope_check(scope);controls=[]
    for key,bad in [('whole_original_accepted',True),('new_original_credit',1),('new_conjecture_credit',1),('new_Lean',1),('new_measurement',1),('finite_ambient_group_census_premises',['unreviewed search']),('source_edition','all editions'),('type',[31,31,31])]:
        changed=copy.deepcopy(scope);changed[key]=bad
        try:scope_check(changed)
        except ValueError:controls.append(key)
        else:raise ValueError('scope control accepted '+key)
    external=0
    if a.study_root:
        for row in load('dependencies.json')['bindings']:binding(a.study_root,row);external+=1
    exact=subprocess.run([sys.executable,str(HERE/'check_arithmetic.py'),'--out',str(a.out.resolve()/'exact')],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60)
    (a.out/'exact.log').write_text(exact.stdout);require(exact.returncode==0,'arithmetic replay failed')
    result=json.loads((a.out/'exact/report.json').read_text());require(result==load('expected_arithmetic.json'),'arithmetic certificate changed')
    pages=None
    if a.render:
        from pypdf import PdfReader
        native=a.out/'native';native.mkdir();shutil.copyfile(HERE/'rank4_counterexample.tex',native/'rank4_counterexample.tex')
        for n in [1,2]:
            run=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','rank4_counterexample.tex'],cwd=native,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60)
            (native/('pass'+str(n)+'.log')).write_text(run.stdout);require(run.returncode==0,'native compilation failed')
        log=(native/'rank4_counterexample.log').read_text()
        for bad in ['Overfull','LaTeX Warning:','undefined references']:require(bad not in log,'native diagnostic '+bad)
        texts=[p.extract_text()or'' for p in PdfReader(native/'rank4_counterexample.pdf').pages]
        md=load('native.json');require(len(texts)==md['pages']==5,'page count')
        require([hashlib.sha256(t.encode()).hexdigest()for t in texts]==md['page_text_sha256'],'native page text changed');pages=len(texts)
    report={'status':'PASS','exports':len(man['exports']),'external_bindings':external,'scope_controls':controls,'native_pages':pages,'rotation_orders':result['orders'],'source_equation13_residual':result['source_diagnostic']['inadmissible_source_equation_residuals']['13'],'whole_original_accepted':False,'distinct_review':False}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
