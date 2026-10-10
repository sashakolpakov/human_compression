# Completing the second unitary congruence class

10 October 2026. Original phase-fifteen proposed proof, supported by exact finite-field certificates and separate internal reviews. External peer review and publication priority are not established. The frozen earlier phases are unchanged.

**Theorem.** For every prime power $q\equiv3\pmod4$ with $q\ge7$, the group $\operatorname{PSU}_4(q)$ has a rank-four string C-group representation.

Together with the frozen [first congruence-class theorem](phase13_unitary_sieve.md), this gives rank-four existence for every odd $q\ge5$. Together with our separately reviewed [unitary upper bound](phase9_linear_unitary.md) and published rank-three existence, its rank set is exactly $\{3,4\}$ for odd $q\ge5$. The excluded group $\operatorname{PSU}_4(3)$ has no string C-group representation, by the retained Leemans–Vandenschrick Theorem 1.1; it must not be silently included in an “all odd fields” statement. These consequences retain the earlier theorems and their dependencies rather than reprove them here.

## 1. The uniform mathematical reduction

The [generation theorem](phase15_unitary_generation.md) and [intersection theorem](phase15_unitary_intersection.md) use the four explicit matrices of the sphere template

$$a=it,\quad b=x+iy,\quad i^2=-1,\quad t^2+x^2+y^2=1.$$

The [parameter reduction](phase15_unitary_parameter_reduction.md) shows that for $q\ge27$ it is enough to find one primitive $\lambda\in\mathbb F_{q^2}^*$ satisfying

$$\operatorname{Norm}_{q^2/q}(\lambda-\lambda^{-1})=-2.$$

Its four eigenvalues give the exact projective middle order $(q^2-1)/2$. That large order forces the full square field, and the $q+1$ possible norm-compatible choices of $b$ outnumber every excluded choice. Thus parameter existence is converted into both full generation and every subgroup intersection, without enumerating a large unitary group.

The [twisted-curve proof](phase15_unitary_curve.md) supplies a genus-one curve with eight simple ramification points when the characteristic is not three, and a rational component with four when it is three. There are no rational boundary points. For $N=q^2-1$, a nontrivial multiplicative character has sum at most $8\sqrt q$ in the first case and $2\sqrt q$ in the second. These are written applications of the retained tame character-sheaf/Weil machinery, independently reviewed separately from the finite computations.

For a squarefree core $a$ containing some of the prime divisors of $N$, let $p_1,\ldots,p_s$ be the omitted primes and set $\delta=1-\sum1/p_j>0$. A sufficient condition outside characteristic three is

$$q+1>A\sqrt q,\qquad
A=8\,2^{\omega(a)}\left(2+\frac{s-1}{\delta}\right)-6.$$

When $s=0$, use $A=8\,2^{\omega(N)}-6$. In characteristic three replace eight by two and the final minus six by minus two. The prime two is included among the divisors of $N$.

## 2. An explicit cutoff with no field-distribution assumptions

Define the positive rational number

$$C^6=\prod_{p<64,\ p\text{ prime}}\frac{64}{p}
=\frac{162259276829213363391578010288128}{58644190679703485491635}.$$

For every positive integer $n$,

$$W(n)^6=64^{\omega(n)}\le C^6\operatorname{rad}(n)\le C^6n.$$

Since $N<q^2$, we get $W(N)<Cq^{1/3}$. The basic character bound is positive whenever $q\ge\lceil8^6C^6\rceil=725311328745792$.

For the remaining range $q<Q$, let $P_j$ be the product of the first $j$ primes, including two. If $P_{w+1}\ge Q^2$, then $\omega(N)\le w$. Choose the core to consist of the smallest $c$ prime divisors of $N$. Replacing the sorted divisors by the first $w$ primes decreases $\delta$ and increases the coefficient, so gives a valid uniform upper bound on $A$. Cases with at most $c$ divisors use the smaller direct bound. The following exact rational computations repeatedly reduce the cutoff:

| Previous cutoff $Q$ | Maximum $\omega(N)$ | Core size $c$ | New cutoff $\lceil A^2\rceil$ |
|---:|---:|---:|---:|
|725311328745792|21|3|16427566|
|16427566|12|2|1574926|
|1574926|11|2|1029254|

Every displayed coefficient is positive. For $q\ge\lceil A^2\rceil$, one has $q+1>A\sqrt q$, including the endpoint. Therefore all eligible fields at least 1029254 are covered. The same constants apply in characteristic three because its stronger bound implies this one.

