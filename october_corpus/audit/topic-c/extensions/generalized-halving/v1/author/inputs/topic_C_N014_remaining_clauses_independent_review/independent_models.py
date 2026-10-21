#!/usr/bin/env python3
"""Independent literal models; imports no author construction or counting code."""
import argparse
import itertools as it
import json
from pathlib import Path


def need(b, m):
    if not b:
        raise ValueError(m)


def model(lifted):
    types = [[(i, j) for j in range(5)] for i in range(2)]
    if lifted:
        types += [[(2, 'X')] + [(2,j,t) for j in range(5) for t in [0,1]],
                  [(3,j,t) for j in range(5) for t in [0,1]]]
    else:
        types += [[(2,'X')] + [(2,j) for j in range(5)],
                  [(3,j) for j in range(5)]]
    def contains(o, v, bit=0):
        if o[1] == 'X':
            return True
        d = (v-o[1]-1) % 5
        return d < 4 and (not lifted or (d+o[2])%2 == bit)
    def inc(x, y):
        if x[0] == y[0]:
            return False
        if x[0] > y[0]:
            x, y = y, x
        if y[0] < 2:
            return ((x[1]-y[1])%5 in [1,4]) if lifted else x[1] in [y[1],(y[1]+1)%5]
        if x[0] < 2:
            if lifted or x[0] == 0:
                return contains(y,x[1],x[0])
            return contains(y,x[1]) and contains(y,(x[1]+1)%5)
        return x[1] == 'X' or x[1:] == y[1:]
    return types, inc


def audit(types, inc):
    flags = []
    for indices in it.product(*[range(-1,len(t)) for t in types]):
        f = tuple(t[i] for t,i in zip(types,indices) if i >= 0)
        if all(inc(x,y) for x,y in it.combinations(f,2)):
            flags.append(f)
    chambers = [set(f) for f in flags if len(f)==4]
    for f in flags:
        need(any(set(f)<=c for c in chambers),'flag does not extend')
    residues = 0
    for f in flags:
        if len(f)>2:
            continue
        verts = [x for t in types for x in t
                 if x[0] not in [y[0] for y in f] and all(inc(x,y) for y in f)]
        need(bool(verts),'empty relevant residue')
        seen = {verts[0]}
        while True:
            extra = {y for x in seen for y in verts if inc(x,y)}-seen
            if not extra:
                break
            seen |= extra
        need(len(seen)==len(verts),'disconnected residue')
        residues += 1
    return dict(objects=list(map(len,types)),flags=len(flags),chambers=len(chambers),
                connected_residues=residues)


def leaf(types,inc,a,b):
    edges = []
    for e in types[b]:
        ends = frozenset(x for x in types[a] if inc(x,e))
        need(len(ends)==2,'two endpoints')
        need(ends not in edges,'double edge')
        edges.append(ends)
        for i in range(4):
            if i in [a,b]:
                continue
            for x in types[i]:
                need(inc(e,x)==all(inc(v,x) for v in ends),'B2')
    return len(edges)


def mul(p,q):
    return tuple(p[q[i]] for i in range(4))


def subgroup(gens):
    seen = {tuple(range(4))}
    todo = list(seen)
    while todo:
        x = todo.pop()
        for g in gens:
            y = mul(x,g)
            if y not in seen:
                seen.add(y);todo.append(y)
    return seen


def prod(A,B):
    return {mul(a,b) for a in A for b in B}


def cosets():
    # A,B,C,D = 0,1,2,3.  These are independent literal permutation tuples.
    a,b,c = (1,0,3,2),(0,2,1,3),(0,1,3,2)
    G = subgroup([a,b,c]); P = subgroup([b,c]); R = subgroup([c]); K = subgroup([a,b])
    aPa = prod(prod({a},P),{a}); Pi=P&K
    need(len(G)==24 and P&aPa == R,'hemicube B1')
    left = prod(K,P)&prod(prod(P,{a}),P)
    right = prod(prod(Pi,{a}),P)
    need(len(left)==18 and len(right)==12 and left!=right,'hemicube B2 failure')
    ba = mul(b,a)
    need(ba in prod(P,{a}) and ba in prod({ba},P),'literal source intersection witness')
    need(prod({ba},P)!=prod({a},P),'literal source antecedent impossible')
    new = mul(mul(a,b),a)
    need(new==(3,1,2,0),'AD conjugate')
    need(len(subgroup([new,c,b]))==24,'tetrahedral new group')
    return dict(group_order=24,B1_intersection_order=len(R),B2_left_group_elements=len(left),
                B2_right_group_elements=len(right),literal_witness='ba',tetrahedral_group_order=24)


def run():
    output={}
    for lifted in [False,True]:
        types,inc=model(lifted)
        r=audit(types,inc)
        r['second_leaf_edges']=leaf(types,inc,2,3)
        if not lifted:
            r['first_leaf_edges']=leaf(types,inc,0,1)
        output['lifted' if lifted else 'original']=r
    need(output['original']==dict(objects=[5,5,6,5],flags=322,chambers=60,
         connected_residues=122,second_leaf_edges=5,first_leaf_edges=5),'original totals')
    need(output['lifted']==dict(objects=[5,5,11,10],flags=362,chambers=60,
         connected_residues=152,second_leaf_edges=10),'lifted totals')
    controls=[]
    types,inc=model(True)
    bad=lambda x,y: inc(x,y) and {x,y}!={(2,'X'),(3,0,0)}
    try:
        leaf(types,bad,2,3)
    except ValueError:
        controls.append('remove central lifted endpoint rejected')
    need(len(controls)==1,'endpoint mutation escaped')
    output['hemicube_cosets']=cosets()
    output['controls']=controls
    output['status']='PASS'
    output['basis']='supplementary independent finite diagnostics; written proof reviewed separately'
    return output


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    r=run();a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r))
