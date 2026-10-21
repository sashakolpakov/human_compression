#!/usr/bin/env python3
"""Independent finite diagnostics for AA.ParabolicPeriods.

Direct quotient-group enumeration is compared with exact integral Schreier
translations and lattice membership. No author implementation is imported.
These checks are not the proof for arbitrary lattices or parameters.
"""
from collections import deque
from itertools import combinations
from math import gcd
from pathlib import Path
import argparse
import json

IDENTITY = (1, 0, 0, 1)
ZERO = (0, 0)


def need(value, reason):
    if not value:
        raise ValueError(reason)


def plus(u, v):
    return (u[0] + v[0], u[1] + v[1])


def minus(u, v):
    return (u[0] - v[0], u[1] - v[1])


def act(q, v):
    return (q[0] * v[0] + q[1] * v[1], q[2] * v[0] + q[3] * v[1])


def mulq(a, b):
    return (a[0]*b[0]+a[1]*b[2], a[0]*b[1]+a[1]*b[3],
            a[2]*b[0]+a[3]*b[2], a[2]*b[1]+a[3]*b[3])


def inverseq(a):
    d = a[0]*a[3] - a[1]*a[2]
    need(abs(d) == 1, 'Unimodular linear part')
    return (a[3]//d, -a[1]//d, -a[2]//d, a[0]//d)


def affine(a, b):
    return mulq(a[0], b[0]), plus(a[1], act(a[0], b[1]))


def inverse(a):
    q = inverseq(a[0]); t = act(q, a[1])
    return q, (-t[0], -t[1])


def det(a, b):
    return a[0]*b[1] - a[1]*b[0]


class Lattice:
    def __init__(self, vectors):
        self.vectors = tuple(sorted(set(v for v in vectors if v != ZERO)))
        self.index = 0
        for a, b in combinations(self.vectors, 2):
            self.index = gcd(self.index, abs(det(a, b)))
        self.direction = None
        if self.vectors and not self.index:
            v = self.vectors[0]; scale = gcd(abs(v[0]), abs(v[1]))
            self.direction = (v[0]//scale, v[1]//scale)
            coordinate = 0 if self.direction[0] else 1
            self.step = 0
            for w in self.vectors:
                need(det(self.direction, w) == 0, 'Rank-one lattice')
                self.step = gcd(self.step, abs(w[coordinate]//self.direction[coordinate]))

    def contains(self, v):
        if not self.vectors:
            return v == ZERO
        if not self.index:
            if det(self.direction, v):
                return False
            coordinate = 0 if self.direction[0] else 1
            d = self.direction[coordinate]
            return v[coordinate] % d == 0 and (v[coordinate]//d) % self.step == 0
        return all(det(w, v) % self.index == 0 for w in self.vectors)


def schreier(markers):
    generators = list(markers) + [inverse(g) for g in markers]
    lifts = {IDENTITY: ZERO}; todo = deque([IDENTITY])
    while todo:
        q = todo.popleft()
        for g in generators:
            a, u = affine((q, lifts[q]), g)
            if a not in lifts:
                lifts[a] = u; todo.append(a)
                need(len(lifts) <= 8, 'Only declared finite linear fixtures')
    translations = []
    for q, u in lifts.items():
        for g in generators:
            a, v = affine((q, u), g)
            translations.append(minus(v, lifts[a]))
    return lifts, Lattice(translations)


class Period:
    def __init__(self, vectors):
        self.lattice = Lattice(vectors)
        need(self.lattice.index > 0, 'Finite diagnostic requires full-rank period')
        self.representatives = [ZERO]; todo = deque([ZERO])
        while todo:
            u = todo.popleft()
            for v in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                w = plus(u, v)
                if not any(self.lattice.contains(minus(w, z)) for z in self.representatives):
                    self.representatives.append(w); todo.append(w)
        need(len(self.representatives) == self.lattice.index, 'Exact lattice index')

    def reduce(self, u):
        return next(v for v in self.representatives if self.lattice.contains(minus(u, v)))

    def multiply(self, a, b):
        q, u = affine(a, b)
        return q, self.reduce(u)

    def subgroup(self, markers):
        unit = (IDENTITY, ZERO); found = {unit}; todo = deque([unit])
        generators = list(markers) + [inverse(g) for g in markers]
        while todo:
            a = todo.popleft()
            for g in generators:
                b = self.multiply(a, g)
                if b not in found:
                    found.add(b); todo.append(b)
        return found


def check_fixture(name, markers, periods):
    p = Period(periods); count = 1 << len(markers)
    linear, translation = schreier(markers)
    need(all(translation.contains(v) for v in periods), 'Period must lie in the actual whole translation kernel')
    need(all(p.lattice.contains(act(q, v)) for q in linear for v in periods), 'Period must be normal')
    lifts, kernels, images = {}, {}, {}
    for mask in range(count):
        subset = [g for i, g in enumerate(markers) if mask & (1 << i)]
        lifts[mask], kernels[mask] = schreier(subset)
        images[mask] = p.subgroup(subset)
        for q, u in lifts[mask].items():
            total = Lattice(kernels[mask].vectors + tuple(periods))
            expected = {v for v in p.representatives if total.contains(minus(v, u))}
            actual = {v for a, v in images[mask] if a == q}
            need(expected == actual, 'Integral Schreier fibers versus direct quotient enumeration')
    failures = []; fiber_pairs = 0; kernels_only_pass = True; exclusions_only_pass = True
    for j in range(count):
        for t in range(count):
            c = j & t
            addj = Lattice(kernels[j].vectors + tuple(periods))
            addt = Lattice(kernels[t].vectors + tuple(periods))
            addc = Lattice(kernels[c].vectors + tuple(periods))
            kj = {v for v in p.representatives if addj.contains(v)}
            kt = {v for v in p.representatives if addt.contains(v)}
            kc = {v for v in p.representatives if addc.contains(v)}
            kernel_condition = kj & kt == kc
            sum_lattice = Lattice(kernels[j].vectors + kernels[t].vectors + tuple(periods))
            outside = set(lifts[j]) & set(lifts[t]) - set(lifts[c])
            excluded = all(not sum_lattice.contains(minus(lifts[j][q], lifts[t][q])) for q in outside)
            intersection = images[j] & images[t]
            actual_ip = intersection == images[c]
            need(actual_ip == (kernel_condition and excluded), 'Exact two-condition equivalence')
            kernels_only_pass &= kernel_condition; exclusions_only_pass &= excluded
            if not actual_ip:
                failures.append([j, t])
            for q in set(lifts[j]) & set(lifts[t]):
                possible = sum_lattice.contains(minus(lifts[j][q], lifts[t][q]))
                actual = {v for a, v in intersection if a == q}
                need(bool(actual) == possible, 'Exact intersection-fiber existence')
                if actual:
                    v = next(iter(actual))
                    need(actual == {p.reduce(plus(v, w)) for w in kj & kt}, 'Exact intersection-fiber coset')
                # Shift the lift by an actual translation generator.
                shift = kernels[j].vectors[0] if kernels[j].vectors else ZERO
                need(sum_lattice.contains(minus(plus(lifts[j][q], shift), lifts[t][q])) == possible,
                     'Independence of lift representative')
                fiber_pairs += 1
    return dict(name=name, point_order=len(linear), period_index=p.lattice.index,
                quotient_order=len(images[count-1]), parabolic_pairs=count*count,
                common_linear_fibers=fiber_pairs, intersection_property=not failures,
                failures=len(failures), kernel_conditions_all=kernels_only_pass,
                exclusion_conditions_all=exclusions_only_pass)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args(); need(not args.out.exists(), 'Fresh output file')
    neg = (-1, 0, 0, -1); swap = (0, 1, 1, 0); flip = (-1, 0, 0, 1)
    translations = [(IDENTITY, (1, 0)), (IDENTITY, (0, 1))]
    reflections = [(neg, ZERO), (neg, (1, 0)), (neg, (0, 1))]
    square = [(swap, ZERO), (flip, ZERO)] + translations
    rows = [check_fixture('diagonal_period', translations, [(1, -1), (0, 2)]),
            check_fixture('separate_coordinates', translations, [(2, 0), (0, 2)]),
            check_fixture('coincident_reflections', reflections, [(1, 0), (0, 1)])]
    for label, markers in [('reflections', reflections), ('square', square)]:
        for n in [2, 3, 4]:
            rows.append(check_fixture(f'{label}_scale_{n}', markers, [(n, 0), (0, n)]))
    rows.append(check_fixture('square_diagonal_lattice', square, [(1, 1), (1, -1)]))
    need(not rows[0]['intersection_property'] and rows[0]['exclusion_conditions_all'], 'Kernel condition is necessary')
    need(not rows[2]['intersection_property'] and rows[2]['kernel_conditions_all'], 'Exclusion condition is necessary')
    try:
        check_fixture('non_normal_period', square, [(2, 0), (0, 3)])
    except ValueError as e:
        need(str(e) == 'Period must be normal', 'Reject at the actual normality hypothesis')
    else:
        raise ValueError('Non-normal period accepted')
    result = dict(status='PASS_INDEPENDENT_AFFINE_PERIOD_DIAGNOSTICS', models=rows,
                  total_parabolic_pairs=sum(r['parabolic_pairs'] for r in rows),
                  total_common_linear_fibers=sum(r['common_linear_fibers'] for r in rows),
                  controls=['omitted_kernel_condition', 'omitted_linear_exclusion', 'non_normal_period'],
                  author_modules_imported=False, full_parameter_proof=False,
                  arbitrary_rank_periods_formalized=False, role='Optional reviewer diagnostics; written proof is separate')
    args.out.write_text(json.dumps(result, indent=2) + '\n'); print(json.dumps(result))


if __name__ == '__main__':
    main()
