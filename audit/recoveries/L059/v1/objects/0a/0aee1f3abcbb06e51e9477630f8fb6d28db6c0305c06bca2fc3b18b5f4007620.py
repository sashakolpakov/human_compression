"""Count the retained census editions and verify the current graph set.

The historical coverage and uniqueness premises are external mathematical
inputs.  This program does not turn matching invariants into isomorphisms.
"""
import argparse
from collections import Counter, deque
import hashlib
import html
import json
from pathlib import Path
import re
import subprocess
import sys

if sys.flags.optimize:
    raise RuntimeError('optimized Python is unsupported')
import pynauty


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def integer(s):
    if re.fullmatch(r'\d+', s):
        return int(s)
    terms = re.findall(r'\((\d+)\^(\d+)\)', s)
    need(''.join('(' + a + '^' + b + ')' for a, b in terms) == s,
         'invalid integer expression: ' + s)
    value = 1
    for a, b in terms:
        value *= int(a) ** int(b)
    return value


def read_table(path):
    def clean(s):
        return re.sub(r'\s+', '', html.unescape(
            re.sub(r'<[/!]?[A-Za-z][^>]*>', '', s)))
    records = []
    for raw_row in re.split(r'<TR>', path.read_text(), flags=re.I)[1:]:
        cells = re.split(r'<TD>', raw_row, flags=re.I)[1:]
        if not cells:
            continue
        cells = [clean(c) for c in cells]
        match = re.search(r'C4\[(\d+),(\d+)\]', cells[0])
        need(match is not None and len(cells) in (12, 13), 'table row format')
        n, i = map(int, match.groups())
        need(int(cells[1]) == n, 'table order disagreement')
        need(cells[3] in ('DT', 'HT', 'SS'), 'unknown symmetry type')
        records.append(dict(n=n, i=i, tr=cells[3], bipartite=cells[5] == 'Bip',
                            aut_order=integer(cells[6]),
                            vertex_stabilizer=integer(cells[7])))
    need(len({(r['n'], r['i']) for r in records}) == len(records),
         'repeated table identifier')
    return records


def eligible(r):
    return (r['n'] <= 150 and r['bipartite'] and r['tr'] in ('DT', 'SS')
            and r['vertex_stabilizer'] < 200)


def graph_inputs(path):
    raw = path.read_text()
    matches = list(re.finditer(r'Graph<(\d+)\|\{(.*?)\}>', raw, re.S))
    need(len(matches) == raw.count('Graph<') and raw.rstrip().endswith(';'),
         'incomplete graph-source parse')
    seen = Counter()
    graphs = []
    for match in matches:
        n = int(match[1])
        seen[n] += 1
        if n > 150:
            continue
        edges = [tuple(sorted(map(int, pair))) for pair in
                 re.findall(r'\{\s*(\d+)\s*,\s*(\d+)\s*\}', match[2])]
        residue = re.sub(r'\{\s*\d+\s*,\s*\d+\s*\}|[\s,]', '', match[2])
        need(not residue and len(edges) == 2 * n and len(set(edges)) == 2 * n,
             'invalid edge list')
        adjacency = {v: [] for v in range(n)}
        for a, b in edges:
            need(1 <= a < b <= n, 'edge endpoints')
            adjacency[a - 1].append(b - 1)
            adjacency[b - 1].append(a - 1)
        need(all(len(a) == 4 for a in adjacency.values()), 'degree')
        bipartite = True
        colours = {0: 0}
        queue = deque([0])
        while queue:
            a = queue.popleft()
            for b in adjacency[a]:
                if b not in colours:
                    colours[b] = 1 - colours[a]
                    queue.append(b)
                elif colours[b] == colours[a]:
                    bipartite = False
        need(len(colours) == n, 'disconnected current graph')
        if bipartite:
            graphs.append(dict(n=n, i=seen[n], adjacency=adjacency,
                               edges={(a - 1, b - 1) for a, b in edges}))
    return graphs, len(matches), sum(v for n, v in seen.items() if n <= 150)


