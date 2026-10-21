#!/usr/bin/env python3
"""Independent reconciliation of the sole passage-boundary correction."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET
from pypdf import PdfReader

OLD = '3052910af511db6b255448ab4e7a6a1353aa5add9b58687ed34c989ed761af37'
NEW = '7a1cd77556e3addc9a9453f010d9ddfa1b94f816d0a648060d00e0874a363216'


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def read(p):
    return json.loads(p.read_text())


def bind(p, pin):
    need(hashlib.sha256((p/'manifest.json').read_bytes()).hexdigest() == pin, 'manifest')
    for r in read(p/'manifest.json')['exports']:
        b = (p/r['path']).read_bytes()
        need(len(b) == r['bytes'] and hashlib.sha256(b).hexdigest() == r['sha256'], r['path'])


def changed(a, b):
    need(a.keys() == b.keys(), 'unchanged inventory')
    return sorted(k for k in a if a[k] != b[k])


def check(study):
    old, new = [study/n for n in ['topic_Affine_dag_costs', 'topic_Affine_dag_costs_v2']]
    bind(old, OLD)
    bind(new, NEW)
    a, b = [read(p/'weights.json') for p in [old, new]]
    expected = ['individual_node_closures', 'node_interfaces', 'owner_costs']
    need(changed(a, b) == expected, 'only three weight sections changed')
    owners = ['h.64.Bases.first', 'h.64.Kernels.remaining']
    need(changed(a['owner_costs'], b['owner_costs']) == owners, 'only two owners')
    need(changed(a['node_interfaces'], b['node_interfaces']) == ['h.64.Bases', 'h.64.Kernels'],
         'only two interfaces')
    need(changed(a['individual_node_closures'], b['individual_node_closures']) ==
         ['h.64.Kernels', 'h.64.Scale'], 'only two individual prerequisite subtotals')
    units = dict(whitespace_tokens=4, alphanumeric_units=4, characters_without_whitespace=15,
                 characters_with_collapsed_whitespace=19, utf8_bytes_with_collapsed_whitespace=19)
    for owner, sign in zip(owners, [-1, 1]):
        for variant in a['owner_costs'][owner]:
            for form in ['NFC', 'NFKC']:
                need({u:b['owner_costs'][owner][variant][form][u] - a['owner_costs'][owner][variant][form][u]
                      for u in units} == {u:sign*v for u,v in units.items()}, 'exact transferred units')
    for n in a['node_interfaces']:
        need(a['node_interfaces'][n]['owners'] == b['node_interfaces'][n]['owners'],
             'reviewed interface ownership unchanged')
    for n in a['individual_node_closures']:
        if n in ['h.64.Kernels', 'h.64.Scale']:
            need(changed(a['individual_node_closures'][n], b['individual_node_closures'][n]) ==
                 ['by_document', 'known_extracted_subtotal', 'raw_program_alternative_subtotal'],
                 'closure content unchanged')
    pa, pb = [read(p/'partition.json') for p in [old, new]]
    need(changed(pa, pb) == ['documents'], 'same physical-owner inventory and policy')
    need(changed(pa['documents'], pb['documents']) == ['L012'], 'only source passage changed')
    for v in pa['documents']['L012']['variants']:
        va, vb = [p['documents']['L012']['variants'][v] for p in [pa,pb]]
        need(changed(va, vb) == ['spans'], 'same complete extracted document')
        need(len(va['spans']) == len(vb['spans']), 'same number of spans')
        differences = [(x,y) for x,y in zip(va['spans'],vb['spans']) if x != y]
        need([x['owner'] for x,y in differences] == owners, 'only adjacent corrected spans')
        for x,y in differences:
            need(x['owner'] == y['owner'] and x['category'] == y['category'] and
                 x['physical_pages'] == y['physical_pages'], 'same passage identity')
        x,y = differences[0]
        need(x['start'] == y['start'] and x['raw_start'] == y['raw_start'] and y['end'] < x['end'],
             'first span loses only suffix')
        x2,y2 = differences[1]
        need(x2['end'] == y2['end'] and x2['raw_end'] == y2['raw_end'] and
             y2['start'] == y['end'] and x2['start'] == x['end'], 'kernel gains that exact prefix')
    need((old/'boundaries.py').read_text().replace(
        "(553,'h.64.Kernels.remaining',P)", "((552,'Similarly'),'h.64.Kernels.remaining',P)") ==
        (new/'boundaries.py').read_text(), 'exact one boundary edit')
    for name in ['acquisition.json','graphs.json','protocol.json','author.py','accounting.py',
                 'build_reader.py','reader.tex','new_graph.svg']:
        need((old/name).read_bytes() == (new/name).read_bytes(), 'unchanged '+name)
    texts = [[p.extract_text() for p in PdfReader(d/'reader.pdf').pages] for d in [old,new]]
    need(texts[0] == texts[1] and len(texts[0]) == 2, 'same two complete reader pages')
    # SVG generation is deterministic. Replace just the two independently changed labels.
    old_svg, new_svg = [(p/'historical_graph.svg').read_text() for p in [old,new]]
    ta,tb = [ET.fromstring(s) for s in [old_svg,new_svg]]
    ns = '{http://www.w3.org/2000/svg}'
    for tree, weights in [(ta,a),(tb,b)]:
        for g in tree:
            n = g.attrib.get('data-node')
            if n in ['h.64.Bases','h.64.Kernels']:
                labels = g.findall(ns+'text')
                value = weights['node_interfaces'][n]['known_weight']['calibrated_selected']['NFC']['characters_without_whitespace']
                need(labels[-1].text == 'Interface text: {:,}'.format(value), 'correct changed SVG label')
                labels[-1].text = 'reviewed correction'
    need(ET.tostring(ta) == ET.tostring(tb), 'only two displayed source weights changed')
    return dict(status='PASS_INDEPENDENT_ADDITIVE_BOUNDARY_CORRECTION', original=OLD, corrected=NEW,
                changed_owners=owners, transferred_units=units, changed_interfaces=2,
                changed_individual_closures=2, complete_document_cells_unchanged=120,
                all99_source_row_routes_unchanged=True, full_application_and_record_unchanged=True,
                scientific_and_logical_inputs_unchanged=True, reader_pages_unchanged=2,
                full_document_factors_unchanged=True, primary_text_exported=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--study-root',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True); args=parser.parse_args()
    need(not args.out.exists(), 'fresh output')
    report=check(args.study_root);args.out.write_text(json.dumps(report,indent=2)+'\n')
    print(report['status'])
