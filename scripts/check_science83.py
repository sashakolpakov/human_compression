"""Verify only the additive L052 principal registration and preserved history."""
import sys
if sys.flags.optimize:raise RuntimeError('Optimized Python is not supported')
from pathlib import Path
import argparse,ast,copy,gzip,hashlib,json
AUD='audit/science83/v1';REC='audit/recoveries/L052/v1'
TRANSPORT='c64f5db6637f6b91835493c6985c5980f6b64098c074b08fd75ec2a17e66612f'
PROPOSAL='4178477673fc4f72f4e1ce950b1ddf8a916cab6811a905de4ea371690cae5eab'
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
 for key,n in [('admitted_original_ids',83),('handled_mathematical_original_ids',84),('measurement_pending_original_ids',30),('scientific_unmeasured_original_ids',30)]:
  unique(c[key],old[key]+['L052'],'Only L052 added '+key);need(len(c[key])==n,'Current cardinality')
 unique(c['accessible_pending_original_ids'],set(old['accessible_pending_original_ids'])-{'L052'},'Only L052 removed')
 need((c['admitted_principal_originals'],c['handled_mathematical_originals'],c['accessible_pending_complete_recovery'])==(83,84,21),'Exact partition')
 mutable={'status','admitted_principal_originals','handled_mathematical_originals','accessible_pending_complete_recovery','previous_snapshot','active_catalogue','current_science_registration','admitted_original_ids','handled_mathematical_original_ids','measurement_pending_original_ids','scientific_unmeasured_original_ids','accessible_pending_original_ids','added_admissions','snapshot'}
 need(set(c)==set(old),'Corpus schema unchanged')
 for k in set(old)-mutable:need(c[k]==old[k],'Unrelated corpus field '+k)
 need(c['added_admissions'][:-1]==old['added_admissions']and c['added_admissions'][-1]['path']==REC+'/admission.json','One admission')
 need({'L046','F009','F012'}<=set(c['accessible_pending_original_ids']) and 'L019' in c['admitted_original_ids'],'Other original dispositions unchanged')
 need(a['source_ids']==['L052']and a['principal_originals_added']==1 and a['whole_original_credit']==0,'Root gate alone grants credit')
 # The reviewed proposal fixes all scientific claims and scope. The registration
 # wrapper is allowed only its explicit status, manuscript-key and gate fields.
 extra={'source_ids','publication_gate','source_map','scope_routes','portable_checker','operational_review_gate','new_native_manuscripts'}
 need(set(a)==(set(proposal)-{'manuscripts'})|extra,'Admission schema')
 for k in set(proposal)-{'status','manuscripts'}:need(a[k]==proposal[k],'Scientific proposal changed '+k)
 need(a['status']=='ROOT_ACCEPTED_MATHEMATICS_PUBLICATION_REQUIRES_SCIENCE83_GATE','Admission status')
 need(a['new_native_manuscripts']==proposal['manuscripts'],'Exact three manuscripts')
 need(a['complete_principal_contract_recovered']and a['corrected_principal_recovery']and not a['all_original_assertions_claimed'],'Corrected principal scope')
 need(a['compression_factor']is a['software_inclusive_factor']is None and a['new_question_credit']==a['new_Lean_declarations']==a['new_measurements']==0 and not a['measured']and not a['whole_source_formalized'],'No unrelated credit')
 need(set(a['component_acceptance']['complete'])=={'author','distinct_review','root_adoption'},'Exact author, distinct review and root adoption')
 expected_math={'author': 'b049a901a2bd38852fad99b636a70575617306c8aee3c5c37c1bda5d91f4ae1d', 'distinct_review': '9a8105bfe4e0b0a26c8acd02f6778ab01f584c55f091eeb86371dc4d6dfe1cc6', 'root_adoption': '1eb788b4facfdcdd3d0bebd8e43669fde6c599e73f7cb38eddd2cf29f336f687'}
 need({k:v['decoded_sha256']for k,v in a['component_acceptance']['complete'].items()}==expected_math,'Exact mathematical acceptance chain')
 need(scope['original']=='L052'and scope['principal_contract']==a['principal_contract']and scope['source_identity']==a['source_identity'],'Exact source contract')
 need(scope['corrections']==a['intermediate_corrections']and len(a['intermediate_corrections'])==4,'Four explicit corrections')
 need(scope['retained_assertions']==a['retained_assertions']==a['retained_inputs']['named_inputs']and len(a['retained_assertions'])==4,'Four named retained classifications')
 need(scope['qualifications']==a['proof_qualifications']and scope['principal_hypotheses']==a['principal_hypotheses'],'Exact geometric hypotheses')
 need(scope['question_dispositions']==a['source_question_dispositions']and len(a['source_question_dispositions'])==5,'Five precise question dispositions')
 need(scope['status']=='ROOT_MATHEMATICS_ACCEPTED_PUBLICATION_GATE_PENDING'and scope['whole_original_credit']==0 and scope['frozen_source_routes_unchanged'],'Gate and frozen source routes')
 need(not scope['classification_completeness_inferred_from_positive_rows']and not scope['all_original_assertions_claimed']and not a['chiral_table_completeness_claimed']and not a['new_general_Cplus_converse_claimed'],'No completeness or converse inference')
 need(a['counts']=={'claims': 62, 'named_clauses': 19, 'acquired_named_clauses': 18, 'retained_named_clauses': 1, 'table1_rows': 12, 'table2_rows': 11, 'examples': 3, 'retained_classifications': 4, 'question_dispositions': 5, 'acquired_old_question_answers': 2, 'unsolved_question_dispositions': 3, 'contextual_antecedents': 7, 'source_corrections': 4} and len(scope['claims'])==62,'Exact source dispositions')
 need(len(a['retained_inputs']['contextual_antecedents'])==7,'Seven contextual antecedents retained')
 need((a['immediate_manuscripts'],a['physical_pages'],a['synthesis_pages'])==(3,18,5),'Full reading volume counted once')
 need(len(a['complete_acquired_proofs'])==30 and len(a['new_native_manuscripts'])==3 and sum(m['physical_pages']for m in a['new_native_manuscripts'])==18,'Complete proof closure')
 need((a['logical_files'],a['restored_mathematical_and_audit_files'],a['acquired_packets'],a['source_assets_hash_only'],a['relative_locator_records'])==(1167,1153,30,14,374),'Exact closure')
 need(a['required_predecessor']=={'recoveries': 82, 'principal_refutations': 1, 'handled_mathematical_originals': 83, 'pending_mathematical_originals': 22, 'measured_recoveries': 53, 'unmeasured_recoveries': 29},'Exact predecessor')
 need(a['proposed_register_after']=={'recoveries': 83, 'principal_refutations': 1, 'handled_mathematical_originals': 84, 'pending_mathematical_originals': 21, 'measured_recoveries': 53, 'unmeasured_recoveries': 30},'Exact proposed disposition')
