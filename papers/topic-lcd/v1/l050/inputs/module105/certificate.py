#!/usr/bin/env python3
"""Exact instances of the shared matrix, minimum-support and distance arguments."""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path
import numpy as np
from steiner_construction import graph105, dot4, mul4, need, srg_check
from shared_certificate import rref, permute, orbit, group_order, matrix_algebra, refinement_bound


def module_matrices(B, generators):
    B=np.array(B,dtype=np.int64)%3
    reduced,pivots=rref(B)
    need(np.array_equal(B,reduced),'systematic module basis')
    matrices=[]
    for g in generators:
        image=np.array([list(permute(bytes(row.tolist()),g))for row in B],dtype=np.int64)
        matrix=image[:,pivots]
        need(np.array_equal(matrix@B%3,image),'module invariance')
        matrices.append(matrix)
    return matrices,pivots


def span_vectors(seed, matrices, column=False):
    vectors=[seed.copy()]
    words=[[]]
    cursor=0
    while cursor<len(vectors):
        v=vectors[cursor]
        for i,M in enumerate(matrices):
            w=(M@v if column else v@M)%3
            if len(rref(vectors+[w])[0])>len(vectors):
                vectors.append(w);words.append(words[cursor]+[i+1])
        cursor+=1
    return vectors,words


def rank_one_algebra(matrices, terms, polynomial):
    d=len(matrices[0]);T=np.zeros((d,d),dtype=np.int64)
    for coefficient,word in terms:
        W=np.eye(d,dtype=np.int64)
        for i in word:
            need(1<=i<=len(matrices),'matrix generator word')
            W=W@matrices[i-1]%3
        T=(T+coefficient*W)%3
    P=np.zeros((d,d),dtype=np.int64)
    for coefficient in reversed(polynomial):
        P=(P@T+coefficient*np.eye(d,dtype=np.int64))%3
    need(len(rref(P)[0])==1,'rank-one algebra element')
    i,j=map(int,np.argwhere(P)[0])
    columns,left=span_vectors(P[:,j],matrices,True)
    rows,right=span_vectors(P[i,:],matrices,False)
    need(len(columns)==d and len(rows)==d,'left and right cyclic bases')
    return {'dimension':d*d,'rank_one':True,'left_dimension':d,'right_dimension':d,
            'left_words':left,'right_words':right}


def natural_complement():
    points=[v for v in itertools.product(range(4),repeat=3)
            if any(v) and next(x for x in v if x)==1]
    flags=[(p,l)for p in points for l in points if dot4(p,l)==0]
    pos={f:i for i,f in enumerate(flags)}
    inverse={1:1,2:3,3:2}
    def norm(v):
        a=inverse[next(x for x in v if x)]
        return tuple(mul4(a,x)for x in v)
    diagonal=[];field=[];duality=[]
    for p,l in flags:
        diagonal.append(pos[(norm((mul4(2,p[0]),p[1],p[2])),norm((mul4(3,l[0]),l[1],l[2])))]+1)
        field.append(pos[(tuple(mul4(x,x)for x in p),tuple(mul4(x,x)for x in l))]+1)
        duality.append(pos[(l,p)]+1)
    return [diagonal,field,duality]


