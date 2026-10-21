"""Science71 additive registration guard; no new mathematical computation."""
from pathlib import Path,PurePosixPath
import argparse,ast,copy,hashlib,json,re
P=Path(__file__).resolve().parent;AUD='audit/science71/v1';SCI='audit/recoveries/F002/v1';NAT='papers/recoveries/F002/v1'
def need(v,m):
 if not v:raise ValueError('SCIENCE71: '+m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(root,r):
 p=PurePosixPath(r['path']);need(not p.is_absolute()and'..'not in p.parts,'safe path');q=root/p
 need(q.is_file()and q.stat().st_size==r['bytes']and sha(q)==r['sha256'],'binding '+r['path'])
def semantics(c,old,cat,oldcat,sc,oldsc,ad,roles,source,scope,review,adoption):
 need(tuple(c[k]for k in ['originals','admitted_principal_originals','currently_measured_originals','accessible_pending_complete_recovery','editorial_originals','archived_unavailable_originals'])==(106,71,53,34,1,55),'partition')
 need(len(c['admitted_original_ids'])==len(set(c['admitted_original_ids']))==71 and set(c['admitted_original_ids'])==set(old['admitted_original_ids'])|{'F002'},'one new original')
 need(len(c['accessible_pending_original_ids'])==34 and set(c['accessible_pending_original_ids'])==set(old['accessible_pending_original_ids'])-{'F002'},'pending subtraction')
 need(c['measurement_pending_original_ids']==c['scientific_unmeasured_original_ids']==sorted(old['measurement_pending_original_ids']+['F002'])and len(c['measurement_pending_original_ids'])==18,'eighteen unmeasured')
 for k in ['measured_original_ids','added_measurements','current_topic_replacements','historical_admitted_ids','active_original_ids','archived_original_ids','editorial_original_ids','editorial_factor','source_retrieval_in_scope','all_original_proofs_recovered','all_conjectures_resolved']:need(c[k]==old[k],'unchanged '+k)
 need(c['added_admissions']==old['added_admissions']+[c['current_science_registration']],'one new registration')
 before={x['original_id']:x for x in oldcat['entries']};after={x['original_id']:x for x in cat['entries']};need(len(after)==len(cat['entries'])==106 and before.keys()==after.keys(),'same original roster')
 need(all(before[k]==after[k]for k in before if k!='F002'),'105 records unchanged')
 for k in before['F002']:
  if k not in ['current_principal_recovery','next_obligation']:need(before['F002'][k]==after['F002'][k],'source history '+k)
 r=after['F002']['current_principal_recovery'];need(r['historical_admission_evidence']==before['F002']['current_principal_recovery']and r['principal_contract_admitted']and not r['measured']and r['compression_factor']is None,'accepted unmeasured')
 need(ad['source_ids']==['F002']and ad['status']=='ROOT_ACCEPTED_SCIENCE_PUBLIC_INTEGRATION_REQUIRES_SCIENCE71_GATE'and ad['principal_originals_added']==1,'one scientific admission')
 need(ad['physical_pages']==[2,2]and ad['retained_acquisition_files']==380,'whole acquisition')
 need((ad['source_pages'],ad['source_routes'],ad['source_graph_rows'],ad['source_orbit_cells'])==(28,40,5,10),'source boundary')
 need(not ad['measured']and not ad['comparison_topic_created']and not ad['current_measurements_changed']and ad['compression_factor']is ad['software_inclusive_factor']is None,'no new factor')
 need(ad['new_question_credit']==ad['new_Lean_declarations']==0 and not ad['whole_source_formalized']and not ad['theorem_sets_equivalent'],'credit boundary')
 need(roles['source_software_cost']is roles['external_proof_cost']is roles['measurement']is None and roles['no_software_inclusive_factor'],'unknown costs')
 need([x['path']for x in roles['whole_files']]==['enumerate_even.g','checks.g','compare.g','source_markings.g','generated_markings.g','check.py','run.py'],'whole raw inventory')
 need(len(roles['required_programs'])==3 and len(roles['required_mathematical_data'])==2 and len(roles['operational_drivers'])==2 and len(roles['retained_public_files'])==380,'program/data roles')
 need(source['all_named_statements']==len(source['rows'])==len({x['id']for x in source['rows']})==40 and source['no_literal_theorem_set_equivalence'],'complete dispositions')
 byid={x['id']:x for x in source['rows']};need(byid['5.3']['status']=='ANCILLARY_SOURCE_PROOF_ROUTE_NOT_INDEPENDENTLY_RECOVERED'and byid['8.8']['status']=='RECOVERED_MAIN_PRINCIPAL_CONTRACT','principal/appendix boundary')
 need(scope['original_id']=='F002'and scope['principal_result']=='Theorem8.8'and scope['whole_original_credit']==scope['new_conjecture_credit']==scope['new_Lean_credit']==0 and scope['new_compression_factor']is None,'frozen author status')
 need(len(scope['retained_mathematical_premises'])==3 and scope['retained_software_premises']==['GAP exact permutation group algorithms'],'retained premises')
 need(review['status']=='ACCEPTED_COMPLETE_PRINCIPAL_CONTRACT'and review['reviewer']=='enumeration_volume'and review['new_scientific_author']=='root','distinct review roles')
 need(review['author']['manifest_sha256']==ad['author_manifest']['sha256']and review['no_literal_theorem_set_equivalence']and review['prior_roles']['reviewer_previously_authored_retained_projective_theory'],'review scope/provenance')
 need(adoption['status']=='ROOT_ADOPTS_DISTINCTLY_ACCEPTED_PRINCIPAL_RECOVERY'and adoption['original_id']=='F002'and adoption['new_scientific_author']=='root'and adoption['distinct_reviewer']=='enumeration_volume','root adoption')
 need(adoption['author_manifest']['sha256']==ad['author_manifest']['sha256']and adoption['distinct_review_manifest']['sha256']==ad['distinct_review_manifest']['sha256']and adoption['whole_original_credit']==1 and adoption['public_registration_pending'],'adoption exact scope')
 need(adoption['new_Lean_credit']==adoption['new_conjecture_credit']==0 and adoption['new_factor']is None,'adoption no extras')
 need(sc['entries'][:-2]==oldsc['entries']and sc['acquired_dependencies']==oldsc['acquired_dependencies']and sc['original_ids']==oldsc['original_ids']+['F002'],'old scientific papers')
 need(sc['existing_comparison_topic_count']==19 and sc['new_measurements']==0,'unchanged comparison topics')
 need([x['physical_pages']for x in sc['entries'][-2:]]==[2,2]and all(x['source_ids']==['F002']and x['compiler']=='pdflatex'and not x['measured']and not x['existing_public_dependency']for x in sc['entries'][-2:]),'new native routes')
def controls(args):
 changes=[('measurement inflation',lambda x:x[0].update(currently_measured_originals=71)),('duplicate original',lambda x:x[0]['admitted_original_ids'].append('F002')),('another pending removed',lambda x:x[0]['accessible_pending_original_ids'].pop()),('old measurement changed',lambda x:x[0]['added_measurements'].append({})),('other source edited',lambda x:x[2]['entries'][0].update(title='changed')),('free acquired theory',lambda x:x[6].update(retained_acquisition_files=0)),('drop common paper',lambda x:x[6]['physical_pages'].pop()),('invent factor',lambda x:x[6].update(compression_factor=1)),('literal equivalence',lambda x:x[6].update(theorem_sets_equivalent=True)),('full formal claim',lambda x:x[6].update(whole_source_formalized=True)),('source software zero',lambda x:x[7].update(source_software_cost=0)),('required program removed',lambda x:x[7]['required_programs'].pop()),('required data removed',lambda x:x[7]['required_mathematical_data'].pop()),('driver removed',lambda x:x[7]['operational_drivers'].pop()),('disposition removed',lambda x:x[8]['rows'].pop()),('appendix falsely recovered',lambda x:next(y for y in x[8]['rows']if y['id']=='5.3').update(status='RECOVERED')),('source quantifier changed',lambda x:x[9].update(principal_result='ALL_RANKS')),('self review',lambda x:x[10].update(reviewer='root')),('missing prior role',lambda x:x[10]['prior_roles'].update(reviewer_previously_authored_retained_projective_theory=False)),('wrong adoption',lambda x:x[11].update(original_id='N011')),('old native dropped',lambda x:x[4]['entries'].pop(0)),('new comparison topic',lambda x:x[4].update(existing_comparison_topic_count=20))]
 out=[]
 for name,f in changes:
  x=copy.deepcopy(args);f(x)
  try:semantics(*x)
  except(ValueError,KeyError,IndexError):out.append(name)
  else:raise ValueError('accepted control '+name)
 return out
def root_gate(g,required):
 need(g['status']=='ROOT_ACCEPTED_SCIENCE71_PUBLICATION'and g['source_ids']==['F002']and g['measurements_added']==g['new_question_credit']==0,'root publication gate')
 paths=[r['path']for r in g['bindings']];need(len(paths)==len(set(paths))and required<=set(paths),'complete root gate bindings')
def verify(root,require_root=False):
 root=Path(root).resolve();base=load(P/'baseline.json');plan=load(P/'copy_plan.json');wr=load(P/'wrapper_routes.json')['files']
 if(P/'manifest.json').exists():
  for x in load(P/'manifest.json')['exports']:bind(P,x)
 for x in wr+base['protected_files']+plan['public_dependencies']:bind(root,x)
 routes={r['study_path']:r for r in plan['files']};need(len(routes)==438 and len(plan['packets'])==3 and plan['reused_existing_public_files']==380 and plan['new_public_files']==58,'complete mapped closure')
 for r in plan['files']:
  need(not r['public_path'].endswith('.md')and not any(x in PurePosixPath(r['public_path']).parts for x in ['sources','fonts','rasters','private_source']),'private primary boundary');bind(root,dict(path=r['public_path'],bytes=r['bytes'],sha256=r['sha256']))
 for packet in plan['packets']:
  bind(root,packet['manifest']);m=load(root/packet['manifest']['path']);need(len(m['exports'])==packet['exports'],'whole packet')
  for row in m['exports']:
   key=str(PurePosixPath(packet['study_manifest']).parent/row['path']);need(key in routes and all(routes[key][k]==row[k]for k in ['bytes','sha256']),'whole export mapping')
 history=load(root/AUD/'history_routes.json')['routes'];need(history==base['history'],'historical routes')
 for r in history.values():bind(root,r)
 old=load(root/history['audit/corpus/latest.json']['path']);c=load(root/'audit/corpus/latest.json')
 for k in ['active_catalogue','snapshot','current_science_registration']:bind(root,c[k])
 need(load(root/c['snapshot']['path'])=={k:v for k,v in c.items()if k!='snapshot'},'exact snapshot');bind(root,base['old_catalogue'])
 cat=load(root/c['active_catalogue']['path']);oldcat=load(root/base['old_catalogue']['path']);papers=load(root/'papers/latest_catalogue.json');oldpapers=load(root/history['papers/latest_catalogue.json']['path'])
 for k in oldpapers:
  if k not in ['status','active_source_catalogue','corrected_unmeasured_scientific_catalogue']:need(papers[k]==oldpapers[k],'old paper field '+k)
 need(papers['active_source_catalogue']==c['active_catalogue']and papers['status']=='CURRENT_MANUSCRIPTS_53_MEASURED_PLUS_EIGHTEEN_CORRECTED_UNMEASURED','current paper routing');bind(root,papers['corrected_unmeasured_scientific_catalogue'])
 sc=load(root/papers['corrected_unmeasured_scientific_catalogue']['path']);oldsc=load(root/history['papers/catalogue_corrected_unmeasured.json']['path'])
 reg=load(root/c['current_science_registration']['path']);need(reg['source_ids']==['F002']and reg['previous_registration']==old['current_science_registration']and reg['measurement_originals_added']==reg['new_question_credit']==reg['new_Lean_declarations']==0 and len(reg['admissions'])==1,'one registration')
 bind(root,reg['admissions'][0]);ad=load(root/reg['admissions'][0]['path'])
 for k in ['author_manifest','distinct_review_manifest','root_scientific_acceptance','source_map','source_contract','dependency_boundary','program_roles','retained_common','retained_application']:bind(root,ad[k])
 acceptance=load(P/'acceptance_binding.json');need(acceptance['author_manifest']==ad['author_manifest']and acceptance['distinct_review_manifest']==ad['distinct_review_manifest']and acceptance['root_adoption_manifest']==ad['root_scientific_acceptance'],'complete acceptance chain')
 roles=load(root/ad['program_roles']['path']);inv=load(root/SCI/'author/program_inventory.json');need(all(roles[k]==v for k,v in inv.items()),'all inherited roles')
 for x in roles['public_bindings']+roles['retained_public_files']+ad['whole_scientific_manuscripts']+ad['finite_premises']+ad['required_mathematical_data']:bind(root,x)
 need(ad['finite_premises']==roles['required_programs']and ad['required_mathematical_data']==roles['required_mathematical_data'],'required code/data routing')
 retained=load(root/ad['dependency_boundary']['path']);need(len(retained['whole_files'])==380,'entire dependency count')
 for x in retained['whole_files']:
  rr=routes[plan['author_directory']+'/'+x['path']];need(rr['transport']=='EXISTING_PUBLIC'and all(rr[k]==x[k]for k in ['bytes','sha256']),'paid whole dependency')
 source=load(root/ad['source_map']['path']);scope=load(root/ad['source_contract']['path']);review=load(root/SCI/'independent_review/review.json');adoption=load(root/SCI/'root_adoption/adoption.json')
 args=[c,old,cat,oldcat,sc,oldsc,ad,roles,source,scope,review,adoption];semantics(*args);tests=controls(args)
 from pypdf import PdfReader
 for x in sc['entries'][-2:]:
  need(re.search(r'\\title\{([^{}]+)\}',(root/x['tex']).read_text()).group(1)==x['title']and len(PdfReader(root/x['pdf']).pages)==x['physical_pages']and x['admission']==reg['admissions'][0],'literal native title/pages')
 actual={n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest()for n in ast.parse((root/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'}
 need(len(base['old_nonmain_ASTs'])==167 and all(actual.get(k)==v for k,v in base['old_nonmain_ASTs'].items()),'167 old ASTs')
 text=(root/'README.rst').read_text();proto=(root/'audit/protocol.tex').read_text()
 for s in ['71 accessible originals','53 are measured and eighteen','34 await mathematical recovery','F002 guide','52-tuple appendix are not separately recovered']:need(s in text,'reader '+s)
 need('106=71' in proto and 'recoveries}+34' in proto and 'Of the 71 corrected recoveries, 53' in proto,'protocol count')
 links=0
 for name in ['README.rst','audit/completion.rst',NAT+'/PUBLICATION.rst']:
  for link in re.findall(r'<([^<>\n]+)>`_',(root/name).read_text()):
   if re.match(r'\w+://',link):continue
   need((root/PurePosixPath(name).parent/link).exists(),'local link '+link);links+=1
 required={x['path']for x in wr}|{x[k]for x in sc['entries'][-2:]for k in ['tex','pdf']}|{AUD+'/publication_plan/manifest.json','scripts/verify_snapshot.py'}
 if require_root:
  gate=load(root/AUD/'root_integration.json');root_gate(gate,required)
  for r in gate['bindings']:bind(root,r)
 return dict(status='PASS_SCIENCE71_PUBLICATION_ROUTES',publication_status='ROOT_ACCEPTED'if require_root else'ROOT_PUBLICATION_NOT_ADJUDICATED',counts=dict(active=106,corrected_recoveries=71,measured=53,unmeasured=18,mathematical_pending=34,editorial=1,archived=55,comparison_topics=19),logical_payload_routes=438,complete_frozen_packets=3,reused_public_files=380,other_originals_preserved=105,old_verifier_functions_preserved=167,new_native_pages=[2,2],new_factors=0,checked_links=links,controls=tests,required_root_gate_paths=sorted(required))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',required=True,type=Path);p.add_argument('--out',type=Path);p.add_argument('--require-root',action='store_true');a=p.parse_args();r=verify(a.repo,a.require_root)
 if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n')
 print(json.dumps(r))
