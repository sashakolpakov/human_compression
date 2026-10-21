"""Exact finite checks for the eleven drawings in L019, Proposition 2.5.

The direct permutation enumeration does not use GAP's subgroup algorithms.
It enumerates the two end groups and their literal intersection; for graph
(9) it also checks all 256 pairs of label subsets. No degree/rank census is
claimed. The uniform central-extension conclusion is a separate proof.
"""
from pathlib import Path
import argparse
import collections
import hashlib
import json
import sys

if sys.flags.optimize:
    raise RuntimeError('optimized Python is unsupported')

def need(ok, message):
    if not ok:
        raise ValueError(message)

def multiply(a, b):
    return tuple(b[x] for x in a)

def generated(generators, n, cap=11000):
    identity = tuple(range(n))
    seen = {identity}
    queue = collections.deque([identity])
    while queue:
        element = queue.popleft()
        for mark in generators:
            product = multiply(element, mark)
            if product not in seen:
                seen.add(product)
                need(len(seen) <= cap, 'declared finite enumeration cap exceeded')
                queue.append(product)
    # Every retained element is an explicit product of the input marks.
    # Exhaustion of this queue certifies closure under right multiplication.
    return seen

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=Path, default=Path(__file__).with_name('graphs.json'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    need(not args.output.exists(), 'refuse to replace a replay')
    rows = json.loads(args.data.read_text())
    expected = {
        '1': [4320,10080,240,20,12], '2': [2880,10080,144,24,6],
        '3': [720,720,120,10,12], '4': [4320,10080,240,20,12],
        '5a': [10080,10080,480,20,24], '5b': [10080,10080,240,20,12],
        '6a': [5040,1440,240,20,12], '6b': [5040,1440,120,20,6],
        '7': [5040,720,144,24,6], '8': [5040,720,144,24,6],
        '9': [60,720,10,10,1],
    }
    need(len(rows) == len(expected) and {x['source_graph'] for x in rows} == set(expected),
         'exact source drawings')
    report = []
    for row in rows:
        tag, n = row['source_graph'], row['degree']
        need(type(n) is int and 7 <= n <= 11, 'degree')
        identity, marks = tuple(range(n)), []
        need(len(row['transpositions']) == 4, 'rank four')
        for edges in row['transpositions']:
            used, perm = set(), list(identity)
            need(edges, 'nonidentity mark')
            for pair in edges:
                need(len(pair) == 2 and all(type(x) is int for x in pair), 'edge syntax')
                a,b = pair
                need(1 <= a < b <= n and a not in used and b not in used, 'matching edge')
                used.update(pair)
                perm[a-1],perm[b-1] = b-1,a-1
            marks.append(tuple(perm))
        need(len(set(marks)) == 4 and all(multiply(s,s) == identity for s in marks), 'involutions')
        need(all(multiply(marks[i],marks[j]) == multiply(marks[j],marks[i])
                 for i in range(4) for j in range(i+2,4)), 'string commutations')
        left = generated(marks[1:], n)
        right = generated(marks[:-1], n)
        middle = generated(marks[1:3], n)
        intersection = left & right
        need(middle <= intersection and len(intersection) % len(middle) == 0, 'middle inclusion')
        values = [len(left),len(right),len(intersection),len(middle),len(intersection)//len(middle)]
        need(values == expected[tag], 'exact finite orders '+tag)
        result = {'source_graph': tag, 'degree': n, 'end_orders': values[:2],
                  'intersection_order': values[2], 'middle_order': values[3],
                  'intersection_index': values[4]}
        if tag != '9':
            need(values[4] % 3 == 0, 'odd prime obstruction')
            result['central_2_extension_obstruction'] = True
        else:
            groups = [generated([marks[i] for i in range(4) if mask & (1 << i)], n)
                      for mask in range(16)]
            need(len(groups[15]) == 5040, 'full symmetric group of degree seven')
            need(all(groups[a] & groups[b] == groups[a & b]
                     for a in range(16) for b in range(16)), 'all 256 subset intersections')
            product_orders = [len(generated([multiply(marks[i], marks[i+1])], n))
                              for i in range(3)]
            need(product_orders == [6,5,5], 'adjacent product orders')
            result.update(full_group_order=5040, all_subset_pairs=256,
                          adjacent_product_orders=product_orders, intersection_property=True,
                          central_2_extension_obstruction=False)
        report.append(result)
    data = {'status': 'PASS_TEN_EXCLUSIONS_AND_ONE_POSITIVE_SOURCE_CORRECTION',
            'method': 'exhaustive right-product closure in literal permutation tuples',
            'data_sha256': hashlib.sha256(args.data.read_bytes()).hexdigest(),
            'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'whole_original_credit': 0, 'main_stability_claim': 'pending', 'graphs': report}
    args.output.write_text(json.dumps(data, indent=2)+'\n')
    print('PASS_TEN_EXCLUSIONS_AND_ONE_POSITIVE_SOURCE_CORRECTION')

if __name__ == '__main__':
    main()
