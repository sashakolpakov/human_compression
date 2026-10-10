# Rank bounds for linear and unitary groups in dimension four

10 October 2026. This is a written corollary of the internally reviewed
[dimension-four bilinear-form alternative](phase8_psl4_rank6.md), §9.
The arguments below verify its hypotheses uniformly, including the
smallest odd field. They supply no rank-four construction for a unitary
group or an extension. Priority and external peer review remain
unverified.

## 1. Statements and exact scope

**Theorem A.** Let $q$ be an odd prime power. Each string C-group
representation of a group $G$ in either interval
\[
 \operatorname{PSL}_4(q)\le G\le\operatorname{PGL}_4(q),\qquad
 \operatorname{PSU}_4(q)\le G\le\operatorname{PGU}_4(q)
\]
has rank at most four. These are groups of linear projectivities; field
and graph automorphisms are outside the statement.

**Theorem B.** In either interval, an intermediate group of index four
over the simple socle has no involution generating set, and consequently
no string C-group representation of any rank. In particular this holds
for $\operatorname{PGL}_4(q)$ when $q\equiv1\pmod4$, and for
$\operatorname{PGU}_4(q)$ when $q\equiv3\pmod4$.

Combining A with the published existence results specified in §7 gives:

* $\operatorname{PSL}_4(q)$ has maximum rank four, as already obtained
  in phase eight.
* $\operatorname{PSU}_4(3)$ has no string C-group representation. This
  is an existing result, retained here rather than rederived.
* For every odd $q\ge5$, the rank spectrum of
  $\operatorname{PSU}_4(q)$ contains 3 and is contained in $\{3,4\}$.
  This note does not decide whether 4 belongs to that spectrum.
* The index-two extensions have the upper bound in A. No general
  existence assertion for them is made here.

## 2. A small monomial subgroup forbids a bilinear similarity form

Work over an algebraically closed field $k$ of characteristic $p$.
Let $m\ge3$, $p\nmid m$, and let $\zeta$ have order $m$. Put
\[
 D=\{\operatorname{diag}(\zeta^{a_1},\ldots,\zeta^{a_4}):
             a_i\in\mathbb Z/m,\ \sum_i a_i=0\},
 \qquad M=D\rtimes A_4,
\]
where $A_4$ acts by its determinant-one coordinate permutation matrices.

**Lemma 2.1.** The natural $M$-module is irreducible. No nonzero
bilinear form on it is preserved up to scalar by all of $M$.

**Proof.** The characters of $D$ are represented by exponent vectors
modulo $m$, with two vectors representing the same character precisely
when their difference is a constant vector. Indeed, testing on the
diagonal elements with exponents $a_r=1,a_s=-1$ proves necessity, and
the determinant-one condition proves sufficiency.

The four coordinate characters are distinct. The ten characters
$e_i+e_j$, $1\le i\le j\le4$, are also pairwise distinct. To check
this last assertion uniformly, subtract two different degree-two
exponent vectors. If their combined support uses at most three
coordinates, the difference has a zero coordinate and a nonzero
coordinate of absolute value at most two, so cannot be constant modulo
$m\ge3$. If their combined support uses all four coordinates, they
are two disjoint pairs; their difference has two entries 1 and two
entries $-1$, which cannot be congruent modulo $m\ge3$.
This includes $m=4$; no large-order assumption has been used.

Since $|D|=m^3$ is prime to $p$, a $D$-invariant subspace is a
sum of its distinct coordinate weight lines. The transitive group
$A_4$ leaves no proper nonempty set of those lines invariant, proving
irreducibility even over the algebraic closure.

Suppose a nonzero matrix $B$ satisfies $g^{\mathsf T}Bg=\mu(g)B$
for every $g\in M$. Its restriction to $D$ is a character, so all
nonzero entries of $B$ have the same degree-two weight. The preceding
separation shows that its support lies in one unordered pair: either
one diagonal position, or the positions $(i,j),(j,i)$. Thus
$\operatorname{rank}B\le2$. Its left radical is a nonzero proper
$M$-invariant subspace, contradicting irreducibility. ∎

**Lemma 2.2.** The projective centralizer of $M$ is trivial.

