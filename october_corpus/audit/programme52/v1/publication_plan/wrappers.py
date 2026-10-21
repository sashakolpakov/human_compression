#!/usr/bin/env python3
"""Generate proposed publication metadata privately from accepted immutable payloads."""
from pathlib import Path
from copy import deepcopy
import argparse,json
from prepare import H,SCI,AUD,TOP,NUM,REG,SNAP,ACTIVE,PAPERS,load,need,rec,write

def generate(repo):
 need(not(H/'manifest.json').exists(),'preserve frozen proposal')
 plan=load(H/'copy_plan.json');need(not plan['numerical_root_adoption_pending'],'root numeric adoption first')
 routes={r['public_path']:r for r in plan['files']};reuse={r['path']:r for r in load(H/'reused_science.json')['files']};out=H/'wrappers';rows=load(H/'catalogue_additions.json')['entries'];raw=load(H/'raw_roles.json')
 def put(n,q):write('wrappers/'+n,q)
 def bind(n):
  if n in routes:return {k:(n if k=='path'else routes[n][k])for k in ['path','bytes','sha256']}
  if(out/n).exists():return rec(out/n,n)
  if n in reuse:return reuse[n]
  return rec(repo/n,n)
 def records(prefix):return [bind(n)for n in routes if n.startswith(prefix+'/')]
 science=dict(status='ROOT_ADOPTED_COMPLETE_CORRECTED_PRINCIPAL_CONTRACT',topic='B',source_ids=['L047'],source_rows=58,regenerated_ancillary_Table3_reports=0,attributed_ancillary_Table3_reports=23,source_map=SCI+'/source_map.json',scope=SCI+'/scope.json',author_manifest=bind(SCI+'/manifest.json'),independent_manifest=bind(AUD+'/scientific_review/manifest.json'),root_adoption=bind(AUD+'/root_adoption/manifest.json'),retained_common=bind('papers/topic-b/v3/umbrella.pdf'),required_new_files=6,whole_topic_program_files=10,optional_program_files=2,new_Lean_declarations=0,reused_partial_Lean_declarations=14,full_formalization=False,new_question_credit=0,artifacts=records(SCI)+records(AUD),publication_effect='New original registration occurs only with the separate programme52 registration; this wrapper preserves the accepted scientific scope.')
 put(AUD+'/admission.json',science)
 numerical=dict(status='ROOT_ADOPTED_DISTINCT_NUMERICAL_COMPARISON',topic='B',source_ids=['N001','N003','N008','L030','L040','L047'],author_manifest=bind(NUM+'/packet/manifest.json'),independent_manifest=bind(NUM+'/independent_review/manifest.json'),root_adoption=bind(NUM+'/independent_review/manifest.json'),review_and_adoption_same_root_packet=True,root_checker_private_path_disclosed=True,author_checker_export_only_portable=True,exact_fractions=270,software_inclusive_factor=None,whole_written={'numerator':144877,'denominator':149071,'interpretation':'expansion'},conditional_requires_both_whole_common_and_required_topic_premises=True,artifacts=records(NUM))
 put(NUM+'/admission.json',numerical)
 topic=dict(status='ROOT_ADOPTED_SIX_ORIGINAL_B_CURRENT_SCIENCE_AND_NUMBERS',topic='B',source_ids=numerical['source_ids'],scientific_admissions=[bind('audit/topic-b/v3/admission.json'),bind(AUD+'/admission.json')],measurement_admission=bind(NUM+'/admission.json'),common_papers=[bind('papers/topic-b/v3/umbrella.pdf'),bind(SCI+'/string_rank_theory.pdf')],applications=[bind(r['pdf'])for r in rows if r['role']=='application'],whole_common_pages=26,whole_application_pages=30,required_or_auxiliary_files=8,optional_files=2,operational_files=5,formal_files=2,whole_raw_inventory=raw,partial_declarations=14,whole_source_formalized=False,software_inclusive_factor=None,new_question_credit=0,new_original_registration=REG+'/new_original_registration.json',artifacts=[])
 put(TOP+'/admission.json',topic)
 reg=dict(status='ROOT_ADMITTED_NEW_PRINCIPAL_ORIGINAL_MEASUREMENT',source_ids=['L047'],admitted_source_ids=['L047'],measured_source_ids=['L047'],scientific_admission=bind(AUD+'/admission.json'),current_topic_admission=bind(TOP+'/admission.json'),measurement_admission=bind(NUM+'/admission.json'),no_duplicate_old_source_credit=True,new_question_credit=0,new_formal_credit=0,whole_source_formalized=False)
 put(REG+'/new_original_registration.json',reg)
 # The historical catalogue validator needs PASS/artifacts. These are literal
 # derivatives of accepted payload bindings, not a new mathematical verdict.
 artifacts={n:bind(n)for row in rows for n in [row['tex'],row['pdf']]+row['tex_inputs']}
 put(REG+'/catalogue_review.json',dict(status='PASS',scope='Exact current accepted scientific TeX/PDF bindings for canonical catalogue compatibility; mathematical acceptances stay in the cited distinct reviews.',source_admissions=[bind('audit/topic-b/v3/admission.json'),bind(AUD+'/admission.json')],scientific_reviews=[bind('audit/topic-b/v3/independent_review/manifest.json'),bind(AUD+'/scientific_review/manifest.json')],artifacts=list(artifacts.values())))
 put('papers/topic-b/latest.json',dict(status='CURRENT_SIX_ORIGINAL_B_EDITION',admission=bind(TOP+'/admission.json'),originals=numerical['source_ids'],common_papers=topic['common_papers'],applications=topic['applications'],measurement=bind(NUM+'/packet/results.json'),reader=bind(NUM+'/packet/reader.pdf'),required_raw_inventory=raw,whole_written_expansion=True,software_inclusive_factor=None))
 active=load(H/'proposed/audit/corpus/active_catalogue.json');active['status']='CURRENT_ACCESSIBLE106_PROGRAMME52';put(ACTIVE,active)
 latest=load(H/'proposed/papers/latest_catalogue.json');latest['status']='CURRENT_MANUSCRIPT_CATALOGUE_52';latest['unified_B_current_edition']=bind('papers/topic-b/latest.json');latest['active_source_catalogue']=bind(ACTIVE);put(PAPERS,latest);put('papers/latest_catalogue.json',latest)
 catalogue=load(H/'proposed/papers/catalogue.json');put('papers/catalogue.json',catalogue)
 current=load(H/'proposed/audit/corpus/next.json');current.pop('publication_pending');current.pop('pending_root_routes');current['status']='CURRENT_PROGRAMME_52_MEASURED_53_MATHEMATICAL_PENDING_1_EDITORIAL';current['active_catalogue']=bind(ACTIVE)
 for key in ['added_admissions','added_measurements']:current[key].append(bind(REG+'/new_original_registration.json'))
 current['current_topic_replacements'].append(bind(TOP+'/admission.json'));current['previous_snapshot']=rec(H/'baseline/audit/corpus/latest.json',REG+'/previous/audit/corpus/latest.json');current.pop('snapshot',None);put(SNAP,current);current['snapshot']=bind(SNAP);put('audit/corpus/latest.json',current)
 for name in load(H/'history_routes.json')['routes']:
  dst=out/REG/'previous'/name;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((H/'baseline'/name).read_bytes())
 put(REG+'/history_routes.json',load(H/'history_routes.json'))
 report=dict(status='PRIVATE_ROOT_INTEGRATION_TEMPLATE',baseline_commit=load(H/'baseline.json')['commit'],new_originals=['L047'],measured=52,mathematical_pending=53,editorial=1,archived=55,topics=19,changed_active_records=['L047'],unchanged_active_records=105,science_documents=8,science_pages=56,root_public_writer_only=True,bindings=[bind(n)for n in [AUD+'/admission.json',NUM+'/admission.json',TOP+'/admission.json',REG+'/new_original_registration.json',ACTIVE,SNAP,'audit/corpus/latest.json',PAPERS,'papers/latest_catalogue.json','papers/catalogue.json','papers/topic-b/latest.json']])
 put(REG+'/registration_report.json',report)
 # Guides are current wrappers; historical scientific READMEs remain exact.
 guide=out/TOP/'README.rst';guide.parent.mkdir(parents=True,exist_ok=True);guide.write_text('''Topic B: six complete applications\n==================================\n\nThe whole common boundary is the unchanged sixteen-page Forest coordinates\nand relative generation plus the ten-page String separators, normal modules\nand transitive rank. All six complete applications remain paid. The written\ncomparison is 144877/149071 = 0.971866: a whole-topic expansion. The new L047\nconditional factor is 19971/5503 = 3.629111, after both entire common papers and\nall required topic premises are acquired. The five earlier conditional values\nare unchanged.\n\nRead `the four-page comparison <measurement/packet/reader.pdf>`_ and\n`the exact current admission <admission.json>`_. Executable software is excluded\nsymmetrically; complete raw and printed alternatives are separately inventoried,\nwith no software-inclusive factor. Required programs remain proof premises.\n\nThe scientific addition recovers the corrected principal L047 contract. Its\n23 finer ancillary Table 3 reports remain attributed rather than regenerated;\nall source text is charged. The source-recorded conjecture was already resolved\nin L044, and no new question answer is credited here. Fourteen inherited Lean\ndeclarations remain partial. All exact earlier proof and measurement editions\nremain available as historical records.\n''')
 files=[dict(proposal_path=str(p.relative_to(H)),public_path=str(p.relative_to(out)),**{k:v for k,v in rec(p).items()if k!='path'})for p in sorted(out.rglob('*'))if p.is_file()]
 write('wrapper_routes.json',dict(status='PRIVATE_PROPOSED_ROOT_INSTALLATION',files=files,overviews_and_current_documents_pending=True))
 return dict(wrappers=len(files),artifacts_for_catalogue=len(artifacts),root_public_writer_only=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,required=True);a=p.parse_args();print(json.dumps(generate(a.repo),indent=2))
