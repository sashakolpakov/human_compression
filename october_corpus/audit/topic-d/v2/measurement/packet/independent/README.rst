Topic D: independent review of measurement inputs
================================================

The corrected input edition is accepted. This is an acceptance of the counting
inputs, their boundaries and glyph identities; numerical compression factors
are a subsequent calculation. The original proposal remains preserved.

An independent recount re-extracted all eight complete PDFs and all 57 physical
pages. A separately written scanner reproduced 240 PDF metric cells, 48
normalized text hashes and 100 whole-program/driver metric cells. It did not
import the author's counting functions, although both implementations use the
pinned pypdf extractor. All titles, abstracts, references and acknowledgements
remain. All 56 omitted page-number/header spans were checked in rendered crops.

The font review found an error in the original proposal: fourteen square
brackets shared extracted private-use characters with brace pieces. The first
font evidence also overwrote distinct encoded glyph records. The corrected
edition binds every one of the 148 repairs to its actual PDF text event and
encoded byte. The independent checker aligns all 48,276 actual source glyphs,
checks all 21 calibrated encoded forms against embedded outlines, and confirms
that none of the actual source glyphs decode to whitespace. The correction
changes only two numerical cells: calibrated L066 UTF-8 length decreases by
28 bytes under both NFC and NFKC. Ordinary character counts are unchanged.

The root inspected the fifteen original glyph crops, the ten separately
rendered L066 extension-font outlines, all omitted furniture crops and five
complete source pages relevant to tables, front matter and diagrams. The prior
independent mathematical review and the input author inspected every complete
page; this review does not claim a second full-page inspection of all 57 pages.

The accepted mathematical edition and its 37 detailed source clauses are
unchanged. The complete appendix includes all five required programs and all
three diagnostics, once each. Their full raw files are an alternate accounting
representation. Both complete execution drivers are separately inventoried.
No code branch or diagnostic was pruned. Full source lengths are compared for
the accepted main-result contracts, with the L104 diagrams, Aut/Cor assertions
and doubling exclusions explicit. External proofs, catalogue construction,
graphics and historical software costs remain unknown.

The fresh run of the author's portable checker exactly matches its frozen
counts and rejects all twelve corruption controls. That is a replay of the
author's checks; the independent font analysis and recount are separate.
No new source or question credit, end-to-end Lean claim or ratio is admitted.

Reproduce the independent checks with the local source PDFs and public edition::

  python -B -O recount.py --proposal /study/topic_D_measurement_v2 \
    --study /study --public /repo --out /fresh/text.json
  python -B -O font_review.py --proposal /study/topic_D_measurement_v2 \
    --study /study --out /fresh/fonts.json
  python -B -O boundary_check.py --study /study --public /repo \
    --font-report /fresh/fonts.json --out /fresh/boundary.json

Use pypdf 6.13.0 and fontTools 4.63.0. Each output filename must be fresh.
The recount's status deliberately says that font and selection review is still
separate; the combined acceptance is recorded in ``review.json``. No primary
PDF, extracted manuscript, raster or embedded font is exported here.
