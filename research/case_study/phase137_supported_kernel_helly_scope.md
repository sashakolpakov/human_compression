# Exact formal scope of typed Helly transfer

Author candidate, 10 October 2026; independent review is pending. This additive module formalizes U.SK.Helly from the phase130 attachment to **Marked groups, kernels and intersections**, and binds it to the actual supported-kernel construction. It leaves all frozen U, A, core and consequence files unchanged.

The result concerns finite families of right cosets P g. In the formal convention, x belongs to P g exactly when x g⁻¹ belongs to P. The old TorsorPartitions and CosetCoordinates modules use left-coset coordinates; their established results are not silently substituted for this argument. In particular, an assumed coordinate-cover condition would not prove the required Helly transfer. Here the common base fiber, its pairwise intersections, and a solution of its coordinate constraints are all constructed.

## Exact theorem interfaces

TypedHelly(P) says that for every finite set K of types and one coset representative g(t) for each type, pairwise intersection of the selected cosets implies their total intersection is nonempty. A finite set contains each type at most once. The empty family is allowed. The definition includes the self-pairs; a coset already contains its own representative, so this imposes no extra condition.

The general theorem marked_typed_helly takes:

1. A marked group H, a surjective homomorphism q:H→B, and the induced base marking q(r_i).
2. The complete intersection property for the induced base marking.
3. An explicit multiplicative equivalence ker(q) ≃ ∏_a E_a.
4. A chosen finite label set L(t) for each permitted type and a set of free coordinates A(t), with the exact equivalence

       k ∈ H_(L(t))  iff  every coordinate of k outside A(t) is one,

   for every k in ker(q).
5. Typed Helly for the selected base parabolics.

Its conclusion is TypedHelly for the corresponding actual generated parabolics of H. There is no assumed IP upstairs, common-fiber intersection conclusion, commutativity of a kernel factor, or finiteness of the groups. The coordinate index itself may be infinite in this generic theorem; the written phase130 statement's finite factor set is included. Labels are represented by finite sets, matching the finite-rank written theorem.

The internal theorem typed_helly_transfer allows arbitrary subgroup families P(t),Q(t) with the exact image identities and

    q(P(s) ∩ P(t)) = Q(s) ∩ Q(t).

The separate theorem marked_intersection_image proves this last identity from base IP and the corresponding generated markings. It first uses q(H_(L∩M))=B_(L∩M), then the inclusion H_(L∩M)≤H_L∩H_M. Thus the marked theorem does not leave this substantive premise unbound.

The further theorem supported_kernel_typed_helly takes the literal support hypotheses of the reviewed SupportedKernelGeneration module, base generation, base IP, and typed Helly for any selected family of base parabolics. It concludes typed Helly for those parabolics in the fully generated tuple group. In this theorem every kernel profile and the multiplicative coordinate equivalence are derived from the reviewed construction. Their desired conclusions are not additional inputs.

## Declarations and proofs

All names below are in MathCompression.SupportedKernelHelly.

| Declaration | Proved role |
|---|---|
| right_coset_rebase | If x and y lie in P g, then y lies in P x. |
| right_coset_trans | If x lies in P g and y lies in P x, then y lies in P g. |
| coordinate_constraints_glue | A family of compatible constraints, each fixing a coordinate or leaving it free, has a common solution. This uses sets and choice, without a group law. |
| common_fiber_pair | Two intersecting right cosets can be moved to intersect inside any common base fiber, using the exact intersection-image identity. |
| coordinate_coset_iff | In a fixed base fiber, membership in a right coset is equivalent to equality in its constrained kernel coordinates. Both implications are proved. |
| typed_helly_transfer | The full subgroup-family transfer, including base selection, common-fiber adjustment, and coordinate gluing. |
| marked_intersection_image | Base IP derives the intersection-image identity for actual marked parabolics. |
| marked_typed_helly | The complete general marked coordinate-kernel theorem U.SK.Helly. |
| parabolicInFull_image | A parabolic regarded inside the fully generated group has exactly its stated base image. |
| kernelCoordinatesMulEquiv | The previously proved kernel-coordinate equivalence preserves multiplication. |
| supported_kernel_typed_helly | The actual supported-kernel attachment with all generic profile, image and coordinate premises discharged. |

