#!/usr/bin/env python3
"""Materialize proposed public wrappers in this private folder after numerical adoption."""
from pathlib import Path
from copy import deepcopy
import argparse,hashlib,json
from prepare import SCI,AUD,NUM,ED
H=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def need(x,m):
    if not x:raise ValueError(m)
def write(path,value):
    p=H/'wrappers'/path;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n');return bind(p,path)
def bind(file,path):
    b=file.read_bytes();return dict(path=path,bytes=len(b),sha256=sha(b))
def main(study):
    need(not(H/'manifest.json').exists(),'preserve final freeze')
    plan=load(H/'copy_plan.json');need(not plan['numerical_root_adoption_pending'],'root numeric adoption first')
    routes=plan['files'];packets={r['role']:next(dict(path=x['public_path'],bytes=x['bytes'],sha256=x['sha256'])for x in routes
        if x['role']==r['role']and x['study_path']==r['study_directory']+'/manifest.json')for r in plan['packets']}
    def payload(roles):return[dict(path=x['public_path'],bytes=x['bytes'],sha256=x['sha256'])for x in routes if x['role']in roles]
    def mapped(study_path):
        x=next(r for r in routes if r['study_path']==study_path);return dict(path=x['public_path'],bytes=x['bytes'],sha256=x['sha256'])
    baseline=load(H/'baseline.json');history={}
    names={'audit/corpus/latest.json':'previous_corpus_pointer.json','papers/latest_catalogue.json':'previous_catalogue.json',
           'papers/catalogue.json':'previous_full_catalogue.json','papers/topic-a/latest.json':'previous_a_pointer.json',
           'audit/overview/latest.json':'previous_overview_pointer.json','README.rst':'previous_README.rst',
           'audit/completion.rst':'previous_completion.rst','audit/protocol.tex':'previous_protocol.tex','audit/protocol.pdf':'previous_protocol.pdf'}
    for source,name in names.items():
        p=H/'baseline'/source;dest='audit/programme51/v1/'+name;t=H/'wrappers'/dest;t.parent.mkdir(parents=True,exist_ok=True);t.write_bytes(p.read_bytes());history[source]=bind(t,dest)
    editorial=write(ED+'/admission.json',dict(status='ROOT_ADOPTED_EDITORIAL_DISPOSITION',original_id='L022',
      author=packets['editorial_author'],distinct_review=packets['editorial_review'],root_adoption=packets['editorial_adoption'],
      frozen_payloads=payload(['editorial_author','editorial_review','editorial_adoption']),
      recovery_status='NO_PRINCIPAL_MATHEMATICAL_RESULT_TO_RECOVER',accessible_original_retained=True,
      active_original_count=1,measured_original_credit=0,factor=None,new_question_credit=0,new_formal_credit=0,
      scope='Complete five-paragraph editorial reading; other contributions described in the preface are not theorem obligations of this editorial.'))
    sc=load(H/'source_contract.json')
    science=write(AUD+'/admission.json',dict(status='ROOT_ADOPTED_COMPLETE_CORRECTED_L121_PRINCIPAL_CONTRACT',
      original_id='L121',topic='A',application_id='A9',source=sc['source'],source_dispositions=27,
      application=mapped('topic_A_L121_application/application.pdf'),source_map=mapped('topic_A_L121_application/source_map.json'),
      scientific_scope=mapped('topic_A_L121_application/scope.json'),
      author=packets['science'],distinct_review=packets['scientific_review'],root_adoption=packets['scientific_adoption'],
      frozen_payloads=payload(['science','scientific_review','scientific_adoption']),
      common_theory='papers/topic-a/v3/umbrella.pdf',common_pages=23,application_pages=11,
      inherited_common_bytes_unchanged=True,required_programs=8,required_data_files=1,operational_runners=4,
      new_partial_Lean_declarations=6,whole_source_formalized=False,retained_classical_inputs=sc['retained_premises'],
      original_intake_added=0,principal_originals_added=['L121'],new_question_credit=0,
      historical_source_software_cost=None,source_asset_redistributed=False,
      source_corrections=sc['source_corrections']))
    r=load(study/'topic_A_L121_measurement_results/results.json');x=r['coordinates'][r['primary_coordinate']]
    a=write('audit/topic-a/v4/admission.json',dict(status='ROOT_ADOPTED_NINE_ORIGINAL_A_SCIENCE_AND_SYMMETRIC_MANUSCRIPT_MEASUREMENT',
      topic='A',source_ids=r['source_ids'],principal_originals_added=['L121'],original_intake_added=0,new_question_credit=0,
      prior_eight_original_admission=next(z for z in load(H/'baseline/papers/topic-a/latest.json').values()if isinstance(z,dict)and z.get('path')=='audit/topic-a/v3/admission.json'),
      new_scientific_admission=science,numerical_author=packets['numbers'],numerical_distinct_review=packets['numerical_review'],
      numerical_root_adoption=packets['numerical_root_adoption'],frozen_payloads=payload(['numbers','numerical_review','numerical_root_adoption']),
      measurement=mapped('topic_A_L121_measurement_results/results.json'),reader=mapped('topic_A_L121_measurement_results/reader.pdf'),
      input_author=mapped('topic_A_L121_measurement_results/inputs/input/manifest.json'),
      input_distinct_review=mapped('topic_A_L121_measurement_results/inputs/input_review/manifest.json'),
      input_root_adoption=mapped('topic_A_L121_measurement_results/inputs/input_adoption/manifest.json'),
      primary_coordinate=r['primary_coordinate'],primary=x['written'],conditionals=x['conditional'],
      source_sum=x['source_sum'],whole_common=x['whole_common'],application_sum=x['application_sum'],whole_written=x['whole_written'],
      source_pages=131,whole_common_pages=23,whole_application_pages=56,source_dispositions=129,
      coordinates=30,exact_fractions=300,old_conditionals_preserved=240,
      whole_raw_files=45,required_program_or_data_files=20,auxiliaries=3,operational_runners=6,partial_Lean_modules=15,
      formal_dependency_manifests=1,new_partial_declarations=6,whole_source_formalized=False,
      old_printed_appendices_pages=30,old_printed_appendices_required_files=11,
      complete_enlarged_printed_program_representation=None,symmetric_program_exclusion=True,
      software_inclusive_factor=None,historical_source_software_cost=None,full_graphic_cost=None,
      all_existing_scientific_bytes_unchanged=True,
      role_disclosure='Root assembled L121; rewrite_termination independently reviewed its assembly and input counts, then authored the new numerical packet. Enumeration_volume independently reviewed the new numerical derivation; root adopted it. Historical roles remain explicit.'))
    pointer=load(H/'topic_pointer_proposal.json');pointer.update(status='CURRENT_ACCEPTED_NINE_ORIGINAL_A_CONTRACTS_AND_SYMMETRIC_MEASUREMENT',
      admission=a,reader=mapped('topic_A_L121_measurement_results/reader.pdf'),measurement=mapped('topic_A_L121_measurement_results/results.json'))
    for row in pointer['catalogue_entries']:row['status']='ROOT_ADMITTED_CURRENT_EDITION'
    write('papers/topic-a/latest.json',pointer)
    cat=load(H/'proposed/papers/catalogue.json')
    for row in cat['new_editions']:
        if row['id']=='topic-a/extensions/locally-toroidal/v1/application':row['status']='ROOT_ADMITTED_CURRENT_EDITION'
    write('papers/catalogue.json',cat)
    active=load(H/'proposed/audit/corpus/active_catalogue.json')
    active['status']='CURRENT_ACCESSIBLE106_CATALOGUE_51_MEASURED_54_MATHEMATICAL_PENDING_1_EDITORIAL'
    active['previous_catalogue']=load(H/'baseline/audit/corpus/latest.json')['active_catalogue']
    if'recovery_snapshot'in active:active['prior_recovery_snapshot']=active.pop('recovery_snapshot')
    for row in active['entries']:
        if row['original_id']=='L121':
            row['current_principal_recovery']['status']='ROOT_ADMITTED_COMPLETE_CORRECTED_PRINCIPAL_CONTRACT'
            row['current_principal_recovery']['latest_admission_references']=[science,a]
        if row['original_id']=='L022':
            row['current_principal_recovery']['latest_admission_references']=[editorial]
    ac=write('audit/corpus/accessible106/updates/l121-editorial-catalogue.json',active)
    corpus=load(H/'proposed/audit/corpus/next.json')
    for k in ['snapshot','proposal_only','future_snapshot_path','pending_root_bindings']:corpus.pop(k,None)
    corpus.update(status='CURRENT_PROGRAMME_51_MEASURED_54_MATHEMATICAL_PENDING_1_EDITORIAL',previous_snapshot=history['audit/corpus/latest.json'],active_catalogue=ac)
    corpus['added_admissions'].append(science);corpus['added_measurements'].append(a);corpus['current_topic_replacements'].append(a)
    corpus['editorial_dispositions']=[editorial]
    snap=write('audit/corpus/updates/accessible106-l121-measured-editorial.json',corpus)
    corpus['snapshot']=snap;write('audit/corpus/latest.json',corpus)
    latest=load(H/'proposed/papers/latest_catalogue.json');latest['status']='CURRENT_MANUSCRIPT_CATALOGUE_51_MEASURED_WITH_EDITORIAL_DISPOSITION'
    latest['previous_catalogue']=history['papers/latest_catalogue.json'];latest['active_source_catalogue']=ac
    z=latest['unified_A_current_edition'];z.pop('future_admission',None);z['admission']=a
    for row in latest['entries']:
        if row.get('source_contracts')==['L121']:row['status']='ROOT_ADMITTED_CURRENT_EDITION'
    write('papers/latest_catalogue.json',latest)
    write('audit/programme51/v1/proposed_history_routes.json',dict(routes=history,
      old_nonmain_functions_preserved=True,old_nonmain_function_count=len(baseline['prior_nonmain_verifier_ASTs']),
      historical_current_guards=['check_unified_a_current_admission','check_programme50','check_lcd_overview50'],
      root_action='Add a historical wrapper using these exact pointer bytes and separate new current calls; do not alter old function ASTs.'))
    generated=[]
    for f in sorted((H/'wrappers').rglob('*')):
        if f.is_file():generated.append(dict(proposal_path=str(f.relative_to(H)),public_path=str(f.relative_to(H/'wrappers')),bytes=f.stat().st_size,sha256=sha(f.read_bytes())))
    (H/'wrapper_routes.json').write_text(json.dumps(dict(status='PRIVATE_ROOT_REVIEWABLE_PROPOSED_PUBLIC_FILES',files=generated,public_files_written=False,
      source_packets_immutable=True,overview17_separately_authored=True),indent=2)+'\n')
    print(json.dumps(dict(wrappers=len(generated),science_admission=science,current_A_admission=a,corpus_snapshot=snap,active_catalogue=ac)))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);main(p.parse_args().study_root)
