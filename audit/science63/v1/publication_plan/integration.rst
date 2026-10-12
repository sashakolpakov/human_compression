Root integration of L122
=======================

Baseline: committed science62 575f7e7d61310c2f7fe153e2f4dc4804bb6d8798.
This proposal has not changed the public repository.

1. Install exact proposal exports and manifest at audit/science63/v1/publication_plan,
   the 73 payloads in copy_plan.json, and the 24 wrapper routes. Preserve all
   accepted author and root-review bytes, including historical pending labels.
2. Add snapshot_additions.py's two functions before main. Preserve all 151 old
   non-main ASTs. Main's current check_previous_science62()/check_science62()
   calls become the science63 pair. Update the main-only display to 63 reviewed,
   53 measured, ten unmeasured, 42 mathematical targets and one editorial.
   The new historical wrapper tests science62 and its entire saved-pointer chain.
3. Preserve the measured catalogue/build routes, all fractions and overview v19.
   The four standalone native papers are appended only to the existing separate
   corrected-unmeasured catalogue. No new comparison topic is created.
4. Root alone supplies audit/science63/v1/root_integration.json, status
   ROOT_ACCEPTED_SCIENCE63_PUBLICATION, source_ids [L122], measurements_added 0,
   new_question_credit 0. Bind every exact path in reports/gate_controls.json,
   including the actual verifier, proposal manifest and complete native files.
   No broad path exception or fabricated root approval is needed.
5. Run the full snapshot, then commit and push. Record local acceptance separately
   from transport results. Any altered integration file requires an explicit
   root delta and rebinding; the proposal and science freezes remain immutable.

Reproduce the private/public-only checks with global Python containing pypdf::

  python -B -O stage.py --study /Users/sasha/medusa/research/leemans --repo /Users/sasha/medusa/math_compression --out FRESH_STAGE
  python -B -O check.py --repo FRESH_STAGE --out FRESH_ROUTES.json
  python -B -O check_gate_controls.py --repo FRESH_STAGE --out FRESH_GATE.json
  python -B -O replay.py --repo FRESH_STAGE --out FRESH_NATIVE --render
  python -B -O FRESH_STAGE/scripts/check_science63_history.py --repo FRESH_STAGE

The public guard requires root integration acceptance; the private checker does
not. The native adapter restores the exact logical directory layout, including
nested component manifests; JSON source-route strings refer to that layout,
while the public guide/catalogue supplies canonical native paths. It checks
accepted positive GAP receipts and freshly executes the whole small pure-integer
counterexample; it does not rerun the positive large finite examples or claim
new source/GAP/Lean acceptance. All 4+4+3+2 page texts rebuild exactly.
