"""Literal finite controls for the root-group quotients; no ambient census."""
from pathlib import Path
import argparse
import json
import time


def need(ok, message):
    if not ok:
        raise ValueError(message)


class Field:
    def __init__(self, n, polynomial):
        self.n, self.q, self.polynomial = n, 1 << n, polynomial

    def mul(self, a, b):
        out = 0
        while b:
            if b & 1:
                out ^= a
            b >>= 1
            a <<= 1
            if a & self.q:
                a ^= self.polynomial
        return out

    def power(self, a, k):
        out = 1
        while k:
            if k & 1:
                out = self.mul(out, a)
            a = self.mul(a, a)
            k >>= 1
        return out


def orbit_partition(items, operations):
    remaining = set(items)
    orbits = []
    while remaining:
        seed = min(remaining)
        found, queue = {seed}, [seed]
        for x in queue:
            for operation in operations:
                y = operation(x)
                need(y in items, 'operation preserves declared finite universe')
                if y not in found:
                    found.add(y)
                    queue.append(y)
        need(found <= remaining, 'orbits disjoint')
        remaining -= found
        orbits.append(frozenset(found))
    need(set().union(*orbits) == set(items), 'orbit partition complete')
    return orbits


def one(n, polynomial):
    f = Field(n, polynomial)
    q, theta = f.q, 1 << ((n + 1) // 2)
    need(all(f.power(a, q - 1) == 1 for a in range(1, q)), 'literal field units')
    theta_powers = [f.power(a, theta) for a in range(q)]
    def mul(x, y):
        a, b = x
        c, d = y
        return (a ^ c, b ^ d ^ f.mul(a, theta_powers[c]))
    def inv(x):
        a, b = x
        return (a, b ^ f.mul(a, theta_powers[a]))
    def phi(x):
        return (f.mul(x[0], x[0]), f.mul(x[1], x[1]))
    identity = (0, 0)
    P = frozenset((a, b) for a in range(q) for b in range(q))
    Z = frozenset(x for x in P if x[0] == 0)
    z, w = (0, 1), (1, 0)
    J2 = frozenset([identity, z])
    J4 = frozenset([identity, w, z, mul(w, z)])
    need(len(J4) == 4 and mul(w, w) == z, 'standard order-four subgroup')
    need(all(mul(x, inv(x)) == identity == mul(inv(x), x) for x in P), 'inverse identities')
    def conjugate(x, h):
        return mul(mul(inv(x), h), x)
    actual_normalizer = frozenset(x for x in P if frozenset(conjugate(x, h) for h in J4) == J4)
    R = frozenset(x for x in P if x[0] in (0, 1))
    need(actual_normalizer == R, 'literal normalizer of J4 inside acquired involution centralizer')
    need(all(mul(x, y) == mul(y, x) for x in R for y in R), 'R is abelian')
    need(frozenset(x for x in P if phi(x) == x) == J4, 'literal Frobenius fixed subgroup')
    involutions = frozenset(x for x in P if mul(x, x) == identity)
    need(involutions == Z, 'involutions of P, including identity')

    def cosets(universe, subgroup):
        coset_set = frozenset(frozenset(mul(x, j) for j in subgroup) for x in universe)
        need(sum(map(len, coset_set)) == len(universe), 'cosets partition exact universe')
        return coset_set
    def coset_phi(c):
        return frozenset(phi(x) for x in c)
    Q2, Q4, R4 = cosets(P, J2), cosets(P, J4), cosets(R, J4)
    need([len(Q2), len(Q4), len(R4)] == [q*q//2, q*q//4, q//2], 'three quotient sizes')
    fixed = [sum(coset_phi(c) == c for c in Q) for Q in (Q2, Q4, R4)]
    need(fixed == [2, 1, 1], 'three actual quotient fixed-point counts')
    def inverse_coset(c):
        return frozenset(inv(x) for x in c)
    nonidentity = Q2 - {J2}
    inversion = orbit_partition(nonidentity, [inverse_coset])
    need(len(inversion) == q*q//4 + q//2 - 1, 'inversion orbit count')
    need(sum(frozenset(coset_phi(c) for c in o) == o for o in inversion) == 1,
         'Frobenius fixed inversion classes')
    diagonal = orbit_partition(nonidentity, [inverse_coset, coset_phi])

    cyclic_four = frozenset(frozenset([identity, x, mul(x, x), mul(mul(x, x), x)])
                           for x in P if mul(x, x) == z)
    four_groups = frozenset(frozenset([identity, z, x, mul(z, x)]) for x in Z - J2)
    eight_groups = frozenset(J4 | frozenset(mul(x, h) for h in J4) for x in R - J4)
    need(all(len(x) == 4 for x in cyclic_four | four_groups), 'actual order-four subgroups')
    need(all(len(x) == 8 for x in eight_groups), 'actual order-eight subgroups')
    need([len(cyclic_four), len(four_groups), len(eight_groups)] == [q//2, q//2-1, q//2-1],
         'subgroups containing prescribed intersection')
    need(all(mul(x, y) in H for H in cyclic_four | four_groups | eight_groups for x in H for y in H),
         'literal subgroup closure')
    counts = dict(same_split=len(diagonal), other_dihedral=len(orbit_partition(Q4, [coset_phi])),
                  four_group=len(orbit_partition(four_groups, [coset_phi])),
                  cyclic_four=len(orbit_partition(cyclic_four, [coset_phi])),
                  same_nonsplit=len(orbit_partition(R4 - {J4}, [coset_phi])),
                  other_nonsplit=len(orbit_partition(R4, [coset_phi])),
                  eight_group=len(orbit_partition(eight_groups, [coset_phi])))
    expected = dict(same_split=1+(q-2)*(q+4)//(4*n),
                    other_dihedral=1+(q-2)*(q+2)//(4*n), four_group=(q-2)//(2*n),
                    cyclic_four=1+(q-2)//(2*n), same_nonsplit=(q-2)//(2*n),
                    other_nonsplit=1+(q-2)//(2*n), eight_group=(q-2)//(2*n))
    need((q-2) % (2*n) == 0, 'integer prime-exponent formula')
    need(counts == expected, 'literal quotient orbits match all seven count formulas')
    return dict(n=n, q=q, polynomial=polynomial, root_group_order=len(P),
                normalizer_order=len(R), quotient_fixed=fixed, actual_counts=counts)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', required=True, type=Path)
    a = p.parse_args()
    need(not a.out.exists(), 'fresh output')
    start = time.monotonic()
    rows = [one(n, polynomial) for n, polynomial in [(3, 0xb), (5, 0x25), (7, 0x83)]]
    result = dict(status='PASS_LITERAL_SUZUKI_ROOT_QUOTIENT_CONTROLS', rows=rows,
                  seconds=time.monotonic()-start, ambient_group_censuses=0,
                  numerical_source_credit=0, whole_original_credit=0,
                  qualification='Checks the finite quotient algebra, not the borrowed ambient subgroup classification.')
    a.out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
