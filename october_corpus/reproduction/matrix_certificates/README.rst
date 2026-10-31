Finite matrix certificates for 2,308 original quartets
======================================================

This package verifies 2,035 failures of the intersection property and
273 nongeneration certificates from original job 24 in the acquired
natural matrix model of G2(11). From the repository root run::

    python3 -E -B -S october_corpus/reproduction/matrix_certificates/verify.py

Python 3.9 or later and its standard library suffice. Do not use -O.
The program reads six pinned local JSON files and writes its result to
standard output. It opens no private or historical absolute path.

The exact 2,308-case verifier passed its first guarded replay in
2.915 seconds. It read 1,391,673 bytes of pinned input, used 145,447
matrix products and 16,989 RREF field operations, and checked 943,200
determinant terms. The outer guard observed a peak of 62,291,968 bytes
against its 128 MiB limit and returned PASS within its 125-second limit.
REPLAY.json records the published execution and exact verifier edition.

What is retained and what is added
----------------------------------

Every earlier case is retained unchanged: 1,322 intersection failures and
273 nongeneration certificates. The successor adds 711 obstructions from
a shared centralizer and spectrum argument, one order-19/order-4 case,
and one order-19 case with an 8,779-line orbit certificate.

For the 711 spectrum cases, the verifier reconstructs the original marks,
checks all three supplied centralizer commutator witnesses, and verifies
the exact adjacent product order using all proper prime-divisor tests.
It recomputes the eight common prefix sign-system ranks once. Each new
left end is then checked to move all three possible common prefix lines.
The full centralizer identity, finite Levi structure and maximal subgroup
classification remain explicit borrowed premises; they are not inferred
from three supplied matrices or a group label.

The order-19/order-4 case checks literal words in the same left end.
For position 1556, the verifier checks a left word of order 19 and a
middle dihedral subgroup of order 20 preserving the seed line. It then
checks 8,779 distinct canonical lines and every one of their 8,778
parent edges using an actual left generator. A Janko left end would allow
at most 8,778 such images. This lower bound needs no orbit closure or
identification of the full right unitary end.

THEORY.rst gives the arguments and references. SOURCE_PROVENANCE.json
identifies the arithmetic and actual accepted certificates.

Limits and interpretation
-------------------------

The 400,000 matrix-product cap, 200,000 RREF-operation cap, 2 MiB total
JSON-read limit, 1 MiB limit per JSON file and 100-second internal limit
are unchanged. The requested outer guard remains 128 MiB and 125 seconds.
No counter is reset. The eight extra prefix ranks use the same RREF
counter; determinant terms and graph row images are counted separately.
The existing 943,200-term determinant cap is unchanged.

The accepted snapshot has 3,397 additional exclusions: 3,124 intersection
failures and 273 nongeneration cases, with 209 positions unresolved.
The earlier 1,089 exclusions remain in historical archives; this package
covers the other 2,308. Original group/model, faithful frame, membership,
orbit and classification premises remain imported. These negative results
do not complete the positive classification, a census or a manuscript.
No new conjecture, Lean or compression measurement credit is claimed.
