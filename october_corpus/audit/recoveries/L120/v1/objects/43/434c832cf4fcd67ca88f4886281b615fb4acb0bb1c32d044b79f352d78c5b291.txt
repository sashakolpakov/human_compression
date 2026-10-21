# Independent review of the q=9^e unitary parameter theorem

10 October 2026. Root reviewed every section of
[the parameter proof](phase12_unitary_parameters.md). The written argument
passes internal mathematical review under its declared retained inputs.
The final source and check hashes are recorded in the accompanying JSON.
This is neither external peer review nor a priority determination.

## Character estimate and exact count

The norm-one torus descent is essential. The Cayley expression changes
to its reciprocal under coefficient conjugation, so it defines a morphism
over F_q to that torus. Its character sheaf is obtained from the torus
Lang isogeny. Root independently opened the primary author-hosted Katz
book and read §§2.3.1–2.3.2, the proof surrounding §3.6.1, and §4.3
(PDF pages 20,24,33; printed pages 32–33,40–41,58–59). These supply
the stated Euler, trace, weight and general commutative-group character
sheaf inputs. No whole-book reading is claimed.

Over an algebraic closure, the split factor has its two ramification
points at zero and infinity; the nonsplit factor has them at the two
conjugate Cayley zero/pole points. Odd nontrivial character orders
remain nontrivial after multiplication by two. The supports are disjoint,
so the tensor product is geometrically nonconstant and tame at four
points. Euler characteristic and vanishing of H_c⁰,H_c² give dimension
two for H_c¹. Finite monodromy and the retained weight bound give 2√q.
This is a written derivation using retained cohomology, not a new proof
of that machinery or a formal certificate.

The two one-character sums are exactly zero and minus two. In particular
the domain has q−1 elements, while its primitive-indicator expansion has
main term q+1: summing the minus-two contributions over the nontrivial
squarefree divisors of n contributes plus two. The indicator coefficients,
their absolute sums W(m)−1 and W(n)−1, and the fact that a nonsquare
already has full two-primary order are all used with the correct groups.
No additional power-of-two sieve is missing.

The universal bound on W uses only primes 5 through 61 as possible
factors larger than one in W(D)/D^(1/6). Since m,n are coprime odd
3-free integers and mn<q²/16, the claimed threshold covers e≥8.
The seven remaining rows use exact integer factorizations and strict
integer inequalities; their executable verification is separate.

## Eigenvalues, projective order and field degree

The characteristic-three Cayley identity gives tt′=2, and expanding the
two quadratics gives the exact template polynomial. Trace-zero elements
have nonsquare squares; this excludes k=0. The first eigenvalue pair
has order exponent 2(q−1), the second q+1. Within-pair coincidences are
excluded by the primitive/odd orders, and their distinct norm behavior
excludes cross-pair coincidences. Thus the matrix is semisimple of order
q²−1. Its half-power has signs minus on one pair and plus on the other,
so it is not scalar. With scalar kernel of order two, this proves the
same projective order; matrix order alone would not suffice.

For the square-field lemma, nonsquareness forces the extension degree
over F_p(k²) to be odd. A proper subfield would therefore have relative
degree at least three and would contain i. The same matrix lies in
SU₄(q₀). The eigenvalue orbits under α↦α^(−q₀) have total length at
most four, bounding its order by (q₀+1)^4. This contradicts its required
order at least q₀⁶−1. Generation is not used to prove the field condition,
so there is no circular appeal to the preceding template theorem.

All hypotheses of the frozen generation and conditional-intersection
proofs are consequently satisfied. Together with the separately retained
rank obstruction, this gives maximum rank four for PSU₄(9^e), every e≥1,
and explicit type {4,q²−1,6}. Other odd field sizes remain outside this
existence proof. No complete Lean formalization, full odd-unitary solution,
infinity marker or new proof-length ratio is inferred.
