"""Exact characteristic-two polynomial certificate for the Suzuki cycle proof.

Polynomials are sets of Laurent monomials: addition is symmetric difference.
This checks identities in F2[a,A,b,B,c,C,d,D], not just sampled field values.
"""
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
N = 8
ZERO = frozenset()
ONE = frozenset({(0,) * N})


def var(i, exponent=1):
    v = [0] * N
    v[i] = exponent
    return frozenset({tuple(v)})


def add(*args):
    result = ZERO
    for arg in args:
        result = result ^ arg
    return result


def mul(*args):
    result = ONE
    for arg in args:
        out = set()
        for x in result:
            for y in arg:
                m = tuple(a+b for a, b in zip(x, y))
                if m in out:
                    out.remove(m)
                else:
                    out.add(m)
        result = frozenset(out)
    return result


def mm(a, b):
    return tuple(tuple(add(*(mul(a[i][k], b[k][j]) for k in range(4)))
                       for j in range(4)) for i in range(4))


def product(*matrices):
    out = tuple(tuple(ONE if i == j else ZERO for j in range(4)) for i in range(4))
    for matrix in matrices:
        out = mm(out, matrix)
    return out


def z(a, A):
    return ((ONE,ZERO,ZERO,ZERO), (ZERO,ONE,ZERO,ZERO),
            (a,ZERO,ONE,ZERO), (A,a,ZERO,ONE))


w = tuple(tuple(ONE if i+j == 3 else ZERO for j in range(4)) for i in range(4))
a,A,b,B,c,C,d,D = [var(i) for i in range(N)]
short3 = product(w,z(a,A),w,z(b,B),w)
short4 = product(w,z(a,A),w,z(b,B),w,z(c,C),w)
full = product(w,z(a,A),w,z(b,B),w,z(c,C),w,z(d,D),w)
assert short3[2][1] == ONE
assert short4[0][1] == mul(A,b)
assert full[2][1] == add(mul(b,c),ONE)
assert full[0][1] == add(mul(A,B,c),mul(a,b,c),a,c)
assert full[3][2] == add(mul(B,C,d),mul(b,c,d),b,d)

ai,Ai = var(0,-1),var(1,-1)
closing = product(w,z(a,A),w,z(ai,Ai),w,z(a,A),w,z(ai,Ai),w)
diag = (A,mul(a,a,Ai),mul(A,ai,ai),Ai)
expected = product(z(ai,Ai),tuple(tuple(diag[i] if i == j else ZERO
                                      for j in range(4)) for i in range(4)))
assert closing == expected


def display(poly):
    names = ['a','A','b','B','c','C','d','D']
    if not poly:
        return '0'
    terms = []
    for monomial in sorted(poly):
        factors = [name if e == 1 else f'{name}^{e}' for name,e in zip(names,monomial) if e]
        terms.append('*'.join(factors) or '1')
    return ' + '.join(terms)


report = {
    'status':'PASS',
    'scope':'Universal polynomial and Laurent-polynomial identities in characteristic two; no floating point.',
    'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
    'three_step_obstruction':display(short3[2][1]),
    'four_step_obstruction':display(short4[0][1]),
    'five_step_zero_entries':{'32':display(full[2][1]),'12':display(full[0][1]),'43':display(full[3][2])},
    'all_sixteen_closing_entries_match':True,
    'closing_matrix':[[display(x) for x in row] for row in closing],
    'remaining_written_steps':['Frobenius injectivity identifies ab=1.',
                               'theta squared equals squaring identifies the diagonal with a Suzuki torus element.',
                               'Coset-walk parametrization identifies the matrix solutions with pentagons.']}
(ROOT/'suzuki_cycle_check.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: five universal matrix entries and all 16 Laurent-polynomial closing entries.')
