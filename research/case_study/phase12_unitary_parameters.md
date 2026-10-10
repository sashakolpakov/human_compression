# A rank-four unitary family over every field of size 9^e

Private phase-twelve proof, 10 October 2026. This is an original parameter-existence argument, conditional only on the explicitly retained character-sum machinery below and the frozen phase-eleven generation and intersection theorems. It does not assert priority or a construction for every odd field size.

**Theorem.** For every integer e≥1, put q=9^e. There is a nonzero k∈F_(q²) such that

1. k^q=−k and F₃(k²)=F_q;
2. the middle matrix T=r₁r₂ of the [unitary template](phase11_unitary_template.md) has projective order q²−1.

Consequently the template and the [intersection criterion](phase11_unitary_intersection.md) give a rank-four string C-group for PSU₄(q), of Schläfli type {4,q²−1,6}. Combined with the previously proved [unitary upper bound](phase9_linear_unitary.md), its maximum string C-group rank is four. The latter conclusion retains the complete phase-eight and phase-nine rank-obstruction arguments; it is not part of the character-sum proof.

The new step is uniform in e. The finite arithmetic table in §3 handles only seven small exponents in an otherwise uniform estimate; it contains no finite-group classification or exhaustive group search.

## 1. A split/nonsplit torus character estimate

This lemma works for every odd q. Write E=F_(q²), choose δ∈E* with δ^q=−δ, and let U={u∈E*:u^(q+1)=1}. For x∈F_q* set

    g(x)=δ²x²,              h(x)=((δx−1)/(δx+1))².

Here g(x)∈F_q* and h(x)∈U. Their denominators do not vanish at rational x, since δ∉F_q.

**Lemma 1.** Let χ be a nontrivial odd-order multiplicative character of F_q*, and ψ a nontrivial odd-order character of U. Then

    |Σ_(x∈F_q*) χ(g(x)) ψ(h(x))| ≤ 2√q.                 (1)

If exactly one character is nontrivial, the corresponding sums are

    Σ χ(g(x)) = 0,                Σ ψ(h(x)) = −2.        (2)

**Proof of (1), including the nonsplit descent.** Over F_q consider the morphism

    f: V → G_m × U,
    V=P¹ minus {0,∞,δ⁻¹,−δ⁻¹},     f(x)=(g(x),h(x)).

The second expression defines an F_q-morphism to the norm-one torus: applying the nontrivial E/F_q automorphism to its coefficients replaces it by its reciprocal. Pull back the exterior product of the rank-one character sheaves attached to χ and ψ by the Lang isogeny of the respective tori. These sheaves are defined over F_q, including for U, and the trace at a rational point is exactly χ(g(x))ψ(h(x)). No extension of ψ to a character of E* and no sum over E-rational points is used.

After extending the coefficient field and the base to algebraic closures, the first factor is a Kummer sheaf on g(x), with nontrivial local characters at 0 and ∞. The second is a Kummer sheaf on h(x), with nontrivial local characters at δ⁻¹ and −δ⁻¹. At each of these points the relevant zero or pole has multiplicity two. The character orders are odd, so these local characters remain nontrivial. The two supports are disjoint. Thus their tensor product L is tame, rank one, and ramified at exactly four geometric points. In particular it is geometrically nonconstant.

The Euler–Poincaré formula gives χ_c(V,L)=2−4=−2. Since V is affine, H_c⁰=0; geometric nonconstancy gives H_c²=0. Therefore dim H_c¹=2. The sheaf has finite monodromy, hence is pure of weight zero; the eigenvalues on H_c¹ have absolute value at most √q. The trace formula now proves (1), since V(F_q)=F_q*.

