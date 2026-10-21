#!/usr/bin/env python3
"""Concrete proposed wrappers, never written into the public checkout."""
from pathlib import Path
from copy import deepcopy
import argparse,json,re
from prepare import H,BASE,SCI,AUD,TOP,NUM,REG,SNAP,ACTIVE,CAT,load,rec,need,write

def prepare_wrappers(study,repo):
 need(not(H/'manifest.json').exists(),'preserve freeze');plan=load(H/'copy_plan.json');payload={r['public_path']:dict(path=r['public_path'],bytes=r['bytes'],sha256=r['sha256'])for r in plan['files']};routes=[]
 def get(n):
  if n in payload:return payload[n]
  if(H/'wrappers'/n).exists():return rec(H/'wrappers'/n,n)
  return rec(repo/n,n)
 def out(n,v):
  p=H/'wrappers'/n;p.parent.mkdir(parents=True,exist_ok=True)
  if isinstance(v,str):p.write_text(v)
  else:p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
  r=rec(p,n);routes.append(dict(proposal_path='wrappers/'+n,public_path=n,bytes=r['bytes'],sha256=r['sha256']));return r
 for original,r in load(H/'history_routes.json')['routes'].items():
  p=H/'wrappers'/r['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((repo/original).read_bytes());routes.append(dict(proposal_path='wrappers/'+r['path'],public_path=r['path'],bytes=r['bytes'],sha256=r['sha256']))
 rows=load(H/'catalogue_additions.json')['entries'];commons=[x['pdf']for x in rows if x['application_id'].startswith('U')];apps={}
 for row in rows:
  if row['application_id'].startswith('A'):
   key='A10'if row['application_id'].startswith('A10')else row['application_id'];apps.setdefault(key,[]).append(row['pdf'])
 need(len(commons)==3 and len(apps)==10,'complete topic routing')
 raw=out(TOP+'/raw_routes.json',load(H/'raw_routes.json'));r=load(study/'topic_A_L003_measurement_results/results.json');p=r['primary']
 science={'status':'ROOT_ACCEPTED_COMPLETE_CORRECTED_L003_CONTRACT','original_id':'L003','source_ids':['L003'],'topic':'A','source':load(study/'topic_A_L003_complete_root_review/review.json')['source'],'source_dispositions':125,'source_table_rows':73,'source_map':get(SCI+'/source_map.json'),'common':commons,'applications':apps,'native_scientific_pages':104,'L003_application_pages':[7,4,4,2],'whole_common_pages':[23,14,4],'L121_adapter_pages':1,'complete_corrected_not_literal_contract':True,'source_corrections':['T5.8 and T5.10 corrected full orders','T4.8 nonsplit corrected shape','twelve ordinary local-period collapses','T8.11 malformed literal period word','missing fourth correlation generator','diagram4 forward geometry retains actual-residue hypotheses; diagram5 experimental geometry not promoted to theorem'],'questions_and_failed_searches_not_new_answers':True,'retained_classical_classifications_explicit':True,'assembly':get(SCI+'/manifest.json'),'root_complete_review':get(AUD+'/root_review/manifest.json'),'component_acceptances':'Copied complete assembly acceptance/ tree; every new mathematical component has a distinct earlier review.','frozen_payloads':[payload[z['public_path']]for z in plan['files']if z['role']in ['science','science_adoption']],'required_whole_content_inventory':raw,'whole_source_formalized':False,'new_Lean_declarations':0,'principal_originals_added':['L003'],'original_intake_added':0,'new_question_credit':0,'source_asset_redistributed':False,'role_disclosure':'enumeration_review authored base, finite structural and correlation papers; enumeration_volume authored seven shared structures and complete assembly; root authored order768. Each contribution has its distinct review. Root complete-contract review accepts the assembled corrected scope.'}
 sci=out(AUD+'/admission.json',science)
 top={'status':'ROOT_ADOPTED_TEN_ORIGINAL_A_SCIENCE_AND_SYMMETRIC_MANUSCRIPT_MEASUREMENT','topic':'A','source_ids':r['source_ids'],'principal_originals_added':['L003'],'original_intake_added':0,'new_question_credit':0,'prior_nine_original_admission':get('audit/topic-a/v4/admission.json'),'new_scientific_admission':sci,'numerical_author':get(NUM+'/packet/manifest.json'),'numerical_distinct_review':get(NUM+'/independent_review/manifest.json'),'numerical_root_adoption':get(NUM+'/root_adoption/manifest.json'),'input_author':get(NUM+'/packet/inputs/input/manifest.json'),'input_root_review':get(NUM+'/packet/inputs/root_review/manifest.json'),'frozen_payloads':[payload[z['public_path']]for z in plan['files']if z['role']in ['numbers','numeric_review','numeric_adoption']],'measurement':get(NUM+'/packet/results.json'),'reader':get(NUM+'/packet/reader.pdf'),'primary_coordinate':r['primary_coordinate'],'primary':p['written'],'conditionals':p['conditional'],'source_sum':p['source_sum'],'whole_common':p['whole_common'],'common_components':p['common_costs'],'application_sum':p['application_sum'],'application_components':p['application_costs'],'whole_written':p['whole_written'],'source_pages':152,'whole_common_pages':[23,14,4],'whole_application_pages':63,'canonical_native_science':rows,'current_common':commons,'current_applications':apps,'source_dispositions':254,'coordinates':30,'exact_fractions':330,'old_conditionals_preserved':240,'whole_raw_files':203,'raw_occurrences':253,'raw_roles':raw,'required_programs':28,'required_data_contents':71,'required_whole_contents':99,'optional_validation_files':5,'operational_files':17,'partial_formal_files':16,'output_receipts':66,'whole_source_formalized':False,'new_Lean_declarations':0,'old_partial_printed_appendix_pages':r['old_partial_printed_appendix_pages'],'complete_enlarged_printed_program_representation':None,'symmetric_program_exclusion':True,'software_inclusive_factor':None,'historical_source_software_cost':None,'full_graphic_cost':None,'all_existing_scientific_bytes_unchanged':True,'scope_change':'L121 current application is the complete1-page adapter; former proofs migrate unchanged into paid common. All four L003 application papers remain included.','role_disclosure':'Root authored A10 arithmetic. enumeration_volume independently reviewed it, disclosing accepted input authorship and earlier numerical-mechanics authorship. Root adopted that distinct review. Publication proposal is enumeration_volume; final public integration is root-only.'}
 topic=out(TOP+'/admission.json',top)
 registration=out(REG+'/new_original_registration.json',dict(status='NEW_ORIGINAL_REGISTRATION_FROM_ACCEPTED_SCIENCE_AND_NUMBERS',source_ids=['L003'],principal_originals_added=['L003'],measured_originals_added=['L003'],scientific_admission=sci,topic_admission=topic,original_intake_added=0,new_question_credit=0,new_Lean=0,full_source_formalized=False,all_ten_topic_ids_registered_again=False))
 pointer=dict(status='CURRENT_ACCEPTED_TEN_ORIGINAL_A_CONTRACTS_AND_SYMMETRIC_MEASUREMENT',source_ids=r['source_ids'],admission=topic,reader=get(NUM+'/packet/reader.pdf'),measurement=get(NUM+'/packet/results.json'),common=commons,applications=apps,catalogue_entries=rows,whole_common_pages=[23,14,4],whole_application_pages=63,required_whole_content_inventory=raw,old_science_bytes_reused=True,old_measurements_preserved=True,software_inclusive_factor=None,complete_enlarged_printed_program_factor=None)
 tp=out('papers/topic-a/latest.json',pointer)
 affine=load(repo/'papers/topic-affine/latest.json');affine['current_topic_pointer']=tp;out('papers/topic-affine/latest.json',affine)
 nl=load(H/'proposed/papers/latest_catalogue.json');nl['unified_A_current_edition']=dict(source_ids=r['source_ids'],validation_excluded_both_sides=True,historical_software_cost=None,current_common=commons,current_applications=apps,prior_admission=get('audit/topic-a/v4/admission.json'),admission=topic,current_topic_pointer=tp)
 # Current catalogue metadata is additive; old entries remain historical records.
 cat=load(H/'proposed/papers/catalogue.json');out(CAT,cat);out('papers/catalogue.json',cat)
 active=load(H/'proposed/audit/corpus/active_catalogue.json');active['status']='CURRENT_ACCESSIBLE106_PROGRAMME53';activebind=out(ACTIVE,active)
 for x in active['entries']:
  if x['original_id']=='L003':need(x['current_principal_recovery']['status']=='ADMITTED_AND_MEASURED','standard measured status')
 nl['status']='CURRENT_MANUSCRIPT_CATALOGUE_53';nl['active_source_catalogue']=activebind;out('papers/latest_catalogue.json',nl)
 nxt=load(H/'proposed/audit/corpus/next.json');nxt['status']='CURRENT_PROGRAMME_53_MEASURED_52_MATHEMATICAL_PENDING_1_EDITORIAL';nxt['previous_snapshot']=get(REG+'/previous/audit/corpus/latest.json');nxt['active_catalogue']=activebind
 for k in ['added_admissions','added_measurements']:nxt[k].append(registration)
 nxt['current_topic_replacements'].append(topic);nxt.pop('snapshot',None);snap=out(SNAP,nxt);nxt['snapshot']=snap;corpus=out('audit/corpus/latest.json',nxt)
 arts={}
 for row in rows:
  for n in [row['tex'],row['pdf']]+row.get('tex_inputs',[]):arts[n]=get(n)
 out(REG+'/catalogue_review.json',dict(status='PASS',scope='Canonical catalogue compatibility record derived exclusively from already accepted exact native TeX/PDF bindings; not a new independent mathematical review.',artifacts=list(arts.values()),source_admission=sci,topic_admission=topic,native_documents=16,pages=104,all_retained_compilers_explicit=True))
 reg=out(REG+'/registration_report.json',dict(status='PROPOSED_EXACT_PROGRAMME53_BINDINGS_ROOT_INTEGRATION_REVIEW_REQUIRED',base_commit=BASE,counts=dict(active=106,measured=53,mathematical_pending=52,editorial=1,archived=55,topics=19),new_original='L003',unchanged_other_topic_count=18,changed_existing_conditional='L121',active_catalogue=activebind,corpus_pointer=corpus,snapshot=snap,papers_pointer=get('papers/latest_catalogue.json'),catalogue=get(CAT),new_original_registration=registration,topic_admission=topic,scientific_admission=sci,overview_admission_route='audit/overview/v19/admission.json',no_L044_or_L096_credit=True))
 old=(repo/'README.rst').read_text();text=old.replace('**52 accessible originals','**53 accessible originals').replace('53 await mathematical recovery','52 await mathematical recovery').replace('audit/overview/v18/','audit/overview/v19/').replace('fifty-two individual','fifty-three individual').replace('first twenty-six individual','first twenty-seven individual').replace('selects v18','selects v19').replace('audit/programme52/v1/previous/','audit/programme53/v1/previous/').replace('papers/topic-a/v4/PUBLICATION.rst','papers/topic-a/v5/PUBLICATION.rst').replace('L032, L034, F016, F013, L035, N009, L128, L012, L121\n','L032, L034, F016, F013, L035, N009, L128, L012, L121, L003\n').replace('     - 1.354347','     - 1.210825')
 a=text.index('Topic B now includes L047.');b=text.index('\nCurrent papers and comparisons',a)
 text=text[:a]+'''Topic A now includes L003. Its three complete common papers cost 108,271
characters; all ten application bundles cost 155,199. The whole factor is
**1.210825**, lower than the preceding nine-original factor of 1.354347.
L121's **12.288729** conditional factor follows moving its substantial proofs
into the fully charged common supplement. L003's complete four-paper
application has factor **1.063284** after that acquisition. All 99 required
program/data contents remain explicit prerequisites; no sibling proof is free.
''' +text[b:];out('README.rst',text)
 tex=(repo/'audit/protocol.tex').read_text().replace('106=52\\ \\text{measured recoveries}+53\\ \\text{mathematical targets}','106=53\\ \\text{measured recoveries}+52\\ \\text{mathematical targets}').replace('overview v18','overview v19').replace('fifty-two\nconditional','fifty-three\nconditional').replace('overview/v18/','overview/v19/').replace('all 23 common pages and all nine applications','all 41 common pages across three complete papers and all ten applications')
 out('audit/protocol.tex',tex)
 guide='''Topic A: complete common theory and ten applications
====================================================

The current edition charges all three common papers and all ten complete
application bundles. The whole manuscript factor is 319,016 / 263,470 =
1.210824761832. The earlier nine-original factor was 1.354347019999; the
additional proof material is retained without adjusting the metric.

Read the `numerical reader <../../../audit/topic-a/v5/measurement/packet/reader.pdf>`_
and `accepted admission <../../../audit/topic-a/v5/admission.json>`_.
The complete `L003 application <../extensions/hexagonal/v1/application_complete.pdf>`_
and `common reading bundle <../extensions/hexagonal/v1/common_complete.pdf>`_
copy entire native constituent papers. The bundles are reading conveniences,
not additional counted documents. The admission lists all sixteen native PDFs
and their exact compilers, and links the unchanged eight earlier applications.
The complete `L121 adapter <../extensions/hexagonal/v1/inputs/base/l121_adapter.pdf>`_
uses proofs moved into the paid fourteen-page common supplement.

The corrected source contract retains all125 L003 dispositions and73 table
rows, including the two order corrections, nonsplitting result, local-period
collapses, malformed word and exact correlation qualifications. Diagram5's
experimental geometric existence and the source questions are not new answers.
Read the `source map <../extensions/hexagonal/v1/source_map.json>`_ before using
an individual claim.

Individual factors require all41 common pages and all99 required complete
program/data contents already acquired. Every complete local application or
companion remains charged. The `whole-file inventory <../../../audit/topic-a/v5/raw_routes.json>`_
retains all253 occurrences/203 contents and their overlapping roles. Concrete
software is excluded symmetrically from manuscript costs; required programs
remain proof premises. No software-inclusive factor or complete enlarged
printed appendix is claimed. Historical software, external proofs and complete
graphics are unknown. All inherited formal statements remain scoped partial
evidence, with no full-source Lean claim.

The `preceding edition <../v4/PUBLICATION.rst>`_ remains immutable. Root alone
performs current public registration. Author/reviewer contributions are retained
in the exact admissions rather than inferred from the publication wrapper.
'''
 out('papers/topic-a/v5/PUBLICATION.rst',guide)
 out(TOP+'/README.rst','''Current ten-original A comparison
====================================

The `publication guide <../../../papers/topic-a/v5/PUBLICATION.rst>`_ gives
all common/application routes and limitations. The `admission <admission.json>`_
binds the complete corrected L003 science, root-accepted inputs, root-authored
numbers, distinct numerical review and root adoption. Earlier frozen labels
are interpreted through these later acceptances. No scientific component,
source correction, required data file or inherited application is omitted.
''')
 out(NUM+'/public_input_routes.json',load(H/'public_input_routes.json'))
 out(NUM+'/public_input_replay.py',(H/'public_input_replay.py').read_text())
 overview=out('audit/overview/v19/admission.json',dict(status='ROOT_ACCEPTED_OVERVIEW53_ARITHMETIC_PUBLIC_INTEGRATION_PENDING',author=get('audit/overview/v19/packet/manifest.json'),distinct_root_review=get('audit/overview/v19/independent_review/manifest.json'),reader=get('audit/overview/v19/packet/reader.pdf'),results=get('audit/overview/v19/packet/results.json'),programme_registration=reg,counts_source=snap,topics=19,measured_originals=53,mathematical_pending=52,editorial=1,active=106,archived=55,exact_fractions=72,actual_bars_per_format=163,software_inclusive_factor=None,pooled_factor=None,new_original_credit_from_arithmetic=0,new_question_credit=0,author_role='enumeration_volume authored overview; root distinctly reviewed it. Root authored A10 numbers and enumeration_volume distinctly reviewed them, with prior input authorship disclosed.'))
 op=load(repo/'audit/overview/latest.json');op.update(status='CURRENT_OVERVIEW53_ROOT_ADOPTED',admission=overview,reader=get('audit/overview/v19/packet/reader.pdf'),counts_source=snap,pending_accessible_originals=52,recovered_originals=53,historically_measured_originals=53,current_conditional_factors=53,written_factors_status='NINETEEN_WHOLE_AND_FIFTY_THREE_CONDITIONAL_MANUSCRIPT_FACTORS',mathematical_pending_originals=52,unmeasured_accessible_originals=53,previous_pointer=get(REG+'/previous/audit/overview/latest.json'));out('audit/overview/latest.json',op)
 write('wrapper_routes.json',dict(files=routes,overview_root_admission_not_invented=True,overview_current_pointer_pending=False,root_only_public_writer=True))
 write('proposed_overview_pointer.json',dict(status='PROPOSED_CURRENT_POINTER_ROOT_ACCEPTED_ARITHMETIC_PUBLIC_INTEGRATION_PENDING',admission_path='audit/overview/v19/admission.json',reader=get('audit/overview/v19/packet/reader.pdf'),counts_source=snap,topics=19,recovered_originals=53,pending_accessible_originals=52,mathematical_pending_originals=52,editorial_originals=1,editorial_original_ids=['L022'],archived_unavailable_originals=55,active_catalogue_originals=106,current_whole_factors=19,current_conditional_factors=53,software_inclusive_factor=None,previous_pointer=get(REG+'/previous/audit/overview/latest.json')))
 print(json.dumps(dict(wrappers=len(routes),registration=reg,overview_root_admission_pending=False)))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);a=p.parse_args();prepare_wrappers(a.study_root,a.repo)
