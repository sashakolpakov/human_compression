# Independent review of the class-four common-quotient proof

10 October 2026. The complete written proof in
[phase15_common_quotient_class_four.md](phase15_common_quotient_class_four.md)
passes this independent mathematical review. Its exact scope is finite
two-groups of nilpotency class at most four with a nondegenerate string
C-group marking, in arbitrary rank. The review does not establish the
unrestricted common-quotient conjecture or publication priority.

The following points were checked directly, rather than inferred from the
finite examples.

* The lower-central generation and exponent claims use no quotient
  intersection property. Weight-four commutators are central involutions;
  the weight-three generators are the edge squares and adjacent triple
  commutators, up to the fourth term.
* With the stated right-conjugation convention, the local calculation is
  exactly `t^b=[x^-1,c y^-1]=[x,y]t^-1`. For four consecutive vertices
  `a,b,c,d`, the left entry follows from
  `[[[b,c],d],a]=[[[b,c],a],d]` modulo the fifth lower-central term,
  because `[a,d]=1`, followed by the three-vertex Jacobi identity.
  The sign disappears in the elementary abelian fourth term. Thus the
  full table, including its less immediate left and middle entries, is
  valid in the asserted class range.
* All five substitutions (9)–(11) follow at the indicated pairs of
  vertex indices. Contributions from other selected edges disappear
  only after the previously proved selected `p` and `s` relations.
  Undefined boundary terms are handled consistently.
* Section 4 assigns every crossing generator of the fourth term to one
  of the actual parabolics. It does not assert that all of those
  generators vanish. The subsequent square-peeling argument uses this
  factorization and the original intersection property.
* At the first selected edge, the two remaining crossing weight-three
  generators can similarly be moved to their respective sides. The
  abelianness of the third term is available in class four and justifies
  its product decomposition. The final support intersection then forces
  the selected edge commutator itself to be trivial, contradicting
  nondegeneracy.
* The target quotient's intersection property is used only after its
  marked identification with the independently constructed path-cocycle
  group. No intersection property of a lower-central quotient is
  presumed earlier in the argument.

A separate original [GAP/NQ script](phase15_common_quotient_audit.g)
constructs the universal path-involution quotients of class four in ranks
2–6. It checks generation of the third and fourth lower-central terms
and 136 exact local identities, including the direct middle-conjugation
and four-vertex interchange identities. The fresh run passes with GAP
4.15.1 and NQ 2.5.11. Its
[captured output](phase15_common_quotient_audit.log) and
[run record](phase15_common_quotient_audit_run.json) are separate from the
author's checker. These are bounded diagnostics of the reviewed identities,
not a proof by extrapolation. The author's complete rank-three quotient
census was not independently rerun as part of this review.

The [review certificate](phase15_common_quotient_independent_audit.json)
binds the reviewed proof, the author's diagnostic artifacts, and this
reviewer's script and captured run. There is no claim of a Lean
formalization, external peer review, or verified priority.
