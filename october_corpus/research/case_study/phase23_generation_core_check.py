#!/usr/bin/env python3
"""Exact diagnostics for phase23_generation_core.md; not a universal proof.

Requires Python 3 and SymPy. Run a scratch copy to preserve old reports.
The finite H^1 calculation builds every cocycle equation independently.
"""
from datetime import datetime, timezone
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import sympy as S

HERE = Path(__file__).resolve().parent
checks = []


def zero(label, expr):
    entries = list(expr) if isinstance(expr, S.MatrixBase) else [expr]
    assert all(S.cancel(x) == 0 for x in entries), label
    checks.append(label)


def mod3(expr):
    """Reduce integer Laurent-polynomial coefficients, preserving variables."""
    expr = S.expand(expr)
    out = 0
    for term in S.Add.make_args(expr):
        coeff, rest = term.as_coeff_Mul()
        assert coeff.q == 1
        out += int(coeff) % 3 * rest
    return S.expand(out)


def zero3(label, expr):
    entries = list(expr) if isinstance(expr, S.MatrixBase) else [expr]
    assert all(mod3(x) == 0 for x in entries), label
    checks.append(label)


u, w, ur, wr, a, z = S.symbols('u w ur wr a z', nonzero=True)
du = S.Matrix(2, 2, S.symbols('u11 u12 u21 u22'))
dw = S.Matrix(2, 2, S.symbols('w11 w12 w21 w22'))
Pu = S.Matrix([[1, u], [0, 1]])
Qw = S.Matrix([[1, 0], [-wr, 1]])
off = Pu * dw + du * Qw
expected = S.Matrix([
    [du[0, 0]+dw[0, 0]+u*dw[1, 0]-wr*du[0, 1],
     du[0, 1]+dw[0, 1]+u*dw[1, 1]],
    [du[1, 0]+dw[1, 0]-wr*du[1, 1], du[1, 1]+dw[1, 1]]])
zero('four off-block cocycle identities', off-expected)
torus_off = S.diag(a, 1/a)*du*S.diag(z, 1/z)
zero('four torus weights', torus_off-S.Matrix([
    [a*z*du[0, 0], a/z*du[0, 1]],
    [z/a*du[1, 0], du[1, 1]/(a*z)]]))

X = S.Matrix(2, 2, S.symbols('x11 x12 x21 x22'))
for i, j in product(range(2), repeat=2):
    k, ell = 1-i, 1-j
    left, right, target = S.zeros(2), S.zeros(2), S.zeros(2)
    left[k, i], right[j, ell], target[k, ell] = 1, 1, u*w*X[i, j]
    zero(f'independent root differences {i}{j}',
         (S.eye(2)+u*left)*X*(S.eye(2)+w*right)
         -(S.eye(2)+u*left)*X-X*(S.eye(2)+w*right)+X-target)

# Cubic symmetric power, constructed directly from polynomial substitutions.
x, y = S.symbols('x y')
basis = [x**3, x*x*y, x*y*y, y**3]


def symmetric_cube(g):
    f1, f2 = g[0, 0]*x+g[1, 0]*y, g[0, 1]*x+g[1, 1]*y
    images = [f1**3, f1*f1*f2, f1*f2*f2, f2**3]
    return S.Matrix(4, 4, lambda i, j: S.Poly(
        S.expand(images[j]), x, y).coeff_monomial(basis[i]))


conj = S.diag(1, -1)
for label, g, twist in [
    ('upper', S.Matrix([[1, u], [0, 1]]), S.Matrix([[1, u**3], [0, 1]])),
    ('lower', S.Matrix([[1, 0], [u, 1]]), S.Matrix([[1, 0], [u**3, 1]])),
    ('torus', S.diag(a, 1/a), S.diag(a**3, a**-3))]:
    sc = symmetric_cube(g)
    zero3(f'cubic {label} invariant cube space', sc.extract([1, 2], [0, 3]))
    zero3(f'cubic {label} Frobenius submodule', sc.extract([0, 3], [0, 3])-twist)
    zero3(f'cubic {label} natural quotient',
          conj*sc.extract([1, 2], [1, 2])*conj-g)

sc = symmetric_cube(S.Matrix([[1, 1], [0, 1]])).applyfunc(mod3)
displayed = S.Matrix([[1, 1, 1, 1], [0, 1, -1, 0],
                      [0, 0, 1, 0], [0, 0, 0, 1]])
zero3('displayed cubic unipotent', sc-displayed)
nil = sc-S.eye(4)
assert any(mod3(c) for c in nil**2)
zero3('cubic nilpotent cube', nil**3)


