"""Exact additive L044 principal registration; old gates remain unchanged."""
from pathlib import Path
import argparse,ast,copy,hashlib,json,sys
if sys.flags.optimize:raise RuntimeError('Optimized Python is not supported')
AUD='audit/science77/v1';IDS=['L044'];DIGEST='507bf6343f589b1fd87b722cfdbf54645cf745e6256f97346d4fb47289b66599'
KEYS={'finite','existence','primitive','primitive_strings','large_blocks','pairs','binary_coordinates','degree_sixteen','binary_omissions','singleton','paired_count','paired_connectedness','paired_ladder'}
def need(ok,s):
 if not ok:raise ValueError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(root,name):return json.loads((root/name).read_text())
def bind(root,row):
 p=root/row['path'];need(not Path(row['path']).is_absolute()and p.resolve().is_relative_to(root.resolve()),'Binding escapes repository');need(p.is_file()and sha(p)==row.get('stored_sha256',row['sha256']),'Public binding changed: '+row['path']);need(p.stat().st_size==row.get('stored_bytes',row.get('bytes',p.stat().st_size)),'Public binding size changed')
def unique(values,expected,label):need(len(values)==len(set(values))and set(values)==set(expected),label)
def semantics(c,old,a,s):
 unique(c['admitted_original_ids'],old['admitted_original_ids']+IDS,'Only L044 admitted');need(len(c['admitted_original_ids'])==c['admitted_principal_originals']==77,'77 recoveries')
 unique(c['accessible_pending_original_ids'],set(old['accessible_pending_original_ids'])-set(IDS),'Only L044 pending removed');need(len(c['accessible_pending_original_ids'])==c['accessible_pending_complete_recovery']==27,'27 pending')
 unique(c['handled_mathematical_original_ids'],old['handled_mathematical_original_ids']+IDS,'Only L044 handled');need(len(c['handled_mathematical_original_ids'])==c['handled_mathematical_originals']==78,'78 handled')
 for key in ['measurement_pending_original_ids','scientific_unmeasured_original_ids']:unique(c[key],old[key]+IDS,'Only L044 unmeasured added');need(len(c[key])==24,'24 unmeasured')
 for key in ['active_original_ids','archived_original_ids','measured_original_ids','added_measurements','current_topic_replacements','editorial_original_ids','refuted_principal_originals','refuted_principal_original_ids','principal_refutation_admissions','all_mathematical_originals_handled','all_original_proofs_recovered','all_conjectures_resolved','current_principal_disposition_registration']:need(c[key]==old[key],'Corpus/measurement/refutation changed: '+key)
 need(c['currently_measured_originals']==53 and c['originals']==106 and c['editorial_originals']==1,'Fixed corpus')
 need(a['source_ids']==IDS and a['principal_originals_added']==1 and a['whole_original_credit']==0,'Root gate alone supplies public credit')
 need(a['complete_principal_contract_recovered']and a['literal_principal_theorem_recovered']and not a['all_original_assertions_claimed'],'Principal-only recovery with auxiliary correction')
 need(a['compression_factor']is a['software_inclusive_factor']is None and a['new_question_credit']==a['new_Lean_declarations']==a['new_measurements']==0 and not a['whole_source_formalized']and not a['measured'],'No new factor/question/formal claim')
 need(set(a['component_acceptance'])=={'complete'}and set(a['component_acceptance']['complete'])=={'author','distinct','root_adoption'},'Complete distinct acceptance chain')
 need(set(a['complete_acquired_proofs'])==KEYS,'All thirteen immediate components')
 for chain in a['complete_acquired_proofs'].values():need(set(chain)=={'author','reviews'}and chain['reviews'],'Every component has a reviewed acquisition')
 need(s['original']=='L044'and len(s['routes'])==11 and len({r['source_claim']for r in s['routes']})==11,'All eleven exact source routes')
 need(s['routes'][-1]['source_claim']=='Theorem1.1, all n>=15 upper bound','Whole induction present')
 need(len(a['intermediate_corrections'])==1 and 'Proposition 3.3' in a['intermediate_corrections'][0]and 'false'in a['intermediate_corrections'][0]and 'narrower'in a['intermediate_corrections'][0],'Explicit auxiliary correction')
 need(a['immediate_manuscripts']==14 and a['physical_pages']==37 and a['acquired_packets']==349 and a['logical_files']==4285 and a['restored_mathematical_and_audit_files']==4273,'Whole documented closure')
 need(a['historical_documentary_exceptions']==243 and a['source_assets_hash_only']==12 and not a['private_runtime_fallback'],'Exact source/cache boundary')
 need(a['document_inventory_not_measurement']=='The immediate manuscripts are entry points to a larger complete proof closure. Neither their pages nor the two-page wrapper are a compression denominator.','Immediate pages not a measurement')
