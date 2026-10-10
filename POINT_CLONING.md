# Point cloning gives gonality-two counterexamples

For every integer a ≥ 2, replace each point of the affine plane AG(2,3)
by a distinct copies, keeping the twelve lines and letting every copy
inherit the original incidences. The resulting input geometry has gonality
two. Its triangle geometry is nevertheless firm, residually connected and
flag-transitive.

This refutes the **unnumbered experimental suggestion** in §7 of Delaby,
Leemans and Tranchida, *Geometries with trialities arising from linear
spaces*, [Algebraic Combinatorics 9(2) (2026), 379–402](https://alco.centre-mersenne.org/articles/10.5802/alco.482/).
It uses the final journal incidence rule and definition of a rank-two
geometry. **Distinct cloned points have identical neighborhoods.** That
is allowed by the source definitions; a variant excluding such points
remains unanswered. The separate question about nonlinear inputs of
gonality three also remains open here.

Read the [complete two-page proof](research/case_study/phase268_point_cloning.pdf),
[its source text](research/case_study/phase265_gonality_two.md), and the
[independent review](research/case_study/phase268_review.md).
The author's earlier pending-review label is superseded by that accepted
review; the original proof file is preserved unchanged.

## Why the construction works

Both clauses of the triangle incidence relation depend only on the
original point and line. Cloning the points therefore clones every
triangle vertex, with exactly the original incidences between fibers.
Every residue has the same description. A connected base residue has a
neighbor at every vertex, so paths lift and two copies of one vertex can
be joined through a neighbor. Thus residual connectivity is preserved.
Chambers lift, their panels acquire a choices for each former vertex,
and independent permutations within fibers preserve incidence.
The affine group aligns projected chambers; fiber permutations align
their chosen copies.

Two copies of one point and two lines through it give a four-cycle in
the input incidence graph, proving gonality two. The original affine
example and triangle construction are attributed to the source authors;
cloning and graph blow-ups are standard constructions. The contribution
is the resulting uniform counterexample and its explicit source audit.
Historical priority is not established.

## Verification

The author's literal program checks the doubled example, including
transitivity on its 3,456 chambers. A separately written program checks
all 648 rank-two residues and 163,296 ordered incidence comparisons in
the cases a = 1, 2, 3. These are checks of actual incidences, not merely
matching parameters. The all-a theorem follows from the written proof.

[Four axiom-free Lean proofs](research/case_study/formal/GraphClones.lean)
construct paths in the cloned relation and establish connectivity under
explicit symmetry and neighbor assumptions. The incidence-geometric
identifications and the whole counterexample are not formalized.
The [formal scope](research/case_study/phase268_formal_scope.md) makes that
boundary explicit.

```sh
python3 -B -O research/case_study/phase270_check.py \
  --out /tmp/NEW-point-cloning \
  --lean LEAN --packages PACKAGES
```

The fresh public replay passed, including the isolated-vertex control for
the essential neighbor assumption. No primary full text is distributed.
The [publication record](provenance/phase132_review.md) binds the proof,
review and checks. This is one new question entry, not a new principal
source recovery or a numerical compression claim.
