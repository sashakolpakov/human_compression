# Case-study research notes, proofs, and certificates

Research begun 9 October 2026; updated 10 October 2026. We have proposed proofs of the two 2017 PSL(2,q) conjectures, the 2005 Hermitian-unital conjecture, the Suzuki graph pentagon-count conjecture, and the missing range in a recent existence theorem for chiral polyhedra, together with exact computations and Lean certificates for key proof components. These results have received internal agent reviews, not external peer review. Priority and novelty remain provisional.

## Current coverage and verification

The [2000 construction](phase32_L111_theory.md) and its [arbitrary-rank
extension](phase32_L111_arbitrary_rank.md) recover complete Theorem4.1 through
chamber/residue maps and parity. The [2018 presentation certificate](phase32_L003_infinite_presentation.md)
proves infinitude for every positive parameter divisible by six, with Lean
checking the exact presentation at six. Its [image structure](phase32_L003_root_audit.md)
also gives finite quotients of unbounded order; the later geometric supplement
establishes actual hypertopes and the universal regular object at parameter six. These additions give component and proposed-result
credit, with no extra principal-paper reduction or infinity marker.

The [parity-compatible halving theorem](phase27_parity_theory.md) gives an
exact residual-connectivity criterion and recovers the full lattice-polytope
geometric construction in Montero–Weiss section 3. The same proof isolates
a firm counterexample family to the broader assertion in the inspected
Piedade–Tranchida preprint. An [independent review](phase27_parity_shadow_rank_audit.md)
and two finite implementations agree. The revised journal text is unverified,
a later [actual regular counterexample](phase30_affine_map.md) disproves the
preprint's regular-preservation consequence too. Its 983,040-chamber geometry
has 122,880 disconnected transformed rank-two residues. The literal Theorem
B/4.4 coset-isomorphism assertion is not refuted.
The [surface-cover theorem](phase31_affine_covers.md) extends this to infinitely
many regular examples at fixed rank and diagram; the separately reviewed
integer-degree corollary and prior-art limits are linked in its evidence. The later
[nested-shadow adapters](phase30_source_adapters.md) recover the 2020 source's
principal application sections and F015 Propositions 11 and 13, with their
complete presentations. Retained inputs and source qualifications are explicit.

The [living paper map](../../PAPER_MAP.md) indexes 160 works and records
16 principal-result reductions. These now include the six 2005 Janko-group
[construction theorems](phase24_L088_theory.md) and the 2001
[Petrial obstruction and conditional structural results](phase25_L108_reduction.md),
with the retained classification and corrected auxiliary claims explicit.
Another recent addition is the
[complete order-1024 statement ledger](phase24_N009_coverage.md): all 27
numbered items and six tables are accounted for, with quoted background
and literal-source discrepancies explicit. Its fresh checks verify 34
raw presentations and 3,328 actual subgroup intersections.

The [third-excess theorem](phase22_excess3_transitions.md) gives the exact
all-rank cubic; the [common generation theorem](phase23_generation_core.md)
unifies specified linear and unitary parabolic-generation steps. There are
27 [formal modules](formal/README.md). One checks finite transfer
arithmetic using native evaluation, with four compiler-evaluation axioms
disclosed separately from the other 30 reports. The affine-data module checks the counterexample's
literal binary data by kernel evaluation. The preceding module proves
the common-coset monodromy obstruction for the
[general graph-cover theorem](phase28_voltage_shadow_theory.md). That theorem
gives exact geometry and residual-connectivity criteria for arbitrary deck
groups, with its classical foundations credited and full written reviews.
The endpoint certificates retain their separate scopes. The two measured ratios
remain 3.34 and 4/3; no infinity marker is assigned. Earlier dated progress
notes below should be read with these later proofs and the living map.

The [general endpoint-change criterion](phase26_halving_core.md) now handles
every endpoint order and infinite ambient groups through one overlap and
one least-support condition. The S6 counterexample proves that the support
condition is indispensable. It adds a reusable theorem, not another paper
credit or numerical ratio.

## The latest uniform reductions