def edge_orbit(edges, generators, ordered=False):
    first = min(edges)
    seen = {first}
    queue = deque([first])
    while queue:
        a, b = queue.popleft()
        for p in generators:
            e = (p[a], p[b]) if ordered else tuple(sorted((p[a], p[b])))
            if e not in seen:
                seen.add(e)
                queue.append(e)
    return seen


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sources', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--gap', default='/opt/homebrew/bin/gap')
    args = parser.parse_args()
    sources = args.sources
    pins = json.loads((Path(__file__).parent / 'inputs.json').read_text())
    for item in pins:
        path = sources / item['path']
        need(path.stat().st_size == item['bytes'] and digest(path) == item['sha256'],
             'input hash: ' + item['path'])
    names = ('c4_table_20080505.html', 'c4_table_20141228.html', 'c4_table.html')
    tables = {name: read_table(sources / name) for name in names}
    need([len(tables[n]) for n in names] == [788, 793, 7364], 'table counts')
    selected = {name: [r for r in tables[name] if eligible(r)] for name in names}
    for name in names:
        need(len(selected[name]) == 397, 'selected table count')
        need(Counter(r['tr'] for r in selected[name]) == {'DT': 272, 'SS': 125},
             'selected symmetry counts')
    graphs, all_count, small_count = graph_inputs(sources / 'C4_FinalFull.mgm')
    need((all_count, small_count, len(graphs)) == (7364, 807, 562), 'graph counts')
    current = {(r['n'], r['i']): r for r in tables[names[-1]]}
    keys = set()
    verified = []
    gap_lines = ['# Generated exact orders of complete nauty automorphism generators.']
    for graph in graphs:
        n = graph['n']
        g = pynauty.Graph(n, adjacency_dict=graph['adjacency'])
        canonical = pynauty.certificate(g)
        need(canonical not in keys, 'isomorphic current graph repetitions')
        keys.add(canonical)
        metadata = current[n, graph['i']]
        need(metadata['bipartite'], 'table/data bipartition mismatch')
        generators, mantissa, exponent, orbits, orbit_count = pynauty.autgrp(g)
        # Nauty's floating group-order encoding can round for large groups.
        # Verify the exact integer order of its complete generators in GAP.
        order = metadata['aut_order']
        perms = ','.join('PermList(' + str([a + 1 for a in p]) + ')' for p in generators)
        gap_lines.append('if Size(Group([' + perms + ']))<>' + str(order)
                         + ' then Print("FAIL exact order ' + str((n, graph['i']))
                         + '\\n"); QUIT_GAP(1); fi;')
        for p in generators:
            need(sorted(p) == list(range(n)), 'invalid automorphism permutation')
            need({tuple(sorted((p[a], p[b]))) for a, b in graph['edges']}
                 == graph['edges'], 'invalid automorphism edge image')
        need(edge_orbit(graph['edges'], generators) == graph['edges'],
             'not edge transitive')
        orbit_sizes = sorted(Counter(orbits).values())
        need(len(orbit_sizes) == orbit_count, 'orbit count mismatch')
        need(orbit_sizes == ([n // 2, n // 2] if metadata['tr'] == 'SS' else [n]),
             'vertex orbit mismatch')
        if orbit_count == 1:
            arcs = graph['edges'] | {(b, a) for a, b in graph['edges']}
            computed_type = 'DT' if edge_orbit(arcs, generators, ordered=True) == arcs else 'HT'
        else:
            computed_type = 'SS'
        need(computed_type == metadata['tr'], 'symmetry type mismatch')
        # The automorphism stabilizer is computed in the full group.
        stabilizer = order // orbit_sizes[0]
        need(order % orbit_sizes[0] == 0 and stabilizer == metadata['vertex_stabilizer'],
             'vertex stabilizer mismatch')
        if not eligible(metadata):
            continue
        verified.append(dict(n=n, i=graph['i'], tr=metadata['tr'],
                             aut_order=order, vertex_stabilizer=stabilizer,
                             canonical_sha256=hashlib.sha256(canonical).hexdigest()))
    need(len(verified) == 397, 'selected data count')
    gap_lines.extend(['Print("PASS_EXACT_ORDERS_562\\n");', 'QUIT_GAP(0);'])
    gap_file = args.output.parent / 'group_orders.g'
    gap_file.write_text('\n'.join(gap_lines) + '\n')
    run = subprocess.run([args.gap, '-q', '-b', '-T', str(gap_file.resolve())],
                         capture_output=True, text=True, timeout=180)
    (args.output.parent / 'group_orders.stdout').write_text(run.stdout)
    (args.output.parent / 'group_orders.stderr').write_text(run.stderr)
    need(run.returncode == 0 and not run.stderr
         and run.stdout.strip() == 'PASS_EXACT_ORDERS_562', 'exact group-order child failed')
    result = dict(status='PASS_FINITE_CHECKS_WITH_EXPLICIT_EXTERNAL_PREMISES',
                  table_counts={name: len(tables[name]) for name in names},
                  selected_counts={name: len(selected[name]) for name in names},
                  selected_types={'DT': 272, 'SS': 125},
                  all_source_graphs=all_count, graphs_at_most150=small_count,
                  pairwise_nonisomorphic_bipartite_graphs_at_most150=len(keys),
                  historical_row_identifier_correspondence_claimed=False,
                  external_premises=['Each historical census entry is one distinct graph class',
                                     'The later census contains the earlier known graphs'],
                  old_identifier_map_inferred=False,
                  exact_group_orders_sha256=digest(gap_file),
                  exact_group_orders_stdout_sha256=digest(args.output.parent / 'group_orders.stdout'),
                  pynauty_version=pynauty.__version__,
                  selected_current_graphs=verified)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print('PASS: historical 397/397; current 397; 562 current classes distinct')


if __name__ == '__main__':
    main()
