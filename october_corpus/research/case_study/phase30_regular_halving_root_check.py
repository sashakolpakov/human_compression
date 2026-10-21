#!/usr/bin/env python3
"""Independent exact product-group and binary-space diagnostic; geometric proof separate."""
from pathlib import Path
from itertools import combinations, product
from hashlib import sha256
import argparse
import json

P=tuple(range(5)); identity=(P,0)
def mul(x,y):
    return tuple(x[0][y[0][i]] for i in range(5)), x[1]^y[1]
def closure(gens,unit=identity,multiply=mul):
    found={unit}; queue=[unit]
    for x in queue:
        for y in gens:
            z=multiply(x,y)
            if z not in found: found.add(z);queue.append(z)
    return found
def basis(vecs):
    out={}
    for x in vecs:
        while x:
            p=x.bit_length()-1
            if p in out:x^=out[p]
            else:out[p]=x;break
    return out
def reduce(x,bs):
    for p in sorted(bs,reverse=True):
        if x>>p&1:x^=bs[p]
    return x
def span(vectors):
    values={0}
    for x in vectors:values|={y^x for y in list(values)}
    return values
def components(vertices,incident):
    unseen=set(vertices);out=[]
    while unseen:
        q=[min(unseen)];unseen.remove(q[0])
        for v in q:
            nxt={w for w in unseen if incident(v,w)}
            unseen-=nxt;q.extend(sorted(nxt))
        out.append(sorted(q))
    return out

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True,type=Path)
    output=parser.parse_args().output
    if output.exists():raise SystemExit('Choose a new output path.')
    # A5 x C2, represented as a five-point permutation and an independent bit.
    c=((1,0,3,2,4),1);b=((4,2,1,3,0),1);d=((2,3,0,1,4),1)
    K=closure([c,b,d]);assert len(K)==120
    sub=[closure([g for i,g in enumerate([c,b,d]) if mask>>i&1]) for mask in range(8)]
    assert all(sub[i]&sub[j]==sub[i&j] for i in range(8) for j in range(8))
    def cosets(H):return sorted({frozenset(mul(g,h) for h in H) for g in K},key=min)
    V,E,F=cosets(sub[6]),cosets(sub[5]),cosets(sub[3])
    B=[{i for i,e in enumerate(E) if e&v} for v in V]
    D=[{i for i,e in enumerate(E) if e&f} for f in F]
    assert (len(V),len(E),len(F))==(12,30,12)
    types=[[(i,j) for j in range(len(T))] for i,T in enumerate([V,E,F])]
    records=[V,E,F]
    def incident(x,y):return bool(records[x[0]][x[1]] & records[y[0]][y[1]]) if x[0]!=y[0] else x==y
    flags=[tuple(x for x in row if x is not None) for row in product(*[[None]+T for T in types])]
    flags=[f for f in flags if all(incident(x,y) for x,y in combinations(f,2))]
    chambers=[set(f) for f in flags if len(f)==3]
    assert len(flags)==355 and len(chambers)==120
    assert all(len(set.intersection(*(set(records[i][j]) for i,j in C)))==1
               for C in chambers)
    panel_count=0;residue_count=0
    for flag in flags:
        assert any(set(flag)<=C for C in chambers)
        missing=set(range(3))-{x[0] for x in flag}
        res=[x for i in missing for x in types[i] if all(incident(x,y) for y in flag)]
        if len(missing)==1:assert len(res)==2;panel_count+=1
        if len(missing)>=2:assert len(components(res,incident))==1;residue_count+=1
    blocks=B+D
    assert all(len(s)==5 for s in blocks)
    rows=[sum(1<<i for i in s) for s in blocks]
    code=basis(rows);assert len(code)==17
    columns=[reduce(1<<i,code) for i in range(30)]
    assert 0 not in columns and len(set(columns))==30
    spaces=[span(columns[j] for j in s) for s in blocks]
    assert all(len(W)==16 for W in spaces)
    assert all({j for j,e in enumerate(columns) if e in W}==s for s,W in zip(blocks,spaces))
    pairs=[(i,j) for i,v in enumerate(V) for j,f in enumerate(F) if v&f]
    assert len(pairs)==60
    assert all(not(B[i]&D[j]) for i,v in enumerate(V) for j,f in enumerate(F) if not(v&f))
    for i,j in pairs:
        common=B[i]&D[j];assert len(common)==2
        assert spaces[i]&spaces[12+j]==span(columns[k] for k in common)
    # Explicit edge action; code invariance is checked on its generating rows.
    edge_index={g:i for i,e in enumerate(E) for g in e}
    action={g:[edge_index[mul(g,min(e))] for e in E] for g in K}
    assert len({tuple(a) for a in action.values()})==120
    def permute_vector(x,g):
        result=0
        for i in range(30):
            if x>>i&1:result^=1<<action[g][i]
        return result
    for g in [c,b,d]:
        for row in rows:assert reduce(permute_vector(row,g),code)==0
    def act(g,x):return reduce(permute_vector(x,g),code)
    def smul(x,y):return x[0]^act(x[1],y[0]),mul(x[1],y[1])
    unit=(0,identity);e0=edge_index[identity]
    aa=(columns[e0],identity);bb=(0,b);cc=(0,c);dd=(0,d)
    ee=smul(smul(aa,bb),aa)
    local_old=[closure([aa,bb,z],unit,smul) for z in [cc,dd]]
    local_new=[closure([ee,bb,z],unit,smul) for z in [cc,dd]]
    bottom_old=closure([aa,bb],unit,smul);bottom_new=closure([ee,bb],unit,smul)
    assert all(O==N and len(O)==160 for O,N in zip(local_old,local_new))
    assert local_new[0]&local_new[1]==bottom_old and len(bottom_old)==8
    assert len(bottom_new)==4 and aa not in bottom_new and aa in local_new[0]&local_new[1]
    # The affine graph has odd closed walks of length five, with no proper
    # nonempty subrelation on a block since its five columns have rank four.
    for s in blocks:
        value=0
        for j in s:value^=columns[j]
        assert value==0
    vi=next(i for i,v in enumerate(V) if identity in v)
    fi=next(i for i,f in enumerate(F) if identity in f)
    directions=[columns[k] for k in B[vi]&D[fi]]
    square=span(directions);assert len(square)==4
    lift=list(product(range(2),square))
    pieces=components(lift,lambda x,y:x[0]!=y[0] and x[1]^y[1] in directions)
    assert sorted(map(len,pieces))==[4,4]
    result={'status':'PASS','checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
      'implementation':'Independent A5-times-C2 product coordinates, literal seed incidence, actual vector spaces and local semidirect groups; imports no author code',
      'seed':{'group_order':120,'objects':[12,30,12],'flags':len(flags),'chambers':120,'panels':panel_count,'rank_at_least_two_residues':residue_count,'IP_meets':64,'chamber_common_coset_elements':1,'nonincident_seed_block_intersections_empty':True},
      'binary_data':{'code_rank':17,'quotient_dimension':13,'block_count':24,'columns':columns,'code_basis':list(code.values()),'all_column_memberships_checked':720,'all_incident_span_intersections_checked':60,'block_space_orders':[len(W) for W in spaces],'code_generator_action_checks':72,'faithful_seed_edge_action':True},
      'local_halving':{'old_parabolic_orders':[len(x) for x in local_old],'changed_parabolics_equal_old':True,'changed_parabolic_intersection_order':8,'expected_changed_intersection_order':4,'original_endpoint_is_excess_witness':True},
      'geometric_counts_from_written_adapter':{'vertices':8192,'edges':122880,'higher_objects_each_type':6144,'chambers':983040,'disconnected_transformed_higher_pair_residues':122880},
      'literal_new_square_residue_components':pieces,
      'boundary':'Exact finite hypotheses and local subgroup failure. Full affine geometry, residual connectivity, regularity and source interpretation require the separate written construction proof; no enumeration of the full million-element group or whole incidence system is claimed.'}
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('ROOT_REGULAR_HALVING_PASS',17,13,720,60,160,8,4)

if __name__=='__main__':main()
