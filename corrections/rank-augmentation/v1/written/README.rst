A counterexample to the six-point case of rank augmentation
=========================================================

Read ``case_three.pdf`` or its complete TeX source first. This is a bounded
correction candidate to L020, Theorem 4.1(3), in arXiv:2212.12563v1. It has
not yet received a distinct mathematical review. It does not recover the
whole paper, decide cases (1) or (2), or refute the separate high-rank
stability theorem.

The original rank-three marking is proved to generate the natural S18 by
seventeen explicit conjugate transpositions forming a spanning tree. Its
full intersection property follows from the displayed dihedral groups and
the explicitly retained end criterion. The new failure is the actual word
``((bc)^45)^(a(bc)^2ba(cb)^8a)=t`` in disjoint sets of labels.

Portable replay from an export-only copy, with the two exact primary files
supplied separately under the study root::

  /Users/sasha/.venvs/global/bin/python -B -O check.py \
    --study-root /Users/sasha/medusa/research/leemans \
    --out /private/tmp/L020_fresh --render

The direct certificate ``python3 -B -O check_case.py`` needs only Python's
standard library. Optional PDF replay needs pypdf and XeLaTeX. It enumerates
only proper old subgroups of order at most 180, not S18. Its three semantic
controls alter the witness exponent, delete a generation-tree edge, and
change the split transposition. The written proof explains why these finite
identities establish the group and intersection claims.

No Lean statement is claimed in this packet. A separate supplement may
verify the explicit obstruction while preserving this freeze. Source
PDF/text are private external inputs and are not redistributed here.
