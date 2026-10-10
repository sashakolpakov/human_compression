# Independent assembled review of Compress_B

10 October 2026. Reviewer: `recent_conjectures`, an internal collaborating agent.

**PASS for the declared eleven-target, four-manuscript contract, conditional on the explicit retained inputs.** I read the complete assembled manuscript, all proofs and Appendix A, the source ledger and machine manifest, and the executable finite census. I found no unresolved mathematical gap after the two scope clarifications recorded below. A fresh unchanged census run reproduced all required counts and relation rows.

The reviewed manuscript is `phase37_compress_twogroups_manuscript.md`, SHA-256 `261a9002e7f0394b2ad817b84dbf9a85e8464851c86f9d3ac247048a9fa53751`. Exact bindings of it, its source assets and the finite evidence are in the companion JSON. This approves a specified main-result replacement, not every statement or construction in the four papers. It does not approve a length numerator, numerical compression factor, novelty claim or complete formalization.

## Primary reading and exact target scope

I reopened the cached primary extractions and checked the following passages against the new manuscript and ledger:

| Source version | Passages checked in this review | Contract confirmed |
|---|---|---|
| L032 revised author PDF, header 8 November 2019 | Introduction and Theorem 1.2, physical page 2 | Exact rank/order/type existence for the stated `d,n,k_i` constraints |
| L035 arXiv:1802.08947v2 | Page 2 existence/classification statements and all eight presentations; page 3 marked C-group conventions and rank-three criterion; page 5 Burnside and cyclic-core inputs | Theorems 1.2 and 1.3, all three high-type branches and recognition of the displayed presentations, with `n >= 10` |
| F013 arXiv:2605.20691v1 | Introduction and Theorems 1.1–1.2; canonical group/interface; equations (7)–(9), auxiliary Theorem 4.2 and its relevant argument | Finite nondegenerate two-group quotient/covering statements, distinguished from the explicitly corrected auxiliary kernel assertion |
| F016 arXiv:2512.15511v1 | Abstract/rank convention; FAP definitions; square-map passages; Theorems 5.1, 5.3, 6.1 and 7.1–7.3 with surrounding proofs and amalgam identifications; cited-background references | All six contracted theorems and their clauses, including universal presentation, full group order/doubling, and the source meaning of infinite two-group |

These are selected-section primary readings. I do not claim a new complete reading of every page of all four source papers, a new PDF visual transcription, or a search for later versions. The supplied bound versions are the objects of comparison. The complete new replacement manuscript was read. Earlier reviews of some ingredients are relevant experience, not substitutes for this assembled review.

L035 is treated as a classification of marked string C-groups: its displayed presentations carry the ordered generators. The manuscript proves both that every admissible marking has one of those models and that each bare presentation defines its claimed model. It does not interpret an arbitrary abstract-group isomorphism as preserving an unrelated marking or reversing its ordered type. F016's extension targets retain its standing rank-at-least-three context. Eleven numbered targets and seventeen clause rows are coverage bookkeeping, not a measure of compression.

## Common construction and graded quotient

The kernel-transport proof lifts an intersection element into the correctly marked downstairs intersection, leaving exactly the claimed kernel defect. Boolean deletion identifies the fixed subgroup and the normal-closure kernel, so gives both IP and actual splitting. The compatible product has the required generating sections; deletion preserves its compatibility equation, rather than merely preserving each factor individually.

In edge inflation, the selected pair-power word isolates one cyclic kernel coordinate because every other pair meets it in at most one endpoint and the original pair order is even. The support formula for each parabolic follows in both directions. The unchosen-pair argument correctly excludes the apparent odd-order/reflection problem using the retraction. The order calculation in Corollary 4.1 includes every endpoint and independent cyclic factor once.

I checked the square-lattice normal form and both invariant-lattice families, their deletion relators, and the exact `gamma_3` lattice index. The recognition argument retains the stated elementary Euclidean stabilizer/fixed-point facts and Gaussian integer classification. It does not multiply perpendicular translation orders when their cyclic subgroups overlap. The optional rank-three presentation identification in section 4 uses normal cyclic power subgroups and an actual quotient order comparison.

For the forest quotient, the lower-central graded construction is explicitly retained. All components are over `F_2` because degree one is elementary abelian and generates the Lie ring. The maximal-depth participating edge makes the single crossing bracket a sum of pure brackets on the other side. The derivation argument then spans every degree by the two pure supports. The descending lift uses finite nilpotency, actual subgroup IP and exact counting, without first assuming quotient IP. Finally the crossing commutator lies in a one-generator intersection and is trivial, giving the needed contradiction. The explicit class-two coordinate model proves the order and IP of the canonical quotient.

## The complete high-type classification

I checked all steps in sections 6–7, including those that require an upper bound for a presented group before its order or cyclic-core properties are known.

The cyclic-core bound is used only after the actual C-group and its order are assumed. The even subgroup has index two by its Frattini image. The prescribed power subgroup is characteristic in the cyclic core and inverted by the remaining involution, hence normal in the full group. Its intersections with the two dihedral parabolics give the quotient IP and exact smaller type. This reduces the three branches to orders 16, 64 and 256.

The finite binary laws define the model groups directly. Their right-conjugation automorphisms, central identifications and commuting involution actions preserve all relations; the divisibilities used to preserve `r^(m/2)=z` hold throughout `n >= 10`. The parabolic intersection calculation is made in these actual normal forms. The distinguishing words concern the ordered markings.

