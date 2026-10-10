#!/usr/bin/env python3
"""Literal certificate for the multiple-of-three-parameter L003 hypertope family."""
import argparse
from collections import deque
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--data',type=Path,default=Path(__file__).with_name('phase34_L003_triple_voltage.json'))
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    if args.output.exists():raise SystemExit('Refusing to overwrite existing evidence')
    raw=args.data.read_bytes();d=json.loads(raw);n=d['degree'];assert n==272
    pp=[tuple(x-1 for x in p) for p in d['permutations']]
    vv=[tuple(v) for v in d['weights']]
    assert len(pp)==len(vv)==3
    assert all(sorted(p)==list(range(n)) for p in pp)
    assert all(len(v)==n and all(type(a)is int for a in v) for v in vv)
    pi=[tuple(p.index(i) for i in range(n)) for p in pp]
    N=2*n;one=(tuple(range(N)),(0,)*N)
    marks=[(tuple(range(n,N))+tuple(range(n)),(0,)*N)]
    for p,v,q in zip(pp,vv,pi):
        marks.append((tuple(n+q[i] for i in range(n))+p,
                      tuple(-v[q[i]] for i in range(n))+v))
    def mul(a,b):
        p,v=a;q,w=b
        return tuple(q[i] for i in p),tuple(v[i]+w[p[i]] for i in range(N))
    def inv(a):
        p,v=a;q=tuple(p.index(i) for i in range(N))
        return q,tuple(-v[i] for i in q)
    def power(a,k):
        if k<0:return power(inv(a),-k)
        b=one
        while k:
            if k&1:b=mul(b,a)
            a=mul(a,a);k//=2
        return b
    def prod(*items):
        a=one
        for b in items:a=mul(a,b)
        return a
    assert all(mul(a,a)==one for a in marks)
    x,y,z=[mul(marks[0],a) for a in marks[1:]]
    rel=[power(x,6),power(y,3),power(z,2),power(prod(z,x),3),
         power(prod(z,y),6),power(prod(inv(x),y),2),
         power(prod(inv(y),power(x,-2)),3),power(prod(z,power(x,3)),2),
         prod(inv(x),z,power(prod(inv(y),z),2),z,x,power(prod(z,y),2))]
    assert all(a==one for a in rel)
    T=prod(y,power(prod(z,y),2));A=power(T,3)
    u=prod(inv(y),z);B=prod(inv(u),A,u)
    assert A[0]==B[0]==one[0] and T[0]!=one[0]
    assert set(A[1])=={-2,0,2} and set(B[1])=={-2,0,2}
    minor=[[A[1][i],B[1][i]] for i in [1,0]]
    assert minor==[[0,-2],[-2,0]]
    assert minor[0][0]*minor[1][1]-minor[0][1]*minor[1][0]==-4
    print('All first-nine source relators and scaled-unit local lattice minor PASS',flush=True)

    # Three fixed maximal parabolics close over the integers and project
    # injectively to their underlying permutations, hence to every modulus.
    fixed_orders={}
    for mask,expected in [(14,36),(11,48),(7,108)]:
        gens=[marks[i] for i in range(4) if mask>>i&1]
        seen={one[0]:one};todo=deque([one])
        while todo:
            a=todo.popleft()
            for g in gens:
                b=mul(a,g)
                if b[0] in seen:assert b==seen[b[0]]
                else:seen[b[0]]=b;todo.append(b)
            assert len(seen)<=expected
        assert len(seen)==expected;fixed_orders[str(mask)]=len(seen)
    print('Three fixed integer parabolics PASS',flush=True)

    # Modulus two gives the source parameter-three base.
    baseone=tuple(range(2*N))
    basegens=[tuple(2*p[i]+((t+v[i])%2) for i in range(N) for t in range(2)) for p,v in marks]
    perms=[baseone];index={baseone:0};todo=deque([baseone])
    while todo:
        p=todo.popleft()
        for g in basegens:
            q=tuple(g[i] for i in p)
            if q not in index:index[q]=len(perms);perms.append(q);todo.append(q)
        assert len(perms)<=13824
    assert len(perms)==13824
    gen_ids=[index[a] for a in basegens]
    @lru_cache(None)
    def pmul(i,j):return index[tuple(perms[j][a] for a in perms[i])]
    def closure(gens):
        seen={0};todo=deque([0])
        while todo:
            a=todo.popleft()
            for g in gens:
                b=pmul(a,g)
                if b not in seen:seen.add(b);todo.append(b)
        return frozenset(seen)
    groups={mask:closure([gen_ids[i] for i in range(4) if mask>>i&1])
            for mask in range(16)}
    assert len(groups[15])==13824
    assert all(groups[a]&groups[b]==groups[a&b] for a in range(16) for b in range(16))
    par_masks=[14,13,11,7];pars=[groups[m] for m in par_masks]
    assert list(map(len,pars))==[36,108,48,108]
    print('Base order13824 and all256 marked meets PASS',flush=True)
    @lru_cache(None)
    def par_product(i,j):return frozenset(pmul(a,b) for a in pars[i] for b in pars[j])
    helly=[]
    for i in range(4):
        others=[j for j in range(4) if j!=i]
        for mask in range(1,8):
            js=[others[k] for k in range(3) if mask>>k&1]
            if len(js)<2:continue
            j0=js[0];meet=pars[i]&pars[j0];covered=set();reps=[]
            for a in sorted(pars[j0]):
                if a in covered:continue
                reps.append(a);covered.update(pmul(t,a) for t in meet)
            assert covered==pars[j0]
            count=sum(all(a in par_product(i,j) for j in js[1:]) for a in reps)
            common=set(pars[js[0]])
            for j in js[1:]:common.intersection_update(pars[j])
            expected=len(common)//len(common&pars[i]);assert count==expected
            helly.append([i,js,count,expected])
    print('All16 base typed-Helly cardinalities PASS',flush=True)
    report={'status':'PASS','checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'data_sha256':sha256(raw).hexdigest(),'states':N,'source_relators':9,
        'relator_state_checks':9*N,'fixed_integer_parabolic_orders':fixed_orders,
        'base_group_order':13824,'base_subgroup_orders':{str(k):len(v) for k,v in groups.items()},
        'base_maximal_parabolic_orders':list(map(len,pars)),'subset_meets':256,
        'typed_helly_checks':helly,'parameter_word':'T=y(zy)^2',
        'parameter_base_order':3, 'coordinate_base_modulus':2,'translation_words':['A=T^3','B=u^-1 A u, u=y^-1 z'],
        'translation_coordinate_indices_zero_based':[1,0],
        'translation_minor':minor,'translation_minor_determinant':-4,
        'scope':'Literal integer first-nine-relator representation, three injective finite parabolics, exact base geometry and twice-unimodular local translation minor. Written all-but-one quotient transport and toroidal order sandwich give the full all-multiples-of-three-source-parameter family; no all-parameter or universal-group-size claim.'}
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print('PHASE34_L003_TRIPLE_PASS',flush=True)


if __name__=='__main__':main()
