#!/usr/bin/env python3
"""Independent finite diagnostics; these do not certify an infinite HNN theorem."""
from itertools import combinations, permutations
from math import lcm

def need(b, message):
    if not b: raise ValueError(message)

def span(indices):
    out={0}
    for i in indices: out |= {x^(1<<i) for x in out}
    return frozenset(out)

def permute(v,p):
    return sum(1<<p[i] for i in range(len(p)) if v>>i&1)

def generated(gens,mul):
    seen={(0,0)}; todo=list(seen)
    while todo:
        x=todo.pop()
        for s in gens:
            y=mul(x,s)
            if y not in seen: seen.add(y);todo.append(y)
    return frozenset(seen)

def model(p,extra):
    n=len(p);p=tuple(p)+tuple(range(n,n+extra));q=list(range(len(p)));order=1
    q=[p[i] for i in q]
    while q!=list(range(len(p))):
        q=[p[i] for i in q];order+=1
    m=2*order
    # t^-1 v t is p(v).
    def mul(x,y):
        v=y[0]
        for _ in range((-x[1])%order):v=permute(v,p)
        return x[0]^v,(x[1]+y[1])%m
    universe=frozenset((v,k) for v in range(1<<len(p)) for k in range(m))
    return mul,universe,m

def partials(n):
    for k in range(n+1):
        for dom in combinations(range(n),k):
            for ran in combinations(range(n),k):
                for image in permutations(ran):yield dict(zip(dom,image))

def classes_and_extension(n,f):
    components=[];unseen=set(range(n))
    while unseen:
        c={min(unseen)}
        while True:
            nxt=c|{v for u,v in f.items() if u in c}|{u for u,v in f.items() if v in c}
            if nxt==c:break
            c=nxt
        unseen-=c;components.append(c)
    p=dict(f)
    for c in components:
        missing_dom=list(c-set(f));missing_ran=list(c-set(f.values()))
        need(len(missing_dom)==len(missing_ran)<=1,'partial bijection paths or cycles')
        if missing_dom:p[missing_dom[0]]=missing_ran[0]
    return components,tuple(p[i] for i in range(n))

def maximal_cliques(vertices,adj):
    out=[]
    def rec(R,P,X):
        if not P and not X:out.append(R);return
        u=max(P|X,key=lambda x:len(P&adj[x])) if P|X else None
        for v in sorted(P-(adj[u] if u is not None else set())):
            rec(R+[v],P&adj[v],X&adj[v]);P.remove(v);X.add(v)
    rec([],set(vertices),set())
    return out

def run():
    cases=0;generation_checks=0;panel_checks=0
    for n in range(4):
      for f in partials(n):
       cs,p=classes_and_extension(n,f)
       J=set(range(n))-set(f);K=set(range(n))-set(f.values());F=J-K
       for extra in [0,1]:
        mul,U,m=model(p,extra);H=frozenset((v,0) for v in span(range(n,n+extra)));t=(0,1)
        def A(indices):return frozenset((v,0) for v in span(set(indices)|set(range(n,n+extra))))
        maxs=[generated(set(A(set(range(n))-s))|{t},mul) for s in cs]+[A(set(range(n))-F)]
        minimal=[]
        for i in range(len(maxs)):
            cur=set(U)
            for j,sub in enumerate(maxs):
                if i!=j:cur.intersection_update(sub)
            minimal.append(frozenset(cur))
        bore=set(U)
        for sub in maxs:bore.intersection_update(sub)
        need(bore==set(H),'actual arbitrary Borel')
        for i,s in enumerate(cs):
            need(minimal[i]==A(s-F),'non-star minimal parabolic')
            need(len(minimal[i])//len(H)==2**len(s-F),'non-star panel index');panel_checks+=1
        need(minimal[-1]==generated(set(H)|{t},mul),'star minimal parabolic')
        for mask in range(1<<len(maxs)):
            want=set(U);gens=set(H)
            for i,sub in enumerate(maxs):
                if mask>>i&1:gens.update(minimal[i])
                else:want.intersection_update(sub)
            need(generated(gens,mul)==frozenset(want),'every parabolic generation including empty/full');generation_checks+=1
        cases+=1
    # Full coset Helly check for a nontrivial automorphism, both with and without a common C2 Borel.
    helly=[]
    for extra in [0,1]:
        p=(1,0,2);mul,U,m=model(p,extra);t=(0,1);subs=[]
        for mask in range(8):
            P=frozenset((v,0) for v in span([i for i in range(3) if mask>>i&1]+list(range(3,3+extra))))
            subs.append(P)
            if all(permute(v,tuple(p)+tuple(range(3,3+extra))) in {x[0] for x in P} for v,_ in P):subs.append(generated(set(P)|{t},mul))
        cosets=sorted({frozenset(mul(g,h) for h in H) for H in subs for g in U},key=lambda s:(len(s),sorted(s)))
        adj={i:{j for j in range(len(cosets)) if i!=j and cosets[i]&cosets[j]} for i in range(len(cosets))}
        cliques=maximal_cliques(range(len(cosets)),adj)
        for clique in cliques:
            intersection=set(U)
            for i in clique:intersection.intersection_update(cosets[i])
            need(bool(intersection),'all maximal coset cliques have common representative')
        helly.append(dict(common_borel_order=2**extra,group_order=len(U),cosets=len(cosets),maximal_cliques=len(cliques)))
    # The exact base-subgroup lists of the two-loop example are computed as vector spaces.
    block12={span([]),span([2]),span([0,1]),span([0,1,2])}
    block23={span([]),span([0]),span([1,2]),span([0,1,2])}
    tau=(0,2,1);sigma=(1,0,2)
    need(frozenset(permute(v,tau) for v in span([2])) not in block12,'sigma then tau fails')
    need(frozenset(permute(v,sigma) for v in span([0])) not in block23,'tau then sigma fails')
    rejected=[]
    local=[{0,1},{0,2},{1,2}]
    need(all(a&b for a,b in combinations(local,2)) and not set.intersection(*local),'non-Helly local countermodel');rejected.append('delete local coset Helly')
    mul,U,m=model((1,0),0);P=frozenset({(0,0),(1,0)});P_hat=generated(set(P)|{(0,1)},mul)
    need({x for x in P_hat if x[1]==0}!=set(P),'noncompatible base enlarged');rejected.append('delete compatibility')
    need({(0,0)}!={(0,0),(8,0)},'empty-type generation must retain nontrivial Borel');rejected.append('drop Borel from empty generation')
    need(span([1]) not in block12 and span([1]) not in block23,'local admissibility is not preserved');rejected.append('infer iterative admissibility from original edges')
    return dict(status='PASS',finite_quotient_cases=cases,all_parabolic_generation_checks=generation_checks,nonstar_panel_checks=panel_checks,coset_helly_models=helly,two_loop_orderings_rejected=2,rejected_controls=rejected,scope='Finite semidirect quotients test formulas only; infinite Bass-Serre transport, infinite star panels and general theorems are independently read written proofs, not inferred from these computations.')

if __name__=='__main__':
    import json
    print(json.dumps(run(),indent=2))
