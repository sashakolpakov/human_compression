#!/usr/bin/env python3
"""Exclusive affine manuscript costs. This author assignment needs independent review."""
import argparse,csv,hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
from accounting import need,sha,total,METRICS,FORMS,VARIANTS,partition_document,allocations,interfaces,route,add
from boundaries import boundaries,supplements
HERE=Path(__file__).resolve().parent
load=lambda p:json.loads(p.read_text())
INPUTS=['topic_Affine_logical_dag_v2/manifest.json','topic_Affine_logical_dag_v2/logical_graph.json','topic_Affine_logical_dag_v2/coverage.json',
 'topic_Affine_logical_independent_review/manifest.json','topic_Affine_logical_independent_review/review.json','topic_Affine_logical_root_adoption/manifest.json',
 'topic_Affine_measurement/manifest.json','topic_Affine_measurement/protocol.json','topic_Affine_measurement/source_input_spec.json','topic_Affine_measurement/replacement_input_spec.json','topic_Affine_measurement/extract_inputs.py','topic_Affine_measurement/calibration.py',
 'topic_Affine_measurement_independent_review/manifest.json','topic_Affine_measurement_independent_review/recount.json',
 'topic_Affine_measurement_results/manifest.json','topic_Affine_measurement_results/results.json',
 'topic_Affine_measurement_results_independent_review/manifest.json','topic_Affine_measurement_root_adoption/manifest.json',
 'topic_D_dag_costs_v2/atomic_base.py']
PROGRAMS=['program.kernel64','program.affine64','program.census384','program.fixed','program.kernel66','program.affine66']
AUX=['driver.check','driver.integrity','diagnostic.controls']
FORMAL=['lean.AffinePeriodIntersections','lean.PeriodSignObstruction','lean.QuotientIntersectionCriterion']

def load_inputs(root):
 p=load(HERE/'protocol.json')
 for f,h in p['input_pins'].items():need(sha((root/f).read_bytes())==h,'admitted input '+f)
 need((HERE/'atomic_base.py').read_bytes()==(root/'topic_D_dag_costs_v2/atomic_base.py').read_bytes(),'unchanged atomic allocator')
 g=load(root/'topic_Affine_logical_dag_v2/logical_graph.json');c=load(root/'topic_Affine_logical_dag_v2/coverage.json')
 rs=load(root/'topic_Affine_measurement/replacement_input_spec.json')
 spec=load(root/'topic_Affine_measurement/source_input_spec.json')['sources']|rs['ours']
 sys.path.insert(0,str(root/'topic_Affine_measurement'))
 ms=importlib.util.spec_from_file_location('bound_affine_extract',root/'topic_Affine_measurement/extract_inputs.py');m=importlib.util.module_from_spec(ms);ms.loader.exec_module(m)
 need(m.pypdf.__version__=='6.13.0','pinned parser')
 ext={k:m.document(root,k,row) for k,row in spec.items()};texts={k:dict(zip(VARIANTS,x[:3])) for k,x in ext.items()}
 raw={};aux={};formal={}
 for dest,ids,rows in [(raw,PROGRAMS,rs['complete_mathematical_programs']),(aux,AUX,rs['complete_auxiliary_scripts']),(formal,FORMAL,rs['complete_formal_files'])]:
  need(len(ids)==len(rows),'complete file inventory')
  for name,row in zip(ids,rows):
   data=(root/row['path']).read_bytes();need(sha(data)==row['sha256'] and len(data)==row['bytes'],'full bound file '+name)
   dest[name]={'binding':row,'metrics':{f:total(data.decode(),f) for f in FORMS}}
 return g,c,spec,ext,texts,raw,aux,formal,load(root/'topic_Affine_measurement_results/results.json')

