#!/usr/bin/env python3
"""Build only in a fresh private stage; no publication, source, GAP or Lean execution."""
from pathlib import Path
import argparse, hashlib, json, shutil, subprocess, sys
from pypdf import PdfReader
H=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def need(b,m):
    if not b:raise ValueError(m)
def copy(row,root,dest):
    p=Path(row['path']);need(not p.is_absolute()and'..'not in p.parts,'safe path')
    b=(root/p).read_bytes();need(len(b)==row['bytes']and sha(b)==row['sha256'],'exact '+str(p))
    target=dest/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b)
def run(study,repo,out,build):
    repo=repo.resolve();out=out.resolve()
    need(not out.exists(),'fresh stage');need(not out.is_relative_to(repo),'no public writes')
    need(out.is_relative_to(Path('/private/tmp'))or out.is_relative_to(H),'private stage only')
    out.mkdir(parents=True);m=load(H/'copy_plan.json')
    for row in m['files']:
        b=(study/row['study_path']).read_bytes();need(len(b)==row['bytes']and sha(b)==row['sha256'],'payload '+row['study_path'])
        t=out/row['public_path'];t.parent.mkdir(parents=True,exist_ok=True);t.write_bytes(b)
    for row in load(H/'reused_science.json')['files']:copy(row,repo,out)
    if(H/'wrapper_routes.json').exists():
        for row in load(H/'wrapper_routes.json')['files']:
            b=(H/row['proposal_path']).read_bytes();need(len(b)==row['bytes']and sha(b)==row['sha256'],'exact proposed wrapper')
            t=out/row['public_path'];t.parent.mkdir(parents=True,exist_ok=True);t.write_bytes(b)
    base=load(H/'baseline.json');brow=next(r for r in base['files']if r['path']=='scripts/build_papers.py');copy(brow,repo,out)
    target=out/'papers/catalogue.json';target.parent.mkdir(parents=True,exist_ok=True)
    if not target.exists():shutil.copyfile(H/'proposed/papers/catalogue.json',target)
    rows=load(H/'catalogue_additions.json')['entries'];render=None
    if build:
        cmd=[sys.executable,'-B',str(out/'scripts/build_papers.py'),'--output-dir',str(out/'build'),'--jobs','2']
        for r in rows:cmd+=['--paper',r['id']]
        p=subprocess.run(cmd,cwd=out,capture_output=True,text=True);(out/'build_stdout.log').write_text(p.stdout+p.stderr)
        need(p.returncode==0,'canonical builder; inspect '+str(out/'build_stdout.log'))
        report=load(out/'build/report.json');textchecks=[]
        for row in rows:
            a=[p.extract_text()or''for p in PdfReader(out/row['pdf']).pages]
            b=[p.extract_text()or''for p in PdfReader(out/'build'/row['id']/'paper.pdf').pages]
            need(a==b,'all rendered page texts exact '+row['id']);need(len(a)==row['physical_pages'],'whole pages')
            result=next(x for x in report['papers']if x['id']==row['id']);need(not result['diagnostics'],'clean '+row['id'])
            textchecks.append(dict(id=row['id'],pages=len(a),compiler=result['compiler'],
                exact_page_text=True,page_text_sha256=[sha(t.encode())for t in a],diagnostics=[]))
        render=dict(papers=10,pages=sum(r['pages']for r in textchecks),checks=textchecks,
                    unchanged_canonical_builder=True,no_GAP_Lean_execution=True)
    result=dict(status='PASS_PRIVATE_EXACT_STAGE',mapped_files=len(m['files']),
                reused_files=len(load(H/'reused_science.json')['files']),render=render,
                public_writes=False,primary_assets_copied=False,numerical_adoption_pending=m['numerical_root_adoption_pending'])
    (out/'stage_report.json').write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);p.add_argument('--repo',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--build',action='store_true');a=p.parse_args()
    r=run(a.study_root,a.repo,a.out,a.build);print(json.dumps({k:v for k,v in r.items()if k!='render'}));print('Built pages:',r['render']['pages']if r['render']else'not requested')
