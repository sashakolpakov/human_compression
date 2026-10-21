"""A six-original, scope-preserving registration; no mathematical replay.

Exact accepted proposals remain unchanged. Separate admission overlays assign
two recovery and four principal-refutation dispositions, with no new measures.
"""
import sys
if sys.flags.optimize: raise RuntimeError('Ordinary Python required')
from pathlib import Path
import argparse, ast, copy, gzip, hashlib, json, re, subprocess
AUD='audit/science87/v1'
BASELINE='ade9feeb7f8feaffa8f773932d57a50e60cb64c2'
RECOVERED=['L027','L076']; REFUTED=['L036','L046','L063','L064']; IDS=sorted(RECOVERED+REFUTED)
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
def admission_path(sid):return f"audit/{'recoveries'if sid in RECOVERED else'principal-refutations'}/{sid}/v1/admission.json"
def final_gate(sid):return str(Path(admission_path(sid)).with_name('root_integration.json'))
def nodes(t,omit):return[ast.dump(n,include_attributes=False)for n in ast.parse(t).body if not(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name in omit)]
def replace_once(t,a,b):need(t.count(a)==1,'Exact verifier anchor '+a);return t.replace(a,b)
def verifier_delta(old):
 functions="def check_previous_science87():\n    spec=importlib.util.spec_from_file_location('science87_history',ROOT/'scripts/check_science87_history.py')\n    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)\n    return module.verify(ROOT)\n\ndef check_science87():\n    spec=importlib.util.spec_from_file_location('science87',ROOT/'scripts/check_science87.py')\n    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)\n    return module.verify(ROOT)\n\n"
 new=replace_once(old,'def main():\n',functions+'def main():\n')
 new=replace_once(new,'    suzuki_disposition_history = check_previous_suzuki_dispositions()',"    science87_history = check_previous_science87()\n    suzuki_disposition_history = science87_history['previous']")
 new=replace_once(new,'    science72 = check_suzuki_dispositions()','    science72 = check_science87()')
 new=replace_once(new,"    print('PASS: exact L029 disposition history preserved; L110, L114 and L115 add three separate principal refutations.')","    print('PASS: exact predecessor history preserved; L027/L076 recovered and four separate principal refutations admitted.')")
 need(nodes(old,{'main'})==nodes(new,{'main','check_previous_science87','check_science87'}),'All old non-main ASTs unchanged')
 return new
