---
title: "Four families of projective general linear maniplexes"
author: "human_compression project"
date: "10 October 2026"
geometry: margin=27mm
fontsize: 11pt
---

## 1. The question

The final paragraph of Section 5 in Leemans and Toledo [LT] proposes four
infinite families of regular rank-four maniplexes with automorphism group
$\operatorname{PGL}_2(q)$. In each family one end group is the full group;
the other is respectively $S_4$, $A_5$, $\operatorname{PSL}_2(q)$, or
$\operatorname{PGL}_2(q)$. We construct all four families over prime fields.
The question asks for infinitely many examples in each class, rather than
an example for every prime power or a classification of all examples.

Throughout, $p$ is an odd prime and

$$G=\operatorname{PGL}_2(\mathbf F_p),\qquad
T=\operatorname{PSL}_2(\mathbf F_p).$$

A string marking of rank four is a generating tuple $(a,b,c,d)$ of
pairwise distinct nonidentity involutions satisfying

$$[a,c]=[a,d]=[b,d]=1.\tag{1}$$

Its two end groups are $\langle a,b,c\rangle$ and $\langle b,c,d\rangle$.
We use the correspondence between such markings and regular maniplexes
from [LT, Section 2]. For the needed direction the proof is immediate:
take the flags to be $G$ and adjacency of colour $i$ to be left
multiplication by the corresponding marker. Every adjacency and every
product of two different adjacencies is fixed-point-free, since the
markers are nonidentity and distinct. Equation (1) gives the required
commutations, and generation gives connectedness. An automorphism
preserving colours commutes with all left translations. Its value at the
identity determines it as a right translation. Thus the full group of
colour-preserving automorphisms is the right regular action of $G$, and
the maniplex is regular. This argument imposes no intersection property.

**Theorem 1.** For every prime in each of the following rows there is a
string marking of $G$ with the indicated end groups.

| Prime condition | $\langle a,b,c\rangle$ | $\langle b,c,d\rangle$ |
|---|---|---|
| $p>5$, $p\equiv3,5\pmod8$ | $S_4$ | $G$ |
| $p\equiv9,11\pmod{20}$ | $A_5$ | $G$ |
| $p\equiv5\pmod{12}$ | $T$ | $G$ |
| $p>3$, $p\equiv3\pmod4$ | $G$ | $G$ |

Reversing the marking in the first three rows puts the full group at the
facet end, as in [LT]. Dirichlet's theorem gives infinitely many primes
in each indicated progression. Since $|G|=p(p^2-1)$ strictly increases,
the resulting maniplexes are pairwise nonisomorphic. Hence Theorem 1
answers the four-family conjecture in the bound May 15, 2023 author
edition of [LT]. A bounded search for later solutions found none; an
exhaustive priority claim is not made.

## 2. Inputs from the common theory and from subgroup classification

The determinant modulo squares gives an epimorphism

$$\epsilon:G\longrightarrow\mathbf F_p^*/(\mathbf F_p^*)^2\cong C_2,
\qquad\ker\epsilon=T.\tag{2}$$

The common projective-line paper [E, Theorem 5] proves the following
centralizer statement without any intersection hypothesis. If two
projective involutions have product of order greater than two in odd
characteristic, their common centralizer is trivial when the product is
unipotent, and has order two when it is semisimple. If a matrix $A$
represents the product in the latter case, the nonidentity common
centralizer element is represented by

$$A-\frac{\operatorname{tr}(A)}2I.\tag{3}$$

We use this proved interface, rather than applying a theorem about
polytopes to a maniplex that may fail intersection.

We retain the following precise classical classification inputs. By
Giudici [G, Theorem 3.5, p. 10], for prime $p>3$ a maximal subgroup of
$G$ not containing $T$ is an affine point stabilizer, a dihedral torus
normalizer, or an $S_4$ subgroup. The last possibility occurs exactly
when $p\equiv\pm3\pmod8$. The minor exceptional omission among the
dihedral groups at $p=5$ does not affect our use. There are no subfield
cases when the field is prime. By [G, Theorem 2.2(6), p. 4], $T$ has an
$A_5$ subgroup for primes $p\equiv\pm1\pmod{10}$. These statements
replace the unrestricted sentence about proper nonabelian subgroups in
[LT, Section 5], which would omit affine, dihedral, and subfield groups.
Both cited page numbers are also the physical page numbers of the bound
Giudici PDF.

