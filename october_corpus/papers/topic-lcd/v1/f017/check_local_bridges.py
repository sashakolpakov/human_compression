#!/usr/bin/env python3
"""Optional finite checks of written F017 bridges; not uniform proof premises."""
import argparse
from collections import Counter
from itertools import combinations
import json
from math import comb
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def basis(rows):
    pivots = {}
    for row in rows:
        while row:
            pivot = row.bit_length() - 1
            if pivot in pivots:
                row ^= pivots[pivot]
            else:
                pivots[pivot] = row
                break
    return pivots


def contains(pivots, row):
    while row:
        pivot = row.bit_length() - 1
        if pivot not in pivots:
            return False
        row ^= pivots[pivot]
    return True


def product_row(row, matrix):
    output = 0
    while row:
        low = row & -row
        output ^= matrix[low.bit_length() - 1]
        row ^= low
    return output


def run():
    point_cases = []
    for n in range(3, 9):
        for k in range(1, n):
            sets = list(combinations(range(n), k))
            incidence = [sum(1 << j for j, t in enumerate(sets) if a in t)
                         for a in range(n)]
            words = set()
            for coefficients in range(1 << n):
                words.add(product_row(coefficients, incidence))
            observed = Counter(w.bit_count() for w in words)
            predicted = Counter()
            for r in range(n + 1):
                weight = sum(choose(r, i) * choose(n-r, k-i)
                             for i in range(1, k+1, 2))
                predicted[weight] += comb(n, r)
            fiber = 2 if k % 2 == 0 else 1
            require(all(c % fiber == 0 for c in predicted.values()), 'fiber')
            predicted = Counter({w: c // fiber for w, c in predicted.items()})
            require(observed == predicted, f'point enumerator {n,k}')
            require(len(basis(incidence)) == n - (k % 2 == 0), 'point rank')
            point_cases.append({'n': n, 'k': k, 'words': len(words)})
            if (n, k) == (8, 2):
                require(observed[16] == 35, 'literal Result4 correction')

    odd_cases = []
    for k in range(1, 5):
        n = 2*k + 1
        sets = list(map(frozenset, combinations(range(n), k)))
        stars = [sum(1 << j for j, t in enumerate(sets) if r <= t)
                 for r in map(frozenset, combinations(range(n), k-1))]
        A = [sum(1 << j for j, y in enumerate(sets) if not (x & y))
             for x in sets]
        E = []
        for x in sets:
            e = 0
            for r, star in zip(combinations(range(n), k-1), stars):
                if frozenset(r) <= x:
                    e ^= star
            E.append(e)
        A2 = [product_row(row, A) for row in A]
        require(A2 == [(1 << i) ^ E[i] for i in range(len(sets))], 'A2')
        require(all(product_row(w, A) == 0 for w in stars), 'Au')
        require([product_row(row, A) for row in A2] == A, 'A3')
        BA, BW = basis(A), basis(stars)
        require(len(BA) == comb(2*k, k), 'odd rank')
        require(len(BA) + len(BW) == len(sets), 'dual dimensions')
        require(all((a & w).bit_count() % 2 == 0 for a in A for w in stars),
                'dual orthogonality')
        one = (1 << len(sets)) - 1
        require(contains(BA, one) == (k % 2 == 0), 'constant in C')
        require(contains(BW, one) == (k % 2 == 1), 'constant in dual')
        if k == 2:
            require(A2[0] != 1, 'literal source odd formula must fail')
        odd_cases.append({'k': k, 'length': len(sets), 'rank': len(BA)})

    subset_rows = json.loads((Path(__file__).parent / 'finite_subset_rows.json').read_text())
    if isinstance(subset_rows, dict):
        subset_rows = subset_rows['rows']
    for row in subset_rows:
        n, k, r, p = (row[x] for x in ('n', 'k', 'r', 'p'))
        degree = choose(k, r)*choose(n-k, k-r)
        P = [(sum(choose(j, a)*choose(k-j, r-a)**2*
                  choose(n-2*k+j, k-2*r+a) for a in range(j+1))
              + (j == r)) % p for j in range(k+1)]
        require(P == row['P_mod_p'], 'page8 count vector')
        require(degree == row['degree'], 'page8 degree')
        require(choose(n, k) == row['N'], 'page8 length')

    ternary = []
    for n in (7, 10, 13):
        sets = list(map(frozenset, combinations(range(n), 3)))
        x = sets[0]
        coefficients = [(1 - (len(x & y) == 0) + (len(x & y) == 1)
                         + len(x & y)) % 3 for y in sets]
        require(coefficients == [int(x == y) for y in sets], 'ternary identity')
        for a in range(n):
            require(all(sum(a in y and not (y & t) for y in sets) % 3 == 0
                        for t in sets), 'ternary point orthogonality')
        ternary.append(n)
    return {'status': 'PASS', 'role': 'optional finite validation of uniform written proofs',
            'point_incidence_cases': point_cases, 'odd_graph_cases': odd_cases,
            'page8_count_rows': len(subset_rows), 'ternary_n': ternary,
            'required_uniform_proof_premise': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    report = run()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'point_cases': len(report['point_incidence_cases']),
                      'odd_cases': len(report['odd_graph_cases']), 'page8_rows': report['page8_count_rows']}))
