# Math Compression

**How much of a research programme can a few good ideas and a strong LLM compress?**

This project tests whether decades of mathematical work across a connected
research community can be reorganized into a small collection of reusable
ideas, shorter proofs and independently checkable certificates. A strong
language model and coordinated agents carry out the literature analysis,
derivations, computation and formalization.

The ambition is substantial: compress results across a network of researchers,
collaborators, students and postdocs, and use the resulting theory to attack
their open problems. Success means reproducing exact theorem statements with
fewer independent arguments, exposing the inputs that remain, and obtaining
new consequences. The evidence is the mathematics and its checks.

[Compress_A](COMPRESS_A.md) now maps three named manuscripts from 1998,
2002 and 2005 to one continuous replacement with 23 explicit source adapters.
Forest cuts, sign kernels and one relative-generation proof connect symmetric
groups to Frattini quotients and finite-p-group coordinate geometries. A
separate agent has reviewed the whole assembled text and its corrected,
explicitly scoped main-result contract. Retained background remains visible.
No three-paper length ratio has been measured. The earlier two-paper
measurement remains a separate representation-sensitive experiment.

A second reviewed manuscript, [Compress_B](COMPRESS_B.md), derives the
declared main theorems of four papers from 2019–2026 using deletion maps,
one square-lattice seed, graded support and bounded cyclic extensions. Its
complete eight-family classification includes an independently replayed
finite census. The [named manuscript map](MANUSCRIPT_MAP.md) records the
seven distinct source manuscripts across these two replacements. The four-paper
bundle has a [reviewed conditional factor of 3.93×](research/case_study/phase38_compress_B_measurement_root_audit.md):
32,476 source PDF-extracted tokens versus 8,267 in the complete rendered
replacement, including its census appendix. Nonwhitespace characters give
3.35×. The listed background proofs remain imported. The three-paper
measurement and integration into one shorter seven-paper theory remain work.

A [proved bridge between the two replacements](research/case_study/phase38_primitive_saturation.md)
now identifies the unique primitive coarsening of each omission action in an
irredundantly marked finite p-group. For the forest two-groups it factors
through the canonical class-two quotient, with exact parabolic kernels and
coset fibers. This yields all face and induced-residue indices of the
prescribed-square family by one formula. The [root review and fresh diagnostics](research/case_study/phase38_primitive_saturation_root_audit.md)
pass the stated theorem. This connects A's Frattini branch to B; A's symmetric
classification remains separate, and the two full manuscripts are not yet
one shorter replacement.

