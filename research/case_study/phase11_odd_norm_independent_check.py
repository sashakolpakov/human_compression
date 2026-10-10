#!/usr/bin/env python3
"""Exact F3 diagnostic for the odd-prime norm lemma, with no external packages.

Enumerates every pair of nilpotent 3x3 matrices N,M with N e1=M e2=0,
N^3=M^3=0, and every vector d. Checks precisely the two norm identities.
This is not an encoding of the p-group theorem or the argument for p>=5.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

P = 3
ZERO = (0,) * 9
E1, E2 = (1, 0, 0), (0, 1, 0)


def multiply(a, b):
    return tuple(sum(a[3*i+k] * b[3*k+j] for k in range(3)) % P
                 for i in range(3) for j in range(3))


def apply(a, v):
    return tuple(sum(a[3*i+j] * v[j] for j in range(3)) % P
                 for i in range(3))


def matrices_annihilating(coordinate):
    free = [3*i+j for i in range(3) for j in range(3) if j != coordinate]
    candidates = []
    for values in itertools.product(range(P), repeat=6):
        matrix = [0] * 9
        for index, value in zip(free, values):
            matrix[index] = value
        matrix = tuple(matrix)
        square = multiply(matrix, matrix)
        if multiply(square, matrix) == ZERO:
            candidates.append((matrix, square))
    return candidates


def run():
    ns = matrices_annihilating(0)
    ms = matrices_annihilating(1)
    vectors = list(itertools.product(range(P), repeat=3))
    commuting_pairs = 0
    solutions = 0
    solution_pairs = set()
    rank_two_candidates = 0
    for n, n2 in ns:
        for m, m2 in ms:
            if multiply(n, m) != multiply(m, n):
                continue
            commuting_pairs += 1
            if n2 != ZERO or m2 != ZERO:
                rank_two_candidates += 1
            mx, ny = apply(m, E1), apply(n, E2)
            for d in vectors:
                minus_n2d = tuple(-v % P for v in apply(n2, d))
                if mx != minus_n2d or ny != apply(m2, d):
                    continue
                assert n2 == m2 == ZERO
                assert mx == ny == (0, 0, 0)
                solutions += 1
                solution_pairs.add((n, m))
    assert solutions > 0
    return dict(
        status='PASS', prime=P, matrix_representation='row-major entries',
        parameter_matrices_per_fixed_coordinate=3**6,
        nilpotent_matrices_fixing_each_named_coordinate=[len(ns), len(ms)],
        commuting_pairs=commuting_pairs,
        commuting_pairs_with_a_length_three_Jordan_block=rank_two_candidates,
        tested_vectors_per_commuting_pair=len(vectors),
        norm_identity_solutions=solutions,
        norm_identity_action_pairs=len(solution_pairs),
        solutions_with_nonzero_N_squared_or_M_squared=0,
        conclusion='Every solution has N^2=M^2=0 and M e1=N e2=0.',
        scope=('Complete finite F3 norm-lemma diagnostic only. The all-prime '
               'p-group induction, lifting, and Sylow-product argument are '
               'reviewed written mathematics, not encoded by this script.'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run()
    root = Path(__file__).resolve().parent
    names = ['phase11_nilpotent_frattini.md', Path(__file__).name]
    result['input_sha256'] = {
        name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in names}
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
