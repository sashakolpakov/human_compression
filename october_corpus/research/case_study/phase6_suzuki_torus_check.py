"""Exact common-torus witnesses, without enumerating the ambient Suzuki group."""
from pathlib import Path
import hashlib
import json
import time
from phase5_suzuki_check import Field, ID, W
from phase5_suzuki_higher_check import BinaryField, echelon, elements


def inv_U(F,a,b):
    return F.U(a,b ^ F.mul(a,F.power(a,1 << ((F.n+1)//2))))


def mat_pow(F,a,n):
    out=ID
    while n:
        if n & 1:
            out=F.mm(out,a)
        a=F.mm(a,a)
        n >>= 1
    return out


def sz_member(F,g):
    theta=1 << ((F.n+1)//2)
    if g[3]:
        d=F.power(g[3],-1)
        a,b=F.mul(g[2],d),F.mul(g[1],d)
        lam=F.power(g[3],pow(theta+1,-1,F.q-1))
        u=F.mm(F.mm(F.mm(g,inv_U(F,a,b)),W),F.h(F.power(lam,-1)))
    else:
        lam=g[5]
        if not lam:
            return False
        u=F.mm(g,F.h(F.power(lam,-1)))
    return u == F.U(u[4],u[13])


def binary_algebra_generator(F,a):
    # Kernel over F2 of X a = a X, X a binary-entry 4x4 matrix.
    pivots={}
    kernel=[]
    for j in range(16):
        E=tuple(int(i==j) for i in range(16))
        lhs,rhs=F.mm(E,a),F.mm(a,E)
        image=sum((x^y) << (F.n*i) for i,(x,y) in enumerate(zip(lhs,rhs)))
        witness=1 << j
        while image:
            p=image.bit_length()-1
            if p not in pivots:
                pivots[p]=(image,witness)
                break
            old,ow=pivots[p]
            image ^= old
            witness ^= ow
        else:
            kernel.append(witness)
    assert len(kernel)==4
    for v in elements(kernel):
        M=tuple((v >> i)&1 for i in range(16))
        if mat_pow(F,M,15)==ID and mat_pow(F,M,3)!=ID and mat_pow(F,M,5)!=ID:
            return M,kernel
    raise AssertionError("No primitive F16 algebra element")


def find_base_algebra():
    F=Field(3,11)
    r=F.U(1,0); ri=mat_pow(F,r,3)
    roots=[F.U(a,b) for a in range(8) for b in range(8)]
    tested=0
    for u in roots:
        for lam in range(1,8):
            left=F.mm(F.mm(u,F.h(lam)),W)
            for v in roots:
                a=F.mm(left,v)
                tested+=1
                if mat_pow(F,a,13)!=ID or a==ID:
                    continue
                f=tuple(F.mul(x,x) for x in a)
                if F.mm(a,f)!=F.mm(f,a):
                    continue
                b=F.mm(F.mm(ri,a),r)
                if F.mm(a,b)!=F.mm(b,a):
                    continue
                M,kernel=binary_algebra_generator(F,a)
                return F,a,r,M,kernel,tested
    raise AssertionError("No F2-defined order13 torus found")


def scalar_shift(M,lam):
    return tuple(x ^ (lam if i//4==i%4 else 0) for i,x in enumerate(M))


def torus_generator(F,M,degree,order,basis=None):
    if basis is None:
        scalar=F.exps[(F.q-1)//((1 << degree)-1)]
        scalars=[F.power(scalar,k) for k in range(1,(1 << degree)-1)]
    else:
        scalars=[a for a in elements(basis) if a not in [0,1]]
    for lam in scalars:
        g=mat_pow(F,scalar_shift(M,lam),((1 << (4*degree))-1)//order)
        if g!=ID and mat_pow(F,g,order)==ID and sz_member(F,g):
            assert all(F.power(x,1 << degree)==x for x in g)
            return g,lam
    raise AssertionError(("no torus generator",degree,order))


def generated(F,gens,limit):
    seen,queue={ID},[ID]
    for a in queue:
        for b in gens:
            c=F.mm(a,b)
            if c not in seen:
                seen.add(c);queue.append(c)
                assert len(seen)<=limit
    return seen


def main():
    started=time.monotonic()
    F8,a13,r,M,kernel,tested=find_base_algebra()
    assert set(M)<={0,1}
    assert not any(x^y^z for x,y,z in zip(mat_pow(F8,M,4),M,ID))
    assert mat_pow(F8,r,4)==ID and mat_pow(F8,r,2)!=ID
    ri=mat_pow(F8,r,3)
    automorphism=next(k for k in [2,8] if F8.mm(F8.mm(ri,M),r)==mat_pow(F8,M,k))
    F=Field(15,32771)
    a,l8=torus_generator(F,M,3,13)
    b,l32=torus_generator(F,M,5,41)
    rank3_a,rank3_b=a,b
    assert F.mm(a,b)==F.mm(b,a)
    c=F.mm(a,b)
    assert mat_pow(F,c,533)==ID and mat_pow(F,c,13)!=ID and mat_pow(F,c,41)!=ID
    ri=mat_pow(F,r,3)
    rc=F.mm(F.mm(ri,c),r)
    action=next(k for k in range(533) if mat_pow(F,c,k)==rc)
    assert pow(action,2,533)==532 and pow(action,4,533)==1
    K=generated(F,[c,r],2132)
    S2=generated(F,[F.U(1,0),W],20)
    assert len(K)==2132 and len(S2)==20
    def over(g,d):return all(F.power(x,1 << d)==x for x in g)
    K8={g for g in K if over(g,3)}
    K32={g for g in K if over(g,5)}
    assert [len(K8),len(K32),len(K&S2),len(K8&K32)]==[52,164,4,4]
    assert all(sz_member(F,g) for g in K)
    assert K8==generated(F,[a,r],52)
    assert K32==generated(F,[b,r],164)
    print("q=2^15 counterexample checks PASS",flush=True)

    # Rank4 extension: standard maximal subfields of F_(2^105), sharing
    # the same F2-defined algebra, with torus prime factors13,41,113.
    for tail in range(3,20000,2):
        try:
            L=BinaryField(105,(1 << 105)|tail);break
        except AssertionError:
            pass
    else:raise AssertionError("No degree105 irreducible modulus")
    gs=[];data=[]
    for d,p in [(3,13),(5,41),(7,113)]:
        basis=L.fixed_basis(d)
        g,lam=torus_generator(L,M,d,p,basis)
        assert sz_member(L,g)
        gs.append(g)
        data.append({"field_degree":d,"torus_prime":p,"scalar":lam,"matrix":list(g)})
    for a in gs:
        for b in gs:
            assert L.mm(a,b)==L.mm(b,a)
    product=ID
    for g in gs:product=L.mm(product,g)
    n=13*41*113
    assert mat_pow(L,product,n)==ID
    assert all(mat_pow(L,product,n//p)!=ID for p in [13,41,113])
    assert sz_member(L,r)
    ri=mat_pow(L,r,3)
    assert L.mm(L.mm(ri,product),r) in [mat_pow(L,product,L.q%n),mat_pow(L,product,(-L.q)%n)]
    # Intersections of the cyclic product with each marked subfield:
    # Frobenius-fixed powers are counted by prime-factor decomposition.
    intersection_rows=[]
    for subset in range(8):
        removed=[d for i,d in enumerate([3,5,7]) if subset >> i & 1]
        field_degree=105
        order=n
        for i,d in enumerate([3,5,7]):
            if subset >> i & 1:
                field_degree//=d;order//=[13,41,113][i]
        for i,g in enumerate(gs):
            fixed=all(L.frobenius(x,field_degree)==x for x in g)
            assert fixed == (not bool(subset >> i & 1))
        intersection_rows.append({"removed_field_primes":removed,"field_degree":field_degree,
                                  "torus_intersection_order":order,"normalizer_intersection_order":4*order})
    result={
        "status":"PASS",
        "scope":"Explicit matrices for a rank3 RWPRI lattice outside the L114 list and rank4 same-torus extension; classical maximality inputs retained.",
        "base_search_tested":tested,"base_F8_order13_matrix":list(a13),
        "binary_centralizer_kernel":kernel,"F2_order15_algebra_generator":list(M),
        "algebra_minimal_polynomial":"X^4+X+1",
        "F2_order4_normalizer":list(r),"algebra_action_exponent":automorphism,
        "rank3":{"q":32768,"field_modulus":32771,"order13_matrix":list(rank3_a),
                 "order41_matrix":list(rank3_b),"combined_torus_order":533,
                 "order13_scalar":l8,"order41_scalar":l32,
                 "normalizer_order":len(K),"action_exponent":action,
                 "intersection_orders":{"K_Sz8":52,"K_Sz32":164,"Sz8_Sz32":20,"triple":4},
                 "all_2132_normalizer_elements_tested_in_Suzuki":True},
        "rank4":{"field_degree":105,"modulus":L.modulus,"subfield_generators":data,
                 "torus_order":n,"normalizer_order":4*n,"subfield_intersections":intersection_rows},
        "elapsed_seconds":round(time.monotonic()-started,3),
        "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "dependency_hashes":{name:hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
          for name in ["phase5_suzuki_check.py","phase5_suzuki_higher_check.py"]},
    }
    Path(__file__).with_suffix(".json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":main()
