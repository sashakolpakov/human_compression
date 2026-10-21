"""Verify only the additive L120 principal registration and preserved history."""
import sys
if sys.flags.optimize:raise RuntimeError('Optimized Python is not supported')
from pathlib import Path
import argparse,ast,copy,gzip,hashlib,json
AUD='audit/science81/v1';REC='audit/recoveries/L120/v1'
TRANSPORT='d49976a5a87612541b042a8ba728bf882551631d8b23016bc7448b7a489189c0'
PROPOSAL='027c99f2a905c929fdc567b303650ae4e7093b960215bb3880b1ad4cdf741c8c'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(root,name):return json.loads((root/name).read_text())
def bind(root,row):
 name=row['path'];p=(root/name).resolve();need(not Path(name).is_absolute()and p.is_relative_to(root),'Unsafe public pin')
 need(p.is_file()and sha(p)==row.get('stored_sha256',row['sha256']),'Changed binding '+name)
 need(p.stat().st_size==row.get('stored_bytes',row.get('bytes',p.stat().st_size)),'Binding length '+name)
def unique(a,b,label):need(len(a)==len(set(a))and set(a)==set(b),label)
def semantics(c,old,a,scope,proposal):
 for key,n in [('admitted_original_ids',81),('handled_mathematical_original_ids',82),('measurement_pending_original_ids',28),('scientific_unmeasured_original_ids',28)]:
  unique(c[key],old[key]+['L120'],'Only L120 added '+key);need(len(c[key])==n,'Current cardinality')
 unique(c['accessible_pending_original_ids'],set(old['accessible_pending_original_ids'])-{'L120'},'Only L120 removed')
 need((c['admitted_principal_originals'],c['handled_mathematical_originals'],c['accessible_pending_complete_recovery'])==(81,82,23),'Exact partition')
 mutable={'status','admitted_principal_originals','handled_mathematical_originals','accessible_pending_complete_recovery','previous_snapshot','active_catalogue','current_science_registration','admitted_original_ids','handled_mathematical_original_ids','measurement_pending_original_ids','scientific_unmeasured_original_ids','accessible_pending_original_ids','added_admissions','snapshot'}
 need(set(c)==set(old),'Corpus schema unchanged')
 for k in set(old)-mutable:need(c[k]==old[k],'Unrelated corpus field '+k)
 need(c['added_admissions'][:-1]==old['added_admissions']and c['added_admissions'][-1]['path']==REC+'/admission.json','One admission')
 need({'L046','F009','F012'}<=set(c['accessible_pending_original_ids']) and 'L019' in c['admitted_original_ids'],'Other original dispositions unchanged')
 need(a['source_ids']==['L120']and a['principal_originals_added']==1 and a['whole_original_credit']==0,'Root gate alone grants credit')
 # The reviewed proposal fixes all scientific claims and scope. The registration
 # wrapper is allowed only its explicit status, manuscript-key and gate fields.
 extra={'source_ids','publication_gate','source_map','scope_routes','portable_checker','operational_review_gate','new_native_manuscripts'}
 need(set(a)==(set(proposal)-{'manuscripts'})|extra,'Admission schema')
 for k in set(proposal)-{'status','manuscripts'}:need(a[k]==proposal[k],'Scientific proposal changed '+k)
 need(a['status']=='ROOT_ACCEPTED_MATHEMATICS_PUBLICATION_REQUIRES_SCIENCE81_GATE','Admission status')
 need(a['new_native_manuscripts']==proposal['manuscripts'],'Exact one manuscript')
 need(a['complete_principal_contract_recovered']and a['corrected_principal_recovery']and not a['all_original_assertions_claimed'],'Corrected principal scope')
 need(a['compression_factor']is a['software_inclusive_factor']is None and a['new_question_credit']==a['new_Lean_declarations']==a['new_measurements']==0 and not a['measured']and not a['whole_source_formalized'],'No unrelated credit')
 need(set(a['component_acceptance']['complete'])=={'author','distinct_root_review'},'Exact author plus distinct root review')
 need(a['component_acceptance']['complete']['author']['decoded_sha256']=='b5860c241cb773ae005ba412237f5b30220f7c045f5c90e21a35f2f133cc7831' and a['component_acceptance']['complete']['distinct_root_review']['decoded_sha256']=='2478f1609c3ff05aec7ca856c44190042bafcaf169b118266a2f9bea40e09543','Exact final mathematical editions')
 need(scope['original']=='L120' and scope['principal_contract']==a['principal_contract'],'Exact complete survey contract')
 need(scope['corrections']==a['intermediate_corrections'] and len(a['intermediate_corrections'])==8,'Eight explicit corrections')
 need(scope['context_only']==a['ancillary_scope'] and scope['status']=='ROOT_MATHEMATICS_ACCEPTED_PUBLICATION_GATE_PENDING' and scope['whole_original_credit']==0 and scope['frozen_source_routes_unchanged'],'Context and publication gate')
 need(scope['retained_assertions']==a['retained_assertions'] and len(a['retained_assertions'])==7 and len(a['retained_inputs']['named'])==7,'Named borrowed assertions preserved')
 need(a['counts']==dict(clauses=50,assertions=32,retained_assertions=7,acquired_or_corrected_assertions=25,questions=18,rank_count_cells=221,project_cells=212,retained_cells=9,source_only_cells=0,formula_controls=100,table2_rows=14,table4_families=2,table4_literal_controls=22,table6_rows=4,figure1_models=18),'Complete source and numerical convention')
 need((a['immediate_manuscripts'],a['physical_pages'])==(1,9),'One nine-page synthesis')
 need((a['logical_files'],a['restored_mathematical_and_audit_files'],a['acquired_packets'],a['source_assets_hash_only'],a['relative_locator_records'])==(9979,9918,503,61,502),'Exact complete closure')
 need(a['required_predecessor']==dict(recoveries=80,principal_refutations=1,handled_mathematical_originals=81,pending_mathematical_originals=24,measured_recoveries=53,unmeasured_recoveries=27),'Exact predecessor')
