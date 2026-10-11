#!/usr/bin/env python3
"""Independent small graph checks, using adjacency backtracking and no GAP code.
This is bounded validation of the delicate local cases, not a uniform proof.
"""
import json
import argparse
from pathlib import Path


def ensure(b, text):
    if not b:
        raise ValueError(text)


def automorphisms(n, edges):
    adjacency = [set() for _ in range(n)]
    for u, v in edges:
        ensure(u != v and 0 <= u < n and 0 <= v < n, 'simple edge')
        adjacency[u].add(v)
        adjacency[v].add(u)
    signature = [(len(adjacency[u]), sorted(len(adjacency[v]) for v in adjacency[u])) for u in range(n)]
    images = [-1] * n
    used = set()
    result = []
    def go():
        if len(used) == n:
            result.append(tuple(images))
            return
        candidates = {}
        for u in range(n):
            if images[u] != -1:
                continue
            candidates[u] = [v for v in range(n) if v not in used and signature[v] == signature[u]
                and all((w in adjacency[u]) == (images[w] in adjacency[v])
                        for w in range(n) if images[w] != -1)]
        u = min(candidates, key=lambda x: (len(candidates[x]), x))
        for v in candidates[u]:
            images[u] = v
            used.add(v)
            go()
            used.remove(v)
            images[u] = -1
    go()
    # Independently check every output on the complete adjacency matrix.
    for p in result:
        ensure(len(set(p)) == n, 'bijection')
        ensure(all((v in adjacency[u]) == (p[v] in adjacency[p[u]])
                   for u in range(n) for v in range(n)), 'adjacency preservation')
    return result


def pair(colors, edges):
    autos = automorphisms(len(colors), edges)
    correlations, kernel = [], []
    for p in autos:
        image_classes = {}
        for i, c in enumerate(colors):
            image_classes.setdefault(c, set()).add(colors[p[i]])
        if all(len(a) == 1 for a in image_classes.values()) and len(set(next(iter(a)) for a in image_classes.values())) == len(image_classes):
            correlations.append(p)
            if all(colors[p[i]] == c for i, c in enumerate(colors)):
                kernel.append(p)
    return {'vertices': len(colors), 'uncolored_order': len(autos),
            'correlation_order': len(correlations), 'kernel_order': len(kernel)}, correlations, kernel


def hexagon(tips):
    edges = [(i, (i+1) % 6) for i in range(6)]
    for k, i in enumerate(tips):
        edges.extend([(6+k, i), (6+k, (i+1) % 6)])
    return [i % 2 for i in range(6)] + [2]*len(tips), edges


def run():
    out = {}
    for name, tips, expected in [('three_tips', [0,2,4], (6,3)), ('all_tips', list(range(6)), (12,6))]:
        colors, edges = hexagon(tips)
        data, _, kernel = pair(colors, edges)
        ensure((data['correlation_order'], data['kernel_order']) == expected, name)
        if name == 'all_tips':
            reflection = tuple([(-i)%6 for i in range(6)] + [6+(-i-1)%6 for i in range(6)])
            ensure(reflection in kernel and reflection != tuple(range(12)), 'actual nonidentity color-preserving reflection')
            ensure(all(reflection[reflection[i]] == i for i in range(12)), 'order two')
            data['reflection'] = list(reflection)
        out[name] = data
    # Independent literal M=1 isolated-vertex gadget, w=7, u_i=i.
    edges = [(i,i+1) for i in range(6)] + [(6,1),(5,2),(7,0),(7,2)]
    colors = [1 if i%2 == 0 else 2 for i in range(7)] + [0]
    data, _, _ = pair(colors, edges)
    ensure((data['correlation_order'], data['kernel_order']) == (1,1), 'M=1 isolated rigidity')
    out['isolated_M1'] = data
    colors, edges = [2,0,1,2], [(0,1),(1,2),(2,3)]
    data, _, _ = pair(colors, edges)
    ensure((data['correlation_order'], data['kernel_order']) == (2,1), 'recursive n=2 pair')
    data['degrees'] = [sum(i in e for e in edges) for i in range(4)]
    ensure(data['degrees'] == [1,2,2,1], 'recursive base has leaves')
    out['recursive_n2'] = data
    controls = []
    # Deliberately false interpretations must be rejected, not silently normalized.
    for name, false_claim in [('printed C3 kernel', out['all_tips']['kernel_order'] == 3),
                              ('degree-two recursive base', min(out['recursive_n2']['degrees']) >= 2),
                              ('nontrivial isolated rigidity kernel', out['isolated_M1']['kernel_order'] > 1)]:
        try:
            ensure(false_claim, name)
        except ValueError:
            controls.append({'name': name, 'rejected': True})
        else:
            raise ValueError('control unexpectedly passed: '+name)
    return {'status': 'PASS', 'algorithm': 'complete degree-refined adjacency backtracking; no author/GAP code imported',
            'models': out, 'controls': controls, 'uniform_proof': False}

if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path);a=p.parse_args()
    result=run();text=json.dumps(result,indent=2)+'\n'
    if a.out:
        ensure(not a.out.exists(), 'fresh report path required');a.out.write_text(text)
    else: print(text,end='')
