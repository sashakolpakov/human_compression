# Independent review of the first two-primary cover obstruction

10 October 2026. Reviewer: `/root/review_unified_seven`.

**PASS, conditional on the declared source construction and standard geometric
interfaces.** I have read the complete frozen phase58 theorem, source ledger,
intake, both complete GAP programs and their runner. The uniform written
argument proves that the facet and cofacet construction routes reduce to the
same minimal double cover for the specified two-primary family. A separate
complete finite computation classifies the degree-two/four covers in the
single stated sample. Neither conclusion proves global uniqueness of minimal
covers or disproves the multiple-minimal-cover conjecture.

The reviewed theorem is `phase58_2primary_cover_theorem.md`, 20,997 bytes,
SHA-256 `4a6f993818ea2aec499657161b60b20852009026f3ba55afb0dd6ee35ea8ef79`.
The author manifest is bound by SHA-256
`a05194d0f85dab4955fdd85069947d883531b780d0e910734efb23fdb2585078`.
No frozen author file was changed during review. This is a mathematical and
certificate audit, not only a manifest-binding check.

## Admitted statements and exact scope

Let `β≥5`, `q=2^β`, and `ε₁,ε₂∈{−1,1}` independently. Retain the
source's tight chiral polytope `P` with the literal Γ2 presentation.
All orders in the following table are **rotation-group orders**.

| Object or conclusion | Reviewed result |
| --- | --- |
| Source `P` | Order `64q`, marked type `(8,q,8)`, exact tight normal form and intersection property retained from the source |
| Smallest regular maniplex `R` | Order `128q`; end intersection has order `2q`, so it is nonpolytopal |
| Facet and cofacet mixes `Qf,Qv` | Each has order `512q` and cyclic-four kernel over `R`; each is polytopal and has one locally noninjective end |
| Reduced cover `S` | Both reductions are the same marked cover; order `256q`, degree two over `R`, injective end maps and global minimality over `P` |
| Shared raw mix `H=Qf⋄Qv` | Order `1024q`; kernel over `R` is `C4×C2`; `S` is its unique minimal regular polytopal quotient over `P` |
| Complete degree-two/four census | Only `β=5, ε₁=ε₂=+1`: one marked degree-two cover and 29 marked degree-four covers, every degree-four cover having a proper polytopal double quotient |

“Global minimality” for `S` means that `S` has no proper regular polytopal
quotient still covering `P`. “Unique” is restricted to the stated finite
interval or finite degree scope. It does not mean that every minimal cover
of `P` is `S`. All equivalences preserve the marking/ranks; arbitrary rank
permutations are not used to identify cases.

## Source interface and attribution

I checked the bound primary author-version extracts at **Table 2, row Γ2**
and the complete **Theorem 4.8** statement and proof, and the retained
Lemma 4.6/Corollary 4.5 interfaces. The source is Cunningham–Pellicer,
*Tight chiral polytopes*, arXiv:2009.04566v1, with the author PDF's September
2020 version and the associated 2021 journal identification. The inspected
mathematical basis is the author-version text, not an asserted identical
publisher PDF. I do not claim a new reading of all 43 pages or a new visual
PDF audit in phase73.

The row has parent type `[8,2^β,8]^+` and exactly

```text
b a² = a² b^(1+ε₁ 2^(β−2)),
c² b = b^(1+ε₂ 2^(β−2)) c²,
β≥5, ε₁,ε₂ independently ±1.
```

Theorem 4.8 includes all four choices and the boundary case `β=5`.
Its source proof distinguishes the `β=5` congruence for its auxiliary
`D=2^(β−3)`. The new manuscript instead uses `h=q/4`, whose square is
divisible by `q` already at `β=5`; it does not incorrectly apply the
source's stronger `D²=0` congruence at that boundary.

The input being retained is substantive: existence of `P`, its exact marked
presentation and orders, tightness/normal form and intersection property.
The source's atomic/local classifications, Table 1 constructions, Lemma 4.6
and Corollary 4.5 are background dependencies of that input. The new package
does not reprove the source classification or compress that whole paper.

The general mix-with-trivial-end-extension strategy belongs to Cunningham's
earlier smallest-cover example. Standard marked rotation/string-C recognition,
the correspondence with regular polytopes, and the smallest-regular-maniplex
universal property are retained. What is newly proved **in this repository**
is the uniform calculation of these covers, their coincidence after reduction,
the shared interval, and the bounded extension census. Historical novelty
has not been cleared. These statements must not receive an open-conjecture-
solved marker merely because they are new to this repository.

