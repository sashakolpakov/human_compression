#!/usr/bin/env python3
"""Author arithmetic and boundary checks; independent review remains separate."""
import argparse,copy,csv,json
from fractions import Fraction
from pathlib import Path
from compute import HERE,VARIANTS,FORMS,UNITS,PREPAID,inputs,derive,tables,need,sha

def validate(result,counted,spec):
    need(result['policy_coordinates']==len(result['coordinates'])==30,'all thirty policy coordinates')
    need(result['whole_common_paper_charged_once'] is True and result['complete_application_charged'] is True and
         result['cross_topic_common_discount'] is False,'whole theory and application, no cross-topic discount')
    need(result['conditional_prepaid']==PREPAID,'explicit full conditional acquisition')
    need(result['program_boundary']==dict(required_complete_files=6,printed_appendix_pages=8,
         embedded_diagnostics_included=True,raw_alternative_not_additional=True,raw_metrics_summed_per_file=True,
         auxiliary_files_separate=3,formal_files_separate=3,auxiliary_and_formal_not_silently_added=True),
         'full program, auxiliary and formal boundary')
    for field in ['complete_mathematical_programs','complete_auxiliary_scripts','complete_formal_files','auxiliary_list_discrepancy']:
        need(result[field]==spec[field],'unchanged complete files and roles')
    need(result['physical_pages']==dict(source=17,common=7,application=9,scientific_replacement=16,printed_program=8,total_input_pages=41),
         'whole physical manuscripts and appendix')
    need(result['source_ids']==['L012'] and result['application_ids']==['AF1'] and result['source_contract_rows']==33 and
         result['existing_principal_contracts']==1 and result['project_total_preserved']==27,'fixed principal contract')
    need(all(result[field] is None for field in ['retained_external_proof_cost','catalogue_and_algorithm_construction_cost',
         'historical_software_cost','graphics_and_formula_layout_cost','minimal_mathematical_complexity']), 'unknown costs')
    need(all(result[field] is False for field in ['full_visible_text_claim','formal_source_application_claim','paired_dependency_audit_complete']) and
         all(result[field]==0 for field in ['new_source_credit','new_question_credit','new_formal_credit']), 'no new or inflated scientific scope')
    count=0
    for row,coordinate in zip(result['coordinates'],[(v,f,m) for v in VARIANTS for f in FORMS for m in UNITS]):
        v,f,m=coordinate
        need((row['variant'],row['normalization'],row['unit'])==coordinate,'fixed coordinate order')
        costs={key:value['variants'][v][f][m] for key,value in counted['documents'].items()}
        raw={group:sum(value['variants'][f][m] for value in records.values()) for group,records in counted['raw_records'].items()}
        source,common,application,code=(costs[key] for key in ['L012','U_Affine','AF1','CODE'])
        expected={'document_costs':costs,'source_sum':source,'common_theory':common,'all_applications':application,
                  'written_denominator':common+application,'printed_program_cost':code,'raw_program_cost':raw['complete_programs'],
                  'separate_auxiliary_cost':raw['complete_auxiliary_scripts'],'separate_formal_cost':raw['complete_formal_files']}
        need(all(row[key]==value for key,value in expected.items()),'complete document or file costs')
        def check_fraction(value,numerator,denominator):
            q=Fraction(numerator,denominator)
            need(value==dict(numerator=numerator,denominator=denominator,reduced_numerator=q.numerator,
                 reduced_denominator=q.denominator,exact_fraction=str(q),factor=float(q)), 'exact complete fraction')
        denominators={'written_papers':common+application,'including_printed_program':common+application+code,
                      'including_raw_program_alternative':common+application+raw['complete_programs']}
        need(set(row['comparisons'])==set(denominators),'three program representations')
        for key,denominator in denominators.items():
            check_fraction(row['comparisons'][key],source,denominator);count+=1
        need(len(row['per_result'])==1,'one complete conditional result')
        item=row['per_result'][0]
        need(item['source']=='L012' and item['application']=='AF1' and item['source_cost']==source and
             item['application_cost']==application,'complete matched pair')
        check_fraction({key:item[key] for key in ['numerator','denominator','reduced_numerator','reduced_denominator','exact_fraction','factor']},source,application)
        count+=1
    need(result['primary']==result['coordinates'][22],'calibrated NFC primary coordinate')
    need((result['exact_combined_fractions'],result['exact_conditional_fractions'],count)==(90,30,120),'all exact fractions')
    return dict(PDF_metric_cells=120,raw_program_cells=60,separate_auxiliary_cells=30,separate_formal_cells=30,
                combined_fractions=90,conditional_fractions=30)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--results-dir',type=Path,default=HERE)
    parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(),'fresh report')
    counted,spec=inputs();result=json.loads((args.results_dir/'results.json').read_text())
    summary=validate(result,counted,spec)
    need({k:v for k,v in result.items() if k!='bindings'}==derive(counted,spec),'deterministic derivation')
    for name,value in result['bindings'].items():need(sha(HERE/name)==value,'exact numerical input binding')
    for name,rows in zip(['overall_costs.csv','conditional_costs.csv'],tables(result)):
        with (args.results_dir/name).open(newline='') as stream:actual=list(csv.DictReader(stream))
        need(actual==[{k:str(v) for k,v in row.items()} for row in rows],'all CSV values')
    mutations=[
        ('omit_common',lambda r:r['coordinates'][0].update(common_theory=0)),
        ('omit_application',lambda r:r['coordinates'][0].update(all_applications=0)),
        ('omit_program',lambda r:r['complete_mathematical_programs'].pop()),
        ('incorrect_fraction',lambda r:r['coordinates'][0]['comparisons']['written_papers'].update(exact_fraction='12')),
        ('double_program_charge',lambda r:r['coordinates'][0]['comparisons']['including_raw_program_alternative'].update(denominator=1)),
        ('wrong_pair',lambda r:r['coordinates'][0]['per_result'][0].update(application='other')),
        ('hide_acquisition',lambda r:r.update(conditional_prepaid='None')),
        ('cross_topic_discount',lambda r:r.update(cross_topic_common_discount=True)),
        ('prune_diagnostics',lambda r:r['program_boundary'].update(embedded_diagnostics_included=False)),
        ('missing_auxiliary',lambda r:r['complete_auxiliary_scripts'].pop()),
        ('outside_cost_zero',lambda r:r.update(retained_external_proof_cost=0)),
        ('historical_software_zero',lambda r:r.update(historical_software_cost=0)),
        ('formal_overclaim',lambda r:r.update(formal_source_application_claim=True)),
        ('new_question_credit',lambda r:r.update(new_question_credit=1)),
        ('wrong_primary',lambda r:r.update(primary=r['coordinates'][0])),
        ('wrong_coordinate',lambda r:r['coordinates'][0].update(normalization='NFKC'))]
    controls=[]
    for name,change in mutations:
        altered=copy.deepcopy(result);change(altered)
        try:validate(altered,counted,spec)
        except ValueError as error:controls.append(dict(name=name,rejected=True,reason=str(error)))
        else:raise ValueError('missed corruption '+name)
    report=dict(status='PASS_AUTHOR_ARITHMETIC_AND_BOUNDARIES',summary=summary,controls=controls,
                independent_numerical_review=False,primary_reextraction_repeated=False,
                group_or_formal_replay_repeated=False,new_source_credit=0,new_question_credit=0)
    args.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(summary))

if __name__=='__main__':main()
