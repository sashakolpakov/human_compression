Independent acceptance of Topic C measurement inputs
===================================================

The complete PDF extraction and font calibration are accepted for subsequent
arithmetic. The independent recount agrees with all 270 PDF metric cells,
54 normalized text hashes and twenty metric cells for the two complete raw
programs. It calculates no compression factor.

The measurement includes three available original PDFs, the complete common
paper, all four applications and the complete printed program appendix.
The original L108 PDF remains unavailable; its authored browser text is
checked against the mathematical edition but is not used as a substitute
numerator. C3 remains in the complete denominator. The raw program files are
an alternative representation of the printed code, not an additional cost.

The checker imports none of the author's extraction, calibration or counting
functions. It shares pypdf 6.13.0, re-extracts all 64 physical pages, checks
the full text and physical-page hashes, and uses a separate character scanner
for the five units under NFC and NFKC. Exact repeated furniture is removed;
title, abstract, bibliography, acknowledgements and article text remain.
Ten corruption controls reject shortened boundaries, altered glyphs, omitted
aliases, invented whitespace events and inexact furniture removals.

The 79 proposed font groups were checked against the actual embedded font
programs: CFF encoding tables for L088, and Type 1 encoding names with the
PDF character map for F014. In addition, all 12,615 selected non-whitespace
L088 occurrences were checked against their CFF glyph identities, including
printable characters outside the correction list. There were no additional
discrepancies or unidentified glyphs. This font check uses fontTools 4.63.0.

I directly inspected twelve complete rendered source pages: L088 pages 1,
3, 4, 9 and 10; F014 pages 6, 8, 9 and 10; N013 pages 1, 4 and 6. These cover
the navigation furniture, representative formulas and diagrams, the three
TeX zero aliases, extended delimiters and the four corrected glyphs that
extract as spaces or a newline. The author's separate record covers all
33 available source pages. This review does not claim another complete
visual reading of those 33 pages or a new review of the mathematical proofs.

The four whitespace-looking F014 occurrences are matched to exact visitor
callbacks, their fonts, page positions and context hashes. Ordinary generated
layout remains whitespace. Mathematical pieces are kept separate; neither
equations nor diagram incidence are reconstructed from their text stream.
Outside proofs, graphics, formula layout and the missing PDF have unknown
costs. Formal proof coverage and the full census remain those of the already
accepted mathematical edition; neither is rerun in this counting review.

Reproduce with the immutable input proposal and local primary sources::

  python3 -B -O recount.py --study-root PRIVATE_STUDY \
    --public-root PUBLIC_REPOSITORY \
    --proposal PRIVATE_STUDY/topic_C_measurement --out FRESH_DIRECTORY

No primary source text, PDF, font stream or raster is exported here. The
review introduces no new recovered-result or solved-question credit.