def semantics(c,old,admissions,specs,proposals):
 mutable={'status','admitted_principal_originals','added_admissions','admitted_original_ids','accessible_pending_complete_recovery','accessible_pending_original_ids','previous_snapshot','active_catalogue','snapshot','measurement_pending_original_ids','scientific_unmeasured_original_ids','refuted_principal_originals','refuted_principal_original_ids','handled_mathematical_originals','handled_mathematical_original_ids','principal_refutation_admissions','current_science_registration','current_principal_disposition_registration'}
 need(set(c)==set(old),'Unchanged corpus schema')
 need(c['status']=='CURRENT_PROGRAMME_87_RECOVERED_9_REFUTED_9_PENDING_1_EDITORIAL','Current status matches disposition counts')
 for k in set(old)-mutable:need(c[k]==old[k],'Unrelated corpus field '+k)
 need(c['admitted_original_ids']==sorted(old['admitted_original_ids']+RECOVERED)and c['admitted_principal_originals']==87,'Exactly two ordinary recoveries')
 need(c['refuted_principal_original_ids']==old['refuted_principal_original_ids']+REFUTED and c['refuted_principal_originals']==9,'Exactly four principal refutations')
 need(c['handled_mathematical_original_ids']==sorted(old['handled_mathematical_original_ids']+IDS)and c['handled_mathematical_originals']==96,'Six separate dispositions')
 need(c['accessible_pending_original_ids']==[i for i in old['accessible_pending_original_ids']if i not in IDS]and c['accessible_pending_complete_recovery']==9,'Exactly nine remaining originals')
 for k in ['measurement_pending_original_ids','scientific_unmeasured_original_ids']:need(c[k]==sorted(old[k]+RECOVERED)and len(c[k])==34,'Unmeasured recovery scope')
 need(len(c['measured_original_ids'])==53 and not c['all_mathematical_originals_handled']and not c['all_original_proofs_recovered']and not c['all_conjectures_resolved'],'No measurement or completion inflation')
 sets=[set(c[k])for k in ['admitted_original_ids','refuted_principal_original_ids','accessible_pending_original_ids','editorial_original_ids']]
 need(all(not a&b for i,a in enumerate(sets)for b in sets[i+1:])and set.union(*sets)==set(c['active_original_ids'])and sum(map(len,sets))==106,'Exact active partition')
 need(set(admissions)==set(specs)==set(IDS),'Exactly six source admissions')
 for sid,a in admissions.items():
  spec=specs[sid];ordinary=sid in RECOVERED
  expected=dict(status='ACCEPTED_MATHEMATICS_REGISTRATION_REQUIRES_ROOT_GATES',source_ids=[sid],disposition_kind='ordinary_recovery'if ordinary else'principal_statement_refuted',accepted_proposal=spec['proposal'],accepted_proposal_contents=proposals[spec['package_id']],source_contract=spec['source_contract'],operational_review=spec['operational_review'],registration_baseline=BASELINE,publication_gate=final_gate(sid),shared_registration_gate=AUD+'/root_integration.json',ordinary_recovery_credit=int(ordinary),principal_refutation_credit=int(not ordinary),handled_original_credit=1,new_measurements=0,new_question_credit=0,new_Lean_declarations=0,whole_source_formalized=False,all_source_assertions_reproved=False,compression_factor=None,software_inclusive_factor=None,all_other_valid_source_claims_recovered=False if not ordinary else None,complete_manuscripts=spec['manuscripts'],scope_note=spec['scope_note'])
  need(a==expected,'Exact independent source admission '+sid)
 need(admissions['L046']['accepted_proposal_contents']['exact_total_claimed']is False and admissions['L046']['accepted_proposal_contents']['all_L046_work_finished']is False,'L046 unpaid science preserved')
 need(admissions['L063']['accepted_proposal']==admissions['L064']['accepted_proposal']and admissions['L063']['accepted_proposal_contents']['mathematical_defects']==1,'One omission, two fixed source IDs')
def damaged_controls(c,old,admissions,specs,proposals):
 tests=[('measurement',lambda c,a:c['measured_original_ids'].pop()),('ordinary inflation',lambda c,a:c['admitted_original_ids'].append('L046')),('duplicate disposition',lambda c,a:c['refuted_principal_original_ids'].append('L036')),('pending overlap',lambda c,a:c['accessible_pending_original_ids'].append('L064')),('lost pending',lambda c,a:c['accessible_pending_original_ids'].pop()),('false completion',lambda c,a:c.update(all_mathematical_originals_handled=True)),('false proof completion',lambda c,a:c.update(all_original_proofs_recovered=True)),('lost source',lambda c,a:a.pop('L064')),('wrong kind',lambda c,a:a['L046'].update(disposition_kind='ordinary_recovery')),('extra question',lambda c,a:a['L076'].update(new_question_credit=1)),('new factor',lambda c,a:a['L027'].update(compression_factor=1.1)),('wrong gate',lambda c,a:a['L063'].update(publication_gate=final_gate('L064'))),('wrong baseline',lambda c,a:a['L036'].update(registration_baseline='0'*40)),('exact total inflation',lambda c,a:a['L046']['accepted_proposal_contents'].update(exact_total_claimed=True)),('lost remaining work',lambda c,a:a['L046'].update(all_other_valid_source_claims_recovered=True)),('split mathematical defect',lambda c,a:a['L064']['accepted_proposal_contents'].update(mathematical_defects=2)),('lost qualification',lambda c,a:a['L076'].update(scope_note='complete everything')),('new formalization',lambda c,a:a['L027'].update(whole_source_formalized=True)),('lost manuscript',lambda c,a:a['L076']['complete_manuscripts'].clear())]
 passed=[]
 for label,change in tests:
  cc,aa=copy.deepcopy((c,admissions));change(cc,aa)
  try:semantics(cc,old,aa,specs,proposals)
  except (ValueError,KeyError):passed.append(label)
  else:raise ValueError('Damaged admission accepted: '+label)
 return passed
