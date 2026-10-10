# Independent audit: cyclic TPP with abelian Frattini subgroup

10 October 2026. Private internal mathematical review by the survey-audit
agent, separate from the proof author. **PASS: no mathematical gap found.**
This is not external peer review or a priority determination.

The reviewed theorem in [the proof](phase11_abelian_frattini.md) is uniform:
for every finite 2-group with abelian Frattini subgroup, a cyclic subgroup
TPP triple has order product at most the group order. It does not settle
the unrestricted cyclic-TPP question, and does not assert the corresponding
inequality for arbitrary subgroups. The bindings in the accompanying JSON
identify the exact reviewed bytes.

## Induction and the actual direct product

I checked each induction operation within the specified class. For a
subgroup H of P, its Frattini subgroup H²[H,H] lies in Φ(P), and a quotient
has Frattini subgroup Φ(P)N/N. Thus both operations preserve abelianness.
A central subgroup of one cyclic factor can be absorbed into that factor
in a lifted quotient relation; the other two factors meet it trivially.
The ratio of the factor-order product to group order is unchanged.

For a proper pair-generated subgroup H, the third cyclic factor is replaced
by C∩H. Its cosets inject into the ambient cosets of H, giving the required
index inequality without assuming H normal. TPP is invariant under all
permutations by inversion and cyclic rotation of the defining relation.
These steps justify pair generation and the three distinct nonzero
Frattini classes in a minimum counterexample.

The maximal-subgroup restriction (A,B²,C²) halves the violation ratio.
Minimality therefore forces ratio exactly two. The elementary disjoint-
conjugate bound, rather than the classification-dependent phase10 theorem,
gives minimum cyclic factor order at least four.

The central counting step is valid precisely because Φ(P) is abelian.
Multiplication from A²×B²×C² is then a homomorphism, and TPP says its
kernel is trivial. Its image has order |P|/4=|Φ(P)|, so it is the entire
Frattini subgroup. This uses a genuinely injective map; it never infers
injectivity of A×B×C from numerical equality alone. All three squared
factors are nontrivial, so their reductions form the asserted basis of
Φ(P)/2Φ(P).

## Binary action and its group origin

The displayed binary lemma was checked line by line, including its
degenerate cases S=I, T=I and S=T. In the remaining case the two nonzero
square-zero operators have rank one. Commutativity forces their product
to vanish. Distinct image lines would give a common two-dimensional
kernel containing all three basis vectors, which is impossible. With a
common image line, the two independent functionals give the three listed
coordinate possibilities. The resulting line is fixed pointwise.

The extra square identities are essential. Merely requiring commuting
involutions fixing x, y and z under S, T and ST respectively is insufficient.
For example, column-coordinate matrices S=(1,5,3), T=(6,2,3), with vectors
encoded by three-bit integers, satisfy those weaker conditions but have
no common fixed basis vector. They do not satisfy the lemma's complete
square identities for any d,f. The independent checker records the unique
such weaker-hypothesis exception in its row convention.

I independently derived the identities using right conjugation and
d=[b,a]. They give bᵃ=bd, aᵇ=ad⁻¹, hence

    (a²)ᵇ = a² − Sd − d,
    (b²)ᵃ = b² + Td + d,
    (ab)² = a²b²dᵇ.

The first two formulas are additive in the abelian Frattini subgroup.
Writing c=abf gives the remaining (I+ST)f term. The signs disappear
only after reduction modulo 2Φ(P), as required. Conjugation actions commute
and square to the identity because their commutators and squares lie in
Φ(P), whose inner action on itself is trivial.

## Lifting is valid for unequal cyclic orders

The conclusion is about an actual involution in P, not just a fixed vector
in a quotient. Let 2ʳ be the largest order of a squared cyclic factor.
Multiplication by 2ʳ⁻¹ kills all coefficients in shorter factors and all
even coefficients in factors of order 2ʳ. If the binary actions are
trivial, any largest factor supplies a fixed involution. If their common
image line is a largest-factor coordinate, that fixed coordinate supplies
one. If the image coordinate is shorter, any largest-factor coordinate
can change modulo two only in that shorter coordinate, which vanishes
after multiplication. This checks all cases, including r=1 and unequal
exponents. The resulting involution centralizes a and b and therefore P,
contradicting the central-quotient reduction.

## Independent executions and limits

The author's complete binary checker was rerun and its report matched
exactly. An independently written [row-matrix checker](phase11_abelian_frattini_independent_check.py)
imports no author code. Its [report](phase11_abelian_frattini_independent_check.json)
checks all 512 binary matrices, finds 22 involutory matrices, and obtains
32 solutions with four action pairs. It also checks 17,580 image-coefficient
vectors across 256 lifting cases with factor exponents between one and four.

The binary enumeration is exhaustive for its finite lemma. The coefficient
enumeration is only a bounded diagnostic; the written maximal-exponent
argument supplies the all-parameter lift. Neither script encodes the
finite-group induction. Any separate Lean certificate must likewise retain
its finite linear-algebra scope. This review does not claim a complete
formal proof of the group theorem or a new publication-priority result.

The hypertope consequence uses the earlier, separately written reduction:
the three cyclic square-rotation subgroups lie in G′, satisfy TPP by the
source's flag-transitivity hypothesis, and |G:G′|=8. Thus the new theorem
applies when Φ(G′) is abelian. It does not replace flag transitivity by
the C-group intersection property.
