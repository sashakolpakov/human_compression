# Independent review: dimension-four linear and unitary rank bounds

**Date:** 10 October 2026. **Reviewer:** survey_audit agent. **Reviewed note:** [phase9_linear_unitary.md](phase9_linear_unitary.md). Final source hashes are recorded in the companion audit JSON.

**Verdict:** no mathematical gap found in the new application arguments for Theorems A and B. The review treats the phase-eight dimension-four bilinear-form alternative as an explicit inherited theorem; it does not independently repeat that theorem's full normal-form classification. No external peer review or priority determination is claimed.

## 1. Character obstruction, including the smallest field

I independently checked the determinant-one diagonal torus over an algebraically closed field of characteristic p, with exponent m prime to p. An exponent vector restricts trivially precisely when all four coordinates are congruent modulo m. For two degree-two weights, a zero difference coordinate and a nonzero coordinate of absolute value at most two separate the characters whenever the combined support has at most three coordinates. Combined support four means two disjoint off-diagonal pairs, giving the difference pattern (1,1,−1,−1), also separated for m ≥ 3. This proves separation for every permitted m, rather than just for large fields.

An independently written checker gives a second exact certificate: for all 45 pairs of the ten weights, subtract their fourth coordinate from the other coordinates and take the integer gcd. Character equality at exponent m is equivalent to m dividing that gcd. The gcd is 1 for 36 pairs and 2 for 9 pairs. Thus no m ≥ 3 gives a collision. These computations are exhaustive over the fixed list of exponent patterns; they are not samples over q.

The coordinate weights are distinct, and the torus order m³ is prime to p, so a torus-invariant subspace is a sum of coordinate weight lines. The even permutation matrices act transitively on those lines. Consequently the natural monomial action is absolutely irreducible, even when p = 3 and the permutation subgroup itself is not semisimple.

For an ordinary bilinear similarity matrix B, all nonzero entries must have the same torus weight. Hence its support is confined to one diagonal position or one unordered off-diagonal pair and its rank is at most two. Since B is nonzero, its left radical is proper and nonzero. Similarities preserve that radical, contradicting irreducibility. The proof applies to arbitrary bilinear forms, without assuming symmetry first.

For SU₄(q), use the identity Hermitian form and m = q+1. Norm-one diagonal matrices of determinant one and the even coordinate permutations lie in SU₄(q). Odd q gives m ≥ 4, including m = 4 at q = 3. The Hermitian form is sesquilinear, so its existence does not conflict with the absence of an ordinary bilinear similarity form over the algebraic closure.

## 2. Projective centralizers and the linear small-field case

The diagonal matrix with entries ζ, ζ⁻¹, 1, 1 has exactly one eigenvalue of multiplicity two when m ≥ 3. If X conjugates it to a scalar multiple of itself, that scalar must be 1. Varying the chosen coordinate pair forces X to be diagonal. Projective commutation with a coordinate 3-cycle then has scalar 1, since the cycle fixes a coordinate on which X has a nonzero entry. The 3-cycles force all entries of X to coincide. This verifies triviality of the projective centralizer without a perfectness assumption or a potentially ambiguous scalar character.

For the linear group the split torus at q = 3 is too small, and the note correctly uses transvections instead. If u = I+Eᵢⱼ preserves B up to scalar, uᵖ = I forces its multiplier to be a p-th root of unity. In characteristic p that multiplier is 1. Subtracting invariance for u and u⁻¹ yields EⱼᵢB + BEᵢⱼ = 0 because 2 is invertible. Every entry of B is an isolated entry of one such equation, so B = 0. I checked the indices directly; the author's row formulation and the independent checker's column formulation both give the same conclusion.

The independent script checks each of the 16 isolated-entry identities on all 16 matrix units, giving 256 exact integer checks. Since these are identities linear in B with coefficients 0 and 1, they are valid over every field. Odd characteristic is still needed in the preceding subtraction step. Absolute irreducibility follows from invariance under all matrix units, and projective centralization of a transvection is ordinary centralization because its only eigenvalue is 1. The resulting common centralizer is scalar.

## 3. Passage to intermediate groups

The note explicitly retains the standard simplicity of PSL₄(q) and PSU₄(q) for odd q. For an intermediate G, its simple socle S is normal and has trivial centralizer in G by the preceding elementary arguments.

