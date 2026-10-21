#!/usr/bin/env python3
"""Exact integer/parabolic certificate for source Example 5.11; no GAP."""
from itertools import combinations
from functools import lru_cache
import json
IDENTITY=(tuple(range(4)),(0,0,0,0))
def need(ok,message):
    if not ok: raise RuntimeError(message)
def mul(a,b):
    p,v=a;q,w=b
    return tuple(p[q[i]] for i in range(4)),tuple(v[i]+w[p.index(i)] for i in range(4))
def refl(i,j,v=(0,0,0,0)):
    p=list(range(4));p[i],p[j]=p[j],p[i]
    return tuple(p),v
MARKS=(refl(0,1),refl(1,2),refl(0,3,(1,0,0,-1)),refl(2,3))
def word(seq):
    out=IDENTITY
    for i in seq:out=mul(out,MARKS[i])
    return out

def subgroup(gens,operation=mul,unit=IDENTITY,limit=100000):
    found={unit};todo=[unit]
    while todo:
        a=todo.pop()
        for b in gens:
            c=operation(a,b)
            if c not in found:
                found.add(c);todo.append(c)
                need(len(found)<=limit,'subgroup cap')
    return frozenset(found)

def proper():
    return [subgroup([MARKS[i] for i in range(4) if mask>>i&1],limit=25) for mask in range(15)]

def model(s):
    modulus=2*s
    def canon(v):
        a=tuple(x%modulus for x in v)
        b=tuple((x+s)%modulus for x in v)
        return min(a,b)
    def image(a):return a[0],canon(a[1])
    def op(a,b):return image(mul(a,b))
    return image,op

def validate():
    need(all(mul(a,a)==IDENTITY for a in MARKS),'involutions')
    for i,j in combinations(range(4),2):
        exponent=2 if {i,j} in ({0,3},{1,2}) else 3
        need(word([i,j]*exponent)==IDENTITY,'Coxeter relation')
    translation=word([2,3,0,1]*2)
    need(translation==(tuple(range(4)),(1,1,-1,-1)),'translation word')
    P=proper()
    need([len(P[m]) for m in [7,11,13,14]]==[24]*4,'four finite parabolics')
    need(max(abs(v) for H in P for _,t in H for v in t)==1,'coordinate bound')
    products={(i,j):frozenset(mul(a,b) for a in P[i] for b in P[j]) for i in range(15) for j in range(15)}
    need(max(abs(v) for H in products.values() for _,t in H for v in t)==2,'product coordinate bound')
    rows=[]
    for s in [1,2,3,4]:
        image,op=model(s)
        Q=[frozenset(map(image,H)) for H in P]
        product={(i,j):frozenset(map(image,H)) for (i,j),H in products.items()}
        ip=[]
        for i in range(15):
            for j in range(15):
                if Q[i]&Q[j]!=Q[i&j]:ip.append([i,j,len(Q[i]&Q[j]),len(Q[i&j])])
        failure=[]
        if not ip:
            for i in range(15):
                for j in range(15):
                    for k in range(15):
                        if product[i,j]&product[i,k]!=product[i,j&k]:failure.append([i,j,k])
        if s>=2:
            need(not ip,'positive IP');need(not failure,'positive product identity')
            need(all(len(Q[i])==len(P[i]) for i in range(15)),'proper injection')
        G=subgroup([image(a) for a in MARKS],op,image(IDENTITY))
        need(len(G)==96*s**3,'quotient order')
        row={'s':s,'order':len(G),'generated_parabolic_IP_failures':ip,'product_failures_if_IP':failure,'IP_pairs':225,'product_triples':3375 if not ip else 0}
        if s==1:
            maxs=[Q[15^(1<<i)] for i in range(4)]
            intersections={0:G}
            for mask in range(1,16):
                intersections[mask]=frozenset.intersection(*(maxs[i] for i in range(4) if mask>>i&1))
            rc=[]
            for mask,H in intersections.items():
                missing=[i for i in range(4) if not mask>>i&1]
                if len(missing)>=2:
                    childgens=set().union(*(intersections[mask|1<<i] for i in missing))
                    child=subgroup(childgens,op,image(IDENTITY))
                    if child!=H:rc.append({'flag_mask':mask,'parabolic_order':len(H),'generated_children_order':len(child),'witness':sorted(H-child)[0]})
            need(rc,'negative residual connectivity')
            row['residual_generation_failures']=rc
        rows.append(row)
    return {'status':'PASS','translation_word':translation,'integer_proper_orders':[len(x) for x in P],'proper_coordinate_bound':1,'product_coordinate_bound':2,'uniform_written_threshold':5,'models':rows}

if __name__=='__main__':print(json.dumps(validate(),sort_keys=True,indent=2))
