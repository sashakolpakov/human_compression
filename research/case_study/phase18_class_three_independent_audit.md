# Independent review of the class-three classification

10 October 2026. This review concerns
[phase18_class_three.md](phase18_class_three.md), with its exact
reviewed bytes identified in the accompanying JSON. It does not edit
or reopen any frozen phase-seventeen artifact.

**Verdict: PASS under the explicitly retained forest canonical-quotient
and elementary-cover construction theorems.** The result classifies
all the stated ordered nondegenerate path markings of finite two-groups
of class at most three, at every rank d≥3 and every excess. It is not
a classification of the higher-class groups at the same excess.

## Why the marked vectors really form a basis

The canonical quotient identifies G/γ3(G) with C_d. Since the group
has class at most three, its kernel K is central. Every edge-square
α and every triple commutator β has order at most two: endpoint
inversion and centrality give c_i⁴=1, while a central commutator
with an involution has square one. The class-three commutator table
generates all of γ3, so K is exactly the elementary-abelian group
spanned by these words. This does not posit a basis in advance.

The restriction K∩G_S=γ3(G_S) is justified by the retained forest
quotient theorem: the local canonical quotient is the induced forest
subgroup of the global C_d, embedded with the same vertex and edge
coordinates. Thus its map is injective, giving the claimed equality
of kernels. In particular each edge contributes E_i=〈α_i〉, and each
triple contributes N_i=〈α_i,α_(i+1),β_i〉.

For the crucial prefix step, Q_(i−1)=N_1+⋯+N_(i−1) is an actual
subgroup because K is central. Its marked support lies in
{1,…,i+1}, while N_i lies in {i,i+1,i+2}. Actual IP in the original
group therefore puts their intersection in the edge {i,i+1}, hence
in E_i. The reverse inclusion follows from E_i≤N_(i−1),N_i. No
intersection property is being assumed for an unproved quotient.

This exact intersection, repeated from left to right, gives the
dimension formula k=Σa_i+Σb_i. Every omitted β lies in the span
of its two adjacent α values, so the nonzero α values and the
locally new β values span K. Their number equals its dimension,
which proves their independence. In particular the classification
does not mistake local novelty for global independence.

## Arbitrary dependent coefficients are realizable

The full seed fiber product has an independent kernel coordinate
for every edge and triple. Its diagonal markers generate the
whole fiber: each parameter word isolates one kernel coordinate,
and their images generate the common canonical quotient. Its
parabolic kernel is exactly the coordinate span of supports wholly
contained in the selected marker set.

Taking a central quotient by the specified linear map realizes
every choice of active edges, intrinsic triples and local dependent
β coefficients. A new β is itself the designated basis vector;
adding an externally chosen basis coefficient would only change
coordinates, not define a further marked invariant. An omitted β,
on the other hand, has a unique coefficient vector in the already
marked neighboring α basis, and all those vectors are permitted.

The image of a parabolic kernel is computed without interchanging
quotients and intersections. Its elements lift to the same parabolic
in the fiber, and mapping to the canonical quotient shows that a
lift representing a kernel element was already in the original
fiber kernel. The image is therefore exactly the stated span.
Every dependent β with its triple contained in S uses only edge
basis coordinates also supported inside S. It contributes no
extra coordinate. Thus the resulting parabolic kernels are precisely
the coordinate subspaces V_S of equation (9).

These satisfy V_S∩V_T=V_(S∩T). For a common parabolic element g,
the canonical quotient supplies a lift h in G_(S∩T) with the same
image. Both g and h lie in each parabolic, so gh⁻¹ lies in the two
kernel subspaces and hence in the expected smaller parabolic. This
proves actual IP for every permitted coefficient choice. The argument
does not require a kernel of order two; it genuinely extends the
phase-seventeen sufficiency step.

## Completeness and counting

The presentation bound is sufficient for uniqueness. Its central
involutory kernel has at most 2^k elements, and collection in the
quotient bounds the remaining order by |C_d|. The constructed group
attains that full order. Every actual group with the same marked
data is a quotient of this complete presentation of that order, so
is isomorphic as an ordered marking. Conversely a marked isomorphism
preserves the α/β words and recovers all the data, including every
dependent coefficient. There is no multiplicity from changing a
chosen external kernel basis.

For each active edge the dimension cost is one. At a triple the
intrinsic option has weight x, while the dependent options number
2^(a_i+a_(i+1)). This proves the product formula. The transfer entry
from a previous bit a to a next bit b is
x^b(x+2^(a+b)), with initial factor x^a, giving exactly the stated
matrix M(x). The formulas for coefficients zero, one and two follow.
I separately checked the three excess-two cases, including adjacent
active edges: their shared triple has four dependent choices, as
the product of the two edge weights requires. At d=3 the polynomial
is 1+5x+6x²+x³, so the end-case formulas also agree.

The final closed-form additions also check. At x=1 the transfer
matrix is the coordinate-swapped fourth power of the Fibonacci
matrix, and the two boundary vectors contribute two further powers,
giving the stated Fibonacci index 4d−5. The trace and determinant
of M are 1+5x+x² and x². Cayley–Hamilton yields the displayed
recurrence; using F2=1+x and F3 above gives numerator 1+x−xt in
the rational rank/excess generating function. The proof explicitly
labels d=2 as an algebraic boundary value.

## Independent finite diagnostic

The separately written standard-library checker
[phase18_class_three_independent_linear_check.py](phase18_class_three_independent_linear_check.py)
and [its report](phase18_class_three_independent_linear_check.json) enumerate
every subspace N of the full universal edge/triple kernel for
ranks three, four and five. They do not use the proposed candidate
classification to select subspaces. Instead, for every marker set S
they form the preimage N+W_S and directly test

    (N+W_S) ∩ (N+W_T) = N+W_(S∩T).

The enumeration uses unique binary reduced-row-echelon bases. It
visits 16, 374 and 29,212 subspaces, respectively, and performs
4,320,898 intersection tests, stopping a failed candidate at its
first failure. All valid candidates complete every unordered pair
test. Counting by quotient dimension gives:

* d=3: [1,5,6,1];
* d=4: [1,10,31,35,11,1];
* d=5: [1,15,81,195,211,90,16,1].

These agree exactly with the proposed generating polynomial. The
checker is an independent finite vector-space diagnostic, not an
enumeration of groups or a proof for arbitrary rank. The universal
theorem is the written argument reviewed above. No fresh Lean
compilation, source-priority determination, or unrestricted
excess-two classification is claimed by this review.
