# Independent review of the elliptic curve and primitive-parameter sieve

10 October 2026. **PASS for the written elliptic and sieve arguments and
the exact finite-field intake.** This review is independent of the author
and root reviews. It covers [the elliptic estimate](phase13_unitary_elliptic.md),
[the primitive sieve](phase13_unitary_sieve.md), and their two Python
checkers. The all-fields conclusion additionally uses the explicit witnesses
in the 406 exceptional fields; their independent field-arithmetic validation
is a separate root certificate, not a computation claimed by this reviewer.

## 1. Geometric hypotheses and local multiplicities

I checked the projective cubic over an algebraic closure. Its three points
at infinity are distinct and nonsingular in odd characteristic. In the
affine singularity test, y=0 forces the nonsingular origin. Otherwise
F−xF_x=−2y(dx²+1), then F_y=0 and F_x=0 force dx²=−1, dxy=2 and finally
3=0. Thus characteristic three is the only remaining singular characteristic;
the displayed factorization there is correct. It is handled by the frozen
phase-twelve theorem rather than by applying a genus-one estimate to a
singular curve. In other characteristics, geometric smoothness implies
geometric integrality of the projective plane cubic, and its genus is one.

The divisors of x and y were checked at all four boundary points, including
the different affine and projective coordinates in the charts at infinity.
At P, the local projective y-coordinate vanishes to order two in z, so
the rational function y=Y/Z has a simple zero; x=X/Z has a simple pole.
At Q the roles reverse. At R both have simple poles, and at O both have
simple zeros. This gives the claimed degree-two maps and divisors, without
losing a multiplicity at infinity.

At y=±δ^−1, the cubic equation reduces to x=±δ^−1. The derivative F_x
there is nonzero, so y minus its specified value is a local parameter.
The Cayley zeros and poles are all simple. The four points form a set
defined over F_q, but none is rational, and they are disjoint from the
four rational zero/pole points of x. Squaring the two functions therefore
gives multiplicity two at exactly their separate sets of four punctures.

## 2. Character sheaves and boundary corrections

