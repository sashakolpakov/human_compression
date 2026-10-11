#!/usr/bin/env python3
"""Complete B/C comparisons using available authored renderings for two sources."""
import argparse
import csv
from fractions import Fraction
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(p):
    return json.loads(p.read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def ratio(n, d):
    need(type(n) is int and type(d) is int and n > 0 and d > 0, 'Whole positive integer costs')
    f = Fraction(n, d)
    return dict(numerator=n, denominator=d, reduced_numerator=f.numerator,
                reduced_denominator=f.denominator, decimal=f'{float(f):.12f}')


def compute(inputs, historical, policy):
    rows = []
    for topic, old in historical.items():
        original = policy['topics'][topic]['rendered_original']
        rendered = inputs['documents'][original]
        need(not rendered['original_PDF_retrieved'], 'Representation remains explicit')
        for coordinate in old['coordinates']:
            variant, norm, unit = [coordinate[k] for k in ['variant','normalization','unit']]
            missing_cost = rendered['metrics'][norm][unit]
            need(coordinate['unknown_source'] == original and coordinate['complete_source_sum'] is None,
                 'Earlier PDF-only comparison stays unchanged')
            results = []
            for item in coordinate['per_result']:
                source_cost = missing_cost if item['source'] == original else item['source_cost']
                results.append(dict(source=item['source'], application=item['application'],
                                    source_representation=('literal_authored_rendering' if item['source']==original
                                                           else 'complete_PDF_'+variant),
                                    source_cost=source_cost, application_cost=item['application_cost'],
                                    comparison=ratio(source_cost, item['application_cost'])))
            source_sum = sum(r['source_cost'] for r in results)
            apps = sum(r['application_cost'] for r in results)
            common = coordinate['common_theory']
            need(apps == coordinate['all_applications'] and len(results)==4, 'Every complete application')
            need(source_sum == coordinate['known_source_sum']+missing_cost, 'Every original manuscript')
            printed = coordinate.get('complete_printed_program_cost', 0)
            raw = coordinate.get('complete_raw_program_cost', 0)
            comparisons = dict(written=ratio(source_sum, common+apps))
            if topic == 'C':
                comparisons.update(including_printed_programs=ratio(source_sum, common+apps+printed),
                                   including_raw_programs=ratio(source_sum, common+apps+raw))
            rows.append(dict(topic=topic, PDF_variant=variant, normalization=norm, unit=unit,
                             comparison_status=('primary_boundary' if variant=='raw_untrimmed' else
                                                'mixed_furniture_sensitivity'),
                             rendered_original=original, rendered_cost=missing_cost,
                             common_theory=common, applications=apps, written_denominator=common+apps,
                             printed_program_cost=printed, raw_program_alternative=raw,
                             source_sum=source_sum, whole=comparisons, individual=results))
    primary = {topic: next(r for r in rows if (r['topic'],r['PDF_variant'],r['normalization'],r['unit']) ==
                           (topic,'raw_untrimmed','NFC','characters_without_whitespace')) for topic in historical}
    return dict(status='AUTHOR_COMPARISONS_PENDING_DISTINCT_ARITHMETIC_REVIEW',
                policy=policy, original_manuscripts=8, rows=rows, primary=primary,
                source_text_exported=False, historical_PDF_coordinates_changed=False,
                new_source_credit=0, new_question_credit=0, full_graphic_and_external_costs=None)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--rendered-inputs', type=Path, required=True)
    ap.add_argument('--public-root', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a=ap.parse_args()
    need(not a.out.exists(), 'Fresh output directory')
    policy=read(HERE/'policy.json')
    need(sha(a.rendered_inputs/'manifest.json') == policy['rendered_input_manifest_sha256'], 'Fixed rendering input')
    for row in read(a.rendered_inputs/'manifest.json')['exports']:
        p=a.rendered_inputs/row['path']
        need(sha(p)==row['sha256'] and p.stat().st_size==row['bytes'], 'Complete rendering input archive')
    old={}
    for topic, item in policy['topics'].items():
        p=a.public_root/item['previous_results_path']
        need(sha(p)==item['previous_results_sha256'], 'Unchanged accepted PDF-only results')
        old[topic]=read(p)
    result=compute(read(a.rendered_inputs/'counts.json'),old,policy)
    a.out.mkdir(parents=True)
    (a.out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    with (a.out/'comparisons.csv').open('w',newline='') as f:
        w=csv.writer(f); w.writerow(['topic','PDF_variant','normalization','unit','comparison','numerator','denominator','reduced_numerator','reduced_denominator','decimal'])
        for r in result['rows']:
            values=list(r['whole'].items())+[(x['source']+'_conditional',x['comparison']) for x in r['individual']]
            for name, value in values:
                w.writerow([r['topic'],r['PDF_variant'],r['normalization'],r['unit'],name,
                            *[value[k] for k in ['numerator','denominator','reduced_numerator','reduced_denominator','decimal']]])
    print(json.dumps(result['primary'],indent=2))


if __name__ == '__main__':
    main()
