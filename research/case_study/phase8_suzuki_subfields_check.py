"""Exact checks for the phase-eight pure-field and scalar-center arguments.

Standard library only. The finite group calculation enumerates Q=Z_512 U_8 H_8,
its subgroup H=U_8 H_8 and every scalar-center overgroup of H. It does not
enumerate an ambient Suzuki group or prove the uniform written theorem.
"""
from collections import deque
from itertools import combinations
from pathlib import Path
import hashlib
import json
import math
import time


def poly_mod(a, b):
    while a.bit_length() >= b.bit_length():
        a ^= b << (a.bit_length() - b.bit_length())
    return a


def poly_gcd(a, b):
    while b:
        a, b = b, poly_mod(a, b)
    return a


class F512:
    n = 9
    size = 512
    modulus = (1 << 9) | (1 << 4) | 1

    @staticmethod
    def mul(a, b):
        z = 0
        while b:
            if b & 1:
                z ^= a
            b >>= 1
            a <<= 1
            if a & 512:
                a ^= F512.modulus
        return z

    @staticmethod
    def power(a, k):
        if k < 0:
            assert a
            k %= 511
        z = 1
        while k:
            if k & 1:
                z = F512.mul(z, a)
            a = F512.mul(a, a)
            k >>= 1
        return z


def span(*vectors):
    values = {0}
    for v in vectors:
        values |= {x ^ v for x in values}
    return values


def suzuki_order(d):
    q = 1 << d
    return q * q * (q * q + 1) * (q - 1)


