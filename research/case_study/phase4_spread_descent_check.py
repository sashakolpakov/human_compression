"""Exhaustive small checks of the semilinear descent obstruction.

Enumerate all F2-subspaces of the selected dimension containing 1, quotient
by scalar/Frobenius equivalence, and compute the full GammaL1 stabilizer of
each representative. Test its action for irreducibility directly. No spread
or classification library is used. The degree-six case is a boundary control.
"""
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path


class BinaryField:
    def __init__(self, degree, modulus):
        self.degree, self.modulus = degree, modulus
        self.size = 1 << degree
        self.table = [[self.multiply(a, b) for b in range(self.size)]
                      for a in range(self.size)]
        self.inverses = [0] + [self.power(a, self.size-2) for a in range(1, self.size)]
        assert all(self.table[a][self.inverses[a]] == 1 for a in range(1, self.size))
        self.frobenius = [[self.power(a, 1 << i) for a in range(self.size)]
                          for i in range(degree)]

    def multiply(self, a, b):
        value = 0
        while b:
            if b & 1:
                value ^= a
            a <<= 1
            if a & self.size:
                a ^= self.modulus
            b >>= 1
        return value

    def power(self, a, exponent):
        value = 1
        while exponent:
            if exponent & 1:
                value = self.table[value][a]
            a = self.table[a][a]
            exponent >>= 1
        return value


def subspaces(n, dimension):
    for pivots in combinations(range(n), dimension):
        positions = [(i, j) for i, pivot in enumerate(pivots)
                     for j in range(pivot+1, n) if j not in pivots]
        for bits in product(range(2), repeat=len(positions)):
            basis = [1 << pivot for pivot in pivots]
            for bit, (i, j) in zip(bits, positions):
                basis[i] |= bit << j
            values = [0]
            for v in basis:
                values += [x ^ v for x in values]
            yield tuple(sorted(values))


def irreducible(U, maps):
    for vector in U[1:]:
        span = {0, vector}
        while True:
            previous = len(span)
            for action in maps:
                for v in tuple(span):
                    w = action[v]
                    if w not in span:
                        span |= {x ^ w for x in tuple(span)}
            if len(span) == previous:
                break
        if len(span) != len(U):
            return False
    return True


def check(degree, dimension, modulus):
    F = BinaryField(degree, modulus)
    seen, total, representatives = set(), 0, []
    for quotient in subspaces(degree-1, dimension-1):
        U = tuple(sorted([2*x for x in quotient] + [2*x+1 for x in quotient]))
        total += 1
        if U in seen:
            continue
        maps = []
        orbit = set()
        for frobenius in F.frobenius:
            image = [frobenius[x] for x in U]
            for w in image[1:]:
                a = F.inverses[w]
                target = tuple(sorted(F.table[a][x] for x in image))
                orbit.add(target)
                if target == U:
                    maps.append({v:F.table[a][frobenius[v]] for v in U})
        assert not (orbit & seen)
        seen |= orbit
        primitive = irreducible(U, maps)
        subfield = all(F.power(v, 1 << dimension) == v for v in U)
        if degree in (4, 8):
            assert primitive == subfield
        representatives.append({'elements':U, 'normalized_orbit_size':len(orbit),
                                'full_semilinear_stabilizer_order':len(maps),
                                'irreducible':primitive, 'subfield':subfield})
    assert len(seen) == total
    expected = {(4,2):7, (8,4):11811, (6,2):31}
    assert total == expected[degree, dimension]
    rows = [r for r in representatives if r['irreducible']]
    if degree in (4, 8):
        assert len(rows) == 1 and rows[0]['subfield']
    else:
        assert any(not r['subfield'] for r in rows)
    report = {'characteristic':2, 'ambient_degree':degree, 'line_dimension':dimension,
              'modulus_bits':modulus, 'putative_spread_size':(F.size-1)//((1 << dimension)-1),
              'subspaces_containing_one':total, 'semilinear_orbits':len(representatives),
              'irreducible_stabilizer_orbits':rows,
              'scope':'All subspaces, not only members of spreads; normalized by scalar/Frobenius equivalence.'}
    print(json.dumps(report), flush=True)
    return report


def main():
    results = [check(4,2,0x13), check(8,4,0x11b), check(6,2,0x43)]
    source = Path(__file__)
    report = {'status':'PASS', 'source_sha256':sha256(source.read_bytes()).hexdigest(),
              'arithmetic':'exact binary polynomial quotients, verified inverses',
              'results':results,
              'boundary':'Degree six has a non-subfield line with irreducible semilinear stabilizer. Its putative spread size is composite; it is not a counterexample to the prime-degree theorem.'}
    source.with_suffix('.json').write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()
