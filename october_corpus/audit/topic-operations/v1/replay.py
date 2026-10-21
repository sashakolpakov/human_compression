#!/usr/bin/env python3
"""Replay the joint edition from published exports and optional user originals."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def read(p):return json.loads(p.read_text())
def need(ok,message):
 if not ok:raise ValueError('OPERATIONS_PUBLIC_REPLAY: '+message)
def bound(p,row):
 data=p.read_bytes();need(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'changed bound input '+str(p))
def run(cmd,out,name):
 result=subprocess.run(cmd,capture_output=True,text=True)
 (out/(name+'.log')).write_text(result.stdout+result.stderr)
 need(result.returncode==0,'failed '+name)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--programs',action='store_true');ap.add_argument('--recount',action='store_true');ap.add_argument('--n005',type=Path);ap.add_argument('--n006',type=Path);ap.add_argument('--n007',type=Path);ap.add_argument('--xelatex',default='xelatex');a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'output must be fresh');a.out.mkdir(parents=True)
 py=[sys.executable,'-B','-O'];plan=HERE/'publication_plan';m=read(plan/'publication_map.json')
 # The frozen mapping guard verifies every mapped public byte and all packet exports.
 run(py+[str(plan/'check.py'),'--study-root',str(a.out/'unused'),'--public-root',str(ROOT),'--out',str(a.out/'mapping'),'--published','--stage-replays'],a.out,'mapping')
 study=a.out/'mapped-study';study.mkdir()
 for name,row in m['study_aliases'].items():
  rel=Path(name);need(not rel.is_absolute() and '..' not in rel.parts,'safe original alias')
  source=ROOT/row['public_path'];need(hashlib.sha256(source.read_bytes()).hexdigest()==row['sha256'],'alias identity')
  dest=study/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
 supplied={}
 for row in m['source_inputs']:
  source=getattr(a,row['id'].lower())
  if source is None:continue
  bound(source,row);dest=study/row['study_path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest);supplied[row['id']]=row['sha256']
 if a.programs:
  cmd=py+[str(ROOT/'papers/topic-operations/v1/integrated/check.py'),'--out',str(a.out/'integrated-programs'),'--programs']
  if a.n005:cmd+=['--source',str(a.n005.resolve())]
  run(cmd,a.out,'integrated-programs')
 renders=[]
 if a.render:
  from pypdf import PdfReader
  for i,row in enumerate(read(plan/'catalogue_proposal.json')['documents']):
   base=ROOT/Path(row['tex']).parent;d=a.out/'renders'/str(i);d.mkdir(parents=True)
   for name in row['tex_inputs']:
    src=ROOT/name;rel=src.relative_to(base);dest=d/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
   filename=Path(row['tex']).name
   for j in [1,2]:
    result=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error',filename],cwd=d,capture_output=True,text=True);(d/f'pass{j}.log').write_text(result.stdout+result.stderr);need(result.returncode==0,'complete render '+row['id'])
   pdf=d/Path(row['pdf']).name;actual=[p.extract_text() or '' for p in PdfReader(pdf).pages];expected=[p.extract_text() or '' for p in PdfReader(ROOT/row['pdf']).pages]
   need(len(actual)==row['pages'] and actual==expected,'whole rendered text '+row['id'])
   log=(d/Path(filename).with_suffix('.log')).read_text(errors='replace');fatal=[line for line in log.splitlines() if 'Missing character:' in line or 'Overfull' in line]
   need(not fatal,'render lost material '+row['id']);notices=[line for line in log.splitlines() if 'Underfull' in line or 'Warning:' in line]
   renders.append(dict(id=row['id'],pages=len(actual),whole_page_text_equal=True,diagnostics=notices))
 if a.recount:
  need(set(supplied)=={'N005','N006','N007'},'recount requires all three exact user originals')
  cmd=py+[str(HERE/'measurement/inputs/check.py'),'--public-root',str(ROOT),'--sources-root',str(study),'--out',str(a.out/'recount')]
  if a.render:cmd+=['--render','--xelatex',a.xelatex]
  run(cmd,a.out,'recount')
 run(py+[str(HERE/'measurement/packet/build.py'),'--out',str(a.out/'numbers')]+(['--render','--xelatex',a.xelatex] if a.render else []),a.out,'numbers')
 run(py+[str(HERE/'measurement/independent_review/check.py'),'--packet',str(HERE/'measurement/packet'),'--out',str(a.out/'distinct-numbers.json')],a.out,'distinct-numbers')
 report=dict(status='PASS_PUBLISHED_OPERATIONS_EDITION',mapped_artifacts=471,complete_source_records=140,current_scientific_documents=6,current_scientific_pages=61,rendered_documents=renders,supplied_originals=supplied,source_recount=a.recount,N005_programs_replayed=a.programs,N006_GAP_and_Lean_repeated=False,exact_numeric_fractions=200,full_source_formalization=False,new_question_credit=0)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
