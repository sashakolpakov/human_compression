"""Verify only the additive L041 principal registration and preserved history."""
import sys
if sys.flags.optimize:raise RuntimeError('Optimized Python is not supported')
from pathlib import Path
import argparse,ast,copy,gzip,hashlib,json
AUD='audit/science85/v1';REC='audit/recoveries/L041/v1'
TRANSPORT='bffd51ffa8670ff8c4d1644cda89cae7071326ba527343ffc7a9ad931a60abca'
PROPOSAL='13bea31e53ff5ef07cb96d5c4b21124484dbfb9ff4ad3fc52b18fcb1e25cbbbc'
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
 for key,n in [('admitted_original_ids',85),('handled_mathematical_original_ids',86),('measurement_pending_original_ids',32),('scientific_unmeasured_original_ids',32)]:
  unique(c[key],old[key]+['L041'],'Only L041 added '+key);need(len(c[key])==n,'Current cardinality')
 unique(c['accessible_pending_original_ids'],set(old['accessible_pending_original_ids'])-{'L041'},'Only L041 removed')
 need((c['admitted_principal_originals'],c['handled_mathematical_originals'],c['accessible_pending_complete_recovery'])==(85,86,19),'Exact partition')
 mutable={'status','admitted_principal_originals','handled_mathematical_originals','accessible_pending_complete_recovery','previous_snapshot','active_catalogue','current_science_registration','admitted_original_ids','handled_mathematical_original_ids','measurement_pending_original_ids','scientific_unmeasured_original_ids','accessible_pending_original_ids','added_admissions','snapshot'}
 need(set(c)==set(old),'Corpus schema unchanged')
 for k in set(old)-mutable:need(c[k]==old[k],'Unrelated corpus field '+k)
 need(c['added_admissions'][:-1]==old['added_admissions']and c['added_admissions'][-1]['path']==REC+'/admission.json','One admission')
 need({'L046','F009','F012'}<=set(c['accessible_pending_original_ids']) and 'L019' in c['admitted_original_ids'],'Other original dispositions unchanged')
 need(a['source_ids']==['L041']and a['principal_originals_added']==1 and a['whole_original_credit']==0,'Root gate alone grants credit')
 # The reviewed proposal fixes all scientific claims and scope. The registration
 # wrapper is allowed only its explicit status, manuscript-key and gate fields.
 extra={'source_ids','publication_gate','source_map','scope_routes','portable_checker','operational_review_gate','new_native_manuscripts'}
 need(set(a)==(set(proposal)-{'manuscripts'})|extra,'Admission schema')
 for k in set(proposal)-{'status','manuscripts'}:need(a[k]==proposal[k],'Scientific proposal changed '+k)
 need(a['status']=='ROOT_ACCEPTED_MATHEMATICS_PUBLICATION_REQUIRES_SCIENCE85_GATE','Admission status')
 need(a['new_native_manuscripts']==proposal['manuscripts'],'Exact one manuscript')
 need(a['complete_principal_contract_recovered']and a['principal_recovery_type']=='complete_corrected_family_recovery'and not a['all_original_assertions_claimed'],'Corrected tetrahedral-family scope')
 need(a['compression_factor']is a['software_inclusive_factor']is None and a['new_question_credit']==a['new_Lean_declarations']==a['new_measurements']==0 and not a['measured']and not a['whole_source_formalized'],'No unrelated credit')
 need(set(a['component_acceptance']['complete'])=={'author','distinct_review','root_adoption'},'Exact author, distinct review and root adoption')
 expected_math={'author': '6f7221a6784c479748786ca2497df0a32f1162cd995e93acb3d9f58dc1665877', 'distinct_review': 'dadef515a37a320ff1c87f9a37982a75ca9a0cb31333d65927a17f8bed07f7dc', 'root_adoption': '37881e86a6112a9723cae5757e14e791a277dab25cf3e913e1599fc34eb56795'}
 need({k:v['decoded_sha256']for k,v in a['component_acceptance']['complete'].items()}==expected_math,'Exact mathematical acceptance chain')
 need(scope['original']=='L041'and scope['principal_contract']==a['principal_contract'],'Exact source contract')
 need(scope['source_rows']==a['proof_qualifications']==a['source_qualifications']and len(scope['source_rows'])==28 and a['numbered_source_statements']==20,'All source dispositions retained')
 need(scope['retained_inputs']==a['retained_assertions']==a['retained_inputs']==['Classical faithful triangular Euclidean rotation presentation and translation lattice', 'Accepted chamber propagation/reconstruction and marked-inversion theorem', 'Elementary finite-field and finite-group facts'],'Exact retained inputs')
 need(scope['background_residue_qualification']==a['background_residue_qualification']=='Source page5 internal residue identification is used only after actual triple-flag transitivity in this family; no generic implication for arbitrary C-plus markings or new counterexample is asserted.','Actual triple-flag residue qualification')
 need(scope['parameters']=='All source family parameters: primesp≠3, q=p forp≡1mod3 andq=p² forp≡2mod3, both primitive roots e.' and scope['finite_cases_are_controls_only']is True,'Uniform family; finite fields are controls')
 need(scope['source_questions']==dict(explicit_open_questions_found=0,new_answers_claimed=0)and a['source_question_dispositions']==[],'No new question claim')
 need(scope['status']=='ROOT_MATHEMATICS_ACCEPTED_PUBLICATION_GATE_PENDING'and scope['whole_original_credit']==scope['new_question_credit']==scope['new_Lean']==scope['new_measurements']==0,'Gate and scope')
 need((a['immediate_manuscripts'],a['physical_pages'])==(1,8),'Exact new manuscript inventory')
 need(len(a['complete_acquired_proofs'])==7 and len(a['new_native_manuscripts'])==1 and a['new_native_manuscripts'][0]['physical_pages']==8,'Complete proof closure')
 need((a['logical_files'],a['restored_mathematical_and_audit_files'],a['acquired_packets'],a['direct_documentary_assets_hash_only'],a['historical_runtime_identities'])==(232,218,7,13,1),'Exact closure')
 need(a['required_predecessor']=={'recoveries': 84, 'principal_refutations': 1, 'handled_mathematical_originals': 85, 'pending_mathematical_originals': 20, 'measured_recoveries': 53, 'unmeasured_recoveries': 31},'Exact predecessor')
 need(a['proposed_register_after']=={'recoveries': 85, 'principal_refutations': 1, 'handled_mathematical_originals': 86, 'pending_mathematical_originals': 19, 'measured_recoveries': 53, 'unmeasured_recoveries': 32},'Exact proposed disposition')
