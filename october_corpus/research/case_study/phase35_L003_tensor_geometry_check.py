#!/usr/bin/env python3
"""Exact bounded-word certificate for the uniform L003 tensor geometry."""
import argparse
from collections import deque
from functools import lru_cache
from hashlib import sha256
import json
from pathlib import Path

I = (1, 0, 0, 1)
D = (0, 1, 1, 0)
R = (1, -1, 0, -1)
S = (0, 1, -1, 0)
Q = (1, 0, 1, -1)
N = (0, 1, 1, 1)
ONE = ((0, 1, 2), (I, I, I))
PARABOLIC_MASKS = (14, 13, 11, 7)
PROTECTED_TYPES = (0, 2, 3)
PROTECTED_ORDERS = (36, 48, 108)


class TensorArithmetic:
    def __init__(self, modulus=None):
        self.modulus = modulus
        self.key = lru_cache(None)(self._key)
        cycle = (2, 0, 1)
        self.x = (cycle, (tuple(-a for a in D), R, R))
        self.y = (cycle, (I, I, I))
        self.z = ((0, 1, 2), (S, Q, S))
        flip = ((2, 1, 0), (I, I, I))
        self.marks = (flip, self.mul(flip, self.x),
                      self.mul(flip, self.y), self.mul(flip, self.z))
        self.one = self.key(ONE)

    def reduce(self, a):
        return a if self.modulus is None else a % self.modulus

    def mm(self, a, b):
        return tuple(self.reduce(c) for c in (
            a[0]*b[0]+a[1]*b[2], a[0]*b[1]+a[1]*b[3],
            a[2]*b[0]+a[3]*b[2], a[2]*b[1]+a[3]*b[3]))

    def mi(self, a):
        determinant = self.reduce(a[0]*a[3]-a[1]*a[2])
        if self.modulus is None:
            assert determinant in (-1, 1)
            reciprocal = determinant
        else:
            reciprocal = pow(determinant, -1, self.modulus)
        return tuple(self.reduce(reciprocal*c)
                     for c in (a[3], -a[1], -a[2], a[0]))

    def mul(self, g, h):
        p, a = g
        q, b = h
        return tuple(q[i] for i in p), tuple(self.mm(a[i], b[p[i]]) for i in range(3))

    def inv(self, g):
        p, a = g
        q = tuple(p.index(i) for i in range(3))
        return q, tuple(self.mi(a[q[i]]) for i in range(3))

    def power(self, g, exponent):
        if exponent < 0:
            return self.power(self.inv(g), -exponent)
        result = ONE
        while exponent:
            if exponent & 1:
                result = self.mul(result, g)
            g = self.mul(g, g)
            exponent //= 2
        return result

    def product(self, *items):
        result = ONE
        for g in items:
            result = self.mul(result, g)
        return result

    def _key(self, g):
        """Literal row-convention 8x8 matrix, never just projective factor data."""
        p, a = g
        return tuple(self.reduce(
            a[0][2*(i >> 2)+((j >> (2-p[0])) & 1)] *
            a[1][2*((i >> 1) & 1)+((j >> (2-p[1])) & 1)] *
            a[2][2*(i & 1)+((j >> (2-p[2])) & 1)])
            for i in range(8) for j in range(8))

    def closure(self, mask, bound):
        generators = [self.marks[i] for i in range(4) if mask >> i & 1]
        seen = {self.one: ONE}
        queue = deque([ONE])
        while queue:
            g = queue.popleft()
            for h in generators:
                gh = self.mul(g, h)
                k = self.key(gh)
                if k not in seen:
                    seen[k] = gh
                    queue.append(gh)
            assert len(seen) <= bound, (mask, bound, len(seen))
        return seen


