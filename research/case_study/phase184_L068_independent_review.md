# Independent review of the Livingstone-graph application

10 October 2026. Reviewed author manifest: `phase179_manifest.json`, SHA256 `6e0a642f79bb1185d66645d259a46d7512b342a0af1c970951e55c9719c7cd36`.

**Verdict: accept the explicitly qualified two-construction contract.** The literal second construction P is recovered, including Proposition 5.1, Theorem 5.1, its diagram and flag-stabilizer lattice. The literal first construction Q is not a geometry under its printed binary incidence relation. The proposed corrected construction is a regular polytope of the intended type and has the intended stabilizer lattice. These are distinct conclusions. The literal false theorem must not be counted as an unchanged corollary.

There is no new whole-source principal credit, open-conjecture solution, end-to-end Lean verification, or compression-ratio claim in this verdict. This is a substantive source-component admission with an explicit corrected principal construction; it is not merely a rerun of abstract J1 existence checks.

## 1. Reading and source identity

I read the full 22-page primary text of Hartley–Hubard–Leemans, *Regular 4-polytopes from the Livingstone graph of Janko's first group*, J. Algebraic Combinatorics 35 (2012), 193–214, DOI 10.1007/s10801-011-0300-x. The exact PDF SHA256 is `e40b3ee73dec3754248a7c9b659fc3015f8ee59c2b98ce46141baae8fe825ad9`. I independently viewed physical pages 10,13,19,20,21,22, checking the disputed auxiliary statement, both face definitions, the two stabilizer lattices, the two main diagrams and the status of the full subgroup lattice as background. The preceding bounded review of the first definition and its rank-two count is superseded by this full mathematical review.

I read the entire new manuscript, all 303 lines of the new GAP program, the portable driver, controls and complete Lean source. I also read the retained Module C finite program and the relevant C recognition and J1 application sections. The full retained C/U manuscripts are dependencies, not newly rereviewed manuscripts in this phase. All six pages of the final application PDF were visually inspected. The render is legible, including the neighbour-count table and displayed counterexample.

All author-manifest file, retained-input and primary-input bindings were verified. All 17 source-ledger rows and 24 proof-span bindings were checked against the final manuscript. The frozen author files were not changed.

## 2. The source-to-coset argument

The reconstruction theorem is correct. A transitive G-set with selected point x and stabilizer H is its coset action. A G-invariant binary relation containing the selected base pair contains its diagonal orbit. If the complete neighbourhood of the first base point equals the orbit of the second under H, translating a related pair back to that neighbourhood proves the converse. Thus the reduction identifies every binary relation and hence every flag and residue. The finite-cardinality variant is valid because the orbit is already contained in the complete neighbour set.

The application actually establishes these hypotheses. It constructs the finite graph objects before looking for the marked base chamber, checks transitivity on each entire face family, computes each full object stabilizer and compares it with the corresponding marked parabolic, and enumerates every member of the appropriate target type when computing a neighbourhood. It does not substitute a chosen flag orbit for a complete literal relation.

The identification of the named degree-266 action and its unique valency-11 orbital graph with the classical Livingstone graph is explicitly retained. Within that model the program checks the complete intersection array for every ordered vertex pair. The pentagon enumeration is exhaustive: the least vertex and the ordered adjacent vertices remove the starting-point and orientation ambiguity, while the girth excludes degenerate cycles. Actual group orbits determine the two colours.

The Petersen-family converse is also justified. In a Petersen graph, a chosen pentagon has five spokes to its complementary pentagon, with the complementary vertices in the pentagram order. Once the first outside neighbour is fixed, girth five forces each subsequent outside vertex as a common neighbour. The nine possible first choices therefore exhaust all extensions. Checking one representative of each of the two pentagon orbits, and proving that every extension obtained lies in the invariant constructed family, establishes completeness for all induced Petersen graphs. This is the point needed to justify the face universe; a count of 1463 constructed sets alone would not suffice.

