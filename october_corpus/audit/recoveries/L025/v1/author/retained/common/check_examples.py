"""Optional finite checks of the written constructions and their endpoints."""
from collections import deque
import json


class Field:
    def __init__(self, q):
        self.q = q
        self.polynomial = {4: 7, 8: 11, 16: 19}.get(q)

    def add(self, a, b):
        return a ^ b if self.polynomial else (a + b) % self.q

    def mul(self, a, b):
        if not self.polynomial:
            return a * b % self.q
        c = 0
        while b:
            if b & 1:
                c ^= a
            a <<= 1
            if a & self.q:
                a ^= self.polynomial
            b >>= 1
        return c

    def power(self, a, n):
        y = 1
        for _ in range(n):
            y = self.mul(y, a)
        return y

    def generator(self):
        return next(a for a in range(1, self.q)
                    if len({self.power(a, i) for i in range(self.q - 1)}) == self.q - 1)


def edge(g, u, v):
    if u == v:
        raise ValueError('loop')
    g[u].add(v)
    g[v].add(u)


def additive(f, s=(), t=()):
    q = f.q
    g = [set() for _ in range(2 * q * q)]
    for x in range(q):
        for y in range(q):
            for m in range(q):
                b = next(b for b in range(q) if f.add(f.mul(m, x), b) == y)
                edge(g, x*q+y, q*q+m*q+b)
            for a in s:
                edge(g, x*q+y, x*q+f.add(y, a))
            for a in t:
                edge(g, q*q+x*q+y, q*q+x*q+f.add(y, a))
    return g


def multiplicative(f, augment=True):
    q = f.q
    vectors = [(a, b) for a in range(q) for b in range(q) if a or b]
    index = {v: i for i, v in enumerate(vectors)}
    n = len(vectors)
    g = [set() for _ in range(2*n)]
    for i, v in enumerate(vectors):
        for j, u in enumerate(vectors):
            if f.add(f.mul(u[0], v[0]), f.mul(u[1], v[1])) == 1:
                edge(g, i, n+j)
    if augment:
        lam = f.generator()
        for i, v in enumerate(vectors):
            edge(g, i, index[tuple(f.mul(lam, a) for a in v)])
            edge(g, n+i, n+index[tuple(f.mul(f.mul(lam, lam), a) for a in v)])
    return g


def invariants(g):
    diameter, girth = 0, len(g)+1
    for root in range(len(g)):
        distance, parent = {root: 0}, {root: None}
        queue = deque([root])
        while queue:
            v = queue.popleft()
            for w in g[v]:
                if w not in distance:
                    distance[w], parent[w] = distance[v]+1, v
                    queue.append(w)
                elif parent[v] != w and parent[w] != v:
                    girth = min(girth, distance[v]+distance[w]+1)
        if len(distance) != len(g):
            raise ValueError('disconnected construction')
        diameter = max(diameter, max(distance.values()))
    return dict(order=len(g), degrees=sorted(set(map(len, g))), girth=girth, diameter=diameter)


def run():
    cases = []
    def check(name, graph, expected):
        actual = invariants(graph)
        if actual != expected:
            raise ValueError((name, actual, expected))
        cases.append(dict(name=name, **actual))
    check('type1 q2 without additions', additive(Field(2)),
          dict(order=8, degrees=[2], girth=8, diameter=4))
    check('type2 q2 without additions', multiplicative(Field(2), False),
          dict(order=6, degrees=[2], girth=6, diameter=3))
    for q in [4, 8, 16]:
        check(f'additive matchings q{q}', additive(Field(q), [1], [2]),
              dict(order=2*q*q, degrees=[q+1], girth=5, diameter=4))
    for q, diameter in [(5, 2), (7, 3), (11, 4)]:
        check(f'additive cycles q{q}', additive(Field(q), [1, q-1], [2, q-2]),
              dict(order=2*q*q, degrees=[q+2], girth=5, diameter=diameter))
    for q, diameter in [(8, 3), (11, 4), (16, 4)]:
        check(f'multiplicative cycles q{q}', multiplicative(Field(q)),
              dict(order=2*(q*q-1), degrees=[q+2], girth=5, diameter=diameter))
    return dict(status='PASS_OPTIONAL_EXAMPLES', cases=cases,
                uniform_proof=False, complete_census=False, new_original_credit=0)


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
