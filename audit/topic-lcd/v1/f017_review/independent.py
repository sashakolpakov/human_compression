#!/usr/bin/env python3
"""Distinct bounded models for the complete written F017 application.

No author imports. These models complement the written review; they do not
replace its uniform proofs or the separately accepted finite certificates.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
from math import comb
from pathlib import Path


def need(ok, message):
    if not ok:
        raise ValueError(message)


def rank(matrix, p):
    a = [list(r) for r in matrix]
    if not a:
        return 0
    k = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(k, len(a)) if a[i][j] % p), None)
        if pivot is None:
            continue
        a[k], a[pivot] = a[pivot], a[k]
        u = pow(a[k][j] % p, -1, p)
        a[k] = [x*u % p for x in a[k]]
        for i in range(k+1, len(a)):
            u = a[i][j] % p
            a[i] = [(x-u*y) % p for x, y in zip(a[i], a[k])]
        k += 1
        if k == len(a):
            break
    return k


def square(a, p):
    return [[sum(x*y for x, y in zip(r, c)) % p for c in zip(*a)] for r in a]


def point_incidence():
    records = []
    for n in range(3, 9):
        for k in range(1, n):
            sets = list(combinations(range(n), k))
            w = [[int(i in t) for t in sets] for i in range(n)]
            for p in (2, 3, 5):
                need(rank(w, p) == n-int(k % p == 0), 'point-incidence rank')
            words = {tuple(sum(c[i] for i in t) % 2 for t in sets)
                     for c in product((0, 1), repeat=n)}
            actual = Counter(sum(v) for v in words)
            predicted = Counter()
            for r in range(n+1):
                weight = sum(comb(r, i)*comb(n-r, k-i)
                             for i in range(1, min(r, k)+1, 2)
                             if 0 <= k-i <= n-r)
                predicted[weight] += comb(n, r)
            fiber = 2 if k % 2 == 0 else 1
            need(all(v % fiber == 0 for v in predicted.values()), 'whole fibers')
            predicted = Counter({w: c//fiber for w, c in predicted.items()})
            need(actual == predicted, 'complete enumerator')
            if (n, k) == (8, 2):
                need(actual[16] == 35 and actual[16] != comb(8, 4), 'source multiplicity correction')
            records.append({'n': n, 'k': k, 'binary_words': len(words), 'rank_primes': [2,3,5]})
    # The strict k<n hypothesis is necessary.
    need(rank([[1]]*4, 2) != 4-1, 'endpoint countermodel')
    return records


def odd_graphs():
    records = []
    for k in range(1, 5):
        sets = list(map(frozenset, combinations(range(2*k+1), k)))
        stars = list(map(frozenset, combinations(range(2*k+1), k-1)))
        a = [[int(not x & y) for y in sets] for x in sets]
        w = [[int(r <= x) for x in sets] for r in stars]
        e = [[sum(r <= x and r <= y for r in stars) % 2 for y in sets] for x in sets]
        a2 = square(a, 2)
        need(a2 == [[int(i == j)^e[i][j] for j in range(len(sets))]
                    for i in range(len(sets))], 'odd square identity')
        need(all(sum(x*y for x,y in zip(row,star)) % 2 == 0 for row in a for star in w), 'A u zero')
        need(rank(a,2) == comb(2*k,k), 'odd rank')
        need(rank(a,2)+rank(w,2) == len(sets), 'orthogonal dimensions')
        one = [1]*len(sets)
        need((rank(a+[one],2) == rank(a,2)) == (k % 2 == 0), 'odd constant clause')
        need((rank(w+[one],2) == rank(w,2)) == (k % 2 == 1), 'dual constant clause')
        if k == 2:
            need(a2[0][1] == 1, 'printed formula fails off diagonal')
            b = [[int(i != j)-a[i][j] for j in range(len(sets))] for i in range(len(sets))]
            need(rank(a,2)+rank(b,2) == len(sets), 'Petersen complementary ranks')
            need(all(sum(x*y for x,y in zip(r,s)) % 2 == 0 for r in a for s in b), 'Petersen CLCD')
            need(a2 != a, 'Petersen not RLCD')
        records.append({'k': k, 'length': len(sets), 'rank': rank(a,2)})
    return records


def scalar_rows(packet):
    data = json.loads((packet/'finite_subset_rows.json').read_text())
    rows = data['rows'] if isinstance(data,dict) else data
    out = []
    for row in rows:
        n,k,r,p = [row[key] for key in ('n','k','r','p')]
        sets = list(map(frozenset, combinations(range(n),k)))
        x = frozenset(range(k))
        neighbours = [z for z in sets if len(z & x) == r]
        counts = []
        for j in range(k+1):
            y = frozenset(list(range(j))+list(range(k,2*k-j)))
            counts.append((sum(len(y & z) == r for z in neighbours)+int(j == r)) % p)
        need(len(neighbours) == row['degree'] and len(sets) == row['N'], 'literal graph parameters')
        need(counts == row['P_mod_p'], 'literal intersections versus reported scalar vector')
        out.append({'n':n,'k':k,'r':r,'p':p,'P':counts})
    need(len(out) == 16,'all sixteen source findings')
    return out


def paley_prime_models():
    out = []
    for q,p in [(13,3),(17,2),(29,7),(41,2),(41,5),(73,2),(73,3)]:
        squares = {i*i % q for i in range(1,q)}
        a = [[int((i-j) % q in squares) for j in range(q)] for i in range(q)]
        b = [[int(i != j)-a[i][j] for j in range(q)] for i in range(q)]
        nonsquare = next(i for i in range(1,q) if i not in squares)
        need(all(a[(nonsquare*i)%q][(nonsquare*j)%q] == b[i][j]
                 for i in range(q) for j in range(q)), 'explicit complement permutation')
        need(square(a,p) == [[-v % p for v in r] for r in a], 'Paley RLCD')
        need(rank(a,p) == rank(b,p) == (q-1)//2, 'nonsquare-order dimension')
        need(rank(a+b,p) == q-1, 'constant line defect')
        out.append({'q':q,'p':p,'rank':rank(a,p),'nonsquare':nonsquare})
    cycle = [[int((i-j)%5 in (1,4)) for j in range(5)] for i in range(5)]
    need((5-2*2-1) % 2 == 0 and square(cycle,2) != cycle, 'congruence insufficient')
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--packet', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    raw = (args.packet/'manifest.json').read_bytes()
    need(sha256(raw).hexdigest() == '87e5cec49b7994c0394a50058e4076fcf8eb99bd64a20a4459b0b207772ed4ae','frozen author edition')
    exports = json.loads(raw)['exports']
    for row in exports:
        b = (args.packet/row['path']).read_bytes()
        need(len(b) == row['bytes'] and sha256(b).hexdigest() == row['sha256'],'author export '+row['path'])
    source = json.loads((args.packet/'source_contract.json').read_text())
    need(len(source['rows']) == len({r['id'] for r in source['rows']}) == 104,'104 distinct dispositions')
    need(set(p for r in source['rows'] for p in r['source_physical_pages']) == set(range(1,18)), 'whole source routing')
    report = {'status':'PASS_DISTINCT_BOUNDED_F017_MODELS','author_manifest_sha256':sha256(raw).hexdigest(),
              'author_exports':len(exports),'source_dispositions':104,
              'point_incidence':point_incidence(),'odd_graphs':odd_graphs(),
              'literal_subset_counts':scalar_rows(args.packet),'nonsquare_Paley':paley_prime_models(),
              'no_author_imports':True,'large_enumerations_repeated':False,
              'proof_scope':'Bounded independent checks; complete written proof review and accepted prior finite evidence are separate.'}
    args.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'point_cases':len(report['point_incidence']),
                      'odd_graphs':len(report['odd_graphs']),'literal_subset_rows':len(report['literal_subset_counts']),
                      'nonsquare_Paley_cases':len(report['nonsquare_Paley'])}))


if __name__ == '__main__':
    main()
