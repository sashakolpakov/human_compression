#!/usr/bin/env python3
"""Literal finite cross-ratio incidence model; no saved tables or assertions."""
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def mul(x, y):
    z = 0
    while y:
        if y & 1:
            z ^= x
        y >>= 1
        x <<= 1
        if x & 4:
            x ^= 7
    return z


def inv(x):
    require(x != 0, 'division by zero')
    return mul(x, x)


def dot(x, y):
    z = 0
    for a, b in zip(x, y):
        z ^= mul(a, b)
    return z


def norm(v):
    c = next(x for x in v if x)
    return tuple(mul(inv(c), x) for x in v)


def cross(q, points):
    p = [points[i] for i in q]
    r, s = next((r, s) for r, s in combinations(range(3), 2)
                if mul(p[0][r], p[1][s]) ^ mul(p[0][s], p[1][r]))
    def det(i, j):
        return mul(p[i][r], p[j][s]) ^ mul(p[i][s], p[j][r])
    return mul(mul(det(0, 2), det(1, 3)), inv(mul(det(0, 3), det(1, 2))))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    require(not args.output.exists(), 'fresh output required')
    # Check the implemented field axioms exhaustively, independently of the
    # projective computations that follow.
    require(all(mul(x, 1) == x and (x == 0 or mul(x, inv(x)) == 1)
                for x in range(4)), 'field units')
    require(all(mul(x, y) == mul(y, x) for x, y in product(range(4), repeat=2)),
            'field commutativity')
    require(all(mul(mul(x, y), z) == mul(x, mul(y, z)) and
                mul(x, y ^ z) == (mul(x, y) ^ mul(x, z))
                for x, y, z in product(range(4), repeat=3)), 'field laws')
    points = sorted({norm(v) for v in product(range(4), repeat=3) if any(v)})
    lines = [tuple(i for i, p in enumerate(points) if dot(f, p) == 0) for f in points]
    require(len(points) == len(lines) == 21 and all(len(l) == 5 for l in lines),
            'literal projective plane counts')
    require(all(sum(set(pair) <= set(l) for l in lines) == 1
                for pair in combinations(range(21), 2)), 'unique joining line')
    records = []
    fibers = defaultdict(list)
    for line, members in enumerate(lines):
        for q in permutations(members, 4):
            lam = cross(q, points)
            require(lam in (2, 3), 'nonprime cross-ratio')
            key = (lam, line, tuple(sorted(q)))
            fibers[key].append(q)
            records.append((lam, line, q))
            require(cross((q[1], q[0], q[3], q[2]), points) == lam,
                    'double interchange preserves cross-ratio')
            require(cross((q[0], q[1], q[3], q[2]), points) == inv(lam),
                    'last interchange inverts cross-ratio')
    require(Counter(r[0] for r in records) == {2: 1260, 3: 1260}, 'new type counts')
    require(len(fibers) == 210 and {len(v) for v in fibers.values()} == {12},
            'complete shadow-fiber multiplicities')
    point_frob = [points.index(norm(tuple(mul(x, x) for x in p))) for p in points]
    line_frob = [lines.index(tuple(sorted(point_frob[i] for i in l))) for l in lines]
    require(sorted(point_frob) == list(range(21)) and
            any(i != j for i, j in enumerate(point_frob)), 'nontrivial Frobenius')
    lookup = set(records)
    for lam, line, q in records:
        fq = tuple(point_frob[i] for i in q)
        target = (fq[0], fq[1], fq[3], fq[2])
        require((lam, line_frob[line], target) in lookup,
                'type-preserving Frobenius lift')
        require(tuple(point_frob[i] for i in (target[0], target[1], target[3], target[2])) == q,
                'Frobenius lift squares to identity')
    key = min(fibers)
    q, q2 = fibers[key][:2]
    lam, line, support = key
    def shadow(qq):
        return {('point', i) for i in qq} | {('line', line)}
    require(q != q2 and shadow(q) == shadow(q2), 'literal distinct twin witness')
    objects = ([('point', i) for i in range(21)] +
               [('line', i) for i in range(21)] +
               [('quad', ll, ell, qq) for ll, ell, qq in records])
    u = objects.index(('quad', lam, line, q))
    v = objects.index(('quad', lam, line, q2))
    def incident(x, y):
        if x[0] == 'quad' and y[0] == 'quad':
            return x[1] != y[1]
        if y[0] == 'quad':
            x, y = y, x
        if x[0] == 'quad':
            return y[1] in x[3] if y[0] == 'point' else y[1] == x[2]
        if x[0] == y[0]:
            return False
        if x[0] == 'line':
            x, y = y, x
        return x[1] in lines[y[1]]
    def swap(i):
        return v if i == u else u if i == v else i
    def preserves(inc):
        # Pairs outside these two rows are fixed pointwise by the permutation.
        return all(inc(objects[i], objects[j]) == inc(objects[swap(i)], objects[swap(j)])
                   for i in (u, v) for j in range(len(objects)))
    require(preserves(incident), 'literal twin transposition preserves all incidences')
    def altered_incident(x, y):
        if {x, y} == {objects[v], ('point', support[0])}:
            return False
        return incident(x, y)
    require(not preserves(altered_incident), 'altered old incidence must break automorphism')
    result = {'status': 'PASS_ROOT_FINITE_CORROBORATION_UNREVIEWED',
              'points': points, 'lines': lines, 'old_type_counts': [21, 21],
              'new_type_counts': [1260, 1260], 'total_objects': 2562,
              'shadow_fibers': len(fibers), 'each_fiber_size': 12,
              'pointwise_kernel': 'Sym(12)^210',
              'witness': {'type': lam, 'line_index': line, 'support': support,
                          'first_tuple': q, 'second_tuple': q2},
              'double_interchange_checked_on': len(records),
              'frobenius_lift_checked_on': len(records),
              'negative_control': 'one removed old incidence breaks the literal transposition automorphism',
              'whole_source_credit': 0, 'open_conjecture_credit': 0,
              'Lean_certificate': False,
              'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest()}
    with args.output.open('x') as f:
        json.dump(result, f, indent=2)
        f.write('\n')
    print('PHASE196_FINITE_PASS', len(records), len(fibers))


if __name__ == '__main__':
    main()
