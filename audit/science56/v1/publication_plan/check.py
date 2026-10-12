"""Publication route/semantic guard only; does not re-adjudicate accepted science."""
from pathlib import Path,PurePosixPath
import argparse,ast,copy,hashlib,json,re
HERE=Path(__file__).resolve().parent
AUDIT='audit/science56/v1'
SCIENCE='audit/topic-g/extensions/local-primitivity/v1'
def need(v,m):
 if not v:raise ValueError('SCIENCE56: '+m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(root,r):
 q=PurePosixPath(r['path']);need(not q.is_absolute()and '..'not in q.parts and str(q)==r['path'],'safe path')
 p=root/q;need(p.stat().st_size==r['bytes']and sha(p)==r['sha256'],'binding '+r['path'])
def semantic(c,old,cat,oldcat,papers,oldpapers,sc,oldsc,ad,roles):
 need(tuple(c[k]for k in ['originals','admitted_principal_originals','currently_measured_originals','accessible_pending_complete_recovery','editorial_originals','archived_unavailable_originals'])==(106,56,53,49,1,55),'complete106 partition')
 need(len(c['admitted_original_ids'])==len(set(c['admitted_original_ids']))==56 and set(c['admitted_original_ids'])==set(old['admitted_original_ids'])|{'L102'},'only L102 added once')
 need(len(c['accessible_pending_original_ids'])==49 and set(c['accessible_pending_original_ids'])==set(old['accessible_pending_original_ids'])-{'L102'},'exact pending subtraction')
 need(c['measurement_pending_original_ids']==c['scientific_unmeasured_original_ids']==['L024','L102','N014'],'three unmeasured')
 for k in ['measured_original_ids','added_measurements','current_topic_replacements','historical_admitted_ids','active_original_ids','archived_original_ids','editorial_original_ids','editorial_factor','source_retrieval_in_scope','all_original_proofs_recovered','all_conjectures_resolved']:
  need(c[k]==old[k],'unchanged scope/measurement '+k)
 ss=[set(c['admitted_original_ids']),set(c['accessible_pending_original_ids']),set(c['editorial_original_ids'])]
 need(set.union(*ss)==set(c['active_original_ids'])and sum(map(len,ss))==106,'disjoint fixed partition')
 need(c['added_admissions'][:-1]==old['added_admissions']and len(c['added_admissions'])==len(old['added_admissions'])+1,'one admission appended')
 before={r['original_id']:r for r in oldcat['entries']};after={r['original_id']:r for r in cat['entries']}
 need(len(after)==len(cat['entries'])==106 and before.keys()==after.keys(),'same106 original objects')
 need(all(before[k]==after[k]for k in before if k!='L102'),'other105 original records exact')
 need(cat['admitted_principal_originals']==56 and cat['accessible_pending_complete_recovery']==49,'catalogue totals')
 row=after['L102'];q=row['current_principal_recovery']
 need(q['status']=='ADMITTED_CORRECTED_PRINCIPAL_RECOVERY_MEASUREMENT_PENDING'and q['principal_contract_admitted']and not q['measured']and q['compression_factor']is None,'L102 admission state')
 need(q['historical_admission_evidence']==before['L102']['current_principal_recovery'],'old L102 evidence retained')
 for k in ['source_access','authors','title','year','edition','historical_proof_status','active','original_count']:
  need(row[k]==before['L102'][k],'fixed L102 source identity '+k)
 need(ad['source_ids']==['L102']and ad['source_id']=='L102'and ad['principal_originals_added']==1,'one exact original')
 need(not ad['measured']and ad['measurement_status']=='pending'and ad['compression_factor']is None and ad['software_inclusive_factor']is None,'no invented scalar')
 need(ad['new_question_credit']==ad['new_Lean_declarations']==0 and not ad['whole_source_formalized']and not ad['theorem_sets_equivalent'],'scope limits')
 need(ad['physical_pages']==[14,8]and len(ad['whole_common'])==len(ad['whole_applications'])==1 and ad['source_pages']==22 and ad['source_routes']==35,'full common/application/source')
 need(not ad['comparison_topic_created']and not ad['current_G_measurement_changed'],'no changed G factor/topic')
 need(ad['distinct_root_review_manifest']==ad['root_scientific_acceptance'],'distinct science root acceptance role')
 for k in oldpapers:
  if k not in ['status','active_source_catalogue','corrected_unmeasured_scientific_catalogue']:need(papers[k]==oldpapers[k],'old paper pointer '+k)
 need(sc['entries'][:len(oldsc['entries'])]==oldsc['entries']and sc['acquired_dependencies']==oldsc['acquired_dependencies'],'old corrected scientific papers exact')
 new=sc['entries'][len(oldsc['entries']):]
 need(len(new)==2 and [r['id']for r in new]==['L102_U','L102_A']and [r['physical_pages']for r in new]==[14,8],'full two new documents')
 need(all(r['compiler']=='xelatex'and r['source_ids']==['L102']and not r['measured']and r['compression_factor']is None and not r['comparison_topic_created']for r in new),'native compiler and no measurement')
 need(new[1]['externaldocument_dependency']=='local_actions.aux'and new[1]['build_order']==['local_actions','linear_spaces'],'actual cross-paper build order')
 need(sc['original_ids']==oldsc['original_ids']+['L102']and sc['existing_comparison_topic_count']==19 and sc['new_measurements']==0,'no measurement/topic count')
 need(len(roles['whole_files'])==15 and roles['required_current_program_count']==2 and roles['optional_current_program_count']==3 and roles['current_operational_count']==1,'complete role closure')
 by={r['path']:r for r in roles['whole_files']}
 need(len(by)==15 and all(r['complete_file']for r in by.values()),'whole raw files')
 for path,prefix in [('small_g2_premise.g','REQUIRED_FINITE'),('feit_bound.cpp','REQUIRED_EXACT'),('small_g2_premise.txt','REQUIRED_BOUND'),('feit_full_result.json','REQUIRED_BOUND'),('check.py','OPERATIONAL'),('check_wbs_small.g','OPTIONAL'),('check_feit_arithmetic.cpp','OPTIONAL'),('validate_arithmetic.py','OPTIONAL')]:
  need(by[path]['role'].startswith(prefix),'role '+path)
 need(roles['source_software']['cost']is None and roles['source_software']['unknown_not_zero']and roles['software_inclusive_factor']is None and roles['new_Lean']==0,'source software/formal scope')
 return True
def controls(args):
 result=[]
 def bad(label,mut):
  a=copy.deepcopy(args);mut(a)
  try:semantic(*a)
  except(ValueError,KeyError,IndexError):result.append(label)
  else:raise ValueError('accepted corruption '+label)
 bad('reviewed counted as measured',lambda a:a[0].__setitem__('currently_measured_originals',56))
 bad('duplicate source admission',lambda a:a[0]['admitted_original_ids'].append('L102'))
 bad('other pending source dropped',lambda a:a[0]['accessible_pending_original_ids'].pop())
 bad('measured admission appended',lambda a:a[0]['added_measurements'].append({}))
 bad('prior admission lost',lambda a:a[0]['added_admissions'].pop(0))
 bad('old original record changed',lambda a:next(r for r in a[2]['entries']if r['original_id']=='L096').__setitem__('next_obligation','changed'))
 bad('source PDF identity changed',lambda a:next(r for r in a[2]['entries']if r['original_id']=='L102')['source_access'].__setitem__('accessible',False))
 bad('L102 assigned factor',lambda a:a[8].__setitem__('compression_factor',2))
 bad('source software priced zero',lambda a:a[9]['source_software'].__setitem__('cost',0))
 bad('whole common shortened',lambda a:a[8].__setitem__('physical_pages',[13,8]))
 bad('common acquisition removed',lambda a:a[8]['whole_common'].clear())
 bad('new topic invented',lambda a:a[8].__setitem__('comparison_topic_created',True))
 bad('old G measurement replaced',lambda a:a[8].__setitem__('current_G_measurement_changed',True))
 bad('literal theorem-set equivalence claimed',lambda a:a[8].__setitem__('theorem_sets_equivalent',True))
 bad('new question credited',lambda a:a[8].__setitem__('new_question_credit',1))
 bad('whole Lean claimed',lambda a:a[8].__setitem__('whole_source_formalized',True))
 bad('old paper removed',lambda a:a[4]['entries'].pop())
 bad('old unmeasured document changed',lambda a:a[6]['entries'][0].__setitem__('physical_pages',7))
 bad('wrong native compiler',lambda a:a[6]['entries'][-1].__setitem__('compiler','pdflatex'))
 bad('cross-reference prerequisite omitted',lambda a:a[6]['entries'][-1].__setitem__('externaldocument_dependency',None))
 bad('required output demoted',lambda a:next(r for r in a[9]['whole_files']if r['path']=='feit_full_result.json').__setitem__('role','OPTIONAL'))
 bad('required program demoted',lambda a:next(r for r in a[9]['whole_files']if r['path']=='feit_bound.cpp').__setitem__('role','OPTIONAL'))
 bad('operational driver omitted',lambda a:a[9]['whole_files'].__setitem__(slice(None),[r for r in a[9]['whole_files']if r['path']!='check.py']))
 bad('retrieval reopened',lambda a:a[0].__setitem__('source_retrieval_in_scope',True))
 return result
def verify(repo,require_root=False):
 repo=Path(repo);base=load(HERE/'baseline.json');plan=load(HERE/'copy_plan.json')
 if(HERE/'manifest.json').exists():
  for r in load(HERE/'manifest.json')['exports']:bind(HERE,r)
 for r in load(HERE/'wrapper_routes.json')['files']:bind(repo,r)
 for r in base['protected_files']:bind(repo,r)
 need(len(plan['files'])==47 and len(plan['packets'])==2,'complete two scientific packets')
 need(len({r['public_path']for r in plan['files']})==47,'unique public destinations')
 for r in plan['files']:
  bind(repo,dict(path=r['public_path'],bytes=r['bytes'],sha256=r['sha256']))
  need(not r['public_path'].endswith('.md')and not any(x in PurePosixPath(r['public_path']).parts for x in ['sources','private_source','rasters','fonts']),'no primary text/font assets')
 for p in plan['packets']:
  bind(repo,p['manifest']);m=load(repo/p['manifest']['path']);rr={r['logical_path']:r for r in plan['files']if r['packet']==p['id']}
  need(len(m['exports'])==p['exports']and set(rr)=={'manifest.json'}|{r['path']for r in m['exports']},'exact complete manifest closure')
  for e in m['exports']:need(all(rr[e['path']][k]==e[k]for k in ['bytes','sha256']),'logical frozen binding')
 h=load(repo/(AUDIT+'/history_routes.json'))['routes'];need(h==base['history'],'exact old history routes')
 for r in h.values():bind(repo,r)
 old=load(repo/h['audit/corpus/latest.json']['path']);c=load(repo/'audit/corpus/latest.json')
 for k in ['snapshot','active_catalogue','current_science_registration']:bind(repo,c[k])
 need(load(repo/c['snapshot']['path'])=={k:v for k,v in c.items()if k!='snapshot'},'exact current snapshot')
 cat=load(repo/c['active_catalogue']['path']);bind(repo,base['old_catalogue']);oldcat=load(repo/base['old_catalogue']['path'])
 papers=load(repo/'papers/latest_catalogue.json');oldpapers=load(repo/h['papers/latest_catalogue.json']['path'])
 bind(repo,papers['corrected_unmeasured_scientific_catalogue']);bind(repo,papers['active_source_catalogue']);need(papers['active_source_catalogue']==c['active_catalogue'],'current catalogue agreement')
 sc=load(repo/papers['corrected_unmeasured_scientific_catalogue']['path']);oldsc=load(repo/h['papers/catalogue_corrected_unmeasured.json']['path'])
 reg=load(repo/c['current_science_registration']['path']);need(reg['source_ids']==['L102']and reg['principal_originals_added']==1 and reg['measurement_originals_added']==0 and reg['previous_registration']==old['current_science_registration'],'L102-only scientific registration')
 need(c['added_admissions'][-1]==c['current_science_registration'],'exact appended route')
 need(len(reg['admissions'])==1,'one admission');bind(repo,reg['admissions'][0]);ad=load(repo/reg['admissions'][0]['path'])
 for k in ['author_manifest','distinct_root_review_manifest','root_scientific_acceptance','source_map','scope','retained_inputs','required_program_inventory']:bind(repo,ad[k])
 row=next(r for r in cat['entries']if r['original_id']=='L102');need(row['current_principal_recovery']['latest_admission_references']==reg['admissions'],'actual L102 admission route')
 roles=load(repo/(AUDIT+'/whole_file_roles.json'))
 for r in roles['whole_files']:bind(repo,dict(path=r['public_path'],bytes=r['bytes'],sha256=r['sha256']))
 original=load(repo/(SCIENCE+'/author/program_inventory.json'))
 need([{k:v for k,v in r.items()if k!='public_path'}for r in roles['whole_files']]==original['whole_files'],'exact inherited role/file identities')
 args=[c,old,cat,oldcat,papers,oldpapers,sc,oldsc,ad,roles];semantic(*args);tests=controls(args)
 from pypdf import PdfReader
 for row in sc['entries'][-2:]:
  text=(repo/row['tex']).read_text();actual=re.search(r'\\title\{([^{}]+)\}',text).group(1)
  need(actual==row['title']and len(PdfReader(repo/row['pdf']).pages)==row['physical_pages'],'literal title/whole PDF')
  need(all((repo/q).is_file()for q in row['tex_inputs']),'whole TeX closure')
  need(row['admission']==reg['admissions'][0],'catalogue scientific admission')
 actual={n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest()for n in ast.parse((repo/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'}
 need(len(base['old_nonmain_ASTs'])==137 and all(actual.get(k)==v for k,v in base['old_nonmain_ASTs'].items()),'all137 previous functions unchanged')
 readme=(repo/'README.rst').read_text();protocol=(repo/'audit/protocol.tex').read_text()
 for s in ['56 accessible originals','53 are measured and three','49 await mathematical recovery','None of these three recoveries has a compression factor','G\'s measured boundary unchanged']:
  need(s in readme,'reader scope '+s)
 need('106=56'in protocol and 'Of the 56 corrected recoveries, 53'in protocol and 'N014, L024 and L102'in protocol,'protocol exact partition')
 links=0
 for name in ['README.rst','audit/completion.rst','papers/topic-g/extensions/local-primitivity/v1/PUBLICATION.rst']:
  for target in re.findall(r'<([^<>\n]+)>`_', (repo/name).read_text()):
   if re.match(r'\w+://',target):continue
   need((repo/Path(name).parent/target).exists(),'local link '+name+' -> '+target);links+=1
 status='PUBLICATION_NOT_ADJUDICATED'
 if require_root:
  gate=load(repo/(AUDIT+'/root_integration.json'));need(gate['status']=='ROOT_ACCEPTED_SCIENCE56_PUBLICATION'and gate['source_ids']==['L102']and gate['measurements_added']==gate['new_question_credit']==0,'root-only integration gate')
  required={'README.rst','audit/completion.rst','audit/protocol.tex','audit/protocol.pdf','audit/corpus/latest.json','papers/latest_catalogue.json','papers/catalogue_corrected_unmeasured.json',AUDIT+'/publication_plan/manifest.json',AUDIT+'/new_original_registration.json',SCIENCE+'/admission.json','scripts/verify_snapshot.py','scripts/check_science56.py','scripts/check_science56_history.py'}
  need(required<={r['path']for r in gate['bindings']},'root gate full current bindings')
  for r in gate['bindings']:bind(repo,r)
  status='ROOT_ACCEPTED'
 return dict(status='PASS_SCIENCE56_ROUTES',publication_status=status,counts=dict(active=106,corrected_recoveries=56,measured=53,unmeasured=3,mathematical_pending=49,editorial=1,archived=55,comparison_topics=19),exact_payload_routes=47,exact_packets=2,other_originals_preserved=105,old_paper_records_preserved=len(oldpapers['entries']),unchanged_verifier_functions=137,unchanged_overview='v19',new_factors=0,native_pages=[14,8],whole_file_roles=15,checked_links=links,controls=tests,scientific_programs_rerun=False,extraction_or_Lean_rerun=False)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path);p.add_argument('--require-root',action='store_true');a=p.parse_args();r=verify(a.repo,a.require_root)
 if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r))