def main():
    started = time.monotonic()
    F = F512
    # Rabin irreducibility: prime divisors of 9 consist of 3.
    assert F.power(2, 1 << 9) == 2
    assert poly_gcd(F.power(2, 1 << 3) ^ 2, F.modulus) == 1
    ft = sorted(x for x in range(512) if F.power(x, 8) == x)
    assert len(ft) == 8
    nonzero = ft[1:]
    lam = nonzero[1]
    assert F.power(lam, 7) == 1 and lam != 1
    # Full multiplication table makes the exhaustive closures independent
    # of any computer-algebra group package.
    mul = [[F.mul(a, b) for b in range(512)] for a in range(512)]
    theta = [F.power(a, 32) for a in range(512)]
    lt = {x: F.power(x, 32) for x in nonzero}
    lz = {x: F.power(x, 34) for x in nonzero}
    assert set(lt.values()) == set(nonzero) == set(lz.values())

    # Coordinates represent U(a,b) h(lambda)^(-1).
    # U(a,b)U(c,d)=U(a+c,b+d+a*c^theta).
    def product(x, y):
        a, b, l = x
        c, d, u = y
        c = mul[lt[l]][c]
        return (a ^ c, b ^ mul[lz[l]][d] ^ mul[a][theta[c]], mul[l][u])

    identity = (0, 0, 1)
    hgens = [(1, 0, 1), (0, 1, 1), (0, 0, lam)]

    def generated(gens, bound):
        known = {identity}
        queue = deque([identity])
        while queue:
            x = queue.popleft()
            for g in gens:
                y = product(x, g)
                if y not in known:
                    known.add(y)
                    assert len(known) <= bound
                    queue.append(y)
        return known

    def model(center):
        return {(a, b, l) for a in ft for b in center for l in nonzero}

    H = generated(hgens, 448)
    assert H == model(ft)
    # Each nonzero first coordinate has order four; all remaining
    # nonidentity unipotents have order two.
    assert all(product((a, b, 1), (a, b, 1)) == (0, mul[a][theta[a]], 1)
               for a in ft for b in range(512))
    # Check the action formula in actual 4x4 matrices, independently
    # of the coordinate group law, for all 28672 (a,b,lambda).
    def mm(a, b):
        out = [0] * 16
        for i in range(4):
            for k in range(4):
                if a[4*i+k]:
                    for j in range(4):
                        out[4*i+j] ^= mul[a[4*i+k]][b[4*k+j]]
        return tuple(out)

    def U(a, b):
        A, B = theta[a], theta[b]
        return (1,0,0,0,a,1,0,0,mul[a][A]^b,A,1,0,
                mul[mul[a][a]][A]^mul[a][b]^B,b,a,1)

    def diagonal(l):
        entries = [F.power(l, 33), l, F.power(l, -1), F.power(l, -33)]
        return tuple(entries[i//4] if i//4 == i%4 else 0 for i in range(16))

    for l in nonzero:
        h, hi = diagonal(l), diagonal(F.power(l, -1))
        for a in ft:
            for b in range(512):
                assert mm(mm(hi, U(a, b)), h) == U(mul[lt[l]][a], mul[lz[l]][b])
    assert all(mm(U(a,b), U(c,d)) == U(a^c, b^d^mul[a][theta[c]])
               for a in ft for b in ft for c in ft for d in ft)

    # F512/F8 is three-dimensional. The F8-subspaces containing F8
    # consist of its base line, nine planes, and the whole space.
    planes = {}
    for v in range(512):
        if v not in ft:
            V = frozenset(x ^ mul[c][v] for x in ft for c in ft)
            assert len(V) == 64
            planes.setdefault(V, v)
    assert len(planes) == 9
    records = []
    for V, v in sorted(planes.items(), key=lambda pair: pair[1]):
        K = generated(hgens + [(0, v, 1)], 3584)
        assert K == model(V)
        assert H < K
        records.append({"extra_center_vector": v, "order": len(K),
                        "index_over_H": len(K)//len(H),
                        "index_in_Q": 28672//len(K),
                        "center": sorted(V)})
    v = next(x for x in range(512) if x not in ft)
    V = frozenset(x ^ mul[c][v] for x in ft for c in ft)
    w = next(x for x in range(512) if x not in V)
    Q = generated(hgens + [(0, v, 1), (0, w, 1)], 28672)
    assert Q == model(range(512))
    assert {(a, l) for a, b, l in H} == {(a, l) for a, b, l in Q}
    # Bind the four root generators used for Q to actual matrices,
    # including the two central coordinates outside F8. These are
    # finite checks of the displayed multiplication formula, alongside
    # the exhaustive diagonal-action check.
    rootgens = [(1, 0), (0, 1), (0, v), (0, w)]
    for a in ft:
        for b in range(512):
            for c, d in rootgens:
                assert mm(U(a,b), U(c,d)) == U(a^c, b^d^mul[a][theta[c]])

    # The all-simple rank-four omitted boundary. Only exact degree
    # arithmetic is checked here; no enormous field is instantiated.
    primes = (3, 5, 7, 11)
    n, e = 3465, 3
    lattice = []
    for r in range(5):
        for J in combinations(range(4), r):
            d = n // math.prod(primes[j] for j in J)
            assert d == e * math.prod(primes[j] for j in range(4) if j not in J)
            for j in range(4):
                if j not in J:
                    assert d % primes[j] == 0 and d//primes[j] >= e
            lattice.append({"types": list(J), "field_exponent": d})
    assert len(lattice) == 16 and lattice[-1]["field_exponent"] == 3

    # Explicit proper torus overgroups of S1 in S_a for a>=5.
    torus_boundaries = []
    for a in (3,5,7,11,13,17,19,23,29,31):
        q = 1 << a
        orders = [q + 1 - (1 << ((a+1)//2)),
                  q + 1 + (1 << ((a+1)//2))]
        h = next(x for x in orders if x % 5 == 0)
        assert (h == 5) == (a == 3)
        assert 4*h < suzuki_order(a)
        torus_boundaries.append({"prime_degree": a, "torus_containing_C5": h,
                                 "overgroup_order": 4*h,
                                 "strict_over_Sz2": h > 5})
    # Number-theoretic conditions behind scalar action, checked far
    # beyond the finite group example (not a uniform proof).
    for d in range(3, 1000, 2):
        assert math.gcd((1 << ((d+1)//2)) + 2, (1 << d) - 1) == 1
    report = {
        "status": "PASS",
        "scope": "Exact finite module/group and parameter checks; uniform results require written proof.",
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "field": {"degree": 9, "irreducible_modulus": F.modulus, "subfield_F8": ft},
        "matrix_action_checks": 28672,
        "matrix_unipotent_product_checks": 4096,
        "matrix_root_generator_product_checks": 16384,
        "Q_order": len(Q), "H_order": len(H),
        "H_surjects_affine_quotient": True,
        "scalar_center_overgroup_count": 11,
        "proper_intermediate_count": len(records),
        "proper_intermediates": records,
        "pure_field_boundary": {"n": n, "selected_primes": primes, "bottom_exponent": e,
                                "source_m": 4, "rank": 4, "intersection_lattice": lattice},
        "Sz2_normalizer_boundaries": torus_boundaries,
        "scalar_coprimality_odd_degrees_checked": [3, 999],
        "elapsed_seconds": round(time.monotonic()-started, 6),
    }
    out = json.dumps(report, indent=2) + "\n"
    Path(__file__).with_suffix(".json").write_text(out)
    print(out, end="")


if __name__ == "__main__":
    main()
