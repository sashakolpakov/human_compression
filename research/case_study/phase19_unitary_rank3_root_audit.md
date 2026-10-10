# Root review: unitary rank-three generation

10 October 2026. **PASS for the stated all-parameter theorem**, under its
explicit retained rank-one and elementary unitary generation inputs.
This is an internal review, not external peer review or a priority claim.
The accompanying JSON binds the final proof, including its explicit
same-marking intersection argument, and fresh bounded executions.

## Generation review

1. The trace-zero full-field parameter exists for every odd q>=5. The
   identities for t and its conjugate prove F_p(t^2)=F_(q^2): the field
   not lying in F_q has odd index, then contains t, s and z. This avoids
   assuming that a prime-field unipotent parameter generates the field.
2. Two opposite root elements on the isotropic plane have different fixed
   lines and full projective trace field. The stated Dickson exclusions
   cover Borels, torus normalizers, subfields and exceptional groups,
   including p=3 and p=5. Perfection lifts the projective conclusion to
   SL2(F_(q^2)). The proof distinguishes this subgroup from the larger
   plane image, which also has determinant-minus-one elements.
3. If the parabolic kernel were trivial, a torus-stable hyperbolic
   complement would give four additive off-block functions. Their torus
   weights are absent from the exponents 2p^j modulo q^2-1 for q>=5.
   The four functional equations force their successive vanishing.
   The resulting block sizes contradict the explicit Jordan type (3,1)
   of U. This supplies the previously missing nonzero-kernel argument.
4. The radical is irreducible as an additive F_p-module, not merely as
   an F_q-module. Root conjugation, its negative parameter and norm
   surjectivity give every Hermitian coordinate using subgroup addition.
   A nonzero invariant kernel therefore contains the entire radical.
5. The reflection sends the isotropic plane to an adjacent plane. The
   radical removes the two extra coordinates of its second basis vector,
   giving an opposite long root. Rank-one Weyl elements and the Levi then
   give both opposite radicals. The retained elementary unitary
   generation theorem now applies. No SU4 maximal-subgroup list is used.

## Projective and intersection review

Determinants 1,-1,1 and the exponent (q+1)/2 in the cyclic diagonal
quotient give index two for q=1 mod4 or q=3 mod8 and index one for
q=7 mod8. The matrix construction therefore does not solve the latter
diagonal-extension problem. It excludes q=3 throughout the generation
argument. Adjacent projective orders are greater than two, with BC
of order 2p, including the s=1 repeated-root case for AB.

Section 6 now gives a full same-marking IP argument. A common nonidentity
rotation of the two dihedral parabolics generates a cyclic normal
subgroup. In the mixed rotation/reflection case, their intersection
instead exhibits the whole group as a product of two commuting
dihedral factors, again forcing a cyclic normal subgroup. Redundant
endpoints force a dihedral whole group. Almost simplicity excludes all
these alternatives. Thus the actual triple has IP. This avoids treating
an existence statement about some triple as a theorem about this triple;
the precise 2025 source criterion and its relation to the older statement
are identified in the proof.

## Fresh execution and boundary

The root reran all 24 identities in the independently written SymPy
checker. It also reran the frozen GAP construction for q=5,7,9,11,13
and the second q=7 parameter with s=1. All six projective order checks,
48 subgroup closures and 384 actual meets pass. These computations
corroborate the all-parameter proof; they are not its justification.

No new Lean formalization of unitary generation is claimed. Simple-socle
rank-three existence was already known. Priority of the diagonal-extension
subfamilies remains unverified; q=3, q=7 mod8 extensions, linear rank-three
extensions and field/graph extensions remain outside this theorem.
No named-open resolution or infinity marker is assigned by this review.