def registration_mutations():
 return [('duplicate',lambda c,a,s:c['admitted_original_ids'].append('L041')),('omit other pending',lambda c,a,s:c['accessible_pending_original_ids'].remove('F009')),('factor',lambda c,a,s:a.update(compression_factor=2)),('unrestricted',lambda c,a,s:a.update(all_original_assertions_claimed=True)),('lose source clause',lambda c,a,s:s['source_rows'].pop()),('lose retained input',lambda c,a,s:s['retained_inputs'].pop()),('lose acquired proof',lambda c,a,s:a['complete_acquired_proofs'].pop(next(iter(a['complete_acquired_proofs'])))),('lose distinct review',lambda c,a,s:a['component_acceptance']['complete'].pop('distinct_review')),('wrong adoption',lambda c,a,s:a['component_acceptance']['complete']['root_adoption'].update(decoded_sha256='0'*64)),('question credit',lambda c,a,s:a.update(new_question_credit=1)),('wrong numbered count',lambda c,a,s:a.update(numbered_source_statements=19)),('extra documentary omission',lambda c,a,s:a.update(direct_documentary_assets_hash_only=14)),('automatic credit',lambda c,a,s:a.update(whole_original_credit=1)),('wrong edition',lambda c,a,s:a['source_identity'].update(sha256='0'*64)),('generic residue assertion',lambda c,a,s:s.update(background_residue_qualification='All C-plus markings')),('finite controls as proof',lambda c,a,s:s.update(finite_cases_are_controls_only=False)),('lost table',lambda c,a,s:a['new_native_manuscripts'][0]['tex_inputs'].pop()),('new measurement',lambda c,a,s:a.update(new_measurements=1)),('lost runtime treatment',lambda c,a,s:a.update(historical_runtime_identities=0))]
