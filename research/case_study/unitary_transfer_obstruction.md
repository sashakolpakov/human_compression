# An obstruction to the direct unitary substitution

The relative-position framework should detect failed constructions as well as
produce examples. Here is a precise limitation of transferring the established
PSL(3,q) construction to PSU(3,q).

Take the three matrices of Leemans–Vandenschrick, [Theorem 1.1](https://dipot.ulb.ac.be/dspace/bitstream/2013/333283/3/psl3-final.pdf).
Instead of choosing x primitive in F_q, choose x of order q+1 in F_(q²),
so that x^q=x^(-1). For every prime power q>2, these three matrices cannot
simultaneously preserve a nonzero Hermitian form. Their projective images
cannot simultaneously preserve a nondegenerate Hermitian form up to scalar
either. Thus this parameter substitution does not yield a PSU(3,q)
construction. This does not rule out other constructions for PSU(3,q).

For a proof, let H be an arbitrary 3-by-3 matrix, with its nine entries as
independent unknowns; imposing Hermitian symmetry is unnecessary. The equations

    bar(M_i)^T H M_i = H,    i=1,2,3,

are 27 homogeneous linear equations, where bar(x)=x^(-1). Index equations
in row-major order, starting at zero, and concatenate the three matrices'
equations. The minor on rows

    1, 2, 3, 4, 5, 6, 11, 14, 18

has determinant

    -(x-1)^7 (x+1)^3 (x²+x+1) / x^7.

Equivalently, multiplying each chosen equation by x² gives a polynomial
matrix with determinant

    -x^11 (x-1)^7 (x+1)^3 (x²+x+1).

The [exact verifier](unitary_transfer_obstruction.py) checks this identity
over Z[x], so it remains valid after reduction in every characteristic.
An element of order q+1>3 is nonzero and is not a root of any displayed
factor. The coefficient matrix has rank nine, forcing H=0.

For the projective assertion, suppose a nondegenerate Hermitian H satisfies
bar(M_i)^T H M_i=lambda_i H. Hermitian symmetry implies lambda_i∈F_q*,
and determinant one gives lambda_i³=1. The first and third generators have
orders dividing q+1, and the second has order dividing 2(q+1). Hence the
order of each lambda_i divides both q-1 and 3 and 2(q+1). Those three
integers have gcd one, so each lambda_i=1. The preceding obstruction applies.

Status: an internally checked algebraic obstruction, with an exact symbolic
certificate. Publication priority has not been investigated. It is a test of
one specific construction, not a solution to the open unitary-group problem.
