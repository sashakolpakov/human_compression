#!/usr/bin/env python3
"""Exact checks of geometric shadow-IP; no external packages or source data.

Enumerating every witness flag and solving the eligible-vertex covering
problem are separate implementations. Finite tests do not replace the proof.
"""
from itertools import combinations, product
from hashlib import sha256
import json
from pathlib import Path
import random


def structure(sizes, bits):
    types = tuple(t for t, n in enumerate(sizes) for _ in range(n))
    rows = [1 << v for v in range(len(types))]
    for u, v in combinations(range(len(types)), 2):
        if types[u] != types[v]:
            if bits & 1:
                rows[u] |= 1 << v
                rows[v] |= 1 << u
            bits >>= 1
    assert bits == 0
    return types, tuple(rows)


def vertices(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def flags(types, rows, active):
    # Independent direct enumeration: one vertex or none from every type.
    classes = [[v for v in vertices(active) if types[v] == t]
               for t in sorted({types[v] for v in vertices(active)})]
    result = []
    for choices in product(*[[-1] + c for c in classes]):
        f = tuple(v for v in choices if v >= 0)
        if all(rows[u] >> v & 1 for u, v in combinations(f, 2)):
            result.append(f)
    return result


def shadow(rows, points, f):
    for v in f:
        points &= rows[v]
    return points


def direct(rows, points, u, all_flags):
    s = shadow(rows, points, u)
    if not s:
        return True
    return any(shadow(rows, points, f) == s and
               all(rows[v] >> w & 1 for v in f for w in u)
               for f in all_flags)


def cover(types, rows, active, i, u):
    points = sum(1 << v for v in vertices(active) if types[v] == i)
    s = shadow(rows, points, u)
    if s.bit_count() <= 1:
        return True
    eligible = [v for v in vertices(active) if types[v] != i
                and all(rows[v] >> w & 1 for w in u)
                and rows[v] & s == s]
    outside = points & ~s
    # Backtrack over binary assignments, checking conflict inequalities and
    # deleting covered outside points. This does not enumerate source flags.
    def solve(pos, chosen, left):
        if not left:
            return True
        possible = 0
        for v in eligible[pos:]:
            possible |= outside & ~rows[v]
        if left & ~possible:
            return False
        if pos == len(eligible):
            return False
        v = eligible[pos]
        if all(rows[v] >> w & 1 for w in chosen):
            if solve(pos + 1, chosen + (v,), left & rows[v]):
                return True
        return solve(pos + 1, chosen, left)
    return solve(0, (), outside)


def check_structure(types, rows, active=None):
    if active is None:
        active = (1 << len(types)) - 1
    fs = flags(types, rows, active)
    comparisons = 0
    ips = []
    for i in sorted({types[v] for v in vertices(active)}):
        points = sum(1 << v for v in vertices(active) if types[v] == i)
        good = True
        for x in vertices(active):
            for f in fs:
                u = (x,) + f
                a = direct(rows, points, u, fs)
                b = cover(types, rows, active, i, u)
                assert a == b, (types, rows, active, i, u, a, b)
                good &= a
                comparisons += 1
        ips.append(good)
    return comparisons, all(ips)


def main():
    totals = {'rank_two_structures': 0, 'rank_two_comparisons': 0,
              'rank_three_structures': 0, 'rank_three_comparisons': 0,
              'larger_structures': 0, 'larger_comparisons': 0,
              'residues_checked': 0, 'residue_comparisons': 0}
    for a in range(1, 4):
        for b in range(1, 4):
            for mask in range(1 << (a*b)):
                types, rows = structure((a, b), mask)
                n, ip = check_structure(types, rows)
                has_square = any((rows[u] & rows[v]).bit_count() >= 2
                                 for u, v in combinations(range(a), 2))
                complete = mask == (1 << (a*b)) - 1
                assert ip == (not has_square or complete)
                totals['rank_two_structures'] += 1
                totals['rank_two_comparisons'] += n
    for mask in range(1 << 12):
        types, rows = structure((2, 2, 2), mask)
        n, _ = check_structure(types, rows)
        totals['rank_three_structures'] += 1
        totals['rank_three_comparisons'] += n

    rng = random.Random(20042026)
    for sizes in ((3, 3, 3), (2, 2, 2, 2)):
        edges = sum(a*b for a, b in combinations(sizes, 2))
        for _ in range(24):
            types, rows = structure(sizes, rng.getrandbits(edges))
            n, _ = check_structure(types, rows)
            totals['larger_structures'] += 1
            totals['larger_comparisons'] += n
            active = (1 << len(types)) - 1
            for f in flags(types, rows, active):
                if not f:
                    continue
                occupied = {types[v] for v in f}
                residue = sum(1 << v for v in vertices(active)
                              if types[v] not in occupied and
                              all(rows[v] >> w & 1 for w in f))
                if len({types[v] for v in vertices(residue)}) >= 2:
                    n, _ = check_structure(types, rows, residue)
                    totals['residues_checked'] += 1
                    totals['residue_comparisons'] += n

    types = (0, 0, 0, 0, 1, 1, 2, 2)
    rows = [1 << v for v in range(8)]
    edges = [(u,v) for u in (4,5) for v in (6,7)]
    edges += [(u,v) for v, ns in ((4,(0,1,2)), (5,(0,1,3)),
                                   (6,(0,1,2)), (7,(0,1,3))) for u in ns]
    for u,v in edges:
        rows[u] |= 1 << v
        rows[v] |= 1 << u
    fs = flags(types, rows, 255)
    assert all(any(set(f) <= set(c) and len(c) == 3 for c in fs) for f in fs)
    assert shadow(rows, 15, (4,5)) == 3
    assert shadow(rows, 15, (6,7)) == 3
    assert not direct(rows, 15, (4,5), fs)
    assert not cover(types, rows, 255, 0, (4,5))
    check_structure(types, rows)
    report = {'status': 'PASS', 'scope':
              'Exact finite comparisons of independent witness and covering procedures; '
              'rank-two characterization; residues; closure obstruction. '
              'Not a sporadic classification or a substitute for the written universal proof.',
              'counts': totals, 'closure_counterexample': {
                  'types': types, 'incidence_bit_rows': rows,
                  'every_flag_extends_to_chamber': True,
                  'tested_x': 4, 'tested_flag': [5], 'shadow': [0,1],
                  'eligible_vertices': [6,7], 'closure_passes': True,
                  'flag_witness_exists': False},
              'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest()}
    Path(__file__).with_suffix('.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', **totals}, indent=2))


if __name__ == '__main__':
    main()
