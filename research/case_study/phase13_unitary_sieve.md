# A prime sieve for the unitary elliptic parameter curve

Original phase-thirteen proof, 10 October 2026. This note sharpens the [elliptic curve estimate](phase13_unitary_elliptic.md). Its finite certificate supplies an explicit parameter for every field left by the exhaustive arithmetic sieve. Separate records describe the internal mathematical reviews and independent execution; no external peer review or publication-priority determination is claimed.

**Theorem.** For every odd prime power q≡1 (mod 4), q≥5, the phase-eleven template gives a rank-four string C-group for PSU₄(q). For q>5 the construction below has type {4,q²−1,2p}; q=5 uses type {4,26,10}. Here p is the characteristic. In combination with the retained unitary upper bound, the maximum rank is four for every group in this congruence class.

The new argument consists of a uniform sieve and a finite list of field-element witnesses. It does not enumerate any finite groups or assume that a collection of random successful searches exhausts the fields.

## 1. A general primitive-character sieve

Retain the nonsingular elliptic curve, open domain V and functions g,h from the companion note, so p≠2,3. Set

    m=oddpart(q−1),   n=(q+1)/2,   D=rad(mn),
    M=|V(F_q)|=|C(F_q)|−4 ≥ q−3−2√q.

The product of the odd-order quotients of F_q* and U² is cyclic. Thus each prime ℓ|D belongs unambiguously to one of the two primitive conditions. For a squarefree divisor a|D, let N(a) count points satisfying the non-ℓth-power condition for all ℓ|a, on the applicable coordinate. Write θ(a)=φ(a)/a and W(a)=2^ω(a).

Every nontrivial character occurring in these indicators has a sum over V(F_q) of absolute value at most 8√q. This follows directly from the companion bounds: mixed characters give 8√q, split-only characters give 4√q, and nonsplit-only characters give at most 4√q+4≤8√q. Therefore character orthogonality gives

    N(a) ≥ θ(a)[M−8(W(a)−1)√q].                         (1)

Let ℓ₁,…,ℓ_s be the primes dividing D/a. Suppose s≥1 and

    δ=1−Σ_i 1/ℓ_i >0.

The pointwise sieve inequality is

    N(D) ≥ Σ_i N(aℓ_i)−(s−1)N(a).                       (2)

To see this, consider a point already counted by N(a). If it satisfies all s extra conditions, it contributes one to both sides; if it fails at least one, its contribution on the right is at most zero. Points outside N(a) contribute zero throughout.

For each ℓ_i, separate the characters whose order is divisible by ℓ_i in the indicator. Their absolute coefficient sum before the θ-factors is W(a). Consequently

    |N(aℓ_i)−θ(ℓ_i)N(a)|
        ≤8θ(a)θ(ℓ_i)W(a)√q.                            (3)

Use Σ_iθ(ℓ_i)=s−1+δ and (1)–(3) to obtain

    N(D) ≥ θ(a)δ {q−3
       −[8W(a)(2+(s−1)/δ)−6]√q}.                      (4)

Every character in the difference (3) is nontrivial because its order includes ℓ_i. Thus no trivial-character main term has been put into an error estimate. The larger constant 8 deliberately absorbs the nonsplit boundary terms; this version does not rely on canceling them exactly.

If s=0, use (1) directly. The analogous sufficient inequality is

    q−3 > [8W(D)−6]√q.                                  (5)

All quantities in (4) and (5), apart from √q, are rational. Positivity is checked exactly by squaring positive sides.

## 2. A uniform cutoff by primorial bootstrapping

Let P_j be the product of the first j odd primes. Since D is odd and squarefree,

    P_(ω(D)) ≤ D ≤ mn < q²/8.                            (6)

The companion note has already proved existence for every q>Q₀, where

    Q₀=3,715,232,694,272.

For fields at most Q₀, (6) implies ω(D)≤17. If h=ω(D)≤w, choose a to contain the c smallest prime factors of D (or all of D if h≤c). When h>c, replacing its sorted prime factors by the first h odd primes can only decrease δ. Replacing h by w can only decrease δ and increase s−1. Therefore the following rational constants give valid uniform bounds for all h≤w:

    δ_(w,c)=1−Σ_(j=c+1)^w 1/p_j,
    A_(w,c)=8·2^c[2+(w−c−1)/δ_(w,c)]−6.

