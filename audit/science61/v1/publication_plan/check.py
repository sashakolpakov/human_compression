"""L011 publication integration guard; not a second scientific proof review."""
from pathlib import Path, PurePosixPath
import argparse, ast, copy, hashlib, json, re
HERE=Path(__file__).resolve().parent
AUDIT='audit/science61/v1'
SCIENCE='audit/recoveries/L011/v1'
NATIVE='papers/recoveries/L011/v1'
def need(v,m):
 if not v: raise ValueError('SCIENCE61: '+m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(root,row):
 p=PurePosixPath(row['path']);need(not p.is_absolute() and '..' not in p.parts,'safe path')
 raw=(root/p).read_bytes();need(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'file '+row['path'])

def semantic(c,old,cat,oldcat,papers,oldpapers,sc,oldsc,ad,roles,review):
 need(tuple(c[k] for k in ['originals','admitted_principal_originals','currently_measured_originals','accessible_pending_complete_recovery','editorial_originals','archived_unavailable_originals'])==(106,61,53,44,1,55),'partition')
 need(len(c['admitted_original_ids'])==len(set(c['admitted_original_ids']))==61 and set(c['admitted_original_ids'])==set(old['admitted_original_ids'])|{'L011'},'L011 added once')
 need(len(c['accessible_pending_original_ids'])==44 and set(c['accessible_pending_original_ids'])==set(old['accessible_pending_original_ids'])-{'L011'},'pending subtraction')
 need(c['measurement_pending_original_ids']==c['scientific_unmeasured_original_ids']==['F008','F011','L011','L013','L024','L039','L102','N014'],'eight unmeasured')
 for k in ['measured_original_ids','added_measurements','current_topic_replacements','historical_admitted_ids','active_original_ids','archived_original_ids','editorial_original_ids','editorial_factor','source_retrieval_in_scope','all_original_proofs_recovered','all_conjectures_resolved']:
  need(c[k]==old[k],'unchanged '+k)
 parts=[set(c['admitted_original_ids']),set(c['accessible_pending_original_ids']),set(c['editorial_original_ids'])]
 need(sum(map(len,parts))==106 and set.union(*parts)==set(c['active_original_ids']),'disjoint partition')
 need(c['added_admissions']==old['added_admissions']+[c['current_science_registration']],'one science registration')
 before={r['original_id']:r for r in oldcat['entries']};after={r['original_id']:r for r in cat['entries']}
 need(len(after)==len(cat['entries'])==106 and before.keys()==after.keys(),'same original roster')
 need(all(before[k]==after[k] for k in before if k!='L011'),'105 other records exact')
 for key in before['L011']:
  if key not in ['current_principal_recovery','next_obligation']:need(before['L011'][key]==after['L011'][key],'source/history retained '+key)
 row=after['L011']['current_principal_recovery']
 need(row['historical_admission_evidence']==before['L011']['current_principal_recovery'] and row['principal_contract_admitted'] and not row['measured'] and row['compression_factor'] is None,'corrected unmeasured original')
 need(ad['source_ids']==['L011'] and ad['source_id']=='L011' and ad['principal_originals_added']==1,'one original')
 need(all(s in ad['source_author_role'] for s in ['Leemans','Vandenschrick']),'source attribution')
 need(ad['physical_pages']==[4,4] and ad['source_pages']==6 and ad['source_routes']==27 and ad['complete_proof_environments']==9,'complete source/papers')
 need(len(ad['whole_scientific_manuscripts'])==2,'both whole papers paid')
 need(not ad['measured'] and not ad['comparison_topic_created'] and not ad['current_measurements_changed'] and ad['compression_factor'] is ad['software_inclusive_factor'] is ad['source_software_cost'] is None,'no invented measurement')
 need(ad['new_question_credit']==ad['new_Lean_declarations']==0 and not ad['whole_source_formalized'] and not ad['theorem_sets_equivalent'],'scope limits')
 required={(r['packet'],r['logical_path']) for r in roles['required_mathematical_programs']}
 need(required=={('author','programs/string_search.g'),('author','programs/unitary_models.g'),('author','programs/run_certificate.g')},'whole required finite programs')
 need(ad['required_mathematical_programs']==[r['public_path'] for r in roles['required_mathematical_programs']],'actual required program routes')
 need(ad['required_data_files']==roles['required_mathematical_data']==[] and roles['generated_receipts_are_not_independent_algorithm_inputs'],'generated receipts distinct from input data')
 need(roles['formal_files']==[] and roles['source_software_cost'] is roles['software_inclusive_factor'] is roles['measurement'] is roles['external_runtime_cost'] is None and roles['unknown_not_zero'],'software symmetry')
 need(len(roles['whole_files'])==29 and all(r['complete_file'] for r in roles['whole_files']),'29 whole-file occurrences')
 names={r['logical_path']:r['role'] for r in roles['whole_files']}
 need(len(names)==29 and all(names[n]=='REQUIRED_MATHEMATICAL_PROGRAM' for _,n in required),'three genuine premise roles')
 need(names['run.py']=='OPERATIONAL_FULL_CERTIFICATE_DRIVER' and names['check.py']=='OPERATIONAL_PACKET_DRIVER' and names['optional_permutation_oracle.py']=='OPTIONAL_VALIDATION','driver and optional roles')
 need(all(v in ['GENERATED_MODEL_OR_EXECUTION_OUTPUT','GENERATED_REQUIRED_CERTIFICATE_RECEIPT'] for k,v in names.items() if k.startswith('reports/')) and sum(k.startswith('reports/') for k in names)==23,'all generated outputs inventoried')
 need('generator-only' in roles['order_verification'] and 'cached' in roles['order_verification'],'fresh order scope')
 need(review['status']=='ACCEPTED_COMPLETE_PRINCIPAL_RECOVERY' and review['reviewer']=='root' and review['original']=='L011' and review['mathematical_author']=='enumeration_volume' and review['distinct_scientific_review'],'actual distinct complete root acceptance')
 need(review['source_rows']==27 and review['complete_proof_environments']==9 and review['full_native_written_pages']==[4,4] and review['complete_primary_text_read'],'whole source and proofs')
 need(review['required_finite_cases']==8 and review['proper_prefixes']==1209 and review['positive_A5_markings']==6 and review['fresh_uncached_order_calculations']==11,'exact accepted finite evidence')
 need(review['retained_positive_classification'] and review['new_question_credit']==review['new_formal_declarations']==0 and review['measurements'] is review['external_proof_cost'] is None,'retained classification and scope')
 for key in oldpapers:
  if key not in ['status','active_source_catalogue','corrected_unmeasured_scientific_catalogue']:need(papers[key]==oldpapers[key],'old measured paper record '+key)
 need(papers['status']=='CURRENT_MANUSCRIPTS_53_MEASURED_PLUS_EIGHT_CORRECTED_UNMEASURED','current paper summary')
 need(sc['entries'][:-2]==oldsc['entries'] and sc['acquired_dependencies']==oldsc['acquired_dependencies'],'old scientific rows exact')
 need(sc['original_ids']==oldsc['original_ids']+['L011'] and sc['existing_comparison_topic_count']==19 and sc['new_measurements']==0,'no comparison-topic growth')
 new=sc['entries'][-2:]
 need([r['id'] for r in new]==['L011_common','L011_application'] and [r['physical_pages'] for r in new]==[4,4],'two native documents')
 need(all(r['source_ids']==['L011'] and r['compiler']=='pdflatex' and not r['measured'] and r['compression_factor'] is None and r['externaldocument_dependency'] is None for r in new),'standalone compiler/scope')

def controls(args):
 results=[]
 def bad(name,mut):
  x=copy.deepcopy(args);mut(x)
  try:semantic(*x)
  except(ValueError,KeyError,IndexError):results.append(name)
  else:raise ValueError('control accepted: '+name)
 bad('reviewed counted as measured',lambda a:a[0].__setitem__('currently_measured_originals',60))
 bad('duplicate L011',lambda a:a[0]['admitted_original_ids'].append('L011'))
 bad('another pending original dropped',lambda a:a[0]['accessible_pending_original_ids'].pop())
 bad('old measurement changed',lambda a:a[0]['added_measurements'].append({}))
 bad('old registration dropped',lambda a:a[0]['added_admissions'].pop(0))
 bad('earlier L039 scope changed',lambda a:next(r for r in a[2]['entries'] if r['original_id']=='L039').__setitem__('next_obligation','changed'))
 bad('source attribution changed',lambda a:a[8].__setitem__('source_author_role','Other'))
 bad('source identity changed',lambda a:next(r for r in a[2]['entries'] if r['original_id']=='L011').__setitem__('authors',['Other']))
 bad('common shortened',lambda a:a[8].__setitem__('physical_pages',[3,4]))
 bad('common free',lambda a:a[8]['whole_scientific_manuscripts'].pop(0))
 bad('source clause lost',lambda a:a[8].__setitem__('source_routes',26))
 bad('new factor invented',lambda a:a[8].__setitem__('compression_factor',1))
 bad('software unknown becomes zero',lambda a:a[9].__setitem__('source_software_cost',0))
 bad('new question credit',lambda a:a[8].__setitem__('new_question_credit',1))
 bad('literal equivalence claimed',lambda a:a[8].__setitem__('theorem_sets_equivalent',True))
 bad('required search becomes optional',lambda a:next(r for r in a[9]['whole_files'] if r['logical_path']=='programs/string_search.g').__setitem__('role','OPTIONAL_VALIDATION'))
 bad('whole output omitted',lambda a:a[9]['whole_files'].pop())
 bad('generated output becomes data premise',lambda a:a[9]['required_mathematical_data'].append({}))
 bad('positive classification erased',lambda a:a[10].__setitem__('retained_positive_classification',False))
 bad('finite exception lost',lambda a:a[10].__setitem__('required_finite_cases',7))
 bad('prefix bound truncated',lambda a:a[10].__setitem__('proper_prefixes',1208))
 bad('cached orders reused',lambda a:a[10].__setitem__('fresh_uncached_order_calculations',0))
 bad('old scientific row removed',lambda a:a[6]['entries'].pop(0))
 bad('wrong native compiler',lambda a:a[6]['entries'][-1].__setitem__('compiler','xelatex'))
 bad('new comparison topic',lambda a:a[6].__setitem__('existing_comparison_topic_count',20))
 bad('retrieval reopened',lambda a:a[0].__setitem__('source_retrieval_in_scope',True))
 bad('review author confused',lambda a:a[10].__setitem__('reviewer','enumeration_volume'))
 return results

def root_gate(gate,required):
 need(gate['status']=='ROOT_ACCEPTED_SCIENCE61_PUBLICATION' and gate['source_ids']==['L011'] and gate['measurements_added']==gate['new_question_credit']==0,'root-only integration gate')
 paths=[r['path'] for r in gate['bindings']]
 need(len(paths)==len(set(paths)) and required<=set(paths),'complete distinct root bindings')

def verify(root,require_root=False):
 root=Path(root).resolve();base=load(HERE/'baseline.json');plan=load(HERE/'copy_plan.json')
 if(HERE/'manifest.json').exists():
  for r in load(HERE/'manifest.json')['exports']:bind(HERE,r)
 for r in load(HERE/'wrapper_routes.json')['files']:bind(root,r)
 for r in base['protected_files']:bind(root,r)
 need(len(plan['files'])==len({r['public_path'] for r in plan['files']})==52 and len(plan['packets'])==2,'complete two-packet closure')
 for r in plan['files']:
  bind(root,dict(path=r['public_path'],bytes=r['bytes'],sha256=r['sha256']))
  need(not r['public_path'].endswith('.md') and not any(p in PurePosixPath(r['public_path']).parts for p in ['sources','private_source','rasters','fonts']),'no primary assets/Markdown')
 for packet in plan['packets']:
  bind(root,packet['manifest']);m=load(root/packet['manifest']['path']);routes={r['logical_path']:r for r in plan['files'] if r['packet']==packet['id']}
  need(len(m['exports'])==packet['exports'] and set(routes)=={'manifest.json'}|{r['path'] for r in m['exports']},'whole logical packet')
  for r in m['exports']:need(all(routes[r['path']][k]==r[k] for k in ['bytes','sha256']),'exact logical bytes')
 history=load(root/AUDIT/'history_routes.json')['routes'];need(history==base['history'],'saved pointer routes')
 for r in history.values():bind(root,r)
 old=load(root/history['audit/corpus/latest.json']['path']);c=load(root/'audit/corpus/latest.json')
 for k in ['active_catalogue','snapshot','current_science_registration']:bind(root,c[k])
 need(load(root/c['snapshot']['path'])=={k:v for k,v in c.items() if k!='snapshot'},'current immutable snapshot')
 bind(root,base['old_catalogue']);oldcat=load(root/base['old_catalogue']['path']);cat=load(root/c['active_catalogue']['path'])
 papers=load(root/'papers/latest_catalogue.json');oldpapers=load(root/history['papers/latest_catalogue.json']['path'])
 need(papers['active_source_catalogue']==c['active_catalogue'],'current catalogue agreement');bind(root,papers['corrected_unmeasured_scientific_catalogue'])
 sc=load(root/papers['corrected_unmeasured_scientific_catalogue']['path']);oldsc=load(root/history['papers/catalogue_corrected_unmeasured.json']['path'])
 reg=load(root/c['current_science_registration']['path'])
 need(reg['source_ids']==['L011'] and reg['principal_originals_added']==1 and reg['measurement_originals_added']==reg['new_question_credit']==reg['new_Lean_declarations']==0 and reg['previous_registration']==old['current_science_registration'],'one science-only original')
 need(len(reg['admissions'])==1,'one admission');bind(root,reg['admissions'][0]);ad=load(root/reg['admissions'][0]['path'])
 for key in ['author_manifest','distinct_root_review_manifest','root_scientific_acceptance','source_map','scope','retained_inputs','program_roles']:bind(root,ad[key])
 need(ad['distinct_root_review_manifest']==ad['root_scientific_acceptance'],'actual root acceptance')
 need(next(r for r in cat['entries'] if r['original_id']=='L011')['current_principal_recovery']['latest_admission_references']==reg['admissions'],'actual L011 route')
 roles=load(root/ad['program_roles']['path']);review=load(root/SCIENCE/'root_review/review.json')
 for r in roles['whole_files']+roles['required_mathematical_data']:bind(root,dict(path=r['public_path'],bytes=r['bytes'],sha256=r['sha256']))
 args=[c,old,cat,oldcat,papers,oldpapers,sc,oldsc,ad,roles,review];semantic(*args);tests=controls(args)
 source_map=load(root/ad['source_map']['path']);need(len(source_map['dispositions'])==27 and not source_map['source_result_false'] and source_map['source']['sha256']=='506b2f864bf44492bc40bb3bc353d527d7d96cd9f5526cc632eb3c6b5c5a29aa','full exact source contract')
 from pypdf import PdfReader
 for row in sc['entries'][-2:]:
  need(re.search(r'\\title\{([^{}]+)\}',(root/row['tex']).read_text()).group(1)==row['title'],'literal title')
  need(len(PdfReader(root/row['pdf']).pages)==row['physical_pages'] and row['admission']==reg['admissions'][0],'whole PDF/admission')
 actual={n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest() for n in ast.parse((root/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name!='main'}
 need(len(base['old_nonmain_ASTs'])==147 and all(actual.get(k)==v for k,v in base['old_nonmain_ASTs'].items()),'147 unchanged old functions')
 readme=(root/'README.rst').read_text();protocol=(root/'audit/protocol.tex').read_text()
 for s in ['61 accessible originals','53 are measured and eight','44 await mathematical recovery','L011 guide','All 27 source dispositions','retained positive classification','auxiliary original,','not focal-group authored','Conjecture 1.1 remains unanswered']:
  need(s in readme,'reader scope '+s)
 need('106=61' in protocol and 'recoveries}+44' in protocol and 'Of the 61 corrected recoveries, 53' in protocol,'protocol partition')
 links=0
 for name in ['README.rst','audit/completion.rst',NATIVE+'/PUBLICATION.rst']:
  for target in re.findall(r'<([^<>\n]+)>`_', (root/name).read_text()):
   if re.match(r'\w+://',target):continue
   need((root/Path(name).parent/target).exists(),'local link '+target);links+=1
 if require_root:
  gate=load(root/AUDIT/'root_integration.json')
  required={r['path'] for r in load(HERE/'wrapper_routes.json')['files']}|{r['public_path'] for r in plan['files'] if r['public_path'].startswith(NATIVE+'/')}|{AUDIT+'/publication_plan/manifest.json','scripts/verify_snapshot.py'}
  root_gate(gate,required)
  for r in gate['bindings']:bind(root,r)
 return dict(status='PASS_SCIENCE61_ROUTES',publication_status='ROOT_ACCEPTED' if require_root else 'PUBLICATION_NOT_ADJUDICATED',counts=dict(active=106,corrected_recoveries=61,measured=53,unmeasured=8,mathematical_pending=44,editorial=1,archived=55,comparison_topics=19),exact_payload_routes=52,exact_packets=2,other_originals_preserved=105,unchanged_verifier_functions=147,unchanged_overview='v19',new_factors=0,native_pages=[4,4],checked_links=links,controls=tests,scientific_programs_rerun=False,extraction_or_Lean_rerun=False)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path);p.add_argument('--require-root',action='store_true');a=p.parse_args();report=verify(a.repo,a.require_root)
 if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report))
