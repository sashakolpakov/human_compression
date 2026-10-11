#!/usr/bin/env python3
"""Exact integer verification of all finite Weil-bound exceptions in Conjecture 6.1.

No third-party packages, floating point, probabilistic primality tests, or external
factorization tables are used. This checks the numerical reduction; the polynomial
and character-sum arguments are in psl2_square_proof.md. Separate GAP files certify
the primitive finite-field witnesses for the cases where this bound is inconclusive.
"""

from math import gcd, prod


def factor(n):
    out = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d = 3 if d == 2 else d + 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def odd_prime_power(n):
    fs = factor(n)
    if len(fs) != 1:
        return None
    p, g = next(iter(fs.items()))
    return (p, g) if p % 2 and g % 2 else None


def check_bound(q, a, require_nonzero=False):
    fs = factor(q - 1)
    assert prod(p**e for p, e in fs.items()) == q - 1
    w = 2 ** len(fs)
    # In the nested case up to four primitive roots of the quartic are removed.
    # Since 1/theta(q-1) <= W(q-1), the sufficient strengthened inequality is
    # q-1 > 4 W(q-1) (a sqrt(q)+1). Non-nested norms have no roots in F_q.
    left = q - 1 - (4 * w if require_nonzero else 0)
    return left > 0 and left**2 > 16 * a * a * w * w * q, fs, w


def main():
    # W(n) <= [64 / 30030^(1/4)] n^(1/4) < 5 n^(1/4).
    assert prod([2, 3, 5, 7, 11, 13]) == 30030
    assert 64**4 < 5**4 * 30030

    # For every odd b>=23, 3^b > [21(b-2)]^4:
    # establish b=23 and a lower bound for each b -> b+2 ratio.
    assert 3**23 > (21 * 21) ** 4
    assert 9 * 21**4 > 23**4

    nons_nested_failures = []
    tested = []
    for b in range(5, 23, 2):
        cap = (21 * (b - 2)) ** 4
        base = 3
        while base**b <= cap:
            pp = odd_prime_power(base)
            if pp:
                p, g = pp
                for a in range(3, b, 2):
                    if gcd(a, b) != 1:
                        continue
                    passed, fs, w = check_bound(base**b, a)
                    record = (base, p, g, a, b, fs, w)
                    tested.append(record)
                    if not passed:
                        nons_nested_failures.append((base, a, b))
            base += 2
        # Exhibits the end of this finite base range explicitly.
        print(f"relative b={b}: all odd bases >= {base} satisfy the uniform bound")

    expected_nonnested = [
        (3, 3, 5), (5, 3, 5),
        (3, 3, 7), (3, 5, 7),
        (3, 5, 9), (3, 7, 9),
    ]
    assert nons_nested_failures == expected_nonnested
    print("NONNESTED_EXCEPTIONS", nons_nested_failures)
    print("NONNESTED_TESTED", len(tested))
    print("COMPOSITE_BASES_TESTED", sorted({r[0] for r in tested if r[2] > 1}))

    cap = 21**4
    nested_fields = []
    nested_failures = []
    p = 3
    while p**3 <= cap:
        if factor(p) == {p: 1}:
            exponent = 3
            while p**exponent <= cap:
                q = p**exponent
                passed, fs, w = check_bound(q, 1, require_nonzero=True)
                nested_fields.append((p, exponent, fs, w))
                if not passed:
                    # Every allowed first exponent divides the second exponent.
                    for first_exponent in range(3, exponent + 1, 2):
                        if exponent % first_exponent == 0:
                            nested_failures.append((p, first_exponent, exponent))
                exponent += 2
        p += 2
    expected_nested = [
        (3, 3, 3), (3, 5, 5),
        (5, 3, 3), (7, 3, 3), (11, 3, 3),
    ]
    assert nested_failures == expected_nested
    assert len(nested_fields) == 23
    print("NESTED_EXCEPTIONS", nested_failures)
    print("NESTED_FIELDS_TESTED", len(nested_fields))
    print("ALL_EXACT_INTEGER_CHECKS_PASSED")


if __name__ == "__main__":
    main()
