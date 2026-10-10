# Independent audit of the primitive-square proof

Date: 11 October 2026. Reviewer: the independent enumeration-review agent.
Disposition: **accepted for the complete stated Conjecture 6.1**, with its stronger nonzero-square conclusion. No mathematical correction is requested. The six declarations in frozen phase266 are accepted within their stated algebraic scope. This is an additional review of an existing result, not a new question answer, a new principal-source recovery, or a claim of historical priority.

The reviewed proof is the unchanged `psl2_square_proof.md`, SHA256 `83a4739db035986a8149b7b813355657cc3a81ea2ad3c929f199c521ca86c249`. The formal author manifest is `phase266_manifest.json`, SHA256 `7c92dee573d004c7d91783fd135f94819eab66e49d8834987089acb06039bbb5`. Exact source and computational bindings appear in `phase267_inputs.json` and the review manifest.

## 1. Primary statement and retained theorem

The bound primary is Leemans–Moerenhout–O'Reilly-Regueiro, *Projective linear groups as automorphism groups of chiral polytopes*, arXiv:1606.08017v1, dated 26 June 2016. Although the local filename and bibliography use the 2017 journal publication, this audit does not claim a separate collation of that journal edition. Conjecture 6.1 is on physical and printed page 22 of the bound 25-page author edition. Its hypotheses are an odd prime $p$ and two odd integers $e_1,e_2>1$. There is no condition that the exponents be distinct or coprime. The target is the existence of primitive elements $j_i\in\mathbb F_{p^{e_i}}$ for which

\[
 \Omega=(j_1+j_1^{-1})^2(j_2+j_2^{-1})^2
       -4\bigl((j_1+j_1^{-1})^2+(j_2+j_2^{-1})^2\bigr)
\]

is a square in the compositum. The reviewed result requires it to be nonzero and therefore implies the source statement under either convention about zero being a square. The introduction and relevant Section 6 context, including the continuation on page 23, were read; the exact target page was visually checked. This audit does not claim a new complete reading or recovery of every result in that paper.

