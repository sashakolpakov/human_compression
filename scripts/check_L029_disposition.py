"""L029-only principal refutation; ordinary recoveries and measurements unchanged."""
import sys
if sys.flags.optimize:raise RuntimeError('Optimized Python is not supported')
from pathlib import Path
import argparse,ast,copy,hashlib,json,re
AUD='audit/principal-refutations/L029/v1';BASE='corrections/chiral-residues/v1'
HISTORY=['README.rst','audit/completion.rst','audit/corpus/latest.json','papers/latest_catalogue.json','papers/catalogue_principal_refutations.json','scripts/verify_snapshot.py','audit/protocol.tex','audit/protocol.pdf']
def need(ok,m):
 if not ok:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(root,name):return json.loads((root/name).read_text())
def bind(root,row):
 name=Path(row['path']);p=(root/name).resolve();need(not name.is_absolute()and'..'not in name.parts and p.is_relative_to(root),'Safe public binding')
 need(p.is_file()and p.stat().st_size==row.get('stored_bytes',row['bytes'])and sha(p)==row.get('stored_sha256',row['sha256']),'Exact binding '+str(name))
def semantics(c,old,a,proposal,scope):
 mutable={'status','accessible_pending_complete_recovery','accessible_pending_original_ids','previous_snapshot','active_catalogue','snapshot','refuted_principal_originals','refuted_principal_original_ids','handled_mathematical_originals','handled_mathematical_original_ids','principal_refutation_admissions','current_principal_disposition_registration'}
 need(set(c)==set(old),'Corpus schema unchanged')
 for k in set(old)-mutable:need(c[k]==old[k],'Unrelated corpus field changed '+k)
 need(c['admitted_original_ids']==old['admitted_original_ids']and len(c['admitted_original_ids'])==c['admitted_principal_originals']==85,'Ordinary recoveries unchanged')
 need(c['refuted_principal_original_ids']==old['refuted_principal_original_ids']+['L029']==['F003','L029']and c['refuted_principal_originals']==2,'Only L029 refutation added')
 need(c['accessible_pending_original_ids']==[x for x in old['accessible_pending_original_ids']if x!='L029']and len(c['accessible_pending_original_ids'])==c['accessible_pending_complete_recovery']==18,'Only L029 leaves pending')
 need(c['handled_mathematical_original_ids']==sorted(old['handled_mathematical_original_ids']+['L029'])and c['handled_mathematical_originals']==87,'Exactly one additional handled original')
 sets=[set(c[k])for k in ['admitted_original_ids','refuted_principal_original_ids','accessible_pending_original_ids','editorial_original_ids']]
 need(all(len(c[k])==len(set(c[k]))for k in ['admitted_original_ids','refuted_principal_original_ids','accessible_pending_original_ids','editorial_original_ids']),'No duplicated original')
 need(all(not x&y for i,x in enumerate(sets)for y in sets[i+1:])and set.union(*sets)==set(c['active_original_ids'])and sum(map(len,sets))==106,'Exact disjoint active partition')
 need(len(c['measured_original_ids'])==53 and len(c['measurement_pending_original_ids'])==len(c['scientific_unmeasured_original_ids'])==32,'No measurement change')
 need(not c['all_mathematical_originals_handled']and not c['all_original_proofs_recovered']and not c['all_conjectures_resolved'],'Remaining programme explicit')
 need(c['current_science_registration']==old['current_science_registration'],'Science85 registration unchanged')
 need(c['principal_refutation_admissions']==old['principal_refutation_admissions']+[c['current_principal_disposition_registration']],'Additive disposition record')
 extra={'operational_review_gate','registration_baseline_commit'}
 need(set(a)==set(proposal)|extra,'Exact admission schema')
 for k in set(proposal)-{'status','principal_refutation_credit','publication_gate','registration_baseline'}:need(a[k]==proposal[k],'Reviewed proposal changed '+k)
 need(a['status']=='REVIEWED_PRINCIPAL_REFUTATION_REQUIRING_ROOT_PUBLICATION_GATE'and a['publication_gate']==AUD+'/root_integration.json','Final root gate required')
 need(a['source_ids']==['L029']and a['disposition_kind']=='principal_statement_refuted'and a['principal_refutation_credit']==1 and a['proposed_principal_refutation_credit']==1,'One refutation')
 need(a['ordinary_recovery_credit']==a['measurement_credit']==a['new_question_credit']==a['new_Lean_declarations']==0,'No other credit')
 need(a['compression_factor']is a['software_inclusive_factor']is None and not a['whole_source_formalized'],'No factor or formalization')
 need(a['root_is_distinct_reviewer']and not any(k in a for k in ['root_scientific_adoption','distinct_v2_addendum']),'Actual review roles; no invented duplicate review')
 need(a['scientific_author']['decoded_sha256']=='d9605890c19fd7f3101844c9df846349b3cbf7ce3d08cd7d7ffe6b77ad5c5176'and a['distinct_mathematical_review']['decoded_sha256']=='4c4c51109f5023fce751ad483d5b804a3cba69bc4f0983033e0cc822288c17dc','Exact mathematical acceptance chain')
 need(a['source_identity']['sha256']=='d4b0c8a21e1afb0d430c179d0caa1994ef3a453f5f2bf4212fd604532abdc919'and a['source_url']=='https://doi.org/10.5802/alco.162','Fixed published source')
 need(a['target']['label']=='Theorem 1.1'and a['target']['printed_page']==491 and a['target']['physical_page']==2,'Exact theorem')
 need(a['scope']==scope==proposal['scope']and len(scope['qualifications'])==7,'All reviewed source boundaries')
 ex=a['accepted_counterexample'];need(ex==scope['example']and ex['specified_group_order']==1092 and ex['full_group_order']==2184 and ex['specified_group_index']==2 and ex['residue_component_sizes']==[6,6]and ex['rank']==4 and ex['objects']==112 and ex['chambers']==4368,'Exact full-Aut counterexample')
 need(not a['priority_claim']and not a['absence_of_errata_claim']and not a['later_source_edition_claim']and a['source_question_dispositions']==[],'No unsupported historical/question claims')
 need((a['scientific_packet_roots'],a['acquired_manifest_records'],a['acquired_exports'],a['logical_files'],a['restored_files'],a['documentary_assets_hash_only'],a['provenance_only_manifest_leaves'],a['historical_metadata_leaves'])==(2,3,50,93,85,8,3,1),'Complete declared closure')
 need(a['complete_manuscript']['physical_pages']==5 and a['complete_manuscript']['tex_inputs']==[],'Complete five-page proof')
 need(a['required_predecessor']==dict(recoveries=85,principal_refutations=1,handled_mathematical_originals=86,pending_mathematical_originals=19,measured_recoveries=53,unmeasured_recoveries=32),'Exact predecessor scope')
 need(a['proposed_register_after']==dict(recoveries=85,principal_refutations=2,handled_mathematical_originals=87,pending_mathematical_originals=18,measured_recoveries=53,unmeasured_recoveries=32),'Exact resulting scope')
