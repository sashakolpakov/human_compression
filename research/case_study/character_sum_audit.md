# Independent audit of the primitive-square character-sum step

9 October2026. This note audits the argument supplied by the survey agent; it does not certify its finite exception enumeration or the separate polytope axioms.

Let p be odd, e1,e2>1 odd, g=gcd(e1,e2), Q0=p^g, a=e1/g and b=e2/g, with a<=b. Thus gcd(a,b)=1. Choose a multiplicatively primitive j1 in F_(Q0^a), and write u=j1+j1^(-1), s=u². Its degree over F_Q0 is a: if s lay in a proper subfield, odd extension degrees imply u lies there, and the quadratic equation for j1 then forces j1 there as well, contradicting its multiplicative order. Also s is neither0 nor4.

Set F_s(X)=(s−4)(X²+1)²−4sX² and P(X)=Norm_(F_(Q0^a)/F_Q0)(F_s(X)). Each quartic is squarefree in odd characteristic; distinct conjugate quartics are disjoint because their difference is (s−t)(X²−1)², while their values at ±1 are−16. Thus P is squarefree, degree D=4a, with P(0) nonzero.

Put Q=Q0^b. The a conjugates defining P are also exactly the conjugates for the norm from F_(Q0^(ab)) to F_Q, because multiplication by b permutes the residues modulo a. For j2 in F_Q*, v=j2+j2^(-1), the desired expression Omega satisfies

```
Omega = F_s(j2)/j2²,
quadratic_character_F_(Q0^(ab))(Omega)
  = quadratic_character_F_Q(P(j2)).
```

For a>1, P has no root in F_Q. A root would imply s=4v²/(v²−4) in F_Q, contradicting the intersection of the two coprime-degree subfields. The exceptional v²=4 gives F_s(j2) nonzero. This is useful because the construction needs a nonzero square.

The precise Weil bound needed is stated in Kim–Yip–Yoo, *Explicit constructions of Diophantine tuples over finite fields*, Ramanujan Journal65(2024), Lemma2.1, citing Lidl–Niederreiter Theorem5.41. For a multiplicative character of order m>1, a polynomial not a scalar multiple of an mth power, and N distinct roots over the splitting field, the complete sum has absolute value at most (N−1)sqrt(Q). [Primary publication](https://link.springer.com/article/10.1007/s11139-024-00888-5). A local PDF is archived as `sources/weil_bound_primary2024.pdf`.

Choose a generator eta of the character group of F_Q*, set n=Q−1, and write psi=eta^k. For k>0,

```
sum_(x in F_Q*) psi(x) chi(P(x))
  = sum_(x in F_Q) eta(x^k P(x)^(n/2)).
```

There are D+1 distinct roots; a root of P has multiplicity n/2, so the polynomial cannot be an nth power. Hence the absolute value is at most D sqrt(Q). For k=0, apply the bound directly to P and remove x=0: (D−1)sqrt(Q)+1<=D sqrt(Q). Nonmonic leading coefficients contribute a unit complex factor and do not affect the bound.

The usual primitive-element character indicator therefore bounds the sum of chi(P(x)) over primitive x by theta(n) W(n) D sqrt(Q), where theta(n)=phi(n)/n and W(n)=2^omega(n). If n>D W(n)sqrt(Q), the primitive values cannot all have character−1. For a>1 they are nonzero, hence at least one is a square. For a=1, zero itself is permitted in the literal square-existence conjecture, though not automatically in the polytope construction.

The elementary global estimate

```
W(n)/n^(1/4) <= product_(prime l<=13) 2/l^(1/4)
                  =64/30030^(1/4)<5
```

is valid because each prime factor at least17 contributes less than1 and higher valuations only decrease the ratio. The sufficient threshold Q^(1/4)>21a has slack for replacing n by Q−1. For coprime distinct odd a,b>1, a<=b−2. The inequality 3^(23/4)>21*21 and monotonicity of 3^(b/4)/(b−2) handle b>=23. The finitely many remaining bases/exponents and explicit primitive witnesses must be checked separately. The survey agent owns that exhaustive finite audit; this note makes no independent completeness claim about it.
