A nonfirm obstruction to the HNN geometry construction
=====================================================

The `four-page proof <proof/nonfirm_hnn.pdf>`_ gives a flag-transitive rank-six
coset geometry of S4 and an automorphism satisfying the literal admissibility
definition in Piedade–Tranchida, *From Group Operations to Geometric Structures*,
`arXiv:2505.24662v1 <https://arxiv.org/abs/2505.24662v1>`_. Its prescribed HNN
construction has a three-element flag that cannot extend to a chamber. Thus
the initial flag-transitivity assertion and clause (a) of Theorem 3.35 fail
without further hypotheses. The input is neither firm nor residually connected.
No assertion restricted to those classes is refuted here.

The proof establishes input flag transitivity by an elementary coset argument
and identifies the infinite HNN group by mutual presentation maps. The failed
output intersections are explicit. Finite enumeration is validation, not
a substitute for the infinite-group proof.

The `distinct mathematical review <independent_review/review.json>`_ reads
the full proof and exact source boundary. Its independent GAP reconstruction
checks all 729 parabolic product identities; the author program checks all
1,336 input flags and four controls. Both published copies pass. Frozen author
files retain their original review-stage wording; the later `admission
<admission.json>`_ records acceptance.

This corrects a theorem in the specified edition. It is not a numbered open
conjecture answer or a whole-paper recovery. Historical priority and full Lean
verification are not claimed. N005 remains in the accessible recovery queue.
No compression ratio or corpus count is changed.

Replay the two finite validations::

  python3 -B -O proof/check.py --out /fresh/author
  gap -q -T independent_review/input_s4.g
