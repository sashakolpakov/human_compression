#!/usr/bin/env python3
"""Exact small-graph certificate, using only the Python standard library.

The finite-field/coset graphs are separate required inputs. Stored automorphism
generators were discovered with pynauty, but no automorphism backend is used here.
Fullness follows from an elementary refinement upper bound and a matching exact
subgroup lower bound. The literal graph inputs and generators are bound by the author manifest.
"""
from pathlib import Path
from collections import Counter, deque
import argparse
import itertools
import json
import math


def require(condition, message):
    if not condition:
        raise ValueError(message)


def compose(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def inverse(a):
    out = [0] * len(a)
    for i, j in enumerate(a):
        out[j] = i
    return tuple(out)


def closure(gens, n, bound):
    identity = tuple(range(n))
    gens = sorted(set(map(tuple, gens)))
    seen, todo = {identity}, [identity]
    for x in todo:
        for g in gens:
            y = compose(x, g)
            if y not in seen:
                seen.add(y)
                todo.append(y)
                require(len(todo) <= bound, "group closure exceeds declared bound")
    return seen


def automorphism(p, adj):
    return (sorted(p) == list(range(len(adj))) and
            all({p[w] for w in adj[v]} == set(adj[p[v]]) for v in range(len(adj))))


def refinement(adj, parts):
    while True:
        location = {v: i for i, cell in enumerate(parts) for v in cell}
        new = []
        for cell in parts:
            buckets = {}
            for v in cell:
                signature = tuple(sorted(Counter(location[w] for w in adj[v]).items()))
                buckets.setdefault(signature, []).append(v)
            new.extend(buckets[s] for s in sorted(buckets))
        if len(new) == len(parts):
            return new
        parts = new


def rooted_cycles(adj, vertex, length):
    def visit(path):
        if len(path) == length:
            return int(vertex in adj[path[-1]])
        return sum(visit(path + (w,)) for w in adj[path[-1]] if w not in path)
    total = visit((vertex,))
    require(total % 2 == 0, "cycle orientation pairing")
    return total // 2


def refinement_bound(adj, use_cycles=False):
    if use_cycles:
        buckets = {}
        for v in range(len(adj)):
            buckets.setdefault(rooted_cycles(adj, v, 5), []).append(v)
        parts = [buckets[k] for k in sorted(buckets)]
    else:
        parts = [list(range(len(adj)))]
    initial = [len(c) for c in parts]
    parts = refinement(adj, parts)
    choices = []
    while len(parts) < len(adj):
        cell = min((c for c in parts if len(c) > 1), key=lambda c: (len(c), c))
        v = min(cell)
        choices.append({"vertex": v, "cell_size": len(cell)})
        parts = refinement(adj, [part for c in parts for part in
                                ([[v], [w for w in c if w != v]] if c is cell else [c])])
    return math.prod(row["cell_size"] for row in choices), initial, choices


def distances(adj, start):
    d = {start: 0}
    todo = deque([start])
    while todo:
        v = todo.popleft()
        for w in adj[v]:
            if w not in d:
                d[w] = d[v] + 1
                todo.append(w)
    return d


def graph_stats(adj):
    n = len(adj)
    seen, components = set(), []
    girth = None
    diameter = 0
    for v in range(n):
        d = distances(adj, v)
        diameter = max(diameter, max(d.values(), default=0))
        if v not in seen:
            component = sorted(d)
            seen.update(component)
            components.append(component)
        # Every cycle has an edge off a rooted shortest-path tree. This usual
        # breadth-first scan minimizes its candidate length over all roots.
        parent = {v: None}
        todo = deque([v])
        while todo:
            x = todo.popleft()
            for y in adj[x]:
                if y not in parent:
                    parent[y] = x
                    todo.append(y)
                elif parent[x] != y and parent[y] != x:
                    candidate = d[x] + d[y] + 1
                    girth = candidate if girth is None else min(girth, candidate)
    return {"vertices": n, "edges": sum(map(len, adj)) // 2,
            "degrees": sorted(Counter(map(len, adj)).items()),
            "components": sorted(Counter(map(len, components)).items()),
            "girth": girth, "diameter": diameter if len(components) == 1 else None,
            "maximum_component_diameter": diameter}


def incidence_eccentricities(adj):
    n = len(adj)
    out = [set() for _ in range(n)]
    for v in range(n):
        for w in adj[v]:
            if v < w:
                e = len(out)
                out.append({v, w})
                out[v].add(e)
                out[w].add(e)
    eccentricities = []
    for v in range(len(out)):
        d = distances(out, v)
        require(len(d) == len(out), "incidence graph must be connected")
        eccentricities.append(max(d.values()))
    return [sorted(set(eccentricities[:n])), sorted(set(eccentricities[n:]))]


def alternating_factor(group, gens):
    n = len(next(iter(group)))
    identity = tuple(range(n))
    center = {x for x in group if all(compose(x, g) == compose(g, x) for g in gens)}
    commutators = {compose(compose(inverse(x), inverse(g)), compose(x, g))
                   for x in group for g in gens}
    derived = closure(commutators, n, 60)
    require(len(derived) == 60 and len(center) == 2, "A5/direct central factor orders")
    require(all({compose(compose(inverse(g), x), g) for x in derived} == derived
                for g in gens), "derived subgroup normality")
    involutions = {x for x in derived if x != identity and compose(x, x) == identity}
    kleins = set()
    for a in involutions:
        for b in involutions:
            if a != b and compose(a, b) == compose(b, a):
                kleins.add(frozenset((identity, a, b, compose(a, b))))
    require(len(kleins) == 5, "five Klein four subgroups")
    kleins = sorted(kleins, key=lambda s: sorted(s))
    lookup = {s: i for i, s in enumerate(kleins)}

    def action(x):
        xi = inverse(x)
        return tuple(lookup[frozenset(compose(compose(xi, a), x) for a in k)] for k in kleins)

    require(len({action(x) for x in derived}) == 60, "faithful degree-five A5 action")
    require(center & derived == {identity}, "central factor intersection")
    if len(group) == 120:
        return "C2 x A5"
    require(len(group) == 240, "expected S5 extension order")
    for u in group - center - derived:
        if compose(u, u) != identity:
            continue
        candidate = closure([*derived, u], n, 240)
        if (len(candidate) == 120 and candidate & center == {identity}
                and len({action(x) for x in candidate}) == 120):
            return "C2 x S5"
    raise ValueError("no certified S5 direct complement")


def large_kernel_lower(adj, gens):
    n = len(adj)
    triangles = []
    for a in range(n):
        for b in adj[a]:
            if a < b:
                for c in set(adj[a]) & set(adj[b]):
                    if b < c:
                        triangles.append((a, b, c))
    require(len(triangles) == 56, "56 triangles")
    require(sorted(v for t in triangles for v in t) == list(range(n)), "unique triangle at each vertex")
    owner = {v: i for i, t in enumerate(triangles) for v in t}
    neighbors = [set() for _ in triangles]
    for v in range(n):
        for w in adj[v]:
            if owner[v] != owner[w]:
                neighbors[owner[v]].add(owner[w])
    buckets = {}
    for i, row in enumerate(neighbors):
        buckets.setdefault(tuple(sorted(row)), []).append(i)
    require(len(buckets) == 28 and all(len(v) == 2 for v in buckets.values()), "28 paired triangles")
    blocks, flips = [], []
    for pair in buckets.values():
        left, right = [triangles[i] for i in pair]
        block = set(left + right)
        p = list(range(n))
        for v in left:
            matches = [w for w in right if set(adj[v]) - block == set(adj[w]) - block]
            require(len(matches) == 1, "unique matching between twin triangles")
            w = matches[0]
            p[v], p[w] = w, v
        require(automorphism(p, adj), "literal six-vertex swap is an automorphism")
        require(sum(i != j for i, j in enumerate(p)) == 6, "six-point support")
        flips.append(tuple(p))
        blocks.append(sorted(block))
    require(sorted(v for b in blocks for v in b) == list(range(n)), "disjoint independent flip supports")
    owner = {v: i for i, b in enumerate(blocks) for v in b}
    induced = []
    for p in gens:
        image = []
        for b in blocks:
            values = {owner[p[v]] for v in b}
            require(len(values) == 1, "generator preserves intrinsic six-point blocks")
            image.append(values.pop())
        induced.append(tuple(image))
    quotient = closure(induced, 28, 336)
    require(len(quotient) == 336, "exact quotient subgroup order336")
    return (2 ** 28) * len(quotient), {"independent_disjoint_flips": 28,
                                      "quotient_order": 336, "blocks": blocks,
                                      "flip_permutations": flips}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    inputs = json.loads((root / 'automorphism_witnesses.json').read_text())
    report = {}
    expected = {'q2_r0_moving': 12, 'q4_r0_union': 120, 'q5_r3_moving': 240,
                'q5_r4_moving': 120, 'q7_r3_moving': 90194313216, 'q9_r0_moving': 1440}
    for name, row in inputs.items():
        source = json.loads((root / row['source_graph']).read_text())
        es = source['edges'] + (source['fixed'] if row['kind'] == 'union' else [])
        vertices = sorted({v for e in es for v in e})
        require(vertices == row['vertices_from_absolute'], "exact removal of isolated vertices")
        index = {v: i for i, v in enumerate(vertices)}
        adj = [set() for _ in vertices]
        for a, b in es:
            a, b = index[a], index[b]
            require(a != b, "loop-free graph")
            adj[a].add(b)
            adj[b].add(a)
        require([sorted(a) for a in adj] == row['adjacency'], "actual graph binding")
        gens = list(map(tuple, row['automorphism_generators']))
        require(all(automorphism(p, adj) for p in gens), "actual adjacency preservation")
        upper, initial, chain = refinement_bound(adj, name == 'q4_r0_union')
        require(upper == expected[name], "full automorphism refinement bound")
        details = {}
        if name == 'q7_r3_moving':
            lower, details = large_kernel_lower(adj, gens)
        else:
            group = closure(gens, len(adj), expected[name])
            lower = len(group)
            if name in ('q4_r0_union', 'q5_r3_moving', 'q5_r4_moving'):
                details['group_structure'] = alternating_factor(group, gens)
            details['vertex_transitive'] = len({p[0] for p in group}) == len(adj)
            if name == 'q5_r3_moving':
                edge = next((a, b) for a in range(len(adj)) for b in adj[a])
                details['arc_transitive'] = len({(p[edge[0]], p[edge[1]]) for p in group}) == sum(map(len, adj))
                require(details['arc_transitive'], "source arc transitivity")
            if name in ('q5_r3_moving', 'q5_r4_moving'):
                require(details['vertex_transitive'], "source vertex transitivity")
        require(lower == upper, "matching lower and upper group orders")
        report[name] = dict(graph_stats(adj), full_automorphism_order=upper,
                            initial_refinement_cell_sizes=initial, refinement_chain=chain,
                            incidence_eccentricities=incidence_eccentricities(adj), **details)
    q7_expected = {
        0: (168, 84, [(1, 168)], [(2, 84)]),
        1: (0, 0, [], []),
        2: (168, 168, [(2, 168)], [(4, 42)]),
        3: (168, 336, [(4, 168)], [(168, 1)]),
        4: (252, 252, [(2, 252)], [(12, 21)]),
        5: (252, 210, [(1, 168), (3, 84)], [(6, 42)]),
        6: (252, 168, [(1, 168), (2, 84)], [(3, 84)]),
    }
    q7_rows = []
    for r, (nv, ne, degree, components) in q7_expected.items():
        row = json.loads((root / f'graph_q7_r{r}.json').read_text())
        vertices = sorted({v for e in row['edges'] for v in e})
        index = {v: i for i, v in enumerate(vertices)}
        adj = [set() for _ in vertices]
        for a, b in row['edges']:
            adj[index[a]].add(index[b])
            adj[index[b]].add(index[a])
        stats = graph_stats(adj)
        require((stats['vertices'], stats['edges'], stats['degrees'], stats['components'])
                == (nv, ne, degree, components), "complete q7 graph-class table")
        require(nv != 84, "no source84-vertex moving graph")
        q7_rows.append(dict(representative=r, **stats))
    report['q7_complete_marking_comparison'] = q7_rows
    q4 = json.loads((root / 'graph_q4_r0.json').read_text())
    adj = [set() for _ in range(q4['absolute'])]
    for a, b in q4['edges']:
        adj[a].add(b)
        adj[b].add(a)
    stats = graph_stats(adj)
    require(stats['components'] == [(2, 15), (5, 12)] and stats['degrees'] == [(1, 30), (2, 60)],
            "exact 15 edges and12 pentagons")
    require(stats['girth'] == 5, "five-cycles rather than other five-point components")
    report['q4_moving_disjoint_components'] = dict(stats, full_automorphism_order=
            2**15 * math.factorial(15) * 10**12 * math.factorial(12))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + '\n')
    print('PASS: six actual graphs, exact full automorphism orders, structural factors and distances')


if __name__ == '__main__':
    main()
