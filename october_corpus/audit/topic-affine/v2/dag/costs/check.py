#!/usr/bin/env python3
"""Replay fixed affine extraction and every exclusive-owner union; never runs proof programs."""
import argparse,copy,csv,io,json,sys
from pathlib import Path
sys.dont_write_bytecode=True
from author import HERE,load,load_inputs,create,INPUTS,PROGRAMS,AUX,FORMAL
from accounting import need,sha,allocations,interfaces,route,add,FORMS,METRICS,VARIANTS
from boundaries import supplements

def verify(p,w,root,data=None):
 g,c,spec,ext,texts,raw,aux,formal,adopted=data or load_inputs(root)
 # The source's complete subject belongs with the following kernel assertion.
 for variant in VARIANTS:
  spans=p['documents']['L012']['variants'][variant]['spans']
  kernel=[s for s in spans if s['owner']=='h.64.Kernels.remaining']
  need(len(kernel)==1,'single remaining-kernel passage')
  text=texts['L012'][variant][kernel[0]['start']:kernel[0]['end']]
  need(text.startswith('Similarly, L and M\nare also'),'complete remaining-kernel subject')
 costs,docs=allocations(p,texts)
 need(w['document_costs']==docs and w['owner_costs']==costs,'exact exclusive weights')
 need(w['unchanged_complete_document_measurement']==adopted,'unchanged full-document results')
 for r in adopted['coordinates']:
  for k in docs:need(docs[k][r['variant']][r['normalization']][r['unit']]==r['document_costs'][k],'all 120 admitted cells')
 need(w['raw_program_alternative']==raw and w['raw_auxiliary_files']==aux and w['raw_formal_files']==formal,'all complete separate files')
 need(len(raw)==6 and len(aux)==3 and sum(len(r['binding']['declarations']) for r in formal.values())==9,'six plus three files and nine declarations')
 links=interfaces(g,p['owners'],costs,supplements())
 need(w['node_interfaces']==links,'complete exact statement/setup owners')
 need(set(links)=={n['id'] for n in g['nodes']},'complete logical node inventory')
 need(set(w['raw_program_alternative'])==set(PROGRAMS),'whole required program roster')
 need({o for n in PROGRAMS for o in links[n]['owners']}=={o for o,v in p['owners'].items() if v['document']=='CODE' and v['category']!='excluded_furniture'},'whole appendix exactly in required union')
 for n in g['nodes']:
  if n['side'] in ['external','verification']:need(links[n['id']]['known_weight'] is None and not links[n['id']]['owners'],'unknown external/evidence costs not invented')
 need(all(w[k] is None for k in ['expanded_external_proof_cost','historical_software_cost','graphic_cost','minimum_description_cost','compression_ratio']),'unknowns stay null')
 for key in ['new_source_credit','new_question_credit','new_formal_credit']:need(w[key]==0,'no new credit')
 need(len(w['source_contract_closures'])==33,'33 exact rows')
 for got,r in zip(w['source_contract_closures'],c['rows']):
  need(got['id']==r['id'] and got['coverage']==r['coverage_kind'],'unchanged source dispositions')
  for side,names in [('historical',r['historical_closure']),('replacement',r['new_closure']),('retained_and_qualification_context',sorted(set(r['retained_context_closure'])|set(r['qualification_context_nodes'])))]:
   need(got[side]==route(names,links,costs,p['owners'],raw),'union before summation '+r['id']+' '+side)
 for target,k in [('new_application_closures','new_output_closures'),('additional_current_outputs','additional_current_outputs')]:
  need(w[target]=={n:route(v,links,costs,p['owners'],raw) for n,v in g[k].items()},'all application/additional unions')
 need(w['full_record_closure']==route(g['full_record_closure'],links,costs,p['owners'],raw),'full record union')
 pred={n['id']:set() for n in g['nodes']}
 for e in g['edges']:
  if e['kind'] in g['logical_edge_kinds']:pred[e['target']].add(e['source'])
 need(set(w['individual_node_closures'])==set(pred),'all individual closures')
 for n in pred:
  seen=set();todo=[n]
  while todo:
   x=todo.pop()
   if x not in seen:seen.add(x);todo.extend(pred[x])
  need(w['individual_node_closures'][n]==route(sorted(seen),links,costs,p['owners'],raw),'prerequisite orientation and logical kinds '+n)
 mapped={o for a in links.values() for o in a['owners']}
 extra=[p['owners'][n] for n in sorted(p['owners'].keys()-mapped)]
 need(p['owners_outside_selected_logical_interfaces']==extra,'explicit unmapped context inventory')
 need(all(x['category'] in ['front_matter','context','references','excluded_furniture'] for x in extra),'every substantive passage mapped')
 return {'pdf_metric_cells':120,'raw_file_metric_cells':120,'individual_closures':119,'contract_closures':99,'full_application_closures':1,'full_record_closures':1,'additional_output_closures':2,'owners':len(p['owners']),'selected_spans':sum(len(d['variants']['calibrated_selected']['spans']) for d in p['documents'].values()),'program_files':6,'auxiliary_files':3,'formal_declarations':9}

