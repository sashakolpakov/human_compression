Independent review of operations measurement inputs
=================================================

Root accepts the complete input boundary and all 770 scalar counts for the three
originals N005, N006 and N007. This permits subsequent numerical comparisons; it
does not itself admit a factor, an original manuscript, or a solved question.

The independent recount imports no author code. It reuses the earlier root
recount method, extends it to the full N005 manuscript and current common theory,
and compares every complete PDF and raw-file coordinate. The font/event decoder
was read and freshly replayed separately; that decoder is not independently
reimplemented. Review independence is from the measurement author, not from all
prior project work.

Run, with Python containing pypdf6.13.0 and exact scientific/source inputs::

  python3 -B -O recount.py --author /path/to/frozen/input/packet \
    --sources-root /path/to/research/leemans \
    --public-root /path/to/math_compression --out /fresh/output

All source PDFs, extracted body text, glyph programs and raster images remain
private. The review records their identities and inspection scope only.
