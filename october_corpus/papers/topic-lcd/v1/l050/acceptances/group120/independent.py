#!/usr/bin/env python3
"""Distinct finite checks. No imports from the author or retained constructors."""
import argparse
import hashlib
import itertools
import json
import math
from pathlib import Path
import subprocess
import numpy as np

AUTHOR_SHA = '49dcf03d9f7deb92478705439c02b4448832a3f00d41e67f84ef89dddf795eaa'

def need(condition, message):
    if not condition:
        raise ValueError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rank(rows, prime=3):
    a = np.array(rows, dtype=np.int64).copy() % prime
    pivot = 0
    for col in range(a.shape[1]):
        candidates = np.flatnonzero(a[pivot:, col])
        if not len(candidates):
            continue
        other = pivot + int(candidates[0])
        a[[pivot, other]] = a[[other, pivot]]
        a[pivot] = a[pivot] * pow(int(a[pivot, col]), -1, prime) % prime
        a[pivot+1:] = (a[pivot+1:] - a[pivot+1:, col, None] * a[pivot]) % prime
        pivot += 1
        if pivot == a.shape[0]:
            break
    return pivot

def run(packet):
    need(sha(packet/'manifest.json') == AUTHOR_SHA, 'author edition')
    manifest = json.loads((packet/'manifest.json').read_text())
    for row in manifest['exports']:
        path = packet/row['path']
        need(path.stat().st_size == row['bytes'] and sha(path) == row['sha256'], row['path'])
    # Independent polynomial construction; message order is part of the coordinate convention.
    polynomial = sum(1 << i for i in (0, 1, 5, 6, 7, 9, 11))
    blocks = []
    for message in range(4096):
        word = 0
        for i in range(12):
            if message & (1 << i):
                word ^= polynomial << i
        if word.bit_count() == 7:
            blocks.append(word)
    need(len(blocks) == 253, 'Steiner heptad count')
    # Verify the Steiner property without a pre-existing constructor.
    tetrads = []
    for block in blocks:
        tetrads.extend(itertools.combinations([i for i in range(23) if block & (1 << i)], 4))
    need(len(tetrads) == len(set(tetrads)) == math.comb(23, 4), 'unique tetrad coverage')
    heptads = [b for b in blocks if not b & 3]
    need(len(heptads) == 120, 'coordinate count')
    A = np.array([[int(x != y and (x & y).bit_count() == 3) for y in heptads] for x in heptads], dtype=np.int64)
    need(np.array_equal(A, A.T) and np.all(A.sum(axis=1) == 77), 'graph symmetry and degree')
    need(np.array_equal(A @ A, 33*np.eye(120, dtype=np.int64) + 8*A + 44*np.ones((120, 120), dtype=np.int64)), 'all SRG products')
    S = (A[1:] - A[0]) % 3
    E = (1-A) % 3
    need(rank(A) == 21 and rank(S) == 20, 'actual C21 and S20')
    need(np.array_equal(E @ E % 3, E) and np.array_equal(E @ A % 3, A), 'orthogonal projector identities')
    need(rank(np.vstack((A, E))) == 21, 'projector image is C')
    certificate = json.loads((packet/'certificate_data.json').read_text())
    seed = tuple(certificate['seed'])
    need(sum(x != 0 for x in seed) == 30 and rank(np.vstack((S, seed))) == 20, 'seed weight and actual S membership')
    generators = json.loads((packet/'retained/module_data.json').read_text())['full_generators']
    inverses = []
    for g in generators:
        need(sorted(g) == list(range(1, 121)), 'generator permutation')
        p = np.array(g)-1
        need(np.array_equal(A[np.ix_(p, p)], A), 'literal graph action')
        inverses.append(np.argsort(p).tolist())
    words = {seed}
    frontier = {seed}
    while frontier:
        following = {tuple(word[i] for i in inverse) for word in frontier for inverse in inverses} - words
        words.update(following)
        need(len(words) <= 112, 'orbit bound')
        frontier = following
    need(len(words) == 112 and all(sum(x != 0 for x in word) == 30 for word in words), '112 words of weight 30')
    need(all(tuple(-x % 3 for x in word) in words for word in words), 'opposite pairs')
    supports = sorted({tuple(x != 0 for x in word) for word in words})
    need(len(supports) == 56, '56 supports')
    B = np.array(supports, dtype=np.int64)
    T = B.T @ B
    need(np.all(T.diagonal() == 14), 'point incidences')
    counts = {}
    for i in range(120):
        for j in range(i):
            edge, incidence = int(A[i, j]), int(T[i, j])
            counts[f'{edge},{incidence}'] = counts.get(f'{edge},{incidence}', 0) + 1
            need(edge == int(incidence != 4), 'recover adjacency from supports')
    need(counts == {'0,4':2520, '1,2':3360, '1,6':1260}, 'all unordered pair counts')
    # Split actual vertex sets by neighbor counts. This implements refinement
    # without the author's numeric color/signature implementation.
    cells = [set(range(120))]
    chain = []
    while True:
        while True:
            refined = []
            for cell in cells:
                pieces = {}
                for vertex in cell:
                    key = tuple(int(A[vertex, sorted(part)].sum()) for part in cells)
                    pieces.setdefault(key, set()).add(vertex)
                refined.extend(pieces.values())
            if len(refined) == len(cells):
                cells = refined
                break
            cells = refined
        nonsingletons = [part for part in cells if len(part) > 1]
        if not nonsingletons:
            break
        selected = min(nonsingletons, key=lambda part:(len(part), sorted(part)))
        vertex = min(selected)
        chain.append([vertex, len(selected)])
        cells.remove(selected)
        cells.extend([{vertex}, selected-{vertex}])
    need(chain == [[0,120],[4,42],[1,8],[2,2]] and len(cells) == 120, 'discrete graph refinement chain')
    upper = math.prod(size for _, size in chain)
    gap_input = 'g := Group(List(' + json.dumps(generators) + ', PermList));;\nPrint(Size(g), "\\n");\nQUIT;\n'
    result = subprocess.run(['/opt/homebrew/bin/gap','-q','-b'], input=gap_input, text=True, capture_output=True, check=True, timeout=30)
    need(result.stdout.strip() == '80640' and not result.stderr.strip(), 'GAP subgroup order equals upper bound')
    retained = json.loads((packet/'retained/120_differences.json').read_text())
    counts_vector = retained['weight_counts']
    need(retained['basis_rows'] == 20 and retained['coefficient_vectors'] == 3**20 and sum(counts_vector) == 3**20, 'retained full enumeration range')
    need(counts_vector[0] == 1 and not any(counts_vector[1:30]) and counts_vector[30] == 112, 'retained minimum count')
    return {'status':'PASS', 'author_manifest_sha256':AUTHOR_SHA, 'author_exports_checked':len(manifest['exports']), 'Steiner_tetrads':len(tetrads), 'code_dimensions':[21,20], 'symmetric_projector_checked':True, 'minimum_orbit_words':112, 'minimum_supports':56, 'support_pair_counts':counts, 'refinement_chain_zero_based':chain, 'graph_upper_bound':upper, 'GAP_subgroup_order':80640, 'complete_word_enumeration':'retained accepted premise; not repeated', 'author_code_imports':False, 'scope':'Actual coordinate permutation groups of C21, S20 and graph; abstract group identification retained; no whole-source or formalization credit'}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    report = run(args.packet)
    args.out.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
