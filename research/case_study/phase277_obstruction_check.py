#!/usr/bin/env python3
"""Literal finite check of the separated-parabolic obstruction example.

This verifies the order-64 marking and its order-128 C-cover.  The theorem
that every cover has even kernel is the written divisibility argument.
"""
import argparse
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def mul_g(x, y):
    # Bits 0,1,2,3 are the four reflection coordinates; bit 4 is
    # the common central coordinate; bit 5 is the independent middle mark.
    cocycle = (((x >> 1) & 1) & (y & 1)) ^ (((x >> 3) & 1) & ((y >> 2) & 1))
    return x ^ y ^ (cocycle << 4)


def mul_r(x, y):
    # The two central coordinates occupy bits 4 and 5; the middle mark is bit 6.
    left = ((x >> 1) & 1) & (y & 1)
    right = ((x >> 3) & 1) & ((y >> 2) & 1)
    return x ^ y ^ (left << 4) ^ (right << 5)


def projection(x):
    return (x & 15) | ((((x >> 4) ^ (x >> 5)) & 1) << 4) | (((x >> 6) & 1) << 5)


def group_check(size, mul):
    table = [[mul(x, y) for y in range(size)] for x in range(size)]
    require(all(table[0][x] == x == table[x][0] for x in range(size)), 'identity')
    require(all(0 in table[x] for x in range(size)), 'inverses')
    require(all(table[table[x][y]][z] == table[x][table[y][z]]
                for x in range(size) for y in range(size) for z in range(size)), 'associativity')
    return table


def parabolics(table, marks):
    result = []
    for mask in range(32):
        generators = [s for i, s in enumerate(marks) if mask & (1 << i)]
        seen, queue = {0}, [0]
        for x in queue:
            for s in generators:
                y = table[x][s]
                if y not in seen:
                    seen.add(y)
                    queue.append(y)
        result.append(seen)
    return result


def run(remove_identification=False):
    tg, tr = group_check(64, mul_g), group_check(128, mul_r)
    mg, mr = [1, 2, 32, 4, 8], [1, 2, 64, 4, 8]
    for table, marks in [(tg, mg), (tr, mr)]:
        require(len(set(marks)) == 5 and 0 not in marks, 'distinct nonidentity marks')
        require(all(table[s][s] == 0 for s in marks), 'involutions')
        require(all(table[marks[i]][marks[j]] == table[marks[j]][marks[i]]
                    for i in range(5) for j in range(i + 2, 5)), 'string commutations')
    pg, pr = parabolics(tg, mg), parabolics(tr, mr)
    require(len(pg[31]) == 64 and len(pr[31]) == 128, 'generated groups')
    require(all(mg[i] not in pg[31 ^ (1 << i)] for i in range(5)), 'independence')
    require(all(projection(tr[x][y]) == tg[projection(x)][projection(y)]
                for x in range(128) for y in range(128)), 'quotient homomorphism')
    require([projection(x) for x in mr] == mg, 'marked quotient')
    kernel = [x for x in range(128) if projection(x) == 0]
    require(kernel == [0, 48], 'central kernel of order two')
    require(all(pr[i] & pr[j] == pr[i & j] for i in range(32) for j in range(32)), 'cover IP')
    for end in [15, 30]:
        masks = [i for i in range(32) if i & end == i]
        require(len(pg[end]) == 32, 'end order')
        require(all(pg[i] & pg[j] == pg[i & j] for i in masks for j in masks), 'end IP')
    separated = pg[3] & pg[24]
    if remove_identification:
        separated = pr[3] & pr[24]
    require(separated == {0, 16}, 'nontrivial separated intersection')
    failures = [[i, j, len(pg[i] & pg[j]), len(pg[i & j])]
                for i in range(32) for j in range(32) if pg[i] & pg[j] != pg[i & j]]
    return {'status': 'PASS', 'base_order': 64, 'cover_order': 128,
            'kernel': kernel, 'base_marks': mg, 'cover_marks': mr,
            'base_parabolic_orders': [len(x) for x in pg],
            'cover_parabolic_orders': [len(x) for x in pr],
            'separated_intersection': sorted(separated),
            'base_IP_failures': failures, 'cover_IP_pairs_checked': 1024,
            'end_IP_pairs_checked': 512, 'associativity_triples_checked': 64**3 + 128**3,
            'scope': 'A non-polytopal independent marking, not a counterexample to the polytope conjecture. No assertion that its displayed cover is the only minimal cover.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--remove-identification', action='store_true')
    args = parser.parse_args()
    report = run(args.remove_identification)
    args.out.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ['status', 'base_order', 'cover_order',
                                           'separated_intersection', 'cover_IP_pairs_checked']}))