The local block family is complete because the relevant A5 subgroups have prime index 11 in the vertex stabilizer and hence are maximal. The complete maximal-class calculation supplies its two classes, and their actual neighbour orbit patterns distinguish the required class. The pair and triple block checks recover the local design and Proposition 3.4. The six choices at a base vertex-block triple verify Proposition 3.5; transitivity transports the conclusion to every triple.

## 3. Literal predicates and the correction

The independent program `phase184_source_predicate_review.g` transcribes all twelve literal relations directly from the two printed definitions. Its opposite-edge condition uses graph distance two between every endpoint pair, a formulation different from the author's nonadjacency test. The relation sets agree with the author's implementation on each complete base neighbourhood. This comparison retains the author's graph and object construction, so it is an independent semantic check rather than a second implementation of all finite group algorithms.

The first definition's type-2/type-3 clause on printed p.205 uses only the edge, the chosen endpoint and the six-block. It omits the white and orange pentagons of the type-2 face. Since every point of the local 2-(11,6,3) design lies in six blocks, it gives six choices at each endpoint, hence twelve neighbours. The later p.208 argument instead uses the whole quadruple to determine a block. There is no unstated common-flag condition in the preceding definition of the face families that repairs the displayed relation.

For the selected type-2 face, I checked all twelve literal neighbours. Their numbers of literal type-1 extensions are

\[
0,0,0,0,0,0,0,0,0,0,5,5.
\]

Thus every one of the ten extra pair-flags fails to extend even to a type-1 face, while the two retained neighbours each have five such extensions. The author's displayed witness is one of these failures. This establishes a defect in the literal geometry axiom, rather than just a discrepancy between an orbit count and a printed group order.

I independently checked the proposed repair by a different definition. For each of the twelve neighbours, intersect its vertex-block stabilizer with the pointwise edge stabilizer. This subgroup has order ten. Its orbit partition on the associated Petersen graph equals the two displayed pentagons exactly for the same two neighbours selected by the graph correspondence in equation (3.2). The graph-based compatibility therefore agrees with the induced-quadruple construction, without arbitrarily assigning a pentagon colour to one of the two local five-sets.

The other source defect is in Proposition 3.3 on printed p.202. The common distance-two set has 40 vertices, not ten. The manuscript's double-counting proof using the intersection array is correct, and the finite program agrees. Adding the white-pentagon condition selects the intended ten-set. That condition is already present in the source paragraph preceding the proposition, and is correctly attributed there. This auxiliary wording defect is separate from the missing principal incidence clause.

## 4. Accepted mathematical coverage

| Source item | Independent outcome |
|---|---|
| Prior classification of exactly two rank-four regular J1 polytopes | Retained background; not reproved by constructing two examples |
| Theorem 2.1, attributed in the source to Aschbacher | Replaced as a proof dependency by retained U/C recognition; no new attribution |
| Classical Livingstone graph identification | Retained; finite intersection-array checks accepted |
| Complete pentagon families | Recovered in the named graph model |
| Propositions 3.1 and 3.2 | Recovered, using the checked completeness of the Petersen family |
| Proposition 3.3 | Literal ten-set wording refuted; stated corrected form recovered |
| Local design and two A5 classes | Exact reconstruction accepted, with classical origin retained |
| Propositions 3.4 and 3.5 | Recovered |
| Six defining relations of Q | Five unchanged; one explicitly refuted and repaired |
| Proposition 4.1 | Full statement recovered for the corrected structure only |
| Proposition 4.2 and Figure 9 | Recovered for the corrected structure only |
| Theorem 4.1 and its diagram | Literal theorem rejected; corrected theorem accepted |
| Six defining relations of P | All recovered literally |
| Proposition 5.1 and Figure 10 | Recovered literally |
| Theorem 5.1 and its diagram | Recovered literally |
| Figure 11, full J1 subgroup lattice | Retained background, not rederived or newly credited |

