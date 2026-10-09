# Proposed proof of the primitive-square conjecture (Conjecture 6.1)

Status: proof derived in this session, with independently checked character-sum estimates, an exact finite integer reduction, and eleven exact finite-field witnesses. It has not been externally peer reviewed. Novelty must still be checked against the broader literature.

Source conjecture: D. Leemans, J. Moerenhout and E. O'Reilly-Regueiro, *Projective linear groups as automorphism groups of chiral polytopes*, J. Geom. 108 (2017), 675–702, [arXiv:1606.08017, Section 6](https://arxiv.org/html/1606.08017#S6).

## Theorem

Let p be an odd prime and let e_1,e_2>1 be odd integers. There exist primitive elements j_i in F_(p^e_i) such that, on putting u=j_1+j_1^(-1) and v=j_2+j_2^(-1),

    Ω = u²v² − 4(u²+v²)

is a **nonzero square** in F_(p^lcm(e_1,e_2)).

This proves the entire stated Conjecture 6.1, including equal or nested fields, provided the elementary finite witnesses below are accepted as part of the proof. The nonzero qualification is slightly stronger than the usual convention that zero counts as a square.

## 1. The polynomial and its norm

Reorder e_1,e_2 so e_1≤e_2, and put

    g=gcd(e_1,e_2),  q_0=p^g,  a=e_1/g,  b=e_2/g.

Thus a,b are coprime odd integers, a≤b, and g is odd. Write E=F_(q_0^a), K=F_(q_0^b), and L=F_(q_0^(ab)). Fix a primitive j_1∈E and put s=(j_1+j_1^(-1))².

We have s≠0,4. The first equality would give j_1 order 4, and the second would give j_1=±1; neither is possible in a field F_(p^e_1) with e_1≥3. Also s has degree a over F_(q_0): if s were in a proper intermediate field, the two quadratic equations for u=j_1+j_1^(-1) and for j_1 show that u and then j_1 would belong to that same field. Here the remaining extension degree is odd, so it has no quadratic subextension. This contradicts primitiveness.

Define the quartic

    f_s(X)=(s−4)(X²+1)²−4sX²
          =s(X²−1)²−4(X²+1)².

For nonzero x, with v=x+x^(-1), we have

    Ω = f_s(x)/x².

The polynomial f_s is squarefree. Indeed, it is quadratic in X² with nonzero constant and leading coefficients s−4; the discriminant of that quadratic is 64s≠0. Its roots are therefore four distinct nonzero elements in an algebraic closure.

Form the coefficient norm

    P(X)=∏_(i=0)^(a−1) f_(s^(q_0^i))(X) ∈ F_(q_0)[X].

Its degree is D=4a, and P(0)≠0. Its quartic factors have disjoint roots: subtracting f_s and f_t for s≠t gives (s−t)(X²−1)², whereas f_s(1)=f_s(−1)=−16≠0. Since the a conjugates of s are distinct, P is squarefree.

For x∈K, the norm from L to K permutes these same a conjugates, because gcd(a,b)=1. Consequently

    N_(L/K)(f_s(x))=P(x).

If χ_L and χ_K are quadratic characters, the standard norm identity gives

    χ_L(Ω)=χ_K(P(x))

whenever x≠0: the norm of x² is a square. Thus it suffices to find a primitive x∈K for which P(x) is a nonzero square.

If a>1, P has **no roots in K**. A root of one quartic would give

    s^(q_0^i)=4(x²+1)²/(x²−1)² ∈ K;

the denominator cannot vanish. This contradicts E∩K=F_(q_0) and the full degree a of the conjugate. When a=1, P is simply the quartic f_s over K, with at most four roots in K.

## 2. A uniform primitive-element character estimate

Let Q=|K|, n=Q−1, W(n)=2^ω(n), and θ(n)=φ(n)/n. Extend multiplicative characters to zero by assigning value zero, including the character trivial on K*.

For any multiplicative character ψ of K*,

    | Σ_(x∈K*) ψ(x)χ_K(P(x)) | ≤ D√Q.                    (1)

To see this when ψ is nontrivial, choose a generator η of the character group, of order n, and write ψ=η^k with 0<k<n. Then the summand equals

    η( x^k P(x)^(n/2) ).