## Uniform algebra and geometry review

### Coordinate and mirror calculations

I checked the sign-sensitive calculations with right conjugation
`z^g=g⁻¹zg`. For `x=b^h`, `u=a²`, `y=c²`, all three elements have
order four. Reordering the first extra relation with `d=ε₁h` gives
`ub=b^(1−d)u`; the square relation then gives the displayed inversion
of `x` by `a`. Reversing and inverting the marking exchanges the parameter
presentations, which proves the analogous `c` formula. This step requires
duality **between** the two sign presentations, not an unproved self-duality
of `P` when its signs differ.

The remaining formulas give `y^a=y⁻¹x^ε₂` and
`y^(a²)=yx^(−2ε₂)=yx²`; hence `x²` is central. The universal mirror
sends each literal extra relator to that central involution. In the second
relator computation, `(ub)^h=x` is justified by `ub=ab⁻¹a⁻¹` and
the inversion of `x`; since `h` is a multiple of four, it also gives the
displayed power simplification. Thus the mirror descends to
`P/⟨x²⟩`.

For `A=(a,a⁻¹)`, `B=(b,a²b)`, `C=(c,c)`, the generated mix lies
in the twisted fiber product over that quotient and contains
`κ=(1,x²)` as a literal relator value. Surjectivity onto the first `P`
therefore proves equality with the whole fiber product and order `128q`.
This is an order proof and normal-form argument, not an extrapolation from
the eight computations.

With `Z=(x^ε₂,x^(−ε₂))`, the identities
`Z B^(−ε₂h)=κ` and `Z²=B^(q/2)` explain the end intersection exactly:
`F∩V=⟨B,Z⟩` has order `2q`, rather than the medial order `q`.
The source intersection property excludes other elements. The source cyclic
intersections and exact marked orders ensure the lower-rank intersections.
The stated intrinsic mirror on the vertex end gives its regularity. Thus
the failure of `R` is precisely the top intersection property.

### Normal closure and the first reduction

For `Y=C²`, the source cyclic intersections make `⟨Y,Z⟩` a genuine
`C4×C4`. The entire action table is consistent with the preceding coordinate
formulas. It proves that this group is exactly the normal closure `W` of
`C²`, not just a normal subgroup containing it: conjugating `Y` obtains
`Z`. Projection and source IP give `W∩F=J=⟨Z⟩`, while
`W∩⟨B⟩=⟨B^(q/2)⟩`. The latter nontrivial intersection is the
essential difference from the odd-prime independent-coordinate situation.

In the trivial extension `T=F⋊⟨t⟩`, the marked last generator
`D=tAB` is an involution. The ends and their intersection give regular
polytopality directly. The normal `J` has actions `(-,+,+)` on the
rotation generators. The presentations and complementary involutions in
`R/W` and `T/J` identify the quotient **with its marking**; killing `C²`
is necessary in every common quotient, so this quotient is the largest one.
The subdirect-product argument then gives `|Qf|=512q` and cyclic-four kernel.

The vertex calculation correctly has common quotient `V/W` of order `q`,
not `2q`: the order of `B` drops to `q/2`. Its order-two kernel is
`M=⟨(1,Z²)⟩`; the facet projection is injective. Projecting an
end-intersection element into `T` forces it to be a medial power, proving
the top IP in `Qf`.

The quotient by `M` remains polytopal. The criterion

\[
q(E)\cap q(F)=q(E\cap F)
\iff N\cap EF=(N\cap E)(N\cap F)
\]

follows directly by lifting a shared image and factoring its kernel
discrepancy. Here `M` lies in the vertex and meets the facet trivially,
so both sides of the kernel-product equality are exactly `M`. The local
ends become the regular ends of `R`; mirror invariance follows from the
unique order-two subgroup of the cyclic-four kernel. This proves the
regular polytope `S`, with both end maps injective. Its degree two over
nonpolytopal `R`, together with the retained universal property of `R`,
proves minimality over `P` among all regular polytopal covers.

### Equality of the two reductions and the shared interval

Equal orders or equal characteristic-two action characters would not prove
the reductions coincide. The manuscript supplies the needed stronger
argument: its presentation (7) is exact. The two extra relators are
independent central involutions in `S`. Conversely, imposing those
conditions on the source power and square relations gives a central kernel
of order at most four over `P`; the already constructed `S` attains the
bound. Hence the surjection is an isomorphism.

Reversing/inverting the marking and exchanging the signs preserves that
presentation. I checked the displayed first-relator identity using the
centrality of the second relator; the second follows symmetrically. This
identifies the cofacet reduction with the **same marked cover over `R`**,
even for unequal signs. It proves the claimed coincidence rather than
inferring it from the finite mix orders.

