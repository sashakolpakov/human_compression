# Modular endpoint reductions for the PSL(4,q) rank question

10 October 2026. New partial proof, with exact scope stated below. This is
an internal research result; publication priority has not been established.
The remaining rank-five configurations and rank six are not resolved by
this note.

The source target is Conjecture 2, §5, of Leemans,
[*String C-group representations of almost simple groups: a survey*](https://arxiv.org/abs/1910.08843):
for odd q, the maximum string C-group rank of PSL(4,q) is four. Rank-four
existence is the Brooksbank–Leemans result cited as Theorem 5.8 there.
The later existence paper
[*On simple groups that admit a string C-group representation*](https://dipot.ulb.ac.be/dspace/bitstream/2013/397490/3/simpleGroups6.pdf)
does not, from the statements examined, establish this maximum-rank claim.
This is a bounded status check, not proof that no subsequent resolution exists.

## 1. Setup and exact result

Work over an algebraically closed field k of odd characteristic p. Let
T₀,…,T₄ be lifts of a hypothetical rank-five string C-group generating
PSL(4,q), normalized by Tᵢ²=I. Distant generators commute up to signs.
Adjacent generators do not commute projectively: otherwise the string
splits into commuting factors, contrary to simplicity and the intersection
property. Also [T₀],[T₂],[T₄] are independent projective involutions.

Put A=T₀T₁ and B=T₃T₄, and let U,V be their multiplicative unipotent parts.
These are intrinsic matrix Jordan decompositions. A normalized lift and
its negative have the same unipotent part. Consequently T₃,T₄ centralize U,
T₀,T₁ invert U; T₀,T₁ centralize V, and T₃,T₄ invert V. In particular U and
V commute. All assertions remain valid in characteristic three.

**Theorem.** Such a generating tuple must satisfy all of the following:

1. Both A and B have nontrivial unipotent parts. Equivalently, both
   projective endpoint product orders are divisible by p.
2. Every Jordan block of U and V has size at most two.
3. Writing U=I+N and V=I+M, we have
   N²=M²=NM=MN=0, with N,M nonzero.

Thus any remaining rank-five example has two nonzero, commuting,
square-zero endpoint nilpotents whose product is zero. Their ranks are
one or two. This conclusion includes all four choices of cross-commutator
signs; it does not assume the entire endpoint action is semisimple.

The obstruction used repeatedly is that all five generators cannot preserve
a common nonzero bilinear form, even a degenerate form and even up to scalar.
For the natural PSL(4,q), this follows by pulling back to the perfect group
SL₄(q), whose form multiplier is trivial, then applying elementary
transvections. The direct proof is in
[psl4_theory.md](psl4_theory.md), final section. We also use the two tensor
lemmas there and the separated-support and completely reducible endpoint
lemmas in [phase3_psl4.md](phase3_psl4.md), §§1, 2, 4 and 6. Section 6
is essential: it handles reducible completely reducible endpoint modules
with mixed cross signs, which the untwisted tensor lemma alone does not.

## 2. One semisimple endpoint is already enough

**Proposition A.** If either endpoint dihedral acts semisimply on k⁴, the
five generators preserve a common nonzero bilinear form.

It suffices that p does not divide the corresponding endpoint product
order: its projective dihedral group then has order prime to p, and the
normalized lifts form a finite central extension with p-prime kernel.
Conversely, a semisimple representation of a finite dihedral group has
semisimple rotation, so the two formulations coincide here.

**Proof.** Suppose R=⟨T₃,T₄⟩ acts semisimply. Its simple modules have dimension
at most two: for an eigenvector v of T₃T₄, the span of v,T₄v is invariant.
There is a two-dimensional simple constituent, since otherwise T₃,T₄
would commute. The left generators normalize the R-algebra by sign twists
and therefore permute its isotypic components.

If all R-constituents have multiplicity one, every orbit sum of constituents
under the left generators is a simple module for the four endpoints:
an endpoint-invariant submodule is an R-submodule and hence a sum of those
distinct simple constituents. The full endpoint action is then completely
reducible, and the result follows from phase3_psl4.md, §6. This invocation
includes a two-dimensional simple constituent plus two distinct characters,
even when the left action exchanges the characters and the cross signs
are mixed. Complete reducibility alone would not justify invoking only
the earlier untwisted lemma.

There are only two other possibilities in dimension four.

First, there can be one simple two-dimensional R-module and a repeated
one-dimensional R-character. On its two-dimensional multiplicity space,
each right generator is scalar. Conjugation by a left generator therefore
cannot negate either right generator; all four cross signs are positive.
Schur's lemma makes the left generators scalar on the simple R-module.
After sign normalizations the four endpoints have separated support

    T₀=L₀⊕I, T₁=L₁⊕I, T₃=I⊕R₃, T₄=I⊕R₄.

The separated-support lemma applies, including triangular L₀,L₁.

Second, R can have two copies of one simple two-dimensional constituent.
Write its action as R₃⊗I,R₄⊗I. Normalize

    R₄=Z=diag(1,−1),   R₃=[[a,b],[−b,−a]],
    a²−b²=1,         X=[[0,1],[1,0]].

Here b≠0 by simplicity and a≠0 because otherwise T₃,T₄ would anticommute
on all of V. The trace of R₃R₄ is nonzero. A sign twist is isomorphic to
this constituent only if it flips both signs or neither; its intertwiner
is respectively X or I. Schur's lemma thus gives

    T₀=X^ε₀⊗L₀,  T₁=X^ε₁⊗L₁,  ε₀,ε₁∈{0,1}.

The Lᵢ are nonscalar involutions: a scalar Lᵢ would make the left pair
commute projectively. Diagonalize L₀ as Z. If ε₀=1, the middle generator
commutes projectively with Z⊗I and X⊗Z. The block calculation in tensor
Lemma 2 gives the common form Z⊗J, where J=[[0,1],[−1,0]]; its use of
independence is justified by [T₀],[T₂],[T₄]. All four endpoints preserve
that form up to scalar, for either ε₁.

If ε₀=0, the middle generator is monomial in the four joint weight lines
of Z⊗I and I⊗Z. Let Q be the nonzero diagonal form for L₀,L₁ in tensor
Lemma 1. According to its two sign commutators, that lemma selects one of

    Z⊗Q, J⊗Q, Z⊗J, J⊗J.

Every selected form is also preserved by X^ε₁⊗L₁, since X preserves both Z
and J up to scalar. This completes all multiplicity cases. ∎

## 3. Endpoint Jordan blocks of size three or four

**Proposition B.** If the unipotent part of either endpoint product has
a Jordan block of size three or four, the tuple is reducible or preserves
a common nonzero symmetric bilinear form.

**Proof.** Consider U. For a block of size four, U is regular unipotent,
so its centralizer consists of polynomials in U and is commutative.
T₃,T₄ centralize U and would commute, a contradiction.

The only remaining partition with a block of size three is (3,1). Put

    X=(U−I)−(U−I)²/2.

Then X has the same Jordan partition, X³=0, X²≠0, and U=I+X+X²/2.
Inverting U sends X to −X. This truncated logarithm uses only the
denominator two, so is valid also when p=3.

In a basis with X=E₁₂+E₂₃, a matrix centralizing X has the form

    R=[[a,b,c,d],[0,a,b,0],[0,0,a,0],[0,0,e,f]].

For an involution R, its square gives

    a²=f²=1, b=0, 2ac+de=0, (a+f)d=(a+f)e=0.

If a=f then R is scalar; otherwise it has eigenspace dimensions 3 and 1.
Thus both T₃,T₄ are reflections after multiplication by signs. Write their
minus lines as kv₃,kv₄ and their fixed hyperplanes as ker f₃,ker f₄.

If their minus lines coincide, that line is invariant under T₀,T₁ and T₂
as well; the latter commutes with T₄. If their fixed hyperplanes coincide,
the same argument gives an invariant hyperplane. We may exclude both
cases. Their distinct minus lines lie in ker X, since a unipotent commuting
with a reflection acts trivially on its one-dimensional minus space.
They therefore span W=ker X.

An invertible matrix cannot anticommute with a 1+3 reflection. Hence T₀,T₁
commute linearly with T₃,T₄ and preserve both minus lines. At least one of
f₃(v₄),f₄(v₃) is nonzero, since otherwise T₃,T₄ commute. Commuting with
this nonzero cross coefficient forces each left generator to have the same
eigenvalue on both lines. Thus each left generator is scalar on W.

An involution which inverts X and is scalar λ on ker X has eigenvalue λ
with multiplicity three and −λ with multiplicity one. Indeed the
three-step X-chain alternates λ,−λ,λ, and the extra kernel line contributes
λ. Normalize T₀,T₁ to be reflections fixing W pointwise. Their product A
centralizes X and fixes ker X, so the displayed centralizer formula shows
all its eigenvalues are one. Thus A=U. As rank(A−I)=2, the minus lines of
T₀,T₁ span P=im X. We have dim(P∩W)=1 and dim(P+W)=3.

Distinct commuting reflections have each minus line in the other's fixed
hyperplane. Consequently the minus line of T₄ is outside P, and that of
T₀ is outside W. Take e₁ spanning P∩W, e₂ on the minus line of T₀, e₃ on
the minus line of T₄, and e₄ completing their common plus space. The four
reflections become

    T₀=diag(1,−1,1,1),  T₄=diag(1,1,−1,1),
    T₁=I−(e₂+a e₁)(2e₂*+b e₄*),
    T₃=I−(e₃+c e₁)(2e₃*+d e₄*).

Here a,c are nonzero because the respective minus lines are distinct;
b≠0 because (A−I)²≠0; and d≠0 because T₃,T₄ have distinct fixed
hyperplanes. Direct multiplication gives a two-parameter space of common
symmetric forms with entries

    F₁₄=F₄₁=bd t,  F₂₂=2ad t,  F₃₃=2bc t,  F₄₄=z,

all other entries zero. Each endpoint preserves every such F.

The middle T₂ commutes linearly with the two outer reflections. It acts
by signs on e₂,e₃ and by an involution C on ⟨e₁,e₄⟩. If C is scalar it
preserves every F. Otherwise C=[[u,v],[w,−u]], u²+vw=1. The single equation

    2u bd t+w z=0

ensures C preserves the restriction [[0,bd t],[bd t,z]], by direct
multiplication. A nonzero solution (t,z) always exists, and produces a
nonzero F because b,d are nonzero. Thus all five generators preserve a
common nonzero symmetric form. ∎

## 4. Nonzero product of the square-zero parts

**Proposition C.** Suppose U=I+N,V=I+M, with N²=M²=0 and NM≠0. Then
the four endpoints have the untwisted two-by-two tensor form.

**Proof.** N and M commute. If NMv≠0, the vectors v,Nv,Mv,NMv are
independent: apply NM, then M and N, to a proposed dependence. Hence V is
the regular module of the four-dimensional algebra

    R=k[N,M]≅k[x,y]/(x²,y²).

Its centralizer is R itself, and ker N∩ker M is one-dimensional. Both T₀
and T₄ preserve that line, so they cannot anticommute; they commute
linearly. Their simultaneous weight decomposition contains a vector v
with NMv≠0, since some weight component of any such vector still has
nonzero image under NM. Using the preceding four vectors as basis gives,
up to signs and ordering of the tensor basis,

    T₀=Z⊗I,  T₄=I⊗Z,  N=n⊗I,  M=I⊗n,

where n is the nonzero two-dimensional square-zero Jordan matrix.

Both A and B centralize R. This is a local algebra: every unit has scalar
semisimple part. Since their respective unipotent parts are I+N and I+M,
we obtain A=λ(I+N), B=μ(I+M). Inversion by T₀ and T₄ respectively gives
λ²=μ²=1. Consequently T₁=T₀A acts on the first tensor factor and
T₃=BT₄ acts on the second. The untwisted tensor lemma applies. ∎

Combining A, B and C proves the theorem in §1.

## 5. Verification and retained boundary

The companion [phase7_psl4_check.py](phase7_psl4_check.py) verifies the
displayed centralizer-square equations, the characteristic-three-safe
logarithm identity, and all common-form matrix identities symbolically.
Its report is [phase7_psl4_check.json](phase7_psl4_check.json). This check
tests those algebraic identities; it does not replace the module-theoretic
case coverage in the written proofs. No new external peer review is claimed.

The remaining rank-five case is precisely N²=M²=NM=0, with N,M nonzero and
of ranks one or two. A separate working analysis may address it, but it is
not part of this theorem. None of these rank-five reductions by themselves
exclude rank six: the relevant rank-five parabolic in a rank-six string
C-group can be a proper subgroup. The existing uniform rank bound remains
at most six, as proved in [phase3_psl4_rank7.md](phase3_psl4_rank7.md).
