from pathlib import Path
import argparse,json
from prepare import H,SCI,AUD,NUM,load,write,need

def prepare(study):
 p=study/'topic_B_L047_measurement_inputs';out={}
 def walk(q):
  if isinstance(q,dict):
   if q.get('root')=='study'and all(k in q for k in ['path','bytes','sha256']):out[q['path']]={k:q[k]for k in ['path','bytes','sha256']}
   for v in q.values():walk(v)
  elif isinstance(q,list):
   for v in q:walk(v)
 for n in ['precount/bindings.json','precount/documents.json','precount/raw_inventory.json','precount/tex_closure.json','precount/source_editions.json','inherited_visual_evidence.json']:walk(load(p/n))
 for q in load(p/'precount/source_editions.json')['inherited']:out[q['declared_source_or_paper_path']]={**{k:q[k]for k in ['bytes','sha256']},'path':q['declared_source_or_paper_path']}
 copied={z['study_path']:z['public_path']for z in load(H/'copy_plan.json')['files']};rows=[]
 for name,r in out.items():
  rows.append(dict(r,source_kind='public_payload'if name in copied else'user_supplied_original',public_path=copied.get(name)))
 need(sum(z['source_kind']=='user_supplied_original'for z in rows)==6,'five wholePDFs and N001browser input')
 write('public_input_routes.json',dict(status='EXACT_ROUTING_ADAPTER_NO_INPUT_CHANGES',frozen_input_public_path=NUM+'/packet/inputs/current',frozen_input_manifest_sha256='33de3038e6bca21ee35e79d819a0bd2bc5e8eb2c594ec16d65d671729f93fcef',files=rows,originals_not_distributed=True,replay_scope='Exact frozen author input checker: four new PDFs and nine new raw files re-extracted;360 earlier document/80raw cells reused as accepted unchanged vectors. It binds all six original representations and the full topic boundary. No numerical ratio or GAP/Lean run.'))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);a=p.parse_args();prepare(a.study_root)
