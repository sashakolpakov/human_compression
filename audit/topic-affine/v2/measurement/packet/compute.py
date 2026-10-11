#!/usr/bin/env python3
"""Affine manuscript costs from independently accepted complete inputs."""
import argparse
import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
VARIANTS = ('raw_untrimmed', 'raw_selected', 'calibrated_selected')
FORMS = ('NFC', 'NFKC')
UNITS = ('whitespace_tokens', 'alphanumeric_units', 'characters_without_whitespace',
         'characters_with_collapsed_whitespace', 'utf8_bytes_with_collapsed_whitespace')
PINS = {'inputs': '4f322184f2d3d67abfc29841567b51b984e7f6d28788b9e3a475faa0c18ae911',
        'independent': 'd9556ea69402dd827426fe3c204aa9eb5895f7b342d58e22644c9283383ec2af'}
PREPAID = 'The whole U_Affine and all six complete required programs have already been acquired.'

def need(ok, message):
    if not ok:
        raise ValueError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text())

def inputs(root=HERE):
    for folder, pin in PINS.items():
        base = root/folder
        need(sha(base/'manifest.json') == pin, 'exact accepted input or review manifest')
        for row in read(base/'manifest.json')['exports']:
            path = base/row['path']
            need(path.stat().st_size == row['bytes'] and sha(path) == row['sha256'], 'frozen export '+row['path'])
    review = read(root/'independent/review.json')
    need(review['status'] == 'ACCEPTED_ROOT_INDEPENDENT_AFFINE_MEASUREMENT_INPUTS' and
         review['proposal_manifest_sha256'] == PINS['inputs'] and not review['requested_corrections'],
         'independently accepted unchanged inputs')
    author = read(root/'inputs/author_counts.json')
    counted = read(root/'independent/recount.json')
    need(set(author['documents']) == set(counted['documents']) == {'L012','U_Affine','AF1','CODE'}, 'four whole PDFs')
    for key, value in counted['documents'].items():
        original = author['documents'][key]
        need(value['variants'] == original['variants'] and value['pdf_sha256'] == original['pdf_sha256'] and
             value['pages'] == original['pages'], 'independent complete document count '+key)
    for group, rows in counted['raw_records'].items():
        need(set(rows) == set(author[group]), 'full file inventory '+group)
        for name, value in rows.items():
            original = author[group][name]
            need(value['variants'] == original['metrics'] and value['sha256'] == original['sha256'] and
                 value['bytes'] == original['bytes'], 'independent complete file count '+name)
    return counted, read(root/'inputs/replacement_input_spec.json')

def fraction(numerator, denominator):
    value = Fraction(numerator, denominator)
    return dict(numerator=numerator, denominator=denominator,
                reduced_numerator=value.numerator, reduced_denominator=value.denominator,
                exact_fraction=str(value), factor=float(value))

