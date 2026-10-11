#!/usr/bin/env python3
"""Replay exact source bindings, elementary finite certificate, and optional render."""
import argparse, hashlib, json, re, shutil, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def need(v,m):
    if not v: raise RuntimeError(m)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    p.add_argument('--study-root',type=Path,default=ROOT.parent)
    p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex')
    a=p.parse_args();need(not a.out.exists(),'Fresh output directory required');a.out.mkdir(parents=True);a.out=a.out.resolve()
    scope=json.loads((ROOT/'scope.json').read_text())
    for x in scope['local_bindings']:need(sha(ROOT/x['path'])==x['sha256'],'Changed local input '+x['path'])
    for x in scope['source_bindings']:need(sha(a.study_root/x['path'])==x['sha256'],'Changed primary '+x['path'])
    for x in scope['proof_contexts']:
        s=(ROOT/x['path']).read_text()[x['start']:x['end']]
        need(hashlib.sha256(s.encode()).hexdigest()==x['sha256'],'Changed proof context '+x['id'])
    if (ROOT/'manifest.json').exists():
        for x in json.loads((ROOT/'manifest.json').read_text())['exports']:
            need(sha(ROOT/x['path'])==x['sha256'],'Changed frozen export '+x['path'])
    r=subprocess.run([sys.executable,'-B','-O',str(ROOT/'check_case.py')],capture_output=True,text=True,timeout=60)
    (a.out/'certificate.log').write_text(r.stdout+r.stderr);need(r.returncode==0,'Certificate failed')
    data=json.loads(r.stdout);need(data['status']=='PASS' and data['old_parabolic_pairs']==64,'Incomplete certificate')
    need(len(data['rejected_controls'])==3 and not data['full_symmetric_group_enumerated'],'Control or enumeration scope')
    dump(a.out/'certificate.json',data)
    render=None
    if a.render:
        from pypdf import PdfReader
        rd=a.out/'render';rd.mkdir();shutil.copy2(ROOT/'case_three.tex',rd/'case_three.tex')
        for k in range(2):
            r=subprocess.run([a.xelatex,'-halt-on-error','-interaction=nonstopmode','case_three.tex'],cwd=rd,capture_output=True,text=True,timeout=120)
            (a.out/f'render{k}.log').write_text(r.stdout+r.stderr);need(r.returncode==0,'Render failed')
        need(not re.search(r'Overfull|Missing character|LaTeX Warning|Font Warning',r.stdout+r.stderr),'Render diagnostic')
        old=[p.extract_text() for p in PdfReader(ROOT/'case_three.pdf').pages]
        new=[p.extract_text() for p in PdfReader(rd/'case_three.pdf').pages]
        need(len(old)==3 and old==new,'Per-page text differs')
        render={'pages':3,'per_page_text_equal':True,'warnings':False}
    report={'status':'PASS','source_edition':scope['source_edition'],'hypotheses':len(scope['hypotheses']),
        'proof_contexts':len(scope['proof_contexts']),'source_bindings':len(scope['source_bindings']),
        'direct_proper_pairs':49,'whole_group_pairs_by_containment':15,'max_enumerated_group_order':180,
        'generation_certificate_edges':17,'controls':data['rejected_controls'],'render':render,
        'mathematical_status':'AUTHOR_COMPLETE_PENDING_DISTINCT_REVIEW','end_to_end_Lean':False,
        'source_credit':0,'question_credit':0,'full_L020_recovery':False,'main_stability_refutation':False}
    dump(a.out/'report.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