We also retain the usual finite Coxeter identifications
$[3,3,3]=W(A_4)$ and $[3,3,4]=W(B_4)$, of orders $120$ and $384$.
The first acts by adjacent transpositions on five letters. The second
acts by adjacent coordinate swaps and a final sign change on four
coordinates, giving $2^4\cdot4!$ elements. Their standard Coxeter
presentations, rather than merely the existence of permutation
quotients of those orders, are the retained input. Independent GAP
calculations verify the exact orders of those literal presentations.
The elementary quadratic-character formulas and Dirichlet's theorem
are also classical inputs.

## 3. A constant quadruple of matrices

Over $\mathbf F_p$, with $p>3$, put

$$R_0=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad
R_1=\begin{pmatrix}1&0\\1&-1\end{pmatrix},\quad
R_2=\begin{pmatrix}-1&0\\0&1\end{pmatrix},\quad
R_3=\begin{pmatrix}1&-2\\2&-1\end{pmatrix}.\tag{4}$$

Let $a,b,c,d$ be their projective classes. Direct multiplication gives
$R_i^2=I$ for $i=0,1,2$, and $R_3^2=-3I$. Their determinants are

$$\det R_0=\det R_1=\det R_2=-1,\qquad\det R_3=3.\tag{5}$$

Each matrix is nonscalar and invertible. The three nonadjacent pairs
anticommute as matrices, so their projective classes satisfy (1).
The classes are pairwise distinct: the zero patterns distinguish
$R_0,R_1,R_2$, whereas $R_3$ has no zero entry. Thus the four classes
are distinct nonidentity involutions. Furthermore,

$$R_1R_2=-\begin{pmatrix}1&0\\1&1\end{pmatrix},\qquad
(R_0R_1)^3=-I.\tag{6}$$

The second product is nonscalar, so $|ab|=3$. If
$L(t)=\left(\begin{smallmatrix}1&0\\t&1\end{smallmatrix}\right)$,
then $L(1)^n=L(n)$. It is scalar exactly when $n=0$ in the field.
Consequently $|bc|=p$, and its powers run through the full group
$U=\{[L(t)]:t\in\mathbf F_p\}$, since the field is prime.

We act on the projective line by fractional linear transformations.
The unique common fixed point of $U$ is $0$. Both $a$ and $d$ move
this point: $a(0)=\infty$ and $d(0)=2$. Each end group therefore
satisfies the following elementary criterion.

**Lemma 2.** If $H\leq G$ contains $U$ and an element $g$ with
$g(0)\ne0$, then $T\leq H$.

*Proof.* The group $gUg^{-1}$ is the full unipotent subgroup fixing
$g(0)$. The action of $U$ on the complement of $0$ is transitive:
reciprocation identifies it with addition on $\mathbf F_p$. Choose
$u\in U$ carrying $g(0)$ to $\infty$. Then $H$ contains
$ugUg^{-1}u^{-1}$, the full upper unipotent subgroup.

Upper and lower elementary matrices generate $\operatorname{SL}_2$.
Here is the needed elimination argument. Write
$V(t)=\left(\begin{smallmatrix}1&t\\0&1\end{smallmatrix}\right)$.
For $t\ne0$,

$$W(t)=V(t)L(-t^{-1})V(t)=
\begin{pmatrix}0&t\\-t^{-1}&0\end{pmatrix},\qquad
W(t)W(-1)=\operatorname{diag}(t,t^{-1}).$$

Multiplication by $W(1)$ makes the top left entry of a determinant-one
matrix nonzero if necessary. A lower elementary operation then clears
the bottom left entry, an upper operation clears the top right entry,
and the remaining diagonal matrix has the displayed form. Thus every
determinant-one matrix is a product of these elementary matrices.
Passing to projective classes proves the lemma. $\square$

Both end groups of (4) contain $T$. If $p\equiv3\pmod4$, then $-1$
is nonsquare, so each end contains $b\notin T$ and equals $G$. This
proves the fourth row of Theorem 1. If $p\equiv5\pmod{12}$, then
$-1$ is square and $3$ is nonsquare. Equations (2) and (5) give
$\langle a,b,c\rangle=T$ and $\langle b,c,d\rangle=G$, proving the
third row, including $p=5$. Neither argument needs the exceptional
subgroup classification.

This quadruple also explains its relationship to [LT]. When
$p\equiv1\pmod{12}$, both determinants are square, and both ends are
$T$. Choose $s$ with $s^2=-1$ and put $D=\operatorname{diag}(-s,1)$.
If $S_i$ are the first three matrices of [LT, Lemma 4.5], then
$DS_0D^{-1}=-sR_0$, $DS_1D^{-1}=sR_1$, and $DS_2D^{-1}=sR_2$.
Their projective classes are therefore the first three classes of (4). The fourth is the
unique nonidentity common centralizer of the first two, so it agrees
as well. Thus (4) is a normalization of the source's known family.
The contribution here is its use at other determinant classes, with
an elementary argument controlling both end groups.

