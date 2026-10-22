"""Check the one pinned literal star example, without census or class lookup.

Author: /root/readme_final_check. Plain BFS, need() and strict JSON reading
are borrowed from Navigation's held cyclic_defects/check_example.py; remaining
star/bipartition/layer logic and same-authenticated-bytes parsing are new.
No historical novelty, current-family membership or completed-census claim.
"""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path
import sys


EXAMPLE_SHA256 = 'bf45d3eda5cc616fd9eb19e0c5dafe76ddad5647cfe56a1dbbe1efc72b7c45d9'


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


def pin_raw(path, raw):
    need(len(raw) <= 65536, 'one bounded literal artifact or Source')
    return dict(path=str(path), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def pin(path):
    return pin_raw(path, path.read_bytes())


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
    need(type(vertices) is list and len(vertices) == length
         and all(type(v) is int and 0 <= v < 32 for v in vertices)
         and len(set(vertices)) == length, 'literal simple cycle vertices')
    need(all(vertices[(i+1) % length] in adjacency[v] for i, v in enumerate(vertices)),
         'every cycle edge including last')


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
    raw = args.input.read_bytes()
    artifact = pin_raw(args.input, raw)
    need(args.input_sha256 == EXAMPLE_SHA256 == artifact['sha256'], 'the one pinned whole literal artifact SHA')
    value = strict(raw)
    need(type(value) is dict and set(value) == {
        'schema', 'description', 'adjacency', 'independent_set', 'bipartition_extra_vertex',
        'roots', 'middle_center', 'defect_edges', 'four_cycle', 'geodesic', 'distance_layers'}
        and value['schema'] == 'F009_LITERAL_ORDER32_STAR_DEFECT_EXAMPLE_V1'
        and type(value['description']) is str, 'exact literal-example metadata fields')

    adjacency = value['adjacency']
    need(type(adjacency) is list and len(adjacency) == 32, 'exact order32')
    for u, neighbors in enumerate(adjacency):
        need(type(neighbors) is list and len(neighbors) == 5
             and all(type(v) is int and 0 <= v < 32 and v != u for v in neighbors)
             and neighbors == sorted(set(neighbors)), 'five distinct ordered neighbors, no loops')
    need(all(u in adjacency[v] for u, neighbors in enumerate(adjacency) for v in neighbors),
         'every adjacency symmetric')
    edges = [(u, v) for u, neighbors in enumerate(adjacency) for v in neighbors if u < v]
    need(len(edges) == 80, 'exact80 undirected edges')
    all_distances = [distances(adjacency, u) for u in range(32)]
    need(all(all(d >= 0 for d in row) for row in all_distances), 'connected graph')
    diameter = max(max(row) for row in all_distances)
    need(diameter == 8 and all_distances[0][10] == 8, 'exact all-pairs diameter and root distance8')
    girth = 33
    for u, v in edges:
        d = distances(adjacency, u, (u, v))[v]
        if d >= 0:
            girth = min(girth, d+1)
    need(girth == 4, 'exact girth4 by every edge-deletion distance')
    cycle(adjacency, value['four_cycle'], 4)

    path = value['geodesic']
    need(type(path) is list and all(type(v) is int for v in path)
         and path == [0,1,9,21,20,25,19,11,10]
         and all(v in adjacency[u] for u, v in zip(path, path[1:])), 'literal eight-edge root geodesic')
    independent = value['independent_set']
    need(type(independent) is list and all(type(v) is int for v in independent)
         and independent == [1,2,3,4,5,11,12,13,14,15,21,22,23,24,25]
         and type(value['roots']) is list and all(type(v) is int for v in value['roots'])
         and value['roots'] == [0,10] and type(value['middle_center']) is int
         and value['middle_center'] == 20
         and set(independent) == set(adjacency[0]+adjacency[20]+adjacency[10])
         and all(v not in independent for u in independent for v in adjacency[u]),
         'exact independent15 from the three center neighborhoods')
    complement = set(range(32))-set(independent)
    defects = [(u, v) for u, v in edges if u in complement and v in complement]
    expected_defects = [(6,31),(7,31),(26,31),(27,31),(30,31)]
    need(type(value['defect_edges']) is list
         and all(type(e) is list and len(e) == 2 and all(type(v) is int for v in e)
                 for e in value['defect_edges'])
         and defects == expected_defects
         and value['defect_edges'] == [list(e) for e in expected_defects],
         'every exact induced defect edge')
    center, leaves = 31, [6,7,26,27,30]
    defect_adjacency = {v: [] for v in complement}
    for u, v in defects:
        defect_adjacency[u].append(v)
        defect_adjacency[v].append(u)
    need(sorted(defect_adjacency[center]) == leaves
         and all(defect_adjacency[v] == [center] for v in leaves)
         and all(not defect_adjacency[v] for v in complement-set(leaves)-{center}),
         'exact K1,5 support and eleven isolates')

    need(type(value['bipartition_extra_vertex']) is int
         and value['bipartition_extra_vertex'] == center, 'literal extra bipartition vertex31')
    left = set(independent)|{center}
    right = set(range(32))-left
    need(len(left) == len(right) == 16
         and all((u in left) != (v in left) for u, v in edges),
         'whole balanced bipartition, every edge crossing')
    expected_layers = [[0], [1,2,3,4,5], [6,7,8,9,26,27], [21,22,31], [20,30],
                       [23,24,25], [16,17,18,19,28,29], [11,12,13,14,15], [10]]
    layers = value['distance_layers']
    need(type(layers) is list
         and all(type(layer) is list and all(type(v) is int for v in layer) for layer in layers)
         and layers == expected_layers, 'all literal distance layers')
    flat = [v for layer in layers for v in layer]
    need(len(flat) == len(set(flat)) == 32 and sorted(flat) == list(range(32)),
         'distance layers form the entire vertex partition')
    layer_of = {v: i for i, layer in enumerate(layers) for v in layer}
    need(all(all_distances[0][v] == layer_of[v] for v in range(32))
         and all(abs(layer_of[u]-layer_of[v]) == 1 for u, v in edges)
         and all(any(layer_of[w] == layer_of[v]-1 for w in adjacency[v])
                 for v in range(1,32)), 'exact root BFS distances and consecutive-layer proof')

    expected_seed = [(0,v) for v in range(1,6)]+[(1,v) for v in range(6,10)]
    expected_seed += [(10,v) for v in range(11,16)]+[(11,v) for v in range(16,20)]
    expected_seed += [(20,v) for v in range(21,26)]+[(9,21),(19,25)]
    expected_seed.sort()
    need(len(expected_seed) == 25 and all(e in edges for e in expected_seed),
         'all25 exact literal old seed edges')
    need(pin(args.input) == artifact, 'pinned input unchanged through the checks')
    need(args.out.is_absolute() and args.out.parent.resolve(strict=True) == args.out.parent
         and not args.out.exists(), 'fresh explicit ordinary result')
    result = dict(schema='F009_CHECKED_LITERAL_ORDER32_STAR_DEFECT_EXAMPLE_V1',
        status='VERIFIED_ONE_EXPLICIT_ORDER32_STAR_DEFECT_GRAPH', artifact=artifact,
        method=pin(Path(__file__).resolve()), vertices=32, edges=80, degree=5,
        simple_symmetric=True, connected=True, girth=girth, diameter=diameter,
        root_distance=all_distances[0][10], literal_geodesic=path,
        independent_set=independent, independent_set_size=15,
        defect_edges=[list(e) for e in defects], defect_shape='K1_5',
        defect_center=center, defect_leaves=leaves, defect_isolates=11,
        bipartite=True, balanced_bipartition=[sorted(left),sorted(right)],
        every_edge_crosses_bipartition=True, distance_layers=layers,
        every_edge_joins_consecutive_layers=True, seed_edges=expected_seed,
        seed_edge_count=25, source_class_set_membership_checked=False,
        current_family_membership_checked=False, graph_isomorphism_or_class_reduction_performed=False,
        accepted_checkpoint_changed=False, census_credit=0, whole_original_credit=0,
        qualification='One pinned independently supplied literal graph only; no source-class comparison, current-family membership, completeness or novelty claim.')
    with args.out.open('x') as stream:
        stream.write(json.dumps(result, indent=2, sort_keys=True, allow_nan=False)+'\n')
    print(json.dumps(dict(status=result['status'], result=pin(args.out)), sort_keys=True))


if __name__ == '__main__':
    main()
