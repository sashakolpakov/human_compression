# Independent root review of one-exceptional quotient transport

Date: 2026-10-10. PASS.

The complete written proof and final Lean statements were read. The only
unprotected proper generator subset is the exceptional maximal subset;
its self-intersection is tautological. Every other nontrivial intersection
has an injective containing parabolic. A typed coset family containing a
nonexceptional type uses it as anchor; a family contained in the exceptional
singleton is handled directly. Exact subgroup images and their meets are
explicit assumptions, with no tacit surjectivity or finite-rank condition.
The combined theorem derives mapped pair intersections from full marked IP.

Fresh compilation from the exported source passed with Lean 4.32.2, after
checking all nine pinned dependency revisions and tracked-file cleanliness.
The runner cleared inherited LEAN_PATH and compiled the retained transport
module first. All exported statements use only propext, Classical.choice
and Quot.sound. Fresh reports are in provenance/phase37_lean_root_run.

This verifies the abstract transport theorem. It does not instantiate the
source presentations, finite groups, geometric residues or all-parameter
family. Compiled dependency libraries remain trusted build inputs, as
recorded by the runner; there is no external peer-review or novelty claim.
