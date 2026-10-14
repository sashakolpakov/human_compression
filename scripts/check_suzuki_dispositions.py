"""Exactly three principal refutations; recoveries and measurements unchanged."""
import sys
if sys.flags.optimize:raise RuntimeError('Optimized Python is not supported')
from pathlib import Path
import argparse,ast,copy,hashlib,json,re
AUD='audit/principal-refutations/suzuki-subfields/v1';BASE='corrections/suzuki-subfields/v1';IDS=['L110','L114','L115']
HISTORY=['README.rst','audit/completion.rst','audit/corpus/latest.json','papers/latest_catalogue.json','papers/catalogue_principal_refutations.json','scripts/verify_snapshot.py','audit/protocol.tex','audit/protocol.pdf']
CHAINS={
 'L110':['09eae7559e84ee7820389c3a2d8859443e161b86368bc460a92ec5a194be85af','53f3e640dd7d88708e7d5909d6288eded4b26fd99f7ae3ae492513e3b16977d5','5c3f7b04210dbab2669147f52a4a3ae8b0ced3ce7d672186d8ab309e0255fd2f'],
 'L114':['fb18e3f0f489141c4728e115eb576cb019c4c0bae8fa9d4fb187eef9d473cf26','2d871a0ea2d00fa590ca8243a73d18a9d4120eb988a18f0f343bc4722207d1a3','d94b8d06d1a1a0ffcc93f5a826a45b18f30693c6a11a495d3b3539da5e461c80'],
 'L115':['de55785460d1c8ef96dfe19581ce273a50b2d01aab22654f1a5f0e75c818a69c','43804821fb1c59bb604aa0e81758aa33fdfc607619815c36851690b0e4df87ed','33fb6d9c4cb1aa2808dfd93ac78e5bd67327be13c3c4b38c739ac3fa2278015e']}
SOURCES={'L110':'9aa05e66b8fc52c25eb1f40a6df44e143957e2f7a89b19242c0d1b312c12aebe','L114':'04142c0b5415b3b3ec6a006c3aab86247f4be3576b94a92944cca9f74007dcc9','L115':'8a94f8a0d72f46fececd21e7a6f437d76106936ef27c0dd18c55f6cd49dd6c51'}
def need(v,m):
 if not v:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(root,name):return json.loads((root/name).read_text())
def bind(root,row):
 name=Path(row['path']);p=(root/name).resolve();need(not name.is_absolute()and'..'not in name.parts and p.is_relative_to(root),'Safe public pin')
 need(p.is_file()and p.stat().st_size==row.get('stored_bytes',row['bytes'])and sha(p)==row.get('stored_sha256',row['sha256']),'Exact binding '+str(name))