For the raw shared mix, the kernel is a subdirect subgroup of
`{(i,j)∈C4² : i≡j mod 2}`. A proper subdirect subgroup would have order
four and be the graph of an automorphism of `C4`; the inversion/fixed
actions of `A` rule that out. Thus its kernel is the full order-eight
group `C4×C2`. Its even-coordinate subgroup `E` has order four and
quotient `S`.

The facet and vertex kernel intersections over `S` are the two distinct
order-two axes. Their intersection is trivial, so lifting the medial
intersection in `S` proves IP in `H`. The lower cyclic intersections still
follow from the exact marked projections to `P`. This supplies the
polytopality needed before using the quotient interval.

Any invariant subgroup containing an odd-coordinate element contains both
even axes, by subtracting its conjugates under `A` and `C`, and therefore
is the whole kernel. Every proper invariant subgroup is consequently
contained in `E`. Its subgroups are mirror stable as well, since the
coordinate actions are inversions on cyclic-four kernels and hence trivial
on their squares. Since `E` is admissible and the whole kernel is not,
`E` is the unique maximal admissible subgroup. This proves uniqueness
**under `H`**, with no inference about covers outside that interval.

## Why the finite extension census is complete

This part needs more than observing that a p-quotient computation terminated.
I checked its finite bounds and the entire two-stage enumeration.

Presentation (9) for rotational `R` is exact: its central relator kernel
over `P` has order at most two, and the actual mix attains the bound.
The full reflection presentation substitutes the adjacent reflection
products and imposes involution/string relations. Its rotation subgroup is
a quotient of that already bounded presentation; the actual reflection
extension provides the reverse order bound. The full group in the sample
therefore has order **8,192**, twice its rotational order **4,096**.
The code's `rr` is the complete eight-relator list added to the involution/
string group `W`; the reused symbol `r1` in prose causes no code ambiguity.

Let `G` have lower exponent-two central class `c`, and let `E→G` be one of
the displayed universal extensions. The kernel is the normal closure of
the relator images. In each presentation, the displayed conjugation
relations reduce that normal closure to a finite, explicitly bounded
abelian 2-group. Thus `E` is itself a finite 2-group, not an arbitrary
infinite group with a detected small quotient.

* In the central elementary-abelian case, the kernel is central of exponent
  two. Once the lower exponent-two series enters it after `c` steps,
  one more step kills it. Thus the class is at most `c+1`.
* In the scalar cyclic-four case, the kernel is abelian of exponent at most
  four, and each generator acts by identity or inversion. Its squares are
  central of exponent two. There are at most two further layers, giving
  class at most `c+2`.
* In the noncentral elementary-abelian case, the commutators `vi` are central
  involutions and the other kernel generators are involutions whose
  conjugation discrepancies lie in their span. Again two layers suffice.

