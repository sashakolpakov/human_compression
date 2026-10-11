Chamber measurement inputs: independent review
=============================================

The frozen author input packet is accepted without correction. This is an input
review, not a numerical factor or new mathematical admission. The reviewer
authored the Chamber scientific edition; its separate scientific acceptance by
enumeration_review and root adoption remain authoritative.

Replay in a fresh directory::

  /Users/sasha/.venvs/global/bin/python -B -O check.py \
    --study-root /Users/sasha/medusa/research/leemans \
    --public-root /Users/sasha/medusa/math_compression \
    --out /private/tmp/chamber-input-independent-fresh

The checker independently reconstructs source glyph bytes, actual PDF font
dictionaries and outlines, all occurrence repairs, whole-page selection and
180 PDF plus 80 raw-file measurements. It rejects 27 scoped semantic corruptions,
including 12 actual-glyph corruptions evaluated beyond the manifest hash gate.
No primary text, embedded font or raster is exported. No GAP or Lean rerun is
needed for this bounded extraction review. See review.json for exact limits.
