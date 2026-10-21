"""Science67 registration guard. Accepted mathematics is not rerun here."""
from pathlib import Path,PurePosixPath
import argparse,ast,copy,hashlib,json,re
HERE=Path(__file__).resolve().parent;AUDIT='audit/science67/v1';SCIENCE='audit/recoveries/L031/v1';NATIVE='papers/recoveries/L031/v1';AUTHOR='corpus106_L031_recovery'
def need(x,m):
 if not x:raise ValueError('SCIENCE67: '+m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(root,r):
 p=PurePosixPath(r['path']);need(not p.is_absolute() and '..' not in p.parts,'safe path');f=root/p
 need(f.is_file() and f.stat().st_size==r['bytes'] and sha(f)==r['sha256'],'binding '+r['path'])
def semantics(c,old,cat,oldcat,papers,oldpapers,sc,oldsc,ad,roles,source,contract):
 need(tuple(c[k] for k in ['originals','admitted_principal_originals','currently_measured_originals','accessible_pending_complete_recovery','editorial_originals','archived_unavailable_originals'])==(106,67,53,38,1,55),'partition')
 need(len(c['admitted_original_ids'])==len(set(c['admitted_original_ids']))==67 and set(c['admitted_original_ids'])==set(old['admitted_original_ids'])|{'L031'},'only L031 added')
 need(len(c['accessible_pending_original_ids'])==38 and set(c['accessible_pending_original_ids'])==set(old['accessible_pending_original_ids'])-{'L031'},'pending subtraction')
 need(c['measurement_pending_original_ids']==c['scientific_unmeasured_original_ids']==sorted(old['measurement_pending_original_ids']+['L031']) and len(c['measurement_pending_original_ids'])==14,'14 unmeasured')
 for k in ['measured_original_ids','added_measurements','current_topic_replacements','historical_admitted_ids','active_original_ids','archived_original_ids','editorial_original_ids','editorial_factor','source_retrieval_in_scope','all_original_proofs_recovered','all_conjectures_resolved']:need(c[k]==old[k],'unchanged '+k)
 parts=[set(c['admitted_original_ids']),set(c['accessible_pending_original_ids']),set(c['editorial_original_ids'])];need(sum(map(len,parts))==106 and set.union(*parts)==set(c['active_original_ids']),'complete partition')
 need(c['added_admissions']==old['added_admissions']+[c['current_science_registration']],'one registration')
 before={r['original_id']:r for r in oldcat['entries']};after={r['original_id']:r for r in cat['entries']};need(len(after)==len(cat['entries'])==106 and before.keys()==after.keys(),'same roster')
 need(all(before[k]==after[k] for k in before if k!='L031'),'105 other original records')
 for k in before['L031']:
  if k not in ['current_principal_recovery','next_obligation']:need(before['L031'][k]==after['L031'][k],'unchanged source/history '+k)
 r=after['L031']['current_principal_recovery'];need(r['historical_admission_evidence']==before['L031']['current_principal_recovery'] and r['principal_contract_admitted'] and not r['measured'] and r['compression_factor'] is None,'corrected unmeasured row')
 need(ad['source_ids']==['L031'] and ad['principal_originals_added']==1 and ad['source_author_role']=='P. A. Brooksbank, J. T. Ferrara and D. Leemans; focal-group-authored source.','one original/authors')
 need(ad['physical_pages']==[5,3,5,2,2,2,4] and len(ad['whole_scientific_manuscripts'])==7,'whole23-page acquisition')
 need((ad['source_pages'],ad['source_routes'],ad['principal_targets'])==(12,57,4) and ad['finite_premises']==[],'whole contract')
 need(not ad['measured'] and not ad['comparison_topic_created'] and not ad['current_measurements_changed'] and ad['compression_factor'] is ad['software_inclusive_factor'] is None,'no measurement')
 need(ad['new_question_credit']==ad['new_Lean_declarations']==0 and not ad['whole_source_formalized'] and not ad['theorem_sets_equivalent'],'qualified scope')
 need(len(roles['whole_executable_files'])==5 and sum(x['role']=='optional_validation' for x in roles['whole_executable_files'])==1 and sum(x['role']=='operational_current' for x in roles['whole_executable_files'])==1 and sum(x['role']=='operational_historical_review' for x in roles['whole_executable_files'])==3,'all whole executable roles')
 need(roles['required_mathematical_programs']==roles['required_mathematical_data']==roles['formal_files']==[],'no finite/formal premise')
 need(roles['historical_source_software_cost'] is roles['source_software_cost'] is roles['external_proof_cost'] is roles['software_inclusive_factor'] is roles['measurement'] is None,'unknown costs')
 rr=source['dispositions'];rows={x['id']:x for x in rr};need(len(rows)==len(rr)==57 and source['source_pages']==12 and source['corrected_principal_contract_not_literal_equivalence'],'all source routes')
 for k in ['Theorem1.4.binary','Proposition3.3.binary']:need(rows[k]['status']=='CORRECTED_FALSE_SOURCE_CLAUSE','binary correction '+k)
 need(rows['Section6.intermediateType']['status']=='CORRECTED_SOURCE_IDENTIFICATION' and rows['Corollary1.5.typeSelection']['status']=='CORRECTED_PROOF_ROUTE','other corrections')
 need(all(rows[k]['status']=='SOURCE_RECORDED_QUESTION' for k in ['Section7.binaryOtherGenerators','Section7.derivedOrthogonal','Section7.PSL']),'source questions retained')
 need(contract['source_id']=='L031' and len(contract['principal_targets'])==4 and contract['mathematical_gap_in_principal_contract'] is None and contract['new_question_credit']==contract['new_formal_declarations']==0,'principal closure')
 for k in oldpapers:
  if k not in ['status','active_source_catalogue','corrected_unmeasured_scientific_catalogue']:need(papers[k]==oldpapers[k],'old measured catalogue '+k)
 need(papers['status']=='CURRENT_MANUSCRIPTS_53_MEASURED_PLUS_FOURTEEN_CORRECTED_UNMEASURED','papers status')
 need(sc['entries'][:-7]==oldsc['entries'] and sc['acquired_dependencies']==oldsc['acquired_dependencies'],'old manuscripts exact')
 need(sc['original_ids']==oldsc['original_ids']+['L031'] and sc['existing_comparison_topic_count']==19 and sc['new_measurements']==0,'old comparison scope')
 new=sc['entries'][-7:];need([x['physical_pages'] for x in new]==[5,3,5,2,2,2,4] and all(x['source_ids']==['L031'] and x['compiler']=='pdflatex' and not x['measured'] for x in new),'seven full native routes')
 need(sum(x['existing_public_dependency'] for x in new)==1 and new[-1]['pdf']=='papers/recoveries/L011/v1/low_dimension_obstructions.pdf','whole existing L011 route')
def controls(args):
 out=[]
 def reject(name,f):
  x=copy.deepcopy(args);f(x)
  try:semantics(*x)
  except (ValueError,KeyError,IndexError):out.append(name);return
  raise ValueError('accepted control '+name)
 reject('science as measurement',lambda x:x[0].update(currently_measured_originals=67))
 reject('duplicate original',lambda x:x[0]['admitted_original_ids'].append('L031'))
 reject('remove other pending',lambda x:x[0]['accessible_pending_original_ids'].pop())
 reject('change old factor boundary',lambda x:x[0]['added_measurements'].append({}))
 reject('edit another source',lambda x:x[2]['entries'][0].update(title='changed'))
 reject('wrong source author',lambda x:x[8].update(source_author_role='one author'))
 reject('free acquired paper',lambda x:x[8]['physical_pages'].pop())
 reject('new factor',lambda x:x[8].update(compression_factor=1))
 reject('literal equivalence',lambda x:x[8].update(theorem_sets_equivalent=True))
 reject('full formalization',lambda x:x[8].update(whole_source_formalized=True))
 reject('drop whole driver',lambda x:x[9]['whole_executable_files'].pop())
 reject('optional as required',lambda x:x[9]['required_mathematical_programs'].append('oracle.py'))
 reject('source software zero',lambda x:x[9].update(source_software_cost=0))
 reject('drop disposition',lambda x:x[10]['dispositions'].pop())
 reject('restore binary theorem',lambda x:next(r for r in x[10]['dispositions'] if r['id']=='Theorem1.4.binary').update(status='RECOVERED'))
 reject('restore binary intersection',lambda x:next(r for r in x[10]['dispositions'] if r['id']=='Proposition3.3.binary').update(status='RECOVERED'))
 reject('wrong literal type',lambda x:next(r for r in x[10]['dispositions'] if r['id']=='Section6.intermediateType').update(status='RECOVERED'))
 reject('primitive prescription certified',lambda x:next(r for r in x[10]['dispositions'] if r['id']=='Corollary1.5.typeSelection').update(status='RECOVERED'))
 reject('question solved',lambda x:next(r for r in x[10]['dispositions'] if r['id']=='Section7.PSL').update(status='RECOVERED'))
 reject('drop principal target',lambda x:x[11]['principal_targets'].pop())
 reject('old native deleted',lambda x:x[6]['entries'].pop(0))
 reject('new comparison topic',lambda x:x[6].update(existing_comparison_topic_count=20))
 reject('free L011',lambda x:x[6]['entries'][-1].update(existing_public_dependency=False))
 reject('retrieval reopened',lambda x:x[0].update(source_retrieval_in_scope=True))
 return out
def acceptance_semantics(r,ad):
 need(r['status']=='ACCEPTED_COMPLETE_CORRECTED_PRINCIPAL_RECOVERY' and r['source_id']=='L031' and r['reviewer']=='root','distinct whole acceptance')
 need(r['author_manifest_sha256']==ad['author_manifest']['sha256'] and r['remaining_principal']==[],'exact accepted edition')
 need(r['source_dispositions']==57 and r['principal_targets']==4 and r['native_acquisition_pages']==23,'accepted full scope')
 need(not r['theorem_set_equivalence'] and r['new_question_credit']==r['new_formal_credit']==0 and r['new_factor'] is None,'acceptance limits')
 need(r['root_authored_components_distinctly_reviewed']==['binary_boundary','binary_exclusion','rank_bound'] and r['required_mathematical_programs']==[],'distinct inherited roles')
def acceptance_controls(r,ad):
 tests=[]
 for name,key,value in [('self-review','reviewer','enumeration_volume'),('wrong accepted edition','author_manifest_sha256','0'*64),('unresolved principal','remaining_principal',['P1']),('accepted measurement','new_factor',1),('missing component review','root_authored_components_distinctly_reviewed',[])]:
  x=copy.deepcopy(r);x[key]=value
  try:acceptance_semantics(x,ad)
  except (ValueError,KeyError):tests.append(name)
  else:raise ValueError('acceptance control accepted '+name)
 return tests
def root_gate(g,required):
 need(g['status']=='ROOT_ACCEPTED_SCIENCE67_PUBLICATION' and g['source_ids']==['L031'] and g['measurements_added']==g['new_question_credit']==0,'root-only publication gate')
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
 need(plan['packets'][0]['exports']==69,'whole current science')
 history=load(root/AUDIT/'history_routes.json')['routes'];need(history==base['history'],'history overlay')
 for x in history.values():bind(root,x)
 old=load(root/history['audit/corpus/latest.json']['path']);c=load(root/'audit/corpus/latest.json')
 for k in ['active_catalogue','snapshot','current_science_registration']:bind(root,c[k])
 need(load(root/c['snapshot']['path'])=={k:v for k,v in c.items() if k!='snapshot'},'current snapshot')
 bind(root,base['old_catalogue']);cat=load(root/c['active_catalogue']['path']);oldcat=load(root/base['old_catalogue']['path'])
 papers=load(root/'papers/latest_catalogue.json');oldpapers=load(root/history['papers/latest_catalogue.json']['path']);need(papers['active_source_catalogue']==c['active_catalogue'],'current catalogue agreement');bind(root,papers['corrected_unmeasured_scientific_catalogue'])
 sc=load(root/papers['corrected_unmeasured_scientific_catalogue']['path']);oldsc=load(root/history['papers/catalogue_corrected_unmeasured.json']['path'])
 reg=load(root/c['current_science_registration']['path']);need(reg['source_ids']==['L031'] and reg['previous_registration']==old['current_science_registration'] and reg['measurement_originals_added']==reg['new_question_credit']==reg['new_Lean_declarations']==0,'one science registration');need(len(reg['admissions'])==1,'one admission');bind(root,reg['admissions'][0]);ad=load(root/reg['admissions'][0]['path'])
 for k in ['author_manifest','distinct_root_review_manifest','root_scientific_acceptance','source_map','source_contract','dependency_boundary','migration','program_roles']:bind(root,ad[k])
 need(ad['author_manifest']['sha256']==plan['current_pins'][AUTHOR] and ad['distinct_root_review_manifest']['sha256']==plan['current_pins'][plan['root_review_directory']],'acceptance pins')
 acceptance=load(HERE/'acceptance_binding.json');need(acceptance['root_review_manifest']==ad['distinct_root_review_manifest'] and acceptance['author_manifest_sha256']==ad['author_manifest']['sha256'] and acceptance['distinct_whole_acceptance'],'exact root acceptance overlay')
 for x in acceptance['public_review_records']:bind(root,x)
 roles=load(root/ad['program_roles']['path']);source=load(root/ad['source_map']['path']);contract=load(root/ad['source_contract']['path']);inv=load(root/SCIENCE/'author/program_inventory.json')
 need([{k:v for k,v in x.items() if k!='public_binding'} for x in roles['whole_executable_files']]==inv['whole_executable_files'],'all original whole roles')
 for x in roles['whole_executable_files']:
  y=routes[AUTHOR+'/'+x['path']];need(x['public_binding']==dict(path=y['public_path'],bytes=y['bytes'],sha256=y['sha256']),'raw route');bind(root,x['public_binding'])
 args=[c,old,cat,oldcat,papers,oldpapers,sc,oldsc,ad,roles,source,contract];semantics(*args);tests=controls(args)
 review=load(root/SCIENCE/'root_review/review.json');acceptance_semantics(review,ad);tests+=acceptance_controls(review,ad)
 from pypdf import PdfReader
 for x in sc['entries'][-7:]:
  need(re.search(r'\\title\{([^{}]+)\}',(root/x['tex']).read_text()).group(1)==x['title'],'literal title');need(len(PdfReader(root/x['pdf']).pages)==x['physical_pages'] and x['admission']==reg['admissions'][0],'native/admission')
 actual={n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest() for n in ast.parse((root/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name!='main'}
 need(len(base['old_nonmain_ASTs'])==159 and all(actual.get(k)==v for k,v in base['old_nonmain_ASTs'].items()),'159 prior functions exact')
 t=(root/'README.rst').read_text();p=(root/'audit/protocol.tex').read_text()
 for x in ['67 accessible originals','53 are measured and fourteen','38 await mathematical recovery','L031 guide','Conjecture 1.1 remains unanswered']:need(x in t,'current reader '+x)
 need('106=67' in p and 'recoveries}+38' in p and 'Of the 67 corrected recoveries, 53' in p,'current protocol')
 need('L044 and L096\nremain pending' not in (root/'audit/completion.rst').read_text(),'stale L096 corrected')
 links=0
 for n in ['README.rst','audit/completion.rst',NATIVE+'/PUBLICATION.rst']:
  for x in re.findall(r'<([^<>\n]+)>`_',(root/n).read_text()):
   if re.match(r'\w+://',x):continue
   need((root/PurePosixPath(n).parent/x).exists(),'local link '+x);links+=1
 native_paths={x[k] for x in sc['entries'][-7:] for k in ['tex','pdf']}
 required={x['path'] for x in wrappers}|native_paths|{AUDIT+'/publication_plan/manifest.json','scripts/verify_snapshot.py'}
 if require_root:
  g=load(root/AUDIT/'root_integration.json');root_gate(g,required)
  for x in g['bindings']:bind(root,x)
 return dict(status='PASS_SCIENCE67_PUBLICATION_ROUTES',publication_status='ROOT_ACCEPTED' if require_root else 'ROOT_PUBLICATION_NOT_ADJUDICATED',counts=dict(active=106,corrected_recoveries=67,measured=53,unmeasured=14,mathematical_pending=38,editorial=1,archived=55,comparison_topics=19),logical_payload_routes=len(plan['files']),complete_frozen_packets=2,other_originals_preserved=105,old_verifier_functions_preserved=159,new_native_pages=[5,3,5,2,2,2,4],new_factors=0,checked_links=links,controls=tests,required_root_gate_paths=sorted(required))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',required=True,type=Path);p.add_argument('--out',type=Path);p.add_argument('--require-root',action='store_true');a=p.parse_args();r=verify(a.repo,a.require_root)
 if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r))
