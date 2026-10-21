#!/usr/bin/env python3
"""Build exclusive Topic D PDF ownership; requires independent ownership review."""
import argparse,csv,hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
from accounting import need,sha,total,METRICS,FORMS,VARIANTS,partition_document,allocations,interfaces,route
from boundaries import boundaries,supplements
HERE=Path(__file__).resolve().parent
INPUTS=['topic_D_logical_v3_delta_review/manifest.json','topic_D_logical_dag_v3/manifest.json','topic_D_logical_dag_v3/logical_graph.json','topic_D_logical_dag_v3/coverage.json',
 'topic_D_logical_dag_independent_review/manifest.json','topic_D_logical_dag_independent_review/review.json',
 'topic_D_measurement_v2/manifest.json','topic_D_measurement_v2/protocol.json','topic_D_measurement_v2/source_input_spec.json',
 'topic_D_measurement_v2/replacement_input_spec.json','topic_D_measurement_v2/extract_inputs.py','topic_D_measurement_v2/calibration.py',
 'topic_D_measurement_independent_review/manifest.json','topic_D_measurement_independent_review/recount_corrected.json',
 'topic_D_measurement_results/manifest.json','topic_D_measurement_results/results.json',
 'topic_D_measurement_results_independent_review/manifest.json','topic_D_measurement_results_root_adoption/manifest.json',
 'topic_C_dag_costs/atomic_base.py']
PINS={'topic_D_logical_v3_delta_review/manifest.json':'2419f2195a19113681d1696f9455a648944bb2647a10b6ea64cfdb758c85fbd5','topic_D_logical_dag_v3/manifest.json':'ca1fa6326c457ec8e768db8b1942969627aded7acde02b09ee80674f48416943',
 'topic_D_logical_dag_independent_review/manifest.json':'f0a21397229ae9bd62d4488ffe8b59b5bdcafed1174be77531bfc50e7a837034',
 'topic_D_measurement_v2/manifest.json':'8f7729bd219adb61212d3e0c6215b7b84a09e798640ee47e3d5688239edb80d0',
 'topic_D_measurement_independent_review/manifest.json':'61f1d290429b9d30e2c106beb15ee5eaaadce984c433abd68100288aa90c85ff',
 'topic_D_measurement_results/manifest.json':'7c72bf563e7b2c96c5e1927a41a9170108a5787a424fc1418aa9b97ebdabbe1d'}
def load_inputs(root):
 load=lambda f:json.loads((root/f).read_text())
 need((HERE/'atomic_base.py').read_bytes()==(root/'topic_C_dag_costs/atomic_base.py').read_bytes(),'unchanged accepted atomic allocator')
 for f,h in PINS.items():need(sha((root/f).read_bytes())==h,'fixed admitted input '+f)
 graph=load('topic_D_logical_dag_v3/logical_graph.json');coverage=load('topic_D_logical_dag_v3/coverage.json')
 spec=load('topic_D_measurement_v2/source_input_spec.json')['sources']|load('topic_D_measurement_v2/replacement_input_spec.json')['ours']
 sys.path.insert(0,str(root/'topic_D_measurement_v2'))
 ms=importlib.util.spec_from_file_location('bound_d_extract',root/'topic_D_measurement_v2/extract_inputs.py');m=importlib.util.module_from_spec(ms);ms.loader.exec_module(m)
 need(m.pypdf.__version__=='6.13.0','bound parser')
 extracted={k:m.document(root,k,row) for k,row in spec.items()}
 texts={k:dict(zip(VARIANTS,x[:3])) for k,x in extracted.items()}
 raw={};drivers={}
 names=['program.exceptional','diagnostic.pairs','diagnostic.fields','diagnostic.q8','program.search','program.fusion','program.verify','program.predicates']
 rs=load('topic_D_measurement_v2/replacement_input_spec.json')
 for dest,ids,rows in [(raw,names,rs['complete_mathematical_programs']),(drivers,['driver.pairs','driver.enumeration'],rs['complete_drivers'])]:
  need(len(ids)==len(rows),'complete code inventory')
  for name,row in zip(ids,rows):
   data=(root/row['path']).read_bytes();need(sha(data)==row['sha256'] and len(data)==row['bytes'],'full raw program/driver')
   dest[name]={'binding':row,'metrics':{f:total(data.decode(),f) for f in FORMS}}
 return graph,coverage,spec,extracted,texts,raw,drivers,load('topic_D_measurement_independent_review/recount_corrected.json')

