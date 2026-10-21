#!/usr/bin/env python3
"""Independent finite affine checks of phase130; no primary files or predecessor code."""
import argparse, hashlib, json, time
from pathlib import Path


def require(ok, msg):
    if not ok:
        raise ValueError(msg)


def closure(gens, one, mul):
    seen, todo = {one}, [one]
    for x in todo:
        for g in gens:
            y = mul(x, g)
            if y not in seen:
                seen.add(y); todo.append(y)
    return seen


def check(q, diagonal):
    I = (1, 0, 0, 1)
    def normalize(v):
        x, y = v
        if not diagonal:
            return x % q, y % q
        # Invariant residues x-y mod2q and y modq characterize this lattice.
        w = y % q
        return (x - y) % (2*q) + w, w
    def mul(g, h):
        (x,y), (a,b,c,d) = g
        (u,v), (e,f,k,l) = h
        return normalize((x+a*u+b*v, y+c*u+d*v)), (a*e+b*k,a*f+b*l,c*e+d*k,c*f+d*l)
    one = ((0,0),I)
    a = ((0,0),(-1,0,0,1))
    b = ((0,0),(0,1,1,0))
    c = (normalize((0,1)),(1,0,0,-1))
    def prod(*words):
        out = one
        for g in words:
            out = mul(out,g)
        return out
    def power(g,k):
        return prod(*([g]*k))
    marks=[a,b,c]
    require(all(power(g,2)==one and g!=one for g in marks),'involutions')
    require(power(prod(a,b),4)==one and power(prod(b,c),4)==one and prod(a,c)==prod(c,a),'Coxeter relators')
    require(prod(b,c,b,a)==(normalize((1,0)),I),'source square word')
    require(power(prod(c,b,a),2)==(normalize((1,1)),I),'source diagonal word')
    A=power(prod(a,b),2); C=power(prod(b,c),2)
    require(prod(A,c,A,c)==(normalize((0,-2)),I),'first commutator translation')
    require(prod(A,C,A,C)==(normalize((-2,-2)),I),'second commutator translation')
    full=closure(marks,one,mul)
    require(len(full)==(16 if diagonal else 8)*q*q,'whole quotient order')
    if diagonal:
        left=closure([prod(a,b,a),prod(c,b,c)],one,mul)
        ac=prod(a,c)
        right=closure([b,prod(ac,b,ac)],one,mul)
        complement=closure([a,c],one,mul)
    else:
        left=closure([a,prod(b,c,b)],one,mul)
        right=closure([prod(b,a,b),c],one,mul)
        complement=closure([b],one,mul)
    require(len(left)==len(right)==2*q,'dihedral factor orders')
    require(left&right=={one},'factor intersection')
    require(all(mul(g,h)==mul(h,g) for g in left for h in right),'factor commutation')
    factors={mul(g,h) for g in left for h in right}
    require(factors&complement=={one},'complement intersection')
    require({mul(g,h) for g in factors for h in complement}==full,'factor complement generation')
    # All complement elements here are involutions, including their identity.
    require(all({prod(h,g,h) for g in factors}==factors for h in complement),'normalization')
    return {'q':q,'lattice':'diagonal' if diagonal else 'square','order':len(full),
            'factor_orders':[len(left),len(right)],'complement_order':len(complement),
            'all_relators_words_intersections_and_actions':True}


def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    require(not a.report.exists(),'Refusing existing output')
    start=time.monotonic()
    rows=[check(q,d) for q in range(2,8) for d in [False,True]]
    out={'status':'PASS','scope':'12 bounded lattice decompositions only; written proof gives all q and general typed Helly',
         'rows':rows,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'seconds':time.monotonic()-start}
    with a.report.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
    print(json.dumps({'status':out['status'],'cases':len(rows),'seconds':out['seconds']}))


if __name__=='__main__':main()
