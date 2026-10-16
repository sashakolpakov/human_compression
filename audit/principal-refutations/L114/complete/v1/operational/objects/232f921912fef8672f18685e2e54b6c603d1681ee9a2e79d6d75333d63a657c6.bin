# A missing Suzuki rank-three lattice and its rank-four extension

10 October 2026. Exact computational witnesses, with a proof of every
subgroup-lattice RWPRI condition. The source's classical Suzuki subgroup
theory is retained. The rank-three example is also firm, residually
connected, and flag-transitive, by the short factorization argument below.

## 1. Result and exact source scope

In \(G=\operatorname{Sz}(2^{15})\), there are subgroups

\[
S=\operatorname{Sz}(8),\qquad T=\operatorname{Sz}(32),\qquad
K=C_{533}:C_4
\]

whose complete proper intersection lattice has orders

| Intersection | Group | Order |
|---|---|---:|
| \(S\cap T\) | \(\operatorname{Sz}(2)=C_5:C_4\) | 20 |
| \(S\cap K\) | \(C_{13}:C_4\) | 52 |
| \(T\cap K\) | \(C_{41}:C_4\) | 164 |
| \(S\cap T\cap K\) | \(C_4\) | 4 |

Every proper subset of the three labels admits a maximal-subgroup step.
Consequently this is a rank-three RWPRI geometry in the precise sense of
L114, Leemans, [*The rank 3 geometries of the simple Suzuki groups
Sz(q)*](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v19n1p43/837),
Note di Matematica 19 (1999), 43–63.

This lattice is absent from the asserted exhaustive list in its Theorem 5.5.
Here \(15=3\cdot5\), so the sum of prime exponents is two. Only shapes 1–5
apply. Among those, only shape 5 has two Suzuki maximal parabolics and an
odd cyclic group extended by \(C_4\). It prescribes the intersection of the
two Suzuki parabolics as \(C_4\times C_2\), of order eight. Our intersection
has order twenty. Permuting labels cannot remove the discrepancy.

The contradiction to the source list does not require flag transitivity.
The introduction on p.44 explicitly studies RWPRI geometries whether
flag-transitive or not. The definition on p.46 is the subgroup-lattice
condition used below. Lemma 2.1 on p.45 says every rank-three coset
pregeometry is a geometry. The terminology on p.47 excludes the nonsimple
\(\operatorname{Sz}(2)\) from being *of Suzuki type*; it does not prohibit
that group as an intersection. Shape 8 is in the separate branch where
the sum of prime exponents exceeds two, so allowing its base parameter
to equal two would not insert our example into the applicable branch.

The same matrix algebra gives a rank-four RWPRI pregeometry in
\(\operatorname{Sz}(2^{105})\), with maximal parabolics

\[
\operatorname{Sz}(2^{35}),\quad \operatorname{Sz}(2^{21}),\quad
\operatorname{Sz}(2^{15}),\quad C_{60229}:C_4,
\qquad 60229=13\cdot41\cdot113.
\]

It realizes the maximal-parabolic types in Construction 6 of L110,
[*The residually weakly primitive pre-geometries of the Suzuki simple
groups*](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v20n1p1/995),
Note di Matematica 20 (2000/2001), pp.17–18, using prime field degrees
3, 5, 7 and torus primes 13, 41, 113. Thus it is **not** claimed to be
outside that list of parabolic types. Its lower lattice differs from the
purported rank-three shape used in the preceding discussion. This
distinction is essential: a construction specifying only parabolic
isomorphism types is weaker than a prescribed intersection lattice.
L110's Theorem 3 also repeats the rank-three completeness assertion and
the order-eight meet as shape R8; the same counterexample applies there.

These are proposed corrections supported by explicit exact witnesses and
independent internal review. Establishing publication priority or a fully
corrected classification would require further work.

## 2. Retained facts, and what the computation proves

