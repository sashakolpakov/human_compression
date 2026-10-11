#!/usr/bin/env python3
"""Check the exact edition and the two corrected proof-owner links.

This is a document-binding audit, not a replacement for the written review.
Use --research-root for the private primary records; no source text is exported.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

BASE = '9029bb003c3b419bb9aa3b2edeefca473b2143b25cc6b30dab0c9dfd663e02c0'
DELTA = '2f958b2991b71c983efa09984629045f4c1b748b1eddd29b8555b4b868f15750'
OLD = '1ffea38c96453c7d096656d84e4f664f8e61c0ced4383922d2a038fc479549ae'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest(root, expected):
    need(sha(root / 'manifest.json') == expected, 'exact manifest: ' + str(root))
    m = json.loads((root / 'manifest.json').read_text())
    for row in m['exports']:
        p = root / row['path']
        need(p.is_file() and p.stat().st_size == row['bytes'] and sha(p) == row['sha256'],
             'export: ' + row['path'])
    return m


def verify_map(base, revised, old_rows, nodes, root):
    need(set(base) == set(revised), 'unchanged top-level keys')
    need(all(base[k] == revised[k] for k in base if k != 'rows'), 'unchanged map metadata')
    need(len(revised['rows']) == 30, 'thirty source rows')
    before = {r['adapter']: r for r in base['rows']}
    after = {r['adapter']: r for r in revised['rows']}
    need(len(after) == 30 and set(after) == set(before) == set(old_rows), 'same row IDs')
    expected = {'C10': ['B3.Coordinates', 'B3.Ladder'],
                'C11': ['B3.Frattini', 'B3.Quotient']}
    for key, row in after.items():
        need(all(row[k] == v for k, v in old_rows[key].items()), 'preserved old clause: ' + key)
        permitted = {'new_tex_nodes', 'new_tex_spans'} if key in expected else set()
        need(set(row) == set(before[key]), 'same row keys: ' + key)
        need(all(row[k] == before[key][k] for k in row if k not in permitted),
             'only declared owner correction: ' + key)
        if key in expected:
            need(row['new_tex_nodes'] == expected[key], 'corrected owner identity: ' + key)
        need(row['new_tex_nodes'] == [s['id'] for s in row['new_tex_spans']],
             'owner/span consistency: ' + key)
        for span in row['new_tex_spans']:
            need(all(nodes[span['id']][k] == v for k, v in span.items()),
                 'complete bound proof span: ' + key)
    for key, row in nodes.items():
        text = (root / row['file']).read_text()
        part = text[row['start_codepoint']:row['end_codepoint_exclusive']]
        need(hashlib.sha256(part.encode()).hexdigest() == row['sha256_utf8'],
             'actual TeX proof bytes: ' + key)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--research-root', required=True, type=Path)
    ap.add_argument('--out', required=True, type=Path)
    a = ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(), 'fresh report path')
    root = a.research_root
    volume = root / 'topic_B_volume'
    delta = root / 'topic_B_volume_mapping_delta'
    m = manifest(volume, BASE)
    d = manifest(delta, DELTA)
    need(d['base_manifest_sha256'] == BASE, 'delta binds base')
    for row in m['private_retained_bindings']:
        need(sha(root / row['path']) == row['sha256'], 'primary/history binding: ' + row['path'])
    old_path = root / 'phase141_module_B_review.json'
    need(sha(old_path) == OLD, 'exact previous contract review')
    old = {r['adapter']: r for r in json.loads(old_path.read_text())['source_contracts']}
    base = json.loads((volume / 'source_contract_map.json').read_text())
    revised = json.loads((delta / 'source_contract_map.json').read_text())
    proof = json.loads((volume / 'proof_map.json').read_text())
    nodes = {r['id']: r for r in proof['nodes']}
    need(len(nodes) == 29, '29 complete proof spans')
    verify_map(base, revised, old, nodes, volume)
    rejected = []
    for label in ['old_swapped_mapping', 'changed_source_contract', 'changed_span_hash']:
        bad = copy.deepcopy(revised)
        if label == 'old_swapped_mapping':
            bad = copy.deepcopy(base)
        elif label == 'changed_source_contract':
            bad['rows'][0]['source_contract'] += ' ALTERED'
        else:
            bad['rows'][0]['new_tex_spans'][0]['sha256_utf8'] = '0' * 64
        try:
            verify_map(base, bad, old, nodes, volume)
        except ValueError:
            rejected.append(label)
    need(len(rejected) == 3, 'all meaningful document controls rejected')
    report = dict(status='PASS_BINDINGS_AND_ADDITIVE_MAPPING_CORRECTION',
                  base_manifest_sha256=BASE, delta_manifest_sha256=DELTA,
                  exports_verified=len(m['exports']) + len(d['exports']),
                  primary_history_bindings=len(m['private_retained_bindings']),
                  preserved_contract_rows=30, exact_tex_spans=29,
                  corrected_owners={'C10': ['B3.Coordinates', 'B3.Ladder'],
                                    'C11': ['B3.Frattini', 'B3.Quotient']},
                  controls_rejected=rejected,
                  mathematical_proof_verified_by_this_script=False)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
