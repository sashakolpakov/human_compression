# Natural-matrix certificate for the PSU₄(5) rank-four example

10 October 2026. Supplement to the frozen
[permutation certificate](phase10_unitary_rank4.md).
This alternative certificate identifies the group by explicit containment
and an order comparison. It requires no ATLAS generator file,
finite-simple-group recognition or invocation of the classification of
finite simple groups.

The original file [phase10_unitary_matrix_witness.g](phase10_unitary_matrix_witness.g)
contains four explicit 4-by-4 matrices over GF(25). In GAP's notation
Z(25) is a primitive field generator t satisfying t²-t+2=0 over GF(5);
Z(5)=2. These are actual determinant-one matrices for the Hermitian form
\[
 H=\begin{pmatrix}
 0&0&0&1\\0&0&1&0\\0&1&0&0\\1&0&0&0
 \end{pmatrix}.
\]
The Frobenius involution is entrywise fifth power. The checker verifies
both determinant one and $M H\bar M^{\mathsf T}=H$ for every matrix.
Their squares are respectively $I,I,-I,-I$; their projective images
are involutions.

Let K be their generated matrix group. The checker acts with K on the
orbit of the totally isotropic plane spanned by the first two coordinate
vectors. It obtains 756 planes, and forms the induced permutation group
P. Every scalar acts trivially on these planes. Consequently this action
factors through the projective image of K, a subgroup of PSU₄(5).

Exact GAP permutation-group computation gives
\[
 |P|=14\,742\,000\,000
     =\frac{5^6(5^2-1)(5^3+1)(5^4-1)}{\gcd(4,6)}
     =|\operatorname{PSU}_4(5)|.
\]
The inequalities
\[
 |P|\le|\text{projective image of }K|\le|\operatorname{PSU}_4(5)|
\]
therefore are equalities. Hence K maps onto the whole PSU₄(5), the
plane action is faithful on its projective image, and P is isomorphic
to PSU₄(5). This argument does not assume in advance that the four
matrices generate the full unitary group, or that this plane action
has only scalar kernel.

Finally the checker verifies type $\{4,26,10\}$, the string commutations,
all 16 generated subset groups, and all 256 ordered intersection
equalities inside P. This proves the same finite rank-four existence
statement directly from compact matrices.

Run from the directory containing both original files:

    gap -q phase10_unitary_matrix_check.g

The mathematical external input for the identification is the standard
order formula for the finite projective special unitary group. Exact
finite-field arithmetic, matrix operations, orbit calculation and
permutation-subgroup computations are delegated to GAP 4.15.1.
This is a computational certificate for q=5, not a universal
construction and not a complete Lean formalization. Publication priority
is unverified.

For discovery only, an isomorphism from the original permutation group
to the natural SU₄(5) action on isotropic planes was constructed and
the four projective generators were lifted. The standalone checker
does not read that isomorphism, the old permutation witness, or an
external source. Thus this description of discovery supplies no
additional assumption to the verification.
