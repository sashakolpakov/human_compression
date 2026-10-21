#!/usr/bin/env python3
"""Independent complete arithmetic and actual chart check for enlarged Mixes."""
import argparse
import csv
import hashlib
import json
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from pypdf import PdfReader
from pypdf.generic import ContentStream


def read(path):
    return json.loads(path.read_text())


def need(ok, message):
    if not ok:
        raise ValueError(message)


def verify_manifest(path, pin):
    need(hashlib.sha256(path.read_bytes()).hexdigest() == pin, str(path))
    entries = read(path)['exports']
    for row in entries:
        data = (path.parent / row['path']).read_bytes()
        need(len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'], row['path'])
    return len(entries)


def bounds(points):
    xs, ys = zip(*points)
    return [min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)]


def near(a, b):
    return len(a) == len(b) and all(abs(x - y) < 0.00002 for x, y in zip(a, b))


def check(study):
    packet = study / 'topic_Mix_L016_measurement_results'
    pins = {
        'topic_Mix_L016_measurement_results': 'c6a5365047aba5b466737aeaf20a42bb6e6aac27184dfdf9ef0c2eccbe0533fe',
        'topic_Mix_L016_measurement_inputs': '6327d4327795eeebd3c3ceb044a99f056ea18ddf865bba720c4920d378db727e',
        'topic_Mix_F005_measurement_inputs': '3f02f43dd6e0037cfded61d4b3096b69a8412eeba669ec5714ea1190a24990a8',
        'topic_Mix_L016_input_root_review': 'e34a51d925bd900257d06f7b1b0aee33487c7a236b3239c7ece32b193ff43a65',
    }
    exports = sum(verify_manifest(study / folder / 'manifest.json', pin) for folder, pin in pins.items())
    old = read(study / 'topic_Mix_F005_measurement_inputs/author_counts.json')
    new = read(study / 'topic_Mix_L016_measurement_inputs/author_counts.json')
    need(new['retained_accepted_inputs'] == old, 'all literal previous input vectors')
    docs = {dict(U='U0', CODE1='OLD_CODE1', CODE2='OLD_CODE2').get(k, k): row
            for k, row in old['documents'].items()}
    docs.update(new['documents'])
    files = {kind: dict(old['raw_files'][kind], **new['raw_files'][kind])
             for kind in ['programs', 'drivers', 'formal']}
    need([len(files[k]) for k in ['programs', 'drivers', 'formal']] == [6, 5, 2], 'whole raw inventory')
    required = ['topic_Mix_F005_recovery/check_coprime.g', 'topic_Mix_L016_recovery/base_certificate.g']
    optional = sorted(set(files['programs']) - set(required))
    result = read(packet / 'results.json')
    need(result['whole_raw_file_inventory'] == files and result['required_files'] == required and
         sorted(result['optional_files']) == optional, 'whole files and proof roles')
    need(result['complete_document_metric_vectors'] == {k: row['metrics'] for k, row in docs.items()},
         'complete original and current metric vectors')
    need(result['common_documents'] == ['U0', 'U1'] and
         result['application_documents'] == {'MX1': {'source': 'F005', 'documents': ['A1', 'A2']},
                                              'MX2': {'source': 'L016', 'documents': ['A3']}},
         'all common and local papers paid')
    units = ['whitespace_tokens', 'alphanumeric_units', 'characters_without_whitespace',
             'characters_with_collapsed_whitespace', 'utf8_bytes_with_collapsed_whitespace']
    coordinates = [(v, n, u) for v in ['raw_untrimmed', 'raw_selected', 'calibrated_selected']
                   for n in ['NFC', 'NFKC'] for u in units]
    need(len(result['coordinates']) == 30, 'all coordinates')
    csv_expected = []
    for (v, n, u), row in zip(coordinates, result['coordinates']):
        need((row['variant'], row['normalization'], row['unit']) == (v, n, u), 'coordinate identity')
        d = {k: r['metrics'][v][n][u] for k, r in docs.items()}
        raw = {g: {k: r['metrics'][n][u] for k, r in rr.items()} for g, rr in files.items()}
        need(row['document_costs'] == d and row['raw_file_costs'] == raw, 'every coordinate cost')
        source = d['F005'] + d['L016']; common = d['U0'] + d['U1']
        apps = {'MX1': d['A1'] + d['A2'], 'MX2': d['A3']}
        need(row['source_cost'] == source and row['common_cost'] == common and
             row['application_costs'] == apps and row['written_denominator'] == common + sum(apps.values()),
             'full summed manuscript costs')
        expected = [('whole_topic', source, common + sum(apps.values())),
                    ('conditional_MX1', d['F005'], apps['MX1']),
                    ('conditional_MX2', d['L016'], apps['MX2'])]
        need(list(row['comparisons']) == [a for a, _, _ in expected], 'only three authorized ratios')
        for name, a, b in expected:
            gcd = math.gcd(a, b); num, den = a // gcd, b // gcd
            ratio = dict(numerator=a, denominator=b, reduced_numerator=num, reduced_denominator=den,
                         exact_fraction=str(num) if den == 1 else f'{num}/{den}', decimal=f'{a/b:.12f}')
            need(row['comparisons'][name] == ratio, 'exact arithmetic ' + name)
            csv_expected.append(dict(variant=v, normalization=n, unit=u, comparison=name, **ratio))
        inventory = dict(required_raw=sum(raw['programs'][p] for p in required),
                         optional_raw=sum(raw['programs'][p] for p in optional),
                         drivers=sum(raw['drivers'].values()), formal=sum(raw['formal'].values()),
                         required_printed_alternative=d['REQ'], new_optional_printed_inventory=d['VAL'],
                         historical_mixed_appendices_inventory=d['OLD_CODE1'] + d['OLD_CODE2'])
        need(row['separate_inventory_costs'] == inventory, 'all separate inventory costs')
    with (packet / 'comparisons.csv').open() as stream:
        need(list(csv.DictReader(stream)) == [{k: str(v) for k, v in row.items()} for row in csv_expected],
             'all ninety CSV rows')
    need(result['primary'] == result['coordinates'][2], 'fixed raw primary')
    need(result['originals'] == ['F005', 'L016'] and result['original_count'] == 2 and
         result['software_inclusive_factor'] is None and result['historical_software_cost'] is None and
         all(v is None for v in result['unknown_costs'].values()) and
         result['whole_umbrellas_charged_once'] and result['required_finite_premises_not_optional'] and
         result['optional_validation_symmetric_exclusion'] and not result['cross_topic_discount'] and
         not result['overlap_discount'] and not result['end_to_end_formalization'] and
         result['partial_formal_declarations'] == 6 and result['new_source_credit'] == 0 and
         result['new_question_credit'] == 0, 'scope, symmetric boundary and partial formalization')
    need('both complete required finite certificates' in result['conditional_prepaid'] and
         len(result['source_scope_limits']) == 3, 'all retained acquisition and source qualifications')

    # Derive chart dimensions from the declared fixed canvas and axes, rather
    # than accepting the author's geometry records as the expected answer.
    d = result['primary']['document_costs']; height = 252.; width = 720.
    axis_width = width * (.995 - .09) / 2.36
    expected = {}
    for axis, stacks, maximum in [
            (0, [(0, ['F005', 'L016']), (1, ['U0', 'U1', 'A1', 'A2', 'A3'])],
             (d['F005'] + d['L016']) * 1.17),
            (1, [(0, ['F005']), (1, ['A1', 'A2']), (3, ['L016']), (4, ['A3'])],
             max(d['F005'], d['L016']) * 1.2)]:
        m = 1 if axis == 0 else 4
        margin = .05 * (m + .62); xmin = -.31 - margin
        xscale = axis_width / (m + .62 + 2 * margin)
        origin = width * .09 + axis * axis_width * 1.36
        yscale = height * (.87 - .30) / maximum
        for xpos, keys in stacks:
            base = 0
            for key in keys:
                name = ('whole-' if axis == 0 else 'conditional-') + key
                expected[name] = [origin + (xpos - .31 - xmin) * xscale,
                                  height * .30 + base * yscale, .62 * xscale, d[key] * yscale]
                base += d[key]
    tree = ET.fromstring((packet / 'complete_costs.svg').read_text())
    found = {}
    for node in tree.iter():
        name = node.attrib.get('id', '')
        if name.startswith(('whole-', 'conditional-')):
            paths = [x for x in node if x.tag.endswith('path')]
            need(len(paths) == 1, 'one cost rectangle path')
            path = paths[0].attrib['d']; need(not re.search('[cqast]', path, re.I), 'straight rectangle')
            nums = list(map(float, re.findall(r'[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?', path)))
            bb = bounds(list(zip(nums[::2], nums[1::2])))
            found[name] = [bb[0], height - bb[1] - bb[3], bb[2], bb[3]]
    need(set(found) == set(expected) and all(near(found[k], b) for k, b in expected.items()),
         'all twelve actual SVG bars have independently derived dimensions')
    pdf = PdfReader(packet / 'complete_costs.pdf')
    need(len(pdf.pages) == 1 and near(list(map(float, pdf.pages[0].mediabox)), [0, 0, width, height]),
         'complete PDF canvas')
    points, boxes = [], []
    for operands, operator in ContentStream(pdf.pages[0].get_contents(), pdf).operations:
        if operator == b'm': points = [tuple(map(float, operands))]
        elif operator == b'l': points.append(tuple(map(float, operands)))
        elif operator == b're':
            x, y, w, h = map(float, operands); points = [(x,y), (x+w,y), (x+w,y+h), (x,y+h)]
        elif operator in [b'f', b'f*', b'B', b'B*']:
            if len(points) in [4, 5]: boxes.append(bounds(points))
            points = []
        elif operator in [b'n', b'S', b's']: points = []
    need(all(sum(near(box, b) for box in boxes) == 1 for b in expected.values()), 'all twelve actual PDF bars')
    geometry = read(packet / 'plot_geometry.json')
    need(len(geometry['bars']) == 12 and all(near(b['pdf'], expected[b['id']]) for b in geometry['bars']),
         'geometry metadata agrees with independently derived coordinates')
    graphs = read(packet / 'document_graphs.json')
    need({x['id']: x['cost'] for x in graphs['nodes']} ==
         {**{k:d[k] for k in ['F005','L016','U0','U1','A1','A2','A3']}, 'external':None},
         'complete document graph nodes and unknown outside costs')
    need(graphs['current_edges'] == [['U0','U1'],['U0','A1'],['U0','A2'],['U1','A3']] and
         graphs['historical_edges'] == [['external','F005'],['external','L016']] and
         graphs['required_files'] == required, 'document reuse and explicit finite premises')
    pages = [p.extract_text() or '' for p in PdfReader(packet / 'measurement.pdf').pages]
    need(len(pages) == 3, 'three complete reader pages')
    full = ' '.join(' '.join(pages).split())
    for value in d.values(): need(str(value) in full, 'whole observed cost in actual reader')
    for comparison in result['primary']['comparisons'].values():
        need(f"{comparison['numerator']/comparison['denominator']:.6f}" in full, 'actual displayed primary ratio')
    for phrase in ['22801', 'both whole required finite certificates', 'unknown cost', 'six generic dec- larations',
                   'three final problems remain unanswered', 'not an exhaustive historical theorem graph']:
        need(phrase in full, 'reader scope ' + phrase)
    for row in result['coordinates'][:5]:
        values = [f"{r['numerator']/r['denominator']:.3f}" for r in row['comparisons'].values()]
        need(' '.join(values) in full, 'all five actual sensitivity rows')
    return dict(status='PASS_ROOT_INDEPENDENT_ENLARGED_MIXES_NUMBERS', verified_exports=exports,
                coordinates=30, exact_fractions=90, csv_rows=90, whole_documents=11,
                whole_raw_files=13, actual_SVG_bars=12, actual_PDF_bars=12, reader_pages=3,
                author_modules_imported=False, source_text_reextracted=False,
                mathematical_or_Lean_execution=False, software_inclusive_factor=None)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--study', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True); args = parser.parse_args()
    need(not args.out.exists(), 'fresh output'); result = check(args.study)
    args.out.write_text(json.dumps(result, indent=2) + '\n'); print(json.dumps(result))