def registration_mutations():
 return [('duplicate',lambda c,a,s:c['admitted_original_ids'].append('L052')),('omit other pending',lambda c,a,s:c['accessible_pending_original_ids'].remove('F009')),('factor',lambda c,a,s:a.update(compression_factor=2)),('unrestricted',lambda c,a,s:a.update(all_original_assertions_claimed=True)),('lose correction',lambda c,a,s:a['intermediate_corrections'].pop()),('lose retained theorem',lambda c,a,s:s['retained_assertions'].pop()),('lose acquired proof',lambda c,a,s:a['complete_acquired_proofs'].pop(next(iter(a['complete_acquired_proofs'])))),('lose distinct review',lambda c,a,s:a['component_acceptance']['complete'].pop('distinct_review')),('wrong adoption',lambda c,a,s:a['component_acceptance']['complete']['root_adoption'].update(decoded_sha256='0'*64)),('question',lambda c,a,s:a.update(new_question_credit=1)),('wrong finite count',lambda c,a,s:a['counts'].update(table2_rows=10)),('extra documentary omission',lambda c,a,s:a.update(source_assets_hash_only=15)),('borrowed proof erased',lambda c,a,s:a['retained_inputs']['named_inputs'].pop()),('automatic credit',lambda c,a,s:a.update(whole_original_credit=1)),('wrong edition',lambda c,a,s:a['source_identity'].update(sha256='0'*64)),('omit coverage',lambda c,a,s:a['literal_coverage'].update(sha256='0'*64)),('unqualified converse',lambda c,a,s:a.update(new_general_Cplus_converse_claimed=True)),('chiral completeness',lambda c,a,s:a.update(chiral_table_completeness_claimed=True)),('geometric hypothesis',lambda c,a,s:s['principal_hypotheses'].update(Cplus_converse_requires_hypertope=False)),('promote question',lambda c,a,s:s['question_dispositions'][0].update(status='SOLVED')),('truncations thin',lambda c,a,s:a['principal_hypotheses'].update(proper_truncations_claimed_thin=True)),('wrong native input',lambda c,a,s:a['new_native_manuscripts'][0]['tex_inputs'].append('missing.tex'))]
