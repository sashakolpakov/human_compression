# Proposed completion of the PSL(2,q) chiral rank-four classification

Status: a proof assembled in this session from the two proposed conjecture proofs and established structural results. The mathematical argument has received internal independent review, but has not been externally peer reviewed. The character-sum argument and eleven exact exceptional witnesses are in [psl2_square_proof.md](psl2_square_proof.md); the intersection argument is in [psl2_intersection_proof.md](psl2_intersection_proof.md).

Source: D. Leemans, J. Moerenhout and E. O'Reilly-Regueiro, *Projective linear groups as automorphism groups of chiral polytopes*, J. Geom. 108 (2017), 675–702; [arXiv:1606.08017](https://arxiv.org/abs/1606.08017). Its introduction states the classification conjecture below. Section 2.1 supplies the rank-four group criterion, Proposition 2.3 supplies Dickson's maximal subgroup classification, and Section 6 supplies the matrices used here.

## Classification for nonprime fields

Let q=p^d with p prime and d>1. Then PSL(2,q) is the full automorphism group of a chiral abstract polytope of rank four if and only if one of the following holds:

1. q is even and q>4;
2. q≡1 modulo 4 and q>9;
3. q≡3 modulo 4 and d is not a prime power.

Cases 1 and 2, and the nonexistence part of case 3 when d is a prime power, are established in the source's Theorem 1. The new argument supplies existence for every exponent in case 3. The source separately classifies the prime-field case d=1 by more intricate congruence and square conditions; the statement above deliberately keeps its original hypothesis d>1.

Together with the source's established nonexistence in rank three and ranks at least five, this completes the existence classification for chiral polytopes with PSL(2,q) as their full automorphism group, subject to verification of the proposed proofs.

## Uniform construction for the missing case

In fact the following construction works for every odd prime p and every odd integer d that is not a prime power, regardless of p modulo 4.

Factor d=e_1e_2 with e_1,e_2>1 odd and coprime. Such a factorization exists by separating the distinct prime-power factors of d into two nonempty sets. Set

    F_1=F_(p^e_1), F_2=F_(p^e_2), L=F_(p^d).

By the proposed proof of Conjecture 6.1, choose primitive j_i∈F_i such that, with

    u=j_1+j_1^(-1), v=j_2+j_2^(-1),

there is a nonzero D∈L satisfying

    D²=u²v²−4(u²+v²).

Use the determinant-one matrices

    α = (1/2) [[u,u+2],[u−2,u]],
    β = (1/2) [[2+u,u],[−u,2−u]],
    γ = (1/(2u)) [[v(u−2),D],[D,v(u+2)]].

We use the same letters for their images in PSL(2,L). All denominators are nonzero. The scalar in γ restores determinant one to the source's final projective representative.

Both u² and v² generate their full respective fields over F_p. For example, if u² belonged to a proper subfield E⊊F_1, the odd degree [F_1:E] and the equation u²∈E would first imply u∈E. Then j_1 satisfies X²−uX+1=0, so the same odd-degree argument implies j_1∈E, contrary to its primitiveness. This also shows u,v≠0, and u²,v²≠4.

## Relations and cyclic intersections

The matrices α and γ have determinant one and traces u and v, so their eigenvalues are respectively j_1,j_1^(-1) and j_2,j_2^(-1). Their projective orders are therefore

    |α|=(p^e_1−1)/2, |γ|=(p^e_2−1)/2.

The matrix β=I+N has N≠0 and N²=0, so its projective order is p. Thus

    <α>∩<β>=1, <β>∩<γ>=1.

Direct multiplication gives

    αβ=[[0,1],[−1,0]],
    tr(βγ)=0, tr(αβγ)=0.

Each of these three matrices has determinant one and trace zero. Its square is −I, and it is nonscalar in odd characteristic, so its projective image has order two. Hence the defining rotation relations hold, with Schläfli type

    { (p^e_1−1)/2, p, (p^e_2−1)/2 }.

The proposed proof of Conjecture 6.2 gives the remaining rank-four intersection condition:

    <α,β>∩<β,γ>=<β>.

This proof establishes equality using intersections of containing conjugate subfield groups; it does not assume that α,β,γ generate PSL(2,L). There is consequently no circularity with the following generation argument.

## Generation of the full group

Let H=<α,β,γ>≤PSL(2,L). We exclude every possible proper maximal overgroup using Dickson's list, as stated in the source's Proposition 2.3.

The element β has order p. With

    T=[[1,2/u],[−1,0]],

the conjugates are

    T^(-1)βT=[[1,1],[0,1]],
    T^(-1)αT=[[1,(2−u)/u],[−u,u−1]].