def create(root):
 graph,coverage,spec,extracted,texts,raw,drivers,adopted=load_inputs(root)
 owners={};docs={k:partition_document(k,row,extracted[k],boundaries()[k],owners) for k,row in spec.items()}
 partition={'schema':'topic-d-proof-costs.exclusive-partition.v1','documents':docs,'owners':owners,'all_three_original_source_pdfs_measured':True,
 'allocation_policy':'One owner per codepoint. Whole normalized tokens and collapsed whitespace runs belong to their first codepoint owner. Normalized chunk concatenation must equal whole-document normalization. One-codepoint glyph calibration retains ownership; declared furniture has a separate owner in the untrimmed coordinate. Selected joins inherit their explicitly assigned selected owner.',
 'no_primary_text_export':True,'node_count_ratio':None}
 costs,docweights=allocations(partition,texts)
 for k,w in docweights.items():
  for v in VARIANTS:
   for f in FORMS:need(w[v][f]=={m:adopted['documents'][k]['variants'][v][f][m] for m in METRICS},'all adopted document cells '+k)
 links=interfaces(graph,owners,costs,supplements())
 rows=[{'id':r['id'],'source_id':r['source'],'coverage':r['coverage_kind'],
 'historical':route(r['historical_closure'],links,costs,owners,raw),
 'replacement':route(r['new_closure'],links,costs,owners,raw),'retained_and_qualification_context':route(sorted(set(r['retained_context_closure'])|set(r['qualification_context_nodes'])),links,costs,owners,raw)} for r in coverage['rows']]
 mapped={o for n in links.values() for o in n['owners']}
 partition['owners_outside_selected_logical_interfaces']=[owners[n] for n in sorted(owners.keys()-mapped)]
 for n in partition['owners_outside_selected_logical_interfaces']:
  if n['document'] in ['U_D','D1','D2','D3','CODE']:need(n['category'] in ['front_matter','context','references','excluded_furniture'],'unmapped substantive current passage '+n['id'])
 weights={'schema':'topic-d-proof-costs.prerequisite-unions.v1','status':'AUTHOR_PROPOSAL_PENDING_INDEPENDENT_OWNERSHIP_REVIEW',
 'document_costs':docweights,'owner_costs':costs,'node_interfaces':links,'raw_program_alternative':raw,'raw_operational_drivers':drivers,
 'source_contract_closures':rows,
 'new_application_closures':{k:route(v,links,costs,owners,raw) for k,v in graph['new_output_closures'].items()},
 'additional_current_comparisons':{k:route(v,links,costs,owners,raw) for k,v in graph['additional_current_outputs'].items()},
 'primary_coordinate':['calibrated_selected','NFC','characters_without_whitespace'],
 'complete_historical_pdf_cost':__import__('accounting').add(docweights[k] for k in ['L066','L074','L104']),'expanded_external_proof_cost':None,'graphic_cost':None,'compression_ratio':None,
 'program_policy':'Complete CODE appendix is counted once. All eight full raw files are an alternative representation, not an addition. A node using one program pays that complete file and the shared printed appendix wrapper in the printed coordinate.',
 'new_source_credit':0,'new_question_credit':0}
 return partition,weights

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh output directory');a.out.mkdir(parents=True)
 p,w=create(a.study_root.resolve())
 for f,x in [('partition.json',p),('weights.json',w)]: (a.out/f).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
 with (a.out/'owner_costs.csv').open('w',newline='') as f:
  writer=csv.writer(f);writer.writerow(['owner','document','category','variant','normalization']+list(METRICS))
  for name,row in p['owners'].items():
   for v in VARIANTS:
    for norm in FORMS:writer.writerow([name,row['document'],row['category'],v,norm]+[w['owner_costs'][name][v][norm][m] for m in METRICS])
 inventory={'status':'AUTHOR_COST_BOUNDARY_PENDING_INDEPENDENT_REVIEW','inputs':[{'path':f,'bytes':(a.study_root/f).stat().st_size,'sha256':sha((a.study_root/f).read_bytes())} for f in INPUTS],
 'algorithm_ancestry':'atomic_base.py is the byte-identical accepted Topic B allocator. This layer adds explicit furniture ownership and projects the one semantic partition to all three admitted text policies.',
 'no_source_or_scientific_mutation':True,'no_primary_text_export':True,'source_graph_independently_accepted':True,'source_graph_v3_delta_review_sha256':'2419f2195a19113681d1696f9455a648944bb2647a10b6ea64cfdb758c85fbd5','weights_independently_accepted':False,
 'missing_original_pdf':None,'node_count_ratio':None,'all_document_coordinates':30,'raw_program_coordinates':10}
 (a.out/'input_bindings.json').write_text(json.dumps(inventory,indent=2)+'\n')
 print(json.dumps({'documents':len(p['documents']),'owners':len(p['owners']),'selected_spans':sum(len(r['variants']['calibrated_selected']['spans']) for r in p['documents'].values()),'logical_interfaces':len(w['node_interfaces']),'clauses':len(w['source_contract_closures'])}))
if __name__=='__main__':main()
