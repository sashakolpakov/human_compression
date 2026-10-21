# A uniform four-generator string construction for odd unitary groups

Private phase-eleven continuation, 10 October 2026. This note proves **generation and the string relations**, not the intersection property. The frozen phase-ten snapshot certified PSU₄(5); the present standalone checker also certifies examples for PSU₄(9) and PSU₄(13). No uniform rank-four existence or priority claim is made here.

## 1. Explicit matrices and the theorem

Let q=p^e≡1 (mod 4), q≥5, let E=F_(q²), and write bar(x)=x^q. Choose i∈F_q with i²=−1 and k∈E* with bar(k)=−k. Assume

    F_p(k²)=F_q.                                             (1)

This hypothesis is always attainable: take k to be a square root in E of a primitive element of F_q*. Define

    H = diag(1,−1,1,−1),       R = [[0,i],[i,0]],
    S = [[k,i−k],[i+k,−k]],    r₂ = diag(R,S),
    r₀ = diag(1,1,−1,−1),
    r₁ = [[1,0,0,0],[0,0,0,1],[0,0,−1,0],[0,1,0,0]],
    r₃ = [[0,I₂],[−I₂,0]].

**Theorem.** These four matrices generate SU(H)=SU₄(q). Their projective images are nonidentity involutions satisfying all string commutations. The first and last adjacent product orders are 4 and 2p, respectively. The middle product has characteristic polynomial

    X⁴+kX³−kX+1.                                           (2)

The group they generate is therefore a rank-four *string-generated group*. The theorem does not assert that this marking is a string C-group.

