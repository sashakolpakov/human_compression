"""Exact binary linear-algebra certificate for the proposed R12 obstruction.

Uses F_(2^45), with subfields F_(2^9), F_(2^15), F_(2^3).
No group of order comparable to Sz(2^45) is enumerated.
"""
from pathlib import Path
import hashlib
import json
import time


def poly_mod(a,b):
    while a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length()-b.bit_length())
    return a


def poly_gcd(a,b):
    while b:
        a,b = b,poly_mod(a,b)
    return a


def prime_factors(n):
    out=[]
    p=2
    while p*p <= n:
        if n % p == 0:
            out.append(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        out.append(n)
    return out


class BinaryField:
    def __init__(self,n,modulus):
        self.n,self.q,self.modulus = n,1 << n,modulus
        assert modulus.bit_length() == n+1
        x=2
        powers=[x]
        for i in range(n):
            x=self.mul(x,x)
            powers.append(x)
        assert powers[n] == 2
        for p in prime_factors(n):
            assert poly_gcd(powers[n//p]^2,modulus) == 1
        self.rabin_powers=powers

    def mul(self,a,b):
        result=0
        while b:
            if b & 1:
                result ^= a
            b >>= 1
            a <<= 1
            if a & self.q:
                a ^= self.modulus
        return result

    def power(self,a,n):
        if n < 0:
            assert a
            n %= self.q-1
        out=1
        while n:
            if n & 1:
                out=self.mul(out,a)
            a=self.mul(a,a)
            n >>= 1
        return out

    def frobenius(self,a,d):
        for _ in range(d):
            a=self.mul(a,a)
        return a

    def fixed_basis(self,d):
        image_basis={}
        null=[]
        for j in range(self.n):
            image=self.frobenius(1 << j,d) ^ (1 << j)
            witness=1 << j
            while image:
                pivot=image.bit_length()-1
                if pivot not in image_basis:
                    image_basis[pivot]=(image,witness)
                    break
                old_image,old_witness=image_basis[pivot]
                image ^= old_image
                witness ^= old_witness
            else:
                null.append(witness)
        assert len(null) == d
        assert all(self.frobenius(x,d) == x for x in null)
        return null

    def mm(self,a,b):
        out=[0]*16
        for i in range(4):
            for k in range(4):
                if a[4*i+k]:
                    for j in range(4):
                        out[4*i+j] ^= self.mul(a[4*i+k],b[4*k+j])
        return tuple(out)

    def U(self,a,b):
        theta=(self.n+1)//2
        A=self.frobenius(a,theta)
        B=self.frobenius(b,theta)
        return (1,0,0,0,a,1,0,0,self.mul(a,A)^b,A,1,0,
                self.mul(A,self.mul(a,a))^self.mul(a,b)^B,b,a,1)

    def h(self,lam):
        theta=1 << ((self.n+1)//2)
        return (self.power(lam,theta+1),0,0,0,0,lam,0,0,
                0,0,self.power(lam,-1),0,0,0,0,self.power(lam,-theta-1))


def echelon(vectors):
    basis={}
    for v in vectors:
        while v:
            p=v.bit_length()-1
            if p not in basis:
                basis[p]=v
                break
            v ^= basis[p]
    return basis


def inside(v,basis):
    while v:
        p=v.bit_length()-1
        if p not in basis:
            return False
        v ^= basis[p]
    return True


def elements(basis):
    out=[0]
    for a in basis:
        out += [v^a for v in out]
    return out


def main():
    started=time.monotonic()
    n=45
    for tail in range(3,10000,2):
        try:
            F=BinaryField(n,(1 << n)|tail)
            break
        except AssertionError:
            pass
    else:
        raise AssertionError("No irreducible modulus found")
    sub={d:F.fixed_basis(d) for d in [3,9,15]}
    spaces={d:echelon(B) for d,B in sub.items()}
    assert len(echelon(sub[9]+sub[15])) == 21
    assert all(inside(x,spaces[9]) and inside(x,spaces[15]) for x in sub[3])
    Ft=elements(sub[3])
    lam=next(x for x in Ft if x not in [0,1])
    assert F.power(lam,7) == 1
    h,hi=F.h(lam),F.h(F.power(lam,-1))
    records=[]
    for d in [9,15]:
        v=next(1 << j for j in range(n) if not inside(1 << j,spaces[d]))
        V=echelon(sub[d]+[F.mul(a,v) for a in sub[3]])
        assert len(V) == d+3 < n
        assert all(inside(F.mul(a,b),V) for a in Ft for b in V.values())
        # The Frobenius square root restricts correctly to every subfield.
        assert all(F.frobenius(b,23) == F.frobenius(b,(d+1)//2) for b in sub[d])
        # Direct matrix normalization on an F2 basis suffices for all z(V):
        # z is an additive homomorphism and V is an F2-vector space.
        for b in V.values():
            z=F.U(0,b)
            conjugate=F.mm(F.mm(hi,z),h)
            assert conjugate == F.U(0,conjugate[8])
            assert inside(conjugate[8],V)
            for a in Ft:
                for c in Ft:
                    u=F.U(a,c)
                    assert F.mm(u,z) == F.mm(z,u)
        records.append({
            "smaller_field_degree":d,
            "subfield_basis":sub[d],
            "extension_vector":v,
            "intermediate_center_basis":list(V.values()),
            "dimensions_over_F2":[d,len(V),n],
            "group_orders":[(1 << d)*8*7,(1 << len(V))*8*7,(1 << n)*8*7],
            "strict_intermediate_subgroup":True,
        })
    # Integer parameters for positive shapes7 and8 at the same ambient q.
    q,s,sp,t=1 << 45,1 << 9,1 << 15,8
    split=[]
    for p2 in [31,151]:
        p,m=73,7*73*p2
        assert (q-1) % m == 0
        from math import gcd
        assert gcd(m,s-1) == 7*p and gcd(m,sp-1) == 7*p2
        split.append({"p":p,"p_prime":p2,"m":m})
    nonsplit=[]
    aq=q+(1 << 23)+1
    for p2 in [41,61]:
        m,p=13,37
        order=m*p*p2
        assert aq % order == 0
        assert gcd(order,481) == m*p and gcd(order,32513) == m*p2
        nonsplit.append({"m":m,"p":p,"p_prime":p2,"torus_subgroup_order":order})
    result={
        "status":"PASS",
        "scope":"Exact F2^45 subspace/intermediate-subgroup certificate plus integer torus parameters; uniform claims remain written proofs.",
        "n":n,"modulus_binary_integer":F.modulus,
        "irreducibility":"Rabin criterion: x^(2^45)=x and gcd checks at degrees15,9.",
        "common_subfield_degree":3,"common_subfield_basis":sub[3],
        "rank_of_F2_9_plus_F2_15":21,
        "intermediate_subgroups":records,
        "shape7_integer_parameters":split,
        "shape8_integer_parameters":nonsplit,
        "elapsed_seconds":round(time.monotonic()-started,3),
        "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    Path(__file__).with_suffix(".json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
