#!/usr/bin/env python3
"""Bounded rank-extension counterexample replay; no source-level formal proof claim."""
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
    need('PASS all source hypotheses; old C256/256; new failures72/1024; explicit disjoint words; five subgroup formulas; three end intersections; orbit counts5/4/4/4;3 controls' in out,'Incomplete diagnostic')
    raw=(ROOT/'check_counterexample.g').read_text();controls=[]
    for name,old,new in [('input_central_twist_removed','tau:=(8,9)','tau:=()'),('witness_factor_removed','sigma:=(6,7)','sigma:=()'),('new_twist_omitted','new:=[old[1],(2,10),(3,10)*sigma,old[3],old[4]]','new:=[old[1],(2,10),(3,10),old[3],old[4]]')]:
        need(raw.count(old)==1,'Control anchor');path=a.out/(name+'.g');path.write_text(raw.replace(old,new));cr,co=run([a.gap,'-q','-b','-x','240',path]);(a.out/(name+'.log')).write_text(co)
        need((cr!=0 or 'Error,' in co) and 'PASS all source hypotheses' not in co,'Damaged example accepted: '+name);controls.append(name)
    render=None
    if a.render:
        from pypdf import PdfReader
        rd=a.out/'render';rd.mkdir();shutil.copy2(ROOT/'rank_extension_correction.tex',rd/'rank_extension_correction.tex')
        for k in range(2):
            rc,out=run([a.xelatex,'-halt-on-error','-interaction=nonstopmode','rank_extension_correction.tex'],rd);(a.out/f'render{k}.log').write_text(out);need(rc==0,'Render failed')
        need(not re.search('Overfull|Missing character|LaTeX Warning|Font Warning',out),'Render diagnostics')
        old=[x.extract_text() for x in PdfReader(ROOT/'rank_extension_correction.pdf').pages];new=[x.extract_text() for x in PdfReader(rd/'rank_extension_correction.pdf').pages]
        need(len(old)==3 and old==new,'PDF page text changed');render={'pages':3,'per_page_text_equal':True}
    result={'status':'PASS','frozen_exports_checked':frozen,'source_sha256':source['sha256'],'original_intersection_checks':256,'extended_intersection_checks':1024,'original_failures':0,'extended_failures':72,'subgroup_formulas':5,'end_intersections':3,'all_source_hypotheses_checked':True,'diagnostic_countermodels':3,'rejected_damaged_examples':controls,'render':render,'scope':'Author diagnostic and integrity replay; complete proof is written; no Lean or independent acceptance claim.','source_credit':0,'question_credit':0}
    dump(a.out/'report.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
