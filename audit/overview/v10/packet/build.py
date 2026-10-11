#!/usr/bin/env python3
"""Consolidate accepted manuscript costs under the symmetric validation policy.

The plotting and vector-reading helpers are adapted from overview42. This
builder does not extract source PDFs or reaccept any mathematical proof.
"""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal, localcontext
import argparse
import copy
import csv
import hashlib
import io
import json
import os
import subprocess

import plotting
import reader

ROOT = Path(__file__).resolve().parent


def need(ok, message):
    if not ok:
        raise ValueError(message)


def load(path):
    return json.loads(path.read_text())


def dump(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def ratio(n, d):
    need(type(n) is int and type(d) is int and n > 0 and d > 0, 'Positive integer costs required.')
    with localcontext() as ctx:
        ctx.prec = 50
        decimal = f'{Decimal(n) / Decimal(d):.12f}'
    return dict(numerator=n, denominator=d, exact_fraction=str(Fraction(n, d)), decimal=decimal)


def inputs():
    protocol = load(ROOT / 'protocol.json')
    need(protocol['status'] == 'BOUND_TO_ACCEPTED_SYMMETRIC_F_NUMBERS', 'F numbers have not yet been accepted.')
    data = {}
    for key, row in protocol['inputs'].items():
        p = Path(row['path'])
        need(not p.is_absolute() and '..' not in p.parts, 'Relative evidence only.')
        raw = (ROOT / p).read_bytes()
        need(len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256'], 'Changed input: ' + key)
        data[key] = json.loads(raw)
    need(data['measurement_policy']['status'] == 'CURRENT_SYMMETRIC_MEASUREMENT_POLICY', 'Symmetric policy absent.')
    need(data['F_review']['status'] == 'ROOT_ACCEPTED_SYMMETRIC_EXPANDED_F_NUMERICAL_COMPARISON' and
         protocol['inputs']['F_manifest']['sha256'] == data['F_review']['numerical_manifest_sha256'] ==
         '3a24e6ba85542b0cde991b56a40a93cb0e7ed540abd33d0b69b899b5e8f30527' and
         protocol['inputs']['F_review_manifest']['sha256'] ==
         '5dfd6f564a6c5ddb2c90f2d79cfb27834b5fd9a47a76aae0b40a85fc7c7b9db7',
         'Distinct F numerical acceptance absent or changed.')
    for manifest, exported, key in [('F_manifest', 'results.json', 'F_results'),
                                     ('F_review_manifest', 'review.json', 'F_review')]:
        item = next(r for r in data[manifest]['exports'] if r['path'] == exported)
        need((item['bytes'], item['sha256']) ==
             (protocol['inputs'][key]['bytes'], protocol['inputs'][key]['sha256']), 'Accepted manifest does not own numerical evidence.')
    need(data['F_review']['primary'] == data['F_results']['primary'] == data['F_admission']['primary'],
         'Admission differs from the independently accepted primary comparison.')
    need(data['F_admission']['source_ids'] == ['L014', 'L007'] and
         data['F_admission']['principal_originals_added'] == 1, 'Expanded F source boundary differs.')
    return protocol, data


def manuscript_row(old):
    """Retain the earlier text and cost inventory without its asymmetric ratios."""
    row = copy.deepcopy(old)
    for key in ['including_printed_programs', 'including_raw_programs', 'including_optional_validation']:
        row[key] = None
    row['software_comparison_status'] = 'UNAVAILABLE_UNTIL_BOTH_SIDES_INVENTORIED'
    row['written_comparison_scope'] = 'Complete manuscript lengths at the stated representation; separate programs excluded on both sides.'
    row['embedded_validation_listings_screened'] = False
    row['historical_acquisition_inventory'] = row.pop('conditional_prepaid')
    if 'conditional_raw_alternative_prepaid' in row:
        row['historical_raw_acquisition_inventory'] = row.pop('conditional_raw_alternative_prepaid')
    row['conditional_assumption'] = 'Whole common theory and the declared required dependencies already acquired. Optional validation is not a mathematical premise.'
    return row


def expanded_f(result):
    x = result['primary']; c = x['costs']; raw = x['raw_costs']
    need(c == dict(L014=25574, L007=44251, U=15876, A1=11504, A2=15894, CODE=22466), 'Changed accepted F primary.')
    need(raw['programs'] == 21691, 'Changed complete F validation inventory.')
    pairs = []
    for source, doc, application in [('L014', 'A1', 'F1'), ('L007', 'A2', 'F2')]:
        pairs.append(dict(source=source, application=application, source_cost=c[source],
                          application_cost=c[doc], source_representation='complete_PDF_raw_untrimmed',
                          conditional=ratio(c[source], c[doc])))
    return dict(topic='F', title='Odd kernels and cyclotomic constructions', source_count=2,
                source_ids=['L014', 'L007'], pairs=pairs, common_theory=c['U'],
                common_components=dict(whole_common=c['U']),
                application_components={'F1': {'whole_application': c['A1']}, 'F2': {'whole_application': c['A2']}},
                source_sum=c['L014'] + c['L007'], applications_sum=c['A1'] + c['A2'],
                written_denominator=c['U'] + c['A1'] + c['A2'],
                written=ratio(c['L014'] + c['L007'], c['U'] + c['A1'] + c['A2']),
                printed_program_cost=c['CODE'], raw_program_alternative=raw['programs'],
                optional_validation_printed=c['CODE'], validation_cost_already_in_printed_inventory=True,
                including_printed_programs=None, including_raw_programs=None, including_optional_validation=None,
                software_comparison_status='UNAVAILABLE_UNTIL_BOTH_SIDES_INVENTORIED',
                representation='raw_untrimmed_pdf', normalization='NFC', unit='characters_without_whitespace',
                numerical_status='DISTINCTLY_ACCEPTED_SYMMETRIC_F_COMPARISON',
                written_comparison_scope='Complete original papers versus whole common theory and both complete applications; validation excluded on both sides.',
                embedded_validation_listings_screened=True,
                conditional_assumption='Whole common theory and retained mathematical premises acquired; all nine programs are optional validation.',
                program_roles='Nine complete optional validation files; no program is a premise of a uniform proof. Four drivers and three Lean files are separate.',
                source_admission='audit/topic-f/v3/admission.json',
                source_dispositions=63, whole_common_pages=7, application_pages=[5, 6],
                full_source_formalized=False, formal_declarations=12, new_generic_declarations=3,
                scientific_boundary='L014 principal contract retained; L007 Theorems 1.1, 1.2 and 1.4 with all parameter ranges, corrected Remark 1.3, full used Section 3 construction and Section 6 claims. Section 7 prior lift separately attributed. No new question or priority claim.',
                external_proof_cost=None, historical_software_cost=None, complete_graphic_cost=None, full_formalization_cost=None)


def make(data):
    previous = data['previous_results']
    rows = [expanded_f(data['F_results']) if t['topic'] == 'F' else manuscript_row(t) for t in previous['topics']]
    snapshot = data['current_corpus']
    need(snapshot['admitted_principal_originals'] == snapshot['currently_measured_originals'] == 43 and
         snapshot['accessible_pending_complete_recovery'] == 63 and snapshot['originals'] == 106,
         'Current programme snapshot is not43 of106.')
    answer = dict(status='AUTHOR_OVERVIEW43_PENDING_DISTINCT_REVIEW', topic_count=19,
                  original_manuscript_count=43, active_originals=106, archived_unavailable_originals=55,
                  accessible_pending_originals=63, topics=rows, pooled_factor=None,
                  cross_topic_deduplication=False, written_and_conditional_comparisons=62,
                  original_ids=sorted(q['source'] for t in rows for q in t['pairs']),
                  no_new_mathematical_acceptance=True, new_source_credit=0, new_question_credit=0, new_formal_credit=0,
                  software_inclusive_comparisons_available=False,
                  policy='Validation excluded on both sides by default; complete manuscript boundaries preserved with embedded-listing audit limits explicit.',
                  programme_snapshot_status=snapshot['status'])
    validate(answer, previous, snapshot)
    return answer


def validate(answer, previous, snapshot):
    need(len(answer['topics']) == 19 and len(answer['original_ids']) == len(set(answer['original_ids'])) == 43,
         'Topic or original count differs.')
    need(answer['original_ids'] == snapshot['measured_original_ids'], 'Source partition differs from programme.')
    old = {t['topic']: t for t in previous['topics']}
    for t in answer['topics']:
        need(sum(t['common_components'].values()) == t['common_theory'], 'Common paper omitted.')
        need(sum(q['source_cost'] for q in t['pairs']) == t['source_sum'] and
             sum(q['application_cost'] for q in t['pairs']) == t['applications_sum'], 'Paper cost omitted.')
        need(t['written_denominator'] == t['common_theory'] + t['applications_sum'] and
             t['written'] == ratio(t['source_sum'], t['written_denominator']), 'Whole topic arithmetic differs.')
        for q in t['pairs']:
            need(q['conditional'] == ratio(q['source_cost'], q['application_cost']), 'Conditional arithmetic differs.')
            if 'application_components' in t:
                need(sum(t['application_components'][q['application']].values()) == q['application_cost'], 'Companion omitted.')
        need(all(t[k] is None for k in ['including_printed_programs', 'including_raw_programs', 'including_optional_validation']),
             'Asymmetric software factor retained.')
        if t['topic'] != 'F':
            need(t == manuscript_row(old[t['topic']]), 'Unrelated topic changed beyond symmetric presentation.')


def tables(result):
    output = {}
    definitions = {
        'topics.csv': (['topic', 'title', 'originals', 'representation', 'sources', 'common', 'applications', 'written', 'factor'],
                       [[t['topic'], t['title'], t['source_count'], t['representation'], t['source_sum'], t['common_theory'], t['applications_sum'], t['written_denominator'], t['written']['decimal']] for t in result['topics']]),
        'applications.csv': (['topic', 'source', 'application', 'source_cost', 'application_cost', 'conditional_exact', 'conditional_factor', 'whole_common_cost', 'assumption'],
                             [[t['topic'], q['source'], q['application'], q['source_cost'], q['application_cost'], q['conditional']['exact_fraction'], q['conditional']['decimal'], t['common_theory'], t['conditional_assumption']] for t in result['topics'] for q in t['pairs']]),
        'program_inventory.csv': (['topic', 'printed_programs', 'raw_programs', 'mandatory_data', 'optional_printed', 'optional_already_in_printed', 'source_software_cost', 'symmetric_software_factor', 'roles'],
                                 [[t['topic'], t['printed_program_cost'], t['raw_program_alternative'], t.get('mandatory_data_cost'), t.get('optional_validation_printed'), t.get('validation_cost_already_in_printed_inventory', False), 'unknown', 'unknown', t.get('program_roles', '')] for t in result['topics']])}
    for name, (header, rows) in definitions.items():
        stream = io.StringIO(newline=''); writer = csv.writer(stream, lineterminator='\n')
        writer.writerow(header); writer.writerows(rows); output[name] = stream.getvalue()
    return output


def build(out, render=False, xelatex='xelatex'):
    need(not out.exists(), 'Use a fresh output directory.')
    protocol, data = inputs(); result = make(data); out.mkdir(parents=True)
    dump(out / 'results.json', result)
    for name, text in tables(result).items():
        (out / name).write_text(text)
    os.environ.setdefault('MPLCONFIGDIR', str(out / 'mpl-cache'))
    os.environ.setdefault('XDG_CACHE_HOME', str(out / 'cache'))
    specs = {k: plotting.plot_spec(result, k) for k in ['whole_topics', 'conditional_1', 'conditional_2']}
    dump(out / 'plot_data.json', specs)
    for spec in specs.values():
        plotting.draw(spec, out)
    (out / 'summary.tex').write_text(reader.tex(result))
    if render:
        for i in [1, 2]:
            run = subprocess.run([xelatex, '-interaction=nonstopmode', '-halt-on-error', 'summary.tex'], cwd=out, capture_output=True)
            (out / f'render{i}.log').write_bytes(run.stdout + run.stderr)
            need(run.returncode == 0, 'Reader compilation failed.')
        diagnostics = [line for line in (out / 'summary.log').read_text(errors='replace').splitlines()
                       if any(word in line for word in ['Overfull', 'Underfull', 'Missing character', 'Font Warning', 'LaTeX Warning'])]
        need(not diagnostics, 'Reader diagnostics: ' + repr(diagnostics))
    dump(out / 'build_report.json', dict(status='PASS', topics=19, originals=43, written_and_conditional_comparisons=62,
                                       other_topic_costs_unchanged=18, rendered=render, optional_software_factors=0))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--render', action='store_true')
    parser.add_argument('--xelatex', default='xelatex')
    args = parser.parse_args()
    build(args.out, args.render, args.xelatex)