The polynomial inside η has at most D+1 distinct roots, and is not an n-th power: at every root of P its multiplicity is exactly n/2. Weil's multiplicative-character bound therefore gives D√Q. A leading scalar in the polynomial has no effect on the estimate. When ψ is trivial, apply the quadratic-character version to P on all of K, then remove x=0. This gives (D−1)√Q+1≤D√Q.

The exact root-count form of Weil's bound used here is stated, for example, as Theorem 5 of Cohen–Kapetanakis–Reis, [*The existence of F_q-primitive points on curves using freeness*](https://comptes-rendus.academie-sciences.fr/mathematique/item/10.5802/crmath.328.pdf), and as Lemma 2.1 of Kim–Yip–Yoo, [*Explicit constructions of Diophantine tuples over finite fields*](https://link.springer.com/article/10.1007/s11139-024-00888-5), citing Lidl–Niederreiter, Theorem 5.41. The estimate counts **distinct roots**, not the potentially large total degree of x^kP^(n/2).

The standard character indicator for primitive elements is

    1_primitive(x)=θ(n) Σ_(d|n) μ(d)/φ(d) Σ_(ord ψ=d) ψ(x).

For a derivation one can apply character orthogonality to the cyclic group K*. Formula (2) of the Cohen–Kapetanakis–Reis source specializes to this formula. There are φ(d) characters of order d, and exactly W(n) squarefree divisors. Applying (1) yields

    | Σ_(x primitive) χ_K(P(x)) | ≤ θ(n) D W(n) √Q.       (2)

Let Z count primitive roots of P. The number N of primitive x for which P(x) is a nonzero square is

    N = [φ(n) + Σ_(x primitive) χ_K(P(x)) − Z]/2.

It follows that N>0 whenever

    n > D W(n)√Q + Z/θ(n).                               (3)

For the non-nested case a>1, Z=0, so the sufficient condition is

    Q−1 > 4a W(Q−1)√Q.                                  (4)

For the nested case a=1, Z≤4. Since 1/θ(n)=∏_(ℓ|n) ℓ/(ℓ−1)≤W(n), it is enough that

    Q−1 > 4W(Q−1)(√Q+1).                                (5)

## 3. Reduction of (4) to six cases

For every positive integer n,

    W(n) ≤ [64/30030^(1/4)] n^(1/4) < 5n^(1/4).           (6)

Indeed, for each prime ℓ≥17, 2≤ℓ^(1/4). The only factors that enlarge W(n)/n^(1/4) are among 2,3,5,7,11,13, whose product is 30030. Repeated prime powers only decrease this ratio. The final strict inequality follows from 64^4<5^4·30030.

A sufficient condition for (4) is

    Q > (21a)^4.                                        (7)

In fact, (6) bounds its right side by 20a Q^(3/4), which (7) makes less than (20/21)Q<Q−1.

In the non-nested case, a,b>1 are coprime odd integers, so 3≤a≤b−2 and b≥5. If b≥23 then

    Q ≥ 3^b > [21(b−2)]^4 ≥ (21a)^4.

For rigor, the middle inequality holds at b=23 by direct integer comparison. On increasing an odd b≥23 by two, its left-to-right ratio is multiplied by

    9[(b−2)/b]^4 ≥ 9(21/23)^4 > 1.

It remains to inspect odd b from 5 through 21 and odd prime-power bases q_0 satisfying

    q_0^b ≤ [21(b−2)]^4,

where q_0=p^g with g odd. These upper bounds are tiny: the possible bases are at most 27 for b=5, at most 13 for b=7, at most 9 for b=9, at most 5 for b=11,13, and at most 3 for b=15,17,19,21. Restricting to odd exponent g leaves 27 as the only composite base needing inspection; it passes (4).

The exact integer check of (4) is

    (Q−1)² > 16a² W(Q−1)² Q.

Trial division and this comparison for all 66 remaining parameter triples leave exactly

    (q_0,a,b)=(3,3,5), (5,3,5), (3,3,7),
               (3,5,7), (3,5,9), (3,7,9).                (8)

No floating-point estimates or probabilistic factorizations are involved. The entire reduction is executable in [psl2_square_bound_check.py](psl2_square_bound_check.py).

