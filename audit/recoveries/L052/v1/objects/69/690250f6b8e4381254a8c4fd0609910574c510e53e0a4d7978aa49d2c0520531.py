"""Literal small geometries and subgroup checks, independent of author code."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Optimized execution is not supported')
import itertools
import json
from pathlib import Path

def need(x, msg):
    if not x: raise ValueError(msg)

def mul(a,b): return tuple(a[b[i]] for i in range(len(a)))
def inv(a): return tuple(a.index(i) for i in range(len(a)))
def closure(gens,n):
    e=tuple(range(n)); seen={e}; todo=[e]
    while todo:
        a=todo.pop()
        for b in gens:
            c=mul(a,b)
            if c not in seen:seen.add(c);todo.append(c)
    return frozenset(seen)
def product(A,B):return frozenset(mul(a,b) for a in A for b in B)
def leftcosets(G,H):return frozenset(frozenset(mul(g,h) for h in H) for g in G)
def rightcosets(G,H):return frozenset(frozenset(mul(h,g) for h in H) for g in G)
def face(g,F):return frozenset(g[i] for i in F)
def chamber(g,C):return tuple(face(g,F) for F in C)

def geometry(name,rhos,C):
    n=len(rhos[0]);e=tuple(range(n));r=len(rhos)
    G=closure(rhos,n);Ch=frozenset(chamber(g,C) for g in G)
    need(len(Ch)==len(G),'Regular actual chamber action')
    def adjacent(D,i):
        xs=[E for E in Ch if E!=D and all(E[j]==D[j] for j in range(r) if j!=i)]
        need(len(xs)==1,'Thin actual geometry');return xs[0]
    for i in range(r):need(chamber(rhos[i],C)==adjacent(C,i),'Actual left generator')
    subsets=[set(i for i in range(r) if mask>>i&1) for mask in range(1<<r)]
    regular=0
    for S in subsets:
        H=closure([rhos[i] for i in S],n)
        K={g for g in G if all(face(g,C[j])==C[j] for j in range(r) if j not in S)}
        need(H==K,'Regular literal residue stabilizer');regular+=1
    alphas=[e]+[mul(rhos[0],rhos[i]) for i in range(1,r)]
    H=closure(alphas,n);need(len(G)==2*len(H),'Actual two-orbit subgroup')
    hs={}
    for i,j in itertools.product(range(r),repeat=2):
        a=mul(inv(alphas[i]),alphas[j])
        need(chamber(a,C)==adjacent(adjacent(C,i),j),'Left two-step identity')
    for S in subsets:
        T=closure([mul(inv(alphas[i]),alphas[j]) for i in S for j in S],n)
        K={g for g in H if all(face(g,C[j])==C[j] for j in range(r) if j not in S)}
        need(T==K,'Even literal residue stabilizer');hs[frozenset(S)]=T
    parabolics=[hs[frozenset(set(range(r))-{i})] for i in range(r)]
    cosets=[leftcosets(H,P) for P in parabolics]
    coset_chambers=[tuple(D) for D in itertools.product(*cosets) if all(D[i]&D[j] for i in range(r) for j in range(i))]
    actual_maps=[]
    for i in range(r):
        mapping={K:face(next(iter(K)),C[i]) for K in cosets[i]}
        need(len(set(mapping.values()))==len(mapping),'Actual object bijection')
        actual_maps.append(mapping)
    need({tuple(actual_maps[i][D[i]] for i in range(r)) for D in coset_chambers}==Ch,'All coset chambers reconstructed')
    C0=adjacent(C,0)
    coordinates={chamber(g,C):(g,1) for g in H}
    coordinates.update({chamber(g,C0):(g,-1) for g in H})
    need(len(coordinates)==len(Ch),'Exactly two free orbits')
    for g in H:
        for i in range(r):
            need(adjacent(chamber(g,C),i)==chamber(mul(g,inv(alphas[i])),C0),'Exact coordinate adjacency')
    theta=lambda g:mul(mul(rhos[0],g),rhos[0])
    need(all(theta(a)==inv(a) for a in alphas),'Marked inversion')
    flips={D:chamber(theta(g),C0 if sign==1 else C) for D,(g,sign) in coordinates.items()}
    need(all(flips[flips[D]]==D and flips[D]!=D for D in Ch),'Nontrivial order-two geometric flip')
    need(all(flips[adjacent(D,i)]==adjacent(flips[D],i) for D in Ch for i in range(r)),'Full colour-preserving reflection')
    theta_identity=all(theta(g)==g for g in H)
    return dict(model=name,group_order=len(G),even_order=len(H),chambers=len(Ch),regular_stabilizers=regular,even_stabilizers=len(subsets),two_step_identities=r*r,coordinate_edges=len(H)*r,theta_is_identity=theta_identity,geometric_flip_nontrivial=True)

def helly():
    n=3;e=tuple(range(n));G=frozenset(itertools.permutations(range(n)))
    sub={closure([],n)};todo=list(sub)
    while todo:
        H=todo.pop()
        for x in G-H:
            K=closure(list(H)+[x],n)
            if K not in sub:sub.add(K);todo.append(K)
    triples=0;coset_triples=0
    for A,B,D in itertools.product(sub,repeat=3):
        one=product(A,B)&product(A,D)==product(A,B&D)
        two=product(A&B,A&D)==A&product(B,D)
        three=True
        for a,b,d in itertools.product(rightcosets(G,A),rightcosets(G,B),rightcosets(G,D)):
            coset_triples+=1
            if a&b and a&d and b&d and not a&b&d:three=False
        need(one==two==three,'All three literal Helly conditions');triples+=1
    return dict(group='S3',subgroups=len(sub),subgroup_triples=triples,right_coset_triples=coset_triples)

def main():
    e=tuple(range(4));rs=[]
    for i in range(3):
        a=list(e);a[i],a[i+1]=a[i+1],a[i];rs.append(tuple(a))
    simplex=geometry('tetrahedron actual flags',rs,tuple(frozenset(range(i+1)) for i in range(3)))
    es=tuple(range(6));rs=[]
    for i in range(3):
        a=list(es);a[2*i],a[2*i+1]=a[2*i+1],a[2*i];rs.append(tuple(a))
    digons=geometry('three independent two-object types',rs,tuple(frozenset({2*i}) for i in range(3)))
    need(digons['theta_is_identity'],'Explicit identity-action edge case')
    report=dict(status='PASS_INDEPENDENT_L052_SMALL_CONTROLS',geometries=[simplex,digons],helly=helly(),author_code_imported=False,proof_by_sampling_claimed=False)
    out=Path(__file__).parent/'controls_report.json';out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':main()
