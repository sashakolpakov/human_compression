#!/usr/bin/env python3
"""Independent semantic-interface and fixed-point closure audit of the reviewed C graph.

This checks the specifically reviewed dependency assertions. It does not discover
mathematical dependencies automatically or prove edge necessity/minimality.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(graph, coverage, expected, source_scope):
    nodes = {n['id']: n for n in graph['nodes']}
    edges = {(e['source'], e['target'], e['kind']) for e in graph['edges']}
    need(len(nodes) == len(graph['nodes']), 'unique node IDs')
    logical = set(graph['logical_edge_kinds'])
    need(logical == {'proof_use', 'definition_use', 'hypothesis_use', 'proof_assembly', 'retained_input_use'},
         'only declared mathematical edge kinds traverse')
    for src, dst in expected['required_logical_edges']:
        need(any((src, dst, kind) in edges for kind in logical), 'reviewed dependency ' + src + ' -> ' + dst)
    for src, dst in expected['forbidden_logical_edges']:
        need(not any((src, dst, kind) in edges for kind in logical), 'spurious dependency ' + src + ' -> ' + dst)
    for src, dst, kind in expected['required_typed_edges']:
        need((src, dst, kind) in edges, 'typed evidence boundary ' + src + ' -> ' + dst)
    for edge in graph['edges']:
        need(edge['source'] in nodes and edge['target'] in nodes, 'existing edge endpoints')
        if edge['kind'] in logical:
            need(nodes[edge['source']]['side'] != 'verification', 'verification is not a mathematical premise')
            need(not (nodes[edge['source']]['side'] == 'historical' and nodes[edge['target']]['side'] == 'new'),
                 'historical attribution is not silently retained as a theorem')
    need(all(n['cost'] is None for n in nodes.values()), 'unknown or unmeasured cost is null')
    need(graph['source_bindings']['L108']['original_pdf_available'] is False and
         graph['source_bindings']['L108']['pdf_cost'] is None, 'browser L108 has no original-PDF cost')
    need(graph['compression_ratio'] is None and graph['new_source_credit'] == graph['new_question_credit'] == 0,
         'no factor or research credit')
    need(graph['required_mathematical_programs'] == ['program.construction', 'program.census'],
         'both complete required programs')
    for name in expected['flagged_nodes']:
        need(nodes[name]['documentary_flags'], 'historical clause qualification ' + name)

    # Independent fixed-point relation saturation: no author adjacency helper is imported.
    ancestors = {n: {n} for n in nodes}
    for _ in range(len(nodes)):
        changed = False
        for source, target, kind in edges:
            if kind in logical:
                before = len(ancestors[target])
                ancestors[target] |= ancestors[source]
                changed |= len(ancestors[target]) != before
        if not changed:
            break
    for source, target, kind in edges:
        if kind in logical:
            need(target not in ancestors[source], 'acyclic proof relation')
    def closure(outputs):
        return sorted(set().union(*(ancestors[x] for x in outputs))) if outputs else []
    for target in ['h.J.method', 'h.J.T5.2', 'h.J.T5.4']:
        need('ext.Aschbacher' not in ancestors[target], 'no string-only recognition transferred to nonstring exercises')
    original = {r['id']: r for r in source_scope['source_result_rows']}
    rows = {r['id']: r for r in coverage['rows']}
    need(len(rows) == len(coverage['rows']) == 40 and rows.keys() == original.keys(), 'all forty fixed source rows')
    count = 0
    for name, row in rows.items():
        need(row['accepted_record'] == original[name], 'unchanged accepted record ' + name)
        for side in ['historical', 'new']:
            need(row[side + '_closure'] == closure(row[side + '_outputs']), 'actual ' + side + ' closure ' + name)
            count += 1
        if row['coverage'] == 'excluded_auxiliary':
            need(not row['new_outputs'], 'excluded comparison is not recovered')
    need(not rows['N14']['new_outputs'] and not rows['N15']['new_outputs'], 'two explicit exclusions')
    for name in ['J10', 'N13', 'P4', 'P7', 'P8']:
        need(rows[name]['coverage'] == 'corrected_or_qualified_assertion', 'corrected status ' + name)
    for name in ['F1', 'F2', 'F3', 'F4', 'F5']:
        need(not any(x.startswith('program.') for x in rows[name]['new_closure']), 'uniform F014 proof has no finite sample premise')
    need('program.construction' in rows['J1']['new_closure'] and 'program.census' in rows['J9']['new_closure'],
         'actual construction and exhaustive census routes')
    need('UC.Geometry' in rows['J11']['new_closure'], 'spherical residue identifications require the geometry')
    for source, outputs in graph['new_application_outputs'].items():
        need(graph['new_output_closures'][source] == closure(outputs), 'application closure ' + source)
        count += 1
    for source, outputs in graph['additional_current_comparisons'].items():
        need(graph['additional_comparison_closures'][source] == closure(outputs), 'additional comparison closure ' + source)
        count += 1
    return {'nodes': len(nodes), 'edges': len(edges), 'closures': count, 'source_rows': len(rows),
            'required_semantic_edges': len(expected['required_logical_edges']), 'actual_geometry_in_J11': True,
            'source_only_Aschbacher_boundary': True, 'all_costs_null': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--public-root', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(), 'fresh output file')
    root = Path(__file__).resolve().parent
    expected = json.loads((root / 'reviewed_interfaces.json').read_text())
    graph = json.loads((args.packet / 'logical_graph.json').read_text())
    coverage = json.loads((args.packet / 'coverage.json').read_text())
    scope_path = args.public_root / 'papers/topic-c/v2/scope.json'
    need(digest(scope_path) == expected['public_scope_sha256'], 'fixed public scope record')
    scope = json.loads(scope_path.read_text())
    for name, value in expected['final_packet_hashes'].items():
        need(digest(args.packet / name) == value, 'frozen final input ' + name)
    result = validate(graph, coverage, expected, scope)
    controls = []
    for source, target in expected['repair_edges_to_mutate']:
        changed = copy.deepcopy(graph)
        changed['edges'] = [e for e in changed['edges'] if (e['source'], e['target']) != (source, target)]
        try:
            validate(changed, coverage, expected, scope)
        except ValueError as exc:
            controls.append({'removed_edge': [source, target], 'rejected': True, 'reason': str(exc)})
        else:
            raise RuntimeError('Missed semantic edge corruption')
    for label in ['spurious_binary_dependency', 'source_attribution_as_premise', 'formal_as_premise',
                  'invent_L108_PDF', 'external_zero', 'omit_required_census', 'promote_exclusion']:
        g, c = copy.deepcopy(graph), copy.deepcopy(coverage)
        if label == 'spurious_binary_dependency':
            g['edges'].append({'source': 'UC.BinarySetup', 'target': 'UC.displacements', 'kind': 'definition_use'})
        elif label == 'source_attribution_as_premise':
            next(e for e in g['edges'] if e['source'] == 'h.F.displacement' and e['target'] == 'UC.displacements')['kind'] = 'proof_use'
        elif label == 'formal_as_premise':
            next(e for e in g['edges'] if e['kind'] == 'formal_scope')['kind'] = 'proof_use'
        elif label == 'invent_L108_PDF':
            g['source_bindings']['L108']['original_pdf_available'] = True
        elif label == 'external_zero':
            next(n for n in g['nodes'] if n['side'] == 'external')['cost'] = 0
        elif label == 'omit_required_census':
            g['required_mathematical_programs'].pop()
        else:
            next(r for r in c['rows'] if r['id'] == 'N15')['new_outputs'] = ['C.Halving']
        try:
            validate(g, c, expected, scope)
        except ValueError as exc:
            controls.append({'name': label, 'rejected': True, 'reason': str(exc)})
        else:
            raise RuntimeError('Missed scope corruption ' + label)
    report = {'status': 'PASS_INDEPENDENT_REVIEWED_INTERFACES_AND_CLOSURES', **result,
              'controls': controls, 'packet_manifest_sha256': digest(args.packet / 'manifest.json'),
              'semantics_basis': 'Independent full source/current proof read documented in review.json; automated checks enforce those reviewed interfaces only.',
              'weights_assigned': False, 'new_source_credit': 0, 'new_question_credit': 0}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
