Root integration of science70
=============================

Use exact committed baseline 6b0ca7eacea91a764f527b1945837cc64bedf720.
Root is the sole public writer. Scientific acceptance is the bound N011 root
review; publication additionally requires root's separate integration decision.

1. Install this proposal's manifest-listed exports and manifest at
   audit/science70/v1/publication_plan. Copy all 21 whole frozen payload routes
   and all 24 wrapper_routes.json files. There is no primary asset, Markdown or
   private fallback. Both whole manuscripts use their original pdfLaTeX engine.
2. Add the two snapshot_additions.py functions before main; change only main's
   current science69 route to science70. Preserve all 165 old non-main ASTs.
   apply_stage_verifier.py demonstrates the edit only in a marked private stage
   and refuses the public repository. The saved read-only science69 overlay
   replays its current and nested history guards through programme53.
3. Preserve all 53 measured originals, nineteen topic comparisons, overview v19,
   the measured catalogue and its builder. Only N011's recovery status and the
   science-only manuscript catalogue are extended. The whole optional symbolic
   check/output and operational driver remain separate from proof premises.
4. Root alone creates audit/science70/v1/root_integration.json, with status
   ROOT_ACCEPTED_SCIENCE70_PUBLICATION, source_ids [N011], measurements_added 0
   and new_question_credit 0. Bind every exact path required by
   reports/gate_controls.json, including the actual final verifier and proposal
   manifest. In-memory test fixtures are not acceptance records.
5. Run the full root snapshot before committing and publishing. Any integration
   correction must be an explicit additive record; frozen scientific and
   proposal bytes remain unchanged.

Private staging and public-only replay::

  python -B -O stage.py --study STUDY --repo PUBLIC --out FRESH_STAGE
  python -B -O apply_stage_verifier.py --stage FRESH_STAGE --out AST_REPORT
  python -B -O check.py --repo FRESH_STAGE --out ROUTE_REPORT
  python -B -O check_gate_controls.py --repo FRESH_STAGE --out GATE_REPORT
  python -B -O replay.py --repo FRESH_STAGE --out FRESH_REPLAY --render
  python -B -O FRESH_STAGE/scripts/check_science70_history.py --repo FRESH_STAGE

Only initial staging reads the exact private packets. Thereafter replay.py
reconstructs them entirely from their proposed public files. It reruns optional
symbolic validation and the author scope/controls and rebuilds both complete
manuscripts. There is no required finite search, census, Lean or source extraction
to repeat. Historical source assets remain private.
