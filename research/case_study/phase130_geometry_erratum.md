# Additive correction to Corollary U.SK.Geometry

This note corrects the frozen `phase130_typed_helly_L034.md`, SHA-256 `b52accdbd852b2383f3f5aa5a138e05190495ada91358cca633a71684e861b03`. Its original bytes remain unchanged. The correction was identified by the root's independent reading.

Replace the first sentence of Corollary U.SK.Geometry with:

> In the supported-kernel realization U.SK, assume the base marking gives a regular hypertope and every marked generator in every attached group is an involution. Then the resulting marking also gives a regular hypertope, and its full type-preserving automorphism group is the constructed group.

Replace the proof sentence “The generators remain nonidentity involutions because their base images are such” with:

> Each constructed generator is a tuple whose base coordinate and every nontrivial attached coordinate are involutions; hence its square is the identity. Its base image is nonidentity, so its order is exactly two.

The added hypothesis cannot be omitted. For a one-element type set and its singleton support, take base C2, attached group C4, and the quotient C4→C2. The only proper local parabolic is trivial, so U.SK's proper-parabolic injectivity hypothesis holds. The resulting group is C4 and its distinguished generator has order four. A nonidentity involutory image does not make the generator itself involutory.

A sufficient alternative hypothesis is that every support has size at least two. Indeed, a singleton subset of such a support is proper; injectivity on its marked cyclic subgroup, and its nonidentity involutory image in the base, force that local generator to have order two. All three supports in the L034 application are pairs. Their attached groups are explicitly marked dihedral groups with involutory generators, so both formulations apply. At the invocation of U.SK.Geometry in §3, insert:

> The three supports have size two, and their local dihedral markers are involutions; the additional hypothesis in the corrected U.SK.Geometry therefore holds.

The typed-Helly theorem itself, the supported-kernel subgroup calculations, and all L034 parameter, presentation and order proofs are unchanged. This note is an additional required mathematical input whenever the geometric corollary is used or the full L034 recovery is assessed. It is not a claim that the original corollary was correct as written.
