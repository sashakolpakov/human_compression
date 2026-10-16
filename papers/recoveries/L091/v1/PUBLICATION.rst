The Higman--Sims classification: proofs and source audit
======================================================

This directory publishes the accepted disposition of original L091.  The
eleven-page ``synthesis.pdf`` explains the classification method, its logical
premises and the corrections to the source.  ``complete.pdf`` contains that
synthesis, a divider, and all twenty-six previously accepted proof chapters:
seventy-eight pages in total.  The chapters are also available separately in
``proofs/``.  Every TeX input is supplied, including ``proofs/counts.tex``, which
the tenth chapter requires.  Run TeX from the directory containing each main
file.  The principal entry points are ``synthesis.tex`` and ``complete.tex``.

The classification has 86 source diagrams, 398 local structure occurrences and
312 parabolic occurrences.  The original Higman--Sims rank counts survive the
audit.  Some group labels, numerical fields and construction prescriptions
require the corrections stated in the synthesis and in ``corrections.json``.
Source errors, originally blank fields and our own transcription mistakes are
listed separately.  The correction categories overlap; their sizes are not
added to produce an error total.

The comparison with other sporadic groups retains the equivalence relation of
each cited classification.  In particular, the J3 comparison uses the nineteen
supplied classes.  Its global coverage and absence of higher ranks remain
explicit premises attributed to L091 reference [9], catalogue record L097.
This publication does not claim to recover that external classification or
award an additional original to its source.

The full proof volume retains the accepted PDF unchanged.  Its imported
chapter pages have exactly the original mathematical content streams.  The
volume additionally numbers those pages; this does not alter the separate
chapter PDFs.  ``native_streams.json`` in the audit directory records the exact
sixty-six imported streams.  ``selected_inputs.json`` records every adjacent
native input for the twenty-eight TeX entry points.

Exact evidence and replay
-------------------------

The accompanying ``audit/recoveries/L091/v1`` directory supplies the complete
accepted dependency closure.  A logical file index routes identical contents
to previously published files or to new bounded packs.  Each route checks both
the encoded and decoded lengths and SHA-256 hashes.  Reused segments additionally
bind the complete published files that contain them.  No full private tree
needs to be restored.

The exact list in ``premises.json`` separates original source documents and
installed software from the evidence carried here.  Those documentary and
environmental files remain explicit premises, identified by their recorded
locations and hashes.  Derived mathematical tables, generators, proofs, code,
transcripts, controls and review records remain in the payload.  The software
premises include the previously stated role of complete graph-automorphism
computations; hash checks are not a proof of a software implementation.

The portable checker verifies the whole transport, then restores only thirty-
one small inputs needed by the unchanged accepted occurrence join.  It runs
that join and its ten damage controls and compares their complete outputs with
the independent mathematical review.  It does not rerun a group search.  With
``--render`` it also compiles the synthesis and complete volume, checks their
text against the accepted PDFs, and checks every new synthesis raster against
the pages already directly viewed in mathematical review.

The replay command, with the externally recorded manifest hashes substituted,
is::

  python audit/recoveries/L091/v1/portable_check.py \
    --repo "$PWD" --out /absolute/fresh/output \
    --expected-stage STAGE_MANIFEST_SHA256 \
    --expected-transport TRANSPORT_SHA256 --render

The transport and occurrence replay do not repeat every earlier mathematical
review.  The accepted component proofs, their assumptions and their review
records are carried unchanged and explicitly acquired by the synthesis.

Scope
-----

This is one corrected original.  It claims no newly settled open conjecture,
new Lean formalization or measured mathematical compression factor.  Encoded
storage size is solely a publication resource measure.  Mathematical source
disposition and public registration are separate decisions; historical author
status fields are preserved rather than retrospectively overwritten.
