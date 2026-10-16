"""Separate coordinate representation for the order-four subgroup example."""
import json
from itertools import product, combinations

G = list(product(range(2), repeat=2))
zero = (0, 0)


def add(x, y):
    return tuple((a + b) % 2 for a, b in zip(x, y))


def main():
    subgroups = [frozenset(c) for n in range(1, 5) for c in combinations(G, n)
                 if zero in c and all(add(x, y) in c for x in c for y in c)]
    maximals = [h for h in subgroups if len(h) == 2]
    if len(subgroups) != 5 or len(maximals) != 3:
        raise ValueError('complete four-element subgroup census')
    pairs = [(h, k) for h, k in product(maximals, repeat=2) if h != k]
    if len(pairs) != 6 or any({add(x, y) for x in h for y in k} != set(G) for h, k in pairs):
        raise ValueError('all distinct maximal pairs generate the whole group')
    print(json.dumps(dict(group='binary coordinate pairs', all_subgroups=5,
                          maximal_proper_subgroups=3, distinct_ordered_pairs=6,
                          all_products_whole=True), indent=2))


if __name__ == '__main__':
    main()
