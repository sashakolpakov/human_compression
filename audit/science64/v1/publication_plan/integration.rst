Root integration of L015
=======================

Baseline: committed and published science63
41983bd1827137c629d1aa00c6bb79ea9e66ba95. Public files remain untouched here.

1. Install the exact proposal exports and manifest at
   audit/science64/v1/publication_plan, all 26 payloads in copy_plan.json,
   and the 24 wrapper routes. Preserve all frozen author/root-review bytes,
   including the author's historical pending labels.
2. Add snapshot_additions.py's two functions before main. Preserve all 153
   existing non-main ASTs. Replace main's current science63 pair with the
   science64 pair. Update the main-only display to 64 reviewed, 53 measured,
   eleven unmeasured, 41 remaining mathematical targets and one editorial.
   The historical wrapper tests science63 and its full saved-pointer chain.
3. Preserve the measured catalogue/build routes, all factors and overview v19.
   The three standalone native papers are appended only to the separate
   corrected-unmeasured catalogue. No new comparison topic is created.
4. Root alone writes audit/science64/v1/root_integration.json, status
   ROOT_ACCEPTED_SCIENCE64_PUBLICATION, source_ids [L015], measurements_added 0,
   new_question_credit 0. Bind every exact path in reports/gate_controls.json,
   including the actual verifier, proposal manifest and six native files.
   Do not replace these exact paths with a whole-prefix allowance.
5. Run the full snapshot, then commit and push. Distinguish local acceptance
   from actual transport. Any altered integration file requires an explicit
   root delta/rebinding; accepted science and proposal freezes remain immutable.

Private/public-route checks, with global Python containing pypdf::

  python -B -O stage.py --study /Users/sasha/medusa/research/leemans --repo /Users/sasha/medusa/math_compression --out FRESH_STAGE
  python -B -O check.py --repo FRESH_STAGE --out FRESH_ROUTES.json
  python -B -O check_gate_controls.py --repo FRESH_STAGE --out FRESH_GATE.json
  python -B -O replay.py --repo FRESH_STAGE --out FRESH_NATIVE --render --optional
  python -B -O FRESH_STAGE/scripts/check_science64_history.py --repo FRESH_STAGE

The public entry guard requires root integration acceptance; the private route
checker does not. Native replay restores exact logical packet paths and checks
all three full native papers. Optional validation remains optional evidence,
not a proof premise or software-inclusive factor. There is no new source
extraction, GAP census or Lean run. Current admission supersedes only the
frozen author's provisional status, not its scientific contents or boundaries.

Use this v2 proposal instead of the uninstalled predecessor c44596a4. Its sole
substantive correction is all-three-author publication attribution; changes to
current catalogue/pointer hashes follow from that corrected admission. Native
science, protocol PDF/text, source dispositions and factors remain unchanged.
