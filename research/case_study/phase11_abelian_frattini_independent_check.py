#!/usr/bin/env python3
"""Independent finite diagnostics for the abelian-Frattini proof.

Uses row masks, without importing the author's column-coordinate checker.
This checks the entire finite binary lemma and bounded coefficient lifting;
it does not formalize the group-theoretic induction or prove the uniform lift.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path


def act(rows, vector):
    return sum(((row & vector).bit_count() % 2) << i
               for i, row in enumerate(rows))


def compose(rows, other):
    return tuple(sum(((act(rows, act(other, 1 << j)) >> i) & 1) << j
                     for j in range(3)) for i in range(3))


def run():
    identity = (1, 2, 4)
    matrices = list(itertools.product(range(8), repeat=3))
    involutions = [m for m in matrices if compose(m, m) == identity]
    solutions = []
    weak_failures = []
    for s in involutions:
        if act(s, 1) != 1:
            continue
        for t in involutions:
            if act(t, 2) != 2 or compose(s, t) != compose(t, s):
                continue
            st = compose(s, t)
            if act(st, 4) == 4 and not any(
                    act(s, e) == act(t, e) == e for e in (1, 2, 4)):
                weak_failures.append([list(s), list(t)])
            for d, f in itertools.product(range(8), repeat=2):
                if act(t, 1) != (1 ^ d ^ act(s, d)):
                    continue
                if act(s, 2) != (2 ^ d ^ act(t, d)):
                    continue
                if 4 != (1 ^ 2 ^ act(t, d) ^ f ^ act(st, f)):
                    continue
                image_s = {act(s, v) ^ v for v in range(8)}
                image_t = {act(t, v) ^ v for v in range(8)}
                if s == t == identity:
                    coordinate = None
                else:
                    assert image_s == image_t
                    assert len(image_s) == 2
                    coordinate, = image_s - {0}
                    assert coordinate in (1, 2, 4)
                    assert act(s, coordinate) == act(t, coordinate) == coordinate
                solutions.append(dict(S_rows=s, T_rows=t, d=d, f=f,
                                      common_image_coordinate=coordinate))
    pairs = sorted({(s['S_rows'], s['T_rows']) for s in solutions})
    assert len(solutions) == 32 and len(pairs) == 4
    assert len(weak_failures) == 1

    # Enumerate all image coefficient vectors with the parity relevant to
    # the chosen maximal-order factor. No automorphism assumption is needed
    # for this stronger, elementary coefficient test.
    coefficient_vectors = 0
    lifting_cases = 0
    for exponents in itertools.product(range(1, 5), repeat=3):
        orders = tuple(2**r for r in exponents)
        maximum = max(exponents)
        scale = 2**(maximum - 1)
        for line in (None, 0, 1, 2):
            selected = (line if line is not None and exponents[line] == maximum
                        else exponents.index(maximum))
            allowed = {1 << selected}
            if line is not None and line != selected:
                allowed.add((1 << selected) ^ (1 << line))
            target = tuple(scale if i == selected else 0 for i in range(3))
            lifting_cases += 1
            for coefficients in itertools.product(*(range(o) for o in orders)):
                parity = sum((value % 2) << i for i, value in enumerate(coefficients))
                if parity not in allowed:
                    continue
                image = tuple(scale * value % order
                              for value, order in zip(coefficients, orders))
                assert image == target
                coefficient_vectors += 1

    return dict(
        status='PASS', matrix_representation='three row masks over F2',
        all_binary_matrices=len(matrices), involutory_matrices=len(involutions),
        binary_hypothesis_solutions=len(solutions), action_pairs=pairs,
        solutions=solutions, weaker_hypotheses_counterexample_rows=weak_failures,
        lifting_exponents=[1, 2, 3, 4], lifting_cases=lifting_cases,
        lifting_coefficient_vectors=coefficient_vectors,
        scope=('Complete finite binary-lemma verification and bounded coefficient '
               'lifting diagnostics; the all-parameter lifting and finite-group '
               'induction are reviewed mathematical proofs, not encoded here.'))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run()
    root = Path(__file__).resolve().parent
    names = ['phase11_abelian_frattini.md', Path(__file__).name]
    result['input_sha256'] = {
        name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in names}
    output = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(output)
    print(output, end='')


if __name__ == '__main__':
    main()
