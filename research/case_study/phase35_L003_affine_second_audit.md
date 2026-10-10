# Independent review of the compact affine construction

Date: 2026-10-10. Result: **PASS for the stated mathematical and executable scope.**

I read the complete frozen `phase35_L003_affine_model.md`, its standalone checker, and its comparison checker. This record binds the exact files in the adjacent JSON. It records a written and code review, not a fresh execution by this reviewer. The root reviewer separately executed both checkers.

The four displayed integral affine maps, the right-action convention, and the first-nine-relator adapter are consistent. The Schreier calculation checks all generators of the translation kernel, not merely selected independent translations: every kernel generator has even coordinates, and six explicitly supplied words give the six vectors twice the standard basis. Together with the complete linear-image enumeration this proves the exact kernel and all finite orders. The modulus argument uses the literal lattice and remains valid for composite moduli.

The three protected maximal parabolics are finite and inject under the reductions used in the proof. The exceptional maximal parabolic has two independent translation coordinates and attains the full source toroidal order. The base intersection and typed-coset-Helly checks are separate. Applying the one-exceptional-parabolic transport theorem therefore gives the claimed regular geometries without assuming that subgroup IP implies flag transitivity.

The comparison identity uses the correct pullback convention for the original voltage action. The affine intertwiner is checked on all generators and coordinates. Its linear part is faithful on the finite permutation quotient; the remaining translation map is injective on the known lattice. This proves the marked identification and its reductions, rather than just equality of the finite group orders.

Retained dependencies include the already reviewed voltage-family lattice certificate, the one-exceptional transport theorem, and the source local toroidal presentations. I authored the earlier voltage-family construction, so this is an independent review of the new compact implementation and its comparison proof, not an independent rediscovery of every retained input. No new source-status or priority claim is made. No assertion of universal-group faithfulness or splitting is added.
