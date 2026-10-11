Topic F: independent publication integration review
==================================================

Accepted against candidate bindings_v2.json, SHA256
45dbdfa0a66b579099df8e45701f6bc21877aefae28a3ad745d9f48eddffa0bc.
The six frozen packets are copied exactly; thirty-two old verifier functions
and their dispatch order are unchanged. This review adds no mathematical,
source, question, formal, font or measurement credit.

Two integration findings were corrected before acceptance: the standalone
input adapter now pins the executable independent-review packet, and the
publication guard enforces both the 90 combined and 30 conditional fractions.
Actual private corruption tests exercise both repairs.

Read review.json for roles, costs and visual limits; replay.json records
all 34 controls, public links and the preserved SVG whitespace exception.
The reviewer authored the earlier input/numerical reviews and reuses their
root-adopted acceptances here, rather than presenting them as new work.

Run the bounded read-only integration checker::

  python3 -B -O check.py --repository /path/to/math_compression \
    --study /path/to/leemans --out /fresh/review.json

The optional study root verifies private/public copy equality. The public
repository must retain the frozen baseline commit for AST comparison. No
primary PDF, GAP, Lean or parser installation is required by this review.

Portability revision
--------------------

This v2 preserves the original review freeze 22aa2d18 and all 62 candidate
bytes. The checker also works after its own review and root acceptance
are published. It allows only the six exact review exports plus their
manifest, publication_root_replay.json and publication_acceptance.json.
The report and root acceptance must both exist and bind the exact review,
candidate and passing replay. No directory-prefix exemption is used.
Private fixture controls exercise all three publication stages and reject
corrupted or unbound additions. The global publication manifest separately
anchors the root acceptance; no circular self-hash is claimed.
