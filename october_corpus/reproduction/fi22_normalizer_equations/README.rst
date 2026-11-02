Finite normalizer equations
===========================

This small certificate checks permutations and two supplied words on 3,510
points using the Python standard library. It verifies that all 39 maps are
bijections, that all 36 CP maps centralize a, that a and c generate a Klein
four group K, and that the five complete permutation equations hold::

    a^g = c,  a^r = a,  c^r = ac,  a^t = c,  c^t = a.

Here maps act on the right, x^(uv) = (x^u)^v, x^h = h^-1 x h,
and t = CP36(q_word) g. Signed CP labels evaluate in the written order;
negative labels use the complete inverse permutation. There is no search.

Run from this directory, without Python optimization::

    python3 -B -S verify.py --controls
    python3 -B -S verify.py --check

The first command checks 22 synthetic S4/V4 and malformed-input controls and
reads no original permutation data. The second checks the entire supplied
finite certificate. Both use the exact three Source files pinned by
manifest.json and reopen all consumed inputs before reporting success.
Darwin and Linux RSS units are normalized to bytes. The worker stops at
128 MiB, 20 seconds or ten million shared work units; Root also uses a
separate 128 MiB / 150 second outer guard. Inputs are limited to 8 MiB,
32 paths and 2 MiB per file; manifest and word inputs have 16 KiB limits.

The mathematical conclusion is conditional on the stated accepted imports:
a, c, g and all CP maps are elements of the same named group A. Those
memberships, the original full automorphism/Out(2) frame and its word
meanings are attributed premises. This checker does not recognize the
original group or prove those premises. Under them, r and t act as two
different transpositions on the three nonidentity elements of K, so
N_A(K)/C_A(K) is S3. The order 6144 follows only if the separate accepted
premise C_A(K) = H and |H| = 1024 is also used. No centralizer or normalizer
is freshly counted. See lemma.tex and PROVENANCE.json.

Classical map operations and the scope of this application are attributed in
`ATTRIBUTION.rst <ATTRIBUTION.rst>`_.

maps.bin uses an explicit little-endian unsigned-16-bit format: eight bytes
L026NMS1, then degree 3510 and CP-map count 36 as two uint16 values, then
39 complete vectors in the order a, c, g, CP1, ..., CP36. words.json keeps
the two old word lists unchanged; its old private acceptance path is
replaced by the same acceptance body's byte extent and SHA256 digest.
The exported numerical vector bytes are unchanged. The public provenance
contains content anchors rather than private machine paths.

VALIDATION.json records Root's actual private and installed executions and
whole-input hashes. It is an external validation record and is not an
input to either command. Its claims are limited to this certificate and
the listed controls. The retained equation body and primitive definitions
are identified in SOURCE_REUSE.json. There is no fresh C++ build, Native
API event, bank action, candidate-family coverage, class count, paper-wide
reproduction, Original-data recognition, census or Lean credit here.