def semantics(c,old,a,proposal,scope):
 mutable={'status','accessible_pending_complete_recovery','accessible_pending_original_ids','previous_snapshot','active_catalogue','snapshot','refuted_principal_originals','refuted_principal_original_ids','handled_mathematical_originals','handled_mathematical_original_ids','principal_refutation_admissions','current_principal_disposition_registration'}
 need(set(c)==set(old),'Unchanged corpus schema')
 for k in set(old)-mutable:need(c[k]==old[k],'Unrelated corpus field changed '+k)
 need(c['admitted_original_ids']==old['admitted_original_ids']and len(c['admitted_original_ids'])==c['admitted_principal_originals']==85,'No ordinary recovery added')
 need(c['refuted_principal_original_ids']==old['refuted_principal_original_ids']+IDS==['F003','L029']+IDS and c['refuted_principal_originals']==5,'Exactly three refutations')
 need(c['accessible_pending_original_ids']==[s for s in old['accessible_pending_original_ids']if s not in IDS]and len(c['accessible_pending_original_ids'])==c['accessible_pending_complete_recovery']==15,'Only three sources leave pending')
 need(c['handled_mathematical_original_ids']==sorted(old['handled_mathematical_original_ids']+IDS)and c['handled_mathematical_originals']==90,'Exactly three handled originals')
 keys=['admitted_original_ids','refuted_principal_original_ids','accessible_pending_original_ids','editorial_original_ids'];sets=[set(c[k])for k in keys]
 need(all(len(c[k])==len(set(c[k]))for k in keys)and all(not x&y for i,x in enumerate(sets)for y in sets[i+1:])and set.union(*sets)==set(c['active_original_ids'])and sum(map(len,sets))==106,'Exact active partition')
 need(len(c['measured_original_ids'])==53 and len(c['measurement_pending_original_ids'])==len(c['scientific_unmeasured_original_ids'])==32,'Measurement counts unchanged')
 need(not c['all_mathematical_originals_handled']and not c['all_original_proofs_recovered']and not c['all_conjectures_resolved'],'Remaining programme explicit')
 need(c['current_science_registration']==old['current_science_registration'],'Science85 unchanged')
 need(c['principal_refutation_admissions']==old['principal_refutation_admissions']+[c['current_principal_disposition_registration']],'Additive shared registration')
 extra={'publication_gate','operational_review_gate','registration_baseline_commit'}
 need(set(a)==set(proposal)|extra,'Exact aggregate admission schema')
 for k in set(proposal)-{'status','principal_refutation_credit','components'}:need(a[k]==proposal[k],'Accepted proposal altered '+k)
 need(a['status']=='REVIEWED_THREE_PRINCIPAL_REFUTATIONS_REQUIRING_ROOT_GATES'and a['publication_gate']==AUD+'/root_integration.json'and a['operational_review_gate']==AUD+'/operational_review.json','Root gates remain required')
 need(a['source_ids']==IDS and a['disposition_kind']=='principal_statement_refuted'and a['principal_refutation_credit']==a['proposed_principal_refutation_credit']==3,'Three separate dispositions')
 need(a['ordinary_recovery_credit']==a['measurement_credit']==a['new_question_credit']==a['new_Lean_declarations']==0,'No recovery, measurement, question or Lean credit')
 need(not a['whole_sources_recovered']and not a['whole_sources_formalized']and a['compression_factor']is a['software_inclusive_factor']is None,'No whole recovery or factors')
 need(not a['priority_claim']and not a['absence_of_errata_claim']and not a['later_source_edition_claim']and a['source_question_dispositions']==[],'No historical or question claims')
 need([x['source_id']for x in a['components']]==IDS and len(scope['components'])==3,'Three ordered source scopes')
 for x,y,s in zip(a['components'],proposal['components'],scope['components']):
  sid=x['source_id'];need(set(x)==set(y),'Separate component schema')
  for k in set(y)-{'principal_refutation_credit'}:need(x[k]==y[k],'Separate accepted component altered '+sid+' '+k)
  need(x['principal_refutation_credit']==x['proposed_principal_refutation_credit']==1 and x['ordinary_recovery_credit']==0,'One refutation per original')
  need(x['scope']==s==y['scope']and s['source_id']==sid and s['source']['sha256']==SOURCES[sid],'Exact source and complete qualifications')
  need([x[k]['decoded_sha256']for k in ['scientific_author','distinct_mathematical_review','root_adoption']]==CHAINS[sid],'Actual author/distinct/adoption chain')
  need(x['publication_gate']==f'audit/principal-refutations/{sid}/v1/root_integration.json','Distinct per-source gate')
  need(x['complete_manuscript']['physical_pages']=={'L110':3,'L114':4,'L115':4}[sid]and x['complete_manuscript']['tex_inputs']==[],'Complete manuscript')
 need([s['scope']for s in a['components']]==a['literal_scope_routes'],'Source routes identical')
 w={s['source_id']:s['scope']['witness']for s in a['components']}
 need(w['L110']['rank']==4 and w['L110']['intersection_groups']==16 and w['L110']['maximal_inclusions']==32,'Actual weak rank-four witness')
 need(w['L114']['intersection_orders']==[20,52,164,4]and w['L114']['rank_two_counterexample_valencies']==[65,8]and w['L114']['source_rank_two_valencies']==[2,32768],'Rank-three lattice and rank-two valencies')
 need(w['L115']['full_Aut_classes']==41 and w['L115']['source_total']==14 and w['L115']['valencies']==[65,8],'Specified-Aut family only')
 need((a['scientific_author_packets'],a['distinct_review_packets'],a['root_adoption_packets'],a['acquired_manifest_records'],a['acquired_exports'],a['logical_files'],a['restored_files'],a['documentary_assets_hash_only'],a['nonacquiring_historical_provenance_leaves'])==(3,3,3,9,61,185,161,24,14),'Exact complete closure')
 need(a['required_predecessor']==dict(recoveries=85,principal_refutations=2,handled_mathematical_originals=87,pending_mathematical_originals=18,measured_recoveries=53,unmeasured_recoveries=32),'Exact predecessor counts')
 need(a['proposed_register_after']==dict(recoveries=85,principal_refutations=5,handled_mathematical_originals=90,pending_mathematical_originals=15,measured_recoveries=53,unmeasured_recoveries=32),'Exact proposed counts')
