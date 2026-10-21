"""Verify only the additive N010 principal registration and preserved history."""
import sys
if sys.flags.optimize:raise RuntimeError('Optimized Python is not supported')
from pathlib import Path
import argparse,ast,copy,gzip,hashlib,json
AUD='audit/science84/v1';REC='audit/recoveries/N010/v1'
TRANSPORT='1012b5a56135fe516e304659b332087d32fb33b5d4f75f57dcb5923d58d5bcdc'
PROPOSAL='a8ed4ded99db9cc34361bcc168bab694390b66bb0b9f46a66fffaf2178482a14'
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
 for key,n in [('admitted_original_ids',84),('handled_mathematical_original_ids',85),('measurement_pending_original_ids',31),('scientific_unmeasured_original_ids',31)]:
  unique(c[key],old[key]+['N010'],'Only N010 added '+key);need(len(c[key])==n,'Current cardinality')
 unique(c['accessible_pending_original_ids'],set(old['accessible_pending_original_ids'])-{'N010'},'Only N010 removed')
 need((c['admitted_principal_originals'],c['handled_mathematical_originals'],c['accessible_pending_complete_recovery'])==(84,85,20),'Exact partition')
 mutable={'status','admitted_principal_originals','handled_mathematical_originals','accessible_pending_complete_recovery','previous_snapshot','active_catalogue','current_science_registration','admitted_original_ids','handled_mathematical_original_ids','measurement_pending_original_ids','scientific_unmeasured_original_ids','accessible_pending_original_ids','added_admissions','snapshot'}
 need(set(c)==set(old),'Corpus schema unchanged')
 for k in set(old)-mutable:need(c[k]==old[k],'Unrelated corpus field '+k)
 need(c['added_admissions'][:-1]==old['added_admissions']and c['added_admissions'][-1]['path']==REC+'/admission.json','One admission')
 need({'L046','F009','F012'}<=set(c['accessible_pending_original_ids']) and 'L019' in c['admitted_original_ids'],'Other original dispositions unchanged')
 need(a['source_ids']==['N010']and a['principal_originals_added']==1 and a['whole_original_credit']==0,'Root gate alone grants credit')
 # The reviewed proposal fixes all scientific claims and scope. The registration
 # wrapper is allowed only its explicit status, manuscript-key and gate fields.
 extra={'source_ids','publication_gate','source_map','scope_routes','portable_checker','operational_review_gate','new_native_manuscripts'}
 need(set(a)==(set(proposal)-{'manuscripts'})|extra,'Admission schema')
 for k in set(proposal)-{'status','manuscripts'}:need(a[k]==proposal[k],'Scientific proposal changed '+k)
 need(a['status']=='ROOT_ACCEPTED_MATHEMATICS_PUBLICATION_REQUIRES_SCIENCE84_GATE','Admission status')
 need(a['new_native_manuscripts']==proposal['manuscripts'],'Exact five manuscripts')
 need(a['complete_principal_contract_recovered']and a['principal_recovery_type']=='complete_attributed_survey_disposition'and not a['all_original_assertions_claimed'],'Attributed survey principal scope')
 need(a['compression_factor']is a['software_inclusive_factor']is None and a['new_question_credit']==a['new_Lean_declarations']==a['new_measurements']==0 and not a['measured']and not a['whole_source_formalized'],'No unrelated credit')
 need(set(a['component_acceptance']['complete'])=={'author','distinct_review','root_adoption'},'Exact author, distinct review and root adoption')
 expected_math={'author': 'ba06d64f5d5e08ff25df0e1fdb98e04362c6d7055ad489b14bbe40c625f8c271', 'distinct_review': '9679450e6c769404889f873a00f624e60a9c6ab3c47a09ec6e5d30943b40fa35', 'root_adoption': '56c02b706f9c999fd370dca79c38c93464dd79d19dc456e5cd9f62a16addd486'}
 need({k:v['decoded_sha256']for k,v in a['component_acceptance']['complete'].items()}==expected_math,'Exact mathematical acceptance chain')
 need(scope['original']=='N010'and scope['principal_contract']==a['principal_contract']and scope['source_edition']==a['source_edition'],'Exact source contract')
 need(scope['established_clauses']==a['retained_assertions']and len(a['retained_assertions'])==52,'All52source clauses retained')
 need(scope['source_question_dispositions']==a['source_question_dispositions']and len(a['source_question_dispositions'])==34,'All34source questions retained')
 need(scope['secondary_records']==a['secondary_question_records']and len(a['secondary_question_records'])==14,'All14secondary records retained')
 need(scope['source_qualifications']==a['proof_qualifications']and len(scope['contexts'])==16 and len(scope['source_bibliography'])==66,'Exact context/bibliography/qualifications')
 need(scope['status']=='ROOT_MATHEMATICS_ACCEPTED_PUBLICATION_GATE_PENDING'and scope['whole_original_credit']==0 and scope['frozen_source_routes_unchanged'],'Gate and frozen source routes')
 for key in ['all_classifications_reproved','source_questions_asserted_currently_open','all_source_questions_solved','retained_primary_classifications_independently_reacquired']:
  need(scope[key]is False and a[key]is False,'Retained survey boundary '+key)
 need(scope['source_only_aggregates']==a['source_only_aggregates']==[17,441]and scope['corrected_family_count']==a['corrected_family_count']==137 and scope['corrected_global_total']is a['corrected_global_total']is None and not a['global_aggregates_independently_reproduced'],'No global census inference')
 need(a['counts']=={'contexts': 16, 'established_clauses': 52, 'legacy_register_clauses': 51, 'numbered_questions': 34, 'secondary_records': 14, 'bibliography_entries': 66},'Exact source disposition counts')
 need((a['immediate_manuscripts'],a['physical_pages'],a['synthesis_pages'])==(5,22,11),'Full reading volume counted once')
 need(len(a['complete_acquired_proofs'])==25 and len(a['complete_published_collections'])==6 and len(a['new_native_manuscripts'])==5 and sum(m['physical_pages']for m in a['new_native_manuscripts'])==22,'Complete proof closure')
 need((a['logical_files'],a['restored_mathematical_and_audit_files'],a['acquired_packets'],a['direct_documentary_assets_hash_only'],a['inherited_documentary_records'])==(5962,5947,25,15,107),'Exact closure')
 need(a['required_predecessor']=={'recoveries': 83, 'principal_refutations': 1, 'handled_mathematical_originals': 84, 'pending_mathematical_originals': 21, 'measured_recoveries': 53, 'unmeasured_recoveries': 30},'Exact predecessor')
 need(a['proposed_register_after']=={'recoveries': 84, 'principal_refutations': 1, 'handled_mathematical_originals': 85, 'pending_mathematical_originals': 20, 'measured_recoveries': 53, 'unmeasured_recoveries': 31},'Exact proposed disposition')
