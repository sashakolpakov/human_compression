#!/usr/bin/env python3
"""Exact optional checks for the rank-three construction boundary in F007.

The accompanying proof uses the explicit permutations; enumeration is a
diagnostic, not a premise for the infinite classification.
"""
import json
from collections import deque


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def components(generators, colors):
    remaining = set(range(len(generators[0])))
    result = []
    while remaining:
        todo = [min(remaining)]
        found = set(todo)
        while todo:
            u = todo.pop()
            for color in colors:
                v = generators[color][u]
                if v not in found:
                    found.add(v)
                    todo.append(v)
        remaining -= found
        result.append(sorted(found))
    return result


def automorphisms(generators):
    n = len(generators[0])
    result = []
    for target in range(n):
        mapping = {0: target}
        queue = deque([0])
        consistent = True
        while queue and consistent:
            u = queue.popleft()
            for g in generators:
                v, image = g[u], g[mapping[u]]
                if v in mapping:
                    if mapping[v] != image:
                        consistent = False
                        break
                else:
                    mapping[v] = image
                    queue.append(v)
        if consistent and len(mapping) == n and len(set(mapping.values())) == n:
            result.append([mapping[i] for i in range(n)])
    return result


def maniplex(g):
    n = len(g[0])
    return (len(components(g, [0, 1, 2])) == 1
            and all(g[i][g[i][x]] == x for i in range(3) for x in range(n))
            and all(len({x, *(g[i][x] for i in range(3))}) == 4 for x in range(n))
            and all(g[0][g[2][x]] == g[2][g[0][x]] for x in range(n)))


def truncation(g, torus, corrected=False):
    n = len(g[0])
    result = [[], [], []]
    for x in range(n):
        for layer in range(2):
            result[0].append(2 * g[layer][x] + layer)
            result[1].append(2 * x + (1 - layer))
            if not layer:
                result[2].append(2 * g[2][x])
                continue
            y, period = g[1][g[0][x]], 1
            while y != x:
                y = g[1][g[0][y]]
                period += 1
            need(period % 2 == 0, 'Failed small-map property at source line 74')
            y = x
            for _ in range(period // 2):
                y = g[1][g[0][y]]
            if torus:
                y = g[1 if corrected else 0][y]
            result[2].append(2 * y + 1)
    return result


def main():
    # A point is (v, layer), with v in C2 x C2, encoded as 2*v+layer.
    g = [[], [], []]
    for v in range(4):
        for layer in range(2):
            g[0].append(2 * (v ^ (1 if layer == 0 else 2)) + layer)
            g[1].append(2 * v + (1 - layer))
            g[2].append(2 * (v ^ (2 if layer == 0 else 3)) + layer)
    need(maniplex(g), 'Failed small-map property at source line 92')
    auto = automorphisms(g)
    expected = [[2 * ((x // 2) ^ v) + x % 2 for x in range(8)] for v in range(4)]
    need(sorted(auto) == sorted(expected), 'Failed small-map property at source line 95')
    faces = [components(g, [j for j in range(3) if j != i]) for i in range(3)]
    need([len(f) for f in faces] == [1, 2, 1], 'Failed small-map property at source line 97')
    chains = []
    for x in range(8):
        chain = set(range(8))
        for ff in faces:
            chain &= set(next(f for f in ff if x in f))
        chains.append(sorted(chain))
    need(all((len(c) == 4 for c in chains)), 'Failed small-map property at source line 104')
    # The short word relation distinguishes the two automorphism orbits.
    word_holds = [g[1][g[0][g[1][x]]] == g[2][x] for x in range(8)]
    need(word_holds == [x % 2 == 0 for x in range(8)], 'Failed small-map property at source line 107')
    # Any four-flag rank-three maniplex is the colored K4, up to relabeling.
    # Its three fixed-point-free involutions are the three perfect matchings.
    k4 = [[x ^ v for x in range(4)] for v in [1, 2, 3]]
    need(maniplex(k4) and len(automorphisms(k4)) == 4, 'Failed small-map property at source line 111')
    p = truncation(k4, False)
    t = truncation(k4, True)
    need(maniplex(p) and len(automorphisms(p)) == 8, 'Failed small-map property at source line 114')
    need(not maniplex(t), 'Failed small-map property at source line 115')
    need(all((t[0][x] == t[2][x] for x in range(8) if x % 2)), 'Failed small-map property at source line 116')
    # Exchange the two layers and use the reordered K4 marks (y,x,xy).
    # This realizes the example inside the repaired family, not a new family.
    repaired = truncation([k4[1], k4[0], k4[2]], True, corrected=True)
    swap = [x ^ 1 for x in range(8)]
    need(maniplex(repaired) and len(automorphisms(repaired)) == 4, 'Failed small-map property at source line 121')
    need(all((swap[g[i][x]] == repaired[i][swap[x]] for i in range(3) for x in range(8))), 'Failed small-map property at source line 122')
    print(json.dumps({
        'status': 'PASS_EXACT_EIGHT_FLAG_BOUNDARY_EXAMPLE',
        'generators': g, 'automorphisms': auto, 'faces': faces,
        'chain_classes': sorted({tuple(c) for c in chains}),
        'symmetry_type': '2_{0,2}',
        'four_flag_base_unique_up_to_colored_isomorphism': True,
        'projective_truncation_regular': True,
        'torus_truncation_has_parallel_edges': True,
        'corrected_torus_contains_example_after_layer_exchange': True,
        'source_5_9_and_5_10_literal_scope_fails': True,
        'general_classification_proved_by_this_program': False,
    }, indent=2))


if __name__ == '__main__':
    main()
