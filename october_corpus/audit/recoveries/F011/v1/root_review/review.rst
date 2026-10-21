Independent scientific review of F011
====================================

Decision: ACCEPTED_COMPLETE_CORRECTED_PRINCIPAL_RECOVERY.

Reviewer: root. Mathematical author: enumeration_volume. This is a distinct
reading of the frozen candidate, not a second author receipt. The author
manifest is 4e8f54e949cf0a389c3cf7a513ad100b395dd069db3969c94dc9f65692386092.
The source is Kim, Yip and Yoo, Explicit constructions of Diophantine tuples
over finite fields, Ramanujan Journal 65 (2024), 163–172, DOI
10.1007/s11139-024-00888-5. Its exact PDF has SHA256
9a864806aba2fab588a65ff20da6ba0ebdf8d68ebd9319695204dcecbac7b0bd.

I read the entire ten-page source text, both complete TeX manuscripts, the
22 source dispositions, proof map, program roles and operational checker.
I directly viewed source physical pages 3, 5, 7, 8 and 9 to verify the
literal claims and formulas involved in the corrections. I also viewed
every page of a fresh native rebuild of the four-page common theory and
four-page application. No requested mathematical correction remains.

Character and cyclotomic arguments
---------------------------------

The prescribed-character indicator is exact away from its distinct roots;
at the ith root its value is 1/d, while the other factors are zero or one.
Thus the total discrepancy is between zero and k/d. Each nonconstant
expanded polynomial has some exponent in 1,...,d-1 and cannot be a dth
power. Summing the Weil coefficients by support gives exactly
k-1-k/d+d^(-k). The external Weil theorem is explicitly retained; this
packet does not acquire a proof of it.

The square filter is a weight at roots, not a count. Coprimality and
squarefreeness ensure that every nonempty product satisfies the retained
Weil hypothesis. Every factor occurs in half the subsets, so the total
degree coefficient is D/2-1+2^(-T). Frobenius makes p-divisible cyclotomic
factors squares. The prime-to-p factors are coprime by separability of a
common multiple. These arguments recover source Lemmas 2.2 and 2.4.

The common degree estimate is proved independently of Cohen's cited
totient estimate. With m-1=pu+v and r=(p-1)u+v, the sum of the admissible
indices is p(p-1)u^2/2+puv+v(v+1)/2. Subtracting this from alpha*r(r+1)/2
gives pu/2+v(v+1)/(2(p-1)). Also phi(2i)<=i and phi(i)<=phi(2i).
This pays source Lemma 3.4 and yields the stronger bound K used below.

For either pattern, the degree-one factor X is included. At most K
nonzero points have forbidden low order. Zero costs weight 1/2, including
the minus pattern when -1 is square. From z>alpha*2^(T-2)*T^2 and
K+1<=alpha*T^2/2 one gets z>2^(T-1)(K+1). Substitution in the weighted
lower bound leaves a positive expression even at T=2. The polynomial
factorization of X^j+1 avoids dividing by a value that may vanish.

The first explicit parameter lemma uses T<=m/alpha+1<=B+2. Since
log(q)>2, it gives T<log(q)/(2 log(2)); alpha<=3/2<4(log(2))^2 then
proves the stated strict positivity threshold. The elementary lower
bound log(2)>2/3 is sufficient. These are uniform inequalities, not
inferences from the optional sampled parameters.

The stronger bound
------------------

This is the decisive new local construction in the current recovery.
For n entries, take z^(2i-(n-1)), 0<=i<n, with z^2=y. Ratios are
y^(i-j), so ord(y)>=n guarantees distinctness. Products are
y^(i+j-(n-1)); for distinct indices these exponents lie between
-(n-2) and n-2. The even case therefore needs only n-2 square conditions,
just as the odd case does. Negative exponents are harmless because y is
a nonzero square, and exponent zero uses the supplementary law for 2.

