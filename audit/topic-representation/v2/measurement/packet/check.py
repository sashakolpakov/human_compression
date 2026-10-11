#!/usr/bin/env python3
"""Author arithmetic and scope controls; independent input counts are retained."""
import argparse, copy, csv, json, math
from pathlib import Path
from compute import PINS, UNITS, VARIANTS, FORMS, RAW, ORDER, CONDITION, arguments, inputs, derive, need, read, write, csv_rows

def validate(r, counts, policy, boundary, bindings):
    need(r['coordinate_count']==len(r['coordinates'])==30, 'all thirty coordinates')
    need(r['comparison_order']==ORDER, 'written, conditional and validation comparisons')
    need(r['whole_common_once'] and r['whole_application'] and not r['cross_topic_discount'], 'whole common and application')
    need(r['conditional_prepaid']==CONDITION, 'whole common and validation acquisition')
    need(r['source_to_application_sequence']==[dict(source='F010',application='R1',source_pages=13,application_pages=5)], 'complete source/app pair')
    need(r['source_contract_rows']==6 and r['accepted_proof_contexts']==13 and r['principal_contracts_unchanged']==1, 'unchanged source scope')
    need(r['source_qualifications']==boundary['source_qualifications'] and r['source_exclusions']==boundary['exclusions'], 'all qualifications/exclusions')
    need(r['original_authors']==boundary['attribution'], 'exact original author attribution')
    need(r['input_bindings']==bindings, 'exact accepted/current bindings')
    expected=dict(complete_validation_programs=2,uniform_finite_proof_premises=0,
                  primary_representation='Whole4-page printed appendix counted once',
                  alternative_representation='Both complete raw files summed per file, never added to the appendix',
                  complete_operational_drivers_separate=2,complete_Lean_files_separate=2,
                  prior_partial_Lean_declarations=12,formal_generic=8,formal_reused_local=4,
                  full_application_formalized=False,drivers_added_to_comparisons=False,Lean_added_to_comparisons=False)
    need(r['program_boundary']==expected, 'validation and partial formal boundary')
    need(r['raw_file_inventory']=={k:counts[k] for k in RAW}, 'all six whole separate files')
    need(r['physical_pages']==dict(source=13,common=5,application=5,written_replacement=10,printed_validation=4,total_inputs=27), 'all physical pages')
    for k in ['retained_external_proof_cost','historical_program_cost','graphics_and_formula_layout_cost','operational_engineering_cost','minimal_mathematical_complexity']:
        need(r[k] is None, 'unknown not zero: '+k)
    for k in ['full_visible_graphical_text_claim','sawtooth_claim','primary_text_fonts_images_exported']:
        need(r[k] is False, 'bounded claim: '+k)
    need(r['new_source_credit']==r['new_question_credit']==r['new_formal_credit']==0, 'no new result credit')
    need(r['source_question_answer']=='Original Theorem A already answers Question2.4; no new answer.', 'original question answer attribution')
    fractions=0
    for c,(v,n,u) in zip(r['coordinates'],[(v,n,u) for v in VARIANTS for n in FORMS for u in UNITS]):
        need((c['variant'],c['normalization'],c['unit'])==(v,n,u), 'coordinate order')
        costs={k:row['variants'][v][n][u] for k,row in counts['documents'].items()}
        raw={k:sum(row['metrics'][n][u] for row in counts[k].values()) for k in RAW}
        need(c['document_costs']==costs and c['raw_costs']==raw, 'whole PDF and raw costs')
        source=costs['F010'];written=costs['U_R']+costs['R1']
        need(c['source_sum']==source and c['written_denominator']==written, 'full written denominator')
        need(c['acquired_common']==costs['U_R'] and c['acquired_printed_validation']==costs['CODE'] and c['acquired_raw_validation_alternative']==raw['complete_validation_programs'], 'explicit acquisition costs')
        denoms=dict(written_papers=written,conditional_application=costs['R1'],
                    including_printed_validation=written+costs['CODE'],
                    including_raw_validation_alternative=written+raw['complete_validation_programs'])
        need(list(c['comparisons'])==ORDER, 'comparison identities and order')
        for name,den in denoms.items():
            g=math.gcd(source,den);num0,den0=source//g,den//g
            exact=str(num0) if den0==1 else str(num0)+'/'+str(den0)
            need(c['comparisons'][name]==dict(numerator=source,denominator=den,reduced_numerator=num0,reduced_denominator=den0,exact_fraction=exact,decimal=f'{source/den:.12f}'), 'exact fraction '+name)
            fractions+=1
    need(r['primary']==r['coordinates'][22], 'calibrated NFC nonspace primary')
    need(r['exact_fraction_count']==fractions==120 and r['combined_exact_fractions']==90 and r['conditional_exact_fractions']==30, '120 exact comparisons')
    need(r==derive(counts,policy,boundary,bindings), 'complete deterministic result')
    return dict(coordinates=30,exact_fractions=120,combined=90,conditional=30,pdf_cells=120,separate_raw_cells=60)

