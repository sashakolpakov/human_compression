"""Exact seed and polynomial checks for the uniform Suzuki descent proof.

Does not prove Lang--Steinberg or replace the all-rank paper argument.
All arithmetic below uses the Python standard library. Old outputs are read
only; this script writes only its own phase7 JSON.
"""
from pathlib import Path
from math import gcd, prod
import hashlib
import json
import time

from phase5_suzuki_check import Field, ID, W
from phase6_suzuki_torus_check import mat_pow, generated, sz_member


# Sparse polynomials over F2; negative exponents are also allowed, for tori.
def add(a, b):
    return a ^ b


def mul(a, b):
    out = set()
    for x in a:
        for y in b:
            z = tuple(u + v for u, v in zip(x, y))
            if z in out:
                out.remove(z)
            else:
                out.add(z)
    return frozenset(out)


def mono(*exponents):
    return frozenset([tuple(exponents)])


PAIRS = [(0, 1), (0, 2), (1, 3), (2, 3)]


def rho_poly(g):
    out = []
    for i, j in PAIRS:
        for k, l in PAIRS:
            out.append(add(mul(g[4*i+k], g[4*j+l]),
                           mul(g[4*i+l], g[4*j+k])))
    return tuple(out)


def square_poly(g):
    return tuple(frozenset(tuple(2*x for x in v) for v in p) for p in g)


def polynomial_model_checks():
    z, one = frozenset(), mono(0, 0, 0, 0)
    a, A, b, B = [mono(*(int(i == j) for i in range(4))) for j in range(4)]
    U = (
        one, z, z, z,
        a, one, z, z,
        add(mul(a, A), b), A, one, z,
        add(add(mul(mul(a, a), A), mul(a, b)), B), b, a, one
    )

    def exceptional_substitution(p):
        return frozenset((2*v[1], v[0], 2*v[3], v[2]) for v in p)

    rho_U = rho_poly(U)
    assert rho_U == tuple(exceptional_substitution(p) for p in U)
    assert rho_poly(rho_U) == square_poly(U)
    # Direct symplectic identity U^t J U = J for four independent variables.
    for i in range(4):
        for j in range(4):
            value = z
            for k in range(4):
                value = add(value, mul(U[4*k+i], U[4*(3-k)+j]))
            assert value == (one if i+j == 3 else z)

    z2, one2 = frozenset(), mono(0, 0)
    x, y, yi, xi = mono(1, 0), mono(0, 1), mono(0, -1), mono(-1, 0)
    D = tuple([x, z2, z2, z2, z2, y, z2, z2,
               z2, z2, yi, z2, z2, z2, z2, xi])
    assert rho_poly(rho_poly(D)) == square_poly(D)
    w = tuple(one2 if i//4+i%4 == 3 else z2 for i in range(16))
    assert rho_poly(w) == w
    # Every quotient-basis column has equal omitted 14 and 23 coefficients:
    # it is in ker(contraction), and their sum is the discarded invariant line.
    for k, l in PAIRS:
        omitted_14 = add(mul(U[k], U[12+l]), mul(U[l], U[12+k]))
        omitted_23 = add(mul(U[4+k], U[8+l]), mul(U[4+l], U[8+k]))
        assert omitted_14 == omitted_23
    return {
        "generic_unipotent_variables": ["a", "A", "b", "B"],
        "exceptional_parameter_map": ["A", "a^2", "B", "b^2"],
        "generic_unipotent_symplectic_identity": True,
        "rho_squared_is_frobenius_on_unipotents": True,
        "rho_squared_is_frobenius_on_diagonal_torus": True,
        "rho_fixes_antidiagonal_w": True,
        "wedge_quotient_basis": ["12", "13", "24", "34"],
        "quotient_kernel_coefficients_checked": True,
    }


def rho_matrix(F, g):
    return tuple(
        F.mul(g[4*i+k], g[4*j+l]) ^ F.mul(g[4*i+l], g[4*j+k])
        for i, j in PAIRS for k, l in PAIRS
    )


def tau(d):
    assert d > 0 and d % 2
    a, b = 2, 2
    for _ in range(1, d):
        a, b = b, 2*b-2*a
    return (1 << d)+1-b


def factors(n):
    out = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0)+1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0)+1
    return out


