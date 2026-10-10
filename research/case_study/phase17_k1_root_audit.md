# Root review of the first-excess classification

10 October 2026. Independent internal review of
[the uniform proof](phase17_k1_classification.md), with the reviewed hashes
and fresh finite execution recorded in the companion JSON. Publication
priority and external peer review are separate, unresolved questions.

**Verdict: PASS under the stated canonical-quotient and central-join inputs.**
For every d>=3 there are exactly 5d−10 ordered marked nondegenerate string
C-group two-groups of order 2^(2d). Nondegenerate means that every adjacent
product has order at least four. The proof also classifies the larger
space of involutory string-marked central covers of C_d with kernel gamma3
of order two. The string and involution hypotheses are essential to that
larger statement.

## Completeness and realizability

The earlier canonical-quotient theorem gives a central gamma3 of order
two. Endpoint inversion, the distant commutations and the class-three
Hall–Witt identity give the displayed alpha/beta commutator table.
The presentation consequently has at most 2^(2d) elements: after reducing
modulo the central involution, the markers and adjacent commutators have
the canonical class-two collected normal form. No presentation lower
bound is being assumed at this step.

The D16 and UT4(F2) seed markings have the claimed orders, parameters
and intersection property. Applying the retained central join creates
one-coordinate extensions of the same marked quotient. In their fiber
product, an active parameter word produces exactly one kernel basis
vector. This proves generation by the diagonal marker lifts, rather than
assuming that arbitrary lifts generate a fiber product. Quotienting by
the even-sum kernel realizes every nonzero parameter vector at the full
order. This supplies the missing lower bound and proves the completeness
of the presentation. Ordered marked isomorphisms preserve the unique
kernel involution and the alpha/beta words, so the parameters are complete
invariants in the specified category.

## Parabolics and the decisive support criterion

Before taking the central quotient, a parabolic's kernel coordinates are
exactly those whose active supports it contains. Projection into each
seed extension proves the upper inclusion; the isolated parameter words
prove the lower inclusion. After quotienting, a parabolic contains the
remaining kernel involution exactly when it contains some active support.
An element of the quotient parabolic lying over the identity in C_d has
a representative in that original parabolic's intersection with the
fiber kernel. Thus no additional kernel membership is introduced by an
unjustified interchange of intersection and quotient.

If the active supports have a least member J, either a pair of parabolics
contains the kernel on both sides and their index-set intersection also
contains J, or at least one parabolic has injective quotient map. In each
case exact quotient intersections and the already included intersection
parabolic force equality. If there is no least support, two distinct
minimal supports give an explicit kernel involution in their parabolic
intersection which is absent from the intersection parabolic. This proves
both directions of actual IP, including the failure cases.

The remaining count has d−2 isolated triple supports, two choices at each
end edge and four choices at every interior edge. Their sum is 5d−10.
Reversal fixes one class at odd rank and two at even rank, giving the
stated duality counts. These arguments use the full presentation and
support classification, not an extrapolation of finite data.

## Fresh computation and source overlap

A fresh root execution of the author's GAP/NQ presentation checker agrees
with the saved report: 165 nonzero vectors in ranks three through five,
4,616 parabolic orders and 138,432 exact subgroup intersections. It finds
5, 10 and 15 IP markings, respectively, and tests every rejected vector
as well as every accepted vector. NQ and GAP computations are bounded
diagnostics; the written normal-form and construction proof supplies the
all-rank theorem.

I separately read the rank-five/order-1024 entries in Table 6, p.17 of
[Gomi–Loyola–de Las Peñas (2018)](https://cdm.ucalgary.ca/article/download/62475/46803),
and the corresponding section of
[Conder's primary census](https://www.math.auckland.ac.nz/~conder/RegularPolytopesWithFewFlags-ByOrder.txt).
Both list eight classes up to duality: two all-four types, two end-eight
types and four inner-eight types. The census marks one as self-dual.
These match the new formula at d=5. This is a count/type comparison;
individual source presentations have not been matched here.

The 2013 smallest-polytopes article was located through its
[publisher record](https://www.sciencedirect.com/science/article/pii/S000187081200463X)
and the author's lecture material. Its full proof was not retrieved in
this review. The author's preprint index explicitly stops at 2010.
Consequently this review does not claim an exhaustive prior-art audit or
that the all-rank formula was previously open. No infinity marker or
matched proof-length ratio is assigned.
