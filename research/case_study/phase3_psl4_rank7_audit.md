# Independent internal audit of the rank-seven Pauli obstruction

9 October 2026. Audited by the separate `recent_conjectures` agent. This
is an internal mathematical review, not external peer review. No stable
research file was changed during the review.

**Verdict: the written proof passes.** The reviewed version of
[phase3_psl4_rank7.md](phase3_psl4_rank7.md) has SHA-256
`1c9a6262ae3600dbbbbacde0428a34cad789c532c1e9c01186823b7d45aaba5d`.
Together with the previously certified rank-at-most-seven theorem, it
proves rank at most six for string C-group representations of PSL(4,q)
in odd characteristic. Ranks five and six remain unresolved here.
Publication priority has not been established.

## Points checked adversarially

1. **Projective scalars.** Normalizing involution lifts to square to I
   over the algebraic closure makes every projective commutation scalar
   equal to +1 or -1. Therefore Pauli conjugation eigenspaces and the
   subsequent simultaneous sign-intertwiner calculation apply exactly.

2. **Support dimension without a semisimplicity assumption.** For
   L=span(v0,v2), R=span(v4,v6), the pairing L×R-perp is nondegenerate
   because its left kernel is L intersect R=0. A proper difference span
   of supp(T1) would therefore yield a nonzero z in L whose projective
   matrix centralizes rho1. The three possibilities z=v0,v2,v0+v2 are
   excluded respectively by adjacent noncommutation and the local
   intersection-property lemma. This proves the full difference span;
   the same argument applies on the right. Reducibility of either
   three-generator parabolic is not assumed away.

3. **No cancellation in multiplying the supports.** The two direction
   spaces R-perp and L-perp meet trivially. Consequently any label a+b
   in the product expansion has only one supported decomposition and
   its coefficient cannot vanish by cancellation. Comparing T1T5 with
   its signed reverse forces the commutator pairing to be constant on
   the complete Cartesian product of supports.

4. **Both affine shifts vanish.** Double differences force the two
   direction planes to be orthogonal. Single differences then put each
   support in the orthogonal complement of the other direction plane.
   Since these planes have dimension two and are complementary, the
   supports lie in the planes themselves, and those planes are exactly
   L and R. Their restricted alternating forms are nondegenerate.

5. **The middle generator is a pure tensor even in the reducible
   boundary cases.** With L0=diag(1,-1) and
   L1=[[a,b],[c,-a]], projective noncommutation gives a nonzero and
   (b,c) not both zero. A diagonal simultaneous sign-intertwiner is
   scalar in the ++ case and zero in the +- case. An off-diagonal
   intertwiner [[0,x],[y,0]] is zero in the -+ case, while the -- case
   has the one equation cx+by=0. This last solution space is exactly
   the line spanned by [[0,b],[-c,0]], including b=0 or c=0. Thus all
   tensor coefficients of T3 belong to a common one-dimensional
   space. Invertibility of T3 forces its two tensor factors to be
   invertible; no hidden assumption that bc is nonzero is required.

6. **The preserved form is valid for the entire group.** The identity
   M-transpose J M=det(M)J gives preservation up to scalar of the
   symmetric nondegenerate form J tensor J by every invertible pure
   tensor. The argument yields one common tensor decomposition for all
   seven generators, not a different form for each generator.

7. **The PSL4 obstruction has no finite-field center gap.** Passing to
   the algebraic closure is harmless for a projective similarity form.
   Pulling back to SL4(q) gives a similarity multiplier homomorphism,
   which is trivial because SL4(q) is perfect. For an invariant matrix
   H, applying I+Eij and I-Eij and subtracting the equations gives
   Eji H+H Eij=0. Its (k,j) entry for k not equal to j is Hki. Choosing
   j different from i and k forces every Hki to vanish. Thus even a
   nonzero degenerate invariant bilinear form is impossible. Odd
   characteristic is essential to this subtraction argument.

## Checks and limits

The accompanying support-check script was inspected: its 28
nondegenerate alternating forms and 11,200 pairs of full affine
supports cover the entire four-dimensional F2 support calculation.
Its certificate reports only 25 compatible support pairs, all for the
single required block-diagonal commutator form. This finite check
supports the written argument; it does not replace it.

Independently, direct enumeration of all two-by-two matrices over F3,
F5 and F7 checked the complete four-sign intertwiner table for every
normalized noncommuting pair in the stated normal form. The numbers
of pairs were respectively 8, 24 and 48, giving 32, 96 and 192 sign
spaces. All passed, including the b=0 or c=0 cases. The proof of the
table above is characteristic-independent for odd characteristic.

The local intersection-property obstruction has a Lean certificate in
`formal/StringIntersection.lean`. The Pauli support argument and the
full tensor-reduction theorem have written proofs and internal review;
they are not claimed to be fully formalized in Lean.
