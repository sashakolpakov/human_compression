#!/usr/bin/env python3
"""Exact finite hypotheses and local witnesses for the affine regular hypertope."""
from itertools import combinations, product
from pathlib import Path
from hashlib import sha256
import json
import argparse


def perm(*cycles):
    out = list(range(7))
    for cycle in cycles:
        for x, y in zip(cycle, cycle[1:] + cycle[:1]):
            out[x-1] = y-1
    return tuple(out)


def mul(g, h):
    return tuple(g[h[i]] for i in range(7))


one = tuple(range(7))
c = perm((1,2), (3,4), (6,7))
b = perm((1,5), (2,3), (6,7))
d = perm((1,3), (2,4), (6,7))


def closure(gens):
    found = {one}; todo = [one]
    while todo:
        g = todo.pop()
        for h in gens:
            x = mul(g, h)
            if x not in found:
                found.add(x); todo.append(x)
    return frozenset(found)


def span_basis(words):
    basis = {}
    for word in words:
        while word:
            p = word.bit_length()-1
            if p in basis:
                word ^= basis[p]
            else:
                basis[p] = word
                break
    return tuple(basis[p] for p in sorted(basis, reverse=True))


def reduce(word, basis):
    for pivot in basis:
        if word.bit_length() == pivot.bit_length():
            word ^= pivot
        elif word & (1 << (pivot.bit_length()-1)):
            word ^= pivot
    return word


def left_cosets(K, H):
    unseen = set(K); out = []
    while unseen:
        g = min(unseen)
        coset = frozenset(mul(g, h) for h in H)
        out.append(coset); unseen -= coset
    return out


def span(words):
    values = {0}
    for word in words:
        values |= {x ^ word for x in tuple(values)}
    return frozenset(values)


def components(objects, incident):
    unseen = set(objects)
    result = []
    while unseen:
        queue = [min(unseen)]; unseen.remove(queue[0])
        for obj in queue:
            neighbors = {x for x in unseen if incident(obj, x)}
            unseen -= neighbors; queue.extend(sorted(neighbors))
        result.append(queue)
    return result


