"""Register the complete corrected fixed-source L033 recovery without scientific replay."""
import sys
if sys.flags.optimize: raise RuntimeError('Ordinary Python required')
from pathlib import Path
import argparse, ast, copy, gzip, hashlib, json, re
AUD='audit/science89/v1'
BASELINE='5cbf9a6908d3a4cb20d1184297764ae8c6d596ab'
IDS=['L033']
OP_SHA='fab8cfc9f1bb2b7f7a153c7e3e25aa27cf1974ccff33218fd16ac7ca7fa5d640'
PROPOSAL_SHA='afb5148510bb7627ed7562a9112bf0c3e5427be3c23c9c6c4f7e42eb205b43e2'
HISTORY=['README.rst','audit/completion.rst','audit/corpus/latest.json','papers/latest_catalogue.json','papers/catalogue_corrected_unmeasured.json','papers/catalogue_principal_refutations.json','scripts/verify_snapshot.py','audit/protocol.tex','audit/protocol.pdf']
def need(v,m):
 if not v: raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(root,name):return json.loads((root/name).read_text())
def safe(root,name):
 n=Path(name);p=(root/n).resolve();need(not n.is_absolute() and '..'not in n.parts and p.is_relative_to(root),'Safe relative path');return p
def bind(root,r):
 name=r.get('public_path',r.get('path'));need(name is not None,'Public route required');p=safe(root,name)
 need(p.is_file()and p.stat().st_size==r.get('stored_bytes',r['bytes'])and sha(p)==r.get('stored_sha256',r['sha256']),'Exact public binding '+name)
 if 'decoded_sha256'in r:
  raw=p.read_bytes();raw=gzip.decompress(raw)if r.get('encoding')=='gzip'else raw
  need(len(raw)==r['decoded_bytes']and hashlib.sha256(raw).hexdigest()==r['decoded_sha256'],'Exact decoded identity '+name)
 return p
def admission_path():return 'audit/recoveries/L033/v1/admission.json'
def final_gate():return 'audit/recoveries/L033/v1/root_integration.json'
def nodes(t,omit):return[ast.dump(n,include_attributes=False)for n in ast.parse(t).body if not(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name in omit)]
def replace_once(t,a,b):need(t.count(a)==1,'Exact verifier anchor '+a);return t.replace(a,b)
def verifier_delta(old):
 functions="def check_previous_science89():\n    spec=importlib.util.spec_from_file_location('science89_history',ROOT/'scripts/check_science89_history.py')\n    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)\n    return module.verify(ROOT)\n\ndef check_science89():\n    spec=importlib.util.spec_from_file_location('science89',ROOT/'scripts/check_science89.py')\n    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)\n    return module.verify(ROOT)\n\n"
 new=replace_once(old,'def main():\n',functions+'def main():\n')
 new=replace_once(new,'    science88_history = check_previous_science88()',"    science89_history = check_previous_science89()\n    science88_history = science89_history['previous']")
 new=replace_once(new,'    science72 = check_science88()','    science72 = check_science89()')
 new=replace_once(new,"    print('PASS: exact predecessor history preserved; L100 complete corrected fixed-source recovery admitted without measurement.')","    print('PASS: exact predecessor history preserved; L033 complete corrected fixed-source recovery admitted without measurement.')")
 need(nodes(old,{'main'})==nodes(new,{'main','check_previous_science89','check_science89'}),'All old non-main ASTs unchanged')
 return new
def expected_admission(spec,proposal):
 return dict(status='ACCEPTED_MATHEMATICS_REGISTRATION_REQUIRES_ROOT_GATES',source_ids=IDS,disposition_kind='ordinary_recovery',accepted_proposal=spec['proposal'],accepted_proposal_contents=proposal,source_contract=spec['source_contract'],operational_review=spec['operational_review'],registration_baseline=BASELINE,publication_gate=final_gate(),shared_registration_gate=AUD+'/root_integration.json',ordinary_recovery_credit=1,principal_refutation_credit=0,handled_original_credit=1,new_measurements=0,new_question_credit=0,new_Lean_declarations=0,whole_source_formalized=False,all_source_assertions_reproved=False,compression_factor=None,software_inclusive_factor=None,complete_manuscripts=spec['manuscripts'],scope_note=spec['scope_note'])
