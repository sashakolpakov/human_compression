# Older problems: source intake and a semilinear descent theorem

Audit date: 9 October 2026. This pass concerns papers published in 2006 or
earlier. A historical question is not automatically a currently open problem.
The new argument below is a proposed solution of a precisely delimited
mathematical statement; publication priority and external review are separate.
No source full text is intended for the public export.

## 1. The 2003 spread-space question

**Source.** F. Buekenhout, P.-O. Dehaye and D. Leemans, *RWPRI and
(2T)1 flag-transitive linear spaces*, Beiträge zur Algebra und Geometrie
44 (2003), 25–46. The question is in §5.1.2, printed p.39, immediately
after Proposition 5.5; Theorem 6.1(1) and its footnote 11 retain this
unclassified possibility. [Primary PDF](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.44/no.1/b44h1bue.pdf).
Local primary text: `sources/older_L102_gwdg.txt`.

The question asks whether every flag-transitive RWPRI linear space of
spread type in the **one-dimensional affine semilinear case** is
Desarguesian. This context is essential. The same paper includes Hering
spaces outside that case; the unqualified statement about all spread
spaces is not what is proved here.

The relevant source material was read beyond the question: definitions in
§2.2; the affine reduction in Proposition 5.2; §§5.1–5.3; and the
remaining case in Theorem 6.1. In rank two, the RWPRI condition here is
equivalent to local primitivity on both kinds of residue. The spread
description gives the following concrete formulation.

Let F=F_(p^d), regarded as an additive vector space over F_p. Let S be a
spread of l-dimensional F_p-subspaces, with 0<l<d: its nonzero members
partition F minus {0}. Form a linear space whose points are F and whose
lines are all additive translates of members of S. Suppose H≤ΓL1(F)
acts transitively and primitively on S and, for each U∈S, H_U acts
irreducibly on U over F_p. These are precisely the two local
primitivity conditions for the affine group T⋊H, where T is the full
translation group. The proposed answer is that S is the Desarguesian
spread consisting of the one-dimensional F_(p^l)-subspaces of F.

### Theorem A: rigidity of locally primitive semilinear spreads

Under the hypotheses just stated, S is Desarguesian. Consequently the
associated linear space is AG(d/l,p^l). In particular this answers the
mathematical question in §5.1.2, subject to the separate review and
priority boundaries below.

The proof has three short ingredients. The prime-degree observation
also recovers the relevant direction of the source's Proposition 5.1;
the arithmetic argument recovers Proposition 5.4 in the prime case
without a general exponential Diophantine theorem.

**Lemma A1 (metacyclic primitive actions).** A finite primitive
permutation group with a cyclic normal subgroup and cyclic quotient
has prime degree, provided the degree is greater than one.

Indeed the normal cyclic subgroup either fixes every point or is
transitive. In the first case the induced group is cyclic, and a
primitive regular cyclic group has prime order. In the second case
its faithful image is cyclic and regular. Any proper nontrivial
characteristic subgroup would have a nontrivial block system preserved
by the full group. A cyclic group of composite order has such a
subgroup, so its order, equal to the degree, is prime. This reasoning
allows nonfaithful actions before taking the induced permutation group.

Apply this to H on S: the normal scalar subgroup H∩F* is cyclic and
H/(H∩F*) is a subgroup of the cyclic Galois group of F/F_p. Thus

    r = |S| = (p^d−1)/(p^l−1)

is prime. The spread counting identity implies l divides d: writing
d=al+b with 0≤b<l, divisibility p^l−1 | p^d−1 implies p^l−1 | p^b−1,
and b=0 follows. Put u=d/l>1.

**Lemma A2 (prime repunit arithmetic).** If

    (p^(ul)−1)/(p^l−1)

is prime, then u is prime, l=u^e for some e≥0, and p is not congruent
to 1 modulo u.

