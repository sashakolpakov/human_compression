#!/usr/bin/env python3
"""Build exclusive Topic C PDF ownership; requires independent ownership review."""
import argparse,csv,hashlib,importlib.util,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
from accounting import need,sha,total,METRICS,FORMS,VARIANTS,partition_document,allocations,interfaces,route
from boundaries import boundaries,supplements
HERE=Path(__file__).resolve().parent
INPUTS=['topic_C_logical_dag_v2/manifest.json','topic_C_logical_dag_v2/logical_graph.json','topic_C_logical_dag_v2/coverage.json',
 'topic_C_logical_dag_independent_review/manifest.json','topic_C_logical_dag_independent_review/review.json',
 'topic_C_measurement/manifest.json','topic_C_measurement/protocol.json','topic_C_measurement/source_input_spec.json',
 'topic_C_measurement/replacement_input_spec.json','topic_C_measurement/extract_inputs.py','topic_C_measurement/calibration.py',
 'topic_C_measurement_results_v2/manifest.json','topic_C_measurement_results_v2/results.json',
 'topic_C_measurement_results_v2/independent/manifest.json','topic_C_measurement_results_v2/independent/recount.json',
 'topic_C_measurement_publication_review/manifest.json','topic_B_weighted_dag_v2/accounting.py']
PINS={'topic_C_logical_dag_v2/manifest.json':'214e8c47cedb21897a590387cb25557189e600b3356b828f20f722293d84bdf3',
 'topic_C_logical_dag_independent_review/manifest.json':'f1376df93d5a10c5e1b0783d0d70fa6d775c4ca182aaa7799f999e88406312d8',
 'topic_C_measurement_results_v2/manifest.json':'89528371ec03f188fa3cebc7934f32412ebb78189b30023694ee9262d5700cce'}
def load_inputs(root):
 load=lambda f:json.loads((root/f).read_text())
 for f,h in PINS.items():need(sha((root/f).read_bytes())==h,'fixed admitted input '+f)
 graph=load('topic_C_logical_dag_v2/logical_graph.json');coverage=load('topic_C_logical_dag_v2/coverage.json')
 spec=load('topic_C_measurement/source_input_spec.json')['sources']|load('topic_C_measurement/replacement_input_spec.json')['ours']
 sys.path.insert(0,str(root/'topic_C_measurement'))
 ms=importlib.util.spec_from_file_location('bound_c_extract',root/'topic_C_measurement/extract_inputs.py');m=importlib.util.module_from_spec(ms);ms.loader.exec_module(m)
 need(m.pypdf.__version__=='6.13.0','bound parser')
 extracted={k:m.document(root,k,row) for k,row in spec.items()}
 texts={k:dict(zip(VARIANTS,x[:3])) for k,x in extracted.items()}
 raw={}
 for name,row in zip(['program.construction','program.census'],load('topic_C_measurement/replacement_input_spec.json')['required_mathematical_programs']):
  data=(root/row['path']).read_bytes();need(sha(data)==row['sha256'] and len(data)==row['bytes'],'full raw program')
  raw[name]={'binding':row,'metrics':{f:total(data.decode(),f) for f in FORMS}}
 return graph,coverage,spec,extracted,texts,raw,load('topic_C_measurement_results_v2/independent/recount.json')

def create(root):
 graph,coverage,spec,extracted,texts,raw,adopted=load_inputs(root)
 owners={};docs={k:partition_document(k,row,extracted[k],boundaries()[k],owners) for k,row in spec.items()}
 partition={'schema':'topic-c-proof-costs.exclusive-partition.v1','documents':docs,'owners':owners,'missing_L108_original_pdf_cost':None,
 'allocation_policy':'One owner per codepoint. Whole normalized tokens and collapsed whitespace runs belong to their first codepoint owner. Normalized chunk concatenation must equal whole-document normalization. One-codepoint glyph calibration retains ownership; declared furniture has a separate owner in the untrimmed coordinate. Selected joins inherit their explicitly assigned selected owner.',
 'no_primary_text_export':True,'node_count_ratio':None}
 costs,docweights=allocations(partition,texts)
 for k,w in docweights.items():
  for v in VARIANTS:
   for f in FORMS:need(w[v][f]=={m:adopted['documents'][k]['variants'][v][f][m] for m in METRICS},'all adopted document cells '+k)
 links=interfaces(graph,owners,costs,supplements())
 rows=[{'id':r['id'],'source_id':r['source'],'coverage':r['coverage'],
 'historical':route(r['historical_closure'],links,costs,owners,raw),
 'replacement':route(r['new_closure'],links,costs,owners,raw)} for r in coverage['rows']]
 mapped={o for n in links.values() for o in n['owners']}
 partition['owners_outside_selected_logical_interfaces']=[owners[n] for n in sorted(owners.keys()-mapped)]
 for n in partition['owners_outside_selected_logical_interfaces']:
  if n['document'] in ['U_C','C1','C2','C3','C4','CODE']:need(n['category'] in ['front_matter','context','references','excluded_furniture'],'unmapped substantive current passage '+n['id'])
 weights={'schema':'topic-c-proof-costs.prerequisite-unions.v1','status':'AUTHOR_PROPOSAL_PENDING_INDEPENDENT_OWNERSHIP_REVIEW',
 'document_costs':docweights,'owner_costs':costs,'node_interfaces':links,'raw_program_alternative':raw,
 'source_contract_closures':rows,
 'new_application_closures':{k:route(v,links,costs,owners,raw) for k,v in graph['new_output_closures'].items()},
 'additional_current_comparisons':{k:route(v,links,costs,owners,raw) for k,v in graph['additional_comparison_closures'].items()},
 'primary_coordinate':['calibrated_selected','NFC','characters_without_whitespace'],
 'complete_historical_pdf_cost':None,'expanded_external_proof_cost':None,'graphic_cost':None,'compression_ratio':None,
 'program_policy':'Complete CODE appendix is counted once. Both full raw files are an alternative representation, not an addition. A node using one program pays that complete file and the shared printed appendix wrapper in the printed coordinate.',
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
 'no_source_or_scientific_mutation':True,'no_primary_text_export':True,'source_graph_independently_accepted':True,'weights_independently_accepted':False,
 'missing_original_pdf':'L108','node_count_ratio':None,'all_document_coordinates':30,'raw_program_coordinates':10}
 (a.out/'input_bindings.json').write_text(json.dumps(inventory,indent=2)+'\n')
 print(json.dumps({'documents':len(p['documents']),'owners':len(p['owners']),'selected_spans':sum(len(r['variants']['calibrated_selected']['spans']) for r in p['documents'].values()),'logical_interfaces':len(w['node_interfaces']),'clauses':len(w['source_contract_closures'])}))
if __name__=='__main__':main()
