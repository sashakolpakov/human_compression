"""Verify only the additive L045 principal registration and preserved history."""
import sys
if sys.flags.optimize:raise RuntimeError('Optimized Python is not supported')
from pathlib import Path
import argparse,ast,copy,gzip,hashlib,json
AUD='audit/science82/v1';REC='audit/recoveries/L045/v1'
TRANSPORT='a76cd461e0e24b6522b0a5d4100af368dc7d14c003ac106961f6347cd375031d'
PROPOSAL='18edc85f6812fed5088c231263752c54e55ab99277e1e1510292821a70477c0e'
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
 for key,n in [('admitted_original_ids',82),('handled_mathematical_original_ids',83),('measurement_pending_original_ids',29),('scientific_unmeasured_original_ids',29)]:
  unique(c[key],old[key]+['L045'],'Only L045 added '+key);need(len(c[key])==n,'Current cardinality')
 unique(c['accessible_pending_original_ids'],set(old['accessible_pending_original_ids'])-{'L045'},'Only L045 removed')
 need((c['admitted_principal_originals'],c['handled_mathematical_originals'],c['accessible_pending_complete_recovery'])==(82,83,22),'Exact partition')
 mutable={'status','admitted_principal_originals','handled_mathematical_originals','accessible_pending_complete_recovery','previous_snapshot','active_catalogue','current_science_registration','admitted_original_ids','handled_mathematical_original_ids','measurement_pending_original_ids','scientific_unmeasured_original_ids','accessible_pending_original_ids','added_admissions','snapshot'}
 need(set(c)==set(old),'Corpus schema unchanged')
 for k in set(old)-mutable:need(c[k]==old[k],'Unrelated corpus field '+k)
 need(c['added_admissions'][:-1]==old['added_admissions']and c['added_admissions'][-1]['path']==REC+'/admission.json','One admission')
 need({'L046','F009','F012'}<=set(c['accessible_pending_original_ids']) and 'L019' in c['admitted_original_ids'],'Other original dispositions unchanged')
 need(a['source_ids']==['L045']and a['principal_originals_added']==1 and a['whole_original_credit']==0,'Root gate alone grants credit')
 # The reviewed proposal fixes all scientific claims and scope. The registration
 # wrapper is allowed only its explicit status, manuscript-key and gate fields.
 extra={'source_ids','publication_gate','source_map','scope_routes','portable_checker','operational_review_gate','new_native_manuscripts'}
 need(set(a)==(set(proposal)-{'manuscripts'})|extra,'Admission schema')
 for k in set(proposal)-{'status','manuscripts'}:need(a[k]==proposal[k],'Scientific proposal changed '+k)
 need(a['status']=='ROOT_ACCEPTED_MATHEMATICS_PUBLICATION_REQUIRES_SCIENCE82_GATE','Admission status')
 need(a['new_native_manuscripts']==proposal['manuscripts'],'Exact fifteen manuscripts')
 need(a['complete_principal_contract_recovered']and a['corrected_principal_recovery']and not a['all_original_assertions_claimed'],'Corrected principal scope')
 need(a['compression_factor']is a['software_inclusive_factor']is None and a['new_question_credit']==a['new_Lean_declarations']==a['new_measurements']==0 and not a['measured']and not a['whole_source_formalized'],'No unrelated credit')
 need(set(a['component_acceptance']['complete'])=={'author','distinct_review','root_adoption'},'Exact author, distinct review and root adoption')
 expected_math={'author':'a8f8f195a841a33933cdf96692a140c4b0e62126b7794af591711368cef47c68','distinct_review':'ac809df4a7380be8f0959bd97d98f3eaf781492d45f059d242a2b100758b2355','root_adoption':'9fcdf6f8401acce17c358ab777dd9788d00720556c43136fc5c2e09f5ddcc07d'}
 need({k:v['decoded_sha256']for k,v in a['component_acceptance']['complete'].items()}==expected_math,'Exact mathematical acceptance chain')
 need(scope['original']=='L045'and scope['principal_contract']==a['principal_contract'],'Exact positive principal contract')
 need(scope['corrections']==a['intermediate_corrections']and len(a['intermediate_corrections'])==5,'Five explicit supporting corrections')
 need(scope['context_only']==a['ancillary_scope']and len(a['ancillary_scope'])==5 and scope['status']=='ROOT_MATHEMATICS_ACCEPTED_PUBLICATION_GATE_PENDING'and scope['whole_original_credit']==0 and scope['frozen_source_routes_unchanged'],'Historical context and publication gate')
 need(scope['retained_assertions']==a['retained_assertions']and len(a['retained_assertions'])==11 and a['retained_assertions']==a['retained_inputs']['proof_inputs'],'Named borrowed assertions preserved')
 need(not a['principal_negative_converse_claimed']and not scope['principal_negative_converse_claimed']and scope['announced_PSL3_PSU3_negative_not_promoted']and scope['full_Aut_reversal'],'Positive-only theorem and full automorphism criterion')
 need(len(scope['claims'])==36 and len(a['principal_claims'])==2 and all(not x.get('conditional_on',[])for x in a['principal_claims']),'All exact source dispositions and complete principal routes')
 need(a['counts']==dict(source_dispositions=36,principal_positive_statements=2,components=13,finite_parameter_entries=35,sporadic_groups=26,manuscripts=15,synthesis_pages=7,acquired_pages=51,complete_reading_volume_pages=58),'Exact source and finite conventions')
 need((a['immediate_manuscripts'],a['physical_pages'],a['synthesis_pages'])==(15,58,7),'Complete reading volume without duplicate page count')
 need(len(a['complete_acquired_proofs'])==47 and len(a['new_native_manuscripts'])==15 and sum(m['physical_pages']for m in a['new_native_manuscripts'])==58,'Complete acquired proof closure')
 need((a['logical_files'],a['restored_mathematical_and_audit_files'],a['acquired_packets'],a['source_assets_hash_only'],a['relative_locator_records'])==(2635,2544,48,91,993),'Exact complete closure')
 need(a['required_predecessor']==dict(recoveries=81,principal_refutations=1,handled_mathematical_originals=82,pending_mathematical_originals=23,measured_recoveries=53,unmeasured_recoveries=28),'Exact predecessor')
 need(a['proposed_register_after']==dict(recoveries=82,principal_refutations=1,handled_mathematical_originals=83,pending_mathematical_originals=22,measured_recoveries=53,unmeasured_recoveries=29),'Exact proposed disposition')