def main():
    p=argparse.ArgumentParser();arguments(p);p.add_argument('--results-dir',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(), 'fresh output')
    args=inputs({k:getattr(a,k) for k in PINS},a.public_root);r=read(a.results_dir/'results.json');summary=validate(r,*args)
    with (a.results_dir/'comparisons.csv').open(newline='') as f:actual=list(csv.DictReader(f))
    need(actual==[{k:str(v) for k,v in row.items()} for row in csv_rows(r)], 'all120 exact CSV rows')
    need(read(a.results_dir/'input_bindings.json')==args[3], 'companion bindings')
    controls=[]
    def reject(name,change):
        x=copy.deepcopy(r);change(x)
        try:validate(x,*args)
        except ValueError as e:controls.append(dict(name=name,rejected=True,reason=str(e)))
        else:raise ValueError('accepted corruption '+name)
    reject('drop_common',lambda x:x['coordinates'][0]['comparisons']['written_papers'].update(denominator=x['coordinates'][0]['document_costs']['R1']))
    reject('drop_application',lambda x:x['coordinates'][0].update(written_denominator=x['coordinates'][0]['document_costs']['U_R']))
    reject('omit_whole_validation_file',lambda x:x['raw_file_inventory']['complete_validation_programs'].pop('phase177_hexagon_check.g'))
    reject('drop_printed_validation',lambda x:x['coordinates'][0]['comparisons']['including_printed_validation'].update(denominator=x['coordinates'][0]['written_denominator']))
    reject('charge_both_code_representations',lambda x:x['coordinates'][0]['comparisons']['including_raw_validation_alternative'].update(denominator=x['coordinates'][0]['written_denominator']+x['coordinates'][0]['document_costs']['CODE']+x['coordinates'][0]['raw_costs']['complete_validation_programs']))
    reject('add_drivers_silently',lambda x:x['coordinates'][0]['comparisons']['written_papers'].update(denominator=x['coordinates'][0]['written_denominator']+x['coordinates'][0]['raw_costs']['complete_operational_drivers']))
    reject('wrong_reduced_fraction',lambda x:x['coordinates'][0]['comparisons']['written_papers'].update(reduced_denominator=1))
    reject('wrong_conditional_denominator',lambda x:x['coordinates'][0]['comparisons']['conditional_application'].update(denominator=x['coordinates'][0]['document_costs']['U_R']))
    reject('hide_acquisition',lambda x:x.update(conditional_prepaid='Only the application is charged.'))
    reject('cross_topic_discount',lambda x:x.update(cross_topic_discount=True))
    reject('validation_as_uniform_proof',lambda x:x['program_boundary'].update(uniform_finite_proof_premises=2))
    reject('full_application_Lean',lambda x:x['program_boundary'].update(full_application_formalized=True))
    reject('double_formal_credit',lambda x:x['program_boundary'].update(prior_partial_Lean_declarations=24))
    reject('external_cost_zero',lambda x:x.update(retained_external_proof_cost=0))
    reject('graphic_cost_zero',lambda x:x.update(graphics_and_formula_layout_cost=0))
    reject('erase_source_qualification',lambda x:x['source_qualifications'].pop())
    reject('source_question_credit',lambda x:x.update(new_question_credit=1))
    reject('new_source_credit',lambda x:x.update(new_source_credit=1))
    reject('claimed_sawtooth',lambda x:x.update(sawtooth_claim=True))
    reject('full_graphic_text_claim',lambda x:x.update(full_visible_graphical_text_claim=True))
    reject('wrong_primary',lambda x:x.update(primary=x['coordinates'][0]))
    reject('omit_coordinate',lambda x:x['coordinates'].pop())
    reject('source_page_omission',lambda x:x['physical_pages'].update(source=12))
    reject('wrong_original_authors',lambda x:x['original_authors'].update(authors=['anonymous']))
    a.out.parent.mkdir(parents=True,exist_ok=True);write(a.out,dict(status='PASS_AUTHOR_ARITHMETIC_AND_BOUNDARY_CONTROLS',counts=summary,controls=controls,control_count=len(controls),source_extraction_repeated=False,scientific_computation_repeated=False,independent_arithmetic_review=False,input_manifest_sha256=PINS))
    print(json.dumps(dict(status='PASS',**summary,controls=len(controls))))

if __name__=='__main__':main()
