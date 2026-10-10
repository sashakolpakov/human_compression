# Admission of formal coset certificates through rank three

10 October 2026. The [reader](../COSET_CERTIFICATES.md) describes the new formal verification supporting the already admitted label-eleven obstruction. The [author manuscript](../research/case_study/phase219_coset_certificates.md), [scope](../research/case_study/phase219_scope.md), and [independent semantic review](../research/case_study/phase226_coset_review.md) give the complete record.

## Mathematical and formal review

The root read all 409 lines of the inference kernel, all concrete dihedral examples, both certificate generators and the replay runner. The rank-three source was checked at its literal-relator interface, inference-term generation and complete row-array assembly. It contains 3,072 edge proofs. Lean checks these individually, so neither the external table nor the Python generator supplies a logical premise.

The core constructs actual right cosets for arbitrary subgroups and proves right multiplication well defined. Each inference constructor is sound. Tree edges require literal representative-word identities; relator deductions require the exact relator and already proved forward and reverse paths. Induction on these proofs rules out circular transition assumptions. Completeness yields a surjection onto actual cosets and proves finiteness. The presented-group interface uses exactly the normal closure of generator squares and the listed relators.

This addresses the distinction between a finite quotient action and an upper bound for the universal group. A quotient action alone would not suffice. The concrete rank-two examples prove the dihedral order bound 22. The rank-three result proves finite facet index at most 1,024 in the exact source presentation. The comparison of the emitted list with the three pair relators and all ten triple-power relators is itself kernel-checked.

The independent review reads the complete inference core, generators and interfaces and replays the deduction records separately. Its frozen manifest has SHA256 `cf954b578659b0db48cf08b6afb25c883e2fd4b0394a8549559d9160adbef6ff`. A fresh public execution of its separate checker passed all 3,072 deductions and rejected three corrupted certificates. It does not claim that this finite replay proves the generic theorem; Lean supplies that proof.

## Fresh public execution

The 24 author artifacts and manifest were copied unchanged. The author manifest has SHA256 `0e97c6931e3c0ae67ef9a33c429d1d017a43cc193f10e65101e39b05dd6d8469`. A fresh public replay with Lean 4.32.2 checks all nine dependency revisions and tracked-source cleanliness, builds absent required mathlib modules in a local output cache, reproduces both generated sources byte for byte, and compiles all three formal files.

All 25 selected axiom reports contain only `propext`, `Classical.choice`, and `Quot.sound`. Four rejection examples are proved by ordinary Lean reduction. Two mutations removing the tree-word or relator-membership check fail to compile. No native-evaluation axiom, proof hole, GAP computation or C++ computation is used by this replay. Existing cached dependency objects, the compiler and the Lean kernel remain trusted execution components.

The [fresh report](../research/case_study/phase225_public_replay/report.json) binds source hashes and raw outputs. The three canonical formal files are byte-identical to the frozen author sources and have their own compiler records and scope documents.

## Attribution and accounting

The deduction method is classical coset enumeration. The source presentation belongs to Li–Zhang; Mathlib supplies the group, quotient and cardinality infrastructure. The formal inference implementation, its soundness proof and the concrete certificates are the contribution of this package. The generated proof text and its generators are retained in the publication and must be included in any future cost measurement.

The concrete dihedral-to-facet map needed to compose the rank-three group-order bound 22,528 has not been formalized. The rank-four and rank-five coset computations, concrete large matrix-group orders and memberships, and the complete F014 refutation remain outside this Lean claim. The original preprint-version and historical-priority qualifications remain unchanged. There are no new solved questions or source-compression credits. The catalogue remains at eleven questions, ten recorded complete answers and one ambiguous formulation; principal-source coverage remains 20. The canonical scoped Lean file count rises from 78 to 81. The [export record](../research/case_study/phase225_export.json) preserves the admitted bytes.