def semantics(c,old,a,spec,p):
 mutable={'status','admitted_principal_originals','added_admissions','admitted_original_ids','accessible_pending_complete_recovery','accessible_pending_original_ids','previous_snapshot','active_catalogue','snapshot','measurement_pending_original_ids','scientific_unmeasured_original_ids','handled_mathematical_originals','handled_mathematical_original_ids','current_science_registration'}
 need(set(c)==set(old),'Unchanged corpus schema')
 for k in set(old)-mutable:need(c[k]==old[k],'Unrelated corpus field '+k)
 need(c['status']=='CURRENT_PROGRAMME_89_RECOVERED_9_REFUTED_7_PENDING_1_EDITORIAL','Current status')
 need(c['admitted_original_ids']==sorted(old['admitted_original_ids']+IDS)and c['admitted_principal_originals']==89,'One ordinary recovery')
 need(c['refuted_principal_originals']==9 and len(c['refuted_principal_original_ids'])==9,'Refutations unchanged')
 need(c['handled_mathematical_original_ids']==sorted(old['handled_mathematical_original_ids']+IDS)and c['handled_mathematical_originals']==98,'One new disposition')
 need(c['accessible_pending_original_ids']==[i for i in old['accessible_pending_original_ids']if i not in IDS]and c['accessible_pending_complete_recovery']==7,'Seven pending originals')
 for k in ['measurement_pending_original_ids','scientific_unmeasured_original_ids']:need(c[k]==sorted(old[k]+IDS)and len(c[k])==36,'Unmeasured recovery')
 need(len(c['measured_original_ids'])==53 and not c['all_mathematical_originals_handled']and not c['all_original_proofs_recovered']and not c['all_conjectures_resolved'],'No measurement or completion inflation')
 sets=[set(c[k])for k in ['admitted_original_ids','refuted_principal_original_ids','accessible_pending_original_ids','editorial_original_ids']]
 need(all(not x&y for i,x in enumerate(sets)for y in sets[i+1:])and set.union(*sets)==set(c['active_original_ids'])and sum(map(len,sets))==106,'Exact active partition')
 need(a==expected_admission(spec,p),'Exact L033 source admission')
def damaged_controls(c,old,a,spec,p):
 tests=[('measurement',lambda c,a:c['measured_original_ids'].pop()),('ordinary inflation',lambda c,a:c['admitted_original_ids'].append('L033')),('refutation change',lambda c,a:c['refuted_principal_original_ids'].pop()),('pending overlap',lambda c,a:c['accessible_pending_original_ids'].append('L033')),('lost pending',lambda c,a:c['accessible_pending_original_ids'].pop()),('false completion',lambda c,a:c.update(all_mathematical_originals_handled=True)),('false proof completion',lambda c,a:c.update(all_original_proofs_recovered=True)),('wrong kind',lambda c,a:a.update(disposition_kind='principal_statement_refuted')),('extra question',lambda c,a:a.update(new_question_credit=1)),('new factor',lambda c,a:a.update(compression_factor=1.1)),('wrong gate',lambda c,a:a.update(publication_gate='other')),('wrong baseline',lambda c,a:a.update(registration_baseline='0'*40)),('lost qualification',lambda c,a:a.update(scope_note='everything reproved')),('new formalization',lambda c,a:a.update(whole_source_formalized=True)),('lost manuscript',lambda c,a:a['complete_manuscripts'].clear()),('lost native table',lambda c,a:a['complete_manuscripts'][0]['tex_inputs'].clear()),('source mutation',lambda c,a:a['source_contract'].clear()),('false source assertion',lambda c,a:a.update(all_source_assertions_reproved=True))]
 passed=[]
 for label,change in tests:
  cc,aa=copy.deepcopy((c,a));change(cc,aa)
  try:semantics(cc,old,aa,spec,p)
  except (ValueError,KeyError):passed.append(label)
  else:raise ValueError('Damaged admission accepted: '+label)
 return passed
