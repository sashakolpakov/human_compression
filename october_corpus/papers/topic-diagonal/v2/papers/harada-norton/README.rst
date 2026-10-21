Harada--Norton additive certificate
==================================

This packet supplies the HN case lying within the literal scope of N006
Theorem 5.3 but omitted from its nine-case proof discussion. The two saved
markings have product orders (12,2,5) and (12,12,5). The nine-case packet
``corpus161_N006_sporadic`` remains immutable; this packet is an addition.
Both Fischer exceptions remain outside the recovered assertion. No priority
or new-question credit is asserted.

Replay
------

With Python 3 and GAP 4.15.1 with CTblLib 1.3.11::

  python3 -B -O check.py --out /fresh/absolute/path --atlas-root /path/to/atlas/files

The Atlas directory must contain the two original binary files named in
``retained_inputs.json``. They are not distributed here. Their total size is
18,240,024 bytes. The replay verifies both hashes, decodes the complete
permutations, verifies every image is used once, and writes generated GAP
inputs only to the new output directory. No random search is run.

The decoder interprets the verified twelve-byte header (-1,1140000,1) as
little-endian signed 32-bit integers, followed by 1,140,000 little-endian
unsigned 64-bit images. The decoded representation is an alternative to
the same binary input, not additional mathematical data to charge twice.

The complete local checker tests all 49 proper-subset intersections for
each marking. The fifteen pairs containing the full subset are immediate
subgroup identities, explained in the paper. Each of the six flag equations
is tested as an actual product-set inclusion; the reverse inclusion is an
elementary identity. The full ambient permutation group is never enumerated.

Generation uses the actual outer generator and two saved words of exact
orders 11 and 19. The complete thirteen-entry maximal-subgroup classification
is retained explicitly. All names and orders are recorded and checked; the
CTblLib files and indices used are hash-bound. This is not a classification
proof or an identification of a group merely by its order. The Atlas named
representation and the location of the outer involution are retained too.

Programs and validation
-----------------------

``programs/local_geometry.g`` and ``programs/verify_hn.g`` are complete
mathematical verification programs; ``witnesses/HN_compact.g`` contains all
word data. The entire ``check.py`` driver and binary decoder are retained.
The twelve controls cover malformed data, the generation interface, wrong
markings, IP without flag transitivity, the halving exponent and GAP errors
with a zero process exit. Existing output paths and dangling symlinks are
refused. Each frozen export is checked before replay.

Search programs and their logs remain private construction history. They
are not needed to verify the fixed witness. No Lean declaration is claimed.
Full classification proofs and external software/data costs remain visible
retained inputs, not zero costs. The four-page note and all complete programs
belong in the full N006 application boundary; no numerical comparison is
made here.

The author finite replay and negative-control reports are saved under
``author_replay``. Independent review and admission are separate steps.
The exported manifest deliberately omits all external primary/Atlas files,
decoded million-point permutations and search traces.