def verify(root,require_root=True):
 root=Path(root).resolve();history=load(root,AUD+'/history_routes.json')['routes']
 need(set(history)=={'README.rst','audit/completion.rst','audit/corpus/latest.json','papers/latest_catalogue.json','papers/catalogue_corrected_unmeasured.json','scripts/verify_snapshot.py','audit/protocol.tex','audit/protocol.pdf'},'Eight exact historical pointers')
 for r in history.values():bind(root,r)
 old=load(root,history['audit/corpus/latest.json']['path']);c=load(root,'audit/corpus/latest.json');a=load(root,REC+'/admission.json');scope=load(root,REC+'/scope_routes.json');proposal=load(root,REC+'/admission_proposal.json')
 need(sha(root/REC/'admission_proposal.json')==PROPOSAL,'Exact reviewed proposal');semantics(c,old,a,scope,proposal)
 for k in ['active_catalogue','snapshot','current_science_registration']:bind(root,c[k])
 need(load(root,c['snapshot']['path'])=={k:v for k,v in c.items()if k!='snapshot'},'Exact snapshot')
 cat=load(root,c['active_catalogue']['path']);before=load(root,old['active_catalogue']['path']);need(len(cat['entries'])==len(before['entries'])==106,'Fixed catalogue')
 for x,y in zip(before['entries'],cat['entries']):
  if x['original_id']!='L120':need(x==y,'Another original entry changed')
  else:
   need(set(x)==set(y),'L120 original schema')
   for k in set(x)-{'current_principal_recovery','next_obligation'}:need(x[k]==y[k],'Historical L120 property changed')
   q=y['current_principal_recovery'];need(q['historical_admission_evidence']==x['current_principal_recovery']and q['principal_contract_admitted']and q['complete_principal_contract_recovered']and q['corrected_principal_recovery']and not q['all_original_assertions_claimed']and not q['measured'],'Qualified recovery')
   need(q['source_qualifications']==a['intermediate_corrections']and q['ancillary_scope']==a['ancillary_scope']and q['counts']==a['counts'],'Catalogue scope preserved')
 need(cat['current_recovery_counts']==dict(active=106,admitted=81,refuted=1,handled=82,measured=53,measurement_pending=28,pending=23,editorial=1),'Catalogue partition')
 reg=load(root,c['current_science_registration']['path']);need(reg['source_ids']==['L120']and reg['previous_registration']==old['current_science_registration']and reg['principal_originals_added']==1 and reg['measurement_originals_added']==reg['new_question_credit']==reg['new_Lean_declarations']==reg['comparison_topics_added']==0 and reg['compression_factor']is None and not reg['whole_source_formalized'],'One scientific registration')
 need(len(reg['admissions'])==1 and reg['admissions'][0]['path']==REC+'/admission.json','Registration admission');bind(root,reg['admissions'][0])
 for r in list(a['component_acceptance']['complete'].values())+list(a['complete_acquired_proofs'].values()):bind(root,r)
 for k in ['literal_source_contract','literal_named_clauses','literal_numerical_scope','portable_policy','public_application_adapter','manuscript_inventory']:bind(root,a[k])
 for k in ['source_map','scope_routes','portable_report','portable_checker','portable_replay','portable_transport','portable_adaptation']:bind(root,a[k])
 for m in a['new_native_manuscripts']:bind(root,m['tex']);bind(root,m['pdf'])
 t=load(root,a['portable_transport']['path']);need(sha(root/a['portable_transport']['path'])==TRANSPORT and len(t['files'])==9979 and len(t['packets'])==503 and t['whole_original_credit']==0,'Frozen complete transport')
 payloads={r['public_path']:r for r in t['files']if 'public_path'in r};need(len(payloads)==6142 and sum(r['transport'].endswith('HASH_ONLY')for r in t['files'])==61,'Exact payload and documentary boundary')
 for path,r in payloads.items():bind(root,dict(r,path=path))
 replay=load(root,a['portable_report']['path']);need(replay['status']=='PASS_PUBLIC_L120_COMPLETE_CLOSURE'and replay['transport_sha256']==TRANSPORT and replay['checker_sha256']==a['portable_checker']['sha256'],'Completed exact replay')
 need((replay['logical_records'],replay['restored_files'],replay['distinct_decoded_payloads'],replay['acquired_packets'],replay['acquired_exports'],replay['exact_metadata_pins_checked'])==(9979,9918,6174,503,5696,24595),'Complete public replay scope')
 application=replay['application'];need(application['status']=='PASS_PUBLIC_L120_APPLICATION' and application['interfaces']['status']=='PASS_COMPLETE_L120_SOURCE_INTERFACES','Exact source-free mathematical interface replay')
 need({k:application['interfaces'][k]for k in a['counts']}==a['counts'],'All fixed clauses and tables')
 need(application['interfaces']['source_replay'] is None and not application['primary_source_replayed'] and application['unchanged_author_mathematical_code'],'Documentary boundary and unchanged mathematics')
 need(application['damaged_controls']==6 and application['optimization_guards']==6 and len(replay['malformed_transport_controls'])==11 and len(replay['portable_optimization_guards'])==2 and not replay['private_proof_fallback'] and not replay['mathematical_census_repeated'],'Meaningful guards and no private fallback')
 need(replay['native_pages']==9 and replay['native_text_identical'] and replay['application_stderr_empty'],'Complete native/execution output')
 prior=load(root,history['papers/catalogue_corrected_unmeasured.json']['path']);native=load(root,'papers/catalogue_corrected_unmeasured.json');need(native['entries'][:-1]==prior['entries']and native['original_ids']==prior['original_ids']+['L120']and native['acquired_dependencies']==prior['acquired_dependencies']and native['existing_comparison_topic_count']==19 and native['new_measurements']==0,'Previous native and measured catalogue unchanged')
 for x,y in zip(native['entries'][-1:],a['new_native_manuscripts']):need(x['id']==y['id']and x['tex']==y['tex']['path']and x['pdf']==y['pdf']['path']and x['physical_pages']==y['physical_pages']and not x['measured']and x['compression_factor']is None,'Exact native routes')
 paper=load(root,'papers/latest_catalogue.json');oldpaper=load(root,history['papers/latest_catalogue.json']['path']);need(set(paper)==set(oldpaper),'Paper schema')
 for k in set(oldpaper)-{'active_source_catalogue','corrected_unmeasured_scientific_catalogue'}:need(paper[k]==oldpaper[k],'Other paper route changed')
 need(paper['active_source_catalogue']==c['active_catalogue'],'Active source route');bind(root,paper['corrected_unmeasured_scientific_catalogue'])
 oldtree=ast.parse((root/history['scripts/verify_snapshot.py']['path']).read_text());newtree=ast.parse((root/'scripts/verify_snapshot.py').read_text());added={'check_previous_science81','check_science81'}
 def funcs(tree):return {n.name:ast.dump(n,include_attributes=False)for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'}
 oldf,newf=funcs(oldtree),funcs(newtree);need(set(newf)-set(oldf)==added and all(newf.get(k)==v for k,v in oldf.items()),'Exactly two additive functions; old functions unchanged')
 def other(tree,exc):return [ast.dump(n,include_attributes=False)for n in tree.body if not(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name in exc)]
 need(other(oldtree,{'main'})==other(newtree,{'main'}|added),'All other top-level AST nodes unchanged')
 controls=[]
 mutations=[('duplicate',lambda c,a,s:c['admitted_original_ids'].append('L120')),('omit other pending',lambda c,a,s:c['accessible_pending_original_ids'].remove('F009')),('factor',lambda c,a,s:a.update(compression_factor=2)),('unrestricted',lambda c,a,s:a.update(all_original_assertions_claimed=True)),('lose correction',lambda c,a,s:a['intermediate_corrections'].pop()),('lose retained theorem',lambda c,a,s:s['retained_assertions'].pop()),('lose acquired proof',lambda c,a,s:a['complete_acquired_proofs'].pop('corpus106_L120_four_rows_v1')),('lose review',lambda c,a,s:a['component_acceptance']['complete'].pop('distinct_root_review')),('invent adoption',lambda c,a,s:a['component_acceptance']['complete'].update(root_adoption={})),('question',lambda c,a,s:a.update(new_question_credit=1)),('wrong count',lambda c,a,s:a['counts'].update(project_cells=221)),('extra documentary omission',lambda c,a,s:a.update(source_assets_hash_only=62)),('borrowed proof claimed',lambda c,a,s:a['retained_inputs']['named'].pop()),('automatic credit',lambda c,a,s:a.update(whole_original_credit=1)),('wrong edition',lambda c,a,s:a['source_identity'].update(sha256='0'*64)),('omit table',lambda c,a,s:a['literal_numerical_scope'].update(sha256='0'*64))]
 for label,fn in mutations:
  cc,aa,ss=copy.deepcopy((c,a,scope));fn(cc,aa,ss)
  try:semantics(cc,old,aa,ss,proposal)
  except (ValueError,KeyError):controls.append(label)
  else:raise ValueError('Invalid registration accepted '+label)
 op=load(root,AUD+'/operational_review.json');need(op['status']=='ACCEPTED_L120_PUBLIC_TRANSPORT'and op['whole_original_credit']==0,'Root operational acceptance')
 mapping=load(root,AUD+'/operational_review/mapping.json');need(mapping['manifest_sha256']==sha(root/mapping['manifest']['path']),'Exact review manifest')
 for r in mapping['bindings'].values():bind(root,r)
 omitted={(r['origin'],r['path'],r['bytes'],r['sha256'])for r in t['files']if r['transport'].endswith('HASH_ONLY')}
 for r in mapping['hash_only_bindings'].values():need((r['origin'],r['path'],r['bytes'],r['sha256'])in omitted,'Only exact inherited source omissions')
 parameters=load(root,AUD+'/registration_parameters.json');need(isinstance(parameters['baseline_commit'],str) and len(parameters['baseline_commit'])==40 and parameters['baseline_commit']==load(root,AUD+'/history_routes.json')['baseline_commit'],'Exact bound predecessor commit');need(mapping['manifest_sha256']==parameters['operational_manifest'] and isinstance(parameters['operational_manifest'],str) and len(parameters['operational_manifest'])==64,'Exact bound operational review')
 if require_root:
  gate=load(root,AUD+'/root_integration.json');need(gate['status']=='ROOT_ACCEPTED_SCIENCE81_PUBLICATION'and gate['source_ids']==['L120']and gate['whole_original_credit']==1 and gate['new_question_credit']==gate['new_Lean_declarations']==gate['new_measurements']==0 and gate['compression_factor']is None,'Final root admission')
  for r in gate['bindings']:bind(root,r)
  need(load(root,AUD+'/registration_review/review.json')['status']=='ACCEPTED_L120_REGISTRATION','Distinct registration review')
 return dict(status='PASS_SCIENCE81_PUBLICATION',counts=dict(active=106,corrected_recoveries=81,refuted=1,handled=82,measured=53,unmeasured=28,mathematical_pending=23,editorial=1,archived=55,comparison_topics=19),source_ids=['L120'],old_verifier_functions_preserved=len(oldf),public_payloads={'L120':6142},controls=controls)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--preflight',action='store_true');a=p.parse_args();print(json.dumps(verify(a.repo,not a.preflight)))
