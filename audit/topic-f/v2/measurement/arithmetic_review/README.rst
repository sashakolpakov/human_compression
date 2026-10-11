Independent Topic F numerical and reader review
==============================================

The root-authored numerical packet is accepted within the previously fixed
extracted-text boundary. ``arithmetic.py`` independently reconstructs the
complete denominators, reduces all fractions using integer gcd, and checks
twelve-place decimals using Decimal arithmetic. It does not import the
author's builder or Fraction-based calculation. All thirty coordinates and
120 fractions agree; twenty-one semantic corruptions are rejected.

Reproduce against the four frozen packets::

  python -B -O arithmetic.py \
    --inputs /path/topic_F_measurement_inputs \
    --input-review /path/topic_F_measurement_input_review \
    --input-adoption /path/topic_F_measurement_input_root_adoption \
    --result /path/topic_F_measurement_numerical/measurement.json \
    --out /fresh/independent.json

The author's independent fresh reader build used::

  python -B -O /path/topic_F_measurement_numerical/build.py \
    --inputs /path/topic_F_measurement_inputs \
    --input-review /path/topic_F_measurement_input_review \
    --input-adoption /path/topic_F_measurement_input_root_adoption \
    --out /fresh/render --xelatex /path/to/xelatex

That replay regenerated the JSON, TeX and two vector charts byte for byte,
and both reader pages have identical extracted text. Both pages and the
standalone chart were visually read. The PDF's volatile production metadata
is not claimed byte-identical. See reader_replay.json for exact comparisons.

The reviewer independently reviewed the earlier input proposal; root then
adopted it and authored this numerical packet. This review checks the new
arithmetic, presentation and build, reusing the accepted inputs. It performs
no further primary extraction, mathematical adjudication or GAP/Lean replay.
Prior contributions to inherited mathematics do not become self-acceptance
of that mathematics here.

Whole written comparison comes first. The complete validation appendix is
reported separately, with the three raw programs as an alternative, never
an additional charge. The conditional application figure prepays the whole
common theory and complete validation package. Two drivers and one Lean
file remain separate. Retained proof, graphics/layout and historical software
costs remain unknown. These are text-length comparisons, not minimum proof
complexity or total research effort. One application supplies no recurring
sawtooth evidence. No source, question or formal credit is added.