def main():
    started = time.monotonic()
    here = Path(__file__).parent
    phase6_path = here/"phase6_suzuki_torus_check.json"
    phase6 = json.loads(phase6_path.read_text())
    assert hashlib.sha256(phase6_path.read_bytes()).hexdigest() == \
        "6873f35b666700ee0e90eb3fd6618d687cdf43949b78eb9b3ad604b267a13376"
    model = polynomial_model_checks()
    F = Field(3, 11)
    M = tuple(phase6["F2_order15_algebra_generator"])
    r = tuple(phase6["F2_order4_normalizer"])
    a = tuple(phase6["base_F8_order13_matrix"])
    assert mat_pow(F, M, 15) == ID
    assert not any(x ^ y ^ z for x, y, z in zip(mat_pow(F, M, 4), M, ID))
    assert mat_pow(F, a, 13) == ID and a != ID
    assert all(pow(8, i, 13) != 1 for i in [1, 2, 3])
    assert pow(8, 4, 13) == 1
    assert F.mm(a, M) == F.mm(M, a)
    assert sz_member(F, a)
    ra = rho_matrix(F, a)
    assert ra == tuple(F.power(x, 4) for x in a)
    assert rho_matrix(F, ra) == tuple(F.power(x, 2) for x in a)
    assert rho_matrix(F, rho_matrix(F, ra)) == a
    assert rho_matrix(F, r) == r and rho_matrix(F, W) == W
    S2 = generated(F, [r, W], 20)
    assert len(S2) == 20 and all(rho_matrix(F, g) == g for g in S2)
    fixed = [g for g in S2 if F.mm(g, M) == F.mm(M, g)]
    assert fixed == [ID]
    five = F.mm(mat_pow(F, r, 2), W)
    assert mat_pow(F, five, 5) == ID and five != ID
    assert F.mm(five, M) != F.mm(M, five)

    # Finite corroboration of the proved recurrence/arithmetic; not induction.
    sequence_checks = 0
    for d in range(1, 202, 2):
        sign = 1 if d % 8 in [1, 7] else -1
        t = tau(d)
        assert t == (1 << d)+1-sign*(1 << ((d+1)//2))
        other = 2*((1 << d)+1)-t
        assert t*other == (1 << (2*d))+1
        assert gcd(t, other) == 1
        sequence_checks += 1
    gcd_checks = 0
    for a0 in range(1, 100, 2):
        for b0 in range(1, 100, 2):
            assert gcd(tau(a0), tau(b0)) == tau(gcd(a0, b0))
            gcd_checks += 1
    quotient_checks = 0
    for e in range(3, 20, 2):
        for p in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
            if tau(e) % p == 0:
                continue
            assert tau(e*p) % tau(e) == 0
            quotient = tau(e*p)//tau(e)
            assert quotient > 1 and gcd(quotient, tau(e)) == 1
            quotient_checks += 1

    examples = []
    for p in [3, 5, 7, 11]:
        quotient = tau(3*p)//13
        fs = factors(quotient)
        assert prod(a0**v for a0, v in fs.items()) == quotient
        ell = min(fs)
        assert 13 % ell and gcd(13, ell) == 1
        examples.append({"relative_field_prime": p, "torus_degree": 3*p,
                         "torus_order": tau(3*p), "quotient": quotient,
                         "quotient_factorization": fs, "selected_prime": ell})
    assert len({v["selected_prime"] for v in examples}) == 4

    # Exact coordinate-cover input for the immutable rank-four instance:
    # V has product size, and the three indicated stabilizers omit one factor.
    rows = phase6["rank4"]["subfield_intersections"]
    n = 13*41*113
    assert phase6["rank4"]["torus_order"] == n
    coordinate_indices = []
    for p, ell in [(3, 13), (5, 41), (7, 113)]:
        row = next(v for v in rows if v["removed_field_primes"] == [p])
        assert row["torus_intersection_order"] == n//ell
        assert row["normalizer_intersection_order"] == 4*n//ell
        coordinate_indices.append(ell)
    bottom = next(v for v in rows if len(v["removed_field_primes"]) == 3)
    assert bottom["torus_intersection_order"] == 1
    assert bottom["normalizer_intersection_order"] == 4
    assert prod(coordinate_indices) == n

    # Thickness bound in the smallest base; formula grows for q >=8.
    assert (8**2*(8-1)*(2*(8+1)-tau(3)))//4 == 560
    result = {
        "status": "PASS",
        "scope": "Exact polynomial model, binary/F8 torus seed, integer examples and hash-bound coordinate inputs; not a computation of all-rank geometry or Lang theorem.",
        "polynomial_model": model,
        "seed": {"field_modulus": 11, "order13_matrix": list(a),
                 "algebra_matrix": list(M), "normalizing_order4_matrix": list(r),
                 "rho_cube_fixes_order13_matrix": True,
                 "rho_on_seed_equals_entrywise_fourth_power": True,
                 "Sz2_elements": 20, "Sz2_centralizer_of_M": 1,
                 "binary_order5_noncentralizing_matrix": list(five)},
        "finite_arithmetic": {"odd_degrees_checked": sequence_checks,
                              "gcd_pairs_checked": gcd_checks,
                              "new_prime_quotients_checked": quotient_checks},
        "rank5_example": {"base_degree": 3, "ambient_degree": 3465,
                          "parameters": examples,
                          "torus_subgroup_order": 13*prod(v["selected_prime"] for v in examples),
                          "ambient_field_or_group_enumerated": False},
        "rank4_coordinate_input": {"ambient_degree": 105, "V_order": n,
                                    "coset_indices": coordinate_indices,
                                    "intersection_with_V_order": 1},
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "input_hashes": {name: hashlib.sha256((here/name).read_bytes()).hexdigest()
                         for name in ["phase5_suzuki_check.py",
                                      "phase5_suzuki_higher_check.py",
                                      "phase6_suzuki_torus_check.py",
                                      "phase6_suzuki_torus_check.json"]},
        "elapsed_seconds": round(time.monotonic()-started, 3),
    }
    Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
