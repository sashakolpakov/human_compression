"""Verify only the additive L019 principal registration and preserved history."""
import sys
if sys.flags.optimize:raise RuntimeError('Optimized Python is not supported')
from pathlib import Path
import argparse,ast,copy,gzip,hashlib,json
AUD='audit/science79/v1';REC='audit/recoveries/L019/v1'
TRANSPORT='501d8bdc9010dcd7e406601a860649c32d89f065ec189816a88b613f8953ec5a'
PROPOSAL='d2a070c8434edb059898646bcc56be81484b7821200e8850fec4c30254af85aa'
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
 for key,n in [('admitted_original_ids',79),('handled_mathematical_original_ids',80),('measurement_pending_original_ids',26),('scientific_unmeasured_original_ids',26)]:
  unique(c[key],old[key]+['L019'],'Only L019 added '+key);need(len(c[key])==n,'Current cardinality')
 unique(c['accessible_pending_original_ids'],set(old['accessible_pending_original_ids'])-{'L019'},'Only L019 removed')
 need((c['admitted_principal_originals'],c['handled_mathematical_originals'],c['accessible_pending_complete_recovery'])==(79,80,25),'Exact partition')
 mutable={'status','admitted_principal_originals','handled_mathematical_originals','accessible_pending_complete_recovery','previous_snapshot','active_catalogue','current_science_registration','admitted_original_ids','handled_mathematical_original_ids','measurement_pending_original_ids','scientific_unmeasured_original_ids','accessible_pending_original_ids','added_admissions','snapshot'}
 need(set(c)==set(old),'Corpus schema unchanged')
 for k in set(old)-mutable:need(c[k]==old[k],'Unrelated corpus field '+k)
 need(c['added_admissions'][:-1]==old['added_admissions']and c['added_admissions'][-1]['path']==REC+'/admission.json','One admission')
 need({'L042','L046','F009','F012'}<=set(c['accessible_pending_original_ids']),'Other pending originals unchanged')
 need(a['source_ids']==['L019']and a['principal_originals_added']==1 and a['whole_original_credit']==0,'Root gate alone grants credit')
 # The reviewed proposal fixes all scientific claims and scope. The registration
 # wrapper is allowed only its explicit status, manuscript-key and gate fields.
 extra={'source_ids','publication_gate','source_map','scope_routes','portable_checker','operational_review_gate','new_native_manuscripts'}
 need(set(a)==(set(proposal)-{'manuscripts'})|extra,'Admission schema')
 for k in set(proposal)-{'status','manuscripts'}:need(a[k]==proposal[k],'Scientific proposal changed '+k)
 need(a['status']=='ROOT_ACCEPTED_MATHEMATICS_PUBLICATION_REQUIRES_SCIENCE79_GATE','Admission status')
 need(a['new_native_manuscripts']==proposal['manuscripts'],'Exact three manuscripts')
 need(a['complete_principal_contract_recovered']and a['corrected_principal_recovery']and not a['all_original_assertions_claimed'],'Corrected principal scope')
 need(a['compression_factor']is a['software_inclusive_factor']is None and a['new_question_credit']==a['new_Lean_declarations']==a['new_measurements']==0 and not a['measured']and not a['whole_source_formalized'],'No unrelated credit')
 need(set(a['complete_acquired_proofs'])=={'pure_bijection','balanced_pairs'},'Both complete components')
 for chain in [a['component_acceptance']['complete']]+list(a['complete_acquired_proofs'].values()):need(set(chain)=={'author','distinct','root_adoption'},'Complete review chains')
 need(scope['original']=='L019'and scope['principal_contract']==a['principal_claims']and len(scope['principal_contract'])==3,'All three principal routes')
 need(scope['retained_auxiliary_corrections']==a['intermediate_corrections']and len(a['intermediate_corrections'])==4,'All four auxiliary corrections')
 need(scope['whole_original_status']=='ROOT_MATHEMATICS_ACCEPTED_PUBLICATION_GATE_PENDING'and scope['whole_original_credit']==0 and scope['frozen_source_routes_unchanged'],'Historical status explicit')
 need(a['counts']==dict(rooted_wings=[1,1,6,3,11,19],boundary_classes=[1,1,7,9,35,48],wing_representatives=41,boundary_representatives=101,labelled_degree6_survivors=720),'Exact finite theorem')
 need((a['logical_files'],a['restored_mathematical_and_audit_files'],a['acquired_packets'],a['source_assets_hash_only'],a['relative_locator_records'])==(6652,6607,439,45,42),'Exact closure')
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
  if x['original_id']!='L019':need(x==y,'Another original entry changed')
  else:
   need(set(x)==set(y),'L019 original schema')
   for k in set(x)-{'current_principal_recovery','next_obligation'}:need(x[k]==y[k],'Historical L019 property changed')
   q=y['current_principal_recovery'];need(q['historical_admission_evidence']==x['current_principal_recovery']and q['principal_contract_admitted']and q['complete_principal_contract_recovered']and q['corrected_principal_recovery']and not q['all_original_assertions_claimed']and not q['measured'],'Qualified recovery')
   need(q['source_qualifications']==a['intermediate_corrections']and q['scope_exclusions']==a['scope_exclusions']and q['counts']==a['counts'],'Catalogue scope preserved')
 need(cat['current_recovery_counts']==dict(active=106,admitted=79,refuted=1,handled=80,measured=53,measurement_pending=26,pending=25,editorial=1),'Catalogue partition')
 reg=load(root,c['current_science_registration']['path']);need(reg['source_ids']==['L019']and reg['previous_registration']==old['current_science_registration']and reg['principal_originals_added']==1 and reg['measurement_originals_added']==reg['new_question_credit']==reg['new_Lean_declarations']==reg['comparison_topics_added']==0 and reg['compression_factor']is None and not reg['whole_source_formalized'],'One scientific registration')
 need(len(reg['admissions'])==1 and reg['admissions'][0]['path']==REC+'/admission.json','Registration admission');bind(root,reg['admissions'][0])
 for chain in [a['component_acceptance']['complete']]+list(a['complete_acquired_proofs'].values()):
  for r in chain.values():bind(root,r)
 for k in ['source_map','scope_routes','portable_report','portable_checker','portable_replay','portable_transport','portable_adaptation']:bind(root,a[k])
 for m in a['new_native_manuscripts']:bind(root,m['tex']);bind(root,m['pdf'])
 t=load(root,a['portable_transport']['path']);need(sha(root/a['portable_transport']['path'])==TRANSPORT and len(t['files'])==6652 and len(t['packets'])==439 and t['whole_original_credit']==0,'Frozen complete transport')
 payloads={r['public_path']:r for r in t['files']if 'public_path'in r};need(len(payloads)==4660 and sum(r['transport'].endswith('HASH_ONLY')for r in t['files'])==45,'Exact payload and documentary boundary')
 for path,r in payloads.items():bind(root,dict(r,path=path))
 replay=load(root,a['portable_report']['path']);need(replay['status']=='PASS_PUBLIC_L019_COMPLETE_CLOSURE'and replay['transport_sha256']==TRANSPORT and replay['checker_sha256']==a['portable_checker']['sha256'],'Completed exact replay')
 need((replay['logical_records'],replay['restored_files'],replay['distinct_payloads'],replay['acquired_packets'],replay['acquired_exports'],replay['exact_metadata_pins_checked'])==(6652,6607,4660,439,3714,27632),'Complete replay scope')
 need(replay['wing_counts']=={str(i):n for i,n in enumerate([1,1,6,3,11,19],1)}and replay['boundary_counts']=={str(i):n for i,n in enumerate([1,1,7,9,35,48],1)},'Exact finite counts')
 need(replay['fresh_complete_censuses']==[dict(degree=n,wings=k)for n,k in zip(range(2,13,2),[1,1,6,3,11,19])]and replay['independent_labelled_degree6']==720 and replay['positive_wings']==41 and replay['positive_glued_markings']==101,'Complete finite replay')
 need(len(replay['malformed_controls'])==10 and len(replay['optimization_guards'])==2 and replay['malformed_literal_controls']==3 and not replay['private_proof_fallback'],'Controls and no private fallback')
 need([x['pages']for x in replay['native']]==[2,4,3]and all(x['text_identical']for x in replay['native']),'Native texts')
 prior=load(root,history['papers/catalogue_corrected_unmeasured.json']['path']);native=load(root,'papers/catalogue_corrected_unmeasured.json');need(native['entries'][:-3]==prior['entries']and native['original_ids']==prior['original_ids']+['L019']and native['acquired_dependencies']==prior['acquired_dependencies']and native['existing_comparison_topic_count']==19 and native['new_measurements']==0,'Previous native and measured catalogue unchanged')
 for x,y in zip(native['entries'][-3:],a['new_native_manuscripts']):need(x['id']==y['id']and x['tex']==y['tex']['path']and x['pdf']==y['pdf']['path']and x['physical_pages']==y['physical_pages']and not x['measured']and x['compression_factor']is None,'Exact native routes')
 paper=load(root,'papers/latest_catalogue.json');oldpaper=load(root,history['papers/latest_catalogue.json']['path']);need(set(paper)==set(oldpaper),'Paper schema')
 for k in set(oldpaper)-{'active_source_catalogue','corrected_unmeasured_scientific_catalogue'}:need(paper[k]==oldpaper[k],'Other paper route changed')
 need(paper['active_source_catalogue']==c['active_catalogue'],'Active source route');bind(root,paper['corrected_unmeasured_scientific_catalogue'])
 oldtree=ast.parse((root/history['scripts/verify_snapshot.py']['path']).read_text());newtree=ast.parse((root/'scripts/verify_snapshot.py').read_text());added={'check_previous_science79','check_science79'}
 def funcs(tree):return {n.name:ast.dump(n,include_attributes=False)for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'}
 oldf,newf=funcs(oldtree),funcs(newtree);need(set(newf)-set(oldf)==added and all(newf.get(k)==v for k,v in oldf.items()),'Exactly two additive functions; old functions unchanged')
 def other(tree,exc):return [ast.dump(n,include_attributes=False)for n in tree.body if not(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name in exc)]
 need(other(oldtree,{'main'})==other(newtree,{'main'}|added),'All other top-level AST nodes unchanged')
 controls=[]
 mutations=[('duplicate',lambda c,a,s:c['admitted_original_ids'].append('L019')),('omit other pending',lambda c,a,s:c['accessible_pending_original_ids'].remove('L042')),('factor',lambda c,a,s:a.update(compression_factor=2)),('unrestricted',lambda c,a,s:a.update(all_original_assertions_claimed=True)),('lose correction',lambda c,a,s:a['intermediate_corrections'].pop()),('lose route',lambda c,a,s:s['principal_contract'].pop()),('lose acquired component',lambda c,a,s:a['complete_acquired_proofs'].pop('balanced_pairs')),('lose review',lambda c,a,s:a['component_acceptance']['complete'].pop('distinct')),('question',lambda c,a,s:a.update(new_question_credit=1)),('wrong count',lambda c,a,s:a['counts']['boundary_classes'].__setitem__(5,49)),('extra documentary omission',lambda c,a,s:a.update(source_assets_hash_only=46)),('wrong convention',lambda c,a,s:a['principal_claims'][0].update(claim='Isomorphism without reversal')),('automatic credit',lambda c,a,s:a.update(whole_original_credit=1)),('wrong edition',lambda c,a,s:a['source_identity'].update(sha256='0'*64))]
 for label,fn in mutations:
  cc,aa,ss=copy.deepcopy((c,a,scope));fn(cc,aa,ss)
  try:semantics(cc,old,aa,ss,proposal)
  except (ValueError,KeyError):controls.append(label)
  else:raise ValueError('Invalid registration accepted '+label)
 op=load(root,AUD+'/operational_review.json');need(op['status']=='ACCEPTED_L019_PUBLIC_TRANSPORT'and op['whole_original_credit']==0,'Root operational acceptance')
 mapping=load(root,AUD+'/operational_review/mapping.json');need(mapping['manifest_sha256']==sha(root/mapping['manifest']['path']),'Exact review manifest')
 for r in mapping['bindings'].values():bind(root,r)
 omitted={(r['origin'],r['path'],r['bytes'],r['sha256'])for r in t['files']if r['transport'].endswith('HASH_ONLY')}
 for r in mapping['hash_only_bindings'].values():need((r['origin'],r['path'],r['bytes'],r['sha256'])in omitted,'Only exact inherited source omissions')
 need(mapping['manifest_sha256']=='41387ab7828281bb13d9878b76c9b45e94854126efea2aa6d1199908d649e295','Exact root operational review')
 if require_root:
  gate=load(root,AUD+'/root_integration.json');need(gate['status']=='ROOT_ACCEPTED_SCIENCE79_PUBLICATION'and gate['source_ids']==['L019']and gate['whole_original_credit']==1 and gate['new_question_credit']==gate['new_Lean_declarations']==gate['new_measurements']==0 and gate['compression_factor']is None,'Final root admission')
  for r in gate['bindings']:bind(root,r)
  need(load(root,AUD+'/registration_review/review.json')['status']=='ACCEPTED_L019_REGISTRATION','Distinct registration review')
 return dict(status='PASS_SCIENCE79_PUBLICATION',counts=dict(active=106,corrected_recoveries=79,refuted=1,handled=80,measured=53,unmeasured=26,mathematical_pending=25,editorial=1,archived=55,comparison_topics=19),source_ids=['L019'],old_verifier_functions_preserved=len(oldf),public_payloads={'L019':4660},controls=controls)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--preflight',action='store_true');a=p.parse_args();print(json.dumps(verify(a.repo,not a.preflight)))