def mutations():
 return [('duplicate refutation',lambda c,a,s:c['refuted_principal_original_ids'].append('L114')),('false recovery',lambda c,a,s:c['admitted_original_ids'].append('L110')),('pending overlap',lambda c,a,s:c['accessible_pending_original_ids'].append('L115')),('lose other pending',lambda c,a,s:c['accessible_pending_original_ids'].pop()),('measurement change',lambda c,a,s:c['measured_original_ids'].pop()),('false completion',lambda c,a,s:c.update(all_mathematical_originals_handled=True)),('ordinary credit',lambda c,a,s:a.update(ordinary_recovery_credit=3)),('question credit',lambda c,a,s:a.update(new_question_credit=1)),('formal credit',lambda c,a,s:a.update(whole_sources_formalized=True)),('factor',lambda c,a,s:a.update(compression_factor=2)),('lost original',lambda c,a,s:a['components'].pop()),('swapped review',lambda c,a,s:a['components'][0].update(distinct_mathematical_review=a['components'][1]['distinct_mathematical_review'])),('bare incidence count',lambda c,a,s:a['components'][2]['scope']['witness'].update(bare_incidence_classes=41)),('lost qualification',lambda c,a,s:s['components'][1]['qualifications'].pop()),('wrong source',lambda c,a,s:a['components'][2]['scope']['source'].update(sha256='0'*64)),('wrong gate',lambda c,a,s:a['components'][1].update(publication_gate=a['components'][0]['publication_gate'])),('duplicate credit',lambda c,a,s:a['components'][0].update(principal_refutation_credit=2)),('invented review',lambda c,a,s:a.update(second_distinct_root_mathematical_review={})),('old science pointer',lambda c,a,s:c['current_science_registration'].update(path='wrong')),('missing acquired proof',lambda c,a,s:a['complete_acquired_manifest_records'].pop(next(iter(a['complete_acquired_manifest_records'])))),('wrong predecessor',lambda c,a,s:a['required_predecessor'].update(handled_mathematical_originals=86)),('strong rank-four geometry',lambda c,a,s:a['components'][0]['scope']['witness'].update(flag_transitive=True))]
