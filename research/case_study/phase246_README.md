# Locally faithful finite covers

This is a private author package for independent review. Its six-page paper gives an exact abelian-kernel construction and obstruction in every finite rank at least three, assuming that both marked end groups of the finite base group are C-groups. It also classifies the locally faithful abelian-kernel covers of the Tomotope. It does **not** solve the unrestricted finite minimal-cover question.

Read `phase246_locally_faithful_covers.md` or its PDF first. The main statements are Proposition 2.1 (completion kernel), Theorems 3.1–3.2 (exact abelian criteria), Corollary 3.3 (prime-kernel obstruction), Theorem 4.1 (conditional finite multiplicity), and Proposition 5.1 (Tomotope classification).

The source and proof boundaries are recorded in `phase246_source_ledger.json` and `phase246_scope.json`. In particular, the earlier Tomotope covers and its infinite minimal-cover multiplicity remain attributed to Monson–Pellicer–Williams. No whole-source replacement or new principal/conjecture count is claimed.

## Replay

Use a fresh output directory and explicit local executable/package paths:

```sh
python3 -B -O phase246_check.py \
  --out /path/to/FRESH_DIRECTORY \
  --gap /path/to/gap \
  --lean /path/to/lean-4.32.2 \
  --packages /path/to/pinned/.lake/packages
```

The portable driver rejects an existing output path, including a dangling symlink. It requires Python's standard library, GAP and the retained Lean dependency revisions in `formal/dependency_manifest.json`. It verifies those package revisions and their clean tracked worktrees. No network is needed.

The driver regenerates all cell matrices, performs exact finite-field elimination, replays the independent integer reduction, constructs the actual voltage permutations, verifies their group and all 256 parabolic intersections in GAP, checks the normal kernel-line census, and compiles three Lean declarations. It also rejects (i) killing the actual defect by an additional relation, (ii) deleting the voltage data, and (iii) a false kernel order. A two-element semantic example records why end injectivity is necessary in the formal criterion.

The expected Tomotope result is: base order 18432; kernel `C2 x C2`; locally faithful cover order 73728; exactly one normal kernel line; unique minimal abelian quotient order 36864. The latter agrees, by the complete classification, with the cover already proved in Proposition 4.5 of the primary paper.

## Required retained inputs

The retained bindings in `phase246_manifest.json` specify exact bytes. The three finite inputs are `phase224_small_models.json` (only its first diagnostic), `phase109_cover_families_generalization_model.json`, and `phase211_literal_Tomotope_model.json`. The two smaller groups are diagnostic examples in this packet; no new source-to-polytope bridge is asserted for them.

The independent integral calculation is `phase245_tomotope_integral.py`, together with `phase245_tomotope_complex.json` and the separately frozen `phase245_integer_manifest.json`. The fresh complex is compared with that supplied matrix before replay. The phase245 note and operation certificate are retained for audit. That review establishes the integer lattice computation; a separate review is still required for the full phase246 geometric interpretation and source application.

The literal primary-to-Tomotope model bridge is retained from phase211/218. The complete primary PDF, Monson–Schulte's finite-cover PDF, and the earlier arbitrary-cover proof/review are research dependencies, not reproduced source texts. Exact source versions and locators are in the ledger.

## Formal and computational limits

`phase246_formal/LocallyFaithfulIntersection.lean` proves a subgroup-image intersection equivalence for actual quotient homomorphisms, faithfulness of an end group under a quotient over the base, and the direction of kernel containment. Its three declarations use only the standard Lean axioms listed in the replay. The first equivalence requires injectivity on one end; the written C-group application has both ends embedded.

Neither Bass–Serre theory nor cellular homology nor the integer and GAP computations are translated into Lean here. Those parts are complete written arguments and exact external computations. The generated permutations are certified directly; their equality with the universal elementary abelian quotient then follows from the written universal property and the exact order.

No historical novelty claim, numerical compression rate or unconditional finite multiplicity claim is made.
