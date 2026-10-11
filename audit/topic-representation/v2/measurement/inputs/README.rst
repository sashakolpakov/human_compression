Representation: measurement inputs
=================================

This proposal fixes the input boundary and reports counts only. It does not
admit or calculate a compression factor. Independent extraction, font and
boundary review must precede that step.

The source is the complete thirteen-page arXiv:2511.02410v2 manuscript by
Antonio Díaz Ramos, Rémi Molinier and Antonio Viruel. Its title, abstract,
acknowledgements, bibliography, author addresses and original arXiv banner all
remain counted. Only the first-page numeral and twelve exact running headers
are removed. Source statements are measured as printed, including the three
qualifications in the accepted scientific contract. The source already answers
its Question 2.4; this project does not claim a new answer.

The current edition contains the whole five-page common paper, whole five-page
application and whole four-page appendix. All pages count, including the common
paper's short references page. Only their trailing page numerals are removed.
The first intended comparison is the complete source divided by the complete
common paper plus application. A separate comparison includes the complete
printed appendix. Both whole raw validation files form an alternative to that
appendix, never an addition. The conditional source/application comparison is
after acquiring the whole common paper and complete validation package.
Neither program is a premise of the uniform written proofs.

Both archival drivers and both full Lean files are inventoried separately.
The latter contain eight generic restriction declarations and four reused local
hexagon declarations. They do not formalize the full geometric construction.
The scientific scope retains all six source blocks and thirteen proof contexts,
with no new source or question credit. The independent scientific review and
its exact role correction remain bound.

Extraction and calibration
--------------------------

The fixed ruler uses pypdf 6.13.0 and FontTools 4.63.0. Every PDF is counted in
three variants: raw, raw after exact furniture removal, and calibrated after
that removal. Each is reported in NFC and NFKC under five units: whitespace
words, alphanumeric runs, non-whitespace characters, characters with collapsed
whitespace, and UTF-8 bytes with collapsed whitespace. Line-end hyphens and
printed code-continuation arrows remain. There is no prose correction, formula
rearrangement, dehyphenation or OCR substitution.

All 566 actual source glyph classes are reconciled against their actual PDF
font dictionaries, effective encodings and embedded outlines. The 134 changes
cover fourteen visible aliases. They include braces and parenthesis pieces,
a script G, square-union signs and wide tilde accents extracted as letters.
Three right braces on page 8 are decoded tabs: their exact byte-9 text events
are distinguished from real whitespace. Four mapsto vertical strokes remain
separate from their adjacent right arrows. No formula is merged. Actual spaces
and generated whitespace are otherwise preserved. The unembedded standard
Times-Roman font belongs only to the original identification banner; no
embedded outline is claimed for it. Literal decoded ligature expansions remain
unchanged, with normalization sensitivity explicit.

Every source page and all fourteen current pages were visually inspected.
The source contains vector figures on pages 5, 7, 9, 10, 11 and 12, with
extractable labels. Edges, vertex positions, colors, dashed curves and formula
placement are not text. Their cost remains unknown; absence of raster images
is not absence of graphical content. This is a complete-PDF extracted-text
coordinate, not a complete graphical-description cost. External proof,
historical program and operational engineering costs likewise remain unknown.

Replay
------

Use the original source and exact accepted packet already in the private study.
Only metadata, scripts, bindings and count reports are exported::

  python -B -O extract_inputs.py \
    --study-root /path/to/research/leemans \
    --public-root /path/to/human_compression \
    --out /fresh/representation-inputs

The output rechecks all original bytes, exact page/furniture/glyph events,
complete font evidence, all 120 PDF metric cells, sixty separate raw-file
metric cells and 23 deliberate corruptions. It runs neither GAP nor Lean.
The font_view.py command can render the exact source outline evidence privately;
its images and all full source text remain outside the export manifest.
