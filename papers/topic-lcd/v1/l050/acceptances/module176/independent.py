#!/usr/bin/env python3
"""Independent minimum-word orbit, matrix witnesses and partition refinement."""
import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
import numpy as np


def require(test, message):
    if not test:
        raise ValueError(message)


def rank(rows):
    pivots = {}
    for incoming in rows:
        v = [int(x) % 3 for x in incoming]
        for j, row in sorted(pivots.items()):
            c = v[j]
            if c:
                v = [(x-c*y) % 3 for x, y in zip(v, row)]
        if any(v):
            j = next(j for j, x in enumerate(v) if x)
            pivots[j] = [x*(1 if v[j] == 1 else 2) % 3 for x in v]
    return len(pivots)


def refine(neighbors, cells):
    while True:
        new = []
        for cell in cells:
            groups = defaultdict(set)
            for v in cell:
                groups[tuple(len(neighbors[v] & target) for target in cells)].add(v)
            new.extend(groups.values())
        if len(new) == len(cells):
            return new
        cells = new


def run(packet, replay):
    data = json.loads((packet/'module_data.json').read_text())
    lines = (packet/'retained/176_basis.txt').read_text().splitlines()
    require(lines[0] == '176 21', 'exact dimensions')
    basis = [[int(c) for c in line] for line in lines[1:]]
    pivots = [next(j for j, x in enumerate(row) if x) for row in basis]
    require(rank(basis) == 21 and all(row[j] == int(i == k)
            for i, row in enumerate(basis) for k, j in enumerate(pivots)), 'systematic basis')
    generators = [[x-1 for x in row] for row in data['coordinate_generators']]
    def act(w, g):
        result = [0]*176
        for i, x in enumerate(w):
            result[g[i]] = x
        return tuple(result)
    matrices = []
    for g in generators:
        images = [act(row, g) for row in basis]
        M = [[row[j] for j in pivots] for row in images]
        require(np.array_equal(np.array(M) @ basis % 3, images), 'matrix on actual code')
        matrices.append(np.array(M, dtype=np.int64))
    wordlist = json.loads((replay/'algebra_words.json').read_text())
    flattened = []
    for word in wordlist:
        M = np.eye(21, dtype=np.int64)
        for letter in word:
            M = M @ matrices[letter-1] % 3
        flattened.append(M.reshape(-1))
    require(len(flattened) == 441 and rank(flattened) == 441, 'independent matrix words')
    seed = tuple(data['minimum_seed'])
    seen, queue = {seed}, [seed]
    for word in queue:
        for g in generators:
            image = act(word, g)
            if image not in seen:
                seen.add(image)
                queue.append(image)
    opposite = {tuple(-x % 3 for x in word) for word in seen}
    require(len(seen) == 462 and seen.isdisjoint(opposite), 'two scalar orbits')
    allwords = seen | opposite
    require(all(sum(x != 0 for x in w) == 56 for w in allwords), 'constant minimum weight')
    supports = {frozenset(i for i, x in enumerate(w) if x) for w in allwords}
    old = {frozenset(x-1 for x in s) for s in json.loads((replay/'supports.json').read_text())}
    require(len(supports) == 462 and supports == old, 'all support data independently reconstructed')
    neighbors = [set() for _ in range(638)]
    for i, support in enumerate(sorted(supports, key=lambda s: tuple(sorted(s)))):
        for v in support:
            neighbors[v].add(176+i)
            neighbors[176+i].add(v)
    cells = [set(range(176)), set(range(176,638))]
    sizes = []
    for chosen in [1,5,29,61,2]:
        cells = refine(neighbors, cells)
        selected = next(cell for cell in cells if chosen-1 in cell)
        sizes.append(len(selected))
        cells = [cell for cell in cells if cell is not selected] + [{chosen-1}, selected-{chosen-1}]
    cells = refine(neighbors, cells)
    require(sizes == [176,70,6,2,3] and all(len(c) == 1 for c in cells), 'independent group upper bound')
    return dict(status='PASS',author_implementation_imported=False,matrix_word_rank=441,
                positive_orbit=462,negative_orbit=462,minimum_supports=462,
                stabilizer_bounds=sizes,automorphism_upper=math.prod(sizes),
                exhaustive_minimum_count_premise='Previously accepted complete enumeration; not rerun.')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--packet', type=Path, required=True)
    p.add_argument('--replay', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    result = run(a.packet, a.replay)
    require(not a.out.exists(), 'fresh report')
    a.out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))
