#!/usr/bin/env python3
"""Independent integer permutation checks and saved-record audit; no GAP imports."""
import argparse
from collections import deque
from datetime import datetime, timezone
import hashlib
import json
from math import lcm
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def product(p, q):
    # GAP/right-action convention: apply p, then q.
    return tuple(q[i-1] for i in p)


def power(p, k):
    result = tuple(range(1, len(p)+1))
    while k:
        if k & 1:
            result = product(result, p)
        p = product(p, p)
        k //= 2
    return result


def order(p):
    seen, result = set(), 1
    for x in range(1, len(p)+1):
        if x in seen:
            continue
        y, length = x, 0
        while y not in seen:
            seen.add(y)
            length += 1
            y = p[y-1]
        result = lcm(result, length)
    return result


def word(gens, letters):
    result = tuple(range(1, len(gens[0])+1))
    for i in letters:
        result = product(result, gens[i])
    return result


def source_relations(gens):
    letters = [[i, i] for i in range(4)]
    letters += [[i, j]*m for i, j, m in
                [(0, 1, 5), (0, 2, 2), (0, 3, 2),
                 (1, 2, 3), (1, 3, 2), (2, 3, 5)]]
    letters += [[0, 1, 2]*5, ([3, 2, 1]*5+[0])*3]
    identity = tuple(range(1, len(gens[0])+1))
    assert all(word(gens, w) == identity for w in letters)
    return len(letters)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inputs', type=Path, default=Path(__file__).parent)
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).with_suffix('.json'))
    args = parser.parse_args()
    names = ['phase24_L088_seed.json', 'phase24_L088_results.json',
             'phase24_L088_coset_table.json', 'phase24_L088_run.json']
    seed, rows, table, run = [json.loads((args.inputs/n).read_text()) for n in names]
    seed = [tuple(p) for p in seed]
    assert len(seed) == 4
    assert all(sorted(p) == list(range(1, 267)) for p in seed)
    rel_count = source_relations(seed)
    a, b, c, d = seed
    w = power(word(seed, [1, 2, 3]), 5)
    wb = product(w, b)
    conj = lambda p, x: product(product(x, p), x)  # x is involutory here.
    markings = [seed, [a, wb, c, d], [a, b, c, conj(c, d)],
                [conj(b, a), b, c, d], [conj(b, a), b, c, conj(c, d)],
                [conj(wb, a), wb, c, d]]
    assert order(w) == 2
    assert all(product(w, p) == product(p, w) for p in [b, c, d])
    positive, negative, doubles = rows
    assert len(positive) == 6 and len(negative) == 2 and doubles == [10, 10]
    expected_parabolics = [[120, 20, 20, 60], [120, 20, 20, 660],
                          [120, 20, 60, 60], [120, 120, 20, 60],
                          [120, 120, 60, 60], [120, 120, 20, 660]]
    pair_count = 0
    helly_count = 0
    residue_count = 0
    for i, (mark, row) in enumerate(zip(markings, positive)):
        assert all(order(p) == 2 for p in mark)
        pairs = [order(product(mark[j], mark[k]))
                 for j in range(4) for k in range(j+1, 4)]
        assert pairs == row[1]
        pair_count += len(pairs)
        assert row[0] == 175560 and row[3] == expected_parabolics[i]
        assert row[5:9] == [1, [2, 2, 2, 2], 256, []]
        assert len(row[2]) == 16
        assert len(row[9]) == 5
        assert len(row[10]) == 11
        for subset, conditions in row[9]:
            assert len(conditions) == (16 if len(subset) == 4 else 3)
            for _, _, actual, expected in conditions:
                assert actual == expected
                helly_count += 1
        assert all(entry[2] for entry in row[10])
        residue_count += len(row[10])
    assert helly_count == 168 and residue_count == 66
    assert len({tuple(sorted(row[3])) for row in positive}) == 6
    for i, row in enumerate(negative):
        assert row[0] == 175560 and row[5] == 1 and len(row[8]) == 8
        assert row[6] == [[2, 4, 2, 2], [2, 2, 2, 4]][i]
        assert all(x[2] == x[3] for _, conditions in row[9] for x in conditions)
    assert len(table) == 8
    assert all(sorted(p) == list(range(1, 1464)) for p in table)
    assert all(table[2*i] == table[2*i+1] for i in range(4))
    coset_gens = [tuple(table[2*i]) for i in range(4)]
    assert source_relations(coset_gens) == rel_count
    assert all(p[0] == 1 for p in coset_gens[1:])
    reached, queue = {1}, deque([1])
    while queue:
        x = queue.popleft()
        for p in coset_gens:
            y = p[x-1]
            if y not in reached:
                reached.add(y)
                queue.append(y)
    assert len(reached) == 1463
    assert run['status'] == 'PASS'
    for record in run['runs']:
        assert record['exit_code'] == 0
        assert digest(args.inputs/record['script']) == record['sha256']
        assert digest(args.inputs/record['log']) == record['log_sha256']
    report = {
        'status': 'PASS', 'execution_utc': datetime.now(timezone.utc).isoformat(),
        'scope': 'Independent plain-integer permutation identities and transitive coset-table checks, plus saved GAP-result consistency. Does not independently re-enumerate subgroup closures or replay Todd–Coxeter upper-bound correctness.',
        'seed_degree': 266, 'coset_action_degree': 1463,
        'source_relations_per_action': rel_count,
        'independent_pair_order_checks': pair_count,
        'recorded_full_subgroup_meets': 1536,
        'recorded_typed_helly_equalities': helly_count,
        'recorded_residue_generation_checks': residue_count,
        'six_distinct_parabolic_order_multisets': True,
        'negative_panel_orders': [row[6] for row in negative],
        'input_hashes': {n: digest(args.inputs/n) for n in names},
        'checker_sha256': digest(Path(__file__)),
        'presentation_upper_bound_retained': 'GAP completed coset enumeration plus spherical Coxeter [3,5] order120; mere validity of a coset table is not an upper-bound certificate.',
    }
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print('L088_INDEPENDENT_DATA_PASS', pair_count, helly_count, residue_count)


if __name__ == '__main__':
    main()