The shorter filter still excludes EVERY order below n. Relative to the
previous bound, at most phi(n-1) additional points are lost. The written
bound K+n-1<=K+alpha*T is valid since T>= (n-1)/alpha. For n>=4 and
odd p, T>=3 and K>=alpha*T. The resulting positive margin is
(2^(T-1)-5/2)*K+2^(T-1)-1. Thus the shorter filter has not silently
weakened the distinctness condition.

For q congruent to 7 modulo 8, p is congruent to 7 modulo 8 and the
extension degree is odd. Writing n=pu+v gives T=n/alpha for v=0,
T=n/alpha+1/p for v=1, and T=n/alpha+v/p-1 otherwise. Consequently
T<=B+2+1/p. Since q>7 implies q>=23 here, log(q)>3. The inequalities
alpha*2^(1/p)<= (7/6)*2^(1/7)<7/4<16/9<4(log(2))^2 pay the extra
rounding term. The exact source +2 bound is therefore recovered.

For n<=3, the elementary quadratic sum gives exactly (q-7)/4 choices
of y other than 0 and 1 with y and y+1 nonzero squares. The root weights
at 0,1,-1 are respectively 1/2,1,0. Such a y has odd order at least
three, giving the tuple {y^-1,1,y}. This completes every small parameter
case. Source Theorem 3.5 is interpreted with the explicit hypothesis
of its containing Section 3.2, q congruent to 7 modulo 8.

Other results and corrections
----------------------------

Consecutive integer powers prove Theorem 1.1 in the minus and plus
branches. The q=5 case completes Corollary 3.2. Nonnegative powers
avoid exponent zero in the residue-three branch and prove Remark 3.6
with its original asymptotic half factor. The square-subfield construction
is given with a full elementary proof.

For maximal tuples of size m>=3 the proof correctly removes 0 as well
as the m existing entries. At sqrt(q)>=2^(m-1)*m, its additional margin
is at least (2^(m-1)-2)*m-1>0. For m=2 the complete quadratic sum gives
weight at least four when q>=17, whereas removing the three forbidden
points costs at most three. Singletons cannot be maximal, including
q=3. This recovers the strict bound in source Proposition 2.3 without
its omitted-point error.

The F17 example genuinely contradicts the literal m+1 cardinality in
source Proposition 3.1: with y=-1, r=4, m=2 the list is (13,4,13),
and 15 and 0 are squares. Strict order repairs that intermediate claim.
Source Proposition 3.3 avoids the same issue because its y has odd order
and m is even. The least-nonresidue example in the introduction violates
the source's nonzero-element convention; the valid nonzero interval and
the p=3 counterexample to the literal bound are correctly identified.

The source's degree omission and rounding failure are also genuine.
For m=2 its alleged count lower bound exceeds the exact (q-7)/4 count.
The q=7^11 rounding example and q=7^5 small-parameter example lie in the
relevant residue class. These are defects in intermediate steps, not
counterexamples to the recovered existence theorems.

Admission and retained scope
----------------------------

All 22 source dispositions are accounted for. The principal existence
bounds and supporting results have complete written proofs, with the
literal false intermediate statements explicitly corrected. The source
square-field upper bound, historical integer-tuple results and GRH
background remain attributed external material. The source conjecture
M(q)>=(1-o(1))*log_2(q) is recorded without an answer or a claim about its
current literature status. The present proof does not solve it.

The fresh root replay checked 13 exports, 13 proof environments, source
and provenance bindings, 15 bounded metadata controls, and exact native
page texts after two-pass pdfLaTeX builds. Both logs were clean. The
optional diagnostics reran 196 degree cases, 32 prime-field filter cases,
586 centered constructions and 294 parameter cases. These checks support
inspection but are not premises of the uniform proofs or substitutes for
this mathematical review. There is no required mathematical program,
new Lean proof, numerical compression factor or claim of historical
priority. Source software costs remain unknown.

Root admits one further mathematical original, F011, as a complete
corrected principal recovery. The private reviewed count becomes 57 of
105, leaving 48. Public registration is a separate pending operation.
The latest instruction remains: finish reviewed recoveries for all 105,
then stop.