**Proof.** For each pair $i\ne j$, let $D_{ij}$ have diagonal entries
$\zeta,\zeta^{-1}$ in those positions and 1 elsewhere. Since $m\ge3$,
its eigenvalue 1 is uniquely of multiplicity two. If
$XD_{ij}X^{-1}=\lambda D_{ij}$, equality of the unique double
eigenvalues forces $\lambda=1$. Commuting with all $D_{ij}$ forces
$X$ to preserve each coordinate line, hence to be diagonal. If such an
$X$ commutes projectively with a coordinate 3-cycle, the scalar
commutator is 1 by inspecting its fixed coordinate. The 3-cycles then
force all diagonal entries of $X$ to be equal. Thus $[X]=1$. ∎

## 3. The unitary application

Use the Hermitian form $h(v,w)=\sum_i v_i^q w_i$ over
$\mathbb F_{q^2}$. The norm-one scalar group has order $m=q+1\ge4$.
The diagonal group $D$ from §2 and the even coordinate permutations
all lie in $\operatorname{SU}_4(q)$. Lemmas 2.1–2.2 show that its
natural action is absolutely irreducible, admits no nonzero bilinear
similarity form over the algebraic closure, and has trivial projective
centralizer. These properties therefore hold for every group containing
its projective image $S=\operatorname{PSU}_4(q)$.

The existing Hermitian form causes no contradiction: the phase-eight
obstruction produces an ordinary bilinear form, not a sesquilinear form.
Neither perfectness of $\operatorname{SU}_4(q)$ nor a multiplier
character calculation is needed here. In particular, $q=3$ is covered
by the same elementary argument with $m=4$.

## 4. The linear application, including q=3

Let $E_{ij}$ be a matrix unit with $i\ne j$. If a nonzero bilinear
form is preserved up to scalar by $u=I+E_{ij}\in\operatorname{SL}_4(q)$,
the multiplier is 1: $u^p=I$ and the only $p$-th root of unity in
characteristic $p$ is 1. The same holds for $u^{-1}=I-E_{ij}$.
Subtracting their two invariance equations and using odd characteristic
gives
\[
 E_{ji}B+B E_{ij}=0.
\]
For any fixed row $i$ and column $b$, choose $j\notin\{i,b\}$.
The $(j,b)$-entry of this equation is $B_{ib}=0$. Hence $B=0$,
a contradiction. This proves the required no-form statement for every
odd $q$, including $q=3$, where the determinant-one split diagonal
torus alone is too small for §2.

The natural action is absolutely irreducible: invariance under all
$I+E_{ij}$ implies invariance under all $E_{ij}$, which send any
nonzero coordinate of a vector to every other coordinate line. The
projective centralizer is trivial as well. If
$XuX^{-1}=\lambda u$, the eigenvalues of $u$ are all 1, so
$\lambda=1$. Commuting with all matrix units forces $X$ scalar.

## 5. Why a string diagram cannot disconnect

We use the standard simplicity of the natural groups
$\operatorname{PSL}_4(q)$ and $\operatorname{PSU}_4(q)$ for odd $q$.
Let $S$ denote this nonabelian simple normal subgroup of an
intermediate group $G$. Sections 3–4 give $C_G(S)=1$.

If adjacent string generators $\rho_i,\rho_{i+1}$ commute, every
generator to the left commutes with every generator to the right, by
the string relations. The intersection property gives
\[
 G=A\times B,\quad
 A=\langle\rho_0,\ldots,\rho_i\rangle,\quad
 B=\langle\rho_{i+1},\ldots,\rho_{r-1}\rangle.
\]
Both factors are nontrivial. Since they are normal, $A\cap S$ is
normal in $S$. If $A\cap S=1$, then
$[A,S]\le A\cap S=1$, contrary to $C_G(S)=1$. Otherwise $S\le A$,
and $B\le C_G(S)=1$, another contradiction. Thus every adjacent pair
is noncommuting.

Now $G\le\operatorname{PGL}_4(k)$ is finite, acts irreducibly, and
satisfies all the hypotheses of the phase-eight form alternative.
Rank at least five would give a nondegenerate bilinear similarity form,
contradicting §§3–4. This proves Theorem A.

## 6. The index-four obstruction

