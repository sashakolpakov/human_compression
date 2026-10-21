"""Check the science-only successor; no extraction, arithmetic or proof execution."""
from pathlib import Path, PurePosixPath
import argparse, ast, copy, hashlib, json, re
HERE=Path(__file__).resolve().parent
AUDIT='audit/science55/v1'
def need(t,m):
 if not t:raise ValueError('SCIENCE55: '+m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(root,e):
 p=PurePosixPath(e['path']);need(not p.is_absolute()and '..'not in p.parts and str(p)==e['path'],'safe path');f=root/p
 need(f.stat().st_size==e['bytes']and sha(f)==e['sha256'],'exact binding '+str(p))
def semantic(corpus,old,cat,oldcat,papers,oldpapers,sc,admissions,roles):
 need((corpus['originals'],corpus['admitted_principal_originals'],corpus['currently_measured_originals'],corpus['accessible_pending_complete_recovery'],corpus['editorial_originals'],corpus['archived_unavailable_originals'])==(106,55,53,50,1,55),'complete106 partition')
 need(set(corpus['admitted_original_ids'])==set(old['admitted_original_ids'])|{'N014','L024'},'exact two scientific recoveries')
 need(len(corpus['admitted_original_ids'])==55 and len(corpus['accessible_pending_original_ids'])==50,'unique admitted and pending lists')
 need(set(corpus['accessible_pending_original_ids'])==set(old['accessible_pending_original_ids'])-{'N014','L024'},'exact pending subtraction')
 need(corpus['measurement_pending_original_ids']==['L024','N014']and corpus['scientific_unmeasured_original_ids']==['L024','N014'],'two unmeasured originals')
 for key in ['measured_original_ids','added_measurements','current_topic_replacements','historical_admitted_ids','active_original_ids','archived_original_ids','editorial_original_ids','editorial_factor']:
  need(corpus[key]==old[key],'no measurement/scope change '+key)
 need(not corpus['source_retrieval_in_scope']and not corpus['all_original_proofs_recovered']and not corpus['all_conjectures_resolved'],'unfinished fixed scope')
 sets=[set(corpus['admitted_original_ids']),set(corpus['accessible_pending_original_ids']),set(corpus['editorial_original_ids'])]
 need(set.union(*sets)==set(corpus['active_original_ids'])and sum(map(len,sets))==106,'disjoint active partition')
 need(len(set(corpus['measured_original_ids']))==53 and set(corpus['measured_original_ids'])<sets[0],'53 unique measured subset')
 before={x['original_id']:x for x in oldcat['entries']};after={x['original_id']:x for x in cat['entries']}
 need(len(cat['entries'])==len(after)==106 and before.keys()==after.keys(),'same106 original identities')
 need(all(after[k]==before[k]for k in before if k not in ['N014','L024']),'104 other records exact')
 need(cat['admitted_principal_originals']==55 and cat['accessible_pending_complete_recovery']==50,'catalogue counts')
 for oid in ['N014','L024']:
  row=after[oid];q=row['current_principal_recovery'];a=admissions[oid]
  need(q['status']=='ADMITTED_CORRECTED_PRINCIPAL_RECOVERY_MEASUREMENT_PENDING'and not q['measured']and q['compression_factor']is None,'scientific status '+oid)
  need(q['historical_admission_evidence']==before[oid]['current_principal_recovery'],'prior evidence retained '+oid)
  for key in ['source_access','authors','title','year','edition','historical_proof_status','active','original_count']:
   need(row[key]==before[oid][key],'unchanged source identity '+oid+'/'+key)
  need(a['source_ids']==[oid]and a['measurement_status']=='pending'and not a['measured']and a['compression_factor']is None and a['software_inclusive_factor']is None,'no scalar '+oid)
  need(a['new_question_credit']==a['new_Lean_declarations']==0 and not a['whole_source_formalized']and not a['theorem_sets_equivalent'],'scope limits '+oid)
 need(admissions['N014']['physical_pages']==[10,8,17]and len(admissions['N014']['whole_common'])==2,'complete C acquisition')
 need(admissions['L024']['physical_pages']==[5]and not admissions['L024']['comparison_topic_created'],'five-page L024 not a topic ratio')
 need(papers['entries']==oldpapers['entries'],'all103 earlier paper records unchanged')
 for k in oldpapers:
  if k not in ['status','active_source_catalogue']:need(papers[k]==oldpapers[k],'other manuscript pointer metadata '+k)
 need(len(sc['entries'])==3 and [x['physical_pages']for x in sc['entries']]==[8,17,5]and [x['physical_pages']for x in sc['acquired_dependencies']]==[10],'native complete boundaries')
 need([x['compiler']for x in sc['entries']]==['xelatex','xelatex','pdflatex']and sc['acquired_dependencies'][0]['compiler']=='xelatex','accepted native compiler identities')
 need([x['source_ids']for x in sc['entries']]==[['N014'],['N014'],['L024']],'exact scientific routing')
 need(sc['new_measurements']==0 and sc['existing_comparison_topic_count']==19 and all(not r['measured']and r['compression_factor']is None and not r['comparison_topic_created']for r in sc['entries']),'no topic or comparison added')
 current=roles['current_files'];need(len(current)==15 and roles['software_inclusive_factor']is None and roles['no_disjoint_role_sum'],'whole role overlay')
 n=[x for x in current if x['original_id']=='N014'];need(len(n)==13,'12 inherited and top driver')
 need({x['path']for x in n if x.get('required_for_N014')}=={'inputs/phase30_affine_map_check.py','inputs/phase30_affine_map_check.json'},'complete finite premise')
 need(next(x for x in n if x['path']=='check.py')['role']=='operational_assembly_driver','whole top-level driver')
 l=[x for x in current if x['original_id']=='L024'];need(len(l)==2 and next(x for x in l if x['path']=='verify_schur_example.g')['role']=='required_mathematical_program','whole required L024 program')
 need('pp3–5'in roles['source_listing_policy']['L024'],'future symmetric source-code boundary')
 return True
def controls(args):
 cases=[]
 def test(label,mut):
  a=copy.deepcopy(args);mut(a)
  try:semantic(*a)
  except (ValueError,KeyError,StopIteration):cases.append(label)
  else:raise ValueError('control accepted '+label)
 test('recoveries confused with measurements',lambda a:a[0].__setitem__('currently_measured_originals',55))
 test('pending original lost',lambda a:a[0]['accessible_pending_original_ids'].pop())
 test('new original counted twice',lambda a:a[0]['admitted_original_ids'].append('N014'))
 test('measurement admission invented',lambda a:a[0]['added_measurements'].append({}))
 test('N014 assigned old C factor',lambda a:a[7]['N014'].__setitem__('compression_factor',1.291738))
 test('unknown source software priced zero',lambda a:a[7]['L024'].__setitem__('software_inclusive_factor',0))
 test('common acquired partly',lambda a:a[7]['N014']['whole_common'].pop())
 test('old common dropped',lambda a:a[7]['N014'].__setitem__('physical_pages',[8,17]))
 test('new numerical topic invented',lambda a:a[7]['L024'].__setitem__('comparison_topic_created',True))
 test('theorem-set equivalence claimed',lambda a:a[7]['N014'].__setitem__('theorem_sets_equivalent',True))
 test('new question credit claimed',lambda a:a[7]['L024'].__setitem__('new_question_credit',1))
 test('whole Lean claimed',lambda a:a[7]['N014'].__setitem__('whole_source_formalized',True))
 test('old record changed',lambda a:next(r for r in a[2]['entries']if r['original_id']=='L003').__setitem__('next_obligation','changed'))
 test('L022 factor added',lambda a:a[0].__setitem__('editorial_factor',1))
 test('old measured manuscript changed',lambda a:a[4]['entries'].pop())
 test('full application shortened',lambda a:a[6]['entries'][1].__setitem__('physical_pages',16))
 test('compiler replaced',lambda a:a[6]['entries'][2].__setitem__('compiler','xelatex'))
 test('extra comparison counted',lambda a:a[6].__setitem__('existing_comparison_topic_count',20))
 test('top operational driver omitted',lambda a:a[8]['current_files'].pop(12))
 test('required data demoted',lambda a:next(x for x in a[8]['current_files']if x['path']=='inputs/phase30_affine_map_check.json').__setitem__('required_for_N014',False))
 test('required L024 file demoted',lambda a:next(x for x in a[8]['current_files']if x['path']=='verify_schur_example.g').__setitem__('role','optional_validation'))
 test('archive retrieval reopened',lambda a:a[0].__setitem__('source_retrieval_in_scope',True))
 return cases
def verify(repo,require_root=False):
 repo=Path(repo);base=load(HERE/'baseline.json');plan=load(HERE/'copy_plan.json');wr=load(HERE/'wrapper_routes.json')
 if (HERE/'manifest.json').exists():
  for e in load(HERE/'manifest.json')['exports']:bind(HERE,e)
 for e in wr['files']:bind(repo,e)
 for e in base['protected_files']:bind(repo,e)
 rows=plan['files'];need(len(rows)==224 and len(plan['packets'])==6,'complete six packets')
 need(len({r['public_path']for r in rows})==224,'unique public routes')
 for r in rows:
  bind(repo,dict(path=r['public_path'],bytes=r['bytes'],sha256=r['sha256']))
  need(not r['public_path'].endswith('.md')and not any(x in PurePosixPath(r['public_path']).parts for x in ['sources','private_source','rasters','fonts']),'no new primary assets/Markdown')
 for p in plan['packets']:
  bind(repo,p['manifest']);m=load(repo/p['manifest']['path']);actual={r['logical_path']:r for r in rows if r['packet']==p['id']}
  need(set(actual)=={'manifest.json'}|{x['path']for x in m['exports']}and len(m['exports'])==p['exports'],'exact complete packet map '+p['id'])
  for e in m['exports']:need(all(actual[e['path']][k]==e[k]for k in ['bytes','sha256']),'logical file binding '+e['path'])
 rename=load(HERE/'provenance_path_map.json')['renames'];need(len(rename)==8,'eight explicit extension-only maps')
 for r in rename:
  match=next(x for x in rows if x['packet']==r['packet']and x['logical_path']==r['logical_path']);need(match['public_path']==r['public_path']and all(match[k]==r[k]for k in ['bytes','sha256']),'unchanged prose map')
 reused=load(HERE/'reused_science.json');need(len(reused['files'])==7 and reused['whole_old_common_required']and reused['whole_old_common_pages']==10,'old C acquired in full')
 for e in reused['files']:bind(repo,e)
 history=load(repo/(AUDIT+'/history_routes.json'))['routes']
 for key,e in history.items():bind(repo,e);need(e==base['history'][key],'exact preceding reader/pointer')
 old=load(repo/history['audit/corpus/latest.json']['path']);corpus=load(repo/'audit/corpus/latest.json');bind(repo,corpus['active_catalogue']);bind(repo,corpus['snapshot']);bind(repo,corpus['current_science_registration'])
 oldcat=load(repo/base['old_catalogue']['path']);bind(repo,base['old_catalogue']);cat=load(repo/corpus['active_catalogue']['path'])
 oldpapers=load(repo/history['papers/latest_catalogue.json']['path']);papers=load(repo/'papers/latest_catalogue.json');bind(repo,papers['corrected_unmeasured_scientific_catalogue']);sc=load(repo/papers['corrected_unmeasured_scientific_catalogue']['path'])
 registration=load(repo/corpus['current_science_registration']['path']);need(registration['source_ids']==['N014','L024']and registration['measurement_originals_added']==0,'science-only registration')
 admissions={}
 for e in registration['admissions']:
  bind(repo,e);ad=load(repo/e['path']);admissions[ad['source_id']]=ad
  for k in ['author_manifest','distinct_review_manifest','root_adoption_manifest','source_map','scope']:bind(repo,ad[k])
 roles=load(repo/(AUDIT+'/whole_file_roles.json'))
 for e in roles['current_files']:bind(repo,dict(path=e['public_path'],bytes=e['bytes'],sha256=e['sha256']))
 args=[corpus,old,cat,oldcat,papers,oldpapers,sc,admissions,roles];semantic(*args);tests=controls(args)
 from pypdf import PdfReader
 for row in sc['entries']+sc['acquired_dependencies']:
  title=re.search(r'\\title\{([^{}]+)\}',(repo/row['tex']).read_text()).group(1)
  need(row['title']==title and len(PdfReader(repo/row['pdf']).pages)==row['physical_pages'],'literal title and complete PDF '+row['id'])
  need(all((repo/p).is_file()for p in row['tex_inputs']),'whole native TeX closure '+row['id'])
 # Unique measurements remain supplied exclusively by the existing53 registry.
 extra=[oid for e in corpus['added_measurements']for oid in load(repo/e['path'])['source_ids']]
 need(len(extra)==len(set(extra))and set(extra).isdisjoint(corpus['historical_admitted_ids'])and set(extra)|set(corpus['historical_admitted_ids'])==set(corpus['measured_original_ids']),'unchanged unique measured partition')
 actual={n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest()for n in ast.parse((repo/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'}
 need(len(base['old_nonmain_ASTs'])==135 and all(actual.get(k)==v for k,v in base['old_nonmain_ASTs'].items()),'all135 prior nonmain ASTs exact')
 readme=(repo/'README.rst').read_text();tex=(repo/'audit/protocol.tex').read_text()
 for phrase in ['55 accessible originals','53 are measured','50 await mathematical recovery','three complete common papers (41 pages)','application bundles (63 pages)','Neither recovery has a compression factor','fifty-three individual']:
  need(phrase in readme,'reader scope '+phrase)
 need('106=55'in tex and '53 have accepted manuscript measurements'in tex and 'all 105 mathematical originals, then stop'in tex,'protocol counts and stop')
 links=[]
 for name in ['README.rst','audit/completion.rst','papers/topic-c/extensions/generalized-halving/v1/PUBLICATION.rst','papers/recoveries/L024/v1/PUBLICATION.rst']:
  for target in re.findall(r'<([^<>\n]+)>`_', (repo/name).read_text()):
   if re.match(r'\w+://',target):continue
   need((repo/Path(name).parent/target).exists(),'guide route '+name+' -> '+target);links.append(target)
 root_status='PUBLICATION_NOT_ADJUDICATED'
 if require_root:
  a=load(repo/(AUDIT+'/root_integration.json'));need(a['status']=='ROOT_ACCEPTED_SCIENCE55_PUBLICATION','root publication acceptance')
  need(a['source_ids']==['N014','L024']and a['measurements_added']==0 and a['new_question_credit']==0,'root integration scope')
  required={'audit/corpus/latest.json','papers/latest_catalogue.json','README.rst','audit/protocol.tex','audit/protocol.pdf','audit/completion.rst',AUDIT+'/publication_plan/manifest.json'}
  need(required<={x['path']for x in a['bindings']},'complete root acceptance bindings')
  for e in a['bindings']:bind(repo,e)
  root_status='ROOT_ACCEPTED'
 return dict(status='PASS_SCIENCE55_ROUTES',publication_status=root_status,counts=dict(active=106,corrected_recoveries=55,measured=53,unmeasured=2,mathematical_pending=50,editorial=1,archived=55,comparison_topics=19),exact_payload_routes=len(rows),exact_packets=6,other_originals_preserved=104,old_paper_records_preserved=len(oldpapers['entries']),unchanged_verifier_functions=135,unchanged_overview='v19',new_comparison_factors=0,native_pages=[10,8,17,5],private_prose_extension_maps=8,whole_current_role_occurrences=15,checked_links=len(links),controls=tests,scientific_programs_rerun=False,extraction_or_Lean_rerun=False)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path);p.add_argument('--require-root',action='store_true');a=p.parse_args();r=verify(a.repo,a.require_root)
 if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r))
