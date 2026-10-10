# Independent review of the 2002 tree-and-parity reduction

10 October 2026. Root reviewed the complete replacement proof and all
twelve pages of the primary author manuscript of Cameron–Cara,
*Independent generating sets and geometries for symmetric groups*.
The manuscript PDF and extraction hashes are bound in the intake record.
The internal mathematical verdict is PASS for the specified finite-group
bounds and the classifications for n≥7, retaining W1, W2 and the other
inputs declared in the proof. This is not external peer review.

## Exact theorem coverage

[The replacement](phase12_N003_reduction.md) recovers Theorem 1.1,
Theorem 2.1, Corollaries 2.2–2.4, Theorems 3.1–3.2 and Corollary 3.3.
Both generator families, all three enumerative formulas, every subgroup
intersection and both directions of the geometry correspondence are
included. Whiston's maximum-independent-family result W1 and the exact
omission-subgroup trichotomy W2 are separately retained. The latter does
not follow merely by citing W1. The CFSG dependence has not disappeared.
The unnumbered small-degree exceptional claims and the source's open
questions are excluded. The general bounds are stated for finite groups.

## Checks of the replacement steps

The normal-subgroup bound correctly uses correction words in a minimal
quotient-generating subset. In the abelian refinement all conjugation
actions can be represented by those words, giving action independence.
The imprimitive exclusion spells out the necessary permutation-module
argument. An independent action family is linearly independent; equality
in dimension m would make all coordinate hyperplanes invariant and the
action trivial. After W1 forces the full symmetric quotient, any
nonconstant vector generates the even-weight subspace under that action.
This leaves at most two independent vectors and gives the contradiction.

The edge construction gives a tree: every edge except possibly the first
crosses the orbits of its own omission group, and no other edge does.
The resulting tree-cut components are exactly those two orbits. Applying
the common forest-intersection formula then puts the first generator in
a single C₂ and every other generator in an S₃ or C₂×C₂. Parity identifies
the two claimed branches. This is the substantive shortcut in the forward
classification; it retains rather than reproves W2.

The sign-kernel identity is correct for every subforest containing the
distinguished edge, including the empty set of retained twisted generators.
It proves all strong intersections. The counting argument normalizes
actual generators through s times each generator, giving a unique tree
with distinguished edge. Identifying inverses instead contracts that edge;
these give exactly the two source twisted counts without overcounting
orientations. Ordinary trees give the remaining count by Cayley's formula.

The overgroup argument needs no further symmetric-group classification:
conjugate within-block transpositions either connect the two components
or preserve the unordered bipartition. Only a balanced cut admits its
proper unordered stabilizer. There is at most one such cut. A distinct
pendant-edge parabolic forces B to fix a point, excluding a half-swapping
element and proving the relative-B corollary.

For the geometries, pairwise subset intersection sizes impose exactly
the base laminar containment and disjointness relations. Matching the
resulting atom sizes gives a common permutation for a partial flag.
In the twisted branch every cut stabilizer intersection contains the
odd distinguished transposition; hence either parity can be chosen
without changing the cut flag. The geometry is the weighted-tree
geometry joined with a two-point type, with its specified S_n action.
The RWPRI proof handles residues with the parity type both fixed and
unfixed, and uses the distinguished component to adjust parity in any
other symmetric factor. The remaining single component has the stated
primitive alternating action.

Finally §9 supplies a needed explicit bridge for Corollary 3.3. For
arbitrary maximum-rank chosen parabolics, at most one balanced-cut
parabolic might be enlarged. Any other cut has a nonempty side within
one of its halves, excluding a swap in their intersection. There are
enough types for this to preserve every panel intersection. Source
residual generation then recovers all parabolics from those panels,
eliminating the enlargement. This avoids presuming that independent
generators alone identify arbitrary chosen overgroups.

## Measurement and verification boundaries

This promotes a complete set of identified principal results, with
the finite-group and n≥7 scopes above. Some adapters reproduce elementary
arguments already in the source; a common notation alone receives no
compression credit. Any numerical comparison must charge the full
forest/parity core and all added adapters, on the same retained background.
No new matched length ratio is assigned by this audit. The missing 1998
source spans remain a separate limitation. Exact finite diagnostics,
when cited in the bound JSON, supplement the written uniform argument;
they do not prove the classification for arbitrary n.
