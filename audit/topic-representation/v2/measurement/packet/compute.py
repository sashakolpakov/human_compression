#!/usr/bin/env python3
"""Complete Representation comparisons from accepted counts; no PDF extraction."""
import argparse, csv, hashlib, json
from fractions import Fraction
from pathlib import Path

PINS = {
    'inputs': '122820fac69c94d484444a88b4318fa7ae1a588770c4378737af7d457a037af1',
    'input_review': 'd9b130046c95f625946762a4414fc294d2366e5bed3803aae783bb43967b69f3',
    'input_adoption': 'c6cd89907ac02b7384fb887e93e3d4f941dcab2f963cc9156341cbeb5b2a24c5',
}
UNITS = ['whitespace_tokens', 'alphanumeric_units', 'characters_without_whitespace',
         'characters_with_collapsed_whitespace', 'utf8_bytes_with_collapsed_whitespace']
VARIANTS = ['raw_untrimmed', 'raw_selected', 'calibrated_selected']
FORMS = ['NFC', 'NFKC']
RAW = ['complete_validation_programs', 'complete_operational_drivers', 'complete_formal_files']
ORDER = ['written_papers', 'conditional_application', 'including_printed_validation', 'including_raw_validation_alternative']
CONDITION = 'After acquiring the whole U_R and both complete validation programs; neither program is a uniform written-proof premise.'

def need(value, message):
    if not value:
        raise ValueError('REPRESENTATION_COST_REJECT: '+message)