Every abelian quotient of an involution-generated group has exponent
at most two. Determinants give the cyclic quotients
\[
 \operatorname{PGL}_4(q)/\operatorname{PSL}_4(q)
     \cong \mathbb F_q^*/(\mathbb F_q^*)^4
     \cong C_{\gcd(4,q-1)},
\]
\[
 \operatorname{PGU}_4(q)/\operatorname{PSU}_4(q)
     \cong \mu_{q+1}/\mu_{q+1}^4
     \cong C_{\gcd(4,q+1)}.
\]
For completeness, define the projective unitary group here as the image
of the unitary isometry group $U_4(q)$ in $\operatorname{PGL}_4(q^2)$.
Its determinant is onto $\mu_{q+1}$, as witnessed by
$\operatorname{diag}(t,1,1,1)$; the kernel is $SU_4(q)$, and scalar
matrices have determinant $t^4$. This proves the second formula. A
unitary similitude can be rescaled to an isometry because the field norm
is onto, so this definition agrees with the projective similitude
convention. The first formula is the same determinant argument over
$\mathbb F_q$.

An intermediate quotient of order four is cyclic, not $C_2\times C_2$.
It therefore cannot be generated by images of involutions. This proves
Theorem B. These quotient obstructions are elementary; no novelty claim
is attached to them.

## 7. Primary sources, existence, and remaining questions

The source problem is **Problem 7**, §5.7 of Leemans,
[*String C-group representations of almost simple groups: a survey*](https://arxiv.org/abs/1910.08843),
version 2 (11 May 2020): determine maximal ranks for almost simple
groups with socle $\operatorname{PSL}_4(q)$. Theorem A addresses the
odd-field linear part of that question; it does not address field or
graph extensions, nor settle the existence question for every
index-two group. The same section's Conjecture 2 is the simple-group
maximum-four conjecture treated in phase eight.

Brooksbank–Leemans,
[*Polytopes of large rank for PSL(4,q)*](https://digitalcommons.bucknell.edu/fac_journ/1204/),
Journal of Algebra 452 (2016), 390–400, Theorem 1.1, supplies the retained
rank-four existence theorem for every odd $q$.

Leemans–Vandenschrick,
[*On simple groups that admit a string C-group representation*](https://dipot.ulb.ac.be/dspace/bitstream/2013/397490/3/simpleGroups6.pdf),
Theorem 1.1 and the accompanying introduction, supplies two distinct
facts used here: $\operatorname{PSU}_4(3)$ has no representation of any
rank; every $\operatorname{PSU}_4(q)$ with odd $q\ge5$ has a rank-three
representation. A group generated by one or two involutions is cyclic
or dihedral, so these nonabelian simple groups cannot have ranks one
or two. This justifies the spectrum statement in §1. The locally stored
author manuscript has placeholder journal dates; the repository lists
the article in 2026. We rely on the theorem text, not an inferred date
of priority.

The searches on 10 October 2026 included the explicit strings PSU4,
PSU(4,q), PGU4, PGL4, orthogonal minus six, and combinations with
string C-group, maximum rank and regular polytopes. The primary survey,
the above simple-group paper, the relevant section of Brooksbank's
[*On the ranks of string C-group representations for symplectic and orthogonal groups*](https://arxiv.org/abs/1912.05512),
and the authors' online polytope atlas were also inspected. The last
paper constructs high-rank orthogonal isometry subgroups, which should
not be identified with the simple even-dimensional derived groups.
No primary source establishing uniform rank-four existence for odd
$\operatorname{PSU}_4(q)$, or an existing identical upper-bound theorem,
was found in this bounded search. This is not a proof that those results
are unpublished. No named PSU4 maximum-rank conjecture was located in
the survey.

## 8. Verification boundary

The companion [checker](phase9_linear_unitary_check.py) verifies all
45 degree-two weight separations by integer witnesses of absolute
value one or two, including the disjoint-pair case; the six degree-one
separations; and the coordinate permutation facts. Those integer
witnesses are uniform for every $m\ge3$, rather than a finite-field
sample. It also checks the matrix-unit coefficient argument over the
integers and the small-modulus character tables as supplementary tests.
The logical proofs are given above. The checker does not independently
reprove the phase-eight normal-form classification, simplicity of the
socles, or the retained existence theorems. No new Lean formalization
is claimed here.
