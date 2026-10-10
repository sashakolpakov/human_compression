# Independent audit: generation and conditional unitary intersection property

10 October 2026. Private internal review by the survey-audit agent.
**PASS: no mathematical gap found** in the frozen
[generation theorem](phase11_unitary_template.md) or the
[conditional intersection theorem](phase11_unitary_intersection.md),
under their explicitly retained group-theoretic inputs. The accompanying
JSON binds both proofs, the checkers and fresh independent run records.
This is not external peer review or a publication-priority determination.

The result concerns q≡1 modulo 4 and the stated trace-zero parameter of
full square-field degree. Generation and the string relations hold under
those hypotheses. The complete intersection property is proved when the
middle projective product order is q²−1 or q²+1. The existence of such a
parameter for every intended q is not proved.

## Generation reviewed separately

The parameter condition is attainable for generation alone: a primitive
element of F_q is a nonsquare, and its square root in F_(q²) is nonzero
and trace-zero. The explicit unitary matrices have determinant one, the
stated central squares and distant commutation signs. Projectivization
therefore gives nonidentity string involutions, not involutions in the
unquotiented matrix group.

The second-block projective group contains the required unipotent, whose
unique fixed line is moved by the diagonal element Z. This excludes the
Borel case; its p-element excludes the two dihedral types. The determinant
and norm calculation puts Z outside PSU₂(q). The trace-ratio invariant
of ZS generates the full base field, excluding conjugate subfield groups.
The standard PGU₂/PGL₂ identification is explicitly realized by conjugacy
inside PGL₂(F_(q²)), so this use of the matrix invariant is justified.
The remaining S₄ case occurs only for prime q in the retained list, and
then p≥5 excludes its p-element. The proof retains the exact rank-one
maximal-subgroup list; it does not classify four-dimensional subgroups.

The kernel word is nontrivial in the second projective block because its
unsquared matrix is nonscalar with nonzero trace. The normal-subgroup
argument then supplies PSU₂(q) in that projection. Equal block determinants
and the norm-one condition force the scalar first block to be ±I₂.
Perfection converts the surjective projective second image into the whole
SU₂(q), and taking commutators removes the first block exactly. The claim
that the kernel's derived subgroup is I₂×SU₂(q) is therefore justified.

Conjugates supply coordinate SU₂ groups on a connected graph. Each such
group has a determinant-one unitary monomial map exchanging its coordinate
lines, by surjectivity of the norm. These maps give all coordinate pairs.
The elimination step is valid: a vector of nonzero norm has a pair of
nonzero coordinates with nonzero combined norm unless it already has
one nonzero coordinate. Pairwise cancellation for three or more nonzero
coordinates would contradict odd characteristic. SU₂ acts transitively
on vectors of the prescribed nonzero pair norm by orthogonal-basis
completion and determinant adjustment. Successive elimination and final
diagonal factors generate the full SU₄(q).

## Exact-form descent

For both forms, the displayed semilinear square is a nonzero scalar.
If gFgᵀ=αF with g unitary, then gFH=αFH bar(g). Squaring this relation
as a semilinear relation gives Norm(α)=1. Determinants also give α⁴=1.
Since q+1≡2 modulo 4, only α=±1 remains.

I checked the descent with column vectors and the inverse alternating
matrix. For J₀=aAH conjugation and Norm(a)=c_A⁻¹, J₀²=1. The displayed
decomposition gives a four-dimensional fixed space over F_q spanning
the original space over F_(q²). On fixed vectors the inverse-form value
satisfies bar(F)=−bar(a)F/a; multiplying by δ/a makes it F_q-valued.
Its restriction is nondegenerate because the fixed space spans the entire
space. Exact preservation of A is equivalent to preservation of this
alternating form, and commuting with J₀ recovers unitarity in the converse
direction. The determinant is one. Thus the exact A-stabilizer is indeed
Sp₄(q), not a guessed subgroup inferred from its order.

## Regularity, tori and the factor of two

The projective center of SU₄(q) in this congruence class has order two.
Hence the large projective middle order implies that T has matrix order
prime to p. Its nonzero Krylov determinant makes its characteristic and
minimal polynomials equal, so semisimplicity makes all four roots distinct.
The discriminant then excludes k²=8. The other potential zero factors
are excluded by k≠0 and k∉F_q. Comparing P(X) with P(−X) excludes
opposite eigenvalues, since neither 1 nor −1 is a root in odd characteristic.
Therefore T² also has four distinct eigenvalues.

The independent discriminant calculation for A⁻¹B agrees with the proof.
Its denominator and all its numerator factors are nonzero under the same
conditions. The form ratio W is regular semisimple and commutes with T;
their matrix centralizers, and that of T², are consequently the same
diagonal algebra in a common eigenbasis. Exact preservation of both forms
forces centralization of W, and hence of T².

In the descended symplectic space, reciprocal eigenline pairs give the
five stated torus types. Two individually stable pairs contribute factors
q−1 or q+1; an exchanged pair of pairs gives a cyclic factor q²−1 or
q²+1. No extra disconnected centralizer component occurs for a matrix
with four distinct eigenvalues: a commuting matrix preserves each eigenline.

The projective order of T² is m/2>q+1, ruling out both equal-factor
product tori by exponent. The mixed product torus has order q²−1 and
is correctly left in the list. The gcd exclusions remove the inappropriate
remaining quadratic order. Thus the relevant symplectic centralizer has
order exactly m and bounds the exact common stabilizer by m.

The two independent sign multipliers allow at most four cosets of that
exact stabilizer. Dividing by the central subgroup {±I₄}, which is already
inside the kernel, gives a projective bound 2m. The subgroup generated
by the two middle involutions already has that order. This proves equality
and the exact intersection of the two rank-three subgroups; there is no
missing orientation or central factor in this count.

## The smaller intersections

For the first triple, the order-eight dihedral group has the stated
diagonal Klein four subgroup and its r₁-coset. Every off-diagonal entry
of A is nonzero: k cannot be 0 or ±2i. A diagonal sign matrix can scale
all six entries uniformly only when all its signs agree. Only the identity
from the displayed Klein four has that property. Since r₁ already scales
A, the intersection is exactly the middle involution subgroup.

For the second triple, the projective dihedral group has the stated
4p representatives. Because r₂ already scales B, testing powers of
r₂r₃ suffices. The even-power off-diagonal expression forces t=0.
For odd powers the off-diagonal expression forces t=0 or −1, whereas
the diagonal difference then remains nonzero, including characteristic
three. Thus the only surviving intersection is the other middle
involution subgroup. These arguments require no large middle-order
hypothesis. The standard recursive string-intersection criterion now
applies to both rank-three C-groups and their exact common rank-two group.

## Executed evidence and limits

I separately recomputed the Krylov determinant, both discriminants and
all three power expressions using SymPy. I also reran both supplied
symbolic checkers in scratch directories, preserving their original reports.
The 33 generation identities and 14 intersection checks passed, and their
reports match the saved reports apart from timestamps.

A fresh GAP run of the standalone examples checker passed all four cases:
positive q=5,9,13 and the failed q=9 marking as a negative control. It
constructs 64 subset groups and tests 1,024 pairwise intersections. Its
unitary containment plus full projective action order identifies the
ambient projective groups without a simple-group recognition routine.
The fresh log is saved separately; original scripts and reports are
unchanged. These examples do not prove the remaining parameter-existence
claim. The full generation, descent, torus and intersection arguments are
written proofs, not encoded by the symbolic scripts or a complete Lean
certificate.
