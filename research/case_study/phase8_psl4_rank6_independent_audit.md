# Independent review of the rank-six PSL(4,q) obstruction

10 October 2026. **PASS.** Independent internal written mathematical
review by the `rank_stability` agent. This is not external peer review,
a Lean formalization of the theorem, or an assertion of publication
priority. Exact reviewed versions are bound in
[phase8_psl4_rank6_independent_audit.json](phase8_psl4_rank6_independent_audit.json).

The reviewed claim is that natural PSL(4,q), for every odd prime power q,
has no rank-six string C-group representation. The proof treats rank six
directly through its additional commutation relations. It does not assume
that a rank-five parabolic generates the whole group.
The final proof is [phase8_psl4_rank6.md](phase8_psl4_rank6.md); its
Section 9 structural corollary is also covered by this review.

## Setup and tensor cases

The extra relations are correctly indexed: T₂ centralizes the right
endpoint pair projectively and T₃ centralizes the left pair projectively.
They therefore centralize the corresponding unipotent parts linearly,
since multiplication of a matrix by a scalar leaves its unipotent
Jordan part unchanged.

For an untwisted tensor pair, the four simultaneous signed intertwiner
spaces of the two-dimensional endpoint generators have dimensions at
most one. The displayed equations remain valid for triangular pairs.
When the negative-negative line is singular, invertibility rules out
that choice; it does not leave additional blocks. This proves that each
middle generator is a pure tensor, so J tensor J is a common form.

For separated support, all endpoint generators are projective
reflections. Their unequal eigenspace dimensions force actual linear
commutation with any projective centralizer. A coinciding minus line
or fixed hyperplane is preserved by both middles using the indicated
outer-member commutations. Otherwise the two distinct minus lines span
the relevant support and the two fixed hyperplanes intersect in the
other support. The middle commuting with that full pair preserves both
supports. This excludes the case even when an endpoint pair is not
semisimple.

## Repeated simple endpoint and irreducible joint modules

For a repeated simple two-dimensional endpoint module, the only sign
twists returning the same simple module are the two equal-sign twists.
The nonzero trace of the endpoint rotation excludes the other two.
Schur's lemma consequently gives the stated pure-tensor form of the
left endpoints and the nearer middle.

I checked all three epsilon cases. When the outer left exponent is one,
the relevant commuting projective triple has pairwise distant indices,
so its independence follows from the intersection property. The
anticommuting tensor lemma gives Z tensor J, and every other generator
is visibly a similarity of that same form. When both exponents vanish,
the opposite middle is a pure tensor. In the remaining mixed case, the
diagonal coefficient of L₁ is nonzero: otherwise the left adjacent
generators anticommute and hence commute projectively. Comparing that
coefficient in the monomial middle relation gives a ratio independent
of the second coordinate. This forces the coefficient array to factor
and proves pure-tensor form; off-diagonal coefficients cannot contribute
to the same basis position.

In irreducible joint normal form II, the two inequivalent left
constituents and their unique signed intertwiners give precisely
T₃=K^eta tensor C, with C diagonal or off-diagonal. If either right
generator has a K factor, the anticommuting tensor lemma applies to
T₂ and a genuinely independent projective triple. Diagonalizing its
second factor only changes the alternating form J by a scalar, so the
other endpoint and the extra Z factor in T₁ still preserve the selected
form. If neither has a K factor, both middles are pure tensors. Thus
the form chosen for one middle is also a form for the other; two
unrelated rank-five form arguments have not been conflated.

## Reducible completely reducible modules

The old complete cross-sign table leaves one negative, two in one row
or column, or four negatives. I rechecked its scalar/nonscalar patterns
and the displayed normal forms. The additive-commutator argument gives
a particularly direct proof, independent of any additional assertion
of complete reducibility after restricting to a triple.

