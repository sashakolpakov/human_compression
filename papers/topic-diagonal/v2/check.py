#!/usr/bin/env python3
"""Replay the exact accepted N006 assembly; preserve scientific trust boundaries."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent

def read(p):return json.loads(p.read_text())
def need(ok,msg):
 if not ok:raise ValueError('N006_ASSEMBLY_REJECT: '+msg)
def items(m):
 e=m['exports'];return [dict(v,path=k) for k,v in e.items()] if isinstance(e,dict) else e
def exact(root,row):
 rel=Path(row['path']);need(not rel.is_absolute() and '..' not in rel.parts,'relative path')
 p=root/rel;b=p.read_bytes();need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'bound bytes '+str(rel))
def call(cmd,out,cwd=None):
 r=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True);out.write_text(r.stdout+r.stderr);need(r.returncode==0,'command failed; see '+str(out))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
 for x in ['xelatex','gap']:ap.add_argument('--'+x,default=shutil.which(x))
 ap.add_argument('--programs',action='store_true');ap.add_argument('--formal',action='store_true')
 for x in ['atlas-nine','atlas-hn','lean','packages']:ap.add_argument('--'+x,type=Path)
 q=ap.parse_args();need(not q.out.exists(),'fresh output');q.out.mkdir(parents=True);assembly=read(ROOT/'assembly.json')
 own=[]
 if (ROOT/'manifest.json').exists():
  own=items(read(ROOT/'manifest.json'))
  for row in own:exact(ROOT,row)
 for row in assembly['scientific_files']:exact(ROOT,row)
 review=ROOT/'reviews/application';need(hashlib.sha256((review/'manifest.json').read_bytes()).hexdigest()==assembly['complete_review_sha256'],'accepted review identity')
 need(assembly['pages']==dict(common=8,application=8,nine_case_note=5,HN_note=4),'entire papers')
 study=q.out/'study';study.mkdir()
 for original,rel in assembly['layout'].items():
  source=ROOT/rel;dest=study/original;dest.mkdir()
  if original=='corpus161_N006_recovery':
   rows=[dict(r,path=str(Path(r['path']).relative_to('papers'))) for r in assembly['scientific_files'] if Path(r['path']).parts[1] not in ['sporadic','harada-norton']]
  else:
   m=read(source/'manifest.json');rows=items(m);shutil.copyfile(source/'manifest.json',dest/'manifest.json')
  for row in rows:
   exact(source,row);p=dest/row['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source/row['path'],p)
 cmd=[sys.executable,'-B','-O',str(study/'corpus161_N006_application_independent_review/check.py'),'--study-root',str(study),'--out',str(q.out/'distinct_review')]
 if q.programs:
  need(q.gap and q.atlas_nine and q.atlas_hn,'explicit finite replay dependencies');cmd+=['--programs','--gap',q.gap,'--atlas-nine',str(q.atlas_nine),'--atlas-hn',str(q.atlas_hn)]
 if q.formal:
  need(q.lean and q.packages,'explicit formal dependencies');cmd+=['--formal','--lean',str(q.lean),'--packages',str(q.packages)]
 call(cmd,q.out/'review.log');replay=read(q.out/'distinct_review/report.json')
 need(replay['source_rows']==27 and replay['affirmative_cases']==10 and replay['fresh_evidence']['fresh_formal_declarations']==17,'accepted complete scope')
 render=[]
 for sub,stem,engine,pages in [('corpus161_N006_recovery','umbrella',q.xelatex,8),('corpus161_N006_recovery','wreath_applications',q.xelatex,8),('corpus161_N006_sporadic','sporadic_certificates',q.xelatex,5),('corpus161_N006_HN','harada_norton',q.xelatex,4)]:
  need(engine is not None,'TeX compiler');work=study/sub
  for k in [1,2]:call([engine,'-interaction=nonstopmode','-halt-on-error',stem+'.tex'],q.out/(stem+f'.render{k}.log'),work)
  log=(work/(stem+'.log')).read_text(errors='replace');need(not any(x in log for x in ['Overfull','Missing character:','LaTeX Warning: There were undefined references']),'render diagnostic '+stem)
  original=ROOT/assembly['layout'][sub]/(stem+'.pdf');fresh=work/(stem+'.pdf');a=PdfReader(original).pages;b=PdfReader(fresh).pages
  need(len(a)==len(b)==pages and [p.extract_text() for p in a]==[p.extract_text() for p in b],'complete page text '+stem)
  render.append(dict(paper=stem,pages=pages,per_page_text_identical=True))
 report=dict(status='PASS',bound_exports=len(own),scientific_bindings=len(assembly['scientific_files']),distinct_review=replay,render=render,expensive_program_replay=q.programs,expensive_formal_replay=q.formal,source_PDFs_redistributed=False,new_question_credit=0,complete_formalization=False)
 (q.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
