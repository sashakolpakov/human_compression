"""Check primary LCF reconstruction and exact reuse of earlier graph inputs.

This verifies supplied data. Completeness of the graph classifications is a
separately attributed premise from the Conder--Potocnik census.
"""
from pathlib import Path
import collections
import argparse
import hashlib
import json
import re
import sys
import pynauty

if sys.flags.optimize:
    raise RuntimeError('optimized Python is unsupported')
parser = argparse.ArgumentParser()
parser.add_argument("--sources", type=Path, default=Path(__file__).resolve().parent)
parser.add_argument("--output", type=Path)
args = parser.parse_args()
W = args.sources.resolve()

def need(ok, message):
    if not ok:
        raise ValueError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def parse(path, prefix, cutoff):
    rows = []
    seen = set()
    for number, line in enumerate(path.read_text().splitlines(), 1):
        match = re.fullmatch(r'([!?]) (\d+) (\d+): \[(-?\d+(?:,-?\d+)*)\]\^(\d+)', line)
        missing = re.fullmatch(r'# (\d+) (\d+):', line)
        need(match is not None or missing is not None, f'grammar {path.name}:{number}')
        if match:
            _, ns, ix, shifts, power = match.groups()
            shifts = [int(x) for x in shifts.split(',')]
            power = int(power)
        else:
            ns, ix = missing.groups()
            shifts, power = None, None
        n = int(ns)
        name = f'{prefix}_{n}_{int(ix)}'
        need(name not in seen, f'duplicate primary identifier {name}')
        seen.add(name)
        if shifts is not None:
            need(len(shifts) * power == n, f'LCF repetition {name}')
        if n > cutoff:
            continue
        if shifts is None:
            need(name in {'CAT_10_1', 'CAT_28_1'}, f'unhandled placeholder {name}')
            if n == 10:
                edges = {(i, (i + 1) % 5) for i in range(5)}
                edges |= {(i + 5, (i + 2) % 5 + 5) for i in range(5)}
                edges |= {(i, i + 5) for i in range(5)}
            else:
                # Exact construction in Sage's retained CoxeterGraph source.
                edges = {(i, i + 1) for i in range(23)} | {(0, 23)}
                edges |= {(0,24),(2,25),(6,27),(7,24),(8,25),(10,26),
                          (14,27),(15,25),(16,26),(18,24),(22,27),(23,26),
                          (5,11),(9,20),(12,1),(13,19),(17,4),(3,21)}
        else:
            edges = {(i, (i + 1) % n) for i in range(n)}
            edges |= {(i, (i + shifts[i % len(shifts)]) % n) for i in range(n)}
        edges = {tuple(sorted(edge)) for edge in edges}
        need(len(edges) == 3*n//2 and all(a < b for a,b in edges), f'simple cubic edge count {name}')
        adjacency = {i: [] for i in range(n)}
        for a,b in edges:
            adjacency[a].append(b)
            adjacency[b].append(a)
        need(all(len(v) == 3 for v in adjacency.values()), f'degree {name}')
        colours = {0:0}
        queue = collections.deque([0])
        bipartite = True
        while queue:
            a = queue.popleft()
            for b in adjacency[a]:
                if b not in colours:
                    colours[b] = 1-colours[a]
                    queue.append(b)
                elif colours[b] == colours[a]:
                    bipartite = False
        need(len(colours) == n, f'connectedness {name}')
        rows.append({'id':name, 'n':n, 'edges':sorted(edges), 'bipartite':bipartite,
                     'line_number':number, 'lcf':shifts, 'power':power,
                     'primary_line_sha256':hashlib.sha256(line.encode()).hexdigest()})
    return rows, len(seen)

def graph(n, edges):
    adj = {i:[] for i in range(n)}
    for a,b in edges:
        adj[a].append(b)
        adj[b].append(a)
    return pynauty.Graph(n, adjacency_dict=adj)

cat, cat_total = parse(W/'CAT_lcf.txt', 'CAT', 2048)
css, css_total = parse(W/'CSS_lcf.txt', 'CSS', 768)
need((cat_total,css_total,len(cat),len(css)) == (3815,1043,796,43), 'primary scope counts')
bip = json.loads((W/'cubic_2048_bipartite.json').read_text())
nonbip = json.loads((W/'cubic_2048_nonbipartite.json').read_text())
inputs = json.loads((W/'cubic_markings/inputs.json').read_text())
old = {g['id']:g for g in inputs}
need(len(old) == len(inputs) == 304, 'earlier input identifiers')
retained = {g['id']:g for g in bip+nonbip+[g for g in inputs if g['family']=='semisymmetric']}
need(len(retained) == 839 and set(retained) == {g['id'] for g in cat+css}, 'scope identity')
seen = set()
records = []
for number, row in enumerate(cat+css, 1):
    name = row['id']
    saved = retained[name]
    need(row['n'] == saved['n'] and row['edges'] == sorted(tuple(e) for e in saved['edges']), f'exact edges {name}')
    if row['lcf'] is not None:
        need(row['lcf'] == saved['lcf'] and row['power'] == saved['power'], f'LCF metadata {name}')
    need(row['bipartite'] == (name.startswith('CSS_') or name in {g['id'] for g in bip}), f'bipartition {name}')
    G = graph(row['n'], row['edges'])
    certificate = pynauty.certificate(G)
    need(certificate not in seen, f'duplicate isomorphism class {name}')
    seen.add(certificate)
    record = {'id':name, 'n':row['n'], 'primary_line':row['line_number'],
              'primary_line_sha256':row['primary_line_sha256'],
              'canonical_sha256':hashlib.sha256(certificate).hexdigest()}
    if 'retained_id' in saved:
        prior = old[saved['retained_id']]
        H = graph(prior['n'], prior['edges'])
        need(pynauty.certificate(H) == certificate, f'reused graph class {name}')
        left, right = pynauty.canon_label(G), pynauty.canon_label(H)
        permutation = [None]*row['n']
        for a,b in zip(left,right):
            permutation[a] = b
        need(sorted(permutation) == list(range(row['n'])), f'reuse permutation {name}')
        image = {tuple(sorted((permutation[a],permutation[b]))) for a,b in row['edges']}
        need(image == {tuple(e) for e in prior['edges']}, f'explicit reuse isomorphism {name}')
        record.update(retained_id=saved['retained_id'], isomorphism=permutation)
    records.append(record)
    if number % 100 == 0:
        print('VERIFIED_PRIMARY_GRAPHS',number,flush=True)
need(sum('retained_id' in r for r in records) == 261, 'reuse count')
need(sha(W/'sage_smallgraphs_source.py') == '9f9b34048e99ec9e85d3dffde4e76a6f7ea533c8c2f518efaa807363d0e4cdd9', 'Coxeter source')
report = {'status':'PASS', 'classification_completeness':'borrowed primary census premise',
          'symmetric_scope':796, 'symmetric_bipartite':714, 'symmetric_nonbipartite':82,
          'semisymmetric_scope':43, 'distinct_classes':839, 'explicit_reuse_isomorphisms':261,
          'pynauty_version':pynauty.__version__,
          'inputs':{p:sha(W/p) for p in ['CAT_lcf.txt','CSS_lcf.txt','foster_primary.html',
                     'sage_smallgraphs_source.py','cubic_2048_bipartite.json',
                     'cubic_2048_nonbipartite.json','cubic_markings/inputs.json']},
          'checker_sha256':sha(Path(__file__)), 'graphs':records}
(args.output or W/'cubic_source_verification.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS_PRIMARY_CUBIC_SOURCES_839_REUSE_261',flush=True)
