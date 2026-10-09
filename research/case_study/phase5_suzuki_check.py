"""Exact small coordinate checks for the Suzuki realization proof.

Standard-library arithmetic only. These checks corroborate the uniform
proof; they do not enumerate every conjugate subfield group in a large G.
"""
from collections import Counter
from pathlib import Path
from math import gcd
import hashlib
import json
import time


def factors(n):
    result = []
    d = 2
    while d*d <= n:
        if n % d == 0:
            result.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        result.append(n)
    return result


class Field:
    def __init__(self, n, modulus):
        self.n, self.q, self.modulus = n, 1 << n, modulus
        assert modulus.bit_length() == n+1
        # An orbit containing every nonzero polynomial class certifies both
        # that the quotient is a field and that x is primitive.
        self.exps, self.logs = [], [-1] * self.q
        x = 1
        for i in range(self.q-1):
            assert x != 0 and self.logs[x] == -1
            self.exps.append(x)
            self.logs[x] = i
            x <<= 1
            if x & self.q:
                x ^= modulus
        assert x == 1 and all(v >= 0 for v in self.logs[1:])
        self.theta = 1 << ((n+1)//2)

    def mul(self, a, b):
        return 0 if a == 0 or b == 0 else self.exps[
            (self.logs[a]+self.logs[b]) % (self.q-1)]

    def power(self, a, k):
        if a == 0:
            assert k >= 0
            return int(k == 0)
        return self.exps[self.logs[a]*k % (self.q-1)]

    def subfield(self, d):
        assert self.n % d == 0
        return {0} | {self.exps[i] for i in
                     range(0, self.q-1, (self.q-1)//((1 << d)-1))}

    def mm(self, a, b):
        out = [0] * 16
        for i in range(4):
            for k in range(4):
                if a[4*i+k]:
                    for j in range(4):
                        out[4*i+j] ^= self.mul(a[4*i+k], b[4*k+j])
        return tuple(out)

    def mpow(self, a, n):
        out = ID
        while n:
            if n & 1:
                out = self.mm(out, a)
            a = self.mm(a, a)
            n >>= 1
        return out

    def U(self, a, b):
        at = self.power(a, self.theta)
        return (1,0,0,0, a,1,0,0,
                self.mul(at,a)^b,at,1,0,
                self.mul(at,self.mul(a,a))^self.mul(a,b)^self.power(b,self.theta),
                b,a,1)

    def h(self, a):
        return (self.power(a,self.theta+1),0,0,0, 0,a,0,0,
                0,0,self.power(a,-1),0,
                0,0,0,self.power(a,-self.theta-1))

    def in_H(self, a):
        if a[5] == 0:
            return False
        return a == self.h(a[5])

    def in_N(self, a):
        return self.in_H(a) or self.in_H(self.mm(a,W))

    def in_ZH(self, a):
        if a[5] == 0 or a[0] == 0:
            return False
        b = self.mul(a[8], self.power(a[0],-1))
        return a == self.mm(self.U(0,b), self.h(a[5]))

    def conjugate(self, a, u, ui):
        return self.mm(self.mm(ui,a),u)

    def generated(self, generators, expected_max):
        found, queue = {ID}, [ID]
        for a in queue:
            for b in generators:
                c = self.mm(a,b)
                if c not in found:
                    found.add(c)
                    queue.append(c)
                    assert len(found) <= expected_max
        return found

    def order(self, a):
        n = self.q*self.q*(self.q*self.q+1)*(self.q-1)
        assert self.mpow(a,n) == ID
        for p in factors(n):
            while n % p == 0 and self.mpow(a,n//p) == ID:
                n //= p
        return n


ID = tuple(int(i == j) for i in range(4) for j in range(4))
W = tuple(int(i+j == 3) for i in range(4) for j in range(4))
MODULI = {3:0b1011, 5:0b100101, 7:0b10001001,
          9:0b1000010001, 15:0b1000000000000011}


def trace_checks(F):
    by_order = {}
    for a in range(1,F.q):
        g = F.mm(W,F.U(0,a))
        assert g[0]^g[5]^g[10]^g[15] == F.power(a,F.theta)
        order = F.order(g)
        assert order % 2 == 1 and order > 1
        by_order.setdefault(order,[]).append(a)
    assert sum(map(len,by_order.values())) == F.q-1
    records = []
    for p in sorted(factors((F.q-1)*(F.q*F.q+1))):
        assert p in by_order
        a = by_order[p][0]
        D = F.generated([W,F.U(0,a)],2*p)
        assert len(D) == 2*p
        assert sum(F.in_N(x) for x in D) == 2
        assert sum(F.in_ZH(x) for x in D) == 2
        assert sum(F.in_N(x) and F.in_ZH(x) for x in D) == 1
        records.append({"prime":p, "parameter":a, "dihedral_order":len(D)})

    # R1: opposite small affine subgroups transported to the fixed points
    # of W and U(0,a).  W fixes (1,1,1,1); U(1,1) takes (0,0,0,1) there.
    r1_parameter = by_order[F.q-1][0]
    D = F.generated([W,F.U(0,r1_parameter)],2*(F.q-1))
    v, vi = F.U(1,1), F.mpow(F.U(1,1),3)
    assert F.mm(v,vi) == ID
    def in_A(x):
        return F.in_ZH(F.conjugate(x,vi,v))
    def in_B(x):
        y = F.conjugate(x,vi,v)
        return F.in_ZH(F.mm(F.mm(W,y),W))
    assert sum(in_A(x) for x in D) == 2
    assert sum(in_B(x) for x in D) == 2
    assert sum(in_A(x) and in_B(x) for x in D) == 1
    for h in (F.h(lam) for lam in range(1,F.q)):
        x = F.conjugate(h,v,vi)
        assert in_A(x) and in_B(x)
    R3 = []
    primes = sorted(factors((F.q-1)*(F.q*F.q+1)))
    for p_index,p in enumerate([2]+primes):
        others = primes if p == 2 else primes[primes.index(p):]
        for p2 in others:
            t = by_order[F.q-1][0]
            if p == 2:
                x = next(x for x in by_order[p2] if x != t)
                a,b,c = W,F.U(0,t),F.U(0,x)
            elif p == p2:
                x = next(x for x in by_order[p] if x != t)
                z = F.U(0,t)
                a,b,c = W,F.mm(F.mm(z,W),z),F.U(0,x)
            else:
                x,y = by_order[p][0],by_order[p2][0]
                ratio = F.mul(F.power(y,F.theta),F.power(x,-F.theta))
                lam = F.power(ratio,pow(F.theta+1,-1,F.q-1))
                assert lam != 1
                a,b,c = W,F.mm(F.h(lam),W),F.U(0,x)
            A = F.generated([a,b],2*(F.q-1))
            B = F.generated([b,c] if p == 2 else [a,c],2*p)
            C = F.generated([a,c] if p == 2 else [b,c],2*p2)
            assert [len(A),len(B),len(C)] == [2*(F.q-1),2*p,2*p2]
            assert [len(A&B),len(A&C),len(B&C),len(A&B&C)] == [2,2,2,1]
            R3.append({"p":p,"p_prime":p2,"pair_group_orders":[len(A),len(B),len(C)],
                       "intersection_orders":[2,2,2,1]})
    return {"q":F.q, "order_distribution":{str(k):len(v) for k,v in sorted(by_order.items())},
            "R2_witnesses":records, "R1_parameter":r1_parameter,
            "R1_intersection_orders":[2,2,F.q-1,1],
            "R3_all_unordered_prime_parameters":R3}


def field_position_checks(F):
    divisors = [d for d in range(1,F.n+1) if F.n % d == 0]
    subfields = {d:F.subfield(d) for d in divisors}
    for d,A in subfields.items():
        assert len(A) == 1 << d
        assert all(F.power(a,F.theta) == F.power(a,1 << ((d+1)//2)) for a in A)
        assert all(F.power(a,1 << d) == a for a in A)
    for a,A in subfields.items():
        for b,B in subfields.items():
            assert A & B == subfields[gcd(a,b)]

    S2 = F.generated([F.U(1,0),W],20)
    assert len(S2) == 20
    assert Counter(F.order(x) for x in S2) == Counter({1:1,2:5,4:10,5:4})
    assert all(set(x) <= {0,1} for x in S2)
    # Direct commutation check for central root elements and representative
    # U-elements; the universal identity is proved in the note.
    sample = sorted(set([0,1,2,3,F.q-1,F.q//2]))
    for a in sample:
        for b in sample:
            u = F.U(a,b)
            for c in sample:
                z = F.U(0,c)
                assert F.mm(u,z) == F.mm(z,u)
    return {"q":F.q, "subfield_degrees":divisors, "all_pairwise_field_intersections_checked":True,
            "Sz2_order":20, "Sz2_element_orders":{"1":1,"2":5,"4":10,"5":4},
            "center_commutation_samples":len(sample)**3}


def R7_checks(F):
    records = []
    for d in range(3,F.n,2):
        if F.n % d or len(factors(F.n//d)) != 1 or factors(F.n//d)[0] != F.n//d:
            continue
        s, A = 1 << d, F.subfield(d)
        for p in factors((F.q-1)//(s-1)):
            m = (s-1)*p
            M = {F.exps[i] for i in range(0,F.q-1,(F.q-1)//m)}
            assert len(M) == m and M & A == A-{0}
            # Prime relative field degree plus order> s-1 means full degree.
            lam = F.exps[(F.q-1)//m]
            assert min(j for j in range(1,F.n+1) if F.power(lam,1 << j) == lam) == F.n
            D = {F.h(x) for x in M} | {F.mm(F.h(x),W) for x in M}
            assert len(D) == 2*m
            DS = {x for x in D if set(x) <= A}
            assert len(DS) == 2*(s-1)
            assert sum(F.in_ZH(x) for x in D) == m
            # G0∩G2 recognized by parameters: all Z_s H_s matrices lie over
            # Fs and are in Zq Hm; their distinct number is s(s-1).
            affine = {F.mm(F.U(0,b),F.h(l)) for b in A for l in A-{0}}
            assert len(affine) == s*(s-1)
            assert all(F.in_ZH(x) and set(x) <= A for x in affine)
            assert len(DS & affine) == s-1
            records.append({"q":F.q,"s":s,"prime":p,"m":m,
                            "intersection_orders":[2*(s-1),s*(s-1),m,s-1],
                            "torus_scalar_field_degree":F.n})
    return records


def main():
    started = time.monotonic()
    fields = {n:Field(n,m) for n,m in MODULI.items()}
    result = {
        "scope":"Exact coordinate examples and parameter tests; no exhaustive conjugate-subfield search.",
        "field_moduli":{str(n):m for n,m in MODULI.items()},
        "trace_and_small_lattice_checks":[trace_checks(fields[n]) for n in [3,5,7]],
        "field_position_checks":[field_position_checks(fields[n]) for n in [3,9,15]],
        "R7_realizations":[r for n in [9,15] for r in R7_checks(fields[n])],
        "status":"PASS",
        "elapsed_seconds":round(time.monotonic()-started,3),
        "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    target = Path(__file__).with_suffix(".json")
    target.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
