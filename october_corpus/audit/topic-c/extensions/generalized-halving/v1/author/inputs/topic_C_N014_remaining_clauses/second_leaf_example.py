"""Literal finite incidence example for the second-leaf criterion.

This optional diagnostic imports no previous construction code. The written
proof gives the general criterion and proves the example independently.
"""
from itertools import product, combinations
from pathlib import Path
import argparse
import json

def need(value, message):
    if not value:
        raise ValueError(message)

def flags(types, inc):
    return [tuple(x for x in row if x is not None)
            for row in product(*([None]+list(t) for t in types))
            if all(inc(x,y) for x,y in combinations([x for x in row if x is not None],2))]

def connected(vertices, inc):
    if not vertices:
        return False
    seen={vertices[0]}; todo=[vertices[0]]
    while todo:
        x=todo.pop()
        for y in vertices:
            if y not in seen and inc(x,y):
                seen.add(y);todo.append(y)
    return len(seen)==len(vertices)

def audit(types, inc):
    all_flags=flags(types,inc)
    chambers=[f for f in all_flags if len(f)==len(types)]
    need(all(any(set(f)<=set(c) for c in chambers) for f in all_flags),'every flag extends')
    checked=0
    for f in all_flags:
        missing=[i for i in range(len(types)) if i not in {x[0] for x in f}]
        if len(missing)<2:
            continue
        residue=[x for i in missing for x in types[i] if all(inc(x,y) for y in f)]
        need(connected(residue,inc),'connected residue '+repr(f));checked+=1
    return {'objects':list(map(len,types)),'flags':len(all_flags),'chambers':len(chambers),'connected_residues':checked}

def leaf(types,inc,vtype,etype):
    pairs={}
    for e in types[etype]:
        ends=frozenset(v for v in types[vtype] if inc(v,e))
        need(len(ends)==2,'two endpoints')
        need(ends not in pairs,'no parallel edges')
        pairs[ends]=e
        for i,t in enumerate(types):
            if i in [vtype,etype]:continue
            for x in t:
                need(inc(e,x)==all(inc(v,x) for v in ends),'B2')
    return len(pairs)

def graph_components(vertices, edges):
    adj={v:set() for v in vertices}
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    unseen=set(vertices);out=[]
    while unseen:
        root=min(unseen);seen={root};todo=[root]
        while todo:
            for x in adj[todo.pop()]:
                if x not in seen:seen.add(x);todo.append(x)
        out.append(frozenset(seen));unseen-=seen
    return out

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
    vertices=set(range(5));edges={i:frozenset((i,(i+1)%5)) for i in range(5)}
    types=[[(0,i) for i in range(5)],[(1,i) for i in range(5)],[(2,i) for i in range(6)],[(3,i) for i in range(5)]]
    # x_5 is the central vertex of the second leaf; x_j and y_j omit j.
    def shadow(x):
        if x[0]==0:return {x[1]}
        if x[0]==1:return edges[x[1]]
        return vertices if x==(2,5) else vertices-{x[1]}
    def inc(a,b):
        if a[0]==b[0]:return False
        if a[0]>b[0]:a,b=b,a
        if (a[0],b[0])==(2,3):return a[1] in [5,b[1]]
        return shadow(a)<=shadow(b)
    original=audit(types,inc);original['leaves']={'01':leaf(types,inc,0,1),'23':leaf(types,inc,2,3)}
    lifted=[[(0,v) for v in range(5)],[(1,v) for v in range(5)],[],[]]
    components={}
    for i in [2,3]:
        for x in types[i]:
            vs=[(v,c) for v in shadow(x) for c in [0,1]]
            es=[((v,0),(w,1)) for v in shadow(x) for w in shadow(x) if frozenset((v,w)) in edges.values()]
            for j,c in enumerate(graph_components(vs,es)):
                obj=(i,x[1],j);lifted[i].append(obj);components[obj]=c
    def project(x):return (x[0],x[1])
    def new_inc(a,b):
        if a[0]==b[0]:return False
        if a[0]>b[0]:a,b=b,a
        if b[0]<2:return frozenset((a[1],b[1])) in edges.values()
        if a[0]<2:return (a[1],a[0]) in components[b]
        return inc(project(a),project(b)) and bool(components[a]&components[b])
    transformed=audit(lifted,new_inc);transformed['leaf23']=leaf(lifted,new_inc,2,3)
    need(len([x for x in components if project(x)==(2,5)])==1,'central C5 is nonbipartite')
    need(all(len([x for x in components if project(x)==(3,j)])==2 for j in range(5)),'each edge shadow is bipartite')
    # Wrong incidence deletion is detected at a literal flag-extension/B2 check.
    damaged=lambda a,b: new_inc(a,b) and {a,b}!={(2,5,0),lifted[3][0]}
    rejected=False
    try:leaf(lifted,damaged,2,3)
    except ValueError:rejected=True
    need(rejected,'missing lifted endpoint must fail B1')
    result={'status':'PASS_SECOND_LEAF_COUNTEREXAMPLE','original':original,'transformed':transformed,
            'printed_condition':False,'corrected_condition':True,'both_geometries_residually_connected':True,
            'thin_or_regular_claim':False,'negative_control':'deleted lifted endpoint rejected',
            'scope':'Insufficiency of the necessity direction in N014v1 Proposition3.17 for general geometries; not a regular-hypertope counterexample.'}
    args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

if __name__=='__main__':main()