def verify(root,require_root=True):
 root=Path(root).resolve();history=load(root,AUD+'/history_routes.json');routes=history['routes'];need(set(routes)==set(HISTORY),'Eight exact old pointers')
 for r in routes.values():bind(root,r)
 old=load(root,routes['audit/corpus/latest.json']['path']);c=load(root,'audit/corpus/latest.json');a=load(root,BASE+'/admission.json');proposal=load(root,BASE+'/admission_proposal.json');scope=load(root,BASE+'/scope_routes.json');params=load(root,AUD+'/registration_parameters.json')
 need(sha(root/BASE/'admission_proposal.json')==params['proposal_sha256'],'Exact frozen proposal');semantics(c,old,a,proposal,scope)
 need(a['registration_baseline_commit']==a['registration_baseline']==params['baseline_commit']==history['baseline_commit']=='16fd924ec3fd058225d209d8232dd4473cbc5361','Exact registration baseline')
 for k in ['active_catalogue','snapshot','current_science_registration','current_principal_disposition_registration']:bind(root,c[k])
 need(c['previous_snapshot']==routes['audit/corpus/latest.json']and load(root,c['snapshot']['path'])=={k:v for k,v in c.items()if k!='snapshot'},'Exact current snapshot')
 before=load(root,old['active_catalogue']['path']);cat=load(root,c['active_catalogue']['path']);need(len(cat['entries'])==len(before['entries'])==106 and set(cat)==set(before),'Catalogue schema')
 mutable={'status','entries','accessible_pending_complete_recovery','refuted_principal_originals','refuted_principal_original_ids','handled_mathematical_originals','handled_mathematical_original_ids','review_revision','previous_catalogue','current_recovery_counts','new_principal_refutation_credit'}
 for k in set(before)-mutable:need(cat[k]==before[k],'Other catalogue field '+k)
 components={x['source_id']:x for x in a['components']}
 for x,y in zip(before['entries'],cat['entries']):
  sid=x['original_id']
  if sid not in IDS:need(x==y,'Unrelated original changed')
  else:
   need(set(x)==set(y),'Source entry schema')
   for k in set(x)-{'edition','current_principal_recovery','next_obligation'}:need(x[k]==y[k],'Historical source field changed')
   d=y['current_principal_recovery'];s=components[sid]['scope'];need(d['historical_admission_evidence']==x['current_principal_recovery']and d['status']=='CLOSED_BY_REVIEWED_PRINCIPAL_REFUTATION'and d['disposition_kind']=='principal_statement_refuted'and not d['principal_contract_admitted']and d['original_fully_handled']and not d['all_original_assertions_claimed']and not d['measured']and d['compression_factor']is None and not d['whole_source_formalized'],'Exact qualified disposition')
   need(d['scope']==s and d['source_targets']==s['targets']and y['edition']==s['source']['edition']and d['correction_path']==BASE+'/'+sid+'/admission.json','Exact source-specific route')
 need(cat['current_recovery_counts']==dict(active=106,admitted=85,refuted=5,handled=90,measured=53,measurement_pending=32,pending=15,editorial=1),'Catalogue counts')
 for k in ['refuted_principal_original_ids','refuted_principal_originals','handled_mathematical_original_ids','handled_mathematical_originals']:need(cat[k]==c[k],'Catalogue/current identity')
 need(cat['new_principal_refutation_credit']==3 and cat['new_proof_credit']==0,'Refutations only')
 reg=load(root,c['current_principal_disposition_registration']['path']);need(reg['source_ids']==IDS and reg['principal_refutations_added']==reg['mathematical_originals_handled_added']==3 and reg['ordinary_recoveries_added']==reg['new_measurements']==reg['new_question_credit']==reg['new_Lean_credit']==0 and reg['compression_factor']is None,'Shared registration credit')
 need(reg['previous_science_registration']==old['current_science_registration']and reg['previous_disposition_registration']==old['current_principal_disposition_registration']and reg['previous_corpus']==routes['audit/corpus/latest.json'],'Complete predecessor route');bind(root,reg['admission'])
 need(len(reg['individual_admissions'])==3 and reg['individual_publication_gates']==a['publication_gates'],'Separate admissions/gates')
 for component,r in zip(a['components'],reg['individual_admissions']):
  bind(root,r);one=load(root,r['path']);need(r['path']==BASE+'/'+component['source_id']+'/admission.json','Separate stable admission path')
  need(one==dict(component,status='REVIEWED_PRINCIPAL_REFUTATION_REQUIRING_ROOT_GATE',shared_admission=reg['admission'],operational_review_gate=AUD+'/operational_review.json',registration_baseline_commit=params['baseline_commit']),'Exact individual admission')
 publicpins=[]
 def walk(x):
  if isinstance(x,dict):
   if isinstance(x.get('path'),str)and'sha256'in x and x['path'].startswith(('corrections/','audit/','papers/','scripts/')):bind(root,x);publicpins.append(x['path'])
   for v in x.values():walk(v)
  elif isinstance(x,list):
   for v in x:walk(v)
 walk(a)
 programs=load(root,a['program_inventory']['path']);walk(programs)
 for p in programs['components']:need(p['independent_GAP']['public_alias']['sha256']==p['independent_GAP']['exact_original']['decoded_sha256'],'Exact independent program alias')
 for component in a['components']:
  m=component['complete_manuscript'];need(not re.findall(r'\\(?:input|include)\s*\{([^}]+)\}',(root/m['tex']['path']).read_text()),'No missing literal native input')
 t=load(root,a['portable_transport']['path']);need(len(t['files'])==185 and len(t['packets'])==9 and t['whole_original_credit']==0,'Exact transport inventory');payloads={r['public_path']:r for r in t['files']if'public_path'in r}
 need(len(payloads)==118 and sum(r['transport'].endswith('HASH_ONLY')for r in t['files'])==24,'Exact stored/documentary boundary')
 for name,r in payloads.items():bind(root,dict(r,path=name))
 replay=load(root,a['portable_report']['path']);need(replay['status']=='PASS_PUBLIC_SUZUKI_CLOSURE'and replay['transport_sha256']==a['portable_transport']['sha256']and replay['checker_sha256']==a['portable_checker']['sha256']and replay['adapter_sha256']==a['public_application_adapter']['sha256'],'Exact completed public replay')
 need((replay['logical_files'],replay['restored_files'],replay['decoded_objects'],replay['private_packets'],replay['complete_exports'],replay['metadata_pins'])==(185,161,118,9,61,696)and replay['no_private_fallback']and replay['application_stderr_empty'],'Complete public closure')
 app=replay['application'];need(app['status']=='PASS_PUBLIC_SUZUKI_APPLICATION'and app['native_pages']==11 and[s['source_id']for s in app['components']]==IDS,'Separate exact replays')
 need(all(s['native_text_identical']and s['author_scientific_code_unchanged']for s in app['components'])and[s['native_pages']for s in app['components']]==[3,4,4],'Unchanged complete native manuscripts')
 need([len(s['damage_controls'])for s in app['components']]==[0,3,2]and len(app['optimization_guards'])==14 and len(replay['malformed_transport_controls'])==14 and len(replay['optimization_guards'])==2,'All bounded controls')
 need(not app['runtime_text_patching']and not app['private_fallback']and not app['old_censuses_repeated']and not app['independent_GAP_repeated']and not app['general_proofs_verified_by_program'],'Exact software/proof boundary')
 paper=load(root,'papers/latest_catalogue.json');oldpaper=load(root,routes['papers/latest_catalogue.json']['path']);need(set(paper)==set(oldpaper),'Paper schema')
 for k in set(oldpaper)-{'active_source_catalogue','principal_refutation_catalogue'}:need(paper[k]==oldpaper[k],'Other paper pointer changed')
 need(paper['active_source_catalogue']==c['active_catalogue'],'Active catalogue route');bind(root,paper['principal_refutation_catalogue']);bind(root,paper['corrected_unmeasured_scientific_catalogue'])
 oldnative=load(root,routes['papers/catalogue_principal_refutations.json']['path']);native=load(root,paper['principal_refutation_catalogue']['path']);need(native['original_ids']==oldnative['original_ids']+IDS and native['entries'][:-3]==oldnative['entries'],'Additive separate native entries')
 for k in set(oldnative)-{'original_ids','entries'}:need(native[k]==oldnative[k],'Other native catalogue field changed')
 for e,component,r in zip(native['entries'][-3:],a['components'],reg['individual_admissions']):
  m=component['complete_manuscript'];need(e==dict(id=m['id'],title=m['title'],tex=m['tex']['path'],pdf=m['pdf']['path'],tex_inputs=[],compiler='pdflatex',physical_pages=m['physical_pages'],source_ids=[component['source_id']],role='principal_statement_refutation',measured=False,compression_factor=None,admission=r),'Exact source-specific native entry')
 oldtree=ast.parse((root/routes['scripts/verify_snapshot.py']['path']).read_text());newtree=ast.parse((root/'scripts/verify_snapshot.py').read_text());added={'check_previous_suzuki_dispositions','check_suzuki_dispositions'}
 def nodes(t,omit):return[ast.dump(n,include_attributes=False)for n in t.body if not(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name in omit)]
 names=lambda t:{n.name for n in t.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
 need(nodes(oldtree,{'main'})==nodes(newtree,{'main'}|added)and names(newtree)-names(oldtree)==added,'Exactly two new functions, all old non-main ASTs preserved')
 controls=[]
 for label,change in mutations():
  cc,aa,ss=copy.deepcopy((c,a,scope));change(cc,aa,ss)
  try:semantics(cc,old,aa,proposal,ss)
  except(ValueError,KeyError):controls.append(label)
  else:raise ValueError('Damaged admission accepted '+label)
 op=load(root,AUD+'/operational_review.json');need(op['status']==params['operational_status'],'Accepted operational review');mapping=load(root,AUD+'/operational_review/mapping.json');need(mapping['manifest_sha256']==params['operational_manifest']==sha(root/mapping['manifest']['path']),'Exact operational manifest')
 for r in mapping['bindings'].values():bind(root,r)
 omitted={(r['origin'],r['path'],r['bytes'],r['sha256'])for r in t['files']if r['transport'].endswith('HASH_ONLY')}
 for r in mapping['hash_only_bindings'].values():need((r['origin'],r['path'],r['bytes'],r['sha256'])in omitted,'Only declared documentary omissions')
 if require_root:
  gate=load(root,AUD+'/root_integration.json');need(gate['status']=='ROOT_ACCEPTED_THREE_SUZUKI_PRINCIPAL_REFUTATIONS'and gate['source_ids']==IDS and gate['principal_refutation_credit']==3 and gate['ordinary_recovery_credit']==gate['new_measurements']==gate['new_question_credit']==gate['new_Lean_credit']==0,'Shared final gate')
  for r in gate['bindings']:bind(root,r)
  for sid in IDS:
   g=load(root,f'audit/principal-refutations/{sid}/v1/root_integration.json');need(g['status']=='ROOT_ACCEPTED_SUZUKI_PRINCIPAL_REFUTATION'and g['source_ids']==[sid]and g['principal_refutation_credit']==1 and g['ordinary_recovery_credit']==g['new_measurements']==g['new_question_credit']==g['new_Lean_credit']==0,'Individual final gate '+sid)
   for r in g['bindings']:bind(root,r)
  need(load(root,AUD+'/registration_review/review.json')['status']=='ACCEPTED_THREE_SUZUKI_REGISTRATION','Distinct concrete registration review')
 return dict(status='PASS_THREE_SUZUKI_PRINCIPAL_REFUTATIONS',source_ids=IDS,counts=dict(active=106,corrected_recoveries=85,refuted=5,handled=90,measured=53,unmeasured=32,mathematical_pending=15,editorial=1,archived=55,comparison_topics=19),controls=controls,old_verifier_functions_preserved=len(names(oldtree))-1,proposal_public_pins=len(publicpins))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--preflight',action='store_true');a=p.parse_args();print(json.dumps(verify(a.repo,not a.preflight)))
