#!/usr/bin/env python3
"""Bounded exact checks for the classified cyclic-core equality obstruction.

No external algebra package or subgroup catalogue is used. The retained
classification is mathematical input, not certified by this script.
Usage: python3 phase10_cyclic_tpp_check.py --output report.json
"""
import argparse
import hashlib
import json
from pathlib import Path


def power(mul, x, exponent, one):
    ans = one
    while exponent:
        if exponent & 1:
            ans = mul(ans, x)
        x = mul(x, x)
        exponent >>= 1
    return ans


def semidirect(mul, swap):
    def extended(x, y):
        u, v = x[:2], y[:2]
        if x[2]:
            v = swap(v)
        w = mul(u, v)
        return w[0], w[1], x[2] ^ y[2]
    return extended


def nonmetacyclic(n, k, ell):
    def mul(x, y):
        i, j = x
        u, v = y
        z = 0
        if not (j & 1) and not (u & 1):
            r, s = u, j
        elif not (j & 1):
            r, s, z = u, -j, ell * (j // 2)
        elif not (u & 1):
            r, s, z = -u, j, ell * (u // 2)
        else:
            r, s, z = -u, -j, k + ell * ((u + j) // 2)
        return (i + r + (n // 2) * z) % n, (s + v + (n // 2) * z) % n
    def swap(x):
        return mul((0, x[0]), (x[1], 0))
    return mul, swap


def metacyclic(n, ratio):
    sums = [0]
    for i in range(n):
        sums.append((sums[-1] + pow(ratio, i, n)) % n)
    def mul(x, y):
        i, j = x
        u, v = y
        return (i + u) % n, (j * pow(ratio, u, n) + v) % n
    def swap(x):
        i, j = x
        return i, (sums[i] - j) % n
    return mul, swap, sums


def check_model(n, mul, swap):
    """Check associativity on all generator extensions and the swap locally.

    For n<=8 also check every base-group associativity triple. Larger
    checks are generator-local diagnostics, not independent proof of a
    presentation or of the group order.
    """
    points = [(i, j) for i in range(n) for j in range(n)]
    gens = [(1, 0), (0, 1)]
    one = (0, 0)
    associative_checks = 0
    swap_checks = 0
    for x in points:
        assert mul(one, x) == x == mul(x, one)
        assert swap(swap(x)) == x
        for y in gens:
            assert swap(mul(x, y)) == mul(swap(x), swap(y))
            assert swap(mul(y, x)) == mul(swap(y), swap(x))
            swap_checks += 2
        for y in (points if n <= 8 else gens):
            for z in (points if n <= 8 else gens):
                assert mul(mul(x, y), z) == mul(x, mul(y, z))
                associative_checks += 1
    return associative_checks, swap_checks


def run(max_e):
    counts = dict(nonmetacyclic_models=0, metacyclic_models=0,
                  base_associativity_checks=0, swap_homomorphism_checks=0,
                  nonmetacyclic_forbidden_class_elements=0,
                  metacyclic_forbidden_class_elements=0,
                  full_group_centrality_checks=0)
    records = []
    for e in range(2, max_e + 1):
        n = 2 ** e
        for k, ell in ([(0, 0)] if e == 2 else [(0, 0), (0, 1), (1, 0), (1, 1)]):
            mul, swap = nonmetacyclic(n, k, ell)
            ca, cs = check_model(n, mul, swap)
            counts['base_associativity_checks'] += ca
            counts['swap_homomorphism_checks'] += cs
            ext = semidirect(mul, swap)
            one = (0, 0, 0)
            z = (n // 2, n // 2, 0)
            for gen in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
                assert ext(z, gen) == ext(gen, z)
                counts['full_group_centrality_checks'] += 1
            checked = 0
            for i in range(n):
                for j in range(n):
                    if (i + j) % 2:
                        continue
                    x = (i, j, 1)
                    s = i + j
                    square = ext(x, x)
                    if i % 2 == 0:
                        expected = (s % n, s % n, 0)
                    else:
                        shift = (n // 2) * ell * (s // 2)
                        expected = ((s + shift) % n, (-s + shift) % n, 0)
                    assert square == expected
                    if square != one:
                        y = square
                        for _ in range(e + 1):
                            next_y = ext(y, y)
                            if next_y == one:
                                assert y == z
                                break
                            y = next_y
                        else:
                            raise AssertionError('Power bound exceeded')
                    checked += 1
            counts['nonmetacyclic_models'] += 1
            counts['nonmetacyclic_forbidden_class_elements'] += checked
            records.append(dict(branch='nonmetacyclic', e=e, k=k, ell=ell,
                                ambient_order=2*n*n, checked_class_elements=checked))
        # Every ratio 1 mod4 includes every odd power of every source ratio.
        for ratio in range(1, n, 4):
            mul, swap, sums = metacyclic(n, ratio)
            ca, cs = check_model(n, mul, swap)
            counts['base_associativity_checks'] += ca
            counts['swap_homomorphism_checks'] += cs
            ext = semidirect(mul, swap)
            one = (0, 0, 0)
            z = (0, n // 2, 0)
            for gen in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
                assert ext(z, gen) == ext(gen, z)
                counts['full_group_centrality_checks'] += 1
            checked = 0
            for i in range(1, n, 2):
                for j in range(n):
                    x = (i, j, 1)
                    kk = (j * (pow(ratio, i, n) - 1) + sums[i]) % n
                    assert kk % 2 == 1
                    assert ext(x, x) == ((2*i) % n, kk, 0)
                    assert power(ext, x, n, one) == z
                    assert power(ext, x, 2*n, one) == one
                    checked += 1
            counts['metacyclic_models'] += 1
            counts['metacyclic_forbidden_class_elements'] += checked
            records.append(dict(branch='metacyclic', e=e, ratio=ratio,
                                ambient_order=2*n*n, checked_class_elements=checked))
    return dict(status='PASS', parameter_range=dict(e_min=2, e_max=max_e),
                counts=counts, models=records,
                scope='Exact bounded normal-form diagnostics; classification and all-parameter proof retained separately.')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--max-e', type=int, default=6)
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    if not 2 <= args.max_e <= 10:
        p.error('--max-e must be between 2 and 10')
    report = run(args.max_e)
    root = Path(__file__).resolve().parent
    report['input_sha256'] = {
        name: hashlib.sha256((root/name).read_bytes()).hexdigest()
        for name in ['phase10_cyclic_tpp.md', Path(__file__).name]
    }
    result = json.dumps(report, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(result)
    print(result, end='')


if __name__ == '__main__':
    main()
