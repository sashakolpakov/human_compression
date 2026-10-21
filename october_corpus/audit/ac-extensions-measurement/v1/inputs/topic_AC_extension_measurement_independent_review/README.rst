Independent input review: additions to Topics A and C
====================================================

Accepted exact input boundary e1af6ba206bf6e0870501ea38f4c909eead33cee0590398a52f84b621d5a1028.
No compression factor or new scientific credit is assigned here. review.json
records roles, the full existing-topic closure and representation limitations.
The author packet stays unchanged. Primary PDF/text/font/image bytes are not
included in this review.

Replay from this directory or any copied review packet::

  python3 -B -O check.py --packet /path/to/topic_AC_extension_measurement_inputs \
    --public-root /path/to/math_compression --sources-root /path/to/leemans \
    --out /fresh/output --author-replay --render --xelatex /path/to/xelatex

Requires the pinned pypdf 6.13.0 and fontTools 4.63.0 environment, the exact public
files and the two privately supplied primary PDFs under sources/. For a bounded
independent recount without rebuilding, omit --author-replay and --render.
The full replay creates an export-only author copy (27 exports plus manifest),
then runs its unmodified checker. The new two-page reader and whole five-page
program appendix reproduce their complete page text. It does not execute GAP or
Lean. All 290 metric cells and 58 normalized text hashes match; 18 independent
semantic corruptions and 36 original author controls are rejected.

recount.py implements its own full-page selection and state counters without
importing author counting code. font_recheck.py independently traverses actual
content streams and checks all 36 dictionaries/805 encoded classes; it reuses
the explicitly reviewed low-level font decoder, not the author's event alignment.
Neither is an independently implemented PDF renderer. The separate visual
record documents all 48 physical input pages, two reader pages and 56 outlines;
private raster paths are evidence locations, not replay prerequisites.

Technical format reference: Adobe Technical Note 5176, section 13/Table 22,
https://adobe-type-tools.github.io/font-tech-notes/pdfs/5176.CFF.pdf . The omitted
non-CID charset has default zero (ISOAdobe); explicit PDF MacRoman/WinAnsi
encodings and Differences still govern the actual byte-to-glyph mapping.

Scope and roles: this agent previously reviewed L128 mathematics and authored
the current L068 TeX edition. This measurement review reuses the distinct bound
scientific acceptances; it does not claim a new independent proof review of that
L068 authorship. External/graphic costs remain unknown, shared files are charged
once within each topic, and the full earlier topic inputs remain paid.
