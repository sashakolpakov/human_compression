#!/usr/bin/env python3
"""Build the two 120-coordinate codes from the retained Steiner construction."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
from steiner_construction import steiner_blocks, rank_mod, need


def rref(rows):
    a = [[x % 3 for x in r] for r in rows]
    pivots = []
    for c in range(len(a[0])):
        i = next((i for i in range(len(pivots), len(a)) if a[i][c]), None)
        if i is None:
            continue
        r = len(pivots)
        a[r], a[i] = a[i], a[r]
        z = pow(a[r][c], -1, 3)
        a[r] = [x*z % 3 for x in a[r]]
        for i in range(len(a)):
            if i != r:
                z = a[i][c]
                a[i] = [(x-z*y) % 3 for x,y in zip(a[i],a[r])]
        pivots.append(c)
        if len(pivots) == len(a):
            break
    return a[:len(pivots)], pivots


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, required=True)
    a = p.parse_args()
    a.out.mkdir(parents=True, exist_ok=False)
    blocks, _ = steiner_blocks()
    heptads = [b for b in blocks if b & 3 == 0]
    lines = [b ^ 3 for b in blocks if b & 3 == 3]
    need(len(heptads) == 120 and len(lines) == 21, 'residual sizes')
    need(all(l.bit_count() == 5 for l in lines), 'line sizes')
    for p,q in itertools.combinations(range(2,23),2):
        need(sum(bool((l>>p)&1 and (l>>q)&1) for l in lines) == 1, 'plane pair axiom')
    flags = [(p,l) for p in range(2,23) for l in lines if (l>>p)&1]
    R = [[int(bool((h>>p)&1) and (h&l).bit_count() == 3) for h in heptads]
         for p,l in flags]
    need(len(flags) == 105 and all(sum(r)==24 for r in R), 'flag replication')
    need(all(sum(r[i] for r in R)==21 for i in range(120)), 'subplane flags')
    gram_values = set()
    for i,(p,l) in enumerate(flags):
        for j,(q,m) in enumerate(flags):
            actual = sum(x*y for x,y in zip(R[i],R[j]))
            expected = (24 if i==j else 12 if p==q or l==m
                        else 6 if ((m>>p)&1 or (l>>q)&1) else 3)
            need(actual == expected, 'full integer flag Gram table')
            gram_values.add(actual)
    columns = list(zip(*R))
    Q = [[sum(x*y for x,y in zip(u,v)) % 3 for v in columns] for u in columns]
    K, kp = rref(Q)
    N, np = rref(K+[[1]*120])
    need(len(K)==15 and len(N)==16, 'code dimensions')
    need(all(sum(x*y for x,y in zip(u,v)) % 3 == 0 for u in N for v in N), 'self-orthogonality')
    seed = json.loads(Path(__file__).with_name('module_data.json').read_text())['minimum_seed']
    need(sum(x!=0 for x in seed)==48, 'minimum seed weight')
    need([sum(seed[kp[i]]*K[i][j] for i in range(15))%3 for j in range(120)]==seed,
         'minimum seed belongs to K')
    for name, B in [('K',K),('N',N)]:
        (a.out/(name+'_basis.txt')).write_text(f'120 {len(B)}\n'+''.join(''.join(map(str,r))+'\n' for r in B))
    data = json.loads(Path(__file__).with_name('module_data.json').read_text())
    for key in ['group_generators','full_generators']:
        for g in data[key]:
            need(sorted(g)==list(range(1,121)), 'literal permutation')
            need(all((heptads[i]&heptads[j]).bit_count()==
                     (heptads[g[i]-1]&heptads[g[j]-1]).bit_count()
                     for i in range(120) for j in range(i)), 'source residual graph action')
    data.update({'K_basis':K,'N_basis':N,'points':list(range(2,23)),
                 'heptads':heptads,'lines':lines,'flags':flags})
    (a.out/'constructed.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
    gap = ''.join(k+':='+repr(data[k])+';;\n' for k in
                  ['group_generators','full_generators','outer_complement',
                   'filtration_basis','filtration_cuts','K_basis','N_basis','minimum_seed'])
    (a.out/'constructed.g').write_text(gap)
    result = {'status':'PASS','flag_incidence_shape':[105,120],
              'integer_flag_Gram_values':sorted(gram_values),'R_rank':rank_mod(R,3),
              'K_dimension':15,'N_dimension':16,'both_self_orthogonal':True,
              'minimum_seed_weight':48,'basis_sha256':{name:hashlib.sha256((a.out/(name+'_basis.txt')).read_bytes()).hexdigest() for name in ['K','N']}}
    (a.out/'construction_report.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))


if __name__ == '__main__':
    main()