The [new independent assessment](CURRENT_STATE.md) gives the exact named
intake-to-replacement map, the measured four-paper factor and the next steps.
Its author is separate from the manuscript authors and integration reviewers,
and independently reproduced the counts. The [previous two-paper assessment](CURRENT_ASSESSMENT.md)
and [earlier candidate assessment](INDEPENDENT_ASSESSMENT.md) remain unchanged.
The [measurement protocol](MEASUREMENT.md#the-manuscript-level-experiment)
defines the sum-of-manuscripts ratio and its required coverage audit.

## The method

The initial case study concerns finite groups, highly symmetric polytopes,
incidence geometries and related graphs. Three recurring ideas do much of
the work:

1. **Marked group torsors.** Represent subgroups by invariant partitions of a
   common torsor. Hadamard products compute intersections; matrix products
   count factorizations; a coset Helly condition detects flag transitivity.
   In graph covers, the same coset data control chamber completion, and
   common-shadow monodromy gives an exact residual-connectivity test.
2. **Small quotients and cyclic extensions.** Reduce growing groups to bounded
   quotients. Associativity and marked generator relations become affine
   linear congruences in cocycle coefficients. Kernel arithmetic tests the
   remaining subgroup intersections.
3. **Short matrix equations.** Replace geometric casework by a normal form,
   a word-membership calculation, a Vandermonde rank argument or an invariant
   form obstruction.

Permutation matrices are linear operators. The additional structure matters:
we retain the distinguished basis, or equivalently the multiplication of the
split algebra of functions on the torsor. For fixed cyclic-extension data,
the classification equations themselves become linear over a finite ring.

Start with the [detailed introduction](INTRODUCTION.md), which develops the
ideas through worked examples, and the [paper map](PAPER_MAP.md), which
records the exact scope of each reduction and the older literature intake.
Then see the [torsor theory](research/case_study/torsor_matrix_theory.md),
the [fixed-size extension theorem](research/case_study/phase3_bounded_families.md),
and the [theorem-by-theorem scope table](research/case_study/torsor_compression_overview.md).

The [general parabolic comparison theorem](research/case_study/phase36_parabolic_comparison.md)
now isolates the bounded-product mechanism: exact protected products and
exceptional membership preserve both subgroup intersections and flag
completion across unrelated quotients. [Lean proves both full subgroup-intersection and flag-completion equivalences](research/case_study/formal/ParabolicMarkedComparison.scope.md),
even for arbitrary type sets and nonsurjective homomorphisms.

## Results in this snapshot

An [eight-dimensional integer tensor construction](research/case_study/phase35_L003_tensor_model.md),
with its [geometric completion](research/case_study/phase35_L003_tensor_geometry.md),
now gives finite regular hypertopes with exact ordered toroidal residues
$((3,0),(2,0),(1,1),(s,0))$ for **every integer $s\ge2$**. Fibonacci moduli
give all $s\ge4$; two previously certified small examples supply $s=2,3$.
The uniform geometry proof reduces to 1,928 bounded products, 52 exact
membership witnesses and complete subgroup/flag tests at moduli three and
five. [Lean verifies the uniform Fibonacci arithmetic](research/case_study/formal/FibonacciModulus.scope.md);
the geometric transfer is a separately reviewed written proof with an exact
computational certificate. Current priority remains unverified. This proves
finite examples, not finiteness of every universal group.


The [two triangle-wreath certificates](research/case_study/phase40_triangle_quotients_root_audit.md)
now formally construct the exact rotational and four-involution presentation
maps and explicit subgroup surjections onto the triangle group, uniformly
in the parameter. All ten and fourteen defining words are kernel checked.
Their infinitude transfers explicitly assume triangle-group infinitude;
the real-matrix proof of that hypothesis remains written mathematics.
Both fresh public builds use only the standard recorded axioms.

The [compact even family](research/case_study/phase35_L003_affine_model.md)
also gives a smaller six-coordinate construction for $s=2m$, with group
order $1296m^6$. Its standalone certificate checks all 5,287 flags of the
finite base, and an exact intertwiner identifies it with the earlier voltage
construction. [Lean checks](research/case_study/formal/CompactAffineData.scope.md)
the literal relations and translations. A [short splitting argument](research/case_study/phase35_L003_affine_split.md)
identifies every group as $(\mathbb Z/m\mathbb Z)^6\rtimes Q$, with one
explicit integral group $Q$ of order 1,296.

The separate [multiples-of-three family](research/case_study/phase34_L003_triple_family.md)
has an independent exhaustive check of all 56,225 base flags. The [all-parameter universal corollary](research/case_study/phase35_L003_all_universal.md)
establishes actual marked regular universal objects for every integer
$s\ge2$. Each has a finite quotient preserving all four local groups;
a [new triangle-group quotient proof](research/case_study/phase38_L003_universal_triangle.md)
shows that the universal groups themselves are infinite for **every integer
$s\ge6$**. A subgroup of the wreath-product image maps onto the triangle
group of type (2,3,s), and explicit real reflection matrices prove infinitude.
The [complete written review and fresh exact check](research/case_study/phase38_L003_universal_triangle_root_audit.md)
pass. Finiteness at s=2,3,4,5 remains a retained published computation;
the new theorem's historical priority is unverified.
The [source-scope audit](research/case_study/phase35_L003_problem92_scope.md)
explains precisely which reading of the 2018 existence question is answered.
The [priority audit](research/case_study/phase35_L003_priority_status.md)
retains a material unread comparison with a 2024 covering theorem.

The [unfilled universal group](research/case_study/phase35_L003_unfilled_geometry.md),
before the final parameter relation is imposed, is also an actual regular
hypertope group. A [free-word certificate](research/case_study/phase34_L003_unfilled_structure.md)
gives a subgroup of index 1,296 mapping onto a rank-two free group. This
proves that its virtually abelian affine quotient is proper; it does not
settle the remaining finite parameter cases.

For the 2000 incidence construction, the notes recover the complete
[neighbourhood theorem](research/case_study/phase32_L111_arbitrary_rank.md),
including arbitrary rank, and the merging/splitting construction. They also
give [two counterexamples to assertions in its accessed version](research/case_study/phase32_L111_section6_theory.md).
Correction priority and later versions remain unverified.

These are internally reviewed research drafts. Proposed new resolutions have
not received external peer review, and publication priority remains unverified.
The proposed PSL₄ resolution has a separate
[dated literature audit](research/case_study/phase8_psl4_status_audit.md).

| Result | What is established here | Evidence |
|---|---|---|
| Fixed-excess cyclic extensions | A classification procedure using bounded quotient data, fixed-size affine systems, a free change-of-section action, and exact cyclic intersection tests | [General theorem](research/case_study/phase3_bounded_families.md); exact modular solver |
| Exact bounded-core classification at fixed excess | For order 2^(2d−1+k), a canonical core on at most 5k markers determines the group, and every qualifying core attaches by an explicit central cocycle. The marked count is a degree-k polynomial for d≥6k−1, with leading coefficient 5^k/k! | [Support theorem](research/case_study/phase16_fixed_excess.md), [attachment proof](research/case_study/phase16_central_join.md) and [leading coefficient](research/case_study/phase18_leading_coefficient.md); independent internal reviews. Higher-class markings contribute only lower degree; unrestricted coefficients beyond excess three and priority remain unresolved |
| Finite transition theory for every fixed nilpotency class | Bounded consecutive windows and their actual deletion kernels give an exact finite-state classification in every rank, with rational counting by rank and excess. At excess k, local windows have rank k+2 and order at most 2^(3k+3) | [Construction, IP and completeness proof](research/case_study/phase20_finite_state.md); independent written review and 288,000 exact meets in bounded transition diagnostics. Tests cover positive constructions; general compatibility rejection and noncentral diagonals remain written proof. No practical complexity or priority claim |
| Complete class-at-most-three census in every rank | Binary edge and triple data classify every ordered nondegenerate path marking in this class. A two-by-two transfer matrix counts each excess; the total at rank d is Fibonacci F_(4d−5) | [Uniform classification](research/case_study/phase18_class_three.md); two independent written reviews, 123,072 actual group meets and an independent enumeration of all 29,602 small kernel subspaces. These are bounded diagnostics; the proof is all-rank. [Prior map-classification overlap](research/case_study/phase18_class_three_status.md) remains to be matched before any priority claim |
| Exact first-excess census in every rank | Exactly 5d−10 ordered markings of rank d and order 2^(2d), for every d≥3. Binary edge/triple parameters give a complete presentation; the intersection property holds exactly when the active supports have a least member | [Classification](research/case_study/phase17_k1_classification.md); two independent written reviews, 138,432 exact finite meets and a Lean certificate for the quotient/kernel transport step. Recovers the specified 2018 rank-five counts; priority remains unverified |
| Complete excess-two census in every rank | Exactly (25d²−107d+122)/2 ordered nondegenerate markings of rank d and order 2^(2d+1), for every d≥3. The extra 9d−20 cases have class four | [Classification](research/case_study/phase19_k2_classification.md); two independent written reviews, an independent exhaustive rank-three quotient census and a [Lean nested-kernel adapter](research/case_study/formal/NestedKernelIntersections.scope.md). Seed construction and completeness remain written; priority is unverified |
| Exact excess-three count in every rank | For rank d≥4 and order 2^(2d+2), the ordered-marking count is (125d³−855d²+2380d−2646)/6; rank three has 37 | [Complete transition graph](research/case_study/phase22_excess3_transitions.md) and [exact operator certificate](research/case_study/phase22_excess3_annihilator.md). Fresh GAP regeneration reproduces all 708 states and 1,522 edges, with 731,136 actual meets. The 2,832-coordinate identity (T−I)⁴v₇=0 proves every later rank. A [Lean supplement](research/case_study/formal/Phase23TransferAnnihilator.scope.md) checks the finite identities using native evaluation, with four explicit compiler-evaluation axioms. Group-to-graph completeness, reversal counts, priority and full formalization remain separate |
| Complete principal classification from 2018 | The nondegenerate order-1,024 census has 1, 125, 105 and 8 classes in ranks two through five; an index bound excludes higher ranks. Central-quotient, presentation-lift and affine-center adapters recover the constructive mechanisms | [Rank-three census](research/case_study/phase22_N009_rank3.md), [kernel proof](research/case_study/phase21_kernel_ladder.md), [central adapters](research/case_study/phase21_central_quotient.md), [presentation proof](research/case_study/phase21_N009_presentations.md) and [lemma adapters](research/case_study/phase22_N009_lemma_adapters.md). Fresh rank-three verification checks all 401 candidates and 25,664 full meets. The [Table 6 adapter](research/case_study/phase22_N009_table_labels.md) now also matches all 107 rows through 428 exact marked facet isomorphisms and verifies all 106 finite universal orders. The infinite decomposition is retained. The [complete statement ledger](research/case_study/phase24_N009_coverage.md) now accounts for all 27 numbered items and six tables. Fresh checks add 34 raw presentations and 3,328 meets. Three printed presentation discrepancies and an order-eight boundary are explicit; this is principal-result coverage with retained inputs, not literal whole-document validity |
| Six principal construction theorems from 2025 | Boolean deletion maps and fiber products recover the full finite regular family and presentation, the alternating family, and—with an amalgam torsion lemma—all three infinite extension results | [Complete scoped reduction](research/case_study/phase16_fiber_products.md); 3,008 finite subgroup meets, independent review and two Lean components. The specified geometric correspondences remain explicit inputs |
| Frattini geometry, 2005 | A maximal-chain argument, coset-kernel transport and a coordinate basis recover all principal new geometric results and the finite relative-generator theorem | [Reduction](research/case_study/phase16_frattini_geometry_reduction.md); independent source/proof review and 774,039 finite families checked. The unrestricted infinite relative-generator converse is explicitly excluded |
| Six constructions from one marking, 2005 | Endpoint conjugation and a central involution twist recover all six principal Janko-group construction theorems | [Uniform reduction](research/case_study/phase24_L088_theory.md); fresh verification of 1,536 subgroup meets, 168 typed Helly equalities and 66 residue-generation tests. The source presentation is checked by a completed coset enumeration. The exhaustive six-only classification is retained background; a printed figure-label transposition is recorded. Lean checks the mixed-intersection step |
| General endpoint changes | At any finite rank, including infinite groups, the changed marking has IP exactly when one parabolic overlap is correct and the subsets recovering the removed endpoint have a least support (or are absent) | [Exact criterion](research/case_study/phase26_halving_core.md); independent written review and 21,888 finite diagnostic meets. An explicit S6 example shows the support condition cannot be dropped. Two scoped Lean modules prove the mixed meet and the two-coset obstruction. The geometric overlap criterion has published precedents; full geometry, priority and a matched length ratio remain separate |
| Petrial obstruction and biduality, 2001 | A retained-object action with explicit kernel proves the principal obstruction from thinness alone, then recovers thin-case faithfulness, automorphism equality and biduality | [Proof and exact source ledger](research/case_study/phase25_L108_reduction.md); independent review and seven finite geometric checks. The unconditional automorphism inclusion is corrected by an explicit counterexample, not counted as proved. No finiteness assumption is needed in the written proof |
| Eight high-type families of regular rank-three polytopes | Both principal existence and classification theorems of the source paper rederived | [Proof](research/case_study/phase3_classification.md); eight model checks; exhaustive order-256 seed census |
| Suzuki graph pentagons | Proposed uniform proof of exactly \(q-1\) pentagons per edge | [Proof](research/case_study/suzuki_cycle_proof.md); Lean checks the complete matrix-membership equivalence; independent coset graph |
| Remaining PSL₂ chiral construction | Proposed proofs of the two field/intersection conjectures and their classification consequence | [Proof chain](research/case_study/psl2_chiral_corollary.md); exact finite-field witnesses; partial Lean certificates |
| Commuting involutions | All four principal results of one counting paper rederived, followed by an all-rank extension | [Reduction](research/case_study/commuting_pairs_compression.md); orbit formulas and exact exceptional-case checks |
| Odd-characteristic PSL₄ rank | Complete proposed proof of maximum rank four for every odd q; a broader theorem forces a bilinear form for irreducible four-dimensional projective string actions of rank at least five | [Rank-six proof and dependency map](research/case_study/phase8_psl4_rank6.md); independent internal reviews, exact symbolic checks and two partial Lean components. Published rank-four existence is retained; priority remains unverified |
| Linear and unitary consequences of the same theorem | Rank at most four for every odd-field group between PSL₄ and PGL₄, or between PSU₄ and PGU₄; cyclic index-four extensions cannot be generated by involutions | [Uniform application](research/case_study/phase9_linear_unitary.md); independent review, exact character checks and a [Lean transvection obstruction](research/case_study/formal/TransvectionForms.scope.md). Field/graph extensions remain incomplete |
| A common matrix-generation theorem | Over any field, a subgroup of the special-linear block parabolic with full diagonal-product image and a unipotent Jordan block larger than either diagonal block must be the whole parabolic. A coupled version covers the odd unitary construction for q≥5, with an explicit counterexample at q=3 | [Proof and application adapters](research/case_study/phase23_generation_core.md); independent proof/code review and fresh 22-group diagnostics. Unifies the kernel/complement steps, including characteristic two for independent blocks. Full diagonal image, ambient root extraction and marked intersections remain separate; no additional whole-paper or novelty claim |
| Completing the odd linear diagonal interval | An explicit matrix template gives type {4,2p,2p} for every diagonal index-two extension over F_(p^e). Maximum rank is four at socle index one or two; index four forbids involution generation | [Uniform proof](research/case_study/phase16_linear_diagonal.md); two internal written reviews, 89 symbolic identities and all 1,024 subset meets for q=3,5,7,9. Rank-three existence at q≡3 mod4 is retained from a [2025 theorem](research/case_study/phase20_linear_rank3_intake.md). The new rank-three construction below completes the rank set of the diagonal index-two family. Field/graph cases and priority remain unresolved |
| Completing the odd unitary diagonal interval | The unique diagonal index-two extension has type {4,2(q+1),2p} and maximum rank four for every odd q≥3, including an extension of the exceptional simple socle PSU₄(3) | [First congruence branch](research/case_study/phase17_unitary_diagonal.md) and [second branch](research/case_study/phase17_unitary_twisted.md); two independent written reviews, symbolic checks and 1,792 exact meets in seven fields. The q=3 generation base is computational; other fields use the written proof. The new rank-three construction below completes the rank set for these groups. Priority remains unverified |
| Rank three for every odd linear diagonal extension | A nonsquare endpoint and a reflection generate the diagonal index-two extension of PSL₄(q) for every odd q≥5. The published q=3 case and earlier results give exact rank set {3,4} for every odd q≥3 | [Uniform proof](research/case_study/phase21_linear_rank3.md); two internal written reviews, 34 exact symbolic checks and a fresh six-field GAP run with 384 subgroup meets. The q≡3 mod4 range is already published, and a [primary thesis supplement](research/case_study/phase22_linear_priority_supplement.md) records an earlier q≡5 mod8 claim and a limited printed-witness defect. Priority at q≡1 mod8 remains unverified. No novelty marker |
| Rank three for every odd unitary diagonal extension | A scalar-normalized anti-isometry and a reflection give rank three for every odd q≥3. Together with the retained upper bound and rank-four constructions, the exact rank set is {3,4} | [Uniform proof and finite base](research/case_study/phase20_unitary_rank3.md); independent written review, 31 symbolic identities and two independent literal-field checks of q=3. The author checks six fields and 384 meets. The broad almost-simple classification and publication priority remain unresolved |
| Rank-three generation obstruction | A form-space dimension argument leaves two possible configurations for irreducible four-dimensional triples without a bilinear similarity form, and proves that both direct folds of the rank-four templates always generate proper subgroups | [Form alternative](research/case_study/phase18_rank3_forms.md); two written reviews and exact template comparison. This excludes the specified constructions, not all possible rank-three markings |
| Maximum unitary rank for every odd q≡1 mod 4 | An elliptic parameter curve and primitive-character sieve give PSU₄(q) maximum rank four, with type {4,q²−1,2p} for q>5 and {4,26,10} for q=5 | [Uniform proof](research/case_study/phase13_unitary_sieve.md); exact sieve over 4,795 fields and all 406 exceptional witnesses verified independently by polynomial arithmetic. Generation, intersection and the upper bound retain their reviewed inputs |
| Completing unitary existence for every odd q≥5 | A twisted norm curve and the sphere matrix template supply the remaining q≡3 mod 4 family. With the earlier construction and upper bound, the rank set is {3,4} for every odd q≥5; PSU₄(3) is a retained published exception | [Complete proposed proof](research/case_study/phase15_unitary_sieve.md); independent written reviews, exact sieve over 40,389 fields and independent polynomial verification of all 1,699 exceptions. The q=7 and q=11 cases have full finite group/intersection certificates. Current publication priority remains unverified |
| Cyclic TPP in every finite nilpotent group | Complete proposed proof that every cyclic subgroup triple with TPP satisfies \(\lvert A\rvert\lvert B\rvert\lvert C\rvert\le\lvert G\rvert\), without an order or class cutoff | [Two square-map proof](research/case_study/phase14_cyclic_tpp.md) and retained [odd-prime argument](research/case_study/phase11_odd_nilpotent.md); independent internal reviews. Published powerful-group theory remains an input; no finite catalogue or isobicyclic classification is needed. Priority is unverified |
| Hou–Feng–Leemans's 2019 hypertope order conjecture | Complete proposed proof of Conjecture 3.3: a regular hypertope of type (2ˢ,2ᵗ,2ˡ) and order 2ⁿ requires n≥s+t+l in the stated source range | [Cyclic-TPP theorem and geometric adapter](research/case_study/phase14_cyclic_tpp.md#7-consequences-and-precise-trust-boundary); flag transitivity is essential. The [bounded status audit](research/case_study/phase14_cyclic_tpp_status.md) found no later resolution, but its latest explicit open checkpoint is 2019; current priority remains unverified |
| A 2003 spread-space question | Proposed proof that locally primitive spreads in the one-dimensional affine semilinear setting are Desarguesian | [Semilinear descent](research/case_study/phase4_old_problem_audit.md); exact subspace and stabilizer checks |
| A 2004 geometric intersection algorithm | Exact flag-constrained covering criterion for shadow-IP and its residue variants; rank-two characterization rederived | [Proof and scope](research/case_study/phase4_shadow_ip.md); exhaustive small-structure comparisons |
| A 2002 sporadic-group classification | Complete principal \(J_2\) census independently reproduced: 8 rank-two, 19 rank-three, 3 rank-four geometries and no higher ranks | [Arbitrary-Borel reduction](research/case_study/phase5_j2_theory.md); exhausted augmentation and independent witness recognition, conditional on the retained subgroup catalogue |
| Three further sporadic censuses | One generalized engine gives J₁: 22/8/2; M₁₁: 6/18/12/4; M₁₂: 13/21/20/1 in successive ranks from two, with no higher ranks | [Common proof and source scope](research/case_study/phase6_sporadic_theory.md); all 226 Borel anchors exhausted and 127 witnesses independently checked. TomLib completeness retained; historical M₁₂ comparisons remain qualified |
| Two more classifications with the same engine | M₂₂: 7/25/16/9; M₂₃: 4/13/21/10, with no ranks above five, under the sources' local two-transitivity condition | [Common census](research/case_study/phase7_sporadic_theory.md); 360 anchors exhausted, 105 witnesses independently recognized; primary tables and archived lists match exactly. Original article bodies remain unavailable |
| Dihedral geometries in all ranks | Three arithmetic patterns, exact class counts and automatic geometric properties | [Uniform proof](research/case_study/phase5_dihedral_classification.md); independent subgroup/coset checks. Published all-rank theorem matched through a primary restatement; original full-paper comparison remains |
| Symmetric-group geometries, 1998–2005 | One tree-cut argument recovers primitivity tests, tree correspondence and the path criterion for geometric shadow-IP | [Common derivation](research/case_study/phase5_tree_cuts.md); retained foundational classification, finite checks and a Lean Boolean-shadow witness theorem |
| All principal results of a 2002 generator/geometry paper | Tree cuts and a sign kernel recover all eight numbered results: finite-group bounds, both maximal-generator families, their counts and the full maximum-rank geometry classification for n≥7 | [Compact complete proof](research/case_study/phase15_N003_matched_proof.md); [matched ratio 4/3](research/case_study/phase15_N003_measurement.md), with independent proof and measurement reviews. Whiston's two stated inputs and their CFSG dependence remain |
| A uniform correction to a 2026 auxiliary theorem | A path cocycle gives counterexamples in every rank d≥4 to the specified kernel-size, quotient-order and third-lower-central-subgroup claims | [Exact version and proof](research/case_study/phase12_path_cocycle.md); independent coordinate and presentation checks. The separate main common-quotient existence claim is not refuted |
| A canonical common quotient in every nilpotency class | Graded support separation gives G/γ₃(G) as the graph-cocycle group for every finite 2-group with a forest diagram and marked intersection property. Paths recover both main results of the 2026 source | [Uniform proof](research/case_study/phase15_graded_support.md) and [exact source adapter](research/case_study/phase15_graded_support_scope.md); independent written reviews. The incorrect auxiliary kernel formula remains disproved. A separate [permutation certificate](research/case_study/phase15_quotient_ip.md) shows why intermediate quotients cannot simply be assumed to preserve intersections |
| All truncations of the tree family | Weighted contraction gives exact RWPRI, local two-transitivity, rank-two and full intersection criteria | [Weighted-tree theorem](research/case_study/phase6_weighted_tree.md); exact finite audits and Lean witnesses within retained ranks. The original 2003 full-paper comparison remains |
| A missing geometry in a 1999 classification | Exact matrices in Sz(2¹⁵) give a firm, residually connected, flag-transitive RWPRI geometry absent from the asserted exhaustive list | [Counterexample and rank-four extension](research/case_study/phase6_suzuki_realization.md); exact intersections and internal independent review; Lean proves the abstract Helly implication. Corrected completeness and publication priority remain |
| Suzuki geometries in every rank | Field descent and cyclic coordinates give an unconditional all-rank family, recover the full parameterized existence assertions of two older constructions, and complete the earlier rank-four geometry proof | [All-rank derivation](research/case_study/phase7_suzuki_descent.md); [full two-family argument](research/case_study/phase7_suzuki_torus_families.md); exact checks and [Lean attachment lemma](research/case_study/formal/CosetCoordinates.scope.md). Classical descent and subgroup structure remain explicit inputs |
| Two further older construction families | A sharp pure-subfield rank criterion recovers Construction 11 and its omitted repeated-prime boundary; an exact scalar-subspace overgroup lattice rules out RWPRI for every intended Construction 10 intersection pattern | [Uniform proof and literal source scope](research/case_study/phase8_suzuki_subfields.md); independent mathematical/source review and exact matrix checks. Arbitrary other intersections and a full replacement classification remain |
| Suzuki rank and counting, 2006–2010 | Two marked field coordinates recover the older rank/existence theorem and both principal counting formulas of the later paper; the nested count becomes one Möbius sum | [Common derivation](research/case_study/phase10_suzuki_marked_fields.md); exact field orbits, 42 matrix triples and 2,688 subgroup intersections, plus a [Lean rank obstruction](research/case_study/formal/InvolutionCentralizers.scope.md). Classical Suzuki structure is retained; the original 2006 article body remains unavailable |
| The printed Suzuki realization questions | Uniform decisions for every displayed parameter shape | [Per-shape decision table](research/case_study/phase5_suzuki_higher.md#e-exact-scope-of-the-proposed-resolution). Its former assumption that the source list was exhaustive is superseded by the counterexample above |

Further notes cover affine lattice families, Hermitian-unital connectivity,
normalizer-orbit classifications, incidence constructions and a corrected
Wenger graph cycle count. Exact retained assumptions are listed in the notes.

The [exact geometric halving criterion](research/case_study/phase27_parity_theory.md)
now identifies when local parity choices preserve residual connectivity.
It recovers the complete lattice-polytope construction in a 2020 preprint's
section 3 and gives a firm counterexample family to a broader assertion in
the inspected 2024 preprint. Both finite implementations verify the example;
the all-parameter theorem has an independently reviewed written proof.
The [source-version boundary](research/case_study/phase27_halving_version_status.md)
is explicit: the revised journal body remains unverified. The later
[affine-code construction](research/case_study/phase30_affine_map.md) gives a
regular rank-four counterexample too: 983,040 chambers and 122,880 disconnected
transformed rank-two residues. The literal Theorem B/4.4 coset-isomorphism
assertion is not refuted; its surrounding hypertope-preservation claim fails.
The [surface-cover argument](research/case_study/phase31_affine_covers.md) now
gives infinitely many regular examples at the same rank and diagram. A
separate [corollary](research/case_study/phase31_affine_covers_root_audit.md)
covers every integer n≥2 coprime to six; their group orders are
120n⁸·2^(m_n), with m_n≥6n⁸+2. Standard topology and the certified finite
seed remain explicit inputs. No huge cover enumeration or novelty is claimed. The later [nested-shadow adapters](research/case_study/phase30_source_adapters.md) recover the 2020 source's principal application sections and two complete presentation families in F015.

The [general cover theorem](research/case_study/phase28_voltage_shadow_theory.md)
extends this from parity to arbitrary deck-group torsors. It separates two
exact tests: common points for compatible cosets, and equality of local
monodromy with the subgroup intersection. Two written reviews, exact
nonabelian-cover diagnostics and a [Lean common-fiber certificate](research/case_study/formal/Phase29CosetMonodromy.scope.md)
support its stated scope. Classical covering foundations are credited.

The [lift-extension theorem](research/case_study/phase30_torsor_cover_theory.md)
identifies that cover construction with the original marked chamber torsor.
Its monodromy index is exactly the defect in subgroup intersection, while
the two coset Helly tests are equivalent. The base graph-action kernel
and the separate liftability assumption are retained explicitly.

The common census theorem now supports six finite-group censuses with 262
independently recognized representatives under their recorded axioms. This
measures verified coverage; it is not a numerical proof-compression ratio.
The [principal-result ledger](PAPER_MAP.md) now contains sixteen works, with
the exact statement scopes and retained inputs recorded for each.

## What “compression” means

A shared notation is a starting point. A successful reduction must recover
the original theorem's hypotheses and conclusions, identify every retained
classification or arithmetic input, and show how the replacement argument
produces the result. Counting a partial theorem reduction as an entire paper
would misstate the evidence.

The repository does **not yet establish a reduction of dozens of complete
papers to one solved theory**. It contains several complete principal-result
reductions, broader uniform theorems, proposed conjecture proofs and explicit
remaining gaps. These distinctions are part of the experiment.

[The first matched-proof measurement](research/case_study/phase9_L066_measurement.md)
gives **3.34×** for two exact counting formulas outside degree six: 10,668
normalized non-whitespace characters in the source arguments and 3,192 in
the replacement. The shared orbit argument is counted once; an unnecessary
source proposition is excluded. The ratio is conditional on the stated
common background, and concerns this theorem subset, not the whole paper
or corpus. Token and byte sensitivity measurements are reported alongside it.

[The second matched measurement](research/case_study/phase15_N003_measurement.md)
gives **4/3≈1.33×** for all eight numbered results of the 2002
generator/geometry paper in the declared scope: 9,680 source characters
and 7,260 replacement characters. Both proof validity and the exact span
accounting have independent internal reviews. The two ratios have different
target sets and backgrounds; neither is extrapolated to the corpus.

There is also a [structural encoding bound](MEASUREMENT.md#a-separate-structural-description-bound):
at fixed excess k and rank d, identifying a marked group takes
k log₂ d+k log₂ 5−log₂(k!)+O_k(1/d) bits before rounding, conditional
on the finite core library. This follows from the exact leading
coefficient. It measures descriptions of group objects,
separately from proof-length compression.
At first excess the exact count is now known: conditional on the rank and
decoder, the optimal fixed-length index has ceil(log₂(5d−10)) bits.
At excess two it has ceil(log₂((25d²−107d+122)/2)) bits. These are
object-index costs, with the rank and decoder charged separately.

[Measurement](MEASUREMENT.md) defines the accounting and the separate novelty
assessment for verified solutions of previously open problems. “∞” is reserved
as a qualitative new-resolution marker, not a literal proof-length ratio.
No corpus ratio or infinity marker is assigned yet: proposed resolutions
still need priority verification.

The starting bibliography was seeded from Dimitri Leemans's publication
catalogue and expanded through coauthored papers and relevant followups.
It currently indexes 128 mathematical catalogue entries, 17 followups and
15 additional works across the collaborator network, for 160 in total.
The living registry records 101 accessible complete texts or primary renderings;
reading depth ranges from targeted searches to complete proof reading.
Across the full inventory, 49 entries have abstract-level reading and nine
have metadata/access records only. That is neither complete
proof reading nor an exhaustive inventory of every collaborator's work.
Student and postdoctoral relationships require independent documentation;
coauthorship alone is not evidence of either.

## Check it

```sh
python3 scripts/verify_snapshot.py
python3 scripts/smoke_check.py --quick
```

The first command checks the published artifact hashes and saved certificate
scope. The second reruns selected exact computations in scratch space.
See [REPRODUCING.md](REPRODUCING.md) for dependencies, broader checks and Lean.

Thirty-eight Lean modules certify specified components, with no `sorry` in the checked
sources. They do not constitute an end-to-end formalization of every theorem.
One transfer-arithmetic module uses four explicitly recorded native-evaluation
axioms; the other 37 reports have no native-evaluation axioms.
Finite computations, exhaustive finite classifications, written all-parameter
proofs and formal certificates are identified separately.

## Sources, attribution and contributions

Each reduction cites its source and precise target. Established coset geometry,
group cohomology, finite-group structure and linear algebra remain credited
ingredients. Claims of shorter derivations or stronger consequences concern
mathematical statements, not the people who developed the subject.

Cached papers, extracted full texts, source-page images and dependency libraries
are excluded. [Source metadata](research/case_study/sources/README.md) preserve
links and checksums. [Provenance](provenance/README.md) distinguishes historical
run records from the public snapshot and its portability edits.

Corrections, independent proof reviews, counterexamples and reproducibility
reports are welcome. A useful report identifies the exact statement or file,
the suspected gap, and a minimal argument or computation demonstrating it.
