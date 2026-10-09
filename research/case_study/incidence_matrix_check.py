"""Exact integer checks of the flag-matrix and Kneser residue derivations.

Uses NumPy only for integer matrix multiplication, not floating-point spectra.
This checks small explicit instances; it is not the proof for all parameters.
"""
from collections import deque
from itertools import combinations, product
from pathlib import Path
import json
import math
import numpy as np

ROOT = Path(__file__).resolve().parent


def affine_plane(q):
    points = list(product(range(q), repeat=2))
    lines = [{i for i, (x, y) in enumerate(points) if x == a} for a in range(q)]
    lines += [{i for i, (x, y) in enumerate(points) if (y - m*x-b) % q == 0}
              for m, b in product(range(q), repeat=2)]
    return points, lines


def projective_plane(q):
    points = [(1, x, y) for x, y in product(range(q), repeat=2)]
    points += [(0, 1, x) for x in range(q)] + [(0, 0, 1)]
    lines = [{i for i, x in enumerate(points)
              if sum(a*b for a, b in zip(c, x)) % q == 0} for c in points]
    return points, lines


def connected(adj):
    seen = {0}
    queue = deque([0])
    while queue:
        for v in adj[queue.popleft()]:
            if v not in seen:
                seen.add(v)
                queue.append(v)
    return len(seen) == len(adj)


def check_flags(name, q, constructor):
    points, lines = constructor(q)
    flags = [(p, L) for L, line in enumerate(lines) for p in sorted(line)]
    k = len(lines[0])
    r = sum(0 in line for line in lines)
    assert all(len(line) == k for line in lines)
    assert all(sum(p in line for line in lines) == r for p in range(len(points)))
    m = len(flags)
    A = np.array([[int(p == t) for t, U in flags] for p, L in flags], dtype=np.int64)
    B = np.array([[int(L == U) for t, U in flags] for p, L in flags], dtype=np.int64)
    eye = np.eye(m, dtype=np.int64)
    D = (A-eye) @ (B-eye)
    direct = np.array([[int(p in lines[U] and L != U and p != t)
                        for t, U in flags] for p, L in flags], dtype=np.int64)
    assert np.array_equal(D, direct)
    out, inc = D @ D.T, D.T @ D
    off = ~np.eye(m, dtype=bool)
    alpha, beta = (r-2)*(k-1), (k-2)*(r-1)
    assert int(out[off].max()) == alpha and int(inc[off].max()) == beta
    assert np.array_equal(((out == alpha) & off).astype(np.int64), A-eye)
    assert np.array_equal(((inc == beta) & off).astype(np.int64), B-eye)
    assert set(map(int, out[(A == 0)])) <= {0, k-2}
    assert set(map(int, inc[(B == 0)])) <= {0, r-2}
    # Compare the actual triangle residue to the deleted-pencil model.
    p, L = flags[0]
    next_flags = [j for j in range(m) if D[0, j]]
    prev_flags = [j for j in range(m) if D[j, 0]]
    assert {flags[j][0] for j in next_flags} == set(range(len(points))) - lines[L]
    assert len(next_flags) == len({flags[j][0] for j in next_flags})
    assert {(flags[j][0], flags[j][1]) for j in prev_flags} == {
        (a, M) for a in lines[L] - {p} for M, line in enumerate(lines)
        if M != L and a in line}
    adj = [[] for _ in range(len(next_flags) + len(prev_flags))]
    for a, j in enumerate(next_flags):
        for b, h in enumerate(prev_flags):
            predicted = flags[j][0] in lines[flags[h][1]]
            assert bool(D[j, h]) == predicted
            if predicted:
                adj[a].append(len(next_flags)+b)
                adj[len(next_flags)+b].append(a)
    assert connected(adj)
    return dict(structure=name, q=q, points=len(points), lines=len(lines), flags=m,
                k=k, r=r, point_recovery_value=alpha, line_recovery_value=beta,
                triangle_residue_vertices=len(adj), triangle_residue_connected=True)


def check_kneser(n, k):
    sets = list(map(frozenset, combinations(range(n), k)))
    m = len(sets)
    graph = [[m+j for j, B in enumerate(sets) if not A & B] for A in sets]
    graph += [[j for j, B in enumerate(sets) if not A & B] for A in sets]
    s = n-2*k
    maxdist = 0
    for i, A in enumerate(sets):
        dist = [-1]*(2*m)
        dist[i] = 0
        queue = deque([i])
        while queue:
            x = queue.popleft()
            for y in graph[x]:
                if dist[y] < 0:
                    dist[y] = dist[x]+1
                    queue.append(y)
        for j, B in enumerate(sets):
            c = len(A & B)
            assert dist[j] == 2*((k-c+s-1)//s)
            assert dist[m+j] == 2*((c+s-1)//s)+1
        maxdist = max(maxdist, max(dist))
    assert maxdist == 2*((k+s-1)//s)+1
    # Check the exact triangular inclusion-indicator action underlying the spectrum.
    K = np.array([[int(not A & B) for B in sets] for A in sets], dtype=np.int64)
    for j in range(k+1):
        for T in combinations(range(n), j):
            T = frozenset(T)
            indicator = np.array([int(T <= A) for A in sets], dtype=np.int64)
            predicted = np.array([int(not T & A) * math.comb(n-k-j, k-j)
                                  for A in sets], dtype=np.int64)
            assert np.array_equal(K @ indicator, predicted)
    return dict(n=n, k=k, double_cover_vertices=2*m, exact_diameter=maxdist,
                all_distances_verified=True, inclusion_action_verified=True)


report = dict(
    flag_matrices=[check_flags("PG(2,q)", q, projective_plane) for q in [2,3]]
                  + [check_flags("AG(2,q)", q, affine_plane) for q in [3,5]],
    kneser=[check_kneser(n,k) for n,k in [(3,1),(5,2),(6,2),(7,3),(8,3),(9,3)]],
    arithmetic="integer only",
    status="PASS")
(ROOT / "incidence_matrix_check.json").write_text(json.dumps(report, indent=2)+"\n")
print(json.dumps(report, indent=2))