A nonidentity unipotent has a unique fixed point on the projective line, namely ∞ for the displayed β. The displayed α has nonzero lower-left entry and does not fix ∞. Thus H is in no point stabilizer.

The dihedral maximal subgroups have orders q−1 or q+1, neither divisible by p, and so cannot contain β. The exceptional groups A_4,S_4,A_5 have no element of order at least 13, whereas |α|=(p^e_1−1)/2≥13.

Finally consider any conjugate of a proper subfield subgroup PSL(2,p^k) or PGL(2,p^k). The projective conjugacy invariant

    J(M)=tr(M)²/det(M)

is unchanged on multiplying a representative by a scalar or on conjugating it. It belongs to F_(p^k) for every element of such a subgroup. Consequently both J(α)=u² and J(γ)=v² would belong to F_(p^k). But these elements generate F_1 and F_2 respectively, whose compositum is L. This contradicts k<d. (In the present odd-degree situation the PGL subfield case is absent from Dickson's list anyway.)

All proper maximal overgroups are excluded. Hence H=PSL(2,L).

The same argument also establishes <α,β>≅PSL(2,F_1) and <β,γ>≅PSL(2,F_2) after the respective conjugations in the intersection proof, although these stronger equalities are unnecessary for the construction.

## Chirality: a direct reversal obstruction

The rank-four criterion in the source's Section 2.1 says that the group with the relations and intersections above yields a chiral polytope unless there is an involutory automorphism θ with

    θ(α)=α^(-1), θ(β)=α²β, θ(γ)=γ.

We show there is **no automorphism at all** satisfying the first and third equalities. This avoids any need to classify a possible group extending PSL(2,L) by a reflection.

The standard automorphism theorem gives Aut(PSL(2,L))=PΓL(2,L): an automorphism is projective conjugation composed with a field automorphism τ. This form is stated, for example, in the opening paragraph of D. Gorenstein, [*Finite Groups the Centralizers of whose involutions have Normal 2-Complements*](https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/finite-groups-the-centralizers-of-whose-involutions-have-normal-2complements/6FBC01E6154FF052A081196345F335E9), Canadian J. Math. 21 (1969), 335–357.

Applying the projective invariant J to θ(α)=α^(-1) and θ(γ)=γ gives

    τ(u²)=u², τ(v²)=v².

Since these generate F_1,F_2 and then L, τ is the identity. Thus θ is conjugation by some X∈GL(2,L).

Equality of determinant-one representatives in PSL permits only a sign. Their traces are u and v, both nonzero, while α and α^(-1) have equal trace. Taking traces therefore removes these signs. Choosing the conjugation convention appropriately, X must satisfy

    Xα=α^(-1)X, Xγ=γX.

Put

    A=α−(u/2)I, C=γ−(v/2)I.

These are traceless matrices and A is nonscalar. The centralizer of the nonscalar two-by-two matrix γ is the two-dimensional algebra L[I,γ], so X=xI+tC for some x,t∈L. For traceless two-by-two matrices one has

    AC+CA=tr(AC)I.

Also α^(-1)=uI−α. The first matrix equality consequently becomes

    XA+AX=2xA+t tr(AC)I=0.

The matrices I,A are linearly independent, so x=0 and t tr(AC)=0. However direct multiplication of the displayed α,γ gives

    tr(αγ)=(uv+D)/2,
    tr(AC)=tr(αγ)−uv/2=D/2≠0.

Thus t=0 and X=0, contrary to invertibility. The required reversing automorphism does not exist. The polytope is chiral and its full automorphism group is PSL(2,L).

This proves the construction and supplies the outstanding case of the classification. QED.

## Audit of the complete implication

The dependencies are explicit:

1. The primitive-square theorem supplies j_1,j_2,D for all parameters, using a classical character-sum theorem and eleven finite certificates.
2. The independent intersection theorem uses only these parameters, odd degree, coprime extension degrees, and explicit matrix conjugations.
3. Dickson's maximal subgroup theorem proves generation; the standard semilinear automorphism theorem and the direct trace calculation prove chirality.
4. The established rotation-group criterion produces the chiral rank-four polytope. The source's published positive and negative results supply the other classification cases.

The eleven exceptional certificates were produced by GAP and independently checked by a separate implementation of polynomial quotient fields using Python's standard library; see [verify_square_witnesses.py](verify_square_witnesses.py) and [its result record](psl2_square_witnesses_independent.json). No enumeration in PSL(2,p^d) is assumed. The finite integer reduction is likewise exact and deterministic.

Internal review found no remaining mathematical gap in this chain. The main remaining qualifications are external review and novelty checking; internal audit is not publication or community acceptance. The Lean files in the accompanying directory certify selected algebraic lemmas, not the whole classification or the character-sum theorem.
