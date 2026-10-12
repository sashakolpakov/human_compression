#!/usr/bin/env python3
"""Literal finite incidence check for the residue-parity obstruction."""
from itertools import combinations, product
from collections import Counter
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json


def components(nodes, incident):
    todo=set(nodes); out=[]
    while todo:
        stack=[todo.pop()]; seen=set(stack)
        while stack:
            x=stack.pop()
            new={y for y in todo if incident(x,y)}
            todo-=new; seen|=new; stack.extend(new)
        out.append(frozenset(seen))
    return out


def audit(types, incident):
    flags=[]; chambers=[]; ext_fail=[]; rc_fail=[]; panels=Counter()
    for choices in product(*[[None]+v for v in types]):
        F=tuple(x for x in choices if x is not None)
        if not all(incident(x,y) for x,y in combinations(F,2)):
            continue
        flags.append(F)
        if len(F)==len(types): chambers.append(F)
    for F in flags:
        if not any(set(F)<=set(C) for C in chambers): ext_fail.append(F)
        missing=set(range(len(types)))-{x[0] for x in F}
        residue=[x for i in missing for x in types[i] if all(incident(x,y) for y in F)]
        if len(missing)==1: panels[len(residue)]+=1
        if len(missing)>=2:
            cs=components(residue,incident)
            if len(cs)!=1:rc_fail.append({'flag':F,'component_sizes':sorted(map(len,cs))})
    return {'objects':list(map(len,types)),'flags':len(flags),'chambers':len(chambers),
            'extension_failures':ext_fail,'residual_connectivity_failures':rc_fail,
            'panel_size_distribution':dict(sorted(panels.items()))}


def example(m):
    vertices=[(p,j) for p in range(4) for j in range(m)]
    edges=[frozenset([u,v]) for u,v in combinations(vertices,2) if u[0]!=v[0]]
    triangles=[frozenset(set(range(4))-{missing}) for missing in range(4)]
    base=[[ (0,u) for u in vertices],[(1,e) for e in edges],
          [(2,T) for T in triangles],[(3,T) for T in triangles]]
    def original(x,y):
        if x[0]==y[0]:return x==y
        if x[0]>y[0]:x,y=y,x
        if x[0]==0 and y[0]==1:return x[1] in y[1]
        if x[0]==0:return x[1][0] in y[1]
        if x[0]==1:return all(v[0] in y[1] for v in x[1])
        return True
    new=[[(i,u) for u in vertices] for i in [0,1]]+base[2:]
    def changed(x,y):
        if x[0]==y[0]:return x==y
        if x[0]>y[0]:x,y=y,x
        if y[0]<=1:return x[1][0]!=y[1][0]
        if x[0]<=1:return x[1][0] in y[1]
        return True
    # All single higher-object shadows contain a triangle, so Construction3.6
    # attaches exactly one parity class to each: no higher object is split.
    for T in triangles:
        selected=[next(v for v in vertices if v[0]==p) for p in T]
        assert len(selected)==3 and all(u[0]!=v[0] for u,v in combinations(selected,2))
    # B1: exact distinct endpoint sets, simple graph. B2: edge incidence iff
    # both endpoint vertices belong to each higher shadow.
    assert len(edges)==6*m*m and all(len(e)==2 for e in edges)
    for edge in base[1]:
        for x in base[2]+base[3]:
            assert original(edge,x)==all(original((0,v),x) for v in edge[1])
    old_report=audit(base,original);new_report=audit(new,changed)
    assert not old_report['extension_failures'] and not old_report['residual_connectivity_failures']
    assert not new_report['extension_failures']
    failures=new_report['residual_connectivity_failures']
    assert len(failures)==12
    assert all(len(x['flag'])==2 and {y[0] for y in x['flag']}=={2,3}
               and x['flag'][0][1]!=x['flag'][1][1] and x['component_sizes']==[2*m,2*m]
               for x in failures)
    if m==2: assert min(old_report['panel_size_distribution'])==2
    return {'part_size':m,'B1':True,'B2':True,'original':old_report,'partitioned':new_report}


def encode(x):
    if isinstance(x,(set,frozenset)):return sorted(x)
    raise TypeError(type(x).__name__)

rows=[example(1),example(2)]
report={'date_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS',
        'checker_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'scope':'All flags and residues in two literal finite geometries; no claim about thin or flag-transitive starting geometries.',
        'examples':rows}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,default=encode,indent=2)+'\n')
for row in rows:
    print('PARITY_SHADOW_COUNTEREXAMPLE_PASS',row['part_size'],row['original']['flags'],row['original']['chambers'],
          row['original']['panel_size_distribution'],len(row['partitioned']['residual_connectivity_failures']))
