#!/usr/bin/env python3
"""Exact small lift-extension diagnostics; Python standard library only.

This does not prove the uniform theorem. No other project module is imported.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def mul(g, h):
    p, a = g
    q, b = h
    return (tuple(p[q[i]] for i in range(len(p))), a ^ b)


def inv(g):
    p, bit = g
    result = [0] * len(p)
    for i, j in enumerate(p):
        result[j] = i
    return (tuple(result), bit)


def transposition(n, i, j, bit=0):
    p = list(range(n))
    p[i], p[j] = p[j], p[i]
    return (tuple(p), bit)


def closure(gens, identity):
    ans = {identity}
    todo = [identity]
    while todo:
        a = todo.pop()
        for b in gens:
            c = mul(a, b)
            if c not in ans:
                ans.add(c)
                todo.append(c)
    return ans


def components(vertices, edges):
    unseen = set(vertices)
    out = []
    adjacency = {v: set() for v in vertices}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    while unseen:
        s = unseen.pop()
        part, todo = {s}, [s]
        while todo:
            for t in adjacency[todo.pop()]:
                if t in unseen:
                    unseen.remove(t)
                    part.add(t)
                    todo.append(t)
        out.append(frozenset(part))
    return out


def run_case(parity):
    n = 4 if parity else 3
    ident = (tuple(range(n)), 0)
    group = {(p, b) for p in itertools.permutations(range(n)) for b in range(2)}
    if parity:
        # Ghat=S4 x C2, quotient is S4. The deck bit switches layers.
        vertices = {(v, c) for v in range(n) for c in range(2)}
        edges = {frozenset(((u, 0), (v, 1))) for u in range(n)
                 for v in range(n) if u != v}
        faces = set(range(n))  # the omitted tetrahedron vertex
        face_vertices = {f: frozenset((v, c) for v in range(n) if v != f
                                    for c in range(2)) for f in faces}
        rho = [transposition(n, 0, 1, 1), transposition(n, 1, 2),
               transposition(n, 2, 3)]
        deck = {ident, (ident[0], 1)}
        base_objects = ((0, (0, 0)), (1, frozenset(((0, 0), (1, 1)))), (2, 3))

        def project(g):
            return g[0]

        def vertex_action(g, v):
            return (g[0][v[0]], g[1] ^ v[1])

        def face_action(g, f):
            return g[0][f]
    else:
        # Identity cover of the triangular dihedron. G=S3 x C2 has
        # a nontrivial graph-action kernel, acting by switching its two faces.
        vertices = set(range(n))
        edges = {frozenset(e) for e in itertools.combinations(vertices, 2)}
        faces = {0, 1}
        face_vertices = {f: frozenset(vertices) for f in faces}
        rho = [transposition(n, 0, 1), transposition(n, 1, 2), (ident[0], 1)]
        deck = {ident}
        base_objects = ((0, 0), (1, frozenset((0, 1))), (2, 0))

        def project(g):
            return g

        def vertex_action(g, v):
            return g[0][v]

        def face_action(g, f):
            return g[1] ^ f

    assert all(mul(g, g) == ident and g != ident for g in rho)
    subsets = {mask: closure([rho[i] for i in range(3) if mask >> i & 1], ident)
               for mask in range(8)}
    assert subsets[7] == group
    for a in range(8):
        for b in range(8):
            assert subsets[a] & subsets[b] == subsets[a & b]

    objects = [set((0, v) for v in vertices), set((1, e) for e in edges),
               set((2, f) for f in faces)]

    def act(g, obj):
        typ, x = obj
        if typ == 0:
            return (0, vertex_action(g, x))
        if typ == 1:
            return (1, frozenset(vertex_action(g, v) for v in x))
        return (2, face_action(g, x))

    def incident(a, b):
        if a[0] > b[0]:
            a, b = b, a
        if a[0] == b[0]:
            return a == b
        if (a[0], b[0]) == (0, 1):
            return a[1] in b[1]
        if a[0] == 0:
            return a[1] in face_vertices[b[1]]
        return a[1] <= face_vertices[b[1]]

    for g in group:
        for typ in range(3):
            assert {act(g, o) for o in objects[typ]} == objects[typ]
    graph_kernel = {g for g in group if all(vertex_action(g, v) == v for v in vertices)}
    full_kernel = {g for g in group if all(act(g, o) == o for os in objects for o in os)}
    assert full_kernel == {ident}
    assert len(graph_kernel) == (1 if parity else 2)

    parabolics = [{g for g in group if act(g, base_objects[i]) == base_objects[i]}
                  for i in range(3)]
    assert all(parabolics[i] == subsets[7 ^ (1 << i)] for i in range(3))
    cosets = {o: {g for g in group if act(g, base_objects[i]) == o}
              for i in range(3) for o in objects[i]}
    for i, j in itertools.combinations(range(3), 2):
        for a in objects[i]:
            for b in objects[j]:
                assert incident(a, b) == bool(cosets[a] & cosets[b])

    flags = []
    for selected in itertools.product(*[[None] + list(os) for os in objects]):
        f = tuple(x for x in selected if x is not None)
        if all(incident(a, b) for a, b in itertools.combinations(f, 2)):
            flags.append(f)
    chambers = {frozenset(f) for f in flags if len(f) == 3}
    orbit = {frozenset(act(g, o) for o in base_objects) for g in group}
    assert orbit == chambers and len(chambers) == len(group)
    for f in flags:
        common = set(group)
        for o in f:
            common &= cosets[o]
        assert common  # typed Helly, hence flag completion
        assert any(set(f) <= c for c in chambers)

    # Exact parabolic formulas for every subflag of the base chamber.
    for mask in range(8):
        stab = set(group)
        for i in range(3):
            if mask >> i & 1:
                stab &= parabolics[i]
        assert stab == subsets[7 ^ mask]
    assert all(len(parabolics[i] & deck) == 1 for i in (0, 1))

    # Component-derived monodromy versus the kernel of the higher parabolic.
    face = base_objects[2][1]
    fv = face_vertices[face]
    fe = {e for e in edges if e <= fv}
    comps = components(fv, fe)
    y = base_objects[0][1]
    cf = next(c for c in comps if y in c)
    mono = {a for a in deck if vertex_action(a, y) in cf}
    assert mono == deck & parabolics[2]
    assert len({project(g) for g in parabolics[2]}) * len(mono) == len(parabolics[2])
    lf = {g for g in group if face_action(g, face) == face and
          frozenset(vertex_action(g, z) for z in cf) == cf}
    assert lf == subsets[3] == parabolics[2]
    assert len(parabolics[2]) // len(lf) == len(deck & parabolics[2]) // len(mono)

    result = {
        'group_order': len(group), 'vertices': len(vertices), 'edges': len(edges),
        'higher_objects': len(faces), 'flags': len(flags), 'chambers': len(chambers),
        'all_subset_closures': 8, 'exact_binary_meets': 64,
        'maximal_parabolic_orders': list(map(len, parabolics)),
        'deck_order': len(deck), 'higher_monodromy_order': len(mono),
        'graph_action_kernel_order': len(graph_kernel), 'full_action_kernel_order': len(full_kernel),
        'coset_incidence_and_typed_Helly': True,
        'all_base_subflag_parabolic_formulas': True,
        'local_stabilizer_index_identity': True,
    }
    if parity:
        # Bipartite compression and the two canonical halved generators.
        positive = {g for g in group if g[1] == 0}
        folded = [mul(mul(rho[0], rho[1]), rho[0]), rho[1], rho[2]]
        folded_subgroups = {m: closure([folded[i] for i in range(3) if m >> i & 1], ident)
                            for m in range(8)}
        assert folded_subgroups[7] == positive
        assert len({project(g) for g in positive}) == 24
        assert deck & positive == {ident}
        for a in range(8):
            for b in range(8):
                assert folded_subgroups[a] & folded_subgroups[b] == folded_subgroups[a & b]
        result['compressed_group_order'] = len(positive)
        result['compressed_deck_kernel_order'] = 1
        result['compressed_marking_exact_meets'] = 64
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    out = Path(args.output)
    if out.exists():
        raise SystemExit('Refusing to overwrite an existing report')
    report = {
        'status': 'PASS',
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope': 'Two exact finite examples only; no uniform theorem or primary-source verification by code.',
        'parity_cover_tetrahedron': run_case(True),
        'identity_cover_triangular_dihedron': run_case(False),
    }
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