def controls(p,w,root,data):
 def pcost(x):x['documents']['L012']['variants']['calibrated_selected']['spans'][0]['end']-=1
 def incomplete_subject(x):
  for variant in VARIANTS:
   spans=x['documents']['L012']['variants'][variant]['spans']
   for span in spans:
    if span['owner']=='h.64.Kernels.remaining':
     span['start']+=len('Similarly, L and M\n')
 mutations=[
 ('misassigned_kernel_subject','p',incomplete_subject),
 ('missing_source_character','p',pcost),
 ('duplicate_source_span','p',lambda x:x['documents']['L012']['variants']['raw_selected']['spans'].insert(1,copy.deepcopy(x['documents']['L012']['variants']['raw_selected']['spans'][0]))),
 ('changed_passage_hash','p',lambda x:x['documents']['AF1']['variants']['calibrated_selected']['spans'][0].update(sha256='0'*64)),
 ('foreign_document_owner','p',lambda x:x['owners']['AF.SourcePeriods'].update(document='L012')),
 ('drop_shared_source_statement','w',lambda x:x['node_interfaces']['h.64.Scale']['owners'].remove('h.T4.3.statement')),
 ('drop_branch_presentation','w',lambda x:x['node_interfaces']['h.L4.5.0']['owners'].remove('h.L4.5.setup')),
 ('drop_computational_context','w',lambda x:x['node_interfaces']['h.66.Kernels']['owners'].remove('h.rewriting_context')),
 ('drop_current_statement','w',lambda x:x['node_interfaces']['AF.OddExtension']['owners'].remove('AF.Statements.odd')),
 ('drop_whole_program','w',lambda x:x['raw_program_alternative'].pop('program.kernel66')),
 ('treat_lean_as_free','w',lambda x:x['node_interfaces']['lean.PeriodSignObstruction'].update(known_weight=add([]))),
 ('treat_external_as_free','w',lambda x:x.update(expanded_external_proof_cost=0)),
 ('change_admitted_factor','w',lambda x:x['unchanged_complete_document_measurement']['primary']['comparisons']['written_papers'].update(denominator=1)),
 ('duplicate_route_charge','w',lambda x:x['source_contract_closures'][0]['replacement']['owners'].append(x['source_contract_closures'][0]['replacement']['owners'][0])),
 ('drop_deletion_premise','w',lambda x:x['individual_node_closures']['UA.SK.Delete']['logical_nodes'].remove('UA.D')),
 ('import_comparison_as_premise','w',lambda x:x['individual_node_closures']['AL.4']['logical_nodes'].append('UA.SK')),
 ('new_scope_credit','w',lambda x:x.update(new_source_credit=1)),
 ('remove_unused_common_cost','w',lambda x:x['document_costs']['U_Affine']['calibrated_selected']['NFC'].update(characters_without_whitespace=1))]
 out=[]
 for name,which,mut in mutations:
  pp,ww=copy.deepcopy(p),copy.deepcopy(w);mut(pp if which=='p' else ww)
  try:verify(pp,ww,root,data)
  except (ValueError,RuntimeError,AssertionError,KeyError) as e:out.append({'name':name,'rejected':True,'reason':str(e)})
  else:raise RuntimeError('control accepted '+name)
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();root=a.study_root.resolve()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh output directory');a.out.mkdir(parents=True)
 bindings=load(HERE/'input_bindings.json')
 for r in bindings['inputs']:
  b=(root/r['path']).read_bytes();need(sha(b)==r['sha256'] and len(b)==r['bytes'],'immutable input '+r['path'])
 p=load(HERE/'partition.json');w=load(HERE/'weights.json');data=load_inputs(root)
 report=verify(p,w,root,data)
 pp,ww=create(root);need(pp==p and ww==w,'fresh deterministic regeneration')
 stream=io.StringIO(newline='');writer=csv.writer(stream);writer.writerow(['owner','document','category','variant','normalization']+list(METRICS))
 for n,row in p['owners'].items():
  for v in VARIANTS:
   for f in FORMS:writer.writerow([n,row['document'],row['category'],v,f]+[w['owner_costs'][n][v][f][m] for m in METRICS])
 need(stream.getvalue().encode()==(HERE/'owner_costs.csv').read_bytes(),'complete 5820 owner CSV metric cells')
 report.update(status='PASS_AUTHOR_REPLAY_NOT_INDEPENDENT_REVIEW',controls=controls(p,w,root,data),input_bindings=len(bindings['inputs']),no_proof_programs_rerun=True,no_public_writes=True)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='controls'}))
if __name__=='__main__':main()
