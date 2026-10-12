"""Exact bounded L023 instance. Python integers only; no group/graph backend.

Required finite premise: the displayed SL2(8) marking and its intersections.
The 32-element torus and 72-element product parabolics corroborate the written
counterexample. This is not a census of maps. No external mathematical data.
"""
import argparse
import itertools as it
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def closure(generators, multiply, one):
    seen = {one}
    todo = [one]
    for x in todo:
        for g in generators:
            y = multiply(x, g)
            if y not in seen:
                seen.add(y)
                todo.append(y)
    return seen


def power(g, n, multiply, one):
    ans = one
    for _ in range(n):
        ans = multiply(ans, g)
    return ans


def order(g, multiply, one, bound):
    x = one
    for n in range(1, bound + 1):
        x = multiply(x, g)
        if x == one:
            return n
    raise ValueError('order bound exhausted')


def field_multiply(a, b):
    ans = 0
    while b:
        if b & 1:
            ans ^= a
        b >>= 1
        a <<= 1
        if a & 8:
            a ^= 11  # X^3+X+1
    return ans


def matrix_multiply(a, b):
    f = field_multiply
    return (f(a[0], b[0]) ^ f(a[1], b[2]),
            f(a[0], b[1]) ^ f(a[1], b[3]),
            f(a[2], b[0]) ^ f(a[3], b[2]),
            f(a[2], b[1]) ^ f(a[3], b[3]))


def integer_multiply(a, b):
    return (a[0]*b[0]+a[1]*b[2], a[0]*b[1]+a[1]*b[3],
            a[2]*b[0]+a[3]*b[2], a[2]*b[1]+a[3]*b[3])


I = (1, 0, 0, 1)
T_ONE = ((0, 0), I)


def torus_multiply(g, h):
    t, a = g
    u, b = h
    return (((t[0]+a[0]*u[0]+a[1]*u[1]) % 2,
             (t[1]+a[2]*u[0]+a[3]*u[1]) % 2),
            integer_multiply(a, b))


def cosets(group, subgroup, multiply):
    return sorted({frozenset(multiply(g, h) for h in subgroup) for g in group},
                  key=lambda x: sorted(x))


def parabolics(r, multiply, one):
    a, b, c = r
    return [closure(gs, multiply, one) for gs in
            [(a, b), (a, c), (b, c), (b, multiply(a, c))]]


def check_ip(r, multiply, one):
    subgroups = [closure([r[i] for i in range(3) if mask >> i & 1],
                        multiply, one) for mask in range(8)]
    for i, j in it.product(range(8), repeat=2):
        require(subgroups[i] & subgroups[j] == subgroups[i & j],
                'intersection property')
    return [len(h) for h in subgroups]


def check_marked_hom(r, images, multiply, one):
    image = {one: one}
    todo = [one]
    for x in todo:
        for a, b in zip(r, images):
            y, z = multiply(x, a), multiply(image[x], b)
            if y in image:
                require(image[y] == z, 'marked homomorphism relation')
            else:
                image[y] = z
                todo.append(y)
    require(len(set(image.values())) == len(image), 'marked map bijective')
    return image


def evaluate(word, r, multiply, one):
    out = one
    for letter in word:
        out = multiply(out, r['abc'.index(letter)])
    return out


