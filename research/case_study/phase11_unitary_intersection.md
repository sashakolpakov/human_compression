# An intersection criterion for the unitary matrix template

Private phase-eleven continuation, 10 October 2026. This is a conditional construction theorem. Existence of a parameter satisfying its rotation-order condition for every q is **not** proved.

Use the matrices r₀,r₁,r₂,r₃ and forms H,A,B from [the uniform generation note](phase11_unitary_template.md), with q=p^e≡1 (mod 4), q≥5, k^q=−k≠0 and F_p(k²)=F_q. Write rho_j for their images in PSU₄(q).

**Theorem.** If the projective order m of r₁r₂ is either q²−1 or q²+1, then the four projective involutions form a string C-group for PSU₄(q), of type {4,m,2p}.

The proof establishes the intersections directly using the two forms. It does not require identifying either rank-three subgroup with a full orthogonal or symplectic group.

## 1. Exact-form stabilizers and descent

Let U=SU(H). For a nonsingular matrix F write Sim_U(F) for the set of g∈U such that gFg^T is a scalar multiple of F. The explicit identities are

    A H bar(A) H = c_A I,    c_A=4−k²,
    B H bar(B) H = c_B I,    c_B=−1−k².

Both c_A and c_B are nonzero elements of F_q. If gFg^T=alpha F, unitarity implies

    g F H = alpha F H bar(g).

Composing the corresponding semilinear maps twice shows Norm(alpha)=1. Taking determinants gives alpha⁴=1. Since q+1≡2 (mod 4), these conditions force alpha∈{1,−1}.

Consequently the common similitude stabilizer

    M=Sim_U(A) ∩ Sim_U(B)

has a homomorphism to {±1}², with kernel K consisting of the elements preserving both forms exactly.

The exact A-stabilizer in U is isomorphic to Sp₄(q). Here is the required elementary descent argument. On column vectors put J(v)=A H bar(v), so J²=c_A. Choose a∈E* with Norm(a)=c_A^−1 and set J₀=aJ. Then J₀²=1. Its fixed space V₀ has dimension four over F_q: using any nonzero trace-zero delta, every v has the unique decomposition

    v=(v+J₀v)/2 + delta · (v−J₀v)/(2delta),

with both parenthesized coefficients fixed by J₀. The alternating form F(v,w)=v^T A^−1 w on V₀ satisfies

    bar(F(v,w))=−bar(a)/a · F(v,w).

Therefore (delta/a)F is F_q-valued and nondegenerate on V₀. Elements of the exact A-stabilizer commute with J₀ and preserve this alternating form. Conversely, every isometry of this alternating F_q-form extends E-linearly, preserves A, and commutes with J₀; the relation defining J₀ then recovers preservation of H. Its determinant is one. This identifies the stabilizer with Sp(V₀)≅Sp₄(q).

## 2. A regular centralizer bounds the common stabilizer

Set T=r₁r₂ and W=A B^−1. Each of r₁,r₂ multiplies exactly one of A,B by −1, so T commutes with W. Also T² preserves A and B exactly.

The characteristic polynomial of T is

    P(X)=X⁴+kX³−kX+1.

The determinant of the Krylov matrix with columns e₁,Te₁,T²e₁,T³e₁ is i(k−i), which is nonzero. Hence T is cyclic. Under the theorem's hypothesis its matrix order divides 2m, because the scalar center of SU₄(q) has order two. Since p does not divide 2m, T is semisimple and P is separable. Its discriminant is

    disc(P)=4(k²−8)²(k²+1),

so k²≠8. No two eigenvalues of T are negatives of one another: if P(lambda)=P(−lambda)=0, subtraction gives lambda²=1, whereas P(1)=P(−1)=2≠0. Thus T² also has four distinct eigenvalues.

For completeness, an exact calculation for S=A^−1 B gives

    disc(char_S)
      = −256 k⁸(k−i)(k+i)⁷(k²−8)² / (k²−4)¹⁰.

Every factor in this expression is nonzero under the present hypotheses. Therefore S, and hence W (which is conjugate to S^−1), is regular semisimple. Since W commutes with T, the full matrix centralizers of W,T,T² coincide after extension to an algebraic closure: they are the diagonal matrices in their common eigenbasis. In particular every member of K centralizes T².

