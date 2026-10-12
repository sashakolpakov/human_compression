#!/usr/bin/env python3
"""Independent publication-only review; no author helper imports or science runs."""
from pathlib import Path, PurePosixPath
import argparse, ast, copy, hashlib, json, re
from pypdf import PdfReader
HERE=Path(__file__).resolve().parent
PIN='58f0626ae3f5ddedbea85bc3d8cbf95dedaab60b2f0eb03e12a0e12a0f05e391'
A9='papers/topic-a/extensions/locally-toroidal/v1'
TOP='audit/topic-a/v4/admission.json'
ACTIVE='audit/corpus/accessible106/updates/l121-editorial-catalogue.json'
EXPECTED_IDS=['L032','L034','F016','F013','L035','N009','L128','L012','L121']
PINS={
 'science':'a9acb0e60065cdef16f63fee0328200357347c29a22175beafb1dc5b87981f1e',
 'scientific_review':'8b7f18eadcc6fdf032bca0cf298208a8e2cab8e979aadc1d17cb9317d7e1f215',
 'scientific_adoption':'38901fc13359b1124ee2bbb005b7ac445aca47163ef16dcf62db5bc26f5c04f6',
 'numbers':'0f071b3d9098d48bfdadd8273239c4459ab35c549e2ddae59f6a9c622fa9a90e',
 'editorial_author':'f5f8f9b6d9f247e264c2107b516a7bcb9d6c78f017c7081a85ff72f114f1322e',
 'editorial_review':'0c6ff364496afc73ee36b63db1bba1ea81e840416d1977959c76860bd86b008b',
 'editorial_adoption':'63fd7715402444d0ec49b102ac574dd789f6d6cebe852659a9cced0d3a738de7',
 'numerical_review':'2d071fbfffb2288d5b0d6f434b2c0d4b63fb95f187216b8d0bf5fc093397d04d',
 'numerical_root_adoption':'000bced9618afa28c1e4e65424f464d29ea50682eb6f0e2e95509eab065d5599'}
ROLES={
 **{s:'required_program' for s in ['cubic/certificate.py','cubic/kernel_certificate.g','square/certificate.py','square/kernel_certificate.g','finite/countermodel.py','finite/exact_groups.g','finite/finite_models.py','cubic_relation/check.py']},
 'finite/model_data.json':'required_data',
 **{s:'operational_validation_runner' for s in ['cubic/check.py','square/check.py','finite/check.py','check.py']},
 'finite/formal/SectionFive.lean':'partial_formal', 'finite/formal/dependency_manifest.json':'partial_formal'}
def need(b,s):
 if not b: raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def safe(s):
 p=PurePosixPath(s);need(not p.is_absolute() and '..' not in p.parts and str(p)==s,'unsafe path '+s);return s
def exact(p,r):
 b=p.read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'byte binding '+str(p));return b
def functions(p):
 return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(p.read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name!='main'}
def partition(old,new):
 need(new['active_original_ids']==old['active_original_ids'] and len(set(new['active_original_ids']))==106,'active originals')
 need(new['archived_original_ids']==old['archived_original_ids'] and len(new['archived_original_ids'])==55,'archive unchanged')
 for k in ['admitted_original_ids','measured_original_ids']:
  need(set(new[k])==set(old[k])|{'L121'} and len(new[k])==51,'only L121 measured/admitted')
 need(set(new['accessible_pending_original_ids'])==set(old['accessible_pending_original_ids'])-{'L121','L022'} and len(new['accessible_pending_original_ids'])==54,'54 mathematical pending')
 need(new['editorial_original_ids']==['L022'] and new['editorial_factor'] is None and new['editorial_originals']==1,'editorial no factor')
 need((new['currently_measured_originals'],new['admitted_principal_originals'],new['accessible_pending_complete_recovery'])==(51,51,54),'partition counts')
 need(not(set(new['measured_original_ids'])&set(new['accessible_pending_original_ids'])) and 'L022' not in new['measured_original_ids'],'partition disjoint')
 need(new['new_question_credit']==0 if 'new_question_credit' in new else True,'no question credit')
def roles(r):
 rows=r['new_L121_files'];need(len(rows)==15,'15 new whole files')
 actual={x['path']:x['role'] for x in rows};need(actual==ROLES,'required/data/operational/formal roles')
 need((r['required_programs'],r['required_data'],r['operational'],r['partial_formal_files'],r['declarations'])==(8,1,4,2,6),'new roles counts')
 need((r['entire_topic_files'],r['entire_topic_required_files'])==(45,20),'full topic files')
 need(r['complete_enlarged_printed_cost'] is None and r['source_software_cost'] is None and r['old_printed_appendices_only_old11files'],'printed/software scope')