def create(root):
 g,c,spec,ext,texts,raw,aux,formal,adopted=load_inputs(root)
 owners={};docs={k:partition_document(k,row,ext[k],boundaries()[k],owners) for k,row in spec.items()}
 p={'schema':'affine-costs.exclusive-partition.v1','documents':docs,'owners':owners,
 'allocation_policy':'One owner per codepoint; normalized tokens and collapsed runs belong to their first codepoint owner. Normalized chunk concatenation must equal whole normalization. Furniture has a separate raw owner. Calibration preserves codepoint ownership.',
 'primary_text_exported':False,'node_count_ratio':None}
 costs,docweights=allocations(p,texts)
 for row in adopted['coordinates']:
  for k in docs:need(docweights[k][row['variant']][row['normalization']][row['unit']]==row['document_costs'][k],'all 120 admitted cells '+k)
 links=interfaces(g,owners,costs,supplements())
 rows=[{'id':r['id'],'source':r['source'],'coverage':r['coverage_kind'],
 'historical':route(r['historical_closure'],links,costs,owners,raw),
 'replacement':route(r['new_closure'],links,costs,owners,raw),
 'retained_and_qualification_context':route(sorted(set(r['retained_context_closure'])|set(r['qualification_context_nodes'])),links,costs,owners,raw)} for r in c['rows']]
 mapped={o for n in links.values() for o in n['owners']}
 p['owners_outside_selected_logical_interfaces']=[owners[n] for n in sorted(owners.keys()-mapped)]
 for n in p['owners_outside_selected_logical_interfaces']:
  need(n['category'] in ['front_matter','context','references','excluded_furniture'],'unmapped substantive passage '+n['id'])
 w={'schema':'affine-costs.prerequisite-unions.v1','status':'AUTHOR_PROPOSAL_PENDING_DISTINCT_INDEPENDENT_REVIEW',
 'document_costs':docweights,'owner_costs':costs,'node_interfaces':links,
 'raw_program_alternative':raw,'raw_auxiliary_files':aux,'raw_formal_files':formal,
 'source_contract_closures':rows,
 'new_application_closures':{k:route(v,links,costs,owners,raw) for k,v in g['new_output_closures'].items()},
 'full_record_closure':route(g['full_record_closure'],links,costs,owners,raw),
 'additional_current_outputs':{k:route(v,links,costs,owners,raw) for k,v in g['additional_current_outputs'].items()},
 'individual_node_closures':{},
 'primary_coordinate':['calibrated_selected','NFC','characters_without_whitespace'],
 'unchanged_complete_document_measurement':adopted,
 'expanded_external_proof_cost':None,'historical_software_cost':None,'graphic_cost':None,'minimum_description_cost':None,'compression_ratio':None,
 'program_policy':'All six complete mathematical files are paid once in the full CODE appendix. Raw full-file costs are an alternative representation. Every program interface includes its full printed file and the shared appendix wrapper. Auxiliary and Lean files are separately measured evidence.',
 'new_source_credit':0,'new_question_credit':0,'new_formal_credit':0}
 parents={n['id']:set() for n in g['nodes']}
 for e in g['edges']:
  if e['kind'] in g['logical_edge_kinds']:parents[e['target']].add(e['source'])
 def closure(start):
  seen=set();todo=list(start)
  while todo:
   n=todo.pop()
   if n not in seen:seen.add(n);todo.extend(parents[n])
  return sorted(seen)
 for n in parents:w['individual_node_closures'][n]=route(closure([n]),links,costs,owners,raw)
 return p,w

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh output');a.out.mkdir(parents=True)
 p,w=create(a.study_root.resolve())
 for f,x in [('partition.json',p),('weights.json',w)]: (a.out/f).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
 with (a.out/'owner_costs.csv').open('w',newline='') as f:
  writer=csv.writer(f);writer.writerow(['owner','document','category','variant','normalization']+list(METRICS))
  for n,row in p['owners'].items():
   for v in VARIANTS:
    for form in FORMS:writer.writerow([n,row['document'],row['category'],v,form]+[w['owner_costs'][n][v][form][m] for m in METRICS])
 x={'status':w['status'],'inputs':[{'path':f,'bytes':(a.study_root/f).stat().st_size,'sha256':sha((a.study_root/f).read_bytes())} for f in INPUTS],
 'logical_acceptance':'topic_Affine_logical_root_adoption/manifest.json','algorithm_ancestry':'Byte-identical accepted B/C/D atomic allocator; explicit raw furniture and fixed calibrated selection projection. Longest matching logical ID prevents parent-prefix charging unrelated corollaries.',
 'cost_author_prior_roles':load(HERE/'protocol.json')['roles'],'no_scientific_mutation':True,'primary_text_exported':False,'expanded_external_proof_cost':None,'node_count_ratio':None}
 (a.out/'input_bindings.json').write_text(json.dumps(x,indent=2)+'\n')
 print(json.dumps({'documents':len(p['documents']),'owners':len(p['owners']),'selected_spans':sum(len(x['variants']['calibrated_selected']['spans']) for x in p['documents'].values()),'logical_interfaces':len(w['node_interfaces']),'rows':len(w['source_contract_closures'])}))
if __name__=='__main__':main()
