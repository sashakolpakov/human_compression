Topic B: complete and conditional written costs
===============================================

This packet applies two comparisons to the same fixed mathematical scope:

* Complete topic: all four source manuscripts divided by the common theory
  and all four applications, charging that theory once.
* Each matched result: its source manuscript divided by its application,
  after the whole common theory has been acquired.

The primary unit is NFC characters without whitespace, measured from the
complete PDF extraction after recorded furniture exclusions and visible
glyph repairs. The common theory costs 14,119 and the applications cost
44,942, so the complete denominator is 59,061. The three available source
PDFs cost 57,539. If the missing N001 original PDF has cost x, the overall
expression is (x + 57,539) / 59,061. There is no numerical overall factor.
B1 is still charged. Unknown is not zero.

The conditional factors are unknown for N001/B1, 1.254 for N003/B2,
1.576 for N008/B3 and 1.811 for L030/B4. Separate topics pay their full
common theory even when arguments overlap. This edition requires no
mathematical enumeration program; Lean and finite checks are validation
infrastructure, not uncharged mathematical dependencies.

Read measurement.pdf for the two-page account and cost graph. Exact
fractions and all thirty choices of extraction, normalization and unit
are in results.json, with flat tables in conditional_costs.csv and
overall_costs.csv. The files under inputs/ preserve the author's measurement
proposal, and independent/ preserves the separate full recount: 240 metric
cells and 48 normalized text hashes matched. Their source representations,
external proof costs, graphics and formal scope are explicitly qualified.

The source papers, extracted primary texts and source rasters are not
redistributed. The five public scientific PDFs are bound to the proof
edition at commit 769322e67042671b404917b7a6249e1a5de4ef18. Replaying
extraction requires the privately retained primary artifacts. Deriving
these numerical results from the published checked counts does not::

  python3 -B -O compute.py --out FRESH_RESULT_JSON

The output must match results.json byte for byte. To rebuild the reader,
using pypdf 6.13.0, matplotlib 3.10.9, XeLaTeX and the STIXGeneral font::

  python3 -B build_reader.py --out FRESH_READER_DIRECTORY

The author-stage status is preserved in the frozen output. An independent
arithmetic review and a separate publication admission must bind this
packet before the new factors are presented as accepted. Neither this
measurement nor its graph adds a source-paper or conjecture credit.
