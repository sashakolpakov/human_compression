"""Reviewer controls, without imports from the author's programs."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Normal Python required')
from fractions import Fraction as F
from itertools import combinations, product
import json
from pathlib import Path

def need(t, message):
    if not t:
        raise ValueError(message)

# Weight coordinates x=2a-b,y=-a+2b turn the arrangement into
# x,y,x+y integer. These direct affine formulas are derived independently
# by substituting a=(2x+y)/3,b=(x+2y)/3 into the written matrices.
def s0(v):
    x,y=v
    return (1-y,1-x)
def s1(v):
    x,y=v
    return (-x,x+y)
def s2(v):
    x,y=v
    return (x+y,-y)
ss=[s0,s1,s2]
dirs=[(1,0),(-1,0),(0,1),(0,-1),(1,-1),(-1,1)]
def adjacent(u,v):
    return (v[0]-u[0],v[1]-u[1]) in dirs
def typ(v):
    return (2*v[0]+v[1])%3
def metric(v):
    x,y=v
    a,b=F(2*x+y,3),F(x+2*y,3)
    return 2*a*a-2*a*b+2*b*b
need({metric(d) for d in dirs}=={F(2,3)},'Six equal edge lengths')
v0=(0,0)
need(sum(adjacent(u,v) for u,v in combinations(dirs,2))==6,'Hexagon link')
need(all(sum(adjacent(u,v) for v in dirs)==2 for u in dirs),'Link degrees')
need(all(len({typ(v0),typ(u),typ(v)})==3 for u,v in combinations(dirs,2) if adjacent(u,v)), 'Every local triangle has three types')
for u in dirs:
    common=[v for v in dirs if adjacent(u,v)]
    need(len(common)==2,'Exactly two triangular edge extensions')
for v in product(range(-4,5),repeat=2):
    for s in ss:
        need(s(s(v))==v and typ(s(v))==typ(v),'Reflection and type')
        for d in dirs:
            w=(v[0]+d[0],v[1]+d[1])
            need(adjacent(s(v),s(w)),'Reflection preserves edges')

# Independent finite permutation quotient on (Z/5Z)^2 in root coordinates.
# It checks the written parabolic/kernel phenomenon in a finite companion;
# it is not a substitute for the infinite geometric proof.
points=list(product(range(5),repeat=2));index={v:i for i,v in enumerate(points)}
maps=[lambda a,b:(1-b,1-a),lambda a,b:(-a+b,b),lambda a,b:(a,a-b)]
perms=[tuple(index[(f(a,b)[0]%5,f(a,b)[1]%5)] for a,b in points) for f in maps]
e=tuple(range(25))
def compose(a,b):return tuple(a[b[i]] for i in range(25))
def closure(gens):
    seen={e};queue=[e]
    for p in queue:
        for g in gens:
            q=compose(p,g)
            if q not in seen:seen.add(q);queue.append(q)
    return seen
G=closure(perms)
N={tuple(index[((a+u)%5,(b+v)%5)] for a,b in points) for u,v in points}
H=[closure([perms[j] for j in range(3) if j!=i]) for i in range(3)]
need(len(G)==150 and N<=G and len(N)==25,'Finite affine companion')
need(all(len(h)==6 and h&N=={e} for h in H),'Injective parabolics')
def cosets(h):return {frozenset(compose(n,a) for n in N) for a in h}
need(all(len(cosets(h))==6 for h in H),'All quotient images are S3')
need(all(len({compose(a,b) for a in H[i] for b in H[j]}&N)==3 for i,j in combinations(range(3),2)), 'Product-kernel obstruction')
P=[closure([perms[i] for i in range(3) if mask>>i&1]) for mask in range(8)]
need(all(P[a]&P[b]==P[a&b] for a,b in product(range(8),repeat=2)), 'Finite companion C-group')
out=dict(status='PASS_INDEPENDENT_GEOMETRY_CONTROLS',lattice_points=81,local_link_vertices=6,local_link_edges=6,edge_extensions=2,reflection_edge_controls=81*3*6,finite_companion_order=150,translation_order=25,parabolic_orders=[6]*3,product_kernel_orders=[3]*3,subset_intersections=64,scope='Supplementary exact controls; infinite tiling and general kernel criterion use written proof')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
