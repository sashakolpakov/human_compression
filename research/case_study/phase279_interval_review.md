# Independent review of interval lifting and the coprime-kernel obstruction

11 October 2026. Review phase279. The exact accepted author freeze is
`phase277_export.json`, SHA256
`72e92ed82299be8c658c2f3cb45f75e67f81b0fb48379fb052de05ea3d1007c9`.
No frozen author file has been changed.

## Mathematical verdict and scope

The complete written interval-lifting argument and the separated-parabolic
kernel-divisibility theorem are sound. I have read the complete bound
Monson–Schulte source proof on which the extension depends, the complete
author manuscripts and actual finite checker. No unresolved mathematical
gap was found. A small rank-three omission in an early reduction paragraph
was corrected by the author before freezing; the exact repair is described
below.

The positive theorem says that any prescribed finite minimal marked
C-cover of a contiguous parabolic of a finite string group occurs as
exactly that parabolic in a finite minimal global C-cover. In particular,
infinitely many local minimal covers imply infinitely many global ones.
Combined with the independently accepted phase256 theorem, this proves
finite minimal-cover infinitude for every finite polytope whose monodromy
has a non-C subgroup on four consecutive marks, in any ambient rank.

It does not prove finite minimal-cover infinitude for every finite polytope
in every rank. It does not assert that an arbitrary global minimal cover
restricts to a minimal local one, or that the global cover has prime-power
kernel. It gives no complete historical-source replacement credit and no
compression ratio. The separate rank-five exploration file is not part of
this acceptance or the frozen review exports.

## 1. Exact use of Monson–Schulte

The source is *Finite Polytopes have Finite Regular Covers*, the seven-page
PDF bound in the author's source record and in `phase256_sources.json`.
I checked Lemma 3.1, physical pages 4–5, the whole proof of Lemma 3.3 on
page 5, and the statements of Theorem 3.4 and the covering bridge.
The source edition has the metadata qualifications recorded in the bound
ledger; a local filename is not evidence of a distinct historical edition.

Lemma 3.1 constructs a finite regular extension of a finite C-group Q
with Q as the initial maximal parabolic. In Lemma 3.3, the product
construction with the desired larger marked target does something stronger
than preserving only small parabolics on which Q's target map is faithful.
The subgroup on the original marks is the graph of Q→G_I, so it is exactly
Q even when that map has nontrivial kernel. Projection to the regular
extension is injective on this maximal parabolic, and the quotient
criterion proves that the new marked group is C. Projection to the other
factor gives the required epimorphism to the larger interval of G.

This graph-of-map identity is printed explicitly in the source proof. The
new note uses it correctly; it does not deduce preservation merely from
the weaker wording of a finite-existence theorem. Reindexing an arbitrary
interval, extending to the right, and then reversing indices to extend
to the left preserves each previously constructed maximal parabolic.
Thus the initial prescribed interval remains unchanged throughout. Every
intermediate group and extension is finite. If the original interval is
already the whole marking, no extension is needed.

The source's extension and quotient criterion remain retained inputs.
The manuscript is an application and consequence of that proof, not a new
claim to have first established finite regular-cover existence.

## 2. Minimal descendants and distinct global covers

Inside the finite extension R, choose a C-group quotient M over G minimal
under further C-group quotients over G. Finiteness ensures existence.
Any further such quotient of M remains a quotient of R, so this is global
minimality, not minimality within an artificially truncated catalogue.

The interval restriction is a surjective marked map Q≅R_I→M_I→G_I.
Every standard parabolic of a string C-group is C, so M_I is itself a
C-cover of G_I. Minimality of Q forces Q→M_I to be an isomorphism.
The compatibility with the map to G_I is automatic on the ordered marks.
This proves the asserted occurrence of the whole prescribed local cover.

A marked isomorphism between two resulting global groups restricts to a
marked isomorphism on I. Distinct local covers therefore give distinct
global covers. For an infinite family, arbitrary finite subfamilies
already prove that the global collection cannot be finite. No claim about
their total group orders or prime divisors is needed.

For polytopes, normal flag kernels identify this marked quotient order
with the ordinary regular-cover order. A rank-preserving unrooted
isomorphism can be aligned at a flag by an automorphism of the regular
polytope; its normal flag kernel, and hence its ordered marking, is then
unchanged. This is the already retained covering correspondence. The
local argument has not silently proved a statement only about rooted
objects while claiming a distinctness statement about ordinary regular
covers.

## 3. Applying the rank-four theorem and reducing the residual problem

Four consecutive monodromy marks of an actual polytope are distinct
nonidentity involutions, satisfy the string commutations and have the
required extreme independence. The last property follows from the actual
flag-face action. Thus phase256 applies directly to that finite marked
subgroup; no identification of the subgroup with the monodromy group of
a single section is needed. Its non-C assumption makes every minimal
p-kernel descendant nontrivial over the subgroup. Different primes give
different local orders. Interval lifting then proves the stated all-rank
partial result.

The extension to the full marking may introduce other primes. The author
correctly declines to transport the local prime-power degree to a global
prime-power degree. This distinction is mathematically necessary, not a
technical limitation of the finite certificate.

