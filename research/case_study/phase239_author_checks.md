# Author checks for the uniform pyramid result

10 October 2026. These are author checks, not an independent acceptance.

The complete written argument is `phase239_odd_toroidal_pyramids.md`.
The substantial new step is Sections 2–4: the fixed orientation quotient
applies uniformly because the translation kernel has disjoint supports on
the two end groups, and because the middle coordinates fixing both the
vertex and face centers satisfy an integral restriction. The finite group
calculation is used only after this infinite-parameter argument.

The proof requires no formula for the order of G_n or its top intersection.
It uses only the kernel bound |K_n| dividing n^10, the subgroup J bounding
the image of the top intersection, and the exact fixed quotient kernel.
The old non-C classification for odd n is retained explicitly from the 2022
primary. The general finite-cover conjecture remains outside the result.

Author replay:

    python3 -O phase239_pyramid_check.py --out /private/tmp/phase239_author_replay

Result: PASS in 6.121 seconds. It includes:

* Exact affine-to-face flag bijections for n=3 and n=5, with all four
  adjacency relations and orientation projections. Their 348160 total
  component tests validate these two inputs and conventions; they do not
  replace the uniform proof.
* The 40-point orientation group E, its parabolics, all 3072 elements of the
  end intersection, the 48-element subgroup J, and a checked epimorphism to
  D of order 3840. Its actual kernel of order 16 meets J and C in the same
  subgroup of order 2.
* The reused cellular calculation giving the orientable surface of Euler
  characteristic −640 and its three connected complements. The dimension 642
  is uniform over prime fields by the retained written surface theorem.
* Four new elementary Lean statements, three retained coprime pullback
  statements and six retained minimal-kernel statements, with standard
  axioms only. No claim of full geometric formalization is made.

Material controls all reject:

* Removing the center constraint enlarges the tested kernel intersection
  to order 16, whereas the middle kernel has order 2.
* Replacing the affine reflection r_0=(1−x,y) by its linear part breaks the
  literal flag-adjacency identification.
* Removing distinct supports, allowing modulus 1, and deleting the subgroup
  injectivity hypothesis each causes the corresponding Lean proof to fail.

A separate directory containing only the eight replay files was tested:
`/private/tmp/phase239_portable_packet`. Its replay into the fresh directory
`/private/tmp/phase239_portable_replay` passed in 6.278 seconds. The runtime
requires Python, GAP and the pinned Lean/mathlib environment, but no private
primary PDFs or manifests. The written source review still needs the
separately listed primary sources. Negative Lean logs contain their replay
paths, so their byte hashes need not agree between the two runs; the
positive theorem logs and finite mathematical certificates do agree.

The frozen224 files and all reused scientific dependencies remain unchanged.
No public repository files were modified.
