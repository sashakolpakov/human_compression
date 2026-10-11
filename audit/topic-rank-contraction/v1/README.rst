Rank contraction: proof and numerical admission
===============================================

`admission.json <admission.json>`_ admits the corrected principal contract for
one original, L037, and its complete numerical comparison. The underlying
22 source clauses and 20 proof contexts are not additional manuscripts.

The mathematical `independent review <science_review/review.json>`_ records
the complete written proof, source qualifications, retained constructions and
limits of the four Lean lemmas. The numerical `reader
<measurement/packet/reader.pdf>`_ and `root review
<measurement/independent_review/review.json>`_ give every boundary and ratio.
All thirty coordinates and 120 exact fractions are retained. Complete raw
PDF extraction under NFC is primary; calibrated coordinates are sensitivities.

Fresh public-copy runs reproduce the science, finite examples, four Lean
lemmas, all nine scientific pages, input counts, numerical reader and distinct
checks. Unknown external proof, graphical and full-formalization costs remain
null. Conjecture 5.1 remains open; this admission adds no question credit.

Portable numerical replay, from the repository root::

  python -B -O audit/topic-rank-contraction/v1/measurement/packet/check.py --out /fresh/numbers --render
  python -B -O audit/topic-rank-contraction/v1/measurement/independent_review/check.py --packet audit/topic-rank-contraction/v1/measurement/packet --out /fresh/distinct

The frozen scientific checker also runs GAP, Lean and XeLaTeX. Its --study-root
argument must identify the privately acquired primary assets and retained
audit records listed in packet/scope.json. They are explicitly hash-bound,
not included in this public repository. The independent finite check requires
only the published science packet::

  python -B -O audit/topic-rank-contraction/v1/science_review/check.py --packet papers/topic-rank-contraction/v1/packet --out /fresh/finite

Author candidate labels are preserved as historical evidence. Distinct root
reviews and this admission record their subsequent acceptance.
