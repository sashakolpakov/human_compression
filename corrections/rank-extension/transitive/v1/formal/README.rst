Formal output obstruction for the transitive extension
=====================================================

TransitiveExtensionObstruction.lean proves sixteen declarations about the
literal six-generator output on twelve points. The last theorem states that
its actual generated subgroups fail the intersection property. Both witness
memberships use Subgroup.closure, and the common-label subgroup is bounded
by the explicit subgroup {1, delta 3}. Finite identities use kernel-checked
decide; no native evaluator is used.

The old input C-property, all fracture/split hypotheses and the full
source-level implication remain in the separately frozen written proof.
This is a scoped certificate, not an end-to-end formal refutation of the
source theorem. Earlier disconnected-example certificates are unchanged.

Replay with the pinned Lean and mathlib dependencies::

  python -B -O check.py --study-root /path/to/study --out /fresh/output

Options --lean and --packages relocate the installed toolchain and pinned
packages. The checker verifies package revisions and clean package sources,
then compiles the source freshly and rejects four concrete corruptions.
Existing cached dependency oleans are trusted, as stated in the report.
Distinct mathematical review remains pending at author freeze.
