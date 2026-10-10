#!/usr/bin/env python3
"""Exact abstract-word and polynomial checks for the triangle-wreath quotient.

No numerical triangle-group specialization, finite ambient-group recognition,
or source/author code imports are used. The all-s eigenvalue step is written.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path


PERM_ID = (0, 1, 2)


def perm_mul(a, b):
    return tuple(b[a[i]] for i in range(3))


def wreath_mul(a, b):
    aa, p = a
    bb, r = b
    return tuple(aa[i] + bb[p[i]] for i in range(3)), perm_mul(p, r)


def wreath_inv(a):
    aa, p = a
    pi = tuple(p.index(i) for i in range(3))
    return tuple(aa[pi[i]][::-1] for i in range(3)), pi


WREATH_ID = (("", "", ""), PERM_ID)


def product(*items):
    out = WREATH_ID
    for a in items:
        out = wreath_mul(out, a)
    return out


def power(a, n):
    if n < 0:
        return power(wreath_inv(a), -n)
    out = WREATH_ID
    for _ in range(n):
        out = wreath_mul(out, a)
    return out


def involution_cancel(word):
    stack = []
    for letter in word:
        if stack and stack[-1] == letter:
            stack.pop()
        else:
            stack.append(letter)
    return "".join(stack) or "1"


# Right coset representatives modulo <d>: {1,h} in V4 and {1,q,dq} in S3.
# Each finite-factor multiplication gives a representative followed by d^e.
# Moving that final d into the next factor uses only the shared involution d.
D_PERM = (1, 0, 2)
Q_PERM = (0, 2, 1)
S3_REPS = (PERM_ID, Q_PERM, perm_mul(D_PERM, Q_PERM))
S3_DECOMP = {
    perm_mul(t, D_PERM if e else PERM_ID): (j, e)
    for j, t in enumerate(S3_REPS) for e in range(2)
}
assert len(S3_DECOMP) == 6


def amalgam_reduce(word):
    word = word.replace("v", "dqd")
    syllables = []
    e = 0
    for letter in word:
        assert letter in "dhq"
        if letter == "d":
            e ^= 1
            continue
        factor = 0 if letter == "h" else 1
        if factor == 0:
            j = 1
            if syllables and syllables[-1][0] == factor:
                j ^= syllables.pop()[1]
        else:
            value = perm_mul(D_PERM if e else PERM_ID, Q_PERM)
            if syllables and syllables[-1][0] == factor:
                value = perm_mul(S3_REPS[syllables.pop()[1]], value)
            j, e = S3_DECOMP[value]
        if j:
            syllables.append((factor, j))
    return tuple(syllables), e


def normal(a):
    return tuple(amalgam_reduce(w) for w in a[0]), a[1]


# Integer polynomials in t, stored in increasing degree order.
def poly(a):
    if isinstance(a, int):
        a = (a,)
    a = tuple(a)
    while len(a) > 1 and a[-1] == 0:
        a = a[:-1]
    return a


ZERO, ONE, T = (0,), (1,), (0, 1)


def padd(a, b):
    return poly(tuple((a[i] if i < len(a) else 0) +
                      (b[i] if i < len(b) else 0)
                      for i in range(max(len(a), len(b)))))


def pneg(a):
    return tuple(-v for v in a)


def psub(a, b):
    return padd(a, pneg(b))


def pmul(a, b):
    c = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    return poly(c)


def psum(items):
    out = ZERO
    for item in items:
        out = padd(out, item)
    return out


def matrix(rows):
    return tuple(tuple(poly(c) for c in row) for row in rows)


MAT_ID = matrix(((1, 0, 0), (0, 1, 0), (0, 0, 1)))
MAT_ZERO = matrix(((0, 0, 0), (0, 0, 0), (0, 0, 0)))


def mmul(a, b):
    return tuple(tuple(psum(pmul(a[i][k], b[k][j]) for k in range(3))
                       for j in range(3)) for i in range(3))


def msub(a, b):
    return tuple(tuple(psub(a[i][j], b[i][j]) for j in range(3))
                 for i in range(3))


def mpow(a, n):
    out = MAT_ID
    for _ in range(n):
        out = mmul(out, a)
    return out


def pmod_six(a):
    # Exact reduction modulo t^2-3, not a floating point evaluation.
    ans = [0, 0]
    for i, c in enumerate(a):
        ans[i % 2] += c * 3 ** (i // 2)
    return poly(ans)


def mmod_six(a):
    return tuple(tuple(pmod_six(c) for c in row) for row in a)


def det3(a):
    return psub(psum(pmul(pmul(a[0][i], a[1][(i+1) % 3]),
                          a[2][(i+2) % 3]) for i in range(3)),
                psum(pmul(pmul(a[0][i], a[1][(i+2) % 3]),
                          a[2][(i+1) % 3]) for i in range(3)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("Refusing to overwrite an existing report")
    cycle = (2, 0, 1)
    x = (("d", "v", "v"), cycle)
    y = (("", "", ""), cycle)
    z = (("h", "q", "h"), PERM_ID)
    xi, yi = wreath_inv(x), wreath_inv(y)
    relators = [power(x, 6), power(y, 3), power(z, 2),
                power(product(z, x), 3), power(product(z, y), 6),
                power(product(xi, y), 2),
                power(product(yi, power(x, -2)), 3),
                power(product(z, power(x, 3)), 2),
                product(xi, z, power(product(yi, z), 2), z, x,
                        power(product(z, y), 2))]
    expected_table = [
        ("1", "1", "1"), ("1", "1", "1"), ("1", "1", "1"),
        ("hdhvqv", "qvhdhv", "hvqvhd"), ("1", "1", "1"),
        ("1", "1", "1"), ("vdvdvd", "dvdvdv", "1"),
        ("hdhd", "qvdvqvdv", "hdhd"), ("vqhdhq", "1", "dhqvqh")]
    observed_table = [tuple(involution_cancel(w) for w in a[0]) for a in relators]
    assert observed_table == expected_table
    assert all(normal(a) == normal(WREATH_ID) for a in relators)

    parameter_word = product(y, power(product(z, y), 2))
    parameter_formula = (("hq", "", "qh"), PERM_ID)
    assert normal(parameter_word) == normal(parameter_formula)
    witnesses = [power(x, 3), z, product(yi, z, y)]
    expected_witnesses = [(("d", "q", "d"), PERM_ID), z,
                          (("q", "h", "h"), PERM_ID)]
    assert all(normal(a) == normal(b) for a, b in zip(witnesses, expected_witnesses))
    flip = (("", "", ""), (2, 1, 0))
    assert normal(power(flip, 2)) == normal(WREATH_ID)
    assert all(normal(product(flip, a, flip, a)) == normal(WREATH_ID)
               for a in (x, y, z))
    marks = [flip, product(flip, x), product(flip, y), product(flip, z)]
    assert all(normal(power(a, 2)) == normal(WREATH_ID) for a in marks)
    for i, j, order in ((0, 1, 6), (0, 2, 3), (0, 3, 2),
                         (1, 2, 2), (1, 3, 3), (2, 3, 6)):
        assert normal(power(product(marks[i], marks[j]), order)) == normal(WREATH_ID)

    d = matrix(((-1, 0, 1), (0, 1, 0), (0, 0, 1)))
    h = matrix(((1, 0, 0), (0, -1, T), (0, 0, 1)))
    q = matrix(((1, 0, 0), (0, 1, 0), (1, T, -1)))
    assert all(mpow(a, 2) == MAT_ID for a in (d, h, q))
    assert mmul(d, h) == mmul(h, d)
    assert mpow(mmul(d, q), 3) == MAT_ID
    hq = mmul(h, q)
    t_squared = pmul(T, T)
    assert hq[0] == (ONE, ZERO, ZERO)
    assert psub(pmul(hq[1][1], hq[2][2]), pmul(hq[1][2], hq[2][1])) == ONE
    assert padd(hq[1][1], hq[2][2]) == psub(t_squared, (2,))
    c = mmul(mmul(d, h), q)
    trace = psum(c[i][i] for i in range(3))
    second = psum(psub(pmul(c[i][i], c[j][j]), pmul(c[i][j], c[j][i]))
                  for i in range(3) for j in range(i+1, 3))
    assert trace == psub(t_squared, (2,))
    assert second == psub((2,), t_squared)
    assert det3(c) == (-1,)
    m = mmod_six(msub(mpow(c, 2), MAT_ID))
    expected_m = matrix(((1, T, -2), (T, 3, (0, -2)), (2, (0, 2), -4)))
    assert m == expected_m
    assert m != MAT_ZERO and m[0][0] == ONE
    assert mmod_six(mmul(m, m)) == MAT_ZERO
    report = {
        "result": "PASS",
        "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
        "coefficient_systems": ["V4 amalgamated over C2 with S3", "Z[t]", "Z[t]/(t^2-3)"],
        "fixed_source_relators_checked": 9,
        "fixed_relator_factor_words": observed_table,
        "tenth_relator_uniform_reduction": "T=(hq,1,qh); T^s=1 follows from (hq)^s=1",
        "permutation_convention": "(p*r)(i)=r(p(i)); product coordinate A_i*B_p(i)",
        "parameter_word": ["hq", "1", "qh"],
        "subgroup_projection_witnesses": [["d", "q", "d"], ["h", "q", "h"], ["q", "h", "h"]],
        "reversing_involution_identities": 4,
        "four_involution_square_checks": 4,
        "coxeter_pair_relation_checks": 6,
        "reflection_matrices": {"D": d, "H": h, "Q": q},
        "DHQ_characteristic_polynomial": "(lambda+1)*(lambda^2+(1-t^2)*lambda+1)",
        "s6_nonzero_square_zero_matrix": m,
        "s6_square_zero_exact": True,
        "scope": "Exact abstract word and polynomial identities. Uniform tenth relation, real eigenvalue argument, and subgroup-surjection infinitude are written proofs. No finite-geometry, triangle faithfulness, or small-parameter finiteness computation."
    }
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print("PASS: 9 abstract relators, uniform tenth-word formula, subgroup witnesses, involutory lift, exact polynomial/reflection identities.")


if __name__ == "__main__":
    main()