Use the standard four-dimensional matrix model of
Bray–Bäärnhielm, [*A new method for recognising Suzuki
groups*](https://arxiv.org/abs/1706.05697), equations (1)–(5).
Write \(q=2^n\), \(n\) odd, and \(\theta=2^{(n+1)/2}\). Set

\[
U(a,b)=
\begin{pmatrix}
1&0&0&0\\
a&1&0&0\\
a^{\theta+1}+b&a^\theta&1&0\\
a^{\theta+2}+ab+b^\theta&b&a&1
\end{pmatrix},
\quad
h(\lambda)=\operatorname{diag}
(\lambda^{\theta+1},\lambda,\lambda^{-1},\lambda^{-\theta-1}),
\]

and let \(w\) be the antidiagonal identity matrix. The Bruhat decomposition is

\[
\operatorname{Sz}(q)=UH\ \sqcup\ UH wU.
\]

We retain the following classical facts, used also in the source.

1. Restriction to \(\mathbb F_{2^d}\), for odd \(d\mid n\), gives the
   standard subfield subgroup. It is maximal when \(n/d\) is prime and
   \(d>1\).
2. The normalizers of the nonsplit cyclic tori of orders
   \(q+\sqrt{2q}+1\) and \(q-\sqrt{2q}+1\) have order four times the
   torus order, and are maximal in the simple Suzuki group.
3. The standard order-20 subgroup over \(\mathbb F_2\) is
   \(\operatorname{Sz}(2)=C_5:C_4\).

No enumeration of the ambient groups, no SmallGroups or maximal-subgroup
database, and no assumed completeness of L114 are used by the checker.
Its group membership test comes directly from the displayed Bruhat
decomposition. The subgroup maximality conclusions retain items 1–2.

For completeness, coefficient-field intersections are exact. On
\(\mathbb F_{2^d}\), the ambient Suzuki automorphism restricts to
\(x\mapsto x^{2^{(d+1)/2}}\), since \(n/d\) is odd. Bruhat parameters are
uniquely recovered from matrix entries, so

\[
\operatorname{Sz}(2^a)\cap\operatorname{Sz}(2^b)
=\operatorname{Sz}(2^{\gcd(a,b)})
\]

for standard embedded subgroups, including gcd equal to one.

## 3. A single binary algebra supplies the simultaneous torus

The binary matrices

\[
M=\begin{pmatrix}
1&1&1&0\\0&0&1&1\\0&1&1&1\\1&0&0&0
\end{pmatrix},
\qquad
r=\begin{pmatrix}
1&0&0&0\\1&1&0&0\\1&1&1&0\\1&0&1&1
\end{pmatrix}=U(1,0)
\]

satisfy

\[
M^4+M+I=0,\qquad |M|=15,\qquad |r|=4,\qquad r^{-1}Mr=M^2.
\]

The polynomial \(X^4+X+1\) is irreducible over \(\mathbb F_2\):
it has no binary root and is not divisible by the sole irreducible binary
quadratic \(X^2+X+1\). Thus \(\mathbb F_2[M]\cong\mathbb F_{16}\).
For odd \(n\), its scalar extension to \(\mathbb F_{2^n}\) is again a
field, since \(\gcd(4,n)=1\).

The checker initially discovers \(M\) by searching within the 28,672-matrix
open Bruhat cell of \(\operatorname{Sz}(8)\) for an order-13 element whose cyclic torus is
stable under both binary Frobenius and conjugation by \(r\).
It solves \(Xa=aX\), with binary unknown entries of \(X\), and finds a
four-dimensional binary kernel. The displayed \(M\) is a primitive
element of that algebra. This search explains the construction; the
subsequent exact matrix identities are the certificate.

In
\[
F=\mathbb F_2[z]/(z^{15}+z+1),
\]
the certificate records scalars \(\lambda_8\in\mathbb F_8\) and
\(\lambda_{32}\in\mathbb F_{32}\), and constructs

\[
a=(M+\lambda_8I)^{(8^4-1)/13},\qquad
b=(M+\lambda_{32}I)^{(32^4-1)/41}.
\]

Their exact entries and scalar encodings are in
[the JSON certificate](phase6_suzuki_torus_check.json). Integers encode
binary polynomial coefficients, not residues modulo an integer.
The checker verifies \(a,b\in\operatorname{Sz}(2^{15})\),
\(|a|=13\), \(|b|=41\), that \(a\) has coefficients in \(\mathbb F_8\),
and that \(b\) has coefficients in \(\mathbb F_{32}\).
They commute because both are polynomials in \(M\).

Put \(c=ab\). Then \(|c|=533\), and exact multiplication gives

\[
r^{-1}cr=c^{278},\qquad
278^2\equiv-1\pmod{533}.
\]

Hence \(K=\langle c,r\rangle=C_{533}:C_4\) has order 2132.
This is a cyclic-by-four subgroup of an ambient torus normalizer;
it is not the full normalizer of \(C_{533}\) in \(G\).
The certificate's “normalizer_order” field records this constructed \(K\).
The checker also constructs every element of \(K\) by closure and tests
all 2132 individually for membership in the standard Suzuki group.
Testing their coefficients under the appropriate Frobenius maps gives

\[
|K\cap\operatorname{Sz}(8)|=52,\qquad
|K\cap\operatorname{Sz}(32)|=164.
\]

It verifies that these intersections are exactly \(\langle a,r\rangle\)
and \(\langle b,r\rangle\), respectively. It separately closes
\(\langle U(1,0),w\rangle\) to obtain all twenty elements of
\(\operatorname{Sz}(2)\), and checks that its intersection with \(K\)
is precisely \(\langle r\rangle\).

The simultaneous position matters. Merely knowing that 13 and 41 divide
the ambient torus order \(32513=13\cdot41\cdot61\) would not establish
the claimed intersections with two particular subfield groups.
The common binary algebra supplies exactly that missing compatibility.

## 4. Every rank-three RWPRI condition

For labels \(S,T,K\), write \(G_J\) for their intersection, and
\(G_\varnothing=G\). The source condition is: for each proper label
subset \(J\), some unused label \(i\) has
\(G_{J\cup\{i\}}\) maximal in \(G_J\).

The seven checks are as follows.

| \(J\) | A maximal next intersection | Reason |
|---|---|---|
| \(\varnothing\) | \(S<G\) | prime subfield index in the field degrees: \(15/3=5\) |
| \(\{S\}\) | \(S\cap K<S\) | full order-13 torus normalizer in \(\operatorname{Sz}(8)\) |
| \(\{T\}\) | \(T\cap K<T\) | full order-41 torus normalizer in \(\operatorname{Sz}(32)\) |
| \(\{K\}\) | \(K\cap S<K\) | subgroup index 41 |
| \(\{S,T\}\) | \(\langle r\rangle<\operatorname{Sz}(2)\) | subgroup index 5 |
| \(\{S,K\}\) | \(\langle r\rangle<C_{13}:C_4\) | subgroup index 13 |
| \(\{T,K\}\) | \(\langle r\rangle<C_{41}:C_4\) | subgroup index 41 |

All the indices described as subgroup indices are prime; the first row
uses the retained subfield maximality theorem, not a claim that the
group index equals five. Distinct intersection orders, and distinct
simple parabolic orders, also make all eight vertices of the
intersection lattice distinct.

This proves the source's RWPRI property. Its Lemma 2.1 gives the geometry
axiom in rank three. In fact a product identity proves a stronger result.

**A factorization criterion.** For any three subgroups \(A,B,C\) of a
group, if \(A=(A\cap B)(A\cap C)\), their coset geometry is
flag-transitive. To see this, translate a triple flag so its \(A\)-coset
is \(A\). Write its other cosets as \(bB,cC\), with \(b,c\in A\).
Factor \(b^{-1}c=xy\), where \(x\in A\cap B\) and \(y\in A\cap C\).
Then \(bx=cy^{-1}\) belongs to all three cosets. Thus every chamber has a
common group element and is a translate of the standard chamber.
This is precisely the typed coset-Helly criterion.

Here the product set \((K\cap S)(K\cap T)\) has size
\(52\cdot164/4=2132=|K|\), so equals \(K\). The criterion applies.
This uses the general product-set cardinality formula, not an assumption
that an arbitrary product of subgroups is itself a subgroup.

Flag transitivity identifies every residue with a standard coset residue.
Its incidence graph is connected when the corresponding subgroups
generate. The two subgroups \(S\cap T\) and \(S\cap K\) generate \(S\):
the latter is maximal and the former has an element of order five,
which the latter does not. The same argument gives generation of \(T\).
The factorization gives generation of \(K\). Finally \(S,T\) generate
the ambient \(G\), since \(S\) is maximal and \(T\not\le S\);
for example, 31 divides \(|T|\) but not \(|S|\).
Hence the geometry is residually connected, including its global
incidence graph. Its panels have sizes \(5,13,41\), so it is firm
(indeed thick). No geometric intersection-property axiom is claimed.

There is a visible point in the source case analysis worth revisiting:
the argument for Residue 7 on p.57 discards a pair of cyclic-by-four subgroups
by asserting that their generated group is the whole ambient Suzuki
group. In the present configuration the corresponding
\(C_5:C_4\) and \(C_{41}:C_4\), of orders twenty and 164, generate the
proper subfield group \(\operatorname{Sz}(32)\). The first of these
need not be the full normalizer of its \(C_5\) in that subfield group.
The certificate establishes the counterexample
without depending on a reconstruction of every step of that argument.

## 5. Rank four without enumerating a huge group

Use the same binary \(M,r\) in a polynomial model of
\(\mathbb F_{2^{105}}\). The certificate verifies irreducibility of its
modulus by Rabin's criterion. For degrees \(d=3,5,7\), it solves the
binary linear equations \(x^{2^d}=x\) to obtain the exact embedded
subfields, then constructs matrices \(a_3,a_5,a_7\), polynomials in \(M\),
with orders 13, 41, 113. Each is checked for Suzuki membership and
coefficient-field membership. The three commute. Their product has
order \(60229\); conjugation by \(r\) is a fourth-order power automorphism
whose square is inversion. Consequently

\[
K=\langle a_3,a_5,a_7,r\rangle=C_{60229}:C_4.
\]

For \(i\in\{3,5,7\}\), let
\(S_i=\operatorname{Sz}(2^{105/i})\).
If \(J\subseteq\{3,5,7\}\), put
\(d_J=105/\prod_{i\in J}i\) and
\(m_J=\prod_{i\notin J}\ell_i\), where
\((\ell_3,\ell_5,\ell_7)=(13,41,113)\).
Then the full intersection formulas are

\[
\bigcap_{i\in J}S_i=\operatorname{Sz}(2^{d_J}),
\qquad
K\cap\bigcap_{i\in J}S_i=C_{m_J}:C_4.
\]

The cyclic-factor intersection argument needs no unchecked assumption
about Frobenius preserving a chosen torus. If a product of commuting
elements of distinct prime orders lies in a subfield group, an integer
power isolates each nontrivial prime component. That whole prime
subgroup must therefore lie in the same subfield group. The checker
tests whether each generator is fixed under \(2^{d_J}\)-Frobenius for
all eight subsets \(J\). Since \(r\) is binary, multiplication by
\(r^j\) preserves membership in every standard subfield subgroup.
These observations prove the displayed formulas from the recorded
generator tests.

RWPRI follows uniformly. Before \(K\) is selected, if at least two field
primes remain, select another \(S_i\): this is a maximal proper simple
subfield step. If exactly one remains, select \(K\): the resulting
subgroup is a full nonsplit torus normalizer in \(\operatorname{Sz}(8)\),
\(\operatorname{Sz}(32)\), or \(\operatorname{Sz}(128)\).
Their torus orders 13, 41, 113 are prime. If none remains, the current
group is \(\operatorname{Sz}(2)\), and selecting \(K\) gives its index-five
\(C_4\). Once \(K\) is selected, selecting any remaining \(S_i\)
removes precisely the factor \(\ell_i\), so gives a prime-index subgroup.
This covers all fifteen proper label subsets.

The all-Suzuki intersection has order twenty, and intersecting also with
\(K\) leaves order four. For example, the residue inside
\(S_7=\operatorname{Sz}(2^{15})\) is exactly the preceding rank-three
example. This explains why the source's intended order-eight lower
intersection cannot be used to reject Construction 6 merely from its
parabolic types. The rank-four geometry axiom and flag transitivity
remain untested here.

## 6. Reproduction, evidence, and boundaries

Run, from this directory,

    python3 phase6_suzuki_torus_check.py

The script uses the Python standard library and two hash-bound arithmetic
modules already present in the repository:
[phase5_suzuki_check.py](phase5_suzuki_check.py) and
[phase5_suzuki_higher_check.py](phase5_suzuki_higher_check.py).
It saves the exact matrices, field moduli, subgroup intersection counts,
all eight rank-four intersection rows, and dependency hashes in
[phase6_suzuki_torus_check.json](phase6_suzuki_torus_check.json).
The run log is [phase6_suzuki_torus_check.log](phase6_suzuki_torus_check.log).
An independently executed and mathematically reviewed copy is documented
in [the separate audit](phase6_suzuki_counterexample_audit.md) and
[its run record](phase6_suzuki_counterexample_audit_run.json).

The executable checks are exact finite arithmetic. The proof that the
listed subgroups are maximal uses classical Suzuki group theory. The
source-hypothesis comparison and the RWPRI/Helly arguments are mathematical
review. The generic factorization-to-common-coset-point implication is
separately formalized in
[RankThreeFactorization.lean](formal/RankThreeFactorization.lean), with
[its fresh check report](formal/RankThreeFactorization.check.json) and
[exact scope](formal/RankThreeFactorization.scope.md).
That theorem does not encode the finite fields, the Suzuki subgroup facts,
or this specific group configuration; those remain the exact computation
and paper argument above.

The four impossibility proofs and the positive constructions for the
*printed* L114 lattices in the immutable phase-five notes remain separate
per-shape statements. Their earlier retained assumption that the printed
list was exhaustive must now be withdrawn. This example does not provide
an exhaustive replacement list, an embedding-orbit classification, a
classification of all acting groups. The rank-four example's flag
transitivity remains unproved.
Later corrections and independent publication priority have not been
exhaustively investigated.
