#!/usr/bin/env python3
"""Independent 105-coordinate orbits, incidence bound and rank-one factor.

The root's prior rank/refinement helpers are reused. No author code is imported.
"""
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



def reduced(a):
    a=np.array(a,dtype=np.int64).copy()%3;r=0
    for j in range(a.shape[1]):
        found=next((i for i in range(r,len(a)) if a[i,j]),None)
        if found is None: continue
        a[[r,found]]=a[[found,r]];a[r]=a[r]*int(a[r,j])%3
        for i in range(len(a)):
            if i!=r and a[i,j]: a[i]=(a[i]-a[i,j]*a[r])%3
        r+=1
        if r==len(a): break
    return a,r


def run(packet,replay):
    data=json.loads((packet/'module_data.json').read_text());gens=[[x-1 for x in g]for g in data['coordinate_generators']]
    require(all(sorted(g)==list(range(105))for g in gens),'coordinate permutations')
    def act(w,g):
        out=[0]*105
        for i,x in enumerate(w):out[g[i]]=int(x)
        return tuple(out)
    def orbit(seed):
        queue=[tuple(seed)];seen=set(queue)
        for w in queue:
            for g in gens:
                x=act(w,g)
                if x not in seen:seen.add(x);queue.append(x)
        return seen
    allwords=set();sizes=[]
    for seed in data['minimum33_seeds']:
        found=orbit(seed);require(allwords.isdisjoint(found),'disjoint minimum orbits')
        require(all(sum(x!=0 for x in w)==33 for w in found),'orbit weight')
        allwords.update(found);sizes.append(len(found))
    require(sorted(sizes)==[105,105,280,280] and len(allwords)==770,'minimum orbit sizes')
    supports={frozenset(i for i,x in enumerate(w)if x)for w in allwords}
    expected={frozenset(x-1 for x in s)for s in json.loads((replay/'certificate/supports.json').read_text())}
    require(supports==expected and len(supports)==385,'complete support data')
    neighbors=[set()for _ in range(490)]
    for i,s in enumerate(sorted(supports,key=lambda s:tuple(sorted(s)))):
        for v in s:neighbors[v].add(105+i);neighbors[105+i].add(v)
    cells=[set(range(105)),set(range(105,490))];bounds=[]
    for point in [1,2,3,4,7,12,6]:
        cells=refine(neighbors,cells);cell=next(c for c in cells if point-1 in c);bounds.append(len(cell))
        cells=[c for c in cells if c is not cell]+[{point-1},cell-{point-1}]
    cells=refine(neighbors,cells)
    require(bounds==[105,8,3,2,4,3,4] and all(len(c)==1 for c in cells),'full incidence upper bound')
    E=np.array(data['filtration_basis'],dtype=np.int64);augmented,r=reduced(np.hstack([E,np.eye(105,dtype=np.int64)]))
    require(r==105 and np.array_equal(augmented[:,:105],np.eye(105,dtype=np.int64)),'filtration basis')
    inverse=augmented[:,105:];require(np.array_equal(E@inverse%3,np.eye(105,dtype=np.int64)),'literal inverse')
    matrices=[np.array([act(row,g)for row in E])@inverse%3 for g in gens]
    cuts=[0,1,20,39,84,85,104,105]
    require(data['cuts']==cuts and all(not np.any(M[:c,c:])for M in matrices for c in cuts[1:-1]),'invariant prefixes')
    block=[M[39:84,39:84]for M in matrices];T=np.zeros((45,45),dtype=np.int64)
    for coefficient,word in data['terms']:
        product=np.eye(45,dtype=np.int64)
        for letter in word:product=product@block[letter-1]%3
        T=(T+coefficient*product)%3
    P=np.zeros((45,45),dtype=np.int64);power=np.eye(45,dtype=np.int64)
    for coefficient in data['polynomial']:
        P=(P+coefficient*power)%3;power=power@T%3
    require(rank(P)==1,'actual rank-one element')
    row,col=next((i,j)for i in range(45)for j in range(45)if P[i,j])
    def cyclic(seed,right):
        basis=np.array([seed],dtype=np.int64);previous=0
        while len(basis)!=previous:
            previous=len(basis);candidates=[basis]
            for M in block:candidates.append(basis@M%3 if right else basis@M.T%3)
            rr,dim=reduced(np.vstack(candidates));basis=rr[:dim]
        return len(basis)
    require(cyclic(P[:,col],False)==cyclic(P[row],True)==45,'both full cyclic spaces')
    extra=[]
    for i,B in enumerate(data['code20_bases'][1:]):
        B=np.array(B,dtype=np.int64);rr,dim=reduced(B)
        require(dim==20 and np.array_equal(rr,B),'systematic extra code basis')
        pivots=[next(j for j,x in enumerate(v)if x)for v in B]
        found=orbit(data['extra_minimum_seeds'][i]);found|={tuple(-x%3 for x in w)for w in found}
        d=[30,28][i];require(len(found)==[672,720][i] and all(sum(x!=0 for x in w)==d for w in found),'candidate minimum set')
        require(all(np.array_equal(np.array(w)[pivots]@B%3,w)for w in found),'entire orbit is in code')
        restricted=sum(sum(w[j]!=0 for j in pivots)<=5 for w in found)
        counts=json.loads((replay/f'extra{i+1}.json').read_text())['restricted_weight_counts']
        require(restricted==[342,396][i] and counts[d]==restricted and not any(counts[1:d]),'exact restricted exhaustion')
        extra.append({'minimum_words':len(found),'restricted_minimum_words':restricted})
    return dict(status='PASS_INDEPENDENT_105_FINITE_INSTANCES',author_code_imported=False,
                minimum_orbits=sizes,minimum_supports=385,stabilizer_bounds=bounds,full_group_upper=math.prod(bounds),
                invariant_factor_dimensions=[b-a for a,b in zip(cuts,cuts[1:])],rank_one_factor_dimension=45,
                certified_factor_algebra=2025,additional_minimum_sets=extra,
                group_identification_and_complete_Hom_spaces='Separately read and freshly replayed exact GAP computations.',
                full_enumerations_repeated=False)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--replay',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args();require(not a.out.exists(),'fresh report')
    result=run(a.packet,a.replay);a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