In each viable form, the left adjacent pair commutes on exactly one
two-dimensional summand and has invertible additive commutator on the
other. The right pair has the complementary pattern. Every triple of
four endpoints contains at least one whole adjacent pair. An off-block
intertwiner C with prescribed signs must carry the corresponding
additive commutators with the product sign. One side is zero and the
other invertible, so C=0 in either block direction.

The nonzero determinants are 4, minus (t−t⁻¹) squared, and minus 4b²,
with t nonzero, t² different from one, and b nonzero in the appropriate
forms. These are exactly the nonproportionality conditions in the
classification. Scalar signs on individual blocks do not alter
vanishing or invertibility. The argument holds in every odd
characteristic, including three. Both middles therefore preserve the
same two summands, contradicting absolute irreducibility.

The one-semisimple-endpoint reduction is exhaustive in dimension four:
distinct simple constituents, a two-dimensional simple plus a repeated
character, or a repeated two-dimensional simple. The first gives a
completely reducible joint module; the others are exactly the cases
already treated.

## Modular cases and endpoint-only dependence

The regular-unipotent centralizer is commutative, so it cannot contain
the noncommuting opposite endpoint pair. For Jordan type (3,1), the
characteristic-three-safe logarithm has a two-dimensional kernel. The
opposite endpoints are reflections. Coinciding minus lines or fixed
hyperplanes give invariant subspaces as above; otherwise their distinct
minus lines span that kernel. One middle preserves it by centralizing
both reflections, and the other by centralizing the unipotent part.

If the two square-zero parts have nonzero product, the earlier regular
four-dimensional algebra argument gives untwisted tensor endpoints
before using a middle generator. Applying the rank-six tensor lemma
is therefore justified.

For zero product, I checked that every imported normal-form step is
endpoint-only. In rank pair (1,1), distinct image lines and independent
functionals give separated support; a common image or common kernel is
preserved by both middles through their respective linear
centralizations. In rank pair (1,2), T₂ preserves the rank-two image.
The middle T₃ is monomial on the four distinct outer joint weights and
preserves the rank-one image line. A nonzero weight translation cannot
fix that line, so T₃ is diagonal and preserves the same rank-two image.
In rank pair (2,2), both middles preserve the common image/kernel
directly. The reversed rank pair is covered by reversing the string.
These exhaust the remaining nilpotent possibilities.

## Structural corollary beyond PSL(4,q)

The final Section 9 is valid for a finite irreducible subgroup of
PGL₄(k) with a string C-group generating set whose adjacent pairs do
not commute. I reread the rank-seven Pauli-support proof and checked
the rank-five and rank-six deductions under these broader hypotheses.
They use PSL(4,q) only when rejecting the final common form. Every
other exclusion relies on irreducibility, the string and intersection
properties, adjacent noncommutation, or the four-dimensional module
structure. The general rank bound and rank-eight exclusion reduce
the question to ranks five, six, and seven.

Consequently a rank-at-least-five action satisfying these hypotheses
preserves a nonzero bilinear similarity form. Its radical is invariant,
so irreducibility makes it nondegenerate. Symmetric and alternating
parts inherit the same multipliers. At least one part is nonzero in
odd characteristic and is then nondegenerate by the same argument.
This proves the stated form alternative without classifying all
form-preserving groups or their ranks.

## Checks and conclusion

The exact checker was read and rerun independently to a separate output.
All **33 identities** and **12 three-endpoint witnesses** passed. The
identities supplement the written normal-form and coverage arguments;
the script is not a search through finite groups and does not certify
those arguments by itself. Its nonvanishing factors make the
odd-characteristic scope explicit.

I found no gap in the rank-six exclusion under the stated setup and
previously reviewed endpoint lemmas. Together with the separately
reviewed rank-five exclusion, the earlier uniform upper bound of six,
and the published rank-four existence result, this supplies the stated
maximum-rank-four conclusion. Those dependencies remain separate
written or published inputs; this audit does not rebrand them as newly
machine-formalized results. No novelty conclusion follows from the
bounded literature search.
