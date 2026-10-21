#!/usr/bin/env python3
"""Optional integer-coordinate checks, not premises of the uniform proof."""
import argparse
import itertools
import json
from pathlib import Path


def need(condition, message):
    if not condition:
        raise ValueError(message)


def identity(n):
    return (tuple(range(n)), (1,) * n, (0,) * n)


def compose(f, g):
    p, s, b = f
    q, t, c = g
    return (tuple(q[p[i]] for i in range(len(p))),
            tuple(s[i] * t[p[i]] for i in range(len(p))),
            tuple(b[i] + s[i] * c[p[i]] for i in range(len(p))))


def swap(n, i, j):
    p = list(range(n))
    p[i], p[j] = p[j], p[i]
    return (tuple(p), (1,) * n, (0,) * n)


def reflection(n, i, offset=0):
    s, b = [1] * n, [0] * n
    s[i], b[i] = -1, offset
    return (tuple(range(n)), tuple(s), tuple(b))


def order(f):
    e = identity(len(f[0]))
    g = e
    for k in range(1, 25):
        g = compose(g, f)
        if g == e:
            return k
    raise ValueError('unexpected affine order >24')


def marking(n, a, b):
    g = [reflection(n, 0, 1)]
    g += [swap(n, i, i + 1) for i in range(n - 1)]
    g += [reflection(n, n - 1)]
    if a:
        g[0] = compose(compose(g[0], g[1]), g[0])
    if a == 2:
        g[0] = compose(compose(g[0], g[2]), g[0])
    if b:
        g[n] = compose(compose(g[n], g[n - 1]), g[n])
    if b == 2:
        g[n] = compose(compose(g[n], g[n - 2]), g[n])
    return g


def expected(n, a, b):
    edges = {(i, i + 1): 3 for i in range(1, n - 1)}
    if a == 0:
        edges[0, 1] = 4
    elif a == 1:
        edges[0, 2] = 3
    else:
        edges.update({(0, 1): 3, (0, 2): 3, (0, 3): 4 if n == 3 else 3})
    if b == 0:
        edges[n - 1, n] = 4
    elif b == 1:
        edges[n - 2, n] = 3
    else:
        edges.update({(n - 3, n): 3, (n - 2, n): 3, (n - 1, n): 3})
    if (n, a, b) in [(3, 1, 1), (4, 2, 1), (5, 2, 2)]:
        edges[0, n] = 3
    return edges


def in_lattice(v, n, k, s, even=False):
    if any(x % s for x in v):
        return False
    u = [x // s for x in v]
    inside = k == 1 or (k == 2 and sum(u) % 2 == 0) or (
        k == n and len({x % 2 for x in u}) == 1)
    return inside and (not even or sum(v) % 2 == 0)


def validate_diagram(gens, target):
    actual = {(i, j): order(compose(gens[i], gens[j]))
              for i in range(len(gens)) for j in range(i + 1, len(gens))}
    need({ij: m for ij, m in actual.items() if m > 2} == target,
         'diagram mismatch')
    return actual


def rejects(action):
    try:
        action()
    except ValueError:
        return True
    return False


def run():
    diagrams = []
    for n in range(3, 10):
        states = [(0, 0), (1, 0), (1, 1), (2, 0)]
        if n >= 4:
            states.append((2, 1))
        if n >= 5:
            states.append((2, 2))
        for a, b in states:
            gens = marking(n, a, b)
            need(all(order(x) == 2 for x in gens), 'noninvolution')
            target = expected(n, a, b)
            actual = validate_diagram(gens, target)
            for (i, j), m in actual.items():
                f = compose(gens[i], gens[j])
                linear = (f[0], f[1], (0,) * n)
                need(order(linear) == m, 'linear-order lower bound failed')
            leaves = [i for i in range(n + 1)
                      if sum(i in ij for ij in target) == 1]
            diagrams.append({'n': n, 'state': [a, b], 'edges': [
                [i, j, m] for (i, j), m in sorted(target.items())], 'leaves': leaves})
    lattice_cases = []
    for n in range(3, 7):
        roots = []
        for i, j in itertools.combinations(range(n), 2):
            for u, v in itertools.product([-1, 1], repeat=2):
                r = [0] * n
                r[i], r[j] = u, v
                roots.append(tuple(r))
        for k in [1, 2, n]:
            for s in range(2, 6):
                v = [2] + [0] * (n - 1)
                need(in_lattice(v, n, k, s) == ((k, s) == (1, 2)),
                     'unit-grid exception')
                root_collision = any(in_lattice([x - y for x, y in zip(r, t)],
                                                n, k, s, True)
                                     for r, t in itertools.combinations(roots, 2))
                need(root_collision == ((k, s) in [(1, 2), (2, 2)]),
                     'root-grid exception')
                lattice_cases.append({'n': n, 'k': k, 's': s,
                                      'root_collision': root_collision})
    controls = []
    wrong = expected(5, 2, 2)
    del wrong[0, 5]
    need(rejects(lambda: validate_diagram(marking(5, 2, 2), wrong)),
         'missing overlap control')
    controls.append('deleting n5 terminal overlap bond rejected')
    wrong = expected(3, 2, 0)
    wrong[0, 3] = 3
    need(rejects(lambda: validate_diagram(marking(3, 2, 0), wrong)),
         'small rank label control')
    controls.append('changing n3 overlap bond4 to3 rejected')
    need(rejects(lambda: need(not in_lattice([2, 2, 0], 3, 2, 2, True),
                              'incorrectly asserted no root coincidence')),
         'small period control')
    controls.append('omitting k2s2 root coincidence rejected')
    return {'status': 'PASS', 'role': 'optional coordinate validation only',
            'uniform_proof_premise': False, 'diagrams': diagrams,
            'lattice_cases': lattice_cases, 'controls': controls}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    report = run()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'diagrams': len(report['diagrams']),
                      'lattice_cases': len(report['lattice_cases']),
                      'controls': len(report['controls'])}))
