#!/usr/bin/env python3
"""Construct the complete mod-2 locally faithful coset-complex cover."""
import argparse,itertools,json,pathlib
from phase246_parallel_edges import need,mul,generated,analyze

def reduce2(v,basis):
    while v:
        k=(v&-v).bit_length()-1
        if k not in basis:return v
        v^=basis[k]
    return 0

def cover(model):
    degree=model['degree'];ss=[tuple(x-1 for x in s) for s in model['generators']]
    group,index=generated(ss,degree);n=len(group);one=tuple(range(degree))
    def subgroup(ids):return set(generated([ss[i] for i in ids],degree)[0])
    A=subgroup([0,1,2]);B=subgroup([1,2,3]);C=subgroup([1,2])
    def cosets(H):
        labels={};reps=[]
        for g in group:
            if g not in labels:
                k=len(reps);reps.append(g)
                for h in H:labels[mul(h,g)]=k
        return labels,reps
    la,ra=cosets(A);lb,rb=cosets(B);lc,rc=cosets(C)
    endpoints=[(la[g],len(ra)+lb[g]) for g in rc];nv=len(ra)+len(rb)
    adj=[[] for _ in range(nv)]
    for e,(u,v) in enumerate(endpoints):adj[u].append((v,e));adj[v].append((u,e))
    tree_edges=set();parent={0:None};queue=[0]
    for u in queue:
        for v,e in adj[u]:
            if v not in parent:parent[v]=(u,e);tree_edges.add(e);queue.append(v)
    need(len(parent)==nv,'connected Bass-Serre quotient graph')
    chords=[e for e in range(len(rc)) if e not in tree_edges];ci={e:i for i,e in enumerate(chords)}
    def chord(e):return 1<<ci[e] if e in ci else 0
    # Tree paths have zero chord coordinates. Cellular boundaries are cycles.
    basis={}
    for g in group:
        h=mul(ss[0],g);k=mul(ss[3],g);l=mul(ss[0],k)
        z=chord(lc[g])^chord(lc[h])^chord(lc[k])^chord(lc[l]);z=reduce2(z,basis)
        if z:basis[(z&-z).bit_length()-1]=z
    free=[k for k in range(len(chords)) if k not in basis];b=len(free)
    need(b<12,'bounded concrete cover size')
    def quotient(z):
        # Unlike insertion, complete normal reduction may retain a free pivot
        # before a later occupied pivot, so process every occupied pivot.
        for k in sorted(basis):
            if (z>>k)&1:z^=basis[k]
        need(all(not((z>>k)&1) for k in basis),'quotient normal form')
        return sum(((z>>k)&1)<<i for i,k in enumerate(free))
    perms=[]
    for i,s in enumerate(ss):
        transitions=[]
        for g in group:
            h=mul(s,g);v=quotient(chord(lc[g])^chord(lc[h])) if i==3 else 0
            transitions.append((index[h],v))
        perm=[0]*(n*(1<<b))
        for a in range(1<<b):
            for j,(k,v) in enumerate(transitions):perm[a*n+j]=((a^v)*n+k)+1
        need(sorted(perm)==list(range(1,len(perm)+1)),'voltage permutations')
        perms.append(perm)
    # Every check below is on the actually exported permutations.
    p0=[x-1 for x in perms[0]];p1=[x-1 for x in perms[1]];p2=[x-1 for x in perms[2]];p3=[x-1 for x in perms[3]]
    ps=[p0,p1,p2,p3]
    need(all(all(p[p[j]]==j for j in range(len(p))) for p in ps),'lifted involutions')
    need(all(all(ps[i][ps[j][k]]==ps[j][ps[i][k]] for k in range(len(p0))) for i,j in [(0,2),(0,3),(1,3)]),'lifted string commutations')
    return dict(name=model.get('name'),degree=n*(1<<b),base_order=n,kernel_dimension=b,base_degree=degree,base_generators=model['generators'],generators=perms,
                source='mod-2 homology of the end-coset square complex')

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--input',type=pathlib.Path,required=True);ap.add_argument('--index',type=int);ap.add_argument('--out',type=pathlib.Path,required=True);a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'fresh output')
    m=json.loads(a.input.read_text());m=m if a.index is None else m[a.index]
    r=cover(m);a.out.write_text(json.dumps(r)+'\n');print(json.dumps({k:v for k,v in r.items() if 'generators' not in k}))
