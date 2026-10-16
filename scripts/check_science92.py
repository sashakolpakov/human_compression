"""Register L054 through exact segmented evidence and acquired predecessor bindings."""
import sys
if sys.flags.optimize: raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse, ast, copy, gzip, hashlib, json, re
AUD='audit/science92/v1'
BASELINE='0c52b67b2e064849fa22c09af55aa0de37e4142d'
IDS=['L054']
OP_SHA='1898e76e5fac427a4436d5a578bd10b574037804d862297201dc0cf74604a754'
PROPOSAL_SHA='b2a59b5f3240d2701207bef8be139efd70c3729153a3ec9a942caa056d1fa1aa'
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
def admission_path():return 'audit/recoveries/L054/v1/admission.json'
def final_gate():return 'audit/recoveries/L054/v1/root_integration.json'
def nodes(t,omit):return[ast.dump(n,include_attributes=False)for n in ast.parse(t).body if not(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name in omit)]
def replace_once(t,a,b):need(t.count(a)==1,'Exact verifier anchor '+a);return t.replace(a,b)
def verifier_delta(old):
 n=next(x for x in ast.parse(old).body if isinstance(x,ast.FunctionDef)and x.name=='main');lines=old.splitlines(True)
 added="""def check_science92():
    spec=importlib.util.spec_from_file_location('science92',ROOT/'scripts/check_science92.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.verify(ROOT)

def main():
    current = check_science92()
    print(json.dumps(current, sort_keys=True))
    print('PASS: exact accepted predecessor bytes preserved; L054 complete corrected source recovery registered without measurement.')
    print('Scope: current transition and exact prior evidence bindings checked; historical mathematical replays are acquired, not rerun.')
"""
 new=''.join(lines[:n.lineno-1])+added+''.join(lines[n.end_lineno:])
 need(nodes(old,{'main'})==nodes(new,{'main','check_science92'}),'All old non-main ASTs unchanged')
 return new
def expected_admission(spec,proposal):
 return dict(status='ACCEPTED_MATHEMATICS_REGISTRATION_REQUIRES_ROOT_GATES',source_ids=IDS,disposition_kind='ordinary_recovery',accepted_proposal=spec['proposal'],accepted_proposal_contents=proposal,source_contract=spec['source_contract'],operational_review=spec['operational_review'],registration_baseline=BASELINE,publication_gate=final_gate(),shared_registration_gate=AUD+'/root_integration.json',ordinary_recovery_credit=1,principal_refutation_credit=0,handled_original_credit=1,new_measurements=0,new_question_credit=0,new_Lean_declarations=0,whole_source_formalized=False,all_source_assertions_reproved=False,compression_factor=None,software_inclusive_factor=None,complete_manuscripts=spec['manuscripts'],scope_note=spec['scope_note'])

