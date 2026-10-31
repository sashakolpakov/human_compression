Ten polynomial obstructions in G2(11)
=====================================

The verifier replays ten identities e = f(ab) over F_11. Each polynomial
has seven recorded coefficients. It checks all 49 matrix entries by
Horner evaluation, and verifies that ab has exact order 33 or 55 by
repeated multiplication and every proper prime-divisor test.

From the repository root::

    python3 -E -B -S october_corpus/reproduction/polynomial_prefixes/verify.py --controls
    python3 -E -B -S october_corpus/reproduction/polynomial_prefixes/verify.py --replay

Python 3.9 or later on Linux or macOS and the standard library suffice.
Run without -O. Results are written to standard output. The consumer opens
only four flat local files: its Source, manifest.json, prefixes.json and
certificates.json. Every opened file is rehashed at the end. It performs
no coefficient search or elimination. SOURCE_REUSE.json records the thirteen
complete definitions copied from the independent certificate consumer.
This portable Source has passed 24 bounded controls and the complete ten-prefix
replay. REPLAY.json records the actual execution of this edition.

The common argument
-------------------

Let G be the admitted natural split G2(11), acting faithfully on its
seven-dimensional pure Cayley space. Suppose a, b and e are the recorded
nonidentity involutions, e commutes with a and b, and e = f(ab). Every
ab-invariant subspace is e-invariant, and every operator commuting with
ab commutes with e.

The imported complete maximal-subgroup cover consists of the two
parabolics, the two full quadratic-line stabilizers, involution
centralizers, and four exceptional types. The exceptional types contain
no element of order 33 or 55. Consequently every maximal proper subgroup
containing a and b also contains e. For any fourth mark c, if <a,b,c> is
proper, all four marks lie in a proper subgroup. If <a,b,c> = G, the
nonidentity e belongs to that end, violating the intersection property.
The conclusion is therefore nongeneration OR intersection-property
failure. The replay does not separate these alternatives.

theory.tex gives the complete argument and its references. IMPORTS.rst
states the group, representation, original-frame, membership, maximal-cover
and subgroup-spectrum premises. The runtime matrix equalities do not
establish those imported results.

The ten applications
--------------------

The original comparison is Malcolm Hoong Wai Chen, Abstract regular
polytopes of G2(q) in even characteristic, arXiv:2609.25004v1,
21 September 2026, Table 2, p. 11:
https://arxiv.org/abs/2609.25004v1
The construction concerns even characteristic; Section 4 gives a census for
every prime power 3 ≤ q ≤ 11. We use its q = 11 census entry.
The table reports 105 rank-four classes for q = 11 up to isomorphism
and duality. The present ten-prefix exclusion is one part of that census.

The original rank-four prefix numbers are 156, 160, 166, 167, 168, 170,
174, 175, 183 and 187. The matrices are ordered a, e, b, with original
labels 1, 4, 2 and the original right-row convention. Their literal entries
agree with the existing prefix_centralizers package. The exact order is
33 for prefixes 168 and 170 and 55 for the other eight.

The accepted whole-prefix argument covers 74,330 original positions:
1,030 previously accepted nongenerating positions and 73,300 positions
covered by this disjunctive argument. These are the ten local partitions;
they give no net-new global paid-position count. The previous per-position
branch labels are preserved. The broader intake currently has 125 closed
F004 jobs and 147 pending jobs; this replay concerns these ten prefixes.
It establishes no positive-classification count, whole-original recovery,
conjecture solution, Lean theorem or measured compression ratio.

Limits
------

One invocation retains the 400,000 matrix-product, 200,000 separate
scalar-addition, 128 MiB memory, 100-second internal and 8 MiB input limits.
Each local file is below 1 MiB, and the path limit is 96. Stdout is bounded
by 128 KiB. The independent replay requires exactly 802 matrix products
and 420 diagonal additions: eight order-55 certificates cost 85 products
each, and two order-33 certificates cost 61 each. The actual replay matched
those counts, read 58,716 bytes across five paths, and returned all ten
certificate records exactly as in the accepted independent proof. The 24
controls used 233 products and eight diagonal additions. The external
128 MiB, 125-second guard recorded 0.049 seconds and an observed sampled
RSS peak of 28,065,792 bytes for the replay; its known-process cleanup
lists were empty. The guard's memory samples are observations, not an
exact allocation maximum.