The [complete proposed cyclic-TPP theorem](phase14_cyclic_tpp.md) now gives
`|A||B||C| <= |P|` for three cyclic subgroups with TPP in every finite
nilpotent group. Two equivariant squaring maps through Frattini layers
exclude a minimum 2-group counterexample; the odd-prime proof supplies
the remaining Sylow factors. The regular-hypertope adapter gives the
complete lower bound in the published 2019 Conjecture 3.3. Two independent
internal reviews passed. The [status audit](phase14_cyclic_tpp_status.md)
leaves current priority unverified; the [Lean certificate](formal/MarkedSquareDescent.scope.md)
covers specified action and transport components, not the whole theorem.
The new uniform proof supersedes the earlier bounded subcases and removes
their finite-census and marked-isobicyclic dependencies.

The [elliptic parameter sieve](phase13_unitary_sieve.md), together with
the retained generation and intersection arguments, gives maximum rank
four for PSU4(q) for every odd q congruent to one modulo four. A separate
[exact q=7 witness](phase14_unitary_q7.md) has type `{4,24,4}` and passes
all 256 subgroup intersections. Uniform existence for q congruent to
three modulo four, q at least eleven, remains. The [latest review](../../provenance/phase14_review.md)
records fresh executions and exact scope.

## The older-paper extension

The [2003 spread-space proof](phase4_old_problem_audit.md) gives a proposed
exact existence and uniqueness theorem for the source's one-dimensional
RWPRI case, using prime-degree arithmetic and cyclic semilinear descent.
Two independent internal reviews passed; external priority remains unverified.
The [2004 shadow-IP reduction](phase4_shadow_ip.md) supplies a flag-constrained
covering criterion, with exact small-structure checks. It is distinct from
C-group subgroup intersection. The [2002 J2 track](phase4_old_classification.md)
recovers the thin classification in every rank and verifies the nonthin source
representatives. The subsequent [complete augmentation](phase5_j2_theory.md)
rederived the full census, retaining the subgroup catalogue.

## Torsors and permutation matrices: stronger compression

The [torsor matrix theory](torsor_matrix_theory.md) represents subgroups as invariant partitions of a common regular group torsor. Subgroup intersections become Hadamard products, subgroup generation becomes Boolean matrix closure, and ordinary matrix products count subgroup factorizations. A typed Helly condition detects exactly which coset flags have a common torsor point. The [Lean certificate](formal/TorsorPartitions.lean) proves subgroup/partition reconstruction and the zero-one intersection identity.

This now gives a [complete reduction of the principal results](commuting_pairs_compression.md) of the nine-page 2013 commuting-involutions paper: two short rational generating functions derive all-degree counts; an exhaustive degree-six certificate recovers both exceptional counts and both polyhedron results. The [uniform all-rank extension](elementary_action_theorem.md) replaces permutation enumeration by subspace and character calculations in F2^r. It includes independently checked counts for triples and computed counts for quadruples.

The [matrix verifier](torsor_matrix_check.json) checks all 900 subgroup pairs in S4 and an explicit example showing why ordinary rational linear equivalence loses the distinguished-basis information. The earlier 36-paper audit below records the previous, narrower core; this stronger theory upgrades its L066 assessment.

The [current compression overview](torsor_compression_overview.md) records the exact scope across the completed parallel tracks. A [single grid-and-dihedral construction](compression_phase2.md) derives the principal all-rank 2-power existence theorem, the actual presented 3-hypertope construction, and the existence theorem of the rank-three classification paper. The [new cyclic-core reduction](phase3_classification.md) also recovers its entire eight-family classification, completing both principal theorems. It retains Lucchini's core theorem and one exhaustive order-256 SmallGroups census; all larger parameters follow from binary extension identities. A [three-generator affine model](phase2_cubic_lattices.md) identifies all three published {6,6} lattice families, with orders 192m³, 384m³ and 768m³. One intersection calculation proves all parameters.

The [normalizer-torsor classification](classification_compression.md) reproduces all eight published rank-two J2 objects and all 29 Sz(8) objects using explicit GAP subgroup-catalogue inputs. An additive torsor gives the whole A4–A4 counting family for PSL(2,3^e), including a composite-degree extension with the proper change of geometric scope. The [incidence-matrix reductions](incidence_compression.md) recover the Kneser graph construction and its full automorphism group, the principal chirality test, and substantial triangle-geometry results. They also connect two unital constructions through a common residue.

