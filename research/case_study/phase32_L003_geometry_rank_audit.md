# Independent audit of the fixed-parameter L003 hypertope family

10 October 2026. **PASS for the stated fixed-s=6 construction**, including the infinite integer action and every even coordinate modulus. This is internal review, not external peer review or a resolution of the source's varying-parameter problem.

The reviewed [proof](phase32_L003_fixed_parameter_hypertopes.md) has SHA256 `76378eb5a0cd6cfc568eaa1aed5f965deeff748327371cf49a5dd4fe29cf029b`. I read the entire proof and checker, reran the checker in a fresh temporary output, and compared the result byte for byte with the final authored report. The independent replay is [phase32_L003_geometry_rank_run.json](phase32_L003_geometry_rank_run.json).

## Exact computation

The doubled right-action definitions give four actual involutions. The source rotations are their products with the copy swap. The checker tests all ten rotational relations on all 432 underlying states, so simultaneous inversion on the second copy is verified rather than assumed to preserve the presentation.

Every proper marked subgroup is closed as a set of exact integer transformations. Recording one transformation per underlying permutation, and rejecting any conflicting voltage, proves both finiteness and injectivity of the projection. Closure under involutory generators is enough; no sampling or arbitrary search cutoff is used to certify completion. In particular, every maximal parabolic injects into every coordinate reduction.

The full underlying permutation image has order 432. Its 1,728 exact Schreier loops generate the integer translation kernel; their binary images span dimension six. This proves the mod-two group order 27,648. I checked the implementation's permutation pullback in binary multiplication against its earlier exact integer composition. All 225 proper/proper subgroup meets are directly compared; the remaining 31 meets with the whole group are identities.

The typed-coset calculation is separate from those meets. Right cosets of the intersection in one chosen base parabolic enumerate all incident objects. Membership of a representative in the product of two parabolics is exactly the relevant coset-incidence condition. Each of the sixteen common-incidence counts equals the size of the displayed intersection-stabilizer orbit. Induction on flag size therefore proves flag transitivity and typed Helly. It does not follow merely from the subgroup intersection property.

## Uniform transport and geometry

For the quotient lemma, normalize one coset to a maximal parabolic P0. All other representatives then lie in P0. A downstairs common point lifts inside P0. The downstairs intersection equality supplies a lift of each difference in the actual common marked subgroup; injectivity on P0 identifies that lift with the required difference. This proves typed Helly upstairs, with no finite-group or central-kernel assumption. The subgroup-IP lift uses the same local injectivity in a proper marked subgroup.

The lemma applies to the infinite integer action over its mod-two quotient, and to every even-modulus action over that quotient. Proper local subgroups are unchanged. Flag transitivity, trivial chamber stabilizer and order-two panel stabilizers give a thin geometry; the remaining marked generators connect every residue's chambers. Thinness and chamber connectivity also identify the displayed regular group with the full type-preserving automorphism group.

The pure translation witness has exact order m after reduction modulo m. Thus the even-modulus group orders are unbounded. This proves infinitely many finite regular hypertopes at the same four residue parameters; it does not treat m as a new torus parameter or assume a formula for the coordinate-reduction lattice index.

## Source bridge and scope

I read the primary manuscript's equations (2.3)–(2.4) and §8, alongside the already reviewed parameter presentation and Problem 9.2. All four final local adapters check algebraically. In the order of omitted types 0,1,2,3 they use `(u,v)=(zy,zx),(y^-1 z,y^-1),(x^-1,x^-1 z),(x,y)`. Their torus words are exactly the four verified specialized source relations. The retained triangular-lattice presentations and their full orders 36,432,48,108, together with matching exact image orders, identify the marked local groups; order alone would not suffice.

The proof establishes fixed parameters `((3,0),(2,0),(1,1),(6,0))`, finite and infinite regular examples, and an exact finite certificate supporting the uniform quotient argument. It does not identify the universal group, settle which other parameter values occur, or resolve the literal Problem 9.2. The separately completed Lean infinitude theorem does not formalize this geometric supplement.
