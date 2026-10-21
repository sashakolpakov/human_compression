#!/usr/bin/env python3
"""Finite controls for the source-defined Petrial and exact retained-object kernel.

Standard library only. The operation acts on chambers of incidence structures,
not on a presumed replacement generating set. Original examples use explicit
permutations, without a group catalogue or external presentation library.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def mul(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def inv(p):
    out = [0] * len(p)
    for i, v in enumerate(p):
        out[v] = i
    return tuple(out)


def cyc(n, *cycles):
    out = list(range(n))
    for cycle in cycles:
        for a, b in zip(cycle, cycle[1:] + cycle[:1]):
            out[a] = b
    return tuple(out)


def closure(gens):
    one = tuple(range(len(gens[0])))
    seen, queue = {one}, [one]
    for g in queue:
        for s in gens:
            h = mul(g, s)
            if h not in seen:
                seen.add(h)
                queue.append(h)
    return frozenset(seen)


def order(p):
    return len(closure([p]))


def connected(vertices, adjacent):
    if not vertices:
        return False
    seen, queue = {vertices[0]}, [vertices[0]]
    for v in queue:
        for w in vertices:
            if w not in seen and adjacent(v, w):
                seen.add(w)
                queue.append(w)
    return len(seen) == len(vertices)


class Geometry:
    def __init__(self, sizes, pairs):
        self.sizes = sizes
        self.pairs = {k: frozenset(v) for k, v in pairs.items()}
        self.vertices = [(i, j) for i, s in enumerate(sizes) for j in range(s)]
        self.chambers = tuple(c for c in itertools.product(*map(range, sizes))
                              if all((c[i], c[j]) in self.pairs[i, j]
                                     for i, j in ((0, 1), (0, 2), (1, 2))))
        self.panels = {}
        for c in self.chambers:
            for i in range(3):
                key = (i, tuple(c[j] for j in range(3) if j != i))
                self.panels.setdefault(key, []).append(c)

    def adjacent(self, x, y):
        i, a = x
        j, b = y
        if i == j:
            return a == b
        if i > j:
            i, j, a, b = j, i, b, a
        return (a, b) in self.pairs[i, j]

    def properties(self):
        geometry = bool(self.chambers)
        for i, s in enumerate(self.sizes):
            geometry &= all(any(c[i] == a for c in self.chambers) for a in range(s))
        for (i, j), edges in self.pairs.items():
            geometry &= all(any(c[i] == a and c[j] == b for c in self.chambers)
                            for a, b in edges)
        thin = geometry and all(len(v) == 2 for v in self.panels.values())
        rc = connected(self.vertices, self.adjacent)
        for v in self.vertices:
            residue = [w for w in self.vertices if w[0] != v[0] and self.adjacent(v, w)]
            rc &= connected(residue, self.adjacent)
        return {'geometry': bool(geometry), 'thin': bool(thin),
                'residually_connected': bool(rc), 'type_sizes': list(self.sizes),
                'chambers': len(self.chambers)}

    def flip(self, c, i):
        key = (i, tuple(c[j] for j in range(3) if j != i))
        choices = self.panels[key]
        assert len(choices) == 2 and c in choices
        return choices[choices[0] == c]

    def petrial(self):
        assert self.properties()['thin']
        successors = {}
        for c in self.chambers:
            d = c
            for i in (0, 2, 1):
                d = self.flip(d, i)
            successors[c] = d
        assert len(set(successors.values())) == len(successors)
        remaining = set(self.chambers)
        faces, by_chamber, cycles = set(), {}, []
        while remaining:
            start = min(remaining)
            walk, c = [], start
            while c not in walk:
                walk.append(c)
                c = successors[c]
            assert c == start
            remaining.difference_update(walk)
            face = (frozenset(c[0] for c in walk), frozenset(c[1] for c in walk))
            faces.add(face)
            for c in walk:
                by_chamber[c] = face
            cycles.append({'chambers': len(walk), 'vertices': len(face[0]),
                           'edges': len(face[1])})
        faces = tuple(sorted(faces, key=lambda f: (sorted(f[0]), sorted(f[1]))))
        pairs = {(0, 1): self.pairs[0, 1],
                 (0, 2): {(v, f) for f, face in enumerate(faces) for v in face[0]},
                 (1, 2): {(e, f) for f, face in enumerate(faces) for e in face[1]}}
        return Geometry((self.sizes[0], self.sizes[1], len(faces)), pairs), faces, by_chamber, cycles


def coset_geometry(gens):
    a, b, c = gens
    G = closure(gens)
    subgroups = [closure([a, b]), closure([a, c]), closure([b, c])]
    cosets = []
    for H in subgroups:
        cs = {frozenset(mul(g, h) for h in H) for g in G}
        cosets.append(tuple(sorted(cs, key=lambda x: sorted(x))))
    lookups = [{C: j for j, C in enumerate(cs)} for cs in cosets]
    actions = {g: tuple(tuple(lookups[i][frozenset(mul(g, h) for h in C)]
                             for C in cs) for i, cs in enumerate(cosets)) for g in G}
    pairs = {(i, j): {(x, y) for x, X in enumerate(cosets[i]) for y, Y in enumerate(cosets[j]) if X & Y}
             for i, j in ((0, 1), (0, 2), (1, 2))}
    geom = Geometry(tuple(map(len, cosets)), pairs)
    base = tuple(lookups[i][H] for i, H in enumerate(subgroups))
    return G, geom, base, actions


def run_case(name, generators, expected_thin):
    G, geom, base, actions = coset_geometry(generators)
    prop = geom.properties()
    assert prop['geometry'] and prop['thin'] and prop['residually_connected']
    assert len(geom.chambers) == len(G)
    assert {tuple(actions[g][i][base[i]] for i in range(3)) for g in G} == set(geom.chambers)
    new, faces, by_chamber, cycles = geom.petrial()
    new_prop = new.properties()
    assert new_prop['geometry'] and new_prop['residually_connected']
    assert new_prop['thin'] == expected_thin
    P = by_chamber[base]
    a, b, c = generators
    bP = (frozenset(actions[b][0][v] for v in P[0]), frozenset(actions[b][1][e] for e in P[1]))
    kernel = [g for g in G if all(actions[g][i] == tuple(range(geom.sizes[i])) for i in (0, 1))]
    # Compute the core independently from actual conjugates, then compare the
    # literal retained-object kernel with both forms of the uniform theorem.
    A = closure([a])
    core = set(A)
    for g in G:
        core.intersection_update(mul(mul(g, h), inv(g)) for h in A)
    assert set(kernel) == core
    central = all(mul(a, g) == mul(g, a) for g in G)
    one = tuple(range(len(a)))
    assert core == ({one, a} if central else {one})
    induced = set()
    face_lookup = {P: i for i, P in enumerate(faces)}
    for g in G:
        face_action = tuple(face_lookup[(frozenset(actions[g][0][v] for v in P[0]),
                                        frozenset(actions[g][1][e] for e in P[1]))] for P in faces)
        act = actions[g][:2] + (face_action,)
        induced.add(act)
        assert all(tuple(act[i][C[i]] for i in range(3)) in new.chambers for C in new.chambers)
    out = {'name': name, 'generators_zero_based': list(map(list, generators)),
           'group_order': len(G), 'pair_orders_ab_ac_bc': [order(mul(a, b)), order(mul(a, c)), order(mul(b, c))],
           'original': prop, 'petrial': new_prop, 'action_kernel_order': len(kernel),
           'induced_action_order': len(induced), 'base_face_fixed_by_b': bP == P,
           'computed_core_order': len(core), 'face_marker_central': central,
           'petrie_cycles': sorted(cycles, key=lambda x: (x['chambers'], x['vertices'], x['edges']))}
    if new_prop['thin']:
        assert len(kernel) == 1
        base_new = base[:2] + (face_lookup[P],)
        orbit = {tuple(act[i][base_new[i]] for i in range(3)) for act in induced}
        assert orbit == set(new.chambers)
        second, second_faces, _, _ = new.petrial()
        old_shadows = tuple((frozenset(v for v, f0 in geom.pairs[0, 2] if f0 == f),
                             frozenset(e for e, f0 in geom.pairs[1, 2] if f0 == f))
                            for f in range(geom.sizes[2]))
        assert len(set(old_shadows)) == len(old_shadows)
        assert set(second_faces) == set(old_shadows)
        assert second.properties()['thin'] and second.properties()['residually_connected']
        out['bidual_face_shadows_exact'] = True
        out['induced_action_chamber_regular'] = True
        assert 2 in out['pair_orders_ab_ac_bc'][:2]
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path(__file__).with_suffix('.json'))
    args = parser.parse_args()
    cases = [
        ('C2_cubed', [cyc(6, (0, 1)), cyc(6, (2, 3)), cyc(6, (4, 5))], False),
        ('C2_times_S3', [cyc(5, (0, 1)), cyc(5, (2, 3)), cyc(5, (3, 4))], False),
        ('S4_tetrahedron', [cyc(4, (2, 3)), cyc(4, (1, 2)), cyc(4, (0, 1))], True),
        ('S4_tetrahedron_vertex_edge_swap', [cyc(4, (2, 3)), cyc(4, (0, 1)), cyc(4, (1, 2))], True),
        ('S4_star', [cyc(4, (0, 1)), cyc(4, (0, 2)), cyc(4, (0, 3))], False),
        ('B3_cube', [cyc(6, (2, 4), (3, 5)), cyc(6, (0, 2), (1, 3)), cyc(6, (0, 1))], True),
        ('B3_cube_vertex_edge_swap', [cyc(6, (2, 4), (3, 5)), cyc(6, (0, 1)), cyc(6, (0, 2), (1, 3))], True),
    ]
    results = [run_case(*case) for case in cases]
    assert results[0]['action_kernel_order'] == results[1]['action_kernel_order'] == 2
    assert results[0]['petrial']['type_sizes'] == [2, 2, 1]
    assert results[2]['base_face_fixed_by_b'] and not results[3]['base_face_fixed_by_b']
    report = {'status': 'PASS', 'scope': 'Seven explicit finite examples; no exhaustion or uniform proof claim.',
              'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'cases': results, 'summary': {'examples': len(results),
                 'original_chambers': sum(x['original']['chambers'] for x in results),
                 'thin_petrials': sum(x['petrial']['thin'] for x in results),
                 'nonfaithful_petrial_actions': sum(x['action_kernel_order'] > 1 for x in results)}}
    with args.output.open('x', encoding='utf-8') as stream:
        stream.write(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report['summary'], sort_keys=True))
    print('PASS')


if __name__ == '__main__':
    main()
