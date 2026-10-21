#!/usr/bin/env python3
"""Literal finite tests for the L111 neighbourhood operation; stdlib only."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


class Geometry:
    def __init__(self, types, incident):
        self.types = {i: tuple(row) for i, row in types.items()}
        self.inc = incident
        self.all = tuple(x for row in self.types.values() for x in row)
        assert len(self.all) == len(set(self.all))
        self.flags = [()]
        for i, row in sorted(self.types.items()):
            self.flags += [F + (x,) for F in list(self.flags) for x in row
                           if all(incident(x, y) for y in F)]
        self.chambers = [F for F in self.flags if len(F) == len(types)]
        extendable = {tuple(x for k, x in enumerate(C) if mask >> k & 1)
                      for C in self.chambers for mask in range(1 << len(C))}
        assert set(self.flags) == extendable, 'Not a geometry'

    def residue(self, flag):
        used = {x[0] for x in flag}
        return {i: tuple(x for x in row if all(self.inc(x, y) for y in flag))
                for i, row in self.types.items() if i not in used}


def components(objects, incident):
    unseen = set(objects); out = []
    while unseen:
        todo = [unseen.pop()]; C = set(todo)
        while todo:
            x = todo.pop()
            new = {y for y in unseen if incident(x, y)}
            unseen -= new; C |= new; todo.extend(new)
        out.append(C)
    return out


def stats(G):
    connected = []; disconnected = []; pair_fail = 0
    for F in G.flags:
        R = G.residue(F)
        if len(R) < 2: continue
        C = components([x for row in R.values() for x in row], G.inc)
        (connected if len(C) == 1 else disconnected).append(tuple(map(len, C)))
        for i, j in combinations(R, 2):
            pair_fail += len(components(R[i] + R[j], G.inc)) != 1
    assert (not disconnected) == (pair_fail == 0), 'Finite-rank strong/RC mismatch'
    return dict(objects={str(i): len(row) for i, row in G.types.items()},
                flags=len(G.flags), chambers=len(G.chambers),
                connected_residues=len(connected), disconnected_residues=len(disconnected),
                rc=not disconnected, pair_truncation_failures=pair_fail)


def graph_data(G, a=0, b=1):
    endpoints = {e: frozenset(v for v in G.types[a] if G.inc(e, v)) for e in G.types[b]}
    assert all(len(P) == 2 for P in endpoints.values())
    assert len(endpoints) == len(set(endpoints.values()))
    assert all(any(v in P for P in endpoints.values()) for v in G.types[a])
    for e, P in endpoints.items():
        for i, row in G.types.items():
            if i in (a, b): continue
            for x in row: assert G.inc(e, x) == all(G.inc(v, x) for v in P)
    return endpoints


def transform(G, a=0, b=1):
    endpoints = graph_data(G, a, b)
    edge_of = {P: e for e, P in endpoints.items()}
    types = {i: tuple((i, ('copy', v)) for v in G.types[a]) if i in (a, b) else row
             for i, row in G.types.items()}
    def inc(x, y):
        if x[0] == y[0]: return x == y
        if x[0] in (a, b) and y[0] in (a, b):
            return frozenset((x[1][1], y[1][1])) in edge_of
        if x[0] in (a, b): return G.inc(x[1][1], y)
        if y[0] in (a, b): return G.inc(x, y[1][1])
        return G.inc(x, y)
    return Geometry(types, inc), endpoints, edge_of


def check_iso(A, ia, B, ib, mapping):
    aa = [x for row in A.values() for x in row]
    bb = [x for row in B.values() for x in row]
    assert set(mapping) == set(aa)
    assert len(mapping) == len(set(mapping.values())) and set(mapping.values()) == set(bb)
    assert all(ia(x, y) == ib(mapping[x], mapping[y]) for x in aa for y in aa)


def bipartite(vertices, edges):
    neigh = {v: set() for v in vertices}
    for P in edges:
        x, y = tuple(P); neigh[x].add(y); neigh[y].add(x)
    color = {}
    for root in vertices:
        if root in color: continue
        color[root] = 0; todo = [root]
        while todo:
            x = todo.pop()
            for y in neigh[x]:
                if y in color:
                    if color[y] == color[x]: return False
                else: color[y] = 1 - color[x]; todo.append(y)
    return True


def check(G, name, a=0, b=1, permutations=()):
    U, endpoints, edge_of = transform(G, a, b)
    old = stats(G); new = stats(U)
    images = set()
    for C in G.chambers:
        D = {x[0]: x for x in C}; p, e = D[a], D[b]
        q = next(iter(endpoints[e] - {p}))
        images.add(tuple((i, ('copy', p if i == a else q)) if i in (a, b) else D[i]
                         for i in sorted(G.types)))
    assert images == set(U.chambers) and len(images) == len(G.chambers)
    maps = 0; local_bipartite = 0
    for F in U.flags:
        copies = [x for x in F if x[0] in (a, b)]
        if not copies:
            R = G.residue(F)
            RU = U.residue(F)
            if len(R) == 2:
                V = R[a]; Es = [endpoints[e] for e in R[b]]
                local_bipartite += bipartite(V, Es)
            else:
                assert (len(components([x for row in R.values() for x in row], G.inc)) == 1) == (len(components([x for row in RU.values() for x in row], U.inc)) == 1)
            continue
        first = copies[0]; i = first[0]; p = first[1][1]
        higher = tuple(x for x in F if x[0] not in (a, b))
        original_flag = higher + (p,)
        if len(copies) == 2:
            q = copies[1][1][1]
            original_flag += (edge_of[frozenset((p, q))],)
        A, B = U.residue(F), G.residue(original_flag)
        mapping = {x: edge_of[frozenset((p, x[1][1]))] if x[0] in (a, b) else x
                   for row in A.values() for x in row}
        check_iso(A, U.inc, B, G.inc, mapping); maps += 1
    assert new['rc'] == (old['rc'] and local_bipartite == 0)
    # Verify exact equivariance, not just a chamber count, for supplied actions.
    equivariant_chambers = 0
    for g in permutations:
        assert set(g) == set(G.all) and set(g.values()) == set(G.all)
        assert all(g[x][0] == x[0] for x in G.all)
        assert all(G.inc(x, y) == G.inc(g[x], g[y]) for x in G.all for y in G.all)
        gu = {x: (x[0], ('copy', g[x[1][1]])) if x[0] in (a, b) else g[x] for x in U.all}
        assert all(U.inc(x, y) == U.inc(gu[x], gu[y]) for x in U.all for y in U.all)
        def chamber_map(C):
            D = {x[0]: x for x in C}; p, e = D[a], D[b]
            q = next(iter(endpoints[e] - {p}))
            return tuple((i, ('copy', p if i == a else q)) if i in (a, b) else D[i]
                         for i in sorted(G.types))
        for C in G.chambers:
            assert chamber_map(tuple(g[x] for x in C)) == tuple(gu[x] for x in chamber_map(C))
            equivariant_chambers += 1
    return {'name': name, 'original': old, 'transformed': new,
            'local_bipartite_graphs': local_bipartite,
            'residue_isomorphisms': maps, 'equivariant_chamber_checks': equivariant_chambers}


def rank_three_graph(n, edges, faces):
    types = {0: [(0, i) for i in range(n)],
             1: [(1, tuple(sorted(P))) for P in edges],
             2: [(2, j) for j in range(len(faces))]}
    def inc(x, y):
        if x[0] == y[0]: return x == y
        if x[0] > y[0]: x, y = y, x
        if y[0] == 1: return x[1] in y[1]
        return ({x[1]} if x[0] == 0 else set(x[1])) <= faces[y[1]]
    return Geometry(types, inc)


def simplex(rank):
    types = {i: [(i, P) for P in combinations(range(rank + 1), i + 1)] for i in range(rank)}
    def inc(x, y):
        if x[0] == y[0]: return x == y
        return set(x[1]) <= set(y[1]) or set(y[1]) <= set(x[1])
    return Geometry(types, inc)


def graph_product(m, n):
    types = {}
    for a, p in [(0, m), (2, n)]:
        types[a] = [(a, v) for v in range(p)]
        types[a + 1] = [(a + 1, tuple(sorted((v, (v + 1) % p)))) for v in range(p)]
    def inc(x, y):
        if x[0] == y[0]: return x == y
        if x[0] // 2 != y[0] // 2: return True
        if x[0] > y[0]: x, y = y, x
        return x[1] in y[1]
    return Geometry(types, inc)


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output', required=True)
    args = parser.parse_args(); out = Path(args.output)
    if out.exists(): raise SystemExit('Refusing to overwrite an evidence file')
    rows = []
    for m in range(3, 9):
        G = rank_three_graph(m, [{v, (v + 1) % m} for v in range(m)], [set(range(m))] * 2)
        actions = []
        for shift, sign in [(1, 1), (0, -1)]:
            g = {}
            for x in G.all:
                if x[0] == 0: y = (0, (sign * x[1] + shift) % m)
                elif x[0] == 1: y = (1, tuple(sorted((sign * v + shift) % m for v in x[1])))
                else: y = x
                g[x] = y
            actions.append(g)
        rows.append(check(G, f'dihedron_{m}', permutations=actions))
    for d in [3, 4, 5]: rows.append(check(simplex(d), f'simplex_rank_{d}'))
    # Both individual higher shadows are triangles, but their intersection may be an edge.
    types = {0: [(0, v) for v in range(4)],
             1: [(1, e) for e in combinations(range(4), 2)],
             2: [(2, T) for T in combinations(range(4), 3)],
             3: [(3, T) for T in combinations(range(4), 3)]}
    def inc(x, y):
        if x[0] == y[0]: return x == y
        if x[0] > y[0]: x, y = y, x
        if x[0] >= 2: return True
        return ({x[1]} if x[0] == 0 else set(x[1])) <= set(y[1])
    rows.append(check(Geometry(types, inc), 'triangle_shadows_common_edge_control'))
    iteration = []
    for m, n in [(3, 3), (3, 4), (4, 5)]:
        G = graph_product(m, n)
        A, _, _ = transform(G, 0, 1); B, _, _ = transform(G, 2, 3)
        AB, _, _ = transform(A, 2, 3); BA, _, _ = transform(B, 0, 1)
        assert AB.types == BA.types
        assert all(AB.inc(x, y) == BA.inc(x, y) for x in AB.all for y in AB.all)
        rows.append(check(G, f'product_{m}_{n}_first'))
        rows.append(check(A, f'product_{m}_{n}_second', 2, 3))
        iteration.append({'cycle_lengths': [m, n], 'chambers': len(AB.chambers),
                          'same_incidence': True, 'residually_connected': stats(AB)['rc']})
    # Unfiltered graph/subset input sweep, retaining only the literal geometry condition.
    sweep = Counter()
    for n in [3, 4]:
        all_edges = list(combinations(range(n), 2))
        for mask in range(1 << len(all_edges)):
            edges = [set(e) for j, e in enumerate(all_edges) if mask >> j & 1]
            if any(not any(v in e for e in edges) for v in range(n)): continue
            for subset in range(1 << n):
                face = {v for v in range(n) if subset >> v & 1}
                if len(face) < 2: continue
                induced = [e for e in edges if e <= face]
                if any(not any(v in e for e in induced) for v in face): continue
                G = rank_three_graph(n, edges, [set(range(n)), face])
                row = check(G, f'sweep_{n}_{mask}_{subset}')
                sweep['cases'] += 1
                sweep['original_rc'] += row['original']['rc']
                sweep['transformed_rc'] += row['transformed']['rc']
                sweep['residue_isomorphisms'] += row['residue_isomorphisms']
                sweep['flags_checked'] += row['original']['flags'] + row['transformed']['flags']
    report = {'status': 'PASS', 'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'examples': rows, 'disjoint_pair_iteration': iteration, 'rank_three_input_sweep': dict(sweep),
              'scope': 'Exact finite object/flag/residue/action tests. No complete source body, full automorphism group, infinite-rank theorem or uniform proof inferred from enumeration.'}
    out.write_text(json.dumps(report, sort_keys=True, indent=2) + '\n')
    print('PHASE32_L111_CHECK_PASS', dict(sweep))


if __name__ == '__main__': main()
