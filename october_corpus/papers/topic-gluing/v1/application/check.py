#!/usr/bin/env python3
"""Bind the exact source/application closure, run diagnostics and rebuild the TeX."""
import argparse,hashlib,json,re,shutil,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def run(cmd,**kw):
    r=subprocess.run(list(map(str,cmd)),capture_output=True,text=True,timeout=180,**kw)
    return r,r.stdout+r.stderr

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--study-root',type=Path,default=ROOT.parent);ap.add_argument('--render',action='store_true')
    ap.add_argument('--gap',type=Path,default=Path('/opt/homebrew/bin/gap'));ap.add_argument('--xelatex',type=Path,default=Path('/opt/homebrew/bin/xelatex'))
    a=ap.parse_args();need(not a.out.exists(),'Use a fresh output directory');a.out.mkdir(parents=True)
    scope=json.loads((ROOT/'scope.json').read_text());source=json.loads((ROOT/'source_map.json').read_text())
    for x in scope['bound_files']:
        p=(a.study_root if x['external'] else ROOT)/x['path'];need(sha(p)==x['sha256'],'Changed proof/source binding: '+str(p))
    for folder in ['topic_B_core_theory','topic_B_parallel_trees']:
        d=a.study_root/folder
        for x in json.loads((d/'manifest.json').read_text())['exports']:need(sha(d/x['path'])==x['sha256'],'Changed complete common dependency: '+folder+'/'+x['path'])
    if (ROOT/'manifest.json').exists():
        for x in json.loads((ROOT/'manifest.json').read_text())['exports']:need(sha(ROOT/x['path'])==x['sha256'],'Changed frozen export: '+x['path'])
    need(len(source['records'])==23 and len({r['id'] for r in source['records']})==23,'Exact source ledger')
    byid={r['id']:r for r in source['records']}
    need({r['id'] for r in source['records'] if r['status']=='retained_input'}=={'L010.P2.2','L010.P2.3'},'Retained original theorem boundary')
    need({r['id'] for r in source['records'] if r['status']=='excluded_ancillary'}=={'L010.sequence'},'Ancillary exclusions')
    need(byid['L010.impure.second']['status']=='proved' and byid['L010.C4.1.answer']['status']=='historically_answered','Old result attribution boundary')
    need(source['admitted_source_credit_here']==0 and source['new_question_credit']==0 and scope['ratio'] is None,'No unreviewed credits or factors')
    need(scope['required_finite_programs']==[] and all(not x['proof_premise'] for x in scope['code']),'Diagnostics not universal proof premises')
    need(scope['formal']['new']==4 and scope['formal']['reused']==6 and scope['formal']['end_to_end'] is False,'Exact formal scope')
    r,s=run([a.gap,'-q','-b','--quitonbreak',ROOT/'check_applications.g']);(a.out/'diagnostics.log').write_text(s)
    need(r.returncode==0 and not re.search('Error,|Syntax warning',s),'Diagnostic failure');flat=' '.join(s.split())
    for token in ['PASS folded 4 auxiliary 4 uniform negative 9 cases','PASS second source impure-leaf example, exact orbit and intersection']:need(token in flat,'Missing exact diagnostic completion')
    rendering=None
    if a.render:
        from pypdf import PdfReader
        d=a.out/'render';d.mkdir();shutil.copy2(ROOT/'gluing_applications.tex',d/'gluing_applications.tex')
        for i in range(2):
            r,s=run([a.xelatex,'-halt-on-error','-interaction=nonstopmode','gluing_applications.tex'],cwd=d);(a.out/f'render{i}.log').write_text(s);need(r.returncode==0,'Render failure')
        need(not re.search('Overfull|Missing character|LaTeX Warning|Font Warning',s),'Render diagnostics')
        old=[p.extract_text() for p in PdfReader(ROOT/'gluing_applications.pdf').pages];new=[p.extract_text() for p in PdfReader(d/'gluing_applications.pdf').pages]
        need(old==new,'Rebuilt page text changed');rendering=dict(pages=len(old),per_page_text_equal=True)
    result=dict(status='PASS',independent_mathematical_acceptance=False,source_credit=0,new_question_credit=0,source_rows=23,
      common_papers_fully_bound=['topic_B_core_theory','topic_B_parallel_trees'],finite_diagnostics=scope['code'][0],
      formal_scope=scope['formal'],formal_compiled_here=False,render=rendering)
    dump(a.out/'report.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
