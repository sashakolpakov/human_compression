"""Search cyclic middle graphs for Moore-bound (k;5,4)-cages.

Based on the reduction in Araujo-Pardo et al., arXiv:2401.15539.
An infeasible result excludes only the explicitly imposed cyclic symmetry.
Every positive result is checked independently by BFS and common neighbors.
"""
import argparse
from collections import Counter, deque
from itertools import combinations
import json
from pathlib import Path
import time

from ortools.sat.python import cp_model


def verify(k, edges):
    n = k * (k - 1)
    vertices = [(i, j) for i in range(k) for j in range(k) if i != j]
    graph = [set() for _ in range(n + 2 * k + 2)]
    def add(a, b):
        assert a != b and b not in graph[a]
        graph[a].add(b)
        graph[b].add(a)
    for a, b in edges:
        add(a, b)
    for v, (i, j) in enumerate(vertices):
        assert len(graph[v]) == k - 2
        add(v, n + i)
        add(v, n + k + j)
    for i in range(k):
        add(n + i, n + 2 * k)
        add(n + k + i, n + 2 * k + 1)
    assert all(len(a) == k for a in graph)
    assert all(not (graph[a] & graph[b]) for a in range(len(graph)) for b in graph[a])
    assert all(len(graph[a] & graph[b]) <= 1 for a, b in combinations(range(len(graph)), 2))
    diameter = 0
    five_cycle = None
    for source in range(len(graph)):
        distance = {source: 0}
        queue = deque([source])
        while queue:
            a = queue.popleft()
            for b in graph[a]:
                if b not in distance:
                    distance[b] = distance[a] + 1
                    queue.append(b)
        assert len(distance) == len(graph)
        diameter = max(diameter, max(distance.values()))
        # A 5-cycle is an edge between distance-2 vertices with different
        # neighbors on their unique paths to the root (uniqueness: no C4).
        layer = [a for a in distance if distance[a] == 2]
        for a in layer:
            for b in graph[a]:
                if distance[b] == 2:
                    aa = next(iter(graph[a] & graph[source]))
                    bb = next(iter(graph[b] & graph[source]))
                    if aa != bb:
                        five_cycle = [source, aa, a, b, bb]
    assert diameter == 4 and five_cycle is not None
    return {'order': len(graph), 'degree': k, 'girth': 5, 'diameter': diameter,
            'five_cycle': five_cycle, 'adjacency': [sorted(a) for a in graph]}


def search(k, seconds, seed):
    started = time.monotonic()
    vertices = [(i, j) for i in range(k) for j in range(k) if i != j]
    index = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)
    def shift(v, s):
        i, j = vertices[v]
        return index[((i+s) % k, (j+s) % k)]
    edge_orbit = {}
    orbits = []
    for a, b in combinations(range(n), 2):
        if vertices[a][0] == vertices[b][0] or vertices[a][1] == vertices[b][1]:
            continue
        if (a, b) in edge_orbit:
            continue
        orbit = {tuple(sorted((shift(a, s), shift(b, s)))) for s in range(k)}
        o = len(orbits)
        for e in orbit:
            edge_orbit[e] = o
        orbits.append(sorted(orbit))
    possible = [set() for _ in range(n)]
    def edge(a, b):
        return edge_orbit[tuple(sorted((a, b)))]
    for a, b in edge_orbit:
        possible[a].add(b)
        possible[b].add(a)
    forbidden = set()
    for v in range(n):
        for a, b in combinations(sorted(possible[v]), 2):
            pair = {edge(v, a), edge(v, b)}
            if vertices[a][0] == vertices[b][0] or vertices[a][1] == vertices[b][1]:
                forbidden.add(tuple(sorted(pair)))
            if b in possible[a]:
                forbidden.add(tuple(sorted(pair | {edge(a, b)})))
    for a, b in combinations(range(n), 2):
        for v, w in combinations(sorted(possible[a] & possible[b]), 2):
            forbidden.add(tuple(sorted({edge(a,v),edge(a,w),edge(b,v),edge(b,w)})))
    model = cp_model.CpModel()
    variables = [model.new_bool_var(f'e{i}') for i in range(len(orbits))]
    # One representative per translation orbit of vertices suffices.
    for v in range(k - 1):
        counts = Counter(edge(v, a) for a in possible[v])
        model.add(sum(c * variables[o] for o, c in counts.items()) == k - 2)
    for f in sorted(forbidden):
        model.add_bool_or([variables[o].Not() for o in f])
    print(json.dumps({'k': k, 'orbits': len(orbits), 'forbidden': len(forbidden),
                      'build_seconds': time.monotonic() - started}), flush=True)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 8
    solver.parameters.random_seed = seed
    status = solver.solve(model)
    result = {'k': k, 'symmetry': 'simultaneous translation modulo k',
              'status': solver.status_name(status), 'seed': seed,
              'time_limit_seconds': seconds, 'wall_seconds': time.monotonic() - started,
              'solver_stats': solver.response_stats()}
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        selected = [o for o in range(len(orbits)) if solver.value(variables[o])]
        edges = [e for o in selected for e in orbits[o]]
        result['middle_vertices'] = vertices
        result['orbit_representatives'] = [orbits[o][0] for o in selected]
        result['middle_edges'] = edges
        result['verified'] = verify(k, edges)
    out = Path(__file__).parent / f'cage_k{k}_seed{seed}.json'
    out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ['middle_vertices','middle_edges','verified']}), flush=True)
    if 'verified' in result:
        print(json.dumps({key: value for key, value in result['verified'].items()
                          if key != 'adjacency'}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--k', type=int, default=7)
    parser.add_argument('--seconds', type=float, default=120)
    parser.add_argument('--seed', type=int, default=0)
    args = parser.parse_args()
    search(args.k, args.seconds, args.seed)