These are complete reductions of specific principal results and explicitly bounded partial reductions. Higher-rank censuses, several classification theorems, and sharp nonexistence bounds remain. L029 is qualified because a bridge between the designated acting group and the full automorphism group has not been proved here. The [verification manifest](torsor_verification_manifest.json) and [Lean scope statement](formal/README.md) distinguish checked proof components, exact computations, and remaining written arguments.

## New results from the matrix and finite-extension theory

The [Suzuki graph proof](suzuki_cycle_proof.md) resolves the pentagon-count
equation in Araujo-Pardo–Leemans's Conjecture 3.2. For every
q=2^(2e+1), e≥1, three matrix entries force the four walk parameters to be
`(a,a⁻¹,a,a⁻¹)`, with a nonzero. The closing word has an explicit ZT
factorization, giving exactly q−1 pentagons per edge. The full matrix
membership equivalence is [Lean checked](formal/SuzukiPentagons.lean);
identification with the source coset graph and the cycle correspondence
remain written proofs. An independent GAP coset graph at q=8 and a universal
Laurent-polynomial checker both pass.

The [L035 classification reduction](phase3_classification.md) replaces the
large-order classification with quotients of orders 16, 64 and 256, followed
by eight extension models using at most four binary coordinates. The first
two quotients are handled structurally; the last uses a complete bounded
GAP census. The [certificate](phase3_classification_certificate.json) records
the retained inputs, all eight model checks and the census's 92 valid marked
triples. This upgrades the earlier existence-only reduction to both principal
theorems of that paper.

For the conjectural minimum order of rank-three 2-power hypertopes, the
[new lower-bound argument](phase3_order_bound.md) proves the bound when a
pair order is at most four, when the derived subgroup has class at most two
or an abelian subgroup of index two, or when two distinguished cyclic rotation
subgroups permute. It reduces the remaining cases to a cyclic triple-product
inequality. The [complete phase-fourteen proof](phase14_cyclic_tpp.md)
now supplies that inequality and the full proposed conjecture consequence.

The [Wenger graph audit](phase3_egr_conjecture_audit.md) gives one Vandermonde
rank calculation for the classical Wenger girth counts. It identifies a
discrepancy in a later preprint's odd-characteristic W₂ formula; the checked
formula agrees with Porupsánszki's published generalized-quadrangle count.
This removes that proposed route to L025 Conjecture 4.5, while leaving its
existence statement unresolved.

The [additional PSL(4,q) arguments](phase3_psl4.md) rule out every all-reflection
string representation and every completely reducible endpoint configuration
in rank five. The [rank-seven tensor obstruction](phase3_psl4_rank7.md)
improves the uniform upper bound to six. The desired sharp bound of four
remains unresolved; ranks five and six still need exclusion.

The [fixed-excess theorem](phase3_bounded_families.md) provides the broader
classification method: bounded quotient data, fixed-size affine congruences,
a free change-of-section quotient, and exact cyclic arithmetic for IP.

## New main results: the 2017 PSL(2,q) conjectures

The [proof of Conjecture 6.1](psl2_square_proof.md) establishes the primitive-square assertion for **every odd prime p and all odd e1,e2>1**, including equal and nested fields. It proves the stronger nonzero-square statement. A character-sum bound reduces the theorem to eleven small cases. All eleven have exact GAP witnesses and pass a separate [standard-library Python verifier](verify_square_witnesses.py) implementing polynomial-quotient arithmetic independently of GAP. The [integer reduction](psl2_square_bound_check.py) is also exact.

The [proof of Conjecture 6.2](psl2_intersection_proof.md) establishes the required subgroup intersection for all parameters in the paper's construction. A field automorphism argument puts the conjugation parameter outside the additive sum of two subfields; matrix entries then force the intersection to be precisely the shared cyclic group. The [exact check for q=3^15](psl2_intersection_check.log) enumerates all 19,656 matrices in SL(2,27) and finds an intersection of six matrices, or three projective elements.