The first two classification branches extract exactly one binary relation. In the third, rows III and IV of the finite census are excluded by, respectively, the valuation of a forced rotation power and the exact order of the unit congruent to five modulo eight. The remaining quotient by `<r^4>` is the recognized order-128 square group. Its lifted half-turn subgroup has central commutators of order at most two; conjugation forces precisely the two bits in the final model. This is an all-parameter lifting proof, not extrapolation from the order-256 sample.

For the bare first-branch presentations, centrality and collection give the required bound without importing the conclusion. In the second branch with nonzero twist, I checked `z^a=jz`, `j^2=1`, centrality of `j`, and the relation `(d_0 r)^4=j r^4`; the admissible exponent then forces `j=1`. In the last four presentations, the defining words first make `z` central and `<r^4>` normal. Their quotient is the affine square group modulo `4 Z^2`, of order 128. Thus the order bound is `32m`; the constructed model attains it. No step invokes Lucchini or the target order for the still-unidentified bare presentation.

## Finite completeness evidence

The order-256 catalogue remains a substantial retained input. The algorithm's reduction of the enumeration is complete: an admissible marking has elementary abelianization of dimension three; `r=bc` has a nonzero Frattini image; conjugacy representatives for `r` and centralizer orbits for the inverting involution `c` cover all possibilities. Every possible `a` in the required complement is then tested. The basis condition implies generation, and the exact parabolic intersection plus independence gives rank-three IP. Relation-row exclusivity and exhaustiveness are tested on every surviving marking.

I read the whole GAP census and Appendix A and freshly executed the unchanged program in a disposable directory. The independent wrapper explicitly asserted the final counts, which the executable itself prints: 1,651 eligible catalogue groups, 1,641 active groups, 92 anchored valid triples, row counts `[64,4,16,8]`, and precisely the stated group/row hits. It also checked the source hash before and after execution. GAP 4.15.1 and SmallGroups 1.5.4 were used. The run completed successfully in about 51 seconds wall time; the exact saved log/report record the actual timing.

This is an independent rerun and code/completeness review, not independent implementation of GAP's group arithmetic or reconstruction of the catalogue. I also read the existing exact binary-model checker and the new eight-model report. Those `n=10` checks diagnose the constructions; I did not treat them as an all-parameter proof or claim a fresh model rerun in this audit.

## Prescribed sections and the universal presentation

The bag product embeds each consecutive triple and gives the exact separator order. Its last-factor product proves the face/facet incidence needed for flatness; deletion proves each stated FAP. The independent coordinate kernels in (8.2) and their normality are justified by their projections to the other bags.

The revised universal argument is important. The bare local presentation `P_0` admits all Boolean deletions: every even Coxeter relation and every local lattice relation survives deletion. It therefore has IP even if infinite. The constructed finite quotient guarantees that every local triple and marker has its exact prescribed structure. The ordinary marked C-group/polytope correspondence now constructs the universal object; its existence or presentation is not retained as an unproved version of the target theorem.

The four-marker identity is proved directly. It makes each local third lower-central subgroup normal in the further quotient `Q`, and the quotient by their product is class two. Collection supplies the upper bound, while the constructed compatible product supplies the matching lower bound. This proves F016 5.3 as a statement about the actual universal type group, as well as identifying the finite presentation.

## Retained geometric input and source corrections

Section 9 explicitly retains the alternating assembly theorem and its full-automorphism criterion, and the geometric existence/symmetry/amalgam identifications of the three free extensions. I verified that the stated interfaces match the prior-work interfaces recorded in the inspected F016 source, rather than importing its new two-group conclusions. I did not newly acquire or fully audit all original Monson–Schulte/Schulte–Weiss proofs. These geometric inputs must remain charged as substantial retained background.

Given those inputs, the branched product order, square separator at rank four and exact branch-swap case follow. The normal-form proof for amalgams supplies infinitude and two-primary finite torsion, while finite generation follows from the finite markings. The chiral argument uses only the embedded facet rotation subgroup and its index-two extension, avoiding an unjustified full-facet embedding.

The F013 correction is separate from the main quotient theorem: the explicit class-two path model gives exactly the source-defined Frattini intersection and shows the stated auxiliary kernel order/equality fail. It does not refute the main existence conclusion or every assertion about the auxiliary quotient. The diagonal-square and chiral proof repairs are also explicit. Historical exceptions, power-polytope constructions, open questions, absolute flag minima and N009 are not silently counted.

## Review changes and conclusion

The author corrected two scope points during review: Corollary 5.4 now explicitly says finite nondegenerate **two-group** string C-group, and the section 7 extension applications explicitly retain F016's standing rank `d >= 3`. I reviewed the author's new Boolean-deletion proof for the bare universal local presentation and approve it; it removes a previously retained existence/presentation interface. Final hashes bind these changes.

The resulting text supports the declared corrected main-result contract, with complete written adapters and the charged finite census. It shares substantial construction and quotient work, but the cyclic classification, catalogue calculation and imported geometry remain real costs. Any four-paper length comparison is a separate measurement task; no ratio or source-body numerator is certified here. This is internal mathematical review, not external peer review or a full Lean certificate.

The reviewer contributed to earlier edge-inflation/square-lattice investigations and reviewed several earlier constituent notes. This is a fresh full review and census rerun of the assembled artifact, not independent discovery of every underlying ingredient. The reviewer did not edit or author this assembled manuscript.
