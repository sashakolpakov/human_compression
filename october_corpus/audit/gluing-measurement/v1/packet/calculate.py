#!/usr/bin/env python3
"""Exact complete-document comparisons from accepted Gluing input counts."""
from pathlib import Path
from fractions import Fraction
import hashlib, json

PINS={'inputs':'7f7cc0dc06b772ca150535d53d0a4d20799255da6e447dffa8e88a25f32d5306',
      'input_review':'0b82b7ba065bacb6ccfac7515667503617c57ec0db1f810a064dcf23468be9c1'}
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
FORMS=['NFC','NFKC'];VARIANTS=['raw_untrimmed','raw_selected','calibrated_selected']
def need(c,m):
    if not c:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def bind(root,pin):
    need(sha(root/'manifest.json')==pin,'exact accepted input manifest')
    for row in read(root/'manifest.json')['exports']:
        p=Path(row['path']);need(not p.is_absolute() and '..' not in p.parts,'relative export')
        f=root/p;need(f.stat().st_size==row['bytes'] and sha(f)==row['sha256'],'bound input export '+str(p))
def fraction(n,d):
    need(n>0 and d>0,'positive whole-document length');f=Fraction(n,d)
    return dict(numerator=n,denominator=d,reduced_numerator=f.numerator,reduced_denominator=f.denominator,decimal=f'{float(f):.12f}')

def validate_inputs(policy,counts,independent,review):
    need(review['status']=='ACCEPTED_COMPLETE_INPUT_BOUNDARY_WITH_RECORDED_LIMITS' and review['author_manifest_sha256']==PINS['inputs'],'distinct input acceptance')
    need(policy['units']==UNITS and policy['normalizations']==FORMS and policy['variants']==VARIANTS,'fixed coordinates')
    need(policy['source_id']=='L010' and policy['source_rows']==23 and policy['original_manuscripts']==1,'one complete source contract')
    need(list(counts['documents'])==['L010','U1','U2','A1','CODE'],'all complete documents')
    need([counts['documents'][k]['pages'] for k in counts['documents']]==[15,5,6,5,4],'complete source and replacement pages')
    need(policy['whole_common_papers_charged'] is True and policy['existing_B_common_is_not_a_prerequisite'] is True and policy['cross_topic_discount'] is False,'whole common closure')
    need(policy['all_declared_code_prepurchased_for_conditional_results'] is True and policy['raw_and_printed_code_are_alternatives'] is True,'complete conditional acquisition and alternative representations')
    need(policy['principal_required_programs']==0 and policy['validation_programs']==3,'no finite premises')
    need([len(policy[k])for k in ('programs','drivers','formal')]==[3,3,2],'all eight raw files')
    need(all(r['role']=='finite_validation' and r['uniform_mathematical_premise'] is False for r in policy['programs']),'sample roles remain validation')
    need(policy['whole_source_formalized'] is False and policy['partial_formal_declarations']==10,'scoped formal boundary')
    need(policy['unknown_costs']==dict(full_graphics=None,historical_software=None,retained_external_proofs=None,full_formalization=None),'unknown costs remain null')
    need(policy['ratio'] is None and counts['ratio'] is None,'input packet contains no factor')
    for k,v in counts['documents'].items():
        need(v['metrics']==independent['documents'][k]['metrics'] and v['pdf_sha256']==independent['documents'][k]['pdf_sha256'],'independent PDF recount '+k)
    for kind,files in counts['raw_files'].items():
        need(set(files)=={r['path']for r in policy[kind]},'complete raw inventory')
        for name,v in files.items():need(v['metrics']==independent['raw_files'][kind][name]['metrics'],'independent raw recount')

