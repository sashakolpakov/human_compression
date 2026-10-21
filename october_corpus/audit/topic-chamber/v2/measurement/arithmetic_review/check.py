#!/usr/bin/env python3
"""Independent Chamber arithmetic from the accepted complete-document counts.

No author numerical implementation is imported. Gcd reduction and integer
rounding follow the previous independent Representation review.
"""
import argparse
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET

PINS = {
    'inputs': '5d37d8ad6e775792c0d8750c6984b04023ba4c657ed82625e650251da5201305',
    'input_review': '941d526343519758d0fefd8cdf7c3a2b1d2f0faae827f74a745599143c7a6abb',
    'input_adoption': '1e0e82e85874bbcc57379893e60897e024b1da463f1e8a935e3756f36f7049cf',
    'numbers': '89c751241470fc1595c26077b6862acd39e5566f961af98f62267aceada87931',
}
VARIANTS = ['raw_untrimmed', 'raw_selected', 'calibrated_selected']
FORMS = ['NFC', 'NFKC']
UNITS = ['whitespace_tokens', 'alphanumeric_units', 'characters_without_whitespace',
         'characters_with_collapsed_whitespace', 'utf8_bytes_with_collapsed_whitespace']
RAW = ['complete_mathematical_programs', 'complete_operational_drivers', 'complete_formal_files']


def need(ok, message):
    if not ok:
        raise ValueError(message)


