Two additional measured originals
==================================

The accepted comparison adds F015 and L028 to the earlier 27 measured
originals. The two-page reader is packet/measurement.pdf; complete inputs,
programs, independent recount and separate numerical review are included.
Frozen author candidate labels are historical; admission.json records current
acceptance. No primary PDFs, primary text, glyph rasters or fonts are exported.

Matching: whole written 1.119, conditional 2.211, with printed code 0.976 or raw
code 0.991. Chiral enumeration: whole written 0.925, conditional 1.277, with
printed code 0.674 or raw code 0.687. The primary unit is calibrated NFC
characters excluding whitespace. The complete common paper and full program
bundle are acquired before each conditional comparison. Printed and raw
program costs are alternatives. Source corrections and unpriced outside
proofs/graphics remain explicit; no new conjecture or full formalization is
claimed. Chiral enumeration's small saving in word units does not survive
character counting. Both results remain reported.

From the repository root, replay the public numerical closure::

  python -B -O audit/additional-measurements/v1/packet/run.py \
    --study-root audit/additional-measurements/v1/inputs --out FRESH_OUTPUT

Run the separate independent check::

  python -B -O audit/additional-measurements/v1/independent_review/check.py \
    --author audit/additional-measurements/v1/packet \
    --recount audit/additional-measurements/v1/inputs/additional_sources_inputs_root_review/recount.json \
    --out ANOTHER_FRESH_OUTPUT

The inputs folder provides the documented extractor for a new primary-bound
recount. This publication replay checks the already accepted counts and
rebuilds all numerical, graph and reader outputs; it does not rerun source
extraction or scientific GAP and Lean proofs. Those earlier reviewed checks
remain separately bound. The old ten-topic report remains an immutable
comparison of its 27 originals. No pooled cross-topic factor is assigned.
