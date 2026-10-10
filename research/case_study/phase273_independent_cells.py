#!/usr/bin/env python3
"""Independent cellular audit; imports no author homology or group code."""
import argparse
from collections import deque
import hashlib
import json
from pathlib import Path


def need(condition, message):
    if not condition:
        raise ValueError(message)


def rank_add(rows, vector, p):
    v = dict((i, x % p) for i, x in enumerate(vector) if x % p)
    while v:
        j = min(v)
        if j not in rows:
            inv = pow(v[j], -1, p)
            rows[j] = {k: x*inv % p for k, x in v.items()}
            return True
        c = v[j]
        for k, x in rows[j].items():
            y = (v.get(k, 0)-c*x) % p
            if y:
                v[k] = y
            else:
                v.pop(k, None)
    return False


def basis(vectors, p):
    rows = {}
    for v in vectors:
        rank_add(rows, v, p)
    return rows


def analyze(model):
    degree = len(model['generators'][0])
    marks = [tuple(x-1 for x in s) for s in model['generators']]
    identity = tuple(range(degree))
    need(len(set(marks)) == 4 and identity not in marks, 'distinct nonidentity marks')
    need(all(tuple(s[s[i]] for i in range(degree)) == identity for s in marks), 'involutions')
    need(all(tuple(a[b[i]] for i in range(degree)) == tuple(b[a[i]] for i in range(degree))
             for a,b in ((marks[0],marks[2]),(marks[0],marks[3]),(marks[1],marks[3]))), 'string commuting')
    names = {identity: 0}
    group = [identity]
    neighbors = []
    for x in group:
        row = []
        for s in marks:
            y = tuple(x[s[i]] for i in range(degree))
            if y not in names:
                names[y] = len(group)
                group.append(y)
            row.append(names[y])
        neighbors.append(row)
    g = len(group)
    def orbit(colors, start=0):
        seen = {start}
        queue = [start]
        for x in queue:
            for i in colors:
                y = neighbors[x][i]
                if y not in seen:
                    seen.add(y)
                    queue.append(y)
        return seen
    A, B, C = orbit((0,1,2)), orbit((1,2,3)), orbit((1,2))
    need(neighbors[0][0] not in B and neighbors[0][3] not in A, 'extreme independence')
    edge_names, edge_list = {}, []
    for x in range(g):
        for i, y in enumerate(neighbors[x]):
            key = (min(x,y),max(x,y),i)
            if key not in edge_names:
                edge_names[key] = len(edge_list)
                edge_list.append(key)
    e = len(edge_list)
    need(e == 2*g, 'Cayley edge count')
    def step(x, i):
        y = neighbors[x][i]
        return y, edge_names[(min(x,y),max(x,y),i)], (1 if x < y else -1)
    def polygon(x, i, j):
        start, v, vertices, k = x, [0]*e, [], 0
        while True:
            vertices.append(x)
            y, edge, sign = step(x, (i,j)[k % 2])
            v[edge] += sign
            x, k = y, k+1
            if x == start:
                break
            need(k <= 2*g, 'polygon closes')
        return vertices, v
    faces, boundaries = [], []
    for colors in ((0,2),(0,3),(1,3),(1,2)):
        unused = set(range(g))
        while unused:
            x = min(unused)
            vertices, chain = polygon(x, *colors)
            need(len(set(vertices)) == len(vertices), 'embedded polygon')
            unused.difference_update(vertices)
            row = (colors, vertices, chain)
            (boundaries if colors == (1,2) else faces).append(row)
    need(len(faces) == 3*g//4, 'raw square count')
    # A graph cycle basis written as actual oriented cellular one-chains.
    def cycles(selected):
        adj = [[] for _ in range(g)]
        for edge in selected:
            x,y,_ = edge_list[edge]
            adj[x].append((y,edge,1))
            adj[y].append((x,edge,-1))
        paths, tree_edges = {0:[0]*e}, set()
        queue = [0]
        for x in queue:
            for y,edge,sign in adj[x]:
                if y not in paths:
                    paths[y] = paths[x].copy()
                    paths[y][edge] += sign
                    tree_edges.add(edge)
                    queue.append(y)
        need(all(edge_list[k][0] in paths for k in selected), 'selected graph connected')
        result = []
        for edge in selected:
            if edge in tree_edges:
                continue
            x,y,_ = edge_list[edge]
            row = [a-b for a,b in zip(paths[x],paths[y])]
            row[edge] += 1
            result.append(row)
        return result
    def selected_graph(vertices, colors):
        return {k for k,(x,y,i) in enumerate(edge_list) if x in vertices and i in colors}
    end_cycles = [cycles(selected_graph(A,(0,1,2))), cycles(selected_graph(B,(1,2,3)))]
    q01,q23 = orbit((0,1)), orbit((2,3))
    locals_ = [selected_graph(q01,(0,1)) | selected_graph(C,(1,2)),
               selected_graph(C,(1,2)) | selected_graph(q23,(2,3))]
    # Every row is a closed chain, checked against an independently assembled d1.
    raw = [row[2] for row in faces]
    for chain in raw + [b[2] for b in boundaries] + end_cycles[0] + end_cycles[1]:
        boundary = [0]*g
        for c,(x,y,i) in zip(chain,edge_list):
            boundary[x] -= c
            boundary[y] += c
        need(not any(boundary), 'd1 d2 and graph cycles')
    field_results = []
    for p in (2,3,5):
        raw_basis = basis(raw,p)
        need(len(raw_basis) == len(raw), 'raw H2 zero')
        need(e-g+1-len(raw_basis) == 1+g//4, 'raw H1 dimension')
        for selected in locals_:
            local_cycles = cycles(selected)
            rows = {k:dict(v) for k,v in raw_basis.items()}
            before = len(rows)
            for v in local_cycles:
                rank_add(rows,v,p)
            need(len(rows)-before == len(local_cycles), 'local H1 injectivity')
        checked = 0
        for vertices, cyc in zip((A,B),end_cycles):
            rows = basis(raw+cyc,p)
            for colors, circle, chain in boundaries:
                test = {k:dict(v) for k,v in rows.items()}
                member = not rank_add(test,chain,p)
                need(member == (circle[0] in vertices), 'boundary membership iff end circle')
                checked += 1
        field_results.append({'prime':p,'boundary_membership_checks':checked,'local_injections':2})
    parity = {0:0}
    queue = [0]
    odd = False
    for x in queue:
        for y in neighbors[x]:
            if y not in parity:
                parity[y] = 1-parity[x]
                queue.append(y)
            elif parity[y] == parity[x]:
                odd = True
    return {'name':model['name'],'order':g,'edges':e,'raw_faces':len(faces),
            'boundary_circles':len(boundaries),'raw_H1_dimension':1+g//4,
            'nonorientable':odd,'fields':field_results}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--models',type=Path,default=Path(__file__).with_name('phase256_voltage_models.json'))
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(),'fresh output file')
    raw=args.models.read_bytes()
    models=json.loads(raw)
    # Additional independent q=2 case: elementary abelian C2^4 in its regular action.
    models.append({'name':'independent_C2_four','generators':[[1+(x^(1<<i)) for x in range(16)] for i in range(4)]})
    results=[analyze(m) for m in models]
    controls={}
    bad=dict(models[-1]); bad['generators']=list(bad['generators']); bad['generators'][3]=bad['generators'][0]
    try:
        analyze(bad)
    except ValueError as error:
        need(str(error)=='distinct nonidentity marks','expected negative control')
        controls['coincident_marks']='REJECTED'
    else:
        raise ValueError('invalid marking accepted')
    # G=C2^3 marked a,b,c,ab: distant commuting still holds but extreme independence fails.
    bad={'name':'dependent_extreme','generators':[[1+(x^s) for x in range(8)] for s in (1,2,4,3)]}
    try:
        analyze(bad)
    except ValueError as error:
        need(str(error)=='extreme independence','expected extreme control')
        controls['dependent_extreme']='REJECTED'
    else:
        raise ValueError('dependent extreme accepted')
    report={'status':'PASS','input_sha256':hashlib.sha256(raw).hexdigest(),
            'independence':'No author group, homology, surface or voltage code imported.',
            'scope':'Six literal raw surfaces over F2,F3,F5; finite diagnostics only, not the quantified cover theorem.',
            'results':results,'controls':controls}
    args.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','models':len(results),'fields':[2,3,5],'controls':controls}))

if __name__=='__main__':
    main()