def registration_mutations():
 return [('duplicate',lambda c,a,s:c['admitted_original_ids'].append('L045')),('omit other pending',lambda c,a,s:c['accessible_pending_original_ids'].remove('F009')),('factor',lambda c,a,s:a.update(compression_factor=2)),('unrestricted',lambda c,a,s:a.update(all_original_assertions_claimed=True)),('lose correction',lambda c,a,s:a['intermediate_corrections'].pop()),('lose retained theorem',lambda c,a,s:s['retained_assertions'].pop()),('lose acquired proof',lambda c,a,s:a['complete_acquired_proofs'].pop(next(iter(a['complete_acquired_proofs'])))),('lose distinct review',lambda c,a,s:a['component_acceptance']['complete'].pop('distinct_review')),('wrong adoption',lambda c,a,s:a['component_acceptance']['complete']['root_adoption'].update(decoded_sha256='0'*64)),('question',lambda c,a,s:a.update(new_question_credit=1)),('wrong finite count',lambda c,a,s:a['counts'].update(finite_parameter_entries=34)),('extra documentary omission',lambda c,a,s:a.update(source_assets_hash_only=92)),('borrowed proof erased',lambda c,a,s:a['retained_inputs']['proof_inputs'].pop()),('automatic credit',lambda c,a,s:a.update(whole_original_credit=1)),('wrong edition',lambda c,a,s:a['source_identity'].update(sha256='0'*64)),('omit coverage',lambda c,a,s:a['literal_coverage'].update(sha256='0'*64)),('negative converse',lambda c,a,s:a.update(principal_negative_converse_claimed=True)),('promote announcement',lambda c,a,s:s.update(announced_PSL3_PSU3_negative_not_promoted=False))]
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
  if x['original_id']!='L045':need(x==y,'Another original entry changed')
  else:
   need(set(x)==set(y),'L045 original schema')
   for k in set(x)-{'current_principal_recovery','next_obligation'}:need(x[k]==y[k],'Historical L045 property changed')
   q=y['current_principal_recovery'];need(q['historical_admission_evidence']==x['current_principal_recovery']and q['principal_contract_admitted']and q['complete_principal_contract_recovered']and q['corrected_principal_recovery']and not q['all_original_assertions_claimed']and not q['measured'],'Qualified recovery')
   need(q['source_qualifications']==a['intermediate_corrections']and q['ancillary_scope']==a['ancillary_scope']and q['counts']==a['counts'],'Catalogue scope preserved')
 need(cat['current_recovery_counts']==dict(active=106,admitted=82,refuted=1,handled=83,measured=53,measurement_pending=29,pending=22,editorial=1),'Catalogue partition')
 reg=load(root,c['current_science_registration']['path']);need(reg['source_ids']==['L045']and reg['previous_registration']==old['current_science_registration']and reg['principal_originals_added']==1 and reg['measurement_originals_added']==reg['new_question_credit']==reg['new_Lean_declarations']==reg['comparison_topics_added']==0 and reg['compression_factor']is None and not reg['whole_source_formalized'],'One scientific registration')
 need(len(reg['admissions'])==1 and reg['admissions'][0]['path']==REC+'/admission.json','Registration admission');bind(root,reg['admissions'][0])
 for r in list(a['component_acceptance']['complete'].values())+list(a['complete_acquired_proofs'].values()):bind(root,r)
 for k in ['literal_source_contract','literal_coverage','literal_scope','portable_policy','public_application_adapter','manuscript_inventory','complete_reading_volume']:bind(root,a[k])
 for k in ['source_map','scope_routes','portable_report','portable_checker','portable_replay','portable_transport','portable_adaptation']:bind(root,a[k])
 for m in a['new_native_manuscripts']:bind(root,m['tex']);bind(root,m['pdf'])
 t=load(root,a['portable_transport']['path']);need(sha(root/a['portable_transport']['path'])==TRANSPORT and len(t['files'])==2635 and len(t['packets'])==48 and t['whole_original_credit']==0,'Frozen complete transport')
 payloads={r['public_path']:r for r in t['files']if 'public_path'in r};need(len(payloads)==1474 and sum(r['transport'].endswith('HASH_ONLY')for r in t['files'])==91,'Exact payload and documentary boundary')
 for path,r in payloads.items():bind(root,dict(r,path=path))
 replay=load(root,a['portable_report']['path']);need(replay['status']=='PASS_PUBLIC_L045_COMPLETE_CLOSURE'and replay['transport_sha256']==TRANSPORT and replay['checker_sha256']==a['portable_checker']['sha256'],'Completed exact replay')
 need((replay['logical_records'],replay['restored_files'],replay['distinct_decoded_payloads'],replay['acquired_packets'],replay['acquired_exports'],replay['exact_metadata_pins_checked'])==(2635,2544,1474,48,1866,25542),'Complete public replay scope')
 application=replay['application'];need(application['status']=='PASS_PUBLIC_L045_APPLICATION'and application['interfaces']==dict(source_claims=36,finite_parameters=35,sporadics=26,components=13,pending=[]),'Exact source-free mathematical interface replay')
 need(not application['documentary_source_replayed']and application['unchanged_author_mathematical_code']and not application['new_census'],'Documentary boundary and unchanged mathematics')
 need(len(application['damaged_controls'])==8 and len(application['optimization_guards'])==6 and len(replay['malformed_transport_controls'])==9 and len(replay['portable_optimization_guards'])==2 and not replay['private_proof_fallback']and not replay['mathematical_census_repeated'],'Meaningful guards and no private fallback')
 need(replay['native_pages']==7 and replay['native_text_identical']and replay['application_stderr_empty']and(application['acquired_manuscripts'],application['acquired_pages'],application['synthesis_pages'],application['full_reading_volume_pages'])==(14,51,7,58),'Complete native/execution output')
 prior=load(root,history['papers/catalogue_corrected_unmeasured.json']['path']);native=load(root,'papers/catalogue_corrected_unmeasured.json');need(native['entries'][:-15]==prior['entries']and native['original_ids']==prior['original_ids']+['L045']and native['acquired_dependencies']==prior['acquired_dependencies']and native['existing_comparison_topic_count']==19 and native['new_measurements']==0,'Previous native and measured catalogue unchanged')
 aliases=load(root,AUD+'/native_input_aliases.json')
 expected_alias={'status': 'EXACT_LITERAL_NATIVE_INPUT_ALIAS', 'manuscript_id': 'L045-finite_lie-4', 'literal_input': 'table.tex', 'source': {'path': 'audit/recoveries/L045/v1/objects/a8/a8d5c1570b35fa73029be9667d8f2e0a25e897548c7d1bd40db5fc63f749ccca.tex', 'bytes': 987, 'sha256': 'a8d5c1570b35fa73029be9667d8f2e0a25e897548c7d1bd40db5fc63f749ccca'}, 'alias': {'path': 'audit/recoveries/L045/v1/objects/a1/table.tex', 'bytes': 987, 'sha256': 'a8d5c1570b35fa73029be9667d8f2e0a25e897548c7d1bd40db5fc63f749ccca'}, 'frozen_scientific_bytes_changed': False}
 need(aliases==[expected_alias],'Exact literal TeX table alias only')
 for row in aliases:
  bind(root,row['source']);bind(root,row['alias']);need((root/row['source']['path']).read_bytes()==(root/row['alias']['path']).read_bytes(),'Literal input byte identity')
 for x,y in zip(native['entries'][-15:],a['new_native_manuscripts']):
  need(x['id']==y['id']and x['tex']==y['tex']['path']and x['pdf']==y['pdf']['path']and x['physical_pages']==y['physical_pages']and not x['measured']and x['compression_factor']is None,'Exact native routes')
  need(x['tex_inputs']==([expected_alias['alias']['path']]if x['id']=='L045-finite_lie-4'else[]),'Every actual literal native input registered')
 paper=load(root,'papers/latest_catalogue.json');oldpaper=load(root,history['papers/latest_catalogue.json']['path']);need(set(paper)==set(oldpaper),'Paper schema')
 for k in set(oldpaper)-{'active_source_catalogue','corrected_unmeasured_scientific_catalogue'}:need(paper[k]==oldpaper[k],'Other paper route changed')
 need(paper['active_source_catalogue']==c['active_catalogue'],'Active source route');bind(root,paper['corrected_unmeasured_scientific_catalogue'])
 oldtree=ast.parse((root/history['scripts/verify_snapshot.py']['path']).read_text());newtree=ast.parse((root/'scripts/verify_snapshot.py').read_text());added={'check_previous_science82','check_science82'}
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
 op=load(root,AUD+'/operational_review.json');need(op['status']=='ACCEPTED_L045_PUBLIC_ONLY_PORTABLE_CLOSURE'and op['whole_original_credit']==0,'Root operational acceptance')
 mapping=load(root,AUD+'/operational_review/mapping.json');need(mapping['manifest_sha256']==sha(root/mapping['manifest']['path']),'Exact review manifest')
 for r in mapping['bindings'].values():bind(root,r)
 omitted={(r['origin'],r['path'],r['bytes'],r['sha256'])for r in t['files']if r['transport'].endswith('HASH_ONLY')}
 for r in mapping['hash_only_bindings'].values():need((r['origin'],r['path'],r['bytes'],r['sha256'])in omitted,'Only exact inherited source omissions')
 parameters=load(root,AUD+'/registration_parameters.json');need(isinstance(parameters['baseline_commit'],str) and len(parameters['baseline_commit'])==40 and parameters['baseline_commit']==load(root,AUD+'/history_routes.json')['baseline_commit'],'Exact bound predecessor commit');need(mapping['manifest_sha256']==parameters['operational_manifest'] and isinstance(parameters['operational_manifest'],str) and len(parameters['operational_manifest'])==64,'Exact bound operational review')
 if require_root:
  gate=load(root,AUD+'/root_integration.json');need(gate['status']=='ROOT_ACCEPTED_SCIENCE82_PUBLICATION'and gate['source_ids']==['L045']and gate['whole_original_credit']==1 and gate['new_question_credit']==gate['new_Lean_declarations']==gate['new_measurements']==0 and gate['compression_factor']is None,'Final root admission')
  for r in gate['bindings']:bind(root,r)
  need(load(root,AUD+'/registration_review/review.json')['status']=='ACCEPTED_L045_REGISTRATION','Distinct registration review')
 return dict(status='PASS_SCIENCE82_PUBLICATION',counts=dict(active=106,corrected_recoveries=82,refuted=1,handled=83,measured=53,unmeasured=29,mathematical_pending=22,editorial=1,archived=55,comparison_topics=19),source_ids=['L045'],old_verifier_functions_preserved=len(oldf),public_payloads={'L045':1474},controls=controls)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--preflight',action='store_true');a=p.parse_args();print(json.dumps(verify(a.repo,not a.preflight)))
