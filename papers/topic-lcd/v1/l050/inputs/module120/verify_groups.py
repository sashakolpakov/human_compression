#!/usr/bin/env python3
"""Elementary full code-automorphism bound from all minimum supports."""
import argparse
import collections
import json
import math
from pathlib import Path


def need(x, message):
    if not x:
        raise ValueError(message)


def refine(adj, colors):
    while True:
        signatures = [(colors[v], tuple(sorted(collections.Counter(colors[w] for w in adj[v]).items())))
                      for v in range(len(adj))]
        labels = {x:i for i,x in enumerate(sorted(set(signatures)))}
        new = [labels[x] for x in signatures]
        if len(labels) == len(set(colors)):
            return new
        colors = new


def inspect(constructed, support_data):
    supports = {tuple(v-1 for v in s) for s in support_data['supports']}
    need(len(supports)==630 and all(len(set(s))==48 and min(s)>=0 and max(s)<120 for s in supports), 'support data')
    supports = sorted(supports)
    adj = [[] for _ in range(750)]
    for i,s in enumerate(supports):
        for v in s:
            adj[v].append(120+i)
            adj[120+i].append(v)
    colors = [0]*120+[1]*630
    chain=[]
    while True:
        colors=refine(adj,colors)
        cells=collections.defaultdict(list)
        for v in range(120):
            cells[colors[v]].append(v)
        choices=[s for s in cells.values() if len(s)>1]
        if not choices:
            break
        cell=min(choices,key=lambda s:(len(s),s))
        chain.append([cell[0]+1,len(cell)])
        colors[cell[0]]=max(colors)+1
    need(chain==[[1,120],[6,21],[48,2],[10,4],[2,2],[3,2]], 'complete refinement chain')
    upper=math.prod(c for v,c in chain)
    need(upper==80640 and len(set(colors[:120]))==120, 'full upper bound')
    generators=[tuple(v-1 for v in row) for row in constructed['full_generators']]
    need(support_data['coordinate_generators']==constructed['full_generators'], 'same literal generators')
    support_set=set(supports)
    for g in generators:
        need(len(g)==120 and set(g)==set(range(120)), 'permutation generator')
        need({tuple(sorted(g[v] for v in s)) for s in supports}==support_set, 'minimum support action')
        for name in ['K_basis','N_basis']:
            basis=constructed[name]
            pivots=[next(i for i,x in enumerate(row) if x) for row in basis]
            need(all([row[i] for i in pivots]==[int(k==j) for j in range(len(basis))]
                     for k,row in enumerate(basis)), 'certified echelon basis')
            for row in basis:
                image=[0]*120
                for i,x in enumerate(row):
                    image[g[i]]=x
                recovered=[sum(image[pivots[i]]*basis[i][j] for i in range(len(basis)))%3 for j in range(120)]
                need(recovered==image,'code invariance')
    identity=tuple(range(120))
    seen={identity};todo=collections.deque([identity])
    while todo:
        p=todo.popleft()
        for g in generators:
            q=tuple(g[p[i]] for i in range(120))
            if q not in seen:
                seen.add(q)
                need(len(seen)<=upper,'lower group exceeds upper bound')
                todo.append(q)
    need(len(seen)==upper,'subgroup does not attain full upper bound')
    return {'status':'PASS','minimum_supports':630,'coordinate_vertices':120,
            'refinement_chain':chain,'full_upper_bound':upper,
            'explicit_permutation_group_order':len(seen),'both_codes_invariant':True,
            'no_graph_isomorphism_backend':True}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--constructed',type=Path,required=True)
    p.add_argument('--supports',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    result=inspect(json.loads(a.constructed.read_text()),json.loads(a.supports.read_text()))
    a.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':
    main()
