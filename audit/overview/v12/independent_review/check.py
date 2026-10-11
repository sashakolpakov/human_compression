#!/usr/bin/env python3
"""Independently verify the restoration against accepted numerical records."""
import argparse
import csv
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
from pypdf import PdfReader


def need(value, message):
    if not value:
        raise ValueError(message)


def load(path):
    return json.loads(path.read_text())


def fraction(a, b):
    q = Fraction(a, b)
    with localcontext() as ctx:
        ctx.prec = 50
        decimal = format(Decimal(a) / Decimal(b), '.12f')
    return dict(numerator=a, denominator=b,
                exact_fraction=f'{q.numerator}/{q.denominator}', decimal=decimal)


def check(packet, public):
    manifest = load(packet / 'manifest.json')
    for row in manifest['exports']:
        data = (packet / row['path']).read_bytes()
        need(len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'], row['path'])
    previous = load(public / 'audit/overview/v11/packet/results.json')
    current = load(packet / 'results.json')
    numbers = load(packet / 'inputs/matched_numbers/results.json')['topics']
    changed = {'Chamber': 'L008', 'ChiralEnumeration': 'L028', 'Operations': 'N006'}
    need(current['original_ids'] == previous['original_ids'] and len(set(current['original_ids'])) == 43,
         'Source credit must not change')
    need(current['active_originals'] == 106 and current['accessible_pending_originals'] == 63,
         'Active corpus must not change')
    need(current['pooled_factor'] is None and not current['software_inclusive_comparisons_available'],
         'Unsupported inclusive or pooled ratio')
    need(len(current['topics']) == len(previous['topics']) == 19, 'Topic inventory')
    pairs = []
    allowed = {'source_sum', 'written', 'held_sources', 'representation', 'current_written_status',
               'current_written_reason', 'written_comparison_scope', 'pairs'}
    allowed_pair = {'source_cost', 'conditional', 'current_conditional_status', 'current_conditional_reason'}
    for old, new in zip(previous['topics'], current['topics']):
        topic = old['topic']
        need(new['topic'] == topic, 'Topic order')
        if topic not in changed:
            need(new == old, 'Unchanged whole topic: ' + topic)
        else:
            for key, value in old.items():
                if key not in allowed:
                    need(new[key] == value, 'Old complete inventory changed: ' + topic + '/' + key)
            primary = numbers[topic]['primary']
            need(new['source_sum'] == primary['source_sum'] and
                 new['common_theory'] == primary['common_sum'] and
                 new['written_denominator'] == primary['whole_written'], 'Accepted whole costs')
            need(new['historical_source_sum'] == old['source_sum'], 'Original count lost')
        need(new['written_denominator'] == new['common_theory'] + new['applications_sum'], 'Whole common paid')
        need(new['written'] == fraction(new['source_sum'], new['written_denominator']), 'Whole arithmetic')
        need(sum(p['application_cost'] for p in new['pairs']) == new['applications_sum'], 'All applications paid')
        need(sum(p['source_cost'] for p in new['pairs']) == new['source_sum'], 'All originals paid')
        for key in ['including_printed_programs', 'including_raw_programs',
                    'including_optional_validation', 'historical_software_cost']:
            need(new.get(key) is None, 'Unknown software replaced by a number')
        need(len(new['pairs']) == len(old['pairs']), 'Original count')
        for a, b in zip(old['pairs'], new['pairs']):
            if a['source'] not in changed.values():
                need(a == b, 'Unchanged individual record')
            else:
                for key, value in a.items():
                    if key not in allowed_pair:
                        need(b[key] == value, 'Required local inventory changed: ' + key)
                need(b['source_cost'] == numbers[topic]['primary']['document_costs'][b['source']],
                     'Accepted listing-excluded source cost')
                need(b['historical_source_cost'] == a['source_cost'], 'Original local count lost')
            need(b['conditional'] == fraction(b['source_cost'], b['application_cost']), 'Conditional arithmetic')
            pairs.append((topic, new['common_theory'], b))
    need(len(pairs) == 43, 'Complete application count')
    topics_csv = list(csv.DictReader((packet / 'topics.csv').open()))
    apps_csv = list(csv.DictReader((packet / 'applications.csv').open()))
    need(len(topics_csv) == 19 and len(apps_csv) == 43, 'CSV row count')
    for row, t in zip(topics_csv, current['topics']):
        need(row['topic'] == t['topic'] and int(row['originals']) == t['source_count'], 'Topic CSV identity')
        for key, name in [('current_source_cost', 'source_sum'), ('whole_common_cost', 'common_theory'),
                          ('whole_application_cost', 'applications_sum'), ('written_denominator', 'written_denominator')]:
            need(int(row[key]) == t[name], 'Topic CSV cost')
        for prefix, f in [('current', t['written']), ('historical', t['historical_written'])]:
            need(row[prefix + '_written_exact'] == f['exact_fraction'] and
                 row[prefix + '_written_factor'] == f['decimal'], 'CSV whole history or current fraction')
    for row, (topic, common, p) in zip(apps_csv, pairs):
        need((row['topic'], row['source'], row['application']) == (topic, p['source'], p['application']), 'Local CSV identity')
        need(int(row['current_source_cost']) == p['source_cost'] and int(row['whole_application_cost']) == p['application_cost']
             and int(row['whole_common_prepaid']) == common, 'Local CSV cost')
        for prefix, f in [('current', p['conditional']), ('historical', p['historical_conditional'])]:
            need(row[prefix + '_conditional_exact'] == f['exact_fraction'] and
                 row[prefix + '_conditional_factor'] == f['decimal'], 'CSV individual history or current fraction')
    # Reuse the previously accepted low-level vector parser. Expected dimensions
    # are derived here from accepted costs, not from the current author's plot data.
    spec = importlib.util.spec_from_file_location('previous_vector_parser', public / 'audit/overview/v10/packet/geometry_checks.py')
    geometry = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(geometry)
    whole = [(t['topic'], [('source', t['source_sum']), ('common', t['common_theory']), ('applications', t['applications_sum'])]) for t in current['topics']]
    individual = [(p['source'], [('source', p['source_cost']), ('application', p['application_cost'])]) for _, _, p in pairs]
    plots = [('whole_topics', whole, 604.8, 3), ('conditional_1', individual[:22], 655.2, 2),
             ('conditional_2', individual[22:], 655.2, 2)]
    bars = 0
    for name, rows, height, legend in plots:
        maximum = max(max(v[0][1], sum(n for _, n in v[1:])) for _, v in rows)
        sx = 777.6 * .77 / (maximum * 1.08)
        sy = height * .84 / len(rows)
        expected = {}
        for i, (identity, values) in enumerate(rows):
            start = 0
            for k, (kind, value) in enumerate(values):
                expected[f'bar-{identity}-{kind}'] = [777.6 * .19 + (start * sx if k else 0),
                    height * .08 + (i + (.535 if k else .235)) * sy, value * sx, .23 * sy]
                if k:
                    start += value
        svg = (packet / (name + '.svg')).read_text()
        geometry.compare_geometry(geometry.svg_rectangles(svg), expected)
        rectangles, actual_height = geometry.pdf_rectangles(packet / (name + '.pdf'))
        need(abs(actual_height - height) < 1e-6, 'PDF dimensions')
        geometry.compare_pdf(rectangles, height, expected, legend)
        need('awaiting matched code boundary' not in svg, 'Stale graph hold')
        bars += len(expected)
    need(bars == 143, 'All visible bars')
    pages = [p.extract_text() or '' for p in PdfReader(packet / 'reader.pdf').pages]
    need(len(pages) == 6, 'Whole reader')
    flat = [' '.join(p.split()) for p in pages]
    for t in current['topics']:
        cells = [t['topic'], str(t['source_count']), format(t['source_sum'], ','),
                 format(t['common_theory'], ','), format(t['applications_sum'], ','), f"{float(t['written']['decimal']):.3f}"]
        need(' '.join(cells) in flat[0], 'Reader topic row')
    for i, (topic, _, p) in enumerate(pairs):
        cells = [p['source'], topic, format(p['source_cost'], ','), format(p['application_cost'], ','), f"{float(p['conditional']['decimal']):.3f}"]
        need(' '.join(cells) in flat[1 if i < 22 else 2], 'Reader individual row')
    need('historical source software costs are unknown' in flat[1], 'Reader software boundary')
    return dict(status='PASS_INDEPENDENT_RESTORED_OVERVIEW', exact_fractions=62, unchanged_topics=16,
                unchanged_conditionals=40, SVG_bars=bars, PDF_bars=bars, reader_pages=6,
                recovered=43, pending=63, software_inclusive_factor=None, new_source_credit=0,
                full_source_or_formal_replay=False)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--packet', required=True, type=Path)
    ap.add_argument('--public', required=True, type=Path)
    ap.add_argument('--out', required=True, type=Path)
    a = ap.parse_args()
    need(not a.out.exists(), 'Fresh output required')
    result = check(a.packet, a.public)
    a.out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))
