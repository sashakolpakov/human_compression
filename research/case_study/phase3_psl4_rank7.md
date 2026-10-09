# A tensor obstruction for rank seven in odd-characteristic PGL4

9 October 2026. This is a separate extension of
[phase3_psl4.md](phase3_psl4.md). The proof below does not assume
semisimplicity of a parabolic subgroup. Publication priority has not been
established. Its scope is rank seven; it does not resolve the maximum-rank
four conjecture for PSL(4,q).

**Theorem.** Let k be algebraically closed of odd characteristic. Let
ρ₀,…,ρ₆ be a rank-seven string C-group embedded in PGL₄(k), and suppose
every adjacent pair fails to commute. Then, after conjugacy, the entire
group lies in the projective image of GL₂(k)⊗GL₂(k). In particular it
preserves a nondegenerate symmetric bilinear form up to scalar.

Consequently PSL(4,q), q odd, has no rank-seven string C-group
representation. Together with the independently proved rank-eight
exclusion and elementary-abelian bound in phase3_psl4.md, this gives the
uniform upper bound **six**. Ranks five and six remain unresolved.

## The Pauli algebra and its supports

Normalize lifts Tᵢ of the involutions so Tᵢ²=I. The intersection property
makes E=⟨ρ₀,ρ₂,ρ₄,ρ₆⟩ an elementary abelian group of rank four. The
dimension bound from §5 of phase3_psl4.md implies that its lift
commutator form ω is nondegenerate, and its four-dimensional action is
irreducible. Write its underlying F₂-vector space as V, with ordered
basis v₀,v₂,v₄,v₆ corresponding to these four generators.

Choose a nonzero lift P_v for each v∈V. The sixteen matrices P_v form a
basis of M₄(k), the Pauli basis, and satisfy

    P_v P_w = c(v,w) P_(v+w),      c(v,w) ≠ 0,
    P_v P_w = (−1)^ω(v,w) P_w P_v.                 (1)

These assertions follow directly by taking a symplectic basis of V:
each anticommuting pair generates M₂(k), and the two commuting pairs
give M₂(k)⊗M₂(k)=M₄(k). No finite-field arithmetic is used here.

For a nonzero matrix A, let supp(A) be the set of labels having nonzero
coefficient in its Pauli-basis expansion. If A commutes projectively
with every P_u for u in a subspace U of V, then its support lies in an
affine coset of U⊥. Indeed conjugation by P_u is diagonal on the Pauli
basis, with eigenvalue (−1)^ω(u,v), so every supported label must have
the same eigenvalue for each u.

## The intersection property forces full two-dimensional supports

Put

    L=span(v₀,v₂),             R=span(v₄,v₆),
    W₁=R⊥,                    W₅=L⊥,
    S₁=supp(T₁),              S₅=supp(T₅).

The string relations place S₁ in an affine coset of W₁ and S₅ in an
affine coset of W₅. Both W₁ and W₅ have dimension two, and

    W₁∩W₅=(L+R)⊥=0.                              (2)

We claim that the differences of points of S₁ span all of W₁. The
pairing ω:L×W₁→F₂ is nondegenerate: its left kernel is
L∩W₁⊥=L∩R=0, and both spaces have dimension two. If the difference
span were proper, some nonzero z∈L would annihilate it. Then ω(z,v)
would be constant over v∈S₁, so P_z would commute or anticommute with
T₁. Thus the nonidentity projective element z, one of ρ₀,ρ₂,ρ₀ρ₂,
would commute with ρ₁.

The first two choices directly contradict noncommutation of adjacent
generators. The last contradicts the local intersection-property lemma:
if r,s,t are consecutive generators and rt commutes with s, then
(sr)²=(st)² belongs to ⟨r,s⟩∩⟨s,t⟩=⟨s⟩, which forces (sr)²=1.
For completeness the alternative (sr)²=s would imply rsr=1 and hence
s=1, impossible for a generator. This proves the claim. The same
argument applies to S₅ and the adjacent pair ρ₄,ρ₆. Therefore

    span(S₁−S₁)=W₁,       span(S₅−S₅)=W₅.         (3)

