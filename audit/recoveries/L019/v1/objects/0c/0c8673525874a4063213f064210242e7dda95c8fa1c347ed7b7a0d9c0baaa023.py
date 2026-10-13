"""Literal S4 control of interval intersections versus every subset pair."""
import argparse
from functools import lru_cache
import itertools as it
import json
import os
from pathlib import Path
import sys

if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):
    raise RuntimeError('normal Python required')

ID = tuple(range(4))


def product(p, q):
    return tuple(q[p[i]] for i in range(4))


@lru_cache(None)
def generated(gens):
    found = {ID}
    pending = [ID]
    for p in pending:
        for q in gens:
            r = product(p, q)
            if r not in found:
                found.add(r)
                pending.append(r)
    return frozenset(found)


def group(gens):
    return generated(tuple(sorted(set(gens))))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    involutions = [p for p in it.permutations(range(4)) if p != ID and product(p, p) == ID]
    counts = []
    intersections = 0
    for rank in range(1, 5):
        tested = passed = 0
        for gs in it.permutations(involutions, rank):
            if any(product(gs[i], gs[j]) != product(gs[j], gs[i])
                   for i in range(rank) for j in range(i + 2, rank)):
                continue
            tested += 1
            groups = [group(gs[i] for i in range(rank) if mask >> i & 1)
                      for mask in range(1 << rank)]
            full = True
            for left in range(1 << rank):
                for right in range(left + 1):
                    intersections += 1
                    if groups[left] & groups[right] != groups[left & right]:
                        full = False
            interval = True
            for length in range(3, rank + 1):
                for i in range(rank - length + 1):
                    j = i + length
                    if group(gs[i:j - 1]) & group(gs[i + 1:j]) != group(gs[i + 1:j - 1]):
                        interval = False
            if full != interval:
                raise ValueError('interval criterion differs from all subset intersections')
            passed += full
        counts.append({'rank': rank, 'string_tuples': tested, 'C_markings': passed})
    result = {'status': 'PASS', 'involutions': len(involutions), 'counts': counts,
              'literal_subset_intersections': intersections,
              'group_order_bound': 24, 'GAP_imported': False}
    args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
