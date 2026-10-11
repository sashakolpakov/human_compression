Topic C: complete comparison and conditional application costs
===============================================================

This author calculation uses the independently accepted Topic C input
measurements. It does not alter the proof edition or acquire a new source.
The two-page measurement.pdf and costs.svg show one complete-topic
comparison and the four matched application comparisons.

The primary coordinate is calibrated selected PDF text, NFC characters
excluding whitespace. Complete costs are:

* available source PDFs: 60,256; L108 original PDF: unknown x;
* whole common paper U_C: 27,131;
* all four applications: 44,146, including C3's 10,071;
* complete required printed program appendix: 8,799.

The primary overall comparison is therefore (x + 60,256) / 80,076.
There is no numerical overall factor. After acquiring the whole U_C and
both complete required programs, the conditional application factors are
1.118 (L088/C1), 1.709 (N013/C2), unknown (L108/C3) and 2.960 (F014/C4).
These are full source-paper/application lengths at the accepted contract
scope, not claims to recover every auxiliary statement in each source.
The forty-row scope table retains its qualifications and exclusions.

Two separate sensitivities use the written-paper denominator 71,277 or
replace the printed appendix by both full raw programs, giving 79,600.
The full raw files total 9,241 bytes and 8,323 NFC nonspace characters.
Their metrics are summed file by file. Raw programs are never added to
CODE, and no diagnostic or other program portion is pruned. Every topic
pays its own complete common theory, without a cross-topic discount.

The exact arithmetic is recorded for all five units, NFC/NFKC and all
three extraction variants. overall_costs.csv has 90 representation rows;
conditional_costs.csv has 120 rows, including the thirty unknown C3
coordinates. Exact reduced fractions are retained alongside displayed
decimals. The complete printed appendix is the primary required-cost
representation in every coordinate.

Reproduce in a fresh directory, without primary PDFs or network access::

  python3 -B -O compute.py --out /fresh/results
  python3 -B -O check.py --results-dir /fresh/results --out /fresh/check.json
  python3 -B build_reader.py --results /fresh/results/results.json \
    --out /fresh/render --xelatex /path/to/xelatex

The first two commands require Python's standard library. The reader
uses Matplotlib, pypdf, XeLaTeX and STIXGeneral. Its PDF metadata may vary
between builds; exact page text is the render comparison. All frozen
input-proposal exports and the independent input acceptance are copied
byte-exact to inputs/ and independent/. No primary text or source images
are included. The supplied source extraction and independent font-recount
programs are preserved evidence; this arithmetic replay does not invoke
them or repeat source/Lean/GAP verification.

Eleven semantic controls reject omitted C3 or CODE costs, double program
charging, program pruning, invented L108/overall costs, altered fractions,
lost common/program prepayment, external-cost zero, new credit and wrong
primary selection. These are author consistency checks. Independent
arithmetic and reader review must precede admission of this packet.

Expanded external proofs, catalogue construction, graphics and formula
layout remain unmeasured. This is an extracted-text comparison, not total
research effort or minimum mathematical complexity. The 16 scoped Lean
declarations and other proof-validation infrastructure remain separately
inventoried. No source or question credit is added.