def read(path):
    return json.loads(path.read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n')

def bind(root, pin):
    need(sha(root/'manifest.json') == pin, 'accepted manifest changed')
    rows = read(root/'manifest.json')['exports']
    for row in rows:
        p = Path(row['path'])
        need(not p.is_absolute() and '..' not in p.parts, 'safe exported path')
        need((root/p).stat().st_size == row['bytes'] and sha(root/p) == row['sha256'], 'changed accepted export '+str(p))
    return len(rows)

def inputs(roots, public):
    verified = {k: bind(roots[k], pin) for k, pin in PINS.items()}
    counts = read(roots['inputs']/'author_counts.json')
    independent = read(roots['input_review']/'independent_replay.json')
    review = read(roots['input_review']/'review.json')
    adoption = read(roots['input_adoption']/'review.json')
    policy = read(roots['inputs']/'policy.json')
    boundary = read(roots['inputs']/'source_contract_boundary.json')
    mapping = read(roots['input_adoption']/'public_mapping.json')
    need(review['status'] == 'ACCEPTED_INDEPENDENT_REPRESENTATION_MEASUREMENT_INPUTS', 'independent input acceptance')
    need(adoption['status'] == 'ROOT_ACCEPTED_REPRESENTATION_MEASUREMENT_INPUTS', 'root input acceptance')
    need(counts['documents'] == independent['documents'] and counts['ratios'] is None, 'independent PDF counts')
    for key in RAW:
        need(counts[key] == independent['raw_files'][key] and len(counts[key]) == 2, 'two whole raw files: '+key)
    need(policy['units'] == UNITS and policy['variants'] == VARIANTS and policy['normalizations'] == FORMS, 'accepted ruler')
    need(policy['comparison_policy']['cross_topic_deduplication'] is False, 'no cross-topic discount')
    need(set(counts['documents']) == {'F010', 'U_R', 'R1', 'CODE'}, 'complete four documents')
    need([counts['documents'][k]['pages'] for k in ['F010', 'U_R', 'R1', 'CODE']] == [13, 5, 5, 4], 'all27 pages')
    need(boundary['row_count'] == 6 and len(boundary['proof_spans']) == 13 and boundary['principal_contracts'] == 1, 'accepted6row/13span scope')
    need(not boundary['validation_boundary']['uniform_written_proof_depends_on_finite_results'], 'validation not uniform premise')
    need(len(policy['program_roster']) == 2 and all(r['classification'] == 'validation' and r['complete_original_file'] and not r['uniform_written_proof_premise'] for r in policy['program_roster']), 'whole validation boundary')
    for row in mapping['artifacts']:
        need(sha(public/row['path']) == row['sha256'], 'exact current published byte '+row['path'])
    bindings = dict(accepted_manifest_sha256=PINS, accepted_exports_checked=verified,
                    published_commit=mapping['commit'], published_artifacts=mapping['artifacts'],
                    accepted_metadata={k: [{'path': f, 'sha256': sha(roots[k]/f)} for f in files]
                        for k, files in {
                            'inputs': ['author_counts.json', 'policy.json', 'protocol.json', 'source_contract_boundary.json'],
                            'input_review': ['independent_replay.json', 'review.json'],
                            'input_adoption': ['review.json', 'public_mapping.json']}.items()})
    return counts, policy, boundary, bindings

def fraction(n, d):
    f = Fraction(n, d)
    return dict(numerator=n, denominator=d, reduced_numerator=f.numerator,
                reduced_denominator=f.denominator, exact_fraction=str(f), decimal=f'{float(f):.12f}')

def derive(counts, policy, boundary, bindings):
    coords = []
    for v in VARIANTS:
        for n in FORMS:
            for u in UNITS:
                c = {k: row['variants'][v][n][u] for k, row in counts['documents'].items()}
                raw = {k: sum(row['metrics'][n][u] for row in counts[k].values()) for k in RAW}
                den = c['U_R']+c['R1']
                comp = dict(written_papers=fraction(c['F010'], den),
                            conditional_application=fraction(c['F010'], c['R1']),
                            including_printed_validation=fraction(c['F010'], den+c['CODE']),
                            including_raw_validation_alternative=fraction(c['F010'], den+raw['complete_validation_programs']))
                coords.append(dict(variant=v, normalization=n, unit=u, document_costs=c,
                                   raw_costs=raw, source_sum=c['F010'], written_denominator=den,
                                   comparisons=comp, acquired_common=c['U_R'],
                                   acquired_printed_validation=c['CODE'],
                                   acquired_raw_validation_alternative=raw['complete_validation_programs']))
    return dict(status='AUTHOR_NUMERICAL_CANDIDATE_PENDING_INDEPENDENT_ARITHMETIC_REVIEW',
                input_bindings=bindings, coordinates=coords, coordinate_count=30,
                exact_fraction_count=120, combined_exact_fractions=90, conditional_exact_fractions=30,
                comparison_order=ORDER, primary=coords[22],
                source_to_application_sequence=[dict(source='F010', application='R1', source_pages=13, application_pages=5)],
                whole_common_once=True, whole_application=True, cross_topic_discount=False,
                conditional_prepaid=CONDITION,
                program_boundary=dict(complete_validation_programs=2, uniform_finite_proof_premises=0,
                    primary_representation='Whole4-page printed appendix counted once',
                    alternative_representation='Both complete raw files summed per file, never added to the appendix',
                    complete_operational_drivers_separate=2, complete_Lean_files_separate=2,
                    prior_partial_Lean_declarations=12, formal_generic=8, formal_reused_local=4,
                    full_application_formalized=False, drivers_added_to_comparisons=False, Lean_added_to_comparisons=False),
                raw_file_inventory={key:counts[key] for key in RAW},
                physical_pages=dict(source=13, common=5, application=5, written_replacement=10, printed_validation=4, total_inputs=27),
                source_contract_rows=6, accepted_proof_contexts=13, principal_contracts_unchanged=1,
                source_qualifications=boundary['source_qualifications'], source_exclusions=boundary['exclusions'],
                original_authors=boundary['attribution'],
                retained_external_proof_cost=None, historical_program_cost=None,
                graphics_and_formula_layout_cost=None, operational_engineering_cost=None,
                minimal_mathematical_complexity=None, full_visible_graphical_text_claim=False,
                sawtooth_claim=False, source_question_answer='Original Theorem A already answers Question2.4; no new answer.',
                new_source_credit=0, new_question_credit=0, new_formal_credit=0,
                primary_text_fonts_images_exported=False,
                interpretation='Complete extracted-text lengths under the accepted principal-result contract and declared qualifications, not total effort or minimum proof length.')

def csv_rows(result):
    rows=[]
    for c in result['coordinates']:
        for name in ORDER:
            rows.append(dict(variant=c['variant'], normalization=c['normalization'], unit=c['unit'],
                             comparison=name, **c['comparisons'][name]))
    return rows

def save_csv(path, rows):
    with path.open('w', newline='') as f:
        w=csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n');w.writeheader();w.writerows(rows)

def arguments(parser):
    for k in PINS:
        parser.add_argument('--'+k.replace('_', '-'), type=Path, required=True)
    parser.add_argument('--public-root', type=Path, required=True)

def main():
    p=argparse.ArgumentParser();arguments(p);p.add_argument('--out', type=Path, required=True);a=p.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(), 'fresh output')
    data=inputs({k:getattr(a,k) for k in PINS},a.public_root);result=derive(*data)
    a.out.mkdir(parents=True);write(a.out/'results.json', result);write(a.out/'input_bindings.json', data[3]);save_csv(a.out/'comparisons.csv',csv_rows(result))
    print(json.dumps(result['primary'],ensure_ascii=False))

if __name__=='__main__':main()
