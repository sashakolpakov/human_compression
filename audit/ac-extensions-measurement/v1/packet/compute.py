#!/usr/bin/env python3
"""Whole-topic additions to A and C; evaluation requires distinct input adoption."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal, localcontext
import argparse
import csv
import hashlib
import json

HERE = Path(__file__).resolve().parent
A_PAIRS = [('L032', 'A1'), ('L034', 'A2'), ('F016', 'A3'),
           ('F013', 'A4'), ('L035', 'A5'), ('N009', 'A6')]
SHARED_C = 'f1d49b61e210e0026468a2bcb2621399e5fda10778893fd1c20d364019f54810'


def need(ok, message):
    if not ok:
        raise ValueError('AC_EXTENSION_COMPARISON_REJECT: ' + message)


def fraction(n, d):
    need(type(n) is int and type(d) is int and n > 0 and d > 0,
         'positive complete-document integer costs')
    f = Fraction(n, d)
    with localcontext() as ctx:
        ctx.prec = 40
        dec = str(Decimal(n) / Decimal(d))
    return dict(numerator=n, denominator=d, reduced_numerator=f.numerator,
                reduced_denominator=f.denominator, decimal=dec)


def load_inputs(protocol, study_root, public_root, locations=None):
    need(protocol['status'] == 'FIXED_NUMERICAL_PROTOCOL_AFTER_DISTINCT_INPUT_ACCEPTANCE',
         'pending extraction review cannot authorize ratios')
    need(protocol.get('input_adoption') is not None, 'distinct root input adoption')
    roots = {'study': study_root, 'public': public_root}
    relocated = {}
    if locations is not None:
        routing = json.loads(locations.read_text())
        need(set(routing).issubset(protocol['bindings']), 'only declared input locations')
        relocated = {key: locations.parent / value for key, value in routing.items()}
    data = {}
    for key, row in protocol['bindings'].items():
        path = relocated.get(key, roots[row['root']] / row['path'])
        b = path.read_bytes()
        need(len(b) == row['bytes'] and hashlib.sha256(b).hexdigest() == row['sha256'],
             'exact bound input ' + key)
        data[key] = json.loads(b)
    # The final protocol binds the actual independent review and root adoption.
    # Their concrete recorded status and reviewed author hash are checked below.
    adoption = protocol['input_adoption']
    need(adoption['binding'] in data, 'bound adoption record')
    record = data[adoption['binding']]
    for key, value in adoption['required_fields'].items():
        need(record.get(key) == value, 'adoption field ' + key)
    need(adoption['author_manifest_sha256'] == protocol['bindings']['author_inputs']['sha256'],
         'adoption concerns this immutable author input')
    return data


def validate_policy(p, d):
    need(p['original_manuscripts'] == 12 and p['additional_originals'] == 2
         and p['new_topics'] == 0, 'twelve originals in two existing topics')
    need(p['cross_topic_discount'] is False and p['no_common_overlap_discount'] is True,
         'full independently charged common theories')
    need(p['topics']['A'] == dict(previous_originals=6, new_original='L128',
         application='A7', new_common=[], new_program='A_CODE_NEW',
         old_program_files=4, new_program_files=1), 'complete A boundary')
    need(p['topics']['C'] == dict(previous_originals=4, new_original='L068',
         application='C5', new_common=['U_C_INC'], new_program='C_CODE_NEW',
         old_program_files=2, new_program_files=1), 'complete C boundary')
    ip = d['input_policy']
    need(ip['whole_topic_rules']['A']['retain_full_previous_common'] and
         ip['whole_topic_rules']['C']['retain_full_previous_common'] and
         ip['whole_topic_rules']['C']['additional_common'] == ['U_C_INC'],
         'accepted whole common-paper boundaries')
    need(ip['shared_program']['sha256'] == SHARED_C and
         ip['old_C_required_programs'][0]['sha256'] == SHARED_C,
         'identical existing C program, not a new uncharged dependency')
    need(len(ip['old_C_required_programs']) == 2 and
         ip['whole_topic_rules']['C']['old_program_bundle_retained'],
         'old C exhaustive program is retained')
    need(len(d['old_A']['complete_raw_program_files']) == 4,
         'four complete original A program files')
    need(len(d['counts']['raw_files']['new_programs']) == 2 and
         len(d['counts']['raw_files']['shared_existing']) == 1,
         'two new whole programs and one recorded shared program')
    need(all(v is None for v in p['unknown_costs'].values()), 'unknown costs stay null')


def compute(p, d):
    validate_policy(p, d)
    counts = d['counts']
    rows = []
    for variant in p['variants']:
        for normalization in p['normalizations']:
            for unit in p['units']:
                def new(key):
                    return counts['documents'][key]['metrics'][variant][normalization][unit]

                def old_a(key):
                    av = 'untrimmed' if variant == 'raw_untrimmed' else variant
                    return d['old_A']['documents'][key]['metrics'][normalization][av][unit]

                def raw(category, topic):
                    return sum(row['metrics'][normalization][unit]
                               for path, row in counts['raw_files'][category].items()
                               if ('topic-a/' if topic == 'A' else 'topic-c/') in path)

                for topic in ['A', 'C']:
                    if topic == 'A':
                        pairs = [dict(source=s, application=a, source_cost=old_a(s),
                                      application_cost=old_a(a),
                                      source_representation='complete_PDF_' + variant)
                                 for s, a in A_PAIRS]
                        common = {'U_A': old_a('U_A')}
                        printed = {'previous_complete_appendix': old_a('code')}
                        raw_old = sum(x['metrics'][normalization][unit]
                                      for x in d['old_A']['complete_raw_program_files'])
                    else:
                        old = [x for x in d['old_C']['rows'] if x['topic'] == 'C'
                               and x['PDF_variant'] == variant
                               and x['normalization'] == normalization and x['unit'] == unit]
                        need(len(old) == 1, 'unique complete earlier C coordinate')
                        old = old[0]
                        pairs = [{k: x[k] for k in ['source', 'application', 'source_cost',
                                  'application_cost', 'source_representation']}
                                 for x in old['individual']]
                        need(len(pairs) == 4 and sum(x['source_cost'] for x in pairs) == old['source_sum']
                             and sum(x['application_cost'] for x in pairs) == old['applications'],
                             'complete earlier C sources and applications')
                        common = {'U_C': old['common_theory'], 'U_C_INC': new('U_C_INC')}
                        printed = {'previous_complete_appendix': old['printed_program_cost']}
                        raw_old = old['raw_program_alternative']
                    spec = p['topics'][topic]
                    pairs.append(dict(source=spec['new_original'], application=spec['application'],
                                      source_cost=new(spec['new_original']),
                                      application_cost=new(spec['application']),
                                      source_representation='complete_PDF_' + variant))
                    printed[spec['new_program']] = new(spec['new_program'])
                    source_sum = sum(x['source_cost'] for x in pairs)
                    apps = sum(x['application_cost'] for x in pairs)
                    whole_common = sum(common.values())
                    whole_printed = sum(printed.values())
                    whole_raw = raw_old + raw('new_programs', topic)
                    written = whole_common + apps
                    whole = dict(written=fraction(source_sum, written),
                                 including_printed_programs=fraction(source_sum, written + whole_printed),
                                 including_raw_programs=fraction(source_sum, written + whole_raw))
                    for item in pairs:
                        item['conditional'] = fraction(item['source_cost'], item['application_cost'])
                    rows.append(dict(topic=topic, variant=variant, normalization=normalization,
                                     unit=unit, original_manuscripts=len(pairs), source_sum=source_sum,
                                     common_components=common, common_theory=whole_common,
                                     applications=apps, written_denominator=written,
                                     printed_program_components=printed, printed_program_cost=whole_printed,
                                     raw_program_components={'previous_complete_files': raw_old,
                                         'new_complete_file': raw('new_programs', topic)},
                                     raw_program_alternative=whole_raw,
                                     shared_program_already_charged_once=(topic == 'C'),
                                     whole=whole, individual=pairs,
                                     conditional_acquisition=dict(full_common=whole_common,
                                         full_printed_programs=whole_printed, full_raw_programs=whole_raw,
                                         printed_and_raw_are_alternatives=True),
                                     new_auxiliary_inventory=dict(drivers=raw('drivers', topic),
                                         partial_formal_sources=raw('formal', topic))))
    primary = {t: next(x for x in rows if x['topic'] == t and
                        all(x[k] == v for k, v in p['primary'][t].items())) for t in ['A', 'C']}
    return dict(status='AUTHOR_NUMERICAL_CANDIDATE_PENDING_DISTINCT_REVIEW',
                existing_topics=['A', 'C'], original_manuscripts=12, additional_originals=2,
                new_topics=0, coordinates_per_topic=30, exact_fractions=540,
                rows=rows, primary=primary, source_contracts_unchanged=True,
                prior_numerical_packets_unchanged=True, full_common_charged_per_topic=True,
                all_declared_whole_programs_charged=True, unknown_costs=p['unknown_costs'],
                new_source_credit=0, new_question_credit=0, full_formalization_claim=False)


def write_outputs(out, result):
    (out / 'results.json').write_text(json.dumps(result, indent=2) + '\n')
    with (out / 'comparisons.csv').open('w', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['topic', 'source', 'variant', 'normalization', 'unit', 'comparison',
                    'numerator', 'denominator', 'decimal'])
        for row in result['rows']:
            for name, val in row['whole'].items():
                w.writerow([row['topic'], 'all', row['variant'], row['normalization'], row['unit'],
                            name, val['numerator'], val['denominator'], val['decimal']])
            for item in row['individual']:
                val = item['conditional']
                w.writerow([row['topic'], item['source'], row['variant'], row['normalization'], row['unit'],
                            'conditional_application', val['numerator'], val['denominator'], val['decimal']])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--study-root', type=Path, required=True)
    ap.add_argument('--public-root', type=Path, required=True)
    ap.add_argument('--protocol', type=Path, default=HERE / 'protocol.json')
    ap.add_argument('--locations', type=Path)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    p = json.loads(args.protocol.read_text())
    d = load_inputs(p, args.study_root, args.public_root, args.locations)
    result = compute(p, d)
    need(not args.out.exists(), 'fresh output')
    args.out.mkdir(parents=True)
    write_outputs(args.out, result)
    print(json.dumps({t: r['whole'] for t, r in result['primary'].items()}, indent=2))


if __name__ == '__main__':
    main()
