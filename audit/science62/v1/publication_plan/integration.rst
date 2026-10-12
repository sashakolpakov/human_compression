Root integration of L025
========================

The exact baseline is science61 commit
769b351478a71a79e447f9293b46f165d0cdb934. This proposal changes no public file.

1. Install the exact proposal exports and manifest at
   audit/science62/v1/publication_plan, the 78 payload routes in copy_plan.json,
   and the 24 wrappers. Keep all accepted scientific and review bytes unchanged.
2. Add the two functions in snapshot_additions.py before main, retaining all
   149 prior non-main ASTs. Change main's current check_previous_science61()
   and check_science61() calls to their science62 successors. Preserve the
   historical return interface and update current summary counts to 62 reviewed,
   53 measured, nine unmeasured, 43 mathematical targets and one editorial.
   The new historical wrapper runs saved science61 and its nested chain through
   programme53 using exact read-only pointer overlays.
3. Leave the measured catalogue, all measurement admissions and overview v19
   unchanged. Append only the three complete L025 native papers to the separate
   corrected-unmeasured catalogue. This adds one original, no comparison topic.
4. The commands below build an isolated stage, validate all routes, reconstruct
   the four portable packets and rebuild their native papers. Six supplied
   graph computations are repeated; no historical census, primary extraction or
   Lean run is required. The complete protocol PDF is already compiled and bound.
5. Root alone creates audit/science62/v1/root_integration.json with status
   ROOT_ACCEPTED_SCIENCE62_PUBLICATION, source_ids [L025], measurements_added 0
   and new_question_credit 0. Bind every exact path in reports/gate_controls.json,
   including the actual verifier, proposal manifest, current wrappers and native
   papers. No broader path exclusion or fabricated acceptance is needed.
6. Root then generates the full snapshot, runs all checks, commits and pushes.
   Record actual local and remote results separately. Later integration changes
   require an explicit delta; this frozen proposal remains immutable.

Run with the global Python environment containing pypdf::

   python -B -O stage.py --study /Users/sasha/medusa/research/leemans --repo /Users/sasha/medusa/math_compression --out FRESH_STAGE
   python -B -O check.py --repo FRESH_STAGE --out FRESH_ROUTE_REPORT.json
   python -B -O check_gate_controls.py --repo FRESH_STAGE --out FRESH_GATE_REPORT.json
   python -B -O replay.py --repo FRESH_STAGE --out FRESH_REPLAY --render
   python -B -O FRESH_STAGE/scripts/check_science62_history.py --repo FRESH_STAGE

The public guard requires root integration acceptance. The private route checker
omits that requirement by default and states that publication has not been
adjudicated. Native titles, compiler selection and full 7+5+3-page boundaries
are exact. Required programs and data remain distinct from optional checks and
partial formal evidence; all external costs remain unknown.
