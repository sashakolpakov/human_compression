"""Replay the L059 input certificate without full upstream source files.

The numeric roster records 796 symmetric cubic inputs and 43 semisymmetric
cubic inputs. Completeness is the same attributed census premise retained
in the principal manuscript. This program proves neither census completeness
nor the graph automorphism/marking classifications.
"""
from pathlib import Path
import argparse
import collections
import gzip
import hashlib
import json
import sys
import pynauty

if sys.flags.optimize:
    raise RuntimeError('optimized Python is unsupported')

def need(ok, message):
    if not ok:
        raise ValueError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def load(path):
    # Publication may store a byte-identical input compressed with gzip.
    if path.is_file():
        raw = path.read_bytes()
    else:
        raw = gzip.decompress(Path(str(path)+'.gz').read_bytes())
    return json.loads(raw), digest(raw)

def graph(n, edges):
    adjacency = {i: [] for i in range(n)}
    for a, b in edges:
        adjacency[a].append(b)
        adjacency[b].append(a)
    return pynauty.Graph(n, adjacency_dict=adjacency)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--derived', type=Path, required=True)
    parser.add_argument('--roster', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    need(not args.output.exists(), 'refuse to replace an existing replay')
    roster, roster_sha = load(args.roster/'numeric_roster.json')
    reuse_rows, reuse_sha = load(args.roster/'reuse_isomorphisms.json')
    provenance, _ = load(args.roster/'extraction_provenance.json')
    pins = {x['path']: x['sha256'] for x in provenance['outputs']}
    need(pins == {'numeric_roster.json': roster_sha, 'reuse_isomorphisms.json': reuse_sha},
         'acquired numeric inputs')
    acquired = {}
    inputs = {}
    for binding in provenance['derived_inputs']:
        value, sha = load(args.derived/binding['path'])
        need(sha == binding['sha256'], 'exact derived bytes '+binding['path'])
        acquired[binding['path']] = sha
        inputs[binding['path']] = value
    bip = inputs['cubic_2048_bipartite.json']
    nonbip = inputs['cubic_2048_nonbipartite.json']
    earlier = inputs['cubic_markings/inputs.json']
    old = {g['id']: g for g in earlier}
    retained_rows = bip + nonbip + [g for g in earlier if g['family'] == 'semisymmetric']
    retained = {g['id']: g for g in retained_rows}
    reuse = {g['id']: g for g in reuse_rows}
    need(len(earlier) == len(old) == 304 and len(retained_rows) == len(retained) == 839,
         'unique derived input identifiers')
    need(len(reuse_rows) == len(reuse) == 261, 'unique reuse identifiers')
    need(len(roster) == 839 and len({g['id'] for g in roster}) == 839 and
         set(retained) == {g['id'] for g in roster}, 'exact roster scope')
    need(sum(g['id'].startswith('CAT_') for g in roster) == 796 and
         sum(g['id'].startswith('CSS_') for g in roster) == 43, 'family counts')
    bip_names = {g['id'] for g in bip}
    seen, used_maps, records = set(), set(), []
    for row in roster:
        name, n = row['id'], row['n']
        prefix = name.split('_')[0]
        need(prefix in {'CAT', 'CSS'} and name == f"{prefix}_{n}_{row['index']}", 'identifier')
        need(0 < n <= (2048 if prefix == 'CAT' else 768) and n % 2 == 0, 'cutoff')
        shifts, power = row['lcf'], row['power']
        if row['construction'] == 'lcf':
            need(isinstance(shifts, list) and shifts and all(type(x) is int for x in shifts)
                 and type(power) is int and power > 0 and len(shifts)*power == n, 'LCF shape')
            need(row['marker'] in {'!', '?'}, 'LCF source marker')
            line = f"{row['marker']} {n} {row['index']}: [" + ','.join(map(str, shifts)) + f']^{power}'
            edges = {(i, (i+1) % n) for i in range(n)}
            edges |= {(i, (i+shifts[i % len(shifts)]) % n) for i in range(n)}
        else:
            need(shifts is None and power is None and row['marker'] == '#', 'placeholder form')
            line = f"# {n} {row['index']}:"
            if row['construction'] == 'petersen':
                need(name == 'CAT_10_1', 'Petersen identifier')
                edges = {(i, (i+1) % 5) for i in range(5)}
                edges |= {(i+5, (i+2) % 5+5) for i in range(5)}
                edges |= {(i, i+5) for i in range(5)}
            else:
                need(row['construction'] == 'coxeter' and name == 'CAT_28_1', 'Coxeter identifier')
                # Numeric construction already checked against the retained Sage source.
                edges = {(i, i+1) for i in range(23)} | {(0, 23)}
                edges |= {(0,24),(2,25),(6,27),(7,24),(8,25),(10,26),
                          (14,27),(15,25),(16,26),(18,24),(22,27),(23,26),
                          (5,11),(9,20),(12,1),(13,19),(17,4),(3,21)}
        need(digest(line.encode()) == row['primary_line_sha256'], 'exact primary numeric line')
        edges = {tuple(sorted(edge)) for edge in edges}
        need(len(edges) == 3*n//2 and all(0 <= a < b < n for a,b in edges), 'simple cubic edges')
        adjacency = {i: [] for i in range(n)}
        for a,b in edges:
            adjacency[a].append(b)
            adjacency[b].append(a)
        need(all(len(v) == 3 for v in adjacency.values()), 'cubic degrees')
        colours, queue, bipartite = {0: 0}, collections.deque([0]), True
        while queue:
            a = queue.popleft()
            for b in adjacency[a]:
                if b not in colours:
                    colours[b] = 1-colours[a]
                    queue.append(b)
                elif colours[b] == colours[a]:
                    bipartite = False
        need(len(colours) == n, 'connectedness')
        saved = retained[name]
        need(saved['n'] == n and edges == {tuple(e) for e in saved['edges']}, 'retained exact graph')
        if shifts is not None:
            need(shifts == saved['lcf'] and power == saved['power'], 'retained LCF metadata')
        need(bipartite == (prefix == 'CSS' or name in bip_names), 'bipartition')
        certificate = pynauty.certificate(graph(n, edges))
        need(certificate not in seen, 'repeated isomorphism class')
        seen.add(certificate)
        record = {'id': name, 'n': n, 'primary_line': row['primary_line'],
                  'primary_line_sha256': row['primary_line_sha256'],
                  'canonical_sha256': digest(certificate)}
        if 'retained_id' in saved:
            need(name in reuse, 'missing reuse map')
            match = reuse[name]
            need(match['retained_id'] == saved['retained_id'] and match['n'] == n, 'reuse endpoint')
            permutation = match['isomorphism']
            need(len(permutation) == n and sorted(permutation) == list(range(n)), 'reuse permutation')
            prior = old[saved['retained_id']]
            need(prior['n'] == n, 'earlier degree')
            image = {tuple(sorted((permutation[a], permutation[b]))) for a,b in edges}
            need(image == {tuple(e) for e in prior['edges']}, 'actual reuse isomorphism')
            record.update(retained_id=saved['retained_id'], isomorphism=permutation)
            used_maps.add(name)
        records.append(record)
    need(used_maps == set(reuse), 'all and only the 261 reuse maps')
    report = {'status': 'PASS_PUBLIC_NUMERIC_INPUTS_839_REUSE_261',
              'classification_completeness': 'borrowed primary census premise',
              'distinct_classes': len(seen), 'explicit_reuse_isomorphisms': len(used_maps),
              'symmetric_scope': 796, 'semisymmetric_scope': 43,
              'symmetric_bipartite': len(bip), 'symmetric_nonbipartite': len(nonbip),
              'numeric_roster_sha256': roster_sha, 'reuse_isomorphisms_sha256': reuse_sha,
              'derived_inputs': acquired, 'checker_sha256': digest(Path(__file__).read_bytes()),
              'pynauty_version': pynauty.__version__, 'graphs': records,
              'full_upstream_files_read': False}
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print('PASS_PUBLIC_NUMERIC_INPUTS_839_REUSE_261')

if __name__ == '__main__':
    main()
