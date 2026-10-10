#!/usr/bin/env python3
"""Exact nested-shadow applications. No external algebra or geometry package."""
import argparse
import json
from hashlib import sha256
from itertools import combinations
from pathlib import Path


def components(vertices, adjacent):
    unseen = set(vertices)
    answer = []
    while unseen:
        seed = next(iter(unseen)); unseen.remove(seed)
        stack = [seed]; seen = {seed}
        while stack:
            u = stack.pop()
            fresh = {v for v in unseen if adjacent(u, v)}
            unseen -= fresh; seen |= fresh; stack.extend(fresh)
        answer.append(frozenset(seen))
    return answer


def audit(types, incident):
    flags = [()]
    for T in types:
        flags += [F + (x,) for F in list(flags) for x in T
                  if all(incident(x, y) for y in F)]
    chambers = [F for F in flags if len(F) == len(types)]
    extendable = {tuple(C[i] for i in range(len(C)) if mask >> i & 1)
                  for C in chambers for mask in range(1 << len(C))}
    assert set(flags) == extendable
    panels = 0; residues = 0
    for F in flags:
        missing = set(range(len(types))) - {x[0] for x in F}
        R = [x for i in missing for x in types[i]
             if all(incident(x, y) for y in F)]
        if len(missing) == 1:
            assert len(R) == 2; panels += 1
        elif len(missing) >= 2:
            assert len(components(R, incident)) == 1; residues += 1
    return dict(objects=list(map(len, types)), flags=len(flags), chambers=len(chambers),
                connected_residues=residues, thin_panels=panels)


def danzer(axes_count, axis_faces):
    """axis_faces[j-1] lists the freely varying coordinate sets of j-faces."""
    types = [[(0, (x,)) for x in range(1 << axes_count)]]
    for j, faces in enumerate(axis_faces, 1):
        objects = []
        for A in faces:
            mask = sum(1 << i for i in A)
            for x in range(1 << axes_count):
                if x & mask: continue
                vertices = tuple(y for y in range(1 << axes_count) if y & ~mask == x)
                objects.append((j, vertices))
        assert len(set(objects)) == len(objects)
        types.append(objects)
    return types


def old_incident(x, y):
    if x[0] == y[0]: return x == y
    if x[0] > y[0]: x, y = y, x
    return set(x[1]) <= set(y[1])


def compress_coordinate(types):
    new = [[(i, (v[1][0],)) for v in types[0]
            if v[1][0].bit_count() % 2 == i] for i in [0, 1]] + types[2:]
    def inc(x, y):
        if x[0] == y[0]: return x == y
        if x[0] > y[0]: x, y = y, x
        if y[0] == 1: return (x[1][0] ^ y[1][0]).bit_count() == 1
        return set(x[1]) <= set(y[1])
    return audit(new, inc)


def cover(types, distinguished_edge, modulus, compress=False):
    base_vertices = [x[1][0] for x in types[0]]
    base_edges = {tuple(sorted(x[1])) for x in types[1]}
    def voltage(u, v):
        return (1 if (u, v) == distinguished_edge else
                -1 if (v, u) == distinguished_edge else 0)
    vertices = [(v, a) for v in base_vertices for a in range(modulus)]
    def adjacent(x, y):
        return tuple(sorted((x[0], y[0]))) in base_edges and (x[1] + voltage(x[0], y[0]) - y[1]) % modulus == 0
    assert len(components(vertices, adjacent)) == 1
    edges = [frozenset((x, y)) for x, y in combinations(vertices, 2) if adjacent(x, y)]
    shadows = {}; bases = {}; higher = []
    for j, T in enumerate(types[2:], 2):
        row = []
        for base_face in T:
            for C in components([v for v in vertices if v[0] in base_face[1]], adjacent):
                x = (j, len(row)); row.append(x); shadows[x] = C; bases[x] = base_face
        higher.append(row)
    lifted = [[(0, v) for v in vertices], [(1, e) for e in edges]] + higher
    def incident(x, y):
        if x[0] == y[0]: return x == y
        if x[0] > y[0]: x, y = y, x
        if y[0] == 1: return x[1] in y[1]
        if x[0] == 0: return x[1] in shadows[y]
        if x[0] == 1: return x[1] <= shadows[y]
        return old_incident(bases[x], bases[y]) and bool(shadows[x] & shadows[y])
    result = {'graph_incidence': audit(lifted, incident)}
    # Every incident higher pair restricts to nested components, not merely an
    # equality of monodromy cardinalities.
    pairs = 0
    for x, y in combinations([x for T in higher for x in T], 2):
        if incident(x, y):
            assert shadows[x] <= shadows[y] or shadows[y] <= shadows[x]; pairs += 1
    result['nested_higher_component_pairs'] = pairs
    if compress:
        assert all(x[0].bit_count() % 2 != y[0].bit_count() % 2 for e in edges for x, y in [tuple(e)])
        colored = [[(i, v) for v in vertices if v[0].bit_count() % 2 == i] for i in [0, 1]] + higher
        def colored_incident(x, y):
            if x[0] == y[0]: return x == y
            if x[0] > y[0]: x, y = y, x
            if y[0] == 1: return adjacent(x[1], y[1])
            if x[0] < 2: return x[1] in shadows[y]
            return incident(x, y)
        result['compression'] = audit(colored, colored_incident)
    else:
        # For the tetrahedral cover, two lifted faces have three disjoint
        # common edges. In particular their intersection has no greatest face.
        long_faces = [x for x in higher[0] if len(shadows[x]) == 9]
        assert len(long_faces) == 2
        meet = shadows[long_faces[0]] & shadows[long_faces[1]]
        assert sorted(map(len, components(meet, adjacent))) == [2, 2, 2]
        result['nonlattice_control_common_components'] = [2, 2, 2]
    return result


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output', required=True)
    args = parser.parse_args(); output = Path(args.output)
    if output.exists(): raise SystemExit('Refusing to overwrite existing evidence')
    rows = []
    for p in [3, 4, 5, 6]:
        types = danzer(p, [[(i,) for i in range(p)],
                           [tuple(sorted((i, (i + 1) % p))) for i in range(p)]])
        result = compress_coordinate(types)
        assert result['objects'] == [2 ** (p - 1), 2 ** (p - 1), p * 2 ** (p - 2)]
        assert result['chambers'] == p * 2 ** p
        rows.append({'polygon_p': p, **result})
    tesseract = danzer(4, [list(combinations(range(4), j)) for j in [1, 2, 3]])
    cube_result = compress_coordinate(tesseract)
    assert cube_result['chambers'] == 192
    tetrahedron = [[(0, (i,)) for i in range(4)],
                   [(1, e) for e in combinations(range(4), 2)],
                   [(2, F) for F in combinations(range(4), 3)]]
    result = {'status': 'PASS', 'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'Danzer_polygon_compressions': rows,
              'Danzer_simplex_rank_four_compression': cube_result,
              'tetrahedron_C3_cover': cover(tetrahedron, (1, 2), 3),
              'tesseract_C3_cover': cover(tesseract, (0, 1), 3, True),
              'scope': 'All flags/panels/residues in these exact coordinate geometries; no uniform theorem inferred from enumeration.'}
    output.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print('PHASE30_SOURCE_GEOMETRY_PASS')


if __name__ == '__main__': main()