The only subgroup-classification input in the proof is the usual maximal-subgroup list for PGL₂(q), recorded, for example, as Proposition 2.3 in the [2017 PSL₂ chiral-polytope paper, arXiv:1606.08017](https://arxiv.org/pdf/1606.08017). The standard rank-one identification PGU₂(q)≅PGL₂(q), realized by conjugacy inside PGL₂(F_(q²)), the simplicity of PSL₂(q) for q≥4 and the perfection of SL₂(q) for q≥4 are retained group-theoretic inputs. The generation argument after the two-dimensional calculation is given explicitly below.

## 2. Matrix identities and a two-dimensional projection

All determinants are one, and r_j H bar(r_j)^T=H. The squares are

    r₀²=r₁²=I₄,    r₂²=r₃²=−I₄.

The distant relations hold already with specified lift signs:

    r₀r₂=r₂r₀,    r₀r₃=−r₃r₀,    r₁r₃=−r₃r₁.

The product r₀r₁ has projective order four. Put Z=diag(1,−1) and

    d=(r₀r₁)²=diag(Z,Z),
    u=(r₂r₃)²
      =diag([[1−ik,ik],[−ik,1+ik]],
            [[1+ik,−ik],[ik,1−ik]]).

Both diagonal blocks of u are nonidentity unipotents of order p. The matrix r₂r₃ has characteristic polynomial (X−1)²(X+1)²; its p-th power is nonscalar of order two. Consequently its projective order is 2p.

Let L=⟨d,r₂,u⟩. Every element of L is block diagonal. Each block preserves h=diag(1,−1), and the two block determinants are equal and belong to {1,−1}. Let J₂ be the image of the second block projection in PGU₂(q).

It contains the classes of Z, S and

    V=[[1+ik,−ik],[ik,1−ik]].

The unipotent V has a unique fixed projective line, and Z moves that line. Thus J₂ is not contained in a point stabilizer. Its element of order p excludes the two dihedral maximal-subgroup types, whose orders are 2(q−1) and 2(q+1).

The class of Z lies outside PSU₂(q). Indeed a scalar multiple cZ could have determinant one only if c²=−1, so c=±i∈F_q. But then Norm(c)=−1, contrary to the unitary condition Norm(c)=1. Thus J₂ is not contained in PSL₂(q) under the standard rank-one identification.

For a nonsingular two-by-two matrix M, the quantity

    tau(M) = Tr(M)²/det(M)

is invariant under scalar multiplication and conjugacy. A conjugate subfield subgroup PGL₂(q₀) has all these quantities in F_(q₀). Here

    tau(ZS)=−4k²,

so (1) excludes every proper subfield subgroup. The remaining exceptional maximal type is S₄, which in the PGL₂ list occurs only when q=p. In this case p≥5 and S₄ has no element of order p. Equivalently, its possible trace-square invariants belong to F_p and its element orders give the same exclusion. The retained maximal-subgroup list therefore gives

    J₂=PGU₂(q).                                           (3)

## 3. A kernel word produces a whole coordinate SU₂

Let N be the kernel of the *first projective block projection* from L. The word w=dr₂ has first block ZR with (ZR)²=I₂. Its second block ZS has trace 2k≠0 and is nonscalar. A nonscalar projective involution in odd characteristic has a traceless representative, so (ZS)² is not scalar. Therefore w²∈N has nontrivial second projective image.

By (3), that second image is a nontrivial normal subgroup of PGU₂(q), and hence contains PSU₂(q). To see the last assertion, intersect with the simple normal PSU₂(q). If that intersection were trivial, the normal subgroup would centralize PSU₂(q), whose centralizer in PGU₂(q) is trivial.

The first block of an element of N is a unitary scalar lambda I₂. Equal block determinants give lambda²∈{1,−1}. Since lambda^(q+1)=1 and q+1≡2 (mod 4), necessarily lambda=±1 and lambda²=1. Thus N lies in

    {±I₂} × SU₂(h).

Its second projection D maps onto PSU₂(q), so SU₂(q)=D Z(SU₂(q)). Perfection of SU₂(q) implies D=SU₂(q). Taking commutators now removes the first scalar block and proves

    N' = {I₂} × SU₂(h).

Conjugation by r₃ swaps the two blocks. Hence the four-generator group contains both coordinate SU₂ groups on {1,2} and {3,4}. Conjugating by r₁ supplies the groups on {1,4} and {2,3} as well.

## 4. Connected coordinate SU₂ groups generate SU₄

Here is an elementary version of the final generation step. In a diagonal nondegenerate Hermitian space over E of odd characteristic, the natural SU₂ group on any coordinate pair contains a determinant-one monomial matrix exchanging those coordinate lines: the required coefficient exists because the norm E*→F_q* is surjective. Therefore SU₂ groups on a connected graph of coordinate pairs provide monomial maps realizing all coordinate permutations, and their conjugates provide SU₂ on every pair.

These pair groups perform unitary elimination. If a vector of nonzero norm has at least two nonzero coordinates, choose a pair whose combined norm is nonzero. Such a pair exists: for three or more nonzero coordinates, failure for every pair would imply x₁=−x₂=−x₃ and x₂+x₃=0 for nonzero coordinate norms x_j, contradicting odd characteristic; for precisely two coordinates, their sum is the given nonzero total norm.

The SU₂ group on this pair sends the two coordinates to a vector with just one nonzero coordinate of the same norm. This follows by extending each nonisotropic vector to a Hermitian orthogonal basis and choosing the complementary-vector scalar to make determinant one. Iteration sends any vector of prescribed nonzero norm to a chosen coordinate vector. Applying the same elimination to successive rows of a unitary matrix reduces it to a diagonal unitary matrix; determinant-one diagonal matrices are products of determinant-one diagonal matrices on coordinate pairs. Thus the pair groups generate the whole special unitary group.

The four pairs obtained in §3 form a connected graph. The theorem follows.

## 5. The two proper parabolics preserve explicit forms

This explains why the template is useful beyond an arbitrary generating set, but it does not identify the parabolics as full classical subgroups. Put

    B = diag(i+k,i+k,i−k,i+k),
    A = [[0,−k,k−2i,k],
         [k,0,k,k+2i],
         [−k+2i,−k,0,−k],
         [−k,−k−2i,k,0]].

The form B is symmetric and nonsingular; A is alternating and

    det(A)=(k²−4)²≠0.

The nonvanishing follows because k² is a nonsquare in F_q, whereas 4 is a square. The exact multiplier relations are

    r₀Br₀^T=B,   r₁Br₁^T=B,   r₂Br₂^T=−B,
    r₁Ar₁^T=−A,  r₂Ar₂^T=A,   r₃Ar₃^T=A.

Thus the first rank-three parabolic preserves B up to scalar and the second preserves A up to scalar. In addition,

    A H bar(A) H = (4−k²)I₄.

These are explicit matrix identities, independent of subgroup recognition or enumeration. They leave the exact intersection and the field forms of both full similitude stabilizers to be analyzed.

## 6. Exact examples, a failed marking, and the remaining step

The standalone `phase11_unitary_examples_check.g` builds the natural matrix action on isotropic two-spaces, verifies the full PSU order, and computes all sixteen subset subgroups and all 256 pairwise meets for each case. It uses GAP core algorithms and the unitary order formula, without a simple-group identification routine or external group database.

* q=5, k=Z(25)^3: type {4,26,10}, full intersection property.
* q=9, k=Z(81)^5 Z(9)^2: type {4,80,6}, full intersection property.
* q=13, k=Z(169)^7 Z(13)^4: type {4,170,26}, full intersection property.
* A negative control, q=9 and k=Z(81)^5, generates full PSU₄(9) but fails the intersection property: its type is {4,40,6}, and the two maximal parabolics meet in order 160 while their required dihedral subgroup has order 80.

Here Z(q) denotes GAP's canonical primitive field element. The matrices are generated from the displayed formulas; the checker needs no downloaded generators. The negative control concerns this marking, not nonexistence of a rank-four polytope.

The companion [conditional intersection theorem](phase11_unitary_intersection.md) proves the intersection property whenever the middle projective order is q²−1 or q²+1. It does not prove that such a parameter exists for every field. A separate private order-only screen supplies exploratory evidence; it is not part of the uniform proof. The construction currently addresses only q≡1 (mod 4).

The exact symbolic companion `phase11_unitary_template_check.py/.json` checks 33 matrix identities. It does not formalize Dickson's theorem or the group-generation argument. This note and the conditional intersection proof are written mathematical proofs, subject to the stated retained inputs and review boundary.
