Independent review of Topic F measurement inputs
================================================

The fixed input proposal is accepted within its extracted-text boundary. This
packet calculates no compression factor and makes no new mathematical claim.

``recount.py`` independently reads the four complete PDFs, checks each page and
furniture cut, aligns the primary's printed characters with actual text bytes
and embedded font encodings, applies the visually reviewed occurrence repairs,
and reproduces all 120 PDF metric cells and 60 separate raw-file cells. It does
not import the author's extraction, calibration or metric functions. It shares
the explicitly pinned pypdf 6.13.0 and fontTools 4.63.0 parser dependencies.

From a study root containing the exact bound inputs::

  python -B -O topic_F_measurement_input_review/recount.py \
    --study-root /path/to/study --out /fresh/recount.json
  python -B -O topic_F_measurement_input_review/controls.py \
    --study-root /path/to/study --out /fresh/controls.json

The optional ``--packet`` argument relocates the immutable author proposal.
Primary PDFs, extracted primary text, font programs and rasters are not exports.

The source includes printed assertions outside the admitted principal contract;
full-document length does not imply that every auxiliary assertion was recovered.
The three complete programs remain validation, not premises of the uniform
proofs. Their printed appendix and full raw files are alternative representations.
The two drivers and one scoped Lean file have separate counts. Retained external
proofs, source graphics/layout and historical computation costs remain unknown.

The reviewer authored inherited phase236 mathematics. This measurement review
reuses the distinct phase248/current F independent acceptance and root adoption;
it does not independently re-adjudicate that inherited mathematics. Current
input authorship, font classification, allocation policy and counts were checked
independently here. See review.json for exact roles, bindings and limitations.