def verify(root,require_root=True):
 root=Path(root).resolve();history=load(root,AUD+'/history_routes.json')['routes']
 need(set(history)=={'README.rst','audit/completion.rst','audit/corpus/latest.json','papers/latest_catalogue.json','papers/catalogue_corrected_unmeasured.json','scripts/verify_snapshot.py','audit/protocol.tex','audit/protocol.pdf'},'Eight exact historical pointers')
 for r in history.values():bind(root,r)
 old=load(root,history['audit/corpus/latest.json']['path']);c=load(root,'audit/corpus/latest.json');a=load(root,REC+'/admission.json');scope=load(root,REC+'/scope_routes.json');proposal=load(root,REC+'/admission_proposal.json')
 need(sha(root/REC/'scope_routes.json')=='231effff2baf47f115b23f59903a4fc102373d0e7fa1b4aa90e249398f4bdc00','Exact frozen source routes');need(sha(root/REC/'admission_proposal.json')==PROPOSAL,'Exact reviewed proposal');semantics(c,old,a,scope,proposal)
 for k in ['active_catalogue','snapshot','current_science_registration']:bind(root,c[k])
 need(load(root,c['snapshot']['path'])=={k:v for k,v in c.items()if k!='snapshot'},'Exact snapshot')
 cat=load(root,c['active_catalogue']['path']);before=load(root,old['active_catalogue']['path']);need(len(cat['entries'])==len(before['entries'])==106,'Fixed catalogue')
 for x,y in zip(before['entries'],cat['entries']):
  if x['original_id']!='L052':need(x==y,'Another original entry changed')
  else:
   need(set(x)==set(y),'L052 original schema')
   for k in set(x)-{'current_principal_recovery','next_obligation'}:need(x[k]==y[k],'Historical L052 property changed')
   q=y['current_principal_recovery'];need(q['historical_admission_evidence']==x['current_principal_recovery']and q['principal_contract_admitted']and q['complete_principal_contract_recovered']and q['corrected_principal_recovery']and not q['all_original_assertions_claimed']and not q['measured'],'Qualified recovery')
   need(q['source_qualifications']==a['intermediate_corrections']and q['principal_hypotheses']==a['principal_hypotheses']and q['question_dispositions']==a['source_question_dispositions']and q['proof_qualifications']==a['proof_qualifications']and q['counts']==a['counts'],'Catalogue scope preserved')
 need(cat['current_recovery_counts']==dict(active=106,admitted=83,refuted=1,handled=84,measured=53,measurement_pending=30,pending=21,editorial=1),'Catalogue partition')
 reg=load(root,c['current_science_registration']['path']);need(reg['source_ids']==['L052']and reg['previous_registration']==old['current_science_registration']and reg['principal_originals_added']==1 and reg['measurement_originals_added']==reg['new_question_credit']==reg['new_Lean_declarations']==reg['comparison_topics_added']==0 and reg['compression_factor']is None and not reg['whole_source_formalized'],'One scientific registration')
 need(len(reg['admissions'])==1 and reg['admissions'][0]['path']==REC+'/admission.json','Registration admission');bind(root,reg['admissions'][0])
 for r in list(a['component_acceptance']['complete'].values())+list(a['complete_acquired_proofs'].values()):bind(root,r)
 for k in ['literal_source_contract','literal_coverage','literal_scope','portable_policy','public_application_adapter','manuscript_inventory','native_input_inventory','complete_reading_volume']:bind(root,a[k])
 for k in ['source_map','scope_routes','portable_report','portable_checker','portable_replay','portable_transport','portable_adaptation']:bind(root,a[k])
 for m in a['new_native_manuscripts']:bind(root,m['tex']);bind(root,m['pdf'])
 t=load(root,a['portable_transport']['path']);need(sha(root/a['portable_transport']['path'])==TRANSPORT and len(t['files'])==1167 and len(t['packets'])==30 and t['whole_original_credit']==0,'Frozen complete transport')
 payloads={r['public_path']:r for r in t['files']if 'public_path'in r};need(len(payloads)==831 and sum(r['transport'].endswith('HASH_ONLY')for r in t['files'])==14,'Exact payload and documentary boundary')
 for path,r in payloads.items():bind(root,dict(r,path=path))
 replay=load(root,a['portable_report']['path']);need(replay['status']=='PASS_PUBLIC_L052_COMPLETE_CLOSURE'and replay['transport_sha256']==TRANSPORT and replay['checker_sha256']==a['portable_checker']['sha256'],'Completed exact replay')
 need((replay['logical_records'],replay['restored_files'],replay['distinct_decoded_payloads'],replay['acquired_packets'],replay['acquired_exports'],replay['exact_metadata_pins_checked'])==(1167,1153,831,30,1523,3046),'Complete public replay scope')
 application=replay['application'];need(application['status']=='PASS_PUBLIC_L052_APPLICATION'and application['counts']=={'claims': 62, 'named_clauses': 19, 'acquired_named_clauses': 18, 'retained_named_clauses': 1, 'table1_rows': 12, 'table2_rows': 11, 'examples': 3, 'retained_classifications': 4, 'question_dispositions': 5, 'acquired_old_question_answers': 2, 'unsolved_question_dispositions': 3, 'contextual_antecedents': 7, 'source_corrections': 4},'Exact source-free interface replay')
 need(not application['original_source_assets_accessed']and application['unchanged_author_mathematical_code']and not application['acquired_census_repeated'],'Exact documentary and mathematical boundary')
 need(len(application['damaged_controls'])==13 and len(application['optimization_guards'])==6 and len(replay['malformed_transport_controls'])==9 and len(replay['portable_optimization_guards'])==2 and not replay['private_proof_fallback']and not replay['mathematical_census_repeated'],'Execution guards and no private fallback')
 need(replay['native_pages']==5 and replay['native_text_identical']and replay['application_stderr_empty']and(application['acquired_manuscripts'],application['acquired_pages'],application['synthesis_pages'],application['full_reading_volume_pages'])==(2,13,5,18),'Complete native output')
 prior=load(root,history['papers/catalogue_corrected_unmeasured.json']['path']);native=load(root,'papers/catalogue_corrected_unmeasured.json');need(native['entries'][:-3]==prior['entries']and native['original_ids']==prior['original_ids']+['L052']and native['acquired_dependencies']==prior['acquired_dependencies']and native['existing_comparison_topic_count']==19 and native['new_measurements']==0,'Previous native and measured catalogue unchanged')
 inventory=load(root,a['native_input_inventory']['path']);need(len(inventory['manuscripts'])==3 and all(not r['literal_inputs'] and not r['tex_inputs']for r in inventory['manuscripts']),'Exact literal native input inventory')
 for x,y in zip(native['entries'][-3:],a['new_native_manuscripts']):
  need(x['id']==y['id']and x['tex']==y['tex']['path']and x['pdf']==y['pdf']['path']and x['physical_pages']==y['physical_pages']and not x['measured']and x['compression_factor']is None,'Exact native routes')
  need(x['tex_inputs']==y['tex_inputs']==[],'Every actual literal native input registered')
 paper=load(root,'papers/latest_catalogue.json');oldpaper=load(root,history['papers/latest_catalogue.json']['path']);need(set(paper)==set(oldpaper),'Paper schema')
 for k in set(oldpaper)-{'active_source_catalogue','corrected_unmeasured_scientific_catalogue'}:need(paper[k]==oldpaper[k],'Other paper route changed')
 need(paper['active_source_catalogue']==c['active_catalogue'],'Active source route');bind(root,paper['corrected_unmeasured_scientific_catalogue'])
 oldtree=ast.parse((root/history['scripts/verify_snapshot.py']['path']).read_text());newtree=ast.parse((root/'scripts/verify_snapshot.py').read_text());added={'check_previous_science83','check_science83'}
 def funcs(tree):return {n.name:ast.dump(n,include_attributes=False)for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'}
 oldf,newf=funcs(oldtree),funcs(newtree);need(set(newf)-set(oldf)==added and all(newf.get(k)==v for k,v in oldf.items()),'Exactly two additive functions; old functions unchanged')
 def other(tree,exc):return [ast.dump(n,include_attributes=False)for n in tree.body if not(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name in exc)]
 need(other(oldtree,{'main'})==other(newtree,{'main'}|added),'All other top-level AST nodes unchanged')
 controls=[]
 mutations=registration_mutations()
 for label,fn in mutations:
  cc,aa,ss=copy.deepcopy((c,a,scope));fn(cc,aa,ss)
  try:semantics(cc,old,aa,ss,proposal)
  except (ValueError,KeyError):controls.append(label)
  else:raise ValueError('Invalid registration accepted '+label)
 op=load(root,AUD+'/operational_review.json');need(op['status']=='ROOT_ACCEPTED_L052_PORTABLE_PUBLICATION'and op['whole_original_credit']==0,'Root operational acceptance')
 mapping=load(root,AUD+'/operational_review/mapping.json');need(mapping['manifest_sha256']==sha(root/mapping['manifest']['path']),'Exact review manifest')
 for r in mapping['bindings'].values():bind(root,r)
 omitted={(r['origin'],r['path'],r['bytes'],r['sha256'])for r in t['files']if r['transport'].endswith('HASH_ONLY')}
 for r in mapping['hash_only_bindings'].values():need((r['origin'],r['path'],r['bytes'],r['sha256'])in omitted,'Only exact inherited source omissions')
 parameters=load(root,AUD+'/registration_parameters.json');need(isinstance(parameters['baseline_commit'],str) and len(parameters['baseline_commit'])==40 and parameters['baseline_commit']==load(root,AUD+'/history_routes.json')['baseline_commit'],'Exact bound predecessor commit');need(mapping['manifest_sha256']==parameters['operational_manifest'] and isinstance(parameters['operational_manifest'],str) and len(parameters['operational_manifest'])==64,'Exact bound operational review')
 if require_root:
  gate=load(root,AUD+'/root_integration.json');need(gate['status']=='ROOT_ACCEPTED_SCIENCE83_PUBLICATION'and gate['source_ids']==['L052']and gate['whole_original_credit']==1 and gate['new_question_credit']==gate['new_Lean_declarations']==gate['new_measurements']==0 and gate['compression_factor']is None,'Final root admission')
  for r in gate['bindings']:bind(root,r)
  need(load(root,AUD+'/registration_review/review.json')['status']=='ACCEPTED_L052_REGISTRATION','Distinct registration review')
 return dict(status='PASS_SCIENCE83_PUBLICATION',counts=dict(active=106,corrected_recoveries=83,refuted=1,handled=84,measured=53,unmeasured=30,mathematical_pending=21,editorial=1,archived=55,comparison_topics=19),source_ids=['L052'],old_verifier_functions_preserved=len(oldf),public_payloads={'L052':831},controls=controls)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--preflight',action='store_true');a=p.parse_args();print(json.dumps(verify(a.repo,not a.preflight)))
