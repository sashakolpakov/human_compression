"""Literal M11 subgroup pairs and incidence graphs. No GAP, source counts or names."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode = True
from pathlib import Path
from collections import Counter, deque
from itertools import combinations
from math import comb
import hashlib
import json
from memory_guard import check_memory, peak_bytes

HERE = Path(__file__).resolve().parent
IDENTITY = tuple(range(11))


def need(ok, message):
    check_memory()
    if not ok:
        raise ValueError(message)


def mul(p, q):
    return tuple(q[x] for x in p)


def inv(p):
    q = [0] * len(p)
    for i, x in enumerate(p):
        q[x] = i
    return tuple(q)


def closure(gens, index):
    seen = {index[IDENTITY]}
    elements = [IDENTITY]
    for x in elements:
        for g in gens:
            y = mul(x, g)
            need(y in index, 'Subgroup stays in acquired group')
            j = index[y]
            if j not in seen:
                seen.add(j)
                elements.append(y)
    return frozenset(seen)


def cosets(H, elements, index):
    assignment = [-1] * len(elements)
    parts = []
    representatives = []
    for i, g in enumerate(elements):
        if assignment[i] >= 0:
            continue
        part = sorted(index[mul(elements[h], g)] for h in H)
        need(len(part) == len(H) and len(set(part)) == len(H), 'Literal right coset')
        k = len(parts)
        for j in part:
            need(assignment[j] == -1, 'Disjoint coset partition')
            assignment[j] = k
        parts.append(part)
        representatives.append(i)
    need(all(x >= 0 for x in assignment), 'Complete coset partition')
    return assignment, parts, representatives


def metrics(adjacency, first_size):
    n = len(adjacency)
    need(all(sorted(set(row)) == row and all(0 <= v < n and u in adjacency[v]
             and ((u < first_size) != (v < first_size)) for v in row)
             for u, row in enumerate(adjacency)), 'Simple undirected bipartite graph')
    eccentricities = []
    girth = n + 1
    for root in range(n):
        distances = [-1] * n
        parent = [-1] * n
        distances[root] = 0
        queue = [root]
        for u in queue:
            for v in adjacency[u]:
                if distances[v] < 0:
                    distances[v] = distances[u] + 1
                    parent[v] = u
                    queue.append(v)
                elif parent[u] != v and parent[v] != u:
                    girth = min(girth, distances[u] + distances[v] + 1)
        need(len(queue) == n, 'Connected incidence graph')
        eccentricities.append(max(distances))
    need(len(set(eccentricities[:first_size])) == 1 and
         len(set(eccentricities[first_size:])) == 1, 'Constant eccentricity on both types')
    need(girth <= n and girth % 2 == 0, 'Actual even cycle')
    return dict(point_diameter=eccentricities[0], gonality=girth // 2,
                line_diameter=eccentricities[first_size], eccentricities=eccentricities,
                girth=girth, graph_vertices=n, graph_edges=sum(map(len, adjacency)) // 2)


def designs(adjacency, first_size, point_side):
    points = list(range(first_size)) if point_side == 0 else list(range(first_size, len(adjacency)))
    blocks = list(range(first_size, len(adjacency))) if point_side == 0 else list(range(first_size))
    pindex = {p:i for i,p in enumerate(points)}
    bindex = {b:i for i,b in enumerate(blocks)}
    blocks_as_points = [tuple(sorted(pindex[p] for p in adjacency[b])) for b in blocks]
    sizes = set(map(len, blocks_as_points))
    need(len(sizes) == 1, 'Constant block size')
    k = next(iter(sizes)); v = len(points)
    masks = [sum(1 << bindex[b] for b in adjacency[p]) for p in points]
    result = dict(v=v, b=len(blocks), k=k, distinct_blocks=len(set(blocks_as_points)),
                  blocks=blocks_as_points, uniform_counts=[], first_failure=None)
    if k == v:
        result.update(complete_incidence=True, uniform_all_t_through=k,
                      constant_lambda=len(blocks), all_subset_checks_complete=True)
        return result
    result['complete_incidence'] = False
    for t in range(1, k + 1):
        if comb(v, t) > 250000:
            result.update(all_subset_checks_complete=False, stopped_before_t=t,
                          reason='Fixed 250000-subset per-strength cap')
            return result
        baseline = None; first = None; count = 0
        for subset in combinations(range(v), t):
            mask = (1 << len(blocks)) - 1
            for p in subset:
                mask &= masks[p]
            value = mask.bit_count(); count += 1
            if baseline is None:
                baseline, first = value, subset
            elif value != baseline:
                result['first_failure'] = dict(t=t, subsets=[first, subset],
                                               counts=[baseline, value], inspected=count)
                result['all_subset_checks_complete'] = True
                return result
        result['uniform_counts'].append(dict(t=t, lambda_value=baseline, subsets_checked=count))
    result['all_subset_checks_complete'] = True
    return result


def conjugates(H, actions, generators, elements, index):
    values = [H]; witnesses = [index[IDENTITY]]; lookup = {H:0}
    for pos, h in enumerate(values):
        for action, g in zip(actions, generators):
            other = frozenset(action[x] for x in h)
            if other not in lookup:
                need(len(values) < 7920, 'Conjugacy orbit bound')
                lookup[other] = len(values)
                values.append(other)
                witnesses.append(index[mul(elements[witnesses[pos]], g)])
    return values, witnesses


def calculate(data):
    model = data['group_model']
    need(model['name'] == 'M11' and model['degree'] == 11, 'Exact acquired named model')
    elements = [tuple(p) for p in model['elements']]
    generators = [tuple(p) for p in model['generators']]
    need(len(elements) == 7920 and len(set(elements)) == 7920 and elements[0] == IDENTITY,
         '7920 distinct permutations with identity')
    need(all(len(p) == 11 and set(p) == set(range(11)) for p in elements), 'Permutation domain')
    index = {g:i for i,g in enumerate(elements)}
    need(closure(generators,index) == frozenset(range(7920)), 'Exact generated group')
    subgroup_gens = [[tuple(p) for p in row] for row in data['subgroup_generators']]
    need(len(subgroup_gens) == 39, 'All acquired representatives')
    subgroups = [closure(row,index) for row in subgroup_gens]
    maximum = data['maximal_class_positions']
    need(maximum == [38,37,35,34,27], 'Frozen maximal selection from acquired census')
    actions = [[index[mul(mul(inv(g), x), g)] for x in elements] for g in generators]
    maxes = []; types = []; conjugators = []
    for k in maximum:
        values, witnesses = conjugates(subgroups[k-1], actions, generators, elements,index)
        maxes.extend(values); types.extend([k] * len(values)); conjugators.extend(witnesses)
    need(len(set(maxes)) == len(maxes) and len(maxes) <= 309, 'Distinct bounded maximal subgroups')
    max_index = {h:i for i,h in enumerate(maxes)}
    permutations = [[max_index[frozenset(action[x] for x in h)] for h in maxes] for action in actions]
    need(all(sorted(p) == list(range(len(maxes))) for p in permutations), 'Conjugation permutations')
    pairs = list(combinations(range(len(maxes)),2))
    need(len(pairs) <= 47586, 'Fixed unordered-pair domain bound')
    position = {p:i for i,p in enumerate(pairs)}
    orbit_assignment = [-1] * len(pairs)
    pair_orbits = []
    for start, pair in enumerate(pairs):
        if orbit_assignment[start] >= 0:
            continue
        number = len(pair_orbits)
        orbit = [start]; orbit_assignment[start] = number
        for j in orbit:
            p = pairs[j]
            for action in permutations:
                q = tuple(sorted((action[p[0]], action[p[1]])))
                k = position[q]
                if orbit_assignment[k] < 0:
                    orbit_assignment[k] = number; orbit.append(k)
                else:
                    need(orbit_assignment[k] == number, 'Disjoint pair orbits')
        pair_orbits.append(dict(representative=pair, pair_positions=orbit))
    needed_orders = {len(maxes[r['representative'][0]] & maxes[r['representative'][1]])
                     for r in pair_orbits}
    intersection_models = {}
    for k, h in enumerate(subgroups,1):
        if len(h) in needed_orders:
            values, witnesses = conjugates(h,actions,generators,elements,index)
            for value,w in zip(values,witnesses):
                need(value not in intersection_models,'Distinct acquired subgroup classes')
                intersection_models[value] = [k,w]
    graphs = []
    coset_cache = {}
    for i,r in enumerate(pair_orbits):
        h,k = r['representative']
        intersection = maxes[h] & maxes[k]
        need(intersection in intersection_models,'Intersection conjugate to an acquired representative')
        for v in [h,k]:
            if v not in coset_cache:
                coset_cache[v] = cosets(maxes[v],elements,index)
        c1,parts1,reps1 = coset_cache[h]
        c2,parts2,reps2 = coset_cache[k]
        n1,n2 = len(parts1),len(parts2)
        adjacency = [set() for _ in range(n1+n2)]
        for u,v in zip(c1,c2):
            adjacency[u].add(n1+v); adjacency[n1+v].add(u)
        adjacency = [sorted(row) for row in adjacency]
        stats = metrics(adjacency,n1)
        need(stats['graph_edges'] * len(intersection) == 7920,'Edge stabilizer formula')
        graphs.append(dict(orbit=i, pair=r['representative'], subgroup_classes=[types[h],types[k]],
            subgroup_orders=[len(maxes[h]),len(maxes[k])], intersection_order=len(intersection),
            intersection_elements=sorted(intersection), intersection_class_witness=intersection_models[intersection],
            coset_representatives=[reps1,reps2], coset_assignment=[c1,c2], adjacency=adjacency,
            type_sizes=[n1,n2], metrics=stats, designs=[designs(adjacency,n1,j) for j in [0,1]]))
    return dict(status='L036_LITERAL_M11_PAIR_GRAPHS_RETURNED', group_order=7920,
        group_indexing='inputs.json group_model.elements', subgroup_elements=[sorted(h) for h in subgroups],
        maximal_subgroups=[dict(class_position=t,conjugator=w,elements=sorted(h))
                           for h,t,w in zip(maxes,types,conjugators)],
        maximal_action=permutations, unordered_pair_ordering='itertools.combinations(range(number_of_maximal_subgroups),2)',
        pair_orbit_assignment=orbit_assignment, pair_orbits=pair_orbits,
        number_of_maximal_subgroups=len(maxes), unordered_pairs=len(pairs), number_of_orbits=len(pair_orbits),
        graphs=graphs, complete_design_checks=all(d['all_subset_checks_complete'] for g in graphs for d in g['designs']),
        named_intersection_identifications_accepted=False, source_comparison_performed=False,
        whole_source_accepted=False)


if __name__ == '__main__':
    # Sampled self-memory guard; the platform rejects kernel limit setters.
    check_memory(force=True)
    raw=(HERE/'inputs.json').read_bytes()
    result=calculate(json.loads(raw))
    result['input_sha256']=hashlib.sha256(raw).hexdigest()
    check_memory(force=True)
    result['peak_rss_bytes_before_output']=peak_bytes()
    encoded=json.dumps(result,separators=(',',':'))
    check_memory(force=True)
    print(encoded)
