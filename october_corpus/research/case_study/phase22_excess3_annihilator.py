#!/usr/bin/env python3
"""Exact all-rank transfer certificate, independently coded from saved graph.

Uses only Python's standard library. Does not regenerate GAP groups.
Writes only --output (default beside this script).
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import json
from pathlib import Path


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summary(vector):
    sparse = [[i, n] for i, n in enumerate(vector) if n]
    return {'nonzero_coordinates': len(sparse),
            'coordinate_sum_by_excess': [sum(vector[k::4]) for k in range(4)],
            'sparse_zero_based_vector': sparse,
            'dense_vector_sha256': hashlib.sha256(
                json.dumps(vector, separators=(',', ':')).encode()).hexdigest()}


def expand_newton(start, coefficients):
    # Independent polynomial arithmetic, using falling products and fractions.
    answer = [Fraction(0)] * len(coefficients)
    basis, factorial = [Fraction(1)], 1
    for j, coefficient in enumerate(coefficients):
        if j:
            factorial *= j
        for i, value in enumerate(basis):
            answer[i] += coefficient*value/factorial
        new = [Fraction(0)]*(len(basis)+1)
        for i, value in enumerate(basis):
            new[i] -= (start+j)*value
            new[i+1] += value
        basis = new
    return answer


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--inputs', type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument('--output', type=Path,
                    default=Path(__file__).with_suffix('.json'))
    args = ap.parse_args()
    p = args.inputs
    names = ['phase22_excess3_final.graph.json',
             'phase22_excess3_final.windows.json',
             'phase22_excess3_final.gluings.json',
             'phase21_rank3_census.json', 'phase21_rank4_census.json',
             'phase21_rank5_census.json']
    objects = [json.loads((p/n).read_text()) for n in names]
    initial, states, edges, saved_rows = objects[0]
    windows, gluings, rank3, rank4, rank5 = objects[1:]
    count, dimension = len(states), 4*len(states)
    assert count == 708 and dimension == 2832 and len(edges) == 1522
    assert Counter(w[1] for w in windows) == {0: 1, 1: 15, 2: 106, 3: 584}
    assert len({tuple(w[0]) for w in windows}) == len(windows) == 706
    assert rank4['universal_order'] == 2**34
    assert rank5['universal_gamma3_order'] == 2**42
    # Canonical pcgs relative factors all have order2, as checked by GAP.
    # Therefore key length recovers subgroup order and transition weight.
    for key, excess, first, last in windows:
        assert len(key) == 42-excess
        assert 0 <= 34-len(first)-7 <= excess
        assert 0 <= 34-len(last)-7 <= excess
    for window, kernel_key, cost, order in states:
        assert order == 2**len(kernel_key)
        assert windows[window-1][1] <= cost <= 3
    assert len({(s[0], tuple(s[1])) for s in states}) == count

    by_first = defaultdict(list)
    for i, w in enumerate(windows, 1):
        by_first[tuple(w[2])].append(i)
    overlap_count = sum(len(by_first[tuple(w[3])]) for w in windows)
    assert overlap_count == 3689
    expected_pairs, budget_rejected = set(), 0
    for source, (old_window, _, cost, _) in enumerate(states, 1):
        old = windows[old_window-1]
        for new_window in by_first[tuple(old[3])]:
            new = windows[new_window-1]
            boundary_excess = 34-len(new[2])-7
            weight = new[1]-boundary_excess
            assert 0 <= weight <= 3
            if cost+weight <= 3:
                expected_pairs.add((source, new_window, weight))
            else:
                budget_rejected += 1
    observed_pairs = set()
    for source, target, weight in edges:
        old = windows[states[source-1][0]-1]
        new_window = states[target-1][0]
        new = windows[new_window-1]
        assert old[3] == new[2]
        assert weight == new[1]-(34-len(new[2])-7)
        observed_pairs.add((source, new_window, weight))
    assert len(observed_pairs) == len(edges)
    assert observed_pairs == expected_pairs
    assert budget_rejected == 2185
    # This verifies graph completeness conditional on the recorded fact that
    # all budget-eligible transitions pass both group compatibility tests.

    distance = [99]*count
    for state, excess in initial:
        distance[state-1] = min(distance[state-1], excess)
    changed, rounds = True, 0
    while changed:
        changed = False
        rounds += 1
        assert rounds <= count
        for source, target, weight in edges:
            value = distance[source-1]+weight
            if value < distance[target-1]:
                distance[target-1] = value
                changed = True
    assert distance == [s[2] for s in states]

    # Column vector convention: coordinate4(s-1)+k corresponds to (s,k).
    def transfer(v):
        out = [0]*dimension
        for source, target, weight in edges:
            s, t = 4*(source-1), 4*(target-1)
            for k in range(4-weight):
                out[t+k+weight] += v[s+k]
        return out

    def delta(v):
        return [a-b for a, b in zip(transfer(v), v)]

    v = [0]*dimension
    for state, excess in initial:
        v[4*(state-1)+excess] += 1
    vectors, recount = {}, []
    for d in range(5, 25):
        vectors[d] = v
        recount.append([d]+[sum(v[k::4]) for k in range(4)])
        v = transfer(v)
    assert recount == saved_rows
    differences = [vectors[7]]
    for _ in range(4):
        differences.append(delta(differences[-1]))
    assert all(x == 0 for x in differences[4])
    terminal_basis = [0]*dimension
    terminal_basis[3] = 1
    assert differences[3] == [125*x for x in terminal_basis]
    assert transfer(terminal_basis) == terminal_basis
    coeff = [sum(v[3::4]) for v in differences[:4]]
    assert coeff == [2499, 1780, 715, 125]
    polynomial = expand_newton(7, coeff)
    assert polynomial == [Fraction(-441), Fraction(1190, 3),
                          Fraction(-285, 2), Fraction(125, 6)]
    evaluate = lambda d: sum(c*d**i for i, c in enumerate(polynomial))
    assert rank4['status'] == rank3['status'] == 'PASS'
    assert rank4['ordered_markings'] == evaluate(4) == 199
    assert rank3['ordered_markings'] == 37 and evaluate(3) == 29
    assert evaluate(5) == sum(vectors[5][3::4]) == 584
    assert evaluate(6) == sum(vectors[6][3::4]) == 1309
    assert all(evaluate(row[0]) == row[4] for row in recount)
    assert len(gluings) == 2 and {g[1] for g in gluings} == {707, 708}

    report = {
        'status': 'PASS',
        'scope': 'New exact finite-graph annihilator supplement and independent arithmetic; no GAP regeneration or new group recognition.',
        'orientation': 'Integer column vectors indexed4*(state-1)+excess; T forwards each edge and adds its weight, discarding excess above3.',
        'dimension': dimension, 'states': count, 'edges': len(edges),
        'window_count': len(windows), 'exact_boundary_pairs': overlap_count,
        'all_budget_eligible_pairs_present': len(expected_pairs),
        'budget_rejections': budget_rejected,
        'minimum_cost_relaxation_rounds': rounds,
        'annihilator': '(T-I)^4 v_7 = 0',
        'stronger_sparse_identity': '(T-I)^3 v_7 = 125*e_(state1,excess3), and T fixes that basis vector',
        'differences_at_rank7': [summary(v) for v in differences],
        'newton_coefficients_excess3': coeff,
        'polynomial_coefficients_ascending': [str(c) for c in polynomial],
        'formula': '(125*d^3-855*d^2+2380*d-2646)/6',
        'all_rank_conclusion': 'd>=7 by binomial operator identity; d4,5,6 separately checked; rank3=37 is exceptional.',
        'recount_ranks5_through24': recount,
        'inputs': [{'path': n, 'sha256': digest(p/n)} for n in names],
        'checker': {'path': Path(__file__).name, 'sha256': digest(Path(__file__))},
        'retained_boundary': 'Complete frozen graph correctness retains phase20/phase21 theory and GAP/NQ. This supplement removes only the separate eventual-polynomiality dependency.',
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'dimension': dimension,
                      'annihilator': report['annihilator'], 'newton_coefficients': coeff,
                      'formula': report['formula']}))


if __name__ == '__main__':
    main()
