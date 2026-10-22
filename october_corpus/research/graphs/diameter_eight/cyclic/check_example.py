"""Check one supplied literal graph; no project imports, census or class lookup."""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path
import sys


def need(ok, label):
    if not ok:
        raise ValueError(label)


def strict(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, 'unique JSON keys')
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs,
        parse_constant=lambda _: (_ for _ in ()).throw(ValueError('finite JSON')))


def pin(path):
    raw = path.read_bytes()
    need(len(raw) <= 65536, 'one bounded literal artifact or Source')
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def distances(adjacency, start, omitted=None):
    d = [-1]*len(adjacency)
    d[start] = 0
    queue = deque([start])
    while queue:
        u = queue.popleft()
        for v in adjacency[u]:
            if omitted is not None and ((u, v) == omitted or (v, u) == omitted):
                continue
            if d[v] < 0:
                d[v] = d[u]+1
                queue.append(v)
    return d


def cycle(adjacency, vertices, length):
    need(type(vertices) is list and len(vertices) == len(set(vertices)) == length
         and all(type(v) is int and 0 <= v < 32 for v in vertices), 'literal simple cycle vertices')
    need(all(vertices[(i+1) % length] in adjacency[v] for i, v in enumerate(vertices)), 'every cycle edge including last')


def main():
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode
         and not sys.flags.optimize, 'ordinary -E -B -S')
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--input-sha256', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(args.input.is_absolute() and args.input.resolve(strict=True) == args.input
         and args.input.is_file() and not args.input.is_symlink(), 'one real explicit literal input')
    artifact = pin(args.input)
    need(artifact['sha256'] == args.input_sha256, 'whole explicit artifact SHA')
    value = strict(args.input.read_bytes())
    need(pin(args.input) == artifact and type(value) is dict
         and value['schema'] == 'F009_LITERAL_ORDER32_CYCLIC_DEFECT_EXAMPLE_V1', 'stable whole literal example')
    adjacency = value['adjacency']
    need(type(adjacency) is list and len(adjacency) == 32, 'exact order32')
    for u, neighbors in enumerate(adjacency):
        need(type(neighbors) is list and len(neighbors) == 5
             and all(type(v) is int and 0 <= v < 32 and v != u for v in neighbors)
             and neighbors == sorted(set(neighbors)), 'five distinct ordered neighbors, no loops')
    need(all(u in adjacency[v] for u, neighbors in enumerate(adjacency) for v in neighbors), 'every adjacency symmetric')
    edges = [(u, v) for u, neighbors in enumerate(adjacency) for v in neighbors if u < v]
    need(len(edges) == 80, 'exact80 undirected edges')
    all_distances = [distances(adjacency, u) for u in range(32)]
    need(all(all(d >= 0 for d in row) for row in all_distances), 'connected graph')
    diameter = max(max(row) for row in all_distances)
    need(diameter == 8 and all_distances[0][10] == 8, 'exact diameter and root distance8')
    girth = 33
    for u, v in edges:
        d = distances(adjacency, u, (u, v))[v]
        if d >= 0:
            girth = min(girth, d+1)
    need(girth == 4, 'exact girth4 by every edge-deletion distance')
    cycle(adjacency, value['four_cycle'], 4)
    cycle(adjacency, value['odd_cycle'], 5)
    path = value['geodesic']
    need(type(path) is list and all(type(v) is int for v in path)
         and path == [0,1,9,21,20,25,19,11,10]
         and all(v in adjacency[u] for u, v in zip(path, path[1:])), 'literal eight-edge geodesic')
    independent = value['independent_set']
    need(type(independent) is list and all(type(v) is int for v in independent)
         and independent == [1,2,3,4,5,11,12,13,14,15,21,22,23,24,25]
         and type(value['roots']) is list and all(type(v) is int for v in value['roots'])
         and value['roots'] == [0,10] and type(value['middle_center']) is int
         and value['middle_center'] == 20
         and set(independent) == set(adjacency[0]+adjacency[20]+adjacency[10])
         and all(v not in independent for u in independent for v in adjacency[u]), 'exact independent15 from three center neighborhoods')
    complement = set(range(32))-set(independent)
    defects = [(u, v) for u, v in edges if u in complement and v in complement]
    expected = [(8,26),(8,27),(9,26),(9,27),(19,31)]
    need(defects == expected and value['defect_edges'] == [list(e) for e in expected]
         and all(type(e) is list and all(type(v) is int for v in e) for e in value['defect_edges']),
         'every exact induced defect edge')
    defect_adjacency = {v: [] for v in complement}
    for u, v in defects:
        defect_adjacency[u].append(v)
        defect_adjacency[v].append(u)
    unseen = {v for v in complement if defect_adjacency[v]}
    components = []
    while unseen:
        start = min(unseen)
        reached = {start}
        queue = deque([start])
        while queue:
            for v in defect_adjacency[queue.popleft()]:
                if v not in reached:
                    reached.add(v)
                    queue.append(v)
        unseen.difference_update(reached)
        components.append((len(reached), sum(len(defect_adjacency[v]) for v in reached)//2,
                           sorted(len(defect_adjacency[v]) for v in reached)))
    need(sorted(components) == [(2,1,[1,1]), (4,4,[2,2,2,2])], 'C4 disjoint union K2, ignoring isolates')
    expected_seed = [(0,v) for v in range(1,6)]+[(1,v) for v in range(6,10)]
    expected_seed += [(10,v) for v in range(11,16)]+[(11,v) for v in range(16,20)]
    expected_seed += [(20,v) for v in range(21,26)]+[(9,21),(19,25)]
    expected_seed.sort()
    need(len(expected_seed) == 25 and value['seed_edges'] == [list(e) for e in expected_seed]
         and all(type(e) is list and all(type(v) is int for v in e) for e in value['seed_edges'])
         and all(e in edges for e in expected_seed), 'all25 exact already described seed edges')
    need(args.out.is_absolute() and args.out.parent.resolve(strict=True) == args.out.parent
         and not args.out.exists(), 'fresh explicit ordinary result')
    result = dict(schema='F009_CHECKED_LITERAL_ORDER32_CYCLIC_DEFECT_EXAMPLE_V1',
        status='VERIFIED_ONE_EXPLICIT_ORDER32_CYCLIC_DEFECT_GRAPH', artifact=artifact,
        method=pin(Path(__file__).resolve()), vertices=32, edges=80, degree=5,
        simple_symmetric=True, connected=True, girth=girth, diameter=diameter,
        root_distance=all_distances[0][10], independent_set_size=15,
        defect_edges=[list(e) for e in defects], defect_shape='C4_DISJOINT_UNION_K2',
        seed_edges=25, nonbipartite_by_checked_odd_cycle=True,
        source_class_set_membership_checked=False, current_family_membership_checked=False,
        graph_isomorphism_or_class_reduction_performed=False, accepted_checkpoint_changed=False,
        census_credit=0, whole_original_credit=0,
        qualification='One independently supplied literal graph only; no source-class comparison, current-family membership, completeness or novelty claim.')
    with args.out.open('x') as stream:
        stream.write(json.dumps(result, indent=2, sort_keys=True, allow_nan=False)+'\n')
    print(json.dumps(dict(status=result['status'], result=pin(args.out)), sort_keys=True))


if __name__ == '__main__':
    main()
