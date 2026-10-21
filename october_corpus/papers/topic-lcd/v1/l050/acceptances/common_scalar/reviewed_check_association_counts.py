#!/usr/bin/env python3
"""Exact scalar criteria and independent finite models for subset/Hamming graphs."""
import argparse
import itertools
import json
from math import comb, factorial, gcd
from pathlib import Path

import sympy as sp


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def subset_counts(n, k, r):
    return {j: sum(choose(k-j, r-a)**2 * choose(j, a) *
                   choose(n-2*k+j, k-2*r+a) for a in range(j+1))
            for j in range(max(0, 2*k-n), k+1)}


def hamming_counts(d, q, k):
    result = {}
    for j in range(d+1):
        total = 0
        for a in range(d-j+1):
            b, e = j+a-k, 2*k-j-2*a
            if b < 0 or e < 0:
                continue
            total += (choose(d-j, a)*(q-1)**a * factorial(j) //
                      (factorial(b)**2*factorial(e))) * (q-2)**e
        result[j] = total
    return result


def conditions(counts, diagonal, adjacent, vertices, prime):
    degree = counts[diagonal]
    products = [v + int(j == adjacent) for j, v in counts.items()]
    reflexive = all(v % prime == 0 for v in products)
    orthogonal = all((degree-v) % prime == 0 for v in products)
    complementary = orthogonal and not (degree % prime == 0 and (vertices-1) % prime == 0)
    return dict(RLCD=reflexive, complement_orthogonal=orthogonal, CLCD=complementary)


def finite_model(vertices, relation, counts, adjacency_relation):
    adjacency = [sum(1 << j for j, y in enumerate(vertices)
                     if i != j and relation(x, y) == adjacency_relation)
                 for i, x in enumerate(vertices)]
    pairs = 0
    for i, x in enumerate(vertices):
        for j in range(i+1):
            if (adjacency[i] & adjacency[j]).bit_count() != counts[relation(x, vertices[j])]:
                raise ValueError('Common-neighbour formula')
            pairs += 1
    return pairs


def families():
    n = sp.symbols('n')
    def binomial_polynomial(x, k):
        return sp.prod(x-i for i in range(k))/sp.factorial(k) if k >= 0 else sp.Integer(0)
    result = []
    for k, r in [(2, 0), (2, 1), (3, 0), (3, 1), (3, 2), (4, 0), (4, 1)]:
        intersections = [sp.expand(sum(choose(k-j, r-a)**2*choose(j, a)*
                            binomial_polynomial(n-2*k+j, k-2*r+a)
                            for a in range(j+1))) for j in range(k+1)]
        reflexive = [sp.expand(x+int(j == r)) for j, x in enumerate(intersections)]
        complement = [sp.expand(intersections[-1]-x) for x in reflexive]
        for mode, polynomials in [('RLCD', reflexive), ('complement_orthogonal', complement)]:
            coefficients, g = [sp.Integer(1)], polynomials[0]
            for f in polynomials[1:]:
                u, v, g = sp.gcdex(g, f, n)
                coefficients = [sp.expand(c*u) for c in coefficients] + [v]
            if sp.expand(sum(a*b for a, b in zip(coefficients, polynomials))-g) != 0:
                raise ValueError('Bezout identity')
            quotients = []
            for f in polynomials:
                q, rem = sp.div(f, g, n)
                if rem != 0:
                    raise ValueError('Common divisor identity')
                quotients.append(sp.expand(q))
            coefficient_denominator = int(sp.ilcm(*[sp.denom(a) for c in coefficients
                                                    for a in sp.Poly(c, n).all_coeffs()]))
            polynomial_denominator = int(sp.ilcm(*[sp.denom(a) for c in polynomials
                                                   for a in sp.Poly(c, n).all_coeffs()]))
            exceptional = sorted(set(map(int, sp.factorint(coefficient_denominator*polynomial_denominator))))
            cases = []
            for p in exceptional:
                period = p
                while period <= k:
                    period *= p
                allowed, full_dual = [], []
                for residue in range(period):
                    representative = residue + period*((2*k+1)//period+1)
                    flags = conditions(subset_counts(representative, k, r), k, r,
                                       choose(representative, k), p)
                    if flags[mode]:
                        allowed.append(residue)
                    if mode == 'complement_orthogonal' and flags['CLCD']:
                        full_dual.append(residue)
                cases.append(dict(prime=p, period=period, residues=allowed,
                                  CLCD_residues=full_dual if mode == 'complement_orthogonal' else None))
            result.append(dict(k=k, r=r, mode=mode, polynomials=list(map(str, polynomials)),
                               rational_gcd=str(g), bezout_coefficients=list(map(str, coefficients)),
                               common_divisor_quotients=list(map(str, quotients)),
                               coefficient_denominator=coefficient_denominator,
                               polynomial_denominator=polynomial_denominator,
                               exceptional_primes=exceptional, finite_cases=cases,
                               all_other_primes='none' if g == 1 else 'n = 5 modulo p'))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise ValueError('Use a fresh output file')
    checks = []
    for n, k in [(5, 2), (6, 3), (7, 3), (7, 4), (8, 4), (9, 4)]:
        vertices = [sum(1 << x for x in s) for s in itertools.combinations(range(n), k)]
        for r in range(k):
            counts = subset_counts(n, k, r)
            pairs = finite_model(vertices, lambda a, b: (a & b).bit_count(), counts, r)
            checks.append(dict(family='subset', n=n, k=k, r=r, checked_pairs=pairs))
    for d, q in [(3, 2), (4, 2), (3, 3), (4, 3), (3, 4)]:
        vertices = list(itertools.product(range(q), repeat=d))
        for k in range(1, d+1):
            counts = hamming_counts(d, q, k)
            pairs = finite_model(vertices, lambda a, b: sum(x != y for x, y in zip(a, b)), counts, k)
            checks.append(dict(family='Hamming', d=d, q=q, k=k, checked_pairs=pairs))
    examples = []
    for d, q, k, p in [(6, 2, 1, 2), (8, 2, 1, 2), (10, 2, 1, 2),
                        (6, 2, 2, 3), (9, 2, 2, 3), (6, 3, 1, 2), (6, 3, 2, 2)]:
        flags = conditions(hamming_counts(d, q, k), 0, k, q**d, p)
        examples.append(dict(d=d, q=q, k=k, prime=p, **flags))
    report = dict(status='PASS_EXACT_COUNTS_AND_CONGRUENCE_CERTIFICATES',
                  finite_models=checks, finite_pair_checks=sum(x['checked_pairs'] for x in checks),
                  subset_family_certificates=families(), source_Hamming_examples=examples,
                  scope='Scalar product criteria and explicit finite validation. No code-distance or full-source claim.')
    args.out.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], finite_models=len(checks),
                         finite_pair_checks=report['finite_pair_checks'],
                         subset_family_certificates=len(report['subset_family_certificates']),
                         source_Hamming_examples=examples), indent=2))


if __name__ == '__main__':
    main()
