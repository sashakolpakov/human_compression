# Pure subfield geometries and the mixed-center obstruction

10 October 2026. Proposed proofs, prepared privately for independent review.
The phase-seven files remain unchanged. This note concerns the literal
Constructions 10 and 11 and Theorem 5 of L110, Dimitri Leemans,
[*The residually weakly primitive pre-geometries of the Suzuki simple
groups*](https://ese-journals.unisalento.it/index.php/notemat/article/download/i15900932v20n1p1/995),
Note di Matematica 20 (2000/2001), 1–20.

The result has two parts. The standard pure-subfield family has a sharp
RWPRI criterion and is always a thick, residually connected,
flag-transitive geometry. The mixed group in Construction 10 has an
invariant-center obstruction: its prescribed intersections cannot be
maximal, for any of the source's admissible parameters. Bare embeddings
of its printed intersection pattern nevertheless exist.

These are statements about explicit subgroup families. No candidate
completeness claim from L110 or L114 is assumed.

## 1. Exact source scope and retained inputs

Write the odd field exponent as

\[
 n=\prod_{j=1}^{m}p_j^{f_j},\qquad p_i\ne p_j\ (i\ne j).
\]

Thus \(m\) counts distinct prime factors, whereas
\(\Omega(n)=\sum_j f_j\) counts factors with multiplicity.
Construction 10, printed p.18, specifies rank
\(3\le\alpha\le\min(m+1,\Omega(n))\), selects
\(k=\alpha-1\) pairwise nonisomorphic maximal Suzuki subfield
groups, puts \(a_i=n/\log_2(s_i)\), and sets
\(t=2^{n/\prod_i a_i}\). Its extra parabolic has type
\((E_q\widehat{\cdot}E_t):C_{t-1}\).
Construction 11 instead specifies \(2\le\alpha\le m-1\)
and selects \(\alpha\) pairwise nonisomorphic maximal Suzuki subfield
groups. Theorem 5 immediately below claims that Constructions 1–11
give all RWPRI pre-geometries of rank at least four.
The rank bound and the distinct-prime convention were checked in the
page image, not only its text extraction.

The source's definition on pp.4–5 is the exact condition used here:
for every proper subset \(J\) of the type set, at least one remaining
intersection \(G_{J\cup\{i\}}\) must be maximal in \(G_J\).
In particular, the condition applies to rank-one residues.
The hat-dot on p.5 means a nonsplit extension; \(E_q\) has order \(q\).
The introduction to the constructions on p.15 instructs the reader to
retain their whole intended intersection lattice, inferred from the
rank-four discussion. Construction 10 comes from the R12 discussion
on pp.14–15. Its intersections with the selected subfield groups
have type \((E_{s_i}\widehat{\cdot}E_t):C_{t-1}\).

We retain the following classical group theory.

1. The Suzuki realization inside \(\operatorname{Sp}_4\), with exceptional
   Steinberg endomorphism \(\rho\), \(\rho^2=\phi_2\), and compatible
   standard groups \(S_d=\operatorname{Sz}(2^d)=\mathbf H^{\rho^d}\)
   for positive odd \(d\). Here \(S_1=\operatorname{Sz}(2)\cong5:4\)
   is allowed as an intersection, although it is not simple.
2. Prime-relative-degree inclusions \(S_d<S_{ad}\), for odd prime
   \(a\) and \(d>1\), are maximal. Standard subfield intersections
   are given by the gcd of their exponents.
3. The Suzuki Sylow-2 group \(U_q\) has exponent four and its
   identity together with its involutions is \(Z_q=Z(U_q)\),
   elementary abelian of order \(q\). A nonidentity involution
   \(z\in Z_q\) has \(C_G(z)=U_q\). Consequently a normalizer
   of \(Z_q\) normalizes \(U_q\), while a normalizer of \(U_q\)
   normalizes its center: \(N_G(Z_q)=N_G(U_q)=B_q\), the
   ovoid point stabilizer \(U_q:H_q\), where \(H_q\cong C_{q-1}\).
4. Nonsplit torus normalizers have order \(4(q\pm\sqrt{2q}+1)\)
   and are maximal for \(q\ge8\). Odd-element centralizers and
   these normalizers have their usual Suzuki structure.
5. Schur–Zassenhaus complement conjugacy for the solvable group
   \(U_q:H_t\). This puts its subgroups of order \(t-1\) into the
   standard \(H_t\).
6. Lang–Steinberg surjectivity on the connected algebraic group
   \(\operatorname{Sp}_4\), as used in the proved finite-descent and
   coset-Helly statements of
   [phase7_suzuki_descent.md](phase7_suzuki_descent.md), Section 2.

The matrix action used in Section 4 is verified directly below. The
retained facts do not include any source classification of all RWPRI
lattices.

## 2. Sharp criterion for the canonical pure-subfield family

**Theorem A.** Let \(n\) be positive and odd. Select \(k\ge2\)
distinct prime divisors \(a_1,\ldots,a_k\) of \(n\), put

\[
 e=\frac{n}{\prod_{i=1}^k a_i},\qquad
 G=S_n,\qquad G_i=S_{n/a_i}.
\]

The standard coset incidence system
\(\Gamma(G;G_1,\ldots,G_k)\) is a thick, residually connected,
flag-transitive geometry. It is RWPRI **if and only if \(e>1\)**.
When \(e>1\), every one-step inclusion in its intersection lattice,
not only one inclusion at each subset, is maximal.

**Proof.** For \(J\subseteq\{1,\ldots,k\}\), set

\[
 n_J=\frac{n}{\prod_{j\in J}a_j}.
\]

Entrywise field intersection gives \(G_J=S_{n_J}\), including
\(G_\varnothing=G\). Apply phase-seven Theorem C with
\(F=\rho^e\) and \(m=\prod_i a_i\).
Any pairwise incident family of cosets has a common representative.
It therefore extends to a translate of the standard chamber.
This proves the geometry axiom and flag transitivity.

Suppose that a residue has at least two remaining types.
For distinct remaining \(i,j\), the two residue parabolics
\(S_{n_J/a_i}\) and \(S_{n_J/a_j}\) are distinct maximal
subgroups of \(S_{n_J}\): their exponents exceed one, even
if \(e=1\), because at least one other relative prime remains.
They generate \(S_{n_J}\). The standard coset-graph connectivity
criterion therefore proves that residue connected. Flag transitivity
identifies every residue with such a standard one, proving RC.

The panel of type \(i\) has
\([S_{ea_i}:S_e]\) chambers. This is at least three. Indeed,
\(S_{ea_i}\) is nonabelian simple and \(S_e\) is a proper
nontrivial subgroup, so its index cannot be two.
This includes \(e=1\), where \(|S_e|=20\). Thus the geometry
is thick.

If \(e>1\), each remaining exponent \(n_J/a_i\) is at least
\(e>1\). Every one-step inclusion is a prime-degree inclusion
of simple subfield groups, and hence maximal. This proves RWPRI.

If \(e=1\), the distinct primes \(a_i\), with \(k\ge2\),
include at least one \(a_i\ge5\). At the subset containing
every type except \(i\), the only remaining inclusion is

\[
 S_1<S_{a_i}.
\]

Let \(C_5\) be the normal subgroup of \(S_1=5:4\).
Inside \(S_{a_i}\), its centralizer is a nonsplit torus.
The order-four complement of \(S_1\) normalizes this centralizer,
so \(S_1\) lies inside the full torus normalizer. Its torus order
is one of \(2^{a_i}\pm2^{(a_i+1)/2}+1\), both of which exceed
five for \(a_i\ge5\). Hence this containment is strict, while
the torus normalizer is proper in \(S_{a_i}\). Consequently
\(S_1\) is not maximal, and RWPRI fails at that rank-one residue.
\(\square\)

The theorem concerns the standard simultaneous embeddings. It does
not assert that arbitrary conjugates of the same maximal-subgroup
types have the same intersections or are flag transitive.
If another family has a common prescribed simple subgroup \(S_e\)
with \(e>1\), however, the retained split-dihedral
normalizer/transporter argument in
[phase5_suzuki_higher.md](phase5_suzuki_higher.md), Section B,
forces simultaneous standard position after conjugating \(S_e\).
Thus within that prescribed common-subfield lattice there is only
one ambient conjugacy class for a fixed labelled selection of exponents.

## 3. Construction 11 and its omitted boundary

Construction 11 has \(k\le m-1\), so an unselected prime
remains in \(e\). In particular \(e>1\), and Theorem A supplies
canonical realizations for **every literal admissible parameter**.
It also answers the source's separate flag-transitivity question for
this family. It does not establish flag transitivity of all arbitrary
relative positions sharing only the maximal-parabolic isomorphism types.

The exact corrected parameter condition for the canonical pure-subfield
family is

\[
 2\le k\le m,\qquad \frac{n}{\prod_{i=1}^k a_i}>1.
\tag{1}
\]

For squarefree \(n\), this recovers \(k\le m-1\).
If any prime factor of \(n\) is repeated, it also permits \(k=m\).
The source's bound omits this latter boundary.

For example take

\[
 n=3^2\cdot5\cdot7\cdot11=3465,\qquad
 (a_1,a_2,a_3,a_4)=(3,5,7,11).
\]

Then

\[
 (G_1,G_2,G_3,G_4)
 =(S_{1155},S_{693},S_{495},S_{315}),\qquad
 G_{1234}=S_3=\operatorname{Sz}(8).
\]

Theorem A proves this is a rank-four thick, RC, FT, RWPRI
geometry, without enumerating its enormous ambient group.
Here \(m=4\), whereas Construction 11 allows only ranks two and
three. Constructions 1–10 each have at least one soluble maximal
parabolic, while all four parabolics here are nonabelian simple.
Consequently this stated-action subgroup family is absent from all
eleven literal constructions.

This contradicts the **literal exhaustive list** in Theorem 5,
as a theorem about the subgroup systems specified in the paper.
It is a boundary omission, distinct from proving that no natural
extension of the constructions could produce the example:
allowing appropriate truncations of larger constructions or replacing
Construction 11's bound by (1) would include it. The statement does
not classify all unlabelled geometries or all possible actions of \(G\).

## 4. A scalar-center normal form

Here \(n\) and \(e\) are odd, \(e\mid n\), \(e>1\),
\(q=2^n\), and \(t=2^e\).
Use standard Suzuki unipotents \(U(a,b)\), with
\(Z_q=\{U(0,b):b\in\mathbb F_q\}\), and diagonal matrices

\[
 h(\lambda)=
 \operatorname{diag}(\lambda^{\theta+1},\lambda,
                     \lambda^{-1},\lambda^{-\theta-1}),
 \qquad \theta=2^{(n+1)/2}.
\]

Multiplying these diagonal and unipotent matrices gives

\[
 h(\lambda)^{-1}U(a,b)h(\lambda)
 =U(\lambda^\theta a,\lambda^{\theta+2}b).
\tag{2}
\]

Both exponents are coprime to \(q-1\). For \(\theta+2\),
if an odd divisor \(c\) divided both \(q-1\) and
\(2^{(n-1)/2}+1\), squaring the latter congruence would give
\(2^{n-1}\equiv1\pmod c\), whereas \(2^n\equiv1\pmod c\);
thus \(2\equiv1\pmod c\), forcing \(c=1\).
Since \(\theta+2=2(2^{(n-1)/2}+1)\), the claim follows.
In particular the standard \(H_t\) acts on both the first
unipotent parameter and the center by all nonzero scalars in
\(\mathbb F_t\). Any additive invariant subgroup is therefore
an \(\mathbb F_t\)-subspace.

**Lemma B: normal form.** Every subgroup \(Q\le S_n\) of
type \((E_q\widehat{\cdot}E_t):C_{t-1}\) is ambient-conjugate
to

\[
 Q_0=Z_qU_tH_t.
\tag{3}
\]

**Proof.** Its normal Sylow-2 subgroup \(P\) has order \(qt\)
and contains the elementary abelian kernel of order \(q\).
Place \(P\) inside an ambient \(U_q\). All its involutions lie
in \(Z_q\), so that elementary abelian kernel must equal
\(Z_q\). Moreover \(Z_q\) is exactly the identity together
with the involutions of \(P\); it is characteristic in \(P\)
and normal in \(Q\). Therefore \(Q\le N_G(Z_q)=B_q\).

Project to \(B_q/U_q=H_q\). The odd complement of \(Q\)
maps isomorphically to the unique subgroup of order \(t-1\),
namely \(H_t\). Complement conjugacy in \(U_q:H_t\)
allows an ambient \(U_q\)-conjugation putting it equal to \(H_t\).
Now \(P/Z_q\) is an additive subgroup \(W\) of the first
unipotent parameter, of order \(t\), normalized by \(H_t\).
By (2), \(W=v\mathbb F_t\) for some nonzero \(v\).
A diagonal conjugation, which centralizes \(H_t\), scales this
line to \(\mathbb F_t\). Because \(P\) contains the full
center, it is the full preimage of that line in \(U_q\);
thus \(P=Z_qU_t\). This proves (3). \(\square\)

**Lemma C: exact maximality test.** Suppose \(H<Q_0\)
has odd part \(t-1\) and a normal Sylow-2 subgroup which is
not elementary abelian. Then \(H\) surjects onto
\(Q_0/Z_q\). Put \(W=H\cap Z_q\), regarded as an
\(\mathbb F_t\)-subspace of \(\mathbb F_q\).
The overgroups of \(H\) in \(Q_0\) correspond exactly to
the \(\mathbb F_t\)-subspaces containing \(W\), by

\[
 V\longmapsto Z_VH,\qquad
 L\longmapsto L\cap Z_q.
\tag{4}
\]

In particular, \(H\) is maximal in \(Q_0\) exactly when
\(\dim_{\mathbb F_t}(\mathbb F_q/W)=1\).

**Proof.** A non-elementary Sylow-2 subgroup inside \(U_q\)
contains an element of order four. Its image modulo \(Z_q\)
is nonzero, so the image of \(H\) in \(Q_0/Z_q\) has a
nonzero normal additive subgroup. The odd projection has full
order \(t-1\) and acts irreducibly on the one-dimensional
\(\mathbb F_t\)-space \(U_t/Z_t\).
It follows that the image contains all this additive group,
and therefore equals \(Q_0/Z_q\).

Thus \(Q_0=Z_qH\). The action of \(H\) on \(Z_q\)
is exactly the scalar action of \(H_t\), so \(W\) and
every center intersection \(L\cap Z_q\) are
\(\mathbb F_t\)-subspaces. Conversely such a subspace \(V\)
is normalized by \(H\), making \(Z_VH\) a subgroup.
Writing every element as \(zh\) proves
\(L=(L\cap Z_q)H\). This gives (4), with the stated
maximality criterion. \(\square\)

This is an overgroup classification inside the specified mixed
parabolic. It reduces maximality to one scalar-module dimension;
no ambient Suzuki group enumeration or search over relative
positions is required.

## 5. Uniform obstruction for Construction 10

**Theorem D.** For every parameter allowed by Construction 10,
the intended bare subgroup-intersection lattice has a canonical
embedding. No embedding having its prescribed mixed parabolic
and pairwise mixed intersections is RWPRI.

**Proof.** Put \(k=\alpha-1\ge2\), select distinct odd
relative primes \(a_i\), and set

\[
 P=\prod_i a_i,\quad n=eP,\quad
 t=2^e,\quad q=2^n,\quad s_i=2^{n/a_i}.
\]

The source's bound \(\alpha\le\Omega(n)\) gives
\(\Omega(e)=\Omega(n)-k\ge1\), hence \(e>1\).
Choose canonical subfield groups \(G_i=S_{n/a_i}\)
and \(Q=Z_qU_tH_t\). For every selection \(J\) of
subfield types,

\[
 \bigcap_{j\in J}G_j=S_{n_J},\qquad
 Q\cap\bigcap_{j\in J}G_j=Z_{2^{n_J}}U_tH_t.
\tag{5}
\]

These are exactly the intended field intersections and
mixed-extension orders, including common Borel \(U_tH_t\).
The extension \(Z_{2^{n_J}}U_t\) by its elementary abelian
center kernel is nonsplit: every element outside that center
has order four, so a nontrivial elementary abelian complement
could not exist. Thus (5) also has the literal hat-dot type.
This proves bare existence.

For any other proposed embedding, Lemma B puts its mixed
parabolic into \(Q_0\). Its pairwise intersections \(H_i\)
have the prescribed type
\((E_{s_i}\widehat{\cdot}E_t):C_{t-1}\).
Their Sylow-2 groups cannot be elementary abelian: an
extension of elementary abelian groups whose total group is
elementary abelian splits as a vector-space extension.
Lemma C therefore applies, and order division gives
\[
 |H_i\cap Z_q|=s_i,\qquad
 \dim_{\mathbb F_t}(\mathbb F_q/(H_i\cap Z_q))
 =P-P/a_i.
\]

Since \(k\ge2\) and every \(a_i\ge3\), this dimension exceeds
one. Every \(H_i\) is therefore nonmaximal in \(Q_0\).
Explicitly, extend \(H_i\cap Z_q\) by one
\(\mathbb F_t\)-dimension; (4) gives a proper intermediate
subgroup. Taking the source's RWPRI subset \(J\) consisting
only of the mixed type leaves no maximal remaining
intersection. This contradicts RWPRI. \(\square\)

The negative conclusion uses only the mixed parabolic and the
specified pairwise intersection types. It does not require
simultaneous alignment of a common simple subfield.
It strengthens the earlier rank-three R12 argument in
[phase5_suzuki_higher.md](phase5_suzuki_higher.md), Section C.
It does not prove that arbitrary choices of the listed maximal
parabolic types, with different intersections, cannot satisfy RWPRI.
Nor does failure of RWPRI imply failure of the geometry or FT axioms.

## 6. Scope and proposed correction

| Exact target | Bare embedding | RWPRI | Geometry, thickness, RC, FT |
|---|---|---|---|
| Every literal Construction 11 parameter, canonical position | Yes | Yes | Yes |
| Canonical pure-subfield family with all distinct relative primes selected and repeated factors in \(n\) | Yes | Yes | Yes |
| Canonical pure-subfield family with bottom exponent \(e=1\), rank at least two | Yes | No | Yes |
| Every intended Construction 10 lattice | Yes | No | Not asserted here |

The all-simple rank-four example supplies a further precise omission
from L110's literal exhaustive list; the Construction 10 argument
supplies a uniform maximality obstruction to that intended family.
Neither result is a full replacement classification of the paper's
remaining relative positions or incidence isomorphism classes.
The work makes no priority claim, and internal review is not external
peer review.

The reusable ingredients are the same ones already isolated in the
workspace: Lang descent gives a common-point theorem for subfield
cosets, and a scalar-module overgroup lattice converts maximality
into an exact dimension condition. The new step is their complete
application to the two source constructions and to the omitted
pure-subfield boundary.

## 7. Exact checks and review boundary

The standard-library script
[phase8_suzuki_subfields_check.py](phase8_suzuki_subfields_check.py)
uses the irreducible polynomial \(x^9+x^4+1\) to construct
\(\mathbb F_{512}\), verifying irreducibility by the Rabin criterion.
It independently builds \(Q=Z_{512}U_8H_8\), of order 28,672,
and \(H=U_8H_8\), of order 448, by closure of explicit generators
in unipotent/diagonal coordinates. It verifies the diagonal-action
formula in actual four-by-four matrices for all 28,672 parameter
triples, the unipotent multiplication law on \(U_8\) for all 4,096
pairs, and another 16,384 products involving four generating
unipotents, including two central parameters outside \(\mathbb F_8\).

The field calculation lists all eleven \(\mathbb F_8\)-subspaces
of \(\mathbb F_{512}\) containing \(\mathbb F_8\): the original
line, nine planes, and the whole space. Independent group closures
verify that all nine planes yield distinct proper intermediate
subgroups, each of order 3,584, between \(H\) and \(Q\).
The assertion that these are *all* overgroups uses Lemma C,
rather than an independent enumeration of every subgroup of \(Q\).

The script also checks the sixteen exact intersection exponents of
the \(n=3465\) rank-four example, ten small prime-degree torus
normalizer boundaries containing \(S_1\), and the scalar
coprimality identity through odd degree 999. It does not instantiate
the field \(\mathbb F_{2^{3465}}\), enumerate its Suzuki group,
or replace the uniform proofs with finite testing.

The root reviewer and rank_stability independently read the complete
mathematical argument and found no gap under the retained classical
inputs. The latter also read the primary source page images 4, 5,
14, 15 and 18, confirming the RWPRI axiom, distinct-prime convention,
mixed intersection types, and literal Construction 11 rank bound.
These are internal reviews. No external review or priority conclusion
is claimed. The new results have not been formalized in Lean;
they use the earlier written Lang-descent theorem and the exact
finite checks with the separate scopes described above.
