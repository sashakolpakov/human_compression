Topic C: proposed measurement inputs
===================================

This packet counts the complete available source PDFs and the accepted Topic C
papers. It is a proposed input boundary, awaiting independent review. It reports
no factor and makes no new source or conjecture claim.

There are three available source PDFs, with 33 physical pages; five scientific
replacement papers, with 27 pages; and a complete required program appendix,
with 4 pages. The L108 original PDF is missing. Its cost and the complete
four-source PDF factor remain unknown, while its four-page application C3
remains charged.

The published edition is commit 87757bf40a3514d592854a0ac662121cafa70205.
Every replacement PDF is checked against its exact frozen/public hash.

Replay
------

Use Python with pypdf version 6.13.0. Supply the three original PDFs locally;
this packet does not redistribute them. The study-root layout is given in
source_input_spec.json. A fresh output directory is required::

  python -B -O extract_inputs.py \
    --study-root /path/to/private/study \
    --public-root /path/to/human_compression \
    --out /fresh/output

Without --public-root the exact replacement files are read under study-root.
The runner records all 270 PDF metric cells: three variants, two Unicode
normalizations and five units for each of nine documents. The two complete raw
programs are counted separately as an alternative to the printed appendix.
Five deliberate calibration mutations must be rejected.

What is counted
---------------

The whole source manuscripts are included: titles, abstracts, acknowledgements,
references and unique frontmatter. Only exact repeated running furniture,
page numbers and L088's electronic-reader navigation/sidebar are removed.
The raw untrimmed, raw selected and calibrated selected coordinates remain
visible. No dehyphenation or correction of a source theorem is performed.

L088 has 941 exact glyph substitutions and F014 has 184. Each substitution has
a font, physical page, offset and context hash. The CFF font names and visible
page checks justify printable aliases as well as control characters. Four
F014 whitespace-looking mathematical glyphs also have exact visitor-event
locations, distinguishing them from generated layout whitespace. N013 and the
replacement PDFs require no declared substitutions. Delimiter and edge pieces
are never merged; ligatures are handled explicitly by NFC/NFKC sensitivity.

Whole-topic acquisition charges the complete common paper and all four
applications, with the complete program appendix once. A later local factor
would compare a source with its application after acquiring the whole common
paper and both complete programs. No overlap with another topic is deducted.

Limits
------

These are extracted-text counts, not a reconstruction of all visible content.
L088's incidence diagrams, N013's diagrams and the positioning of F014's
matrices/formulas have unmeasured graphical cost. No such page is deleted and
no missing graphic cost is assigned zero. Required external results and
catalogue construction also remain unmeasured. Lean validation is reported
separately; it does not certify every geometric assertion of the volume.

The accepted main-result contracts, literal source corrections and explicit
exclusions remain those recorded in reader.json and the accepted C scope map.
In particular F014 Conjecture 3.7 belongs to the separate question track.
Full manuscript length is the intended source coordinate for these main-result
contracts; it does not assert recovery of every auxiliary statement.

Publication allowlist
---------------------

Only files listed in manifest.json are proposed for later distribution.
Primary PDFs, extracted primary text, raster pages, private preparation scripts
and conversion intermediates are not exports. Visual-review metadata gives
private page paths for the independent reviewer; no raster is included.
