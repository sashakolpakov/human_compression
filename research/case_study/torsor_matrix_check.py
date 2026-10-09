"""Independent exact checks of the basis-aware torsor matrix calculus."""
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json


class FiniteGroup:
    def __init__(self, elements, multiply, one):
        self.elements = list(elements)
        self.index = {x:i for i,x in enumerate(self.elements)}
        self.one = self.index[one]
        self.n = len(elements)
        self.mul = [[self.index[multiply(x,y)] for y in elements] for x in elements]
        self.inv = [next(j for j in range(self.n) if self.mul[i][j] == self.one)
                    for i in range(self.n)]

    def closure(self, generators):
        found = {self.one}
        todo = [self.one]
        while todo:
            x = todo.pop()
            for g in generators:
                y = self.mul[x][g]
                if y not in found:
                    found.add(y)
                    todo.append(y)
        return frozenset(found)

    def all_subgroups(self):
        trivial = frozenset([self.one])
        found, todo = {trivial}, [trivial]
        while todo:
            h = todo.pop()
            for g in range(self.n):
                if g not in h:
                    k = self.closure(tuple(h)+(g,))
                    if k not in found:
                        found.add(k)
                        todo.append(k)
        return sorted(found, key=lambda h:(len(h), sorted(h)))

    def matrix(self, h):
        return [sum(1 << y for y in range(self.n)
                    if self.mul[self.inv[x]][y] in h) for x in range(self.n)]

    def cosets(self, h):
        return set(frozenset(self.mul[x][y] for y in h) for x in range(self.n))


def compose(p,q):
    return tuple(p[q[i]] for i in range(len(p)))


def symmetric_matrix_check():
    es = list(permutations(range(4)))
    g = FiniteGroup(es, compose, tuple(range(4)))
    subs = g.all_subgroups()
    assert len(subs) == 30
    matrices = {h:g.matrix(h) for h in subs}
    for h in subs:
        rows = matrices[h]
        assert all(r.bit_count() == len(h) for r in rows)
        assert len(set(rows))*len(h) == g.n
        for k in subs:
            a, b = matrices[h], matrices[k]
            meet = h & k
            assert [x & y for x,y in zip(a,b)] == matrices[meet]
            hk = {g.mul[x][y] for x in h for y in k}
            support = g.matrix(hk)
            for x in range(g.n):
                for z in range(g.n):
                    value = (a[x] & b[z]).bit_count()
                    assert value == len(meet)*((support[x] >> z) & 1)
            # Boolean transitive closure, performed independently on matrices.
            join = g.closure(tuple(h | k))
            expected = matrices[join]
            for x in range(g.n):
                reached = 1 << x
                while True:
                    extended = reached
                    for y in range(g.n):
                        if (reached >> y) & 1:
                            extended |= a[y] | b[y]
                    if extended == reached:
                        break
                    reached = extended
                assert reached == expected[x]
    return {'group':'S4', 'subgroups':len(subs),
            'subgroup_pairs':len(subs)**2,
            'ordinary_product_entries_checked':len(subs)**2*g.n*g.n}


def helly_obstruction():
    es = list(product(range(2),range(3),range(3)))
    def mul(x,y):
        e,a,b=x; f,c,d=y
        sign = 1 if e == 0 else -1
        return ((e+f)%2,(a+sign*c)%3,(b+sign*d)%3)
    g = FiniteGroup(es,mul,(0,0,0))
    rs = [g.index[x] for x in [(1,0,0),(1,1,0),(1,0,1)]]
    distinguished = {mask:g.closure([rs[i] for i in range(3) if (mask >> i) & 1])
                     for mask in range(8)}
    for a in range(8):
        for b in range(8):
            assert distinguished[a] & distinguished[b] == distinguished[a & b]
    parabolics = [distinguished[7 ^ (1 << i)] for i in range(3)]
    cosets = [g.cosets(h) for h in parabolics]
    flags = list(product(*cosets))
    assert len(flags) == 27
    assert all(all(a & b for a,b in combinations(flag,2)) for flag in flags)
    nonhelly = [flag for flag in flags if not set.intersection(*map(set,flag))]
    assert len(nonhelly) == 9
    return {'group':'C3^2 semidirect C2', 'order':g.n,
            'intersection_property_checks':64,
            'chambers':27,'torsor_chambers':18,'empty_total_intersections':9}


def determinant(a):
    a = [[Fraction(x) for x in row] for row in a]
    d = Fraction(1)
    for j in range(len(a)):
        pivot = next(i for i in range(j,len(a)) if a[i][j])
        if pivot != j:
            a[j],a[pivot] = a[pivot],a[j]
            d = -d
        v=a[j][j]; d *= v
        a[j]=[x/v for x in a[j]]
        for i in range(j+1,len(a)):
            v=a[i][j]
            a[i]=[x-v*y for x,y in zip(a[i],a[j])]
    return d


def lost_basis_example():
    t = [[2,2,0,0,0,0],[0,0,2,2,0,0],[1,-1,1,-1,4,0],
         [-1,1,-1,1,4,0],[1,-1,-1,1,0,4],[-1,1,1,-1,0,4]]
    a=(1,0,3,2,4,5); b=(2,3,0,1,4,5)
    aa=(0,1,3,2,5,4); bb=(1,0,2,3,5,4)
    for p,q in [(a,aa),(b,bb)]:
        # T P = Q T for column-vector permutation matrices.
        assert all(t[i][p[j]] == t[q[i]][j] for i in range(6) for j in range(6))
    assert determinant(t) == -2048
    def orbits(gens):
        unseen=set(range(6)); sizes=[]
        while unseen:
            found={min(unseen)}; todo=list(found)
            while todo:
                x=todo.pop()
                for gen in gens:
                    y=gen[x]
                    if y not in found:
                        found.add(y); todo.append(y)
            unseen -= found; sizes.append(len(found))
        return sorted(sizes)
    assert orbits([a,b]) == [1,1,4]
    assert orbits([aa,bb]) == [2,2,2]
    return {'intertwiner_determinant':-2048,'first_orbits':[1,1,4],
            'second_orbits':[2,2,2]}


def main():
    report={'status':'PASS',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'matrix_calculus':symmetric_matrix_check(),
            'helly_obstruction':helly_obstruction(),
            'basis_loss':lost_basis_example()}
    Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
