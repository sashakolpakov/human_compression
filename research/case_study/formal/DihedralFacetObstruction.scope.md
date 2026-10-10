# Scope of DihedralFacetObstruction.lean

Five declarations verify the abstract normalizer step in the common
PSL₂/PGL₂ classification proof. An involution with an odd vanishing power
is trivial; the homomorphism and quotient forms transfer this fact to
membership in a normal subgroup. Generation by a subgroup and one
normalizing element supplies normality. An independent generator then
contradicts the odd adjacent relation.

The final theorem assumes the stated generation, normalizer, involution
and odd-power conditions. It assumes neither normality of the facet nor
the desired membership conclusion. The written projective matrix argument
establishes its normalizer hypothesis in the application.

The public source is byte-identical to the frozen phase230 source.
The fresh phase235 replay compiles all five declarations with only
propext, Classical.choice and Quot.sound. Cached dependency objects are
trusted; the pinned revisions appear in the check report.

This file does not prove the matrix centralizer calculation, Dickson's
classification, the finite presentation orders, or the full geometric
classification. See the complete manuscript and independent review.
