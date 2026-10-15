"""Independent matrix closure, set incidence and invariant-equivalence checks.

No author Python/GAP helper is imported.  Saved records are comparison data.
"""
import sys
if sys.flags.optimize:
    raise RuntimeError('ordinary Python required')
from array import array
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path
import time

def require(ok, message):
    if not ok:
        raise ValueError(message)

MULT = ((0,0,0,0),(0,1,2,3),(0,2,3,1),(0,3,1,2))
INV = (0,1,3,2)
def normal(v):
    scalar = INV[next(x for x in v if x)]
    return tuple(MULT[scalar][x] for x in v)

def field_dot(a,b):
    return MULT[a[0]][b[0]] ^ MULT[a[1]][b[1]] ^ MULT[a[2]][b[2]]

def determinant(a,b,c):
    return (MULT[a[0]][MULT[b[1]][c[2]] ^ MULT[b[2]][c[1]]]
            ^ MULT[a[1]][MULT[b[0]][c[2]] ^ MULT[b[2]][c[0]]]
            ^ MULT[a[2]][MULT[b[0]][c[1]] ^ MULT[b[1]][c[0]]])

def members(mask):
    return frozenset(i for i in range(21) if mask & (1 << i))

def matrix_group():
    identity = (1,0,0,0,1,0,0,0,1)
    found = {identity}; queue = [identity]
    for m in queue:
        # Right multiplication by the two displayed determinant-one matrices.
        diagonal = tuple(MULT[x][(1,2,3)[i % 3]] for i,x in enumerate(m))
        cycle = tuple(y for i in (0,3,6) for y in (m[i+1],m[i+2],m[i]^m[i+2]))
        for n in (normal(diagonal), normal(cycle)):
            if n not in found:
                found.add(n); queue.append(n)
    require(len(queue)==20160, 'complete projective matrix closure')
    require(all(determinant(m[:3],m[3:6],m[6:])==1 for m in queue), 'all determinants one')
    return queue

def connected(vertices, edges):
    vertices = set(vertices)
    seen = {min(vertices)}
    todo = list(seen)
    for x in todo:
        for y in edges(x):
            if y not in seen:
                seen.add(y); todo.append(y)
    return seen == vertices

def primitive(stabilizer, action, domain):
    """Generate the invariant equivalence joining each actual point pair.

    Complete group elements are available; no point-stabilizer orbit routine
    or author's orbital graph implementation supplies this calculation.
    """
    n = len(domain)
    require(n>=2, 'firm domain')
    position = {x:i for i,x in enumerate(domain)}
    x = domain[0]
    require({action[g][x] for g in stabilizer}==set(domain), 'literal transitivity')
    for y in domain[1:]:
        parent = list(range(n)); components = n
        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]; a=parent[a]
            return a
        for g in stabilizer:
            a = find(position[action[g][x]])
            b = find(position[action[g][y]])
            if a != b:
                parent[a] = b; components -= 1
                if components == 1:
                    break
        if components != 1:
            return False
    return True

def incident(i,a,j,b,variant):
    if i > j:
        return incident(j,b,i,a,variant)
    if i == 0:
        return bool(a & b) if j==3 and variant=='5.1' else not (a & b)
    if i == 1:
        return a <= b
    if (i,j)==(2,3):
        return len(a & b)==3
    if j == 4:
        return b <= a
    raise ValueError('unknown type relation')

def flags(types, objects, adjacency):
    # Reverse the author's type order; use literal sets rather than bit masks.
    order = tuple(reversed(types))
    rows = []
    def visit(chosen):
        if len(chosen)==len(order):
            rows.append(tuple(chosen[t] for t in types)); return
        t = order[len(chosen)]
        possible = set(range(len(objects[t])))
        for u,v in chosen.items():
            possible.intersection_update(adjacency[u,t][v])
        for v in sorted(possible):
            visit({**chosen,t:v})
    visit({})
    return rows

