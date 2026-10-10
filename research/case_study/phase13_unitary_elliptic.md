# An elliptic parameter curve for sufficiently large odd unitary groups

Original phase-thirteen proof, 10 October 2026. This proof is separate from the frozen characteristic-three construction. It establishes a large-field bound. The stronger [prime-sieve companion](phase13_unitary_sieve.md) handles the remaining finite range with additional arithmetic and explicit field certificates; that work is not assumed in this note.

**Theorem.** Let q≡1 (mod 4) be an odd prime power. If

    q > 3,715,232,694,272,                                  (1)

then the phase-eleven unitary template has a parameter of full square-field degree and middle projective order q²−1. It therefore gives a rank-four string C-group for PSU₄(q), of type {4,q²−1,2p}, where p is the characteristic. In characteristic three the [phase-twelve theorem](phase12_unitary_parameters.md) already removes the size restriction completely.

A more useful field-specific criterion is

    q+1 > [8W(m)W(n)−4W(m)−4W(n)+2]√q,                   (2)
    m=oddpart(q−1),    n=(q+1)/2,    W(r)=2^ω(r).

The conclusion holds whenever (2) holds, independently of the deliberately coarse threshold (1). These results retain the [generation theorem](phase11_unitary_template.md), [intersection theorem](phase11_unitary_intersection.md), and standard finite-field character-sum machinery stated explicitly below. Priority has not been established.

## 1. The parameter curve and all singular characteristics

For now suppose p≠2,3. Choose a nonsquare d∈F_q*, and δ∈F_(q²) with δ²=d and δ^q=−δ. Consider the projective plane cubic C:

    dXY² + 2dX²Y − XZ² − 2YZ² = 0.                       (3)

In the affine chart Z=1, write its equation as

    F(x,y)=dxy²+2dx²y−x−2y=0.

The three points at infinity are

    P=[1:0:0],   Q=[0:1:0],   R=[1:−2:0].

They are all nonsingular: the Y-derivative at P is 2d, the X-derivative at Q is d, and the X-derivative at R is −4d. At a singular affine point, y=0 would imply x=0, where F_x=−1. For y≠0, the identity

    F−xF_x=−2y(dx²+1)

forces dx²=−1. The equation F_y=0 then forces dxy=2, hence y=−2x. Substitution into F_x gives F_x=3. Thus there are no singular points when p≠2,3. This proves geometric smoothness over the algebraic closure, not just smoothness on rational points.

A smooth projective plane cubic is geometrically integral and has genus one. The rational point O=[0:0:1] exists. The Hasse–Weil bound therefore gives

    |C(F_q)| ≥ q+1−2√q.                                  (4)

The characteristic-three exception is genuine: (3) factors there as

    (Y−X)(dXY+Z²)=0.

Its diagonal component is the rational parametrization used in phase twelve. No elliptic-curve bound is applied to that singular/reducible cubic.

## 2. Divisors and the exact eight punctures

The rational functions x=X/Z and y=Y/Z have

    div(x)=O+Q−P−R,             div(y)=O+P−Q−R.           (5)

For example, in the chart X=1 near P the equation is

    dy²+2dy−z²−2yz²=0,

so z is a local parameter and y=z²/(2d)+higher terms. Thus x=1/z has a simple pole and the affine y-coordinate y/z has a simple zero. The analogous chart at Q gives a simple zero of x and simple pole of y. At R both have simple poles; at O both have simple zeros. This proves (5), including multiplicities, without reading them off from an affine drawing.

Put D₀={O,P,Q,R}. All four points are rational. On C minus D₀, x and y are finite and nonzero. Define

    g=d x²,       μ=(δy−1)/(δy+1),       h=μ².

The function g maps to the split multiplicative group and h to the norm-one torus U over F_q; coefficient conjugation replaces h by h⁻¹.

The zeros of μ have y=δ⁻¹ and x=±δ⁻¹; the poles have y=−δ⁻¹ and x=±δ⁻¹. Let D₁ be these four points. They are distinct, disjoint from D₀, and none is F_q-rational. Each zero and pole is simple: in the affine equation, at y=±δ⁻¹ and x=±δ⁻¹, the derivative F_x=4dxy is nonzero, so y is a local parameter. Hence div(g) has multiplicities ±2 at D₀ and div(h) has multiplicities ±2 at D₁.

In particular V=C minus (D₀∪D₁) is defined over F_q and

    V(F_q)=C(F_q) minus D₀,       |V(F_q)|=|C(F_q)|−4.   (6)

## 3. The character sums, with all boundary terms

Use odd-order characters χ of F_q* and ψ of U(F_q), and sum

    S(χ,ψ)=Σ_(a∈V(F_q)) χ(g(a))ψ(h(a)).

The character sheaves are obtained from the Lang isogenies of G_m and U, as in [phase twelve, Lemma 1](phase12_unitary_parameters.md). Over the algebraic closure the U-Lang isogeny is t↦t^(q+1), so the geometric character order is exactly ord(ψ). Odd character orders ensure that the multiplicities two in §2 do not annihilate local monodromy.

If both characters are nontrivial, their ramification supports are disjoint and consist of all eight points. The tame rank-one local system is geometrically nonconstant. On this genus-one curve its compactly supported Euler characteristic is 2−2·1−8=−8; H_c⁰=H_c²=0, and therefore dim H_c¹=8. The weight estimate and trace formula give

    |S(χ,ψ)| ≤ 8√q.                                     (7)