def registration_mutations():
 return [('duplicate',lambda c,a,s:c['admitted_original_ids'].append('N010')),('omit other pending',lambda c,a,s:c['accessible_pending_original_ids'].remove('F009')),('factor',lambda c,a,s:a.update(compression_factor=2)),('unrestricted',lambda c,a,s:a.update(all_original_assertions_claimed=True)),('lose clause',lambda c,a,s:s['established_clauses'].pop()),('lose question',lambda c,a,s:s['source_question_dispositions'].pop()),('lose secondary',lambda c,a,s:s['secondary_records'].pop()),('lose bibliography',lambda c,a,s:s['source_bibliography'].pop(next(iter(s['source_bibliography'])))),('lose acquired proof',lambda c,a,s:a['complete_acquired_proofs'].pop(next(iter(a['complete_acquired_proofs'])))),('lose distinct review',lambda c,a,s:a['component_acceptance']['complete'].pop('distinct_review')),('wrong adoption',lambda c,a,s:a['component_acceptance']['complete']['root_adoption'].update(decoded_sha256='0'*64)),('question credit',lambda c,a,s:a.update(new_question_credit=1)),('wrong clause count',lambda c,a,s:a['counts'].update(established_clauses=51)),('extra documentary omission',lambda c,a,s:a.update(direct_documentary_assets_hash_only=16)),('automatic credit',lambda c,a,s:a.update(whole_original_credit=1)),('wrong edition',lambda c,a,s:a['source_identity'][0].update(sha256='0'*64)),('current problem status',lambda c,a,s:a.update(source_questions_asserted_currently_open=True)),('reprove all classifications',lambda c,a,s:s.update(all_classifications_reproved=True)),('global census',lambda c,a,s:a.update(global_aggregates_independently_reproduced=True)),('invent global corrected total',lambda c,a,s:s.update(corrected_global_total=137)),('promote question',lambda c,a,s:s['source_question_dispositions'][0].update(status='SOLVED')),('lost table',lambda c,a,s:a['new_native_manuscripts'][0]['tex_inputs'].pop()),('new measurement',lambda c,a,s:a.update(new_measurements=1)),('lost context',lambda c,a,s:s['contexts'].pop()),('lost inherited closure',lambda c,a,s:a['complete_published_collections'].pop()),('all source questions solved',lambda c,a,s:s.update(all_source_questions_solved=True))]
