#!/usr/bin/env python3
"""Independent literal finite semidirect implementation of Example 5.11, s=1."""
from affine_example import MARKS, IDENTITY, model, mul, need, subgroup
from collections import deque
import json

def compose(p,q):return tuple(p[q[i]] for i in range(len(p)))

def check():
    image,operation=model(1);one=image(IDENTITY);marks=tuple(map(image,MARKS))
    words={one:()};queue=deque([one])
    while queue:
        a=queue.popleft()
        for i,g in enumerate(marks):
            b=operation(a,g)
            if b not in words:words[b]=words[a]+(i,);queue.append(b)
    need(len(words)==96,'literal affine quotient size')
    p=(1,0,3,2);q=(0,2,1,3);bid=tuple(range(4))
    outer=subgroup([p,q],compose,bid)
    need(len(outer)==8,'diagram group')
    action={}
    for b in outer:
        transform={}
        for a,w in words.items():
            z=one
            for i in w:z=operation(z,marks[b[i]])
            transform[a]=z
        need(len(set(transform.values()))==96,'automorphism bijection')
        for a in words:
            for i,g in enumerate(marks):
                need(transform[operation(a,g)]==operation(transform[a],marks[b[i]]),'automorphism relator transition')
        action[b]=transform
    for b in outer:
        for c in outer:
            for a in words:
                need(action[b][action[c][a]]==action[compose(b,c)][a],'action multiplication')
    unit=(one,bid)
    def op(a,b):return operation(a[0],action[a[1]][b[0]]),compose(a[1],b[1])
    x=(marks[0],bid);pp=(one,p);qq=(one,q);gen=(x,pp,qq)
    allg=frozenset((a,b) for a in words for b in outer)
    generated=subgroup(gen,op,unit)
    need(generated==allg,'full generation')
    subs=[subgroup([gen[i] for i in range(3) if mask>>i&1],op,unit) for mask in range(8)]
    need([len(subs[m]) for m in [3,5,6]]==[12,4,8],'rank-two orders')
    pairs=0;triples=0
    for i in range(8):
        for j in range(8):
            need(subs[i]&subs[j]==subs[i&j],'full IP');pairs+=1
    products={(i,j):frozenset(op(a,b) for a in subs[i] for b in subs[j]) for i in range(7) for j in range(7)}
    for i in range(7):
        for j in range(7):
            for k in range(7):
                need(products[i,j]&products[i,k]==products[i,j&k],'coset Helly product');triples+=1
    # Literal Definition4.6: first intersect actual quotient maximal parabolics.
    base_max=[subgroup([marks[j] for j in range(4) if i!=j],operation,one) for i in range(4)]
    need(all(len(h)==24 for h in base_max),'quotient maximal orders')
    one_support=frozenset.intersection(*base_max[1:])
    two_support=base_max[2]&base_max[3]
    borel=frozenset.intersection(*base_max)
    need([len(one_support),len(two_support),len(borel)]==[2,6,1],'actual source intersections')
    source_x=subgroup([(a,bid) for a in one_support]+[qq],op,unit)
    source_y=subgroup([(a,bid) for a in two_support]+[pp],op,unit)
    source_orbit=subgroup([(a,bid) for a in borel]+[pp,qq],op,unit)
    need((source_orbit,source_x,source_y)==(subs[6],subs[5],subs[3]),'literal-to-marked parabolics')
    return {'status':'PASS','base_order':96,'outer_order':8,'whole_order':len(allg),'proper_orders':[len(s) for s in subs[:7]],'actual_base_intersection_orders':[len(one_support),len(two_support),len(borel)],'IP_pairs':pairs,'proper_product_triples':triples,'conclusion':'The literal s=1, F0=1 twist is thin, residually connected and flag-transitive; source nonregular inference fails.'}
if __name__=='__main__':print(json.dumps(check(),indent=2,sort_keys=True))
