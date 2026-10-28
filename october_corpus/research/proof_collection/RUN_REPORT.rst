Finite certificates: completed replay
====================================

The checks recorded here were executed on 28 October 2026. The packet README
files preserve the earlier author handoff, when these runs were still pending.
This report records the subsequent execution and independent review.

The relative checkers use only files inside an explicitly supplied corpus
directory. Their original machine paths serve as provenance keys. All six
packet integrity checks passed, including the complete archived proof bodies.
Both interfaces passed seven control tests before their mathematical runs.

Results
-------

For the natural G2(11) model, the new relative checker independently verified
the two supplied words for each of 27 original markings. Each end subgroup
contains an element of order 37. The separately attributed written theorem
then excludes the intersection property. The faithful model, original orbit
and transporter data, and classified subgroup premises remain imports.
The check used 1,802 matrix products and read 4,320,430 bytes across 29 files.
This packet preserves the earlier 27 applications; it is not a register of
every later local computation on G2(11).

For one fixed endpoint in Fi22, all 78 formula runs passed and were joined
against their exact source, plan, certificates and disjoint intervals:

====================  =====  ==================  ====================================
Stage                 Parts  Original rows       Result
====================  =====  ==================  ====================================
Unordered triangles      31  500,178              89,069 unordered orbits
Partner involution       31  500,178              46,596 components; 4,123 fixed
Product orbit masses     16  500,178              Total mass 36,486,450
====================  =====  ==================  ====================================

There are 42,473 exchanged pairs, so 4,123 + 2(42,473) = 89,069 and
4,123 + 42,473 = 46,596. Each stage examines the same original owner index
set for a different formula. Fixed cases and nonfree orbits are retained.
The largest run read 8,293,597 bytes and used 5,484,416 work units; the
largest reported resident memory was 33,587,200 bytes.

The complete join is in verification/complete_fi22_replay.json. Its
independent review is verification/reviews/complete_join.json. The exact
results, complete execution captures and resource guard records for all
78 runs are preserved under verification/fi22/.

The named group, faithful action, original Reader and word calculations,
graph, global conjugacy class, two-fibre geometry, H=B premise and meanings
of the acquired input maps remain explicit imports. Generation, reversal
of the whole marking and the other endpoints remain to be established.
These finite checks add no complete manuscript, solved conjecture, Lean
proof or compression measurement.

Reproduce
---------

Replace /ABS/october_corpus below with the canonical absolute directory of
the October corpus in a clone. Python must have little endian native
integers for the Fi22 typed arrays. The mathematical checkers use the
standard library. Their own read, work, time and memory checks remain active.

The complete relative input inventory is collection.json. Reproduction
commands, including controls, are in:

* `G2(11) replay <../groups/two_unitary_ends/replay/README.rst>`_
* `Fi22 replay <../fi22/triangle_quotients/replay/README.rst>`_

The Fi22 first_calls.json lists all 78 calls with a placeholder corpus
directory. Run each listed stage and part with the same source and plan.
The packet contains the original arrays and supplied certificates needed
for every call. Inspect their premises alongside the written arguments.

Verify the additional records in this report with:

::

    python3 -E -B -S /ABS/october_corpus/research/proof_collection/check_integrity.py \
      --corpus-root /ABS/october_corpus \
      --manifest research/proof_collection/verification/manifest.json \
      --manifest-sha256 e2236aa3d19138b581e3a0d1df1b919f22d72dcca1111e97e73d4153e583a880 \
      --self-sha256 d84128ef725e52650330c68b31109ded146da00712b96d5a8740d17492af37fb

That manifest maps all 416 preserved execution and review files by full
content identity. Its integrity check authenticates those files. The
relative mathematical commands perform the arithmetic checks themselves.
The archived join script and its historical absolute paths document the
recorded execution; the relative mathematical interfaces provide the
commands for a new clone.