def order(g, multiply=mul, identity=one):
    power = identity; value = 0
    while True:
        power = multiply(power, g); value += 1
        if power == identity:
            return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit('Choose a new output path; existing certificates are not overwritten.')
    K = closure([c,b,d])
    parabolics = [closure([x for i,x in enumerate([c,b,d]) if mask >> i & 1])
                  for mask in range(8)]
    assert len(K) == 120
    assert all(parabolics[i] & parabolics[j] == parabolics[i & j]
               for i in range(8) for j in range(8))
    assert [order(mul(x,y)) for x,y in [(c,b),(b,d),(c,d)]] == [5,5,2]
    R = closure([c,d]); V = closure([b,d]); F = closure([c,b])
    edge_cosets = left_cosets(K,R)
    vertices = left_cosets(K,V); faces = left_cosets(K,F)
    assert (len(edge_cosets),len(vertices),len(faces)) == (30,12,12)
    seed_types = [vertices,edge_cosets,faces]
    seed_objects = [[(i,j) for j in range(len(T))] for i,T in enumerate(seed_types)]
    def incident(x,y):
        return (x == y) if x[0] == y[0] else bool(seed_types[x[0]][x[1]] & seed_types[y[0]][y[1]])
    flags = [tuple(x for x in row if x is not None)
             for row in product(*[[None]+T for T in seed_objects])]
    flags = [flag for flag in flags if all(incident(x,y) for x,y in combinations(flag,2))]
    chambers = [frozenset(flag) for flag in flags if len(flag)==3]
    assert len(flags)==355 and len(chambers)==120
    panel_count = residue_count = 0
    for flag in flags:
        assert any(set(flag) <= chamber for chamber in chambers)
        absent = set(range(3)) - {x[0] for x in flag}
        residue = [x for i in absent for x in seed_objects[i]
                   if all(incident(x,y) for y in flag)]
        if len(absent)==1:
            assert len(residue)==2; panel_count += 1
        if len(absent)>=2:
            assert len(components(residue,incident))==1; residue_count += 1
    # A unique common group element for every chamber proves the literal
    # left-coset action is free and transitive, with no C-group shortcut.
    assert all(len(set.intersection(*(set(seed_types[i][j]) for i,j in chamber)))==1
               for chamber in chambers)
    vertex_blocks = [tuple(i for i,e in enumerate(edge_cosets) if e & v) for v in vertices]
    face_blocks = [tuple(i for i,e in enumerate(edge_cosets) if e & f) for f in faces]
    blocks = vertex_blocks + face_blocks
    assert all(len(B)==5 for B in blocks)
    incident_pairs = [(i,j) for i,v in enumerate(vertices) for j,f in enumerate(faces) if v & f]
    assert len(incident_pairs)==60
    assert all(len(set(vertex_blocks[i]) & set(face_blocks[j]))==2 for i,j in incident_pairs)
    assert all(not(set(vertex_blocks[i]) & set(face_blocks[j]))
               for i,v in enumerate(vertices) for j,f in enumerate(faces) if not(v & f))
    rows = [sum(1 << i for i in B) for B in blocks]
    code = span_basis(rows)
    assert len(code)==17
    columns = [reduce(1 << i,code) for i in range(30)]
    assert all(columns) and len(set(columns))==30
    block_spaces = [span(columns[i] for i in B) for B in blocks]
    assert all(len(W)==16 for W in block_spaces)
    assert all({i for i,q in enumerate(columns) if q in W}==set(B)
               for B,W in zip(blocks,block_spaces))
    intersections = []
    for i,j in incident_pairs:
        shared = sorted(set(vertex_blocks[i]) & set(face_blocks[j]))
        expected = span(columns[e] for e in shared)
        assert len(expected)==4 and block_spaces[i] & block_spaces[12+j]==expected
        intersections.append({'vertex':i,'face':j,'edges':shared,'space':sorted(expected)})
    for B in blocks:
        value = 0
        for e in B:
            value ^= columns[e]
        assert value==0
        # Rank four and exactly one five-term dependence imply a simple odd cycle.
        assert len(span_basis(columns[e] for e in B))==4
    edge_of = {g:i for i,E in enumerate(edge_cosets) for g in E}
    actions = {g:tuple(edge_of[mul(g,min(E))] for E in edge_cosets) for g in K}
    assert len(set(actions.values()))==120
    def permute(word,g):
        value = 0
        for i in range(30):
            if word >> i & 1:
                value ^= 1 << actions[g][i]
        return value
    assert all(reduce(permute(row,g),code)==0 for g in [c,b,d] for row in rows)
    def act(g,q):
        return reduce(permute(q,g),code)
    # All 51 action checks on a code basis also bind the induced linear action.
    assert all(reduce(permute(row,g),code)==0 for g in [c,b,d] for row in code)
    free_positions = [i for i in range(30) if i not in {r.bit_length()-1 for r in code}]
    assert len(free_positions)==13
    def compress(word):
        assert all(not(word >> (r.bit_length()-1) & 1) for r in code)
        return sum(((word >> i)&1) << j for j,i in enumerate(free_positions))
    compressed_columns = [compress(q) for q in columns]
    action_matrices = [[compress(act(g,1 << p)) for p in free_positions] for g in [c,b,d]]
    base_edge = edge_of[one]
    a = (columns[base_edge],one)
    bb,cc,dd = [(0,g) for g in [b,c,d]]
    identity = (0,one)
    def smul(x,y):
        return x[0] ^ act(x[1],y[0]),mul(x[1],y[1])
    def sclosure(gens):
        found={identity}; queue=[identity]
        for g in queue:
            for h in gens:
                x=smul(g,h)
                if x not in found:
                    found.add(x);queue.append(x)
        return frozenset(found)
    aprime = smul(smul(a,bb),a)
    old_local = [sclosure([a,bb,h]) for h in [cc,dd]]
    new_local = [sclosure([aprime,bb,h]) for h in [cc,dd]]
    old_bottom = sclosure([a,bb]); new_bottom = sclosure([aprime,bb])
    assert all(O==H and len(O)==160 for O,H in zip(old_local,new_local))
    assert new_local[0] & new_local[1] == old_bottom and len(old_bottom)==8
    assert len(new_bottom)==4 and a in new_local[0] & new_local[1] and a not in new_bottom
    marked_orders = [order(smul(x,y),smul,identity)
                     for x,y in [(a,bb),(bb,cc),(bb,dd),(a,cc),(a,dd),(cc,dd)]]
    assert marked_orders==[4,5,5,2,2,2]
    vi = next(i for i,Vv in enumerate(vertices) if one in Vv)
    fi = next(i for i,Ff in enumerate(faces) if one in Ff)
    directions = [columns[e] for e in set(vertex_blocks[vi]) & set(face_blocks[fi])]
    square = span(directions)
    doubled = list(product(range(2),square))
    pieces = components(doubled,lambda x,y:x[0]!=y[0] and x[1]^y[1] in directions)
    assert sorted(map(len,pieces))==[4,4]
    record = {
        'status':'PASS','checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'implementation':'stdlib exact permutations, full seed incidence, binary linear algebra, explicit local semidirect products',
        'marking_1_based':[[x+1 for x in g] for g in [c,b,d]],
        'seed':{'group_order':120,'parabolic_orders':[len(P) for P in parabolics],
                'IP_meets':64,'object_counts':[12,30,12],'flags':len(flags),'chambers':len(chambers),
                'panels':panel_count,'rank_at_least_two_residues':residue_count,
                'literal_flag_completion':True,'chamber_regular':True},
        'edge_coset_representatives_1_based':[[x+1 for x in min(E)] for E in edge_cosets],
        'base_edge_index':base_edge,'vertex_blocks':vertex_blocks,'face_blocks':face_blocks,
        'incident_pairs':incident_pairs,'code_basis_30bit':code,'code_dimension':17,
        'quotient_dimension':13,'free_coordinate_positions':free_positions,
        'columns_30bit':columns,'columns_13bit':compressed_columns,
        'quotient_generator_action_columns_13bit':action_matrices,
        'edge_generator_permutations':[actions[g] for g in [c,b,d]],
        'code_generator_invariance_checks':72,'code_basis_invariance_checks':51,
        'faithful_seed_edge_action':True,'block_space_orders':[len(W) for W in block_spaces],
        'column_membership_tests':720,'literal_span_intersections':intersections,
        'odd_five_term_relations':24,
        'local_halving':{'old_orders':[len(O) for O in old_local],
                        'changed_parabolics_equal_old':True,'intersection_order':8,
                        'expected_intersection_order':4,'endpoint_is_excess_witness':True,
                        'marked_product_orders':marked_orders},
        'new_square_residue_components':pieces,
        'derived_geometric_counts':{'vertices':8192,'edges':122880,'higher_objects_each':6144,
                                    'chambers':983040,'bad_new_higher_pair_residues':122880},
        'scope':'Checks every finite hypothesis and the local subgroup failure. Global geometry, residual connectivity, regularity and derived counts use phase30_affine_map.md. No full global group or geometry enumeration.'}
    args.output.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print('AFFINE_MAP_PASS seed=120 flags=355 code=17 quotient=13 memberships=720 intersections=60 local=160,160 meet=8>4')


if __name__=='__main__':
    main()
