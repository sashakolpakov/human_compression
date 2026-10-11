Matching extensions and parity
==============================

Accepted complete corrected principal recovery of F015, Claudio Alexandre
Piedade, *Infinite Families of Hypertopes from Centrally Symmetric Polytopes*,
Electronic Journal of Combinatorics 30(2) (2023), P2.20.

Read ``umbrella.pdf`` (six pages), ``spherical-families.pdf`` (seven pages),
and the complete ``programs.pdf`` (two pages). Their TeX sources, the full
GAP program and seven reused Lean component proofs are beside them.

The root admission is ``../../../audit/topic-matching/v1/admission.json``.
It supersedes the pre-review status recorded in the unchanged author packet.
This adds one original manuscript, not eight family credits. Length
measurement is pending; no compression factor is inferred from page counts.

The source's two literal 120-cell presentations are proved infinite throughout
the stated parameter range. Twenty missing pair relations recover the intended
finite constructions. This is a published-result correction, not a new answer
to an open conjecture. The original constructions and classical extension,
lattice, toroidal and Coxeter inputs retain their attribution.

Reproduction
------------

Run the complete author check from a checkout with pinned dependencies::

  python -B -O check.py --out /fresh/output --gap /path/to/gap \
    --lean /path/to/lean --packages /path/to/pinned/packages \
    --render --xelatex /path/to/xelatex

The optional ``--study-root`` verifies the private primary PDF. Public replay
requires no original PDF. The full written geometry and presentation theorem
are not claimed formalized. The independent review also provides a separate
exact four-dimensional reflection model of the 600 vertices.