def integer_certificate():
    ar = TensorArithmetic()
    assert all(ar.key(ar.power(g, 2)) == ar.one and ar.key(g) != ar.one
               for g in ar.marks)
    # Check the normalizer action used in the written membership lemma.
    for a in (S, Q):
        assert ar.mm(ar.mm(ar.mi(a), N), a) == (1, -1, -1, 0)
    pure_permutations = ar.closure(5, 6)
    assert len(pure_permutations) == 6
    assert all(g[1] == (I, I, I) for g in pure_permutations.values())
    torus = ar.product(ar.y, ar.power(ar.mul(ar.z, ar.y), 2))
    assert ar.key(torus) == ar.key(((0, 1, 2), (ar.mi(N), I, N)))
    protected_groups = [ar.closure(PARABOLIC_MASKS[i], bound)
                        for i, bound in zip(PROTECTED_TYPES, PROTECTED_ORDERS)]
    assert list(map(len, protected_groups)) == list(PROTECTED_ORDERS)
    protected = {k: g for group in protected_groups for k, g in group.items()}
    words = {}
    for a in protected.values():
        for b in protected.values():
            ab = ar.mul(a, b)
            words[ar.key(ab)] = ab
    assert len(protected) == 172 and len(words) == 1928
    entry_bound = max(abs(c) for k in words for c in k)
    assert entry_bound == 2

    # This is a finite literal lookup, not a unit-group classification.
    powers = {}
    for exponent in range(-2, 3):
        matrix = I
        step = N if exponent >= 0 else ar.mi(N)
        for _ in range(abs(exponent)):
            matrix = ar.mm(matrix, step)
        for sign in (-1, 1):
            powers[tuple(sign*c for c in matrix)] = (exponent, sign)
    assert len(powers) == 10
    witnesses = []
    bound = 0
    for index, k in enumerate(sorted(words)):
        g = words[k]
        for epsilon in (0, 1):
            h = ar.mul(g, ar.z) if epsilon else g
            commutators = [tuple(c-d for c, d in zip(ar.mm(a, N), ar.mm(N, a)))
                           for a in h[1]]
            bound = max(bound, max(abs(c) for row in commutators for c in row))
            if all(row == (0, 0, 0, 0) for row in commutators):
                assert all(a in powers for a in h[1])
                labels = [powers[a] for a in h[1]]
                assert sum(k for k, sign in labels) == 0
                assert labels[0][1]*labels[1][1]*labels[2][1] == 1
                witnesses.append({'sorted_product_index': index,
                                  'epsilon': epsilon,
                                  'permutation': list(h[0]),
                                  'factor_matrices': [list(a) for a in h[1]],
                                  'exponents_and_signs': labels})
    assert bound == 4 and len(witnesses) == 52
    return {'protected_subgroup_orders': list(map(len, protected_groups)),
            'protected_union_size': len(protected), 'pair_product_size': len(words),
            'pair_product_entry_bound': entry_bound,
            'commutator_tests': 2*len(words), 'factor_commutators_per_test': 3,
            'commutator_entry_bound': bound, 'commuting_cases': len(witnesses),
            'maximum_absolute_witness_exponent': 2,
            'membership_witnesses': witnesses}


def base_certificate(modulus, parameter):
    ar = TensorArithmetic(modulus)
    assert all(ar.key(ar.power(g, 2)) == ar.one and ar.key(g) != ar.one for g in ar.marks)
    groups = {mask: ar.closure(mask, 12*parameter*parameter if mask == 13 else 108)
              for mask in range(15)}
    assert all(groups[a].keys() & groups[b].keys() == groups[a & b].keys()
               for a in range(15) for b in range(15))
    pars = [groups[mask] for mask in PARABOLIC_MASKS]
    assert list(map(len, pars)) == [36, 12*parameter*parameter, 48, 108]
    representatives = {k: g for group in groups.values() for k, g in group.items()}

    @lru_cache(None)
    def in_product(k, i, j):
        a = representatives[k]
        # If a variable parabolic occurs, always enumerate the other factor.
        if i == 1:
            assert j != 1
            return any(ar.key(ar.mul(a, ar.inv(b))) in pars[i] for b in pars[j].values())
        if j == 1:
            return any(ar.key(ar.mul(ar.inv(b), a)) in pars[j] for b in pars[i].values())
        return any(ar.key(ar.mul(ar.inv(b), a)) in pars[j] for b in pars[i].values())

    helly = []
    for i in range(4):
        others = [j for j in range(4) if j != i]
        for mask in range(1, 8):
            js = [others[k] for k in range(3) if mask >> k & 1]
            if len(js) < 2:
                continue
            j0 = next(j for j in js if j != 1)
            meet = pars[i].keys() & pars[j0].keys()
            covered = set()
            reps = []
            for k, a in pars[j0].items():
                if k not in covered:
                    reps.append(k)
                    covered.update(ar.key(ar.mul(pars[j0][b], a)) for b in meet)
            assert covered == pars[j0].keys()
            eligible = sum(all(in_product(k, i, j) for j in js if j != j0) for k in reps)
            common = set(pars[j0])
            for j in js:
                common.intersection_update(pars[j])
            assert len(common) % len(common & pars[i].keys()) == 0
            supplied = len(common) // len(common & pars[i].keys())
            assert eligible == supplied, (modulus, i, js, eligible, supplied)
            helly.append({'new_type': i, 'base_types': js, 'protected_anchor': j0,
                          'representative_count': len(reps), 'eligible_cosets': eligible,
                          'common_point_cosets': supplied})
    assert len(helly) == 16
    return {'modulus': modulus, 'source_parameter': parameter,
            'proper_subgroup_orders': {str(k): len(v) for k, v in groups.items()},
            'executed_proper_subgroup_meets': 225,
            'additional_tautological_meets_with_full_group': 31,
            'typed_helly_cardinality_checks': helly,
            'ambient_group_enumerated': False}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise SystemExit('Refusing to overwrite an existing certificate')
    integer = integer_certificate()
    print('PASS:172 protected elements,1928 products, entry bound2, commutator bound4,52 exact witnesses.', flush=True)
    bases = [base_certificate(3, 4), base_certificate(5, 5)]
    print('PASS: moduli3/5,450 proper meets and32 typed-Helly cardinalities.', flush=True)
    report = {'result': 'PASS', 'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
              'integer_certificate': integer, 'base_certificates': bases,
              'scope': 'Exact finite bounded-word data and complete proper-subgroup/typed-Helly checks at moduli3/5. All-modulus transfer, the factor-algebra lemma and geometry adapter are written proofs; no ambient recognition or full Lean theorem.'}
    args.output.write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
