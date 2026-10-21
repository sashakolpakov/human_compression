"""L015 publication integration guard; not a second scientific proof review."""
from pathlib import Path, PurePosixPath
import argparse, ast, copy, hashlib, json, re
HERE=Path(__file__).resolve().parent
AUDIT='audit/science64/v1'
SCIENCE='audit/recoveries/L015/v1'
NATIVE='papers/recoveries/L015/v1'
def need(v,m):
 if not v: raise ValueError('SCIENCE64: '+m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(root,row):
 p=PurePosixPath(row['path']);need(not p.is_absolute() and '..' not in p.parts,'safe path')
 raw=(root/p).read_bytes();need(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'file '+row['path'])

def source_semantics(m):
 rows={r['id']:r for r in m['rows']}
 wanted={'T3.2.Generation':'REFUTED_EXACT_WRITTEN_COUNTEREXAMPLE','C3.5':'REFUTED_EXACT_WRITTEN_COUNTEREXAMPLE','C3.7.Universal':'REFUTED_AMBIENT_GENERATION_PART','T3.14.RC':'REFUTED_AS_PRINTED_AND_REPAIRED','T3.16':'RECOVERED_CORRECTED_PRINCIPAL_THEOREM','C3.7.Existential':'RECOVERED_CORRECTED_UNIFORM_PROOF','T2.5':'RETAINED_WITH_CONVENTION_REPAIR','Introduction.Sz8Counts':'RETAINED_HISTORICAL_NOT_PREMISE'}
 need(all(rows[k]['disposition']==v for k,v in wanted.items()),'corrected source dispositions')
 need(not m['literal_theorem_set_equivalence'],'source theorem equivalence')

def semantic(c,old,cat,oldcat,papers,oldpapers,sc,oldsc,ad,roles,review):
 need(tuple(c[k] for k in ['originals','admitted_principal_originals','currently_measured_originals','accessible_pending_complete_recovery','editorial_originals','archived_unavailable_originals'])==(106,64,53,41,1,55),'partition')
 need(len(c['admitted_original_ids'])==len(set(c['admitted_original_ids']))==64 and set(c['admitted_original_ids'])==set(old['admitted_original_ids'])|{'L015'},'L015 added once')
 need(len(c['accessible_pending_original_ids'])==41 and set(c['accessible_pending_original_ids'])==set(old['accessible_pending_original_ids'])-{'L015'},'pending subtraction')
 need(c['measurement_pending_original_ids']==c['scientific_unmeasured_original_ids']==['F008','F011','L011','L013','L015','L024','L025','L039','L102','L122','N014'],'eleven unmeasured')
 for k in ['measured_original_ids','added_measurements','current_topic_replacements','historical_admitted_ids','active_original_ids','archived_original_ids','editorial_original_ids','editorial_factor','source_retrieval_in_scope','all_original_proofs_recovered','all_conjectures_resolved']:
  need(c[k]==old[k],'unchanged '+k)
 parts=[set(c['admitted_original_ids']),set(c['accessible_pending_original_ids']),set(c['editorial_original_ids'])]
 need(sum(map(len,parts))==106 and set.union(*parts)==set(c['active_original_ids']),'disjoint partition')
 need(c['added_admissions']==old['added_admissions']+[c['current_science_registration']],'one science registration')
 before={r['original_id']:r for r in oldcat['entries']};after={r['original_id']:r for r in cat['entries']}
 need(len(after)==len(cat['entries'])==106 and before.keys()==after.keys(),'same original roster')
 need(all(before[k]==after[k] for k in before if k!='L015'),'105 other records exact')
 for key in before['L015']:
  if key not in ['current_principal_recovery','next_obligation']:need(before['L015'][key]==after['L015'][key],'source/history retained '+key)
 row=after['L015']['current_principal_recovery']
 need(row['historical_admission_evidence']==before['L015']['current_principal_recovery'] and row['principal_contract_admitted'] and not row['measured'] and row['compression_factor'] is None,'corrected unmeasured original')
 need(ad['source_ids']==['L015'] and ad['source_id']=='L015' and ad['principal_originals_added']==1,'one original')
 need(all(x in ad['source_author_role'] for x in ['Leemans','Stokes','Tranchida']),'source authors')
 need(ad['physical_pages']==[4,6,4] and ad['source_pages']==14 and ad['source_routes']==45,'whole source/native papers')
 need(len(ad['whole_scientific_manuscripts'])==3,'all complete papers')
 need(not ad['measured'] and not ad['comparison_topic_created'] and not ad['current_measurements_changed'] and ad['compression_factor'] is ad['software_inclusive_factor'] is ad['source_software_cost'] is None,'no new metric')
 need(ad['new_question_credit']==ad['new_Lean_declarations']==0 and not ad['whole_source_formalized'] and not ad['theorem_sets_equivalent'],'corrected scope')
 need(roles['required_mathematical_programs']==roles['required_mathematical_data']==ad['required_mathematical_programs']==ad['required_data_files']==[],'written proof, no finite premises')
 need(len(roles['whole_files'])==2 and all(x['complete_file'] for x in roles['whole_files']),'whole2 role inventory')
 names={x['logical_path']:x['role'] for x in roles['whole_files']}
 need(names=={'optional_checks.py':'OPTIONAL_BOUNDED_VALIDATION','check.py':'OPERATIONAL_BINDING_SCOPE_RENDER'},'exact optional and driver roles')
 need(len(roles['optional_validation'])==len(roles['operational_drivers'])==1 and roles['archived_discovery']==roles['formal_files']==[],'validation/driver/formal boundary')
 for key,role in [('optional_validation','OPTIONAL_BOUNDED_VALIDATION'),('operational_drivers','OPERATIONAL_BINDING_SCOPE_RENDER')]:need(roles[key]==[x for x in roles['whole_files'] if x['role']==role],'consistent role view '+key)
 need(roles['source_executable_listing_pages']==[] and roles['source_software_cost'] is roles['external_proof_cost'] is roles['external_runtime_cost'] is roles['software_inclusive_factor'] is roles['measurement'] is None and roles['unknown_not_zero'],'symmetric unknown software')
 need('not copied as a required premise' in roles['historical_finite_seed'],'old seed not imported')
 need(review['decision']=='ACCEPTED_COMPLETE_CORRECTED_PRINCIPAL_RECOVERY' and review['original']=='L015' and review['reviewer']=='root','distinct root science acceptance')
 need(review['whole_native_pages']==[4,6,4] and review['new_original_credit']==1 and review['new_conjecture_credit']==review['new_Lean_declarations']==0 and review['new_factors'] is None and not review['literal_theorem_set_equivalence'],'whole accepted scope')
 need(review['author_manifest_sha256']==ad['author_manifest']['sha256'] and review['source_sha256']=='627439f5c866001bcaa12add9599f3b60c2a18d53677b5585703111c055df3cc','actual reviewed author/source')
 need(all(x in ad['scope_note'] for x in ['proper-Sz8-in-Sz(2^15)','General-m coset flag transitivity is not asserted','historical','unknown']),'source and frozen status limits')
 for key in oldpapers:
  if key not in ['status','active_source_catalogue','corrected_unmeasured_scientific_catalogue']:need(papers[key]==oldpapers[key],'old measured paper record '+key)
 need(papers['status']=='CURRENT_MANUSCRIPTS_53_MEASURED_PLUS_ELEVEN_CORRECTED_UNMEASURED','current paper summary')
 need(sc['entries'][:-3]==oldsc['entries'] and sc['acquired_dependencies']==oldsc['acquired_dependencies'],'old scientific rows exact')
 need(sc['original_ids']==oldsc['original_ids']+['L015'] and sc['existing_comparison_topic_count']==19 and sc['new_measurements']==0,'no comparison-topic growth')
 new=sc['entries'][-3:]
 need([r['id'] for r in new]==['L015_generation','L015_application','L015_inherited_common'] and [r['physical_pages'] for r in new]==[4,6,4],'three native papers')
 need(all(r['source_ids']==['L015'] and r['compiler']=='pdflatex' and not r['measured'] and r['compression_factor'] is None and r['externaldocument_dependency'] is None for r in new),'standalone compiler/scope')

def controls(args):
 results=[]
 def bad(name,mut):
  x=copy.deepcopy(args);mut(x)
  try:semantic(*x)
  except(ValueError,KeyError,IndexError):results.append(name)
  else:raise ValueError('control accepted: '+name)
 bad('reviewed counted measured',lambda a:a[0].__setitem__('currently_measured_originals',64))
 bad('duplicate original',lambda a:a[0]['admitted_original_ids'].append('L015'))
 bad('other target dropped',lambda a:a[0]['accessible_pending_original_ids'].pop())
 bad('old measurement changed',lambda a:a[0]['added_measurements'].append({}))
 bad('old admission lost',lambda a:a[0]['added_admissions'].pop(0))
 bad('old L122 row changed',lambda a:next(x for x in a[2]['entries'] if x['original_id']=='L122').__setitem__('next_obligation','changed'))
 bad('source attribution',lambda a:a[8].__setitem__('source_author_role','Other'))
 bad('third coauthor omitted',lambda a:a[8].__setitem__('source_author_role','Dimitri Leemans and Klara Stokes; focal-group-authored source.'))
 bad('primary metadata altered',lambda a:next(x for x in a[2]['entries'] if x['original_id']=='L015').__setitem__('authors',['Other']))
 bad('inherited common shortened',lambda a:a[8].__setitem__('physical_pages',[4,6,0]))
 bad('inherited common free',lambda a:a[8]['whole_scientific_manuscripts'].pop())
 bad('source row missing',lambda a:a[8].__setitem__('source_routes',44))
 bad('factor invented',lambda a:a[8].__setitem__('compression_factor',1))
 bad('unknown software zero',lambda a:a[9].__setitem__('source_software_cost',0))
 bad('new question',lambda a:a[8].__setitem__('new_question_credit',1))
 bad('literal equivalence',lambda a:a[8].__setitem__('theorem_sets_equivalent',True))
 bad('optional code made premise',lambda a:a[9]['whole_files'][0].__setitem__('role','REQUIRED_MATHEMATICAL_PROGRAM'))
 bad('whole driver omitted',lambda a:a[9]['whole_files'].pop())
 bad('finite data invented',lambda a:a[9]['required_mathematical_data'].append({}))
 bad('formalization invented',lambda a:a[9]['formal_files'].append('new.lean'))
 bad('review status pending',lambda a:a[10].__setitem__('decision','PENDING'))
 bad('reviewer changed to author',lambda a:a[10].__setitem__('reviewer','rewrite_termination'))
 bad('different author reviewed',lambda a:a[10].__setitem__('author_manifest_sha256','0'*64))
 bad('counterexample scope lost',lambda a:a[8].__setitem__('scope_note','All source theorems proved'))
 bad('historical scientific row lost',lambda a:a[6]['entries'].pop(0))
 bad('wrong compiler',lambda a:a[6]['entries'][-1].__setitem__('compiler','xelatex'))
 bad('new topic',lambda a:a[6].__setitem__('existing_comparison_topic_count',20))
 bad('retrieval reopened',lambda a:a[0].__setitem__('source_retrieval_in_scope',True))
 return results

def root_gate(gate,required):
 need(gate['status']=='ROOT_ACCEPTED_SCIENCE64_PUBLICATION' and gate['source_ids']==['L015'] and gate['measurements_added']==gate['new_question_credit']==0,'root-only integration gate')
 paths=[r['path'] for r in gate['bindings']]
 need(len(paths)==len(set(paths)) and required<=set(paths),'complete distinct root bindings')

def verify(root,require_root=False):
 root=Path(root).resolve();base=load(HERE/'baseline.json');plan=load(HERE/'copy_plan.json')
 if(HERE/'manifest.json').exists():
  for r in load(HERE/'manifest.json')['exports']:bind(HERE,r)
 for r in load(HERE/'wrapper_routes.json')['files']:bind(root,r)
 for r in base['protected_files']:bind(root,r)
 need(len(plan['files'])==len({r['public_path'] for r in plan['files']})==26 and len(plan['packets'])==2,'complete two-packet closure')
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
 need(reg['source_ids']==['L015'] and reg['principal_originals_added']==1 and reg['measurement_originals_added']==reg['new_question_credit']==reg['new_Lean_declarations']==0 and reg['previous_registration']==old['current_science_registration'],'one science-only original')
 need(len(reg['admissions'])==1,'one admission');bind(root,reg['admissions'][0]);ad=load(root/reg['admissions'][0]['path'])
 for key in ['author_manifest','distinct_root_review_manifest','root_scientific_acceptance','source_map','scope','retained_inputs','dependency_boundary','program_roles']:bind(root,ad[key])
 need(ad['distinct_root_review_manifest']==ad['root_scientific_acceptance'],'exact root review/adoption role')
 for field,key in [('author_manifest','author'),('distinct_root_review_manifest','root_review')]:need(ad[field]==next(p['manifest'] for p in plan['packets'] if p['id']==key),'exact reviewed packet '+field)
 need(next(x for x in cat['entries'] if x['original_id']=='L015')['current_principal_recovery']['latest_admission_references']==reg['admissions'],'actual original route')
 roles=load(root/ad['program_roles']['path']);review=load(root/SCIENCE/'root_review/review.json')
 for r in roles['whole_files']+roles['required_mathematical_data']:bind(root,dict(path=r['public_path'],bytes=r['bytes'],sha256=r['sha256']))
 args=[c,old,cat,oldcat,papers,oldpapers,sc,oldsc,ad,roles,review];semantic(*args);tests=controls(args)
 source_map=load(root/ad['source_map']['path']);need(len(source_map['rows'])==len({x['id'] for x in source_map['rows']})==45 and source_map['source']['sha256']=='627439f5c866001bcaa12add9599f3b60c2a18d53677b5585703111c055df3cc','entire exact source')
 source_semantics(source_map)
 for claim in ['T3.2.Generation','C3.5','C3.7.Universal','T3.14.RC','T3.16','C3.7.Existential','T2.5','Introduction.Sz8Counts']:
  changed=copy.deepcopy(source_map);next(r for r in changed['rows'] if r['id']==claim)['disposition']='UNQUALIFIED'
  try:source_semantics(changed)
  except ValueError:tests.append('source disposition '+claim)
  else:raise ValueError('source mutation accepted')
 from pypdf import PdfReader
 for row in sc['entries'][-3:]:
  need(re.search(r'\\title\{([^{}]+)\}',(root/row['tex']).read_text()).group(1)==row['title'],'literal title')
  need(len(PdfReader(root/row['pdf']).pages)==row['physical_pages'] and row['admission']==reg['admissions'][0],'whole PDF/admission')
 actual={n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest() for n in ast.parse((root/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name!='main'}
 need(len(base['old_nonmain_ASTs'])==153 and all(actual.get(k)==v for k,v in base['old_nonmain_ASTs'].items()),'153 unchanged old functions')
 readme=(root/'README.rst').read_text();protocol=(root/'audit/protocol.tex').read_text()
 for s in ['64 accessible originals','53 are measured and eleven','41 await mathematical recovery','L015 guide','All 45','unrestricted generation','auxiliary original,','not focal-group authored','Conjecture 1.1 remains unanswered']:
  need(s in readme,'reader scope '+s)
 need('106=64' in protocol and 'recoveries}+41' in protocol and 'Of the 64 corrected recoveries, 53' in protocol,'protocol partition')
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
 return dict(status='PASS_SCIENCE64_ROUTES',publication_status='ROOT_ACCEPTED' if require_root else 'PUBLICATION_NOT_ADJUDICATED',counts=dict(active=106,corrected_recoveries=64,measured=53,unmeasured=11,mathematical_pending=41,editorial=1,archived=55,comparison_topics=19),exact_payload_routes=26,exact_packets=2,other_originals_preserved=105,unchanged_verifier_functions=153,unchanged_overview='v19',new_factors=0,native_pages=[4,6,4],checked_links=links,controls=tests,scientific_programs_rerun=False,extraction_or_Lean_rerun=False)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path);p.add_argument('--require-root',action='store_true');a=p.parse_args();report=verify(a.repo,a.require_root)
 if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report))
