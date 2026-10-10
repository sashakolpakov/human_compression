#!/usr/bin/env python3
"""Independent exact finite certificates for uniform four-dimensional arguments.

For a determinant-one diagonal torus of exponent m, exponent vectors a,b
induce equal characters iff m divides all differences (a_i-b_i)-(a_3-b_3).
The listed integer gcds therefore decide collisions for every m at once.
No group enumeration, source-paper tables, or third-party packages are used.
"""
import argparse
import hashlib
import itertools
import json
import math
from collections import Counter
from pathlib import Path


def elementary(i, j):
    return [[int(r == i and c == j) for c in range(4)] for r in range(4)]


def multiply(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(4))
             for j in range(4)] for i in range(4)]


def run():
    exponents = []
    for i in range(4):
        for j in range(i, 4):
            a = [0] * 4
            a[i] += 1
            a[j] += 1
            exponents.append(((i, j), a))
    comparisons = []
    for (ij, a), (kl, b) in itertools.combinations(exponents, 2):
        difference = [x - y for x, y in zip(a, b)]
        coordinates = [difference[i] - difference[3] for i in range(3)]
        divisor = math.gcd(*coordinates)
        assert divisor in (1, 2)
        comparisons.append(dict(first=ij, second=kl,
                                quotient_character_difference=coordinates,
                                collision_modulus_divides=divisor))
    assert len(comparisons) == 45

    # Each entry B[r,i] is one isolated entry of E[j,i] B + B E[i,j],
    # for any j distinct from r and i. Checking on all 16 matrix units
    # proves the integer-coefficient identity for an arbitrary matrix B.
    entry_identities = []
    for r, i in itertools.product(range(4), repeat=2):
        j = next(j for j in range(4) if j not in (r, i))
        for a, b in itertools.product(range(4), repeat=2):
            matrix = elementary(a, b)
            left = multiply(elementary(j, i), matrix)
            right = multiply(matrix, elementary(i, j))
            assert left[r][j] + right[r][j] == matrix[r][i]
        entry_identities.append(dict(row=r, column=i, auxiliary=j,
                                     isolated_entry=[r, j]))

    return dict(
        status='PASS',
        arithmetic='Exact integers; Python standard library only',
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        degree_two_weights=[dict(indices=ij, exponent=a) for ij, a in exponents],
        collision_divisor_counts=dict(sorted(Counter(
            x['collision_modulus_divides'] for x in comparisons).items())),
        comparisons=comparisons,
        universal_consequence='All ten degree-two characters are distinct for every integer m >= 3.',
        form_entry_identities=entry_identities,
        entry_basis_checks=256,
        scope='Checks the finite integer character comparisons and linear matrix-entry identities. Does not check the inherited dimension-four structural theorem, group simplicity, full rank bounds, or publication priority.'
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    arguments = parser.parse_args()
    report = run()
    text = json.dumps(report, indent=2) + '\n'
    if arguments.output:
        arguments.output.write_text(text)
    print(json.dumps({k: report[k] for k in
                      ('status', 'collision_divisor_counts', 'entry_basis_checks')}))