def verify(root,require_root=True):
 root=Path(root).resolve();history=load(root,AUD+'/history_routes.json')['routes']
 need(set(history)=={'README.rst','audit/completion.rst','audit/corpus/latest.json','papers/latest_catalogue.json','papers/catalogue_corrected_unmeasured.json','scripts/verify_snapshot.py','audit/protocol.tex','audit/protocol.pdf'},'Eight exact historical pointers')
 for r in history.values():bind(root,r)
 old=load(root,history['audit/corpus/latest.json']['path']);c=load(root,'audit/corpus/latest.json');a=load(root,REC+'/admission.json');scope=load(root,REC+'/scope_routes.json');proposal=load(root,REC+'/admission_proposal.json')
 need(sha(root/REC/'scope_routes.json')=='384418ceae7d71b1eb8e931596c3151903064c6df2709b957480974c6b4a9f75','Exact frozen source routes');need(sha(root/REC/'admission_proposal.json')==PROPOSAL,'Exact reviewed proposal');semantics(c,old,a,scope,proposal)
 for k in ['active_catalogue','snapshot','current_science_registration']:bind(root,c[k])
 need(load(root,c['snapshot']['path'])=={k:v for k,v in c.items()if k!='snapshot'},'Exact snapshot')
 cat=load(root,c['active_catalogue']['path']);before=load(root,old['active_catalogue']['path']);need(len(cat['entries'])==len(before['entries'])==106,'Fixed catalogue')
 for x,y in zip(before['entries'],cat['entries']):
  if x['original_id']!='L041':need(x==y,'Another original entry changed')
  else:
   need(set(x)==set(y),'L041 original schema')
   for k in set(x)-{'current_principal_recovery','next_obligation'}:need(x[k]==y[k],'Historical L041 property changed')
   q=y['current_principal_recovery'];need(q['historical_admission_evidence']==x['current_principal_recovery']and q['principal_contract_admitted']and q['complete_principal_contract_recovered']and q['corrected_principal_recovery']and not q['all_original_assertions_claimed']and not q['measured'],'Qualified recovery')
   need(q['source_qualifications']==a['proof_qualifications']and q['retained_assertions']==a['retained_assertions']and q['question_dispositions']==a['source_question_dispositions']and q['principal_recovery_type']==a['principal_recovery_type']and q['background_residue_qualification']==a['background_residue_qualification']and q['finite_cases_are_controls_only']is True,'Catalogue exact family scope preserved')
 need(cat['current_recovery_counts']==dict(active=106,admitted=85,refuted=1,handled=86,measured=53,measurement_pending=32,pending=19,editorial=1),'Catalogue partition')
 reg=load(root,c['current_science_registration']['path']);need(reg['source_ids']==['L041']and reg['previous_registration']==old['current_science_registration']and reg['principal_originals_added']==1 and reg['measurement_originals_added']==reg['new_question_credit']==reg['new_Lean_declarations']==reg['comparison_topics_added']==0 and reg['compression_factor']is None and not reg['whole_source_formalized'],'One scientific registration')
 need(len(reg['admissions'])==1 and reg['admissions'][0]['path']==REC+'/admission.json','Registration admission');bind(root,reg['admissions'][0])
 for r in list(a['component_acceptance']['complete'].values())+list(a['complete_acquired_proofs'].values()):bind(root,r)
 for k in ['literal_source_contract','literal_scope','portable_policy','public_application_adapter','manuscript_inventory','native_input_inventory']:bind(root,a[k])
 for k in ['source_map','scope_routes','portable_report','portable_checker','portable_replay','portable_transport','portable_adaptation']:bind(root,a[k])
 for m in a['new_native_manuscripts']:
  bind(root,m['tex']);bind(root,m['pdf'])
  for q in m['tex_inputs']:bind(root,q)
 t=load(root,a['portable_transport']['path']);need(sha(root/a['portable_transport']['path'])==TRANSPORT and len(t['files'])==232 and len(t['packets'])==7 and t['whole_original_credit']==0,'Frozen complete transport')
 payloads={r['public_path']:r for r in t['files']if 'public_path'in r};need(len(payloads)==188 and sum(r['transport'].endswith('HASH_ONLY')for r in t['files'])==14,'Exact payload/documentary/runtime boundary')
 for path,r in payloads.items():bind(root,dict(r,path=path))
 replay=load(root,a['portable_report']['path']);need(replay['status']=='PASS_PUBLIC_L041_CLOSURE'and replay['transport_sha256']==TRANSPORT and replay['checker_sha256']==a['portable_checker']['sha256'],'Completed exact replay')
 need((replay['logical_files'],replay['restored_files'],replay['decoded_objects'],replay['private_packets'],replay['complete_exports'],replay['metadata_pins'])==(232,218,188,7,72,1158),'Complete public replay scope')
 need((replay['documentary_assets'],replay['runtime_identities'],replay['tracked_reused_objects'])==(13,1,134),'Declared omission and tracked reuse boundaries')
 application=replay['application'];need(application['status']=='PASS_PUBLIC_L041_APPLICATION'and application['finite_fields']==[4,7,13,19,25]and application['finite_exact'],'Exact public controls')
 need(not application['original_documentary_assets_read']and application['author_scientific_code_unchanged']and not application['runtime_text_patching']and not application['acquired_censuses_repeated']and not application['general_proof_verified_by_program'],'Exact documentary and mathematical boundary')
 need(len(application['optimization_guards'])==6 and len(replay['malformed_transport_controls'])==13 and len(replay['optimization_guards'])==2 and replay['no_private_fallback']and not replay['acquired_censuses_repeated'],'Execution guards and no private fallback')
 need(application['native_pages']==8 and application['native_text_identical']and replay['application_stderr_empty']and not replay['principal_review_pending'],'Complete native output')
 prior=load(root,history['papers/catalogue_corrected_unmeasured.json']['path']);native=load(root,'papers/catalogue_corrected_unmeasured.json');need(native['entries'][:-1]==prior['entries']and native['original_ids']==prior['original_ids']+['L041']and native['acquired_dependencies']==prior['acquired_dependencies']and native['existing_comparison_topic_count']==19 and native['new_measurements']==0,'Previous native and measured catalogue unchanged')
 inventory=load(root,a['native_input_inventory']['path']);need(inventory['manuscripts']==a['new_native_manuscripts']and len(inventory['manuscripts'])==1,'Exact literal native inventory')
 import re
 for x,y in zip(native['entries'][-1:],a['new_native_manuscripts']):
  need(x['id']==y['id']and x['tex']==y['tex']['path']and x['pdf']==y['pdf']['path']and x['physical_pages']==y['physical_pages']and not x['measured']and x['compression_factor']is None,'Exact native routes')
  need(x['tex_inputs']==[q['path']for q in y['tex_inputs']],'Every literal native input registered')
  actual=re.findall(r'\\(?:input|include)\s*\{([^}]+)\}',(root/x['tex']).read_text())
  need(actual==['tetrahedra_section']and [Path(q['path']).name for q in y['tex_inputs']]==['tetrahedra_section.tex'],'Actual literal source input resolves')
  for q in y['tex_inputs']:need(Path(q['path']).parent==Path(x['tex']).parent,'Literal input adjacent');bind(root,q)
 paper=load(root,'papers/latest_catalogue.json');oldpaper=load(root,history['papers/latest_catalogue.json']['path']);need(set(paper)==set(oldpaper),'Paper schema')
 for k in set(oldpaper)-{'active_source_catalogue','corrected_unmeasured_scientific_catalogue'}:need(paper[k]==oldpaper[k],'Other paper route changed')
 need(paper['active_source_catalogue']==c['active_catalogue'],'Active source route');bind(root,paper['corrected_unmeasured_scientific_catalogue'])
 oldtree=ast.parse((root/history['scripts/verify_snapshot.py']['path']).read_text());newtree=ast.parse((root/'scripts/verify_snapshot.py').read_text());added={'check_previous_science85','check_science85'}
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
 op=load(root,AUD+'/operational_review.json');need(op['status']==load(root,AUD+'/registration_parameters.json')['operational_status']and op['whole_original_credit']==0,'Root operational acceptance')
 mapping=load(root,AUD+'/operational_review/mapping.json');need(mapping['manifest_sha256']==sha(root/mapping['manifest']['path']),'Exact review manifest')
 for r in mapping['bindings'].values():bind(root,r)
 omitted={(r['origin'],r['path'],r['bytes'],r['sha256'])for r in t['files']if r['transport'].endswith('HASH_ONLY')}
 for r in mapping['hash_only_bindings'].values():need((r['origin'],r['path'],r['bytes'],r['sha256'])in omitted,'Only exact inherited source omissions')
 parameters=load(root,AUD+'/registration_parameters.json');need(isinstance(parameters['baseline_commit'],str) and len(parameters['baseline_commit'])==40 and parameters['baseline_commit']==load(root,AUD+'/history_routes.json')['baseline_commit'],'Exact bound predecessor commit');need(mapping['manifest_sha256']==parameters['operational_manifest'] and isinstance(parameters['operational_manifest'],str) and len(parameters['operational_manifest'])==64,'Exact bound operational review')
 if require_root:
  gate=load(root,AUD+'/root_integration.json');need(gate['status']=='ROOT_ACCEPTED_SCIENCE85_PUBLICATION'and gate['source_ids']==['L041']and gate['whole_original_credit']==1 and gate['new_question_credit']==gate['new_Lean_declarations']==gate['new_measurements']==0 and gate['compression_factor']is None,'Final root admission')
  for r in gate['bindings']:bind(root,r)
  need(load(root,AUD+'/registration_review/review.json')['status']=='ACCEPTED_L041_REGISTRATION','Distinct registration review')
 return dict(status='PASS_SCIENCE85_PUBLICATION',counts=dict(active=106,corrected_recoveries=85,refuted=1,handled=86,measured=53,unmeasured=32,mathematical_pending=19,editorial=1,archived=55,comparison_topics=19),source_ids=['L041'],old_verifier_functions_preserved=len(oldf),public_payloads={'L041':188},controls=controls)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--preflight',action='store_true');a=p.parse_args();print(json.dumps(verify(a.repo,not a.preflight)))