def rank_mod(rows, p):
    rows = [[int(t) % p for t in row] for row in rows]
    rank = 0
    if not rows:
        return 0
    for col in range(len(rows[0])):
        pivot = next((i for i in range(rank, len(rows)) if rows[i][col]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col], -1, p)
        rows[rank] = [t*inv % p for t in rows[rank]]
        for i in range(rank+1, len(rows)):
            coeff = rows[i][col]
            rows[i] = [(a-coeff*b) % p for a, b in zip(rows[i], rows[rank])]
        rank += 1
    return rank


nil_ranks = [rank_mod((nil**i).tolist(), 3) for i in (1, 2, 3)]
assert nil_ranks == [2, 1, 0]
checks.append('cubic exception Jordan ranks 2,1,0')

# Complete cocycle computation for SL2(F2) x SL2(F2), no presentation oracle.
def mm(g, h):
    return tuple(sum(g[2*i+k]*h[2*k+j] for k in range(2)) % 2
                 for i in range(2) for j in range(2))


def inv(g):
    return (g[3], g[1], g[2], g[0])


sl2 = [g for g in product(range(2), repeat=4) if (g[0]*g[3]-g[1]*g[2]) % 2 == 1]
assert len(sl2) == 6
group = list(product(sl2, repeat=2))
idx = {g: i for i, g in enumerate(group)}
units = [tuple(int(k == j) for k in range(4)) for j in range(4)]
actions = []
for g, h in group:
    columns = [mm(mm(g, e), inv(h)) for e in units]
    actions.append([[columns[j][i] for j in range(4)] for i in range(4)])

pivots = {}
equations = 0
for i, (g1, g2) in enumerate(group):
    for j, (h1, h2) in enumerate(group):
        ij = idx[(mm(g1, h1), mm(g2, h2))]
        for r in range(4):
            row = (1 << (4*ij+r)) ^ (1 << (4*i+r))
            for s in range(4):
                if actions[i][r][s]:
                    row ^= 1 << (4*j+s)
            while row:
                pivot = row.bit_length()-1
                if pivot not in pivots:
                    pivots[pivot] = row
                    break
                row ^= pivots[pivot]
            equations += 1
cocycle_dimension = 4*len(group)-len(pivots)
coboundary_rows = [[actions[i][r][s] ^ int(r == s) for s in range(4)]
                  for i in range(len(group)) for r in range(4)]
coboundary_dimension = rank_mod(coboundary_rows, 2)
assert cocycle_dimension == coboundary_dimension == 4
checks.append('complete characteristic-two product H1 vanishing')