def verify(root,require_root=True):
 root=Path(root).resolve();params=load(root,AUD+'/registration_parameters.json');need(params['baseline']==BASELINE and params['source_ids']==IDS,'Exact transition')
 need(params['operational_manifest_sha256']==OP_SHA and params['operational_status']=='ACCEPTED_PUBLIC_L033_PORTABLE_CLOSURE','Frozen operational decision')
 history=load(root,AUD+'/history_routes.json');need(history['baseline_commit']==BASELINE and set(history['routes'])==set(HISTORY),'Nine historical pointers')
 for r in history['routes'].values():bind(root,r)
 old=load(root,history['routes']['audit/corpus/latest.json']['path']);c=load(root,'audit/corpus/latest.json')
 need([old[k]for k in ['admitted_principal_originals','refuted_principal_originals','handled_mathematical_originals','accessible_pending_complete_recovery']]==[88,9,97,8],'Exact predecessor counts')
 spec=params['source_spec'];package=params['package'];p=load(root,package['proposal']['path']);need(sha(bind(root,package['proposal']))==PROPOSAL_SHA,'Exact accepted scientific proposal')
 a=load(root,admission_path());semantics(c,old,a,spec,p)
 need(spec['source_contract']==load(root,p['scope_routes']['path']) and spec['edition']==p['source_edition'],'Exact complete source scope')
 need(p['scientific_author']['sha256']=='3e72fe3b8bcaad6c315a9cf9c32cd64dd3b5e101b9024889cebf99c738d9cbfc'and p['distinct_mathematical_review']['sha256']=='cfde0cdbf82f655eeda8cf9ccb6a036cf3f0293f02cb616a6c493f984863e25b','Exact mathematical chain')
 stage=load(root,AUD+'/payload_manifest.json')
 for r in stage['files']:bind(root,r)
 op=load(root,package['operational_review']['path']);bind(root,package['operational_review'])
 need(op['original_manifest_sha256']==params['operational_manifest_sha256']and op['original_status']==params['operational_status'],'Exact accepted operational gate')
 need(op['manifest']['decoded_sha256']==params['operational_manifest_sha256'],'Operational manifest identity')
 for r in op['bindings'].values():bind(root,r)
 transport=load(root,package['transport']);docs={(r['origin'],r['path'],r['bytes'],r['sha256'])for r in transport['files']if r['transport'].endswith('HASH_ONLY')}
 for r in transport['files']:
  if 'public_path'in r:bind(root,r)
 for r in op['hash_only_bindings'].values():need((r['origin'],r['path'],r['bytes'],r['sha256'])in docs,'Exact documentary omission')
 def walk(x):
  if isinstance(x,dict):
   if 'sha256'in x and ('public_path'in x or isinstance(x.get('path'),str)and x['path'].startswith(('audit/','papers/','corrections/','scripts/'))):bind(root,x)
   for v in x.values():walk(v)
  elif isinstance(x,list):
   for v in x:walk(v)
 walk(p)
 need(len(spec['manuscripts'])==13 and sum(m['physical_pages']for m in spec['manuscripts'])==50,'Thirteen complete manuscripts')
 for m in spec['manuscripts']:
  tex=bind(root,m['tex']);bind(root,m['pdf']);declared={Path(x['path']).name:x for x in m['tex_inputs']}
  inputs=re.findall(r'\\(?:input|include)\s*\{([^}]+)\}',tex.read_text())
  need({x if Path(x).suffix else x+'.tex'for x in inputs}==set(declared),'All literal native inputs '+m['id'])
  for name,r in declared.items():need(bind(root,r)==tex.parent/name,'Adjacent input '+name)
 before=load(root,old['active_catalogue']['path']);cat=load(root,c['active_catalogue']['path']);need(len(before['entries'])==len(cat['entries'])==106 and set(before)==set(cat),'Exact catalogue schema')
 mutable={'status','admitted_principal_originals','accessible_pending_complete_recovery','entries','review_revision','previous_catalogue','current_recovery_counts','measurement_pending_original_ids','handled_mathematical_originals','handled_mathematical_original_ids','new_principal_refutation_credit'}
 for k in set(before)-mutable:need(cat[k]==before[k],'Unrelated catalogue field '+k)
 for x,y in zip(before['entries'],cat['entries']):
  if x['original_id']!='L033':need(x==y,'Other original changed');continue
  need(set(x)==set(y),'Source schema preserved')
  for k in set(x)-{'edition','current_principal_recovery','next_obligation'}:need(x[k]==y[k],'Historical source evidence changed')
  d=y['current_principal_recovery'];need(d==params['catalogue_disposition']and d['historical_admission_evidence']==x['current_principal_recovery'],'Exact qualified source disposition')
  need(d['status']=='CORRECTED_PRINCIPAL_RECOVERY_ACCEPTED_MEASUREMENT_PENDING'and d['disposition_kind']=='ordinary_recovery'and d['original_fully_handled']is True and d['principal_contract_admitted']is True and d['complete_principal_contract_recovered']is True and d['all_original_assertions_claimed']is False and d['whole_source_formalized']is False and d['measured']is False and d['compression_factor']is None,'Corrected ordinary contract without false source assertions')
  need(d['source_contract']==spec['source_contract']and d['accepted_proposal']==spec['proposal']and y['edition']==spec['edition']and y['next_obligation']==spec['scope_note'],'Exact source qualifications')
 need(cat['current_recovery_counts']==dict(active=106,admitted=89,refuted=9,handled=98,measured=53,measurement_pending=36,pending=7,editorial=1),'Catalogue counts')
 need(cat['status']=='CURRENT_ACCESSIBLE106_89_RECOVERED_9_REFUTED_7_PENDING'and cat['new_principal_refutation_credit']==cat['new_proof_credit']==cat['new_question_credit']==0,'Catalogue credit boundary')
 for k in ['admitted_principal_originals','accessible_pending_complete_recovery','measurement_pending_original_ids','refuted_principal_originals','refuted_principal_original_ids','handled_mathematical_originals','handled_mathematical_original_ids']:need(cat[k]==c[k],'Catalogue/current join '+k)
 for k in ['active_catalogue','snapshot','current_science_registration','current_principal_disposition_registration']:bind(root,c[k])
 need(c['previous_snapshot']==history['routes']['audit/corpus/latest.json']and load(root,c['snapshot']['path'])=={k:v for k,v in c.items()if k!='snapshot'},'Exact current snapshot')
 reg=load(root,c['current_science_registration']['path']);need(c['current_science_registration']['path']==AUD+'/new_original_registration.json','New ordinary registration path')
 need(reg['source_ids']==IDS and reg['ordinary_recoveries_added']==reg['handled_originals_added']==1 and reg['principal_refutations_added']==reg['new_measurements']==reg['new_question_credit']==reg['new_Lean_credit']==0,'Separate registration credit')
 need(reg['previous_science_registration']==old['current_science_registration']and reg['previous_disposition_registration']==old['current_principal_disposition_registration']and reg['previous_corpus']==history['routes']['audit/corpus/latest.json'],'Prior registration routes')
 need(reg['publication_gate']==AUD+'/root_integration.json'and reg['individual_publication_gates']==[final_gate()]and reg['compression_factor']is None,'Exact publication gates')
 need([r['path']for r in reg['admissions']]==[admission_path()]and c['added_admissions']==old['added_admissions']+reg['admissions'],'Additive admission route')
 for r in reg['admissions']:bind(root,r)
 name='papers/catalogue_corrected_unmeasured.json';n=load(root,name);o=load(root,history['routes'][name]['path']);need(n['original_ids']==o['original_ids']+IDS and n['entries'][:len(o['entries'])]==o['entries'],'Old native entries unchanged')
 for k in set(o)-{'original_ids','entries','root_publication_gate'}:need(n[k]==o[k],'Other native field '+k)
 need(n['entries'][len(o['entries']):]==params['native_additions']and len(params['native_additions'])==13,'Exact native additions')
 for entry,m in zip(params['native_additions'],spec['manuscripts']):need(entry['id']==m['id']and entry['tex']==m['tex']['path']and entry['pdf']==m['pdf']['path']and entry['tex_inputs']==[r['path']for r in m['tex_inputs']]and entry['physical_pages']==m['physical_pages']and entry['source_ids']==IDS and entry['measured']is False and entry['compression_factor']is None,'Literal native route')
 need((root/'papers/catalogue_principal_refutations.json').read_bytes()==(root/history['routes']['papers/catalogue_principal_refutations.json']['path']).read_bytes(),'Refutation catalogue byte unchanged')
 paper=load(root,'papers/latest_catalogue.json');oldpaper=load(root,history['routes']['papers/latest_catalogue.json']['path'])
 for k in set(oldpaper)-{'active_source_catalogue','corrected_unmeasured_scientific_catalogue'}:need(paper[k]==oldpaper[k],'Other paper pointer '+k)
 need(paper['active_source_catalogue']==c['active_catalogue'],'Current source catalogue');bind(root,paper['corrected_unmeasured_scientific_catalogue'])
 oldtext=(root/history['routes']['scripts/verify_snapshot.py']['path']).read_text();need((root/'scripts/verify_snapshot.py').read_text()==verifier_delta(oldtext),'Exact main delta/all old functions')
 for name in ['README.rst','audit/completion.rst','audit/protocol.tex']:
  text=(root/history['routes'][name]['path']).read_text()
  for row in params['narrative_delta']:
   if row['path']!=name:continue
   need(text.count(row['before'])==row['occurrences'],'Exact documentary predecessor');text=text.replace(row['before'],row['after'])
  need((root/name).read_text()==text,'Only declared documentary changes')
 controls=damaged_controls(c,old,a,spec,p)
 tree=load(root,AUD+'/predecessor_tree.json');need(tree['commit']==BASELINE,'Exact old tree')
 for r in tree['files']:
  if r['path']=='provenance/publication_manifest.json':
   archived=dict(r,path=AUD+'/manifest_history/predecessor_publication_manifest.json');q=bind(root,archived);need(not q.is_symlink()and bool(q.stat().st_mode&0o111)==(r['mode']=='100755'),'Archived publication manifest');continue
  if r['path']in HISTORY:
   oldpin=history['routes'][r['path']];need((oldpin['bytes'],oldpin['sha256'])==(r['bytes'],r['sha256']),'Archived mutable pointer equals baseline');continue
  q=root/r['path']
  if r['mode']=='120000':need(q.is_symlink()and str(q.readlink())==r['link'],'Old symlink preserved')
  else:bind(root,r);need(bool(q.stat().st_mode&0o111)==(r['mode']=='100755'),'Old executable mode')
 if require_root:
  gate=load(root,AUD+'/root_integration.json');need(gate['status']=='ROOT_ACCEPTED_SCIENCE89_L033_RECOVERY'and gate['source_ids']==IDS and gate['ordinary_recovery_credit']==1 and gate['principal_refutation_credit']==0,'Final shared root gate')
  need(gate['new_measurements']==gate['new_question_credit']==gate['new_Lean_credit']==0,'No extra credit')
  for r in gate['bindings']:bind(root,r)
  g=load(root,final_gate());need(g['status']=='ROOT_ACCEPTED_SOURCE_DISPOSITION'and g['source_ids']==IDS and g['disposition_kind']=='ordinary_recovery'and g['ordinary_recovery_credit']==1 and g['principal_refutation_credit']==g['new_measurements']==g['new_question_credit']==g['new_Lean_credit']==0,'Individual root gate')
  for r in g['bindings']:bind(root,r)
  review=load(root,AUD+'/registration_review/review.json');need(review['status']=='ACCEPTED_SCIENCE89_REGISTRATION','Distinct concrete registration review')
 return dict(status='PASS_SCIENCE89_L033_RECOVERY',source_ids=IDS,counts=dict(active=106,corrected_recoveries=89,refuted=9,handled=98,measured=53,unmeasured=36,mathematical_pending=7,editorial=1,archived=55,comparison_topics=19),controls=controls,predecessor_paths=len(tree['files']),old_verifier_functions_preserved=sum(isinstance(n,ast.FunctionDef)and n.name!='main'for n in ast.parse(oldtext).body),no_mathematical_census_repeated=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--preflight',action='store_true');a=ap.parse_args();print(json.dumps(verify(a.repo,not a.preflight)))
