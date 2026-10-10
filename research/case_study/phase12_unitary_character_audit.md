# Independent audit of the split/nonsplit character estimate

10 October 2026. Internal review by the survey-audit agent, separate from
the author and root reviews. **PASS: no mathematical gap found.** The main
target is Lemma 1 of [phase12_unitary_parameters.md](phase12_unitary_parameters.md),
with the complete written proof also read. This is not external peer review,
a novelty assessment, a Lean formalization, or an independent rerun of the
author's finite-field programs. The companion JSON binds the reviewed bytes.

## Primary input actually checked

I opened the complete author-hosted primary PDF of N. M. Katz,
[*Gauss Sums, Kloosterman Sums, and Monodromy Groups*](https://web.math.princeton.edu/~nmk/Katz-GKM.pdf),
and read §§2.3.1–2.3.3, the proof surrounding §3.6.1, and §4.3.
These support, respectively, the tame Euler-characteristic and trace
formulas; the weight-at-most-one bound on compactly supported degree-one
cohomology of a weight-zero sheaf; and the character-sheaf construction for
smooth geometrically connected commutative groups. The last explicitly uses
the Lang map 1−F and specifies the corresponding character value as its
rational-point trace. The source was read through its rendered primary PDF;
no fabricated local PDF hash or claim of reading the entire book is made.

## Exact geometric order and descent

Let q be odd, E=F_(q²), δ^q=−δ≠0, and U the norm-one torus. The domain
V=P¹\{0,∞,δ⁻¹,−δ⁻¹} is defined over F_q: its two nonrational punctures
are interchanged by Frobenius. The function g=δ²x² is F_q-valued, while
the coefficient conjugate of h=((δx−1)/(δx+1))² is h^−1. Thus the pair
really is an F_q-morphism V→G_m×U. It is not an illicit extension of a
character of U(F_q) to all E*.

There is a direct check of a subtle point in the proof. Over an algebraic
closure, identify U with G_m using its first split coordinate. Its F_q
Frobenius is t↦t^(−q), so the Lang map 1−F is t↦t^(q+1). This connected
Kummer cover has the full geometric deck group μ_(q+1). Consequently pushing
it out by a character ψ of U(F_q) gives geometric monodromy of *exactly*
ord(ψ), not a potentially smaller order. The split torus similarly has
the usual degree-(q−1) connected Kummer cover. The trace normalization is
the one stated in Katz §4.3; even reversing it would not change the bound,
but no reversal is needed here.

The zero and pole of g have multiplicity two at 0 and ∞. Those of h have
multiplicity two at δ⁻¹ and −δ⁻¹. These four points are distinct, and the
two supports are disjoint. Both input characters have nontrivial odd order;
squaring therefore preserves nontriviality of each local character. There
is no possible cancellation between the two tensor factors at a puncture.
All character orders are prime to the characteristic, so the ramification
is tame.

The resulting rank-one sheaf is geometrically nonconstant. H_c⁰ vanishes
on the affine connected curve; H_c² vanishes because the geometric
rank-one representation has no invariants or coinvariants. The tame
Euler characteristic is 2−4=−2, hence dim H_c¹=2. Finite arithmetic
monodromy gives weight zero. Applying the specified weight bound and trace
formula gives absolute value at most 2√q. Only this upper bound on weights
is required; no unnecessary assertion that all eigenvalues have exact
weight one enters the proof.

## Boundary terms and the subsequent application

The split-only term is zero, since χ² remains nontrivial. For the other
term, the Cayley map x↦(δx−1)/(δx+1) is an injective fractional-linear map
P¹(F_q)→U(F_q), hence a bijection by equal cardinalities. It sends 0 and
∞ to −1 and 1. Summing ψ² over U gives zero, and each of the two removed
points contributes one. The exact answer is therefore −2, including its
sign; it is not an error term bounded by two.

I also checked the rest of the written argument:

* The non-power character indicator is applied in the correct cyclic groups.
  A nonsquare has the full two-primary order in F_q*, and h lies in the
  subgroup U² of odd order (q+1)/2 when q=9^e. The ψ-only contribution is
  exactly +2 after the Möbius coefficients are summed, producing q+1.
* The supports of the odd prime factors of m and n are disjoint. This
  justifies W(m)W(n)=W(mn); the stated universal constant and seven-small-
  exponent strategy use no unproved factor-density assumption. Exact
  integer-table execution remains a separate certificate.
* In characteristic three, the Cayley relation gives tt′=−4=2. The two
  quadratic factors yield the four distinct middle eigenvalues as stated.
  Their combined order is q²−1. Its halfway power is −1 on the first pair
  and +1 on the second, so the scalar quotient does not halve that order.
* In the square-field lemma, a proper degree d is odd and at least three.
  All matrix entries then lie in the smaller quadratic field with the same
  unitary form. The semisimple eigenvalue-orbit bound is at most (q₀+1)^4,
  contradicting projective order at least q₀^6−1. This avoids silently
  assuming full trace field from one eigenvalue.

The resulting family remains conditional on the already recorded generation,
intersection and maximum-rank proofs. Those inputs are not re-proved by a
character estimate. The conclusion applies to q=9^e, e≥1; it does not give
every odd field or establish publication priority.