# Explicit unitary complement over F9 = F3[i]/(i^2+1), all 720 elements.
# Integers a+3*b encode a+b*i. No external finite-field or group backend.
def fa(x, y):
    return (x % 3+y % 3) % 3+3*((x//3+y//3) % 3)


def fn(x):
    return (-(x % 3) % 3)+3*((-(x//3)) % 3)


def fm(x, y):
    a, b, c, d = x % 3, x//3, y % 3, y//3
    return (a*c-b*d) % 3+3*((a*d+b*c) % 3)


def fp(x, n):
    out = 1
    while n:
        if n & 1:
            out = fm(out, x)
        x = fm(x, x)
        n //= 2
    return out


def fsum(xs):
    out = 0
    for x in xs:
        out = fa(out, x)
    return out


def matmul(g, h):
    n, mid, m = len(g), len(h), len(h[0])
    return tuple(tuple(fsum(fm(g[i][k], h[k][j]) for k in range(mid))
                       for j in range(m)) for i in range(n))


def matadd(g, h):
    return tuple(tuple(fa(a, b) for a, b in zip(r, s)) for r, s in zip(g, h))


def scale(g, c):
    return tuple(tuple(fm(x, c) for x in row) for row in g)


def star(g):
    return tuple(tuple(fp(g[j][i], 3) for j in range(len(g)))
                 for i in range(len(g[0])))


def inv2(g):
    return ((g[1][1], fn(g[0][1])), (fn(g[1][0]), g[0][0]))


def eye(n):
    return tuple(tuple(int(i == j) for j in range(n)) for i in range(n))


f9sl2 = [((a, b), (c, d)) for a, b, c, d in product(range(9), repeat=4)
         if fa(fm(a, d), fn(fm(b, c))) == 1]
assert len(f9sl2) == 720
root_generators = [((1, v), (0, 1)) for v in (1, 3)]
root_generators += [((1, 0), (v, 1)) for v in (1, 3)]
seen, todo = {eye(2)}, [eye(2)]
while todo:
    g = todo.pop()
    for h in root_generators:
        gh = matmul(g, h)
        if gh not in seen:
            seen.add(gh)
            todo.append(gh)
assert len(seen) == 720


def cocycle_minus(g):
    (a, b), (c, d) = g
    d3 = ((fm(fm(a, a), b), fm(a, fm(b, b))),
          (fm(fm(c, c), d), fm(c, fm(d, d))))
    transpose = tuple(zip(*d3))
    c0 = scale(matmul(matmul(g, ((0, 1), (1, 0))), transpose), 2)
    return scale(matadd(c0, scale(star(c0), 2)), 2)


def graph(g):
    lower = star(inv2(g))
    off = matmul(cocycle_minus(g), lower)
    return tuple(tuple(g[i][j] if i < 2 and j < 2 else
                       off[i][j-2] if i < 2 else
                       0 if j < 2 else lower[i-2][j-2]
                       for j in range(4)) for i in range(4))


hermitian = ((0, 0, 1, 0), (0, 0, 0, 1),
             (1, 0, 0, 0), (0, 1, 0, 0))
graphs = {g: graph(g) for g in f9sl2}
for g in f9sl2:
    pg = graphs[g]
    assert matmul(matmul(star(pg), hermitian), pg) == hermitian
    for h in root_generators:
        assert matmul(pg, graphs[h]) == graphs[matmul(g, h)]
assert len(set(graphs.values())) == 720
uf = root_generators[0]
assert cocycle_minus(uf) == ((0, 2), (1, 0))
nil9 = matadd(graphs[uf], scale(eye(4), 2))
nil9sq = matmul(nil9, nil9)
assert nil9sq == ((0, 0, 2, 0), (0, 0, 0, 0),
                  (0, 0, 0, 0), (0, 0, 0, 0))
assert matmul(nil9sq, nil9) == tuple((0,)*4 for _ in range(4))
checks.append('all 720 explicit unitary complement matrices and 2880 generator products')
checks.append('explicit F9 skew-Hermitian complement has Jordan-three element')

# Bounded integer diagnostics for the all-parameter inequality proof.
primes = list(S.primerange(3, 100))
parameter_cases, congruences, exceptional_cases = 0, 0, []
for p in primes:
    for m in range(2, 17):
        for f in range(1, m):
            modulus, r = int(p)**m-1, int(p)**f
            weights = {(1+r) % modulus, (1-r) % modulus,
                       (r-1) % modulus, (-r-1) % modulus}
            hits = [(j, (2*int(p)**j) % modulus) for j in range(m)
                    if (2*int(p)**j) % modulus in weights]
            expected = p == 3 and f in {1, m-1}
            assert bool(hits) == expected, (p, m, f, hits)
            if hits:
                exceptional_cases.append({'p': int(p), 'm': m, 'f': f, 'hits': hits})
            parameter_cases += 1
            congruences += 4*m
checks.append('bounded nonresonance roster matches exact stated cases')

report = {
    'status': 'PASS',
    'executed_utc': datetime.now(timezone.utc).isoformat(),
    'script_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
    'proof_sha256': sha256((HERE/'phase23_generation_core.md').read_bytes()).hexdigest(),
    'symbolic_and_exact_checks': checks,
    'check_count': len(checks),
    'product_H1': {'field_order': 2, 'factor_order': 6, 'group_order': 36,
                   'module_dimension': 4, 'cocycle_variables': 144,
                   'cocycle_equations': equations, 'equation_rank': len(pivots),
                   'Z1_dimension': cocycle_dimension, 'B1_dimension': coboundary_dimension,
                   'H1_dimension': cocycle_dimension-coboundary_dimension},
    'cubic_exception': {'characteristic': 3, 'nilpotent_power_ranks': nil_ranks,
                        'Jordan_type': [3, 1]},
    'unitary_exception': {'field_polynomial_low_to_high': [1, 0, 1],
                           'field_order': 9, 'complement_order': 720,
                           'all_unitary_relations': 720, 'generator_products': 2880,
                           'radical_intersection_order': 1, 'Jordan_type': [3, 1]},
    'weight_diagnostics': {'primes': [int(p) for p in primes], 'm_range': [2, 16],
                           'parameter_cases': parameter_cases, 'congruences': congruences,
                           'exceptional_cases': exceptional_cases},
    'scope': 'Exact identities and finite diagnostics only; the universal proofs and hypotheses remain in the note.',
}
output = HERE/'phase23_generation_core_check.json'
output.write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({k: report[k] for k in ['status', 'check_count', 'product_H1', 'cubic_exception']}))