def verify(root,require_root=True):
 root=Path(root).resolve();history=load(root,AUD+'/history_routes.json')['routes']
 for row in history.values():bind(root,row)
 old=load(root,history['audit/corpus/latest.json']['path']);c=load(root,'audit/corpus/latest.json');a=load(root,'audit/recoveries/L044/v1/admission.json');s=load(root,'audit/recoveries/L044/v1/scope_routes.json');semantics(c,old,a,s)
 for key in ['active_catalogue','snapshot','current_science_registration']:bind(root,c[key])
 need(load(root,c['snapshot']['path'])=={k:v for k,v in c.items()if k!='snapshot'},'Exact current snapshot')
 cat=load(root,c['active_catalogue']['path']);oldcat=load(root,old['active_catalogue']['path']);need(len(cat['entries'])==len(oldcat['entries'])==106,'Fixed catalogue')
 for before,after in zip(oldcat['entries'],cat['entries']):
  if before['original_id']!='L044':need(before==after,'Another original changed')
  else:
   need(set(before)==set(after),'Original schema changed')
   for key in set(before)-{'current_principal_recovery','next_obligation'}:need(before[key]==after[key],'Original historical data changed')
   x=after['current_principal_recovery'];need(x['historical_admission_evidence']==before['current_principal_recovery']and x['principal_contract_admitted']and x['literal_principal_theorem_recovered']and not x['measured'],'L044 contract/history');need(x['auxiliary_corrections']==a['intermediate_corrections'],'Catalogue correction preserved')
 reg=load(root,c['current_science_registration']['path']);need(reg['source_ids']==IDS and reg['previous_registration']==old['current_science_registration']and reg['principal_originals_added']==1 and reg['measurement_originals_added']==reg['new_question_credit']==reg['new_Lean_declarations']==reg['comparison_topics_added']==0 and reg['compression_factor']is None and not reg['whole_source_formalized'],'One-original registration')
 need(len(reg['admissions'])==1 and reg['admissions'][0]['path']=='audit/recoveries/L044/v1/admission.json','Exact admission');bind(root,reg['admissions'][0])
 for row in a['component_acceptance']['complete'].values():bind(root,row)
 for chain in a['complete_acquired_proofs'].values():
  bind(root,chain['author'])
  for row in chain['reviews']:bind(root,row)
 for key in ['source_routes','source_map','scope_routes','portable_report','portable_checker','portable_replay','portable_transport']:bind(root,a[key])
 need(load(root,a['source_routes']['path'])['routes']==s['routes'],'Frozen routes unchanged')
 for item in a['new_native_manuscripts']:bind(root,item['tex']);bind(root,item['pdf'])
 t=load(root,a['portable_transport']['path']);need(sha(root/a['portable_transport']['path'])==DIGEST and t['logical_files']==4285 and len(t['packets'])==349,'Exact complete transport')
 public={r['public_path']:r for r in t['files']if 'public_path'in r};need(len(public)==3328 and len(t['files'])==4285 and sum('public_path'not in r for r in t['files'])==12 and not t['private_mathematical_proof_fallback'],'Exact payload/source counts')
 for path,row in public.items():bind(root,dict(row,path=path))
 replay=load(root,a['portable_report']['path']);need(replay['status']=='PASS_PUBLIC_L044_COMPLETE_CLOSURE'and replay['transport_sha256']==DIGEST and replay['logical_records']==4285 and replay['restored_files']==4273 and replay['distinct_payloads']==3328 and replay['acquired_packets']==349 and replay['acquired_exports']==2481 and replay['exact_metadata_pins_checked']==10953 and replay['documentary_metadata_pins_acquired']==243,'Complete public replay')
 need(replay['degree16_full_subset_pairs']==5413998 and replay['small_maxima_recorded_exhaustions_reused']and replay['native_pages']==2 and not replay['private_proof_fallback']and not replay['large_group_censuses_repeated']and replay['whole_original_credit']==0 and len(replay['malformed_controls'])==8,'Exact bounded finite/native replay')
 previous=load(root,history['papers/catalogue_corrected_unmeasured.json']['path']);native=load(root,'papers/catalogue_corrected_unmeasured.json');need(native['entries'][:-14]==previous['entries']and native['original_ids']==previous['original_ids']+IDS and native['existing_comparison_topic_count']==19 and native['new_measurements']==0,'Old manuscripts/measurements unchanged')
 need([e['physical_pages']for e in native['entries'][-14:]]==[2,3,3,2,2,4,1,2,3,2,2,5,2,4],'Fourteen complete immediate documents')
 for actual,expected in zip(native['entries'][-14:],a['new_native_manuscripts']):need(actual['id']==expected['id']and actual['tex']==expected['tex']['path']and actual['pdf']==expected['pdf']['path']and not actual['measured']and actual['compression_factor']is None,'Exact new native routes')
 paper=load(root,'papers/latest_catalogue.json');oldpaper=load(root,history['papers/latest_catalogue.json']['path']);need(set(paper)==set(oldpaper),'Paper routing schema')
 for k in set(oldpaper)-{'status','active_source_catalogue','corrected_unmeasured_scientific_catalogue'}:need(paper[k]==oldpaper[k],'Other paper routing changed')
 need(paper['active_source_catalogue']==c['active_catalogue'],'Current paper routing');bind(root,paper['corrected_unmeasured_scientific_catalogue'])
 oldtree=ast.parse((root/history['scripts/verify_snapshot.py']['path']).read_text());newtree=ast.parse((root/'scripts/verify_snapshot.py').read_text())
 def functions(t):return {n.name:ast.dump(n,include_attributes=False)for n in t.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'}
 oldf,newf=functions(oldtree),functions(newtree);need(all(newf.get(k)==v for k,v in oldf.items()),'Old verifier functions changed');added={'check_previous_science77','check_science77'};need(set(newf)-set(oldf)==added,'Exactly two new verifier functions')
 def remaining(t,exclude):return [ast.dump(n,include_attributes=False)for n in t.body if not(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name in exclude)]
 need(remaining(oldtree,{'main'})==remaining(newtree,{'main'}|added),'All other top-level verifier nodes preserved')
 controls=[];mutations=[('duplicate original',lambda c,a,s:c['admitted_original_ids'].append('L044')),('remove other pending',lambda c,a,s:c['accessible_pending_original_ids'].pop()),('invent factor',lambda c,a,s:a.update(compression_factor=2)),('auxiliary overclaim',lambda c,a,s:a.update(all_original_assertions_claimed=True)),('missing route',lambda c,a,s:s['routes'].pop()),('missing component',lambda c,a,s:a['complete_acquired_proofs'].pop('singleton')),('missing distinct review',lambda c,a,s:a['component_acceptance']['complete'].pop('distinct')),('lost correction',lambda c,a,s:a.update(intermediate_corrections=[])),('source omission expansion',lambda c,a,s:a.update(source_assets_hash_only=13)),('wrapper-only length',lambda c,a,s:a.update(document_inventory_not_measurement='2 pages')),('invent question',lambda c,a,s:a.update(new_question_credit=1))]
 for label,fn in mutations:
  cc,aa,ss=copy.deepcopy((c,a,s));fn(cc,aa,ss)
  try:semantics(cc,old,aa,ss)
  except (ValueError,KeyError):controls.append(label)
  else:raise ValueError('Invalid registration accepted: '+label)
 operational=load(root,AUD+'/operational_review.json');need(operational['status']=='ACCEPTED_L044_PUBLIC_TRANSPORT'and operational['logical_files_rehashed']==4273 and operational['distinct_payloads']==3328 and operational['whole_original_credit']==0,'Exact distinct operational review')
 for row in load(root,AUD+'/operational_review/mapping.json')['bindings'].values():bind(root,row)
 if require_root:
  gate=load(root,AUD+'/root_integration.json');need(gate['status']=='ROOT_ACCEPTED_SCIENCE77_PUBLICATION'and gate['source_ids']==IDS and gate['whole_original_credit']==1 and gate['new_question_credit']==gate['new_Lean_declarations']==gate['new_measurements']==0 and gate['compression_factor']is None,'Exact final root publication credit')
  for row in gate['bindings']:bind(root,row)
  need(load(root,AUD+'/operational_review.json')['status']=='ACCEPTED_L044_PUBLIC_TRANSPORT','Distinct operational review required')
  need(load(root,AUD+'/registration_review/review.json')['status']=='ACCEPTED_L044_REGISTRATION','Distinct registration review required')
 return dict(status='PASS_SCIENCE77_PUBLICATION',counts=dict(active=106,corrected_recoveries=77,refuted=1,handled=78,measured=53,unmeasured=24,mathematical_pending=27,editorial=1,archived=55,comparison_topics=19),source_ids=IDS,old_verifier_functions_preserved=len(oldf),public_payloads={'L044':3328},controls=controls)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--preflight',action='store_true');a=p.parse_args();print(json.dumps(verify(a.repo,require_root=not a.preflight)))
