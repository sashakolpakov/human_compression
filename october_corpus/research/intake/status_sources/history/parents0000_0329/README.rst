Sources for the current intake counts
====================================

The four gzip files preserve the exact intake, controller, runtime and F004
job 20 selector editions used by the current status page. ``manifest.json``
joins each original byte length and SHA256 to its compressed byte length and
SHA256. The original absolute paths are provenance labels; the reader never
opens them. Compression changes no expanded byte.

From the repository root::

    python3 -E -B -S october_corpus/research/intake/status_sources/verify.py

The reader verifies all four expanded and compressed hashes, checks the
controller/runtime and intake/selector pointer joins, compares active counters
between intake and runtime, and prints their exact values. It refuses ``-O``.
Each expanded file is limited to 4 MiB and all expanded files to 16 MiB;
compressed reads have the same bounds. Its metadata checks use a 125 second
timer and a 256 MiB RSS check. It writes no extracted files or compiler cache.

The saved metadata also contains earlier prose, counters and cache records.
They remain unchanged. The reader selects the active fields recorded in the
manifest rather than treating every historical field as current. The L026
CURRENT digest is a pointer shared by these source editions; the bank and
its full mathematical dependency closure are not supplied by this package.

This is a source and status check. It does not repeat a matrix, permutation,
group or graph calculation, complete an unfinished manuscript, or provide
full portable mathematical replay. The adjacent ``proof_methods`` archive
preserves a separate finite selection of proofs and execution evidence; the
corpus reproduction guide lists existing portable mathematical entry points.
