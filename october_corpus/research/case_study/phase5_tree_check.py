#!/usr/bin/env python3
"""Exact independent small checks for the tree-cut derivation.

NetworkX supplies nonisomorphic trees only. Group closure, incidence flags,
permutation orbits and shadow witnesses are checked here from finite sets.
These are finite audits, not a replacement for the written all-rank proof.
"""
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path
import networkx as nx


def components(n, edges):
    labels = list(range(n))
    for a, b in edges:
        x, y = labels[a], labels[b]
        labels = [x if z == y else z for z in labels]
    return tuple(frozenset(i for i in range(n) if labels[i] == z)
                 for z in sorted(set(labels)))


def generated(n, edges):
    identity = tuple(range(n))
    seen, todo = {identity}, [identity]
    while todo:
        p = todo.pop()
        for a, b in edges:
            q = list(p)
            q[a], q[b] = q[b], q[a]
            q = tuple(q)
            if q not in seen:
                seen.add(q)
                todo.append(q)
    return seen


def all_flags(classes, rows):
    result = []
    def visit(i, current):
        if i == len(classes):
            result.append(current)
            return
        visit(i + 1, current)
        for v in classes[i]:
            if all(rows[v] >> w & 1 for w in current):
                visit(i + 1, current + (v,))
    visit(0, ())
    return result


def subset_geometry(n, cuts):
    vertices = [(i, frozenset(c)) for i, a in enumerate(cuts)
                for c in combinations(range(n), len(a))]
    classes = [[v for v, (i, _) in enumerate(vertices) if i == j]
               for j in range(len(cuts))]
    rows = [1 << v for v in range(len(vertices))]
    for v, w in combinations(range(len(vertices)), 2):
        i, a = vertices[v]
        j, b = vertices[w]
        if i != j and len(a & b) == len(cuts[i] & cuts[j]):
            rows[v] |= 1 << w
            rows[w] |= 1 << v
    return vertices, classes, rows


def shadow(rows, points, flag):
    for v in flag:
        points &= rows[v]
    return points


def main():
    counts = dict(trees=0, partition_meets=0, generated_subgroups=0,
                  group_meets=0, flag_orbit_comparisons=0,
                  boolean_shadow_queries=0)
    by_order = {}
    for n in range(2, 8):
        trees = list(nx.nonisomorphic_trees(n))
        by_order[n] = len(trees)
        for t in trees:
            edges = list(t.edges())
            forests = [[e for i, e in enumerate(edges) if mask >> i & 1]
                       for mask in range(1 << len(edges))]
            parts = [components(n, f) for f in forests]
            for i, p in enumerate(parts):
                for j, q in enumerate(parts):
                    meet = {a & b for a in p for b in q if a & b}
                    assert meet == set(parts[i & j])
                    counts['partition_meets'] += 1
            if n <= 6:
                perms = list(permutations(range(n)))
                groups = [generated(n, f) for f in forests]
                for g, p in zip(groups, parts):
                    expected = {s for s in perms if all(
                        frozenset(s[x] for x in a) == a for a in p)}
                    assert g == expected
                    counts['generated_subgroups'] += 1
                for i, g in enumerate(groups):
                    for j, h in enumerate(groups):
                        assert g & h == groups[i & j]
                        counts['group_meets'] += 1
                full = (1 << len(edges)) - 1
                cuts = [next(a for a in parts[full ^ (1 << i)] if 0 not in a)
                        for i in range(len(edges))]
                vs, classes, rows = subset_geometry(n, cuts)
                flags = set(all_flags(classes, rows))
                lookup = {v: i for i, v in enumerate(vs)}
                orbit_flags = set()
                for s in perms:
                    chamber = tuple(lookup[(i, frozenset(s[x] for x in a))]
                                    for i, a in enumerate(cuts))
                    for mask in range(1 << len(edges)):
                        orbit_flags.add(tuple(v for i, v in enumerate(chamber)
                                              if mask >> i & 1))
                assert flags == orbit_flags
                counts['flag_orbit_comparisons'] += len(flags)
            counts['trees'] += 1

    # Independently enumerate every x+flag query in Boolean geometries,
    # then validate the proposed at-most-two-vertex witness against rows.
    for n in range(2, 7):
        omega = frozenset(range(n))
        cuts = [frozenset(range(k)) for k in range(1, n)]
        vs, classes, rows = subset_geometry(n, cuts)
        fs = all_flags(classes, rows)
        lookup = {a: v for v, (_, a) in enumerate(vs)}
        for k, vertices in enumerate(classes, start=1):
            points = sum(1 << v for v in vertices)
            for x in range(len(vs)):
                for f in fs:
                    u = (x,) + f
                    s = shadow(rows, points, u)
                    counts['boolean_shadow_queries'] += 1
                    if not s:
                        continue
                    if s.bit_count() == 1:
                        witness = (s.bit_length() - 1,)
                    else:
                        low = frozenset().union(*(vs[v][1] for v in u
                                                 if len(vs[v][1]) < k))
                        high = omega
                        for v in u:
                            if len(vs[v][1]) > k:
                                high &= vs[v][1]
                        witness = tuple(lookup[a] for a in (low, high)
                                        if a and a != omega)
                    assert len(witness) <= 2
                    assert all(rows[v] >> w & 1 for v, w in combinations(witness, 2))
                    assert all(rows[v] >> w & 1 for v in witness for w in u)
                    assert shadow(rows, points, witness) == s

    cuts = [frozenset({i}) for i in range(3)]
    vs, classes, rows = subset_geometry(4, cuts)
    fs = all_flags(classes, rows)
    lookup = {v: i for i, v in enumerate(vs)}
    x, y = lookup[(1, frozenset({0}))], lookup[(1, frozenset({1}))]
    points = sum(1 << v for v in classes[0])
    s = shadow(rows, points, (x, y))
    assert s.bit_count() == 2
    assert not any(shadow(rows, points, f) == s and
                   all(rows[v] >> w & 1 for v in f for w in (x, y)) for f in fs)
    report = dict(status='PASS', counts=counts, tree_counts_by_order=by_order,
                  claw_shadow_failure=True,
                  scope='Finite forest/group/flag checks and explicit Boolean shadow witnesses; no universal or whole-paper claim from computation alone.',
                  dependencies={'networkx': nx.__version__, 'usage': 'nonisomorphic tree generation'},
                  script_sha256=sha256(Path(__file__).read_bytes()).hexdigest())
    Path(__file__).with_suffix('.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
