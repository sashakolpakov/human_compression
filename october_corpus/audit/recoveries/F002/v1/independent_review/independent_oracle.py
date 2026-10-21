"""Independent coordinate oracles; no author arithmetic/search imports."""
import argparse
import itertools
import json
from functools import lru_cache
from pathlib import Path

def mul(a, b):
    return tuple((b[x] for x in a))

def inv(a):
    return tuple((a.index(i) for i in range(len(a))))

def closure(gens, n):
    one = tuple(range(n))
    seen = {one}
    todo = [one]
    for a in todo:
        for b in gens:
            c = mul(a, b)
            if c not in seen:
                seen.add(c)
                todo.append(c)
    return frozenset(seen)

def cycles(n, pairs):
    p = list(range(n))
    for a, b in pairs:
        p[a - 1], p[b - 1] = (p[b - 1], p[a - 1])
    return tuple(p)
SOURCE_EDGES = [[[(2, 3), (4, 5), (6, 7), (8, 9)], [(1, 2), (3, 4), (7, 8), (9, 10)], [(2, 8), (3, 9), (6, 7), (10, 11)]], [[(1, 2), (3, 4), (6, 7), (8, 9)], [(2, 3), (4, 5), (7, 8), (9, 10)], [(1, 6), (2, 7), (3, 4), (10, 11)]], [[(1, 2), (3, 4), (8, 9), (10, 11)], [(2, 3), (4, 5), (7, 8), (9, 10)], [(1, 10), (2, 11), (3, 4), (5, 6)]], [[(1, 2), (6, 7), (8, 9), (10, 11)], [(2, 3), (4, 5), (7, 8), (9, 10)], [(1, 6), (2, 7), (3, 4), (10, 11)]], [[(1, 2), (5, 6), (8, 9), (10, 11)], [(2, 3), (4, 5), (7, 8), (10, 11)], [(3, 4), (5, 6), (8, 10), (9, 11)], [(4, 7), (5, 8), (6, 9), (10, 11)]]]

def source_oracle():
    marks = [tuple((cycles(11, x) for x in row)) for row in SOURCE_EDGES]

    @lru_cache(None)
    def sg(gens):
        return closure(gens, 11)

    def full_ip(t):
        groups = [sg(tuple((t[i] for i in range(len(t)) if s >> i & 1))) for s in range(1 << len(t))]
        return all((groups[i] & groups[j] == groups[i & j] for i in range(len(groups)) for j in range(len(groups))))

    def order(p):
        one = tuple(range(11))
        v = p
        k = 1
        while v != one:
            v = mul(v, p)
            k += 1
        return k

    def orbit_sizes(t):
        g = sg(t)
        unseen = set(range(11))
        sizes = []
        while unseen:
            x = min(unseen)
            orb = {a[x] for a in g}
            unseen -= orb
            sizes.append(len(orb))
        return sorted(sizes)

    def marked_isomorphism(t, u):
        one = tuple(range(11))
        mapping = {one: one}
        todo = [one]
        for a in todo:
            for x, y in zip(t, u):
                ax, by = (mul(a, x), mul(mapping[a], y))
                if ax in mapping:
                    if mapping[ax] != by:
                        return False
                else:
                    mapping[ax] = by
                    todo.append(ax)
        return len(set(mapping.values())) == len(mapping) == len(sg(u))
    rows = []
    for i, t in enumerate(marks, 1):
        if not len(sg(t)) == 660:
            raise AssertionError('len(sg(t)) == 660')
        if not orbit_sizes(t) == [11]:
            raise AssertionError('orbit_sizes(t) == [11]')
        if not full_ip(t):
            raise AssertionError('full_ip(t)')
        if not all((mul(t[i], t[j]) == mul(t[j], t[i]) for i in range(len(t)) for j in range(i + 2, len(t)))):
            raise AssertionError('all((mul(t[i], t[j]) == mul(t[j], t[i]) for i in range(len(t)) for j in range(i + 2, len(t))))')
        rows.append(dict(row=i, group_order=len(sg(t)), full_subset_ip=True, type=[order(mul(t[j], t[j + 1])) for j in range(len(t) - 1)], suffix_orbits=orbit_sizes(t[1:]), dual_suffix_orbits=orbit_sizes(tuple(reversed(t))[1:]), abstract_self_dual=marked_isomorphism(t, tuple(reversed(t)))))
    if not marked_isomorphism(marks[1], marks[2]):
        raise AssertionError('marked_isomorphism(marks[1], marks[2])')
    if not not full_ip((marks[0][0], marks[0][1], marks[0][0])):
        raise AssertionError('not full_ip((marks[0][0], marks[0][1], marks[0][0]))')
    wrong = list(marks[0])
    wrong[0] = cycles(11, [(2, 3), (4, 5)])
    if not mul(wrong[0], wrong[2]) != mul(wrong[2], wrong[0]):
        raise AssertionError('mul(wrong[0], wrong[2]) != mul(wrong[2], wrong[0])')
    return dict(rows=rows, rows_2_3_ordered_isomorphic=True, controls=['duplicate-generator IP rejection', 'deleted-edges rejection'])