def verify(root,require_root=True):
 root=Path(root).resolve();history=load(root,AUD+'/history_routes.json')['routes']
 need(set(history)=={'README.rst','audit/completion.rst','audit/corpus/latest.json','papers/latest_catalogue.json','papers/catalogue_corrected_unmeasured.json','scripts/verify_snapshot.py','audit/protocol.tex','audit/protocol.pdf'},'Eight exact historical pointers')
 for r in history.values():bind(root,r)
 old=load(root,history['audit/corpus/latest.json']['path']);c=load(root,'audit/corpus/latest.json');a=load(root,REC+'/admission.json');scope=load(root,REC+'/scope_routes.json');proposal=load(root,REC+'/admission_proposal.json')
 need(sha(root/REC/'scope_routes.json')=='2fb8589cc324d29d4a13b4e8d17bcc479cbf695c11717f54a4e3aef623d33972','Exact frozen source routes');need(sha(root/REC/'admission_proposal.json')==PROPOSAL,'Exact reviewed proposal');semantics(c,old,a,scope,proposal)
 for k in ['active_catalogue','snapshot','current_science_registration']:bind(root,c[k])
 need(load(root,c['snapshot']['path'])=={k:v for k,v in c.items()if k!='snapshot'},'Exact snapshot')
 cat=load(root,c['active_catalogue']['path']);before=load(root,old['active_catalogue']['path']);need(len(cat['entries'])==len(before['entries'])==106,'Fixed catalogue')
 for x,y in zip(before['entries'],cat['entries']):
  if x['original_id']!='N010':need(x==y,'Another original entry changed')
  else:
   need(set(x)==set(y),'N010 original schema')
   for k in set(x)-{'current_principal_recovery','next_obligation'}:need(x[k]==y[k],'Historical N010 property changed')
   q=y['current_principal_recovery'];need(q['historical_admission_evidence']==x['current_principal_recovery']and q['principal_contract_admitted']and q['complete_principal_contract_recovered']and q['corrected_principal_recovery']and not q['all_original_assertions_claimed']and not q['measured'],'Qualified recovery')
   need(q['source_qualifications']==a['proof_qualifications']and q['retained_assertions']==a['retained_assertions']and q['question_dispositions']==a['source_question_dispositions']and q['secondary_question_records']==a['secondary_question_records']and q['counts']==a['counts']and q['principal_recovery_type']==a['principal_recovery_type']and q['source_only_aggregates']==[17,441]and q['corrected_family_count']==137 and q['corrected_global_total']is None and not q['all_classifications_reproved']and not q['source_questions_asserted_currently_open']and not q['all_source_questions_solved'],'Catalogue survey scope preserved')
 need(cat['current_recovery_counts']==dict(active=106,admitted=84,refuted=1,handled=85,measured=53,measurement_pending=31,pending=20,editorial=1),'Catalogue partition')
 reg=load(root,c['current_science_registration']['path']);need(reg['source_ids']==['N010']and reg['previous_registration']==old['current_science_registration']and reg['principal_originals_added']==1 and reg['measurement_originals_added']==reg['new_question_credit']==reg['new_Lean_declarations']==reg['comparison_topics_added']==0 and reg['compression_factor']is None and not reg['whole_source_formalized'],'One scientific registration')
 need(len(reg['admissions'])==1 and reg['admissions'][0]['path']==REC+'/admission.json','Registration admission');bind(root,reg['admissions'][0])
 for r in list(a['component_acceptance']['complete'].values())+list(a['complete_acquired_proofs'].values()):bind(root,r)
 for k in ['literal_source_contract','literal_scope','portable_policy','public_application_adapter','manuscript_inventory','native_input_inventory','complete_reading_volume']:bind(root,a[k])
 for k in ['source_map','scope_routes','portable_report','portable_checker','portable_replay','portable_transport','portable_adaptation']:bind(root,a[k])
 for m in a['new_native_manuscripts']:
  bind(root,m['tex']);bind(root,m['pdf'])
  for q in m['tex_inputs']:bind(root,q)
 t=load(root,a['portable_transport']['path']);need(sha(root/a['portable_transport']['path'])==TRANSPORT and len(t['files'])==5962 and len(t['packets'])==25 and t['whole_original_credit']==0,'Frozen complete transport')
 payloads={r['public_path']:r for r in t['files']if 'public_path'in r};need(len(payloads)==5663 and sum(r['transport'].endswith('HASH_ONLY')for r in t['files'])==15,'Exact payload and documentary boundary')
 for path,r in payloads.items():bind(root,dict(r,path=path))
 replay=load(root,a['portable_report']['path']);need(replay['status']=='PASS_PUBLIC_N010_COMPLETE_SURVEY_CLOSURE'and replay['transport_sha256']==TRANSPORT and replay['checker_sha256']==a['portable_checker']['sha256'],'Completed exact replay')
 need((replay['logical_records'],replay['restored_files'],replay['distinct_decoded_payloads'],replay['private_packets'],replay['private_exports'],replay['metadata_pins_checked'])==(5962,5947,5664,25,215,26965),'Complete public replay scope')
 need((replay['inherited_logical_records'],replay['inherited_decoded_payloads'],replay['inherited_documentary_records'],replay['principal_dependency_pins'])==(7633,4800,107,5777),'Inherited full closure')
 application=replay['application'];need(application['status']=='PASS_PUBLIC_N010_APPLICATION'and application['counts']=={k:v for k,v in a['counts'].items()if k!='legacy_register_clauses'},'Exact public source-interface replay')
 need(not application['original_source_assets_accessed']and application['unchanged_author_validate']and not application['runtime_text_patching']and not application['acquired_censuses_repeated'],'Exact documentary and mathematical boundary')
 need(len(application['damaged_controls'])==17 and len(application['optimization_guards'])==4 and len(replay['malformed_transport_controls'])==10 and len(replay['portable_optimization_guards'])==2 and not replay['private_proof_fallback']and not replay['acquired_censuses_repeated'],'Execution guards and no private fallback')
 need(replay['native_pages']==11 and application['native_text_identical']and replay['application_stderr_empty']and(application['acquired_components'],application['acquired_pages'],application['synthesis_pages'],application['full_reading_volume_pages'])==(4,11,11,22),'Complete native output')
 prior=load(root,history['papers/catalogue_corrected_unmeasured.json']['path']);native=load(root,'papers/catalogue_corrected_unmeasured.json');need(native['entries'][:-5]==prior['entries']and native['original_ids']==prior['original_ids']+['N010']and native['acquired_dependencies']==prior['acquired_dependencies']and native['existing_comparison_topic_count']==19 and native['new_measurements']==0,'Previous native and measured catalogue unchanged')
 inventory=load(root,a['native_input_inventory']['path']);need(len(inventory['manuscripts'])==5 and inventory['manuscripts'][0]['literal_inputs']==['context_table.tex','question_table.tex','secondary_table.tex']and all(not m['literal_inputs']for m in inventory['manuscripts'][1:]),'Exact literal native input inventory')
 import re
 for x,y in zip(native['entries'][-5:],a['new_native_manuscripts']):
  need(x['id']==y['id']and x['tex']==y['tex']['path']and x['pdf']==y['pdf']['path']and x['physical_pages']==y['physical_pages']and not x['measured']and x['compression_factor']is None,'Exact native routes')
  need(x['tex_inputs']==[q['path']for q in y['tex_inputs']],'Every literal native input registered')
  actual=re.findall(r'\\(?:input|include|includegraphics)(?:\[[^]]*\])?\s*\{([^}]+)\}',(root/x['tex']).read_text())
  need(actual==[Path(q['path']).name for q in y['tex_inputs']],'Actual literal source inputs match')
  for q in y['tex_inputs']:need(Path(q['path']).parent==Path(x['tex']).parent,'Literal input adjacent');bind(root,q)
 paper=load(root,'papers/latest_catalogue.json');oldpaper=load(root,history['papers/latest_catalogue.json']['path']);need(set(paper)==set(oldpaper),'Paper schema')
 for k in set(oldpaper)-{'active_source_catalogue','corrected_unmeasured_scientific_catalogue'}:need(paper[k]==oldpaper[k],'Other paper route changed')
 need(paper['active_source_catalogue']==c['active_catalogue'],'Active source route');bind(root,paper['corrected_unmeasured_scientific_catalogue'])
 oldtree=ast.parse((root/history['scripts/verify_snapshot.py']['path']).read_text());newtree=ast.parse((root/'scripts/verify_snapshot.py').read_text());added={'check_previous_science84','check_science84'}
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
 op=load(root,AUD+'/operational_review.json');need(op['status']=='ROOT_ACCEPTED_N010_PORTABLE_PUBLICATION_STORAGE_SUCCESSOR'and op['whole_original_credit']==0,'Root operational acceptance')
 mapping=load(root,AUD+'/operational_review/mapping.json');need(mapping['manifest_sha256']==sha(root/mapping['manifest']['path']),'Exact review manifest')
 for r in mapping['bindings'].values():bind(root,r)
 omitted={(r['origin'],r['path'],r['bytes'],r['sha256'])for r in t['files']if r['transport'].endswith('HASH_ONLY')}
 for r in mapping['hash_only_bindings'].values():need((r['origin'],r['path'],r['bytes'],r['sha256'])in omitted,'Only exact inherited source omissions')
 parameters=load(root,AUD+'/registration_parameters.json');need(isinstance(parameters['baseline_commit'],str) and len(parameters['baseline_commit'])==40 and parameters['baseline_commit']==load(root,AUD+'/history_routes.json')['baseline_commit'],'Exact bound predecessor commit');need(mapping['manifest_sha256']==parameters['operational_manifest'] and isinstance(parameters['operational_manifest'],str) and len(parameters['operational_manifest'])==64,'Exact bound operational review')
 if require_root:
  gate=load(root,AUD+'/root_integration.json');need(gate['status']=='ROOT_ACCEPTED_SCIENCE84_PUBLICATION'and gate['source_ids']==['N010']and gate['whole_original_credit']==1 and gate['new_question_credit']==gate['new_Lean_declarations']==gate['new_measurements']==0 and gate['compression_factor']is None,'Final root admission')
  for r in gate['bindings']:bind(root,r)
  need(load(root,AUD+'/registration_review/review.json')['status']=='ACCEPTED_N010_REGISTRATION','Distinct registration review')
 return dict(status='PASS_SCIENCE84_PUBLICATION',counts=dict(active=106,corrected_recoveries=84,refuted=1,handled=85,measured=53,unmeasured=31,mathematical_pending=20,editorial=1,archived=55,comparison_topics=19),source_ids=['N010'],old_verifier_functions_preserved=len(oldf),public_payloads={'N010':5663},controls=controls)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--preflight',action='store_true');a=p.parse_args();print(json.dumps(verify(a.repo,not a.preflight)))