## 4. Excluding affine and dihedral end groups

The remaining constructions extend an exceptional local group by the
centralizer element (3). We first isolate the obstruction needed to
show that the opposite end is the full group.

**Lemma 3.** Suppose $(a,b,c,d)$ is a string marking of $G$, with
$|bc|=3$ and $|ab|>2$. Then $H=\langle b,c,d\rangle$ is contained
in neither an affine point stabilizer nor a dihedral subgroup of $G$.

*Proof.* The centre of $G$ is trivial. Indeed, a central projectivity
must fix the unique common fixed point of each unipotent subgroup, so
fixes every point of the projective line and is the identity.

In an affine point stabilizer in odd characteristic, a nonidentity
involution has the form $x\mapsto-x+t$. Two such involutions commute
only if they coincide, as their two products are translations by
$t-u$ and $u-t$. The distinct commuting involutions $b,d$ exclude
this possibility.

Suppose next that $H$ is dihedral. Since $|bc|=3$, both $b$ and $c$
are noncentral reflections. If $d$ were central in $H$, it would
commute with $b,c$ and also with $a$, making it central in $G$.
Otherwise $d$ is another reflection. As $b,d$ are distinct and
commute, $z=bd$ is the nonidentity central involution of $H$, and
$d=bz$. Thus $cd=(cb)z$ has order six and $(cd)^3=z$. In particular,
$b=dz\in\langle c,d\rangle$. But $a$ commutes with $c,d$, so would
commute with $b$, contrary to $|ab|>2$. A nonabelian subgroup of a
dihedral group is itself dihedral, which proves the assertion about
containment as well. $\square$

## 5. The symmetric local group

Let $p>5$ and $p\equiv\pm3\pmod8$. The retained subgroup theorem
gives a maximal subgroup $S\cong S_4$ of $G$ not containing $T$.
It cannot lie inside $T$, since then $S<T<G$ would contradict
maximality. The restriction of $\epsilon$ to $S$ is consequently its
unique nontrivial homomorphism to $C_2$, namely the sign character.

Under an isomorphism with $S_4$, take

$$a=(1\,2),\qquad b=(2\,3),\qquad c=(3\,4).\tag{7}$$

These generate $S$, have $|ab|=|bc|=3$, and satisfy $[a,c]=1$.
Since $p\ne3$, the product $ab$ is semisimple. By (3) the common
centralizer of $a,b$ in $G$ is $\{1,d\}$. Inside $S_4$ the
centralizer of $\langle(1\,2),(2\,3)\rangle$ is trivial: its
centralizer on the first three letters is trivial, and the fourth
letter must be fixed. Hence $d\notin S$. It is an involution,
distinct from $a,b,c$, and maximality gives $\langle S,d\rangle=G$.
All relations (1) hold.

It remains to prove $H=\langle b,c,d\rangle=G$. Since $b\notin T$,
a proper $H$ lies in a maximal subgroup not containing $T$: the only
subgroups containing the index-two group $T$ are $T$ and $G$.
The retained list and Lemma 3 would therefore put $H$ inside an
$S_4$ subgroup $S'$. Its intersection with $T$ is $A_4$. Both $b,c$
are odd involutions in $S'$, hence transpositions, and $|bc|=3$.

Relabel the four letters of $S'$ so that $b=(1\,2)$ and
$c=(2\,3)$. A distinct involution commuting with $b$ is either
$(3\,4)$ or $(1\,2)(3\,4)$. In the first case $|cd|=3$; in the
second $|cd|=4$. Thus the full group $G=\langle a,b,c,d\rangle$
would be a quotient of $[3,3,3]$ or $[3,3,4]$. Its order would divide
$120$ or $384$. This is impossible: the prime $p>5$ divides $|G|$
and divides neither number. Hence $H=G$, proving the first row.

## 6. The alternating local group

Let $p\equiv9,11\pmod{20}$. Since $p\equiv\pm1\pmod{10}$,
the retained theorem supplies $A\cong A_5$ inside $T$. Choose

$$a=(1\,2)(3\,4),\qquad b=(2\,4)(3\,5),\qquad
c=(1\,3)(2\,4)\tag{8}$$

under an isomorphism with $A_5$. These are distinct involutions with
$[a,c]=1$, $|ab|=5$ and $|bc|=3$. Their subgroup has order divisible
by $2,3,5$, and an index-two subgroup of $A_5$ is impossible because
$A_5$ is simple. They therefore generate $A$. This is the classical
hemi-dodecahedral marking, retained as a local map.

