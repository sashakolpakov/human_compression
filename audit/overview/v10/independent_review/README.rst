Independent review of overview43
================================

Accepted unchanged at author manifest 4da624cc48c891c089e05823f88c218a4113f2ad5319fd632c5479dfffc2c26a.
This bounded review covers the root-authored consolidation, not a fresh
adjudication of the accepted source proofs or measurement inputs.

The independent checker derives all 62 fractions, verifies all 81 CSV and
actual PDF rows, compares all 106 active originals, and reads actual SVG/PDF
bar geometry. It imports no author arithmetic or plotting helper. All 24
semantic/output mutations are rejected. Every reader page was directly viewed.
A fresh export-only author replay also passes with all six page texts exact.

Replay with a full public checkout containing the pinned inputs::

  python -B -O check.py --candidate /frozen/overview43 --artifacts /frozen/overview43 --public-root /checkout --out /fresh/review
  python -B -O controls.py --candidate /frozen/overview43 --public-root /checkout --out /fresh/controls

The external old/new catalogues stay in the public checkout; their complete
paths, sizes and digests are verified rather than duplicating their contents.
The author packet's own command can separately rebuild the six-page reader::

  python -B -O /frozen/overview43/check.py --out /fresh/rebuild --public-root /checkout --render --xelatex /path/to/xelatex

Python requires pypdf; a fresh author rebuild additionally uses matplotlib and
XeLaTeX. No source extraction, GAP or Lean run is part of this bounded review.
Software-inclusive comparisons remain unavailable; proof-essential programs
are not recategorized as optional. Prior scientific authorship and accepted
numerical inputs are disclosed in review.json. No public file was changed.