def read(p):
    return json.loads(p.read_text())


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def quotient(n, d):
    need(type(n) is int and type(d) is int and n > 0 and d > 0, 'Positive integer costs')
    g = math.gcd(n, d)
    q, r = divmod(n * 10**12, d)
    if 2*r > d or (2*r == d and q % 2):
        q += 1
    a, b = divmod(q, 10**12)
    return dict(numerator=n, denominator=d, reduced_numerator=n//g,
                reduced_denominator=d//g, decimal=f'{a}.{b:012d}')


def expected_rows(counts):
    rows = []
    for v, f, u in itertools.product(VARIANTS, FORMS, UNITS):
        c = {k: d['variants'][v][f][u] for k, d in counts['documents'].items()}
        raw = {k: sum(d['metrics'][f][u] for d in counts[k].values()) for k in RAW}
        source = c['L008'] + c['N016']
        whole = c['U_H'] + c['H1'] + c['H2']
        role = {name: counts[RAW[0]][file]['metrics'][f][u]
                for name, file in [('required', 'chiral_cover.g'), ('diagnostic', 'reflection_models.py')]}
        rows.append(dict(variant=v, normalization=f, unit=u, documents=c,
                         raw_costs=raw, program_costs_by_role=role, source_sum=source,
                         written_denominator=whole,
                         combined={'written': quotient(source, whole),
                                   'including_printed_programs': quotient(source, whole+c['CODE']),
                                   'including_raw_programs': quotient(source, whole+raw[RAW[0]])},
                         conditional={s: dict(application=a, comparison=quotient(c[s], c[a]))
                                      for s, a in [('L008', 'H1'), ('N016', 'H2')]},
                         acquisition=dict(whole_common=c['U_H'], whole_printed_programs=c['CODE'],
                                          whole_raw_programs_alternative=raw[RAW[0]])))
    return rows


def bars(svg, primary):
    ns = {'s': 'http://www.w3.org/2000/svg'}
    root = ET.fromstring(svg)
    d = primary['documents']
    groups = [(['total-source', 'total-common', 'total-applications'],
               [primary['source_sum'], d['U_H'], d['H1']+d['H2']]),
              (['component-'+k for k in ['U_H','L008','H1','N016','H2','CODE']],
               [d[k] for k in ['U_H','L008','H1','N016','H2','CODE']])]
    checked = 0
    for ids, costs in groups:
        rectangles = []
        for gid in ids:
            path = root.find(f'.//s:g[@id="bar-{gid}"]/s:path', ns)
            need(path is not None, 'Actual bar '+gid)
            n = [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', path.get('d', ''))]
            need(len(n) == 8, 'Rectangle coordinates')
            rectangles.append((min(n[1::2]), max(n[1::2]), min(n[::2]), max(n[::2])))
        scale = (rectangles[0][1]-rectangles[0][0])/costs[0]
        for rectangle, cost in zip(rectangles, costs):
            need(abs(rectangle[1]-rectangle[0]-scale*cost) < 2e-5, 'Actual bar height')
        if ids[0] == 'total-source':
            need(abs(rectangles[0][1]-rectangles[1][1]) < 1e-6, 'Shared zero baseline')
            need(abs(rectangles[1][0]-rectangles[2][1]) < 1e-6 and
                 rectangles[1][2:] == rectangles[2][2:], 'Whole common/application stack')
        else:
            need(max(r[1] for r in rectangles)-min(r[1] for r in rectangles) < 1e-6,
                 'Component zero baselines')
        checked += len(ids)
    return checked


def main():
    ap = argparse.ArgumentParser()
    for k in PINS:
        ap.add_argument('--'+k.replace('_','-'), type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    need(not a.out.exists(), 'Fresh output')
    for role, pin in PINS.items():
        folder = getattr(a, role)
        need(sha(folder/'manifest.json') == pin, 'Accepted manifest '+role)
        for row in read(folder/'manifest.json')['exports']:
            p = folder/row['path']
            need(p.stat().st_size == row['bytes'] and sha(p) == row['sha256'], 'Bound export '+str(p))
    counts = read(a.inputs/'input_counts.json')
    recounted = read(a.input_review/'recount.json')
    need(set(counts['documents']) == {'L008','N016','U_H','H1','H2','CODE'}, 'Six complete documents')
    for k, d in counts['documents'].items():
        need(d['variants'] == recounted['documents'][k]['variants'], 'Independent primitive PDF costs')
    for k in RAW:
        need(counts[k] == recounted['raw_files'][k], 'Independent complete raw costs')
    need([len(counts[k]) for k in RAW] == [2,3,3], 'Whole executable and formal file inventory')
    expected = expected_rows(counts)
    actual = read(a.numbers/'results.json')
    need(actual['coordinates'] == expected, 'Every complete coordinate record agrees')
    primary = expected[22]
    need(actual['primary'] == primary and primary['unit'] == UNITS[2], 'Primary coordinate')
    need((actual['principal_source_manuscripts'], actual['detailed_source_rows'],
          actual['proof_contexts'], actual['exact_fractions']) == (2,27,22,150), 'Scope and fraction counts')
    b = actual['boundary']
    need(b['whole_common_once_within_topic'] and not b['cross_topic_discount'], 'Whole topic costs')
    need(not b['end_to_end_formalized'] and not b['full_all_rank_finite_cover_answer'], 'Formal and question limits')
    need(all(b[k] is None for k in ['retained_external_proof_cost','historical_software_cost',
                                  'graphics_and_formula_layout_cost','operational_engineering_cost']), 'Unknown costs')
    need(b['required_mathematical_programs'] == b['diagnostic_programs'] == 1, 'Program roles')
    need(read(a.numbers/'protocol.json')['conditional_prepayment'] == ['U_H','both_complete_programs'],
         'Full prior acquisition for each conditional')
    with (a.numbers/'comparisons.csv').open(newline='') as f:
        saved = list(csv.DictReader(f))
    csvrows = []
    for r in expected:
        values = list(r['combined'].items())+[(s+'_conditional', x['comparison']) for s,x in r['conditional'].items()]
        for name, q in values:
            csvrows.append(dict(variant=r['variant'], normalization=r['normalization'], unit=r['unit'],
                                comparison=name, **{k:str(v) for k,v in q.items()}))
    need(saved == csvrows and len(csvrows) == 150, 'Every CSV numerator, denominator and display')
    bar_count = bars((a.numbers/'complete_costs.svg').read_text(), primary)
    tex = (a.numbers/'measurement.tex').read_text()
    for n in [*primary['documents'].values(), primary['source_sum'], primary['written_denominator'],
              *primary['raw_costs'].values()]:
        need(str(n) in tex, 'Reader complete cost')
    for phrase in ['whole common paper and both complete programs', 'alternatives,\nnever added together',
                   'not a complete\nLean verification', 'remains unresolved',
                   'printed source software and other ancillary claims are\noutside the replacement contract']:
        need(phrase in tex, 'Reader scope: '+phrase)
    report = dict(status='PASS_INDEPENDENT_ROOT_CHAMBER_ARITHMETIC', reviewer='root',
                  accepted_manifests=PINS, primitive_PDF_cells=180, primitive_raw_cells=80,
                  coordinates=30, exact_fractions=150, CSV_rows=150, actual_SVG_bars=bar_count,
                  primary=primary, method='No author arithmetic imports; integer sums, gcd and nearest-even rounding.',
                  scientific_and_input_adoptions_retained=True, fresh_Lean_or_GAP_replay=False,
                  numerical_author_is_distinct=True, primary_text_exported=False, new_credit=0)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','coordinates','exact_fractions','CSV_rows','actual_SVG_bars']}))


if __name__ == '__main__':
    main()
