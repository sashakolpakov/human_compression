# Root review of the two diagonal unitary constructions

10 October 2026. Independent internal review of
[the q=1 modulo 4 branch](phase17_unitary_diagonal.md) and
[the q=3 modulo 4 branch](phase17_unitary_twisted.md). The companion JSON
identifies reviewed bytes and fresh computations. This is not external
peer review or a publication-priority determination.

**Verdict: PASS under the explicitly retained inputs.** The unique
diagonal index-two extension of PSU4(q) inside PGU4(q), for every odd
prime power q, has the displayed rank-four marking of type
{4,2(q+1),2p}. Its maximum rank is four using the retained dimension-four
upper bound. For q=1 modulo 4 this extension is all of PGU4(q); for
q=3 modulo 4 it is a proper subgroup of PGU4(q). The cyclic index-four
socle quotient prevents involution generation of the larger group in
the latter case. No rank-three extension theorem is inferred.

## Parameters and generation

In the first branch, nonsquareness of k² forces a hypothetical proper
subfield degree to be odd. The two field-containment calculations then
put the parameter of order q+1 in a multiplicative group too small to
contain it. In the second branch, Frobenius on the two roots lambda²
and lambda^(-2) forces their order to divide r−1 or r+1 for a proposed
proper subfield Fr. Both arguments prove the full trace-square field
uniformly, without a hidden exceptional-field list.

The algebraic template gives the claimed projective involutions and
adjacent orders in both branches. In the first branch scalar powers of
the middle eigenvalues must have exponent divisible by 2(q+1); in the
second a ratio of eigenvalues has exactly that order. The last product
has a nontrivial unipotent factor of order p and projective semisimple
factor of order two. The determinant computations put the generators
in precisely the required diagonal subgroup once the socle is generated.

The generation proof retains the rank-one Dickson subgroup list and
the earlier coordinate SU2 elimination argument. I read that earlier
adapter. The moved unipotent fixed point, outer witness and full
trace-square field exclude the respective proper subgroup types. The
exceptional S4 case reduces to the prime-field case, where the element
of order p excludes it for the stated uniform ranges. A nontrivial
normal second projection of the first-projection kernel contains PSU2.
Perfection supplies actual SU2, stripping scalar ambiguities. In the
second branch, taking the derived subgroup is necessary: its first
scalar block becomes the identity, while D'Z=SU2 and perfection give
D'=SU2. No false restriction to first-block scalars ±I is used there.

For q=3, rank-one perfection is not invoked. The exact natural-action
order is 6,531,840. The projective matrix group lies in the stated
ambient subgroup and has an action of that ambient order, so the two
order inequalities give equality. This does not require assuming that
the action is faithful before performing the order comparison.

## Arbitrary projective lifts and full intersection property

The row-Hermitian and column-Hermitian conventions agree because H²=I.
The semilinear map sigma=BH followed by field conjugation has the
claimed nonzero scalar square. The isotropic vectors v and sigma(v)
have nonzero cross-pair and span a nondegenerate plane. Their nonzero
cross-pair is also what constrains an initially arbitrary B-similitude
multiplier; a sign restriction cannot simply be assumed from the facet
generators.

In the first branch the vertex eigenvalue alpha lies in the prime-base
fourth roots and forces mu=alpha². In the second, the essential extra
identity is that the Hermitian multiplier epsilon equals alpha² for
every word in the unnormalized vertex lifts. The intertwining relation
then gives mu=epsilon=alpha². In both cases the alpha=1 kernel fixes
the indicated plane pointwise and commutes with sigma on its complement.
Scaling sigma to an antiunitary involution and applying the explicit
quadratic descent formula identifies its fixed space as a nondegenerate
binary symmetric space over Fq. This gives at most 2(q+1) kernel
elements. Four eigenvalue fibers and division by the actual two scalar
elements give the projective upper bound 4(q+1), attained by the middle
dihedral subgroup.

The left rank-three meet follows from the four-element projective line
orbit. The right meet could exceed the required involution only by
containing the central rotation involution of the order-4p dihedral
group. Its displayed representative has a nonzero B-form defect, even
after allowing arbitrary similitude multipliers. Thus both rank-three
markings have IP. Their exact maximal-parabolic meet supplies every
hypothesis of the retained recursive string C-group criterion.

## Fresh checks and limits

Fresh root executions pass the natural-action GAP checkers at q=5,9,13,17
and q=3,7,11: 112 marked subgroups and 1,792 exact subset intersections,
with the expected generated orders and adjacent orders. The q=3 base
is a proof input for generation in that exceptional case. The other
finite checks are diagnostics for the uniform written arguments.
The independent reviewer's two symbolic checkers verify the algebraic
identities separately from the author's checker.

The complete group-generation argument, field reasoning, binary
orthogonal order bound and recursive intersection criterion remain
written mathematics with their stated inputs. No new end-to-end Lean
formalization is claimed for these unitary theorems. Broader field and
graph extensions, rank-three existence for the diagonal extensions,
and current publication priority remain unresolved here.