def mutations():
 return [('duplicate refutation',lambda c,a,s:c['refuted_principal_original_ids'].append('L029')),('false recovery',lambda c,a,s:c['admitted_original_ids'].append('L029')),('pending overlap',lambda c,a,s:c['accessible_pending_original_ids'].append('L029')),('lose other pending',lambda c,a,s:c['accessible_pending_original_ids'].pop()),('changed measurements',lambda c,a,s:c['measured_original_ids'].pop()),('false completion',lambda c,a,s:c.update(all_mathematical_originals_handled=True)),('ordinary credit',lambda c,a,s:a.update(ordinary_recovery_credit=1)),('question credit',lambda c,a,s:a.update(new_question_credit=1)),('formal credit',lambda c,a,s:a.update(whole_source_formalized=True)),('factor',lambda c,a,s:a.update(compression_factor=2)),('false review role',lambda c,a,s:a.update(root_is_distinct_reviewer=False)),('group conflation',lambda c,a,s:a['accepted_counterexample'].update(full_group_order=1092)),('lose qualification',lambda c,a,s:s['qualifications'].pop()),('wrong source',lambda c,a,s:a['source_identity'].update(sha256='0'*64)),('wrong review',lambda c,a,s:a['distinct_mathematical_review'].update(decoded_sha256='0'*64)),('invented adoption',lambda c,a,s:a.update(root_scientific_adoption={})),('ordinary science pointer',lambda c,a,s:c['current_science_registration'].update(path='wrong')),('missing proof record',lambda c,a,s:a['complete_acquired_manifest_records'].pop(next(iter(a['complete_acquired_manifest_records']))))]
