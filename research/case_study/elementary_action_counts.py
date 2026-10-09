"""Faithful F2^r-actions up to point conjugacy and permutation of marked generators.

Uses orbit multiplicities, subgroup-lattice Mobius inversion, Burnside's
lemma, and an optional sign-character filter. No group enumeration in S_N.
"""
from itertools import permutations
from pathlib import Path
import hashlib
import json
import math


def subspaces(rank):
    zero=frozenset([0]); found={zero}; todo=[zero]
    while todo:
        h=todo.pop()
        for v in range(1 << rank):
            k=h | frozenset(x ^ v for x in h)
            if k not in found:
                found.add(k); todo.append(k)
    return sorted(found, key=lambda h:(len(h), sorted(h)))


def transform(v, perm):
    return sum(((v >> i) & 1) << perm[i] for i in range(len(perm)))


def mobius_zero(h):
    d=len(h).bit_length()-1
    return (-1)**d * 2**(d*(d-1)//2)


def geometric_product(factors, limit):
    out=[1]+[0]*limit
    for weight,sign in factors:
        for n in range(weight,limit+1):
            out[n] += sign*out[n-weight]
    return out


def formula(rank,limit,alternating=False):
    subs=subspaces(rank); index={h:i for i,h in enumerate(subs)}
    size=1 << rank; characters={}
    for h in subs:
        if len(h)*2 == size:
            characters[h]=next(c for c in range(1,size)
                               if all((c & x).bit_count()%2 == 0 for x in h))
    total=[0]*(limit+1)
    for perm in permutations(range(rank)):
        action=[index[frozenset(transform(v,perm) for v in h)] for h in subs]
        unseen=set(range(len(subs))); orbits=[]
        while unseen:
            first=min(unseen); indices=[first]; nxt=action[first]
            while nxt != first:
                indices.append(nxt); nxt=action[nxt]
            unseen -= set(indices)
            orbit=[subs[i] for i in indices]
            common=frozenset.intersection(*orbit)
            weight=sum(size//len(h) for h in orbit)
            character=0
            for h in orbit:
                character ^= characters.get(h,0)
            orbits.append((common,weight,character))
        for j in subs:
            mu=mobius_zero(j)
            allowed=[(weight,char) for common,weight,char in orbits if j <= common]
            for v in (range(size) if alternating else [0]):
                factors=[(weight,(-1)**((char & v).bit_count()%2))
                         for weight,char in allowed]
                coeff=geometric_product(factors,limit)
                total=[x+mu*y for x,y in zip(total,coeff)]
    denominator=math.factorial(rank)*(size if alternating else 1)
    assert all(x % denominator == 0 for x in total)
    return [x//denominator for x in total]


def direct_orbit_count(rank,limit,alternating=False):
    """Independent multiplicity enumeration, canonicalized under S_r."""
    size=1 << rank; subs=subspaces(rank); index={h:i for i,h in enumerate(subs)}
    perms=list(permutations(range(rank)))
    actions=[[index[frozenset(transform(v,p) for v in h)] for h in subs] for p in perms]
    weights=[size//len(h) for h in subs]
    characters=[]
    for h in subs:
        c=0
        if len(h)*2 == size:
            c=next(c for c in range(1,size) if all((c & x).bit_count()%2 == 0 for x in h))
        characters.append(c)
    counts=[set() for _ in range(limit+1)]
    multiplicities=[0]*len(subs)
    def visit(i,remaining,used,kernel,sign):
        if i == len(subs):
            if len(kernel) != 1 or (alternating and sign):
                return
            forms=[]
            for action in actions:
                result=[0]*len(subs)
                for j,m in enumerate(multiplicities): result[action[j]]=m
                forms.append(tuple(result))
            counts[used].add(min(forms))
            return
        for m in range(remaining//weights[i]+1):
            multiplicities[i]=m
            visit(i+1,remaining-m*weights[i],used+m*weights[i],
                  kernel & subs[i] if m else kernel,
                  sign ^ characters[i] if m%2 else sign)
        multiplicities[i]=0
    visit(0,limit,0,frozenset(range(size)),0)
    return list(map(len,counts))


def main():
    limit=24; result={}
    for rank in (2,3,4):
        symmetric=formula(rank,limit)
        alternating=formula(rank,limit,True)
        if rank <= 3:
            stop=12 if rank == 3 else 16
            assert direct_orbit_count(rank,stop) == symmetric[:stop+1]
            assert direct_orbit_count(rank,stop,True) == alternating[:stop+1]
        result[str(rank)]={'symmetric_point_conjugacy':symmetric,
                           'alternating_elements_point_conjugacy':alternating}
    # Independent two-variable geometric-series formulas from the pair proof.
    from commuting_pairs_formula_check import series
    s,a=series(limit//2)
    assert result['2']['symmetric_point_conjugacy'] == [s[n//2] for n in range(limit+1)]
    assert result['2']['alternating_elements_point_conjugacy'] == [a[n//2] for n in range(limit+1)]
    report={'status':'PASS','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'degree_range':[0,limit], 'counts':result,
            'scope':'Independent marked generators, modulo point conjugacy and S_r relabeling; exceptional outer automorphisms not included.',
            'independent_direct_checks':{'rank2_degrees':[0,16],'rank3_degrees':[0,12]}}
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