def semantics(c,old,a,spec,p):
 mutable={'status','admitted_principal_originals','added_admissions','admitted_original_ids','accessible_pending_complete_recovery','accessible_pending_original_ids','previous_snapshot','active_catalogue','snapshot','measurement_pending_original_ids','scientific_unmeasured_original_ids','handled_mathematical_originals','handled_mathematical_original_ids','current_science_registration','current_scope','completion_obligation_original_ids','completion_obligation_originals','handled_count_meaning','fully_treated_original_ids','fully_treated_originals'}
 need(set(c)==set(old),'Exact corpus schema, no new completion semantics')
 for k in set(old)-mutable:need(c[k]==old[k],'Unrelated corpus field '+k)
 need(c['status']=='CURRENT_PROGRAMME_92_RECOVERED_9_PRINCIPAL_REFUTATIONS_4_PENDING_1_EDITORIAL','Current status')
 need(c['admitted_original_ids']==sorted(old['admitted_original_ids']+IDS) and c['admitted_principal_originals']==92,'One ordinary recovery')
 need(c['handled_mathematical_original_ids']==sorted(old['handled_mathematical_original_ids']+IDS) and c['handled_mathematical_originals']==101,'One new principal disposition')
 need(c['accessible_pending_original_ids']==[i for i in old['accessible_pending_original_ids']if i not in IDS] and c['accessible_pending_complete_recovery']==4,'Four pending principal dispositions')
 for k in ['measurement_pending_original_ids','scientific_unmeasured_original_ids']:need(c[k]==sorted(old[k]+IDS) and len(c[k])==39,'Thirty-nine unmeasured recoveries')
 need(c['measured_original_ids']==old['measured_original_ids'] and len(c['measured_original_ids'])==53 and c['currently_measured_originals']==53,'All53 measured IDs unchanged')
 need(not c['all_mathematical_originals_handled'] and not c['all_original_proofs_recovered'] and not c['all_conjectures_resolved'],'No completion inflation')
 need(c['source_complete_refutation_original_ids']==old['source_complete_refutation_original_ids']==['F003','L029','L036'] and c['source_complete_refutation_originals']==3,'Preserve three completed refutations')
 need(c['surviving_claim_obligation_original_ids']==old['surviving_claim_obligation_original_ids'] and c['surviving_claim_obligation_originals']==6,'Six surviving source obligations unchanged')
 remaining=sorted(set(c['accessible_pending_original_ids'])|set(c['surviving_claim_obligation_original_ids']))
 need(c['completion_obligation_original_ids']==remaining and len(remaining)==c['completion_obligation_originals']==10,'Ten originals retain completion obligations')
 need(c['fully_treated_original_ids']==sorted(old['fully_treated_original_ids']+IDS)==sorted(c['admitted_original_ids']+c['source_complete_refutation_original_ids']) and c['fully_treated_originals']==95,'Ninety-five complete treatments')
 need(c['handled_count_meaning']=='Principal dispositions only: 92 corrected recoveries and nine principal refutations. F003, L029 and L036 have complete surviving-source dispositions; six other refutations retain surviving-claim obligations.','Explicit legacy count meaning')
 need(c['current_scope']=='Complete reviewed source dispositions for all 105 mathematical originals, including surviving claims after a refutation, then stop.','Exact stopping condition')
 sets=[set(c[k])for k in ['admitted_original_ids','refuted_principal_original_ids','accessible_pending_original_ids','editorial_original_ids']]
 need(all(not x&y for i,x in enumerate(sets)for y in sets[i+1:]) and set.union(*sets)==set(c['active_original_ids']) and sum(map(len,sets))==106,'Exact active partition')
 need(a==expected_admission(spec,p),'Exact L054 source admission')
def damaged_controls(c,old,a,spec,p):
 tests=[('measurement',lambda c,a:c['measured_original_ids'].pop()),('ordinary inflation',lambda c,a:c['admitted_original_ids'].append('L054')),('refutation change',lambda c,a:c['refuted_principal_original_ids'].pop()),('pending overlap',lambda c,a:c['accessible_pending_original_ids'].append('L054')),('lost pending',lambda c,a:c['accessible_pending_original_ids'].pop()),('false completion',lambda c,a:c.update(all_mathematical_originals_handled=True)),('false proof completion',lambda c,a:c.update(all_original_proofs_recovered=True)),('wrong kind',lambda c,a:a.update(disposition_kind='principal_statement_refuted')),('extra question',lambda c,a:a.update(new_question_credit=1)),('new factor',lambda c,a:a.update(compression_factor=1.1)),('wrong gate',lambda c,a:a.update(publication_gate='other')),('wrong baseline',lambda c,a:a.update(registration_baseline='0'*40)),('lost qualification',lambda c,a:a.update(scope_note='everything reproved')),('new formalization',lambda c,a:a.update(whole_source_formalized=True)),('lost manuscript',lambda c,a:a['complete_manuscripts'].clear()),('damaged native PDF',lambda c,a:a['complete_manuscripts'][0]['pdf'].update(sha256='0'*64)),('source mutation',lambda c,a:a['source_contract'].clear()),('false source assertion',lambda c,a:a.update(all_source_assertions_reproved=True))]
 tests += [('same-size measured substitution',lambda c,a:c['measured_original_ids'].__setitem__(0,'UNREVIEWED')),('lost surviving claim',lambda c,a:c['surviving_claim_obligation_original_ids'].pop()),('false surviving completion',lambda c,a:c.update(surviving_claim_obligation_originals=0)),('lost completion obligation',lambda c,a:c['completion_obligation_original_ids'].pop()),('false remaining count',lambda c,a:c.update(completion_obligation_originals=5)),('wrong stopping condition',lambda c,a:c.update(current_scope='stop after principal refutations'))]
 tests += [('lost completed refutation',lambda c,a:c['source_complete_refutation_original_ids'].pop()),('inflated complete count',lambda c,a:c.update(fully_treated_originals=96)),('lost complete source',lambda c,a:c['fully_treated_original_ids'].pop())]
 passed=[]
 for label,change in tests:
  cc,aa=copy.deepcopy((c,a));change(cc,aa)
  try:semantics(cc,old,aa,spec,p)
  except (ValueError,KeyError):passed.append(label)
  else:raise ValueError('Damaged admission accepted: '+label)
 return passed
