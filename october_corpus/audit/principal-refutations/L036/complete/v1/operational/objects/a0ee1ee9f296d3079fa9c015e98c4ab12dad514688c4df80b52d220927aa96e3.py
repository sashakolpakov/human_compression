"""Exact mark arithmetic; library completeness and named groups are premises."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode = True
from pathlib import Path
from fractions import Fraction
from collections import Counter
from math import gcd
import argparse
import hashlib
import json
import re

OUTER = ['M12.2', 'J2.2', 'J3.2', 'HS.2', 'McL.2', 'He.2']
SIMPLE = ['M11', 'M12', 'M22', 'M23', 'J1']


def need(ok, message):
    if not ok:
        raise ValueError(message)


def positive(x):
    return type(x) is int and x > 0


def divide(n, d, message):
    need(type(n) is int and n >= 0 and positive(d) and n % d == 0, message)
    return n // d


def whole(x, message):
    need(x.denominator == 1, message)
    return x.numerator


class MarkData:
    def __init__(self, data):
        need(type(data) is list and len(data) == 12, 'Twelve-field input row')
        (self.name, self.identifier, self.order, self.orders, subs, marks,
         self.centralizers, self.square, self.element_orders, fusion,
         self.maximal_names, self.maximal_permutation) = data
        need(self.name in OUTER + SIMPLE and self.identifier == self.name, 'Named table identity')
        need(positive(self.order) and type(self.orders) is list and self.orders, 'Positive parent order')
        self.n = len(self.orders)
        need(self.orders[0] == 1 and self.orders[-1] == self.order, 'Trivial and full subgroup classes')
        need(type(subs) is list and type(marks) is list and len(subs) == len(marks) == self.n,
             'Complete supplied sparse table dimensions')
        self.rows = []
        for i, (order, positions, values) in enumerate(zip(self.orders, subs, marks)):
            divide(self.order, order, 'Subgroup order divides group order')
            need(type(positions) is list and type(values) is list and positions and
                 len(positions) == len(values), 'Nonempty parallel sparse row')
            need(all(positive(p) and p <= i + 1 for p in positions) and
                 positions == sorted(set(positions)) and positions[0] == 1 and positions[-1] == i + 1,
                 'Strict triangular sparse support with identity and diagonal')
            need(all(positive(v) and v <= self.order // order for v in values), 'Positive bounded marks')
            row = {p - 1: v for p, v in zip(positions, values)}
            need(row[0] == self.order // order, 'Identity mark is the subgroup index')
            divide(self.order, order * row[i], 'Normalizer order divides parent order')
            self.rows.append(row)
        need(self.rows[-1] == {i: 1 for i in range(self.n)}, 'Full subgroup row contains every class once')
        for i, row in enumerate(self.rows):
            for j, value in row.items():
                divide(self.orders[i], self.orders[j], 'Containment order divisibility')
                divide(value * self.orders[i], self.orders[j] * self.rows[j][j],
                       'Integral number of conjugates contained in a subgroup')
        cents = self.centralizers
        need(type(cents) is list and cents and cents[0] == self.order, 'Identity centralizer')
        need(sum(divide(self.order, c, 'Centralizer divisor') for c in cents) == self.order,
             'Element conjugacy classes exhaust group')
        k = len(cents)
        need(type(self.square) is list and type(self.element_orders) is list and type(fusion) is list and
             len(self.square) == len(self.element_orders) == len(fusion) == k,
             'Class-array dimensions')
        need(self.square[0] == fusion[0] == self.element_orders[0] == 1, 'Identity maps')
        need(all(positive(s) and s <= k for s in self.square), 'Square map range')
        need(all(positive(f) and f <= self.n for f in fusion), 'Cyclic fusion range')
        self.fusion = [f - 1 for f in fusion]
        for i, (order, f, s) in enumerate(zip(self.element_orders, self.fusion, self.square)):
            divide(self.order, order, 'Element order divisor')
            need(self.orders[f] == order, 'Fusion preserves cyclic order')
            need(self.element_orders[s - 1] == order // gcd(order, 2), 'Square element order')
            divide(cents[s - 1], cents[i], 'Centralizer inclusion on squaring')
        if self.name in OUTER:
            need(self.maximal_names == self.maximal_permutation == [], 'No outer maximal-name input')
        else:
            names = self.maximal_names
            perm = self.maximal_permutation
            # Isomorphic maximal classes can share a character-table identifier
            # (the two A7 classes in M22 do). Positions distinguish classes.
            need(type(names) is list and names and all(type(s) is str and s for s in names),
                 'Maximal character identifiers, with class positions retained')
            need(type(perm) is list and sorted(perm) == list(range(1, len(names) + 1)),
                 'Stored maximal-class bijection')

    def maximal_below(self, top):
        proper = set(self.rows[top]) - {top}
        below_proper = set()
        for j in proper:
            below_proper.update(set(self.rows[j]) - {j})
        maxima = proper - below_proper
        need(maxima and maxima <= proper, 'Nonempty maximal classes below parent')
        # Descending class positions agree with the documented GAP list order.
        return sorted(maxima, reverse=True)

    def character(self, index):
        row = self.rows[index]
        chi = [row.get(f, 0) for f in self.fusion]
        need(chi[0] == self.order // self.orders[index], 'Transitive character degree')
        need(sum(Fraction(x, c) for x, c in zip(chi, self.centralizers)) == 1,
             'Transitive character has one orbit')
        return chi

    def pair_count(self):
        if self.name in OUTER:
            candidates = [i for i, order in enumerate(self.orders) if 2 * order == self.order]
            need(len(candidates) == 1, 'Unique subgroup class of index two')
            socle = candidates[0]
            # A subgroup of index two is normal, so its coset character is 0 or 2.
            need(set(self.character(socle)) <= {0, 2}, 'Normal socle coset character')
        else:
            socle = self.n - 1
        maxima = self.maximal_below(socle)
        normalizers = []
        for m in maxima:
            diagonal = self.rows[m][m]
            need(diagonal in [1, 2] if self.name in OUTER else diagonal == 1,
                 'Simple-group maximal normalizer index')
            if diagonal == 1:
                normalizers.append(m)
            else:
                choices = [j for j, order in enumerate(self.orders)
                           if order == 2 * self.orders[m] and m in self.rows[j]]
                need(len(choices) == 1, 'Unique containing normalizer of twice the order')
                normalizers.append(choices[0])
        characters = [self.character(j) for j in normalizers]
        psi = [sum(values) for values in zip(*characters)]
        cents = self.centralizers
        need(sum(Fraction(x, c) for x, c in zip(psi, cents)) == len(maxima),
             'One subgroup orbit per supplied maximal class')
        fixed_pairs = []
        for i, x in enumerate(psi):
            numerator = x * x - 2 * x + psi[self.square[i] - 1]
            fixed_pairs.append(divide(numerator, 2, 'Integral nonnegative fixed unordered pairs'))
        count = whole(sum(Fraction(x, c) for x, c in zip(fixed_pairs, cents)), 'Integral Burnside count')
        ordered = whole(sum(Fraction(x * x, c) for x, c in zip(psi, cents)), 'Integral ordered count')
        square_mean = whole(sum(Fraction(psi[s - 1], c) for s, c in zip(self.square, cents)),
                            'Integral square-map average')
        need(2 * count == ordered - 2 * len(maxima) + square_mean, 'Equivalent count formulas')
        return dict(name=self.name, order=self.order, subgroup_classes=self.n,
                    socle_class=socle + 1, socle_order=self.orders[socle],
                    maximal_classes=[i + 1 for i in maxima],
                    maximal_orders=[self.orders[i] for i in maxima],
                    normalizer_classes=[i + 1 for i in normalizers],
                    normalizer_orders=[self.orders[i] for i in normalizers],
                    characters=characters, total_fixed_points=psi, fixed_unordered_pairs=fixed_pairs,
                    maximal_subgroups=psi[0], subgroup_orbits=len(maxima),
                    ordered_pair_orbits=ordered, square_map_average=square_mean,
                    unordered_pair_orbits=count,
                    equivalence='full automorphism group' if self.name in OUTER or self.name in ['M11', 'M23', 'J1']
                                else 'inner automorphisms only; not the source Table 1 equivalence')

    def product(self, h, k):
        residual = {j: x * self.rows[k][j] for j, x in self.rows[h].items() if j in self.rows[k]}
        coefficients = []
        for i in range(self.n - 1, -1, -1):
            value = residual.get(i, 0)
            if not value:
                continue
            coefficient = divide(value, self.rows[i][i], 'Integral nonnegative row coefficient')
            coefficients.append([i + 1, coefficient])
            for j, mark in self.rows[i].items():
                value = residual.get(j, 0) - coefficient * mark
                need(value >= 0, 'Nonnegative residual mark vector')
                residual[j] = value
        need(not any(residual.values()), 'Exact full row-product decomposition')
        lengths = Counter()
        for position, coefficient in coefficients:
            length = divide(self.orders[h], self.orders[position - 1], 'Suborbit length divisibility')
            lengths[length] += coefficient
        need(sum(length * count for length, count in lengths.items()) == self.order // self.orders[k],
             'Suborbits partition the entire target coset set')
        need(lengths.get(1, 0) == int(h == k), 'Singleton orbit exactly when maximal classes coincide')
        return dict(H_class=h + 1, K_class=k + 1, coefficients=coefficients,
                    lengths=[[n, lengths[n]] for n in sorted(lengths)], number_of_orbits=sum(lengths.values()))

    def suborbits(self):
        maxima = self.maximal_below(self.n - 1)
        need(len(maxima) == len(self.maximal_names), 'All maximal character names match table classes')
        labels = [self.maximal_names[i - 1] for i in self.maximal_permutation]
        characters = [self.character(m) for m in maxima]
        equal_characters = [[i + 1, j + 1] for i in range(len(maxima))
                            for j in range(i + 1, len(maxima)) if characters[i] == characters[j]]
        rows = [[self.product(h, k) for k in maxima] for h in maxima]
        for i, h in enumerate(maxima):
            for j, k in enumerate(maxima):
                need(rows[i][j]['coefficients'] == rows[j][i]['coefficients'], 'Symmetric mark product')
        upper = sum(rows[i][j]['number_of_orbits'] - int(i == j)
                    for i in range(len(maxima)) for j in range(i, len(maxima)))
        return dict(name=self.name, maximal_classes=[m + 1 for m in maxima],
                    maximal_orders=[self.orders[m] for m in maxima],
                    maximal_names_in_Tom_order=labels,
                    equal_maximal_character_positions=equal_characters,
                    source_label_join_accepted=False, full_suborbit_matrix=rows,
                    upper_triangle_without_singletons=upper)

    def M23_label_certificate(self):
        need(self.name == 'M23', 'This structural join is only for M23')
        maxima = self.maximal_below(self.n - 1)
        candidates = [m for m in maxima if self.order // self.orders[m] == 253]
        need(len(candidates) == 2, 'Two maximal classes of degree 253')
        witnesses = []
        for m in candidates:
            for l, mark in self.rows[m].items():
                if self.orders[l] != 16:
                    continue
                normalizer = self.orders[l] * self.rows[l][l]
                number = divide(mark * self.orders[m], normalizer, 'Contained ambient conjugate count')
                cyclic = sorted(set(self.fusion) & set(self.rows[l]))
                if number != 1 or any(self.orders[j] > 2 for j in cyclic):
                    continue
                involutions = sum(divide(v * self.orders[l], self.orders[j] * self.rows[j][j],
                                         'Contained involution subgroup count')
                                  for j, v in self.rows[l].items() if self.orders[j] == 2)
                need(involutions == 15, 'All fifteen nonidentity elements are involutions')
                witnesses.append(dict(maximal_class=m + 1, maximal_order=self.orders[m],
                    normal_class=l + 1, normal_order=self.orders[l], containment_mark=mark,
                    normal_diagonal_mark=self.rows[l][l], ambient_normalizer_order=normalizer,
                    contained_conjugates=number, contained_cyclic_classes=[[j + 1, self.orders[j]] for j in cyclic],
                    involutions=involutions))
        need(len(witnesses) == 1, 'Unique positive elementary-abelian normal certificate')
        normal_class = witnesses[0]['maximal_class']
        other = next(m + 1 for m in candidates if m + 1 != normal_class)
        return dict(witness=witnesses[0], shapes=[dict(Tom_class=normal_class, shape='2^4:A7'),
                                               dict(Tom_class=other, shape='L3(4):2')],
                    borrowed_premise='The two maximal subgroups of index 253 have the classical shapes 2^4:A7 and L3(4):2; L3(4) is nonabelian simple.',
                    deduction='A group L3(4):2 cannot have a normal subgroup of order 16: its intersection with the simple index-two subgroup is trivial, so it injects into C2.')


def parse(raw):
    begin = b'BEGIN_L036_MARK_INPUTS\n'
    end = b'END_L036_MARK_INPUTS\n'
    need(raw.count(begin) == raw.count(end) == 1, 'Unique literal export markers')
    prefix, body = raw.split(begin)
    payload, suffix = body.split(end)
    need(not prefix.strip() and not suffix.strip(), 'No unbound diagnostics around export')
    # GAP prints an interval-valued list as [a .. b]. Expand only this literal
    # notation outside quoted strings; preserve raw output separately.
    pieces = re.split(r'("(?:[^"\\]|\\.)*")', payload.decode('ascii'))
    ranges = []
    def expand(match):
        lower, upper = map(int, match.groups())
        need(1 <= lower <= upper <= 65536, 'Bounded positive GAP interval list')
        values = list(range(lower, upper + 1))
        ranges.append(dict(literal=match.group(0), lower=lower, upper=upper, length=len(values)))
        return json.dumps(values)
    for i in range(0, len(pieces), 2):
        pieces[i] = re.sub(r'\[\s*(\d+)\s*\.\.\s*(\d+)\s*\]', expand, pieces[i])
    data = json.loads(''.join(pieces))
    need(type(data) is list and [row[0] for row in data] == OUTER + SIMPLE, 'Exact eleven-table order')
    return data, ranges


def calculate(data):
    counts = []
    suborbits = []
    structural_labels = []
    for row in data:
        table = MarkData(row)
        counts.append(table.pair_count())
        if table.name in SIMPLE:
            suborbits.append(table.suborbits())
        if table.name == 'M23':
            structural_labels.append(table.M23_label_certificate())
    return dict(status='PASS_L036_MARK_ARITHMETIC', counts=counts, suborbits=suborbits,
                structural_label_certificates=structural_labels,
                scope='Conditional on explicit complete mark tables and compatible named character data.',
                source_table_joins_accepted=False, M11_geometries_accepted=False, whole_source_accepted=False)


def main(args):
    raw = args.input.read_bytes()
    need(len(raw) <= 64 * 2**20 and hashlib.sha256(raw).hexdigest() == args.expected_sha, 'Exact acquired output')
    need(args.out.is_absolute() and not args.out.exists(), 'Fresh absolute result')
    data, ranges = parse(raw)
    result = calculate(data)
    result['literal_GAP_interval_adapter'] = ranges
    result['input_sha256'] = args.expected_sha
    args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(status=result['status'], counts={r['name']: r['unordered_pair_orbits'] for r in result['counts']},
                         source_joins_accepted=False, whole_source_accepted=False)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--expected-sha', required=True)
    parser.add_argument('--out', type=Path, required=True)
    main(parser.parse_args())
