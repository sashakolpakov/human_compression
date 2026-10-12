#!/usr/bin/env python3
"""Finite augmentation-module certificate; completed enumerations are inputs."""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from steiner_construction import steiner_blocks, need


def rref(rows):
    a = np.array(rows, dtype=np.int64) % 3
    pivots = []
    for j in range(a.shape[1]):
        nz = np.flatnonzero(a[len(pivots):, j])
        if not len(nz):
            continue
        r, i = len(pivots), len(pivots) + int(nz[0])
        a[[r, i]] = a[[i, r]]
        a[r] = a[r] * pow(int(a[r, j]), -1, 3) % 3
        for k in range(len(a)):
            if k != r and a[k, j]:
                a[k] = (a[k] - a[k, j] * a[r]) % 3
        pivots.append(j)
        if len(pivots) == len(a):
            break
    return a[:len(pivots)], pivots


def algebra_words(matrices):
    """Retain explicit independent products until the whole algebra is spanned."""
    d = len(matrices[0])
    products, words, echelon = [], [], []
    def insert(matrix, word):
        row = matrix.reshape(-1).copy()
        for pivot, earlier in echelon:
            row = (row - row[pivot] * earlier) % 3
        nz = np.flatnonzero(row)
        if not len(nz):
            return
        pivot = int(nz[0])
        row = row * pow(int(row[pivot]), -1, 3) % 3
        echelon.append((pivot, row))
        echelon.sort(key=lambda pair: pair[0])
        products.append(matrix)
        words.append(word)
    insert(np.eye(d, dtype=np.int64), [])
    cursor = 0
    while cursor < len(products) and len(products) < d*d:
        for i, g in enumerate(matrices):
            insert(products[cursor] @ g % 3, words[cursor] + [i])
            if len(products) == d*d:
                break
        cursor += 1
    # Check the words as products again, using an independent full row reduction.
    rebuilt = []
    for word in words:
        x = np.eye(d, dtype=np.int64)
        for i in word:
            x = x @ matrices[i] % 3
        rebuilt.append(x.reshape(-1))
    need(len(rref(rebuilt)[0]) == d*d, 'full matrix-algebra witness')
    return words


def incidence_bound(blocks):
    """Bound the point automorphisms by invariant color refinement."""
    adj = [[] for _ in range(23 + len(blocks))]
    for b, mask in enumerate(blocks):
        for i in range(23):
            if mask >> i & 1:
                adj[i].append(23+b)
                adj[23+b].append(i)
    colors = [0]*23 + [1]*len(blocks)
    chain = []
    while True:
        while True:
            signatures = [(colors[i], tuple(sorted(Counter(colors[j] for j in row).items())))
                          for i, row in enumerate(adj)]
            table = {x: i for i, x in enumerate(sorted(set(signatures)))}
            new = [table[x] for x in signatures]
            stable = len(set(new)) == len(set(colors))
            colors = new
            if stable:
                break
        cells = {}
        for i in range(23):
            cells.setdefault(colors[i], []).append(i)
        choices = [x for x in cells.values() if len(x) > 1]
        if not choices:
            break
        cell = min(choices, key=lambda x: (-len(x), x))
        chain.append([cell[0]+1, len(cell)])
        colors[cell[0]] = max(colors)+1
    need(len(set(colors[:23])) == 23, 'pointwise terminal stabilizer')
    return chain, math.prod(size for _, size in chain)