def verify(root,require_root=True):
 root=Path(root).resolve();params=load(root,AUD+'/registration_parameters.json');need(params['baseline']==BASELINE and params['source_ids']==IDS,'Exact transition')
 need(params['operational_manifest_sha256']==OP_SHA and params['operational_status']=='ACCEPTED_L054_PORTABLE_PUBLICATION_V1','Frozen operational decision')
 history=load(root,AUD+'/history_routes.json');need(history['baseline_commit']==BASELINE and set(history['routes'])==set(HISTORY),'Nine historical pointers')
 for r in history['routes'].values():bind(root,r)
 old=load(root,history['routes']['audit/corpus/latest.json']['path']);c=load(root,'audit/corpus/latest.json')
 need([old[k]for k in ['admitted_principal_originals','refuted_principal_originals','handled_mathematical_originals','accessible_pending_complete_recovery']]==[91,9,100,5],'Exact predecessor counts')
 spec=params['source_spec'];package=params['package'];p=load(root,package['proposal']['path']);need(sha(bind(root,package['proposal']))==PROPOSAL_SHA,'Exact accepted scientific proposal')
 a=load(root,admission_path());semantics(c,old,a,spec,p)
 need(spec['source_contract']==load(root,p['scope_routes']['path']) and spec['edition']==p['source_edition'],'Exact complete source scope')
 need(p['scientific_author']['sha256']=='9e11a0c98a2a25f06a13b8a1017e72ad31733904fdd5d9cb85dcdc00d2ad77ae'and p['distinct_mathematical_review']['sha256']=='01de4f62d06c9e111f7dcb4dcf91dbd570834e30272448d7968cdb2a6337e371','Exact mathematical chain')
 stage=load(root,AUD+'/payload_manifest.json')
 for r in stage['files']:bind(root,r)
 op=load(root,package['operational_review']['path']);bind(root,package['operational_review'])
 need(op['original_manifest_sha256']==OP_SHA and op['original_status']==params['operational_status'],'Exact accepted operational gate')
 for r in op['direct_bindings']:bind(root,r)
 om=load(root,op['manifest']['path']);need(sha(bind(root,op['manifest']))==OP_SHA and om['status']==params['operational_status'],'Actual operational manifest')
 transport=load(root,package['transport']);need(transport['format']=='L054_SEGMENTED_EXACT_CONTENT_V1','Explicit segmented transport')
 declared=load(root,op['dependencies']['path'])
 origins=[r['original_path']for r in op['direct_bindings']if r['path']==op['manifest']['path']]
 need(len(origins)==1,'Unique original operational manifest')
 original_manifest=origins[0];prefix=str(Path(original_manifest).parent)
 declared=declared+[dict(x,path=prefix+'/'+x['path'])for x in om['exports']]+[dict(path=original_manifest,bytes=op['manifest']['bytes'],sha256=OP_SHA)]
 mappings={r['original_path']:r for r in op['direct_bindings']};need(len(mappings)==len(op['direct_bindings'])==len(declared),'Exact unique operational closure')
 need(set(mappings)=={r['path']for r in declared},'No omitted operational binding')
 for r in declared:need((r['bytes'],r['sha256'])==(mappings[r['path']]['bytes'],mappings[r['path']]['sha256']),'Exact original operational identity')
 review=load(root,op['review']['path'])
 need(review['fresh_validation']['report']['sha256']==op['root_portable_report']['sha256'] and review['mathematical_authority']['sha256']==p['distinct_mathematical_review']['sha256'] and review['stage_manifest']['sha256']==p['portable_stage_manifest']['sha256'] and review['transport']['sha256']==p['portable_transport']['sha256'],'Whole operational decision joins actual mathematical authority, stage and report; registration separately reviews proposal')
 need(sha(root/package['transport'])=='b76bd24a9f69edaed849c964992dbb5dc7fc88ecb319d15f2891f79570039328','Exact reviewed transport')
 need(transport['root_acceptance']['sha256']==p['distinct_mathematical_review']['sha256'],'Root mathematical acceptance')
 for r in transport['packs']+transport['existing_public_files']:bind(root,r)
 need(op['segmented_bindings']==[],'Operational package requires complete direct public bindings')
 report=load(root,op['root_portable_report']['path']);bind(root,op['root_portable_report'])
 need(report['status']=='PASS_PUBLIC_L054_ARTICLE_MAIN_RESULTS_COMPLETE_CLOSURE' and report['transport']['sha256']==p['portable_transport']['sha256'] and report['stage_manifest']['sha256']==p['portable_stage_manifest']['sha256'],'Distinct exact portable run')
 need([report[k]for k in ['logical_files','unique_content_objects','verified_payload_objects','premise_objects','complete_prior_manuscripts','complete_proof_pages','selected_files','native_pages','source_clauses','complete_groups','structural_rows']]==[77176,48820,47660,1160,41,107,20,7,21,134,15988],'Exact accepted complete operational extent')
 need(report['new_censuses']==report['new_group_calls']==report['whole_original_registration_credit']==0 and report['compression_measurement']is None,'No new scientific or measurement credit')
 need(report['corrected_A11_labels']==1 and not report['all_current_companion_tables_recovered'] and not report['companion_socle_bound_established'],'Explicit article/companion boundary')
 need(report['synthesis_damages']==15 and len(report['admission_controls']['metadata_and_boundary_rejections'])==12 and len(report['admission_controls']['real_cli_rejections'])==2,'Actual controls acquired')
 def walk(x):
  if isinstance(x,dict):
   if 'sha256'in x and ('public_path'in x or isinstance(x.get('path'),str)and x['path'].startswith(('audit/','papers/','corrections/','scripts/'))):bind(root,x)
   for v in x.values():walk(v)
  elif isinstance(x,list):
   for v in x:walk(v)
 walk(p)
 need(len(spec['manuscripts'])==42 and sum(m['physical_pages']for m in spec['manuscripts'])==107 and p['complete_proof_pages']==107 and p['principal_already_in_volume'],'Forty-two complete manuscripts,107pages')
 native=load(root,p['native_input_inventory']['path']);readable=load(root,'papers/recoveries/L054/v1/complete_manuscripts.json')
 need(len(native['manuscripts'])==len(readable['manuscripts'])==41,'All41 previous native inputs')
 for m in spec['manuscripts']:
  bind(root,m['tex']);bind(root,m['pdf'])
  for r in m['tex_inputs']:bind(root,r)
 first=spec['manuscripts'][0];need(first['tex']['path']=='papers/recoveries/L054/v1/principal.tex' and first['tex_inputs']==[dict(path='papers/recoveries/L054/v1/roster.tex',bytes=(root/'papers/recoveries/L054/v1/roster.tex').stat().st_size,sha256=sha(root/'papers/recoveries/L054/v1/roster.tex'))],'Exact principal native inputs')
 for m,ni,rr in zip(spec['manuscripts'][1:],native['manuscripts'],readable['manuscripts']):
  need(ni['tex']=={k:rr['tex'][k]for k in ['path','bytes','sha256']} and rr['adjacent_inputs']==ni['adjacent_inputs'],'Exact accepted component native inputs')
  for kind in ['tex','pdf']:need(m[kind]==dict(path=rr[kind]['public_path'],bytes=rr[kind]['bytes'],sha256=rr[kind]['sha256']),'Exact complete native route')
  expected=[dict(path=r['public_path'],bytes=r['bytes'],sha256=r['sha256'])for r in ni['adjacent_inputs']]
  need(m['tex_inputs']==expected,'All recursive adjacent inputs')
 before=load(root,old['active_catalogue']['path']);cat=load(root,c['active_catalogue']['path']);need(len(before['entries'])==len(cat['entries'])==106 and set(before)==set(cat),'Exact catalogue schema')
 mutable={'status','admitted_principal_originals','accessible_pending_complete_recovery','entries','review_revision','previous_catalogue','current_recovery_counts','measurement_pending_original_ids','handled_mathematical_originals','handled_mathematical_original_ids','new_principal_refutation_credit','fully_treated_originals','fully_treated_original_ids'}
 for k in set(before)-mutable:need(cat[k]==before[k],'Unrelated catalogue field '+k)
 for x,y in zip(before['entries'],cat['entries']):
  if x['original_id']!='L054':need(x==y,'Other original changed');continue
  need(set(x)==set(y),'Source schema preserved')
  for k in set(x)-{'authors','title','edition','current_principal_recovery','next_obligation'}:need(x[k]==y[k],'Historical source evidence changed')
  need(y['authors']==['Thomas Connor','Dimitri Leemans'] and y['title']==p['title'],'Exact source title and first-page author order')
  d=y['current_principal_recovery'];need(d==params['catalogue_disposition']and d['historical_admission_evidence']==x['current_principal_recovery'],'Exact qualified source disposition')
  need(d['status']=='CORRECTED_PRINCIPAL_RECOVERY_ACCEPTED_MEASUREMENT_PENDING'and d['disposition_kind']=='ordinary_recovery'and d['original_fully_handled']is True and d['principal_contract_admitted']is True and d['complete_principal_contract_recovered']is True and d['all_original_assertions_claimed']is False and d['whole_source_formalized']is False and d['measured']is False and d['compression_factor']is None,'Corrected ordinary contract without false source assertions')
  need(d['source_contract']==spec['source_contract']and d['accepted_proposal']==spec['proposal']and y['edition']==spec['edition']and y['next_obligation']==spec['scope_note'],'Exact source qualifications')
 need(cat['current_recovery_counts']==dict(active=106,admitted=92,refuted=9,handled=101,measured=53,measurement_pending=39,pending=4,editorial=1,surviving_claim_obligations=6,completion_obligations=10,fully_treated=95,completed_refutation_sources=3),'Catalogue counts')
 need(cat['status']=='CURRENT_ACCESSIBLE106_92_RECOVERED_9_PRINCIPAL_REFUTATIONS_4_PENDING'and cat['new_principal_refutation_credit']==cat['new_proof_credit']==cat['new_question_credit']==0,'Catalogue credit boundary')
 for k in ['admitted_principal_originals','accessible_pending_complete_recovery','measurement_pending_original_ids','refuted_principal_originals','refuted_principal_original_ids','handled_mathematical_originals','handled_mathematical_original_ids','fully_treated_original_ids','fully_treated_originals','source_complete_refutation_original_ids','source_complete_refutation_originals']:need(cat[k]==c[k],'Catalogue/current join '+k)
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
 need(n['entries'][len(o['entries']):]==params['native_additions']and len(params['native_additions'])==42,'Exact native additions')
 for entry,m in zip(params['native_additions'],spec['manuscripts']):need(entry['id']==m['id']and entry['tex']==m['tex']['path']and entry['pdf']==m['pdf']['path']and entry['tex_inputs']==[r['path']for r in m['tex_inputs']]and entry['physical_pages']==m['physical_pages']and entry['source_ids']==IDS and entry['measured']is False and entry['compression_factor']is None,'Literal native route')
 need((root/'papers/catalogue_principal_refutations.json').read_bytes()==(root/history['routes']['papers/catalogue_principal_refutations.json']['path']).read_bytes(),'Refutation catalogue byte unchanged')
 paper=load(root,'papers/latest_catalogue.json');oldpaper=load(root,history['routes']['papers/latest_catalogue.json']['path'])
 for k in set(oldpaper)-{'status','active_source_catalogue','corrected_unmeasured_scientific_catalogue'}:need(paper[k]==oldpaper[k],'Other paper pointer '+k)
 need(paper['status']=='CURRENT_MANUSCRIPTS_53_MEASURED_PLUS_THIRTY_NINE_CORRECTED_UNMEASURED','Updated current manuscript status')
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
  gate=load(root,AUD+'/root_integration.json');need(gate['status']=='ROOT_ACCEPTED_SCIENCE92_L054_RECOVERY'and gate['source_ids']==IDS and gate['ordinary_recovery_credit']==1 and gate['principal_refutation_credit']==0,'Final shared root gate')
  need(gate['new_measurements']==gate['new_question_credit']==gate['new_Lean_credit']==0,'No extra credit')
  for r in gate['bindings']:bind(root,r)
  g=load(root,final_gate());need(g['status']=='ROOT_ACCEPTED_SOURCE_DISPOSITION'and g['source_ids']==IDS and g['disposition_kind']=='ordinary_recovery'and g['ordinary_recovery_credit']==1 and g['principal_refutation_credit']==g['new_measurements']==g['new_question_credit']==g['new_Lean_credit']==0,'Individual root gate')
  for r in g['bindings']:bind(root,r)
  review=load(root,AUD+'/registration_review/review.json');need(review['status']=='ACCEPTED_SCIENCE92_REGISTRATION','Distinct concrete registration review')
 return dict(status='PASS_SCIENCE92_L054_RECOVERY',source_ids=IDS,counts=dict(active=106,corrected_recoveries=92,refuted=9,handled=101,measured=53,unmeasured=39,mathematical_pending=4,editorial=1,archived=55,comparison_topics=19,surviving_claim_obligations=6,completion_obligations=10,fully_treated=95,completed_refutation_sources=3),controls=controls,predecessor_paths=len(tree['files']),old_verifier_functions_preserved=sum(isinstance(n,ast.FunctionDef)and n.name!='main'for n in ast.parse(oldtext).body),no_mathematical_census_repeated=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--preflight',action='store_true');a=ap.parse_args();print(json.dumps(verify(a.repo,not a.preflight)))
