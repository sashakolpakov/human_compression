Representation measurement publication integration
=================================================

This is an independent review of the fixed publication integration, not a new
scientific, font or numerical audit. The reviewer previously reviewed the
Representation science and input boundary and contributed an inherited local
gadget validation. Distinct numerical review and root adoptions are reused.
All 78 candidate bindings, six exact accepted packets, 16 public input routes,
37 unchanged earlier checker functions and the new 120/120 guard pass.
The 47 semantic/path corruption tests are rejected. All seven protocol pages
were visually read. No source, question or formal credit is added.

Replay
------

From a Python environment supporting the current public verifier::

  python -B -O check.py --public-root /path/to/human_compression \
    --out /fresh/report.json

Add ``--study-root /path/to/private/study`` only to compare the six frozen
private packets to their public copies. The primary PDF is not needed.
The checked edition is fixed to the 78-file candidate in bindings.json, based
on Git commit 3c83237dcb7c8c68461bfd0f1bfcb9e7da0967b5. Unrelated subsequent
public changes are deliberately rejected. The frozen replay predates its own
manifest and records the self-copy fixture as deferred; a fresh postfreeze
run exercises that fixture using the actual manifest.

Exact postpublication additions
-------------------------------

Under ``audit/topic-representation/v2/measurement/``, the only additional
allowed files are this packet's seven exact exports plus manifest.json in
``publication_review/``, and the two exact basenames
``root_publication_replay.json`` and ``root_publication_acceptance.json``.
There is no directory-prefix allowance. The root replay is the unmodified
fresh output of this checker before root adoption. The acceptance JSON must
have exactly these fields (no additional keys)::

  {
    "status": "ROOT_ACCEPTED_REPRESENTATION_MEASUREMENT_PUBLICATION_INTEGRATION",
    "independent_manifest_sha256": "<this manifest SHA256>",
    "independent_review_sha256": "<review.json SHA256>",
    "candidate_bindings_sha256": "8bb4f3e6d103231e750f2f44a23be45109ca21243c65c4a49be31dbc1236b528",
    "admission_sha256": "aa3863bfd37920a3879abce71525ef5da9ee20d65222e9108460199a7a922cff",
    "fresh_root_replay": {
      "path": "root_publication_replay.json",
      "bytes": 0,
      "sha256": "<actual replay SHA256>"
    },
    "controls_rejected": 47,
    "author_and_reviewer_roles_preserved": true,
    "no_primary_export": true,
    "source_extraction_repeated": false,
    "GAP_or_Lean_replayed": false,
    "new_source_credit": 0,
    "new_question_credit": 0,
    "new_formal_credit": 0
  }

Replace the replay ``bytes`` placeholder by the actual byte length. All other
non-placeholder values are literal. The replay must report the same candidate,
admission, 78 files, 66 frozen files/manifests, 16 public routes, 37 unchanged
checks, 120/120 result and all 47 named rejected controls. The public review
manifest and every export must match this exact packet. The global publication
manifest remains separate to avoid a circular binding.

Scope and whitespace
--------------------

The whole written factor remains first, followed by the conditional factor
and separate printed/raw validation-program alternatives. The small written
saving reverses under UTF-8 bytes. Two drivers and two scoped Lean files are
separate, unknown retained/graphical costs remain unknown, and dependency
passage costs are pending. All underlying accepted costs are reused.
``whitespace.json`` inventories 896 frozen diagnostics in three copied files;
those immutable bytes were preserved. No scientific or primary files changed.