## 3. Exact finite-field coverage

The [arithmetic checker](phase15_unitary_sieve_check.py) uses an Eratosthenes prime sieve and exact integer powers to enumerate every $q<1029254$ with $q\equiv3\pmod4$ and $q\ge7$. Equivalently $q=p^e$ with $p\equiv3\pmod4$ and $e$ odd. There are 40389 such fields. Factoring $q-1$ and $q+1$ gives the full prime support of $N$. Every possible core consisting of the smallest $c$ factors is tested by exact rational arithmetic and by squaring positive sides of the sufficient inequality.

Exactly 1699 field sizes remain; the largest is 245519. This is a finite list requiring witnesses, not a list of counterexamples. The six composite cases are 27,343,1331,6859,12167,29791. The characteristic-three estimate is used in its own range, so its only finite witness case is 27.

A fast deterministic coordinate construction supplies 1697 primitive norm witnesses. In the tower $\mathbb F_q[i]$, write $\lambda=A+iB$ and $s=\operatorname{Norm}(\lambda)$. The required norm equation is equivalent to

$$A^2=(s^2+4s+1)/4,\qquad B^2=-(s^2+1)/4.$$

Iterate primitive $s\in\mathbb F_q^*$. Since $q\equiv3\pmod4$, square roots are obtained by exponentiation to $(q+1)/4$, with each result checked by squaring. The candidate $\lambda$ is then checked to have exact order $N$: its $N$th power is one and its $N/r$th power is not one for every prime $r\mid N$. Finally the norm equation and the derived parameter $t$ are checked directly.

The prime-field implementation supplies 1691 witnesses; the GAP tower implementation supplies all six composite witnesses. The [portable coordinate file](phase15_unitary_witnesses.json) gives the defining polynomial of each base field and low-to-high coefficients for both parts of $\lambda$, its norm and $t$. The quadratic extension is always $i^2=-1$, irreducible because $q\equiv3\pmod4$. The JSON compiler proves that its field list is exactly the arithmetic exception list; it is not itself an independent field-arithmetic verifier.

Two fields use explicit direct parameters instead of a primitive norm-curve point. A third small field uses the same direct check because the uniform $b$-count begins at 27:

|$q$|$t$|$x$|$y$|Middle order|Orders of $ZS,RS,(ZR)S$|
|---:|---:|---:|---:|---:|---:|
|19|8|15|4|181|9,10,10|
|23|5|6|3|265|11,11,11|
|43|27|22|11|924|21,11,3|

The [special-parameter checker](phase15_unitary_special_parameters.g) checks the sphere, nonzero $txyh$, exact projective middle order, and the rank-one order criterion. The written generation and intersection theorems therefore apply. No large group enumeration is involved in these three checks.

## 4. The remaining small groups

For $q=7$, retain the frozen [phase-fourteen matrix certificate](phase14_unitary_q7.md), of type $\{4,24,4\}$. Its parameter has $y=0$, so it lies outside the sufficient generation/intersection criteria above; its complete finite certificate is essential.

For $q=11$, use $t=2,x=9,y=2$ in the present sphere template. Its type is $\{4,60,10\}$. The [complete finite certificate](phase15_unitary_q11.md) constructs the natural four-by-four matrices, checks special unitarity, obtains the full projective group by an order sandwich on all 15984 totally isotropic planes, and checks every one of the 16 marked subgroup closures and 256 intersections. The three auxiliary rank-one products have order at most five, so the sufficient generation clause is not invoked for this example.

This treats every field below 27. All other exceptional fields either have a primitive norm witness and $q\ge27$, or are the explicit q=43 direct parameter. Combined with the uniform sieve, this proves the stated existence theorem.

## 5. Scope and retained inputs

The mathematical dependencies are the Dickson rank-one maximal-subgroup list, perfection/simplicity of the standard rank-one groups, coordinate-SU2 generation by the previously proved elimination argument, finite-field descent of the exact alternating-form stabilizer, the elementary rank-two symplectic torus list, the recursive string C-group intersection criterion, and the standard tame character-sum/Weil results. The concrete q7/q11 cases retain exact finite computation. Full source and priority audits remain separate; no new named-conjecture or first-priority claim is inferred from this construction.

The symbolic companion checks 37 exact identities. The arithmetic sieve checks the cutoff and complete finite field-size coverage. The coordinate searches check existence in each remaining field. Independent written audits and independent executable checks are separate layers and must be described by their actual recorded scopes. None of this theorem is claimed to be fully formalized in Lean.