def inspect(data, enumeration_dir, out):
    out.mkdir(parents=True,exist_ok=False)
    A=np.array(graph105(),dtype=np.int64)
    srg_check(A.tolist(),(105,72,51,45))
    points=[v for v in itertools.product(range(4),repeat=3)
            if any(v) and next(x for x in v if x)==1]
    flags=[(p,l)for p in points for l in points if dot4(p,l)==0]
    literal_degrees=[]
    for p,l in flags:
        conjunctive=disjunctive=0
        for q,m in flags:
            if (p,l)==(q,m):continue
            same=p==q or l==m;cross=dot4(p,m)==0 or dot4(q,l)==0
            conjunctive+=same and cross;disjunctive+=same or cross
        literal_degrees.append([conjunctive,disjunctive])
    need(literal_degrees==[[8,40]]*105,'literal source adjacency readings')
    C,cp=rref(A)
    D,dp=rref(A[1:]-A[0])
    need(len(C)==20 and len(D)==19,'code dimensions')
    need(not np.any(C@C.T%3),'self-orthogonality')
    need(np.array_equal(rref(np.vstack([D,np.ones(105,dtype=np.int64)]))[0],C),'internal constant direct sum')
    for name,B in [('adjacency',C),('differences',D)]:
        literal=f'105 {len(B)}\n'+''.join(''.join(map(str,r))+'\n'for r in B.tolist())
        need(literal.encode()==(enumeration_dir/f'bases/105_{name}.txt').read_bytes(),'retained exact basis '+name)
    generators=[[x-1 for x in row]for row in data['coordinate_generators']]
    need(all(sorted(g)==list(range(105))for g in generators),'permutation generators')
    for g in generators:
        need(np.array_equal(A[np.ix_(g,g)],A),'literal graph automorphism')
    CM,_=module_matrices(C,generators)
    DM,_=module_matrices(D,generators)
    algebra,words=matrix_algebra(DM)
    need(len(algebra)==361,'nineteen-dimensional full matrix algebra')
    minima=set();orbit_sizes=[]
    for s in data['minimum33_seeds']:
        seed=bytes(s);v=np.array(s,dtype=np.int64)
        need(sum(x!=0 for x in s)==33 and np.array_equal(v[cp]@C%3,v),'minimum33 seed')
        O=orbit(seed,generators)
        need(minima.isdisjoint(O),'disjoint minimum33 orbits')
        minima|=O;orbit_sizes.append(len(O))
    need(sorted(orbit_sizes)==[105,105,280,280] and len(minima)==770,'complete retained minimum33 count')
    supports=sorted({tuple(i for i,x in enumerate(w)if x)for w in minima})
    chain,upper=refinement_bound(supports,105)
    need(len(supports)==385 and chain==[[1,105],[2,8],[3,3],[4,2],[7,4],[12,3],[6,4]] and upper==241920,'full support bound')
    lower=group_order(generators,105,upper)
    need(lower==upper,'full group lower bound')
    E=np.array(data['filtration_basis'],dtype=np.int64)%3
    need(E.shape==(105,105),'filtration basis dimensions')
    inverse,pivots=rref(np.hstack([E,np.eye(105,dtype=np.int64)]))
    need(pivots==list(range(105)),'filtration basis nonsingular')
    inverse=inverse[:,105:]
    changed=[]
    for g in generators:
        image=np.array([list(permute(bytes(row.tolist()),g))for row in E],dtype=np.int64)
        changed.append(image@inverse%3)
    cuts=data['cuts']
    need(cuts==[0,1,20,39,84,85,104,105],'filtration cuts')
    for cut in cuts[1:-1]:
        need(all(not np.any(T[:cut,cut:])for T in changed),'invariant filtration')
    dimensions=[];algebras=[];rank_one=None;nineteen=[]
    for a,b in zip(cuts,cuts[1:]):
        d=b-a;matrices=[T[a:b,a:b]for T in changed];dimensions.append(d)
        if d==19:
            nineteen.append([M.tolist()for M in matrices])
        if d==45:
            rank_one=rank_one_algebra(matrices,data['terms'],data['polynomial'])
            algebras.append(rank_one['dimension'])
        else:
            generated,_=matrix_algebra(matrices);need(len(generated)==d*d,'simple filtration factor')
            algebras.append(len(generated))
    code20=[np.array(B,dtype=np.int64)for B in data['code20_bases']]
    need(len(code20)==3 and np.array_equal(code20[0],C),'three source modules')
    extra=[]
    for i,B in enumerate(code20):
        _,bp=module_matrices(B,generators)
        need(len(B)==20,'extra code dimension')
        has_D=len(rref(np.vstack([B,D]))[0])==20
        has_j=len(rref(np.vstack([B,np.ones(105,dtype=np.int64)]))[0])==20
        need((has_D,has_j)==[(True,True),(False,True),(True,False)][i],'distinct simple submodules of the three20-modules')
        if i:
            seed=bytes(data['extra_minimum_seeds'][i-1]);v=np.array(list(seed),dtype=np.int64)
            distance=[30,28][i-1]
            need(sum(x!=0 for x in seed)==distance and np.array_equal(v[bp]@B%3,v),'extra minimum seed')
            O=orbit(seed,generators);O|={bytes((-x)%3 for x in word)for word in O}
            need(len(O)==[672,720][i-1],'extra minimum candidate count')
            restricted=sum(sum(word[j]!=0 for j in bp)<=5 for word in O)
            extra.append({'id':i,'dimension':20,'distance':distance,'minimum_words':len(O),'restricted_minimum_count':restricted,'information_set':[x+1 for x in bp]})
            (out/f'extra{i}_basis.txt').write_text('105 20 3 5\n'+''.join(''.join(map(str,r))+'\n'for r in B.tolist()))
    gap=''.join(name+':='+repr(value)+';;\n'for name,value in [
        ('coordinate_generators',data['coordinate_generators']),('D_basis',D.tolist()),('C_basis',C.tolist()),
        ('D_matrices',[M.tolist()for M in DM]),('complement_generators',natural_complement()),
        ('nineteen_factors',nineteen),
        ('codes20',data['code20_bases'])])
    (out/'constructed.g').write_text(gap)
    (out/'rank_one_certificate.json').write_text(json.dumps(rank_one,indent=2)+'\n')
    (out/'supports.json').write_text(json.dumps([[x+1 for x in s]for s in supports],separators=(',',':'))+'\n')
    result={'status':'PASS','graph_parameters':[105,72,51,45],'C_dimension':20,'D_dimension':19,
            'literal_source_adjacency_degrees':[8,40],
            'self_orthogonal':True,'constant_direct_sum':True,'D_matrix_algebra':361,'minimum33_orbit_sizes':orbit_sizes,
            'minimum_supports':385,'refinement_chain':chain,'full_group_order':lower,
            'filtration_factor_dimensions':dimensions,'filtration_algebra_dimensions':algebras,
            'extra_codes_pending_distance_enumeration':extra}
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--enumeration-dir',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();print(json.dumps(inspect(json.loads(Path(__file__).with_name('module_data.json').read_text()),a.enumeration_dir,a.out),sort_keys=True))