def certify(expected, objects, actions, group_size, variant):
    types = tuple(t-1 for t in expected['retained_types'])
    adjacency = {(i,j):[frozenset(b for b,y in enumerate(objects[j])
                                  if incident(i,x,j,y,variant))
                        for x in objects[i]]
                 for i in types for j in types if i!=j}
    chambers = flags(types,objects,adjacency)
    require(len(chambers)==expected['chambers'], 'chamber number')
    base = dict(zip(types,max(chambers)))
    orbit = {tuple(actions[t][g][base[t]] for t in types) for g in range(group_size)}
    require(orbit==set(chambers), 'actual complete chamber orbit')
    by_flag = {tuple(r['types']):r for r in expected['flag_rows']}
    by_residue = {tuple(r['fixed_types']):r for r in expected['residue_rows']}
    primitive_checks = pair_checks = flag_count = 0
    for size in range(len(types)+1):
        for fixed in it.combinations(types,size):
            complete_flags = flags(fixed,objects,adjacency)
            projected = {tuple(c[types.index(t)] for t in fixed) for c in chambers}
            require(set(complete_flags)==projected, 'every partial flag extends')
            row = by_flag[fixed]
            require(len(complete_flags)==row['count'], 'complete flag count')
            stabilizer = [g for g in range(group_size)
                          if all(actions[t][g][base[t]]==base[t] for t in fixed)]
            require(len(stabilizer)==row['stabilizer_order'], 'actual flag stabilizer')
            flag_count += len(complete_flags)
            remaining = tuple(t for t in types if t not in fixed)
            if not remaining:
                continue
            domains = {}
            for t in remaining:
                allowed = set(range(len(objects[t])))
                for u in fixed:
                    allowed.intersection_update(adjacency[u,t][base[u]])
                domains[t] = sorted(allowed)
                require(len(allowed)==row['extensions'][str(t)], 'literal extensions')
            if len(remaining)>=2:
                vertices = [(t,v) for t in remaining for v in domains[t]]
                require(connected(vertices,lambda tv:((u,w) for u in remaining if u!=tv[0]
                    for w in domains[u] if w in adjacency[tv[0],u][tv[1]])), 'residue connectivity')
            actual_primitive=[]; actual_two=[]
            for t in remaining:
                domain=domains[t]
                actual_primitive.append(primitive(stabilizer,actions[t],domain))
                actual_two.append({actions[t][g][domain[1]] for g in stabilizer
                    if actions[t][g][domain[0]]==domain[0]}==set(domain[1:]))
                primitive_checks+=1
            saved=by_residue[fixed]
            require(actual_primitive==saved['primitive_actions'], 'invariant-equivalence primitive flags')
            require(actual_two==saved['two_transitive_actions'], 'literal double transitivity')
            require(any(actual_primitive), 'residue weak primitivity')
            if len(remaining)==2:
                i,j=remaining; right=set(domains[j])
                neighbours=[adjacency[i,j][x] & right for x in domains[i]]
                complete=all(n==right for n in neighbours)
                linear=all(len(a&b)<=1 for a,b in it.combinations(neighbours,2))
                require((complete or linear)==saved['IP2_if_rank_two']==True, 'IP2 set test')
                pair_checks+=len(neighbours)*(len(neighbours)-1)//2
    return dict(model=variant,source_label=expected['source_label'],chambers=len(chambers),
                flags=flag_count,primitive_actions=primitive_checks,neighbour_pairs=pair_checks)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--packet',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    require(not args.out.exists(),'fresh output')
    args.out.mkdir(parents=True); started=time.monotonic()
    directory=args.packet/'expected'; data=json.loads((directory/'model.json').read_text())
    points=sorted({normal(v) for v in it.product(range(4),repeat=3) if any(v)})
    require(points==[tuple(x) for x in data['coordinate_points']],'coordinate points')
    labels=tuple(data['coordinate_to_retained']); require(sorted(labels)==list(range(21)),'label bijection')
    coordinate_lines={frozenset(labels[i] for i,v in enumerate(points) if field_dot(a,v)==0) for a in points}
    lines=[members(x) for x in data['lines']]
    require(coordinate_lines==set(lines),'every coordinate line')
    # Independently test collinearity by 3x3 determinants, not line masks.
    good=set(); tested=0
    for six in it.combinations(range(21),6):
        tested+=1
        if all(determinant(*(points[i] for i in triple))!=0 for triple in it.combinations(six,3)):
            good.add(frozenset(labels[i] for i in six))
    hypers=[list(map(members,o)) for o in data['hyperoval_orbits']]
    require(len(good)==168 and set().union(*map(set,hypers))==good,'complete determinant hyperovals')
    matrices=matrix_group(); point_index={v:i for i,v in enumerate(points)}
    permutations=[]
    for matrix in matrices:
        rows=(matrix[:3],matrix[3:6],matrix[6:]); p=[None]*21
        for i,v in enumerate(points):
            p[labels[i]]=labels[point_index[normal(tuple(field_dot(row,v) for row in rows))]]
        permutations.append(tuple(p))
    require(len(set(permutations))==20160,'faithful projective matrix action')
    specified=((1,0,0,0,2,0,0,0,3),(0,0,1,1,0,0,0,1,1))
    require([tuple(g) for g in data['retained_generators']]
            == [permutations[matrices.index(m)] for m in specified],
            'both actual retained generators equal the displayed matrices')
    for hyperoval_class in hypers:
        first=hyperoval_class[0]
        require({frozenset(p[i] for i in first) for p in permutations}==set(hyperoval_class),'literal orbit from matrices')
    objects=[lines,[frozenset([i]) for i in range(21)],hypers[0],hypers[1],
             [frozenset(pair) for pair in it.combinations(range(21),2)]]
    actions=[]
    for domain in objects:
        index={obj:i for i,obj in enumerate(domain)}
        actions.append([array('H',(index[frozenset(p[i] for i in obj)] for obj in domain)) for p in permutations])
    print('PASS_INDEPENDENT_PLANE_AND_MATRIX_GROUP',flush=True)
    records=[]
    expected=[json.loads((directory/('model_'+v+'.json')).read_text()) for v in ['5.1','5.2']]
    expected+=json.loads((directory/'truncations.json').read_text())
    for e in expected:
        r=certify(e,objects,actions,len(matrices),e['model']);records.append(r)
        print('PASS_INDEPENDENT_CONSTRUCTION',r,flush=True)
    result=dict(status='PASS_INDEPENDENT_L100_PROJECTIVE_CONSTRUCTIONS',six_subsets=tested,
        hyperovals=len(good),projective_matrices=len(matrices),records=records,
        seconds=time.monotonic()-started,author_helpers_imported=False,whole_source_credit=0)
    (args.out/'report.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':
    main()