def verify(root,require_root=True):
 root=Path(root).resolve();params=load(root,AUD+'/registration_parameters.json');need(params['baseline']==BASELINE and params['source_ids']==IDS,'Exact frozen transition')
 history=load(root,AUD+'/history_routes.json');need(history['baseline_commit']==BASELINE and set(history['routes'])==set(HISTORY),'Nine preserved pointers')
 for r in history['routes'].values():bind(root,r)
 old=load(root,history['routes']['audit/corpus/latest.json']['path']);c=load(root,'audit/corpus/latest.json')
 need([old[k]for k in ['admitted_principal_originals','refuted_principal_originals','handled_mathematical_originals','accessible_pending_complete_recovery']]==[85,5,90,15],'Actual predecessor')
 bundle=load(root,AUD+'/accepted_bundle.json');specs=params['source_specs'];proposals={}
 for p in params['packages']:
  bind(root,p['proposal']);proposals[p['id']]=load(root,p['proposal']['path'])
 admissions={sid:load(root,admission_path(sid))for sid in IDS};semantics(c,old,admissions,specs,proposals)
 stage=load(root,AUD+'/payload_manifest.json')
 for r in stage['files']:bind(root,r)
 for p in params['packages']:
  op=load(root,p['operational_review']['path']);need(op['original_manifest_sha256']==p['operational_manifest_sha256']and op['original_status']==p['operational_status'],'Exact accepted operational gate')
  for r in op['bindings'].values():bind(root,r)
  need(op['manifest']['decoded_sha256']==p['operational_manifest_sha256'],'Operational manifest identity')
  if p.get('transport'):
   t=load(root,p['transport']);docs={(r['origin'],r['path'],r['bytes'],r['sha256'])for r in t['files']if r['transport'].endswith('HASH_ONLY')}
   for r in t['files']:
    if 'public_path'in r:bind(root,r)
   for r in op['hash_only_bindings'].values():need((r['origin'],r['path'],r['bytes'],r['sha256'])in docs,'Declared documentary exclusion only')
  else:need(not op['hash_only_bindings'],'No administrative source omission')
  # Recursively bind all actual public references, while documentary logical
  # source paths and historical absolute names remain declared provenance.
  def walk(x):
   if isinstance(x,dict):
    if 'sha256'in x and ('public_path'in x or isinstance(x.get('path'),str)and x['path'].startswith(('audit/','papers/','corrections/','scripts/'))):bind(root,x)
    for v in x.values():walk(v)
   elif isinstance(x,list):
    for v in x:walk(v)
  walk(proposals[p['id']])
 for sid,spec in specs.items():
  for m in spec['manuscripts']:
   tex=bind(root,m['tex']);bind(root,m['pdf']);declared={Path(x['path']).name:x for x in m['tex_inputs']}
   inputs=re.findall(r'\\(?:input|include)\s*\{([^}]+)\}',tex.read_text())
   need({x if Path(x).suffix else x+'.tex'for x in inputs}==set(declared),'All literal native inputs '+m['id'])
   for name,r in declared.items():need(bind(root,r)==tex.parent/name,'Adjacent native input '+name)
 before=load(root,old['active_catalogue']['path']);cat=load(root,c['active_catalogue']['path']);need(len(before['entries'])==len(cat['entries'])==106 and set(before)==set(cat),'Exact catalogue schema')
 mutable={'status','admitted_principal_originals','accessible_pending_complete_recovery','entries','review_revision','previous_catalogue','current_recovery_counts','measurement_pending_original_ids','refuted_principal_originals','refuted_principal_original_ids','handled_mathematical_originals','handled_mathematical_original_ids','new_principal_refutation_credit'}
 for k in set(before)-mutable:need(cat[k]==before[k],'Unrelated catalogue field '+k)
 for x,y in zip(before['entries'],cat['entries']):
  sid=x['original_id']
  if sid not in IDS:need(x==y,'Other original changed '+sid);continue
  need(set(x)==set(y),'Source schema preserved')
  for k in set(x)-{'edition','current_principal_recovery','next_obligation'}:need(x[k]==y[k],'Historical source evidence changed')
  need(y['current_principal_recovery']==params['catalogue_dispositions'][sid]and y['current_principal_recovery']['historical_admission_evidence']==x['current_principal_recovery'],'Exact qualified source disposition')
  need(y['edition']==specs[sid]['edition']and y['next_obligation']==specs[sid]['scope_note'],'Exact source edition and remaining scope')
  need(y['current_principal_recovery']['original_fully_handled']==(sid in RECOVERED),'Refutation dispositions do not recover all remaining source work')
 need(cat['current_recovery_counts']==dict(active=106,admitted=87,refuted=9,handled=96,measured=53,measurement_pending=34,pending=9,editorial=1),'Exact catalogue counts')
 need(cat['status']=='CURRENT_ACCESSIBLE106_87_RECOVERED_9_REFUTED_9_PENDING'and cat['new_principal_refutation_credit']==4 and cat['new_proof_credit']==cat['new_question_credit']==0,'Exact catalogue status and credit boundary')
 for k in ['admitted_principal_originals','accessible_pending_complete_recovery','measurement_pending_original_ids','refuted_principal_originals','refuted_principal_original_ids','handled_mathematical_originals','handled_mathematical_original_ids']:need(cat[k]==c[k],'Catalogue/current join '+k)
 for k in ['active_catalogue','snapshot','current_science_registration','current_principal_disposition_registration']:bind(root,c[k])
 need(c['previous_snapshot']==history['routes']['audit/corpus/latest.json']and load(root,c['snapshot']['path'])=={k:v for k,v in c.items()if k!='snapshot'},'Exact current snapshot')
 regs=[load(root,c[k]['path'])for k in ['current_science_registration','current_principal_disposition_registration']]
 need(c['current_science_registration']['path']==AUD+'/new_original_registration.json'and c['current_principal_disposition_registration']['path']==AUD+'/principal_refutation_registration.json','Exact separate registration paths')
 for reg,ids,ordinary in zip(regs,[RECOVERED,REFUTED],[True,False]):
  need(reg['source_ids']==ids and reg['ordinary_recoveries_added']==(2 if ordinary else 0)and reg['principal_refutations_added']==(0 if ordinary else 4)and reg['new_measurements']==reg['new_question_credit']==reg['new_Lean_credit']==0,'Separate registration counts')
  need(reg['previous_science_registration']==old['current_science_registration']and reg['previous_disposition_registration']==old['current_principal_disposition_registration'],'Both predecessor registrations retained')
  need(reg['status']=='REVIEWED_DISPOSITIONS_REQUIRING_ROOT_GATES'and reg['previous_corpus']==history['routes']['audit/corpus/latest.json']and reg['publication_gate']==AUD+'/root_integration.json'and reg['individual_publication_gates']==[final_gate(s)for s in ids]and reg['handled_originals_added']==len(ids)and reg['compression_factor']is None,'Exact registration gate and prior corpus scope')
  need([r['path']for r in reg['admissions']]==[admission_path(s)for s in ids],'Exact admissions')
  for r in reg['admissions']:bind(root,r)
 need(c['added_admissions']==old['added_admissions']+regs[0]['admissions']and c['principal_refutation_admissions']==old['principal_refutation_admissions']+[c['current_principal_disposition_registration']],'Additive admission routes')
 for name,ids in [('papers/catalogue_corrected_unmeasured.json',RECOVERED),('papers/catalogue_principal_refutations.json',REFUTED)]:
  n=load(root,name);o=load(root,history['routes'][name]['path']);need(n['original_ids']==o['original_ids']+ids and n['entries'][:len(o['entries'])]==o['entries'],'Existing native entries unchanged')
  for k in set(o)-{'original_ids','entries','root_publication_gate'}:need(n[k]==o[k],'Other native field '+k)
  need(n['entries'][len(o['entries']):]==params['native_additions'][name],'Exact native additions')
 paper=load(root,'papers/latest_catalogue.json');oldpaper=load(root,history['routes']['papers/latest_catalogue.json']['path'])
 for k in set(oldpaper)-{'active_source_catalogue','corrected_unmeasured_scientific_catalogue','principal_refutation_catalogue'}:need(paper[k]==oldpaper[k],'Other paper pointer '+k)
 need(paper['active_source_catalogue']==c['active_catalogue'],'Current source catalogue')
 for k in ['corrected_unmeasured_scientific_catalogue','principal_refutation_catalogue']:bind(root,paper[k])
 oldtext=(root/history['routes']['scripts/verify_snapshot.py']['path']).read_text();need((root/'scripts/verify_snapshot.py').read_text()==verifier_delta(oldtext),'Exact main delta and all prior ASTs')
 for name in ['README.rst','audit/completion.rst','audit/protocol.tex']:
  text=(root/history['routes'][name]['path']).read_text()
  for row in params['narrative_delta']:
   if row['path']!=name:continue
   need(text.count(row['before'])==row['occurrences'],'Exact documentary predecessor');text=text.replace(row['before'],row['after'])
  need((root/name).read_text()==text,'Only stated documentary changes')
 controls=damaged_controls(c,old,admissions,specs,proposals)
 # A full predecessor tree audit includes symlink identities and file modes.
 tree=load(root,AUD+'/predecessor_tree.json');need(tree['commit']==BASELINE,'Exact old tree')
 for r in tree['files']:
  if r['path']in HISTORY:
   oldpin=history['routes'][r['path']];need((oldpin['bytes'],oldpin['sha256'])==(r['bytes'],r['sha256']),'Archived mutable pointer equals baseline tree');continue
  p=root/r['path']
  if r['mode']=='120000':need(p.is_symlink()and str(p.readlink())==r['link'],'Old symlink preserved')
  else:
   bind(root,r);need(bool(p.stat().st_mode&0o111)==(r['mode']=='100755'),'Old executable mode preserved')
 # L046's actual old no-credit and pending assertions remain literal bytes.
 layer=proposals['L046'];remaining=load(root,layer['remaining_claims']);need(remaining==params['L046_remaining_claims'],'Every unpaid L046 claim retained')
 if require_root:
  gate=load(root,AUD+'/root_integration.json');need(gate['status']=='ROOT_ACCEPTED_SCIENCE87_SIX_DISPOSITIONS'and gate['source_ids']==IDS and gate['ordinary_recovery_credit']==2 and gate['principal_refutation_credit']==4,'Final shared root gate')
  need(gate['new_measurements']==gate['new_question_credit']==gate['new_Lean_credit']==0,'No extra credit')
  for r in gate['bindings']:bind(root,r)
  for sid in IDS:
   g=load(root,final_gate(sid));need(g['status']=='ROOT_ACCEPTED_SOURCE_DISPOSITION'and g['source_ids']==[sid]and g['disposition_kind']==admissions[sid]['disposition_kind'],'Individual source root gate')
   need(g['ordinary_recovery_credit']==int(sid in RECOVERED)and g['principal_refutation_credit']==int(sid in REFUTED)and g['new_measurements']==g['new_question_credit']==g['new_Lean_credit']==0,'Exact individual gate credits')
   for r in g['bindings']:bind(root,r)
  review=load(root,AUD+'/registration_review/review.json');need(review['status']=='ACCEPTED_SCIENCE87_REGISTRATION','Distinct concrete registration review')
 return dict(status='PASS_SCIENCE87_SIX_DISPOSITIONS',source_ids=IDS,counts=dict(active=106,corrected_recoveries=87,refuted=9,handled=96,measured=53,unmeasured=34,mathematical_pending=9,editorial=1,archived=55,comparison_topics=19),controls=controls,predecessor_paths=len(tree['files']),old_verifier_functions_preserved=sum(isinstance(n,ast.FunctionDef)and n.name!='main'for n in ast.parse(oldtext).body),no_mathematical_census_repeated=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--preflight',action='store_true');a=p.parse_args();print(json.dumps(verify(a.repo,not a.preflight)))