def calculate(inputs,input_review):
    bind(inputs,PINS['inputs']);bind(input_review,PINS['input_review'])
    policy=read(inputs/'policy.json');counts=read(inputs/'author_counts.json');independent=read(input_review/'recount.json');review=read(input_review/'review.json')
    validate_inputs(policy,counts,independent,review)
    rows=[]
    for variant in VARIANTS:
        for form in FORMS:
            for unit in UNITS:
                costs={k:v['metrics'][variant][form][unit]for k,v in counts['documents'].items()}
                raw={k:sum(v['metrics'][form][unit]for v in files.values())for k,files in counts['raw_files'].items()}
                u=costs['U1']+costs['U2'];written=u+costs['A1'];source=costs['L010']
                rows.append(dict(variant=variant,normalization=form,unit=unit,costs=costs,raw_costs=raw,
                    totals=dict(source=source,common=u,applications=costs['A1'],written=written,with_printed_programs=written+costs['CODE'],with_raw_programs=written+raw['programs']),
                    comparisons=dict(written=fraction(source,written),including_printed_programs=fraction(source,written+costs['CODE']),including_raw_programs=fraction(source,written+raw['programs']),conditional_application=fraction(source,costs['A1'])),
                    conditional_acquisition=dict(whole_common_papers=['U1','U2'],common_cost=u,printed_program_package=costs['CODE'],raw_program_package_alternative=raw['programs'],complete_local_application=costs['A1'])))
    primary=next(r for r in rows if (r['variant'],r['normalization'],r['unit'])==('calibrated_selected','NFC','characters_without_whitespace'))
    result=dict(status='AUTHOR_NUMERICAL_CANDIDATE_PENDING_DISTINCT_ROOT_REVIEW',input_manifests=PINS,
        source_ids=['L010'],source_records=23,whole_documents=['L010','U1','U2','A1','CODE'],physical_pages=[15,5,6,5,4],
        coordinate_count=30,exact_fraction_count=120,combined_fractions=90,conditional_fractions=30,coordinates=rows,primary=primary,
        boundary=dict(whole_common_once=['U1','U2'],whole_application=True,old_B_common_imported=False,cross_topic_discount=False,
            whole_validation_programs=3,uniform_finite_program_premises=0,
            program_representations='Complete four-page appendix or three whole raw files, never both.',
            conditional='After both entire common papers and all three complete declared programs have been acquired; validation is not a premise of the uniform proofs.',
            separate_drivers=3,separate_formal_files=2,partial_Lean_declarations=10,whole_source_formalized=False,
            unknown_costs=policy['unknown_costs'],source_qualification='Full original length is charged. Recovery follows the23 accepted dispositions; the historical numerical sequence and unused preliminaries are not claimed newly proved.',
            interpretation='Lengths of complete available texts in fixed representations; not minimum proof complexity, total effort or a pooled factor.',
            retained_inputs=['Endpoint sesquiextension theorem, via source Proposition2.2.','Classical end-parabolic criterion, via source Proposition2.3.']),
        author_role='enumeration_review authored this arithmetic/reader and previously independently reviewed the input packet. Distinct numerical review is required; scientific acceptance remains root authority.',
        new_source_credit=0,new_question_credit=0,new_formal_credit=0,primary_material_exported=False)
    validate_result(result);return result

def validate_result(result):
    rows=result['coordinates'];need(len(rows)==30,'all thirty coordinates')
    need({(r['variant'],r['normalization'],r['unit'])for r in rows}=={(v,n,u)for v in VARIANTS for n in FORMS for u in UNITS},'unique complete coordinate set')
    for r in rows:
        c=r['costs'];raw=r['raw_costs'];u=c['U1']+c['U2'];w=u+c['A1'];s=c['L010']
        need(r['totals']==dict(source=s,common=u,applications=c['A1'],written=w,with_printed_programs=w+c['CODE'],with_raw_programs=w+raw['programs']),'whole denominator accounting')
        for name,d in [('written',w),('including_printed_programs',w+c['CODE']),('including_raw_programs',w+raw['programs']),('conditional_application',c['A1'])]:
            need(r['comparisons'][name]==fraction(s,d),'exact fraction '+name)
        need(r['conditional_acquisition']==dict(whole_common_papers=['U1','U2'],common_cost=u,printed_program_package=c['CODE'],raw_program_package_alternative=raw['programs'],complete_local_application=c['A1']),'both common papers and whole code acquired')
    need(result['primary']==next(r for r in rows if (r['variant'],r['normalization'],r['unit'])==('calibrated_selected','NFC','characters_without_whitespace')),'fixed primary coordinate')
    need(result['boundary']['unknown_costs']==dict(full_graphics=None,historical_software=None,retained_external_proofs=None,full_formalization=None),'no zero unknowns')
    need(result['boundary']['uniform_finite_program_premises']==0 and result['boundary']['whole_validation_programs']==3,'code role')
    need(result['boundary']['separate_drivers']==3 and result['boundary']['separate_formal_files']==2 and result['boundary']['partial_Lean_declarations']==10,'operational/formal separate')
    need((result['coordinate_count'],result['exact_fraction_count'],result['combined_fractions'],result['conditional_fractions'])==(30,120,90,30),'exact count summary')
    need(all(result[k]==0 for k in ('new_source_credit','new_question_credit','new_formal_credit')),'zero new credits')
