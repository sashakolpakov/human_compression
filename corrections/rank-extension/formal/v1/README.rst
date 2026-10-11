Lean verification of the output obstruction
===========================================

Ten `Lean declarations <packet/RankExtensionObstruction.lean>`_ verify the
actual five permutations on ten points and prove that their generated
subgroups fail the intersection property. The proof uses kernel-checked
finite identities and ordinary subgroup closure, with no native evaluator.
All ten axiom reports use only the standard logical axioms.

This is a supplement to the `complete written counterexample
<../../v1/rank_extension/rank_extension_correction.pdf>`_. The old input
C-property and every fracture and split hypothesis remain written proofs;
this certificate is not a full formalization of the source theorem.

The portable distinct checker uses only published project files. From the
repository root, with the pinned compiler and package cache available::

  python3 -B -O corrections/rank-extension/formal/v1/independent_review/check.py \
    --packet corrections/rank-extension/formal/v1/packet \
    --correction corrections/rank-extension/v1/rank_extension \
    --lean /path/to/lean --packages /path/to/packages --out /fresh/path

The new module is compiled afresh; cached upstream dependencies are trusted
and explicitly pinned. The separate author replay includes three rejected
mutations. No manuscript, conjecture-answer or compression credit is added.
