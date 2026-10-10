#!/usr/bin/env python3
"""Check literal Lean graph data and the binding of its successful compile."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

GRAPH_SHA = 'b3cf789f5278c773636a9e440a06115dd023b11c0519bbe3c68a51ce33b3c0d6'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', type=Path, default=Path(__file__).parent)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--compile-report', type=Path)
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).with_suffix('.json'))
    args = parser.parse_args()
    source = args.source or args.inputs/'formal/Phase23TransferAnnihilator.lean'
    compile_path = args.compile_report or source.with_suffix('.check.json')
    graph_path = args.inputs/'phase22_excess3_final.graph.json'
    assert sha(graph_path) == GRAPH_SHA
    initial, states, edges, _ = json.loads(graph_path.read_text())
    text = source.read_text()
    match = re.search(r'def initialRows[^\n]*:= #\[(.*?)\]\n', text, re.S)
    assert match
    literal_initial = [list(map(int, m)) for m in
                       re.findall(r'\((\d+), (\d+)\)', match[1])]
    match = re.search(r'def edges[^\n]*:= #\[(.*?)\]\n', text, re.S)
    assert match
    literal_edges = [list(map(int, m)) for m in
                     re.findall(r'\((\d+), (\d+), (\d+)\)', match[1])]
    assert literal_initial == initial and literal_edges == edges
    assert (len(initial), len(states), len(edges)) == (706, 708, 1522)
    assert 'def stateCount : Nat := 708' in text
    assert 'def dimension : Nat := 4 * stateCount' in text
    assert GRAPH_SHA in text
    assert all(1 <= s <= 708 and 0 <= k <= 3 for s, k in initial)
    assert all(1 <= s <= 708 and 1 <= t <= 708 and 0 <= w <= 3
               for s, t, w in edges)
    # These bounds ensure every read/write in the actual operator is in range.
    assert all(0 <= 4*(s-1)+k < 2832 and
               0 <= 4*(t-1)+k+w < 2832
               for s, t, w in edges for k in range(4-w))
    compile_record = json.loads(compile_path.read_text())
    assert compile_record['exit_code'] == 0
    assert compile_record['sha256'] == sha(source)
    assert 'version 4.32.2,' in compile_record['lean']
    output = compile_record['stdout']
    assert 'sorryAx' not in output and 'error:' not in output
    claims = ['third_difference', 'terminal_basis_fixed',
              'fourth_difference', 'newton_coefficients']
    assert output.count('native_decide.ax_1_1') == 4
    for name in claims:
        assert f'{name}._native.native_decide.ax_1_1' in output
    assert 'literal_data_dimensions\' does not depend on any axioms' in output
    report = {
        'status': 'PASS',
        'execution_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Literal-data equality and saved successful Lean compilation binding; not a second Lean execution or group census.',
        'graph_sha256': GRAPH_SHA,
        'source_sha256': sha(source),
        'compile_report_sha256': sha(compile_path),
        'checker_sha256': sha(Path(__file__)),
        'literal_initial_rows': len(initial),
        'literal_edges': len(edges),
        'states': len(states),
        'integer_coordinates': 4*len(states),
        'all_operator_indices_in_range': True,
        'native_checked_closed_claims': claims,
        'native_evaluation_axioms': [f'{n}._native.native_decide.ax_1_1'
                                     for n in claims],
        'ordinary_axioms_on_native_claims': ['propext', 'Quot.sound'],
        'kernel_only_claim': 'literal_data_dimensions',
        'trust_boundary': 'The four numeric identities trust Lean native compiler/interpreter evaluation; group-to-graph completeness and all-rank algebra remain outside this module.',
    }
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: report[k] for k in
                      ['status', 'literal_initial_rows', 'literal_edges',
                       'integer_coordinates', 'source_sha256']}))


if __name__ == '__main__':
    main()
