Independent review of Topic D
=============================

The frozen common paper and all three applications are accepted under the
exact retained inputs and exclusions in review.json. All 37 source rows are
checked. This is a proof review, with no new source or question credit and no
compression factor. The later support-count Lean supplement is not included.

Fresh execution used all eight complete programs, both scoped Lean modules
and all five documents. All 31 rendered pages match the author PDFs; all 26
primary pages were read and viewed. Primary text and images are not exported.

Replay the complete author packet in a fresh directory, using Python with
pypdf 6.13.0, GAP/TomLib and the pinned Lean package tree::

  python -B -O /path/to/topic_D_volume/check.py --out /fresh/replay \
    --study-root /path/to/private/study --programs --formal --render \
    --xelatex /path/to/xelatex

The study-root option verifies primary/proof-bank hashes. Omit it only when
those external byte checks are unavailable; the mathematical inputs remain.
Then run the separately authored interface and witness checks::

  python -B -O check.py --author /path/to/topic_D_volume \
    --replay /fresh/replay --out /fresh/independent.json

The independent checker uses actual GAP subgroup equality for all 170 panel
and parabolic records. Printed generating lists can change on a fresh run;
this does not alter the groups. Two deliberately damaged witness controls
reject. The support models exercise noninvariant proper support sublevels
and nonfaithful actions; the general formula is accepted from its written
proof, not extrapolated from these finite tests.

The retained Suzuki structure, full TomLib catalogue, exact GAP algorithms
and ordinary regular-polytope correspondence remain explicit dependencies.
L104's printed diagrams, full automorphism/correlation groups and doubling
relation remain outside its principal census contract.
