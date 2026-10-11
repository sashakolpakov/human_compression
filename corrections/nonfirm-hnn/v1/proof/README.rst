Nonfirm HNN correction
======================

The four-page note gives a complete written counterexample to the initial
flag-transitivity assertion and geometry clause of Piedade--Tranchida,
arXiv:2505.24662v1, Theorem 3.35. It uses the literal admissibility and
indexed subgroup construction, with both associated subgroups equal to S4.

The input is neither firm nor residually connected. The note does not
disprove the firm-input theorem, assert a new numbered-conjecture answer,
or claim historical priority. It is separate from the independent review
of the root-authored positive free-product, join, and firm-input notes.

The full hand proof establishes input coset Helly, the actual infinite
semidirect normal form, and a flag that cannot extend to a chamber. The
pure Python finite check and its four incorrect-data controls are validation
only. There are no Lean assertions and no required external finite-group
catalogue. The exact primary edition is hash-bound but not distributed.

Portable replay from this directory::

    python3 -B -O check.py --out /fresh/absolute/output

Add ``--source /path/to/2505.24662v1.pdf`` to verify the primary hash.
The output directory must not exist. To rebuild the readable proof, run
XeLaTeX twice on ``nonfirm_hnn.tex`` using STIXGeneral and STIX Two Math.
The frozen PDF has four pages; finite reports do not certify arbitrary
integer coordinates or replace the written proof.