A commuting adjacent pair in a string C-group splits its distinguished generators into two mutually commuting nonempty sets. The subgroup intersection property makes their generated subgroups intersect trivially, so G is their internal direct product. For a nontrivial factor A, simplicity gives A∩S = 1 or S. In the first case [A,S] = 1, contradicting the trivial centralizer; in the second the other factor centralizes S, with the same contradiction. Thus all adjacent generators are noncommuting.

The group is finite, lies in PGL₄ over the algebraic closure, and acts irreducibly. All hypotheses of the inherited phase-eight theorem therefore apply. Rank at least five would produce the forbidden nondegenerate ordinary bilinear similarity form. This proves the stated upper bound of four for both intermediate-group intervals. It does not address field or graph automorphisms, which need not act by linear projectivities in this four-dimensional representation.

## 4. Quotients and exact conclusions

The determinant quotient computations pass. On the unitary side the determinant of an isometry ranges over the norm-one cyclic group; scalar isometries contribute fourth powers. A similitude can be rescaled to an isometry because the finite-field norm is onto. Therefore PGU₄(q)/PSU₄(q) is cyclic of order gcd(4,q+1), with the analogous order gcd(4,q−1) on the linear side.

An involution-generated group's abelian quotient has exponent at most two. The cyclic quotient of order four is consequently an absolute obstruction to involution generation. The full PGL₄(q) obstruction occurs at q ≡ 1 mod 4; the full PGU₄(q) obstruction occurs at q ≡ 3 mod 4. A cyclic quotient of order two supplies no existence theorem. The note makes this distinction correctly.

Rank-four existence is retained only for PSL₄(q), from Brooksbank–Leemans. The unitary conclusions retain the Leemans–Vandenschrick existence classification: PSU₄(3) has no string C-group representations; for odd q ≥ 5, PSU₄(q) has rank three and the present result limits its spectrum to {3,4}. Whether rank four occurs is not decided. No existence inference is made for index-two extensions, and the result is not presented as a full solution of the survey's Problem 7.

## 5. Bounded primary-source check

I reread the relevant passages of the [survey](https://arxiv.org/html/1910.08843v2): Theorem 3.1 records PSU₄(3) as a rank-three exception; §5.7, Problem 7 asks for maximal ranks of arbitrary almost-simple groups with socle PSL₄(q). No named PSU₄ maximum-rank conjecture was located in that survey.

The [Leemans–Vandenschrick author manuscript](https://dipot.ulb.ac.be/dspace/bitstream/2013/397490/3/simpleGroups6.pdf), Theorem 1.1 and its introduction, supports exactly the two unitary existence statements used above. This is an existence classification, not a maximum-rank theorem. The [2026 publication record](https://repozitorij.upr.si/IzpisGradiva.php?id=22370&lang=eng) distinguishes its November 2025 online publication from its 2026 journal issue.

The checked [Brooksbank symplectic/orthogonal rank paper](https://arxiv.org/html/1912.05512v1) has an exact-rank theorem for PSp₄(q), not PSU₄(q). Its discussion of full orthogonal or symmetry-generated groups must not be transferred to PΩ₆⁻(q) ≅ PSU₄(q) without an additional argument. The [Cameron–Herman–Leemans Schur-index paper](https://research-repository.st-andrews.ac.uk/bitstream/10023/26879/1/210414jpaaCHL_final.pdf), introduction and §4 inspected, uses rank-three unitary representations and does not give a PSU₄ maximum-rank or rank-four-existence theorem. Its Theorem 3 has n ≥ 8; it is not a source for the four-dimensional case.

Fourteen targeted search queries used PSU₄/PSU(4,q), PGU₄, PGL₄ and orthogonal-minus-six variants with string C-groups, polytopes and maximum rank. No primary source explicitly proving the same uniform upper bound or uniform odd-PSU₄ rank-four existence was located. Mathematical notation is imperfectly indexed, and this was not an exhaustive thesis, language or unpublished-work search. Absence of a match does not establish novelty or current openness. The companion JSON preserves the query strings and reading scope.

## 6. Certificate scope

[phase9_torus_character_audit.py](phase9_torus_character_audit.py) and its [report](phase9_torus_character_audit.json) are independent of the author's checker and use only Python's standard library. They certify the uniform character-divisor list and the 256 isolated-entry identities. The written review supplies the links from those identities to the group-theoretic application. Neither script formalizes the full application or the inherited phase-eight theorem; group simplicity and the published existence statements remain retained inputs.