GAP's documented class parameter returns the quotient by the corresponding
lower exponent-p central term; the proved bounds therefore make the computed
quotient the **whole presented extension**. `PClassPGroup` uses that same
series. This checks the off-by-one convention, rather than trusting the
name of a software option. See the official [PQuotient documentation](https://gap-system.github.io/gap/doc/ref/chap47_mj.html)
and [PClassPGroup documentation](https://gap-system.github.io/gap/doc/ref/chap39_mj.html).

Every degree-two marked extension has a central `C2` kernel and is covered
by the first universal presentation. Its 15 kernel hyperplanes are
therefore exhaustive. All 67 subgroups of `C2^4` give the complete larger
central-elementary-abelian interval.

A degree-four kernel is either `C4` or `V4`, and its conjugation action
factors through `G` because the kernel is abelian. For `C4`, all sixteen
assignments of inversion/fixed signs to the four reflections are tested.
Every surjection of the resulting abelian kernel onto `C4` is enumerated
from independent abelian generators. The order filters are valid because
only orders 1, 2 and 4 occur. Duplicate homomorphisms with the same kernel
are removed; every such subgroup is invariant under the scalar actions.

For a noncentral `V4`, a 2-group has image of order two in
`Aut(V4)≅S3`. In a suitable basis this is the unique nontrivial Jordan
involution. The fifteen nonzero binary characters exhaust the choices of
which reflections act nontrivially. Choosing a pivot reflection with bit
one and setting `vi=[wi,rpivot]` yields exactly the displayed universal
relations for every such module extension. Enumerating a hyperplane and
then one of its hyperplanes reaches every codimension-two subgroup; normality
filters exactly the invariant ones. Central quotients are explicitly
excluded from this branch to avoid overlap with the first computation.

Different nontrivial characters cannot describe the same marked extension
over `G`, because the action on its abelian kernel is intrinsic. For a
fixed universal presentation, equal quotient-map kernels are exactly the
duplicate marked quotients; a change of basis does not create additional
marked covers. The scalar and elementary-abelian kernel types are disjoint.
Thus the summed counts are counts of marked covers, not raw presentations
or repeated maps.

The four-reflection IP test checks both rank-three end intersections and
the rank-four end intersection. Nonadjacent commutation is imposed in `W`;
the projection onto the exact base ensures nontrivial distinct involutions
and the lower rank-two nondegeneracy. Consequently the test is the recursive
string-C criterion, not merely a group-order filter.

For each accepted cyclic-four kernel, squaring its generators gives its
unique intermediate subgroup of order two. A noncentral `V4` has exactly
one invariant line, which the code explicitly verifies. The resulting
degree-two quotient's IP is then checked. All central-V4 cases lie in the
already completely enumerated central interval, whose unique maximal
admissible subgroup gives the same double quotient. Hence no proper
intermediate possibility needed for the degree-four minimality claim is
omitted.

## Fresh computation and exact evidence

I freshly ran the frozen runner with new private report and log paths.
The two standalone programs took **36.899058** and **8.869749** seconds,
respectively. Both completed successfully with empty stderr. The complete
9,025-byte combined log was then read in full and is byte-identical to the
author's frozen log, SHA-256
`1f3bba0c157b740812e7a6a3d429c70ec42282466e18893f7a332987d8b7bff2`.

The exact source/program hashes were verified before this run. The
independent evidence checker subsequently verified every order and all six
kernel/IP rows in each of the eight uniform cases, every shared-interval
row, all sixteen scalar-character rows and all fifteen noncentral-character
rows. It also checked all **26 bound inputs** remained unchanged. A fresh
attempt to reuse the two existing replay output paths failed before GAP
and preserved both files. This is an additional refusal test, not another
census execution.

| Sample output | Fresh result |
| --- | ---: |
| Full `R` order and lower exponent-two class | 8,192 and 5 |
| Universal central extension order / kernel | 131,072 / `C2^4` |
| Double-cover hyperplanes / polytopal quotients | 15 / 1 |
| Entire central interval subgroups / polytopal quotients | 67 / 4 |
| Sizes of admissible subgroups in the central kernel | 2, 4, 4, 8 |
| Maximal admissible central-kernel subgroup | Unique, order 8 |
| Polytopal quartic cyclic kernels | 16 |
| Polytopal quartic central `V4` kernels | 2 |
| Polytopal quartic noncentral `V4` kernels | 11 |
| Total marked quartic covers / new minimal quartic covers | 29 / 0 |

All eight uniform checks cover `β=5,6` and every sign pair. Those rows are
cross-checks of the written all-parameter proof. The complete extension
census remains only for `β=5`, signs `(+,+)`; it cannot be promoted to an
all-parameter degree-four classification.

The active stock GAP executable reported **4.15.1** and is bound in the
independent evidence. Its exact finite-presentation, p-quotient, permutation
group, subgroup and homomorphism algorithms remain trusted computational
inputs. No Lean build or new Lean component is supplied by phase58 or
this audit. In particular, the separate odd-prime character-separation
Lean theorem cannot be applied with `p=2`.

The historical runner still binds private primary-extraction and earlier
package files. The two GAP programs themselves are standalone. A public
wrapper can bind and execute them without exporting those primary captures;
that packaging would be a separate change, not an additional proof.

## Remaining limits and admission

The retained source family and geometry are explicitly identified, and the
new proof does not import its target cover coincidence or interval result.
I found no mathematical gap requiring a change to the frozen theorem.
The result is admissible at its exact stated scope, together with the
trusted-GAP finite certificate boundary.

The other three two-primary source families, higher-degree extensions,
odd-order kernels, arbitrary covers outside `H`, global uniqueness and
global join-density are outside this package. Later phase66 work must be
reviewed separately and does not retrospectively enlarge phase58's frozen
statement. No current-literature/priority clearance is claimed.

This review adds no source manuscript to the ten-source compression assembly,
no whole-paper compression claim and no measured length factor. It supplies
an independently reviewed new repository theorem about a construction's
limitation and a separately bounded finite classification. The exact export
allowlist includes the author package and this independent evidence, while
keeping primary source captures private. Public admission/export is a
separate root action.
