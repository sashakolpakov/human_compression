Exceptional two-orbit mix: additive F005 proof
=============================================

Read exceptional_two_orbits.pdf (four pages) and scope.json. The exact
source is Cunningham--Hubard arXiv:2506.19334v1, physical pages17 and19.
The new construction satisfies actual class 2_{1,2}, two medial orbits,
uniform polyhedral end types, polytopality of both inputs and of their
smallest regular cover. Its embedded intersections have orders3 and2.
Their distinction disproves the two printed necessity assertions and
justifies retaining the two actual rooted tests.

This packet preserves topic_Mix_F005_recovery unchanged. It updates only
the disposition of its rows R23 and R29 by an additive source table.
The three final questions remain outside the recovery contract. No new
source credit, numerical measurement or historical-priority claim is made.

The four-page argument proves the finite construction, all hypotheses,
all subgroup formulas and the geometric conclusions. The complete
check_exceptional.py is bounded validation, printed in full in the
three-page programs.pdf. check.py is an operational replay driver,
including six semantic corruptions; it is inventoried separately.
No new Lean theorem is claimed. The main packet's two generic fiber
statements remain partial formal evidence, not a formalization of this
coordinate construction or its polytope interpretation.

Replay from an export-only copy, with the already bound source and main
packet available under the stated study root::

  /Users/sasha/.venvs/global/bin/python -B -O check.py \
    --out /private/tmp/fresh-exceptional-replay \
    --study-root /Users/sasha/medusa/research/leemans --render

The output directory must be fresh. The test checks every flag and all
256 color-subset pairs on each graph, not merely the one displayed
intersection. It also computes the actual monodromy, complete affine
pair formulas, automorphism orbit obstruction, and both embedded fibers.

Discovery scripts and candidate JSON graphs are not dependencies and are
not exported. Source PDFs, text, font data and page images stay private.
