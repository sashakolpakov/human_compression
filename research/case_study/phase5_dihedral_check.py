#!/usr/bin/env python3
"""Independent finite-set audit of phase5_dihedral_classification.md.

Standard library only. Subgroups are generated from the multiplication table,
not supplied by the classification. All irredundant subgroup families are
enumerated, including nonmaximal subgroup candidates. Reports are written next
to this file. Finite checks do not establish the all-n theorem.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import time


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def primes(n):
    out = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            out.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        out.append(n)
    return out


def choose(n, k):
    return math.comb(n, k) if 0 <= k <= n else 0


class Dihedral:
    def __init__(self, n):
        self.n = n
        self.size = 2 * n
        self.whole = (1 << self.size) - 1
        self.mul = [[((a % n + (-1 if a >= n else 1) * (b % n)) % n)
                     + n * ((a // n) ^ (b // n))
                     for b in range(self.size)] for a in range(self.size)]
        # Discover the entire subgroup lattice by adjoining all possible elements.
        gens = {1: ()}
        queue = [1]
        for h in queue:
            for g in bits(self.whole ^ h):
                gs = gens[h] + (g,)
                new = self.closure(gs)
                if new not in gens:
                    gens[new] = gs
                    queue.append(new)
        self.groups = sorted(queue, key=lambda x: (x.bit_count(), x))
        self.proper = [h for h in self.groups if h != self.whole]
        self.maxdown = {}
        for h in self.groups:
            lower = [a for a in self.groups if a != h and a & h == a]
            self.maxdown[h] = {
                a for a in lower
                if not any(a != b and a & b == a for b in lower)
            }
        self.rotation = self.closure((1,))
        self.hpa = {(p, a): self.closure((p % n, n + a))
                    for p in primes(n) for a in range(p)}
        assert len(self.groups) == sum(1 + d for d in range(1, n + 1) if n % d == 0)

    def closure(self, gs):
        known = {0}
        queue = [0]
        for a in queue:
            for b in gs:
                c = self.mul[a][b]
                if c not in known:
                    known.add(c)
                    queue.append(c)
        return sum(1 << x for x in known)

    def meet(self, family):
        result = self.whole
        for h in family:
            result &= h
        return result

    def irredundant(self, family):
        total = self.meet(family)
        return all(self.meet(family[:j] + family[j+1:]) != total
                   for j in range(len(family)))

    def rwpri(self, family):
        intersections = [self.whole]
        for h in family:
            intersections += [a & h for a in intersections]
        k = len(family)
        for mask in range((1 << k) - 1):
            if not any(intersections[mask | (1 << j)] in self.maxdown[intersections[mask]]
                       for j in range(k) if not mask & (1 << j)):
                return False
        return True

    def predicted(self):
        ps = primes(self.n)
        families = set()
        for mask in range(1 << len(ps)):
            selected = [p for j, p in enumerate(ps) if mask & (1 << j)]
            for residues in itertools.product(*(range(p) for p in selected)):
                hs = tuple(self.hpa[p, a] for p, a in zip(selected, residues))
                if hs:
                    families.add(tuple(sorted(hs)))
                families.add(tuple(sorted(hs + (self.rotation,))))
        for p in ps:
            other = [q for q in ps if q != p]
            for a, b in itertools.combinations(range(p), 2):
                pair = (self.hpa[p, a], self.hpa[p, b])
                for mask in range(1 << len(other)):
                    selected = [q for j, q in enumerate(other) if mask & (1 << j)]
                    for residues in itertools.product(*(range(q) for q in selected)):
                        hs = tuple(self.hpa[q, c] for q, c in zip(selected, residues))
                        families.add(tuple(sorted(pair + hs)))
        return families

    def all_rwpri(self):
        tested = {}
        accepted = set()
        def extend(family, start):
            for i in range(start, len(self.proper)):
                h = self.proper[i]
                if any((a & h) in (a, h) for a in family):
                    continue
                new = family + (h,)
                # Redundancy cannot disappear by adding more subgroup intersections.
                if not self.irredundant(new):
                    continue
                tested[len(new)] = tested.get(len(new), 0) + 1
                if self.rwpri(new):
                    accepted.add(tuple(sorted(new)))
                    # Audit the stronger conclusion directly in the actual lattice.
                    for mask in range(1 << len(new)):
                        current = self.meet(tuple(new[j] for j in range(len(new))
                                                  if mask & (1 << j)))
                        for j, a in enumerate(new):
                            if not mask & (1 << j):
                                assert current & a in self.maxdown[current]
                extend(new, i + 1)
        extend((), 0)
        return accepted, tested

    def automorphisms(self):
        n = self.n
        if n == 2:
            for a, b in itertools.permutations((1, 2, 3), 2):
                yield [0, a, b, self.mul[a][b]]
        else:
            for u in range(n):
                if math.gcd(u, n) == 1:
                    for v in range(n):
                        yield [(u * (g % n) + v * (g // n)) % n + n * (g // n)
                               for g in range(2 * n)]

    def orbit_reps(self, families):
        transformations = []
        for perm in self.automorphisms():
            transformations.append({h: sum(1 << perm[g] for g in bits(h))
                                    for h in self.proper})
        orbits = {}
        for family in families:
            rep = min(tuple(sorted(tr[h] for h in family)) for tr in transformations)
            orbits[rep] = family
        return sorted(orbits)

    def cosets(self, h):
        unseen = self.whole
        out = []
        while unseen:
            g = next(bits(unseen))
            c = sum(1 << self.mul[g][x] for x in bits(h))
            assert c & unseen == c
            out.append(c)
            unseen ^= c
        return out

    def geometry_audit(self, family):
        types = [self.cosets(h) for h in family]
        flag_count = 0
        residue_count = 0
        for selection in itertools.product(*([None] + xs for xs in types)):
            present = [x for x in selection if x is not None]
            if any(not a & b for a, b in itertools.combinations(present, 2)):
                continue
            flag_count += 1
            assert self.meet(present), 'Typed Helly failure'
            residue = [[x for x in types[i] if all(x & y for y in present)]
                       for i in range(len(types)) if selection[i] is None]
            if len(residue) == 1:
                assert len(residue[0]) >= 2, 'Firmness failure'
            if len(residue) >= 2:
                vertices = [(i, x) for i, xs in enumerate(residue) for x in xs]
                seen = {vertices[0]}
                queue = [vertices[0]]
                for i, a in queue:
                    for j, b in vertices:
                        if i != j and a & b and (j, b) not in seen:
                            seen.add((j, b))
                            queue.append((j, b))
                assert len(seen) == len(vertices), 'Residual connectivity failure'
            if len(residue) == 2:
                residue_count += 1
                left, right = residue
                complete = all(a & b for a in left for b in right)
                if not complete:
                    for xs, ys in ((left, right), (right, left)):
                        for a, b in itertools.combinations(xs, 2):
                            assert sum(bool(a & y and b & y) for y in ys) <= 1, 'IP2 failure'
        return flag_count, residue_count


def run(n):
    start = time.monotonic()
    group = Dihedral(n)
    accepted, tested = group.all_rwpri()
    assert accepted == group.predicted(), (n, len(accepted), len(group.predicted()))
    reps = group.orbit_reps(accepted)
    counts = {k: sum(len(t) == k for t in reps) for k in range(1, max(tested) + 2)}
    m = len(primes(n))
    expected = {k: (int(k in (1, 2)) if n == 2 else
                    choose(m, k) + choose(m, k-1) + m * choose(m-1, k-2))
                for k in counts}
    assert counts == expected, (n, counts, expected)
    flags = residues = 0
    for family in reps:
        f, r = group.geometry_audit(family)
        flags += f
        residues += r
    result = dict(n=n, group_order=2*n, subgroup_count=len(group.groups),
                  irredundant_candidates_by_rank=tested,
                  rwpri_marked_families=len(accepted),
                  automorphism_and_type_classes_by_rank=counts,
                  flags_checked=flags, rank_two_residues_checked=residues,
                  elapsed_seconds=round(time.monotonic()-start, 4))
    print(f'n={n}: PASS; {len(group.groups)} subgroups, '
          f'{sum(tested.values())} irredundant candidates, classes {counts}', flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, nargs='+', default=list(range(2, 17)) + [18, 24, 30])
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).with_suffix('.json'))
    args = parser.parse_args()
    assert all(n >= 2 for n in args.n)
    results = [run(n) for n in args.n]
    report = dict(status='PASS', method='exact finite sets from group multiplication',
                  scope='Finite audit only; all-n classification is a separate paper proof.',
                  checks=['all subgroups generated by successive element adjunction',
                          'all irredundant proper-subgroup families enumerated',
                          'RWPRI tested from exact maximal-subgroup inclusion lattice',
                          'accepted families equal the three arithmetic patterns',
                          'every parabolic cover maximal in accepted families',
                          'all automorphism/type orbit counts equal the formula',
                          'typed coset Helly, firmness, residual connectivity and IP2'],
                  script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  results=results)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(f'PASS {len(results)}/{len(results)} dihedral groups; report {args.output.name}')


if __name__ == '__main__':
    main()
