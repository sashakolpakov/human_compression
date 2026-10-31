Finite matrix certificates for 1,595 original quartets
======================================================

This package verifies 1,322 failures of the intersection property and
273 nongeneration certificates from original job 24 in the acquired
natural matrix model of G2(11). From the repository root run::

    python3 -E -B -S october_corpus/reproduction/matrix_certificates/verify.py

Python 3.9 or later and its standard library suffice. Do not use -O.
The program reads five supplied JSON files, checks their complete hashes,
and writes its result to standard output. It needs no private source tree.
Absolute paths retained inside the original data are provenance only.

This edition passed its first guarded execution on 31 October 2026:
1,595 certificates, 102,923 matrix products and 1,245,951 charged input
bytes in 2.43 seconds. The observed process memory stayed below 60 MB.
REPLAY.json records the code identity, actual result and execution limits.
The earlier 285-case edition is preserved in the Git history.

Proofs and scope
----------------

For every intersection obstruction, an explicit word in one actual end
has a cofactor power of exact order 37. A generator of that same end moves
its fixed line. The imported complete maximal subgroup classification
then forces the end to equal G. Its intersection with the subgroup of
the omitted nonidentity mark violates the intersection property.

The 12 inherited cases retain their recorded word matrices and an
independently computed fixed row. For the 1,310 newly adopted cases, the
program checks the supplied nonzero fixed row and a supplied minor of
order six in Y-I by a 720-term Leibniz determinant. These prove rank six
without additional row reduction. Determinant work has a separate counter;
the 200,000-operation RREF cap is unchanged and never reset.

For each of the 273 nongeneration cases, all four marks preserve a line
and a known ambient group element moves it. Their subgroup is proper.
This argument uses no maximal subgroup classification.

THEORY.rst gives the proofs and references. The original group and model,
faithful frame, membership and orbit associations remain imported. This
replay does not repeat the original point-action bridge, identify the
named group or finish the positive classification. The seven separate
conditional generation facts are not among these 1,595 exclusions.

The accepted snapshot has 2,684 additional exclusions: 2,411 intersection
failures and 273 nongeneration cases, with 922 positions unresolved. The
earlier 1,089 exclusions remain in their historical archives; this package
covers the other 1,595. It adds no completed manuscript, open conjecture
result, Lean verification or compression measurement.
