"""Exact determinant certificate for the naive PSL3-to-PSU3 substitution.

SymPy performs polynomial arithmetic over ZZ[x]; no numerical rank test.
The matrix coefficients express bar(M).T H M = H, with bar(x)=1/x.
"""
import sympy as s
from sympy.polys.matrices import DomainMatrix

x = s.symbols('x')
matrices = [
    s.Matrix([[x, 1, 0], [0, 1+1/x, -1/x], [0, 1, 0]]),
    s.Matrix([[-1/x, 0, 0], [0, 0, 1], [0, x, 0]]),
    s.Matrix([[x, 0, 0], [x-1/x, 1, 0], [x-1/x, 0, 1/x]]),
]
h = s.symbols('h0:9')
H = s.Matrix(3, 3, h)
equations = []
for M in matrices:
    assert s.simplify(M.det()) == 1
    equations.extend(M.subs(x, 1/x).T * H * M - H)
coefficients, rhs = s.linear_eq_to_matrix(equations, h)
assert rhs == s.zeros(27, 1)
rows = [1, 2, 3, 4, 5, 6, 11, 14, 18]
minor = coefficients[rows, :]
polynomial_minor = minor.applyfunc(lambda entry: s.cancel(x**2 * entry).expand())
domain_matrix = DomainMatrix.from_Matrix(polynomial_minor).convert_to(s.ZZ.poly_ring(x))
determinant = domain_matrix.det().as_expr()
expected = -x**11 * (x-1)**7 * (x+1)**3 * (x**2+x+1)
assert s.expand(determinant - expected) == 0
print('SymPy', s.__version__)
print('Rows (zero based):', rows)
print('Determinant after multiplying each selected equation by x^2:')
print(s.factor(determinant))
print('PASS: exact identity in ZZ[x]')