The retained C program verifies both markings' involution orders, generation, all subgroup-meet identities, typed coset Helly equalities, trivial chamber stabilizer and order-two panel stabilizers. The program's pair orders are the required string types. The new bridge identifies the entire source structures with these marked geometries, so the regularity and residue conclusions follow from the already retained U/C recognition results.

The two printed stabilizer lattices are also recovered under the stated scope. The new program prints all sixteen intersections; these agree with the primary figures, including S3 versus C2×S3 at the differing type-0/type-3 pair. The complete-group argument is sound: a type-preserving automorphism fixing a chamber fixes every adjacent chamber by thinness, hence every chamber by connectedness, and then every face. The regular J1 subgroup already reaches the resulting upper bound. No converse assertion that geometry automorphisms must arise from graph automorphisms is required.

This review does not assert that every incidental sentence or every classical subgroup assertion printed in the source has been separately rederived. The source ledger accurately distinguishes the needed finite components, the two main constructions and the retained background.

## 5. Fresh verification and non-vacuity

The portable author driver was run from fresh output `/private/tmp/phase184_independent_replay` with Python optimization enabled. The retained C certificate, new source-object computation and fresh Lean compilation passed. Their three logs are byte-identical to the frozen author's corresponding logs. Observed times were approximately 1.656,7.254 and 5.144 seconds, respectively; these are run observations, not performance bounds.

All three author-designed mathematical controls rejected: omitting the repair, changing P's white-pentagon facet condition to orange, and changing Q's required block overlap from three to two. Two additional reviewer-designed controls run after the complete unchanged author calculation. Replacing P's facet colour is rejected by the independently transcribed source relation; deleting the repair is rejected by the independent D10 orbit criterion. GAP may return process status zero after a mathematical `Error` in batch mode, so these controls require the actual rejection message and absence of the review completion marker.

The positive independent semantic run checks all twelve source relation sets, all twelve Q pair-neighbours, their extension counts, and the alternative algebraic repair. The final successful run has no syntax warnings. The earlier exploratory reviewer run with an unbound-global syntax warning is not the frozen accepted replay.

The Lean component proves three generic declarations. Its checked axioms are limited to `propext`, `Classical.choice` and `Quot.sound` as reported. There is no `sorry`, new axiom or native-evaluation certificate. It proves reconstruction of an invariant relation from its base neighbourhood and the finite-cardinality implication. It does not formally construct coset quotient sets or verify the J1 data, the source predicates, the GAP computations or either complete polytope theorem.

The fresh compiler is Lean 4.32.2; the runner checks pinned dependency revisions and tracked source cleanliness and reads cached dependency objects through a private overlay. Those dependency objects remain trusted. GAP 4.15.1, TomLib 1.2.11 and the named J1 data hash are recorded in the replay. Exact group algorithms, named data, the classical graph identification, and retained U/C mathematical results remain explicit dependencies.

## 6. Attribution and cost

The intended geometric constructions, their ingredients and results are attributed to Hartley–Hubard–Leemans. Propositions 3.1–3.3 are already attributed by that source to the classical graph literature. The local design, named J1 representation, subgroup structure and earlier abstract-polytope classification are not claimed as new ideas. The equivariant reconstruction is a standard argument, organized into a reusable verification interface. The new work consists of its source-specific certificate bridge and the explicit audit and repair. No historical priority for a correction is asserted.

The manifest's required inventory is exact: 44,524 new bytes, comprising manuscript, mathematical GAP program, real driver and Lean file; 135,006 retained bytes for the full U/C manuscripts and retained C finite program; total 179,530 uncompressed UTF-8 bytes under that file-level allocation. Review evidence is additional support. The six-page rendered application excludes the retained manuscripts and programs and therefore is not a six-page total replacement. The source's 22 printed pages are bibliographic metadata, not a matched compression numerator. No ratio is assigned.

The admission supported by this review is **one unchanged principal construction and one corrected principal construction**, together with the precisely listed finite components. It supports no increase in the count of manuscripts whose complete literal principal statements have all been recovered unchanged. Any living-registry update should preserve this distinction rather than treating the correction as ordinary unchanged compression.
