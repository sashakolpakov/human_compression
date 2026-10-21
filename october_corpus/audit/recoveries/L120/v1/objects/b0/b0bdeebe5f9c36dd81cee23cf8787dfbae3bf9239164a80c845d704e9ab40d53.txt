# Phase 18: a bilinear-form alternative for rank-three markings in dimension four

Date: 2026-10-10. This is a written structural result and a diagnostic for the frozen phase-16/17 constructions. It does not establish uniform rank-three existence or nonexistence for either diagonal extension. No publication-priority claim is made.

## 1. The two possible configurations

Let $K$ be algebraically closed of characteristic different from two. Let $a,b,c\in\operatorname{PGL}(V)$ be nonidentity involutions, where $\dim_K V=4$ and $ac=ca$. Assume $\langle a,b,c\rangle$ acts irreducibly on $V$. Choose lifts $A,B,C$ with $A^2=B^2=C^2=I$. The relation between the endpoint lifts is either $AC=CA$ or $AC=-CA$.

**Theorem.** At least one of the following holds:

1. The generated projective group preserves a nondegenerate symmetric or alternating bilinear form up to scalar.
2. $AC=CA$, all four simultaneous characters of $\langle A,C\rangle$ occur with multiplicity one, and $B$ has eigenvalue multiplicities $(2,2)$.
3. $AC=-CA$, and $B$ has eigenvalue multiplicities $(3,1)$ or $(1,3)$.

These alternatives need not be mutually exclusive. In particular, the two listed configurations are necessary possibilities for a group with no bilinear similarity form; they are not sufficient criteria for generation.

**Proof.** The vector space of symmetric bilinear forms has dimension ten. If $AC=CA$, write the dimensions of the simultaneous eigenspaces as $d_1,\ldots,d_t$. The forms invariant under both $A$ and $C$ are exactly the symmetric forms supported on these diagonal blocks, and have dimension
\[
  \sum_j d_j(d_j+1)/2.
\]
This is four precisely when all four dimensions are one, and is at least five otherwise. A nontrivial involution $B$ with multiplicities $(2,2)$ has a six-dimensional space of invariant symmetric forms. With multiplicities $(3,1)$ it has a seven-dimensional such space. The dimension inequality for two subspaces of a ten-dimensional space therefore gives a nonzero form invariant under $A,B,C$, unless configuration 2 holds.

If $AC=-CA$, the $+1$ and $-1$ eigenspaces of $A$ have equal dimensions and are interchanged by $C$. A basis gives
\[
 A=\begin{pmatrix}I_2&0\\0&-I_2\end{pmatrix},\qquad
 C=\begin{pmatrix}0&I_2\\I_2&0\end{pmatrix}.
\]
The alternating forms satisfying $A^tFA=-F$ and $C^tFC=-F$ include exactly the three-dimensional space
\[
 F=\begin{pmatrix}0&S\\-S&0\end{pmatrix},\qquad S=S^t.
\]
If $B$ has multiplicities $(2,2)$, its alternating forms satisfying $B^tFB=-F$ form a four-dimensional space: in a $B$-eigenbasis they are the arbitrary cross-block forms. Both spaces lie in the six-dimensional space of all alternating forms, so their intersection is nonzero. This leaves configuration 3 as the only other case.

In either form-producing case, its radical is invariant under all three generators. Irreducibility therefore makes every resulting nonzero form nondegenerate. Rescaling a lift changes only its similarity multiplier, so the conclusion is projectively meaningful. $\square$

The endpoint commutator is indeed $\pm I$: if $AC=\lambda CA$, conjugation of $C^2=I$ by $A$ gives $\lambda^2=1$.

## 2. Consequences for folds of the frozen constructions

Let $(r_0,r_1,r_2,r_3)$ be either the phase-16 linear marking or either phase-17 unitary marking. Both proposed direct folds
\[
 (r_0,r_1r_3,r_2),\qquad (r_1,r_0r_2,r_3)
\]
generate proper subgroups for **every** parameter covered by those constructions.

For the first fold, the lifts of $r_0,r_2$ commute ordinarily, and $r_1r_3$ is a projective reflection. In the unitary matrix pattern it is the coordinate transposition $(1\ 3)$. In the linear pattern its diagonal is $(-1,1,-1,-1)$. The first part of the theorem supplies a symmetric form whenever the folded group is irreducible.

For the second fold, the commuting endpoint lifts are $r_1,r_3$, and $r_1$ is a reflection. Their simultaneous eigenspaces cannot have four distinct one-dimensional characters: the one-dimensional exceptional eigenspace of $r_1$ supports only one character, and its three-dimensional complementary eigenspace supports at most two. Thus the endpoint form space has dimension at least five, again forcing a symmetric form if the folded group is irreducible.

The full ambient groups are absolutely irreducible and have no bilinear similarity form by the retained [phase-nine argument](phase9_linear_unitary.md). Consequently a reducible folded group or an irreducible folded group preserving such a form is necessarily proper. This deduction does not rely on finite sampling.

The original local hypothesis of Brooksbank--Leemans rank reduction fails as well. In an irreducible rank-four string C-group,
\[
 \langle r_0,r_2,r_3\rangle=\langle r_0\rangle\times\langle r_2,r_3\rangle.
\]
When $|r_2r_3|$ is even, the dihedral factor has a homomorphism to $C_2$ sending $r_2$ to one and $r_3$ to zero. The subgroup $\langle r_0r_2,r_3\rangle$ lies in its graph and excludes $r_0$. The dual argument applies at the other end. The primary [rank-reduction paper, Theorem 1.1 and Corollary 1.2](https://arxiv.org/abs/1812.01055) only gives sufficient hypotheses and explicitly does not claim necessity; hence their failure alone would not have proved the present generation obstruction.

## 3. What remains to construct

The frozen almost-simple diagonal groups have no nontrivial cyclic normal subgroup: such a subgroup intersects their nonabelian simple socle trivially, then commutes with it, contradicting the trivial socle centralizer. Conder--Oliveros, *The intersection condition for regular polytopes*, Theorem 4.1, therefore makes the intersection property automatic for any generating triple of nonidentity involutions with commuting distinct endpoints and adjacent product orders greater than two. This primary theorem is also explicitly restated as Theorem A in [Baktybekov--Conder--Nuzhin--Rezantseva (2025), pp. 498--505](https://elib.sfu-kras.ru/handle/2311/156158), and in [Conder's slides, pp. 21--22](https://www.fields.utoronto.ca/programs/scientific/13-14/discretegeom/Slides/Conder.pdf).

Thus uniform rank-three existence has been reduced to a generation problem. The theorem above sharply narrows the possible four-dimensional configurations; it does not solve that generation problem. The discovery scripts `phase18_folding_probe.g`, `phase18_pauli_probe.g`, `phase18_twisted_middle_probe.g` and `phase18_split_middle_probe.g` are exploratory exact computations, not universal existence proofs.
