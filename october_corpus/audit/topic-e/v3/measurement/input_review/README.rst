Expanded Topic E: independent measurement-input review
======================================================

Accepted input boundary, with one nonblocking historical-software attribution
clarification in source_software_review.json. The author input freeze is
preserved. No ratios, new scientific credit or formalization claim is made.

The distinct recount verifies all 390 PDF and 250 raw-file metric cells,
256 text hashes, actual source font dictionaries/glyph occurrences and whole
program inclusion. It shares only the reviewed low-level embedded-font parser;
it imports none of the author metric, selection, calibration or event-alignment
implementations. The separate scope checker rejects 27 semantic corruptions.

Reproduce with Python 3 and the pinned pypdf/fontTools dependencies:

  python -B -O recount.py --packet /path/to/topic_E_expanded_measurement_inputs --study-root /path/to/leemans --out /fresh/recount.json
  python -B -O check_scope.py --packet /path/to/topic_E_expanded_measurement_inputs --study-root /path/to/leemans --out /fresh/scope.json

The copied-author replay is additional evidence, not a substitute for the
independent recount. It rebuilds the three-page reader, checks all 24 author
controls and uses only the 38 exported files plus explicitly bound source and
scientific inputs. Primary PDFs, extracted full text, fonts and rasters are not
included in this review. Exact prior scientific and bibliography reviews are
reused transparently; unchanged mathematics was not executed again.

Fresh visual scope: all 34 older-source pages, 31 actual outline classes and
three reader pages. Earlier exact full views of the 33 newer-source pages and
61 scientific/code pages are reused with the accepted bibliography overlay.
All five original manuscripts and all six replacement scientific papers remain
whole. No partial or complete executable listing was found in any source.
Historical unavailable software and full graphical costs remain unknown.