The product $ab$ is semisimple. Its centralizer is a cyclic torus of
order $p-1$ when $p\equiv1\pmod5$, and of order $p+1$ when
$p\equiv-1\pmod5$. To see the determinant condition explicitly, the
split torus is the group of eigenvalue ratios $\mathbf F_p^*$, on
which $\epsilon$ is the ratio modulo squares. The nonsplit torus is
$\mathbf F_{p^2}^*/\mathbf F_p^*$, acting by multiplication on the
two-dimensional space $\mathbf F_{p^2}$. Its determinant is the field
norm. The norm of a generator of $\mathbf F_{p^2}^*$ is a generator
of $\mathbf F_p^*$, so $\epsilon$ is onto in this case too.
Consequently the torus intersection with $T$ has exactly half its
order in either case.

The unique nonidentity element $d$ centralizing both $a,b$ is the
involution of this torus. Indeed, conjugation by $a$ inverts $ab$
and acts by inversion on the torus, so precisely its identity and
involution centralize $a$. If $p\equiv11\pmod{20}$, the order of
the torus intersection with $T$ is $(p-1)/2$, which is odd. If
$p\equiv9\pmod{20}$, that order is $(p+1)/2$, also odd. Thus
$d\notin T$ in both cases.

Now $\langle A,d\rangle$ is not contained in $T$. None of the
other proper maximal subgroups in the retained list contains $A_5$:
the affine and dihedral groups are soluble, and $S_4$ has smaller
order. Hence $\langle a,b,c,d\rangle=G$. The markers are distinct
because $d\notin T$ and $a,b,c\in T$, and (1) follows from the
choice of $d$.

Finally $H=\langle b,c,d\rangle$ is not contained in $T$. Lemma 3
excludes its containment in an affine or dihedral subgroup. If it
were contained in $S'\cong S_4$, then $S'\cap T$ would be $A_4$.
The involutions $b,c$ would both lie in its normal Klein four subgroup
and hence commute, contradicting $|bc|=3$. The maximal-subgroup list
therefore forces $H=G$, proving the second row. This completes the
proof of Theorem 1. $\square$

## 7. Attribution and verification

The conjecture, the use of local maps, the centralizer extension, and
the underlying special-linear matrix family come from [LT]. The
centralizer calculation is reused from [E] and has classical
antecedents. The additions in this paper are the prime progressions
selected by the determinant character, the extension of the normalized
matrix family to two general-linear configurations, and the complete
arguments forcing the opposite end to be the full group in the two
exceptional cases. The subgroup classification, finite Coxeter
presentations, quadratic-character formulas, and Dirichlet's theorem
remain explicitly retained inputs. These attributions distinguish the
new arguments of this project from claims of historical priority.

The author's GAP program constructs 16 actual marked groups, four in
each family, checks the distant commutations and generation, and
computes both end-group orders. An independent implementation constructs
17 examples using a different projective action, checks the complete
small $S_4$ case split, and verifies the two Coxeter presentation orders.
These calculations test the constructions; the written proofs above
supply the universal prime quantifiers.

The accompanying Lean file has eleven declarations. They verify the
matrix squares, determinants, anticommutations, adjacent products,
nonscalar marks and pairwise nonproportionality, together with the exact
lower-unipotent power formula, projective period and exhaustion of the
prime-field root group. All use standard Lean axioms only. They do not
formalize Lemma 2, the subgroup classification, the exceptional-group
arguments, Dirichlet's theorem, or the complete four-family theorem.
The runner checks the declared software versions and rejects altered
matrices, collapsed markings, and a false unipotent period statement.

The source ledger fixes the exact 2023 edition and each retained
interface. The independent review and its bounded priority search are
separate records. This manuscript supplies one answer to the single
four-family conjecture; the four cases do not count as four independent
question results or as four recovered historical papers. No compression
ratio is inferred from solving a question that the source posed.

## References

[E] *Dihedral centralizers and regular polytopes over a projective line*,
`phase230_rank_one_classification.md`, Theorem 5. Its exact frozen
manifest and supporting matrix certificate are bound in this packet.

[G] Michael Giudici, *Maximal subgroups of almost simple groups with
socle PSL(2,q)*, arXiv:math/0703685 (2007), Theorems 2.2 and 3.5.
<https://arxiv.org/abs/math/0703685>.

[LT] Dimitri Leemans and Micael Toledo, *Maniplexes with automorphism
group PSL(2,q)*, author manuscript dated May 15, 2023, Section 5,
physical and printed page 9. Journal reference: Discrete Mathematics
346 (2023), article 113527, DOI 10.1016/j.disc.2023.113527. The present
argument is bound to the author edition, not to an uncollated journal
text. <https://dipot.ulb.ac.be/dspace/bitstream/2013/359689/3/projectivemaniplexes_final.pdf>.
