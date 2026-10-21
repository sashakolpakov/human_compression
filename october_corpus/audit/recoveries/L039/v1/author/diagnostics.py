#!/usr/bin/env python3
"""Optional small-coordinate validation; no Ree enumeration or proof premise."""
import itertools
import json

def need(ok, message):
    if not ok:
        raise ValueError(message)

def mul(a, b):
    ans = 0
    while b:
        if b & 1:
            ans ^= a
        b >>= 1
        a <<= 1
        if a & 8:
            a ^= 0b1011
    return ans

def mm(a, b):
    return (mul(a[0], b[0]) ^ mul(a[1], b[2]),
            mul(a[0], b[1]) ^ mul(a[1], b[3]),
            mul(a[2], b[0]) ^ mul(a[3], b[2]),
            mul(a[2], b[1]) ^ mul(a[3], b[3]))

def inv(a):
    return (a[3], a[1], a[2], a[0])

def power(a, n):
    ans = (1, 0, 0, 1)
    for _ in range(n):
        ans = mm(ans, a)
    return ans

def conj(x, g):
    return mm(mm(inv(g), x), g)

def main():
    group = [a for a in itertools.product(range(8), repeat=4)
             if mul(a[0], a[3]) ^ mul(a[1], a[2]) == 1]
    need(len(group) == 504, 'literal SL2(8) order')
    lam = 2
    lam_inv = next(x for x in range(1, 8) if mul(lam, x) == 1)
    r = (lam, 0, 0, lam_inv)
    w = (0, 1, 1, 0)
    rotations = {power(r, i) for i in range(7)}
    reflections = {mm(w, x) for x in rotations}
    d = rotations | reflections
    need(len(d) == 14, 'split dihedral')
    normalizer = [g for g in group if {conj(x, g) for x in d} == d]
    centralizer = [g for g in group if all(conj(x, g) == x for x in (r, w))]
    need(set(normalizer) == d and centralizer == [(1, 0, 0, 1)], 'K normalizer/centralizer')
    def frob(x, e):
        for _ in range(e):
            x = tuple(mul(a, a) for a in x)
        return x
    pair = (w, mm(w, r))
    orbit = {(conj(frob(pair[0], e), g), conj(frob(pair[1], e), g))
             for e in range(3) for g in normalizer}
    expected = {(x, y) for x in reflections for y in reflections if x != y}
    need(orbit == expected and len(orbit) == 42, 'all ordered pairs under inner-field action')
    need(frob(r, 1) == power(r, 2) and frob(w, 1) == w, 'field map on torus')
    need(len(group) // len(normalizer) == 36, 'dihedral subgroup count in K')
    # The endpoint transposition generates a genuinely nonabelian 2-group.
    def permutation_product(a, b):
        return tuple(b[a[i]] for i in range(len(a)))
    i4 = tuple(range(4))
    a = (1, 0, 3, 2)
    b = (2, 3, 0, 1)
    u = (0, 2, 1, 3)
    closure = {i4}
    todo = [i4]
    while todo:
        x = todo.pop()
        for g in (a, b, u):
            y = permutation_product(x, g)
            if y not in closure:
                closure.add(y)
                todo.append(y)
    need(len(closure) == 8 and permutation_product(a, u) != permutation_product(u, a), 'D8 contradiction model')
    need(permutation_product(permutation_product(u, a), u) == b, 'endpoint swap')
    # Unipotent order-three actions over F3 have nonzero fixed vectors.
    fixed_checks = []
    for dim in range(1, 7):
        vectors = list(itertools.product(range(3), repeat=dim))
        # All direct sums of Jordan blocks of sizes <=3 represented by compositions.
        def compositions(n):
            if n == 0:
                yield []
            for k in range(1, min(3, n) + 1):
                for rest in compositions(n-k):
                    yield [k]+rest
        for blocks in compositions(dim):
            cuts = set(itertools.accumulate(blocks))
            def action(v):
                return tuple((v[i] + (v[i+1] if i+1 < dim and i+1 not in cuts else 0)) % 3
                             for i in range(dim))
            need(all(action(action(action(v))) == v for v in vectors), 'order-three linear action')
            count = sum(action(v) == v for v in vectors)
            need(count >= 3 and count % 3 == 0, 'nontrivial fixed vector')
            fixed_checks.append({'dimension': dim, 'blocks': blocks, 'fixed': count})
    return {'status': 'PASS', 'role': 'OPTIONAL_VALIDATION_NOT_A_PROOF_PREMISE',
            'SL2_8_order': 504, 'dihedral_order': 14, 'centralizer_order': 1,
            'normalizer_order': 14, 'ordered_pair_orbit': 42,
            'K_dihedral_subgroups': 36, 'endpoint_swap_group_order': 8,
            'order_three_fixed_checks': len(fixed_checks),
            'Ree_groups_enumerated': 0}

if __name__ == '__main__':
    print(json.dumps(main(), indent=2))
