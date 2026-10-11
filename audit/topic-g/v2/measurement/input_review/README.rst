Independent Topic G measurement input review
===========================================

Accepted input edition: topic_G_measurement_inputs_v2, manifest
c46e1742d44138d9a63af86ae2ee9dd9d1498d0b4ca0d75cf1fd19a022af978d.
The original 79ee51fd edition is preserved and is not the accepted font evidence.

The independent recount matches all 180 PDF measurement cells and 220 whole-file
cells, including normalized text hashes. It verifies the source cover sensitivity,
full document selections, every actual font dictionary/encoding and all 509
calibrated occurrences. The source pages contain 1,209 used dictionary/byte
classes and 75,909 nonspace decoded characters. All 101 pages and 71 additional
outline cases were visually inspected. The review retains the distinction between
extractable text and unknown graphical or retained external proof costs.

The review found and required one correction: a font name was used as an encoding
cache key although four names identify two distinct effective encodings apiece.
The corrected edition repairs 701 event records across nine glyph classes.
No measured text, calibration output or cost cell changes.

Reproduction, using the separately retained primary PDFs, accepted scientific
files, both input editions and the current public scientific PDFs::

  python -B -O check.py --study-root /path/to/research/leemans \
    --public-root /path/to/human_compression --out /fresh/report.json

Optional --packet and --original arguments locate the two frozen input editions.
Python dependencies are pypdf 6.13.0 and fontTools 4.63.0. The checker does not
import the author's extraction/calibration/metric code. It independently traverses
actual PDF events and counts Unicode characters with state-based counters, while
retaining those same PDF/font parser libraries. Twenty-one independent boundary
and font-evidence mutations must be rejected. The separate fresh author replay
also rejected its twenty-two controls.

The report is an input acceptance only. It supplies no compression factors, new
scientific claims, or additional source, question or formal-proof credit. The
scientific scope remains 79 clauses and 34 proof spans, thirteen whole programs
(four finite inputs, two witness/certificate bridges, seven validation files),
three separately measured drivers and six separately measured Lean files with
forty previously scoped declarations. No GAP or Lean replay is claimed here.

Only metadata, counts, code and evidence hashes are exported. Primary PDF pages,
extracted source manuscripts, font programs and raster images remain private.
