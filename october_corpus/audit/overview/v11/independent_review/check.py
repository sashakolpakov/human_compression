#!/usr/bin/env python3
"""Independently verify current factors, historical observations and graph bars."""
import argparse
import csv
import hashlib
import importlib.util
import json
import re
from pathlib import Path

from pypdf import PdfReader


def read(path):
    return json.loads(path.read_text())


def need(condition, message):
    if not condition:
        raise ValueError(message)


def check(packet, public):
    for row in read(packet / 'manifest.json')['exports']:
        data = (packet / row['path']).read_bytes()
        need(len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'], row['path'])
    prior = read(public / 'audit/overview/v10/packet/results.json')
    current = read(packet / 'results.json')
    held_topics = {'Chamber', 'ChiralEnumeration', 'Operations'}
    held_sources = {'L008', 'L028', 'N006'}
    need(current['original_ids'] == prior['original_ids'] and len(current['original_ids']) == 43,
         'all original recoveries preserved')
    need(current['active_originals'] == 106 and current['accessible_pending_originals'] == 63,
         'programme counts')
    need(current['pooled_factor'] is None and not current['software_inclusive_comparisons_available'],
         'no unmatched aggregate factors')
    need(len(current['topics']) == 19, 'all topics retained')
    current_pairs = []
    for old, new in zip(prior['topics'], current['topics']):
        name = old['topic']
        need(new['topic'] == name, 'topic order')
        for key in ['source_ids', 'common_theory', 'common_components', 'source_sum',
                    'applications_sum', 'written_denominator', 'program_roles',
                    'printed_program_cost', 'raw_program_alternative']:
            need(new.get(key) == old.get(key), name + ' unchanged observation ' + key)
        need(new['historical_written'] == old['written'], 'old whole-topic fraction preserved')
        need(new['written'] == (None if name in held_topics else old['written']),
             'current whole-topic fraction')
        need(len(old['pairs']) == len(new['pairs']), 'all individual rows retained')
        for a, b in zip(old['pairs'], new['pairs']):
            for key in a:
                if key != 'conditional':
                    need(b[key] == a[key], 'unchanged individual observation ' + key)
            need(b['historical_conditional'] == a['conditional'], 'historical individual fraction')
            need(b['conditional'] == (None if a['source'] in held_sources else a['conditional']),
                 'current individual fraction')
            current_pairs.append((name, new['common_theory'], b))
    need(sum(t['written'] is not None for t in current['topics']) == 16 and
         sum(p['conditional'] is not None for _, _, p in current_pairs) == 40,
         'exact current comparison counts')

    with (packet / 'topics.csv').open() as stream:
        topics_csv = list(csv.DictReader(stream))
    need(len(topics_csv) == 19, 'all topic CSV rows')
    for row, topic in zip(topics_csv, current['topics']):
        need(row['topic'] == topic['topic'] and int(row['originals']) == len(topic['source_ids']),
             'topic CSV identity')
        for key, target in [('source_cost_observed', 'source_sum'),
                            ('whole_common_cost_observed', 'common_theory'),
                            ('application_cost_observed', 'applications_sum'),
                            ('written_denominator_observed', 'written_denominator')]:
            need(int(row[key]) == topic[target], 'topic CSV observed cost')
        for prefix, value in [('current', topic['written']), ('historical', topic['historical_written'])]:
            need(row[prefix + '_written_exact'] == ('null' if value is None else value['exact_fraction'])
                 and row[prefix + '_written_factor'] == ('null' if value is None else value['decimal']),
                 'topic CSV current/historical distinction')
    with (packet / 'applications.csv').open() as stream:
        applications_csv = list(csv.DictReader(stream))
    need(len(applications_csv) == 43, 'all individual CSV rows')
    for row, (name, common, pair) in zip(applications_csv, current_pairs):
        need((row['topic'], row['source'], row['application']) ==
             (name, pair['source'], pair['application']), 'individual CSV identity')
        need(int(row['source_cost_observed']) == pair['source_cost'] and
             int(row['application_cost_observed']) == pair['application_cost'] and
             int(row['whole_common_cost_observed']) == common, 'individual CSV costs')
        for prefix, value in [('current', pair['conditional']), ('historical', pair['historical_conditional'])]:
            need(row[prefix + '_conditional_exact'] == ('null' if value is None else value['exact_fraction'])
                 and row[prefix + '_conditional_factor'] == ('null' if value is None else value['decimal']),
                 'individual CSV current/historical distinction')

    # Use the previously accepted PDF/SVG path parser; independently reconstruct
    # geometry from the original v10 numbers and the published chart scale.
    module_spec = importlib.util.spec_from_file_location(
        'previous_geometry', public / 'audit/overview/v10/packet/geometry_checks.py')
    geometry = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(geometry)
    whole = [(t['topic'], t['topic'] in held_topics,
              [('source', t['source_sum']), ('common', t['common_theory']),
               ('applications', t['applications_sum'])]) for t in prior['topics']]
    individual = [(p['source'], p['source'] in held_sources,
                   [('source', p['source_cost']), ('application', p['application_cost'])])
                  for t in prior['topics'] for p in t['pairs']]
    plots = [('whole_topics', whole, 604.8, 3),
             ('conditional_1', individual[:22], 655.2, 2),
             ('conditional_2', individual[22:], 655.2, 2)]
    bars = 0
    for name, records, height, legend in plots:
        maximum = max(max(values[0][1], sum(value for _, value in values[1:]))
                      for _, held, values in records if not held)
        x_scale = 777.6 * .77 / (maximum * 1.08)
        row_height = height * .84 / len(records)
        expected = {}
        for index, (identity, held, values) in enumerate(records):
            if held:
                continue
            start = 0
            for position, (kind, value) in enumerate(values):
                x = 777.6 * .19 + (0 if position == 0 else start * x_scale)
                y = height * .08 + (index + (.235 if position == 0 else .535)) * row_height
                expected['bar-' + identity + '-' + kind] = [x, y, value * x_scale, .23 * row_height]
                if position:
                    start += value
        svg = (packet / (name + '.svg')).read_text()
        geometry.compare_geometry(geometry.svg_rectangles(svg), expected)
        rectangles, actual_height = geometry.pdf_rectangles(packet / (name + '.pdf'))
        need(abs(actual_height - height) < 1e-6, 'PDF dimensions')
        geometry.compare_pdf(rectangles, height, expected, legend)
        pdf_text = ''.join(page.extract_text() or '' for page in PdfReader(packet / (name + '.pdf')).pages)
        need(svg.count('awaiting matched code boundary') == sum(r[1] for r in records)
             and pdf_text.count('awaiting matched code boundary') == sum(r[1] for r in records),
             'actual withheld labels in both graph formats')
        bars += len(expected)
    need(bars == 128, 'all current bars checked')

    pages = [page.extract_text() or '' for page in PdfReader(packet / 'reader.pdf').pages]
    need(len(pages) == 2, 'complete two-page reader')
    flat = ' '.join(pages[1].split())
    for topic in prior['topics']:
        name = topic['topic']
        value = '— held' if name in held_topics else topic['written']['decimal'] + ' unchanged'
        need(name + ' ' + str(len(topic['source_ids'])) + ' ' + value in flat,
             'actual topic row in PDF')
    need('16 available whole-topic factors and 40 available conditional' in ' '.join(pages[0].split()),
         'reader current count')
    return {'status': 'PASS_INDEPENDENT_CURRENT_LISTING_COMPARISON',
            'topic_rows': 19, 'individual_rows': 43, 'current_whole': 16,
            'current_conditional': 40, 'historical_comparisons_preserved': 62,
            'SVG_bars': bars, 'PDF_bars': bars, 'reader_pages': 2,
            'all_old_costs_preserved': True, 'new_ratios_computed': False,
            'recovery_count': 43, 'pending_recovery_count': 63,
            'scientific_programs_or_Lean_executed': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--public', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(not args.out.exists(), 'fresh output')
    result = check(args.packet, args.public)
    args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