Together these address the missing family in Leemans–Moerenhout–O'Reilly-Regueiro's [2017 classification](https://arxiv.org/abs/1606.08017): chiral rank-four polytopes with group PSL(2,p^d), where p^d is 3 modulo 4 and d>1 is not a prime power. The [complete classification argument](psl2_chiral_corollary.md) verifies generation, all required intersections, and a direct obstruction to a reversing automorphism. The first residual case gives type {13,3,121} with group PSL(2,3^15).

The [Lean certificates and scope statement](formal/README.md) cover the field obstruction, matrix-entry intersection and reversal obstructions, and the central-lift transfer lemmas. They compile without `sorry`. They do **not** formalize the entire character-sum argument or the full polytope correspondence.

The [systematic literature audit](literature_audit_v2.md) and [machine-readable inventory](literature_inventory.json) distinguish catalogue coverage, full-text searches, relevant-section reading, and complete reading. Cataloguing all works is not the same as reading every proof; the remaining coverage is explicit.

## General theory track

The [36-paper compression audit](compression_audit.md) tests the framework against exact published statements. It supplies complete reductions of particular theorem components and reusable propagation steps across seven papers. It also records the essential seed, classification and arithmetic arguments that remain. It does not demonstrate that dozens of entire papers follow from one short theory.

The [general framework](general_framework.md) organizes much of the group-and-polytope programme around prescribed subgroup intersections, group generation, and marked symmetries. It builds on established coset geometry and mixing theory, with explicit reusable transport and obstruction results.

The [general transvection intersection theorem](transvection_intersection_audit.md) works in every dimension over arbitrary subfields. Together with the general kernel-intersection transport theorem, it supplies reusable statements behind both successful constructions. Its [Lean certificate](formal/TransvectionIntersection.lean) proves the dimension-independent entrywise characterization. The framework also proves an exact obstruction when the PSL(2) field degrees are not coprime, and compatibility of rank reduction with suitable odd-kernel covers.

An [exact unitary-transfer obstruction](unitary_transfer_obstruction.md) shows why substituting a norm-one parameter into the known PSL(3) construction cannot produce the desired PSU(3) family. This is a certified limitation of one construction, not a resolution of the unitary existence problem. The framework explicitly identifies problems, including general Mondrian tilings, for which it supplies no solution.

The [multiple-parameter intersection theorem](multiple_twist_theorem.md) realizes the simultaneous centralizer of any prescribed collection of square-zero matrices as the exact intersection of two conjugate subfield groups. Adjacent matrix units give a root-group intersection in every dimension, subject to the stated projective-center condition. A complete [5,616-matrix GAP check](multiple_twist_check.log) verifies the first three-dimensional example. The theorem does not by itself prove generation of the ambient group.

After doubling the dimension, the same theorem realizes arbitrary matrix-algebra centralizers, and hence unit groups of finite-dimensional algebras, as such GL intersections. A separate [20,160-matrix exhaustive check](algebra_intersection_check.log) verifies the example realizing the three units of F_4.

Two [short structural proofs](coset_geometry_obstructions.md) give negative answers to the example requests in Problems 9.3 and 9.4 of the 2016 *Highly symmetric hypertopes* paper, under its standard parabolic coset construction. Thinness and residual connectedness force chamber transitivity; rank-three standard coset systems are always residually connected. An [independent definition audit](hypertope_questions_independent_audit.md) checks the scope. The [abstract chamber-orbit criterion](formal/ChamberOrbit.lean) is verified in Lean; the geometry-specific arguments remain written proofs. No priority claim is made for these elementary observations.

## Hermitian-unital conjecture: a torsor application

The [proposed proof](hermitian_unital_proof.md) of Conjecture 1 in Leemans's [2005 Van Nypelseer paper](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.46/no.2/b46h2lee.pdf) establishes firmness, residual connectedness and flag transitivity for every prime power q>2, and also q=2. It strengthens transitivity to a regular action of PGU(3,q) on chambers.

The difficult block residue becomes the set of vectors of norm minus one in a Hermitian plane. SU(2,q) acts freely and transitively on this set: it is a torsor. Elementary upper and lower unipotents generate the group and give allowed adjacency moves, which proves connectivity. The [general connectivity lemma](formal/ResidueConnectivity.lean) is checked in Lean; the Hermitian geometry and group identifications are proved in the written argument. Independent [GAP checks](hermitian_unital_check.log) pass for q=2,3,4,5. Searches found no later resolution, but publication priority remains unverified.

## Central cyclic lift

**Candidate theorem.** For every odd prime \(p\) and positive integer \(m\), a non-tight chiral abstract polyhedron with full automorphism-group order \(2p^m\) exists if and only if \(m\ge5\).

The additional range established by this work is

\[
m\text{ even},\qquad 6\le m\le p+1.
\]

Our examples in this range have Schläfli type \(\{p^2,2p^2\}\). The remaining cases and nonexistence for smaller exponents come from Kong–Feng–Hou–Leemans–Qu, [*Chiral polytopes of order 2p^m*](https://amc-journal.eu/index.php/amc/article/download/3716/2232), Theorems 1.1, 1.2 and 1.4. The accepted manuscript, accepted 19 January 2026, explicitly identifies the omitted range in Section 7, page 20. Its conjectural sentence prints “tight,” although the surrounding discussion and Theorem 1.4 concern non-tight examples. We disclose this apparent typo instead of silently rewriting its conjecture.

This is a concrete specialist result in the existence theory of chiral abstract polytopes. It would complete the parameter range of a recent theorem, if confirmed. It does not classify the individual groups or polyhedra, and it does not settle the broader simple-group conjectures below.

Read the [complete proof](central_lift_proof.md) and the [separate proof audit](central_lift_audit.md).

The key construction is short. From the paper's chiral base pair \((G_0;a_0,b_0)\), of type \(\{p^2,2p\}\) and order \(2p^{m-1}\), take

\[
H=\langle(a_0,x),(b_0,x^{-1})\rangle\le G_0\times C_{p^2},
\qquad |x|=p^2.
\]

A compatible quotient \(G_0\to C_p\) makes the projection kernel exactly \(C_p\), so \(|H|=2p^m\). The first cyclic subgroup projects injectively, which proves the required intersection property. A hypothetical automorphism inverting both new generators must preserve the kernel, since the kernel is generated by the \(2p\)-th power of the second generator. It would descend to a forbidden reversing automorphism of the original chiral pair. Thus the lift stays chiral. Its type product is \(2p^4<2p^m\), proving non-tightness.

## Verification

The [GAP program](central_lift.g) and [saved transcript](central_lift_results.txt) use exact finite-group computations:

| Prime p | Exponent m | Group order | Type | Intersection of generator subgroups | Reversing homomorphism |
|---|---|---|---|---|---|
| 5 | 6 | 31,250 | {25,50} | Trivial | None |
| 7 | 6 | 235,298 | {49,98} | Trivial | None |
| 7 | 8 | 11,529,602 | {49,98} | Trivial | None |

All three also have generator product of order two and the predicted projection kernel. A [separate Python implementation](verify_lift_normalforms.py), using explicit group multiplication rather than GAP's group-presentation machinery, independently verified the first two cases' orders, generation, cyclic intersections, and kernels. The uniform proof establishes the infinite family; these calculations are cross-checks. The [Lean lift certificate](formal/LiftCertificate.lean) verifies the chirality-transfer and cyclic-intersection lemmas, with the source construction as an explicit input.

From the workspace root:

```sh
gap -q research/leemans/central_lift.g
python3 research/leemans/verify_lift_normalforms.py --p 5 --r 4
```

## Significant questions that still appear open

The status below is based on the primary literature found, not a guarantee that no unindexed or unpublished resolution exists. Significance is assessed within the relevant mathematical specialty.

| Target | Precise question | Why it matters | Status in this investigation |
|---|---|---|---|
| PSL(4,q) maximum rank | Is four the maximum string C-group rank for every odd prime power q? | An infinite-family classification of possible dimensions for regular polytopes with a prescribed simple symmetry group. | No later uniform resolution found. Exhaustive GAP searches verify q=3 and q=5 at all ranks; several uniform subcases have proofs. |
| A11 rank gaps | Is A11 the only finite simple group whose string C-group rank spectrum has gaps? | A broad structural prediction about which dimensions can occur; stronger in scope than a single-family construction. | No later resolution found. Unsolved here. |
| Perfect Mondrian partitions | Can an integer-sided square be tiled by at least two equal-area, pairwise noncongruent, integer-sided rectangles? The conjecture says no. | A concise arithmetic tiling obstruction connecting combinatorics and divisor distribution. | Still explicitly conjectural in an August 2026 primary preprint. Unsolved here. |

The first two are Conjectures 2 and 3 in [Leemans's survey](https://arxiv.org/abs/1910.08843). See the [survey audit](survey_audit.md) for later papers and the limited PSL(4,q) argument. The Mondrian problem was studied by García-Colín–Leemans–Müßig–Roldán in [their computational paper](https://arxiv.org/abs/2311.02385); [Lebowitz-Lockard–Tenenbaum's August 2026 preprint](https://tenenb.perso.math.cnrs.fr/PPP/Mondrian.pdf) still states nonexistence as Conjecture 1.1. Its positive-density exclusion does not settle all square sizes. The [September 2026 upper bound on defect](https://arxiv.org/abs/2609.01998) also does not settle zero defect.

## Older conjectures removed from the target list

Several plausible targets were already resolved:

- The maximum rank for alternating groups: proved in 2017, [*Highest rank of a polytope for A_n*](https://arxiv.org/abs/1605.09173).
- Stabilization of high-rank symmetric-group representation counts: proved in [Cameron–Fernandes–Leemans, 2024](https://doi.org/10.1016/j.aim.2024.109832).
- Suzuki chiral polytopes have rank three: proved in [Spiga, 2021](https://arxiv.org/abs/2010.04080).
- A later conjecture about certain permutation representation graphs: counterexamples appear in [Leemans–Mulpas, 2026](https://arxiv.org/abs/2504.17535).

The [recent-paper audit](recent_conjectures.md) and [rank-stability audit](rank_stability.md) preserve the detailed distinctions. In particular, an existence classification for simple groups does not automatically classify their rank spectra.

The [PSL(4,q) search report](psl4_search_results.md) explains exhaustive coverage and its limits. The [partial uniform proofs](psl4_theory.md) identify which tensor representations have been excluded and which cases remain.

## Other exploratory work

[cage_search.py](cage_search.py) encodes cyclically symmetric middle graphs for the construction in [Araujo-Pardo–Conder–García-Colín–Kiss–Leemans](https://arxiv.org/abs/2401.15539). This was an exploratory search, not a completed classification or a proof of nonexistence. A negative result under the imposed cyclic symmetry would not rule out general graphs.

The exploratory k=7 cage run did not produce a verified solver conclusion.
No mathematical claim in this repository depends on it.

## Reproducing the new checks

The following commands run the small exact verifiers and the general theorem
examples. GAP checks use GAP 4.15.1; the Python square-witness verifier uses
only the standard library. The Lean instructions and pinned dependencies are
in [formal/README.md](formal/README.md).

```sh
python3 research/leemans/psl2_square_bound_check.py
python3 research/leemans/verify_square_witnesses.py
gap -q research/leemans/hermitian_unital_check.g
gap -q research/leemans/multiple_twist_check.g
gap -q research/leemans/algebra_intersection_check.g
```

The PSL(4) exhaustive searches and larger source constructions have separate
scripts and saved reports linked above. Finite checks verify the specified
instances; the infinite-family arguments are the written proofs.

The public repository includes [source metadata and links](sources/README.md).
Cached PDFs, extracted full texts and source images are not redistributed.
No author contact was made during the research audit.


The [fixed-parameter geometry certificate](phase32_L003_fixed_parameter_hypertopes.md)
now lifts a checked modulus-two action to every even coordinate modulus,
producing infinitely many finite regular hypertopes with source parameter6.
The [universal corollary](phase32_L003_universal_hypertope.md) proves that the
regular universal object itself is infinite and has the exact source rotation
presentation. The [formal quotient criterion](formal/ParabolicQuotientTransport.scope.md)
checks the reusable subgroup and flag-completion transport. Source parameters
do not vary with the quotient modulus, and priority remains unverified.


The [2000 merging/splitting adapter](phase32_L111_section6_theory.md) now
recovers the positive arbitrary-rank construction and identifies two exact
boundaries in the accessed source: disconnected symmetry and local versus
global graph bipartiteness. Its statement ledger records the corrections
separately. The [one-exceptional quotient theorem](phase33_one_exceptional_transport.md)
and Lean module allow one maximal local group to grow under an otherwise
injective quotient. Particular varying-parameter applications remain separate.


The [all-even construction](phase33_L003_even_family.md) now varies the
actual source parameter s=2m, with one toroidal residue growing by m².
A unit translation minor proves the exact local type at every modulus;
three fixed parabolics allow quotient transport from a checked base.
The [universal-even corollary](phase33_L003_universal_even.md) proves
marked regular universality and infinitude when6|s. The source-status audit
keeps finite existence, universal finiteness, all-integer scope and priority
separate. No general full-group order formula is asserted by this package.
