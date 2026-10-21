# Maximum string C-group rank four for PSL(4,q), q odd

10 October 2026. Written proof with two independent internal mathematical
reviews and exact algebra checks. This is not external peer review;
publication priority remains provisional.

**Theorem.** For every odd prime power q, PSL(4,q) has maximum string
C-group rank four.

The new step in this note excludes rank six. Together with the earlier
rank bounds and rank-five exclusion listed in §8, and the published
rank-four constructions, it proves the theorem. The precise target is
Conjecture 2 in §5.7 of Leemans's
[*String C-group representations of almost simple groups: a survey*](https://arxiv.org/abs/1910.08843).
The retained existence input is Brooksbank–Leemans,
[*Polytopes of large rank for PSL(4,q)*](https://digitalcommons.bucknell.edu/fac_journ/1204/),
Journal of Algebra 452 (2016), 390–400, Theorem 1.1.

## 1. Setup and extra commutations

Let T₀,…,T₅ be normalized involution lifts of a hypothetical rank-six
string C-group generating natural PSL(4,q), over an algebraically closed
field k of odd characteristic. Every adjacent projective pair does not
commute, and each triple of pairwise distant generators is independent.
Put

    A=T₀T₁, B=T₄T₅, U=A_unipotent, V=B_unipotent.

The endpoint group H=⟨T₀,T₁,T₄,T₅⟩ has the same signed cross-commutation
relations as the four endpoints in the rank-five analysis. The decisive
extra relations are

    T₂ centralizes T₀,T₄,T₅ projectively;
    T₃ centralizes T₀,T₁,T₅ projectively.

In particular T₂ centralizes V linearly and T₃ centralizes U linearly.
All endpoint matrices preserve the images and kernels of both unipotent
parts. A common proper invariant subspace or nonzero bilinear similarity
form is incompatible with natural PSL(4,q).

## 2. Two basic endpoint configurations

### 2.1 Untwisted tensor endpoints

Suppose

    T₀=L₀⊗I, T₁=L₁⊗I, T₄=I⊗R₄, T₅=I⊗R₅,

with noncommuting projective adjacent pairs. Then both middle matrices
are pure tensors, and all six preserve J⊗J up to scalar.

Here is a direct intertwiner argument valid also for triangular pairs.
Normalize R₅=Z and write R₄=[[a,b],[c,−a]]. Noncommutation projectively
gives a≠0 and (b,c)≠(0,0). For each prescribed pair of commutation signs,
the simultaneous sign-intertwiner space in M₂(k) has dimension at most
one. The positive-positive space is the scalar line. The negative-negative
space consists of [[0,x],[y,0]] with by+cx=0. The two other sign spaces
are zero, because a≠0. Each 2×2 block of T₂ lies in the same such space,
so T₂=C⊗D. Invertibility forces D invertible. The same argument gives
T₃=E⊗F from its left-pair commutations. Every 2×2 matrix is a similarity
of the alternating form J; hence the tensor claim follows.

### 2.2 Separated support

Suppose

    T₀=L₀⊕I, T₁=L₁⊕I, T₄=I⊕R₄, T₅=I⊕R₅.

The four endpoint matrices are projective reflections. All their distant
commutations are linear. If either adjacent endpoint pair has the same
minus line, the whole rank-six group preserves it: the near middle
commutes with the outer member and the other middle with both. If the
pair has the same fixed hyperplane, the same argument gives an invariant
hyperplane.

Otherwise each pair has distinct minus lines and fixed hyperplanes.
The two minus lines of the left pair span its two-dimensional support,
and their fixed hyperplanes intersect in the other support. Thus T₃,
which commutes with both left reflections, preserves both supports.
The same argument with the right pair applies to T₂. All six matrices
therefore preserve the direct-sum decomposition. This case is reducible.

## 3. A repeated simple endpoint module

Suppose the right endpoint dihedral acts as two copies of one simple
two-dimensional module. Normalize as in phase7_psl4.md:

    T₄=R₄⊗I, T₅=R₅⊗I,
    R₅=Z, R₄=[[a,b],[−b,−a]], a,b≠0,
    K=X, T₀=K^ε₀⊗L₀, T₁=K^ε₁⊗L₁.

The Lᵢ are nonscalar involutions whose pair does not commute projectively.
Schur's lemma and the two allowed sign twists give

    T₂=K^η⊗C.

If ε₀=1, diagonalize L₀=Z. The middle T₃ commutes projectively with
T₀=X⊗Z and T₅=Z⊗I. The anticommuting tensor lemma in psl4_theory.md
gives the form Z⊗J; the needed independence is that of [T₀],[T₃],[T₅].
All endpoints preserve it, and so does T₂=K^η⊗C. Thus it is common to
all six.

If ε₀=ε₁=0, the argument in §2.1 makes T₃ a pure tensor. All six are
then pure tensors and preserve J⊗J.

It remains that ε₀=0, ε₁=1. Set L₀=Z and write
L₁=[[c,d],[e,−c]], with c≠0: otherwise T₀,T₁ would anticommute.
The four joint weight lines of T₀=I⊗Z and T₅=Z⊗I are distinct. Hence
T₃ is monomial, with a fixed translation (α,β) on their square. Write

    T₃ e_(i,j)=h_(i,j)e_(i+α,j+β).

Compare the term in T₁=X⊗L₁ that changes i and keeps j. Its coefficient
is c(−1)^j, which is nonzero. The relation T₃T₁=σT₁T₃ gives

    h_(i+1,j)=σ(−1)^β h_(i,j).

The ratio is independent of j, so h_(i,j)=r_i s_j and T₃ is a pure
tensor. Again every generator preserves J⊗J.

By reversing the string, the same conclusion holds if the left dihedral
is a repeated simple two-dimensional module.

## 4. Completely reducible endpoint action

The classification in phase3_psl4.md, §§2, 4 and 6, applies to H.
Untwisted tensor and separated support were handled in §2. If H is
irreducible, its two normal forms there are

    (I) T₀=L₀⊗I, T₁=L₁⊗I;
    (II) T₀=L₀⊗I, T₁=L₁⊗Z,

with L₀=Z, L₁=[[a,b],[−b,−a]], a,b≠0, and

    Tⱼ=K^εⱼ⊗Rⱼ, K=X, j=4,5.

Form I is already covered by the repeated-simple-module result, with
left and right reversed. In form II, R₄,R₅ are off-diagonal, and the same
sign-intertwiner classification of the two inequivalent left constituents
gives T₃=K^η⊗C, with C diagonal or off-diagonal.

If ε₄=1 or ε₅=1, choose such a j. T₂ commutes projectively with
T₀=Z⊗I and Tⱼ=X⊗Rⱼ. The triple [T₀],[T₂],[Tⱼ] is independent because
its indices are pairwise distant. Diagonalize Rⱼ and apply the anticommuting
tensor lemma to get the form Z⊗J. All four endpoints and the pure tensor
T₃ preserve that form too.

If ε₄=ε₅=0, the right pair acts only on the second factor. Its
two-dimensional sign-intertwiner spaces have dimension at most one by
§2.1, so T₂ is a pure tensor as well. Then J⊗J is common.

### 4.1 Reducible mixed-sign endpoint modules

The remaining completely reducible case is H=U⊕W, dim U=dim W=2, with
a negative cross sign. The complete sign table in phase3_psl4.md, §6,
leaves one negative, two in one row or column, or four negatives.
Two opposite-corner negatives and three negatives already make an
adjacent pair commute projectively and are impossible.

We claim that in every viable case a matrix centralizing any three
endpoint generators projectively preserves U and W. The following
normal forms establish the claim. Overall signs on individual blocks do
not affect the argument, since every intertwiner may already twist each
generator by a prescribed sign.

For one negative cross sign, the four matrices, in their respective
roles, are

    Z⊕Z, X⊕X, X⊕I, I⊕Z.

If a triple includes the first two, its restrictions on both U,W are
simple Pauli modules; the third has scalar action on exactly one block,
so those modules are inequivalent under every sign twist. If a triple
omits one of the first two, its restriction on one block is a sum of
characters and its restriction on the other is simple two-dimensional.
There are no off-diagonal intertwiners in either situation.

For two negatives in a row, take

    Z⊕Z, X⊕I, X⊕X, X⊕Y,

where Y is off-diagonal and Y≠±X. A column is the same argument with
left and right reversed. Omitting Z⊕Z leaves an abelian action on U
and the simple pair X,Y on W; simplicity holds because Y is off-diagonal
and not proportional to X. Omitting X⊕I leaves simple modules on both
blocks, distinguished by whether the last two generators commute
linearly. Omitting either right generator leaves simple modules on both
blocks, distinguished by the scalar versus nonscalar action of X⊕I.
Again every off-diagonal intertwiner vanishes.

For four negatives, normalize T₀=Z⊕Z and T₄=X⊕X. In each block write
T₁=aZ+bJ and T₅=cX+dJ. Their required anticommutation gives bd=0.
Global projective noncommutation of the adjacent pairs forces complementary
blocks, giving, after a possible block exchange,

    T₀=Z⊕Z, T₁=L⊕Z, T₄=X⊕X, T₅=X⊕R,

where L anticommutes with X and L≠±Z, while R anticommutes with Z
and R≠±X. Every triple acts simply on both blocks. A triple containing
both left generators distinguishes U,W by their noncommutation versus
commutation; a triple containing both right generators does so in the
opposite direction. Every three-element subset contains one such pair.
Sign twists preserve a commutator, so no off-diagonal intertwiner exists.

Both middle generators centralize three endpoints projectively. The
claim makes them preserve U and W, contradicting irreducibility. This
finishes all completely reducible endpoint actions.

There is also a direct uniform certificate for the vanishing of the
off-diagonal intertwiners, avoiding any module-simplicity inference in
this subsection. In each displayed normal form, the left adjacent pair
commutes on exactly one block and has invertible additive commutator
PQ−QP on the other; the right adjacent pair has the complementary
pattern. Every triple contains one of the two adjacent pairs. An
off-diagonal intertwiner C for that pair satisfies

    (P_U Q_U−Q_U P_U) C
      =σ_P σ_Q C (P_W Q_W−Q_W P_W).

One commutator is zero and the other invertible, forcing C=0, and likewise
for the opposite block direction. The needed nonzero determinants are
det(ZX−XZ)=4, det(XY−YX)=−(t−t⁻¹)² for
Y=[[0,t],[t⁻¹,0]], and det(ZL−LZ)=−4b² for L=aZ+bJ.
Here t²≠1 and b≠0 are precisely the nonproportionality conditions above.

## 5. One semisimple endpoint suffices in rank six too

Suppose the right endpoint acts semisimply. As in phase7_psl4.md,
its simple constituents have dimensions one or two and at least one
has dimension two. If its constituents have multiplicity one, the full
endpoint action is completely reducible and §4 applies. If it has one
simple two-dimensional constituent plus a repeated character, the four
endpoints have separated support and §2.2 applies. If it is two copies
of one simple constituent, §3 applies. These exhaust the dimension budget.
The same argument holds at the left endpoint.

Consequently a surviving rank-six tuple would require both U,V nontrivial.

## 6. Jordan blocks of size three or four

If U is regular unipotent of size four, its commutative centralizer
contains T₄,T₅, an immediate contradiction. If U has type (3,1), let
X=(U−I)−(U−I)²/2. The proof in phase7_psl4.md makes the right endpoints
reflections. If their minus lines or fixed hyperplanes coincide, the
whole rank-six group preserves that line or hyperplane, because T₂
commutes with both and T₃ with the outer right reflection.

Otherwise their distinct minus lines span W=ker X. The four endpoints
preserve W. So does T₂, since it commutes with both right reflections.
So does T₃, since it centralizes U, hence X. Therefore W is a common
proper invariant subspace. This excludes type (3,1). The right endpoint
is symmetric. We are left with U=I+N,V=I+M and N²=M²=0.

If NM≠0, Proposition C of phase7_psl4.md gives untwisted tensor endpoints,
which §2.1 excludes. Hence NM=MN=0.

## 7. The zero-product modules in rank six

Use the complete endpoint normal-form classification in
phase7_psl4_zero_product.md; its derivation uses only the endpoint
relations until the explicitly marked middle-generator analysis.

For rank pair (1,1), distinct image lines and independent defining
functionals yield separated support, covered by §2.2. A common image
line is preserved by T₂ because it centralizes M and by T₃ because it
centralizes N. A common kernel gives the dual invariant hyperplane.
Thus all rank-(1,1) cases are reducible.

For rank pair (1,2), use

    N=E₁₄, M=E₁₃+E₂₄,
    T₀=diag(1,−1,1,−1), T₅=diag(1,−1,−1,1).

T₂ preserves W=im M=⟨e₁,e₂⟩. The outer joint weight lines are distinct,
so T₃, which commutes projectively with both outer generators, is monomial
with a fixed weight-square translation. It also centralizes N and hence
preserves its image line ke₁. A nonzero translation fixes no weight line,
so its translation is zero: T₃ is diagonal. Thus it preserves W as well.
The four endpoints preserve W, giving reducibility. The reversed rank
pair is symmetric.

For rank pair (2,2), the common space W=im N=ker N=im M=ker M has
dimension two. Both middles preserve it by their respective centralizations
of M and N. This case is immediately reducible.

## 8. Conclusion and exact dependency map

The endpoint action is either completely reducible, has a semisimple
endpoint, has a unipotent block of size at least three, has square-zero
parts with nonzero product, or has nonzero square-zero parts with zero
product. Sections 2–7 exhaust these alternatives. Each forces a proper
invariant subspace or a common nonzero bilinear similarity form, neither
of which natural PSL(4,q) permits. Hence rank six is impossible.

The full maximum-rank theorem uses the following explicit chain.

| Step | Result used |
|---|---|
| Ranks above eight | Elementary-abelian dimension bound, [phase3_psl4.md](phase3_psl4.md), §5 |
| Rank eight | Intersection-property and projective-centralizer argument, phase3_psl4.md, §7 |
| Rank seven | Pauli support and tensor obstruction, [phase3_psl4_rank7.md](phase3_psl4_rank7.md) |
| Rank five | [phase7_psl4.md](phase7_psl4.md) and [phase7_psl4_zero_product.md](phase7_psl4_zero_product.md) |
| Rank six | The present note, §§1–7 |
| Rank four exists | Brooksbank–Leemans (2016), Theorem 1.1; also survey Theorem 5.8 |

The endpoint classifications in phase3_psl4.md, §§2, 4 and 6, and the
tensor/common-form arguments in [psl4_theory.md](psl4_theory.md) are retained
proof dependencies. The rank-six modular reduction uses only the endpoint
normal-form portions of the rank-five proof, plus the stronger middle
commutations available in rank six. It does not infer that a rank-five
parabolic must generate the full group.

The root agent and `rank_stability` agent independently reviewed the
whole proof and found no gap. The latter also independently reran
[phase8_psl4_rank6_check.py](phase8_psl4_rank6_check.py): 33 exact identities
and 12 three-endpoint distinguishing-pair witnesses passed. The report is
[phase8_psl4_rank6_check.json](phase8_psl4_rank6_check.json). These checks
verify the new intertwiner and form identities, including their explicit
nonvanishing factors in every odd characteristic; the written proof and
reviews establish case coverage. The generic additive-commutator transport
and zero-intertwiner step are also formalized in
[IntertwinerSeparation.lean](formal/IntertwinerSeparation.lean). That limited
formal certificate does not formalize the whole classification or theorem.

A current-status check on 10 October 2026 located the survey's exact
conjecture and the original rank-four existence statement. The later
Leemans–Vandenschrick
[*On simple groups that admit a string C-group representation*](https://dipot.ulb.ac.be/dspace/bitstream/2013/397490/3/simpleGroups6.pdf),
Theorem 1.1, classifies existence and does not state this odd-PSL4 maximum-
rank result. Targeted searches located no explicit later resolution.
That is bounded search evidence, not a proof of publication priority.

## 9. Structural consequence beyond PSL(4,q)

**Corollary.** Let G be a finite subgroup of PGL₄(k), with k algebraically
closed of odd characteristic. Suppose its natural projective action is
irreducible and G is a string C-group with every adjacent pair noncommuting.
If its rank is at least five, it preserves a nondegenerate symmetric or
alternating bilinear form up to scalar.

**Proof.** The elementary-abelian dimension bound and rank-eight exclusion
apply to every such projective string C-group, so the rank is at most
seven. The rank-seven proof already gives a nondegenerate symmetric form.
In the rank-five and rank-six analyses, every case gives either a proper
invariant subspace or a nonzero common bilinear similarity form. All
preliminary normal-form and sign arguments use only the stated string,
independence and dimension hypotheses; the PSL4-specific input occurs
solely when excluding that final form. Irreducibility rules out the
invariant-subspace branches, and the radical of a nonzero common form is
invariant, so that form is nondegenerate.

For completeness, if a produced bilinear form is not already symmetric
or alternating, its symmetric and alternating parts are similarity forms
with the same multiplier. At least one is nonzero in odd characteristic;
its radical is invariant, so it too is nondegenerate. This proves the
corollary. ∎

This corollary explains the obstruction uniformly: a four-dimensional
irreducible projective string action of rank at least five must preserve
one of these forms. It does not classify all such form-preserving groups,
assert a maximal rank for them, or address general field/graph automorphism
extensions of PSL(4,q).
