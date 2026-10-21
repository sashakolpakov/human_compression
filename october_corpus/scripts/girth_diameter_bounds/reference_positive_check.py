#!/usr/bin/env python3
"""Independent bounded evidence checker. No author program imports.

NetworkX supplies a separate graph6/sparse6 parser and graph algorithms.
Optional native recount reuses the exact countg executable, not geng.
The large positive runs and their nonisomorphism checks are retained receipts.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import zipfile
import networkx as nx

AUTHOR_SHA = '9a0d33ed2203315134db573c42cbeff51cd7dc7f7f728b68db25546de86740bb'
PREDECESSOR_SHA = '836aeeae067a40dca373feaea245041c0ed39166dacbe2f4078f34a3b6ec077e'

def require(condition, message):
    if not condition:
        raise ValueError(message)

def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def load(path):
    return json.loads(path.read_text())

def key(r):
    return tuple(r[x] for x in ('k', 'g', 'd'))

def indexed(rows, getkey=key):
    out = {}
    for row in rows:
        k = getkey(row)
        require(k not in out, 'duplicate row')
        out[k] = row
    return out

def bound(k, g, diameter):
    # Moore balls are evaluated by breadth layers, not geometric closed forms.
    def ball(j):
        if j < 1:
            return 0
        layers = [1]
        if j % 2:
            for level in range(1, (j-1)//2+1):
                layers.append(k * (k-1)**(level-1))
            return sum(layers)
        return 2 * sum((k-1)**level for level in range(j//2))
    radius = g//2
    if diameter <= 2*radius:
        ordinary = ball(g) + ball(2*diameter-2*radius-1)
    else:
        remaining = diameter-2*radius-1
        number = 2
        while remaining >= g:
            number += 1
            remaining -= g
        ordinary = number*ball(g) + ball(remaining)
    if g % 2 == 0 and radius <= diameter <= 2*radius:
        h = diameter-radius-1
        layers = [] if h < 0 else [1] + [k*(k-1)**(i-1) for i in range(1, h+1)]
        strengthened = ball(g) + 2*max(sum(layers[::2]), sum(layers[1::2]))
        ordinary = max(ordinary, strengthened)
    return ordinary

def graph_properties(raw):
    raw = raw.strip()
    graph = nx.from_graph6_bytes(raw)
    require(nx.is_connected(graph), 'disconnected first witness')
    return graph, [len(graph), min(dict(graph.degree()).values()),
                   max(dict(graph.degree()).values()), nx.girth(graph),
                   nx.diameter(graph), int(nx.is_bipartite(graph))]

def positive_row(row, source, cells, iso_text, properties):
    k, g, d = key(source)
    target = [source['cage_order'], k, k, g, d]
    require(row['triple'] == [k,g,d] and row['order'] == target[0], 'positive route')
    require(row['supplied_path'] == source['supplied_path'] and
            row['supplied_sha256'] == source['supplied_sha256'], 'source input binding')
    require(cells == row['property_cells'] and bool(cells), 'property stdout')
    require(all(len(c)==7 and c[:5]==target and c[5] in (0,1) and c[6]>0 for c in cells), 'property cells')
    require(sum(c[-1] for c in cells)==source['cage_count']==row['graphs_checked'], 'positive count')
    all_bip = all(c[5] == 1 for c in cells)
    require(row['all_bipartite'] == all_bip, 'bipartite aggregation')
    expected_bip = source['bipartite_source_text']
    if expected_bip in ('Yes', 'All found graphs are bipartite'):
        require(all_bip, 'source bipartite claim')
    elif expected_bip == 'No':
        require(not all_bip, 'source nonuniversal bipartite claim')
    else:
        require(expected_bip == '', 'unrecognized bipartite qualifier')
    read = re.findall(r'>Z (\d+) graphs read from', iso_text)
    produced = re.findall(r'>Z (\d+) graphs produced', iso_text)
    require(read == produced == [str(source['cage_count'])], 'nonisomorphism receipt')
    require(row['pairwise_nonisomorphic'] is True, 'nonisomorphism status')
    require(row['minimum_order_established_here'] is False and
            row['exhaustiveness_established_here'] is False, 'positive evidence promoted to exhaustion')
    require(properties == row['independent_first_witness_properties'] and properties[:5]==target, 'first witness')

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--author', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--study-root', type=Path)
    ap.add_argument('--native-recount', action='store_true')
    a = ap.parse_args()
    p = a.author.resolve()
    a.out.mkdir(parents=True, exist_ok=False)
    own = Path(__file__).resolve().parent
    if (own/'manifest.json').exists():
        for f in load(own/'manifest.json')['exports']:
            require((own/f['path']).stat().st_size==f['bytes'] and sha(own/f['path'])==f['sha256'], 'review export '+f['path'])
    require(sha(p/'manifest.json') == AUTHOR_SHA, 'author manifest')
    manifest = load(p/'manifest.json')
    require(len(manifest['exports']) == 754, 'whole author boundary')
    exports = indexed(manifest['exports'], lambda x:x['path'])
    for name, rec in exports.items():
        require((p/name).stat().st_size==rec['bytes'] and sha(p/name)==rec['sha256'], 'export '+name)
    predecessors = list((p/'predecessor').glob('*.json'))
    require(len(predecessors)==1 and sha(predecessors[0])==PREDECESSOR_SHA, 'predecessor manifest')
    prior = load(predecessors[0])['exports']
    require(len(prior)==398 and all(exports[x['path']]==x for x in prior), '398-byte-boundary conservation')
    require(len(list(p.glob('positive_verification/*/*.first.g6')))==177 and
            len(list(p.glob('positive_verification/*/*.properties.txt')))==177, 'added witness/stdout closure')
    source = load(p/'source_tables.json')
    sources = indexed(source['rows'])
    routes = indexed(load(p/'supplied_graph_routes.json')['rows'])
    require(len(sources)==177 and sources.keys()==routes.keys(), '177 complete table routes')
    require(sum(not r['count_qualified_lower_bound'] for r in sources.values())==source['exact_count_claims']==123, 'count qualifiers')
    for k, r in routes.items():
        require(all(r[name]==value for name,value in sources[k].items()), 'unaltered source record')
    inventory = load(p/'source_software_inventory.json')
    input_files = indexed(inventory['exports'], lambda x:x['path'])
    require(len(input_files)==inventory['files']==201 and sum(x['bytes'] for x in input_files.values())==inventory['bytes']==263417838, 'whole source inventory')
    for r in routes.values():
        f = input_files[r['supplied_path']]
        require((f['sha256'],f['bytes'])==(r['supplied_sha256'],r['supplied_bytes']), 'supplied input inventory')
    if a.study_root:
        study = a.study_root.resolve()
        for f in input_files.values():
            path = study/'corpus106_F009_recovery'/f['path']
            require(path.stat().st_size==f['bytes'] and sha(path)==f['sha256'], 'full acquired input bytes')
        for f in load(p/'dependencies.json')['bindings']:
            path = study/f['path']
            require(path.stat().st_size==f['bytes'] and sha(path)==f['sha256'], 'retained source/layer premise')
    witnesses, seen, batch_sizes, cases = [], set(), [], []
    for batch in ('small','medium','large'):
        directory = p/'positive_verification'/batch
        report = load(directory/'report.json')
        require(report['whole_original_credit']==0 and report['verifier_sha256']==sha(p/'verify_supplied_graphs.py'), 'positive program/status')
        for name, f in report['programs'].items():
            require(sha(p/'native_tools'/name)==f['sha256'], 'native receipt executable')
        require(len(report['rows'])==report['row_count'] and sum(r['graphs_checked'] for r in report['rows'])==report['graph_count'], 'batch totals')
        batch_sizes.append(report['row_count'])
        for row in report['rows']:
            k = tuple(row['triple'])
            require(k not in seen and k in routes, 'positive partition')
            seen.add(k)
            r = routes[k]
            stem = f"n{r['cage_order']}_k{k[0]}_g{k[1]}_d{k[2]}"
            cells = [list(map(int,line.split())) for line in (directory/(stem+'.properties.txt')).read_text().splitlines() if line.strip()]
            iso = (directory/(stem+'.isomorphism.log')).read_text()
            graph, props = graph_properties((directory/(stem+'.first.g6')).read_bytes())
            positive_row(row,r,cells,iso,props)
            if a.study_root:
                path = study/'corpus106_F009_recovery'/r['supplied_path']
                if path.suffix=='.zip':
                    with zipfile.ZipFile(path) as z:
                        names = [name for name in z.namelist() if not name.endswith('/')]
                        require(len(names)==1, 'one source graph stream')
                        with z.open(names[0]) as f:
                            first = f.readline().strip()
                else:
                    with path.open('rb') as f:
                        first = f.readline().strip()
                original = nx.from_sparse6_bytes(first) if first.startswith(b':') else nx.from_graph6_bytes(first)
                require(set(original.edges())==set(graph.edges()) and set(original)==set(graph), 'source first witness equality')
            witnesses.append({'triple':list(k),'properties':props,'first_sha256':sha(directory/(stem+'.first.g6'))})
            cases.append((row,r,cells,iso,props))
    require(seen==sources.keys() and batch_sizes==[171,3,3], 'positive exact partition')
    require(sum(r['cage_count'] for r in sources.values())==31158706, 'positive total')
    reconciliation = load(p/'table_bound_reconciliation.json')
    recs = indexed(reconciliation['rows'], lambda x:tuple(x['triple']))
    require(recs.keys()==sources.keys() and reconciliation['source_sha256']==sha(p/'source_tables.json') and reconciliation['program_sha256']==sha(p/'verify_table_bounds.py'), 'bound interface')
    for k,r in sources.items():
        b = bound(*k)
        require(b==r['lower_bound']==recs[k]['proved_bound'] and recs[k]['feasible_order_bound']==b+(k[0]*b%2), 'bound formula/parity')
    small = load(p/'small_cubic/report.json')
    require(small['verifier_sha256']==sha(p/'cubic_small_exhaustion.py'), 'small verifier')
    counts, small_totals = {}, []
    for run in small['runs']:
        n = run['order']
        graphfile = p/'small_cubic'/run['graph_file']
        logfile = p/'small_cubic'/run['receipt_file']
        require(sha(graphfile)==run['graph_sha256'] and sha(logfile)==run['receipt_sha256'], 'small stream/receipt')
        number = sum(bool(line.strip()) for line in graphfile.open('rb'))
        require(re.findall(r'>Z (\d+) graphs generated in', logfile.read_text())==[str(number)] and number==run['graphs'], 'completed geng stream')
        require(run['command'][1:3]==['-cd3D3t',str(n)], 'complete connected cubic trianglefree command')
        cells = run['property_cells']
        if a.native_recount:
            result = subprocess.run([str(p/'native_tools/countg'),'-q','-1','--ndDgZb',str(graphfile)],capture_output=True,text=True,check=True)
            (a.out/f'order{n}.properties').write_text(result.stdout)
            require([list(map(int,line.split())) for line in result.stdout.splitlines() if line.strip()]==cells, 'fresh native small recount')
        require(sum(c[-1] for c in cells)==number and all(len(c)==7 and c[:3]==[n,3,3] and c[3]>=4 for c in cells), 'small cells')
        for _,_,_,g,d,bip,count in cells:
            counts[n,g,d] = counts.get((n,g,d),0)+count
        small_totals.append([n,number])
    require(small_totals==[[n,c] for n,c in zip(range(6,21,2),(1,2,6,22,110,792,7805,97546))] and sum(c for n,c in small_totals)==small['graph_count']==106284, 'small full boundary')
    recovered = indexed(small['rows'],lambda r:tuple(r['triple']))
    subset = {k:r for k,r in sources.items() if k[0]==3 and r['cage_order']<=20}
    require(len(subset)==small['source_rows_recovered']==15 and recovered.keys()==subset.keys(), 'bounded exact fifteen')
    for k,r in subset.items():
        n = r['cage_order']; g,d=k[1:]
        require(counts.get((n,g,d),0)==r['cage_count']==recovered[k]['complete_count'] and
                all(counts.get((m,g,d),0)==0 for m in range(6,n,2)) and
                recovered[k]['minimum_order']==n and recovered[k]['lower_even_orders_exhausted']==list(range(6,n,2)), 'small minima/counts')
    controls = []
    def rejects(name, call):
        try:
            call()
        except (ValueError, nx.NetworkXException):
            controls.append(name)
        else:
            raise ValueError('control accepted: '+name)
    row,r,cells,iso,props = cases[0]
    for field,value in [('graphs_checked',2),('minimum_order_established_here',True),('exhaustiveness_established_here',True),('pairwise_nonisomorphic',False),('all_bipartite',False),('supplied_sha256','0'*64)]:
        changed=copy.deepcopy(row);changed[field]=value
        rejects(field,lambda changed=changed:positive_row(changed,r,cells,iso,props))
    for column in range(7):
        changed=copy.deepcopy(cells);changed[0][column]+=1
        rejects('property_column_'+str(column),lambda changed=changed:positive_row(row,r,changed,iso,props))
    rejects('missing_iso_completion',lambda:positive_row(row,r,cells,iso.replace('graphs produced','incomplete'),props))
    rejects('wrong_diameter_witness',lambda:positive_row(row,r,cells,iso,props[:4]+[99]+props[5:]))
    rejects('duplicate_source_key',lambda:indexed(source['rows']+[source['rows'][0]]))
    rejects('disconnected_witness',lambda:graph_properties(nx.to_graph6_bytes(nx.disjoint_union(nx.cycle_graph(4),nx.cycle_graph(4)),header=False)))
    scope = load(p/'scope.json')
    require(scope['whole_original_credit']==0 and scope['source_complete_recovery'] is False and scope['new_formal_claim'] is False, 'bounded scientific scope')
    result = {'status':'PASS','author_manifest_sha256':AUTHOR_SHA,'author_exports':754,'unchanged_predecessor_exports':398,
              'positive_rows':177,'positive_graphs_in_reused_receipts':31158706,'independent_first_witnesses':177,
              'independent_formula_rows':177,'small_graphs':106284,'small_exact_rows':15,'small_stream_counts':small_totals,
              'fresh_native_small_recount':a.native_recount,'whole_external_input_hashes':201 if a.study_root else 0,
              'external_input_bytes':263417838,'source_first_witness_comparisons':177 if a.study_root else 0,
              'semantic_negative_controls':controls,'networkx_version':nx.__version__,
              'retained_scope':'Large positive/nonisomorphism receipts are not rerun; all native software correctness and geng completeness remain retained premises. Only fifteen rows receive bounded complete census status.',
              'whole_original_credit':0}
    (a.out/'witnesses.json').write_text(json.dumps(witnesses,indent=2)+'\n')
    (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
