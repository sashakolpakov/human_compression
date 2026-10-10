#!/usr/bin/env python3
"""Independent literal-coordinate q=3 check; no GAP or author-code imports.

Field elements a+3*b represent a+b*T, T^2=T+1 over F3.  SymPy's
Schreier--Sims supplies the one large permutation-group order calculation.
All proper marked subgroups and their intersections are enumerated directly.
"""
from collections import deque
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import time
import sympy
from sympy.combinatorics import Permutation, PermutationGroup


def add(a, b):
    return ((a % 3 + b % 3) % 3) + 3 * ((a // 3 + b // 3) % 3)


def neg(a):
    return (-a % 3) + 3 * ((-(a // 3)) % 3)


def mul(a, b):
    x, y, z, w = a % 3, a // 3, b % 3, b // 3
    return (x*z+y*w) % 3 + 3*((x*w+y*z+y*w) % 3)


def power(a, n):
    ans = 1
    while n:
        if n & 1:
            ans = mul(ans, a)
        a = mul(a, a)
        n >>= 1
    return ans


def fsum(xs):
    ans = 0
    for x in xs:
        ans = add(ans, x)
    return ans


def mm(a, b):
    return tuple(tuple(fsum(mul(a[i][k], b[k][j]) for k in range(len(b)))
                       for j in range(len(b[0]))) for i in range(len(a)))


def adjoint(a):
    return tuple(tuple(power(a[j][i], 3) for j in range(len(a)))
                 for i in range(len(a[0])))


def scale(t, a):
    return tuple(tuple(mul(t, x) for x in row) for row in a)


def rref(rows):
    a = [list(row) for row in rows]
    r = 0
    for j in range(4):
        pivot = next((k for k in range(r, len(a)) if a[k][j]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        a[r] = [mul(x, power(a[r][j], 7)) for x in a[r]]
        for k in range(len(a)):
            if k != r and a[k][j]:
                t = neg(a[k][j])
                a[k] = [add(x, mul(t, y)) for x, y in zip(a[k], a[r])]
        r += 1
        if r == len(a):
            break
    return tuple(tuple(row) for row in a[:r])


def determinant(a):
    a = [list(row) for row in a]
    ans = 1
    for i in range(4):
        j = next((j for j in range(i, 4) if a[j][i]), None)
        if j is None:
            return 0
        if j != i:
            a[j], a[i] = a[i], a[j]
            ans = neg(ans)
        x = a[i][i]
        ans = mul(ans, x)
        for j in range(i+1, 4):
            t = neg(mul(a[j][i], power(x, 7)))
            a[j] = [add(u, mul(t, v)) for u, v in zip(a[j], a[i])]
    return ans


def compose(a, b):
    return tuple(b[a[i]] for i in range(len(a)))


def closure(gens, identity):
    out = {identity}
    queue = deque([identity])
    while queue:
        a = queue.popleft()
        for b in gens:
            ab = compose(a, b)
            if ab not in out:
                out.add(ab)
                queue.append(ab)
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path(__file__).with_suffix('.json'))
    args = parser.parse_args()
    start = time.monotonic()
    t = 3
    assert power(t, 2) == add(t, 1) and power(t, 4) == 2 and power(t, 8) == 1
    assert power(t, 3) == add(1, neg(t))
    ident = tuple(tuple(int(i == j) for j in range(4)) for i in range(4))
    h = ((0,1,0,0),(1,0,0,0),(0,0,0,2),(0,0,2,0))
    a = scale(t, ((0,0,1,0),(0,0,0,1),(1,0,0,0),(0,1,0,0)))
    b = ((1,1,t,neg(t)),(0,1,0,0),(0,add(1,neg(t)),0,1),
         (0,add(t,2),1,0))
    c = ((1,0,0,0),(0,1,0,0),(0,0,2,0),(0,0,0,2))
    gens = (a,b,c)
    assert all(mm(mm(adjoint(g),h),g) == h for g in gens)
    assert [determinant(g) for g in gens] == [2,2,1]
    assert mm(a,a) == scale(power(t,2), ident)
    assert mm(b,b) == ident and mm(c,c) == ident
    assert mm(a,c) == scale(2, mm(c,a))
    base = ((1,0,0,0),(0,0,1,0))
    planes = [base]
    index = {base: 0}
    for plane in planes:
        for g in gens:
            image = rref(mm(plane,g))
            if image not in index:
                index[image] = len(planes)
                planes.append(image)
    assert len(planes) == (3+1)*(3**3+1) == 112
    zero2 = ((0,0),(0,0))
    assert all(mm(mm(plane,h),adjoint(plane)) == zero2 for plane in planes)
    perms = [tuple(index[rref(mm(plane,g))] for plane in planes) for g in gens]
    identity = tuple(range(112))
    assert all(compose(g,g) == identity and g != identity for g in perms)
    assert compose(perms[0],perms[2]) == compose(perms[2],perms[0]) != identity
    group = PermutationGroup([Permutation(list(g)) for g in perms])
    order = int(group.order())
    expected = 2*3**6*(3**2-1)*(3**3+1)*(3**4-1)//4
    assert order == expected == 6531840
    masks = range(8)
    proper = {mask: closure([perms[i] for i in range(3) if mask & (1<<i)], identity)
              for mask in masks if mask != 7}
    # The full group is the already order-certified generated group. Meets with
    # it are tautological, while every proper/proper meet is enumerated exactly.
    meets = 0
    for s in masks:
        for u in masks:
            if s == 7 or u == 7:
                assert (s & u) == min(s,u)
            else:
                assert proper[s] & proper[u] == proper[s & u]
            meets += 1
    def perm_order(g):
        x = identity
        for n in range(1, 100):
            x = compose(x,g)
            if x == identity:
                return n
        raise AssertionError('order unexpectedly exceeds finite bound')
    schlafli = [perm_order(compose(perms[i],perms[i+1])) for i in range(2)]
    assert schlafli == [8,6]
    report = {
        'status': 'PASS', 'field': 'F3[T]/(T^2-T-1)',
        'field_encoding': 'a+3*b encodes a+b*T',
        'q': 3, 'isotropic_plane_orbit': len(planes),
        'projective_image_order': order, 'expected_U2_order': expected,
        'schlafli_type': schlafli, 'marked_subgroups': 8,
        'proper_subgroup_orders_by_mask': {str(k):len(v) for k,v in proper.items()},
        'proper_pair_meets_enumerated': 49, 'all_marked_meets': meets,
        'large_order_algorithm': 'SymPy PermutationGroup.order (Schreier--Sims)',
        'sympy_version': sympy.__version__,
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'elapsed_seconds': round(time.monotonic()-start,6),
        'scope': 'Literal-coordinate q=3 base only. Independent arithmetic and plane orbit; no GAP, ATLAS, author code, or group-recognition oracle. Classical unitary order and the written projective containment supply the order sandwich. No uniform-q claim follows from this check.'
    }
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
