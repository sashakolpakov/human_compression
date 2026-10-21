"""Science66 public-registration guard; accepted mathematics is not rerun here."""
from pathlib import Path,PurePosixPath
import argparse,ast,copy,hashlib,json,re
HERE=Path(__file__).resolve().parent;AUDIT='audit/science66/v1';SCIENCE='audit/recoveries/L023/v1';NATIVE='papers/recoveries/L023/v1'
def need(x,m):
 if not x:raise ValueError('SCIENCE66: '+m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(root,r):
 p=PurePosixPath(r['path']);need(not p.is_absolute() and '..' not in p.parts,'safe path');f=root/p
 need(f.is_file() and f.stat().st_size==r['bytes'] and sha(f)==r['sha256'],'binding '+r['path'])
def semantics(c,old,cat,oldcat,papers,oldpapers,sc,oldsc,ad,roles,review,source):
 need(tuple(c[k] for k in ['originals','admitted_principal_originals','currently_measured_originals','accessible_pending_complete_recovery','editorial_originals','archived_unavailable_originals'])==(106,66,53,39,1,55),'partition')
 need(len(c['admitted_original_ids'])==len(set(c['admitted_original_ids']))==66 and set(c['admitted_original_ids'])==set(old['admitted_original_ids'])|{'L023'},'only L023 added')
 need(len(c['accessible_pending_original_ids'])==39 and set(c['accessible_pending_original_ids'])==set(old['accessible_pending_original_ids'])-{'L023'},'pending subtraction')
 need(c['measurement_pending_original_ids']==c['scientific_unmeasured_original_ids']==sorted(old['measurement_pending_original_ids']+['L023']) and len(c['measurement_pending_original_ids'])==13,'13 unmeasured')
 for k in ['measured_original_ids','added_measurements','current_topic_replacements','historical_admitted_ids','active_original_ids','archived_original_ids','editorial_original_ids','editorial_factor','source_retrieval_in_scope','all_original_proofs_recovered','all_conjectures_resolved']:need(c[k]==old[k],'unchanged '+k)
 parts=[set(c['admitted_original_ids']),set(c['accessible_pending_original_ids']),set(c['editorial_original_ids'])];need(sum(map(len,parts))==106 and set.union(*parts)==set(c['active_original_ids']),'complete disjoint partition')
 need(c['added_admissions']==old['added_admissions']+[c['current_science_registration']],'one science registration')
 before={r['original_id']:r for r in oldcat['entries']};after={r['original_id']:r for r in cat['entries']};need(len(after)==len(cat['entries'])==106 and before.keys()==after.keys(),'same source roster')
 need(all(before[k]==after[k] for k in before if k!='L023'),'105 other records exact')
 for k in before['L023']:
  if k not in ['current_principal_recovery','next_obligation']:need(before['L023'][k]==after['L023'][k],'unchanged L023 source/history '+k)
 r=after['L023']['current_principal_recovery'];need(r['historical_admission_evidence']==before['L023']['current_principal_recovery'] and r['principal_contract_admitted'] and not r['measured'] and r['compression_factor'] is None,'corrected unmeasured current record')
 need(ad['source_ids']==['L023'] and ad['principal_originals_added']==1 and ad['source_author_role']=='Dimitri Leemans and Klara Stokes; focal-group-authored source.','one original and source authors')
 need(ad['physical_pages']==[3,4,3,1,5,3] and len(ad['whole_scientific_manuscripts'])==6,'whole19-page acquisition')
 need((ad['source_pages'],ad['source_routes'],ad['numbered_source_items'],ad['finite_table_rows'])==(13,70,10,12),'complete source contract')
 need(not ad['measured'] and not ad['comparison_topic_created'] and not ad['current_measurements_changed'] and ad['compression_factor'] is ad['software_inclusive_factor'] is None,'no new measurement')
 need(ad['new_question_credit']==ad['new_Lean_declarations']==0 and not ad['whole_source_formalized'] and not ad['theorem_sets_equivalent'],'qualified scope')
 need(len(roles['whole_files'])==12 and sum(x['role']=='REQUIRED_MATHEMATICAL_PROGRAM' for x in roles['whole_files'])==2,'complete whole program roles')
 need(sorted(x['path'] for x in roles['whole_files'] if x['role']=='REQUIRED_MATHEMATICAL_PROGRAM')==['components/geometry/certificate.py','components/polynomial/polynomial_table.g'],'actual required code')
 need(roles['required_stored_data']==[] and roles['source_software_cost'] is roles['external_proof_cost'] is roles['software_inclusive_factor'] is roles['measurement'] is None,'unknown costs, no invented input data')
 need(review['status']=='ACCEPTED_COMPLETE_CORRECTED_PRINCIPAL_RECOVERY' and review['source_id']=='L023' and review['reviewer']=='root','distinct complete acceptance')
 need(review['author_manifest_sha256']==ad['author_manifest']['sha256'] and review['native_acquisition_pages']==19 and review['remaining_principal']==[] and not review['theorem_set_equivalence'],'exact accepted edition/limits')
 rows={x['id']:x for x in source['rows']};need(len(rows)==len(source['rows'])==70 and source['all_named_numbers']==list(range(1,11)) and source['remaining_principal']==[],'all source routes')
 need(rows['L7']['disposition']=='REFUTED' and rows['T1.6']['disposition']=='ANCILLARY_PARITY_CORRECTED','source corrections preserved')
 need(all(rows[k]['disposition']=='RECOVERED_BY_UNIFORM_COMPLETION' for k in ['Abstract.infinite_geometries','S5.infinite_geometries']),'actual infinite geometry closure')
 need(rows['S5.final_problem']['disposition']=='ANSWERED_BY_ATTRIBUTED_LATER_WORK' and source['new_question_credit']==0,'later answer, no new question credit')
 need(rows['S4.other_orders']['disposition']=='ANCILLARY_EXPERIMENT_NOT_EXHAUSTED','ancillary limit')
 for k in oldpapers:
  if k not in ['status','active_source_catalogue','corrected_unmeasured_scientific_catalogue']:need(papers[k]==oldpapers[k],'old measured catalogue '+k)
 need(papers['status']=='CURRENT_MANUSCRIPTS_53_MEASURED_PLUS_THIRTEEN_CORRECTED_UNMEASURED','papers status')
 need(sc['entries'][:-6]==oldsc['entries'] and sc['acquired_dependencies']==oldsc['acquired_dependencies'],'all old manuscripts/dependencies exact')
 need(sc['original_ids']==oldsc['original_ids']+['L023'] and sc['existing_comparison_topic_count']==19 and sc['new_measurements']==0,'old comparison scope')
 need([x['physical_pages'] for x in sc['entries'][-6:]]==[3,4,3,1,5,3] and all(x['source_ids']==['L023'] and x['compiler']=='pdflatex' and not x['measured'] for x in sc['entries'][-6:]),'six exact native routes')
def controls(args):
 out=[]
 def reject(name,f):
  x=copy.deepcopy(args);f(x)
  try:semantics(*x)
  except (ValueError,KeyError,IndexError):out.append(name);return
  raise ValueError('accepted control '+name)
 reject('science counted as measurement',lambda x:x[0].update(currently_measured_originals=66))
 reject('duplicate source',lambda x:x[0]['admitted_original_ids'].append('L023'))
 reject('remove other pending source',lambda x:x[0]['accessible_pending_original_ids'].pop())
 reject('old factor changed',lambda x:x[0]['added_measurements'].append({}))
 reject('other source edited',lambda x:x[2]['entries'][0].update(title='changed'))
 reject('wrong source authors',lambda x:x[8].update(source_author_role='one author'))
 reject('free completion paper',lambda x:x[8]['physical_pages'].pop())
 reject('new factor',lambda x:x[8].update(compression_factor=1))
 reject('literal theorem equivalence',lambda x:x[8].update(theorem_sets_equivalent=True))
 reject('full formalization',lambda x:x[8].update(whole_source_formalized=True))
 reject('omit whole required code',lambda x:x[9]['whole_files'].pop())
 reject('unknown software is zero',lambda x:x[9].update(source_software_cost=0))
 reject('self-review',lambda x:x[10].update(reviewer='rewrite_termination'))
 reject('wrong accepted edition',lambda x:x[10].update(author_manifest_sha256='0'*64))
 reject('drop source row',lambda x:x[11]['rows'].pop())
 reject('restore false L7',lambda x:next(r for r in x[11]['rows'] if r['id']=='L7').update(disposition='RECOVERED'))
 reject('omit infinite completion',lambda x:next(r for r in x[11]['rows'] if r['id']=='S5.infinite_geometries').update(disposition='PENDING'))
 reject('stale final question',lambda x:next(r for r in x[11]['rows'] if r['id']=='S5.final_problem').update(disposition='UNANSWERED'))
 reject('old native deleted',lambda x:x[6]['entries'].pop(0))
 reject('new comparison topic',lambda x:x[6].update(existing_comparison_topic_count=20))
 reject('retrieval reopened',lambda x:x[0].update(source_retrieval_in_scope=True))
 return out
def root_gate(g,required):
 need(g['status']=='ROOT_ACCEPTED_SCIENCE66_PUBLICATION' and g['source_ids']==['L023'] and g['measurements_added']==g['new_question_credit']==0,'root-only publication gate')
 paths=[x['path'] for x in g['bindings']];need(len(paths)==len(set(paths)) and required<=set(paths),'exact gate paths')
def verify(root,require_root=False):
 root=Path(root).resolve();base=load(HERE/'baseline.json');plan=load(HERE/'copy_plan.json')
 if (HERE/'manifest.json').exists():
  for x in load(HERE/'manifest.json')['exports']:bind(HERE,x)
 wrappers=load(HERE/'wrapper_routes.json')['files']
 for x in wrappers+base['protected_files']+plan['public_dependencies']:bind(root,x)
 routes={x['study_path']:x for x in plan['files']};need(len(routes)==len(plan['files'])==94,'complete payload')
 for x in plan['files']:
  n=x['public_path'];need(not n.endswith('.md') and not any(y in PurePosixPath(n).parts for y in ['sources','private_source','fonts','rasters']),'no primary export');bind(root,dict(path=n,bytes=x['bytes'],sha256=x['sha256']))
 for p in plan['packets']:
  bind(root,p['manifest']);m=load(root/p['manifest']['path']);need(len(m['exports'])==p['exports'],'entire frozen packet')
  for x in m['exports']:
   n=str(PurePosixPath(p['study_manifest']).parent/x['path']);need(n in routes and all(routes[n][k]==x[k] for k in ['bytes','sha256']),'all manifest exports routed')
 history=load(root/AUDIT/'history_routes.json')['routes'];need(history==base['history'],'history overlay')
 for x in history.values():bind(root,x)
 old=load(root/history['audit/corpus/latest.json']['path']);c=load(root/'audit/corpus/latest.json')
 for k in ['active_catalogue','snapshot','current_science_registration']:bind(root,c[k])
 need(load(root/c['snapshot']['path'])=={k:v for k,v in c.items() if k!='snapshot'},'current snapshot')
 bind(root,base['old_catalogue']);cat=load(root/c['active_catalogue']['path']);oldcat=load(root/base['old_catalogue']['path'])
 papers=load(root/'papers/latest_catalogue.json');oldpapers=load(root/history['papers/latest_catalogue.json']['path']);need(papers['active_source_catalogue']==c['active_catalogue'],'current catalogue agreement');bind(root,papers['corrected_unmeasured_scientific_catalogue'])
 sc=load(root/papers['corrected_unmeasured_scientific_catalogue']['path']);oldsc=load(root/history['papers/catalogue_corrected_unmeasured.json']['path'])
 reg=load(root/c['current_science_registration']['path']);need(reg['source_ids']==['L023'] and reg['previous_registration']==old['current_science_registration'] and reg['measurement_originals_added']==reg['new_question_credit']==reg['new_Lean_declarations']==0,'one science-only registration');need(len(reg['admissions'])==1,'one admission');bind(root,reg['admissions'][0]);ad=load(root/reg['admissions'][0]['path'])
 for k in ['author_manifest','distinct_root_review_manifest','root_scientific_acceptance','source_map','dependency_boundary','source_ledger','retained_inputs','historical_question','program_roles']:bind(root,ad[k])
 need(ad['author_manifest']['sha256']==plan['current_pins']['corpus106_L023_complete_candidate'] and ad['distinct_root_review_manifest']['sha256']==plan['current_pins']['corpus106_L023_complete_root_review'],'exact acceptance pins')
 roles=load(root/ad['program_roles']['path']);review=load(root/SCIENCE/'root_review/review.json');source=load(root/ad['source_map']['path']);inv=load(root/SCIENCE/'author/program_inventory.json')
 need([{k:v for k,v in x.items() if k!='public_binding'} for x in roles['whole_files']]==inv['whole_files'],'all whole original roles')
 for x in roles['whole_files']:
  y=routes['corpus106_L023_complete_candidate/'+x['path']];need(x['public_binding']==dict(path=y['public_path'],bytes=y['bytes'],sha256=y['sha256']),'actual raw route');bind(root,x['public_binding'])
 h=load(root/ad['historical_question']['path']);need(h['authors']==['Dimitri Leemans','Klara Stokes','Philippe Tranchida'] and not h['proof_premise_of_completion'] and h['new_question_credit']==0,'precise later answer')
 need(ad['historical_answer_public_bindings']==plan['public_dependencies'],'historical result routes')
 args=[c,old,cat,oldcat,papers,oldpapers,sc,oldsc,ad,roles,review,source];semantics(*args);tests=controls(args)
 from pypdf import PdfReader
 for x in sc['entries'][-6:]:
  need(re.search(r'\\title\{([^{}]+)\}',(root/x['tex']).read_text()).group(1)==x['title'],'literal title');need(len(PdfReader(root/x['pdf']).pages)==x['physical_pages'] and x['admission']==reg['admissions'][0],'whole native/admission')
 actual={n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest() for n in ast.parse((root/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name!='main'}
 need(len(base['old_nonmain_ASTs'])==157 and all(actual.get(k)==v for k,v in base['old_nonmain_ASTs'].items()),'157 prior functions exact')
 t=(root/'README.rst').read_text();p=(root/'audit/protocol.tex').read_text()
 for x in ['66 accessible originals','53 are measured and thirteen','39 await mathematical recovery','L023 guide','Leemans, Stokes and Tranchida','Conjecture 1.1 remains unanswered']:need(x in t,'current reader '+x)
 need('106=66' in p and 'recoveries}+39' in p and 'Of the 66 corrected recoveries, 53' in p,'current protocol partition')
 links=0
 for n in ['README.rst','audit/completion.rst',NATIVE+'/PUBLICATION.rst']:
  for x in re.findall(r'<([^<>\n]+)>`_',(root/n).read_text()):
   if re.match(r'\w+://',x):continue
   need((root/PurePosixPath(n).parent/x).exists(),'local link '+x);links+=1
 required={x['path'] for x in wrappers}|{x['public_path'] for x in plan['files'] if x['public_path'].startswith(NATIVE+'/')}|{AUDIT+'/publication_plan/manifest.json','scripts/verify_snapshot.py'}
 if require_root:
  g=load(root/AUDIT/'root_integration.json');root_gate(g,required)
  for x in g['bindings']:bind(root,x)
 return dict(status='PASS_SCIENCE66_PUBLICATION_ROUTES',publication_status='ROOT_ACCEPTED' if require_root else 'ROOT_PUBLICATION_NOT_ADJUDICATED',counts=dict(active=106,corrected_recoveries=66,measured=53,unmeasured=13,mathematical_pending=39,editorial=1,archived=55,comparison_topics=19),logical_payload_routes=94,complete_frozen_packets=2,other_originals_preserved=105,old_verifier_functions_preserved=157,new_native_pages=[3,4,3,1,5,3],new_factors=0,checked_links=links,controls=tests,required_root_gate_paths=sorted(required))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',required=True,type=Path);p.add_argument('--out',type=Path);p.add_argument('--require-root',action='store_true');a=p.parse_args();r=verify(a.repo,a.require_root)
 if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r))
