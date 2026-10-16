"""Literal identities for the binary intermediate example; no group search.

All entries lie in the prime field, fixed by every relevant Frobenius.
The extension from basis defects to all orthogonal pairs is a written proof.
"""
import json

if not __debug__:
    raise SystemExit('optimization is not an admitted execution mode')


def need(value, message):
    if not value:
        raise ValueError(message)


def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(4)) % 2
             for j in range(4)] for i in range(4)]


def mv(a, v):
    return [sum(a[i][j] * v[j] for j in range(4)) % 2 for i in range(4)]


def product(u, v):
    return [(u[1] * v[3] + u[3] * v[1]) % 2,
            (u[0] * v[1] + u[1] * v[0]) % 2,
            (u[2] * v[3] + u[3] * v[2]) % 2,
            (u[0] * v[2] + u[2] * v[0]) % 2]


def check(x):
    need(len(x) == 4 and all(len(r) == 4 for r in x), 'matrix shape')
    need(all(type(v) is int and v in [0, 1] for r in x for v in r), 'prime field')
    j = [[int(i + k == 3) for k in range(4)] for i in range(4)]
    need(x == [list(r) for r in zip(*x)], 'symmetry')
    need(mul(mul(x, j), x) == j, 'symplectic identity')
    basis = [[int(i == k) for k in range(4)] for i in range(4)]
    defects = {}
    for i in range(4):
        for k in range(i + 1, 4):
            left = product(mv(x, basis[i]), mv(x, basis[k]))
            right = mv(x, product(basis[i], basis[k]))
            defects[str(i + 1) + str(k + 1)] = [(a + b) % 2 for a, b in zip(left, right)]
    for pair in ['12', '13', '24', '34']:
        need(defects[pair] == [0, 0, 0, 0], 'orthogonal defect ' + pair)
    need(defects['14'] == defects['23'] == [0, 1, 0, 0], 'nonorthogonal defects')
    sides = [x[0][1] * x[0][3] % 2, x[0][0] * x[1][3] % 2]
    need(sides == [1, 0], 'source equation 14 counterexample')
    return dict(status='PASS_BINARY_INTERMEDIATE_EXAMPLE', matrix=x,
                symmetric=True, xJx_equals_J=True, basis_defects=defects,
                source_equation_14_sides=sides, group_elements_enumerated=0,
                polytope_witness_reacquired=False,
                general_field_extension='Prime-field entries and the proved defect lemma')


MATRIX = [[0, 1, 0, 1], [1, 1, 1, 0], [0, 1, 0, 0], [1, 0, 0, 0]]


if __name__ == '__main__':
    print(json.dumps(check(MATRIX), indent=2))
