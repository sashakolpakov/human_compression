# Independent review of the second unitary congruence class

10 October 2026. Internal mathematical review by the survey-audit agent, independent of the author and of the root review. This record binds the frozen authored package through the accompanying JSON. No authored proof or earlier certificate was modified.

**Verdict: PASS.** No mathematical gap was found in the five-note chain proving rank-four string C-group existence for every prime power $q\equiv3\pmod4$, $q\ge7$. Independent standard-library computations reproduce the complete sieve and verify every exceptional-field coordinate. The separate full group certificates for $q=7,11$ remain explicit computational inputs. This verdict is an internal review, not external peer review, a novelty determination, or a full formal proof.

## 1. Exact material reviewed

The complete frozen [generation](phase15_unitary_generation.md), [intersection](phase15_unitary_intersection.md), [parameter reduction](phase15_unitary_parameter_reduction.md), [curve](phase15_unitary_curve.md), and [sieve/completion](phase15_unitary_sieve.md) notes were read. The frozen [author manifest](phase15_unitary_manifest.json) records 23 authored artifacts; every listed artifact and retained dependency was checked against its stated SHA256. The q11 note and complete GAP checker were also read. This review does not claim to have freshly executed the author's symbolic checker, GAP searches, or q7/q11 subgroup-closure checks.

Two independent executable checks were written and run:

- [Sieve checker](phase15_unitary_sieve_independent_check.py) and its [report](phase15_unitary_sieve_independent_check.json). It imports no author code and independently uses an Eratosthenes sieve, trial-division factorizations, exact fractions, and cleared-denominator inequalities.
- [Field-witness checker](phase15_unitary_witnesses_independent_check.py) and its [report](phase15_unitary_witnesses_independent_check.json). It imports no author code or GAP arithmetic. It uses polynomial quotients, Rabin irreducibility checks, a separately implemented quadratic extension, and direct matrix multiplication and powering.

## 2. Generation and intersection arguments

The rank-one generation argument correctly distinguishes projective special unitary from projective general unitary groups. The determinant-one lift of the diagonal involution places the block group in PSU2. The diagonal and off-diagonal involutions form a Klein four group, excluding a Borel; a Klein four in a dihedral group contains its central involution, and the third involution commutes with none of its three nonidentity elements. The full trace-square field excludes every conjugate subfield subgroup. The odd extension degree and the explicit prime-field order-greater-than-five condition correctly handle Dickson's exceptional cases. The exact retained list was checked in Proposition 2.3 of the cached primary paper `sources/psl2_chiral2017.txt`, lines 195–245; it is not a claim to reprove Dickson's theorem.

The kernel word has scalar first block and nontrivial second projective block. Taking the kernel's derived subgroup removes all first-block scalars, including possible fourth roots of unity. Perfection then supplies the full second coordinate SU2, and the previously proved connected coordinate-pair elimination supplies SU4. This proves generation independently of the intersection argument.

For intersections, the actual form multipliers are signs. Two lifts of a common projective element differ by a scalar in $\mu_4$ whose square is a sign. Thus the use of the sign-restricted simultaneous stabilizer is justified. Its quotient by the four-element scalar center has order at most the exact common stabilizer, without losing a factor four. Quadratic semilinear descent identifies the exact alternating-form stabilizer with Sp4; the earlier descent argument does not require the earlier congruence class.

The middle rotation is semisimple and cyclic. Its roots are distinct and no pair differs by a sign; its square is therefore regular semisimple. Every factor in the displayed discriminant of the form ratio is nonzero under the stated hypotheses, so its centralizer agrees with the rotation's diagonal algebra. The symplectic torus bound retains the mixed torus $C_{q-1}\times C_{q+1}$ in the minus case: its order is still exactly the required upper bound $2m$. The plus case excludes it by the stated coprimality. This is an order argument, not an erroneous exclusion by the mixed torus exponent.

Both rank-three checks were read and independently checked algebraically. For the left triple, all six off-diagonal form entries are nonzero, forcing any diagonal sign similitude to be scalar. For the right triple, Cayley–Hamilton gives the displayed two-parameter form of every power. The even-power off-diagonal entry forces a scalar power. The odd-power off-diagonal entry and diagonal difference cannot vanish simultaneously. These establish the two required rank-three intersections, and the exact maximal-parabolic intersection gives full rank-four IP by the retained recursive criterion.

## 3. Parameter reduction

The theorem explicitly assumes four distinct quartic eigenvalues. Large projective order forces the full square field: a proper subfield has odd index at least three, while the same characteristic polynomial occurs in SU4 of that subfield. The elementary semisimple order bound $(q_0+1)^4$ is smaller than $(q_0^6-1)/2$, including $q_0=3$.

For a fixed first parameter there are exactly $q+1$ compatible second-block choices. The composite-field argument excludes at most six; the prime-field argument excludes at most 26, including the rank-one small-order possibilities. The small fields below 27 are handled separately, rather than covered by that inequality. For a primitive norm witness, the four explicitly listed eigenvalues are distinct and the greatest common divisor of their exponent differences with $q^2-1$ is two. This gives the exact projective middle order, not merely a divisor bound.

