#!/usr/bin/env python3
"""Exact F017 Table1 checks by field arithmetic and transitive-code averaging.

No external graph database or coding package is used. Large-code distances
remain upper bounds, exactly as in the source. The restricted histograms are
not presented as complete weight enumerators. The accompanying averaging
lemma, rather than an empirical search assumption, supplies each lower bound.
"""
import argparse
import hashlib
import itertools
import json
import math
import subprocess
from pathlib import Path


def need(b, message):
    if not b:
        raise RuntimeError(message)


def digits(x, p, d):
    a = []
    for _ in range(d):
        a.append(x % p)
        x //= p
    return a


def encode(a, p):
    return sum(x * p**i for i, x in enumerate(a))


def remainder(a, b, p):
    a = list(a)
    for i in range(len(a) - 1, len(b) - 2, -1):
        c = a[i] * pow(b[-1], -1, p) % p
        for j in range(len(b)):
            a[i - len(b) + 1 + j] = (a[i - len(b) + 1 + j] - c * b[j]) % p
    return a[:len(b) - 1]


def irreducible(f, p):
    d = len(f) - 1
    # Every reducible monic polynomial has a monic factor of degree <= d/2.
    return all(any(remainder(f, digits(t, p, e) + [1], p))
               for e in range(1, d // 2 + 1) for t in range(p**e))


class Field:
    def __init__(self, p, d):
        self.p, self.d, self.q = p, d, p**d
        self.f = next(digits(t, p, d) + [1] for t in range(1, self.q)
                      if irreducible(digits(t, p, d) + [1], p))
        self.vec = [digits(x, p, d) for x in range(self.q)]
        self.plus = [[encode([(x+y) % p for x, y in zip(a, b)], p)
                      for b in self.vec] for a in self.vec]
        self.neg = [encode([(-a) % p for a in v], p) for v in self.vec]
        factors = [s for s in range(2, self.q) if (self.q-1) % s == 0
                   and all(s % t for t in range(2, math.isqrt(s)+1))]
        self.primitive = next(a for a in range(1, self.q)
                              if all(self.power(a, (self.q-1)//s) != 1 for s in factors))
        need(len({self.power(self.primitive, i) for i in range(self.q-1)}) == self.q-1,
             'primitive generator order')

    def mul(self, a, b):
        prod = [0] * (2*self.d-1)
        for i, x in enumerate(self.vec[a]):
            for j, y in enumerate(self.vec[b]):
                prod[i+j] = (prod[i+j] + x*y) % self.p
        return encode(remainder(prod, self.f, self.p), self.p)

    def power(self, a, n):
        x = 1
        while n:
            if n & 1:
                x = self.mul(x, a)
            a = self.mul(a, a)
            n >>= 1
        return x


def rref(matrix, p):
    rows = [list(r) for r in matrix]
    rank, pivots = 0, []
    for j in range(len(rows[0])):
        i = next((i for i in range(rank, len(rows)) if rows[i][j] % p), None)
        if i is None:
            continue
        rows[i], rows[rank] = rows[rank], rows[i]
        inv = pow(rows[rank][j] % p, -1, p)
        rows[rank] = [x*inv % p for x in rows[rank]]
        for i, row in enumerate(rows):
            if i != rank and row[j] % p:
                c = row[j] % p
                rows[i] = [(x-c*y) % p for x, y in zip(row, rows[rank])]
        pivots.append(j)
        rank += 1
        if rank == len(rows):
            break
    return rows[:rank], pivots


def row_member(v, basis, pivots, p):
    v = list(v)
    for row, j in zip(basis, pivots):
        c = v[j]
        v = [(x-c*y) % p for x, y in zip(v, row)]
    return not any(v)


def spectrum(n, degree, lam, mu):
    disc = (lam-mu)**2 + 4*(degree-mu)
    sq = math.isqrt(disc)
    need(sq*sq == disc, 'integral SRG roots')
    need((lam-mu+sq) % 2 == 0, 'integral eigenvalues')
    r, s = (lam-mu+sq)//2, (lam-mu-sq)//2
    num = -degree-(n-1)*s
    need(num % (r-s) == 0, 'integral multiplicities')
    f = num//(r-s)
    return [(degree, 1), (r, f), (s, n-1-f)]


def check_case(field, index, p, parameters, dims, distances, min_rows, exe, out):
    n, degree, lam, mu = parameters
    need(field.q == n and (n-1)//index == degree, 'field and subgroup order')
    subgroup = {field.power(field.primitive, index*i) for i in range(degree)}
    need(len(subgroup) == degree and 0 not in subgroup, 'subgroup cardinality')
    need({field.neg[x] for x in subgroup} == subgroup, 'undirected Cayley graph')
    # Translation sends an arbitrary ordered pair (x,y) to (0,y-x).
    counts = [len(subgroup & {field.plus[t][s] for s in subgroup}) for t in range(n)]
    need(counts[0] == degree and all(counts[t] == (lam if t in subgroup else mu)
                                   for t in range(1, n)), 'all common-neighbour counts')
    need(degree % p == 0 and (lam+1) % p == 0 and mu % p == 0, 'RLCD identity')
    need((degree-mu) % p != 0 or (degree-1-lam) % p != 0 or
         (degree % p == 0 and (n-1) % p == 0), 'not CLCD')
    eig = spectrum(*parameters)
    ranks = [sum(m for val, m in eig if (val+shift) % p) for shift in [0, 1]]
    need(ranks == list(dims), 'ranks from idempotents and characteristic polynomial')
    tag = f'gp{n}_{index}_p{p}'
    item = {'id': tag, 'field_prime': field.p, 'field_degree': field.d,
            'field_polynomial_low_coefficients_first': field.f,
            'primitive_element': field.primitive, 'subgroup': sorted(subgroup),
            'parameters': list(parameters), 'common_neighbour_counts_from_zero': counts,
            'spectrum': eig, 'ranks': ranks, 'RLCD': True, 'CLCD': False, 'codes': []}
    if n > 121:
        item['codes'] = [{'kind': name, 'dimension': rank, 'distance_upper_bound': degree+shift,
                          'witness': 'a row of A plus shift times I; no exact distance claimed'}
                         for name, rank, shift in zip(['A', 'A+I'], ranks, [0, 1])]
        return item
    adjacency = [[int(y in {field.plus[x][s] for s in subgroup}) for y in range(n)]
                 for x in range(n)]
    for shift, name, target, dim in zip([0, 1], ['A', 'A+I'], distances, dims):
        matrix = [[(v+shift*(i==j)) % p for j, v in enumerate(row)]
                  for i, row in enumerate(adjacency)]
        basis, pivots = rref(matrix, p)
        need(len(basis) == dim and all(row[j] == int(i==t) for i, row in enumerate(basis)
                                       for t, j in enumerate(pivots)), 'systematic generator')
        need(all(row_member(row, basis, pivots, p) for row in matrix), 'row-space equality')
        bound = dim*(target-1)//n
        basis_path = out/f'{tag}_{shift}.txt'
        basis_path.write_text(f'{n} {dim} {p} {bound}\n' +
                              ''.join(''.join(map(str, row))+'\n' for row in basis))
        raw = subprocess.run([str(exe), str(basis_path)], check=True, text=True,
                             capture_output=True).stdout
        result = json.loads(raw)
        expected_messages = sum(math.comb(dim, j)*(p-1)**j for j in range(bound+1))
        need(result['messages'] == expected_messages == sum(result['restricted_weight_counts']),
             'restricted enumeration cardinality')
        need(result['restricted_weight_counts'][0] == 1, 'basis independence')
        need(not any(result['restricted_weight_counts'][1:target]), 'averaging distance lower bound')
        witness = [int(x) for x in result['minimum_witness']]
        need(len(witness) == n and row_member(witness, basis, pivots, p), 'distance witness membership')
        need(sum(x != 0 for x in witness) == target, 'distance attained')
        (out/f'{tag}_{shift}.json').write_text(raw)
        report = {'kind': name, 'dimension': dim, 'distance': target, 'information_set': pivots,
                  'lower_bound_message_weight': bound, 'enumerated_messages': expected_messages,
                  'enumeration_sha256': hashlib.sha256(raw.encode()).hexdigest(),
                  'basis_sha256': hashlib.sha256(basis_path.read_bytes()).hexdigest()}
        if min_rows and shift == 0:
            # Every minimum word can be translated to one in this second finite set.
            # Translations preserve the set of adjacency rows, proving exhaustiveness.
            cap = dim*target//n
            actual, rows_set = set(), {tuple(row) for row in adjacency}
            for size in range(1, cap+1):
                for indices in itertools.combinations(range(dim), size):
                    for coefs in itertools.product(range(1, p), repeat=size):
                        word = tuple(sum(c*basis[i][j] for i, c in zip(indices, coefs)) % p
                                     for j in range(n))
                        if sum(x != 0 for x in word) == target:
                            need(word in rows_set, 'all minimum words are adjacency rows')
                            actual.add(word)
            need(actual and all(sum(row) == target for row in adjacency), 'all rows attain distance')
            report['all_minimum_words'] = 'exactly the adjacency rows'
            report['minimum_word_count'] = len(rows_set)
            report['minimum_message_weight_bound'] = cap
            report['minimum_words_in_restricted_set'] = len(actual)
        item['codes'].append(report)
    return item


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--enumerator', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    need(not args.out.exists(), 'use a fresh output directory')
    executable_hash_before = hashlib.sha256(args.enumerator.read_bytes()).hexdigest()
    args.out.mkdir(parents=True)
    cases = [
        (5,2,3,2,(25,8,3,2),(8,17),(8,4),True),
        (7,2,4,2,(49,12,5,2),(12,37),(12,4),True),
        (3,4,4,2,(81,20,1,6),(20,61),(20,6),True),
        (3,4,5,2,(81,16,7,2),(16,65),(16,4),True),
        (11,2,3,2,(121,40,15,12),(40,81),(20,8),False),
        (11,2,4,2,(121,30,11,6),(90,31),(6,11),False),
        (11,2,4,3,(121,30,11,6),(30,91),(20,6),False),
        (11,2,6,2,(121,20,9,2),(20,101),(20,4),True),
        (3,5,11,2,(243,22,1,2),(110,133),(None,None),False),
        (3,6,4,2,(729,182,55,42),(546,183),(None,None),False),
        (3,6,7,2,(729,104,31,12),(104,625),(None,None),False),
        (3,6,14,2,(729,52,25,2),(52,677),(None,None),False)]
    fields, results = {}, []
    for ell,d,index,p,params,dims,distances,min_rows in cases:
        fields.setdefault((ell,d), None)
        if fields[ell,d] is None:
            fields[ell,d] = Field(ell,d)
        result = check_case(fields[ell,d], index,p,params,dims,distances,min_rows,
                            args.enumerator.resolve(), args.out)
        results.append(result)
        print(result['id'], 'PASS', flush=True)
    need(hashlib.sha256(args.enumerator.read_bytes()).hexdigest() == executable_hash_before,
         'enumerator unchanged through the run')
    report = {'status':'EXACT_FINITE_CHECKS_AWAITING_DISTINCT_REVIEW',
              'enumerator_sha256':executable_hash_before,
              'method':'systematic information set, transitive translations, exact restricted enumeration',
              'source':'F017 Table1; literal degree201 corrected to20 for GP(81,4)',
              'cases':results, 'new_conjecture_credit':0,
              'limits':['Requires the written averaging and idempotent rank lemmas.',
                        'No full weight distributions or full automorphism groups claimed.',
                        'Four large graphs retain only the source distance upper bounds.']}
    (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__ == '__main__':
    main()
