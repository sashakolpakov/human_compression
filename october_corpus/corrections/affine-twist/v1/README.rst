Regularity of the smallest affine twist
=======================================

The `three-page proof <proof/affine_twist.pdf>`_ corrects the parameter-one
conclusion of Example 5.11 in Piedade and Tranchida, *From Group Operations
to Geometric Structures*, `arXiv:2505.24662v1
<https://arxiv.org/abs/2505.24662v1>`_. With the specified representative type,
the literal twist is a regular rank-three geometry of adjacent orders six
and four for every positive parameter. At parameter one its input still
has the disconnected residue described by the source.

The proof identifies the actual quotient parabolic intersections and then
proves the marked intersection property, flag transitivity, thinness and
residual connectedness directly. It retains the classical faithful affine
Coxeter realization. The precise borrowed input and a reference for its
semidirect model are recorded in the `distinct review
<independent_review/review.json>`_. No finite computation is a premise of
the uniform theorem.

A separate GAP reconstruction of the smallest quotient checks all 64
marked subgroup intersections and 343 proper parabolic product identities.
The author program and four controls also pass from the published files.
All three proof pages were read, rebuilt and visually reviewed. Frozen
author files retain their earlier candidate wording; the later `admission
<admission.json>`_ records acceptance of the second author edition.

This is an example correction in the specified edition, with no historical
priority or full Lean claim. It is not a numbered-conjecture answer or a
whole-paper recovery. N005 remains in the recovery queue and no compression
ratio changes.

Replay the supplementary validations::

  python3 -B -O proof/check.py --out /fresh/author
  gap -q -T independent_review/literal_twist.g
