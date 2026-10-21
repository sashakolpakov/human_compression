#!/usr/bin/env python3
"""Exact small-model checks for the written two-stage rank-four argument.

The full first homology cover is represented by base vertices and vectors,
not enumerated. Boundary membership is checked for every base vertex; safe
translated paths are checked for specified fibers and all graph generators.
This is a finite diagnostic, not a proof of the quantified topological theorem.
"""
import argparse
import hashlib
import json
from pathlib import Path
import time

from phase211_surface_check import analyze


def require(value, message):
    if not value:
        raise ValueError(message)


def add(a, b, p):
    return tuple((x+y) % p for x, y in zip(a, b))


def sub(a, b, p):
    return tuple((x-y) % p for x, y in zip(a, b))


def scale(k, a, p):
    return tuple(k*x % p for x in a)


class Span:
    def __init__(self, p, width):
        self.p, self.width, self.rows = p, width, {}

    def reduce(self, vector):
        a = list(vector)
        for j, b in sorted(self.rows.items()):
            if a[j]:
                k = a[j]
                a = [(x-k*y) % self.p for x, y in zip(a, b)]
        return tuple(a)

    def insert(self, vector):
        a = self.reduce(vector)
        j = next((j for j, x in enumerate(a) if x), None)
        if j is None:
            return False
        a = scale(pow(a[j], -1, self.p), a, self.p)
        self.rows[j] = a
        return True

    def contains(self, vector):
        return not any(self.reduce(vector))


def next_prime(n):
    n += 1
    while any(n % d == 0 for d in range(2, int(n**0.5)+1)):
        n += 1
    return n


