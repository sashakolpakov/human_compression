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

## The method

The initial case study concerns finite groups, highly symmetric polytopes,
incidence geometries and related graphs. Three recurring ideas do much of
the work:

1. **Marked group torsors.** Represent subgroups by invariant partitions of a
   common torsor. Hadamard products compute intersections; matrix products
   count factorizations; a coset Helly condition detects flag transitivity.
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

## Results in this snapshot

These are internally reviewed research drafts. Proposed new resolutions have
not received external peer review, and publication priority remains unverified.
The proposed PSL₄ resolution has a separate
[dated literature audit](research/case_study/phase8_psl4_status_audit.md).

| Result | What is established here | Evidence |
|---|---|---|
| Fixed-excess cyclic extensions | A classification procedure using bounded quotient data, fixed-size affine systems, a free change-of-section action, and exact cyclic intersection tests | [General theorem](research/case_study/phase3_bounded_families.md); exact modular solver |
| Eight high-type families of regular rank-three polytopes | Both principal existence and classification theorems of the source paper rederived | [Proof](research/case_study/phase3_classification.md); eight model checks; exhaustive order-256 seed census |
| Suzuki graph pentagons | Proposed uniform proof of exactly \(q-1\) pentagons per edge | [Proof](research/case_study/suzuki_cycle_proof.md); Lean checks the complete matrix-membership equivalence; independent coset graph |
| Remaining PSL₂ chiral construction | Proposed proofs of the two field/intersection conjectures and their classification consequence | [Proof chain](research/case_study/psl2_chiral_corollary.md); exact finite-field witnesses; partial Lean certificates |
| Commuting involutions | All four principal results of one counting paper rederived, followed by an all-rank extension | [Reduction](research/case_study/commuting_pairs_compression.md); orbit formulas and exact exceptional-case checks |
| Odd-characteristic PSL₄ rank | Complete proposed proof of maximum rank four for every odd q; a broader theorem forces a bilinear form for irreducible four-dimensional projective string actions of rank at least five | [Rank-six proof and dependency map](research/case_study/phase8_psl4_rank6.md); independent internal reviews, exact symbolic checks and two partial Lean components. Published rank-four existence is retained; priority remains unverified |
| Hypertope order bound | Uniform classes now include metacyclic derived subgroups; exhaustive auxiliary certificate verifies the conjecture through group order \(2^{12}\) | [Metacyclic theorem and finite extension](research/case_study/phase7_cyclic_tpp.md); independent proof review and exact checks. The full conjecture remains unresolved |
| A 2003 spread-space question | Proposed proof that locally primitive spreads in the one-dimensional affine semilinear setting are Desarguesian | [Semilinear descent](research/case_study/phase4_old_problem_audit.md); exact subspace and stabilizer checks |
| A 2004 geometric intersection algorithm | Exact flag-constrained covering criterion for shadow-IP and its residue variants; rank-two characterization rederived | [Proof and scope](research/case_study/phase4_shadow_ip.md); exhaustive small-structure comparisons |
| A 2002 sporadic-group classification | Complete principal \(J_2\) census independently reproduced: 8 rank-two, 19 rank-three, 3 rank-four geometries and no higher ranks | [Arbitrary-Borel reduction](research/case_study/phase5_j2_theory.md); exhausted augmentation and independent witness recognition, conditional on the retained subgroup catalogue |
| Three further sporadic censuses | One generalized engine gives J₁: 22/8/2; M₁₁: 6/18/12/4; M₁₂: 13/21/20/1 in successive ranks from two, with no higher ranks | [Common proof and source scope](research/case_study/phase6_sporadic_theory.md); all 226 Borel anchors exhausted and 127 witnesses independently checked. TomLib completeness retained; historical M₁₂ comparisons remain qualified |
| Two more classifications with the same engine | M₂₂: 7/25/16/9; M₂₃: 4/13/21/10, with no ranks above five, under the sources' local two-transitivity condition | [Common census](research/case_study/phase7_sporadic_theory.md); 360 anchors exhausted, 105 witnesses independently recognized; primary tables and archived lists match exactly. Original article bodies remain unavailable |
| Dihedral geometries in all ranks | Three arithmetic patterns, exact class counts and automatic geometric properties | [Uniform proof](research/case_study/phase5_dihedral_classification.md); independent subgroup/coset checks. Published all-rank theorem matched through a primary restatement; original full-paper comparison remains |
| Symmetric-group geometries, 1998–2005 | One tree-cut argument recovers primitivity tests, tree correspondence and the path criterion for geometric shadow-IP | [Common derivation](research/case_study/phase5_tree_cuts.md); retained foundational classification, finite checks and a Lean Boolean-shadow witness theorem |
| All truncations of the tree family | Weighted contraction gives exact RWPRI, local two-transitivity, rank-two and full intersection criteria | [Weighted-tree theorem](research/case_study/phase6_weighted_tree.md); exact finite audits and Lean witnesses within retained ranks. The original 2003 full-paper comparison remains |
| A missing geometry in a 1999 classification | Exact matrices in Sz(2¹⁵) give a firm, residually connected, flag-transitive RWPRI geometry absent from the asserted exhaustive list | [Counterexample and rank-four extension](research/case_study/phase6_suzuki_realization.md); exact intersections and internal independent review; Lean proves the abstract Helly implication. Corrected completeness and publication priority remain |
| Suzuki geometries in every rank | Field descent and cyclic coordinates give an unconditional all-rank family, recover the full parameterized existence assertions of two older constructions, and complete the earlier rank-four geometry proof | [All-rank derivation](research/case_study/phase7_suzuki_descent.md); [full two-family argument](research/case_study/phase7_suzuki_torus_families.md); exact checks and [Lean attachment lemma](research/case_study/formal/CosetCoordinates.scope.md). Classical descent and subgroup structure remain explicit inputs |
| Two further older construction families | A sharp pure-subfield rank criterion recovers Construction 11 and its omitted repeated-prime boundary; an exact scalar-subspace overgroup lattice rules out RWPRI for every intended Construction 10 intersection pattern | [Uniform proof and literal source scope](research/case_study/phase8_suzuki_subfields.md); independent mathematical/source review and exact matrix checks. Arbitrary other intersections and a full replacement classification remain |
| The printed Suzuki realization questions | Uniform decisions for every displayed parameter shape | [Per-shape decision table](research/case_study/phase5_suzuki_higher.md#e-exact-scope-of-the-proposed-resolution). Its former assumption that the source list was exhaustive is superseded by the counterexample above |

Further notes cover affine lattice families, Hermitian-unital connectivity,
normalizer-orbit classifications, incidence constructions and a corrected
Wenger graph cycle count. Exact retained assumptions are listed in the notes.

The common census theorem now supports six finite-group censuses with 262
independently recognized representatives under their recorded axioms. This
measures verified coverage; it is not a numerical proof-compression ratio.

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

[Measurement](MEASUREMENT.md) defines how to estimate compression over equal
theorem content and account for shared dependencies. Verified solutions of
previously open problems receive a separate novelty assessment; “∞” is
reserved as an explicitly qualitative marker. No corpus ratio or infinity
marker is assigned yet: proposed resolutions still need priority verification.

The starting bibliography was seeded from Dimitri Leemans's publication
catalogue and expanded through coauthored papers and relevant followups.
It currently indexes 128 mathematical catalogue entries, 17 followups and
seven additional papers across the collaborator network;
73 catalogue full texts were searched or read in part, 46 have abstract-level
coverage and nine have metadata/access records only. That is neither complete
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

Fourteen Lean modules certify specified components, with no `sorry` in the checked
sources. They do not constitute an end-to-end formalization of every theorem.
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
