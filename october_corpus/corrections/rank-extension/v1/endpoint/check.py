#!/usr/bin/env python3
"""Bounded literal counterexample replay; no source-level formal proof claim."""
import argparse,hashlib,json,re,shutil,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def run(cmd,cwd=None):
    p=subprocess.run(list(map(str,cmd)),cwd=cwd,text=True,capture_output=True,timeout=90)
    return p.returncode,p.stdout+p.stderr

def main():
    p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,default=ROOT.parent);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--gap',default='/opt/homebrew/bin/gap');p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');p.add_argument('--render',action='store_true');a=p.parse_args()
    need(not a.out.exists(),'Use a fresh output directory');a.out.mkdir(parents=True)
    scope=json.loads((ROOT/'scope.json').read_text());source=scope['source']
    need(sha(a.study_root/source['path'])==source['sha256'],'Source edition changed')
    for x in scope['bound_files']:need(sha(ROOT/x['path'])==x['sha256'],'Bound file changed: '+x['path'])
    frozen=(ROOT/'manifest.json').exists()
    if frozen:
        for x in json.loads((ROOT/'manifest.json').read_text())['exports']:
            need(sha(ROOT/x['path'])==x['sha256'],'Frozen export changed: '+x['path'])
    rc,out=run([a.gap,'-q','-b','-x','240',ROOT/'check_counterexample.g']);(a.out/'gap.log').write_text(out)
    need(rc==0 and 'Error,' not in out and 'Syntax warning' not in out,'Diagnostic failed')
    need('PASS source hypotheses; groups4/8;64+64 intersections;8 independent parabolic orders;3 controls' in out,'Incomplete diagnostic')
    raw=(ROOT/'check_counterexample.g').read_text();controls=[]
    for name,old,new in [('central_factor_removed','tau:=(5,6)','tau:=()'),('dependent_mark_duplicated','old:=[a,b,a*b]','old:=[a,b,b]'),('twist_not_applied','lifted:=[a*tau,b,a*b]','lifted:=[a,b,a*b]')]:
        need(raw.count(old)==1,'Control anchor');path=a.out/(name+'.g');path.write_text(raw.replace(old,new));cr,co=run([a.gap,'-q','-b','-x','240',path]);(a.out/(name+'.log')).write_text(co)
        need((cr!=0 or 'Error,' in co) and 'PASS source hypotheses' not in co,'Damaged example accepted: '+name);controls.append(name)
    render=None
    if a.render:
        from pypdf import PdfReader
        rd=a.out/'render';rd.mkdir();shutil.copy2(ROOT/'endpoint_converse.tex',rd/'endpoint_converse.tex')
        for k in range(2):
            rc,out=run([a.xelatex,'-halt-on-error','-interaction=nonstopmode','endpoint_converse.tex'],rd);(a.out/f'render{k}.log').write_text(out);need(rc==0,'Render failed')
        need(not re.search('Overfull|Missing character|LaTeX Warning|Font Warning',out),'Render diagnostics')
        old=[x.extract_text() for x in PdfReader(ROOT/'endpoint_converse.pdf').pages];new=[x.extract_text() for x in PdfReader(rd/'endpoint_converse.pdf').pages]
        need(len(old)==2 and old==new,'PDF page text changed');render={'pages':2,'per_page_text_equal':True}
    result={'status':'PASS','frozen_exports_checked':frozen,'source_sha256':source['sha256'],'original_intersection_checks':64,'lifted_intersection_checks':64,'original_failures':12,'lifted_failures':0,'parabolic_orders':8,'diagnostic_countermodels':3,'rejected_damaged_examples':controls,'render':render,'scope':'Author diagnostic and integrity replay; complete proof is written; no Lean or independent acceptance claim.','source_credit':0,'question_credit':0}
    dump(a.out/'report.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
