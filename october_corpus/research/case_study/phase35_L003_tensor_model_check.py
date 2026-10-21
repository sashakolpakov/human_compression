#!/usr/bin/env python3
"""Eight-dimensional integral tensor model of the first-nine L003 relations."""
import argparse
from collections import deque
from hashlib import sha256
import json
from pathlib import Path

DIM = 8
I2 = ((1, 0), (0, 1))
D = ((0, 1), (1, 0))
R = ((1, -1), (0, -1))
S = ((0, 1), (-1, 0))
Q = ((1, 0), (1, -1))
N = ((0, 1), (1, 1))
N_INV = ((-1, 1), (1, 0))
IDENTITY = tuple(tuple(int(i == j) for j in range(DIM)) for i in range(DIM))


def mul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(DIM))
                       for j in range(DIM)) for i in range(DIM))


def power(a, n):
    assert n >= 0
    out = IDENTITY
    while n:
        if n & 1:
            out = mul(out, a)
        a = mul(a, a); n //= 2
    return out


def prod(*items):
    out = IDENTITY
    for a in items:
        out = mul(out, a)
    return out


def tensor(factors, permutation=(0, 1, 2), scalar=1):
    """Row convention: input factor i maps to output factor permutation[i]."""
    out = [[0] * DIM for _ in range(DIM)]
    for a in range(DIM):
        aa = [(a >> (2-i)) & 1 for i in range(3)]
        for b in range(DIM):
            bb = [(b >> (2-i)) & 1 for i in range(3)]
            c = scalar
            for i in range(3):
                c *= factors[i][aa[i]][bb[permutation[i]]]
            out[a][b] = c
    return tuple(map(tuple, out))


def closure(gens, bound):
    seen, queue = {IDENTITY}, deque([IDENTITY])
    while queue:
        g = queue.popleft()
        for h in gens:
            k = mul(g, h)
            if k not in seen:
                seen.add(k); queue.append(k)
                assert len(seen) <= bound
    return seen


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise SystemExit('Refusing to overwrite an existing report')
    cycle = (2, 0, 1)
    x = tensor((D, R, R), cycle, -1)
    y = tensor((I2, I2, I2), cycle)
    z = tensor((S, Q, S))
    x_inv, y_inv = power(x, 5), power(y, 2)
    relators = [power(x, 6), power(y, 3), power(z, 2), power(mul(z, x), 3),
                power(mul(z, y), 6), power(mul(x_inv, y), 2),
                power(mul(y_inv, power(x, 4)), 3), power(mul(z, power(x, 3)), 2),
                prod(x_inv, z, power(mul(y_inv, z), 2), z, x, power(mul(z, y), 2))]
    assert all(g == IDENTITY for g in relators)
    flip = tensor((I2, I2, I2), (2, 1, 0))
    assert power(flip, 2) == IDENTITY
    assert prod(flip, x, flip) == x_inv
    assert prod(flip, y, flip) == y_inv
    assert prod(flip, z, flip) == z
    marks = [flip, mul(flip, x), mul(flip, y), mul(flip, z)]
    assert all(power(g, 2) == IDENTITY and g != IDENTITY for g in marks)
    torus = mul(y, power(mul(z, y), 2))
    assert torus == tensor((N_INV, I2, N))
    torus_conjugate = prod(y_inv, torus, y)
    assert torus_conjugate == tensor((I2, N, N_INV))
    assert mul(torus, torus_conjugate) == mul(torus_conjugate, torus)
    fixed = {}
    for omitted, expected in [(0, 36), (2, 48), (3, 108)]:
        group = closure([g for i, g in enumerate(marks) if i != omitted], expected)
        assert len(group) == expected
        fixed[str(omitted)] = {
            'order': len(group),
            'maximum_absolute_entry': max(abs(c) for g in group for row in g for c in row),
            'reduction_orders': {str(n): len({tuple(tuple(c % n for c in row) for row in g)
                                            for g in group}) for n in (2, 3)}
        }
        assert fixed[str(omitted)]['reduction_orders']['3'] == expected
    assert fixed['2']['reduction_orders']['2'] == 12
    # Exact sample diagnostics for the uniform Fibonacci argument in the note.
    fib = [0, 1]
    for _ in range(2, 26):
        fib.append(sum(fib[-2:]))
    fibonacci_samples = []
    for s in range(3, 26):
        modulus = fib[s]
        eye = tuple(tuple(c % modulus for c in row) for row in IDENTITY)
        a = eye
        for k in range(1, s + 1):
            a = tuple(tuple(c % modulus for c in row) for row in mul(a, torus))
            assert (a == eye) == (k == s)
        fibonacci_samples.append({'s': s, 'modulus': modulus, 'exact_order': s})
    report = {
        'result': 'PASS', 'dimension': DIM, 'coefficient_ring': 'Z',
        'integer_relators_checked': 9, 'relator_entries_checked': 9 * DIM * DIM,
        'four_nontrivial_involutions': True, 'reversal_identities': 3,
        'fixed_integer_parabolics': fixed,
        'torus_identity': 'T = N^{-1} tensor I2 tensor N; N=[[0,1],[1,1]]',
        'conjugate_translation': 'y^{-1} T y = I2 tensor N tensor N^{-1}',
        'fibonacci_samples': fibonacci_samples,
        'marking_matrices': marks,
        'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope': 'Integer identities and finite fixed parabolics; uniform exact parameter follows written Fibonacci proof. No IP/Helly, faithful ambient identification, or all-parameter hypertope claim.'
    }
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print('PASS: 9 integer relations, 4 involutions, torus formula, fixed parabolics36/48/108, 23 Fibonacci reductions.')


if __name__ == '__main__':
    main()
