Root integration of science67
=============================

Use exact baseline 2783b3c3c03aa71dcf3c3cb9b30a2b0b9055d939.
Root is the sole public writer. Scientific acceptance is already bound;
publication still requires root's independent integration decision.

1. Install the proposal's manifest-listed exports and manifest at
   audit/science67/v1/publication_plan. For every copy_plan.json row, check
   bytes and SHA-256. Copy the 65 COPY_FROZEN destinations and verify the
   nine EXISTING_PUBLIC destinations without overwriting them. The latter
   are the exact L011 native TeX/PDF and seven provenance/review files.
   Copy all 24 wrapper_routes.json files.
2. Insert the two snapshot_additions.py functions before main and change
   only main's current science66 calls/local variable to science67. Preserve
   all 159 old non-main ASTs exactly. apply_stage_verifier.py demonstrates
   this change only in a marked private stage and refuses the public repo.
   The new historical wrapper loads saved science66 pointers and its complete
   nested programme53 guard. No old guard function needs modification.
3. Preserve all 53 measurements, nineteen comparison topics, overview v19,
   the canonical measured catalogue and build script. The separate corrected
   science catalogue appends seven acquisition entries, of which the final
   L011 entry points to its existing native paper. All seven use pdfLaTeX;
   the updated general protocol uses its existing XeLaTeX workflow.
4. Root alone creates audit/science67/v1/root_integration.json with status
   ROOT_ACCEPTED_SCIENCE67_PUBLICATION, source_ids [L031], measurements_added 0
   and new_question_credit 0. Bind every one of the 40 exact required paths
   in reports/gate_controls.json, including the actual verifier and proposal
   manifest. Prefix-wide allowances do not replace these exact bindings.
   This proposal contains no purported root publication acceptance.
5. Run the full root snapshot before committing and publishing. If integration
   needs an adjustment, record an explicit root delta and bind the resulting
   bytes without mutating this proposal or any accepted scientific packet.

Private staging and replay commands::

  python -B -O stage.py --study STUDY --repo PUBLIC --out FRESH_STAGE
  python -B -O apply_stage_verifier.py --stage FRESH_STAGE --out AST_REPORT
  python -B -O check.py --repo FRESH_STAGE --out ROUTE_REPORT
  python -B -O check_gate_controls.py --repo FRESH_STAGE --out GATE_REPORT
  python -B -O replay.py --repo FRESH_STAGE --out FRESH_REPLAY --render
  python -B -O FRESH_STAGE/scripts/check_science67_history.py --repo FRESH_STAGE

Staging uses the explicitly pinned private science files to create public
routes. replay.py then needs only those public routes: it reconstructs the
complete immutable author and root-review packets in a fresh directory and
checks all 23 native page texts. No source extraction, finite census, new
mathematical computation or Lean build is performed. Historical verification
reuses exact previously accepted evidence. The operational tools are whole
files in publication_tools.json and create no additional mathematical premise.
