"""Literal Figure 1 families from arXiv:1509.01032v1.

Vertices are numbered along the top row, then along the lower row.
A tuple at a word position means parallel edges with those labels.
These are transcribed source data, not a completeness assumption.
"""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')

def need(condition, message):
    if not condition:
        raise ValueError(message)

FAMILIES = [
    (1, 'simplex', 1), (2, 'second', 2),
    (3, 'A', 3), (3, 'G', 3), (3, 'K', 2),
    (3, 'L2', 3), (3, 'L1', 2), (3, 'M2(0)', 3), (3, 'L3', 3),
    (4, 'B', 4), (4, 'E', 3), (4, 'I2', 3),
    (4, 'N1', 2), (4, 'N2', 3), (4, 'N3', 3),
    (4, 'O2(0)', 3), (4, 'P1', 2), (4, 'Q2', 4),
]

def graph(k, name, n):
    need((k, name) in [(a, b) for a, b, _ in FAMILIES], 'unknown family')
    need(type(n) is int and n >= 2*k+3, 'outside stated range')
    end = n-k-1
    extra = []
    if k == 1:
        word = list(range(end+1))
    elif k == 2:
        word = [1, 0] + list(range(1, end+1))
    elif name == 'A':
        word = [2, 1] + list(range(2, end+1))
        top = len(word)+1
        extra = [(0, top, 0), (1, top+1, 0), (top, top+1, 2)]
    elif name in ('G', 'I2'):
        word = list(range(end+1)) + ([end-1] if k == 4 else [])
        top = len(word)+1
        extra = [(0, top, 1), (0, top, 2), (1, top+1, 2), (top, top+1, 0)]
    elif name == 'K':
        word = [1, 0] + list(range(1, end+1)) + [end-1]
    elif name in ('L2', 'N2'):
        word = [2, 1, 0] + list(range(1, end+1)) + ([end-1] if k == 4 else [])
    elif name in ('L1', 'N1'):
        word = [0, 1, 0] + list(range(1, end+1)) + ([end-1] if k == 4 else [])
    elif name in ('M2(0)', 'O2(0)'):
        word = [0, 1, (0, 2)] + list(range(1, end+1)) + ([end-1] if k == 4 else [])
    elif name in ('L3', 'N3'):
        word = [(0, 2), 1, 0] + list(range(1, end+1)) + ([end-1] if k == 4 else [])
    elif name == 'B':
        word = list(range(end+1))
        top = len(word)+1
        extra = [(i, top+i, 3) for i in range(3)] + [(top, top+1, 0), (top+1, top+2, 1)]
    elif name == 'E':
        word = list(range(end+1)) + [end-1]
        top = len(word)+1
        extra = [(0, top, 2), (1, top+1, 2), (top, top+1, 0)]
    elif name == 'P1':
        word = [1, 0, 1, 0] + list(range(1, end+1))
    elif name == 'Q2':
        word = [3, 2, 1, 0] + list(range(1, end+1))
    else:
        raise ValueError('unimplemented family')
    edges = list(extra)
    for i, labels in enumerate(word):
        for label in labels if isinstance(labels, tuple) else (labels,):
            edges.append((i, i+1, label))
    need(set(v for a,b,_ in edges for v in (a,b)) == set(range(n)), 'vertex count')
    marks = [list(range(n)) for _ in range(n-k)]
    for a,b,label in edges:
        need(0 <= label < n-k, 'label range')
        need(marks[label][a] == a and marks[label][b] == b, 'not a matching')
        marks[label][a],marks[label][b] = b,a
    return tuple(tuple(g) for g in marks), tuple(sorted(edges))

def validate(t):
    need(bool(t) and bool(t[0]), 'empty tuple')
    n = len(t[0])
    for g in t:
        need(len(g) == n and sorted(g) == list(range(n)), 'not a permutation')
        need(any(g[v] != v for v in range(n)), 'identity mark')
        need(all(g[g[v]] == v for v in range(n)), 'not an involution')
    need(all(all(g[h[v]] == h[g[v]] for v in range(n))
             for i,g in enumerate(t) for j,h in enumerate(t) if abs(i-j)>1), 'distant commutation')
    return n

def rooted(t, v):
    n = validate(t)
    queue=[v]; labels={v:0}
    for x in queue:
        for g in t:
            y=g[x]
            if y not in labels:
                labels[y]=len(queue);queue.append(y)
    need(len(queue)==n, 'not transitive')
    return tuple(tuple(labels[g[x]] for x in queue) for g in t), tuple(queue)

def isomorphism(source, target):
    n=validate(source);need(validate(target)==n, 'degree mismatch')
    key, order = rooted(source,0)
    for reverse in (False,True):
        orient=tuple(reversed(target)) if reverse else target
        for v in range(n):
            other, images=rooted(orient,v)
            if key==other:
                phi=[None]*n
                for a,b in zip(order,images):phi[a]=b
                need(all(phi[g[x]]==h[phi[x]] for g,h in zip(source,orient) for x in range(n)), 'literal conjugacy')
                return {'reverse_target':reverse,'point_map':phi}
    return None

def pure_cut(t, j):
    n=validate(t)
    moved=[v for v in range(n) if t[j][v]!=v]
    need(len(moved)==2, 'cut is not pure')
    remain=set(range(n));parts=[]
    while remain:
        a=min(remain);q=[a];o={a}
        for v in q:
            for i,g in enumerate(t):
                if i!=j and g[v] not in o:o.add(g[v]);q.append(g[v])
        parts.append(o);remain-=o
    need(len(parts)==2 and (moved[0] in parts[0]) != (moved[1] in parts[0]), 'not a unique bridge')
    for A,B in (parts, list(reversed(parts))):
        if all(g[v]==v for g in t[:j] for v in B) and all(g[v]==v for g in t[j+1:] for v in A):
            a=next(v for v in moved if v in A);b=next(v for v in moved if v in B)
            return a,b
    raise ValueError('cut is not perfect')

def subdivide(t,j):
    n=len(t[0]);a,b=pure_cut(t,j)
    u=list(range(n+1));u[a],u[n]=n,a
    v=list(range(n+1));v[b],v[n]=n,b
    return tuple(tuple(g)+(n,) for g in t[:j])+(tuple(u),tuple(v))+tuple(tuple(g)+(n,) for g in t[j+1:])
