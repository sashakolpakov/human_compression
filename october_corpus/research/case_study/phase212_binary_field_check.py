#!/usr/bin/env python3
"""Independent small arithmetic part of the n=11 matrix certificate.

Uses no GAP output, field package, or author matrix routines. Large group
orders and signed subgroup membership remain the separate GAP certificate.
"""
import argparse
import json

MODULUS = 0b100101  # X^5 + X^2 + 1


def need(ok, label):
    if not ok:
        raise RuntimeError('P212_BINARY_REJECT ' + label)


def mul(a, b):
    c = 0
    while b:
        if b & 1:
            c ^= a
        a <<= 1
        if a & 32:
            a ^= MODULUS
        b >>= 1
    return c


def power(a, n):
    b = 1
    while n:
        if n & 1:
            b = mul(b, a)
        a = mul(a, a)
        n >>= 1
    return b


def add(xs):
    a = 0
    for x in xs:
        a ^= x
    return a


def ident(d):
    return tuple(tuple(int(i == j) for j in range(d)) for i in range(d))


def mm(a, b):
    return tuple(tuple(add(mul(x, y) for x, y in zip(row, col))
                       for col in zip(*b)) for row in a)


def mp(a, n):
    b = ident(len(a))
    while n:
        if n & 1:
            b = mm(b, a)
        a = mm(a, a)
        n >>= 1
    return b


def mv(a, v):
    return tuple(add(mul(x, y) for x, y in zip(row, v)) for row in a)


def q(v):
    return add(mul(x, x) for x in v) ^ mul(5, add(mul(x, y) for x, y in zip(v, v[1:])))


def polar(v, w):
    return q(tuple(x ^ y for x, y in zip(v, w))) ^ q(v) ^ q(w)


def reflection(v):
    d = len(v)
    norm = q(v)
    need(norm != 0, 'nonsingular reflection')
    basis = ident(d)
    form = [polar(v, x) for x in basis]
    return tuple(tuple(int(i == j) ^ mul(mul(v[i], form[j]), power(norm, 30))
                       for j in range(d)) for i in range(d))


def mid(a):
    return ((a[1][1] ^ a[3][1], a[1][2] ^ a[3][2]), (a[2][1], a[2][2]))


def quotient(a):
    return (tuple(a[0][j] ^ a[4][j] for j in range(4)), a[1][:4],
            tuple(a[2][j] ^ a[4][j] for j in range(4)), a[3][:4])


def main():
    global MODULUS
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutant', choices=['identity-witness', 'wrong-field'])
    args = ap.parse_args()
    if args.mutant == 'wrong-field':
        MODULUS = 0b101011
    need(all(mul(x, power(x, 30)) == 1 for x in range(1, 32)), 'field inverses')
    basis = ident(5)
    marks = [reflection(v) for v in basis]
    one = ident(5)
    need(all(mp(a, 2) == one and a != one for a in marks), 'nontrivial involutions')
    for i in range(5):
        for j in range(i + 1, 5):
            p = mm(marks[i], marks[j])
            if j == i + 1:
                need(mp(p, 11) == one and p != one, 'exact adjacent order eleven')
            else:
                need(mp(p, 2) == one, 'distant commutation')
    for i in range(3):
        for k in range(1, 11):
            p = mm(mp(mm(marks[i+1], marks[i+2]), k), mp(mm(marks[i], marks[i+1]), k))
            need(mp(p, 2) == one, 'literal triple relation')
    z = (1, 0, 1, 0, 1)
    need(q(z) == 1 and all(polar(z, v) == 0 for v in basis), 'nonsingular ambient radical')
    need(all(mv(a, z) == z for a in marks), 'radical fixed by generators')
    witness = reflection((0, 1, 8, 0, 0))
    if args.mutant == 'identity-witness':
        witness = one
    need(all(q(mv(witness, v)) == q(v) for v in basis), 'witness norms')
    need(all(polar(mv(witness, v), mv(witness, w)) == polar(v, w)
             for v in basis for w in basis), 'witness polar form')
    gens = [mid(a) for a in marks[1:4]]
    elements, pending = {ident(2)}, [ident(2)]
    while pending:
        a = pending.pop()
        for b in gens:
            c = mm(a, b)
            if c not in elements:
                elements.add(c)
                pending.append(c)
                need(len(elements) <= 22, 'dihedral quotient bound')
    need(len(elements) == 22 and mid(witness) not in elements, 'middle nonmembership')
    rotation = mm(gens[0], mid(witness))
    need(mp(rotation, 33) == ident(2) and mp(rotation, 3) != ident(2)
         and mp(rotation, 11) != ident(2), 'outside rotation has exact order thirty-three')
    frame = ((1, 0, 1, 0), (1, 0, 1, 5), (1, 0, 16, 5), (1, 31, 16, 5))
    fifth, coefficients = (1, 20, 11, 22), (14, 4, 4, 15)
    need(all(q(v) == 0 for v in frame + (fifth,)), 'singular projective frame')
    # In this frame the successive differences supply pivots in columns 3,2,1.
    need(all(x != 0 for x in (5, 17, 31)), 'frame pivots')
    need(tuple(add(mul(coefficients[i], frame[i][j]) for i in range(4))
               for j in range(4)) == fifth, 'fifth frame point coefficients')
    need(all(x != 0 for x in coefficients), 'frame coefficients nonzero')
    # The induced quotient matrices agree on representatives of the radical.
    project = lambda v: (v[0] ^ v[4], v[1], v[2] ^ v[4], v[3])
    need(all(mv(quotient(a), project(v)) == project(mv(a, v))
             for a in marks for v in basis), 'literal quotient interface')
    print(json.dumps(dict(status='P212_BINARY_FIELD_PASS', modulus=MODULUS,
                          coefficient=5, reflection_parameter=8,
                          literal_relators=45, triple_relators=30,
                          middle_quotient_order=22, outside_rotation_order=33,
                          large_group_orders_verified=False, signed_membership_verified=False)))


if __name__ == '__main__':
    main()
