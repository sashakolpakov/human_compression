# Root review of the multiples-of-three parameter family

Date:2026-10-10. PASS after complete final proof/code/source-adapter review.

The same nine source words hold literally on544 integer states. For
T=y(zy)^2 the underlying permutation has exact order3 and A=T³ is a
translation with coordinates0,±2. The displayed conjugate B gives the
two-coordinate matrix [[0,-2],[-2,0]]. Reducing modulo2m therefore gives
independent translations of exact order m. The proof cancels2 in integer
divisibility, rather than assuming2 is invertible modulo2m.

Both translations vanish modulo2 and lie in the exceptional parabolic.
Its image order108 yields lower bound108m². The exact source toroidal
presentation bounds it above by12(3m)², giving the marked local isomorphism.
The other three integer parabolics close with unique weights per underlying
permutation, so they inject into every quotient and into the mod2 base.
One-exceptional transport gives full IP and typed Helly; the standard
chamber argument gives the regular thin residually connected geometry.
All four local rotation substitutions match the previously source-checked
presentation. There is no collapse of the claimed source parameter.

A fresh run of the author checker reproduced its saved report byte-for-byte:
4896 integer relator/state checks, exact base order13824,256 subgroup meets
and16 nonautomatic Helly cardinalities. This is a replay of the author's
implementation.

A separate root implementation extends the earlier independent Cayley
component checker to the actual mod2 permutations. It enumerates all56225
typed pairwise-incident flags and asserts a common representative for each.
The13824 chambers have singleton intersections; all256 marked meets pass.
The enumeration tests pairwise incidence before common intersection and
therefore does not assume the property it checks. It imports no author
implementation and replaces the orbit-cardinality test by exhaustive flags.

The generic transport theorem is separately Lean-checked. The voltage and
source adapter are not an end-to-end Lean proof. The retained toroidal
presentation/order formula, current-priority gap and unproved parameters
coprime to6 remain explicit. No universal order or infinity marker follows.
