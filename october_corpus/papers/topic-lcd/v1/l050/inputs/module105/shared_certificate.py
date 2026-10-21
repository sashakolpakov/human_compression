"""Exact shared matrix, orbit and support-refinement routines from the176 packet."""
import collections
import math
import numpy as np
from steiner_construction import need

def rref(rows):
    a = np.array(rows, dtype=np.int64) % 3
    pivots = []
    for j in range(a.shape[1]):
        candidates = np.flatnonzero(a[len(pivots):, j])
        if not len(candidates):
            continue
        i, r = int(candidates[0])+len(pivots), len(pivots)
        a[[i, r]] = a[[r, i]]
        a[r] = a[r]*pow(int(a[r, j]), -1, 3) % 3
        for k in range(len(a)):
            if k != r and a[k, j]:
                a[k] = (a[k]-a[k, j]*a[r]) % 3
        pivots.append(j)
        if len(pivots) == len(a):
            break
    return a[:len(pivots)], pivots


def refine(adj, colors):
    """Same equitable-refinement argument used for the 120-coordinate codes."""
    while True:
        signatures = [(colors[v], tuple(sorted(collections.Counter(colors[w] for w in adj[v]).items())))
                      for v in range(len(adj))]
        labels = {s:i for i,s in enumerate(sorted(set(signatures)))}
        new = [labels[s] for s in signatures]
        if len(labels) == len(set(colors)):
            return new
        colors = new


def refinement_bound(supports, n):
    adj = [[] for _ in range(n+len(supports))]
    for i, support in enumerate(supports):
        for v in support:
            adj[v].append(n+i)
            adj[n+i].append(v)
    colors = [0]*n+[1]*len(supports)
    chain = []
    while True:
        colors = refine(adj, colors)
        cells = collections.defaultdict(list)
        for v in range(n):
            cells[colors[v]].append(v)
        choices = [s for s in cells.values() if len(s)>1]
        if not choices:
            break
        cell = min(choices, key=lambda s:(len(s), s))
        chain.append([cell[0]+1, len(cell)])
        colors[cell[0]] = max(colors)+1
    need(len(set(colors[:n])) == n, 'refinement did not distinguish coordinates')
    return chain, math.prod(size for _, size in chain)


def permute(word, permutation):
    image = bytearray(len(word))
    for i, x in enumerate(word):
        image[permutation[i]] = x
    return bytes(image)


def orbit(seed, generators):
    seen, todo = {seed}, collections.deque([seed])
    while todo:
        word = todo.popleft()
        for g in generators:
            image = permute(word, g)
            if image not in seen:
                seen.add(image)
                todo.append(image)
    return seen


def group_order(generators, n, upper):
    # translate composes byte permutations exactly in C; no external group tool.
    tables = [bytes(g)+bytes(range(n, 256)) for g in generators]
    identity = bytes(range(n))
    seen, todo = {identity}, collections.deque([identity])
    while todo:
        permutation = todo.popleft()
        for table in tables:
            image = permutation.translate(table)
            if image not in seen:
                seen.add(image)
                need(len(seen)<=upper, 'explicit subgroup exceeds proved upper bound')
                todo.append(image)
    return len(seen)


def matrix_algebra(matrices):
    """Close under right multiplication while retaining independent products."""
    d = len(matrices[0])
    products, words, echelon = [], [], []
    def insert(matrix, word):
        row = matrix.reshape(-1).copy() % 3
        for pivot, previous in echelon:
            if row[pivot]:
                row = (row-row[pivot]*previous) % 3
        nonzero = np.flatnonzero(row)
        if not len(nonzero):
            return False
        pivot = int(nonzero[0])
        row = row*pow(int(row[pivot]), -1, 3) % 3
        echelon.append((pivot, row))
        echelon.sort(key=lambda pair:pair[0])
        products.append(matrix)
        words.append(word)
        return True
    insert(np.eye(d, dtype=np.int64), [])
    cursor = 0
    while cursor<len(products) and len(products)<d*d:
        matrix, word = products[cursor], words[cursor]
        for i, generator in enumerate(matrices):
            insert(matrix@generator % 3, word+[i+1])
            if len(products)==d*d:
                break
        cursor += 1
    # Reevaluate every retained word and independently eliminate their rows.
    for word, matrix in zip(words, products):
        actual = np.eye(d, dtype=np.int64)
        for i in word:
            actual = actual@matrices[i-1] % 3
        need(np.array_equal(actual, matrix), 'matrix word witness')
    reduced, _ = rref([matrix.reshape(-1) for matrix in products])
    need(len(reduced)==len(products), 'matrix product independence')
    return products, words


