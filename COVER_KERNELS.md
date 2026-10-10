# Cover kernels: from subgroup intersections to linear algebra

The [reviewed manuscript](research/case_study/phase46_cover_theorem.md) gives
two conditional classification theorems and one complete finite interval.
The [independent review](research/case_study/phase50_cover_recent_audit.md)
and [root admission](research/case_study/phase54_cover_interval_root_audit.md)
check the written proofs and exact finite computation. The general
multiple-minimal-cover problem remains unresolved here.

Let H be a finite marked regular polytope group, with end subgroups A and B.
Suppose H maps onto R, the smallest regular maniplex cover of a polytope P,
with kernel L, and the map is injective on A and B. In the rotation-group
version, include the mirror automorphism in every invariance condition.
Define the subset

    D = L ∩ AB.

For each normal, mirror-invariant subgroup M of L, the intermediate quotient
H/M remains polytopal exactly when

    M ∩ D = {1}.

Thus one defect set controls the entire interval of possible quotient covers.
Maximal successful kernels give globally minimal regular covers of P. The
list is complete among quotients of H; covers outside that interval require
additional work.

The algebraic mechanism is the exact equivalence

    f(A) ∩ f(B) = f(A ∩ B)
       iff ker(f) ∩ AB = (ker(f) ∩ A)(ker(f) ∩ B).

Products here are subset products. This statement holds for arbitrary groups
and homomorphisms, without finiteness or surjectivity, and is
[proved in Lean](research/case_study/formal/QuotientIntersectionCriterion.scope.md).
The polytope interpretation additionally uses the stated local hypotheses and
standard geometric recognition.

When L is elementary abelian, it is a vector space over a finite field. The
conjugation and mirror actions become linear operators. If it is a direct
sum of pairwise nonisomorphic simple modules, every invariant subspace is a
sum of some of those summands. Record the coordinate support of each nonzero
element of D as a hyperedge. Successful kernels are exactly the coordinate
subsets that contain no hyperedge; maximal such subsets classify the minimal
covers in the interval. If every individual summand avoids D, their universal
preimages generate the entire target kernel. A nonpolytopal R then forces
at least two distinct minimal covers. Existence of such an H and such a
module decomposition is an explicit hypothesis.

There is a second exact case. If L is central of dimension d over F_p,
and the mirror acts by a scalar where needed, D is a subspace of dimension e.
The maximal successful kernels are its complements, so there are exactly

    p^(e(d-e))

of them, each giving a cover of degree p^e over R. For 0<e<d these complements
also generate L. This count applies to the specified interval; it supplies
at least that many globally minimal covers without classifying every cover.

In the worked chiral example, H has rotation order 8,748 and
L is the two-dimensional vector space over F_3. In its explicit basis, the
generator and mirror actions are

    a: diag(1,-1),  b: identity,  c: diag(-1,1),  mirror: diag(1,-1).

The defect is the diagonal line. The two coordinate axes are exactly the
maximal invariant subspaces avoiding it. Consequently the known two covers
are the complete minimal-cover list within this interval. The computation
checks the actual groups, elements, intersections and actions, including all
six subspaces and all four invariant quotients. The kernel is noncentral,
so this example uses the support theorem rather than the central count.

Reproduce that complete finite certificate with stock GAP 4.15.1:

```sh
python3 research/case_study/phase54_cover_interval_verify.py \
  --gap /path/to/gap --output-dir /tmp/cover-interval-new
```

The directory must be new. This public runner needs only the distributed
complete GAP program; primary-source captures are unnecessary. Its program
is byte-identical to the independently reviewed assembly. The historical
author runner remains preserved but checks private source manifests.

The written support and complement theorems are conditional all-parameter
proofs. GAP certifies the finite example; Lean certifies the underlying
algebraic criterion. This package adds no source manuscript to the compression
intake and makes no priority or general-conjecture claim.
