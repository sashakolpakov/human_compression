Topic G measurement inputs
==========================

This is a proposed input boundary and reproducible count, awaiting independent
review. It contains no compression factor. The scientific edition is the
accepted common paper, two complete applications and complete program appendix
published at dc9d521b16f6399934416f09caba14f50d4a48b8. All 79 source-contract rows
and 34 current proof spans are preserved. This task adds no mathematical result,
source credit or question answer.

Complete documents
------------------

L009 has 25 physical PDF pages: a publisher identification cover and 24 article
pages. The primary coordinate includes the cover; a separately identified
article-only sensitivity is supplied. L092 has 14 pages. Our common paper has
12 pages, the two applications 8 and 22 pages, and the program appendix 20 pages.
All 101 pages were visually inspected. Complete titles, abstracts, body text,
references, unique identification matter and extractable diagram labels are
included. Only occurrence-bound running headers and page numbers are removed.

The primary unit is the number of non-whitespace characters after NFC
normalization and declared visible-glyph calibration. The report also supplies
all five units for NFC and NFKC and the raw-untrimmed, raw-selected and calibrated-
selected variants. Printed discretionary hyphens and actual/generated whitespace
are retained. No formula or diagram is priced as if text extraction captured its
entire content.

The intended first comparison uses both complete source PDFs against the whole
common paper plus both complete applications. The program-inclusive comparison
adds the whole printed appendix once. An alternative uses all thirteen complete
raw programs in place of that appendix, never in addition to it. Conditional
source/application comparisons presuppose acquisition of the whole common paper
and the complete programme. No cross-topic umbrella cost is deducted.

Programs and retained costs
---------------------------

The thirteen complete programs comprise four mathematical finite computations,
two witness/certificate bridges and seven validation files. Their exact roles
are bound in replacement_input_spec.json. The complete appendix is retained even
where a file contains diagnostics as well as a necessary computation. Three
complete operational drivers and six Lean files (40 previously scoped
declarations) are counted separately. They are not silently added to the
scientific paper denominator. No new GAP or Lean proof run is inferred from this
measurement replay.

The complete retained Buekenhout--Delandtsheer--Doyen and Kantor proofs, original
historical code, graphic construction and layout costs remain unknown, not zero.
L009 cover emblems include lettering with no extracted text. Source vector paths,
colors, geometry and formula layout are also unpriced. graphic_inventory.json
records the affected pages. This is a complete-document extractable-text
coordinate, not a claim to measure all visible or graphical information.

Font and parser evidence
------------------------

Every one of the 509 substitutions is tied to its physical page, exact extracted
text offset and context hash, embedded font stream, encoded byte and actual PDF
text event. Full evidence includes 1,165 used encoded glyph classes and 75,909
non-whitespace decoded characters. The source-specific mappings are not borrowed
from earlier topic calibrations. The substitutions include printable aliases:
script letters, a LASY square, line-font diagonals and circle-font solid nodes,
as well as brace pieces. No own-document substitution is needed.

There are four explicit parser qualifications.

* On the L009 cover, pypdf's visitor emits one duplicate aggregate Form summary
  with font=None and the exact text ``ALGEBRAIC\n COMBINATORICS``. Only that
  callback is ignored for font alignment. The counted page.extract_text() string
  remains unchanged, and recursive event replay visits the actual logo once.
* L092 repeats font dictionary keys /F18 and /F27 at offsets 0xbad and 0xc0d.
  Each duplicate points to the same object as its first occurrence. The parser
  warnings are expected; no competing font definition is selected.
* Some old Type1 subsets omit unused Subrs or contain null unused array slots.
  The narrowly scoped font reader permits those absent entries while decoding
  every used charstring from unchanged font bytes. CFF StandardEncoding and
  explicit PDF WinAnsi mappings are resolved to actual glyph names.
* Ligatures may decode to multiple Unicode characters. Each decoded character
  records its index in that one encoded event. Actual space glyphs and generated
  extraction whitespace remain unchanged; the one encoded blank-space glyph has
  an empty outline.

The visible source font outlines and all pages were inspected privately. The
packet exports evidence metadata and hashes, not font programs, primary images,
full primary extracted text or any OCR transcription.

Reproduction
------------

Use Python with pypdf 6.13.0 and fontTools 4.63.0. The installed interpreter used
here is /Users/sasha/.venvs/global/bin/python. With the separately retained
primary PDFs and accepted scientific packet available, run::

  python -B -O extract_inputs.py \
    --study-root /path/to/research/leemans \
    --public-root /path/to/human_compression \
    --out /fresh/output/directory

The public-root argument is optional; when supplied it verifies the exact public
admission and all four current PDFs. Output must not exist, including as a
symlink. The replay checks 180 PDF metric cells, 130 raw program cells, 30 driver
cells and 60 formal-file cells, and runs 18 rejection controls. It outputs only
metadata and counts, including text hashes, never the complete primary text.
The private outline renderer and resulting panels are author working materials;
they are not distributed in this packet.