In these rows δ_(w,c)>0. For h≤c, the simpler coefficient 8·2^h−6 is smaller than the displayed A_(w,c). The sufficient cutoff is

    B_(w,c)=ceil((A_(w,c)+1)²).

Indeed q≥B implies √q≥A+1 and q−3−A√q≥√q−3>0, since all the displayed A exceed two. Every line of the following table uses exact rational and integer arithmetic:

| Previously unexamined q≤Q | Maximum ω(D) | c | New sufficient cutoff B |
|---:|---:|---:|---:|
| 3,715,232,694,272 | 17 | 2 | 2,135,383 |
| 2,135,383 | 10 | 1 | 255,289 |
| 255,289 | 9 | 1 | 160,372 |
| 160,372 | 8 | 1 | 98,660 |

For each row the maximum is certified by 8P_(w+1)≥Q². The logical use is iterative: values above the previous cutoff were already covered, and the sieve now covers every value between the new and old cutoffs. It follows that every eligible field with q≥98,660 has a suitable parameter. No distributional assumption on prime factors is used.

## 3. Exact exhaustion below the cutoff

The arithmetic checker enumerates every prime power q<98,660 with q≡1 (mod 4) and characteristic p≥5 by a complete Eratosthenes prime sieve and integer powering. There are 4,795 such values. Characteristic-three fields are all powers of nine and are already covered by the frozen phase-twelve theorem.

For each of these fields the checker factors q−1 and q+1 exactly, removes their two-parts, and tests (4) for every core a consisting of its c smallest odd prime factors, including c=0 and c=h. The exact arithmetic covers all but 406 values. The largest exception is q=43,889. This list is a list of fields requiring witnesses, not a list of counterexamples.

For q>5 in this finite list, a witness consists of field elements x,y on the companion elliptic curve such that dx² is primitive and ((δy−1)/(δy+1))² has order (q+1)/2. These are checked by exact finite-field arithmetic. The resulting k is then checked independently for trace zero, nonzero value, full square field and exact projective middle-matrix order q²−1.

The witness search is elementary. Given x, put g=dx². The quadratic equation for y has discriminant 4(g²−g+1), and when it has a square root z in F_q one may take

    y=(1−g±z)/(dx).

The checker tries deterministic powers of a canonical field generator until a pair passes. Completeness is certified by one successful pair for every field on the exhaustive 405-value list, not by interpreting a failed search as a nonexistence proof.

For q=5 the elliptic curve has just its four boundary rational points, so that particular split-torus construction cannot work. The already certified plus-branch parameter is k=Z(25)^3 in GAP's canonical field notation. The finite checker separately verifies its projective middle order 26 and the full square field, applying the same frozen generation and intersection theorems. Its matrix order is 52 and T²⁶=−I; the check correctly permits this central scalar. For the other 405 witnesses the matrix and projective orders are both q²−1.

## 4. Scope and dependencies

The geometric and character bounds remain written proofs. Run the [arithmetic checker](phase13_unitary_sieve_check.py) with Python 3; it writes the complete 4,795-field record and the exact 406-field exception list. Run the [finite-field checker](phase13_unitary_witnesses.g) with `gap -q -T phase13_unitary_witnesses.g`. All 406 cases pass. The [coordinate data](phase13_unitary_witnesses.json) record each field as F_p[z]/f(z) with its monic defining polynomial and low-to-high power-basis coordinates for δ,x,y,k,i, allowing a separate implementation to verify the certificates without GAP or its canonical-element conventions.

The finite certificate checks field arithmetic and four-by-four matrix powers, not a large permutation representation of PSU₄(q). The two phase-eleven theorems convert these parameter conditions into full generation and all intersection properties. Their retained Dickson classification, recursive string-intersection criterion and finite-field facts remain explicit dependencies. The phase-nine theorem supplies only the final maximum-rank upper bound.

The conclusion concerns q≡1 (mod 4). No assertion is made here about rank-four existence for q≡3 (mod 4). Internal review and exact computation are not external peer review, and the publication priority of the resulting family has not been determined.