def numerical(a):
 need(a['source_ids']==EXPECTED_IDS and a['principal_originals_added']==['L121'],'A9 sources')
 need((a['source_sum'],a['whole_common'],a['application_sum'],a['whole_written'])==(273937,66140,136125,202265),'full manuscript costs')
 need((a['source_pages'],a['whole_common_pages'],a['whole_application_pages'])==(131,23,56),'full pages')
 need((a['exact_fractions'],a['old_conditionals_preserved'],a['source_dispositions'])==(300,240,129),'scope/fractions')
 need(a['software_inclusive_factor'] is None and a['historical_source_software_cost'] is None and a['full_graphic_cost'] is None and a['complete_enlarged_printed_program_representation'] is None,'null unknown/software')
 need(a['symmetric_program_exclusion'] and not a['whole_source_formalized'] and a['new_question_credit']==0,'no extra formal/question claim')
 need((a['whole_raw_files'],a['required_program_or_data_files'],a['auxiliaries'],a['operational_runners'],a['partial_Lean_modules'],a['formal_dependency_manifests'])==(45,20,3,6,15,1),'complete raw inventory')
def catalogue(old,new,rows):
 need(old['papers']==new['papers'],'all old papers unchanged')
 need(new['new_editions'][:len(old['new_editions'])]==old['new_editions'],'all old canonical editions unchanged')
 appended=new['new_editions'][len(old['new_editions']):];need(len(appended)==10,'ten added science routes')
 need([x['id'] for x in appended]==[x['id'] for x in rows],'exact new ids')
 for a,b in zip(appended,rows):
  need({k:v for k,v in a.items() if k!='status'}=={k:v for k,v in b.items() if k!='status'},'complete canonical row')
 need({k:v for k,v in new['current_topic_editions'].items() if k!='A'}=={k:v for k,v in old['current_topic_editions'].items() if k!='A'},'other topic routes')
 need(new['current_topic_editions']['A']==[r['id'] for r in rows],'current A ten science routes')
 need([r['physical_pages'] for r in rows]==[23,4,3,6,3,6,11,3,9,11] and sum(r['physical_pages'] for r in rows)==79,'complete 79 pages')
 need([r['compiler'] for r in rows]==['xelatex']*9+['pdflatex'],'actual compilers')
 need(rows[-1]['required_program_inputs']==[A9+'/'+p for p,v in ROLES.items() if v=='required_program'],'all eight program inputs')
 need(rows[-1]['required_data_inputs']==[A9+'/finite/model_data.json'],'mandatory data input')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--proposal',type=Path,required=True);ap.add_argument('--study-root',type=Path);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--public-stage',action='store_true');ap.add_argument('--build-evidence-root',type=Path);a=ap.parse_args()
 p=a.proposal;s=a.study_root;repo=a.public_root;need(a.public_stage or s is not None,'proposal mode needs study root');a.out.mkdir(parents=True,exist_ok=False)
 need(sha((p/'manifest.json').read_bytes())==PIN,'frozen proposal pin');m=load(p/'manifest.json')
 need(len(m['exports'])==63,'63 exports')
 for r in m['exports']:exact(p/safe(r['path']),r)
 plan=load(p/'copy_plan.json');wr=load(p/'wrapper_routes.json');reuse=load(p/'reused_science.json');base=load(p/'baseline.json');rows=load(p/'catalogue_additions.json')['entries'];rr=load(p/'raw_roles.json')
 need(len(plan['files'])==167 and len(plan['packets'])==9 and len(reuse['files'])==47 and len(wr['files'])==23,'route cardinalities')
 need({r['role']:r['manifest_sha256'] for r in plan['packets']}==PINS,'nine accepted packet pins')
 actual={r['public_path']:r for r in plan['files']};need(len(actual)==167,'no duplicate destinations');expected={}
 mapped={};receipts=[]
 for pk in plan['packets']:
  q=(repo/pk['public_directory']) if a.public_stage else (s/pk['study_directory']);need(sha((q/'manifest.json').read_bytes())==pk['manifest_sha256'],'accepted manifest')
  exports=load(q/'manifest.json')['exports'];need(len(exports)==pk['exports'],'complete manifest exports')
  for r in exports+[{'path':'manifest.json','bytes':(q/'manifest.json').stat().st_size,'sha256':pk['manifest_sha256']}]:
   target=safe(pk['public_directory']+'/'+r['path']);source=pk['study_directory']+'/'+r['path']
   expected[target]={'role':pk['role'],'study_path':source,'public_path':target,'bytes':r['bytes'],'sha256':r['sha256']}
   b=exact(q/safe(r['path']),r);mapped[target]=q/r['path']
   if a.public_stage:exact(repo/target,r)
 need(actual==expected,'exact full accepted export mapping')
 for r in reuse['files']:
  exact(repo/safe(r['path']),r);mapped[r['path']]=repo/r['path']
 for r in wr['files']:
  exact(p/safe(r['proposal_path']),r);need(r['public_path'] not in mapped,'wrapper collision');mapped[safe(r['public_path'])]=p/r['proposal_path']
 for r in base['files']:exact(p/'baseline'/safe(r['path']),r)
 need(not any(x.startswith(('sources/','primary/')) for x in mapped),'no primary assets exported')
 oldf=functions(p/'baseline/scripts/verify_snapshot.py');newf=functions(repo/'scripts/verify_snapshot.py')
 need(len(oldf)==125 and all(newf.get(k)==v for k,v in oldf.items()),'125 existing verifier functions unchanged')
 b=next(x for x in base['files'] if x['path']=='scripts/build_papers.py');exact(repo/b['path'],b)
 history=load(p/'wrappers/audit/programme51/v1/proposed_history_routes.json')['routes']
 for src,r in history.items():need(exact(mapped[r['path']],r)==(p/'baseline'/src).read_bytes(),'exact historical pointer '+src)
 def resolve(path):return mapped.get(path,repo/path)
 def j(path):return load(resolve(path))
 old=load(p/'baseline/audit/corpus/latest.json');new=j('audit/corpus/latest.json');partition(old,new)
 cat0=load(p/'baseline'/old['active_catalogue']['path']);cat=j(ACTIVE)
 before={r['original_id']:r for r in cat0['entries']};after={r['original_id']:r for r in cat['entries']}
 need(set(before)==set(after) and len(after)==106,'complete active catalogue')
 need([k for k in before if before[k]!=after[k]]==['L022','L121'],'exactly two original record changes')
 ed=after['L022'];need(ed['active'] and ed['current_principal_recovery']['factor'] is None and not ed['current_principal_recovery']['count_as_measured_mathematical_recovery'] and ed['principal_results_to_recover']['principal_mathematical_results']==[],'editorial no result/factor')
 need(after['L121']['current_principal_recovery']['source_dispositions']==27,'27 exact source dispositions')
 roles(rr);numerical(j(TOP));catalogue(load(p/'baseline/papers/catalogue.json'),j('papers/catalogue.json'),rows)
 for r in rr['new_L121_files']:exact(resolve(r['public_path']),r)
 latest0=load(p/'baseline/papers/latest_catalogue.json');latest=j('papers/latest_catalogue.json')
 need(len(latest['entries'])==len(latest0['entries'])+1,'one new scientific application')
 for oldrow,newrow in zip(latest0['entries'],latest['entries']):
  if oldrow.get('topic')!='A':need(oldrow==newrow,'non-A row unchanged')
  else:need({k:v for k,v in oldrow.items() if k!='measurement_admission'}=={k:v for k,v in newrow.items() if k!='measurement_admission'},'old A row only measurement pointer changes')
 need(set(latest['original_ids'])==set(latest0['original_ids'])|{'L121'} and latest['new_question_credit']==0,'only new L121 original')
 # Independent binding of existing fresh render evidence to every actual TeX input and authoritative page.
 br=load(p/'reports/canonical_build_report.json')['papers'];sr=load(p/'reports/stage_report.json')['render']['checks']
 need(len(br)==len(sr)==10,'ten build records')
 for row in rows:
  doc=next(x for x in br if x['id']==row['id']);text=next(x for x in sr if x['id']==row['id'])
  need(doc['compiler']==row['compiler'] and not doc['diagnostics'] and doc['status']=='compiled','clean actual compiler')
  need(sha(resolve(row['tex']).read_bytes())==doc['tex_sha256'],'bound TeX build')
  need([x['path'] for x in doc['tex_inputs']]==row['tex_inputs'],'complete build input list')
  for x in doc['tex_inputs']:exact(resolve(x['path']),x)
  pdf=PdfReader(resolve(row['pdf'])); hashes=[sha((x.extract_text() or '').encode()) for x in pdf.pages]
  need(len(hashes)==row['physical_pages'] and hashes==text['page_text_sha256'] and text['exact_page_text'] and not text['diagnostics'],'79 authoritative page hashes')
  tex=resolve(row['tex']).read_text();title=re.search(r'\\title\{([^{}]*)\}',tex)
  need(title is not None and ' '.join(title.group(1).split())==row['title'],'literal title')
  if a.build_evidence_root:
   built=a.build_evidence_root/row['id']/'paper.pdf';need(sha(built.read_bytes())==doc['pdf_sha256'],'actual fresh built PDF')
   need([sha((x.extract_text() or '').encode()) for x in PdfReader(built).pages]==hashes,'fresh and authoritative page texts')
  receipts.append({'id':row['id'],'title':row['title'],'pages':len(hashes),'compiler':row['compiler'],'bound_inputs':len(doc['tex_inputs'])})
 # README is exactly the declared editorial migration, with old complete text retained.
 text=(p/'baseline/README.rst').read_text()
 for d in load(p/'documentation_delta.json')['readme_replacements']:
  need(text.count(d['before'])==d['occurrences'],'exact documentation patch');text=text.replace(d['before'],d['after'])
 need(text==resolve('README.rst').read_text(),'only declared README changes')
 # Known proposal findings are explicit, not silently accepted.
 pointer=latest['affine_topic_consolidated_into_A']['current_pointer'];need(pointer['sha256']!=sha(resolve(pointer['path']).read_bytes()),'known stale pointer exists in original')
 need(new['added_measurements'][-1]['path']==TOP and len(j(TOP)['source_ids'])==9,'known duplicate-registration route exists in original')
 controls=[]
 def reject(name,fn,obj,edit):
  x=copy.deepcopy(obj);edit(x)
  try:fn(x)
  except (ValueError,KeyError,TypeError,IndexError):controls.append(name);return
  raise ValueError('accepted corrupt control '+name)
 reject('editorial_factor_zero',lambda x:partition(old,x),new,lambda x:x.update(editorial_factor=0))
 reject('editorial_measured_credit',lambda x:partition(old,x),new,lambda x:x['measured_original_ids'].append('L022'))
 reject('dropped_active_original',lambda x:partition(old,x),new,lambda x:x['active_original_ids'].pop())
 reject('dropped_archived_original',lambda x:partition(old,x),new,lambda x:x['archived_original_ids'].pop())
 reject('missing_new_admission',lambda x:partition(old,x),new,lambda x:x['admitted_original_ids'].remove('L121'))
 reject('pending_editorial',lambda x:partition(old,x),new,lambda x:x['accessible_pending_original_ids'].append('L022'))
 reject('required_coordinate_checker_demoted',roles,rr,lambda x:next(r for r in x['new_L121_files'] if r['path']=='cubic_relation/check.py').update(role='operational_validation_runner'))
 reject('mandatory_model_data_omitted',roles,rr,lambda x:x.update(new_L121_files=[r for r in x['new_L121_files'] if r['path']!='finite/model_data.json']))
 reject('historical_software_zero',roles,rr,lambda x:x.update(source_software_cost=0))
 reject('false_complete_printed_representation',roles,rr,lambda x:x.update(complete_enlarged_printed_cost=123))
 adm=j(TOP)
 reject('discounted_common',numerical,adm,lambda x:x.update(whole_common=0))
 reject('omitted_application',numerical,adm,lambda x:x.update(application_sum=110576))
 reject('software_inclusive_scalar',numerical,adm,lambda x:x.update(software_inclusive_factor=1.5))
 reject('full_Lean_claim',numerical,adm,lambda x:x.update(whole_source_formalized=True))
 reject('new_question_credit',numerical,adm,lambda x:x.update(new_question_credit=1))
 reject('wrong_compiler',lambda x:catalogue(load(p/'baseline/papers/catalogue.json'),j('papers/catalogue.json'),x),rows,lambda x:x[-1].update(compiler='xelatex'))
 reject('incomplete_application_pages',lambda x:catalogue(load(p/'baseline/papers/catalogue.json'),j('papers/catalogue.json'),x),rows,lambda x:x[-1].update(physical_pages=10))
 # Public correction checker is a separately bound exact overlay; no broad path exclusion.
 pub=None
 if a.public_stage:
  delta=load(HERE/'publication_delta.json')
  allowed={r['path']:r for r in delta['corrected_files']}
  for r in wr['files']:
   expected=allowed.get(r['public_path'],r);exact(repo/r['public_path'],expected)
  for r in delta['added_files']:exact(repo/r['path'],r)
  cur=load(repo/'audit/corpus/latest.json');partition(old,cur)
  ptr=load(repo/'papers/latest_catalogue.json')['affine_topic_consolidated_into_A']['current_pointer'];exact(repo/ptr['path'],ptr)
  reg=load(repo/delta['new_original_registration']);need(reg['source_ids']==['L121'],'new registration only L121')
  need(cur['added_measurements'][:-1]==old['added_measurements'] and cur['added_measurements'][-1]['path']==delta['new_original_registration'],'only one additional-original registration')
  need(cur['added_admissions'][:-1]==old['added_admissions'] and cur['added_admissions'][-1]['path']==delta['new_original_registration'],'only one additional-original admission')
  need(cur['current_topic_replacements'][-1]['path']==TOP,'full nine-source A remains current topic')
  for k in ['added_measurements','added_admissions','current_topic_replacements']:
   for r in cur[k]:exact(repo/r['path'],r)
  exact(repo/cur['snapshot']['path'],cur['snapshot']);exact(repo/cur['active_catalogue']['path'],cur['active_catalogue'])
  reject('new_registration_recounts_old_eight',lambda x:need(x['source_ids']==['L121'],'only L121 newly registered'),reg,lambda x:x.update(source_ids=EXPECTED_IDS))
  reject('stale_current_A_pointer',lambda x:exact(repo/x['path'],x),ptr,lambda x:x.update(bytes=14202,sha256='bb7bccb9fd8f02be4676861b934927659b1aa72bcae0e81048ccb8b195a547ce'))
  reject('full_topic_used_as_new_measurement',lambda x:need(x['added_measurements'][-1]['path']==delta['new_original_registration'],'new-only measurement'),cur,lambda x:x['added_measurements'][-1].update(path=TOP))
  current_rows=load(repo/ACTIVE)['entries']
  current_by_id={r['original_id']:r for r in current_rows}
  need({r['original_id'] for r in current_rows if r['current_principal_recovery']['status']=='ADMITTED_AND_MEASURED'}==set(cur['measured_original_ids']),'all 51 current measured classifications')
  need(all(current_by_id[k]==before[k] for k in before if k not in ['L121','L022']),'104 final records unchanged')
  need(current_by_id['L121']['current_principal_recovery']['whole_source_formalized'] is False and current_by_id['L121']['current_principal_recovery']['historical_admission_evidence']==before['L121']['historical_proof_status'],'L121 partial formal and historical status preserved')
  reject('L121_missing_standard_measured_status',lambda x:need(x['current_principal_recovery']['status']=='ADMITTED_AND_MEASURED','registered measured status'),current_by_id['L121'],lambda x:x['current_principal_recovery'].update(status='ROOT_ADMITTED_COMPLETE_CORRECTED_PRINCIPAL_CONTRACT'))
  pub={'status':'PASS_EXACT_ROOT_REGISTRATION_CORRECTIONS','corrected_files':len(allowed),'added_files':len(delta['added_files'])}
 result={'status':'PASS_BOUNDED_PUBLICATION_REVIEW' if pub else 'PASS_PAYLOADS_WITH_DECLARED_REQUIRED_REGISTRATION_CORRECTIONS','proposal_manifest':PIN,'proposal_exports':63,'accepted_packets':9,'exact_payload_routes':167,'reused_science_files':47,'proposed_wrappers':23,'prior_verifier_functions':125,'source_records_unchanged':104,'canonical_scientific_routes':10,'scientific_pages':79,'build_receipts':receipts,'whole_raw_new_files':15,'whole_raw_topic_files':45,'programme':{'active':106,'measured':51,'mathematical_pending':54,'editorial':1,'archived':55,'topics':19},'negative_controls':controls,'public_corrections':pub,'no_new_math_source_extraction_or_Lean_replay':True,'fresh_compilation_repeated':False}
 (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['build_receipts','negative_controls']}));print('Controls rejected:',len(controls))
if __name__=='__main__':main()
