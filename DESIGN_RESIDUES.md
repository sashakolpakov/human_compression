# Design constructions: residues, chamber actions and classification

The corrected main results of L092 are now recovered: its rank-three
applications, complete higher-rank Steiner classification and rank-six
Mathieu construction. The source is D. Leemans, *A Generalization of a
Construction due to Van Nypelseer*, Beiträge zur Algebra und Geometrie
46 (2005), 561–574. The construction and its predecessors retain their
attribution. This is reviewed material for the new topic papers, with
no measured compression ratio yet.

## The common arguments

The [residue theorem](research/case_study/phase182_steiner_residue_recursion.md)
reduces connectivity in every rank to constructions on derived linear
spaces. Its proof identifies ordinary residues with Boolean joins and
handles the exceptional types explicitly. The
[chamber theorem](research/case_study/phase186_steiner_fiber_and_intersections.md)
identifies every chamber with an ordered tuple and one alternative block.
Chamber transitivity is therefore equivalent to transitivity on tuples
and transitivity of one tuple stabilizer on its block fiber. The same
manuscript proves the rank-two intersection property uniformly.

The [projective and affine bases](research/case_study/phase186_linear_space_bases.md),
[explicit Witt models](research/case_study/phase186_witt_group_identifications.md)
and previously reviewed deleted-line and subline arguments supply the
applications. The [classification proof](research/case_study/phase186_higher_rank_classification.md)
then obtains the final list without using the false intermediate assertions.

| Source result | What is recovered | Qualifications |
|---|---|---|
| Theorem 1 | The linear-space, dual-linear-space and (4,3,4) alternatives; the exact chamber-transitivity condition | Retains the hypothesis of a thick connected partial linear space. Chambers correspond to three-edge paths; the conventional four-edge wording is corrected. |
| Theorems 3–4 | Projective and affine constructions, all residue types, diagram parameters and stated actions | Includes the projective order-two case and the exceptional affine semilinear action. |
| Theorem 5 | The iterated point-residue construction is not flag-transitive | An intrinsic incidence invariant supplies the obstruction. |
| Theorem 6 | For the deleted-line iteration with q>3: firmness and (IP)₂ always, connectivity exactly when q>4, and flag transitivity exactly when q=4 or 8 | Their conjunction selects **q=8**, correcting the printed q=4. |
| Theorems 7–8 | The higher-dimensional projective and affine constructions are not residually connected | A plane preserved by every residue path gives the exact components. |
| Theorem 9 | The equivariant chamber bijection and exact stabilizer criterion | Connectivity and transitivity are proved separately. |
| Theorem 11 | The complete higher-rank list: the binary affine design in dimension three, the GF(4)-subline design on PG(1,16), and the three large Witt designs | Retains the two substantial classifications already cited by the source as Theorems 2 and 10. |
| Rank-six M24 construction and Figure 3 | Geometry, firmness, connectivity, (IP)₂, transitivity, object counts and actual stabilizer structures; the two rank-five residues are nonisomorphic | Object maps identifying these residues with Pasini's named Γ23(4) and Γ8(4) remain missing. |

The [retained-input statement](research/case_study/phase186_primary_classification_bindings.md)
names Buekenhout–Dehaye–Leemans and Kantor and gives their exact hypotheses.
Their classification proofs are borrowed, not compressed by the elementary
residue theorem. The
[independent review](research/case_study/phase199_L092_review.md) and
[root admission](research/case_study/phase208_root_admission.md) give the
complete coverage boundary. This does not recover every auxiliary
assertion of the source.

## Corrections and the separate conjecture answer

The [deleted-line theorem](research/case_study/phase182_deleted_line_independent_theorem.md)
and [subline theorem](research/case_study/phase182_inversive_residues.md)
correct the earlier parameter restrictions. The
[cyclic biplane](research/case_study/phase186_biplane_delta_correction.md)
refutes the unrestricted neighbor-connectivity implication in Lemma 3(1).
The [path-count example](research/case_study/phase199_path_length_correction.md)
distinguishes the source's four-vertex chamber configuration from four
edges. The [Hermitian diameter proof](research/case_study/phase186_hermitian_residue_diameters.md)
and [numerical audit](research/case_study/phase186_hermitian_figure_audit.md)
correct the specified Figure 2 entries.

The existing [Hermitian-unital proof](research/case_study/hermitian_unital_proof.md)
answers the source's Conjecture 1 for every prime power q>2. It remains
visible in the [question catalogue](CONJECTURE_RESULTS.md) and is counted
once, separately from recovery of the previously published main results.
This admission adds no conjecture answer or historical-priority claim.

## Computation and Lean

Fresh GAP calculations construct all five native Witt designs, compute
full automorphism groups and verify explicit stabilizer maps. Independent
Python arithmetic rebuilds the incidence data. An independent projective
coordinate program checks the literal unital residues at q=3,4,5.

Lean verifies [three explicit maps to PG(2,4)](research/case_study/formal/WittDerivedPlanes.scope.md),
the [literal biplane counterexample](research/case_study/formal/CyclicBiplaneDelta.scope.md)
and the retained [disconnected F4 residue](research/case_study/formal/DeletedLineFourResidue.lean).
The original Witt-to-derived-table identification remains in GAP/Python;
the uniform proofs and full finite-group completeness remain outside Lean.

With the pinned tools and new output directories:

```sh
python3 -B -O research/case_study/phase208_public_check.py --output-dir /tmp/NEW-Steiner --packages PACKAGES --lean LEAN --gap GAP
python3 -B -O research/case_study/phase185_corrections_check.py --output-dir /tmp/NEW-design-residues --packages PACKAGES --lean LEAN --gap GAP
```

These commands require no private primary PDFs. The
[export record](research/case_study/phase208_export.json) preserves frozen
proofs and reviews separately from fresh execution evidence.