def derive(counted, spec):
    coordinates = []
    for variant in VARIANTS:
        for form in FORMS:
            for unit in UNITS:
                costs = {key:row['variants'][variant][form][unit] for key,row in counted['documents'].items()}
                files = {group:sum(row['variants'][form][unit] for row in rows.values())
                         for group,rows in counted['raw_records'].items()}
                source, common, application, code = (costs[key] for key in ('L012','U_Affine','AF1','CODE'))
                coordinates.append(dict(
                    variant=variant, normalization=form, unit=unit, document_costs=costs,
                    source_sum=source, common_theory=common, all_applications=application,
                    written_denominator=common+application, printed_program_cost=code,
                    raw_program_cost=files['complete_programs'],
                    separate_auxiliary_cost=files['complete_auxiliary_scripts'],
                    separate_formal_cost=files['complete_formal_files'],
                    comparisons={
                        'written_papers': fraction(source, common+application),
                        'including_printed_program': fraction(source, common+application+code),
                        'including_raw_program_alternative': fraction(source, common+application+files['complete_programs'])},
                    per_result=[dict(source='L012', application='AF1', source_cost=source,
                                     application_cost=application, **fraction(source, application))]))
    return dict(
        schema='affine_complete_document_measurement_v1', status='AUTHOR_ARITHMETIC_PENDING_INDEPENDENT_REVIEW',
        public_scientific_commit='1eb5745123e610459f413a3473ec7b0029591843',
        public_proof_admission_sha256='23a61a1e913943c4a68234a5af31f2da7fadd6b123a1cd5788f64baf24dd4695',
        primary=coordinates[22], coordinates=coordinates, policy_coordinates=30,
        exact_combined_fractions=90, exact_conditional_fractions=30,
        source_ids=['L012'], application_ids=['AF1'], source_contract_rows=33,
        existing_principal_contracts=1, project_total_preserved=27,
        comparison_order=['written_papers','per_result_conditional','including_printed_program','including_raw_program_alternative'],
        whole_common_paper_charged_once=True, complete_application_charged=True,
        cross_topic_common_discount=False, conditional_prepaid=PREPAID,
        program_boundary=dict(required_complete_files=6, printed_appendix_pages=8,
                              embedded_diagnostics_included=True, raw_alternative_not_additional=True,
                              raw_metrics_summed_per_file=True, auxiliary_files_separate=3,
                              formal_files_separate=3, auxiliary_and_formal_not_silently_added=True),
        complete_mathematical_programs=spec['complete_mathematical_programs'],
        complete_auxiliary_scripts=spec['complete_auxiliary_scripts'],
        complete_formal_files=spec['complete_formal_files'],
        auxiliary_list_discrepancy=spec['auxiliary_list_discrepancy'],
        physical_pages=dict(source=17,common=7,application=9,scientific_replacement=16,printed_program=8,total_input_pages=41),
        raw_file_bytes={group:sum(row['bytes'] for row in rows.values()) for group,rows in counted['raw_records'].items()},
        retained_external_proof_cost=None, catalogue_and_algorithm_construction_cost=None,
        historical_software_cost=None, graphics_and_formula_layout_cost=None,
        minimal_mathematical_complexity=None, full_visible_text_claim=False,
        formal_source_application_claim=False, paired_dependency_audit_complete=False,
        source_scope='Whole source cost for the admitted principal contract. General Problem 1.1, the separate full Table 1 census and the exactly-two-order-384-seed uniqueness assertion remain excluded.',
        new_source_credit=0, new_question_credit=0, new_formal_credit=0)

def tables(results):
    combined, conditional = [], []
    for row in results['coordinates']:
        key = {name:row[name] for name in ('variant','normalization','unit')}
        for representation, value in row['comparisons'].items():
            code = 0 if representation == 'written_papers' else row['printed_program_cost'] if representation == 'including_printed_program' else row['raw_program_cost']
            combined.append(dict(**key, representation=representation, source_cost=row['source_sum'],
                                 whole_common=row['common_theory'], application_cost=row['all_applications'],
                                 program_cost=code, **value))
        conditional.append(dict(**key, **row['per_result'][0], prepaid=results['conditional_prepaid']))
    return combined, conditional

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(), 'fresh output directory')
    results = derive(*inputs())
    results['bindings'] = {name:sha(HERE/name) for name in
        ['inputs/manifest.json','inputs/policy.json','inputs/author_counts.json','inputs/replacement_input_spec.json',
         'inputs/source_contract_boundary.json','independent/manifest.json','independent/review.json',
         'independent/recount.json','compute.py']}
    args.out.mkdir(parents=True)
    (args.out/'results.json').write_text(json.dumps(results, indent=2)+'\n')
    for name, rows in zip(['overall_costs.csv','conditional_costs.csv'], tables(results)):
        with (args.out/name).open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
            writer.writeheader(); writer.writerows(rows)
    print(json.dumps(dict(primary=results['primary'], combined_fractions=90, conditional_fractions=30)))

if __name__ == '__main__':
    main()
