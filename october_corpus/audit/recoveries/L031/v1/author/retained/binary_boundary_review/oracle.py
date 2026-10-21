"""Optional independent binary-coordinate validation, not a proof premise.

Enumerates images of the different basis e_i+e_n, not the author's path basis.
No GAP, group-order tables, author implementation or cached groups are used.
"""
from itertools import permutations
from math import factorial

def need(ok, message):
    if not ok:
        raise ValueError(message)

def dot(x,y):
    return (x & y).bit_count() % 2

def quadratic(x):
    need(x.bit_count()%2 == 0, 'quadratic form domain is even weight')
    return (x.bit_count()//2)%2

def permute(x,p):
    return sum(1 << p[i] for i in range(len(p)) if (x >> i)&1)

def closure(gens,n):
    one=tuple(range(n)); found={one}; todo=[one]
    while todo:
        x=todo.pop()
        for g in gens:
            y=tuple(g[x[i]] for i in range(n))
            if y not in found:
                found.add(y);todo.append(y)
    return found

def examine(n):
    need(type(n) is int and n in (4,5,6), 'bounded optional oracle n=4,5,6')
    d=n-1; E=[x for x in range(1<<n) if x.bit_count()%2==0]
    basis=[(1<<i)|(1<<(n-1)) for i in range(d)]
    candidates=[x for x in E if quadratic(x)==1]
    radical=[x for x in E if all(dot(x,y)==0 for y in E)]
    for x in E:
        for y in E:
            need(quadratic(x^y)^quadratic(x)^quadratic(y)==dot(x,y),'literal polar identity')
    frames=set()
    def recurse(images,span):
        if len(images)==d:
            frame=tuple(images)
            # Full-vector check, independent of relying on the Gram criterion.
            for mask in range(1<<d):
                x=y=0
                for i in range(d):
                    if (mask>>i)&1:
                        x ^= basis[i]; y ^= images[i]
                need(quadratic(x)==quadratic(y),'all-vector isometry')
            frames.add(frame);return
        for y in candidates:
            if y not in span and all(dot(x,y)==1 for x in images):
                recurse(images+[y],span|{x^y for x in span})
    recurse([],{0})
    coordinate_frames={tuple(permute(x,p) for x in basis) for p in permutations(range(n))}
    need(len(coordinate_frames)==factorial(n),'faithful coordinate action')
    need(frames==coordinate_frames,'all isometries are coordinate permutations')
    gens=[]
    for i in range(d):
        p=list(range(n));p[i],p[i+1]=p[i+1],p[i];gens.append(tuple(p))
        v=(1<<i)|(1<<(i+1))
        for x in E:
            need(permute(x,p)==x^(v if dot(x,v) else 0),'literal source symmetry formula')
    subgroups=[closure([g for i,g in enumerate(gens) if (mask>>i)&1],n) for mask in range(1<<d)]
    need(len(subgroups[-1])==factorial(n),'full generation')
    for i in range(1<<d):
        for j in range(1<<d):
            need(subgroups[i]&subgroups[j]==subgroups[i&j],'all subgroup intersections')
    return {'n':n,'dimension':d,'vectors':len(E),'nonsingular_vectors':len(candidates),
            'full_isometry_order':len(frames),'generated_order':len(subgroups[-1]),
            'radical_vectors':radical,'radical_Q':[quadratic(x) for x in radical],
            'all_intersection_pairs':(1<<d)**2,'complete_frame_enumeration':True}

def run():
    controls=[]
    for x in (0,1,2,7,'4',True):
        try:examine(x)
        except ValueError:controls.append(repr(x))
        else:raise ValueError('unsupported oracle parameter accepted')
    try:quadratic(1)
    except ValueError:controls.append('odd weight outside quadratic domain')
    else:raise ValueError('odd domain accepted')
    return {'status':'PASS_OPTIONAL_INDEPENDENT_COORDINATE_CHECK',
            'cases':[examine(n) for n in (4,5,6)],'domain_controls':controls,
            'author_code_imported':False,'proof_premise':False}

if __name__=='__main__':
    import json
    print(json.dumps(run(),indent=2))