If u is composite, the geometric sum factors into two integer
geometric sums greater than one. Thus u is prime. Suppose a prime
v different from u divides l, and write x=p^(l/v). The polynomial
Φ_u(X)=1+X+⋯+X^(u−1) divides Φ_u(X^v): reduction modulo Φ_u(X)
uses X^u=1, and multiplication by v permutes the residues modulo u.
Therefore 1<Φ_u(x)<Φ_u(x^v)=r, contradicting primality. Hence l=u^e.
Finally, p≡1 modulo u would give r≡u≡0 modulo u, whereas r>u.

**Lemma A3 (cyclic semilinear descent).** Let p,u be primes with
p not congruent to 1 modulo u. Let U be an F_p-vector space of
dimension u^e, and let a finite group J act faithfully and
irreducibly on U. Suppose that:

* C is a normal cyclic subgroup of J;
* K=F_p[C] is a field of endomorphisms of U;
* J normalizes K, so its action on U is semilinear over K;
* J/C is a cyclic u-group.

Then U has dimension one over K.

**Proof.** Write |K|=p^h. Since U is a K-vector space, h divides u^e
and is itself a power of u. For every power u^a we have

    p^(u^a)−1 ≢ 0 (mod u).

For p=u this is immediate; otherwise Fermat's congruence gives
p^(u^a)≡p modulo u. In particular u does not divide |K*| or |C|.

Choose an element t whose coset generates J/C, and let y be its
u-primary component in the cyclic group ⟨t⟩. The component of order
coprime to u belongs to C, since J/C is a u-group. It follows that
J=C⟨y⟩. Let σ be the automorphism induced by y on K and m its order.
The operator z=y^m centralizes K, C and y, and hence all of J.

Irreducibility implies that every nonzero operator in the commutative
algebra F_p[z] is invertible: its kernel is J-invariant. Thus this
finite algebra is a field, of order p^a with a dividing dim_Fp(U)=u^e.
The congruence above shows that its multiplicative group has order
coprime to u. But z has u-power order, so z=1. Therefore y^m=1;
its order equals the order of σ.

There exists a nonzero vector w fixed by y, including when u=p.
Here is a proof avoiding division by m. Choose v≠0 and consider

    S(a) = Σ_(i=0)^(m−1) σ^i(a) y^i(v),     a∈K.

Every S(a) is fixed by y. They cannot all vanish: apply a K-linear
functional nonzero on v and use linear independence over K of the
distinct field automorphisms 1,σ,…,σ^(m−1). That independence has
the usual elementary proof: from a shortest nonzero relation between
distinct automorphisms, evaluation on ax minus one automorphism's
value on a times evaluation on x gives a shorter relation.

Now Kw is a nonzero J-invariant F_p-subspace, since C acts by K-scalars
and y fixes w and normalizes K. Irreducibility gives U=Kw. ∎

**Proof of Theorem A.** Fix U∈S. The group H_U modulo its ambient
scalar subgroup C0=H_U∩F* embeds in Gal(F/F_p), whose order is
d=u^(e+1) by A2. Let J be the image of H_U in GL_Fp(U), and let C
be the image of C0. Taking this image is essential: the restriction
of H_U to U need not be faithful.

The scalar subgroup C0 acts faithfully on U. Its generated algebra
K=F_p[C0] is an actual subfield of F, and U is a K-vector space.
The semilinear action normalizes this field, J/C is a cyclic u-group,
and J is irreducible by hypothesis. Lemma A3 yields U=wK with
|K|=p^l. Since finite fields have a unique subfield of each possible
order, K is F_(p^l). Every other spread member is an H-image of U;
a scalar-Frobenius map sends wK to another one-dimensional K-space.
There are exactly r such K-spaces, already the size of S, so S is
the whole Desarguesian spread. ∎

