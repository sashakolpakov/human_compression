"""Literal finite-field/coset controls for the L041 argument; no universal credit."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Run with ordinary Python: assertions are proof controls.')
from collections import deque
from itertools import combinations, product
from math import gcd
import json


class Field:
    def __init__(self, p):
        self.p = p
        self.degree = 1 if p % 3 == 1 else 2
        self.q = p ** self.degree
        self.e = (next(x for x in range(2, p) if (x*x+x+1) % p == 0)
                  if self.degree == 1 else p)
        self.adds = [[self._add(a, b) for b in range(self.q)] for a in range(self.q)]
        self.muls = [[self._mul(a, b) for b in range(self.q)] for a in range(self.q)]
        self.neg = [next(b for b in range(self.q) if self.add(a, b) == 0)
                    for a in range(self.q)]
        self.inv = [0] + [next(b for b in range(1, self.q) if self.mul(a, b) == 1)
                          for a in range(1, self.q)]

    def _add(self, a, b):
        return ((a+b) % self.p if self.degree == 1 else
                (a % self.p+b % self.p) % self.p + self.p*((a//self.p+b//self.p) % self.p))

    def _mul(self, a, b):
        if self.degree == 1:
            return a*b % self.p
        x, y, z, t = a % self.p, a//self.p, b % self.p, b//self.p
        return (x*z-y*t) % self.p + self.p*((x*t+y*z-y*t) % self.p)

    def add(self, a, b): return self.adds[a][b]
    def mul(self, a, b): return self.muls[a][b]
    def sub(self, a, b): return self.add(a, self.neg[b])


def control(p):
    f = Field(p)
    q, e = f.q, f.e
    e2 = f.mul(e, e)
    one = (1, 0, 0, 1)
    def canon(m): return min(m, tuple(f.neg[x] for x in m))
    identity = canon(one)
    def mm(a, b):
        return canon(tuple(f.add(f.mul(a[2*i], b[j]), f.mul(a[2*i+1], b[2+j]))
                           for i in range(2) for j in range(2)))
    def mi(a): return canon((a[3], f.neg[a[1]], f.neg[a[2]], a[0]))
    def mp(a, n):
        z = identity
        for _ in range(n): z = mm(z, a)
        return z
    def mv(a, v):
        return tuple(f.add(f.mul(a[2*i], v[0]), f.mul(a[2*i+1], v[1])) for i in range(2))
    def U(t): return canon((1,t,0,1))
    def V(t): return canon((1,0,t,1))
    a1 = canon((0,1,f.neg[1],1))
    a2, a3, E = canon((e,e2,0,e2)), canon((e2,e,0,e)), canon((e,0,0,e2))
    b2, b3 = mm(mi(a1),a2), mm(mi(a1),a3)
    assert [a2,a3,b2,b3] == [mm(U(1),E),mm(U(1),mi(E)),mm(V(1),E),mm(V(1),mi(E))]
    assert all(mp(a,3) == identity for a in [a1,a2,a3,b2,b3])
    def generated(gens):
        seen = {identity}
        todo = deque([identity])
        while todo:
            a = todo.popleft()
            for b in gens:
                c = mm(a,b)
                if c not in seen: seen.add(c); todo.append(c)
        return seen
    G = generated([a1,a2,a3])
    H = [generated([b2,b3]),generated([a2,a3]),generated([a1,a3]),generated([a1,a2])]
    assert len(G) == q*(q*q-1)//gcd(2,q-1)
    assert list(map(len,H)) == [3*q,3*q,12,12]
    assert all(len(H[i]&H[j]) == 3 for i,j in combinations(range(4),2))
    assert all(len(set.intersection(*(H[i] for i in t))) == 1 for t in combinations(range(4),3))
    K = {1,e,e2,f.neg[1],f.neg[e],f.neg[e2]}
    assert len(K) == 3*gcd(2,q-1)
    def point(v): return min(tuple(f.mul(k,x) for x in v) for k in K)
    def det(v,w): return f.sub(f.mul(v[0],w[1]),f.mul(v[1],w[0]))
    v0, v1 = point((0,1)), point((1,0))
    common = {v0,v1,point((1,1))}
    D2 = frozenset(common|{point((f.neg[e2],1))})
    D3 = frozenset(common|{point((f.neg[e],1))})
    bases = [v0,v1,D2,D3]
    def action(i,g,obj):
        return point(mv(g,obj)) if i < 2 else frozenset(point(mv(g,v)) for v in obj)
    objects = [set() for _ in range(4)]
    edge = {(i,j):set() for i,j in combinations(range(4),2)}
    fibres = [{} for _ in range(4)]
    for g in G:
        z = [action(i,mi(g),bases[i]) for i in range(4)]
        for i in range(4):
            objects[i].add(z[i])
            fibres[i].setdefault(z[i],set()).add(g)
        for i,j in edge: edge[i,j].add((z[i],z[j]))
    for i in range(4):
        assert fibres[i][bases[i]] == H[i]
        for fibre in fibres[i].values():
            g = next(iter(fibre))
            assert fibre == {mm(h,g) for h in H[i]}
    all_points = {point(v) for v in product(range(q),repeat=2) if v != (0,0)}
    assert objects[0] == objects[1] == all_points
    def incident(i,x,j,y):
        if i > j: return incident(j,y,i,x)
        if j < 2: return det(x,y) in K
        if i < 2: return x in y
        return len(x&y) == 3
    for (i,j),edges in edge.items():
        literal = {(x,y) for x in objects[i] for y in objects[j] if incident(i,x,j,y)}
        assert edges == literal, ('coset/model incidence',p,i,j)
    A, B = (f.neg[1],1,0,1), (0,1,1,0)
    def field_power(x,n):
        t=1
        for _ in range(n): t=f.mul(t,x)
        return t
    def frobenius_obj(i,obj):
        if i < 2: return point(tuple(field_power(x,p) for x in obj))
        return frozenset(point(tuple(field_power(x,p) for x in v)) for v in obj)
    symmetry_maps = [('improper',A,[0,1,3,2]),('proper',B,[1,0,3,2])]
    for label,matrix,types in symmetry_maps:
        maps=[{x:action(i,matrix,x) for x in objects[i]} for i in range(4)]
        assert all(set(maps[i].values()) == objects[types[i]] for i in range(4))
        for (i,j),edges in edge.items():
            for x,y in edges: assert incident(types[i],maps[i][x],types[j],maps[j][y])
        transformed={types[i]:maps[i][bases[i]] for i in range(4)}
        assert [transformed[i] for i in range(4)] == ([point((1,1)),v1,D2,D3] if label=='improper' else bases)
    if f.degree == 2:
        regular=[{x:action(i,A,frobenius_obj(i,x)) for x in objects[i]} for i in range(4)]
        assert all(set(regular[i].values()) == objects[i] for i in range(4))
        for (i,j),edges in edge.items():
            for x,y in edges: assert incident(i,regular[i][x],j,regular[j][y])
        assert [regular[i][bases[i]] for i in range(4)] == [point((1,1)),v1,D2,D3]
    adj = {}
    for i in range(4):
        for x in objects[i]: adj[i,x] = {j:set() for j in range(4) if j != i}
    for (i,j),edges in edge.items():
        for x,y in edges: adj[i,x][j].add(y); adj[j,y][i].add(x)
    def connected(vertices):
        if not vertices: return False
        unseen = set(vertices)
        todo = [unseen.pop()]
        while todo:
            i,x = todo.pop()
            reached = {(j,y) for j,ys in adj[i,x].items() for y in ys}&unseen
            unseen -= reached
            todo.extend(reached)
        return not unseen
    assert connected({(i,x) for i in range(4) for x in objects[i]})
    for i in range(4):
        for x in objects[i]:
            assert connected({(j,y) for j,ys in adj[i,x].items() for y in ys})
    for (i,j),edges in edge.items():
        rest = set(range(4))-{i,j}
        for x,y in edges:
            vertices = {(k,z) for k in rest for z in adj[i,x][k]&adj[j,y][k]}
            assert len(vertices) == 6 and connected(vertices)
    flags = {}
    for types in combinations(range(4),3):
        i,j,k = types
        missing = next(iter(set(range(4))-set(types)))
        n = 0
        for x,y in edge[i,j]:
            for z in adj[i,x][k]&adj[j,y][k]:
                completions = adj[i,x][missing]&adj[j,y][missing]&adj[k,z][missing]
                assert len(completions) == 2
                n += 1
        assert n == len(G)
        flags[''.join(map(str,types))] = n
    assert connected({(i,x) for i in (0,1) for x in objects[i]})
    for T, X, Y, epsilon in [(U,a2,a3,e),(V,b2,b3,e2)]:
        u,v = mm(mm(X,mi(Y)),X),mm(X,Y)
        assert u == T(1) and v == T(f.neg[epsilon])
        assert mm(mm(mi(X),Y),mi(X)) == mi(u)
        assert mm(mi(X),mi(Y)) == mm(mi(u),v)
        assert mm(mm(E,u),mi(E)) == mm(mi(u),v)
        assert mm(mm(E,v),mi(E)) == mi(u)
        kernel = {(a,b) for a in range(p) for b in range(p)
                  if f.sub(a, f.mul(epsilon,b)) == 0}
        assert len(kernel) == (p if f.degree == 1 else 1)
    return dict(p=p,q=q,e=e,group_order=len(G),parabolic_orders=list(map(len,H)),
                objects=list(map(len,objects)),edges={str(k):len(v) for k,v in edge.items()},
                rank_three_flags=flags,chambers=2*len(G),residues_connected=True,
                actual_two_type_components=1,printed_two_type_components=(q-1)//len(K))


if __name__ == '__main__':
    out = []
    for prime in [2,7,13,19,5]:
        row = control(prime)
        out.append(row)
        print(json.dumps(row),flush=True)
    assert next(x for x in out if x['q']==13)['printed_two_type_components'] == 2
    assert 7*7+7+1 == 57 and 2*2+2*3+3*3 == 19
    print(json.dumps({'status':'PASS_FINITE_CONTROLS_ONLY','cases':out,
                      'p19':{'actual_translation_index':19,'printed_period_index':57}}))
