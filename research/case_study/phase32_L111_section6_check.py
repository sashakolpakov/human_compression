#!/usr/bin/env python3
"""Exact original diagnostics for L111 section6; no external packages."""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, permutations
import json
from pathlib import Path
from phase32_L111_check import Geometry, components, graph_data, stats, simplex, graph_product, check_iso


def merge(G):
    lower = G.types[0] + G.types[1]
    E = [(p, q) for p in G.types[0] for q in G.types[1] if G.inc(p, q)]
    types = {0: [(0, ('vertex', p)) for p in lower], 1: [(1, e) for e in E]}
    types.update({i: row for i, row in G.types.items() if i > 1})
    def inc(x, y):
        if x[0] == y[0]: return x == y
        if x[0] > y[0]: x, y = y, x
        if x[0] == 0:
            p = x[1][1]
            return p in y[1] if y[0] == 1 else G.inc(p, y)
        if x[0] == 1: return all(G.inc(p, y) for p in x[1])
        return G.inc(x, y)
    return Geometry(types, inc)


def split(G, color):
    ends = graph_data(G)
    assert set(color) == set(G.types[0]) and set(color.values()) == {0, 1}
    assert all(len({color[p] for p in P}) == 2 for P in ends.values())
    types = {i: [(i, ('split', v)) for v in G.types[0] if color[v] == i] for i in [0, 1]}
    types.update({i: row for i, row in G.types.items() if i > 1})
    edge_set = set(ends.values())
    def inc(x, y):
        if x[0] == y[0]: return x == y
        if x[0] > y[0]: x, y = y, x
        if y[0] == 1: return frozenset((x[1][1], y[1][1])) in edge_set
        if x[0] < 2: return G.inc(x[1][1], y)
        return G.inc(x, y)
    return Geometry(types, inc)


def merge_checks(G, name):
    M = merge(G); old, new = stats(G), stats(M)
    assert old['rc'] == new['rc']
    assert (len(components(G.all, G.inc)) == 1) == (len(components(M.all, M.inc)) == 1)
    assert new['chambers'] == 2 * old['chambers']
    graph_data(M)
    images = set()
    for C in G.chambers:
        D = dict((x[0], x) for x in C); p, q = D[0], D[1]
        for selected in (p, q):
            images.add(((0, ('vertex', selected)), (1, (p, q))) + tuple(D[i] for i in sorted(D) if i > 1))
    assert images == set(M.chambers)
    S = split(M, {v: v[1][1][0] for v in M.types[0]})
    mapping = {x: x[1][1][1][1] if x[0] < 2 else x for x in S.all}
    check_iso(S.types, S.inc, G.types, G.inc, mapping)
    residue_isos = 0
    for F in M.flags:
        vertices = [x for x in F if x[0] == 0]
        if not vertices: continue
        p = vertices[0][1][1]
        oldflag = tuple(x for x in F if x[0] > 1) + (p,)
        selected_edges = [x for x in F if x[0] == 1]
        if selected_edges:
            oldflag += tuple(v for v in selected_edges[0][1] if v != p)
        A, B = M.residue(F), G.residue(oldflag)
        f = {x: next(v for v in x[1] if v != p) if x[0] == 1 else x
             for row in A.values() for x in row}
        check_iso(A, M.inc, B, G.inc, f); residue_isos += 1
    return {'name': name, 'original': old, 'merged': new, 'copied_residue_isomorphisms': residue_isos,
            'chosen_bipartition_inverse': True}


def group(gens):
    n = len(gens[0]); identity = tuple(range(n)); seen = {identity}; todo = [identity]
    while todo:
        a = todo.pop()
        for g in gens:
            h = tuple(g[a[i]] for i in range(n))
            if h not in seen: seen.add(h); todo.append(h)
    return seen


def permutation(G, f):
    where = {x: i for i, x in enumerate(G.all)}
    p = tuple(where[f(x)] for x in G.all)
    assert len(set(p)) == len(p)
    assert all(G.all[p[i]][0] == x[0] for i, x in enumerate(G.all))
    assert all(G.inc(x, y) == G.inc(G.all[p[i]], G.all[p[j]])
               for i, x in enumerate(G.all) for j, y in enumerate(G.all))
    return p


def chamber_orbit(G, H):
    index = {x: i for i, x in enumerate(G.all)}
    C = tuple(index[x] for x in G.chambers[0])
    orbit = {tuple(G.all[g[i]] for i in C) for g in H}
    assert orbit == set(G.chambers)
    return len(orbit)


