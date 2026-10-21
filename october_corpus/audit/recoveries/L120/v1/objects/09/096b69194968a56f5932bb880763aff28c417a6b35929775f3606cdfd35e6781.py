"""Independent check on the twelve-point projective line; no author imports."""
from collections import deque
import itertools
import json
from pathlib import Path

Q = 11
IDENTITY = tuple(range(12))


def need(ok, message):
    if not ok:
        raise ValueError(message)


def action(m):
    a,b,c,d = m
    values=[]
    for point in range(12):
        if point == 11:
            numerator,denominator=a,c
        else:
            numerator,denominator=(a*point+b)%Q,(c*point+d)%Q
        values.append(11 if denominator == 0 else numerator*pow(denominator,-1,Q)%Q)
    need(len(set(values)) == 12, "matrix must induce a bijection")
    return tuple(values)


def product(p,q):
    return tuple(p[q[v]] for v in range(12))


def power(p,n):
    ans=IDENTITY
    for _ in range(n):
        ans=product(ans,p)
    return ans


def order(p):
    for n in range(1,661):
        if power(p,n) == IDENTITY:
            return n
    raise ValueError("order exceeds target group")


def group(gens):
    seen={IDENTITY};pending=deque(seen)
    while pending:
        p=pending.popleft()
        for q in gens:
            v=product(p,q)
            if v not in seen:
                seen.add(v);pending.append(v)
    return seen


def verify(gens):
    a,b,c=gens
    need(all(order(g)==2 for g in gens),"involutions")
    ambient={action((a,b,c,d)) for a,b,c,d in itertools.product(range(Q),repeat=4)
             if (a*d-b*c)%Q==1}
    need(len(ambient)==660 and group(gens)==ambient,"full projective group")
    r,s=product(a,b),product(b,c)
    need(group([r,s])==ambient,"rotation group")
    need([order(r),order(s),order(product(a,c))]==[6,6,5],"exact type")
    x,z=power(r,3),power(s,3)
    need(product(x,z)==b,"rotations recover middle involution")
    left,right,shared=group([a,b]),group([b,c]),group([b])
    need(len(left)==len(right)==12 and len(left&right)==4 and len(shared)==2,"exact intersection")
    need(x in left&right and x not in shared,"explicit extra element")
    need(product(b,product(r,b))==power(r,5) and product(b,product(s,b))==power(s,5),"inner inversion")
    ans=IDENTITY
    for letter in "abacbabcac":
        ans=product(ans,gens[ord(letter)-97])
    need(ans==action((1,1,0,1)),"elementary generator word")
    return {"domain":12,"full_group":660,"rotation_group":660,
            "pair_orders":[12,12],"intersection_order":4,"shared_order":2,
            "extra_permutation":list(x)}


gens=[action(m) for m in [(5,1,7,6),(0,1,10,0),(4,3,9,7)]]
report=verify(gens)
try:
    verify([gens[0],gens[1],gens[1]])
except ValueError as error:
    need(str(error)=="full projective group","precise coincident-generator rejection")
else:
    raise ValueError("coincident-generator control accepted")
report.update(status="PASS",negative_control="coincident generator rejected at full generation")
print(json.dumps(report,indent=2))
