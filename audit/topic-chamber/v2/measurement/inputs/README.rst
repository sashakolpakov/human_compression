Topic Chamber: complete measurement inputs
==========================================

This is an input proposal, not a numerical comparison. It fixes the full
source and replacement boundary, exact extraction, glyph calibration,
raw sensitivities and program roles. Independent input review is required
before factors are calculated. No result, question or source credit changes.

The scientific edition is the exact published commit
``b6c0a3cc45c556e3ec0b744df408227c8f922139``. The accepted author packet,
independent mathematical review, root adoption, public admission and public
integration review are bound in ``publication_binding.json``. The policy was
fixed before extraction while publication was a candidate; that historical
policy is preserved. Its candidate status does not override the later
committed publication binding.

Complete documents
------------------

The source inputs are the ten-page arXiv:2511.14562v1 manuscript *Testing
chirality on hypertopes*, by Wei-Juan Zhang and Dimitri Leemans, and the
eight-page author manuscript *Chiral polytopes whose smallest regular cover
is a polytope*, by Gabe Cunningham, dated 25 July 2023. The latter is not
represented as a publisher PDF. Both supplied originals must match their
hashes. Their titles, abstracts, footnotes, references, acknowledgements,
author information and printed source software are included.

The replacement consists of the complete six-page common paper, three-page
chirality application, six-page cover application, and three-page whole
program appendix. There are six PDFs and 36 physical pages. The scientific
scope remains the exact 27 source rows and 22 proof contexts. Full manuscript
lengths will be compared under the accepted principal-result contracts;
this is not a claim to replace every ancillary assertion or software
implementation in either source. The complete source Magma listings remain
in the measured source even though that implementation is outside the
principal recovery contract.

Only exact repeated page furniture is removed: L008's alternating running
author/title headers and page numbers, its first-page number alone, and the
isolated trailing page numbers in all other documents. The arXiv banner
remains counted. Every removal has literal, page, offset and hash bindings.
No body-only span selection is used.

Counting and visible glyphs
---------------------------

The five units are whitespace tokens, alphanumeric units, non-whitespace
characters, characters after collapsing whitespace, and UTF-8 bytes after
collapsing whitespace. Each is computed after NFC and NFKC for all three
variants: full raw extraction, raw extraction after furniture removal,
and calibrated extraction after furniture removal. Printed discretionary
hyphens are retained; no reflow or dehyphenation alters counts.

The pinned parsers are pypdf 6.13.0 and FontTools 4.63.0. Each extracted
source character is aligned with its original text-showing event, actual
font dictionary and effective encoding, original encoded byte and glyph
outline or bitmap identity. Font-stream sharing never merges distinct PDF
font dictionaries. The source audit covers 34 dictionaries, 893 used
encoded glyph classes and 36,083 aligned visible decoded characters.

There are 217 occurrence-bound repairs: 87 in L008 and 130 in N016, with
none in the replacement PDFs. They identify the same visible glyph, not a
mathematical correction. In particular:

* L008 has 36 visible vertical delimiter extensions encoded as form-feed
  whitespace. They become U+23D0, rather than disappearing during whitespace
  collapsing. Oversized parentheses and their pieces remain individual glyphs.
* Intersection signs decoded as printable letters or a backslash, and
  mathematical script letters decoded as ordinary capitals, receive their
  corresponding visible Unicode symbols.
* N016 contains two bitmap bullets in a Type3 font on page 3. Their actual
  38 by 38 character masks and original byte 136 are bound. The bullets become
  U+2022; an empty ``page.images`` list is not evidence that a font lacks ink.
* Literal parser expansions of fi, fl, ff and ffi are retained. Correctly
  decoded primes, normal-subgroup signs, combining negation strokes, angle
  brackets and the diamond symbol remain unchanged.

All 36 pages, all 18 repaired glyph classes and all 33 Adobe-glyph-name
exception classes were visually inspected. Some glyph classes appear in
both panels. Exact font evidence, occurrence locators and class
reconciliation are exported; the original fonts, source text and images
are not. Full-page and outline views remain private. Formula positioning,
table rules and the application's small matching-edge displays have no
measured construction cost. This is an extracted-text coordinate, not a
whole-visible-layout measurement. Their unknown costs are not zero.

Programs, formal evidence and future comparisons
------------------------------------------------

The whole three-page appendix prints both complete files exactly once:
``chiral_cover.g`` is a required finite premise for the six-group example;
``reflection_models.py`` is a bounded diagnostic of the uniform reflection
formula. Neither is pruned. The raw complete two-file total is an alternative
to the printed appendix, never an addition to it. Two complete historical
operational drivers and the complete current driver are inventoried and
counted separately. No scientific program is rerun by this input audit.

The three complete Lean source files are a separate formal coordinate:
14 declarations, seven newly supplied and seven reused, with used and unused
interfaces retained exactly as in the accepted scope. These do not certify
the entire incidence geometry, string-rotation correspondence, retained
classification or finite GAP calculation. No Lean build is repeated here.

The first future comparison is the sum of both complete source manuscripts
divided by the whole common paper plus both whole applications. Including
the complete printed program is a separate comparison. Each conditional
source/application comparison assumes that the entire common paper and
both whole programs have already been acquired; the required and diagnostic
roles remain explicit. No overlapping theory is deducted because another
topic also uses it.

The retained Schulte--Weiss correspondence, specified
Cunningham--Pellicer families, source graphics, historical software and
operational engineering have unknown additional costs. The all-rank finite
minimal-cover question remains unresolved in the separate question map;
earlier answers concerning other cover scopes are not silently imported
as premises or new question credits.

Portable recount
----------------

Use a fresh absolute output directory and an interpreter with the pinned
parser versions. A public repository checkout and the two hash-matching
original PDFs suffice; no private proof bank is required::

  python3 -B -O extract_inputs.py \
    --public-root /path/to/human_compression \
    --source-L008 /path/to/chirality-test-v1.pdf \
    --source-N016 /path/to/cunningham-25-july-2023.pdf \
    --out /fresh/absolute/output

For the existing private source layout, replace the two ``--source`` options
by ``--sources-root /Users/sasha/medusa/research/leemans``. Output contains
only counts, hashes, audit metadata and controls. The replay checks 180 PDF
metric cells, 80 complete raw-file metric cells, the exact accepted scope,
public provenance, whole program inclusion and all glyph evidence. It also
rejects deliberate scope, program, glyph, event, dictionary, encoding,
whitespace, bitmap and furniture corruptions. It does not fetch any source,
run GAP, rebuild Lean, or calculate a factor.

``manifest.json`` is the export allowlist. Private preparation scripts,
full extracted texts, raster views, font/character programs and temporary
rendering files are deliberately excluded. The author counts and checks
are evidence of a proposed boundary, not independent acceptance.