def run(model):
    data = analyze(model, details=True)
    adj, edges = data['Cayley_generator_edges'], data['edges']
    g = data['order']
    p = next_prime(4*g)
    emap = {(v, i): e for e, (a, b, i) in enumerate(edges) for v in [a, b]}

    def paths(root, colors):
        paths = {root: []}
        queue = [root]
        for v in queue:
            for i in colors:
                w = adj[v][i]
                if w not in paths:
                    paths[w] = paths[v]+[i]
                    queue.append(w)
        return paths

    base_paths = paths(0, range(4))
    tree = set()
    for v, word in base_paths.items():
        if word:
            tree.add(emap[v, word[-1]])
    cotree = sorted(set(range(len(edges)))-tree)
    positions = {e: i for i, e in enumerate(cotree)}
    raw_rows = []
    square_span = Span(p, len(cotree))
    for face in data['faces']:
        if face['colors'] == (1, 2) or face['colors'] == [1, 2]:
            continue
        v = min(face['vertices'])
        row = [0]*len(cotree)
        for i in list(face['colors'])*2:
            w = adj[v][i]
            e = emap[v, i]
            if e in positions:
                row[positions[e]] += 1 if v < w else -1
            v = w
        row = tuple(x % p for x in row)
        square_span.insert(row)
        raw_rows.append(row)
    free = sorted(set(range(len(cotree)))-set(square_span.rows))
    d = len(free)
    require(d == 1+g//4, 'raw homology dimension')
    zero = (0,)*d
    edgevolt = [zero]*len(edges)
    for e, j in positions.items():
        row = tuple(int(k == j) for k in range(len(cotree)))
        reduced = square_span.reduce(row)
        edgevolt[e] = tuple(reduced[k] for k in free)

    def step(v, value, i):
        w = adj[v][i]
        vector = edgevolt[emap[v, i]]
        return w, add(value, scale(1 if v < w else -1, vector, p), p)

    def walk(v, value, word, safe=False):
        if safe:
            require(allowed(v, value), 'forbidden initial vertex')
        for i in word:
            v, value = step(v, value, i)
            if safe:
                require(allowed(v, value), 'translated path hits chosen end')
        return v, value

    # Independent literal checks of all square voltages and involution edges.
    for v in range(g):
        for i in range(4):
            require(walk(v, zero, [i, i]) == (v, zero), 'involution voltage')
        for i, j in [(0, 2), (0, 3), (1, 3)]:
            require(walk(v, zero, [i, j, i, j]) == (v, zero), 'square voltage')

    def fiber(colors):
        pp = paths(0, colors)
        centers = {v: walk(0, zero, word)[1] for v, word in pp.items()}
        space = Span(p, d)
        for v in pp:
            for i in colors:
                w, val = step(v, centers[v], i)
                space.insert(sub(val, centers[w], p))
        return pp, centers, space

    aa, ca, va = fiber([0, 1, 2])
    bb, cb, vb = fiber([1, 2, 3])
    require(adj[0][0] not in bb and adj[0][3] not in aa, 'extreme independence')
    cc = paths(0, [1, 2])
    q = len(cc)//2
    middle = [1, 2]*q
    boundary = [walk(v, zero, middle)[1] for v in range(g)]
    for v in range(g):
        require(va.contains(boundary[v]) == (v in aa), 'boundary detects A')
        require(vb.contains(boundary[v]) == (v in bb), 'boundary detects B')
        require(walk(v, zero, middle)[0] == v, 'boundary closure')

    def allowed(v, val):
        return not ((v in aa and va.contains(sub(val, ca[v], p))) or
                    (v in bb and vb.contains(sub(val, cb[v], p))))

    outside = set(range(g))-(aa.keys() | bb.keys())
    require(outside, 'nonempty exterior base')
    h = min(outside)
    hpaths = paths(h, range(4))
    records = []
    tested_edges = 0

    def shift(v, val, k):
        require(v in outside, 'shift base must be exterior')
        cur = v
        for i in middle:
            cur = adj[cur][i]
            require(cur in outside, 'safe middle loop')
        return add(val, scale(k, boundary[v], p), p)

    def avoid(v, value, word):
        nonlocal tested_edges
        require(v in outside, 'avoidance initial base')
        u = boundary[v]
        bad = set()
        cur, val = v, value
        for index in range(len(word)+1):
            for centers, space in [(ca, va), (cb, vb)]:
                if cur not in centers:
                    continue
                a = space.reduce(sub(val, centers[cur], p))
                b = space.reduce(u)
                j = next((j for j, x in enumerate(b) if x), None)
                require(j is not None, 'transverse boundary direction')
                k = -a[j]*pow(b[j], -1, p) % p
                if not any(add(a, scale(k, b, p), p)):
                    bad.add(k)
            if index < len(word):
                cur, val = step(cur, val, word[index])
        require(len(bad) <= 2*(len(word)+1) < p, 'strict avoidance bound')
        k = next(k for k in range(p) if k not in bad)
        endpoint, result = walk(v, shift(v, value, k), word, True)
        expected = add(val, scale(k, u, p), p)
        require(result == expected, 'deck translation commutes with lifting')
        tested_edges += len(word)
        records.append([v, list(value), word, k, len(bad)])
        return endpoint, result, k

    # Each exterior base vertex reaches a common fiber from three coordinates.
    samples = [zero, (1,)*d, tuple((j*j+3*j+7) % p for j in range(d))]
    for v in sorted(outside):
        for value in samples:
            endpoint, _, _ = avoid(v, value, list(reversed(hpaths[v])))
            require(endpoint == h, 'common fiber reached')

    # Every fundamental graph loop acts inside the exterior from each sample.
    cycles = []
    graph_classes = Span(p, d)
    odd = None
    htree = {emap[v, word[-1]] for v, word in hpaths.items() if word}
    for e, (v, w, color) in enumerate(edges):
        if e in htree:
            continue
        word = hpaths[v]+[color]+list(reversed(hpaths[w]))
        require(len(word) <= 2*g-1, 'tree loop length')
        endpoint, displacement = walk(h, zero, word)
        require(endpoint == h, 'graph loop closure')
        graph_classes.insert(displacement)
        cycles.append(word)
        if len(word) % 2:
            odd = word
        for value in samples:
            endpoint, result, k = avoid(h, value, word)
            result = shift(h, result, -k)
            require(endpoint == h and result == add(value, displacement, p),
                    'safe loop realizes correct deck vector')
    require(len(graph_classes.rows) == d, 'graph loop classes generate homology')

    # Literal endpoint escape for every base vertex and supplied coordinates.
    access_count = 0
    for v in range(g):
        for value in samples:
            if not allowed(v, value) or v in outside:
                continue
            if v in aa and v in bb:
                word = [0, 3]
            elif v in aa:
                word = [3]
            else:
                require(v in bb, 'access cases exhaustive')
                word = [0]
            endpoint, _ = walk(v, value, word, True)
            require(endpoint in outside, 'endpoint escape')
            access_count += 1

    odd_report = None
    require((odd is None) == data['orientable'], 'graph and surface orientation')
    if odd is not None:
        value = zero
        choices = []
        for _ in range(p):
            endpoint, result, k = avoid(h, value, odd)
            require(endpoint == h, 'odd path returns to base fiber')
            value = shift(h, result, -k)
            choices.append(k)
        require(value == zero and (p*len(odd)) % 2 == 1,
                'closed orientation-reversing exterior walk')
        odd_report = {'base_loop': odd, 'repetitions': p,
                      'permitted_scalar_counts': {str(k): choices.count(k) for k in sorted(set(choices))},
                      'choices_sha256': hashlib.sha256(bytes(str(choices), 'ascii')).hexdigest(),
                      'closed': True, 'parity': 1}
    encoded = json.dumps(records, separators=(',', ':')).encode()
    return {'name': model['name'], 'order': g, 'prime': p,
            'dimension': d, 'end_space_dimensions': [len(va.rows), len(vb.rows)],
            'boundary_membership_tests': 2*g,
            'base_top_complement_components': len(data['pairs'][0]['complement_components']),
            'base_odd_surface_criterion': data['all_odd_prime_criterion'],
            'orientable': data['orientable'], 'exterior_base_vertices': len(outside),
            'spanning_tree_loops': len(cycles), 'endpoint_escape_tests': access_count,
            'translated_paths': len(records), 'checked_path_edges': tested_edges,
            'path_records_sha256': hashlib.sha256(encoded).hexdigest(),
            'odd_exterior_loop': odd_report, 'status': 'PASS'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--models', type=Path, default=Path(__file__).with_name('phase256_voltage_models.json'))
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    start = time.monotonic()
    models = json.loads(args.models.read_text())
    results = []
    for model in models:
        row = run(model)
        results.append(row)
        print(json.dumps({k: row[k] for k in ['name', 'order', 'prime', 'orientable', 'translated_paths', 'status']}), flush=True)
    report = {'status': 'PASS', 'models_sha256': hashlib.sha256(args.models.read_bytes()).hexdigest(),
              'seconds': round(time.monotonic()-start, 3), 'results': results,
              'scope': 'Exact base homology and symbolic finite-field paths on five specified marked groups. Neither a full enumeration of their homology covers nor the general surface theorem is certified by these tests.'}
    args.out.write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()