If χ≠1, ψ=1, use the larger open curve C minus D₀. It has exactly the same rational points as V. Its sheaf is ramified at just four geometric points, so

    |S(χ,1)| ≤ 4√q.                                     (8)

If χ=1, ψ≠1, first sum on C minus D₁. That four-puncture sum has absolute value at most 4√q. At each of O,P,Q,R the function h has value one: the y-coordinate there is zero or infinity, and the Cayley transform has value −1 or +1. Removing these four rational points yields the precise statement

    |S(1,ψ)+4| ≤ 4√q.                                   (9)

Finally S(1,1)=|C(F_q)|−4. This last subtraction is canceled by the Möbius-weighted −4 terms in (9); it must not be silently dropped before the primitive-character expansion.

The retained standard inputs are the smooth-cubic genus formula, the Hasse–Weil bound (4), and the rank-one tame trace/Euler/weight machinery. For the latter the directly inspected primary reference is [Katz, *Gauss Sums, Kloosterman Sums, and Monodromy Groups*](https://web.math.princeton.edu/~nmk/Katz-GKM.pdf), §§2.3.1–2.3.2, §3.6.1 and its proof, and §4.3. This is a written application of those results, not a new proof of Weil's theorem.

## 4. A primitive-pair count

Put m=oddpart(q−1), n=(q+1)/2, A=W(m), B=W(n), and θ(r)=φ(r)/r. Let N count a∈V(F_q) for which g(a) is primitive in F_q* and h(a) has order n in U².

Since d is a nonsquare, every g(a) is a nonsquare and already has the full two-primary part of its order. Since q≡1 (mod 4), n is odd. Thus the primitive/non-power indicators in phase twelve apply without change.

The trivial/trivial term is |C(F_q)|−4. The boundary corrections for χ=1 and ψ≠1 total

    −4 Σ_(b|n,b>1) μ_Mob(b) = +4,

because n>1. The absolute coefficient sums for nontrivial χ and ψ are A−1 and B−1. Equations (7)–(9) now give

    N ≥ θ(m)θ(n){|C(F_q)|
          −4√q(A−1)−4√q(B−1)−8√q(A−1)(B−1)}
      ≥ θ(m)θ(n){q+1−[8AB−4A−4B+2]√q}.              (10)

This proves positivity under the exact field-specific criterion (2).

## 5. Every counted pair gives the required order

At a counted point put

    λ=δx,      μ=(δy−1)/(δy+1),
    t=λ−λ⁻¹,  t′=μ−μ⁻¹.

Equation (3) is exactly tt′=2: direct substitution gives

    tt′=−4y(dx²−1)/(x(dy²−1)).

All displayed denominators are nonzero at rational points of V. We have λ^q=−λ, μ^q=μ⁻¹, λ² primitive, and μ² of order n. Both t and t′ are nonzero and trace zero. Put k=−t−t′; then k^q=−k.

In fact k≠0. Otherwise the identity

    (X²−tX−1)(X²−t′X−1)=X⁴+kX³−kX+1

would have t′=−t. The roots of its second quadratic would then be −λ and λ⁻¹. Both have norm unequal to one, since their norms are −λ² and −λ⁻² and λ² is primitive of order q−1≥4. This contradicts the norm-one root μ of that quadratic.

The four eigenvalues λ,−λ⁻¹,μ,−μ⁻¹ are distinct by the same norm and within-pair arguments as in phase twelve. Their combined order is q²−1. Its halfway power is −1 on the first pair and +1 on the second, so the projective order is q²−1 as well. Phase twelve, Lemma 2, then forces F_p(k²)=F_q. The frozen generation and intersection theorems apply.

## 6. An explicit uniform threshold and its exact limitation

For any odd positive integer D,

    W(D) ≤ C D^(1/6) < 22D^(1/6),
    C=∏_(prime 3≤ℓ<64) 2/ℓ^(1/6).

The bound C<22 is the exact integer inequality

    2^102 < 22^6 ∏_(prime 3≤ℓ<64) ℓ.

All other prime factors have 2≤ℓ^(1/6), and prime-power multiplicities only enlarge D^(1/6). Since gcd(m,n)=1 and v₂(q−1)≥2,

    mn=(q²−1)/2^(v₂(q−1)+1) < q²/8,
    AB=W(mn)<22q^(1/3)/8^(1/6).

The coefficient 8AB−4A−4B+2 is strictly below 8AB. Therefore (2) follows from

    q > 176^6/8 = 3,715,232,694,272.

This proves (1) for p≠3. If p=3 and q≡1 (mod 4), then q is a power of nine and the complete phase-twelve family applies instead.

The threshold is intentionally elementary and coarse. This note alone does not cover every prime power 5≤q≤3,715,232,694,272; completing that range requires the prime-sieve companion. Neither argument addresses q≡3 (mod 4), where the template's center and determinant constraints change. The [symbolic and finite-field checker](phase13_unitary_elliptic_check.py) uses Python 3 and SymPy, and verifies fourteen small prime-field curve counts and direct matrix orders in explicit quadratic-field arithmetic. These are supporting diagnostics; the genus and character-sum reasoning remain written proofs. Internal review is not external peer review.