The element T² lies in the exact A-stabilizer Sp₄(q) described in §1 and is regular semisimple there. Its centralizer is a rank-two symplectic torus. Its possible structures, obtained by allowing Frobenius to permute the two reciprocal eigenvalue pairs, are

    C_(q−1) × C_(q−1),   C_(q−1) × C_(q+1),
    C_(q+1) × C_(q+1),   C_(q²−1),   C_(q²+1).

This list follows directly from the eigenlines: a Frobenius-fixed reciprocal pair contributes q−1 or q+1; an exchanged pair contributes q²−1 or q²+1 according to whether Frobenius squared fixes or exchanges its two lines. It uses no maximal-subgroup classification of Sp₄.

The projective order of T² is m/2>q+1, so the two equal-factor product tori are excluded by their exponents. If m=q²+1, the remaining order q²−1 types are excluded because gcd((q²+1)/2,q²−1)=1. If m=q²−1, the order q²+1 type is excluded because gcd((q²−1)/2,q²+1)≤2. Thus the relevant centralizer has order exactly m, and |K|≤m.

The center {±I₄} lies in K. The sign quotient has order at most four, so the projective common similitude stabilizer has order at most 2m. It already contains ⟨rho₁,rho₂⟩, a dihedral group of order 2m. Therefore

    projective(M) = ⟨rho₁,rho₂⟩.                       (3)

The first rank-three subgroup preserves B up to scalar, and the second preserves A up to scalar. Equation (3) proves their exact intersection.

## 3. Both rank-three subgroups have the intersection property

The following verifications in fact work for every nonzero trace-zero k, without the large-order hypothesis.

For the first triple, D=⟨rho₀,rho₁⟩ is dihedral of order eight. Its representatives are generated by r₁ and the diagonal Klein four group

    {I₄,r₀,d,r₀d},    d=(r₀r₁)².

All six off-diagonal entries of A are nonzero. A diagonal sign matrix can multiply A by one scalar only if all four signs coincide. Of the displayed Klein four matrices, only I₄ is scalar. Since r₁ multiplies A by −1, it follows that

    D ∩ projective(Sim_U(A)) = ⟨rho₁⟩.

The group ⟨rho₁,rho₂⟩ preserves A up to scalar, which gives the required intersection for the first rank-three subgroup.

For the second triple put v=r₂r₃ and U=v². The projective group ⟨rho₂,rho₃⟩ is dihedral of order 4p, with elements represented by v^j or r₂v^j for 0≤j<2p. Because r₂ already preserves B up to scalar, it is enough to test v^j.

For j=2t with t∈F_p, v^j=U^t. The upper-left block of B is (i+k)I₂. The off-diagonal entry of its transformed upper-left block is

    −2(i+k)k²t².

Hence preservation up to scalar forces t=0. For j=2t+1, the upper-right block of v^j is R times the second block of U^t. The transformed upper-left B block has off-diagonal entry and diagonal difference

    2ik²t(t+1),    −2k(2t+1),

respectively. They cannot both vanish in odd characteristic: the first forces t=0 or −1, and neither solves the second. Thus no odd power preserves B up to scalar, and

    ⟨rho₂,rho₃⟩ ∩ projective(Sim_U(B)) = ⟨rho₂⟩.

This proves the intersection property for the second rank-three subgroup. The standard recursive string-intersection criterion now combines these two rank-three verifications with (3), proving the rank-four intersection property. Full group generation was established independently in the companion note.

## 4. What remains

The theorem reduces uniform existence in this congruence class to a specific parameter problem: find nonzero trace-zero k of full square-field degree for which the projective order of the companion-like matrix with polynomial X⁴+kX³−kX+1 is q²−1 or q²+1.

The standalone `phase11_unitary_examples_check.g` verifies successful parameters for q=5,9,13, testing all sixteen subgroup closures and all 256 pairwise meets in each case; it also verifies a failed q=9 marking as a negative control. The exact symbolic companion `phase11_unitary_intersection_check.py/.json` checks the discriminants, form-ratio identities and the rank-three meet calculations. These finite and symbolic checks do not prove parameter existence for all q. The theorem and the generation argument remain paper proofs supported by those identities; they are not full Lean formalizations.
