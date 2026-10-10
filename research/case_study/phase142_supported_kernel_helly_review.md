# Independent formal review: coordinate-kernel typed Helly

10 October 2026. Root admits `SupportedKernelHelly.lean`, SHA-256
`3951f64e6a0340e086bd21567182350ed460b3d56eda296c266bf161f85c76e2`.
Root read all definitions and proofs, the scope document, the complete
semantic checker and the relevant runner/control code. The eleven
reported declarations match the written U.SK.Helly theorem and its
actual supported-kernel application.

## Exact mathematical content

The cosets are right cosets P g: x belongs exactly when xg^(-1) lies
in P. TypedHelly selects at most one coset of each type, allows the empty
family, and requires pairwise intersections to have a common point.
The nonempty self-pair condition adds no restriction on actual cosets.

The internal transfer theorem starts from a surjective homomorphism,
subgroup images, an exact intersection-image identity, multiplicative
kernel coordinates, coordinate profiles and base typed Helly. Given a
common base point, it explicitly adjusts each pair's common point into
that fiber. The adjustment comes from the image of the subgroup
intersection. Thus a missing common-fiber assertion is not being assumed.

Within the fiber, two kernel representatives lie in the same coset
precisely when their constrained coordinates agree. Both directions
are proved, using coordinate multiplication and cancellation. Pairwise
fiber intersections therefore give compatible fixed values. Choice of
one required value per coordinate, or identity when unconstrained, gives
the common point. Nonabelian factors are permitted; the proof never
interchanges elements within a coordinate group.

The separate marked_intersection_image theorem derives the internal
intersection-image premise from base IP and the actual generated
parabolics. A base element in the intersection lifts from the common
label subset. No IP upstairs is assumed. The general marked theorem
therefore proves the complete written coordinate-kernel transfer, rather
than a conditional fragment with its main lifting step left as a premise.

The final supported_kernel_typed_helly theorem constructs the actual
parabolics inside the fully generated tuple group. Base generation gives
surjectivity. The previously proved kernel-coordinate equivalence is
shown multiplicative. The construction's profile and IP theorems provide
the coordinate and intersection-image identities. Every generic premise
specific to this construction is discharged. Its remaining base Helly
and actual local construction hypotheses are explicit application inputs.

The generic theorem permits infinitely many kernel coordinates and
arbitrary groups. The SK specialization has finite support and label
types. Neither theorem requires involutions: those are needed for the
subsequent geometric recognition step. The mandatory phase130 geometry
erratum remains in force; a base involution alone does not make its
lift involutory.

## Fresh verification

The pinned dedicated wrapper freshly compiled five local sources and
the two specified Mathlib sources in about 24.1 seconds. Eleven new and
twenty-three retained printed declarations use only propext,
Classical.choice and Quot.sound. Nine rejection controls passed.
The author-designed semantic checker was also freshly executed by root:
the positive case has nonabelian kernel D8×S3, and three V4 cases each
remove one of the intersection-image, coordinate-profile or base-Helly
hypotheses while satisfying the other interfaces and failing the result.
These finite diagnostics clarify the hypotheses; they do not prove the
universal theorem or constitute an independently designed test suite.

All local source hashes, compiler version, package revisions and tracked
cleanliness were checked. The compiler and other cached package objects
remain trusted. Frozen author reports are preserved, and fresh root/public
reports are separate. The original written transfer and its mandatory
geometric correction remain exact retained inputs.

This certificate establishes the typed-coset intersection theorem. It
does not formalize full coset-geometry recognition, the L034 presentations
and affine calculations, or every result in U and A. It adds neither
an open-conjecture solution nor a known-source compression factor.
