#!/usr/bin/env python3
"""Exact arithmetic and small-field orbit checks for marked Suzuki triples.

This does not prove the retained Suzuki-group structure or extrapolate group
generation from samples. The all-parameter equivalences are in the written note.
Only Python's standard library is required. Outputs never contain source text.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def mobius(n):
    result = 1
    p = 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            result = -result
            if n % p == 0:
                return 0
            while n % p == 0:
                n //= p
        p += 1
    return -result if n > 1 else result


def lam(n):
    return Fraction(sum(mobius(n // d) * (1 << d) for d in divisors(n)), n)


def psi(n, total):
    return sum((Fraction(sum(mobius(m // d) * ((1 << (n*d)) - 1)
                             for d in divisors(m)), m)
                for m in divisors(total // n)), Fraction(0))


def all_orbits(n):
    return sum((lam(d) * psi(d, n) for d in divisors(n) if d > 1), Fraction(0))


def compact(n):
    return Fraction(sum(mobius(n // d) * ((1 << d) - 2) * ((1 << d) - 1)
                        for d in divisors(n)), 2*n)


class BinaryField:
    def __init__(self, degree, modulus):
        self.degree = degree
        self.modulus = modulus
        self.q = 1 << degree
        assert modulus.bit_length() == degree + 1
        # Finite verification that every nonzero residue is a unit suffices
        # here to certify these three small polynomial quotient fields.
        assert all(self.pow(a, self.q-1) == 1 for a in range(1, self.q))
        self.square = [self.mul(a, a) for a in range(self.q)]
        self.inverse = [0] + [self.pow(a, self.q-2) for a in range(1, self.q)]

    def mul(self, a, b):
        result = 0
        while b:
            if b & 1:
                result ^= a
            a <<= 1
            b >>= 1
            if a & self.q:
                a ^= self.modulus
        return result

    def pow(self, a, exponent):
        result = 1
        while exponent:
            if exponent & 1:
                result = self.mul(result, a)
            a = self.mul(a, a)
            exponent >>= 1
        return result

    def frobenius_orbit(self, point):
        result = []
        current = point
        while current not in result:
            result.append(current)
            current = tuple(self.square[a] for a in current)
        assert current == point and self.degree % len(result) == 0
        return result

    def dual(self, point):
        b, c = point
        return (self.inverse[b], self.mul(b, c))


def field_check(n, modulus):
    field = BinaryField(n, modulus)
    seen = set()
    representatives = {}
    degree_counts = Counter()
    for b in range(2, field.q):
        for c in range(1, field.q):
            point = (b, c)
            assert field.dual(field.dual(point)) == point
            squared = (field.square[b], field.square[c])
            assert field.dual(squared) == tuple(field.square[a] for a in field.dual(point))
            if point in seen:
                continue
            orbit = field.frobenius_orbit(point)
            seen.update(orbit)
            key = min(orbit)
            dual_key = min(field.frobenius_orbit(field.dual(point)))
            assert key != dual_key
            representatives[key] = dual_key
            degree_counts[len(orbit)] += 1
    assert len(seen) == (field.q - 2) * (field.q - 1)
    assert len(representatives) == all_orbits(n)
    assert all(representatives[value] == key for key, value in representatives.items())
    for d, count in degree_counts.items():
        assert count == 2 * compact(d)

    pair_seen = set()
    pair_orbits = 0
    for b in range(2, field.q):
        if b in pair_seen:
            continue
        orbit = [a[0] for a in field.frobenius_orbit((b,))]
        pair_seen.update(orbit)
        assert field.inverse[b] not in orbit
        pair_orbits += 1
    assert pair_orbits == sum(lam(d) for d in divisors(n) if d > 1)
    return dict(degree=n, q=field.q, polynomial_bits=modulus,
                marked_pairs=len(seen), frobenius_orbits=len(representatives),
                orbits_by_exact_joint_degree=dict(sorted(degree_counts.items())),
                full_group_duality_classes=degree_counts[n] // 2,
                unordered_commuting_pair_classes=pair_orbits // 2,
                checked_duality_involutivity_and_frobenius_commutation=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    arithmetic = []
    for n in range(3, 100, 2):
        nested = sum((mobius(n // d) * all_orbits(d) for d in divisors(n)), Fraction(0)) / 2
        simple = compact(n)
        assert nested == simple and simple.denominator == 1 and simple > 0
        arithmetic.append(dict(degree=n, compact_count=int(simple), nested_count=int(nested)))
    fields = [field_check(3, 0b1011), field_check(5, 0b100101),
              field_check(9, (1 << 9) | (1 << 4) | 1)]
    report = dict(status='PASS', executed_utc=datetime.now(timezone.utc).isoformat(),
                  source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  arithmetic='Exact integers and rational numbers; no floating-point comparisons',
                  formula_comparisons=arithmetic, finite_field_orbit_checks=fields,
                  scope='Finite formula/orbit diagnostics only. Uniform formula equivalence, Suzuki normalization, generation and subgroup intersection are written proofs with explicit retained group-structure inputs.')
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status='PASS', odd_degrees_compared=len(arithmetic), fields=fields), indent=2))


if __name__ == '__main__':
    main()
