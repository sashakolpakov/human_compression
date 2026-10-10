#!/usr/bin/env python3
"""Exact doubled voltage action, finite parabolics, and modulus-two geometry.

All arithmetic is integral or binary; no GAP or author-checker import is used.
The written quotient-transport proof is separate from this finite certificate.
"""
import argparse
from collections import deque
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--data',type=Path,default=Path(__file__).with_name('phase32_L003_voltage.json'))
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    if args.output.exists():
        raise SystemExit('Refusing to overwrite an existing report')
    raw=args.data.read_bytes();data=json.loads(raw)
    n=data['degree'];assert n==216
    p=[tuple(j-1 for j in x) for x in data['permutations']]
    v=[tuple(x) for x in data['weights']]
    pi=[tuple(x.index(j) for j in range(n)) for x in p]
    nn=2*n
    ident=(tuple(range(nn)),(0,)*nn)
    swap=(tuple(range(n,nn))+tuple(range(n)),(0,)*nn)
    marks=[swap]
    for j in range(3):
        marks.append((tuple(n+pi[j][i] for i in range(n))+p[j],
                      tuple(-v[j][pi[j][i]] for i in range(n))+v[j]))

    def mul(a,b):
        pp,w=a;qq,z=b
        return tuple(qq[i] for i in pp),tuple(w[i]+z[pp[i]] for i in range(nn))
    def inv(a):
        pp,w=a;qq=tuple(pp.index(i) for i in range(nn))
        return qq,tuple(-w[i] for i in qq)
    def power(a,k):
        if k<0:return power(inv(a),-k)
        b=ident
        while k:
            if k&1:b=mul(b,a)
            a=mul(a,a);k//=2
        return b
    def product(*items):
        b=ident
        for a in items:b=mul(b,a)
        return b
    assert all(mul(a,a)==ident for a in marks)
    x,y,z=[mul(marks[0],a) for a in marks[1:]]
    parameter=product(y,power(product(z,y),2))
    relators=[power(x,6),power(y,3),power(z,2),power(product(z,x),3),
        power(product(z,y),6),power(product(inv(x),y),2),
        power(product(inv(y),power(x,-2)),3),power(product(z,power(x,3)),2),
        product(inv(x),z,power(product(inv(y),z),2),z,x,power(product(z,y),2)),
        power(parameter,6)]
    assert all(a==ident for a in relators)
    assert all(power(parameter,k)!=ident for k in (1,2,3))
    witness=power(product(x,y,x,z),2)
    assert witness[0]==ident[0] and witness[1][0]==-1

    def finite_closure(gens):
        seen={ident[0]:ident};todo=deque([ident])
        while todo:
            a=todo.popleft()
            for g in gens:
                b=mul(a,g)
                if b[0] in seen:
                    assert b==seen[b[0]],'Nonzero translation in a claimed finite parabolic'
                else:
                    seen[b[0]]=b;todo.append(b)
                assert len(seen)<=432
        return frozenset(seen.values())
    locals_full={mask:finite_closure([marks[j] for j in range(4) if mask>>j&1])
                 for mask in range(15)}
    par_masks=[15^(1<<j) for j in range(4)]
    assert [len(locals_full[m]) for m in par_masks]==[36,432,48,108]
    print('Exact finite local closures PASS',flush=True)

    # Enumerate the finite permutation quotient, retaining arbitrary lifted words.
    lifts={ident[0]:ident};todo=deque([ident[0]])
    while todo:
        pp=todo.popleft()
        for a in marks:
            b=mul(lifts[pp],a)
            if b[0] not in lifts:lifts[b[0]]=b;todo.append(b[0])
        assert len(lifts)<=432
    assert len(lifts)==432
    plist=list(lifts);pindex={pp:i for i,pp in enumerate(plist)}
    pinv=[tuple(pp.index(i) for i in range(nn)) for pp in plist]
    def bits(w):return sum((x&1)<<i for i,x in enumerate(w))
    def mod2(a):return pindex[a[0]],bits(a[1])
    @lru_cache(None)
    def pmul(i,j):return pindex[tuple(plist[j][x] for x in plist[i])]
    @lru_cache(None)
    def pull(i,w):
        out=0
        while w:
            t=w&-w;j=t.bit_length()-1;out^=1<<pinv[i][j];w^=t
        return out
    def bm(a,b):return pmul(a[0],b[0]),a[1]^pull(a[0],b[1])
    local={m:frozenset(mod2(a) for a in aa) for m,aa in locals_full.items()}
    assert all(len(local[m])==len(locals_full[m]) for m in local)
    assert all(local[a]&local[b]==local[a&b] for a in range(15) for b in range(15))
    # Meets with the full group are tautological: this certifies all 16^2 meets.
    print('All 256 marked meets PASS',flush=True)

    binary_basis={};loops=0
    for pp,a in lifts.items():
        for g in marks:
            b=mul(a,g);t=mul(b,inv(lifts[b[0]]))
            assert t[0]==ident[0];r=bits(t[1]);loops+=1
            while r:
                piv=r.bit_length()-1
                if piv in binary_basis:r^=binary_basis[piv]
                else:binary_basis[piv]=r;break
    assert loops==1728 and len(binary_basis)==6
    group_order=len(lifts)*(1<<len(binary_basis))
    assert group_order==27648

    pars=[local[m] for m in par_masks]
    @lru_cache(None)
    def par_product(i,j):return frozenset(bm(a,b) for a in pars[i] for b in pars[j])
    helly=[]
    for i in range(4):
        others=[j for j in range(4) if j!=i]
        for mask in range(1,8):
            js=[others[k] for k in range(3) if mask>>k&1]
            if len(js)<2:continue
            j0=js[0];meet=pars[i]&pars[j0];covered=set();reps=[]
            for a in sorted(pars[j0]):
                if a in covered:continue
                reps.append(a);covered.update(bm(t,a) for t in meet)
            assert covered==pars[j0]
            count=sum(all(a in par_product(i,j) for j in js[1:]) for a in reps)
            t=set(pars[js[0]])
            for j in js[1:]:t.intersection_update(pars[j])
            expected=len(t)//len(t&pars[i]);assert count==expected
            helly.append({'type':i,'base_flag_types':js,'common_incident_cosets':count,
                          'intersection_orbit_size':expected})
    print('All 16 typed-Helly cardinalities PASS',flush=True)
    report={'status':'PASS','checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'data_sha256':sha256(raw).hexdigest(),'doubled_states':nn,
        'source_relator_state_equalities':10*nn,'parameter_order':6,
        'witness_first_translation':-1,'proper_subgroup_orders':{str(m):len(local[m]) for m in local},
        'maximal_parabolic_orders':[len(p) for p in pars],
        'permutation_quotient_order':432,'binary_schreier_generators':loops,
        'binary_translation_rank':len(binary_basis),'modulus2_group_order':group_order,
        'subset_meets':256,'typed_helly_checks':helly,
        'scope':'Exact integer local closures and literal modulus-two marking. Written transport supplies the infinite and even-modulus geometric conclusions; no source universal-group identification or varying-s problem resolution.'}
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('L003_GEOMETRY_PASS',flush=True)


if __name__=='__main__':main()
