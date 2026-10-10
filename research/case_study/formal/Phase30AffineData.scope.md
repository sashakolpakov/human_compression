# Scope of Phase30AffineData.lean

This is a partial finite-data certificate for the separately reviewed affine regular-hypertope construction. It embeds the final report's 30 quotient columns as natural-number masks with 13 bits, its 12 vertex blocks and 12 face blocks, and its 60 listed incident vertex-face pairs. The separate transcription checker binds these four literal arrays to the authored report.

The definition `xorSpan` recursively lists all XOR sums of sublists of the given vector list, retaining duplicates. Thus its membership predicate is the literal finite binary span test. The six kernel-checked theorems are:

* `finite_shapes`: list sizes30/12/12/60; all columns nonzero and less than8192; all block and pair indices in range; every listed pair has two common column indices.
* `columns_distinct`: the 30 column masks are pairwise distinct.
* `all_720_memberships`: for each of the24 listed blocks and30 column positions, the column belongs to that block's XOR span exactly when its position belongs to the block.
* `all_60_intersections`: for each listed vertex-face pair, the intersection of the two XOR-span sets equals the XOR span of their common column indices. Both inclusions are tested, rather than only cardinality.
* `all_24_odd_relations`: each listed block has five entries and their XOR is zero.
* `all_24_span_sizes`: each block span has16 distinct mask values.

All six proofs use `by decide`, whose proof terms are checked by Lean's kernel. There is no `native_decide`, `sorry`, or additional evaluation axiom. The saved Lean4.32.2 report lists no axioms for `columns_distinct`, and only `propext` for the other five theorems. No assertion about an arbitrary input file is proved: these are certificates of the literal embedded data.

The formal module does not construct the seed permutation group or its incidence geometry, prove that the60 listed pairs are precisely its incident pairs, compute the original code rank17 or quotient dimension13, establish code invariance under the seed group, or identify the binary masks with that quotient. The transcription and generation of those data are separately hash-bound. The interpretation of a16-element binary span as dimension4 is elementary linear algebra in the written adapter; no general vector-space dimension theorem is used here. The affine geometry, all its flag and residue arguments, and the halving counterexample remain outside this module.

Reproduce in the pinned private setup with `python3 verify_lean.py Phase30AffineData.lean` from the `formal` directory. The public portable runner, if this supplement is exported, must use the same pinned Lean/mathlib environment. The original saved compile report remains a historical record of the private execution.
