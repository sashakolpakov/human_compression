Root integration of science65
=============================

Baseline is local commit e277a8ddcd822e71f0e8ee61e0e9d4ab57508e82. Do not describe
it as remotely published: origin/main was 41983bd1827137c629d1aa00c6bb79ea9e66ba95
at preparation. Record actual transport separately after integration.

1. Install these exact proposal exports and manifest at
   audit/science65/v1/publication_plan. In copy_plan.json, copy each unique
   COPY_FROZEN destination from its study_path and verify its bytes/hash.
   EXISTING_PUBLIC routes must be checked and reused, not needlessly copied.
   Install the 24 wrapper_routes.json files. Preserve all frozen author/review
   manifests byte-for-byte; the plan restores their logical paths for replay.
2. Insert snapshot_additions.py's two new functions before main in the public
   verifier, preserving all 155 old non-main function ASTs. In main only,
   replace the current check_previous_science64/check_science64 pair with the
   science65 pair and update its local variable and display accordingly.
   The new historical wrapper evaluates exact saved science64 pointers and
   its full chain to programme53. No historical guard function is rewritten.
3. Keep every measured catalogue, topic factor, overview v19 and canonical
   build default exact. Three standalone pdfLaTeX papers are appended only
   to the corrected-unmeasured scientific catalogue; the existing Topic D
   common is an explicit acquired dependency. No new comparison topic appears.
4. Root alone creates audit/science65/v1/root_integration.json with status
   ROOT_ACCEPTED_SCIENCE65_PUBLICATION, source_ids [L096], measurements_added 0,
   new_question_credit 0. Bind every exact path in reports/gate_controls.json,
   including the actual verifier and this proposal manifest. The guard checks
   those exact paths, not a broad prefix permission. The current admission
   is a root-science-accepted registration proposal until this gate exists.
5. Run the full snapshot, then commit and attempt transport only as authorized.
   Any integration change belongs in an explicit root delta with propagated
   bindings. Preserve this proposal and every prior accepted byte unchanged.

Private checks::

  python -B -O stage.py --study STUDY --repo PUBLIC --out FRESH_STAGE
  python -B -O check.py --repo FRESH_STAGE --out FRESH_ROUTES.json
  python -B -O check_gate_controls.py --repo FRESH_STAGE --out FRESH_GATE.json
  python -B -O replay.py --repo FRESH_STAGE --out FRESH_REPLAY --render --new-programs
  python -B -O FRESH_STAGE/scripts/check_science65_history.py --repo FRESH_STAGE

The public-only replay restores every required logical file from the explicit
map. It has no private study fallback. Its --new-programs option runs only
the seven current discriminators, not inherited censuses or full shadow runs.
Without that option it checks their complete retained output. Private source
assets remain absent and no new source-reading claim follows from replay.

The scientific role inventory is unchanged. Additional publication preparation,
mapping, restoration and guard scripts are operational tooling, disclosed in
publication_tools.json; they are not new mathematical premises or factors.
