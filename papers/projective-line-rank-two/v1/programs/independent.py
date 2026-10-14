"""Independent global pair orbits, explicit uniform graphs and scalar orbits.

No author-program import. The only candidate data read are literal permutations
in the fresh GAP output; all group and orbit operations below use Python.
"""
import sys
if sys.flags.optimize:
    raise RuntimeError('Ordinary Python required')
from pathlib import Path
from collections import deque
from itertools import combinations, product
import argparse, hashlib, json, re

def closure(gens):
    n=len(gens[0]); one=tuple(range(n)); seen={one}; stack=[one]
    while stack:
        x=stack.pop()
        for g in gens:
            y=tuple(g[x[i]] for i in range(n))
            if y not in seen: seen.add(y);stack.append(y)
    return frozenset(seen)

def conjugate(H,g):
    inv=[0]*len(g)
    for i,j in enumerate(g):inv[j]=i
    return frozenset(tuple(g[h[inv[i]]] for i in range(len(g))) for h in H)

def pair_orbits(row):
    q,gs,hs,*_=row
    gens=[tuple(x-1 for x in g)for g in gs]
    H=closure([tuple(x-1 for x in h)for h in hs]);G=closure(gens)
    assert len(G)==q*(q*q-1)//2 and len(H)==12 and H<=G
    family=[H];indices={H:0}
    for J in family:
        for g in gens:
            K=conjugate(J,g)
            if K not in indices:indices[K]=len(family);family.append(K)
    actions=[[indices[conjugate(J,g)]for J in family]for g in gens]
    eligible={(i,j)for i,J in enumerate(family)for j,K in enumerate(family)if i!=j and len(J&K)==4}
    assert len(family)==len(G)//12 and len(eligible)==len(family)*6
    def orbit_sizes(points,unordered):
        unseen=set(points);sizes=[]
        while unseen:
            seed=next(iter(unseen));unseen.remove(seed);queue=[seed];count=0
            for i,j in queue:
                count+=1
                for a in actions:
                    k=(a[i],a[j]);k=tuple(sorted(k))if unordered else k
                    assert k in points
                    if k in unseen:unseen.remove(k);queue.append(k)
            sizes.append(count)
        return sorted(sizes)
    ordered=orbit_sizes(eligible,False)
    unordered=orbit_sizes({tuple(sorted(x))for x in eligible},True)
    assert ordered==[len(G)//4]*2 and unordered==[len(G)//4]
    return dict(q=q,group_order=len(G),torus_subgroups=len(family),eligible_ordered_pairs=len(eligible),ordered_orbits=ordered,unordered_orbits=unordered)

def field(q,poly):
    def mul(a,b):
        c=0
        while b:
            if b&1:c^=a
            b>>=1;a<<=1
            if a&q:a^=poly
        return c
    table=[[mul(a,b)for b in range(q)]for a in range(q)]
    assert all(sorted(row)==list(range(q))for row in table[1:])
    inv=[None]+[table[a].index(1)for a in range(1,q)]
    return table,inv

def uniform(q,poly):
    table,inv=field(q,poly);n=q+1;points=list(range(n));inf=q
    matrices=[(1,b,c,d)for b,c,d in product(range(q),repeat=3)if d^table[b][c]]
    matrices += [(0,1,c,d)for c in range(1,q)for d in range(q)]
    G=[]
    for a,b,c,d in matrices:
        images=[]
        for x in points:
            numerator,denominator=(a,c)if x==inf else(table[a][x]^b,table[c][x]^d)
            images.append(inf if not denominator else table[numerator][inv[denominator]])
        g=tuple(images);assert sorted(g)==points;G.append(g)
    assert len(set(G))==len(G)==q*(q*q-1)
    def invariants(adj,actions,roots):
        depths=[];ecc=[]
        for root in roots:
            dist={root:0};queue=deque([root])
            while queue:
                x=queue.popleft()
                for y in adj[x]:
                    if y not in dist:dist[y]=dist[x]+1;queue.append(y)
            assert len(dist)==len(adj);ecc.append(max(dist.values()))
            stabilizer=[g for g in actions if g[root]==root];path=[root];depth=0
            while depth<10:
                choices=adj[path[-1]]-({path[-2]}if len(path)>1 else set())
                x=min(choices);orbit={g[x]for g in stabilizer}
                if orbit!=choices:break
                path.append(x);stabilizer=[g for g in stabilizer if g[x]==x];depth+=1
            assert depth<10;depths.append(depth)
        return dict(local_arc_depths=depths,type_diameters=ecc)
    adj=[set()for _ in range(2*n)]
    for a in points:
        for b in points:
            if a!=b:adj[a].add(n+b);adj[n+b].add(a)
    doubled=[g+tuple(n+x for x in g)for g in G]
    one=invariants(adj,doubled,[0,n]);assert one==dict(local_arc_depths=[2,2],type_diameters=[3,3])
    edges=list(combinations(points,2));ei={e:n+i for i,e in enumerate(edges)}
    adj=[set()for _ in range(n+len(edges))]
    for e,j in ei.items():
        for p in e:adj[p].add(j);adj[j].add(p)
    actions=[g+tuple(ei[tuple(sorted((g[a],g[b])))]for a,b in edges)for g in G]
    two=invariants(adj,actions,[0,n]);assert two==dict(local_arc_depths=[4,3],type_diameters=[3,4])
    return dict(q=q,explicit_projective_group=len(G),double_graph=one,point_pair_graph=two)

def scalars():
    table,_=field(64,0b1000011)
    planes={frozenset((0,a,b,a^b))for a in range(1,64)for b in range(a+1,64)}
    assert len(planes)==651
    spaces=set()
    for plane in planes:
        basis=[x for x in plane if x][:2]
        spaces.add(frozenset(x for x in range(64)if all((x&b).bit_count()%2==0 for b in basis)))
    assert len(spaces)==651 and all(len(T)==16 for T in spaces)
    unseen=set(spaces);orbits=[];stabilizers=[]
    while unseen:
        T=next(iter(unseen));orbit={frozenset(table[a][x]for x in T)for a in range(1,64)}
        assert orbit<=spaces and orbit<=unseen;unseen-=orbit
        stab=[a for a in range(1,64)if frozenset(table[a][x]for x in T)==T]
        assert len(orbit)*len(stab)==63;orbits.append(len(orbit));stabilizers.append(len(stab))
    assert sorted(orbits)==[21]+[63]*10 and sorted(stabilizers)==[1]*10+[3]
    return dict(four_dimensional_subspaces=651,scalar_orbit_lengths=sorted(orbits),scalar_stabilizers=sorted(stabilizers))

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    assert not a.out.exists();text=a.input.read_text();rows=[json.loads(x)for x in re.findall(r'(?:^|\n)SWAP\s+(.*?)\nEND_SWAP',text,re.S)]
    unique={x[0]:x for x in rows};assert sorted(unique)==[11,13]
    report=dict(status='PASS_INDEPENDENT_L076_GLOBAL_ORBITS_AND_MODELS',input_sha256=hashlib.sha256(a.input.read_bytes()).hexdigest(),pair_orbits=[pair_orbits(unique[q])for q in sorted(unique)],uniform_graphs=[uniform(q,p)for q,p in [(4,7),(8,11),(16,19)]],scalar_orbits=scalars(),author_programs_imported=False,target_classification_rerun=False)
    a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