def verify(root,require_root=True):
 root=Path(root).resolve();routes=load(root,AUD+'/history_routes.json')['routes'];need(set(routes)==set(HISTORY),'Eight exact predecessor pointers')
 for row in routes.values():bind(root,row)
 old=load(root,routes['audit/corpus/latest.json']['path']);c=load(root,'audit/corpus/latest.json');a=load(root,BASE+'/admission.json');proposal=load(root,BASE+'/admission_proposal.json');scope=load(root,BASE+'/scope_routes.json');params=load(root,AUD+'/registration_parameters.json')
 need(sha(root/BASE/'admission_proposal.json')==params['proposal_sha256'],'Frozen proposal');semantics(c,old,a,proposal,scope)
 need(a['registration_baseline_commit']==params['baseline_commit']==load(root,AUD+'/history_routes.json')['baseline_commit']and len(params['baseline_commit'])==40,'Exact registration baseline')
 need(a['registration_baseline']==params['baseline_commit'],'Registration baseline resolved explicitly')
 for k in ['active_catalogue','snapshot','current_science_registration','current_principal_disposition_registration']:bind(root,c[k])
 need(c['previous_snapshot']==routes['audit/corpus/latest.json']and load(root,c['snapshot']['path'])=={k:v for k,v in c.items()if k!='snapshot'},'Exact current snapshot and predecessor')
 before=load(root,old['active_catalogue']['path']);cat=load(root,c['active_catalogue']['path']);need(len(cat['entries'])==len(before['entries'])==106,'Fixed catalogue')
 mutable={'status','entries','accessible_pending_complete_recovery','refuted_principal_originals','refuted_principal_original_ids','handled_mathematical_originals','handled_mathematical_original_ids','review_revision','previous_catalogue','current_recovery_counts','new_principal_refutation_credit'}
 need(set(cat)==set(before),'Catalogue schema')
 for k in set(before)-mutable:need(cat[k]==before[k],'Other catalogue field '+k)
 for x,y in zip(before['entries'],cat['entries']):
  if x['original_id']!='L029':need(x==y,'Another original changed')
  else:
   need(set(x)==set(y),'L029 source schema')
   for k in set(x)-{'edition','current_principal_recovery','next_obligation'}:need(x[k]==y[k],'Historical L029 property changed')
   d=y['current_principal_recovery'];need(d['historical_admission_evidence']==x['current_principal_recovery']and d['status']=='CLOSED_BY_REVIEWED_PRINCIPAL_REFUTATION'and d['disposition_kind']=='principal_statement_refuted'and not d['principal_contract_admitted']and d['original_fully_handled']and not d['all_original_assertions_claimed']and not d['measured']and d['compression_factor']is None,'Exact qualified disposition')
   need(d['scope']==scope and y['edition']==scope['source_edition']and d['correction_path']==BASE+'/admission.json','Published-edition/source boundary')
 need(cat['current_recovery_counts']==dict(active=106,admitted=85,refuted=2,handled=87,measured=53,measurement_pending=32,pending=18,editorial=1),'Catalogue partition')
 need(cat['refuted_principal_original_ids']==['F003','L029']and cat['refuted_principal_originals']==2 and cat['handled_mathematical_original_ids']==c['handled_mathematical_original_ids']and cat['handled_mathematical_originals']==87 and cat['new_principal_refutation_credit']==1 and cat['new_proof_credit']==0,'Separate catalogue refutation credit')
 reg=load(root,c['current_principal_disposition_registration']['path']);need(reg['source_ids']==['L029']and reg['principal_refutations_added']==reg['mathematical_originals_handled_added']==1 and reg['ordinary_recoveries_added']==reg['new_measurements']==reg['new_question_credit']==reg['new_Lean_credit']==0 and reg['compression_factor']is None,'Only one refutation registered')
 need(reg['previous_science_registration']==old['current_science_registration']and reg['previous_disposition_registration']==old['current_principal_disposition_registration']and reg['previous_corpus']==routes['audit/corpus/latest.json'],'Complete predecessor route');bind(root,reg['admission'])
 for k in ['scientific_author','distinct_mathematical_review','literal_source_contract','literal_frozen_scope','literal_distinct_review','portable_wrapper','portable_checker','portable_transport','portable_policy','public_application_adapter','portable_report','portable_adaptation','native_input_inventory','native_visual_review','program_inventory','scope_routes']:bind(root,a[k])
 for row in a['complete_acquired_manifest_records'].values():bind(root,row)
 programs=load(root,a['program_inventory']['path'])
 for k in ['finite_certificate','expected','original_wrapper','public_adapter']:bind(root,programs[k])
 for k in ['public_alias','exact_original']:bind(root,programs['independent_GAP'][k])
 need(programs['independent_GAP']['public_alias']['sha256']==programs['independent_GAP']['exact_original']['decoded_sha256'],'Literal independent GAP alias')
 for k in ['tex','pdf']:bind(root,a['complete_manuscript'][k])
 need(not re.findall(r'\\(?:input|include)\s*\{([^}]+)\}',(root/a['complete_manuscript']['tex']['path']).read_text()),'No missing literal native input')
 t=load(root,a['portable_transport']['path']);need(len(t['files'])==93 and len(t['packets'])==3 and t['whole_original_credit']==0,'Exact complete transport');payloads={r['public_path']:r for r in t['files']if'public_path'in r}
 need(len(payloads)==53 and sum(r['transport'].endswith('HASH_ONLY')for r in t['files'])==8,'Exact payload/documentary inventory')
 for n,r in payloads.items():bind(root,dict(r,path=n))
 replay=load(root,a['portable_report']['path']);need(replay['status']=='PASS_PUBLIC_L029_CLOSURE'and replay['transport_sha256']==a['portable_transport']['sha256']and replay['checker_sha256']==a['portable_checker']['sha256']and replay['adapter_sha256']==a['public_application_adapter']['sha256'],'Exact completed replay')
 need((replay['logical_files'],replay['restored_files'],replay['decoded_objects'],replay['private_packets'],replay['complete_exports'])==(93,85,53,3,50)and replay['no_private_fallback']and replay['application_stderr_empty'],'Complete public execution')
 app=replay['application'];need(app['finite_exact']and app['specified_group_order']==1092 and app['full_group_order']==2184 and app['subset_intersections']==256 and app['actual_panels']==8736 and app['residue_component_sizes']==[6,6]and app['native_pages']==5 and app['native_text_identical'],'Exact finite/native scope')
 need(len(app['damage_controls'])==3 and len(app['optimization_guards'])==6 and len(replay['malformed_transport_controls'])==12 and len(replay['optimization_guards'])==2,'All execution controls')
 need(app['author_scientific_code_unchanged']and not app['runtime_text_patching']and not app['original_documentary_assets_read']and not app['general_proof_verified_by_program']and not app['independent_GAP_repeated'],'Scientific/runtime boundary')
 paper=load(root,'papers/latest_catalogue.json');oldpaper=load(root,routes['papers/latest_catalogue.json']['path']);need(set(paper)==set(oldpaper),'Paper schema')
 for k in set(oldpaper)-{'active_source_catalogue','principal_refutation_catalogue'}:need(paper[k]==oldpaper[k],'Other paper route changed')
 need(paper['active_source_catalogue']==c['active_catalogue'],'Current source catalogue');bind(root,paper['principal_refutation_catalogue']);bind(root,paper['corrected_unmeasured_scientific_catalogue'])
 before_native=load(root,routes['papers/catalogue_principal_refutations.json']['path']);native=load(root,paper['principal_refutation_catalogue']['path']);need(native['original_ids']==before_native['original_ids']+['L029']and native['entries'][:-1]==before_native['entries'],'Additive separate native refutation catalogue')
 for k in set(before_native)-{'original_ids','entries'}:need(native[k]==before_native[k],'Native catalogue other field')
 e=native['entries'][-1];m=a['complete_manuscript'];need(e['source_ids']==['L029']and e['role']=='principal_statement_refutation'and e['id']==m['id']and e['tex']==m['tex']['path']and e['pdf']==m['pdf']['path']and e['tex_inputs']==[]and e['physical_pages']==5 and not e['measured']and e['compression_factor']is None,'Exact five-page native entry');bind(root,e['admission'])
 oldtree=ast.parse((root/routes['scripts/verify_snapshot.py']['path']).read_text());newtree=ast.parse((root/'scripts/verify_snapshot.py').read_text());added={'check_previous_L029_disposition','check_L029_disposition'}
 def nodes(tree,omit):return [ast.dump(n,include_attributes=False)for n in tree.body if not(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name in omit)]
 need(nodes(oldtree,{'main'})==nodes(newtree,{'main'}|added),'All old non-main verifier ASTs unchanged')
 names=lambda tree:{n.name for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))};need(names(newtree)-names(oldtree)==added,'Exactly two verifier functions')
 controls=[]
 for label,change in mutations():
  cc,aa,ss=copy.deepcopy((c,a,scope));change(cc,aa,ss)
  try:semantics(cc,old,aa,proposal,ss)
  except(ValueError,KeyError):controls.append(label)
  else:raise ValueError('Damaged admission accepted '+label)
 op=load(root,AUD+'/operational_review.json');need(op['status']==params['operational_status'],'Accepted operational review');mapping=load(root,AUD+'/operational_review/mapping.json');need(mapping['manifest_sha256']==params['operational_manifest']==sha(root/mapping['manifest']['path']),'Exact operational manifest')
 for row in mapping['bindings'].values():bind(root,row)
 omitted={(r['origin'],r['path'],r['bytes'],r['sha256'])for r in t['files']if r['transport'].endswith('HASH_ONLY')}
 for row in mapping['hash_only_bindings'].values():need((row['origin'],row['path'],row['bytes'],row['sha256'])in omitted,'Only documentary omissions')
 if require_root:
  gate=load(root,AUD+'/root_integration.json');need(gate['status']=='ROOT_ACCEPTED_L029_PRINCIPAL_REFUTATION_PUBLICATION'and gate['source_ids']==['L029']and gate['principal_refutation_credit']==1 and gate['ordinary_recovery_credit']==gate['new_measurements']==gate['new_question_credit']==gate['new_Lean_credit']==0,'Final root admission')
  for row in gate['bindings']:bind(root,row)
  need(load(root,AUD+'/registration_review/review.json')['status']=='ACCEPTED_SEPARATE_L029_REGISTRATION','Distinct registration acceptance')
 return dict(status='PASS_SEPARATE_L029_PRINCIPAL_REFUTATION',source_ids=['L029'],counts=dict(active=106,corrected_recoveries=85,refuted=2,handled=87,measured=53,unmeasured=32,mathematical_pending=18,editorial=1,archived=55,comparison_topics=19),controls=controls,old_verifier_functions_preserved=len(names(oldtree))-1)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--preflight',action='store_true');a=p.parse_args();print(json.dumps(verify(a.repo,not a.preflight)))
