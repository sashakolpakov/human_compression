#!/usr/bin/env python3
"""Independent finite-incidence validation; no group order oracle is implemented."""
import argparse
import copy
from collections import Counter
from itertools import combinations, product
import json
from math import comb
from pathlib import Path


def require(test, message):
    if not test:
        raise ValueError(message)


def mul4(a, b):
    """Coefficient bits in F2[z]/(z*z+z+1): 0,1,z,z+1."""
    c0 = (a & 1) * (b & 1)
    c1 = ((a & 1) * (b >> 1)) ^ ((a >> 1) * (b & 1))
    c2 = (a >> 1) * (b >> 1)
    return (c0 ^ c2) | ((c1 ^ c2) << 1)


def dot4(a, b):
    return mul4(a[0], b[0]) ^ mul4(a[1], b[1]) ^ mul4(a[2], b[2])


def canonical4(a):
    first = next(x for x in a if x)
    inverse = next(x for x in range(1, 4) if mul4(first, x) == 1)
    return tuple(mul4(x, inverse) for x in a)


def validate(data):
    require(data['field_polynomial'] == 'z^2+z+1', 'field polynomial')
    vectors = [tuple(v) for v in data['plane_vectors']]
    expected_vectors = {canonical4(v) for v in product(range(4), repeat=3) if any(v)}
    require(len(vectors) == 21 and set(vectors) == expected_vectors, 'projective points')
    target = {tuple(i + 1 for i, v in enumerate(vectors) if dot4(n, v) == 0)
              for n in vectors}
    require(len(target) == 21 and {len(b) for b in target} == {5}, 'coordinate lines')
    require(target == {tuple(b) for b in data['plane_blocks']}, 'GAP coordinate plane')
    reports = []
    require([c['v'] for c in data['cases']] == [11, 12, 22, 23, 24], 'case completeness')
    for case in data['cases']:
        v, t, k = case['v'], case['t'], case['k']
        expected = {11:(4,5), 12:(5,6), 22:(3,6), 23:(4,7), 24:(5,8)}[v]
        require((t, k) == expected, 'design parameters')
        blocks = [tuple(b) for b in case['blocks']]
        require(len(blocks) == len(set(blocks)) == comb(v,t)//comb(k,t), 'block count')
        require(all(len(b) == k and tuple(sorted(set(b))) == b and
                    all(1 <= x <= v for x in b) for b in blocks), 'invalid block')
        counts = Counter(s for b in blocks for s in combinations(b, t))
        require(len(counts) == comb(v,t) and set(counts.values()) == {1}, 'Steiner property')
        for key in ('native_generators', 'full_generators'):
            for g in case[key]:
                require(sorted(g) == list(range(1,v+1)), 'not a permutation')
                require({tuple(sorted(g[x-1] for x in b)) for b in blocks} == set(blocks),
                        'group generator violates design')
        # Reported orders depend on the GAP group and DESIGN/GRAPE calculations;
        # comparing the numbers here is only a schema/claim check.
        native = {11:7920,12:95040,22:443520,23:10200960,24:244823040}[v]
        require(case['native_order'] == native, 'native group order claim')
        require(case['full_order'] == native * (2 if v == 22 else 1), 'full order claim')
        if v > 20:
            removed = list(range(1,t-1))
            remaining = list(range(t-1,v+1))
            require(case['derived_at'] == removed and case['remaining_points'] == remaining,
                    'derived point convention')
            derived = {tuple(remaining.index(x)+1 for x in b if x not in removed)
                       for b in blocks if set(removed) <= set(b)}
            require(derived == {tuple(b) for b in case['derived_blocks']}, 'derived blocks')
            p = case['point_map']
            require(sorted(p) == list(range(1,22)), 'derived point map')
            mapped = {tuple(sorted(p[x-1] for x in b)) for b in derived}
            require(mapped == target, 'derived map does not preserve coordinate incidence')
            for b in derived:
                line = tuple(sorted(p[x-1] for x in b))
                for point in range(1,22):
                    require((point in b) == (p[point-1] in line), 'incidence iff')
        reports.append({'v':v,'blocks':len(blocks),'Steiner_subsets':len(counts),
                        'coordinate_incidence_pairs':441 if v>20 else 0})
    return reports


def negative_controls(data):
    bad_block = copy.deepcopy(data)
    b = bad_block['cases'][0]['blocks'][0]
    b[-1] = next(x for x in range(1,12) if x not in b)
    b.sort()
    bad_map = copy.deepcopy(data)
    p = bad_map['cases'][2]['point_map']
    p[0], p[1] = p[1], p[0]
    results = []
    for label, corrupted in [('alter_one_Witt_block',bad_block),
                             ('swap_two_derived_images',bad_map)]:
        try:
            validate(corrupted)
        except ValueError as error:
            results.append({'control':label,'status':'REJECTED','reason':str(error)})
        else:
            raise ValueError('negative control accepted: ' + label)
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('witness', type=Path)
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    data = json.loads(args.witness.read_text())
    result = {'status':'PASS','cases':validate(data),'negative_controls':negative_controls(data),
              'scope':'Finite incidence arithmetic and generator preservation. Full automorphism completeness and group orders remain GAP/DESIGN/GRAPE computations; no Lean certificate.'}
    text = json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.write_text(text)
    print(text,end='')


if __name__ == '__main__':
    main()