def a5_oracle():
    n = 5
    one = tuple(range(n))
    symmetric = list(itertools.permutations(range(n)))
    even = [p for p in symmetric if sum((p[i] > p[j] for i in range(n) for j in range(i + 1, n))) % 2 == 0]
    ivs = [p for p in even if p != one and mul(p, p) == one]
    if not (len(even) == 60 and len(ivs) == 15):
        raise AssertionError('len(even) == 60 and len(ivs) == 15')
    pos = {g: i for i, g in enumerate(even)}
    table = [[pos[mul(a, b)] for b in even] for a in even]
    ids = [pos[x] for x in ivs]
    eid = pos[one]

    @lru_cache(None)
    def generated(gens):
        seen = {eid}
        todo = [eid]
        for a in todo:
            for b in gens:
                c = table[a][b]
                if c not in seen:
                    seen.add(c)
                    todo.append(c)
        return frozenset(seen)

    def sg(t):
        return generated(tuple(sorted(t)))

    def full_ip(t):
        sub = [sg(tuple((t[i] for i in range(len(t)) if s >> i & 1))) for s in range(1 << len(t))]
        return all((sub[i] & sub[j] == sub[i & j] for i in range(len(sub)) for j in range(len(sub))))
    conjugations = [[pos[mul(mul(inv(p), g), p)] for g in even] for p in symmetric]
    orbit_key = lambda t: min((tuple((c[x] for x in t)) for c in conjugations))
    marked = {r: set() for r in range(3, 6)}
    raw = {r: 0 for r in range(6)}

    def visit(t):
        raw[len(t)] += 1
        h = sg(t)
        if len(t) >= 3 and len({even[g][0] for g in h}) == n:
            marked[len(t)].add(orbit_key(t))
        if len(t) == 5:
            return
        for x in ids:
            if x in h or any((table[x][y] != table[y][x] for y in t[:-1])):
                continue
            u = t + (x,)
            if full_ip(u):
                visit(u)
    visit(())
    return dict(ambient_order=60, involutions=15, method='All raw ordered tuples; no orbit/pool/transitivity pruning; direct all-subset IP', raw_ip_prefixes=raw, transitive_orbit_counts={r: len(v) for r, v in marked.items()}, canonical_tuples={r: [[[x + 1 for x in even[j]] for j in t] for t in sorted(v)] for r, v in marked.items()})
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    report = {'status': 'PASS', 'source': source_oracle(), 'small_exhaustion': a5_oracle()}
    Path(args.out).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'source_rows': 5, 'a5_counts': report['small_exhaustion']['transitive_orbit_counts']}))
