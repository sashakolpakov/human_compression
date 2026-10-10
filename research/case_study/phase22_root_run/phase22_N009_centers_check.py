#!/usr/bin/env python3
"""Finite affine diagnostics for N009 Lemma5.2; no all-parameter inference."""
from pathlib import Path
from itertools import product
import hashlib,json,argparse

def matrix_product(a,b):
    return (a[0]*b[0]+a[1]*b[2],a[0]*b[1]+a[1]*b[3],a[2]*b[0]+a[3]*b[2],a[2]*b[1]+a[3]*b[3])
I=(1,0,0,1);X=(-1,0,0,1);B=(0,1,1,0);C=(1,0,0,-1)
D={I};todo=[I]
while todo:
    m=todo.pop()
    for g in (B,C):
        h=matrix_product(m,g)
        if h not in D:D.add(h);todo.append(h)
assert len(D)==8
results=[]
for family,s in [(1,t) for t in (2,4,8,16)]+[(2,t) for t in (1,2,4,8)]:
    def coordinates(x,y):
        return (x%s,y%s) if family==1 else ((x-y)%(2*s),y%s)
    def lift(v):return v if family==1 else (v[0]+v[1],v[1])
    def mul(g,h):
        v,m=g;w,n=h;x,y=lift(v);u,vv=lift(w)
        return coordinates(x+m[0]*u+m[1]*vv,y+m[2]*u+m[3]*vv),matrix_product(m,n)
    one=(coordinates(0,0),I)
    a=(coordinates(1,0),X);b=(coordinates(0,0),B);c=(coordinates(0,0),C)
    def powg(g,n):
        ans=one
        while n:
            if n&1:ans=mul(ans,g)
            g=mul(g,g);n//=2
        return ans
    def word(*args):
        ans=one
        for g in args:ans=mul(ans,g)
        return ans
    def closure(gens):
        seen={one};queue=[one]
        while queue:
            x=queue.pop()
            for g in gens:
                y=mul(x,g)
                if y not in seen:seen.add(y);queue.append(y)
        return seen
    G=closure([a,b,c]);target=(8 if family==1 else 16)*s*s
    assert len(G)==target and all(powg(g,2)==one for g in (a,b,c))
    assert word(a,c)==word(c,a)
    center={g for g in G if all(mul(g,r)==mul(r,g) for r in (a,b,c))}
    if family==1 and s==2:generators=[powg(word(a,b),2),powg(word(b,c),2)]
    elif family==1:generators=[powg(word(a,b,c),s)]
    elif s==1:generators=[word(a,c),powg(word(a,b),2),powg(word(b,c),2)]
    else:generators=[powg(word(a,b,c,b),s)]
    assert center==closure(generators)
    translations={v for v,m in G if m==I}
    fixed={v for v in translations if all(mul((coordinates(0,0),m),(v,I))==mul((v,I),(coordinates(0,0),m)) for m in D)}
    action_kernel={m for m in D if all(mul((coordinates(0,0),m),(v,I))==mul((v,I),(coordinates(0,0),m)) for v in translations)}
    expected_kernel=4 if family==1 and s==2 else 8 if family==2 and s==1 else 1
    assert len(action_kernel)==expected_kernel
    results.append(dict(family=family,s=s,group_order=len(G),center_order=len(center),translation_fixed_order=len(fixed),linear_action_kernel_order=len(action_kernel),center_formula='PASS'))
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path(__file__).with_suffix('.json'));args=p.parse_args()
r=dict(status='PASS',script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=results,total_elements=sum(x['group_order'] for x in results),scope='Eight explicit finite affine models; all elements tested against three generators for centrality. These diagnostics do not prove uniform parameter coverage or the source lattice classification.')
args.output.write_text(json.dumps(r,indent=2)+'\n');print('PASS',len(results),'models,',r['total_elements'],'elements; all center formulas and faithful-action boundaries')
