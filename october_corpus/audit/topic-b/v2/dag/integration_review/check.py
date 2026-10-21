#!/usr/bin/env python3
"""Bounded publication review: immutable copies, verifier delta and controls."""
from pathlib import Path
import argparse,ast,copy,hashlib,importlib.util,json,subprocess,tempfile
PIN='20f85dfd7a75d8fdfefcdea4f01836c2a2c24fe477eadc12b4a231868e3b16ec'
BASE='87757bf40a3514d592854a0ac662121cafa70205'
MAP={'logical_original':'topic_B_logical_dag','logical':'topic_B_logical_dag_v2','logical_review':'topic_B_logical_independent_review','weighted_original':'topic_B_weighted_dag','weighted':'topic_B_weighted_dag_v2','ownership_review':'topic_B_weighted_independent_review','reader':'topic_B_dependency_reader','reader_review':'topic_B_dependency_reader_independent_review'}
def need(v,msg):
 if not v:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh report required')
 root=a.public_root;b=root/'audit/topic-b/v2/dag';need(sha(b/'admission.json')==PIN,'admission changed during review')
 admission=load(b/'admission.json');count=0;exports=[]
 for public,private in MAP.items():
  p=b/public;q=a.study_root/private
  need((p/'manifest.json').read_bytes()==(q/'manifest.json').read_bytes(),'exact manifest '+public)
  for r in load(q/'manifest.json')['exports']:
   name=r['path'];need((p/name).read_bytes()==(q/name).read_bytes(),'exact frozen export '+public+'/'+name)
   exports.append(str((p/name).relative_to(root)));count+=1
 for r in admission['artifacts']:
  p=root/r['path'];need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'admission artifact '+r['path'])
 old=subprocess.check_output(['git','show',BASE+':scripts/verify_snapshot.py'],cwd=root,text=True)
 current=(root/'scripts/verify_snapshot.py').read_text()
 def functions(text):return {x.name:ast.dump(x,include_attributes=False) for x in ast.parse(text).body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef))}
 before=functions(old);after=functions(current);names=set(before)-{'main'}
 need(all(before[n]==after[n] for n in names),'old non-main verifier AST changed')
 need(set(after)-set(before)=={'check_topic_b_dag'},'only new graph checker added')
 changed=subprocess.check_output(['git','diff','--name-only',BASE],cwd=root,text=True).splitlines()
 protected=[p for p in changed if p.startswith('papers/') or p.startswith('audit/topic-b/v2/measurement/') or p in ['audit/topic-b/v2/admission.json','audit/completion.json','research/case_study/formal/lakefile.lean']]
 need(not protected,'old proofs, measurements or coverage changed')
 for p in b.rglob('*'):
  if not p.is_file():continue
  need(p.suffix.lower() not in {'.txt','.md','.olean','.pdf.source'},'unexpected source/text/cache export')
  if p.suffix.lower() in {'.pdf','.png'}:
   need(p.parent.name in {'logical_review','ownership_review','reader'},'only authored review/reader graphics allowed')
 need(not admission['primary_source_text_PDFs_and_rasters_exported'] and admission['new_source_credit']==admission['new_question_credit']==0,'scope/credit guard')
 spec=importlib.util.spec_from_file_location('topic_b_public_verifier',root/'scripts/verify_snapshot.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
 need(v.check_topic_b_dag()==80,'public graph checker')
 controls=[];original_load=v.load
 cases=[('missing_N001_zero','weighted/partition.json',lambda x:x.update(N001_original_pdf_cost=0)),
 ('drop_graph_edge','logical/logical_graph.json',lambda x:x['edges'].pop()),
 ('invent_node_factor','reader/acquisition.json',lambda x:x.update(raw_node_ratio=73/85)),
 ('drop_context_owner','reader/acquisition.json',lambda x:x['stages'][2]['new_owner_ids'].pop()),
 ('duplicate_umbrella','reader/acquisition.json',lambda x:x['stages'][2]['new_owner_ids'].extend(x['stages'][0]['new_owner_ids'])),
 ('source_statement_as_proof','weighted/partition.json',lambda x:x['owners']['h.N008.L3.6'].update(category='proof')),
 ('new_question_credit','admission.json',lambda x:x.update(new_question_credit=1))]
 for name,relative,change in cases:
  path='audit/topic-b/v2/dag/'+relative;mut=copy.deepcopy(original_load(path));change(mut)
  v.load=lambda p,match=path,value=mut:copy.deepcopy(value) if p==match else original_load(p)
  try:v.check_topic_b_dag()
  except (ValueError,KeyError) as e:controls.append(dict(name=name,rejected=True,reason=str(e),mode='in-memory parsed-data mutation; frozen bytes unchanged'))
  else:raise ValueError('accepted mutation '+name)
  finally:v.load=original_load
 # Run the actual byte binding checker against a changed temporary artifact.
 with tempfile.TemporaryDirectory(prefix='topic-b-integrity-') as t:
  path=Path(t)/'artifact.json';path.write_text('{}\n');row=dict(path='artifact.json',bytes=path.stat().st_size,sha256=sha(path));path.write_text('{"tampered":true}\n');oldroot=v.ROOT;v.ROOT=Path(t)
  try:v.check_bindings([row])
  except ValueError as e:controls.append(dict(name='changed_bound_artifact',rejected=True,reason=str(e),mode='temporary file only'))
  else:raise ValueError('byte corruption accepted')
  finally:v.ROOT=oldroot
 # No authored PDF or source text is copied here: artifacts remain hash-bound.
 result=dict(status='PASS_BOUNDED_TOPIC_B_PUBLICATION_REVIEW',base_commit=BASE,admission_sha256=PIN,exact_copied_packet_count=len(MAP),exact_copied_exports=count,admission_bindings=len(admission['artifacts']),previous_nonmain_verifier_ASTs_unchanged=len(names),new_verifier_result=80,
 changed_protected_artifacts=protected,controls=controls,public_paths_verified_at='audit/topic-b/v2/dag/reader/explorer.html',new_source_credit=0,new_question_credit=0,new_factor=None,public_files_modified=False,
 hashes={p:sha(root/p) for p in ['README.rst','audit/work_queue.json','scripts/verify_snapshot.py','audit/topic-b/v2/dag/README.rst','audit/topic-b/v2/dag/root_integration.json']})
 a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:x for k,x in result.items() if k not in ['controls','hashes']}))
if __name__=='__main__':main()