## Unique product labels force a tensor decomposition

The generators ρ₁,ρ₅ commute projectively. Thus
T₁T₅=εT₅T₁ for ε∈{1,−1}. In expanding these two products in the Pauli
basis, a label a+b with a∈S₁,b∈S₅ has a unique such decomposition:
two different decompositions would give a nonzero common difference in
W₁∩W₅, contrary to (2). Its coefficient is nonzero, since it is a
product of two nonzero coefficients and the nonzero scalar c(a,b).
Comparison using (1) therefore gives

    (−1)^ω(a,b)=ε for every a∈S₁,b∈S₅.             (4)

Taking differences in both variables and using (3) gives
ω(W₁,W₅)=0. Since these spaces are complementary and each has
dimension two, they are nondegenerate orthogonal complements.
Taking differences only in a in (4) gives ω(W₁,b)=0 for each b∈S₅,
so S₅⊆W₁⊥=W₅. Likewise S₁⊆W₁. Finally

    W₁=W₅⊥=L,             W₅=W₁⊥=R.               (5)

Thus L and R are orthogonal nondegenerate two-dimensional subspaces of
V, and T₁ lies in the Pauli algebra of L while T₅ lies in that of R.
The resulting tensor decomposition k⁴=k²⊗k² puts six generators in
the forms

    T₀=L₀⊗I,   T₁=L₁⊗I,   T₂=L₂⊗I,
    T₄=I⊗R₄,   T₅=I⊗R₅,   T₆=I⊗R₆.             (6)

In particular L₀,L₂ anticommute, and R₄,R₆ anticommute. Equation (4)
now also implies ε=1, though the sign is not needed below.

## The middle generator is a tensor as well

The string relations make T₃ commute projectively with T₀ and T₁.
Choose a basis in the first factor with

    L₀=diag(1,−1),       L₁=[[a,b],[c,−a]],
    a²+bc=1.

The matrices L₀,L₁ are nonscalar involutions. Since their projective
classes do not commute, a≠0 and (b,c)≠(0,0): a=0 would give
anticommutation, while b=c=0 would give commutation.

For signs ε₀,ε₁, the space of two-by-two matrices A satisfying

    A L₀=ε₀ L₀ A,       A L₁=ε₁ L₁ A

is, by direct entry comparison,

| ε₀ | ε₁ | Intertwiner space |
|---|---|---|
| +1 | +1 | kI |
| +1 | −1 | 0 |
| −1 | +1 | 0 |
| −1 | −1 | k·[[0,b],[−c,0]] |

This calculation does not require bc≠0. If bc=0 the last generator is
singular, but its space still has dimension one.

Expand T₃ as a two-by-two matrix of first-factor coefficient matrices.
Each coefficient lies in the same simultaneous intertwiner space, with
the signs fixed by T₃. Since every nonzero such space has dimension
one, T₃=A⊗B for two matrices A,B. Invertibility of T₃ forces both
A and B to be invertible. This establishes the tensor assertion for
all seven generators.

For J=[[0,1],[−1,0]], every two-by-two matrix M satisfies
MᵀJM=det(M)J. Therefore every invertible tensor A⊗B preserves
J⊗J up to the scalar det(A)det(B). The form J⊗J is symmetric and
nondegenerate. This proves the theorem. ∎

The natural PSL(4,q) cannot preserve such a form: after pullback to
SL₄(q), the similarity multiplier is trivial by perfectness, and the
elementary transvections force every entry of an invariant bilinear
form to vanish. The explicit transvection proof is in psl4_theory.md.

## Verification boundary

The support argument and resulting tensor normal form are proofs over
an algebraically closed field of arbitrary odd characteristic. Finite
examples are not used to establish them. The intersection-property
step is the same local group lemma covered by StringIntersection.lean;
the Pauli-support argument and tensor reduction are not yet formalized
in Lean. This note makes no claim about ranks five or six or about
publication priority.
