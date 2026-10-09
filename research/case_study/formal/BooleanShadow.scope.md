# Boolean shadow certificate

`BooleanShadow.lean` compiles with the existing pinned Lean 4.32.2 and mathlib revision `905b95818eb32af7874a58b427f50c1711a5e96c`. The final run has exit code zero and no warnings. Its three printed theorem dependencies use only `propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx`.

Source SHA-256:

`1c8b81ce65de6d12af8219ebb4d9d397584bd3c9c8c133635a8e3fcf1f1302d3`

Report SHA-256:

`e5d0ec0634e526d727fef3f69ab4c2c9fcc31b483ff39da961b167dcdabf69ff`

The universe is a finite type. A query is an arbitrary finite family U of its finite subsets; U need not be a flag. Two subsets are incident when one contains the other. `Shadow U k Y` means that Y has cardinality k and is incident with every member of U.

The checked statements are:

* `shadow_iff_interval`: if U has no member of cardinality k, its common k-shadow consists exactly of the k-subsets between the union of its smaller members and the intersection of its larger members. The empty intersection is the entire universe.
* `shadow_iff_eq_of_same_rank_member`: if the shadow is nonempty and U contains a k-subset X, the shadow consists exactly of X.
* `exists_witness_card_le_two`: for a proper target rank `0 < k < |Ω|`, every nonempty common shadow has a witness C containing at most two nonempty proper subsets. C is a chain, every member of C is incident with every member of U, and C has exactly the same k-shadow as U. The proof handles singleton boundary cases and removes the empty/full boundary subsets in the two-boundary case.

These are exact shadow and witness statements, not a count check on small sets. The tree-to-subset identification, the claw obstruction, the joins of Boolean intervals describing residues, the retained classification of inductively minimal geometries, and the complete 2005 geometry characterization remain written mathematics. No whole-paper or complete geometric-IP Lean formalization is claimed.

Only this new module and its report were created. The existing nine formal modules were not edited.
