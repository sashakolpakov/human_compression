#!/usr/bin/env python3
"""Exact bounded diagnostics for endpoint halving; Python standard library only."""
import argparse
from functools import lru_cache
from hashlib import sha256
from itertools import permutations, product
import json
from pathlib import Path


def mul(p, q):
    """Compose p after q; permutations are image tuples with zero-based points."""
    return tuple(p[q[i]] for i in range(len(p)))


def cycles(n, *cs):
    p = list(range(n))
    for c in cs:
        for i, v in enumerate(c):
            p[v] = c[(i+1) % len(c)]
    return tuple(p)


@lru_cache(maxsize=8192)
def group(n, gs):
    identity = tuple(range(n))
    seen = {identity}
    todo = [identity]
    for x in todo:
        for g in gs:
            y = mul(x, g)
            if y not in seen:
                seen.add(y)
                todo.append(y)
    return frozenset(seen)


def generated(n, gs):
    return group(n, tuple(sorted(set(gs))))


def lattice(gs):
    return [generated(len(gs[0]), [g for i, g in enumerate(gs) if m >> i & 1])
            for m in range(1 << len(gs))]


def failures(lats):
    # Every ordered pair is checked, not just the maximal parabolics.
    return [(i, j, len(lats[i] & lats[j]), len(lats[i & j]))
            for i in range(len(lats)) for j in range(len(lats))
            if lats[i] & lats[j] != lats[i & j]]


def inspect(gs, name, expected=None):
    n = len(gs[0])
    identity = tuple(range(n))
    assert all(g != identity and mul(g, g) == identity for g in gs)
    a, b, *rs = gs
    assert all(mul(a, r) == mul(r, a) for r in rs)
    old = lattice(gs)
    old_bad = failures(old)
    if old_bad:
        return None
    ap = mul(mul(a, b), a)
    newgs = (ap, b, *rs)
    new = lattice(newgs)
    new_bad = failures(new)
    p = generated(n, (b, *rs))
    pa = frozenset(mul(mul(a, x), a) for x in p)
    r = generated(n, rs)
    overlap = p & pa == r
    f = [j for j in range(1 << len(rs)) if a in new[3 | (j << 2)]]
    fset = set(f)
    fbad = [(i, j) for i in f for j in f if i & j not in fset]
    assert bool(not new_bad) == bool(overlap and not fbad), name
    h = new[-1]
    assert len(old[-1]) // len(h) in (1, 2)
    assert (h == old[-1]) == bool(f), name
    for j in range(1 << len(rs)):
        u_j, h_j = old[3 | (j << 2)], new[3 | (j << 2)]
        assert h_j <= u_j and len(u_j) // len(h_j) in (1, 2)
        assert frozenset(mul(mul(a, x), a) for x in h_j) == h_j
        assert (u_j == h_j) == (j in fset)
    support = None
    if f and not fbad:
        support = (1 << len(rs))-1
        for j in f:
            support &= j
        assert fset == {j for j in range(1 << len(rs)) if j & support == support}
    out = {
        'name': name, 'degree': n, 'rank': len(gs),
        'generators': gs, 'new_first_generator': ap,
        'old_order': len(old[-1]), 'new_order': len(h),
        'old_IP_meets': len(old)**2, 'new_IP_meets': len(new)**2,
        'new_IP_failure_count': len(new_bad),
        'P_order': len(p), 'P_overlap_order': len(p & pa), 'R_order': len(r),
        'overlap_condition': overlap,
        'recovering_subsets_bitmasks': f,
        'filter_failure_pairs': fbad,
        'least_support_bitmask': support,
        'new_IP': not new_bad,
        'criterion_agrees': True,
    }
    if expected:
        for k, v in expected.items():
            assert out[k] == v, (name, k, out[k], v)
    return out


def signed_marking(rank):
    a = cycles(2*rank, (0, rank))
    rs = [cycles(2*rank, (i, i+1), (rank+i, rank+i+1))
          for i in range(rank-1)]
    return (a, *rs)


def hemicube_marking(rank):
    # Signed permutations act on sign vectors modulo simultaneous negation.
    reps = [(0, *v) for v in product((0, 1), repeat=rank-1)]
    index = {v: i for i, v in enumerate(reps)}
    gs = []
    for marker in range(rank):
        p = []
        for v in reps:
            y = list(v)
            if marker == 0:
                y[0] ^= 1
            else:
                y[marker-1], y[marker] = y[marker], y[marker-1]
            if y[0]:
                y = [x ^ 1 for x in y]
            p.append(index[tuple(y)])
        gs.append(tuple(p))
    return tuple(gs)


