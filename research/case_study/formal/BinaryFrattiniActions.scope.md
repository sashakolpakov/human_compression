# Scope of the binary Frattini-action certificate

10 October 2026. The six theorems in BinaryFrattiniActions.lean compile
with the pinned Lean environment. The final source SHA-256 is
`1f550664fdb2ade2f3b74254ee00d866576635ff8384494cc59ffe22fd73ae30`;
the successful private report SHA-256 is
`349ce684f2c2f41eb075ec555a12d942b2c81ec85733d73fc70abf27e25eb6d0`.

Vectors are actual triples of Boolean coordinates. Addition is coordinatewise
xor; a linear map is evaluated from its three columns by selecting and
adding the indicated columns. The theorem `lin_preserves_binary_addition`
checks that these maps preserve that addition. The named x,y,z are the
three nonzero coordinate vectors.

The first map has columns x,sy,sz and the second has columns tx,y,tz,
so they fix x and y respectively. The predicate `compatible` requires
that both maps square to the identity, commute on every vector, and admit
vectors d,f satisfying all three square-extension equations from the
written group proof. In particular the last equation for z is included;
the weaker conditions of commutation and fixed coordinates do not suffice.

`binary_action_classification` and `classified_is_compatible` prove both
directions of the exact four-case classification. The named `_iff` theorem
combines them. The possibilities are the identity pair and the three
explicit pairs whose common nonzero correction line is a coordinate line.
`classified_has_coordinate_support` and `binary_action_has_coordinate_support`
prove the consequence used in the group proof: some coordinate vector w
is fixed by both maps, and each correction S(v)+v or T(v)+v is zero or w.
Thus the certificate proves actual support and fixation, not a predicate
which already assumes the final group-theoretic conclusion.

The finite classification is exhaustive over the specified Boolean vectors.
It uses `decide +kernel`: the kernel checks the resulting finite decision
proof. It does not use `native_decide`, an external solver axiom, a GAP
output or a Python report as a premise. All six theorem dependency reports
contain only propext, Classical.choice and Quot.sound, with no admitted
lemma. The independent review also compared the literal four column pairs
with a separately implemented enumeration and checked nonvacuity.

This is a complete formal certificate for this finite binary action lemma.
It does not formalize the minimum-counterexample induction, Frattini-group
structure, the passage from group conjugation to these coordinates, the
lift to an actual central element, the odd-prime norm argument, or the
nilpotent direct-product theorem. Those are written proofs with separately
recorded internal reviews. No complete Lean proof of cyclic TPP is claimed.

The public portable runner can freshly compile the same frozen source.
Its report is separate from the historical private report bound above.
