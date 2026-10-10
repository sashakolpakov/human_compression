# Simultaneous matching: formal scope

[SimultaneousMatching.lean](SimultaneousMatching.lean) proves an equivalence
between existence of one common eligible image and existence of a
coherent family of preimages, for arbitrary indexed types with a chosen
anchor. Classical choice supplies the simultaneous preimages.

The remaining declarations define a four-element group, prove its
multiplication and inverse laws and the relevant subgroup closures,
identify a translated coset, and prove that three cosets intersect
pairwise but have empty common intersection. The regular action is
faithful. There are twelve printed axiom reports in total.

The [fresh public compile](SimultaneousMatching.check.json) uses Lean
4.32.2 and imports only `Std`. The reported axioms are `Classical.choice`
and `propext`; there is no `sorryAx`, added axiom or native-evaluation
axiom. The compiler and its distributed standard library remain trusted.

The file does not define the source's incidence geometries, identify
their full automorphism groups or formalize the geometric reconstruction
theorem. Those arguments remain in the [written application](../phase187_parallel_gluing.md)
and [review supplement](../phase191_parallel_gluing_review.md), supported
by two independent finite reconstructions. The finite control changes
the third coset to contain the identity; the resulting false declarations
fail to compile.