def product_perm(p, q):
    return p + tuple(len(p)+x for x in q)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('--output must be a new file; historical reports are immutable')
    cases = []
    a = cycles(4, (0, 1), (2, 3))
    b = cycles(4, (1, 2))
    c = cycles(4, (2, 3))
    cases.append(inspect((a, b, c), 'S4 even full-group endpoint', {
        'old_order': 24, 'new_order': 24, 'recovering_subsets_bitmasks': [1],
        'least_support_bitmask': 1, 'new_IP': True,
    }))
    cases.append(inspect((cycles(6, (0, 1)),
                          cycles(6, (0, 2), (1, 3), (4, 5)),
                          cycles(6, (3, 4)), cycles(6, (3, 5))),
                         'S6 isolated filter obstruction', {
        'old_order': 720, 'new_order': 720, 'overlap_condition': True,
        'P_order': 48, 'P_overlap_order': 6, 'R_order': 6,
        'recovering_subsets_bitmasks': [1, 2, 3], 'new_IP': False,
    }))
    # Both tests fail here; this does not establish their logical independence.
    z = mul(mul(a, b), mul(a, b))
    cz = mul(mul(z, c), z)
    cases.append(inspect((product_perm(a, a), product_perm(b, b),
                          product_perm(c, c), product_perm(c, cz)),
                         'S4 twisted diagonal negative control', {
        'old_order': 96, 'new_order': 96, 'overlap_condition': False,
        'recovering_subsets_bitmasks': [1, 2, 3], 'new_IP': False,
    }))
    for rank in (3, 4, 5):
        cases.append(inspect(signed_marking(rank), f'B{rank} signed marking', {
            'recovering_subsets_bitmasks': [], 'new_IP': True,
        }))
        cases.append(inspect(hemicube_marking(rank), f'Hemicube rank {rank}', {
            'recovering_subsets_bitmasks': [2**(rank-2)-1] if rank % 2 else [],
            'new_IP': True,
        }))
    assert all(cases), 'A named original marking failed IP'
    # Exhaustive labelled rank-three search within the 24 permutations of S4.
    all_s4 = tuple(permutations(range(4)))
    identity = tuple(range(4))
    invs = [p for p in all_s4 if p != identity and mul(p, p) == identity]
    census = {'ambient': 'S4 in its natural degree-four action',
              'involutions': len(invs), 'distinct_commuting_endpoint_triples': 0,
              'original_C_group_markings': 0, 'old_IP_meets': 0,
              'new_IP_meets': 0, 'criterion_mismatches': 0,
              'new_C_group_markings': 0, 'proper_index_two': 0,
              'nonempty_least_support': 0, 'both_tests_fail': 0,
              'overlap_only_fails': 0, 'filter_only_fails': 0}
    for gs in permutations(invs, 3):
        if mul(gs[0], gs[2]) != mul(gs[2], gs[0]):
            continue
        census['distinct_commuting_endpoint_triples'] += 1
        census['old_IP_meets'] += 64
        row = inspect(gs, 'exhaustive S4 triple')
        if row is None:
            continue
        census['original_C_group_markings'] += 1
        census['new_IP_meets'] += 64
        census['new_C_group_markings'] += row['new_IP']
        census['proper_index_two'] += row['new_order'] < row['old_order']
        census['nonempty_least_support'] += row['least_support_bitmask'] not in (None, 0)
        ofail, ffail = not row['overlap_condition'], bool(row['filter_failure_pairs'])
        census['both_tests_fail'] += ofail and ffail
        census['overlap_only_fails'] += ofail and not ffail
        census['filter_only_fails'] += ffail and not ofail
    report = {
        'status': 'PASS', 'scope': 'Finite diagnostics and exhaustive S4 rank-three marking test; not a proof for arbitrary groups.',
        'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'convention': 'Zero-based permutation image tuples; mul(p,q)=p after q. Rest-subset bit 0 is the third original generator.',
        'named_examples': cases, 'exhaustive_search': census,
        'named_example_meets': sum(r['old_IP_meets']+r['new_IP_meets'] for r in cases),
        'total_IP_meets': sum(r['old_IP_meets']+r['new_IP_meets'] for r in cases)+census['old_IP_meets']+census['new_IP_meets'],
        'catalogues_used': [], 'formal_scope': 'Separate Lean module proves only mixed-subgroup intersections.',
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print('HALVING_CRITERION_PASS', len(cases), 'named examples;', census,
          'total meets', report['total_IP_meets'])


if __name__ == '__main__':
    main()
