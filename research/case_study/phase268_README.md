# Review of point cloning and gonality two

The frozen author note proves that point cloning supplies an infinite family
of counterexamples to the unnumbered gonality-two experimental suggestion in
§7 of the final journal version of Delaby, Leemans and Tranchida,
*Geometries with trialities arising from linear spaces* (2026).
The input has distinct points with identical neighborhoods, which the stated
rank-two geometry definition permits. A variant excluding such points is not
answered. No priority claim or recovery of the full paper is made here.

Read [the independent review](phase268_review.md),
[the author note](phase265_gonality_two.md), and
[the rendered author note](phase268_point_cloning.pdf).
The author note's earlier statement that review was pending is superseded by
this accepted review; its frozen bytes are preserved.

[The formal scope](phase268_formal_scope.md) identifies four axiom-free Lean
path proofs. They establish connectivity for a graph whose vertices have
been cloned, under explicit symmetry and neighbor hypotheses. They do not
formalize the entire incidence-geometric counterexample.

A fresh replay of both literal finite programs and all four Lean proofs uses:

```sh
python3 -B -O phase268_check.py --out /tmp/fresh-cloning-replay \
  --lean /path/to/lean --packages /path/to/pinned/packages
```

The output directory must not exist. The pinned dependencies are recorded in
`formal/dependency_manifest.json`. No primary publication PDF is required or
distributed. The saved replay verifies all 648 residues and 163,296 ordered
incidence comparisons for one, two and three clones per point, and the
independent author program checks chamber transitivity in the doubled case.
The uniform result follows from the written proof.

The two-page authored PDF was visually checked in full on 11 October 2026.
The source reading was limited to printed pages 381–383 and 400–401, with
visual inspection of pages 382, 383 and 401. This is not a full-source reading
claim. The source edition and search limitations are recorded in the review.