**Why the local hypotheses match the source.** The setwise stabilizer
of the additive line U in T⋊H is T_U⋊H_U, with T_U regular on U.
An affine group with regular elementary abelian translation subgroup
is primitive precisely when its zero stabilizer is irreducible: blocks
containing zero are exactly invariant additive subspaces. Likewise
the stabilizer of zero acts on the lines through zero as H acts on S.
The source's Proposition 5.2 supplies the translation/spread reduction
for its one-dimensional case. These are explicit retained inputs;
the general flag-transitive classification is not reproved here.

### Corollary: exact existence and uniqueness in the remaining case

Fix a prime p and integers 0<l<d with l dividing d. There is a
flag-transitive RWPRI spread space on p^d points, with p^l points on
each line and a designated one-dimensional affine semilinear group,
if and only if

    r = (p^d−1)/(p^l−1)

is prime. When it exists, the space is uniquely determined up to
isomorphism: it is AG(d/l,p^l). Moreover, an action with all the required
properties already exists inside AGL1(F_(p^d)), without using the full
automorphism group of that affine space.

**Proof.** Necessity of the prime condition follows from A1, and
uniqueness is Theorem A. For sufficiency, put F=F_(p^d), K=F_(p^l)
and take the spread S={wK : w∈F*}. Let

    G = T_F ⋊ F* = {x ↦ ax+b : a∈F*, b∈F}.

Translations are transitive on points, and the zero stabilizer F*
is transitive on S, so G is flag-transitive. Its pencil action is
the regular action of F*/K*, a cyclic group of prime order r, hence
primitive. The stabilizer of the line K is T_K⋊K*, which is sharply
2-transitive on K: an ordered pair of distinct points has a unique
affine map to any other such pair. The same is true on every line
by conjugacy. Finally G is sharply 2-transitive on F, so is primitive
on the whole point set. Thus both local actions are primitive and
the geometry is RWPRI. ∎

This gives the spaces and their exact existence condition in the
source's Theorem 6.1(1). It does not enumerate every subgroup that can
act on each space. The sufficiency argument verifies the required
one-dimensional acting group explicitly, rather than relying on the
source's Proposition 5.5 appeal to the full automorphism group.

### Exact checks and an assumption boundary

[phase4_spread_descent_check.py](phase4_spread_descent_check.py) implements
binary finite fields directly and enumerates all subspaces of the
specified dimension containing 1. Scalar/Frobenius orbit representatives
then cover every nonzero subspace. For each representative it computes
the full semilinear stabilizer and tests irreducibility by generating
the invariant span of every nonzero vector.

| Field degree | Line dimension | Subspaces containing 1 | Semilinear orbits | Irreducible stabilizer orbits |
|---|---|---|---|---|
| 4 | 2 | 7 | 2 | 1, the subfield orbit |
| 8 | 4 | 11,811 | 109 | 1, the subfield orbit |
| 6 | 2 | 31 | 4 | 2, including a non-subfield orbit |

The degree-six control shows why the restrictions matter: a non-subfield
two-space can have an irreducible semilinear stabilizer when the ambient
Galois quotient is not a group of prime-power order of the required prime.
Its potential spread size is 21, not prime. No claim is made that this
particular control subspace belongs to a locally primitive spread.
The certificate is [phase4_spread_descent_check.json](phase4_spread_descent_check.json).
These tests support, rather than replace, the uniform proof.

The root agent independently reviewed Lemmas A1–A3 and the exact source
hypotheses, finding no gap, including the possible kernel of the line
action and descent in characteristic u. The separate review record is
[phase4_spread_descent_audit.md](phase4_spread_descent_audit.md).
This is internal agent review; external review and priority remain open.

### Later status and limits

Targeted searches through the audit date found no primary paper explicitly
settling this narrower RWPRI question. This is a search result, not a
proof of novelty. Later papers do produce non-Desarguesian one-dimensional
flag-transitive spaces, so “all one-dimensional flag-transitive spread
spaces are Desarguesian” would be false.

