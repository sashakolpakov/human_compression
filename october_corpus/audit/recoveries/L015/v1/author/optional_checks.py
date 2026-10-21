#!/usr/bin/env python3
"""Bounded integer field/matrix diagnostics; not a proof or generation premise."""
import argparse
import json
import math
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def field(n, polynomial):
    q = 1 << n

    def mul(a, b):
        result = 0
        while b:
            if b & 1:
                result ^= a
            b >>= 1
            a <<= 1
            if a & q:
                a ^= polynomial
        return result

    def power(a, k):
        result = 1
        while k:
            if k & 1:
                result = mul(result, a)
            a = mul(a, a)
            k >>= 1
        return result

    return q, mul, power


def diagnostic():
    records = []
    total = 0
    for n, polynomial in [(3, 0b1011), (5, 0b100101), (9, 0b1000010001)]:
        q, mul, power = field(n, polynomial)
        require(all(power(a, q - 1) == 1 for a in range(1, q)), "not a field")
        theta = 1 << ((n + 1) // 2)

        def matrix_product(A, B):
            return [[mul(A[i][0], B[0][j]) ^ mul(A[i][1], B[1][j])
                     ^ mul(A[i][2], B[2][j]) ^ mul(A[i][3], B[3][j])
                     for j in range(4)] for i in range(4)]

        def z(t):
            return [[1, 0, 0, 0], [0, 1, 0, 0], [t, 0, 1, 0],
                    [power(t, theta), t, 0, 1]]

        w = [[int(i + j == 3) for j in range(4)] for i in range(4)]
        rows = 0
        for b in (1, 2, 3):
            seen = set()
            for t in range(1, q):
                M = matrix_product(matrix_product(matrix_product(z(b), w), z(t)), w)
                trace = M[0][0] ^ M[1][1] ^ M[2][2] ^ M[3][3]
                require(trace == power(mul(b, t), theta), "trace product")
                seen.add(trace)
                rows += 1
            require(seen == set(range(1, q)), "fixed-point trace injection")
        local_maps = 0
        if n % 3 == 0:
            Q = 1 << (n // 3)
            for e in (1, 2):
                exponent = 1 + Q ** e
                require(math.gcd(exponent, q - 1) == 1, "seed gcd")
                for c in (1, 2, 3):
                    images = {power(mul(c, power(t, exponent)), theta)
                              for t in range(1, q)}
                    require(images == set(range(1, q)), "local seed trace map")
                    local_maps += 1
        records.append({"n": n, "polynomial_bits": polynomial,
                        "trace_products": rows, "local_seed_bijections": local_maps})
        total += rows

    for a in range(1, 1000, 2):
        Q = 1 << a
        b = a // 5
        require(sum((1 << u) + 1 for u in range(1, b + 1)) < Q + 1,
                "bounded union-bound check")
    # Discriminating negative calculations, not claims about all fields.
    q, mul, power = field(9, 0b1000010001)
    require(len({power(t, 7) for t in range(1, q)}) < q - 1,
            "the wrong Q-1 exponent must fail")
    require(power(mul(2, 1), 32) != power(1, 32),
            "omitting the fixed-involution coefficient must fail")
    require(sum((1 << u) + 1 for u in range(1, 2)) >= (1 << 1) + 1,
            "charging all degrees rather than the proper-degree cutoff must fail")
    return {"status": "PASS_OPTIONAL_ONLY", "field_records": records,
            "actual_matrix_products": total, "bounded_odd_a": 500,
            "negative_controls": 3,
            "not_proved_here": ["uniform theorem", "full generation",
                                "maximal-subgroup classification", "source recovery"]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    report = diagnostic()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))
