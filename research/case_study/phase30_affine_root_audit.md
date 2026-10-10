# Independent root review of the regular affine obstruction

The final written affine construction passes mathematical review. The
independent [product-coordinate checker](phase30_regular_halving_root_check.py)
also passes: it imports no authored checker and represents the seed as a
five-point permutation together with a separate binary coordinate. The
author uses seven-point permutations. Both implementations recover the
same finite hypotheses and strict local subgroup intersection.

## The geometry is established before its group conclusion

The construction retains the seed vertex or face as part of every higher
object. Incidence between higher objects requires both incidence of their
seed labels and intersection of their affine spaces. This matters: ordinary
affine intersection alone would introduce extra flags. A chamber consists
of a translation vector and a seed chamber. Every flag extends by choosing
its common vector or an endpoint of its prescribed edge, then extending
the resulting seed flag. Panels have precisely the two completions supplied
by the seed map or the two endpoints of an edge.

The residue case split is exhaustive in rank four. At a vector the residue
is the seed map, with reordered types. At an edge it is a join of three
two-element sets. At a single higher object its connected lower graph
joins all other residue objects. For two higher objects the common lower
graph is connected precisely because the intersection of the two translation
spaces is spanned by their common edge columns. The global lower graph is
connected because all columns span the quotient. These prove residual
connectivity directly; no quotient-IP or coset-geometry assumption supplies it.

Translation followed by the seed action is regular on the chamber
parametrization. Thin chamber-gallery propagation then identifies the full
type-preserving group. Distinct nonzero columns give a simple lower graph;
the complete column-membership tests give exactly the endpoint-shadow
condition B2. The marking has pair orders 4,5,5,2,2,2, so the indicated
leaf satisfies the actual source hypotheses.

## Independent exact evidence

The root first reproduced the binary dimensions with a different equivalent
seed marking. Its final standalone checker uses the same explicit seed as
the author but a different representation and implementation. It checks all
355 seed flags, their 120 chambers, every panel and every residue of corank
at least two. Each chamber has exactly one common coset element, certifying
the seed's regular action. It checks the seed's 64 subgroup meets as a
separate property.

The 24 block sums span a code of dimension 17 in 30 coordinates. The quotient
has dimension 13 and thirty distinct nonzero columns. All 720 column tests
and all sixty actual intersections of the sixteen-element block spaces pass.
The checker verifies code invariance under the three seed generators and
faithfulness of the seed edge action. It then constructs the local semidirect
subgroups explicitly. Both changed three-generator subgroups equal their
old subgroups and have order 160. Their intersection has order eight; the
subgroup on their common changed generators has order four. The old endpoint
translation is an explicit element in the difference.

Each individual block has one odd five-term relation and rank four. Its
graph contains a five-cycle. Each incident pair has a common square; the
literal double-cover check yields two disjoint squares. This also proves
the residual-connectivity failure directly. The count 122,880 of affected
higher pairs follows from 983,040 original chambers and eight chambers per
square residue. These global counts use the written affine theorem; neither
implementation enumerates the entire 983,040-element group or incidence system.

The corrected final proof distinguishes global chamber connectivity from
residue chamber connectivity. The transformed global chamber graph is
connected because its new marking generates the full group. Its specified
rank-two residues have disconnected chamber graphs. These facts are compatible.

## Exact source claim

The root reread the inspected preprint's introductory Theorems A and B,
the definitions and standing assumptions, Theorem 3.18, and section 4 through
Theorem 4.4 and the degeneracy discussion. The example refutes the broad
residual-connectivity assertion even when the input is regular and thin.
It also refutes the claimed preservation of regular hypertopes and the
unqualified C-group consequence in the surrounding discussion.

The literal Theorem B / Theorem 4.4 sentence asserts a coset isomorphism.
That narrower assertion is not refuted here: the new maximal parabolics can
still give the transformed coset geometry despite its failed intersections
and residual connectivity. The revised journal body remains inaccessible
and unverified. No correction-priority or new-open-problem resolution is
claimed. This is an internal mathematical and computational review, not
external peer review or an end-to-end Lean proof.