def run():
    r = [(1, 2, 0, 1), (0, 1, 1, 0), (1, 4, 0, 1)]
    s = closure(r, matrix_multiply, I)
    det_one = {x for x in it.product(range(8), repeat=4)
               if field_multiply(x[0], x[3]) ^ field_multiply(x[1], x[2]) == 1}
    require(s == det_one and len(s) == 504, 'complete SL2(8) generation')
    require(all(x != I and matrix_multiply(x, x) == I for x in r), 'involutions')
    a, b, c = r
    require(matrix_multiply(a, c) == matrix_multiply(c, a), 'commutation')
    periods = [order(matrix_multiply(x, b), matrix_multiply, I, 504)
               for x in (a, c, matrix_multiply(a, c))]
    require(periods == [9]*3, 'three periods nine')
    seed_ip = check_ip(r, matrix_multiply, I)
    sq = lambda x: tuple(field_multiply(y, y) for y in x)
    require([sq(a), sq(c), sq(matrix_multiply(a, c)), sq(b)] ==
            [c, matrix_multiply(a, c), a, b], 'field triality')
    require(all(sq(matrix_multiply(x, g)) == matrix_multiply(sq(x), sq(g))
                for x in s for g in r), 'field generator-edge homomorphism')
    word = 'abababcbcbcbababc'
    require(evaluate(word, r, matrix_multiply, I) == I, 'literal relation')
    swapped = evaluate(word, [c, b, a], matrix_multiply, I)
    require(swapped == (6, 6, 2, 1) and swapped != I, 'duality obstruction')
    involutions = {x for x in s if x != I and matrix_multiply(x, x) == I}
    conjugates = set()
    for x in s:
        inv = (x[3], x[1], x[2], x[0])
        conjugates.add(matrix_multiply(matrix_multiply(inv, a), x))
    require(involutions == conjugates and len(involutions) == 63, 'one involution class')

    tr = [((1, 0), (-1, 0, 0, 1)), ((0, 0), (0, 1, 1, 0)),
          ((0, 0), (1, 0, 0, -1))]
    t = closure(tr, torus_multiply, T_ONE)
    require(len(t) == 32, 'full flag torus group, not vertex image')
    ta, tb, tc = tr
    th = parabolics(tr, torus_multiply, T_ONE)
    torus_ip = check_ip(tr, torus_multiply, T_ONE)
    require(list(map(len, th)) == [8, 4, 8, 8], 'torus parabolics')
    translation, central = ((1, 1), I), ((0, 0), (-1, 0, 0, -1))
    rotations = [torus_multiply(x, tb) for x in
                 (ta, tc, torus_multiply(ta, tc))]
    require([power(x, 2, torus_multiply, T_ONE) for x in rotations] ==
            [torus_multiply(translation, central), central, translation], 'torus words')
    check_marked_hom(tr, [tc, tb, torus_multiply(ta, tc)], torus_multiply, T_ONE)
    check_marked_hom(tr, [tc, tb, ta], torus_multiply, T_ONE)
    cs = [cosets(t, h, torus_multiply) for h in th]
    bad = [th[0], {torus_multiply(translation, h) for h in th[2]}, th[3]]
    require(all(x & y for x, y in it.combinations(bad, 2)), 'torus flag incidence')
    completions = [e for e in cs[1] if all(e & x for x in bad)]
    require(not completions, 'no torus completing edge')
    require(any(all(e & x for x in (th[0],th[2],th[3])) for e in cs[1]),
            'base flag has a completion: noncompletion test is discriminating')
    vertex_permutations = {tuple(((g[0][0]+g[1][0]*u+g[1][1]*v)%2,
                                 (g[0][1]+g[1][2]*u+g[1][3]*v)%2)
                                for u,v in it.product(range(2),repeat=2)) for g in t}
    require(len(vertex_permutations)==8, 'vertex-only action loses kernel four')
    bad_count = sum(not any(all(e & x for x in flag) for e in cs[1])
                    for flag in it.product(cs[0], cs[2], cs[3])
                    if all(x & y for x, y in it.combinations(flag, 2)))
    chambers = sum(all(x & y for x, y in it.combinations(flag, 2))
                   for flag in it.product(*cs))
    require((bad_count, chambers) == (16, 64), 'torus complete flag audit')

    # Full product group need not be enumerated: written Goursat proof gives it.
    pm = lambda x, y: (matrix_multiply(x[0], y[0]), torus_multiply(x[1], y[1]))
    po = (I, T_ONE)
    pr = list(zip(r, tr))
    ph = parabolics(pr, pm, po)
    require(list(map(len, ph)) == [72, 4, 72, 72], 'product parabolic sizes')
    require(ph[0] & ph[2] == {po, pr[1]}, 'product end intersection')
    require(ph[0] & ph[1] == {po, pr[0]} and
            ph[2] & ph[1] == {po, pr[2]}, 'product endpoint intersections')
    z = (I, translation)
    pa, pb, pc = pr
    require(power(pm(pm(pa, pc), pb), 18, pm, po) == z and z in ph[3], 'product z word')
    require(pm(power(pm(pa, pb), 18, pm, po),
               power(pm(pb, pc), 18, pm, po)) == z, 'product z factorization')
    pbflag = [ph[0], {pm(z, x) for x in ph[2]}, ph[3]]
    require(all(x & y for x, y in it.combinations(pbflag, 2)), 'product actual flag')
    require([{x[1] for x in f} for f in pbflag] == bad, 'exact projection to obstruction')
    sh = parabolics(r, matrix_multiply, I)
    for i, sr, tt in [(0, matrix_multiply(a,b), rotations[0]),
                      (2, matrix_multiply(c,b), rotations[1]),
                      (3, matrix_multiply(matrix_multiply(a,c),b), rotations[2])]:
        sr0 = {power(sr, n, matrix_multiply, I) for n in range(9)}
        tt0 = {power(tt, n, torus_multiply, T_ONE) for n in range(4)}
        expected = {(x,y) for x in sh[i] for y in th[i] if (x in sr0) == (y in tt0)}
        require(ph[i] == expected, 'exact parity fiber product')

    # Two small dihedra corroborate the uniform written odd/even arguments.
    dihedra=[]
    for n in [3,4]:
        dm = lambda x,y: (tuple(x[0][i] for i in y[0]), x[1]^y[1])
        do = (tuple(range(n)),0)
        dr = [(tuple((1-i)%n for i in range(n)),0),
              (tuple((-i)%n for i in range(n)),0),(tuple(range(n)),1)]
        dg = closure(dr,dm,do);dh=parabolics(dr,dm,do)
        require(len(dg)==4*n, 'dihedron group')
        dc=[cosets(dg,h,dm) for h in dh]
        dch=sum(all(x&y for x,y in it.combinations(f,2)) for f in it.product(*dc))
        require(dch==(4*n if n%2 else 8*n),'dihedron chambers')
        require(all(x&y for i,j in it.combinations(range(4),2) if {i,j}!={1,2}
                    for x in dc[i] for y in dc[j]),'all incidence outside vertex-edge complete')
        require(all(sum(bool(v&e) for e in dc[1])==2 for v in dc[2]) and
                all(sum(bool(v&e) for v in dc[2])==2 for e in dc[1]), 'incidence cycle valencies')
        if n%2: require(dh[3]==dg, 'odd universal Petrie type')
        else:
            require(dh[3]!=dh[0] and len(dh[3])==2*n and dh[3]&dh[2]=={do,dr[1]},'even Petrie pair')
            check_marked_hom(dr,[dm(dr[0],dr[2]),dr[1],dr[2]],dm,do)
        dihedra.append({'n':n,'order':len(dg),'chambers':dch,'parabolic_orders':list(map(len,dh))})
    return {'status': 'PASS', 'seed': {'field_polynomial': 11, 'matrices': r,
        'order': 504, 'periods': periods, 'subgroup_orders': seed_ip,
        'ip_identities': 64, 'no_duality_word': word, 'swapped_value': swapped,
        'involution_class_size': 63}, 'torus': {'order':32, 'markers':tr,
        'subgroup_orders': torus_ip, 'ip_identities':64, 'parabolics':[8,4,8,8],
        'bad_face_vertex_petrie_flags':bad_count, 'full_type_chambers':chambers,
        'witness_translation':translation, 'edge_completions':0,
        'vertex_only_image_order':8,'base_flag_has_completion':True},
        'parallel_product': {'order_by_written_theorem':16128, 'period':36,
        'parabolic_orders':[72,4,72,72], 'z':z, 'exact_parity_fibers':3,
        'all_three_flag_pairs_nonempty':True, 'projected_completion_impossible':True},
        'dihedron_optional_checks': dihedra,
        'scope':'fixed instance; no map census or general theorem decided by sampling'}


def controls():
    # Discriminating rejected mathematical weakenings, separate from premises.
    ans = []
    r = [(1,2,0,1),(0,1,1,0),(1,4,0,1)]
    for name, body in [
        ('duality is a marked automorphism', lambda: check_marked_hom(r,[r[2],r[1],r[0]],matrix_multiply,I)),
        ('wrong word is the identity', lambda: require(evaluate('abababcbcbcbabab',r,matrix_multiply,I)==I,'word')),
        ('repeated endpoint generates SL2(8)', lambda: require(len(closure([r[0],r[1],r[0]],matrix_multiply,I))==504,'generation')),
        ('wrong field relation u^3=1', lambda: require(field_multiply(field_multiply(2,2),2)==1,'field'))]:
        try:
            body()
        except ValueError:
            ans.append({'control':name,'rejected':True})
        else:
            raise ValueError('control unexpectedly passed: '+name)
    return ans


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    result = run()
    result['negative_controls'] = controls()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2)+'\n')
    print('PASS: SL2(8), torus, three exact product fibers, four rejected controls')
