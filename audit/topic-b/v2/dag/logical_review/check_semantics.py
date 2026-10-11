#!/usr/bin/env python3
"""Check the finite interfaces repaired during the independent edge review.

This script does not automate the mathematical reading recorded in review.json.
It independently recomputes prerequisite closures and protects the five repairs.
"""
import argparse
import copy
import hashlib
import json
from collections import Counter
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def inspect(graph, coverage):
    nodes = {n['id']: n for n in graph['nodes']}
    kinds = set(graph['logical_edge_kinds'])
    pairs = {(e['source'], e['target']) for e in graph['edges']
             if e['kind'] in kinds}
    for pair in [
        ('h.N008.T3.1.ladder', 'h.N008.T3.1.propagation'),
        ('ext.CFSG', 'ext.W1'),
        ('h.L030.L2.2', 'h.L030.L3.3'),
    ]:
        require(pair in pairs, 'reviewed prerequisite missing: ' + repr(pair))
    require(all(n['cost'] is None for n in nodes.values()),
            'unweighted or unknown costs cannot become zero')
    require(graph['source_bindings']['N001']['primary_pdf'] is None,
            'missing N001 PDF must remain missing')
    require(graph['required_mathematical_programs'] == [],
            'this topic has no required mathematical census')
    parents = {n: set() for n in nodes}
    for a, b in pairs:
        require(a in nodes and b in nodes, 'edge endpoint is absent')
        require(nodes[a]['side'] != 'verification', 'verification is not a premise')
        parents[b].add(a)
    visiting, done = set(), set()
    def visit(n):
        require(n not in visiting, 'logical dependency cycle')
        if n in done:
            return
        visiting.add(n)
        for p in parents[n]:
            visit(p)
        visiting.remove(n)
        done.add(n)
    for n in nodes:
        visit(n)
    def closure(outputs):
        reached = set(outputs)
        pending = list(outputs)
        while pending:
            n = pending.pop()
            for p in parents[n] - reached:
                reached.add(p)
                pending.append(p)
        return reached
    rows = {r['adapter']: r for r in coverage['rows']}
    require(len(rows) == 30, 'thirty fixed source clauses')
    require(Counter(r['source_id'] for r in rows.values()) ==
            {'N001': 4, 'N003': 8, 'N008': 11, 'L030': 7},
            'complete four-source boundary')
    require('B2.Extremal' in rows['B4']['new_outputs'],
            'arbitrary extremal family needs its classification')
    require('B3.Frattini.containment' in rows['C11']['new_outputs'],
            'Frattini containment must accompany the general core identity')
    for row in rows.values():
        require(closure(row['new_outputs']) == set(row['new_closure']),
                'replacement closure: ' + row['adapter'])
        require(closure([row['historical_output']]) == set(row['historical_closure']),
                'historical closure: ' + row['adapter'])
    for app, output in graph['new_application_outputs'].items():
        require(closure([output]) == set(graph['new_output_closures'][app]),
                'complete application closure: ' + app)
    require(nodes['h.L030.L3.3']['documentary_flags'],
            'the printed connectedness shortcut needs a qualification')
    return {'nodes': len(nodes), 'edges': len(graph['edges']),
            'source_clauses': len(rows), 'independently_recomputed_closures': 64}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    require(not args.out.exists(), 'output must be fresh')
    gp = args.packet / 'logical_graph.json'
    cp = args.packet / 'coverage.json'
    graph, coverage = json.loads(gp.read_text()), json.loads(cp.read_text())
    result = inspect(graph, coverage)
    controls = []
    for name in ['missing_chain_setup', 'missing_extremal_classification',
                 'missing_frattini_containment', 'missing_retained_classification',
                 'missing_connectedness_premise']:
        g, c = copy.deepcopy(graph), copy.deepcopy(coverage)
        pair = None
        if name == 'missing_chain_setup':
            pair = ('h.N008.T3.1.ladder', 'h.N008.T3.1.propagation')
        elif name == 'missing_retained_classification':
            pair = ('ext.CFSG', 'ext.W1')
        elif name == 'missing_connectedness_premise':
            pair = ('h.L030.L2.2', 'h.L030.L3.3')
        elif name == 'missing_extremal_classification':
            next(r for r in c['rows'] if r['adapter'] == 'B4')['new_outputs'].remove('B2.Extremal')
        else:
            next(r for r in c['rows'] if r['adapter'] == 'C11')['new_outputs'].remove('B3.Frattini.containment')
        if pair:
            g['edges'] = [e for e in g['edges'] if (e['source'], e['target']) != pair]
        try:
            inspect(g, c)
        except ValueError as exc:
            controls.append({'name': name, 'rejected': True, 'reason': str(exc)})
        else:
            raise RuntimeError('accepted the removed prerequisite: ' + name)
    output = {'status': 'PASS_INDEPENDENT_REVIEW_INTERFACES', **result,
              'graph_sha256': hashlib.sha256(gp.read_bytes()).hexdigest(),
              'coverage_sha256': hashlib.sha256(cp.read_bytes()).hexdigest(),
              'controls': controls,
              'mathematical_proof_review_is_separate_written_work': True,
              'cost_weights_assigned': False, 'new_mathematical_credit': False}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(output))


if __name__ == '__main__':
    main()
