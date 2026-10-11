#!/usr/bin/env python3
"""Add L040 without removing any earlier complete Topic B cost."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal, localcontext
import argparse
import csv
import hashlib
import json

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError('B5_COMPARISON_REJECT: ' + message)


def fraction(n, d):
    need(type(n) is int and type(d) is int and n > 0 and d > 0, 'positive integer costs')
    f = Fraction(n, d)
    with localcontext() as ctx:
        ctx.prec = 40
        dec = str(Decimal(n) / Decimal(d))
    return dict(numerator=n, denominator=d, reduced_numerator=f.numerator,
                reduced_denominator=f.denominator, decimal=dec)


def load_inputs(p, study_root, public_root, locations=None):
    need(p['status'] == 'FIXED_NUMERICAL_PROTOCOL_AFTER_DISTINCT_INPUT_ACCEPTANCE', 'accepted input first')
    roots = {'study': study_root, 'public': public_root}
    routes = {} if locations is None else json.loads(locations.read_text())
    need(set(routes).issubset(p['bindings']), 'only declared input locations')
    data = {}
    for key, row in p['bindings'].items():
        path = locations.parent / routes[key] if key in routes else roots[row['root']] / row['path']
        b = path.read_bytes()
        need(len(b) == row['bytes'] and hashlib.sha256(b).hexdigest() == row['sha256'], 'bound input ' + key)
        data[key] = json.loads(b)
    adoption = data['root_adoption']
    need(adoption['status'] == 'ADOPTED_INPUT_BOUNDARY' and
         adoption['input_manifest_sha256'] == p['bindings']['author_inputs']['sha256'] and
         adoption['distinct_review_manifest_sha256'] == p['bindings']['independent_input_manifest']['sha256'],
         'exact independent input acceptance and root adoption')
    return data


def compute(p, data):
    need(p['topic'] == 'B' and p['original_manuscripts'] == 5 and p['additional_originals'] == 1
         and p['new_topics'] == 0 and p['no_overlap_discount'] and not p['cross_topic_discount'],
         'five originals in one complete existing topic')
    ip, counts = data['input_policy'], data['counts']
    need(ip['retain_all_four_old_applications'] and ip['retain_complete_old_programs'] and
         ip['new_common_whole_not_deduplicated'] and ip['source_cover_retained_in_primary'],
         'entire admitted topic closure and complete original')
    need(ip['new_code_whole_files'] == 4 and ip['principal_required_programs'] == 1 and
         ip['validation_programs'] == 2 and ip['auxiliary_example_programs'] == 1,
         'all four programs and distinct scientific roles')
    need(counts['source_article_only']['cover_omitted_directly'] and
         counts['source_article_only']['token_subtraction'] is False, 'direct article-only extraction')
    rows = []
    for variant in p['variants']:
        for norm in p['normalizations']:
            for unit in p['units']:
                old = [x for x in data['old_B']['rows'] if
                       (x['topic'], x['PDF_variant'], x['normalization'], x['unit']) == ('B', variant, norm, unit)]
                need(len(old) == 1, 'unique previous complete coordinate')
                old = old[0]
                vals = {k: x['metrics'][variant][norm][unit] for k, x in counts['documents'].items()}
                raw_files = {cat: {path: x['metrics'][norm][unit] for path, x in files.items()}
                             for cat, files in counts['raw_files'].items()}
                pairs = [{k: x[k] for k in ['source', 'application', 'source_cost',
                          'application_cost', 'source_representation']} for x in old['individual']]
                need(len(pairs) == 4 and sum(x['source_cost'] for x in pairs) == old['source_sum'] and
                     sum(x['application_cost'] for x in pairs) == old['applications'], 'all previous sources/applications')
                pairs.append(dict(source='L040', application='B5', source_cost=vals['L040'],
                                  application_cost=vals['A5'], source_representation='complete_PDF_' + variant))
                common = {'U_B_previous': old['common_theory'], 'U_B_high_rank': vals['U_ADD']}
                printed = {'previous_complete_bundle': old['printed_program_cost'], 'new_complete_appendix': vals['CODE']}
                raw = {'previous_complete_files': old['raw_program_alternative'], 'new_complete_files': sum(raw_files['programs'].values())}
                source_sum = old['source_sum'] + vals['L040']
                app_sum = old['applications'] + vals['A5']
                written = sum(common.values()) + app_sum
                whole = {key: fraction(source_sum, den) for key, den in [
                    ('written', written), ('including_printed_programs', written + sum(printed.values())),
                    ('including_raw_programs', written + sum(raw.values()))]}
                for x in pairs:
                    x['conditional'] = fraction(x['source_cost'], x['application_cost'])
                body = counts['source_article_only']['metrics'][variant][norm][unit]
                sensitivity_source = old['source_sum'] + body
                cover = dict(L040_article_cost=body, source_sum=sensitivity_source,
                    whole={key: fraction(sensitivity_source, val['denominator']) for key, val in whole.items()},
                    L040_conditional=fraction(body, vals['A5']), earlier_four_conditionals_unchanged=True,
                    all_replacement_costs_unchanged=True, direct_article_extraction=True)
                rows.append(dict(topic='B', variant=variant, normalization=norm, unit=unit,
                    source_sum=source_sum, common_components=common, common_theory=sum(common.values()),
                    applications=app_sum, written_denominator=written, printed_program_components=printed,
                    printed_program_cost=sum(printed.values()), raw_program_components=raw,
                    raw_program_alternative=sum(raw.values()), new_raw_file_inventory=raw_files,
                    original_manuscripts=5, whole=whole, individual=pairs,
                    conditional_acquisition=dict(full_common=sum(common.values()),
                        full_printed_programs=sum(printed.values()), full_raw_programs=sum(raw.values()),
                        printed_and_raw_are_alternatives=True), article_only_sensitivity=cover))
    primary = next(x for x in rows if all(x[k] == v for k, v in p['primary'].items()))
    return dict(status='AUTHOR_NUMERICAL_CANDIDATE_PENDING_DISTINCT_REVIEW', topic='B',
        original_manuscripts=5, additional_originals=1, new_topics=0, coordinates=30,
        main_exact_fractions=240, cover_sensitivity_fractions=120, rows=rows, primary={'B': primary},
        full_old_common_retained=True, full_new_common_retained=True, whole_new_programs=4,
        program_roles=dict(principal_required=1, validation=2, auxiliary_example=1),
        operational_drivers=2, new_partial_formal_declarations=8,
        source_cover_retained_in_primary=True, unknown_costs=p['unknown_costs'],
        source_contracts_unchanged=True, old_measurements_unchanged=True,
        new_source_credit=0, new_question_credit=0, full_formalization_claim=False)


def csv_records(r):
    out = []
    for row in r['rows']:
        entries = [('full_originals', 'all', key, val) for key, val in row['whole'].items()]
        entries += [('full_originals', x['source'], 'conditional_application', x['conditional']) for x in row['individual']]
        entries += [('L040_article_only', 'all', key, val) for key, val in row['article_only_sensitivity']['whole'].items()]
        entries += [('L040_article_only', 'L040', 'conditional_application', row['article_only_sensitivity']['L040_conditional'])]
        for boundary, source, name, q in entries:
            out.append([row['topic'], source, boundary, row['variant'], row['normalization'], row['unit'],
                        name, q['numerator'], q['denominator'], q['decimal']])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--study-root', type=Path, required=True)
    ap.add_argument('--public-root', type=Path, required=True)
    ap.add_argument('--locations', type=Path)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    p = json.loads((HERE / 'protocol.json').read_text())
    r = compute(p, load_inputs(p, a.study_root, a.public_root, a.locations))
    need(not a.out.exists(), 'fresh output')
    a.out.mkdir(parents=True)
    (a.out / 'results.json').write_text(json.dumps(r, indent=2) + '\n')
    with (a.out / 'comparisons.csv').open('w', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['topic', 'source', 'source_boundary', 'variant', 'normalization', 'unit', 'comparison',
                    'numerator', 'denominator', 'decimal'])
        w.writerows(csv_records(r))
    print(json.dumps(r['primary']['B']['whole'], indent=2))


if __name__ == '__main__':
    main()