* Pauley–Bamberg, *A construction of one-dimensional affine
  flag-transitive linear spaces*, Finite Fields Appl. 14 (2008),
  537–548, [DOI](https://doi.org/10.1016/j.ffa.2007.07.006),
  [author manuscript](https://cage.ugent.be/~bamberg/Research_files/A%20construction%20of%201D%20affine%20flagtrans%20linear%20spaces.pdf).
  Introduction and Theorem 1/proof were inspected: a cyclic orbit of a
  two-space is a spread precisely when a norm-polynomial condition holds.
  Local primitivity on both residues is not their hypothesis.
* Feng–Lu, *New families of flag-transitive linear spaces*,
  [primary preprint](https://arxiv.org/abs/2108.03848), constructs further
  families by permutation-polynomial methods. This is additional
  evidence that the omitted local hypothesis cannot be discarded.
* Jameson–Sheekey, *Cyclic 2-Spreads in V(6,q) and Flag-Transitive
  Affine Linear Spaces*, Finite Fields Appl. 98 (2024), 102463,
  [primary preprint](https://arxiv.org/abs/2309.06872).
  The introduction, §§2.1–2.4 and their precise cyclic-group setup were
  read. Their spread size is q^4+q^2+1=(q^2+q+1)(q^2−q+1), which is
  composite. Those examples cannot have a locally primitive
  one-dimensional affine action by Lemma A1, so they do not answer or
  contradict the 2003 question.
* Sheekey's [2025 conference abstract](https://aca2025.github.io/assets/abstract/14_7.pdf)
  still describes the broader cyclic-spread classification as unfinished
  and announces further orbit-polynomial work. It does not establish the
  status of the narrower 2003 question.
* Guan–Zhou, *Extremely primitive groups and linear spaces*, Czech.
  Math. J. 66 (2016), 445–455,
  [primary PDF](https://dml.cz/bitstream/handle/10338.dmlcz/145735/CzechMathJ_66-2016-2_12.pdf),
  uses “locally primitive” only for pencils of lines. Its main condition
  is extreme primitivity on point suborbits. Theorem 1.1's affine
  exception is AG(m,3), with line size three. Its introduction and the
  proof of Theorem 1.1 were checked; neither supplies the general
  two-sided local-primitivity result required here. The introduction's
  compressed reference to Liebeck's 1998 affine classification is not
  taken as evidence that the one-dimensional case was completely settled:
  the 2008 and 2024 primary works above explicitly retain that case.

The structural bridge is substantive: a primitive local action forces
a prime-size partition; this forces a prime-power Galois quotient; an
irreducible scalar-by-cyclic action then descends to a one-dimensional
module over its scalar field. This identifies the spread rather than
merely recognizing a proposed one. The nontrivial new step relative to
the source is Lemma A3 and its application, not the standard correspondence
between affine blocks and invariant subspaces.
The fixed-vector descent mechanism is classical Galois descent, closely
related to Hilbert 90; no novelty is claimed for that mechanism itself.
The candidate new contribution is its application to this specific
source gap with the arithmetic and local-action hypotheses verified.

## 2. The 2005 Hermitian-unital conjecture

**Source.** D. Leemans, *A generalization of a construction due to Van
Nypelseer*, Beiträge Algebra Geom. 46 (2005), 561–574,
Construction 3 and Conjecture 1 in §4.6, p.569.
[Primary PDF](https://ftp.gwdg.de/pub/misc/EMIS/journals/BAG/vol.46/no.2/b46h2lee.pdf).

For the classical Hermitian unital U_H(q), form a rank-three incidence
structure with types: unital points Q, unital blocks L, and original
flags (p,M). Incidence is Q not in L; Q in M minus {p}; and
L intersect M={p}, respectively. The conjecture says that this
structure is firm, residually connected and flag-transitive for every
prime power q>2.

**Status.** A complete proposed proof already exists in this project,
[hermitian_unital_proof.md](hermitian_unital_proof.md), with exact checks
at q=2,3,4,5 and internal review. The new intake must not count it as
newly solved a second time. Exact-title and unital-specific primary
searches in this pass found no external resolution; priority remains
unverified.

**Reusable reduction.** The difficult block residue identifies with the
norm shell h(v,v)=−1 in a Hermitian plane. SU2(q) acts regularly on
this shell, and upper/lower root-group moves change vectors by isotropic
differences. These moves generate SU2(q), so the residue is connected.
The other residues are elementary; a diagonal unitary torus is regular
on the final chamber choices. Thus PGU3(q) is chamber-regular. This
is a genuine torsor and generator-connectivity argument. The family-specific
input is the explicit Hermitian norm-shell identification, not a
general assertion that every coset geometry is connected.

## 3. The 2004 geometric intersection-property algorithm

**Source.** P. Jacobs and D. Leemans, *An algorithmic analysis of the
intersection property*, LMS J. Comput. Math. 7 (2004), 284–299,
Definitions/Lemmas 2.1–2.2 and §3, especially Figure 1.
[Primary DOI](https://doi.org/10.1112/S1461157000001133).
Local primary text: `sources/catalogue_L096.txt`.

**Exact target.** In every residue R, for every type i, every element x
and every flag F, the intersection of the i-shadows of x and F must
be empty or equal to the i-shadow of a flag F' incident with x and F.
The principal algorithm checks this property by reducing, under a
flag-transitive group, to a fixed incident pair of elements and one
representative of each orbit of its stabilizer on relevant flags.
The weak variants replace “every type” by “at least one type” in
each residue. This geometric shadow property must not be confused
with the subgroup intersection property for distinguished involutions.

**Status.** This is a proved algorithm, not an old open conjecture.
Sections 2–3 were read, including the pruning cases in Figure 1.
The large sporadic-group tables in §§4–5 were not recomputed in this
intake. Therefore no whole-paper rederivation is claimed.

**Uniform matrix reduction.** Let B_ij be the zero-one incidence matrix
between elements of types i and j in a finite residue R, with B_ii=I
for the equality convention within one type. For any flag
F not containing type i, its i-shadow has characteristic vector

    s_i(F) = product_(x in F) B_(i,t(x))[:,x]

where the product is entrywise; the empty product is the all-one vector.
The same formula with B_ii=I handles a flag containing type i and gives
the singleton-shadow case used in the source's algorithm.
Let C(x,F) be the set of flags whose elements are incident with x and
all elements of F. Then the exact acceptance test for the pair (x,F) is

    s_i(x) ⊙ s_i(F) = 0
    or s_i(x) ⊙ s_i(F) belongs to {s_i(E) : E in C(x,F)}.

These identities hold entry by entry by the definition of incidence.
Thus they give an exact finite matrix algorithm for all residues;
the group acts by simultaneous permutation of rows, columns and flag
indices. Taking orbit representatives under an incident-pair stabilizer
preserves every tested identity and recovers the source's §3 reduction.
Singleton shadows and nested-shadow pruning recover the easy cases
in Figure 1. The realization problem for a shadow as an admissible flag
remains essential; replacing it with subgroup meets alone is invalid.

This is an integration of an existing theorem into the basis-aware
torsor calculus, not a new proof of the sporadic table entries. It also
pinpoints a limit of the matrix language: the admissible flag set is
combinatorial input, and ordinary matrix multiplication does not
automatically determine it.

## Intake outcome

Three fully stated old targets were examined: one 2003 question with a
new uniform proposed proof, one 2005 conjecture with an earlier project
proof and renewed status audit, and one 2004 principal algorithm with an
exact matrix reduction. The finite sporadic/Suzuki classification track
is owned separately, avoiding duplicate counts. Machine-readable records
are in `phase4_old_problem_intake.json`.
