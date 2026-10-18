"""Literal checks for three already acquired graph witnesses; no nauty import."""
import argparse
from collections import Counter, deque
import gzip
import hashlib
import json
from pathlib import Path
import sys


def need(ok, message):
    if not ok:
        raise ValueError(message)


def exact(ref):
    data = Path(ref['path']).read_bytes()
    need(len(data) == ref['bytes'] and hashlib.sha256(data).hexdigest() == ref['sha256'], 'Exact input: ' + ref['path'])
    return data


def graph6(text, n):
    need(type(n) is int and n in (16, 20, 40), 'One of the three fixed orders')
    values = [ord(c) - 63 for c in text]
    need(values and values[0] == n and all(0 <= q < 64 for q in values), 'Small graph6 header')
    bits = n * (n - 1) // 2
    need(len(values) == 1 + (bits + 5) // 6, 'Exact graph6 length')
    a = [set() for _ in range(n)]
    bit = 0
    for v in range(n):
        for u in range(v):
            if values[1 + bit // 6] & (1 << (5 - bit % 6)):
                a[u].add(v)
                a[v].add(u)
            bit += 1
    need(all(not values[1 + b // 6] & (1 << (5 - b % 6)) for b in range(bits, 6 * (len(values) - 1))), 'Zero graph6 padding')
    return a


def inputs(case):
    need(case['schema'] == 'F012_THREE_DESCRIPTIVE_WITNESSES_V1', 'Fixed case schema')
    rows = [line.split() for line in gzip.decompress(exact(case['witness_archive'])).decode('ascii').splitlines()]
    need(len(rows) == 736 and all(len(r) == 6 for r in rows), 'Acquired positive archive grammar')
    need(len({r[0] for r in rows}) == 736, 'Unique source IDs')
    selected = {r[0]: r for r in rows}
    expected = [('UntilOrder250_50', 16, 3, 6, 6), ('UntilOrder250_82', 20, 4, 5, 6), ('UntilOrder250_300', 40, 3, 8, 8)]
    need(len(case['graphs']) == 3, 'Three exact witnesses')
    graphs = {}
    for record, target in zip(case['graphs'], expected):
        need(tuple(record[k] for k in ('id', 'n', 'k', 'g', 'lambda')) == target, 'Fixed source parameters')
        raw = selected[record['id']]
        need(list(map(int, raw[1:5])) == list(target[1:]) and raw[5] == record['graph6'], 'Exact acquired graph6')
        a = graph6(record['graph6'], record['n'])
        need(all(len(v) == record['k'] for v in a), 'Literal regularity')
        graphs[record['n']] = a
    return graphs


def permutation(p, n):
    return type(p) is list and len(p) == n and all(type(x) is int for x in p) and sorted(p) == list(range(n))


def preserves(a, b, p):
    return permutation(p, len(a)) and len(a) == len(b) and all({p[v] for v in a[u]} == b[p[u]] for u in range(len(a)))


def standard_mk():
    a = [set() for _ in range(16)]
    for i in range(8):
        for u, v in ((i, (i + 1) % 8), (i, 8 + i), (8 + i, 8 + (i + 3) % 8)):
            a[u].add(v)
            a[v].add(u)
    return a


def orbit(n, generators):
    seen = {0}
    q = deque([0])
    while q:
        u = q.popleft()
        for g in generators:
            v = g[u]
            if v not in seen:
                seen.add(v)
                q.append(v)
    return len(seen)


def walk_diagonal(a, length):
    n = len(a)
    need(type(length) is int and 1 <= length <= 40, 'Bounded walk length')
    m = [[int(i == j) for j in range(n)] for i in range(n)]
    for _ in range(length):
        m = [[sum(m[i][k] for k in a[j]) for j in range(n)] for i in range(n)]
    return [m[i][i] for i in range(n)]


def rooted_histograms(a, rounds):
    n = len(a)
    need(type(rounds) is int and 1 <= rounds <= 40, 'Bounded colour refinement')
    colours = [[int(v == root) for v in range(n)] for root in range(n)]
    for _ in range(rounds):
        signatures = [[(colours[r][v], tuple(sorted(colours[r][w] for w in a[v]))) for v in range(n)] for r in range(n)]
        labels = {x: i for i, x in enumerate(sorted({x for row in signatures for x in row}))}
        colours = [[labels[x] for x in row] for row in signatures]
    return [sorted(Counter(row).items()) for row in colours]


def verify(case, cert):
    graphs = inputs(case)
    need(set(cert) == {'schema', 'graphs', 'mk16_to_standard', 'vt16', 'vt40', 'mk16_to_twenty', 'four_added', 'nonvt20', 'odd_cycle20'}, 'Exact certificate fields')
    need(cert['schema'] == 'F012_LITERAL_DESCRIPTIVE_CERTIFICATES_V1' and cert['graphs'] == case['graphs'], 'Exact certificate source join')
    a, b, c = graphs[16], graphs[20], graphs[40]
    need(preserves(a, standard_mk(), cert['mk16_to_standard']), 'Exact generalized Petersen G(8,3) identification')
    for n, adj, field in ((16, a, 'vt16'), (40, c, 'vt40')):
        generators = cert[field]
        need(type(generators) is list and 1 <= len(generators) <= 80, 'Bounded literal generator list')
        need(all(preserves(adj, adj, g) for g in generators), 'Every full adjacency permutation')
        need(orbit(n, generators) == n, 'Full positive vertex orbit')
    injection = cert['mk16_to_twenty']
    need(type(injection) is list and len(injection) == 16 and all(type(x) is int and 0 <= x < 20 for x in injection) and len(set(injection)) == 16, 'Literal16-to20 injection')
    old = set(injection)
    new = sorted(set(range(20)) - old)
    need(cert['four_added'] == new, 'Exactly four added vertices')
    need(all({injection[v] for v in a[u]} == b[injection[u]] & old for u in range(16)), 'Whole induced old graph')
    need(all(not (b[u] & set(new)) for u in new), 'New four independent')
    need(all(len(b[u] & set(new)) == 1 for u in old), 'One new neighbour per old vertex')
    need(all(len(b[u] & old) == 4 for u in new), 'Four old neighbours per new vertex')
    obstruction = cert['nonvt20']
    need(set(obstruction) == {'kind', 'depth', 'values', 'vertices'}, 'Exact nonVT invariant fields')
    need(obstruction['kind'] in ('closed_walk', 'rooted_colour'), 'Allowed exact invariant')
    values = walk_diagonal(b, obstruction['depth']) if obstruction['kind'] == 'closed_walk' else rooted_histograms(b, obstruction['depth'])
    # JSON changes tuple pairs to lists; compare the complete normalized literal array.
    values = json.loads(json.dumps(values))
    need(obstruction['values'] == values, 'Full invariant recomputation')
    v = obstruction['vertices']
    need(type(v) is list and len(v) == 2 and all(type(i) is int and 0 <= i < 20 for i in v) and values[v[0]] != values[v[1]], 'Two unequal vertex invariants')
    cycle = cert['odd_cycle20']
    need(type(cycle) is list and len(cycle) == 5 and all(type(i) is int and 0 <= i < 20 for i in cycle) and len(set(cycle)) == 5, 'Literal pentagon')
    need(all(cycle[(i + 1) % 5] in b[cycle[i]] for i in range(5)), 'All pentagon edges')
    return dict(status='CHECKED_LITERAL_DESCRIPTIVE_CERTIFICATES', vertex_transitive_orders=[16, 40],
                mk_standard='G(8,3)', induced_MK16_in_order20=True, four_added=new,
                order20_not_vertex_transitive=True, order20_not_edge_transitive=True,
                non_edge_transitivity_argument='A connected edge-transitive graph with two vertex orbits is bipartite; this graph contains the checked odd cycle.',
                no_automorphism_group_completeness_assumption=True, whole_original_credit=0)


def main():
    need(not sys.flags.optimize, 'Ordinary Python required')
    p = argparse.ArgumentParser()
    p.add_argument('--case', type=Path, required=True)
    p.add_argument('--certificate', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    case, cert = (json.loads(q.read_text()) for q in (args.case, args.certificate))
    result = verify(case, cert)
    args.out.mkdir(exist_ok=False)
    (args.out / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, sort_keys=True))


if __name__ == '__main__':
    main()
