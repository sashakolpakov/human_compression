# Formalizing the actual supported-kernel construction

Active author workspace, 10 October 2026. Target: U.SK in the frozen umbrella v2, not merely its last coordinate-intersection consequence. The new source is formal/SupportedKernelGeneration.lean. Nothing in this phase is independently admitted yet.

The exact existing CoordinateKernels module will be reused for the final IP transport after its kernel-product isomorphism and coordinate membership hypotheses have actually been proved. Its assumed hcoords field cannot stand in for the new construction proof.

The declaration sequence is:

1. Prove finite triangular isolation in possibly nonabelian coordinate groups. A witness for coordinate i may still have entries at smaller supports. Inclusion/rank induction removes those entries using the already proved pure-coordinate elements. This step must prove isolation, not assume it.
2. Define actual marked subgroups by closure of literal tuple markers. Prove their coordinate images lie in the intersection of the word support and the local support. Prove compatibility and base fixation from equality of homomorphisms on those literal generators.
3. Derive the triangular witnesses from local marked generation, the actual quotient/deletion equations and injectivity on every proper local parabolic. In particular the base of a lift of a local kernel element must be proved to be one.
4. Apply the isolation theorem with support-cardinality rank, deriving strict descent from distinct supports. Obtain the entire pure local kernel inside the corresponding actual generated parabolic.
5. Assemble those pure kernels and use the actual base projection's surjectivity to prove that the global generated subgroup equals the full simultaneous fiber product.
6. Prove both directions of the complete kernel membership profile on every generated parabolic. Only then identify the kernel with the coordinate product and apply the existing exact coordinate-meet/transport declarations.
7. Bind the antichain, Boolean-deletion, lower-central and separator conclusions separately. Full certification of U.SK's basic generation/IP theorem will not automatically certify those additional corollaries.

The proof uses the existing Mathlib map-of-closure and equality-on-closure theorems, plus finite direct-product assembly. There is no isolated-normal-word premise, finite-group assumption, abelian-kernel assumption or new axiom. The first triangular theorem permits a general well-founded rank relation and is a reusable induction component; it is not claimed to be U.SK until the remaining actual-marker bridges are proved.

Checkpoint status: steps 1–6 are now proved. The pinned fresh run compiles ten substantive new declarations, including supported_kernel_construction, and recompiles the six printed declarations in LiftCertificate and CoordinateKernels. All axiom reports contain only propext, Classical.choice and Quot.sound; there are no warnings or placeholders. Seven author-side wrapper rejection controls pass. The finite cardinality formula and step 7's additional corollaries remain explicit formal obligations. The exact scope is recorded in phase129_supported_kernel_scope.md; independent review is pending.
