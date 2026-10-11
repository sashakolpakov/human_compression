Review of restriction kernels
=============================

The complete `paper <../../../papers/restriction-kernels/v1/restriction_kernels.pdf>`_
and `TeX source <../../../papers/restriction-kernels/v1/restriction_kernels.tex>`_
have passed distinct mathematical review. The publication edition removes only
the private-review title date; all mathematical text is unchanged. All five
fresh publication pages were visually inspected.

The frozen author and independent-review packets are preserved in their
respective subdirectories. Their earlier pending/private labels describe the
frozen submission stage; `admission.json <admission.json>`_ records the current
acceptance. Every theorem and proof was read. Fresh GAP diagnostics cover
600 kernel cases, 180 leaf markings, 312 split instances and 225 rectangles,
with negative controls. A separate Python permutation implementation checks
all 600 kernel cases without GAP or author-program imports.

`RestrictionKernelCriterion.lean <author/RestrictionKernelCriterion.lean>`_
proves three arbitrary-group subgroup lemmas using standard axioms only.
Both the author replay and a separate direct compilation pass. The full
permutation criteria and the standard end criterion are not formalized;
the exact cached dependency revisions remain a trust boundary.

From the repository root, reproduce the distinct finite and Lean check::

  python3 -B -O audit/restriction-kernels/v1/independent_review/check.py \
    --packet audit/restriction-kernels/v1/author --out /fresh/output

The optional --lean and --packages arguments select the documented toolchain
and package location. The full author runner additionally binds the original
private source and preceding proof packets through --study-root. Its internal
impact audit of existing B and Gluing proofs remains attributed as an internal
audit, not a fresh independent rereading of those whole manuscripts.

No original, open-question answer or numerical compression credit is added.
The existing L019 counterexamples, source status and measured topics remain
separate from this positive criterion.
