"""Read the complete bounded GAP certificate; independently check its small graphs.

This is author verification, not an independent mathematical review.  No old
shadow decision, historical IP label or census is recomputed here.
"""
from pathlib import Path
import argparse
import ast
import collections
import json


def need(value, message):
    if not value:
        raise ValueError(message)


def girth(adjacency):
    n = len(adjacency)
    best = n + 1
    for start in range(n):
        distance = [-1] * n
        parent = [-1] * n
        distance[start] = 0
        queue = collections.deque([start])
        while queue:
            u = queue.popleft()
            for v in adjacency[u]:
                v -= 1
                if distance[v] < 0:
                    distance[v] = distance[u] + 1
                    parent[v] = u
                    queue.append(v)
                elif parent[u] != v:
                    best = min(best, distance[u] + distance[v] + 1)
    return best


def parse(text):
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    need(lines[-1:] == ['LABEL_INVARIANTS_PASS'], 'complete success terminator')
    records = []
    for line in lines[:-1]:
        fields = line.split('|')
        tag = fields[0]
        if tag == 'M22_SWAP':
            need(len(fields) == 4 and fields[3] in ['true', 'false'], 'swap syntax')
            row, stabilizer = map(int, fields[1:3])
            need(stabilizer == 1320, 'full stabilizer domain')
            records.append(dict(group='M22', member='prior_m22.rk3', active_row=row,
                                stabilizer_order=stabilizer,
                                source_correlation_type_swap=fields[3] == 'true'))
        elif tag == 'M22_RESIDUE':
            need(len(fields) == 6, 'residue syntax')
            row, order, n, claimed_girth = map(int, fields[1:5])
            adj = ast.literal_eval(fields[5])
            need(len(adj) == n and all(len(set(a)) == len(a) == 3 for a in adj), 'cubic graph')
            need(all(isinstance(v, int) and 1 <= v <= n and v != u
                     for u, a in enumerate(adj, 1) for v in a), 'simple graph vertices')
            need(all(u in adj[v - 1] for u, a in enumerate(adj, 1) for v in a), 'symmetric graph')
            reached = {1}
            frontier = [1]
            for u in frontier:
                for v in adj[u - 1]:
                    if v not in reached:
                        reached.add(v)
                        frontier.append(v)
            need(len(reached) == n, 'connected rank-two graph')
            need(girth(adj) == claimed_girth, 'independently recomputed graph girth')
            records.append(dict(group='M22', member='prior_m22.rk4', active_row=row,
                                residue_group_order=order, residue_girth=claimed_girth,
                                vertices=n, adjacency=adj))
        elif tag == 'J3_SWAP':
            need(len(fields) == 5 and fields[4] == 'true', 'J3 square condition')
            row, domain, swaps = map(int, fields[1:4])
            need(domain == 2448 and swaps in [0, 8], 'complete inner normalizer domain')
            records.append(dict(group='J3', member='j3.rk3', active_row=row,
                                normalizer_order=domain, inner_swaps=swaps,
                                central_type_swap=swaps > 0, all_squares_in_borel=True))
        else:
            raise ValueError('unexpected GAP output: ' + line)
    identities = {(r['group'], r['member'], r['active_row']) for r in records}
    need(len(records) == len(identities) == 7, 'seven unique certificate records')
    need(identities == {('M22', 'prior_m22.rk3', 3), ('M22', 'prior_m22.rk3', 5),
                        ('M22', 'prior_m22.rk4', 11), ('M22', 'prior_m22.rk4', 12),
                        ('J3', 'j3.rk3', 9), ('J3', 'j3.rk3', 10), ('J3', 'j3.rk3', 11)},
         'exact declared family domains')
    return {'status': 'PASS_BOUNDED_LABEL_INVARIANTS', 'records': records,
            'new_shadow_or_census_computation': False,
            'source_label_selection_uses_ip_values': False}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('log', type=Path)
    p.add_argument('--out', required=True, type=Path)
    a = p.parse_args()
    a.out.write_text(json.dumps(parse(a.log.read_text()), indent=2) + '\n')