The character estimate is retained from Cohen–Kapetanakis–Reis, *The existence of Fq-primitive points on curves using freeness*, C. R. Math. 360 (2022), 641–652, DOI 10.5802/crmath.328. The exact primary PDF was obtained from [the publisher](https://comptes-rendus.academie-sciences.fr/mathematique/item/10.5802/crmath.328.pdf). Theorem 5 and formula (2) occur on physical page 4, printed page 643; the PDF has a cover before its numbered article pages. The definitions and these statements were read and visually checked. Definition 4 extends every multiplicative character by zero at zero, including the trivial character. Theorem 5 bounds a sum by $(z-1)\sqrt q$, where $z$ is the number of distinct roots, provided the polynomial is not a scalar times an $r$-th power and the character has order $r>1$. It cites the classical Lidl–Niederreiter theorem. This audit relies on the checked primary statement, not on an unclaimed reading of that book. The old proof's alternative Kim–Yip–Yoo citation is not needed and was not independently checked here.

The finite-field facts, primitive-character indicator and Weil estimate are retained mathematics. The old proof supplies the particular coefficient-norm construction, uniform estimates and complete finite reduction for this conjecture. Phase266 supplies six formal algebraic verifications. Phase267 supplies this independent audit and additional computation. These contributions should remain distinct in attribution.

## 2. Full degree and all field configurations

Reorder the degrees and put $g=\gcd(e_1,e_2)$, $q_0=p^g$, $a=e_1/g$, and $b=e_2/g$. Then $a\le b$ are coprime odd integers, $g$ is odd, and

\[
 E=\mathbb F_{q_0^a},\qquad K=\mathbb F_{q_0^b},\qquad
 L=\mathbb F_{q_0^{ab}},\qquad E\cap K=\mathbb F_{q_0}.
\]

Fix a primitive $j_1\in E$, and set $u=j_1+j_1^{-1}$, $s=u^2$. The exclusions $s\ne0,4$ are valid: the first would force $j_1^2=-1$, the second $j_1=\pm1$. Neither has the multiplicative order $p^{e_1}-1\ge26$.

The full-degree claim for $s$ needs the odd-degree hypothesis twice, and the proof correctly uses it twice. If $s\in E_0\subsetneq E$, the equation $u^2=s$ shows that $[E_0(u):E_0]\le2$. This degree divides the odd integer $[E:E_0]$, so $u\in E_0$. The equation $j_1^2-uj_1+1=0$ gives $j_1\in E_0$ for the same reason. A primitive element cannot lie in a proper subfield. Thus $s$ has degree $a$ over $\mathbb F_{q_0}$. The case $a=1$ is included. This argument neither assumes $g=1$ nor removes equal or properly nested fields.

## 3. Quartic, norm and squarefreeness

For $f_s(X)=(s-4)(X^2+1)^2-4sX^2$, the identity $\Omega=f_s(x)/x^2$ holds when $x\ne0$. As a quadratic in $Y=X^2$, the polynomial has nonzero leading and constant coefficients $s-4$ and discriminant $64s\ne0$. Its two distinct nonzero $Y$-roots each have two distinct square roots in an algebraic closure of odd characteristic. Thus $f_s$ has four simple, nonzero roots.

For distinct parameters $s,t$, subtraction gives

\[
 f_s(X)-f_t(X)=(s-t)(X^2-1)^2.
\]

A common root would satisfy $X^2=1$, but at such an element either quartic takes the nonzero value $-16$. Consequently the distinct Frobenius conjugates of $s$ give pairwise disjoint quartic root sets. Their product

\[
 P(X)=\prod_{i=0}^{a-1}f_{s^{q_0^i}}(X)
\]

belongs to $\mathbb F_{q_0}[X]$, has degree $D=4a$, has nonzero constant coefficient, and is squarefree. The leading coefficient is the nonzero norm of $s-4$; there is no leading-term cancellation or hidden drop in degree.

The Galois group of $L/K$ acts by $q_0^b$-Frobenius. Since $a,b$ are coprime, this action runs through precisely the same $a$ conjugates of $s$, while fixing $x\in K$. Hence $N_{L/K}(f_s(x))=P(x)$. The quadratic-character norm identity follows directly from Euler's formula:

\[
 \chi_K(N_{L/K}y)=y^{(|L|-1)/2}=\chi_L(y)
\]

for $y\ne0$, with both sides zero at zero. Dividing by $x^2$ changes the norm by the square $x^{2a}$. Thus the required character equality is valid in the actual compositum. This argument is a norm calculation, not an unsupported assertion that being a square always survives descent.

When $a>1$, a zero $x\in K$ of a quartic factor would satisfy $x^2\ne1$ and

\[
 s^{q_0^i}=\frac{4(x^2+1)^2}{(x^2-1)^2}\in E\cap K.
\]

That contradicts degree $a>1$. Therefore $P$ has no zeros in $K$. When $a=1$, the proof correctly retains the possible four zeros instead of using this argument.

## 4. Character estimate and strict positivity

Let $Q=|K|$, $n=Q-1$, $W(n)=2^{\omega(n)}$, and $\theta(n)=\varphi(n)/n$. If $\psi=\eta^k$ is a nontrivial character and $\eta$ has order $n$, take $1\le k<n$. Then

\[
 \psi(x)\chi_K(P(x))=\eta\bigl(x^kP(x)^{n/2}\bigr).
\]

The polynomial on the right has exactly $D+1$ distinct roots: the $D$ simple roots of $P$ and zero. At each root of $P$ its multiplicity is $n/2$, which is not divisible by $n$. It cannot be a scalar times an $n$-th power, even over an algebraic closure. These facts check both hypotheses of the retained Weil theorem. The large total degree is irrelevant to its distinct-root bound. Since its value at zero is zero, the estimate on all $K$ equals that on $K^*$, giving $D\sqrt Q$.

For the trivial $\psi$, the quadratic-character theorem applied to $P$ gives $(D-1)\sqrt Q$ on all $K$. Removing zero costs at most one, so again $D\sqrt Q$ is valid. This deals explicitly with the convention for the trivial character at zero.

The primitive indicator follows from cyclic-character orthogonality, or formula (2) of the retained primary with its primitive specialization. Each divisor $d$ contributes $\varphi(d)$ characters and has coefficient $\mu(d)/\varphi(d)$; the total absolute weight is $W(n)$. Thus

\[
 \left|\sum_{x\text{ primitive}}\chi_K(P(x))\right|
 \le\theta(n)DW(n)\sqrt Q.
\]

If $Z$ primitive elements are roots of $P$, the number of primitive arguments giving a nonzero square is exactly

\[
 \frac{\varphi(n)+\sum_{x\text{ primitive}}\chi_K(P(x))-Z}{2}.
\]

The subtraction of $Z$ is necessary and present. For $a>1$, $Z=0$, yielding $Q-1>4aW(Q-1)\sqrt Q$. For $a=1$, $Z\le4$ and $\theta(n)^{-1}\le W(n)$, yielding $Q-1>4W(Q-1)(\sqrt Q+1)$. Strict inequalities ensure positivity; no rounding assumption is used.

## 5. Exhaustiveness of the finite reduction

The elementary estimate

\[
 W(n)\le\frac{64}{30030^{1/4}}n^{1/4}<5n^{1/4}
\]

is valid for every positive integer: only the primes $2,3,5,7,11,13$ can increase $W(n)/n^{1/4}$, and repeated prime powers only decrease it. The final comparison is the exact integer inequality $64^4<5^4\cdot30030$.

For $a>1$, $Q>(21a)^4$ makes $4aW(Q-1)\sqrt Q<20Q/21<Q-1$; the last inequality requires $Q>21$, which is automatic here. Coprime odd $a,b>1$ satisfy $3\le a\le b-2$. The comparison $3^b>[21(b-2)]^4$ holds at $b=23$ and remains true on increasing odd $b$ by two, since the ratio grows by $9((b-2)/b)^4>1$. The remaining enumeration is therefore finite and exactly specified. Independent generation by prime bases and odd exponents, separate from the old consecutive-base test, confirms 66 possible triples and exactly these six failures of the sufficient bound:

\[
 (q_0,a,b)=(3,3,5),(5,3,5),(3,3,7),
 (3,5,7),(3,5,9),(3,7,9).
\]

The only composite admissible base in this small range is 27, and it passes the bound. Exact squaring of positive quantities, $(Q-1)^2>16a^2W(Q-1)^2Q$, introduces no false equivalence.

For $a=1$, put $t=Q^{1/4}>21$. The inequalities $Q/21>441t>20t+1$ and $t>21$ give $Q-1>20Q/21+20t>20t^3+20t$, which proves the sufficient bound for $Q>21^4$. The 23 fields $p^e\le21^4$ with $p$ odd prime and odd $e\ge3$ were independently enumerated, together with their allowed first degrees. Exactly $3^3,3^5,5^3,7^3,11^3$ fail. Their exponents are prime, so $e_1\mid e_2$, $e_1>1$ forces $e_1=e_2$. There is no omitted properly nested exception. The exact test retains the sign condition $Q-1-4W>0$ before squaring.

## 6. Eleven witnesses and their computational meaning

Both old GAP programs were rerun in an isolated directory, regenerating all six nonnested and five equal-field witnesses, their canonical exponents and polynomial values. The separate Python quotient-ring verifier was read in full and rerun with assertions enabled. It does not import GAP or a finite-field package.

Its field justification is sound even without a separately asserted irreducibility test. In a quotient of a degree-$d$ monic polynomial over $\mathbb F_p$, the exact order tests establish that the residue of $X$ has order $p^d-1$. Those powers are distinct nonzero elements and exhaust all nonzero elements of the $p^d$-element ring. Every nonzero element is therefore a unit, so the quotient is a field. The exact-order test precedes use of field inversion; there is no circular appeal to irreducibility.

For a nonnested exception the verifier constructs the coefficient norm in the first quotient field, verifies that its coefficients descend to the prime field, checks them against the certificate, and evaluates at the primitive element of the second quotient field. The degrees in these six cases are coprime. The written norm identity gives the square conclusion in their compositum. The verifier's primitive second element is the residue of $X$ for its listed polynomial, so the JSON canonical-exponent annotation is not a logical premise of this independent existence certificate. The fresh GAP reconstruction separately checks that canonical description. For equal fields the verifier computes the indicated power and $\Omega$ directly and checks primitiveness and nonzero squareness.

The finite certificate list is compared with the complete exception list. These are exact witnesses closing a finite reduction, not finite evidence extrapolated to all parameters. This review does not by itself audit Conjecture 6.2 or the separate chiral-classification corollary mentioned at the end of the old proof.

## 7. Additional independent tests and negative controls

`phase267_independent_arithmetic.py` independently enumerates the 66 and 23 cases, reconstructs exact factorizations and divisor weights, and checks the parameter exclusions. Its finite algebra diagnostics inspect 3,354 parameter/variable pairs over odd prime fields through 31. Explicit small counterexamples record failure after removing characteristic, parameter or degree hypotheses. These tests supplement the uniform argument; they do not replace it.

`phase267_field_checks.g` evaluates $\Omega$ directly for all primitive pairs in each exceptional equal field. The pair counts are respectively 144, 12,100, 3,600, 11,664 and 186,624, totalling 214,132. Every first primitive element has a nonzero-square partner in these five fields. This stronger finite observation is not claimed uniformly.

Four actual compositum tests use $(p,e_1,e_2,k)=(3,3,5,7),(3,3,9,1),(5,3,3,1),(3,9,15,1)$. They check the coefficient field, norm polynomial degree, norm identity and quadratic-character equality. The second is a properly nested configuration; the last has nonprime intersection field $\mathbb F_{27}$. The chosen argument in the properly nested test happens to give a nonsquare: that is consistent with the existential theorem, and the diagnostic correctly checks the identity rather than requiring every primitive pair to work.

Four corrupted variants were rejected: changing a norm coefficient, replacing an equal-field witness with a nonprimitive power, deleting an exceptional case, and underestimating $W$ in the old bound checker. The first three fail the old witness assertions; the fourth fails the old exact exception comparison. Separate phase266 controls exhibit concrete counterexamples to weakened algebraic hypotheses. No frozen mathematical input was modified.

## 8. Exact formal boundary and reproducibility

All six final declarations in `phase266_formal/PrimitiveSquarePolynomial.lean` were read, including their actual definitions and hypotheses, and freshly compiled under Lean 4.32.2 and the bound Mathlib revision. They establish evaluation of the actual polynomial, evaluation of its actual formal derivative, the trace identity, the Bezout identity, absence of a root shared by distinct parameters, and absence of a common polynomial/derivative root for $s\ne0,4$ in characteristic different from two. In particular, the derivative identification is formalized in this final six-declaration version.

The proofs use only the reported standard axioms `propext`, `Classical.choice` and `Quot.sound`; no proof hole, new axiom or `native_decide` is present. Cached dependency objects and the compiler remain trusted. The norm polynomial's `Polynomial.Squarefree` theorem is not a formal declaration here. Its degree, descent and norm identity, the full-degree finite-field argument, the character indicator and norm relation, the Weil estimate, the uniform finite reduction and all witness semantics remain written or computational. This is not a complete Lean verification of Conjecture 6.1.

The fresh aggregate replay passed in 6.082 seconds. Its report and all relevant output are archived in `phase267_replay/`. The runner checks the frozen phase266 manifest and mathematical inputs, creates isolated copies for the old programs, removes `PYTHONOPTIMIZE`, and confirms that the old Python child has optimization level zero. This is material: the old checker uses assertions, and running it under `-O` would remove proof checks. The new aggregate runner itself uses explicit rejection tests and may be run under `-O` safely. It also checks that the frozen old inputs retain their original hashes after replay.

**Final disposition.** Accept the complete arithmetic proof of the exact bound Conjecture 6.1, including equal and nested fields, conditional on its explicitly retained classical theorem and ordinary computational trust. Accept the six limited formal declarations. No mathematical amendment is required; no whole-paper, historical-priority, new-count or full-Lean claim follows from this review.
