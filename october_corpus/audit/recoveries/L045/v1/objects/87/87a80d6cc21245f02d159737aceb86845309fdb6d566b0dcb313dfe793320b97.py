"""Independent small projective/semilinear controls and formal identities."""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
import itertools
import json
from pathlib import Path


def need(b, s):
    if not b:
        raise ValueError(s)


class Field:
    def __init__(self, q): self.q = q
    def add(self, a, b):
        return ((a % 3 + b % 3) % 3 + 3 * ((a // 3 + b // 3) % 3)) if self.q == 9 else (a + b) % self.q
    def neg(self, a):
        return ((-a % 3) + 3 * (-(a // 3) % 3)) if self.q == 9 else -a % self.q
    def mul(self, a, b):
        if self.q != 9: return a * b % self.q
        x, y, z, w = a % 3, a // 3, b % 3, b // 3
        return (x * z - y * w) % 3 + 3 * ((x * w + y * z) % 3)
    def inv(self, a): return next(b for b in range(1, self.q) if self.mul(a, b) == 1)
    def sigma(self, a): return self.mul(self.mul(a, a), a) if self.q == 9 else a


def norm(a, f):
    v = next(x for x in a if x)
    return tuple(f.mul(x, f.inv(v)) for x in a)


def matrix_product(a, b, f):
    return tuple(f.add(f.mul(a[2*i], b[j]), f.mul(a[2*i+1], b[2+j])) for i in range(2) for j in range(2))


def projective(q):
    f = Field(q)
    points = [(1, x) for x in range(q)] + [(0, 1)]
    point_index = {norm(v, f): i for i, v in enumerate(points)}
    matrices = set()
    for a in itertools.product(range(q), repeat=4):
        if f.add(f.mul(a[0], a[3]), f.neg(f.mul(a[1], a[2]))): matrices.add(norm(a, f))
    perms = []
    for a in sorted(matrices):
        image = []
        for x, y in points:
            v = (f.add(f.mul(a[0], x), f.mul(a[1], y)), f.add(f.mul(a[2], x), f.mul(a[3], y)))
            image.append(point_index[norm(v, f)])
        perms.append(tuple(image))
    need(len(set(perms)) == len(matrices) == q * (q*q-1), 'faithful projective action')
    nu = sum(all(p[p[i]] == i for i in range(q+1)) for p in perms)
    need(nu == q*q+1, 'literal PGL2 involutions')
    return f, sorted(matrices), perms, nu


def wreath_nu(perms):
    n = len(perms[0]); count = 0
    for a, b, swap in itertools.product(perms, perms, range(2)):
        p = tuple(a[i] + swap*n for i in range(n)) + tuple(b[i] + (1-swap)*n for i in range(n))
        count += all(p[p[i]] == i for i in range(2*n))
    return count


def add(a, b):
    c = a.copy()
    for i, v in b.items(): c[i] = c.get(i, 0) + v
    return {i:v for i,v in c.items() if v}


def mul(a, b):
    c = {}
    for i, u in a.items():
        for j, v in b.items(): c[i+j] = c.get(i+j, 0) + u*v
    return {i:v for i,v in c.items() if v}


def scale(a, n): return {i:n*v for i,v in a.items() if n*v}


def order_even(m, sign):
    p = mul({m*(m-1):2}, {m:1, 0:-sign})
    for i in range(1, m): p = mul(p, {2*i:1,0:-1})
    return p


def main():
    records=[]
    for q in [3,5,9]:
        f, matrices, perms, nu=projective(q)
        row=dict(q=q, order=len(perms), nu2=nu)
        if q in [3,5]:
            actual=wreath_nu(perms)
            need(actual == q**4+q**3+2*q*q-q+1, 'actual wreath count')
            row['wreath_nu2']=actual
        if q==9:
            semilinear=0
            for a in matrices:
                b=tuple(f.sigma(x) for x in a)
                semilinear += norm(matrix_product(a,b,f),f)==(1,0,0,1)
            need(semilinear==30 and nu+semilinear==112, 'nonsplit O4 field coset')
            row.update(outer_field_nu2=semilinear, pco4_minus_q3_nu2=nu+semilinear)
            scalars=[z for z in range(1,9) if f.mul(z,z) in [1,2]]
            need(len(scalars)==4, 'quadratic-field scalar kernel has two ground-field cosets')
            row['allowed_K_scalars']=scalars
        records.append(row)
    # Actual F3 order-four conformal lift, dimension six, with multiplier two.
    n=6
    a=[[0]*n for _ in range(n)]
    for i in range(3): a[i][i+3]=2;a[i+3][i]=1
    gram=[1]*3+[2]*3
    for i,j in itertools.product(range(n),repeat=2):
        need(sum(a[i][k]*a[k][j] for k in range(n))%3 == (2 if i==j else 0), 'nonsquare lift square')
        need(sum(a[k][i]*gram[k]*a[k][j] for k in range(n))%3 == (2*gram[i]%3 if i==j else 0), 'nonsquare conformal multiplier')
    # Polynomial identities, not evaluations at a finite sample of q.
    plus_num=mul({8:1},mul(mul({2:1,0:1},{2:1,0:1}),{4:1,2:1,0:1}))
    minus_num=mul({8:1},mul({4:1,0:1},{4:1,2:1,0:1}))
    need(scale(order_even(4,1),4)==scale(mul(mul(order_even(2,1),order_even(2,1)),plus_num),2), 'formal plus orbit identity')
    need(scale(order_even(4,-1),2)==mul(mul(order_even(2,1),order_even(2,-1)),minus_num), 'formal minus orbit identity')
    need(all(v>0 for v in add(plus_num,{16:-1}).values()), 'strict plus remainder')
    need(all(v>0 for v in add(minus_num,{16:-1}).values()), 'strict minus remainder')
    report=dict(status='PASS', projective_models=records,nonsquare_lift_matrix=a,
                formal_orbit_identities=2,positive_remainder_polynomials=2,
                source_or_generation_claim=False)
    Path(sys.argv[1]).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__=='__main__': main()
