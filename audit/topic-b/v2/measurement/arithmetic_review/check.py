#!/usr/bin/env python3
"""Independent Topic B arithmetic/CSV audit; does not import either counter."""
import argparse
import copy
import csv
import hashlib
import json
from fractions import Fraction
from pathlib import Path

PAIRS = [('N001', 'B1'), ('N003', 'B2'), ('N008', 'B3'), ('L030', 'B4')]
VARIANTS = ['raw_untrimmed', 'raw_selected', 'calibrated_selected']
FORMS = ['NFC', 'NFKC']
UNITS = ['whitespace_tokens', 'alphanumeric_units', 'characters_without_whitespace',
         'characters_with_collapsed_whitespace', 'utf8_bytes_with_collapsed_whitespace']

def need(ok, message):
    if not ok:
        raise ValueError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text())

def audit(result, author, independent, overall, conditional):
    documents = independent['documents']
    need(set(documents) == {'N003', 'N008', 'L030', 'U_B', 'B1', 'B2', 'B3', 'B4'}, 'document roster')
    need(set(author['documents']) == set(documents), 'author document roster')
    for key, row in documents.items():
        need(row == author['documents'][key]['variants'], 'accepted count equality: '+key)
    need(author['source_pdf_metrics_unknown'] == {'N001': None}, 'missing PDF remains unknown')
    need(author['four_source_pdf_total'] is None, 'source total remains unknown')
    need(len(result['coordinates']) == 30 and len(overall) == 30 and len(conditional) == 120,
         'complete coordinate and CSV cardinalities')
    expected_keys = {(v, f, u) for v in VARIANTS for f in FORMS for u in UNITS}
    rows = {(x['variant'], x['normalization'], x['unit']): x for x in result['coordinates']}
    need(set(rows) == expected_keys, 'distinct complete coordinate keys')
    overall_rows = {(x['variant'], x['normalization'], x['unit']): x for x in overall}
    conditional_rows = {(x['variant'], x['normalization'], x['unit'], x['source']): x for x in conditional}
    need(set(overall_rows) == expected_keys, 'overall CSV keys')
    need(set(conditional_rows) == {k+(s,) for k in expected_keys for s, _ in PAIRS}, 'conditional CSV keys')
    for key in sorted(expected_keys):
        v, f, u = key
        costs = {name: d[v][f][u] for name, d in documents.items()}
        need(all(type(c) is int and c > 0 for c in costs.values()), 'positive integer measured costs')
        common = costs['U_B']
        applications = sum(costs[b] for _, b in PAIRS)
        source = costs['N003'] + costs['N008'] + costs['L030']
        row = rows[key]
        need(row['common_theory'] == common and row['all_applications'] == applications
             and row['complete_denominator'] == common+applications, 'whole denominator, U once and all four apps')
        need(row['known_source_sum'] == source and row['unknown_source'] == 'N001'
             and row['complete_source_sum'] is None and row['overall_factor'] is None, 'unknown complete numerator/factor')
        need(row['overall_formula'] == {'unknown_numerator_coefficient': 1,
             'known_numerator': source, 'denominator': common+applications}, 'symbolic complete formula')
        need([(r['source'], r['application']) for r in row['per_result']] == PAIRS, 'exact matching of applications')
        for r, (s, b) in zip(row['per_result'], PAIRS):
            need(r['application_cost'] == costs[b], 'application cost')
            numerator = costs.get(s)
            need(r['source_cost'] == numerator, 'source cost')
            if numerator is None:
                need(r['fraction'] is None and r['factor'] is None, 'unknown conditional')
            else:
                q = Fraction(numerator, costs[b])
                need(r['fraction'] == str(q) and r['factor'] == float(q), 'exact and floating conditional quotient')
            c = conditional_rows[key+(s,)]
            need(c == dict(variant=v, normalization=f, unit=u,
                 whole_common_theory_prepaid=str(common), source=s, application=b,
                 source_cost='unknown' if numerator is None else str(numerator),
                 application_cost=str(costs[b]), exact_fraction='unknown' if numerator is None else str(q),
                 factor='unknown' if numerator is None else str(float(q))), 'conditional CSV values')
        need(overall_rows[key] == dict(variant=v, normalization=f, unit=u,
             known_source_sum=str(source), unknown_source='N001', common_theory=str(common),
             all_four_applications=str(applications), complete_denominator=str(common+applications),
             overall_factor='unknown'), 'overall CSV values')
    main = rows[('calibrated_selected', 'NFC', 'characters_without_whitespace')]
    need(result['primary'] == main, 'headline equals declared coordinate')
    for key in ['outside_proof_cost', 'unextracted_graphic_cost', 'minimum_mathematical_complexity', 'N001_pdf_pages']:
        need(result[key] is None, 'unknown boundary: '+key)
    need(result['complete_common_theory_prepaid_for_conditional_factors'] is True
         and result['common_theory_discount_for_other_topics'] is False
         and result['all_four_applications_charged'] is True, 'whole-topic acquisition policy')
    need(result['required_mathematical_programs'] == [] and result['required_program_cost'] == 0,
         'no proof-producing program in this edition')
    for key, value in {'known_conditional_fractions':90, 'unknown_conditional_coordinates':30,
                       'unknown_overall_coordinates':30, 'source_pages_available':31,
                       'replacement_scientific_pages':22, 'new_source_credit':0,
                       'new_question_credit':0}.items():
        need(result[key] == value, 'scope count: '+key)
    return main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--packet', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    need(not args.out.exists(), 'fresh output path required')
    root = args.packet.resolve()
    bound = {}
    manifest = read(root/'manifest.json')
    need(digest(root/'manifest.json') == 'c61503c52b1e0136b0eb70ebe7993c63dc635933e6ae0bf9a50d7c164d211609',
         'exact frozen numerical packet')
    for item in manifest['exports']:
        p = root/item['path']
        need(p.is_file() and p.stat().st_size == item['bytes'] and digest(p) == item['sha256'],
             'frozen result export: '+str(p))
    for sub in ['inputs', 'independent']:
        m = read(root/sub/'manifest.json')
        bound[sub+'/manifest.json'] = digest(root/sub/'manifest.json')
        for item in m['exports']:
            p = root/sub/item['path']
            need(p.is_file() and p.stat().st_size == item['bytes'] and digest(p) == item['sha256'],
                 'frozen dependency: '+str(p))
            bound[sub+'/'+item['path']] = digest(p)
    result, author, independent = [read(root/p) for p in
        ['results.json', 'inputs/author_counts.json', 'independent/recount.json']]
    with (root/'overall_costs.csv').open(newline='') as f: overall = list(csv.DictReader(f))
    with (root/'conditional_costs.csv').open(newline='') as f: conditional = list(csv.DictReader(f))
    primary = audit(result, author, independent, overall, conditional)
    for name, h in result['bindings'].items():
        need(digest(root/name) == h, 'result input hash: '+name)
    acceptance = read(root/'independent/review.json')
    need(acceptance['status'] == 'ACCEPT_INDEPENDENT_DOCUMENT_MEASUREMENT'
         and acceptance['proposal_manifest_sha256'] == digest(root/'inputs/manifest.json'),
         'accepted numerical input provenance')
    controls = []
    mutations = [
        ('drop_B1_from_denominator', lambda r,o,c: r['coordinates'][0].__setitem__('complete_denominator',r['coordinates'][0]['complete_denominator']-r['coordinates'][0]['per_result'][0]['application_cost'])),
        ('invent_N001_zero_cost', lambda r,o,c: r['coordinates'][0]['per_result'][0].__setitem__('source_cost',0)),
        ('invent_overall_factor', lambda r,o,c: r['coordinates'][0].__setitem__('overall_factor',1.2)),
        ('wrong_exact_fraction', lambda r,o,c: r['coordinates'][0]['per_result'][1].__setitem__('fraction','1')),
        ('wrong_CSV_fraction', lambda r,o,c: c[1].__setitem__('exact_fraction','1')),
        ('wrong_CSV_total', lambda r,o,c: o[0].__setitem__('complete_denominator','1')),
        ('hide_umbrella_acquisition', lambda r,o,c: r.__setitem__('complete_common_theory_prepaid_for_conditional_factors',False)),
        ('unknown_external_cost_as_zero', lambda r,o,c: r.__setitem__('outside_proof_cost',0)),
        ('add_source_credit', lambda r,o,c: r.__setitem__('new_source_credit',1)),
    ]
    for name, mutate in mutations:
        r,o,c = copy.deepcopy((result,overall,conditional)); mutate(r,o,c)
        try: audit(r,author,independent,o,c)
        except ValueError as e: controls.append(dict(name=name,status='REJECTED',reason=str(e)))
        else: raise ValueError('control not rejected: '+name)
    render = read(root/'render_report.json')
    need(render['results_sha256'] == digest(root/'results.json') and render['pages'] == 2
         and render['diagnostics'] == [], 'reader render binding')
    from pypdf import PdfReader
    pages = [p.extract_text() for p in PdfReader(root/'measurement.pdf').pages]
    need([hashlib.sha256(s.encode()).hexdigest() for s in pages] == render['text_hashes'], 'reader page text hashes')
    for item in render['artifacts']:
        p=root/item['path']; need(digest(p)==item['sha256'] and p.stat().st_size==item['bytes'], 'reader/figure artifact binding')
    text='\n'.join(pages)
    for value in ['14,119','44,942','59,061','57,539','17,765','14,165','17,537','11,128','22,237','12,281','7,368','1.254','1.576','1.811']:
        need(value in text,'printed primary value: '+value)
    need(len(pages)==2 and not any(ord(c)<32 and not c.isspace() or ord(c)==0xfffd or 0xe000<=ord(c)<=0xf8ff for c in text), 'reader pages and glyph scan')
    for p in root.rglob('*'):
        if p.is_file() and p.suffix != '.pyc': bound[str(p.relative_to(root))]=digest(p)
    report=dict(status='PASS_INDEPENDENT_ARITHMETIC_AND_READER_BINDINGS',
        scope='All arithmetic is recomputed from accepted measured inputs without importing compute.py or either document counter. No fresh primary-PDF extraction or mathematical re-review is claimed.',
        coordinates=30, exact_known_conditional_fractions=90, unknown_conditional_coordinates=30,
        unknown_overall_coordinates=30, overall_CSV_rows=30, conditional_CSV_rows=120,
        primary=primary, controls=controls, reader_pages=2, reader_page_hashes=render['text_hashes'],
        input_hashes=bound, checker_sha256=digest(Path(__file__)),
        visual_review='Recorded separately by reviewer; this script checks extraction and bound render artifacts only.')
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','coordinates','exact_known_conditional_fractions','reader_pages']}))

if __name__ == '__main__': main()
