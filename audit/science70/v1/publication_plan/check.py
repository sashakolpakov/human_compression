"""Science70 registration guard. Accepted mathematics is not rerun here."""
from pathlib import Path,PurePosixPath
import argparse,ast,copy,hashlib,json,re
HERE=Path(__file__).resolve().parent;AUDIT='audit/science70/v1';SCIENCE='audit/recoveries/N011/v1';NATIVE='papers/recoveries/N011/v1';AUTHOR='corpus106_N011_recovery'
def need(x,m):
 if not x:raise ValueError('SCIENCE70: '+m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(root,r):
 p=PurePosixPath(r['path']);need(not p.is_absolute() and '..' not in p.parts,'safe path');f=root/p
 need(f.is_file() and f.stat().st_size==r['bytes'] and sha(f)==r['sha256'],'binding '+r['path'])
def semantics(c,old,cat,oldcat,papers,oldpapers,sc,oldsc,ad,roles,source,contract):
 need(tuple(c[k]for k in ['originals','admitted_principal_originals','currently_measured_originals','accessible_pending_complete_recovery','editorial_originals','archived_unavailable_originals'])==(106,70,53,35,1,55),'partition')
 need(len(c['admitted_original_ids'])==len(set(c['admitted_original_ids']))==70 and set(c['admitted_original_ids'])==set(old['admitted_original_ids'])|{'N011'},'only N011 added')
 need(len(c['accessible_pending_original_ids'])==35 and set(c['accessible_pending_original_ids'])==set(old['accessible_pending_original_ids'])-{'N011'},'pending subtraction')
 need(c['measurement_pending_original_ids']==c['scientific_unmeasured_original_ids']==sorted(old['measurement_pending_original_ids']+['N011'])and len(c['measurement_pending_original_ids'])==17,'17 unmeasured')
 for k in ['measured_original_ids','added_measurements','current_topic_replacements','historical_admitted_ids','active_original_ids','archived_original_ids','editorial_original_ids','editorial_factor','source_retrieval_in_scope','all_original_proofs_recovered','all_conjectures_resolved']:need(c[k]==old[k],'unchanged '+k)
 parts=[set(c['admitted_original_ids']),set(c['accessible_pending_original_ids']),set(c['editorial_original_ids'])];need(sum(map(len,parts))==106 and set.union(*parts)==set(c['active_original_ids']),'complete partition')
 need(c['added_admissions']==old['added_admissions']+[c['current_science_registration']],'one registration')
 before={r['original_id']:r for r in oldcat['entries']};after={r['original_id']:r for r in cat['entries']};need(len(after)==len(cat['entries'])==106 and before.keys()==after.keys(),'same roster')
 need(all(before[k]==after[k]for k in before if k!='N011'),'105 other source records')
 for k in before['N011']:
  if k not in ['current_principal_recovery','next_obligation']:need(before['N011'][k]==after['N011'][k],'same source history '+k)
 r=after['N011']['current_principal_recovery'];need(r['historical_admission_evidence']==before['N011']['current_principal_recovery']and r['principal_contract_admitted']and not r['measured']and r['compression_factor']is None,'accepted unmeasured original')
 need(ad['status']=='ROOT_ACCEPTED_SCIENCE_PUBLIC_INTEGRATION_REQUIRES_SCIENCE70_GATE'and ad['source_ids']==['N011']and ad['principal_originals_added']==1 and ad['source_authors']==['Irina A. Markovskaya','Yakov N. Nuzhin'],'complete authors')
 need(ad['physical_pages']==[2,7]and len(ad['whole_scientific_manuscripts'])==2,'two complete papers')
 need((ad['source_pages'],ad['source_routes'],ad['source_table_rows'])==(13,57,12),'complete contract')
 need(ad['finite_premises']==ad['required_mathematical_data']==[],'no invented finite premise')
 need(not ad['measured']and not ad['comparison_topic_created']and not ad['current_measurements_changed']and ad['compression_factor']is ad['software_inclusive_factor']is None,'no factor')
 need(ad['new_question_credit']==ad['new_Lean_declarations']==0 and not ad['whole_source_formalized']and not ad['theorem_sets_equivalent'],'scope limits')
 need(roles['source_software_cost']is roles['external_proof_cost']is roles['measurement']is None,'unknown costs')
 need([(x['path'],x['role'])for x in roles['files']]==[('symbolic_check.py','OPTIONAL_VALIDATION'),('check.py','OPERATIONAL_REPLAY')],'whole program roles')
 need(all(x['whole_file']and x['no_proof_premise']for x in roles['files'])and roles['required_programs']==roles['required_mathematical_data']==[] and roles['optional_result']=='symbolic_report.json','optional scope')
 need(source['disposition_count']==len(source['rows'])==len({x['id']for x in source['rows']})==57 and source['named_results']==dict(theorems=2,lemmas=11,tables=2,table_rows=12),'all source routes')
 need(source['remaining_principal_obligations']==[]and source['retained_inputs_are_not_reproved']and not source['literal_theorem_set_equivalence'],'source limits')
 need(contract['source_id']=='N011'and contract['full_original_pages']==13 and contract['authors']==ad['source_authors'],'source scope')
 need(contract['new_original_credit']==contract['new_conjecture_credit']==contract['new_lean']==contract['new_measurement']==0 and not contract['full_formalization'],'author qualification')
 need(contract['required_new_finite_programs']==[]and contract['optional_validation']==['symbolic_check.py']and len(contract['full_principal_contract'])==5 and len(contract['source_qualifications'])==7,'complete principal boundary')
 for k in oldpapers:
  if k not in ['status','active_source_catalogue','corrected_unmeasured_scientific_catalogue']:need(papers[k]==oldpapers[k],'old measured catalogue '+k)
 need(papers['status']=='CURRENT_MANUSCRIPTS_53_MEASURED_PLUS_SEVENTEEN_CORRECTED_UNMEASURED','papers status')
 need(sc['entries'][:-2]==oldsc['entries']and sc['acquired_dependencies']==oldsc['acquired_dependencies'],'old scientific manuscripts')
 need(sc['original_ids']==oldsc['original_ids']+['N011']and sc['existing_comparison_topic_count']==19 and sc['new_measurements']==0,'old comparison scope')
 new=sc['entries'][-2:];need([x['physical_pages']for x in new]==[2,7]and all(x['source_ids']==['N011']and x['compiler']=='pdflatex'and not x['measured']for x in new),'two native routes')
 need(not any(x['existing_public_dependency']for x in new),'both whole current papers')
def controls(args):
 out=[]
 def reject(name,f):
  x=copy.deepcopy(args);f(x)
  try:semantics(*x)
  except(ValueError,KeyError,IndexError):out.append(name);return
  raise ValueError('accepted control '+name)
 changes=[('science as measurement',lambda x:x[0].update(currently_measured_originals=70)),('duplicate original',lambda x:x[0]['admitted_original_ids'].append('N011')),('remove another pending',lambda x:x[0]['accessible_pending_original_ids'].pop()),('change old factor boundary',lambda x:x[0]['added_measurements'].append({})),('edit another source',lambda x:x[2]['entries'][0].update(title='changed')),('missing coauthor',lambda x:x[8]['source_authors'].pop()),('free common proof',lambda x:x[8]['physical_pages'].pop()),('new factor',lambda x:x[8].update(compression_factor=1)),('literal equivalence',lambda x:x[8].update(theorem_sets_equivalent=True)),('full formalization',lambda x:x[8].update(whole_source_formalized=True)),('validation becomes premise',lambda x:x[8]['finite_premises'].append({})),('source software zero',lambda x:x[9].update(source_software_cost=0)),('drop driver',lambda x:x[9]['files'].pop()),('drop optional result',lambda x:x[9].update(optional_result=None)),('drop disposition',lambda x:x[10]['rows'].pop()),('old native deleted',lambda x:x[6]['entries'].pop(0)),('new comparison topic',lambda x:x[6].update(existing_comparison_topic_count=20)),('free application',lambda x:x[6]['entries'][-1].update(existing_public_dependency=True)),('retrieval reopened',lambda x:x[0].update(source_retrieval_in_scope=True)),('missing parameter branch',lambda x:x[11]['full_principal_contract'].pop()),('discard source correction',lambda x:x[11]['source_qualifications'].pop()),('optional required',lambda x:x[11]['required_new_finite_programs'].append('symbolic_check.py')),('unresolved principal',lambda x:x[10]['remaining_principal_obligations'].append('P1'))]
 for n,f in changes:reject(n,f)
 return out
def acceptance_semantics(r,ad):
 need(r['status']=='ACCEPTED_COMPLETE_CORRECTED_PRINCIPAL_RECOVERY'and r['reviewer']=='root'and r['author']=='rewrite_termination','distinct whole acceptance')
 need(r['author_manifest_sha256']==ad['author_manifest']['sha256']and r['author_manifest']=='corpus106_N011_recovery/manifest.json','exact accepted edition')
 need(r['eligible_new_original_credit']==1 and r['public_admission_separate'],'accepted source scope')
 need(r['new_question_credit']==r['new_formal_credit']==r['new_measurement']==0,'acceptance limits')
def acceptance_controls(r,ad):
 tests=[]
 for name,key,value in [('self-review','reviewer','rewrite_termination'),('wrong accepted edition','author_manifest_sha256','0'*64),('wrong original','author_manifest','corpus106_L018_complete_candidate/manifest.json'),('accepted measurement','new_measurement',1),('missing separate registration','public_admission_separate',False)]:
  x=copy.deepcopy(r);x[key]=value
  try:acceptance_semantics(x,ad)
  except(ValueError,KeyError):tests.append(name)
  else:raise ValueError('acceptance control accepted '+name)
 return tests
def root_gate(g,required):
 need(g['status']=='ROOT_ACCEPTED_SCIENCE70_PUBLICATION' and g['source_ids']==['N011'] and g['measurements_added']==g['new_question_credit']==0,'root-only publication gate')
 paths=[x['path'] for x in g['bindings']];need(len(paths)==len(set(paths)) and required<=set(paths),'exact root gate paths')
def verify(root,require_root=False):
 root=Path(root).resolve();base=load(HERE/'baseline.json');plan=load(HERE/'copy_plan.json')
 if (HERE/'manifest.json').exists():
  for x in load(HERE/'manifest.json')['exports']:bind(HERE,x)
 wrappers=load(HERE/'wrapper_routes.json')['files']
 for x in wrappers+base['protected_files']+plan['public_dependencies']:bind(root,x)
 routes={x['study_path']:x for x in plan['files']};need(len(routes)==len(plan['files']) and len(plan['packets'])==2,'complete payload')
 for x in plan['files']:
  n=x['public_path'];need(not n.endswith('.md') and not any(y in PurePosixPath(n).parts for y in ['sources','private_source','fonts','rasters']),'no primary export');bind(root,dict(path=n,bytes=x['bytes'],sha256=x['sha256']))
 for p in plan['packets']:
  bind(root,p['manifest']);m=load(root/p['manifest']['path']);need(len(m['exports'])==p['exports'],'entire frozen packet')
  for x in m['exports']:
   n=str(PurePosixPath(p['study_manifest']).parent/x['path']);need(n in routes and all(routes[n][k]==x[k] for k in ['bytes','sha256']),'all exports routed')
 need(plan['packets'][0]['exports']==16,'whole current science')
 history=load(root/AUDIT/'history_routes.json')['routes'];need(history==base['history'],'history overlay')
 for x in history.values():bind(root,x)
 old=load(root/history['audit/corpus/latest.json']['path']);c=load(root/'audit/corpus/latest.json')
 for k in ['active_catalogue','snapshot','current_science_registration']:bind(root,c[k])
 need(load(root/c['snapshot']['path'])=={k:v for k,v in c.items() if k!='snapshot'},'current snapshot')
 bind(root,base['old_catalogue']);cat=load(root/c['active_catalogue']['path']);oldcat=load(root/base['old_catalogue']['path'])
 papers=load(root/'papers/latest_catalogue.json');oldpapers=load(root/history['papers/latest_catalogue.json']['path']);need(papers['active_source_catalogue']==c['active_catalogue'],'current catalogue agreement');bind(root,papers['corrected_unmeasured_scientific_catalogue'])
 sc=load(root/papers['corrected_unmeasured_scientific_catalogue']['path']);oldsc=load(root/history['papers/catalogue_corrected_unmeasured.json']['path'])
 reg=load(root/c['current_science_registration']['path']);need(reg['source_ids']==['N011'] and reg['previous_registration']==old['current_science_registration'] and reg['measurement_originals_added']==reg['new_question_credit']==reg['new_Lean_declarations']==0,'one science registration');need(len(reg['admissions'])==1,'one admission');bind(root,reg['admissions'][0]);ad=load(root/reg['admissions'][0]['path'])
 for k in ['author_manifest','distinct_root_review_manifest','root_scientific_acceptance','source_map','source_contract','dependency_boundary','program_roles']:bind(root,ad[k])
 need(ad['author_manifest']['sha256']==plan['current_pins'][AUTHOR] and ad['distinct_root_review_manifest']['sha256']==plan['current_pins'][plan['root_review_directory']],'acceptance pins')
 acceptance=load(HERE/'acceptance_binding.json');need(acceptance['root_review_manifest']==ad['distinct_root_review_manifest'] and acceptance['author_manifest_sha256']==ad['author_manifest']['sha256'] and acceptance['distinct_whole_acceptance'],'exact root acceptance overlay')
 for x in acceptance['public_review_records']:bind(root,x)
 roles=load(root/ad['program_roles']['path']);source=load(root/ad['source_map']['path']);contract=load(root/ad['source_contract']['path']);inv=load(root/SCIENCE/'author/program_inventory.json')
 need(all(roles[k]==v for k,v in inv.items()),'exact entire inherited role inventory')
 for x in roles['public_bindings']:bind(root,x)
 for x in ad['whole_scientific_manuscripts']+ad['finite_premises']+ad['required_mathematical_data']:bind(root,x)
 def logical_binding(n):
  x=routes[AUTHOR+'/'+n];return dict(path=x['public_path'],bytes=x['bytes'],sha256=x['sha256'])
 need(ad['finite_premises']==[],'no required program routes')
 need(ad['required_mathematical_data']==[],'no required data routes')
 native=load(root/SCIENCE/'author/native.json');need(ad['whole_scientific_manuscripts']==[logical_binding(x['pdf'])for x in native['documents']],'exact whole paper routes')
 retained=load(root/ad['dependency_boundary']['path']);need(len(retained['inputs'])==6 and all(x['external_complete_proof_cost']=='UNKNOWN'for x in retained['inputs']),'all retained input costs unknown')
 args=[c,old,cat,oldcat,papers,oldpapers,sc,oldsc,ad,roles,source,contract];semantics(*args);tests=controls(args)
 review=load(root/SCIENCE/'root_review/review.json');acceptance_semantics(review,ad);tests+=acceptance_controls(review,ad)
 from pypdf import PdfReader
 for x in sc['entries'][-2:]:
  need(re.search(r'\\title\{([^{}]+)\}',(root/x['tex']).read_text()).group(1)==x['title'],'literal title');need(len(PdfReader(root/x['pdf']).pages)==x['physical_pages'] and x['admission']==reg['admissions'][0],'native/admission')
 actual={n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest() for n in ast.parse((root/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name!='main'}
 need(len(base['old_nonmain_ASTs'])==165 and all(actual.get(k)==v for k,v in base['old_nonmain_ASTs'].items()),'165 prior functions exact')
 t=(root/'README.rst').read_text();p=(root/'audit/protocol.tex').read_text()
 for x in ['70 accessible originals','53 are measured and seventeen','35 await mathematical recovery','N011 guide','Conjecture 1.1 remains unanswered']:need(x in t,'current reader '+x)
 need('106=70' in p and 'recoveries}+35' in p and 'Of the 70 corrected recoveries, 53' in p,'current protocol')
 need('L044 and L096\nremain pending' not in (root/'audit/completion.rst').read_text(),'stale L096 corrected')
 links=0
 for n in ['README.rst','audit/completion.rst',NATIVE+'/PUBLICATION.rst']:
  for x in re.findall(r'<([^<>\n]+)>`_',(root/n).read_text()):
   if re.match(r'\w+://',x):continue
   need((root/PurePosixPath(n).parent/x).exists(),'local link '+x);links+=1
 native_paths={x[k] for x in sc['entries'][-2:] for k in ['tex','pdf']}
 required={x['path'] for x in wrappers}|native_paths|{AUDIT+'/publication_plan/manifest.json','scripts/verify_snapshot.py'}
 if require_root:
  g=load(root/AUDIT/'root_integration.json');root_gate(g,required)
  for x in g['bindings']:bind(root,x)
 return dict(status='PASS_SCIENCE70_PUBLICATION_ROUTES',publication_status='ROOT_ACCEPTED' if require_root else 'ROOT_PUBLICATION_NOT_ADJUDICATED',counts=dict(active=106,corrected_recoveries=70,measured=53,unmeasured=17,mathematical_pending=35,editorial=1,archived=55,comparison_topics=19),logical_payload_routes=len(plan['files']),complete_frozen_packets=2,other_originals_preserved=105,old_verifier_functions_preserved=165,new_native_pages=[2,7],new_factors=0,checked_links=links,controls=tests,required_root_gate_paths=sorted(required))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',required=True,type=Path);p.add_argument('--out',type=Path);p.add_argument('--require-root',action='store_true');a=p.parse_args();r=verify(a.repo,a.require_root)
 if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r))
