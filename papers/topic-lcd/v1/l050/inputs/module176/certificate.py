#!/usr/bin/env python3
"""Exact module and complete minimum-support automorphism certificate.

The minimum count is retained from the separately completed enumeration.
This checker never enumerates the 3^21 codewords and has no graph-isomorphism
backend. The Steiner construction is the exact shared 120/176/253 input.
"""
import argparse
import collections
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from steiner_construction import steiner_blocks, need, srg_check


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


def dual_distribution(enum):
    """The same classical MacWilliams calculation as for N and K."""
    n, k, counts = 176, 21, enum['weight_counts']
    need(enum['coefficient_vectors']==3**k and len(counts)==n+1 and counts[0]==1
         and all(isinstance(c,int) and c>=0 for c in counts) and sum(counts)==3**k,
         'complete retained weight distribution')
    dual=[]
    for j in range(n+1):
        numerator = sum(c*sum((-1)**s*2**(j-s)*math.comb(i,s)*math.comb(n-i,j-s)
                             for s in range(max(0,j-n+i),min(i,j)+1))
                        for i,c in enumerate(counts) if c)
        need(numerator>=0 and numerator % (3**k)==0, 'MacWilliams coefficient')
        dual.append(numerator//(3**k))
    need(dual[0]==1 and sum(dual)==3**155 and not any(dual[1:6])
         and dual[6]==184800, 'complete dual weight distribution')
    return dual


def inspect(data, basis_path, enumeration_path, out, compute_group=True):
    out.mkdir(parents=True, exist_ok=False)
    blocks, _ = steiner_blocks()
    blocks = [b for b in blocks if b&1==0]
    need(len(blocks)==176, 'residual vertex count')
    adjacency = [[int(x!=y and (x&y).bit_count()!=1) for y in blocks] for x in blocks]
    srg_check(adjacency, (176, 105, 68, 54))
    H = np.array([[(b>>i)&1 for b in blocks] for i in range(1,23)], dtype=np.int64)
    gram = H@H.T
    need(np.array_equal(gram, 40*np.eye(22, dtype=np.int64)+16*np.ones((22,22), dtype=np.int64)), 'integer incidence Gram')
    need(np.array_equal(H.T@(np.ones((22,22), dtype=np.int64)-np.eye(22, dtype=np.int64))@H % 3,
                        np.array(adjacency)%3), 'adjacency incidence factorization')
    basis, pivots = rref(adjacency)
    augmentation, _ = rref(H[:-1]-H[-1])
    need(len(basis)==21 and np.array_equal(basis, augmentation), 'augmentation image')
    need(len({tuple(column) for column in basis.T.tolist()})==176, 'distinct code columns')
    need(len(rref(basis@basis.T)[0])==21, 'LCD Gram rank')
    need(not np.any(basis.sum(axis=1)%3), 'all-ones vector is orthogonal')
    literal = '176 21\n'+''.join(''.join(map(str,row))+'\n' for row in basis.tolist())
    need(literal.encode()==basis_path.read_bytes(), 'exact previously enumerated basis')
    enum = json.loads(enumeration_path.read_text())
    need(enum['length']==176 and enum['basis_rows']==21 and next(i for i,c in enumerate(enum['weight_counts']) if i and c)==56, 'retained enumeration dimensions/distance')
    need(enum['weight_counts'][56]==924, 'retained exact minimum-word count')
    dual = dual_distribution(enum)
    generators = [[x-1 for x in row] for row in data['coordinate_generators']]
    need(len(generators)==2 and all(sorted(g)==list(range(176)) for g in generators), 'literal permutations')
    matrices, natural = [], []
    hrows = {bytes(row.tolist()):i for i,row in enumerate(H)}
    for g in generators:
        need(all(adjacency[g[i]][g[j]]==adjacency[i][j] for i in range(176) for j in range(i)), 'graph automorphism')
        image = np.array([list(permute(bytes(row.tolist()),g)) for row in basis], dtype=np.int64)
        matrix = image[:,pivots]
        need(np.array_equal(matrix@basis % 3,image), 'code module invariance')
        matrices.append(matrix)
        point_action = [hrows.get(permute(bytes(row.tolist()),g)) for row in H]
        need(None not in point_action and sorted(point_action)==list(range(22)), 'point action')
        natural.append([x+1 for x in point_action])
    seed = bytes(data['minimum_seed'])
    need(len(seed)==176 and sum(x!=0 for x in seed)==56, 'minimum seed weight')
    seed_vector = np.frombuffer(seed,dtype=np.uint8).astype(np.int64)
    need(np.array_equal(seed_vector[pivots]@basis % 3,seed_vector), 'seed membership')
    positive = orbit(seed, generators)
    negative = {bytes((-x)%3 for x in word) for word in positive}
    need(len(positive)==462 and positive.isdisjoint(negative), 'two disjoint scalar orbits')
    words = positive|negative
    need(len(words)==enum['weight_counts'][56] and all(sum(x!=0 for x in w)==56 for w in words), 'complete minimum words')
    supports = sorted({tuple(i for i,x in enumerate(w) if x) for w in words})
    need(len(supports)==462, 'minimum support count')
    chain, upper = refinement_bound(supports,176)
    need(chain==[[1,176],[5,70],[29,6],[61,2],[2,3]] and upper==443520, 'full support automorphism bound')
    lower = group_order(generators,176,upper) if compute_group else None
    need(not compute_group or lower==upper, 'explicit group attains bound')
    products, algebra_words = matrix_algebra(matrices)
    need(len(products)==441, 'full matrix algebra')
    out.joinpath('supports.json').write_text(json.dumps([[v+1 for v in s] for s in supports],separators=(',',':'))+'\n')
    out.joinpath('algebra_words.json').write_text(json.dumps(algebra_words,separators=(',',':'))+'\n')
    out.joinpath('dual_weights.json').write_text(json.dumps(dual,separators=(',',':'))+'\n')
    out.joinpath('constructed.g').write_text('coordinate_generators:='+repr(data['coordinate_generators'])+';;\npoint_generators:='+repr(natural)+';;\nmodule_matrices:='+repr([m.tolist() for m in matrices])+';;\n')
    result = {'status':'PASS','graph_parameters':[176,105,68,54], 'dimension':21,
              'LCD':True,'all_ones_in_dual':True,'exact_enumerated_basis_sha256':hashlib.sha256(literal.encode()).hexdigest(),
              'retained_distance':56,'retained_minimum_word_count':924,'one_orbit':462,
              'dual_dimension':155,'dual_distance':6,'dual_minimum_word_count':184800,
              'opposite_orbit_disjoint':True,'minimum_supports':462,'refinement_chain':chain,
              'full_automorphism_upper_bound':upper,'explicit_group_order':lower,
              'generated_matrix_algebra_dimension':len(products), 'matrix_word_maximum_length':max(map(len,algebra_words)),
              'no_graph_isomorphism_backend':True,'no_full_codeword_reenumeration':True}
    out.joinpath('report.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--enumeration-dir',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    print(json.dumps(inspect(json.loads(Path(__file__).with_name('module_data.json').read_text()),
          a.enumeration_dir/'bases/176_adjacency.txt',a.enumeration_dir/'176_adjacency.json',a.out),sort_keys=True))


if __name__=='__main__':
    main()