## 4. Reduction of (5) to five cases

If a=1 then e_1 divides e_2, and Q=p^e_2 with odd e_2≥3. Condition (5) follows whenever Q>21^4: with t=Q^(1/4)>21, (6) gives a right side smaller than 20t³+20t, and

    Q−1 > 20Q/21+20t > 20t³+20t.

For the first inequality use Q/21=t·t³/21>441t>20t+1; for the second use t>21.

There are exactly 23 odd prime-power fields p^e with e≥3 odd and p^e≤21^4. For each, the integer form of (5) is

    Q−1−4W > 0,
    (Q−1−4W)² > 16W²Q.

Only Q=3³,3⁵,5³,7³,11³ fail this sufficient condition. Each exponent is prime, so the required divisor e_1>1 of e_2 forces e_1=e_2. Thus the remaining nested triples are

    (p,e_1,e_2)=(3,3,3), (3,5,5), (5,3,3),
                 (7,3,3), (11,3,3).                     (9)

The same exact-integer script checks these 23 fields, their allowed divisors, and precisely this exception list.

## 5. Exact witnesses for all eleven exceptions

Write z_d=Z(p^d), GAP's canonical primitive element defined by its Conway field representation. In every row choose j_1=z_(e_1) and j_2=z_(e_2)^k. Each k below is coprime to p^e_2−1, so both elements are primitive. The norm-polynomial or quartic value has the indicated even exponent in z_(e_2), proving it is nonzero and a square.

| p | e_1 | e_2 | k | Polynomial value |
|---|---|---|---|---|
| 3 | 3 | 5 | 7 | P(j_2)=z_5^228 |
| 5 | 3 | 5 | 1 | P(j_2)=z_5^2802 |
| 3 | 3 | 7 | 1 | P(j_2)=z_7^1336 |
| 3 | 5 | 7 | 1 | P(j_2)=z_7^406 |
| 3 | 5 | 9 | 5 | P(j_2)=z_9^18778 |
| 3 | 7 | 9 | 1 | P(j_2)=z_9^17426 |
| 3 | 3 | 3 | 1 | f_s(j_2)=z_3^6 |
| 3 | 5 | 5 | 3 | f_s(j_2)=z_5^200 |
| 5 | 3 | 3 | 1 | f_s(j_2)=z_3^84 |
| 7 | 3 | 3 | 1 | f_s(j_2)=z_3^6 |
| 11 | 3 | 3 | 3 | f_s(j_2)=z_3^906 |

The exact computations, defining polynomials, and coefficients of the norm polynomials are recorded in:

- [psl2_square_witnesses.g](psl2_square_witnesses.g) and [its log](psl2_square_witnesses.log), for the six non-nested cases;
- [psl2_nested_witnesses.g](psl2_nested_witnesses.g) and [its log](psl2_nested_witnesses.log), for the five nested cases;
- [psl2_square_witnesses.json](psl2_square_witnesses.json), the finite polynomial certificates.

A separate implementation of polynomial quotient fields using only Python's standard library independently verified all eleven certificates: [verify_square_witnesses.py](verify_square_witnesses.py), with the complete PASS record in [psl2_square_witnesses_independent.json](psl2_square_witnesses_independent.json). This implementation does not import GAP or a finite-field package.

These are eleven explicit witnesses after a uniform theorem, not an extrapolation from a finite sample. Their sizes never exceed F_(3^9) or F_(5^5); no computation in the large compositum is needed. The norm identity in Section 1 proves that the witnesses have the required meaning in that compositum.

Sections 1–4 cover every parameter triple except these eleven, and Section 5 covers all eleven. This proves the theorem. QED.

## Relation to the chiral-polytope problem

For the outstanding odd exponents d with at least two distinct prime divisors, choose d=e_1e_2 with e_1,e_2>1 coprime and odd. The theorem now supplies the primitive parameters assumed by the source's Section 6 construction. The separate [intersection proof](psl2_intersection_proof.md) establishes its Conjecture 6.2. The [classification corollary](psl2_chiral_corollary.md) gives complete generation and chirality arguments and states the resulting classification with the source's hypotheses and exceptional small cases preserved.
