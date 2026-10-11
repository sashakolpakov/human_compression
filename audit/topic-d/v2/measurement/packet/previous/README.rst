Topic D: measurement inputs
===========================

This packet proposes counts for the complete three-source Topic D edition.
The proofs and 37 source clauses are already independently accepted. Numerical
measurement still requires independent input review; no factor is calculated
here. The counting policy was fixed before extraction in ``policy.json``.

Written papers
--------------

The first proposed comparison is the sum of the three complete historical
manuscript lengths divided by the whole common paper and all three applications.
The source sequence is L066 -> D1, L074 -> D2, and L104 -> D3. The source PDFs
have 9, 12 and 5 pages. Our common paper has 6 pages and the applications have
5, 6 and 2 pages. The whole common paper is charged within this topic, including
material also used in another topic.

A per-source comparison uses that whole source manuscript over its application,
after acquiring the whole common paper and the complete programme boundary.
It does not assign a fraction of the common paper to a convenient local result.
Full manuscript length is the intended numerator for the accepted main-result
contracts, with their qualifications explicit; this does not assert that every
printed auxiliary statement has been replaced.

Including the program
---------------------

The complete 12-page printed appendix is a separate cost coordinate. It includes
all five required mathematical programs and all three complete diagnostics.
Its text is added once to the written-paper denominator in that comparison.
The eight whole raw files give an alternative representation, never an addition
to the printed appendix. No diagnostic portion is removed. Both whole execution
drivers are inventoried and counted separately; they are absent from the
printed appendix. The historical M22 branch in one driver remains in those
raw driver counts, although it is not selected by these applications.

What the counts mean
-------------------

All eight physical PDFs and all 57 pages are included. Titles, abstracts,
acknowledgements and references remain. Exact repeated running headers and
page numbers are the only furniture removed. The first-page journal information
of L104 remains. The inputs preserve three variants: raw untrimmed, raw selected
and calibrated selected. Each has NFC and NFKC counts in five units. Printed
hyphens, accent spacing, formula pieces, ordering and literal source mistakes
are not silently corrected.

There are 148 calibrated occurrences in 15 font/glyph classes. The mappings use
these PDFs' own embedded Type1/CFF fonts and rendered pages. All mappings are
bound to their exact font, page, offset and context hash. The source text
operators contain no actual whitespace glyphs, so extracted spaces and newlines
are preserved as layout. Enlarged private crops and all 57 complete page renders
were inspected. No primary PDF, source text, raster or embedded font is exported.

This is extracted text, not a reconstruction of every visible mark. The J2
figures retain extracted labels and font-drawn circles/diagonals, while vector
edges and graph placement remain unpriced. Table rules and formula placement
also have unknown cost. Unknown external classical proofs, subgroup catalogue
construction, exact algorithm implementations and graphics are not assigned zero.
The historical software cost is likewise unknown.

The accepted source boundary is in ``source_contract_boundary.json``. In
particular, the J2 principal census is recovered, but the printed diagrams,
complete Aut/Cor groups, doubling relation and supplement annotations are not
all recovered. Their original extracted text stays in the complete-source
numerator. The L066 reversal and regular-polyhedron qualifications and L074's
retained classical structure remain explicit. No M22 application is included.

The ten scoped Lean declarations belong to separately reported formal
validation. They do not formalize every source application or the completeness
of the external catalogue. A later support-count formal supplement is outside
this initial proof boundary.

Portable reproduction
---------------------

Use Python with pypdf version 6.13.0. Supply the three primary PDFs locally at
the paths and hashes in ``source_input_spec.json``. Supply our bound edition
privately or use its public mapping::

  python -B -O extract_inputs.py --study-root /path/to/private/study \
    --public-root /path/to/human_compression --out /fresh/output

Omit ``--public-root`` to use all bound private paths. The output directory must
not exist, including as a symlink. The runner re-extracts every page, checks fonts
and occurrences, checks all whole program/driver hashes and saves only counts
and hashes. It also runs ten rejection controls. It does not execute the census,
recompile Lean, calculate ratios, contact anyone or distribute source text.

``author_counts.json`` is the author's fresh result. ``portable_replay.json``
records a separate replay of the exported scripts and metadata. Both are input
validation records, not an independent numerical admission.