These are retained standard facts, rather than a new cohomology theorem: the exact references in [Katz, *Gauss Sums, Kloosterman Sums, and Monodromy Groups*](https://web.math.princeton.edu/~nmk/Katz-GKM.pdf) are §§2.3.1–2.3.2 (Euler characteristic and trace), §3.6.1 and its proof (the H_c¹ weight estimate), and §4.3 (Lang character sheaves for smooth connected commutative groups, including nonsplit tori). The needed passages were read in the primary author-hosted text. The finite-monodromy special case also follows by applying the Weil bound to a finite covering curve and taking the character eigenspace.

For (2), χ(δ²)Σχ(x²)=0 because χ² is nontrivial. The Cayley map x↦(δx−1)/(δx+1) is a bijection P¹(F_q)→U, with 0↦−1 and ∞↦1. Since ψ² is nontrivial, its sum over U is zero. Removing these two points subtracts 1+1, giving −2. ∎

## 2. Counting simultaneous primitive parameters

For the rest of the proof q=9^e. Put

    m=oddpart(q−1),       n=(q+1)/2,
    θ(d)=φ(d)/d,          W(d)=2^ω(d),    θ(1)=W(1)=1.

Both m,n are odd, coprime, and not divisible by three. The element g(x)=δ²x² is a nonsquare in F_q*. Therefore it has the full two-primary part of the order q−1. It is primitive exactly when it is not an ℓ-th power for each prime ℓ|m.

Write μ(x)=(δx−1)/(δx+1). The element h(x)=μ(x)² lies in the subgroup U² of order n. It has order n exactly when it is not an ℓ-th power in U for each prime ℓ|n. (Because ℓ is odd, this is equivalent to the same condition within U².)

For a cyclic group C and a squarefree-support divisor d of |C|, the indicator of these non-power conditions is

    θ(d) Σ_(a|d) μ_Mob(a)/φ(a) Σ_(ord χ=a) χ(z).          (3)

This follows prime by prime from character orthogonality: the sum of all characters of order ℓ is ℓ−1 on ℓ-th powers and −1 elsewhere. Multiplying the resulting local indicators proves (3), including d=1.

Let N(q) count x∈F_q* for which g(x) is primitive and h(x) has order n. Apply (3) in F_q* and U, and expand. The trivial/trivial term is q−1. Terms with χ nontrivial and ψ trivial vanish by (2). The total contribution with χ trivial and ψ nontrivial is

    −2 Σ_(b|n, b>1) μ_Mob(b) = 2,

because n>1. This is the reason that the main term below is q+1 even though the summation domain has q−1 elements. The absolute sum of coefficients over nontrivial χ is W(m)−1, and similarly it is W(n)−1 for ψ: there are φ(a) characters of each order a, canceling the denominator in (3). Lemma 1 gives

    N(q) ≥ θ(m)θ(n)
           [q+1 − 2√q (W(m)−1)(W(n)−1)].               (4)

No rounding or asymptotic error is hidden in (4).

## 3. Positivity for every exponent

For every odd integer D not divisible by three,

    W(D) ≤ C D^(1/6) < 13 D^(1/6),
    C= ∏_(prime 5≤ℓ<64) 2/ℓ^(1/6) < 13.               (5)

For primes ℓ≥64 each factor 2/ℓ^(1/6)≤1, while repeated prime factors only increase D^(1/6). The sixteen primes in (5) are 5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61. The bound C<13 is certified without floating point by

    2^96 < 13^6 · ∏_(prime 5≤ℓ<64) ℓ.

Since 8|(q−1),

    mn=(q²−1)/2^(v₂(q−1)+1) < q²/16.

Using gcd(m,n)=1, (5) bounds the error factor in (4) by W(mn)<13q^(1/3)/16^(1/6). Thus positivity follows whenever q>26^6/16=19,307,236. This covers e≥8 because 9^8=43,046,721.

For e=1,…,7 the exact arithmetic is:

| e | q | m | n | (W(m)−1)(W(n)−1) |
|---|---:|---|---|---:|
| 1 | 9 | 1 | 5 | 0 |
| 2 | 81 | 5 | 41 | 1 |
| 3 | 729 | 7·13 | 5·73 | 9 |
| 4 | 6561 | 5·41 | 17·193 | 9 |
| 5 | 59049 | 11²·61 | 5²·1181 | 9 |
| 6 | 531441 | 5·7·13·73 | 41·6481 | 45 |
| 7 | 4782969 | 547·1093 | 5·29·16493 | 21 |

Every listed factor is prime, and each row satisfies the exact integer inequality (q+1)²>4q((W(m)−1)(W(n)−1))². Consequently N(q)>0 for every e≥1.

## 4. From one counted pair to the middle rotation

Choose an x counted by N(q), and put

    λ=δx,          μ=(λ−1)/(λ+1),
    t=λ−λ⁻¹,      t′=μ−μ⁻¹.

Here λ^q=−λ, μ^q=μ⁻¹, λ² is primitive in F_q*, and μ² has order n=(q+1)/2. Direct calculation gives

    tt′=−4=2                    in characteristic three.

Both t,t′ are nonzero trace-zero elements, and t′=2/t. Put k=−t−t′. Then k^q=−k. It is nonzero: k=0 would give t²=−2=1, while the square of a nonzero trace-zero element is a nonsquare in F_q.

The polynomial identity

    (X²−tX−1)(X²−t′X−1) = X⁴+kX³−kX+1              (6)

now identifies the four eigenvalues of the template middle matrix as

    λ, −λ⁻¹, μ, −μ⁻¹.

They are distinct. The first pair could coincide only if λ²=−1, excluded because λ² is primitive and q−1≥8. The second pair could coincide only if μ²=−1, excluded because μ² has odd order n. The norms of the first two eigenvalues are −λ² and −λ⁻², neither equal to one; the other two have norm one. Hence there are no cross-pair coincidences. Thus T is semisimple.

The first pair has exponent 2(q−1): indeed λ² has order q−1, forcing |λ|=2(q−1). The second pair jointly has exponent q+1=2n: μ² has order n, so μ has order n or 2n, and in either case the pair μ,−μ⁻¹ has least common multiple 2n. Consequently

    |T|=lcm(2(q−1),q+1)=q²−1.

Put h=(q²−1)/2. Since n is odd, both first-pair eigenvalues have h-th power −1. Since q+1 divides h, both second-pair eigenvalues have h-th power +1. Thus T^h is not scalar. The scalar center of SU₄(q) has order gcd(4,q+1)=2, so its projective order is also q²−1.

## 5. Large rotation order forces the full square field

The following observation removes a separate subfield sieve. It applies to any odd q≡1 (mod 4) in the template, not only characteristic three.

**Lemma 2.** Suppose k≠0, k^q=−k, and the template middle matrix has projective order q²−1 or q²+1. Then F_p(k²)=F_q.

**Proof.** Write F_(q₀)=F_p(k²). The element k² is a nonsquare in F_q, hence also a nonsquare in F_(q₀), and the extension degree d=[F_q:F_(q₀)] is odd. If this field is proper, d≥3. Since q≡1 (mod 4), also q₀≡1 (mod 4), so the chosen i with i²=−1 belongs to F_(q₀). Moreover k∈F_(q₀²) and k^(q₀)=−k. The explicit matrix T therefore belongs to SU₄(q₀) with the same diagonal Hermitian form.

Its matrix order is prime to p, because its projective order is q²±1 and the scalar kernel in SU₄(q) has order two. Hence T is semisimple. For a semisimple unitary four-by-four matrix, its eigenvalue multiset is invariant under α↦α^(−q₀). Each distinct orbit of length a consists of eigenvalues whose orders divide q₀^a−(−1)^a. The sum of these orbit lengths is at most four. Therefore

    |T| ≤ ∏_orbits (q₀^a−(−1)^a) ≤ (q₀+1)^4.

The first inequality uses the elementary bound lcm≤product; the second follows from q₀^a−(−1)^a≤(q₀+1)^a. On the other hand |T| is at least its projective order, which is at least q²−1≥q₀^6−1>(q₀+1)^4 for q₀≥3. This is a contradiction. Thus d=1. ∎

Lemma 2 applies to the k constructed in §4. All hypotheses of the frozen generation and intersection theorems are now verified, proving the theorem.

## 6. Verification and retained scope

The companion [arithmetic/symbolic checker](phase12_unitary_parameters_check.py) verifies the seven exact factorization and positivity rows, the universal constant and threshold inequalities, the characteristic-three rational identity, and the coefficient identity (6). Run it with Python 3 and SymPy. The [finite-field checker](phase12_unitary_parameters_check.g), run with `gap -q -T phase12_unitary_parameters_check.g`, counts all eligible x and checks one resulting matrix directly for each q∈{9,81,729,6561}. The respective counts are 8,64,456,4800. It checks the four asserted eigenvalues, special unitarity, full square field, actual order and nonscalar half-power. These samples are diagnostics, not the proof of existence for every e.

The character-sum argument and its cohomological inputs remain a written proof. No complete Lean formalization of this family, the prior generation theorem, or the intersection theorem is claimed. The retained inputs are the specified Katz machinery, the phase-eleven group-theoretic inputs recorded in the two companion notes, and—only for the exact maximum-rank conclusion—the earlier rank obstruction. Internal mathematical review is distinct from external peer review. Current-literature priority has not been established.
