#!/usr/bin/env python3
"""Check exact whole-topic costs, conditional acquisition and actual plotted geometry."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal, localcontext
import argparse
import copy
import csv
import hashlib
import json
import re
import xml.etree.ElementTree as ET
import pypdf
from pypdf.generic import ContentStream

HERE = Path(__file__).resolve().parent
COLORS = {'source': (98/255, 108/255, 118/255), 'common': (66/255, 107/255, 154/255),
          'application': (112/255, 165/255, 154/255), 'program': (189/255, 135/255, 78/255)}


def need(ok, message):
    if not ok:
        raise ValueError('AC_NUMERIC_CHECK_REJECT: ' + message)


def bind(protocol, roots, locations=None):
    relocated = {}
    if locations is not None:
        routing = json.loads(locations.read_text())
        need(set(routing).issubset(protocol['bindings']), 'only declared input locations')
        relocated = {key: locations.parent / value for key, value in routing.items()}
    out = {}
    for key, row in protocol['bindings'].items():
        path = relocated.get(key, roots[row['root']] / row['path'])
        b = path.read_bytes()
        need(len(b) == row['bytes'] and hashlib.sha256(b).hexdigest() == row['sha256'],
             'bound input ' + key)
        out[key] = json.loads(b)
    need(out['root_adoption']['status'] == 'ADOPTED_INPUT_BOUNDARY' and
         out['root_adoption']['input_manifest_sha256'] == protocol['bindings']['author_inputs']['sha256'] and
         out['root_adoption']['distinct_review_manifest_sha256'] == protocol['bindings']['independent_input_manifest']['sha256'],
         'exact distinctly adopted input')
    return out


def exact(q, numerator, denominator):
    f = Fraction(numerator, denominator)
    with localcontext() as c:
        c.prec = 40
        dec = str(Decimal(numerator) / Decimal(denominator))
    need(q == dict(numerator=numerator, denominator=denominator,
                   reduced_numerator=f.numerator, reduced_denominator=f.denominator, decimal=dec),
         'exact integer fraction and forty-place decimal')


def arithmetic(result, inputs):
    need(result['original_manuscripts'] == 12 and result['additional_originals'] == 2 and
         result['existing_topics'] == ['A', 'C'] and result['new_topics'] == 0,
         'complete source counts, not clause counts or new topics')
    need(result['new_source_credit'] == result['new_question_credit'] == 0 and
         result['full_formalization_claim'] is False, 'no new mathematical or formal credit')
    need(all(x is None for x in result['unknown_costs'].values()), 'unknown costs remain null')
    need(result['full_common_charged_per_topic'] and result['all_declared_whole_programs_charged'],
         'whole acquisition')
    counts = inputs['counts']
    allcoords = {(t, v, n, u) for t in ['A', 'C'] for v in
                 ['raw_untrimmed', 'raw_selected', 'calibrated_selected']
                 for n in ['NFC', 'NFKC'] for u in ['whitespace_tokens', 'alphanumeric_units',
                    'characters_without_whitespace', 'characters_with_collapsed_whitespace',
                    'utf8_bytes_with_collapsed_whitespace']}
    seen, number = set(), 0
    for row in result['rows']:
        topic, variant, norm, unit = [row[k] for k in ['topic', 'variant', 'normalization', 'unit']]
        coord = (topic, variant, norm, unit)
        need(coord in allcoords and coord not in seen, 'one row per declared coordinate')
        seen.add(coord)
        additional = {k: x['metrics'][variant][norm][unit] for k, x in counts['documents'].items()}
        if topic == 'A':
            old = inputs['old_A']
            key = 'untrimmed' if variant == 'raw_untrimmed' else variant
            val = {k: x['metrics'][norm][key][unit] for k, x in old['documents'].items()}
            pairs = [('L032', 'A1'), ('L034', 'A2'), ('F016', 'A3'), ('F013', 'A4'), ('L035', 'A5'), ('N009', 'A6')]
            expected = [(s, a, val[s], val[a], 'complete_PDF_' + variant) for s, a in pairs]
            expected.append(('L128', 'A7', additional['L128'], additional['A7'], 'complete_PDF_' + variant))
            common = {'U_A': val['U_A']}
            printed = {'previous_complete_appendix': val['code'], 'A_CODE_NEW': additional['A_CODE_NEW']}
            old_raw = sum(x['metrics'][norm][unit] for x in old['complete_raw_program_files'])
        else:
            old = next(x for x in inputs['old_C']['rows'] if
                       (x['topic'], x['PDF_variant'], x['normalization'], x['unit']) == coord)
            expected = [(x['source'], x['application'], x['source_cost'], x['application_cost'],
                         x['source_representation']) for x in old['individual']]
            expected.append(('L068', 'C5', additional['L068'], additional['C5'], 'complete_PDF_' + variant))
            common = {'U_C': old['common_theory'], 'U_C_INC': additional['U_C_INC']}
            printed = {'previous_complete_appendix': old['printed_program_cost'], 'C_CODE_NEW': additional['C_CODE_NEW']}
            old_raw = old['raw_program_alternative']
        prefix = 'topic-a/' if topic == 'A' else 'topic-c/'
        def raw(category):
            return sum(x['metrics'][norm][unit] for p, x in counts['raw_files'][category].items()
                       if prefix in p)
        need(row['common_components'] == common and row['printed_program_components'] == printed,
             'complete old and new common/code components')
        need(row['raw_program_components'] == dict(previous_complete_files=old_raw,
             new_complete_file=raw('new_programs')), 'whole old bundle plus new file exactly once')
        need(row['shared_program_already_charged_once'] == (topic == 'C'), 'shared C file already paid')
        need(row['new_auxiliary_inventory'] == dict(drivers=raw('drivers'),
             partial_formal_sources=raw('formal')), 'new operational/formal costs remain separately visible')
        total_source = sum(x[2] for x in expected)
        total_apps = sum(x[3] for x in expected)
        total_common, total_printed = sum(common.values()), sum(printed.values())
        total_raw, written = old_raw + raw('new_programs'), total_common + total_apps
        for key, value in [('original_manuscripts', len(expected)), ('source_sum', total_source),
                           ('applications', total_apps), ('common_theory', total_common),
                           ('written_denominator', written), ('printed_program_cost', total_printed),
                           ('raw_program_alternative', total_raw)]:
            need(row[key] == value, 'complete coordinate ' + key)
        need(row['conditional_acquisition'] == dict(full_common=total_common,
             full_printed_programs=total_printed, full_raw_programs=total_raw,
             printed_and_raw_are_alternatives=True), 'full enlarged prepayment before every conditional row')
        need(set(row['whole']) == {'written', 'including_printed_programs', 'including_raw_programs'},
             'three whole-topic alternatives')
        for key, denom in [('written', written), ('including_printed_programs', written + total_printed),
                           ('including_raw_programs', written + total_raw)]:
            exact(row['whole'][key], total_source, denom)
            number += 1
        need(len(row['individual']) == len(expected), 'every old and new application')
        for item, (s, a, sc, ac, representation) in zip(row['individual'], expected):
            need((item['source'], item['application'], item['source_cost'], item['application_cost'],
                  item['source_representation']) == (s, a, sc, ac, representation),
                 'matched full original/application and representation')
            exact(item['conditional'], sc, ac)
            number += 1
    need(seen == allcoords and number == result['exact_fractions'] == 540, 'all sixty coordinates/540 fractions')
    for topic, variant in [('A', 'calibrated_selected'), ('C', 'raw_untrimmed')]:
        need(result['primary'][topic] == next(x for x in result['rows'] if
             (x['topic'], x['variant'], x['normalization'], x['unit']) ==
             (topic, variant, 'NFC', 'characters_without_whitespace')), 'unchanged primary representation')
    return number


def expected_bars(result):
    out = []
    for topic, r in result['primary'].items():
        s, c, a, p = [r[k] for k in ['source_sum', 'common_theory', 'applications', 'printed_program_cost']]
        for name, cost, bottom in [('source', s, 0), ('common-written', c, 0),
             ('application-written', a, c), ('common-printed', c, 0),
             ('application-printed', a, c), ('program', p, c+a)]:
            out.append(('bar-' + topic + '-' + name, name.split('-')[0], cost, bottom))
    return out


def svg_boxes(data):
    boxes = {}
    for node in ET.fromstring(data).iter():
        key = node.attrib.get('id', '')
        if not key.startswith('bar-'):
            continue
        path = next((x for x in node.iter() if x.tag.endswith('path')), None)
        need(path is not None, 'actual SVG rectangle')
        v = [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?(?:e[-+]?\d+)?', path.attrib['d'])]
        need(len(v) == 8, 'four actual vertices')
        boxes[key] = (min(v[::2]), max(v[::2]), min(v[1::2]), max(v[1::2]))
    return boxes


def check_svg(data, result):
    boxes = svg_boxes(data)
    bars = expected_bars(result)
    need(set(boxes) == {x[0] for x in bars}, 'all twelve actual SVG bars')
    first = boxes[bars[0][0]]
    scale = (first[3] - first[2]) / bars[0][2]
    for key, role, cost, bottom in bars:
        b = boxes[key]
        need(abs(b[3] - b[2] - cost * scale) < 2e-5, 'actual SVG height ' + key)
        need(abs(b[3] - (first[3] - bottom * scale)) < 2e-5, 'actual SVG baseline/stack ' + key)
    for topic in ['A', 'C']:
        for names in [('common-written', 'application-written'),
                      ('common-printed', 'application-printed', 'program')]:
            widths = [boxes['bar-' + topic + '-' + name][:2] for name in names]
            need(all(max(abs(x-y) for x, y in zip(w, widths[0])) < 2e-5 for w in widths),
                 'actual horizontal stacking')
    return len(boxes)


def pdf_boxes(path):
    reader = pypdf.PdfReader(path)
    need(len(reader.pages) == 1, 'one complete plot page')
    rgb, points, boxes = None, [], []
    for operands, op in ContentStream(reader.pages[0].get_contents(), reader).operations:
        if op == b'rg':
            rgb = tuple(float(x) for x in operands)
        elif op == b'g':
            rgb = (float(operands[0]),) * 3
        elif op == b'm':
            points = [(float(operands[0]), float(operands[1]))]
        elif op == b'l':
            points.append((float(operands[0]), float(operands[1])))
        elif op in (b'f', b'f*', b'B', b'B*'):
            role = next((k for k, color in COLORS.items() if rgb and
                         all(abs(x-y) < 1e-7 for x, y in zip(rgb, color))), None)
            if role and len(points) in (4, 5):
                boxes.append((role, min(x for x, y in points), max(x for x, y in points),
                              min(y for x, y in points), max(y for x, y in points)))
            points = []
    need(len(boxes) == 16 and [x[0] for x in boxes[-4:]] == list(COLORS) and
         all(abs(x[4] - x[3] - 5.6) < 1e-6 for x in boxes[-4:]), 'four separate legend swatches')
    return boxes[:-4]


def check_pdf(path, result):
    got, want = pdf_boxes(path), expected_bars(result)
    need(len(got) == len(want) == 12, 'twelve actual PDF rectangles')
    scale = (got[0][4] - got[0][3]) / want[0][2]
    for box, (_, role, cost, bottom) in zip(got, want):
        need(box[0] == role and abs(box[4] - box[3] - cost * scale) < 2e-5,
             'actual PDF rectangle/color')
        need(abs(box[3] - got[0][3] - bottom * scale) < 2e-5, 'actual PDF baseline/stack')
    return len(got)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--study-root', type=Path, required=True)
    ap.add_argument('--public-root', type=Path, required=True)
    ap.add_argument('--packet', type=Path, default=HERE)
    ap.add_argument('--locations', type=Path)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    need(not args.out.exists(), 'fresh report')
    p = json.loads((HERE / 'protocol.json').read_text())
    inputs = bind(p, {'study': args.study_root, 'public': args.public_root}, args.locations)
    result = json.loads((args.packet / 'results.json').read_text())
    number = arithmetic(result, inputs)
    rows = list(csv.DictReader((args.packet / 'comparisons.csv').open()))
    expect = []
    for row in result['rows']:
        factors = [('all', k, q) for k, q in row['whole'].items()]
        factors += [(i['source'], 'conditional_application', i['conditional']) for i in row['individual']]
        for source, name, q in factors:
            expect.append(dict(zip(['topic', 'source', 'variant', 'normalization', 'unit',
                                    'comparison', 'numerator', 'denominator', 'decimal'],
                 [row['topic'], source, row['variant'], row['normalization'], row['unit'], name,
                  str(q['numerator']), str(q['denominator']), q['decimal']])))
    need(rows == expect, 'all 540 exact CSV rows')
    svg = (args.packet / 'whole_costs.svg').read_text()
    sg, pg = check_svg(svg, result), check_pdf(args.packet / 'whole_costs.pdf', result)
    controls = []
    def reject(name, call):
        try:
            call()
        except (ValueError, KeyError, TypeError, StopIteration):
            controls.append(name)
            return
        raise ValueError('accepted corrupt control ' + name)
    def mutate(change):
        x = copy.deepcopy(result)
        change(x)
        arithmetic(x, inputs)
    reject('drop coordinate', lambda: mutate(lambda x: x['rows'].pop()))
    reject('duplicate coordinate', lambda: mutate(lambda x: x['rows'].append(copy.deepcopy(x['rows'][0]))))
    reject('omit earlier application', lambda: mutate(lambda x: x['rows'][0]['individual'].pop(0)))
    reject('make old common theory free', lambda: mutate(lambda x: x['rows'][0]['common_components'].update(U_A=0)))
    reject('omit complete new common note', lambda: mutate(lambda x: x['rows'][1]['common_components'].update(U_C_INC=0)))
    reject('omit old program bundle', lambda: mutate(lambda x: x['rows'][1]['raw_program_components'].update(previous_complete_files=0)))
    reject('charge shared construction twice', lambda: mutate(lambda x: x['rows'][1]['raw_program_components'].update(new_complete_file=99999)))
    reject('truncate whole program appendix', lambda: mutate(lambda x: x['rows'][0]['printed_program_components'].update(A_CODE_NEW=1)))
    reject('replace literal L108 by zero', lambda: mutate(lambda x: x['rows'][1]['individual'][2].update(source_cost=0)))
    reject('count source clauses as originals', lambda: mutate(lambda x: x.update(original_manuscripts=126)))
    reject('conditional comparison without full acquisition', lambda: mutate(lambda x: x['rows'][1]['conditional_acquisition'].update(full_common=0)))
    reject('printed plus raw duplicate charge', lambda: mutate(lambda x: x['rows'][0]['whole']['including_printed_programs'].update(denominator=1)))
    reject('change exact fraction', lambda: mutate(lambda x: x['rows'][0]['whole']['written'].update(numerator=1)))
    reject('change rounded decimal', lambda: mutate(lambda x: x['rows'][0]['whole']['written'].update(decimal='2')))
    reject('unknown external cost becomes zero', lambda: mutate(lambda x: x['unknown_costs'].update(external=0)))
    reject('infer full formalization', lambda: mutate(lambda x: x.update(full_formalization_claim=True)))
    for name, shift_all in [('distort actual bar height', False), ('shift bar preserving height', True)]:
        tree = ET.fromstring(svg)
        target = next(x for x in tree.iter() if x.attrib.get('id') == 'bar-C-application-written')
        path = next(x for x in target.iter() if x.tag.endswith('path'))
        v = [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?(?:e[-+]?\d+)?', path.attrib['d'])]
        for i in ([1, 3, 5, 7] if shift_all else [3, 5]):
            v[i] += 5
        path.attrib['d'] = f'M {v[0]} {v[1]} L {v[2]} {v[3]} L {v[4]} {v[5]} L {v[6]} {v[7]} z'
        reject(name, lambda: check_svg(ET.tostring(tree).decode(), result))
    pages = [p.extract_text() or '' for p in pypdf.PdfReader(args.packet / 'measurement.pdf').pages]
    need(len(pages) == 2, 'two reader pages')
    text = ' '.join('\n'.join(pages).split())
    for row in result['primary'].values():
        for q in list(row['whole'].values()) + [x['conditional'] for x in row['individual']]:
            need(f"{float(q['decimal']):.3f}" in text, 'reader exact three-place factor')
        for k in ['source_sum', 'common_theory', 'applications', 'printed_program_cost', 'raw_program_alternative']:
            need(f'{row[k]:,}' in text, 'reader complete component value')
    for words in ['Twelve originals', 'entire enlarged common theory', 'same diagram',
                  'complete literal rendering of L108', 'unknown costs, not zero',
                  'No scientific or conjecture credit']:
        need(words in text, 'reader scope ' + words)
    report = dict(status='AUTHOR_CHECK_PASS_PENDING_DISTINCT_REVIEW', exact_fractions=number,
                  csv_rows=len(rows), actual_svg_rectangles=sg, actual_pdf_rectangles=pg,
                  semantic_controls=controls, reader_pages=2, scientific_programs_executed=False)
    args.out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