An earlier draft implicitly skipped independent rank-three marked groups.
They need not be C: one may take D8×C2 with marks a,b,a t for reflection
generators a,b of D8 and independent central t. The final author argument
correctly appends a central independent involution to any rank-three L,
uses phase256 on L×C2, and restricts its p-kernel C-cover to the first three
marks. That restriction is C and still has p-group kernel. Minimal
descendants give infinitude when L is non-C. This uses neither the false
claim that all independent rank-three string groups are C nor the
polytope-only rank-three monodromy theorem.

Consequently a least-rank counterexample to infinitude in the broader
class of finite independent marked groups has all proper contiguous
parabolics C and rank at least five. The final formulation uses
infinitely many local covers, rather than merely two, in this least-rank
argument. Its status is a reduction for that broader class. A monodromy
parabolic need not be the monodromy of one polytope, so the author
correctly warns against transferring that minimal-counterexample argument
without its broader hypotheses.

## 4. The universal kernel-divisibility obstruction

Suppose H→G is a finite C-cover and I,J are disjoint separated color sets.
The lifted groups H_I and H_J commute and have trivial intersection, so
their product is their direct product. For K=ker(H→G), the map

    K∩(H_I H_J) → G_I∩G_J,       ab ↦ image(a)

is well defined because the factorization is unique. It is a homomorphism;
commutation allows the factors to be multiplied separately. For any
common image d, choose preimages a and b of d in the two groups. Then
ab^−1 lies in the domain and maps to d. The map is therefore surjective,
and the first isomorphism theorem followed by Lagrange gives

    |G_I∩G_J| divides |K|.

All quantifiers of this assertion are proved by the written argument.
The finite example does not purport to test all covers. The separated
condition ensures commuting lifted groups; mere commutation of some
images in G would not suffice.

For the central product of two D8 factors, with their central involutions
identified, and one additional C2 mark, the base group has order 64.
All five marks are independent, both rank-four ends are C, but the
separated pairs 01 and 34 have a common central involution. Thus every
finite C-cover has even kernel order. The direct product before central
identification, of order 128, supplies an explicit finite C-cover. This
refutes an odd-primary-kernel generalization to all independent marked
groups. It does not refute finite existence or finite minimal-cover
infinitude for this group.

It is also not a polytope counterexample. Actual monodromy permutations
on disjoint rank sets intersect trivially: a permutation in both fixes
every face of every flag. The central-product marking violates this
necessary condition. The source question remains restricted to actual
polytopes, whereas this obstruction explains why extreme independence
alone cannot support a direct higher-rank version of phase256.

Finally, the order-128 cover is not asserted to be the unique minimal
cover. The middle mark is central in the base because it commutes with
its adjacent neighbors there. These additional commutations need not
lift to a cover. Splitting an arbitrary cover into three direct factors
would therefore be invalid. The author states this qualification explicitly.

## 5. Independent finite reconstruction

My program `phase279_independent_model.py` imports no author code. It uses
rotation/reflection coordinates for D8×D8×C2, then normalizes the diagonal
central quotient by reducing the first rotation coordinate modulo two.
This differs from the author's binary-cocycle model. It verifies the
marked epimorphism and two-element kernel, all 1,024 intersection pairs
in the order-128 cover, all 512 pairs in the two base ends, the independence
of every base mark and the nontrivial separated intersection. It also
checks that leaving the centers unidentified removes that intersection,
and exhibits the failure of adjacent commutations to lift.

The two models agree on every parabolic order and every base intersection
failure after translating their coordinates. Their labels for individual
elements are not expected to agree. This is a bounded independent check
of the literal group used by the universal obstruction, not an enumeration
of possible covers.

Final frozen bindings and fresh replay results are recorded by the
companion runner and manifest. No public file is edited by this review.


## 6. Formal scope, final replay and rendering

I read all three declarations in `formal/IntervalMinimalCoverLifting.lean`.
The first proves that monotone kernel restriction cannot enlarge a maximal
locally admissible kernel while retaining admissibility. The second
combines explicitly supplied exact extension, maximal descent and
admissible restriction. The third says that distinct restrictions imply
distinct global kernels. Larger kernels correctly represent smaller
covers. These are actual order proofs, with no axioms reported by Lean.
The geometric extension, group restriction and polytope correspondence
remain explicit written inputs; the predicates do not conceal an asserted
formal proof of those inputs.

The fresh complete author replay passed in 1.598 seconds. It verified the
two bound primary PDFs, reran the complete finite obstruction model and
compiled the three Lean statements. Reversing the kernel-descent order,
removing local admissibility and removing the central identification all
failed their controls as required. All 32 base parabolic orders, all 32
cover parabolic orders and every base intersection-failure record agree
with the independent rotation/reflection model.

I viewed all three pages of the final interval paper and both pages of
the obstruction paper. Mathematical notation and all proof passages are
legible and present. There is no requested postfreeze correction. The
verdict is acceptance of the exact two written contracts with the
formal/computational scope above, not an answer to the full higher-rank
finite-cover problem.
