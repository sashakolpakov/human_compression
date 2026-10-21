#!/usr/bin/env python3
"""Exact saturated Schreier lattice for the frozen even-parameter voltage data."""
import argparse
from collections import deque
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

BASIS_EDGES = [(143, 0), (152, 3), (162, 2),
               (172, 1), (223, 2), (244, 0)]
COORDINATES = [0, 1, 2, 4, 5, 6]
EXPECTED_MINOR = [
    [0, 0, 1, -1, 0, 0],
    [0, 0, 0, 0, -1, -1],
    [1, 0, 0, 1, 1, 0],
    [0, 0, -1, 0, -1, 1],
    [0, 0, 0, 0, 1, 0],
    [1, 1, -1, 0, 0, 0],
]


def inverse_and_det(M):
    n = len(M)
    A = [[Fraction(a) for a in row] +
         [Fraction(i == j) for j in range(n)] for i, row in enumerate(M)]
    determinant = Fraction(1)
    for i in range(n):
        k = next(k for k in range(i, n) if A[k][i])
        if k != i:
            A[k], A[i] = A[i], A[k]
            determinant = -determinant
        scale = A[i][i]
        determinant *= scale
        A[i] = [a / scale for a in A[i]]
        for k in range(n):
            if k == i:
                continue
            factor = A[k][i]
            if factor:
                A[k] = [a - factor*b for a, b in zip(A[k], A[i])]
    assert all(A[i][j] == (i == j) for i in range(n) for j in range(n))
    return [row[n:] for row in A], determinant


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--data', type=Path, default=Path(__file__).with_name(
        'phase33_L003_even_voltage.json'))
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise SystemExit('Refusing to overwrite saved evidence')
    raw = args.data.read_bytes()
    data = json.loads(raw)
    n = data['degree']
    assert n == 648
    pp = [tuple(a-1 for a in row) for row in data['permutations']]
    vv = [tuple(row) for row in data['weights']]
    assert len(pp) == len(vv) == 3
    assert all(sorted(p) == list(range(n)) for p in pp)
    assert all(len(v) == n and all(type(a) is int for a in v) for v in vv)
    N = 2*n
    identity = (tuple(range(N)), (0,)*N)
    marks = [(tuple(range(n, N)) + tuple(range(n)), (0,)*N)]
    for p, v in zip(pp, vv):
        inv = [0]*n
        for i, j in enumerate(p):
            inv[j] = i
        marks.append((tuple(n+i for i in inv) + p,
                      tuple(-v[i] for i in inv) + v))

    def multiply(a, b):
        p, v = a
        q, w = b
        return (tuple(q[i] for i in p),
                tuple(x+w[i] for x, i in zip(v, p)))

    assert all(multiply(a, a) == identity for a in marks)
    # One fixed right-action representative for every underlying permutation.
    representatives = [identity]
    words = [()]
    index = {identity[0]: 0}
    todo = deque([0])
    edges = []
    while todo:
        a = todo.popleft()
        assert a == len(edges)
        row = []
        for j, mark in enumerate(marks):
            b = multiply(representatives[a], mark)
            if b[0] not in index:
                index[b[0]] = len(representatives)
                representatives.append(b)
                words.append(words[a] + (j,))
                todo.append(index[b[0]])
            row.append(index[b[0]])
        edges.append(row)
        assert len(representatives) <= 1296
    assert len(representatives) == 1296

    def schreier(a, j):
        p, v = representatives[a]
        q, w = marks[j]
        target, voltage = representatives[edges[a][j]]
        assert tuple(q[i] for i in p) == target
        # s(a)*r_j*s(a r_j)^-1 has exactly this pure translation vector.
        return tuple(x+w[i]-y for x, i, y in zip(v, p, voltage))

    basis = [schreier(a, j) for a, j in BASIS_EDGES]
    minor = [[b[i] for b in basis] for i in COORDINATES]
    assert minor == EXPECTED_MINOR
    inverse, determinant = inverse_and_det(minor)
    assert determinant == 1
    assert all(a.denominator == 1 for row in inverse for a in row)
    inverse = [[int(a) for a in row] for row in inverse]

    def coefficients(z):
        return [sum(a*z[i] for a, i in zip(row, COORDINATES))
                for row in inverse]

    coeff_hist = {}
    for a in range(len(representatives)):
        for j in range(4):
            z = schreier(a, j)
            c = coefficients(z)
            assert all(z[i] == sum(t*b[i] for t, b in zip(c, basis))
                       for i in range(N))
            key = str(tuple(c))
            coeff_hist[key] = coeff_hist.get(key, 0) + 1

    # Re-evaluate six literal words, independently of the subtraction formula.
    literal_words = []
    for (a, j), vector in zip(BASIS_EDGES, basis):
        word = words[a] + (j,) + words[edges[a][j]][::-1]
        value = identity
        for letter in word:
            value = multiply(value, marks[letter])
        assert value == (identity[0], vector)
        literal_words.append(list(word))

    # Optional exact normal-action data: columns express r_j^-1*b_i*r_j.
    conjugation = []
    for p, unused in marks:
        cols = []
        for b in basis:
            z = tuple(b[i] for i in p)
            c = coefficients(z)
            assert all(z[i] == sum(t*v[i] for t, v in zip(c, basis))
                       for i in range(N))
            cols.append(c)
        M = [[cols[j][i] for j in range(6)] for i in range(6)]
        assert all(sum(M[i][k]*M[k][j] for k in range(6)) == (i == j)
                   for i in range(6) for j in range(6))
        conjugation.append(M)

    report = {
        'status': 'PASS',
        'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'data_sha256': sha256(raw).hexdigest(),
        'underlying_group_order': len(representatives),
        'integer_coordinates': N,
        'schreier_vectors_checked': len(representatives)*4,
        'vector_coordinate_equalities': len(representatives)*4*N,
        'basis_edges_zero_based': BASIS_EDGES,
        'basis_literal_words_zero_based': literal_words,
        'minor_coordinate_indices_zero_based': COORDINATES,
        'minor': minor,
        'minor_determinant': int(determinant),
        'minor_inverse': inverse,
        'all_schreier_vectors_integral_in_basis': True,
        'distinct_schreier_coefficient_vectors': len(coeff_hist),
        'lattice_rank': 6,
        'lattice_coordinate_projection_is_integral_isomorphism': True,
        'generator_conjugation_matrices_in_basis': conjugation,
        'scope': 'Literal integer-image lattice only. Elementary Schreier telescoping and the unimodular minor prove kernel(reduction mod m)=mL and |G_m|=1296*m^6 for every m>=1. This does not identify the source universal group.'
    }
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print('PHASE34_L003_EVEN_ORDER_PASS', len(representatives)*4,
          'Schreier vectors; rank6; determinant1')


if __name__ == '__main__':
    main()
