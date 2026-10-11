The actual eighteen-point obstruction in Lean
============================================

This supplement preserves the separate written correction candidate at
``topic_B_L020_case_three_correction``. Read its three-page proof for the
original rank-three C-marking, natural S18 identification, and exact source
hypotheses. This supplement does not formalize those ingredients.

``RankAugmentationObstruction.lean`` defines all four actual permutations
on ``Fin 18``. Thirteen declarations prove that these are distinct
nonidentity involutions satisfying the string commutations; compute the
specified word; prove its membership in two subgroups defined by actual
``Subgroup.closure``; prove the corresponding label sets are disjoint; and
deduce failure of the full intersection property. Finite identities use
kernel-checked ``decide``, not an external evaluator. No unproved statement
or new axiom appears.

Permutation composition is handled explicitly: written point k is the
Lean point k-1, and a written right-action product is reversed in Lean's
function composition. Thus written bc is c*b and conjugation by written w
is ``reverseWord * x * reverseWord⁻¹``. The runner also compares the entire
four permutation images to the frozen written certificate.

Replay from an export-only copy::

  /Users/sasha/.venvs/global/bin/python -B -O check.py \
    --study-root /Users/sasha/medusa/research/leemans \
    --out /private/tmp/L020_formal_fresh

Lean 4.32.2 and the exact pinned package sources are checked; cached compiled
mathlib dependencies are trusted. Four mutations change the split
transposition, word exponent, seed exponent, and label overlap. All must
be rejected by fresh Lean typechecking. The original word and membership
proofs remain actual Lean proofs, not an inference from these controls.

This formal supplement and its written parent await distinct review.
No complete-original, conjecture or compression credit is claimed.