## 4. Twisted curve and character sums

The smoothness calculation was checked on the affine and boundary charts. In characteristics other than two and three, the smooth bidegree $(2,2)$ curve is geometrically connected of genus one. Its eight punctures are distinct, are simple zeros or poles of the coordinate functions, have disjoint coordinate supports, and contain no rational point for the twisted field structure. Raising coordinates to the $q$th power and interchanging them is the defining Frobenius endomorphism; the inverse geometric-Galois convention in the trace formula only changes character inverses and does not change the estimates.

The Lang character calculation was checked explicitly, including even-order characters. Writing the Lang map as

$$L(u,v)=(u/v^q,v/u^q)=(x,y)$$

gives

$$u^{q^2-1}=(xy^q)^{-1}.$$

Thus the local exponents are $\pm1$ and $\pm q$. Since $q$ is coprime to $q^2-1$, every nontrivial character retains its full order at every simple puncture. In particular, a quadratic character is not accidentally killed by a doubled divisor. There is no cancellation between the disjoint coordinate supports. The pulled-back finite-order rank-one sheaf is tame, pure of weight zero, and geometrically nonconstant; its compactly supported degree-zero and degree-two cohomology vanish. Euler characteristic gives dimension eight in degree one, and the retained weight bound gives $8\sqrt q$.

In characteristic three, each rational component is preserved by the twist. On the chosen component, the fixed-point cross ratio converts the rationality condition into a norm equal to minus one, giving exactly $q+1$ points. The four simple punctures are nonrational and all genuinely ramified, giving dimension two and the $2\sqrt q$ estimate. Intersections with the other component are ordinary points on this smooth component; their first coordinate has order four, so they never count as primitive for $q\ge27$.

The retained sheaf results were freshly inspected in [Katz's primary monograph](https://web.math.princeton.edu/~nmk/Katz-GKM.pdf), §§2.3.1–2.3.2, the proof of §3.6.1, and §4.3 (PDF pages 20, 24, 33–34; the last section is printed pp.59–60). These supply the tame Euler formula, trace/weight estimate, and rank-one Lang construction. The present proof supplies the specific twist, ramification, and nontriviality calculations. The Weil machinery remains a substantive retained theorem.

## 5. Exact sieve and finite completion

The primitive-character coefficient mass and the prime-by-prime lower sieve were checked with the prime two included. The genus-one coefficient is

$$8W(a)\left(2+\frac{s-1}{\delta}\right)-6,$$

and the characteristic-three coefficient is obtained by replacing eight by two and minus six by minus two. The empty omitted-prime list is handled by the direct bound, not by an invalid division convention.

The independent sieve recomputes the initial cutoff $725311328745792$ and all three primorial reductions, ending at $1029254$. The comparison against first primes bounds every actual support, including supports shorter than the proposed core. Endpoint positivity follows from $q+1>A\sqrt q$ when $q\ge\lceil A^2\rceil$.

The executable comparison passes for **40,389** eligible field sizes and **80,778** factorizations of $q-1$ and $q+1$. Every exact positivity record agrees with the author report. The exception set has **1,699** distinct fields, largest **245,519**.

The independent field checker proves that the coordinate list is exactly this exception set. All **1,697** primitive norm records pass: prime characteristic, irreducible field presentation, exact multiplicative order, norm equation, exported parameter coordinates, four distinct quartic roots, and the required projective order. The full square field is also explicitly checked for the **1,694** such records with $q\ge27$.

The three direct parameter records also pass independently:

| Field | Exact projective middle order | Exact rank-one projective orders |
|---:|---:|---|
|19|181|9, 10, 10|
|23|265|11, 11, 11|
|43|924|21, 11, 3|

For these records the independent checker verifies determinant one, Hermitian preservation, projective involutions and distant string relations, sphere and nondegeneracy conditions, and every exact displayed order. The q19 and q43 records replace norm-curve witnesses in the exception list; q23 is an additional direct record because the generic second-block count begins at 27.

The q7 and q11 cases rely on their separate full finite certificates. The q11 checker was inspected: its natural matrices and permutation-group order give a valid order sandwich, so neither faithfulness nor the ambient projective-group identity is assumed. All 16 subgroup closures and 256 intersections are computed there. This audit does not claim a fresh q7/q11 execution; the root's independent run is a separate record. In particular, the small examples are not incorrectly covered by the sufficient rank-one order criterion.

## 6. Conclusion and boundaries

The chain covers all $q\equiv3\pmod4$, $q\ge7$. Combining it with the separately reviewed earlier congruence class and upper bound gives rank four for every odd $q\ge5$; the further exact rank-set claim retains the published rank-three input. PSU4(3) is excluded by the retained published nonexistence theorem. No statement about that exceptional group is inferred from the new construction.

No source classification, character-sum theorem, or full finite subgroup computation is silently replaced by sampling. No publication-priority claim follows from these checks. The package has no full Lean formalization. The executable evidence verifies explicit finite arithmetic; the unbounded mathematical argument is the written proof reviewed above.
