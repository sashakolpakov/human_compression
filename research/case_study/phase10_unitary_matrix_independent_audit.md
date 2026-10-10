# Independent review of the natural PSU4(5) certificate

10 October 2026. **PASS.** I read the compact matrix witness, the standalone
checker and its mathematical explanation, then freshly ran the checker
using GAP 4.15.1. The [run record](phase10_unitary_matrix_independent_run.json)
binds the exact three source files and reports successful field/form,
projective-order, string and all256 intersection checks.

The four matrices have determinant one and preserve the nondegenerate
antidiagonal Hermitian form under the stated row-vector convention:
M H bar(M)^T=H. The involution of GF(25) is the fifth power. The initial
plane is checked to be totally isotropic, and the action uses canonical
subspace bases, so scalar multiplication fixes each subspace. Thus the
computed permutation image factors through the matrix group's projective
image inside PSU4(5).

The order comparison is sufficient without a hidden faithfulness assumption.
The computed permutation group is a quotient of that projective image;
its order equals the standard order of PSU4(5). Containment bounds the
projective image by the same number, forcing both equalities. Consequently
the generated projective group is the full PSU4(5), and the permutation
action on the selected orbit is faithful. No classification of finite
simple groups, GAP simple-group identification, or ATLAS generator is
needed for this identification. The classical unitary-group order formula
and GAP's exact arithmetic, orbit and permutation-group algorithms remain
explicit inputs.

The checker verifies that the projective generators are involutions, have
adjacent product orders4,26,10 and commute at distant positions. All sixteen
subset groups and all256 ordered intersections are checked directly. This
therefore supplies a second certificate for the finite rank-four existence
statement, with a smaller identification dependency than the frozen
permutation-only record. It is not a uniform construction for odd q, not
a complete Lean formalization, and not a priority claim.

The interpretation of the field generator is also checked by the program:
its minimal polynomial over GF(5) is x^2-x+2, with GAP's Z(5)=2. Neither
that interpretation nor the possible kernel of the plane action is assumed
on the basis of a group-name label.
