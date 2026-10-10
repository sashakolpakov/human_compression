"""Exact affine rank-three seed, using only the Python standard library.

This verifies a single constructive seed, not any classification.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

IDENTITY = (0, 0, 1, 0, 0, 1)


def mul(x, y):
    a, b, c, d, e, f = x
    u, v, w, z, s, t = y
    return ((a + c*u + d*v) % 4, (b + e*u + f*v) % 4,
            (c*w + d*s) % 4, (c*z + d*t) % 4,
            (e*w + f*s) % 4, (e*z + f*t) % 4)


def inv(x):
    a, b, c, d, e, f = x
    # Every matrix used is a signed permutation, hence inverse=transpose.
    return ((-c*a-e*b) % 4, (-d*a-f*b) % 4, c, e, d, f)


def comm(x, y):
    return mul(mul(inv(x), inv(y)), mul(x, y))


def closure(gens):
    known = {IDENTITY}
    todo = [IDENTITY]
    while todo:
        x = todo.pop()
        for y in gens:
            z = mul(x, y)
            if z not in known:
                known.add(z)
                todo.append(z)
    return known


def commute_subgroups(a, b):
    return closure(list({comm(x, y) for x in a for y in b}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    r = [(0, 0, 1, 0, 0, 3), (0, 0, 0, 1, 1, 0),
         (1, 0, 3, 0, 0, 1)]
    assert all(mul(x, x) == IDENTITY for x in r)
    assert comm(r[0], r[2]) == IDENTITY
    group = closure(r)
    assert len(group) == 128
    assert all(mul(x, inv(x)) == IDENTITY for x in group)
    c = [comm(r[0], r[1]), comm(r[1], r[2])]
    assert all(mul(x, x) == IDENTITY for x in c)
    u = comm(c[0], r[2])
    z = comm(u, r[1])
    assert u == (2, 0, 1, 0, 0, 1)
    assert z == (2, 2, 1, 0, 0, 1)
    assert comm(u, r[0]) == comm(u, r[2]) == IDENTITY
    derived = commute_subgroups(group, group)
    third = commute_subgroups(derived, group)
    fourth = commute_subgroups(third, group)
    fifth = commute_subgroups(fourth, group)
    assert third == closure([u, z]) and len(third) == 4
    assert fourth == closure([z]) and len(fourth) == 2
    assert fifth == {IDENTITY}
    pars = [closure([r[i] for i in range(3) if mask >> i & 1])
            for mask in range(8)]
    for mask, par in enumerate(pars):
        assert par & third == (third if mask == 7 else {IDENTITY})
        vertices = mask.bit_count()
        edges = sum((mask >> i & 3) == 3 for i in range(2))
        assert len(par) == 2 ** (vertices + edges) * (4 if mask == 7 else 1)
    for s, t in itertools.product(range(8), repeat=2):
        assert pars[s] & pars[t] == pars[s & t]
    report = {
        'status': 'PASS',
        'scope': 'One exact constructive affine seed; no classification input',
        'model': '(Z/4)^2 semidirect signed coordinate permutations D8',
        'group_order': len(group),
        'generators_affine_vectors_and_row_matrices': r,
        'lower_central_orders': [len(group), len(derived), len(third),
                                len(fourth), len(fifth)],
        'parabolic_kernel_and_order_checks': 8,
        'actual_parabolic_intersections': 64,
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    text = json.dumps(report, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