def disconnected_symmetry():
    G = Geometry({i: [(i, (c, v)) for c in range(2) for v in range(2)] for i in range(3)},
                 lambda x, y: x == y if x[0] == y[0] else x[1][0] == y[1][0])
    maps = []
    for c in range(2):
        for i in range(3):
            maps.append({x: (x[0], (x[1][0], 1 - x[1][1])) if x[0] == i and x[1][0] == c else x for x in G.all})
    maps.append({x: (x[0], (1 - x[1][0], x[1][1])) for x in G.all})
    H = group([permutation(G, f.__getitem__) for f in maps])
    assert len(H) == 128
    M = merge(G)
    extra = {x: (1 - x[0], x[1]) if x[0] < 2 and x[1][0] == 0 else x for x in G.all}
    def lift(f):
        def action(x):
            if x[0] == 0: return (0, ('vertex', f[x[1][1]]))
            if x[0] == 1: return (1, tuple(sorted((f[p] for p in x[1]), key=lambda y: y[0])))
            return f[x]
        return permutation(M, action)
    K = group([lift(f) for f in maps + [extra]])
    assert len(K) == 512
    assert sorted(map(len, components(G.all, G.inc))) == [6, 6]
    assert sorted(map(len, components(M.all, M.inc))) == [10, 10]
    # Exact full-group upper bound: a component permutation, and all square
    # graph automorphisms times the independent interchange of its two faces.
    vertices = [(0, ('vertex', x)) for x in G.types[0] + G.types[1] if x[1][0] == 0]
    ends = graph_data(M); adjacency = set(ends.values())
    square_aut = [p for p in permutations(vertices)
                  if all((frozenset((vertices[i], vertices[j])) in adjacency) ==
                         (frozenset((p[i], p[j])) in adjacency) for i in range(4) for j in range(4))]
    assert len(square_aut) == 8
    assert 2 * (len(square_aut) * 2) ** 2 == len(K)
    assert 2 * (2 ** 3) ** 2 == len(H)
    return {'original': stats(G), 'merged': stats(M), 'full_original_type_aut_order': len(H),
            'full_merged_type_aut_order': len(K), 'original_chamber_orbit': chamber_orbit(G, H),
            'merged_chamber_orbit': chamber_orbit(M, K), 'required_index_two_kernel_order': len(K) // 2,
            'original_full_group_too_small': len(K) // 2 > len(H),
            'construction_test': merge_checks(G, 'disconnected_two_complete_components')}


def torus(m):
    vertices = list(__import__('itertools').product(range(m), repeat=2))
    edges = {frozenset((v, ((v[0] + 1) % m, v[1]))) for v in vertices}
    edges |= {frozenset((v, (v[0], (v[1] + 1) % m))) for v in vertices}
    faces = {frozenset(((x, y), ((x + 1) % m, y), (x, (y + 1) % m), ((x + 1) % m, (y + 1) % m))) for x, y in vertices}
    types = {0: [(0, (v,)) for v in vertices],
             1: [(1, tuple(sorted(e))) for e in sorted(edges, key=lambda e: sorted(e))],
             2: [(2, tuple(sorted(F))) for F in sorted(faces, key=lambda F: sorted(F))]}
    def inc(x, y):
        if x[0] == y[0]: return x == y
        if x[0] > y[0]: x, y = y, x
        return set(x[1]) <= set(y[1])
    G = Geometry(types, inc); R = stats(G)
    assert R['rc'] and R['objects'] == {'0': m*m, '1': 2*m*m, '2': m*m}
    ends = graph_data(G)
    panels = 0
    for F in G.flags:
        if len(F) == 2:
            assert sum(map(len, G.residue(F).values())) == 2; panels += 1
    local_graphs = []
    for Q in G.types[2]:
        res = G.residue((Q,)); vv = res[0]; ee = res[1]
        assert len(vv) == len(ee) == 4
        assert all(sum(v in ends[e] for e in ee) == 2 for v in vv)
        assert len(components(vv, lambda x, y: frozenset((x, y)) in {ends[e] for e in ee})) == 1
        local_graphs.append('C4')
    weak_counts = Counter()
    for e in G.types[1]:
        for Q in G.types[2]:
            common = {v for v in G.types[0] if G.inc(v, e) and G.inc(v, Q)}
            weak_counts[str(len(common))] += 1
            if not common: continue
            F = (next(iter(common)),) if len(common) == 1 else (e,)
            assert all(G.inc(x, e) and G.inc(x, Q) for x in F)
            assert {v for v in G.types[0] if all(G.inc(v, x) for x in F)} == common
    row = [(0, (((x, 0)),)) for x in range(m)]
    assert len(set(row)) == m and m % 2
    assert all(frozenset((row[i], row[(i+1) % m])) in set(ends.values()) for i in range(m))
    def lift_vertex(f):
        return permutation(G, lambda x: (x[0], tuple(sorted(f(v) for v in x[1]))))
    gens = [lift_vertex(lambda v: ((v[0] + 1) % m, v[1])),
            lift_vertex(lambda v: (v[0], (v[1] + 1) % m)),
            lift_vertex(lambda v: ((-v[1]) % m, v[0])),
            lift_vertex(lambda v: (v[1], v[0]))]
    H = group(gens); assert len(H) == 8 * m * m
    return {'m': m, 'geometry': R, 'thin_panels': panels, 'local_graph_residues': dict(Counter(local_graphs)),
            'weak_shadow_checks': dict(weak_counts), 'odd_cycle_vertices': [(x, 0) for x in range(m)],
            'chamber_transitive_group_order': len(H), 'chamber_orbit': chamber_orbit(G, H),
            'global_bipartition_impossible': True}


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True)
    args=parser.parse_args(); output=Path(args.output)
    if output.exists(): raise SystemExit('Refusing to overwrite saved evidence')
    examples = [merge_checks(simplex(d), f'simplex_rank_{d}') for d in [3, 4]]
    P = graph_product(3, 4); MP = merge(P)
    graph_data(P, 2, 3); graph_data(MP, 2, 3)
    examples.append(merge_checks(P, 'cycle_graph_product'))
    report={'status':'PASS','checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
            'retained_helper_sha256':sha256(Path(__file__).with_name('phase32_L111_check.py').read_bytes()).hexdigest(),
            'merging_inverse_examples':examples,'disjoint_graph_pair_preserved':True,
            'disconnected_symmetry_converse':disconnected_symmetry(),
            'odd_square_torus_corollary_control':torus(5),
            'scope':'Exact finite examples and construction maps. No complete source-body access, later-version/priority claim or infinite-rank computation.'}
    output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print('PHASE32_L111_SECTION6_PASS')


if __name__=='__main__': main()
