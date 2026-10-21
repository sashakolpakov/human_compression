#!/usr/bin/env python3
"""Elementary exhaustive certificate; no graph/group package is imported."""
import argparse
import collections
import hashlib
import json
import math
from pathlib import Path


class Rejected(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Rejected(message)


def refinement(adj, star):
    colors = [0] * len(adj)
    for i, v in enumerate(star):
        colors[v] = i + 1
    counts = [len(set(colors))]
    while True:
        signatures = [(colors[v], tuple(sorted(colors[w] for w in adj[v])))
                      for v in range(len(adj))]
        dictionary = {s: i for i, s in enumerate(sorted(set(signatures)))}
        new = [dictionary[s] for s in signatures]
        counts.append(len(dictionary))
        if len(dictionary) == len(set(colors)):
            return new, counts
        colors = new


def group_closure(generators, n, upper):
    identity = tuple(range(n))
    seen = {identity}
    todo = collections.deque([identity])
    while todo:
        p = todo.popleft()
        for g in generators:
            q = tuple(g[p[v]] for v in range(n))
            if q not in seen:
                seen.add(q)
                require(len(seen) <= upper, 'group exceeds certified upper bound')
                todo.append(q)
    return seen


def permutation_order(p):
    seen = set()
    order = 1
    for v in range(len(p)):
        if v in seen:
            continue
        w, length = v, 0
        while w not in seen:
            seen.add(w)
            length += 1
            w = p[w]
        order = math.lcm(order, length)
    return order


def inspect(data, expected=None, require_nonsplit=True):
    adj = [tuple(v - 1 for v in row) for row in data['adjacency']]
    n = len(adj)
    vertices = set(range(n))
    degree = len(adj[0])
    require(degree >= 2, 'minimum degree')
    for v, row in enumerate(adj):
        require(len(row) == degree and len(set(row)) == degree, 'simple regular graph')
        require(v not in row and set(row) <= vertices, 'valid loop-free adjacency')
        require(all(v in adj[w] for w in row), 'symmetric adjacency')
    sides = {0: 0}
    todo = collections.deque([0])
    while todo:
        v = todo.popleft()
        for w in adj[v]:
            if w not in sides:
                sides[w] = 1 - sides[v]
                todo.append(w)
            require(sides[w] != sides[v], 'bipartite')
    require(len(sides) == n, 'connected')
    edges = {tuple(sorted((v, w))) for v in vertices for w in adj[v]}
    part = {v for v in vertices if sides[v] == 0}
    require(len(part) * 2 == n and len(part) != len(edges), 'part and edge sizes')
    star = [v - 1 for v in data['distinguished_star']]
    require(len(star) == degree + 1 and set(star[1:]) == set(adj[star[0]]), 'full star')
    colors, counts = refinement(adj, star)
    require(len(set(colors)) == n, 'star refinement is not discrete')
    # Every automorphism is determined by its images on this ordered star.
    upper = n * math.factorial(degree)
    generators = [tuple(v - 1 for v in row) for row in data['generators']]
    for g in generators:
        require(len(g) == n and set(g) == vertices, 'generator is not permutation')
        require(all({g[w] for w in adj[v]} == set(adj[g[v]]) for v in vertices),
                'generator does not preserve graph')
    group = group_closure(generators, n, upper)
    require(len(group) == upper, 'generated group does not attain full upper bound')
    inside, outside = [], []
    for g in group:
        image = {g[v] for v in part}
        require(image == part or image == vertices - part, 'part transport')
        (inside if image == part else outside).append(g)
    require(len(inside) == len(outside), 'part action is not onto C2')
    edge = min(edges)
    edge_orbit = {tuple(sorted((g[edge[0]], g[edge[1]]))) for g in inside}
    require(edge_orbit == edges, 'part-preserving subgroup is not edge-transitive')
    orders = dict(sorted(collections.Counter(permutation_order(g) for g in outside).items()))
    if require_nonsplit:
        require(1 not in orders and 2 not in orders, 'part-exchanging involution')
    result = {
        'vertices': n, 'edges': len(edges), 'degree': degree,
        'part_sizes': [len(part), n - len(part)],
        'refinement_cell_counts': counts,
        'full_automorphism_upper_bound': upper,
        'generated_group_order': len(group),
        'generator_orders': [permutation_order(g) for g in generators],
        'part_preserving_order': len(inside),
        'part_preserving_edge_orbit_size': len(edge_orbit),
        'exchanging_coset_order_distribution': orders,
        'fullness': 'discrete star refinement upper bound attained by explicit subgroup',
    }
    if expected is not None:
        require(result['vertices'] == expected['vertices'], 'expected vertex count')
        require(result['edges'] == expected['edges'], 'expected edge count')
        require(result['generated_group_order'] == expected['group_order'], 'expected full order')
        require(orders == expected['orders'], 'expected exchanging order distribution')
    return result


def controls(data):
    import copy
    cases = []
    def rejection(name, changed, intended):
        try:
            inspect(changed)
        except Rejected as error:
            require(intended in str(error), 'control rejected at wrong interface: ' + name)
            cases.append({'name': name, 'rejected_at': str(error)})
        else:
            raise Rejected('negative control was accepted: ' + name)
    d = copy.deepcopy(data)
    d['adjacency'][0][0] = 1
    rejection('loop in adjacency', d, 'loop-free')
    d = copy.deepcopy(data)
    d['generators'][0][0] = d['generators'][0][1]
    rejection('nonbijective generator', d, 'not permutation')
    d = copy.deepcopy(data)
    g = list(range(1, len(d['adjacency']) + 1))
    g[0], g[1] = g[1], g[0]
    d['generators'] = [g]
    rejection('nongraph permutation', d, 'does not preserve graph')
    d = copy.deepcopy(data)
    d['generators'] = [list(range(1, len(d['adjacency']) + 1))]
    rejection('proper subgroup substituted for full group', d, 'does not attain')
    d = copy.deepcopy(data)
    d['distinguished_star'] = [1]
    rejection('incomplete star bound', d, 'full star')
    # This connected bipartite edge-transitive graph passes every preceding
    # general interface, including the elementary full-group certificate.
    d = {'adjacency': [[(v - 1) % 6 + 1, (v + 1) % 6 + 1] for v in range(6)],
         'generators': [[(v + 1) % 6 + 1 for v in range(6)],
                        [(-v) % 6 + 1 for v in range(6)]],
         'distinguished_star': [1, 6, 2]}
    rejection('C6 swapping involutions', d, 'part-exchanging involution')
    # Even the actual full star must be distinguished pointwise for the upper bound.
    adj = [tuple(v - 1 for v in row) for row in data['adjacency']]
    colors, _ = refinement(adj, [0])
    require(len(set(colors)) < len(adj), 'root-only weakening unexpectedly discrete')
    cases.append({'name': 'root-only refinement weakening', 'rejected_at': 'nondiscrete partition'})
    return cases


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=Path, default=Path(__file__).with_name('graph.json'))
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    raw = args.data.read_bytes()
    data = json.loads(raw)
    result = inspect(data, {'vertices': 896, 'edges': 1344, 'group_order': 5376,
                           'orders': {4: 1024, 12: 896, 28: 768}})
    result['controls'] = controls(data)
    result['data_sha256'] = hashlib.sha256(raw).hexdigest()
    result['checker_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result['status'] = 'PASS'
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
