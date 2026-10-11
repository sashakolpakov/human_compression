#!/usr/bin/env python3
"""Distinct source-example and exact clarification/dependency review."""
import argparse,hashlib,json,subprocess,shutil,re
from pathlib import Path
from pypdf import PdfReader
H=Path(__file__).resolve().parent
PIN='fa57821c117ba7814cf3f652587beb93b0f346d79a37d0e9a91cc76b36c657a0'
OLD='8c583aa7513f46a4210280bf3f321caca12f3a5339945a3711c8e02e07f2a617'
def need(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def check_exports(d):
 for r in read(d/'manifest.json')['exports']:
  p=Path(r['path']);need(not p.is_absolute()and'..'not in p.parts,'safe export');f=d/p
  need(f.stat().st_size==r['bytes']and sha(f)==r['sha256'],'complete unchanged export')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--gap',default='/opt/homebrew/bin/gap');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args()
 need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True);s=a.study_root;new=s/'topic_B_L020_positive_v2';old=s/'topic_B_L020_positive'
 need(sha(new/'manifest.json')==PIN and sha(old/'manifest.json')==OLD,'bound editions');check_exports(new);check_exports(old)
 delta=read(new/'delta.json');need(delta['original_manifest_sha256']==OLD and len(delta['edits'])==5,'complete declared clarification')
 for n in ['augmentation.tex','source_application.tex']:
  t=(old/n).read_text()
  for e in delta['edits']:
   if e['path']==n:need(t.count(e['old'])==1,'unique edit');t=t.replace(e['old'],e['new'])
  need(t==(new/n).read_text(),'only declared complete proof edits')
 for n in ['check.py','check_examples.g','check_models.g','SupportedIntersections.lean','dependency_manifest.json','programs.tex','programs.pdf']:need((old/n).read_bytes()==(new/n).read_bytes(),'unchanged program/formal input')
 scope=read(new/'scope.json');need(len(scope['source_rows'])==19 and scope['source_id']=='L020','one original19dispositions')
 for r in scope['external_bindings']:need(sha(s/r['path'])==r['sha256'],'whole retained dependency '+r['path'])
 need(sha(s/'sources/rank_augmentation2024.pdf')=='f3719cbdaba005f3ba55cd6390fbc7e19e333649cb424ffe72e3fa01251e296b','exact19pageprimary')
 need(len(PdfReader(s/'sources/rank_augmentation2024.pdf').pages)==19,'whole originalextent')
 need(scope['source_credit']==scope['question_credit']==0 and scope['compression_factor']is None,'not an admission or factor')
 g=subprocess.run([a.gap,'-q','-b','--quitonbreak',str(H/'distinct.g')],capture_output=True,text=True,timeout=120)
 (a.out/'gap.stdout').write_text(g.stdout);(a.out/'gap.stderr').write_text(g.stderr)
 need(g.returncode==0 and g.stderr=='' and g.stdout.strip()=='PASS_DISTINCT_L020_POSITIVE:source_examples=3;actual_direct_factors=3;literal_defects=3;matching_normal_closure=8;matching_obstructions=7','independent actual subgroup replay')
 renders=[]
 if a.render:
  for name in ['augmentation','source_application']:
   out=a.out/name;out.mkdir();shutil.copyfile(new/(name+'.tex'),out/'paper.tex')
   for _ in range(2):
    r=subprocess.run([a.xelatex,'-halt-on-error','-interaction=nonstopmode','paper.tex'],cwd=out,capture_output=True,text=True,timeout=60)
    need(r.returncode==0,'clean document build')
   (out/'build.stdout').write_text(r.stdout);(out/'build.stderr').write_text(r.stderr)
   need(not re.search('Overfull|Missing character|LaTeX Warning|Font Warning',r.stdout+r.stderr),'render diagnostics')
   current=[p.extract_text()for p in PdfReader(new/(name+'.pdf')).pages];fresh=[p.extract_text()for p in PdfReader(out/'paper.pdf').pages]
   need(current==fresh and len(current)==scope['pdf_pages'][name],'whole current page text')
   previous=[p.extract_text()for p in PdfReader(old/(name+'.pdf')).pages]
   changed=[i+1 for i,(u,v)in enumerate(zip(previous,current))if u!=v]
   need(changed==delta['page_comparison'][name]['changed_pages'],'exact changed pages')
   renders.append(dict(name=name,pages=len(current),changed_pages=changed,all_page_text_equal=True))
 report=dict(status='PASS_DISTINCT_ROOT_L020_POSITIVE_V2',author_manifest_sha256=PIN,author_program_imports=False,source_rows=19,proof_edits=5,required_source_examples=3,independent_rank_three_end_intersections=3,independent_supported_direct_products=3,literal_output_defects=3,actual_matching_normal_closure_order=8,all_seven_nonidentity_matching_elements_in_counterexample_K=True,unchanged_GAP_and_Lean_reused_from_fresh_root_v1_replay=True,renders=renders,retained_introductory_census=True,full_source_credit=0,question_credit=0,compression_factor=None,end_to_end_Lean=False)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
