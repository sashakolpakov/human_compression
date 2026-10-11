#!/usr/bin/env python3
"""Stage byte-identical evidence plus explicit current publication routes."""
from pathlib import Path
import argparse,hashlib,json,shutil
HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def need(x,m):
 if not x:raise ValueError(m)
def main():
 p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);p.add_argument('--public-root',type=Path,required=True);a=p.parse_args()
 root=a.study_root;out=HERE/'inputs';need(not out.exists(),'Fresh inputs directory required');out.mkdir()
 copied=[]
 def copy(src,dst,base=root):
  source=base/src;target=out/dst;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target);data=target.read_bytes()
  copied.append(dict(path='inputs/'+dst,sha256=sha(data),bytes=len(data),original_path=src))
 def frozen(src,dst):
  manifest=json.loads((root/src/'manifest.json').read_text())
  for row in manifest['exports']:
   data=(root/src/row['path']).read_bytes();need(sha(data)==row['sha256'] and len(data)==row['bytes'],'Frozen export '+row['path']);copy(src+'/'+row['path'],dst+'/'+row['path'])
  copy(src+'/manifest.json',dst+'/manifest.json')
 frozen('topic_A_logical_dag_v3','logical');frozen('topic_A_logical_independent_review','logical_review');frozen('topic_A_weighted_dag_v2','weighted');frozen('topic_A_weighted_independent_review','weighted_review')
 for src,dst in [('topic_A_measurement/source_input_spec.json','source_spec.json'),('topic_A_numerical_audit/final_replacement_input_spec_private.json','private_replacement_spec.json'),('topic_A_numerical_audit/input_spec.json','public_input_spec.json'),('topic_A_measurement/extract_inputs.py','extract_inputs.py'),('topic_A_numerical_audit/accepted_current_recount.json','independent_recount.json'),('topic_A_numerical_audit/results.json','measurement.json')]:copy(src,dst)
 copy('audit/topic-a/v2/measurement/admission.json','measurement_admission.json',a.public_root)
 g=json.loads((out/'logical/logical_graph.json').read_text());spec=json.loads((out/'public_input_spec.json').read_text())
 published={r['path']:r for r in spec['published_artifacts']};routes={}
 paths={l['path'] for n in g['nodes'] for l in n['locators'] if 'path' in l}
 for path in sorted(paths):
  if not path.startswith(('topic_A_volume/','topic_A_volume_retractions/','topic_A_volume_A6_attribution/')):continue
  suffix=path.split('/',1)[1];target='papers/topic-a/v2/'+suffix
  need(target in published,'Undeclared current evidence '+target)
  data=(a.public_root/target).read_bytes();row=published[target];need(sha(data)==row['sha256'] and len(data)==row['bytes'],'Published input drift '+target)
  routes[path]=dict(path=target,sha256=row['sha256'],bytes=row['bytes'])
 protocol={'schema':'topic_A_portable_graph_adapter_v1','status':'AUTHOR_PREPARATION_PENDING_REVIEW','input_copies':copied,
  'public_proof_commit':spec['published_commit'],'current_evidence_routes':routes,
  'source_files_required':[r['path'] for r in spec['sources'].values()],
  'public_target':'audit/topic-a/v2/dag','frozen_originals_changed':False,
  'replay_scope':'All original graphs, source/current PDF editions, current TeX/program locators and ownership weights. Historical extracted-text locator files are archive evidence; their bytes are not redistributed or replayed. Source PDFs and exact current selected spans are independently bound and re-extracted.',
  'primary_text_or_images_included':False,'new_source_credit':0,'new_question_credit':0,'self_admission':False}
 (HERE/'protocol.json').write_text(json.dumps(protocol,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({'copied_inputs':len(copied),'current_evidence_routes':len(routes)}))
if __name__=='__main__':main()
