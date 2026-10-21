#!/usr/bin/env python3
"""Independent finite audits for weighted-tree truncation formulas.

Standard library plus NetworkX tree generation. Checks do not import the
proof, source tables, or prior checker output. Finite checks are not an
all-parameter certificate. Output is written next to this script.
"""
from collections import deque
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, permutations, product
from math import comb, factorial
from pathlib import Path
import json
import networkx as nx


def comps(n, edges):
    labels = list(range(n))
    for a, b in edges:
        x, y = labels[a], labels[b]
        labels = [x if z == y else z for z in labels]
    return [frozenset(i for i in range(n) if labels[i] == x)
            for x in sorted(set(labels))]


def compositions(n, k):
    if k == 1:
        yield (n,)
    else:
        for a in range(1, n-k+2):
            for rest in compositions(n-a, k-1):
                yield (a,) + rest


def masks(n, k):
    return [sum(1 << x for x in s) for s in combinations(range(n), k)]


def image(s, p):
    return sum(1 << p[x] for x in range(len(p)) if s >> x & 1)


def geometry(n, cuts):
    vs = [(i, s) for i, a in enumerate(cuts) for s in masks(n, a.bit_count())]
    classes = [[v for v, (j, _) in enumerate(vs) if j == i] for i in range(len(cuts))]
    rows = [1 << v for v in range(len(vs))]
    for v, w in combinations(range(len(vs)), 2):
        i, a = vs[v]
        j, b = vs[w]
        if i != j and (a & b).bit_count() == (cuts[i] & cuts[j]).bit_count():
            rows[v] |= 1 << w
            rows[w] |= 1 << v
    flags = []
    def visit(i, f):
        if i == len(classes):
            flags.append(f)
            return
        visit(i+1, f)
        for v in classes[i]:
            if all(rows[v] >> w & 1 for w in f):
                visit(i+1, f+(v,))
    visit(0, ())
    return vs, classes, rows, flags


def shadow(rows, points, u):
    for v in u:
        points &= rows[v]
    return points


def primitive_from_generators(gens, degree):
    # For each pair 0,y, compute the smallest G-invariant equivalence
    # relation containing that pair. A proper nontrivial class is a block.
    for y in range(1, degree):
        labels = list(range(degree))
        def merge(a, b):
            x, z = labels[a], labels[b]
            if x == z:
                return False
            for i in range(degree):
                if labels[i] == z:
                    labels[i] = x
            return True
        merge(0, y)
        changed = True
        while changed:
            changed = False
            blocks = {}
            for i, z in enumerate(labels):
                blocks.setdefault(z, []).append(i)
            for block in blocks.values():
                for g in gens:
                    for x in block[1:]:
                        changed |= merge(g[block[0]], g[x])
        size = sum(z == labels[0] for z in labels)
        if 1 < size < degree:
            return False
    return True


@lru_cache(None)
def panel_action(a, b):
    n = a+b
    ss = masks(n, a)
    index = {s: i for i, s in enumerate(ss)}
    gens = []
    stabgens = []
    base = ss[0]
    for x in range(n-1):
        p = list(range(n))
        p[x], p[x+1] = p[x+1], p[x]
        g = tuple(index[image(s, p)] for s in ss)
        gens.append(g)
        if image(base, p) == base:
            stabgens.append(g)
    # Adjacent transpositions staying inside either base block generate
    # the entire set stabilizer, so its orbit test is independent of formula.
    orbit, todo = {1}, [1]
    while todo:
        x = todo.pop()
        for g in stabgens:
            y = g[x]
            if y not in orbit:
                orbit.add(y)
                todo.append(y)
    return primitive_from_generators(gens, len(ss)), len(orbit) == len(ss)-1


def cut_data(weights, edges):
    blocks, start = [], 0
    for w in weights:
        blocks.append(((1 << w)-1) << start)
        start += w
    cuts = []
    for i in range(len(edges)):
        cs = comps(len(weights), edges[:i]+edges[i+1:])
        away = next(c for c in cs if 0 not in c)
        cuts.append(sum(blocks[v] for v in away))
    return blocks, cuts