def macwilliams(counts, n, k):
    need(len(counts) == n+1 and all(type(x) is int and x >= 0 for x in counts)
         and counts[0] == 1 and sum(counts) == 3**k, 'whole weight distribution')
    result = []
    for j in range(n+1):
        numerator = sum(c * sum((-1)**s * 2**(j-s) * math.comb(i, s)
                               * math.comb(n-i, j-s)
                               for s in range(max(0, j-n+i), min(j, i)+1))
                        for i, c in enumerate(counts) if c)
        need(numerator >= 0 and numerator % 3**k == 0, 'MacWilliams coefficient')
        result.append(numerator // 3**k)
    need(sum(result) == 3**(n-k), 'dual distribution size')
    return result


def run(packet, retained, out):
    need(not out.exists(), 'fresh output directory')
    out.mkdir(parents=True)
    blocks, _ = steiner_blocks()
    H = np.array([[(b >> i) & 1 for b in blocks] for i in range(23)], dtype=np.int64)
    need(np.array_equal(H @ H.T, 56*np.eye(23, dtype=np.int64)
                        + 21*np.ones((23, 23), dtype=np.int64)), 'integer incidence Gram')
    A = np.array([[int(x != y and (x & y).bit_count() == 3)
                   for y in blocks] for x in blocks], dtype=np.int64)
    need(np.array_equal(A % 3, (np.ones((253, 253), dtype=np.int64) - H.T @ H) % 3),
         'adjacency incidence identity')
    augmentation = (H[:-1] - H[-1]) % 3
    C, _ = rref(A)
    D, _ = rref(augmentation)
    need(len(C) == 23 and len(D) == 22, 'code dimensions')
    need(len(rref(D @ D.T)[0]) == 22 and not np.any(D.sum(axis=1) % 3),
         'nondegenerate augmentation orthogonal to constants')
    weights = {}
    for name, basis, d, minimum, multiplicity in [
            ('253_adjacency', C, 23, 77, 46), ('253_differences', D, 22, 97, 3542)]:
        literal = f'253 {d}\n' + ''.join(''.join(map(str, row))+'\n' for row in basis.tolist())
        need(literal.encode() == (retained/'bases'/f'{name}.txt').read_bytes(), 'exact enumerated basis')
        record = json.loads((retained/f'{name}.json').read_text())
        need(record['length'] == 253 and record['basis_rows'] == d
             and record['coefficient_vectors'] == 3**d, 'enumeration domain')
        counts = record['weight_counts']
        dual = macwilliams(counts, 253, d)
        need(next(i for i in range(1, 254) if counts[i]) == minimum
             and counts[minimum] == multiplicity, 'retained minimum words')
        need(not any(dual[1:6]) and dual[6] == 850080, 'dual distance and multiplicity')
        weights[name] = dict(dimension=d, distance=minimum, minimum_words=multiplicity,
                             dual_dimension=253-d, dual_distance=6, dual_minimum_words=850080)
        (out/f'{name}_dual.json').write_text(json.dumps(dual)+'\n')
    point_generators = json.loads((packet/'generators.json').read_text())
    need(point_generators and all(sorted(g) == list(range(1,24)) for g in point_generators),
         'literal point permutations')
    index = {b: i for i, b in enumerate(blocks)}
    matrices, coordinate_generators = [], []
    for row in point_generators:
        g = [x-1 for x in row]
        images = [sum(1 << g[i] for i in range(23) if b >> i & 1) for b in blocks]
        need(set(images) == set(blocks), 'Steiner design automorphism')
        perm = [index[b] for b in images]
        M = np.array([[int(j == g[i])-int(j == g[22]) for j in range(22)]
                      for i in range(22)], dtype=np.int64) % 3
        image = np.zeros_like(augmentation)
        image[:, perm] = augmentation
        need(np.array_equal(M @ augmentation % 3, image), 'equivariant augmentation transfer')
        matrices.append(M)
        coordinate_generators.append([x+1 for x in perm])
    words = algebra_words(matrices)
    chain, upper = incidence_bound(blocks)
    need(chain == [[1,23],[2,22],[3,21],[4,20],[5,16],[6,3]]
         and upper == 10200960, 'exact full design automorphism bound')
    # All minimum supports are precisely the 23 independent incidence rows.
    need(len({tuple(row) for row in H.tolist()}) == 23
         and all(np.count_nonzero(row) == 77 for row in H), 'point minimum supports')
    (out/'algebra_words.json').write_text(json.dumps(words)+'\n')
    (out/'constructed.g').write_text('point_generators:='+str(point_generators)+';;\n'
        +'coordinate_generators:='+str(coordinate_generators)+';;\n'
        +'module_matrices:='+str([M.tolist() for M in matrices])+';;\n'
        +'proved_upper:='+str(upper)+';;\n')
    report = dict(status='PASS_FINITE_MODULE_AND_INCIDENCE_CERTIFICATE',
                  matrix_algebra_dimension=len(words), largest_word_length=max(map(len, words)),
                  refinement_chain=chain, design_automorphism_upper=upper, weights=weights,
                  group_lower_and_name='separate identify.g check required',
                  enumeration_rerun=False, no_Lean_claim=True)
    (out/'report.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--retained', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    print(json.dumps(run(Path(__file__).resolve().parent, a.retained, a.out)))
