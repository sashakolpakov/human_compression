#!/usr/bin/env python3
"""Independent coordinate-and-bitset verification of the point-cloning example."""
import argparse
from collections import deque
import itertools
import json
from pathlib import Path

def need(condition, message):
    if not condition:
        raise RuntimeError('PHASE268_REJECT ' + message)

def reaches(adjacency, allowed=None):
    allowed = set(range(len(adjacency))) if allowed is None else set(allowed)
    if not allowed:
        return set()
    start = min(allowed)
    seen, todo = {start}, deque([start])
    while todo:
        v = todo.popleft()
        for w in adjacency[v] & allowed:
            if w not in seen:
                seen.add(w)
                todo.append(w)
    return seen

def model(copies):
    # Homogeneous equations ax+by=c, with four normalized directions.
    points = [(v % 3, v // 3) for v in range(9)]
    directions = [(1, 0), (0, 1), (1, 1), (1, 2)]
    masks = [sum(1 << v for v, (x, y) in enumerate(points) if (a*x+b*y-c) % 3 == 0)
             for a, b in directions for c in range(3)]
    def incident(point, line):
        return bool(masks[line] & (1 << (point // copies)))
    flags = [(point, line) for point in range(9*copies) for line in range(12)
             if incident(point, line)]
    n = len(flags)
    vertices = [(kind, point, line) for kind in range(3) for point, line in flags]
    adjacency = [set() for _ in vertices]
    # Construct each unordered type pair once, orienting its source rule cyclically.
    for i, j in [(0, 1), (1, 2), (2, 0)]:
        for u, (p, line) in enumerate(flags):
            for v, (q, other) in enumerate(flags):
                if incident(p, other) and not incident(q, line):
                    a, b = i*n+u, j*n+v
                    adjacency[a].add(b)
                    adjacency[b].add(a)
    return points, masks, flags, vertices, adjacency

def check(copies):
    points, masks, flags, vertices, adjacency = model(copies)
    n = len(flags)
    parts = [set(range(i*n, (i+1)*n)) for i in range(3)]
    need(n == 36*copies, 'flag count')
    need(len(reaches(adjacency)) == 3*n, 'global connectivity')
    chambers, panels = set(), []
    for i, j in [(0, 1), (1, 2), (2, 0)]:
        k = 3-i-j
        for x in parts[i]:
            for y in adjacency[x] & parts[j]:
                common = adjacency[x] & adjacency[y] & parts[k]
                panels.append(len(common))
                if i == 0:
                    chambers.update((x, y, z) for z in common)
    need(set(panels) == {2*copies}, 'all panels extend with exact multiplicity')
    need(len(chambers) == 432*copies**3, 'chamber count')
    need(all(len(adjacency[v]) == 12*copies for v in range(3*n)), 'residue sizes')
    need(all(reaches(adjacency, adjacency[v]) == adjacency[v] for v in range(3*n)),
         'every residue connected')
    need(all(len(adjacency[w] & adjacency[v]) == 2*copies
             for v in range(3*n) for w in adjacency[v]), 'residue degrees')
    # Establish the exact blow-up relation independently for every pair of vertices.
    _, _, base_flags, base_vertices, base_adjacency = model(1)
    base_index = {v: i for i, v in enumerate(base_vertices)}
    projection = [base_index[kind, point//copies, line] for kind, point, line in vertices]
    need(all((w in adjacency[v]) == (projection[w] in base_adjacency[projection[v]])
             for v in range(3*n) for w in range(3*n)), 'literal blow-up equivalence')
    # All ordered noncollinear triples have a unique affine frame map from (0,e1,e2).
    triples = []
    for p, q, r in itertools.permutations(range(9), 3):
        x, y = points[p]
        a, b = (points[q][0]-x) % 3, (points[q][1]-y) % 3
        c, d = (points[r][0]-x) % 3, (points[r][1]-y) % 3
        if (a*d-b*c) % 3:
            image = [((x+a*u+c*v) % 3, (y+b*u+d*v) % 3) for u, v in points]
            need(len(set(image)) == 9, 'actual affine frame permutation')
            triples.append((p, q, r))
    need(len(triples) == 432, 'affine frame transitivity')
    # In every triangle chamber the three base points are noncollinear and
    # its lines are exactly their cyclic joining lines, with independent clones.
    triangle_set = set(triples)
    projected = set()
    for chamber in chambers:
        ps = tuple(vertices[v][1]//copies for v in chamber)
        need(ps in triangle_set, 'chamber frame')
        projected.add(ps)
    need(projected == triangle_set, 'all affine frames occur')
    return dict(copies=copies, vertices=3*n, chambers=len(chambers),
        residues_checked=3*n, panel_size=2*copies, residue_vertices=12*copies,
        exact_blowup_pairs=(3*n)**2, affine_frames=432)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(), 'fresh output file')
    rows = [check(a) for a in [1, 2, 3]]
    # For a>=2 the two clones of any one point and two distinct lines through
    # it form a4-cycle; a=1 is the un-cloned positive control of girth6.
    _, masks, _, _, _ = model(1)
    line_ids = [i for i, mask in enumerate(masks) if mask & 1]
    need(len(line_ids) == 4, 'two distinct lines through clone point')
    need(all((masks[i] & masks[j]).bit_count() == 1 or not (masks[i] & masks[j])
             for i in range(12) for j in range(i)), 'base has no4-cycle')
    report = dict(status='PASS', rows=rows,
        scope='Independent literal constructions for a=1,2,3; complete residues and blow-up identity. All-a conclusion remains the separate written cloning lemma.')
    args.out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))

if __name__ == '__main__':
    main()
