# Root interface review and fresh Lean replay of both triangle quotients

10 October 2026. PASS for the exact group-theoretic contracts below. I read
both complete Lean sources, both author scope notes and their pinned runners.
I compared the ten sourceWord entries with the frozen literal rotational
presentation and the fourteen universalWord entries with the four-involution
definition in the universal-geometry manuscript. The marked rotations have
the same order and spelling in both interfaces.

The base module defines the exact six-relator triangle group and ten-relator
source as PresentedGroup types. Its opposite-permutation action implements
the stated row convention. Every auxiliary involution/braid identity used
by the coordinate reductions is proved from the six triangle relations.
The parameter word and its s-th power are uniform in the natural parameter.
No finite numerical specialization or target relation is postulated.

The source homomorphism lands in the explicitly defined row wreath group.
The first-coordinate map is restricted to the actual kernel of the outer
permutation projection, which proves multiplicativity. Its three exhibited
source elements map to the three generators of the actual triangle
presentation; generation proves surjectivity. Infinitude then passes from
that quotient to the kernel subgroup and from the subgroup to the source.

The second module proves reversal by the explicit pure permutation F,
constructs F,FX,FY,FZ, and verifies all fourteen involutory defining words.
The four extra words reuse the literal sourceWord entries through the exact
rotations r0*r1, r0*r2, r0*r3. The direct universalMap has its own source
kernel and the same three triangle-generator witnesses. It assumes neither
an embedding of the rotational group nor the retained semidirect-product
identification of the two source presentations.

I freshly compiled both exact public sources through the public verify_lean
runner in a new output directory. Four absent mathlib dependency objects
were built in a private overlay; the pinned installed checkout was left
unchanged. Both modules passed without warnings, and all eight central
declarations report only propext, Classical.choice and Quot.sound. There
are no native-evaluation or unproved-placeholder axioms in these modules.
Existing compiled dependency objects and the compiler remain trusted inputs.

The final two infinitude statements explicitly assume Infinite(Triangle s).
The separately reviewed real-matrix proof discharges that hypothesis on
paper for every integer s≥6. Its trigonometry and spectral argument are not
formalized by these two modules. Universal hypertope geometry, exact local
orders, the small finite baseline, and bibliographic priority also remain
outside this formal scope. The algebraic interfaces are valid for every
natural s, while the geometric identification retains s≥2.

This closes the group-map and subgroup-surjection portion of the existing
written theorem for both presentations. It adds no source-manuscript credit
or length ratio. The independent current-state report remains frozen at
its earlier thirty-six-module snapshot; this is a later additive result.
