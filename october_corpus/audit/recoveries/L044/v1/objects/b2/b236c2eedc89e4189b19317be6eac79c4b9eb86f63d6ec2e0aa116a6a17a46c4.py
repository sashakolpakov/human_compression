#!/usr/bin/env python3
"""Operational bounded review replay; no machine proof or new finite run."""
import argparse,copy,hashlib,json,re,shutil,subprocess
from pathlib import Path
from pypdf import PdfReader


def require(c,m):
    if not c: raise ValueError(m)


def digest(b): return hashlib.sha256(b).hexdigest()


def verify(root,rows):
    for x in rows:
        b=(root/x['path']).read_bytes()
        require(len(b)==x['bytes'] and digest(b)==x['sha256'],'binding '+x['path'])
    return len(rows)


def scope(r):
    require(r['status']=='ACCEPTED_BOUNDED_WRITTEN_THEOREM_UNCHANGED','status')
    require(r['source_id']=='L044' and r['pages']==2,'source/native scope')
    require(r['author']=='enumeration_review' and r['distinct_reviewer']=='rewrite_termination','roles')
    require(not r['whole_L044_recovered'],'whole-original limit')
    require(not r['fresh_finite_computation'] and not r['fresh_formal_build'],'no new computation')
    require(r['unchanged_prior_proof_bodies']==2,'migration')
    for k in ('new_original_credit','new_question_credit','new_formal_declarations'):
        require(r[k]==0,k)
    require(r['new_factor'] is None,'no factor')
    require(r['corrections_requested']==[],'unchanged acceptance')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path)
    ap.add_argument('--study-root',type=Path);ap.add_argument('--render',action='store_true');a=ap.parse_args()
    a.out.mkdir(parents=True,exist_ok=False);h=Path(__file__).resolve().parent
    m=json.loads((h/'manifest.json').read_text());n=verify(h,m['exports'])
    r=json.loads((h/'review.json').read_text());scope(r)
    ext=None;author=None
    if a.study_root:
        verify(a.study_root,[r['author_manifest']]);author_dir=(a.study_root/r['author_manifest']['path']).parent
        author=verify(author_dir,r['author_exports']);ext=verify(a.study_root,r['external_bindings'])
        texts=[(a.study_root/('topic_B_L044_fixed_label_budget_'+v+'/fixed_label_budget.tex')).read_text() for v in ('v1','v2')]
        bodies=[re.findall(r'\\begin\{proof\}(.*?)\\end\{proof\}',t,re.S) for t in texts]
        require(bodies[0][:2]==bodies[1][:2],'two unchanged inherited proof bodies')
    controls=[]
    for k,v in [('whole_L044_recovered',True),('fresh_finite_computation',True),('fresh_formal_build',True),
                ('new_original_credit',1),('new_question_credit',1),('new_formal_declarations',1),
                ('new_factor',1.0),('unchanged_prior_proof_bodies',1),('author','rewrite_termination')]:
        bad=copy.deepcopy(r);bad[k]=v
        try:scope(bad)
        except ValueError:controls.append(k)
        else:raise ValueError('missed documentary control '+k)
    pdf=h/'reviewed/fixed_label_budget.pdf';diagnostics=[]
    if a.render:
        build=a.out/'native';build.mkdir();shutil.copyfile(h/'reviewed/fixed_label_budget.tex',build/'fixed_label_budget.tex')
        engine=shutil.which('xelatex') or '/opt/homebrew/bin/xelatex'
        for i in (1,2):
            p=subprocess.run([engine,'-interaction=nonstopmode','-halt-on-error','fixed_label_budget.tex'],cwd=build,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,check=True)
            (build/('pass%d.log'%i)).write_bytes(p.stdout)
        log=(build/'fixed_label_budget.log').read_text()
        require(not any(s in log for s in ('LaTeX Warning:','Overfull','Undefined control sequence')),'native error')
        diagnostics=[l for l in log.splitlines() if 'Underfull' in l]
        require(diagnostics==['Underfull \\hbox (badness 1406) in paragraph at lines 12--24'],'exact disclosed layout diagnostic')
        pdf=build/'fixed_label_budget.pdf'
    pages=[p.extract_text() or '' for p in PdfReader(pdf).pages]
    require(len(pages)==2 and [digest(p.encode()) for p in pages]==r['page_text_sha256'],'two exact page texts')
    report={'status':'PASS','review_exports':n,'author_exports':author,'external_bindings':ext,'native_pages':2,
            'documentary_controls':controls,'native_diagnostics':diagnostics,'render':a.render,
            'fresh_finite_or_formal_computation':False,'machine_proof_claim':False}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))


if __name__=='__main__':main()
