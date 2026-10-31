Centralizers of 157 prefixes in G2(11)
=====================================

This package rechecks one acquired prefix at a time. It scans all 14,763
matrices in the corresponding shared bank, determines exactly which commute
with b, and verifies the exact order of ab. It contains the 157 prefix
certificates and a complete written argument excluding both parabolic types
for 81 of them. REPLAY.json records Root's independent arithmetic checks
of this portable edition.

From the repository root, for example::

    python3 -E -B -S october_corpus/reproduction/prefix_centralizers/verify.py --controls
    python3 -E -B -S october_corpus/reproduction/prefix_centralizers/verify.py --prefix 24

The original job numbers are listed in manifest.json. Python 3.9 or later on Linux or macOS and its standard
library suffice. Do not use -O. Each invocation checks one
prefix; there is no arithmetic mode for all prefixes and no counter reset.
The program writes its JSON result to standard output.

The finite check
----------------

The literal marks are ordered a, e, b. The verifier checks their involution
and string relations, the first a in the exact bank, distinctness of all bank
records, and the complete commutation filter with b. It compares every
resulting original J index with the acquired list. The order routine first
tests a finite annihilator and then checks every proper prime divisor. The
entire carried order certificate must agree. These arithmetic, filter and
order routines are copied literally from the owning acquisition program;
SOURCE_REUSE.json records the definitions and attribution.

The group argument
------------------

Put D = <a,b>, U = C_G(D), S = C_U(e), and let N count all nonidentity
involutions of U. For an eligible prefix, N < 5, 5 does not divide |S|,
and 11 does not divide |D|. The preserved theory.tex proves
[U:S] = |e^U| <= N, hence 5 does not divide |U|. If D were contained
in either parabolic, coprime complement conjugacy would embed a Levi centre
of order ten in U, a contradiction. The argument requires no equality U = S.

The 81 applications comprise 77 records with N = 3 and |S| = 4 and four
with N = 1 and |S| = 2. Job 24 already had a stronger retained proof; the
other 80 are distinct applications relative to that record. This is not
a claim of historical novelty. applications.json and theory.tex retain
their accepted bytes. Historical preparation wording in the table is
qualified by THEORY_ADOPTION.json and THEORY_EDITION.json. The runtime
lemma81.json is an exact field projection of that full table.

Imported premises
-----------------

The matrix checks do not establish the full named G2(11) model, its faithful
frame and membership, completeness of the original ordered involution banks,
or identification of the full original S. Those remain explicit inputs.
A list of S coordinates is not a proof that it is the full centralizer.
The embedded finite GL2(11) Levi structure is also imported, with precise
references in theory.tex. The program opens only local relative package
files. Absolute historical paths in SOURCE_PROVENANCE.json are attribution
records and are never opened. No full original context recheck is claimed.

Limits and interpretation
-------------------------

Each process retains the 400,000 matrix-product, 128 MiB memory, 100-second
internal and 8 MiB input limits, with at most 96 input paths. Each local
input file is below 1 MiB. Both bank bodies contain 723,387 bytes and are
copied as exact opaque acquired bytes. All inputs used by a process are
fully rehashed at its end. The test plan requests a separate 128 MiB,
125-second outer guard for every invocation. REPLAY.json gives the measured time, memory and input charges from the
recorded replays.

There is no converse for the 76 ineligible prefixes; their parabolic verdict
is null. These checks do not settle generation of a remaining end, a quartet
intersection property, the positive classification, a full job or manuscript,
an open conjecture, Lean verification or compression measurements. The
existing 2,308-case matrix_certificates package and its history remain
separate and unchanged.
