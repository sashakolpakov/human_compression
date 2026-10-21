#!/usr/bin/env python3
"""Exact construction and rank checks; no distance or group claim is inferred.

The cyclic binary polynomial below is only a construction seed. All 4096 binary
words, their weights and every Steiner four-subset are checked explicitly.
The finite geometry model over F4 is constructed directly from field arithmetic.
"""
import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path


def need(test, message):
    if not test:
        raise RuntimeError(message)


def rank_mod(a, p):
    rows = [[x % p for x in row] for row in a]
    rank = 0
    for j in range(len(rows[0])):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][j]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        b = rows[rank]
        inv = pow(b[j], -1, p)
        b[j:] = [(x * inv) % p for x in b[j:]]
        for i in range(rank + 1, len(rows)):
            c = rows[i][j]
            if c:
                rows[i][j:] = [(x - c * y) % p for x, y in zip(rows[i][j:], b[j:])]
        rank += 1
        if rank == len(rows):
            break
    return rank


def srg_check(a, expected):
    n, k, lam, mu = expected
    need(len(a) == n and all(len(r) == n for r in a), 'matrix size')
    neighbors = [{j for j, x in enumerate(row) if x} for row in a]
    for i in range(n):
        need(a[i][i] == 0 and len(neighbors[i]) == k, 'loop or degree')
        for j in range(i):
            need(a[i][j] == a[j][i], 'symmetry')
            need(len(neighbors[i] & neighbors[j]) == (lam if a[i][j] else mu),
                 'common-neighbour parameter')
    return neighbors


def mul4(a, b):
    c = 0
    while b:
        if b & 1:
            c ^= a
        b >>= 1
        a <<= 1
        if a & 4:
            a ^= 7
    return c


def dot4(a, b):
    c = 0
    for x, y in zip(a, b):
        c ^= mul4(x, y)
    return c


def graph105():
    pts = [v for v in itertools.product(range(4), repeat=3)
           if any(v) and next(x for x in v if x) == 1]
    need(len(pts) == 21, 'projective points')
    flags = [(p, line) for p in pts for line in pts if dot4(p, line) == 0]
    need(len(flags) == 105, 'flags')
    a = [[int(i != j and (p == q or l == m or
               (dot4(p, m) != 0 and dot4(q, l) != 0)))
          for j, (q, m) in enumerate(flags)] for i, (p, l) in enumerate(flags)]
    return a


def steiner_blocks():
    g = sum(1 << i for i in [0, 1, 5, 6, 7, 9, 11])
    words = []
    for m in range(1 << 12):
        w = 0
        for i in range(12):
            if (m >> i) & 1:
                w ^= g << i
        words.append(w)
    need(len(set(words)) == 4096 and max(words) < (1 << 23), 'binary construction')
    weights = Counter(w.bit_count() for w in words)
    need(weights == {0: 1, 7: 253, 8: 506, 11: 1288, 12: 1288,
                     15: 506, 16: 253, 23: 1}, 'binary weights')
    blocks = [w for w in words if w.bit_count() == 7]
    fours = Counter()
    for b in blocks:
        for q in itertools.combinations([i for i in range(23) if (b >> i) & 1], 4):
            fours[q] += 1
    need(len(fours) == 8855 and set(fours.values()) == {1}, 'Steiner condition')
    return blocks, weights


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    need(not args.out.exists(), 'Use a fresh output directory')
    args.out.mkdir(parents=True)
    blocks, weights = steiner_blocks()
    graphs = {105: graph105()}
    for j, n in [(0, 253), (1, 176), (2, 120)]:
        selected = [b for b in blocks if b & ((1 << j) - 1) == 0]
        need(len(selected) == n, 'deleted blocks')
        graphs[n] = [[int(x != y and (x & y).bit_count() != 1) for y in selected]
                     for x in selected]
    parameters = {105: (105, 72, 51, 45), 120: (120, 77, 52, 44),
                  176: (176, 105, 68, 54), 253: (253, 140, 87, 65)}
    report = {'status': 'EXACT_FINITE_GRAPH_AND_RANK_CHECKS',
              'binary_seed_exponents': [0, 1, 5, 6, 7, 9, 11],
              'binary_weights': dict(weights), 'steiner_four_subsets': 8855,
              'graphs': {},
              'limits': ['No minimum-distance or weight-enumerator claim for ternary codes.',
                         'No full automorphism group or irreducible-module claim.',
                         'Finite computations do not prove rank formulas for other graphs sharing parameters.']}
    for n in sorted(graphs):
        a = graphs[n]
        neighbors = srg_check(a, parameters[n])
        b = [[int(i != j) - a[i][j] for j in range(n)] for i in range(n)]
        ranks = {str(p): rank_mod(a, p) for p in [2, 3, 5, 7, 11, 23]}
        rank3 = ranks['3']
        a_squared = [[len(neighbors[i] & neighbors[j]) % 3 for j in range(n)]
                     for i in range(n)]
        square_rank = rank_mod(a_squared, 3)
        complement_rank = rank_mod(b, 3)
        ab_zero = all((sum(a[i]) - a[i][j] - len(neighbors[i] & neighbors[j])) % 3 == 0
                      for i in range(n) for j in range(n))
        row_aug_rank = rank_mod(a + [[1] * n], 3)
        matrix_bytes = bytes(x for row in a for x in row)
        (args.out / f'adjacency_{n}.bin').write_bytes(matrix_bytes)
        need(rank3 == {105: 20, 120: 21, 176: 21, 253: 23}[n], 'ternary rank')
        need(rank3 - square_rank == (20 if n == 105 else 0), 'hull dimension')
        report['graphs'][str(n)] = {
            'parameters': parameters[n], 'matrix_sha256': hashlib.sha256(matrix_bytes).hexdigest(),
            'ranks': ranks, 'ternary_square_rank': square_rank,
            'ternary_hull_dimension': rank3 - square_rank,
            'ternary_complement_rank': complement_rank,
            'ternary_complement_orthogonal': ab_zero,
            'all_ones_in_code': row_aug_rank == rank3}
    (args.out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