To prove common_fiber_pair, choose x in the intersection of P(s)g(s) and P(t)g(t). Let z=q(x), and let b be the desired common base point. Since b and z belong to each of the two base cosets, b z⁻¹ belongs to Q(s)∩Q(t). The proved intersection-image identity supplies h in P(s)∩P(t) with q(h)=b z⁻¹. Then hx lies in both original cosets and maps to b. The proof does not assume that images preserve arbitrary intersections.

For the full transfer, the base Helly property supplies b and surjectivity supplies u with q(u)=b. Each selected coset has a point x_i in the b-fiber, obtained by the preceding lemma applied to its self-pair. Put k_i=x_i u⁻¹ in ker(q). A point represented by k u belongs to the same coset as x_i exactly when k k_i⁻¹ lies in its kernel intersection. By the profile, this is equivalent to equality of the coordinates of k and k_i outside the free-coordinate set.

Apply common_fiber_pair also to each pair of distinct selected cosets. Its witness shows that any two constraints fixing the same coordinate fix it to the same value. For each coordinate, choose that value if there is a constraint, and choose identity otherwise. The coordinate equivalence converts the resulting tuple to a kernel element k. Multiplication by u gives a point in every original coset. This is valid for nonabelian factors: cancellation is performed within one coordinate, and no elements within that factor are interchanged.

In the actual SK attachment, parabolics are literally comaps of the ambient generated subgroups under inclusion of the fully generated group. BaseProjection_range proves surjectivity from base generation. The earlier kernelCoordinatesEquiv is upgraded to a multiplicative equivalence because its coordinates are literal projections. The reviewed kernel_profile proves exactly which coordinates can survive in each parabolic. The reviewed marked_intersection_property and the exact parabolic images give the needed intersection-image identities. These are genuine calls to established proof bodies, not restatements supplied as hypotheses.

## Geometry and correction boundary

The theorem proves typed Helly. It does not formalize the entire coset-geometry recognition theorem, the affine presentation calculations for L034, or that source's full construction theorem.

The frozen phase130 geometric corollary requires its additive geometry erratum. A nonidentity involutory image in the base does not force a lift to be an involution: C4→C2 on a singleton support is a counterexample. The corrected geometric statement requires involutory local markers, or a sufficient condition implying that property. Neither the generic Helly theorem nor its SK attachment needs involutivity. Thus omitting an involutivity hypothesis from these algebraic statements is intentional; deriving the hypertope conclusion without the erratum would be invalid. Both the original phase130 attachment and the mandatory erratum are bound as retained mathematical inputs, and the uncorrected geometry assertion is not certified.

## Verification and trust

Run the pinned wrapper with a fresh output directory:

    python3 -B -O research/leemans/phase137_supported_kernel_helly_check.py \
      --packages /path/to/pinned/.lake/packages \
      --lean /path/to/lean \
      --output-dir /path/to/new/output

It rebuilds all five local source modules and the same two pinned Mathlib modules used by the consequence bundle. Eleven new declarations and twenty-three retained printed declarations must report only propext, Classical.choice and Quot.sound. Exact local source hashes, the dependency manifest, compiler version, package revisions and tracked-file cleanliness are checked. Placeholders, warnings, errors and unexpected axioms are rejected. Other compiled package objects and the installed compiler remain trusted; this is not a rebuild of all Mathlib.

The rejection controls alter each of the new Helly source, retained consequence source, retained construction source, retained coordinate source and dependency manifest. They also test occupied regular files, directories, live symlinks and dangling symlinks, checking those paths are not changed.

Additional finite author diagnostics exhaust all typed subfamilies and right cosets in a positive example H=D8×S3×C2 with kernel D8×S3. Both kernel factors are nonabelian. The checker verifies the explicit coordinate isomorphism and every stated algebraic profile and intersection-image premise. Three V4 examples each remove exactly one of the intersection-image, coordinate-profile, or base-Helly assumptions and fail the conclusion; the remaining assumptions and exact coordinate isomorphism are checked. These are diagnostics for the statement's scope. The universal theorem is supplied by the Lean proof, and these author checks do not constitute independent review.

The checkpoint records new proof acquisition separately from the four retained local modules. Its small draft history distinguishes the initial general transfer/SK attachment from the added complete marked-interface bridge. No compression ratio, historical priority, new source-paper admission, or open-conjecture solution is inferred from this formalization.