The sheaf machinery is the same precise primary input already independently
read for [phase twelve](phase12_unitary_character_audit.md): Katz,
[*Gauss Sums, Kloosterman Sums, and Monodromy Groups*](https://web.math.princeton.edu/~nmk/Katz-GKM.pdf),
§§2.3.1–2.3.3, the proof around §3.6.1, and §4.3. It supplies the Lang
character-sheaf trace, tame Euler characteristic and weight bound. The
smooth-cubic genus formula and Hasse–Weil bound remain separately declared
standard inputs; neither is proved by a finite diagnostic.

The nonsplit torus's geometric Lang map is t↦t^(q+1); hence its character
has the same geometric order as the given finite torus character. All
characters used have odd order, so local multiplicity two cannot make a
nontrivial character trivial. The ramification supports are disjoint.
For mixed nontrivial characters there are eight punctures on a genus-one
curve, giving Euler characteristic −8 and H_c¹ dimension eight; H_c⁰ and
H_c² vanish. Finite monodromy is pure of weight zero, and the compactly
supported eigenvalues have absolute value at most √q. This gives 8√q.

For the split-only character, the four nonrational Cayley punctures can
be restored without changing rational-point sums, giving the four-puncture
bound 4√q. For the nonsplit-only character, restore instead the four rational
points of the x-divisor. The Cayley square h equals one at every restored
point, including its limiting values at y=∞. Removing them subtracts
exactly four; the correct statement is |S(1,ψ)+4|≤4√q. Consequently the
Möbius-weighted boundary constants cancel the trivial term's subtraction
of four. The stated direct primitive-count coefficient
8AB−4A−4B+2 includes the Hasse–Weil contribution correctly.

## 3. The sieve algebra and exhaustive cutoff

The odd parts of q−1 and (q+1)/2 are coprime, so each sieved prime belongs
to exactly one coordinate. The second primitive condition can be tested
with odd-order characters of U, equivalently those of its odd subgroup U².
The nonsquare first coordinate already has its full two-primary order.
Thus the character indicators impose exactly the required two orders.

For a core a and s remaining primes, the pointwise sieve inequality is
valid even on points outside the core count. In the difference
N(aℓ)−θ(ℓ)N(a), every remaining character has order divisible by ℓ, so
is nontrivial. Its absolute coefficient sum is W(a), before θ-factors.
Using δ=1−Σ1/ℓ, the calculation is

    N(D) ≥ δN(a)−8θ(a)W(a)(s−1+δ)√q
         ≥ θ(a)δ{q−3−[8W(a)(2+(s−1)/δ)−6]√q}.

This verifies both the coefficient and the use of δ>0. When s=0 the
separate coefficient 8W(D)−6 is correct. Both sides of each sufficient
inequality are positive in the relevant range; exact squaring introduces
no false acceptance.

For the uniform bootstrap, ordering the prime factors and replacing them
by the first odd primes decreases δ. Increasing their total number to w
also decreases δ and increases the nonnegative numerator s−1. These
changes give a legitimate worst-case coefficient. When there are at most
c factors, the separately stated no-sieve coefficient is smaller.
The primorial test uses the strict D<q²/8, so its weak numerical inequality
8P_(w+1)≥Q² is sufficient even at an endpoint. The cutoff
ceil((A+1)²) is also sufficient: q−3−A√q≥√q−3>0 in every listed row.
The four intervals therefore join with no gap or missed boundary value.

The finite intake enumerates primes by a complete sieve and then all of
their positive integer powers below 98,660. It selects exactly q≡1 mod4,
p≥5; characteristic-three fields in that congruence class are exactly the
already covered powers of nine. Its factor table extends beyond every
q±1 that is queried. All core sizes from zero through all prime factors
are tried. This produces the stated exhaustive list of 406 witness fields,
not a conjectural list derived from random sampling.

## 4. Parameter transfer and executed checks

The cubic identity gives tt′=2 with no vanishing denominator at a rational
interior point: dx² and dy² are nonsquares. If k=−t−t′ were zero, the second
quadratic would have roots −λ and λ^−1, neither of norm one because λ²
is primitive of order at least four. This contradicts its norm-one root.
The four eigenvalues are distinct, have combined order q²−1, and their
halfway power has both +1 and −1 eigenvalues. Thus the scalar quotient
does not halve the order. The already reviewed square-field lemma then
supplies the full field needed by the retained generation theorem.

I inspected both Python programs and executed unchanged copies in fresh
temporary directories. Both exited zero. Their reports matched the author's
reports exactly after removing only the execution timestamp. The saved
independent reports are
[phase13_unitary_elliptic_independent_run.json](phase13_unitary_elliptic_independent_run.json)
and [phase13_unitary_sieve_independent_run.json](phase13_unitary_sieve_independent_run.json).
The first checks exact symbolic identities, the universal constant/threshold,
and curve/primitive-pair/matrix-order diagnostics in fourteen prime fields.
The second checks all four rational bootstrap calculations and the complete
4,795-field intake, leaving 406 fields with maximum 43,889.

These executions do not prove a character-sum theorem, and they do not
validate the full exceptional-field witness list. In particular q=5 is
correctly a negative control for the elliptic branch: it has just four
boundary rational points and no primitive pair. Its separate plus-branch
parameter has matrix order 52 and projective order 26. The other 405
fields use their specified exact elliptic witnesses. The author has
supplied all 406 records, and the separate root certificate reports an
independent finite-field validation; neither execution is attributed to
this reviewer.

The final group conclusion retains the phase-eleven generation and
intersection theorems, including their declared inputs. The maximum-rank
conclusion additionally retains the previous upper bound. Nothing here
addresses q≡3 mod4, establishes publication priority, or constitutes a
complete Lean formalization or external peer review.
