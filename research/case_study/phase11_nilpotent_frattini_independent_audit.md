# Independent audit: nilpotent groups with abelian Frattini subgroup

10 October 2026. Private internal review by the survey-audit agent.
**PASS: no mathematical gap found** in
[phase11_nilpotent_frattini.md](phase11_nilpotent_frattini.md).
The accompanying JSON binds the reviewed proof. This is not external
peer review, a priority determination, or a complete formal verification.

## Minimum-counterexample reductions

The subgroup and quotient closure arguments apply for every prime p:
Φ(H)=H^p[H,H]≤Φ(P), and the Frattini subgroup of P/N is Φ(P)N/N.
The central quotient preserves TPP and the violation ratio by absorbing
the quotient relation into the cyclic factor containing the central kernel.
The proper pair-generated reduction uses an injection of cosets; it does
not assume the pair-generated subgroup is normal. These are the same
valid reductions independently checked in the binary companion audit.

Pair generation forces rank-two Frattini quotient and three different
projective directions. Thus the maximal subgroup containing A meets the
other cyclic factors in B^p and C^p. Restriction to that subgroup divides
the violation ratio by p; minimum order makes the original ratio exactly p.

The bound on cyclic factors also holds for odd p. A normal subgroup of
order p in a p-group is central, because its automorphism group has order
p−1. The order-p subgroup of a center-free cyclic factor is consequently
not normal. A different conjugate has trivial intersection with the
original cyclic subgroup. Their product lies in a maximal subgroup,
giving α²≤|P|/p. Together with ratio p this proves γ≥p², so all three
p-th-power factors used subsequently are nontrivial.

Inside the abelian Frattini subgroup their multiplication map is an
injective homomorphism by TPP, and its order is exactly |Φ(P)|. Hence
the direct product and the three-dimensional basis modulo pΦ(P) are
justified. No generic three-factor injectivity is inferred from a numerical
equality.

## Conjugation norms and characteristic three

I checked the right-conjugation convention with d=[b,a]. It gives
aᵇ=ad⁻¹ and bᵃ=bd. Raising to p-th powers in the abelian kernel gives
the two norm identities with the stated opposite signs. The norm
polynomial becomes (X−1)^(p−1) in characteristic p.

The operators S−I and T−I are nilpotent: their p-th powers vanish,
and their nilpotency indices in dimension three are at most three.
For p≥5 the two norm operators therefore vanish immediately.

For p=3 the exceptional length-three Jordan possibility is correctly
excluded without importing a classification theorem. If N²≠0, a cyclic
vector gives the basis v,Nv,N²v. Any commuting operator is a quadratic
polynomial in N. The constant coefficient of T is one because T is
unipotent. If its linear coefficient is nonzero, its fixed line equals
ker N, which already contains x and cannot also contain the independent y.
If that coefficient is zero, (T−I)²=0, and the second norm identity then
puts y in ker N anyway. Both cases contradict independence. Exchanging
the roles of the two operators excludes the other length-three block;
the minus sign in the exchanged identity does not affect vanishing.

Thus both conjugation maps fix x and y modulo pΦ(P). They induce the
identity on the one-dimensional quotient by their span, because an
operator of p-power order on a one-dimensional F_p-space is trivial.
Their correction to z lies in that span, as stated.

## Actual central element and nilpotent products

The maximal-exponent lift is valid with unequal factor orders. Multiplying
by p^(r−1) erases every shorter-factor term and every coefficient divisible
by p in the largest factors. If x or y is largest, its fixed coordinate
supplies a fixed element of order p. Otherwise z is strictly larger than
both, so its allowed corrections disappear. In each case an actual
nonidentity element of one cyclic factor centralizes both generators of
P. This contradicts the center-free reduction; a fixed quotient vector
alone would not have sufficed.

A finite nilpotent group is the direct product of its Sylow subgroups,
and its Frattini subgroup is the product of theirs. Each cyclic factor
splits into its prime-primary factors. Restricting TPP to a Sylow subgroup
preserves it, and multiplying the resulting prime-power inequalities gives
the claimed finite nilpotent theorem. No interaction between primes is
left unaccounted for.

## Independent exact diagnostic and scope

The standalone [F₃ checker](phase11_odd_norm_independent_check.py) uses
only the standard library and imports no author code. Its
[report](phase11_odd_norm_independent_check.json) enumerates all 729
matrices annihilating each named coordinate, leaving 81 nilpotent matrices
per coordinate. There are 333 commuting pairs, including 144 pairs with
a length-three Jordan block. All 27 possible d vectors are tested for
each pair. Exactly 2,187 solutions, in 81 action pairs, satisfy the norm
identities; every one has N²=M²=0 and fixes the other named coordinate.

This is an exhaustive diagnostic for the finite F₃ norm lemma. It does
not encode induction over p-groups, all odd primes, the unequal-order lift,
or the Sylow-product argument. The binary case is the separately audited
companion proof, including its additional square compatibility. No group
classification or finite group catalogue is used in the uniform theorem.
The unrestricted cyclic-TPP question and historical priority remain outside
this result.
