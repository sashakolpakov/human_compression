"""Integer permutations only: lower bounds, complete IP and coset Helly tests.

This does not prove an upper bound for an abstract presentation. exact_groups.g
provides that separate premise by actual GAP fp-group isomorphisms.
"""
from collections import deque
from itertools import combinations
from math import lcm
import json
from pathlib import Path
from countermodel import BASE, MOD, ORIG, ensure

def mul(a,b): return bytes(a[i] for i in b)
def closure(gs,I):
    done={I}; todo=deque([I])
    while todo:
        a=todo.popleft()
        for b in gs:
            c=mul(a,b)
            if c not in done: done.add(c); todo.append(c)
    return done
def word(gs,w,I):
    a=I
    for i in w: a=mul(a,gs[i])
    return a
def order(g):
    seen=set(); lengths=[]
    for x in range(len(g)):
        if x in seen: continue
        y=x; n=0
        while y not in seen: seen.add(y); n+=1; y=g[y]
        lengths.append(n)
    return lcm(*lengths)
def product(H,K): return {mul(h,k) for h in H for k in K}
def helly(H,K,L): return product(H&K,H&L)==H&product(K,L)
def audit(data):
    reports=[]
    ensure([x['n'] for x in data['models']]==[3,6],'both literal cases')
    for row in data['models']:
        n=row['n']; t=n//3
        gs=[bytes(x-1 for x in r) for r in row['generators']]
        ensure(len(gs)==4,'four markers'); I=bytes(range(len(gs[0])))
        ensure(all(sorted(g)==list(I) for g in gs),'permutation bijections')
        ensure(all(word(gs,w,I)==I for w in BASE),'shared literal relations')
        ensure(word(gs,ORIG*n,I)==I,'original relation')
        ensure(word(gs,MOD*(2*t),I)==I,'modified relation')
        ensure(order(word(gs,[1,3],I))==6,'bd exact order')
        H=[closure([g for i,g in enumerate(gs) if m>>i&1],I) for m in range(16)]
        ensure(len(H[15])==720*t**6,'exact finite image order')
        for m in range(16):
            for k in range(16): ensure(H[m]&H[k]==H[m&k],'IP')
        M=[H[15^(1<<i)] for i in range(4)]
        ensure([len(h) for h in M]==[36*t*t,48,36,48],'ordered maximal subgroups')
        for i,j,k in combinations(range(4),3): ensure(helly(M[i],M[j],M[k]),'global triple Helly')
        for i in range(4):
            subs=[M[i]&M[j] for j in range(4) if i!=j]
            ensure(helly(*subs),'local rank-three Helly')
        markers=[[gs[2],gs[3],gs[1]],[gs[3],gs[2],gs[0]],[gs[0],gs[1],gs[3]],[gs[1],gs[0],gs[2]]]
        torus_rels=[[0,1]*3,[1,2]*6,[0,2]*2]
        for i,rr in enumerate(markers):
            ensure(all(word(rr,w,I)==I for w in torus_rels),'ordered torus edges')
            ensure([order(word(rr,w,I)) for w in [[0,1],[1,2],[0,2]]]==[3,6,2],'no rank-two collapse')
            ensure(closure(rr,I)==M[i],'ordered torus generators')
            period=[0,1,2,1,2]*(2*(t if i==0 else 1)) if i in [0,2] else [0,1,2,1,2,1]*2
            ensure(word(rr,period,I)==I,'torus period relation')
        reports.append({'n':n,'points':len(I),'order':len(H[15]),'parabolic_orders':[len(h) for h in M],
                        'IP_pairs':256,'global_Helly':4,'local_Helly':4,'bd_order':6,'ordered_torus_relations':True})
    return {'status':'PASS','models':reports,'abstract_presentation_upper_bound_proved_here':False}
if __name__=='__main__':
    print(json.dumps(audit(json.loads((Path(__file__).parent/'model_data.json').read_text())),indent=2))