def direct_ip(vs, classes, rows, flags):
    queries = 0
    for points_list in classes:
        points = sum(1 << v for v in points_list)
        # Enumerated witness flags, grouped by their exact shadows. This
        # is a direct existential search, not the interval criterion.
        witnesses = {}
        for f in flags:
            s = shadow(rows, points, f)
            common = (1 << len(vs))-1
            for v in f:
                common &= rows[v]
            witnesses.setdefault(s, []).append(common)
        for x in range(len(vs)):
            for f in flags:
                u = (x,)+f
                s = shadow(rows, points, u)
                queries += 1
                if s:
                    umask = sum(1 << v for v in set(u))
                    if not any(m & umask == umask for m in witnesses.get(s, [])):
                        return False, queries
    return True, queries


def main():
    counts = dict(panel_actions=0, weighted_models=0, flag_orbit_equalities=0,
                  flags=0, residual_primitivity_checks=0, rank_two_models=0,
                  common_neighbor_pairs=0, full_shadow_models=0,
                  full_shadow_queries=0, weighted_claw_obstructions=0,
                  consecutive_rank_queries=0, contraction_models=0)
    for n in range(2, 9):
        for a in range(1, n):
            p, t = panel_action(a, n-a)
            assert p == (2*a != n or n == 2)
            assert t == (min(a, n-a) == 1)
            counts['panel_actions'] += 1

    # All weight assignments of total mass <=6 on all unlabelled trees.
    # Repeated isomorphic weighted trees are harmless and counted as models.
    for n in range(2, 7):
        for k in range(2, n+1):
            for graph in nx.nonisomorphic_trees(k):
                edges = list(graph.edges())
                for weights in compositions(n, k):
                    blocks, cuts = cut_data(weights, edges)
                    vs, classes, rows, flags = geometry(n, cuts)
                    lookup = {v: i for i, v in enumerate(vs)}
                    orbit_flags = set()
                    chambers = set()
                    for p in permutations(range(n)):
                        ch = tuple(lookup[(i, image(a, p))] for i, a in enumerate(cuts))
                        chambers.add(ch)
                        for m in range(1 << len(cuts)):
                            orbit_flags.add(tuple(v for i, v in enumerate(ch) if m >> i & 1))
                    assert set(flags) == orbit_flags
                    assert len(chambers) * product_int(factorial(w) for w in weights) == factorial(n)
                    counts['flag_orbit_equalities'] += 1
                    counts['flags'] += len(flags)
                    # Each residue group is a forest product. Test every
                    # deletion action using independent finite block tests.
                    all_residues_weak = True
                    for m in range(1, 1 << len(edges)):
                        chosen = [e for j, e in enumerate(edges) if m >> j & 1]
                        any_primitive = False
                        for component in comps(k, chosen):
                            ce = [e for e in chosen if e[0] in component]
                            for e in ce:
                                cs = comps(k, [f for f in ce if f != e])
                                left = next(c for c in cs if e[0] in c)
                                a = sum(weights[v] for v in left)
                                b = sum(weights[v] for v in component-left)
                                any_primitive |= panel_action(a, b)[0]
                        all_residues_weak &= any_primitive
                        counts['residual_primitivity_checks'] += 1
                    predicted = all(weights[a] != weights[b] or weights[a] == 1 for a, b in edges)
                    assert all_residues_weak == predicted
                    # Direct full shadow existence on every model mass<=5;
                    # all connected residue models are included in this sweep.
                    if n <= 5:
                        ip, queries = direct_ip(vs, classes, rows, flags)
                        expected = max(dict(graph.degree()).values()) <= 2 and all(
                            weights[v] == 1 for v in graph if graph.degree(v) >= 2)
                        assert ip == expected, (edges, weights, ip)
                        counts['full_shadow_models'] += 1
                        counts['full_shadow_queries'] += queries
                    counts['weighted_models'] += 1

    # Exact incidence graphs, not the binomial formula, give all common
    # neighbor counts for positive path triples with total mass <=9.
    for n in range(3, 10):
        for a, b, c in compositions(n, 3):
            aa, cc = masks(n, a), masks(n, c)
            na = [sum(1 << j for j, z in enumerate(cc) if not x & z) for x in aa]
            nc = [sum(1 << j for j, z in enumerate(aa) if not x & z) for x in cc]
            square = False
            for side, neighbors, target in ((aa, na, c), (cc, nc, a)):
                for i, j in combinations(range(len(side)), 2):
                    common = (neighbors[i] & neighbors[j]).bit_count()
                    remaining = n - (side[i] | side[j]).bit_count()
                    assert common == (comb(remaining, target) if remaining >= target else 0)
                    square |= common > 1
                    counts['common_neighbor_pairs'] += 1
            assert square == (b > 1)
            assert any(x & y for x in aa for y in cc)  # never a digon
            counts['rank_two_models'] += 1

    # General weighted-claw obstruction: enumerate every possible witness.
    for n in range(4, 9):
        for a, b, c in compositions(n-1, 3):
            cuts = [(1 << a)-1, ((1 << b)-1) << a, ((1 << c)-1) << (a+b)]
            vs, classes, rows, flags = geometry(n, cuts)
            lookup = {v: i for i, v in enumerate(vs)}
            x = lookup[(1, (1 << b)-1)]
            y = lookup[(1, ((1 << b)-1) ^ 1 ^ (1 << b))]
            points = sum(1 << v for v in classes[0])
            s = shadow(rows, points, (x,y))
            assert 1 < s.bit_count() < len(classes[0])
            assert not any(shadow(rows, points, f) == s and
                           all(rows[v] >> u & 1 for v in f for u in (x,y)) for f in flags)
            counts['weighted_claw_obstructions'] += 1

    # Check the actual <=2-vertex witnesses in every consecutive-rank
    # Boolean truncation of total mass <=6, using all x+flag queries.
    for n in range(3, 7):
        for lo in range(1, n-1):
            for hi in range(lo+1, n):
                cuts = [(1 << k)-1 for k in range(lo, hi+1)]
                vs, classes, rows, flags = geometry(n, cuts)
                lookup = {s: v for v, (_, s) in enumerate(vs)}
                for k, cls in zip(range(lo, hi+1), classes):
                    points = sum(1 << v for v in cls)
                    for x in range(len(vs)):
                        for f in flags:
                            u = (x,)+f
                            s = shadow(rows, points, u)
                            counts['consecutive_rank_queries'] += 1
                            if not s:
                                continue
                            if s.bit_count() == 1:
                                witness = (s.bit_length()-1,)
                            else:
                                low, high = 0, (1 << n)-1
                                for v in u:
                                    z = vs[v][1]
                                    if z.bit_count() < k:
                                        low |= z
                                    elif z.bit_count() > k:
                                        high &= z
                                witness = tuple(lookup[z] for z in (low, high) if z and z != (1 << n)-1)
                            assert len(witness) <= 2
                            assert all(rows[v] >> w & 1 for v,w in combinations(witness, 2))
                            assert all(rows[v] >> w & 1 for v in witness for w in u)
                            assert shadow(rows, points, witness) == s

    # Direct contraction identity on all unweighted trees through seven
    # vertices and all nonempty retained edge sets; cuts match as point sets.
    for n in range(2, 8):
        for graph in nx.nonisomorphic_trees(n):
            edges = list(graph.edges())
            for mask in range(1, 1 << len(edges)):
                removed = [e for i,e in enumerate(edges) if not mask >> i & 1]
                blocks = comps(n, removed)
                block_of = {v:i for i,b in enumerate(blocks) for v in b}
                retained = [e for i,e in enumerate(edges) if mask >> i & 1]
                quotient = [(block_of[a], block_of[b]) for a,b in retained]
                root = block_of[0]
                for i, e in enumerate(retained):
                    original = next(c for c in comps(n, [f for f in edges if f != e]) if 0 not in c)
                    qc = next(c for c in comps(len(blocks), quotient[:i]+quotient[i+1:]) if root not in c)
                    expanded = frozenset().union(*(blocks[v] for v in qc))
                    assert original == expanded
                counts['contraction_models'] += 1

    report = {'status':'PASS', 'counts':counts,
              'scope':'Finite independent block-system, flag-orbit, full shadow-witness, rank-two incidence and contraction audits. All-parameter proof is written separately; no whole-paper, priority, or Lean claim.',
              'dependencies':{'networkx':nx.__version__, 'usage':'nonisomorphic tree generation only'},
              'script_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    Path(__file__).with_suffix('.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


def product_int(values):
    out = 1
    for v in values:
        out *= v
    return out


if __name__ == '__main__':
    main()
