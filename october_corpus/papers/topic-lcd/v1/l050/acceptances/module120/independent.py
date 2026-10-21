#!/usr/bin/env python3
"""Independent incidence, dual small weights and refinement checks.

Imports no author program. Uses literal records from the fresh full replay.
The lower full-group order and simple-factor/Hom certificate are independently
read and freshly replayed separately; this checker does not replace them.
"""
import argparse
from collections import defaultdict
from itertools import combinations
import json
import math
from pathlib import Path


def require(test, message):
    if not test:
        raise ValueError(message)


def echelon(rows):
    pivots = {}
    for incoming in rows:
        v = [x % 3 for x in incoming]
        for j, row in sorted(pivots.items()):
            c = v[j]
            v = [(x-c*y) % 3 for x,y in zip(v,row)]
        if any(v):
            j = next(j for j,x in enumerate(v) if x)
            inv = 1 if v[j] == 1 else 2
            pivots[j] = [x*inv % 3 for x in v]
    return list(pivots.values())


def dual_small_weights(basis):
    columns = list(zip(*basis))
    zero = (0,)*len(basis)
    singles = defaultdict(list)
    for i,v in enumerate(columns):
        for a in [1,2]:
            singles[tuple(a*x % 3 for x in v)].append(i)
    require(zero not in singles, 'no dual word of weight1')
    pairs = defaultdict(list)
    for i,j in combinations(range(len(columns)),2):
        for a in [1,2]:
            for b in [1,2]:
                key = tuple((a*x+b*y) % 3 for x,y in zip(columns[i],columns[j]))
                pairs[key].append((i,j))
    require(zero not in pairs, 'no dual word of weight2')
    ordered_four = 0
    for key, entries in pairs.items():
        negative = tuple((-x) % 3 for x in key)
        for i,j in entries:
            require(all(t == i or t == j for t in singles.get(negative,[])),
                    'no dual word of weight3')
            for u,v in pairs.get(negative,[]):
                if len({i,j,u,v}) == 4:
                    ordered_four += 1
    # A coefficient word on four distinct coordinates has exactly six
    # ordered partitions into two pairs. Each signed pair occurs once above.
    require(ordered_four % 6 == 0, 'four-word partition multiplicity')
    return {'weights1to3':0, 'weight4':ordered_four//6,
            'signed_pairs':sum(map(len,pairs.values()))}


def refine_cells(neighbors, cells):
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


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--replay',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    require(not args.out.exists(),'fresh output')
    data=json.loads((args.replay/'construction/constructed.json').read_text())
    heptads,lines=data['heptads'],data['lines']
    require(len(set(heptads))==120 and len(set(lines))==21,'distinct incidence sets')
    flags=[(p,l) for p in range(2,23) for l in lines if l & (1<<p)]
    R=[[int(bool(h & (1<<p)) and (h&l).bit_count()==3) for h in heptads] for p,l in flags]
    counts=defaultdict(int)
    for i,(p,l) in enumerate(flags):
        for j,(q,m) in enumerate(flags):
            actual=sum(a*b for a,b in zip(R[i],R[j]))
            expected=24 if i==j else 12 if p==q or l==m else 6 if (m&(1<<p) or l&(1<<q)) else 3
            require(actual==expected,'complete independent Gram table')
            counts[actual]+=1
    cols=list(zip(*R))
    Q=[[sum(a*b for a,b in zip(x,y)) % 3 for y in cols] for x in cols]
    K,N=data['K_basis'],data['N_basis']
    require(len(echelon(Q))==15 and len(echelon(Q+K))==15,'K equals incidence image')
    require(len(echelon(K+[[1]*120]))==16 and len(echelon(K+[[1]*120]+N))==16,
            'N equals K plus constant line')
    require(all(sum(a*b for a,b in zip(x,y)) % 3==0 for x in N for y in N),
            'N self-orthogonal')
    duals={name:dual_small_weights(basis) for name,basis in [('K',K),('N',N)]}
    require(duals['K']['weight4']==2100 and duals['N']['weight4']==1260,'direct dual counts')
    support=json.loads((args.replay/'construction/support_data.json').read_text())
    supports=[frozenset(x-1 for x in s) for s in support['supports']]
    require(len(supports)==len(set(supports))==630,'distinct minimum supports')
    neighbors=[set() for _ in range(750)]
    for i,s in enumerate(supports):
        for v in s:
            neighbors[v].add(120+i);neighbors[120+i].add(v)
    cells=[set(range(120)),set(range(120,750))]
    sizes=[]
    for chosen in [1,6,48,10,2,3]:
        cells=refine_cells(neighbors,cells)
        selected=next(cell for cell in cells if chosen-1 in cell)
        sizes.append(len(selected))
        cells=[cell for cell in cells if cell is not selected]+[{chosen-1},selected-{chosen-1}]
    cells=refine_cells(neighbors,cells)
    require(sizes==[120,21,2,4,2,2] and all(len(cell)==1 for cell in cells),
            'complete independent refinement bound')
    report={'status':'PASS','independent_imports':[],'flag_pairs':len(flags)**2,
            'integer_Gram_pair_counts':dict(counts),'rank_R':len(echelon(R)),
            'rank_Q':15,'rank_N':16,'direct_dual_counts':duals,
            'refinement_orbit_bounds':sizes,'full_group_upper_bound':math.prod(sizes),
            'proof_of_dual_counter':'Six ordered pair partitions per weight4 coefficient word',
            'scope':'No new full-source or formal claim; lower group/module/full weights separately replayed.'}
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__=='__main__':
    main()
