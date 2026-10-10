# An introduction to mathematical compression

This project asks how much of a connected body of mathematics can be recovered
from a small collection of arguments that remain useful as the examples change.
The initial subject is finite groups acting on polytopes, incidence geometries
and graphs. The working bibliography extends over several decades; one concrete
bridge developed below connects a construction published in 2005 with questions
and constructions studied in 2026.

The central proposal is to retain the **marked action**, not just the abstract
group. A group can act on several sets, have several generating tuples, and
support different incidence structures. Those distinctions are often the entire
classification problem. Keeping them makes several recurring calculations
exact: intersections become products of relation matrices, geometric symmetry
becomes an orbit condition, and some growing group classifications become
linear congruences over a fixed finite quotient.

These ideas come from established group actions, coset geometry, extension
theory and linear algebra. Their value here is in the derivations they enable.
A common notation alone does not shorten a proof. A successful compression
must supply the missing generation, intersection, incidence or completeness
argument, and identify the external results it still uses.

There is also recent general theory within the literature itself. Piedade
and Tranchida's [2025–2026 work](https://arxiv.org/html/2505.24662v1)
develops compatible amalgamations, HNN extensions,
semidirect products and twisting for coset geometries. Its Proposition 2.2
collects the flag-transitivity/Helly equivalences used in this subject.
Those established constructions are part of the comparison baseline. Our
specific reductions and certificates must be assessed against them;
introducing a common language is not itself a new unification theorem.

This introduction develops the machinery through examples. The linked notes
contain full hypotheses, source attribution, proofs and certificates. Proposed
new consequences are research drafts with internal checks; they have not yet
received external peer review.

## 1. The object: a torsor with marked partitions

A **left torsor** for a group $G$ is a nonempty set $X$ on which $G$ acts
freely and transitively. For any two points $x,y$, exactly one group element
maps $x$ to $y$. Choosing a base point identifies $X$ with $G$, but the
torsor itself does not privilege an identity point.

Why start with a torsor? In a regular polytope or a regular thin chamber
geometry, the automorphism group acts freely and transitively on chambers.
A chamber can therefore be represented by a group element. Faces and residues
are obtained by grouping chambers into blocks. The relevant object is the
torsor together with those distinguished partitions.

Choose a base point and identify $X=G$. A subgroup $H\leq G$ defines the
partition into left cosets $xH$. Its relation matrix is

$$
A_H[x,y]=\begin{cases}1&x^{-1}y\in H,\\0&\text{otherwise.}\end{cases}
$$

This relation is invariant under simultaneous left translation. Conversely,
every left-invariant equivalence relation $R$ on $G$ comes from a subgroup:
take $H=\{h:R(1,h)\}$. Symmetry, transitivity and translation invariance give
closure under inverses and multiplication, and recover

$$R(x,y)\quad\Longleftrightarrow\quad x^{-1}y\in H.$$

Thus the subgroup and partition descriptions contain exactly the same
information. This is a reconstruction theorem, not an approximation.

There is also an intrinsic algebraic description. For finite $X$, form

$$\mathcal A=\mathbb Q^X$$

with coordinatewise multiplication. The point indicators $e_x$ are precisely
its primitive idempotents, so every algebra automorphism permutes them:

$$\operatorname{Aut}_{\mathbb Q\text{-alg}}(\mathbb Q^X)=\operatorname{Sym}(X).$$

Unital subalgebras correspond to partitions: a partition gives the functions
constant on its blocks. For the converse, declare two points equivalent when
every function in a subalgebra agrees on them. For a point $x$, choose a
function $f_y$ separating it from each point $y$ outside its block. Then

$$\prod_{y\text{ outside the block of }x}
  \frac{f_y-f_y(y)}{f_y(x)-f_y(y)}$$

is the indicator of that block and belongs to the subalgebra. Hence every
block indicator is recovered. Invariant subalgebras correspond to invariant
partitions under the pullback action of $G$.

This answers a natural linear-algebra question: permutation matrices really
are linear operators, and the whole object can be expressed algebraically.
However, arbitrary changes of vector-space basis do not preserve it. One must
retain the point basis, or retain the multiplication that reconstructs that
basis.

For example, let $V=C_2^2$. The six-point $V$-sets

$$X=V\sqcup\{*\}\sqcup\{*\},\qquad
Y=\bigsqcup_{K\text{ of order }2}V/K$$

have orbit sizes $4+1+1$ and $2+2+2$, so they are different actions. Yet
their rational permutation representations are isomorphic: both decompose
as three trivial characters and one copy of each nontrivial character.
Ordinary simultaneous linear similarity forgets the distinction. The split
algebra retains it. The [torsor note](research/case_study/torsor_matrix_theory.md)
gives an explicit invertible intertwining matrix and the formal subgroup–
partition correspondence.

## 2. Three products, three group operations

The relation matrices support three useful calculations. They should not be
confused with one another.

**Entrywise multiplication computes intersection.** For subgroups $H,K$,

$$A_H\odot A_K=A_{H\cap K}.$$

Both entries are one exactly when $x^{-1}y$ belongs to both subgroups.

**Ordinary multiplication counts factorizations.** Define $A_S$ by the same
membership rule for any subset $S\subseteq G$. Then

$$A_HA_K=|H\cap K|A_{HK}.$$

The $(x,z)$-entry counts decompositions $x^{-1}z=hk$. If one exists, all
others have the form $(ht,t^{-1}k)$, with $t\in H\cap K$. This proves the
formula without a commutativity assumption. The product set $HK$ need not
be a subgroup; it is a subgroup precisely when $HK=KH$.

**Boolean reachability computes generation.** The transitive closure of
the union of the relations $A_H,A_K$ is $A_{\langle H,K\rangle}$.
Walking through their blocks is the same as multiplying elements from the
two subgroups.

Sizes and indices also become visible:

$$A_H^2=|H|A_H,\qquad
\operatorname{rank}_{\mathbb Q}(A_H)=|G:H|.$$

After ordering points by cosets, $A_H$ consists of all-ones diagonal blocks.
Its normalization by $|H|$ averages a function over each coset.

Now mark generators $\rho_0,\ldots,\rho_{r-1}$ and put

$$G_I=\langle\rho_i:i\in I\rangle.$$

The **intersection property**, abbreviated IP, is

$$G_I\cap G_J=G_{I\cap J}\quad\text{for every }I,J.$$

It is exactly the family of identities

$$A_{G_I}\odot A_{G_J}=A_{G_{I\cap J}}.$$

For involutory generators, adding commutation of nonadjacent generators
gives the string C-group conditions used for regular abstract polytopes.
The marking matters: changing generators can change whether IP holds.

None of this requires storing $|G|\times|G|$ dense matrices. Translation
invariance determines every row from the identity row. Subgroup lists,
generators and normalizers can provide the compact implementation. The
matrix language explains what is being computed; it need not dictate an
inefficient data structure.

## 3. Geometry adds a Helly condition

Suppose subgroups $H_i\leq G$ represent the maximal parabolics. Vertices of
type $i$ are cosets $gH_i$; two vertices of different types are incident
when their cosets intersect. A flag is a collection of mutually incident
vertices of distinct types.

Pairwise intersection does not generally imply common intersection. This
gap is exactly the geometric condition that the matrix encoding must retain:

> Every pairwise-intersecting collection of cosets of distinct types has a
> common point.

This **typed Helly condition** is equivalent to transitivity of $G$ on each
flag type. A common point $g$ makes the entire flag a translate of the base
flag $\{H_i\}$. Conversely, such a translate contains $g$ in all its
cosets. A common point also supplies missing types, so every flag extends
to a chamber.

Write $B=\bigcap_i H_i$. Under this condition the chamber set is $G/B$.
It is the original $G$-torsor only when $B=1$. A panel missing type $i$
has exactly

$$\left|\bigcap_{j\ne i}H_j:B\right|$$

completions; **thinness** means this index is two.

Connectivity has an equally precise group formulation. For a flag of types
$J$, put $K_J=\bigcap_{j\in J}H_j$. Flag transitivity identifies its
residue with the coset system inside $K_J$. When at least two types remain,
that residue is connected exactly when

$$K_J=\left\langle K_J\cap H_i:i\notin J\right\rangle.$$

This is a Boolean reachability test. The flag-transitivity hypothesis is
essential to this identification. Without it, a suggested internal coset
model can miss incident pairs.

For standard C-group parabolics $H_i=G_{I\setminus\{i\}}$, IP supplies
the panel indices and residue-generation equalities. In a general non-string
diagram it does not by itself supply the Helly condition. The repository
includes an exact small example demonstrating this failure.

The same language counts multiple flag orbits. If $G$ is transitive on
flags of type $J$, extensions by type $k$ are classified by

$$K_J\backslash\left(\bigcap_{j\in J}H_jH_k\right)/H_k.$$

Normalize the $J$-flag first; the remaining freedom is its stabilizer
$K_J$. This double-coset formula explains why certain chirality tests reduce
to product-set cardinalities. A chiral action has two alternating chamber
orbits, so two torsors may be needed. Identifying the designated acting group
with the full automorphism group is a separate step. The
[incidence reductions](research/case_study/incidence_compression.md) keep that
distinction explicit.

There is an additional terminology boundary in the older literature.
Jacobs–Leemans's 2004 intersection-property problem concerns **geometric
shadows**, not the subgroup identity above. A type-$i$ shadow $\sigma_i(F)$
consists of the type-$i$ elements incident with a flag $F$. Their condition,
required in every residue of rank at least two, asks that a nonempty intersection
$\sigma_i(x)\cap\sigma_i(F)$ be the shadow of a suitable flag $F'$ incident
with $x$ and $F$. An intersection of two zero-one shadow vectors is easy to
compute; proving that it has the required flag witness is an additional
existence condition. Neither the Hadamard subgroup identity nor a C-group
certificate proves it automatically. The old classification tables are not
claimed as consequences of the present subgroup-IP machinery. The separate
[shadow-witness reduction](research/case_study/phase4_shadow_ip.md) develops
the Boolean test appropriate to that condition.

## 4. Counting actions by their orbits

Every finite $G$-set decomposes uniquely as a multiset of transitive actions
$G/H$, where $H$ is taken up to conjugacy. Its normal form is therefore
a vector of nonnegative multiplicities $m_H$, with

$$|X|=\sum_Hm_H|G:H|.$$

The action is faithful exactly when the intersection of the cores of its
occupied stabilizers is trivial. For an abelian group, each core is just
the stabilizer itself. This can replace a permutation search in a large
symmetric group with a calculation on a small subgroup lattice.

For $V=\mathbb F_2^2$, there are only five orbit types: the regular orbit,
three two-point quotients, and the fixed point. Two independent commuting
involutions acting on $N$ points are precisely a faithful $V$-action
with a chosen basis of $V$. Conjugacy of the permutations is equivalence
of the actions. Forgetting the order of the two generators adds the basis
swap on this five-coordinate normal form.

Parity is also local to the orbit types. For $V=\mathbb F_2^r$, a quotient
of size $2^d$ makes a nontrivial element act as $2^{d-1}$ transpositions.
Only $d=1$ contributes an odd permutation. Thus the total sign is the sum
modulo two of the linear characters attached to the occupied hyperplane
quotients, counted with multiplicity.

Three classical tools now have distinct jobs. Geometric-series products
count multiplicities. Möbius inversion on the subspace lattice selects
faithful actions. Burnside averaging handles allowed permutations of the
marking. A character average imposes zero total sign. The
[all-rank formula](research/case_study/elementary_action_theorem.md) spells out
this calculation and its precise equivalence relation.

The [commuting-pair reduction](research/case_study/commuting_pairs_compression.md)
recovers all principal results of its 2013 source using this normal form,
while retaining the exceptional degree-six automorphism input explicitly.
The all-rank extension illustrates useful compression: the replacement
argument computes cases beyond the original theorem, with complexity driven
by $r$, rather than by enumeration of $S_N$.

## 5. Covers: isolate the obstruction in the kernel

Let $\pi:\widetilde G\to G$ be a homomorphism with kernel $K$, and let
$\widetilde G_I$ be a monotone family of subgroups mapping onto $G_I$.
Suppose the image family has IP. Put $K_I=K\cap\widetilde G_I$. Then

$$\widetilde G_I\cap\widetilde G_J
=\widetilde G_{I\cap J}(K_I\cap K_J).$$

Indeed, an element in the left side has image in $G_{I\cap J}$. Choose
an element of $\widetilde G_{I\cap J}$ with that image and divide by it.
The remainder lies in both kernel subgroups. The reverse inclusion is
immediate. Hence IP upstairs is equivalent to

$$K_I\cap K_J=K_{I\cap J}.$$

No centrality or finiteness is needed. The difficulty has been localized,
but not automatically solved: one must still construct the cover and
identify its kernel diagram.

A useful case makes the diagram a coordinate system. Suppose
$K=\prod_eK_e$, with each coordinate attached to a set of generator
indices, and

$$K_I=\prod_{e\subseteq I}K_e.$$

Intersecting supported coordinate products immediately gives the required
identity. The [coordinate certificate](research/case_study/formal/CoordinateKernels.lean)
formalizes this abstract implication.

The construction behind several applications is **dihedral edge inflation**.
Start with a marked C-group $B$ whose standard coset geometry is a regular
hypertope. Require retractions onto the selected two-generator dihedral
subgroups that fix their two generators and kill the others. Replace a pair
product of even order $q_e$ by one of order $m_e$, where $q_e\mid m_e$, and take the
simultaneous fiber product over those retractions. Its new kernel coordinate
has order $m_e/q_e$.

The word $(\rho_i\rho_j)^{q_e}$ isolates that coordinate: other pair
coordinates see at most a single involution, killed by the even exponent.
This proves generation of the entire kernel, the exact group order, and
the formula for every parabolic kernel. The coset Helly condition is also
proved: each lifted parabolic coset specifies certain coordinates, and
pairwise intersection says that repeated specifications agree.

Starting with $B=C_2^r$ therefore constructs regular hypertopes for arbitrary
even pair orders, with order

$$2^r\prod_{i<j}\frac{m_{ij}}2.$$

For a string this becomes $2\prod_i m_{i,i+1}$. Affine square-grid seeds
allow additional powers of two in the group order while preserving prescribed
types. The [construction note](research/case_study/compression_phase2.md)
derives the seeds, retractions and actual source presentations. Its
retraction assumptions are substantive; arbitrary marked groups do not
automatically satisfy them.

## 6. Growing classifications become affine congruences

Construction answers “does one exist?” Classification must also prove that
every object arises. A cyclic-core argument supplies that stronger direction
for a particular family.

Fix $s\geq3$. Consider marked rank-three string C-groups $(G;a,b,c)$
of order $2^{t+s}$, type $\{4,2^t\}$, with $t\geq s-1$. Thus $a,b,c$
are involutions, $a,c$ commute, and the two adjacent product orders are
four and $2^t$. Set

$$\ell=2^{s-2},\quad h=2^{2s-2},\quad k=t-s+2,\quad n=2^k.$$

Using Lucchini's cyclic-core bound, the
[classification reduction](research/case_study/phase3_classification.md)
proves that

$$A=\langle(bc)^\ell\rangle\trianglelefteq G,\qquad |A|=n,$$

and that $Q=G/A$ is a marked string C-group of order $h$ and type
$\{4,\ell\}$. As $t$ grows,
the quotient size stays fixed. Its marked classification is a finite retained
input; the growing part is one cyclic kernel.

Identify $A$ with $R=\mathbb Z/n\mathbb Z$, sending the canonical element
$(bc)^\ell$ to $1$. For a fixed marked quotient, its action on $A$ has

$$\rho(\bar b)=\rho(\bar c)=-1,\qquad \rho(\bar a)=u,\qquad u^2=1.$$

There are at most four choices for $u$; each must satisfy the relations
of $Q$. Once the action is fixed, introduce a normalized function
$f:Q\times Q\to R$ and define

$$ (x,g)(y,h)=(x+\rho(g)y+f(g,h),gh). $$

Associativity is exactly the linear cocycle equation

$$\rho(g)f(h,j)-f(gh,j)+f(g,hj)-f(g,h)=0.$$

Normalization $f(1,g)=f(g,1)=0$ gives the identity. Choose lifts
$a=(x_a,\bar a)$, $b=(x_b,\bar b)$, $c=(x_c,\bar c)$, and impose

$$a^2=b^2=c^2=(ac)^2=(ab)^4=1,\qquad (bc)^\ell=(1,1).$$

These are affine linear equations in the values of $f$ and the three
shifts. In evaluating a word, all quotient coordinates are known. Each
step adds a specified multiple of a shift or one cocycle value; it never
multiplies two unknowns. There are at most $(h-1)^2+3$ unknowns, independent
of $t$. The arithmetic is over a ring, so field Gaussian elimination
cannot be used indiscriminately.

These equations suffice. The last relation generates the full kernel;
the quotient marking generates $Q$. The pair $a,b$ maps injectively to
its dihedral quotient, while $b,c$ contains the kernel. The intersection
criterion then gives $\langle a,b\rangle\cap\langle b,c\rangle=\langle b\rangle$.
Conversely, choosing a section of any group under consideration produces
exactly such a cocycle and marking shifts. This proves completeness.

There is a final redundancy to remove. A normalized function $v:Q\to R$
changes section by

$$ (f,x_a,x_b,x_c)\longmapsto
(f+\delta v,x_a-v(\bar a),x_b-v(\bar b),x_c-v(\bar c)),$$

where $\delta v(g,h)=v(g)+\rho(g)v(h)-v(gh)$. This is exactly the relevant
marked isomorphism relation: the marking fixes the canonical kernel
generator and the marked quotient.

The action is free. A stabilizer has $\delta v=0$ and vanishes on all
three quotient generators. The resulting derivation identity forces it to
vanish on every word. Thus for the affine solution set $S$, the exact
number of marked classes for this quotient and action is

$$\frac{|S|}{n^{h-1}}.$$

The [general theorem](research/case_study/phase3_bounded_families.md) also
proves a bound independent of $t$. If $N_s$ counts the possible marked
quotients, one explicit bound is $16\ell N_s h^{h^2}$. It is deliberately
crude. A uniform bound does not imply eventual stabilization, and no such
stabilization is claimed. For the eight-family source classification, the
remaining bounded order-256 census is identified as an external catalogue
input rather than hidden inside the word “uniform.”

## 7. Intersection tests without enumerating the extension

In more general extensions, the quotient may fail IP. The same coordinates
still allow exact filtering without constructing every element upstairs.

Let $H_I$ be a subgroup generated by some marked lifts, with image $Q_I$.
Choose a word lifting each $q\in Q_I$, with coordinate $\alpha_I(q)$.
Schreier generators calculate $H_I\cap A$ from boundedly many words.
If their cyclic coordinates are $\xi_1,\ldots,\xi_m$, put

$$d_I=\gcd(n,\xi_1,\ldots,\xi_m).$$

Then the fiber of $H_I$ above $q$ is exactly

$$\{(x,q):x\equiv\alpha_I(q)\pmod{d_I}\}.$$

Two such fibers meet precisely when their constants agree modulo
$\gcd(d_I,d_J)$; their common fiber is then a congruence class modulo
$\operatorname{lcm}(d_I,d_J)$. Consequently full IP reduces to

$$d_{I\cap J}=\operatorname{lcm}(d_I,d_J)$$

and exclusion of every extra quotient fiber: for
$q\in(Q_I\cap Q_J)\setminus Q_{I\cap J}$, require

$$\alpha_I(q)\not\equiv\alpha_J(q)\pmod{\gcd(d_I,d_J)}.$$

The number of quotient elements and words depends on the bounded quotient
and rank. The growing parameter enters only through integer arithmetic.
This is a genuine algorithmic reduction, although its gcd and inequality
filters are additional to solving the affine equations.

## 8. A bridge from 2005: identify the residue before proving connectivity

The 2005 Van Nypelseer construction applied to Hermitian unitals left a
uniform connectivity and symmetry conjecture. The proposed
[proof here](research/case_study/hermitian_unital_proof.md) identifies the
difficult block residue with a concrete group action.

Let $W$ be a nondegenerate Hermitian plane over $\mathbb F_{q^2}$.
The relevant points form the norm shell

$$X=\{v\in W:h(v,v)=-1\}.$$

Two points have a common neighbor in the residue exactly when their
difference is isotropic. The group $SU(2,q)$ acts freely on $X$, and
both sets have size $q(q^2-1)$, so the action is transitive. Its upper and
lower unipotent subgroups generate it; their displacements are isotropic.
Every generating move therefore stays inside a connected component, and
transitivity forces the residue to be connected.

The reusable statement is short: a transitive group action connects a
relation if a generating set moves every point within its reachability
class. The substantial work is the norm-shell identification and verification
of the permitted moves. Other residues, panel sizes and flag transitivity
are checked separately. The Lean connectivity lemma certifies the abstract
propagation step, not the entire Hermitian construction.

A distinct 2026 triangle construction illustrates another bridge. On flags
of a uniform linear space with at least three points per line and three
lines through each point, let $A,B$ record equality of point and equality
of line. The directed relation $D=(A-I)(B-I)$ creates a three-part incidence
matrix with cyclic blocks $D,D^T$. Cyclic permutation of the parts supplies
triality. More significantly, common-neighbor counts in $DD^T,D^TD$
reconstruct the original two partitions. This recovers the automorphisms
and correlations of the constructed geometry from those of the original
linear space. The [incidence note](research/case_study/incidence_compression.md)
proves the reconstruction, including the distinction between a duality and
an involutory polarity. The 2005 and 2026 geometries are different objects;
the shared method is to solve their local relations explicitly.

### A 2003 gap: local primitivity forces a scalar field

Buekenhout, Dehaye and Leemans asked whether their one-dimensional
flag-transitive RWPRI spread spaces must be Desarguesian. Here a spread
partitions the nonzero vectors of $\mathbb F_{p^d}$ into additive
$l$-dimensional subspaces, and its translates are the lines. The two local
conditions say that the semilinear group acts primitively on the spread
and each line stabilizer acts irreducibly on its line.

The [descent argument](research/case_study/phase4_old_problem_audit.md)
identifies the lines, rather than testing candidates. A primitive action
of a group with cyclic normal subgroup and cyclic quotient has prime
degree. Hence

$$r=\frac{p^d-1}{p^l-1}\text{ is prime},\qquad
d=u^{e+1},\quad l=u^e,\quad p\not\equiv1\pmod u,$$

where $u$ is prime. On one line $U$, let $C$ be the scalar subgroup and
$K=\mathbb F_p[C]$ its generated field. The faithful line action has a
cyclic $u$-group quotient by $C$. Choose a $u$-element $y$ generating this
quotient. If its induced automorphism of $K$ has order $m$, then $y^m$
is central. Irreducibility places this central operator in a finite field
whose degree divides $u^e$. Its multiplicative group has no $u$-torsion,
so $y^m=1$.

Cyclic Galois descent, using the fixed-vector mechanism behind Hilbert 90,
now supplies a nonzero fixed vector $w$. The
$K$-line $Kw$ is invariant, so irreducibility forces $U=Kw$. Every other
spread member is a scalar-Frobenius image, giving precisely the lines
over $\mathbb F_{p^l}$ and the Desarguesian affine space.

This gives an affirmative answer under the paper's exact one-dimensional
and local primitivity hypotheses. The [internal review](research/case_study/phase4_spread_descent_audit.md)
passed; external review and priority remain unverified. Later
non-Desarguesian flag-transitive constructions omit these local
hypotheses. The argument uses them to force the field structure. The
candidate new contribution is this application to the 2003 gap; the
Galois descent mechanism itself is classical.

There is also an explicit converse. On these subfield lines,
$T_F\rtimes F^\times$ acts flag-transitively. Its pencil action is the
regular prime-degree action of $F^\times/K^\times$, and its line stabilizer
acts sharply two-transitively on $K$. Thus prime $r$ is the exact existence
criterion, and the space is uniquely determined. This classifies the spaces
in that remaining case; it does not enumerate every possible acting subgroup.

## 9. Three examples of short matrix equations doing the hard work

**Suzuki pentagons.** For the specified graph built from $Sz(q)$,
$q=2^{2e+1}$, vertices are cosets of $H=ZT$. A next neighbor has a unique
parameter $a\in\mathbb F_q$, represented by $z(a)w$. Starting with a
fixed directed edge, a five-step return is equivalent to

$$wz(a)wz(b)wz(c)wz(d)w\in H.$$

Three forced zero entries imply $bc=1$, $ab=1$, and $d=b$.
The only possibilities are

$$(a,b,c,d)=(a,a^{-1},a,a^{-1}),\qquad a\ne0.$$

A complete matrix identity proves the converse. Shorter words exclude
triangles and nonbacktracking four-step returns. Thus every closing word
is a pentagon, and there are $q-1$ through each edge. There is no factor
of two: an undirected cycle containing a fixed directed edge has one
traversal beginning with that edge. The
[proof](research/case_study/suzuki_cycle_proof.md) checks the source graph
identification; the Lean module checks the full word-membership equivalence.

**Pauli supports in dimension four.** Projectively commuting involutions
need not have commuting matrix lifts: the lifts can anticommute. For a
rank-seven string C-group in odd-characteristic $PGL_4$ with noncommuting
adjacent generators, four alternating
generators yield a nondegenerate commutator form on $V=\mathbb F_2^4$.
Their sixteen lifted products give a basis $P_v$ of the matrix algebra,
with

$$P_vP_w=(-1)^{\omega(v,w)}P_wP_v.$$

Projective commutation constrains a matrix's support in this basis to an
affine subspace. IP forces two endpoint supports to span their available
two-dimensional directions. Because those directions intersect trivially,
product labels have unique decompositions: coefficients cannot cancel
between different pairs. Comparing coefficients forces orthogonality,
then a tensor decomposition $k^4=k^2\otimes k^2$.

All seven generators consequently preserve the symmetric form $J\otimes J$
up to scalar, where $J$ is the alternating form on $k^2$. The natural
$PSL_4(q)$ cannot preserve such a form. The
[tensor proof](research/case_study/phase3_psl4_rank7.md), together with earlier
rank exclusions, gives the upper bound six.

A subsequent [rank-five argument](research/case_study/phase7_psl4_zero_product.md)
uses the same principle through the multiplicative Jordan decomposition.
Each endpoint product separates into commuting semisimple and unipotent
parts. The left endpoint involutions invert their own unipotent part and
centralize the right one; the right endpoints satisfy the reversed rules.
These constraints drastically restrict the algebra generated by the two
unipotent parts on a four-dimensional space.

Semisimple endpoint modules and larger Jordan blocks first give invariant
forms or invariant subspaces. A nonzero product of the two square-zero
nilpotent parts forces a two-by-two tensor representation. In the remaining
case, the nilpotents $N,M$ satisfy

$$N^2=M^2=NM=MN=0.$$

Their ranks are one or two. Three cases now suffice: ranks $(1,1)$,
$(1,2)$ and $(2,2)$. Common images, kernels and weight spaces either force
reducibility or produce an alternating form preserved by all five
generators. The proof treats odd characteristic uniformly, including three;
exact symbolic checks corroborate the displayed matrix identities. This
excludes rank five. A rank-five parabolic inside a rank-six geometry need
not generate the whole group, so rank six requires its own argument.

The [rank-six extension](research/case_study/phase8_psl4_rank6.md) supplies
that argument. There are now two middle generators, each centralizing an
entire endpoint pair. In a reducible endpoint module, an adjacent pair
commutes on one summand but has an invertible additive commutator on the
other. A matrix block intertwining those actions must therefore vanish:

$$AC=CX,\quad BC=CY
\quad\Longrightarrow\quad (AB-BA)C=C(XY-YX).$$

If $AB=BA$ and $XY-YX$ is invertible, then $C=0$. Lean certifies this
abstract implication. The endpoint normal forms supply its hypotheses;
the other cases force a tensor form or a common image or kernel. This
completes the proposed maximum-rank-four proof, retaining the published
rank-four existence construction.

The structural conclusion is broader: a finite irreducible projective
string action in dimension four, in odd characteristic, with noncommuting
adjacent generators and rank at least five preserves a nondegenerate
symmetric or alternating bilinear form up to scalar. This theorem is
proved by the same case analysis; its full normal-form coverage remains
written mathematics, independently reviewed internally.

The [linear and unitary application](research/case_study/phase9_linear_unitary.md)
shows how this structural theorem can do new work without repeating the
normal-form classification. In $SU_4(q)$, take the determinant-one diagonal
torus with norm-one entries, together with the even permutation matrices.
The torus's ten unordered degree-two characters are distinct, including at
$q=3$. A bilinear similarity form therefore has nonzero entries in at most
one unordered coordinate pair, so has rank at most two. Its radical would
be a proper invariant subspace, whereas this monomial subgroup is
irreducible. Thus the unitary group preserves no ordinary bilinear similarity
form. Its familiar Hermitian form is sesquilinear and does not conflict
with this conclusion.

For $SL_4(q)$, an elementary transvection has order equal to the field
characteristic, so its similarity multiplier must be one. From

$$ (I+E_{ij})^{\mathsf T}B(I+E_{ij})=B, $$

the $(j,b)$ entry with $j\notin\{i,b\}$ gives
$B_{jb}+B_{ib}=B_{jb}$. Every entry of $B$ vanishes. The new
[Lean certificate](research/case_study/formal/TransvectionForms.scope.md)
checks this matrix argument over any ring, including the four-dimensional
instance; the multiplier reduction remains in the written proof.

Both simple groups have trivial projective centralizer. This prevents an
intermediate group's string diagram from splitting into a direct product,
so the form theorem applies. Consequently every group between $PSL_4(q)$
and $PGL_4(q)$, or between $PSU_4(q)$ and $PGU_4(q)$, has string C-group
rank at most four for odd $q$. The determinant quotient gives a further
test: an index-four extension has cyclic quotient $C_4$, which cannot be
generated by images of involutions. These are uniform upper bounds and
nonexistence statements. Rank-four existence for odd $PSU_4(q)$ remains
undecided here, and field or graph automorphisms require further arguments.

**Vandermonde cycle counts.** A coordinate change puts the classical Wenger
graph $W_2(q)$ into the incidence equations

$$u+r=xy,\qquad v+s=xy^2.$$

For a closed eight-step walk, let $y_0,\ldots,y_3$ be the successive line
parameters and $d_i$ the point-coordinate increments. Closure is

$$\sum_i d_i=\sum_i d_iy_i=\sum_i d_iy_i^2=0.$$

Nonbacktracking requires nonzero $d_i$ and distinct adjacent $y_i$.
Normalize the starting edge so $y_0=0$. Four distinct parameters give a
one-dimensional Vandermonde kernel with every coordinate nonzero. Three
distinct parameters give none. Two distinct parameters must alternate,
giving $d_2=-d_0,d_3=-d_1$. Counting these cases gives

$$\lambda=(q-1)^2(q-2)(q-3)+(q-1)^3
=(q-1)^2\big((q-2)^2+1\big).$$

The same rank argument excludes shorter cycles. This characteristic-free
calculation agrees with an already published formula and exposes a conflicting
odd-characteristic claim for the same graph. The
[source audit](research/case_study/phase3_egr_conjecture_audit.md) distinguishes
correcting that construction from disproving an existential conjecture about
other graphs. Exact identification of the graph is as important as the count.

## 10. Older classifications through the same action data

The older literature supplies useful tests of whether the language does real
work. Several reductions now reach beyond an encoding and actually recover
classification or characterization statements.

**Tree cuts.** Start with a tree $T$ on $N$ points, and attach to each edge
the transposition of its endpoints. For an edge subset $I$, these generators
give exactly

$$K_I=\prod_{C\text{ a component of }(V(T),I)}\operatorname{Sym}(C).$$

The unique-path property gives $K_I\cap K_J=K_{I\cap J}$. Rooting the tree
makes its edge cuts a nested-or-disjoint family of subsets. Coset vertices
are subsets of the prescribed sizes, and incidence means that their pairwise
intersection sizes agree with those of the original cuts. Any pairwise
incident family has the same nested structure and atom sizes; bijections
between its atoms assemble into one permutation. This proves the coset Helly
property and flag transitivity directly.

Residues come from deleting edges. A leaf cut gives a maximal point stabilizer;
a balanced cut gives the intermediate unordered two-block stabilizer. These
two observations produce all four principal primitivity and local-property
tests of a 1998 paper. The stronger geometric shadow intersection property
has an equally concrete test. A branching vertex contains a claw residue
that fails it. For a path, the geometry is the proper Boolean lattice, and
every nonempty shadow on $k$-subsets is

$$\{Y: |Y|=k,\ L\subseteq Y\subseteq V\},$$

where $L$ is the union of lower-rank constraints and $V$ the intersection of
upper-rank constraints. The boundary subsets give a witness flag of at most
two vertices, with singleton and empty-boundary cases handled explicitly.
The [Boolean shadow certificate](research/case_study/formal/BooleanShadow.scope.md)
now proves this exact bounded-size witness theorem in Lean for arbitrary
finite query families at every proper rank.
This recovers the advertised 2005 path characterization. The known tree model
and the foundational classification identifying all inductively minimal
pairs remain credited inputs; these are rederivations of published results.
See the [tree proof and exact scope](research/case_study/phase5_tree_cuts.md).

**Dihedral arithmetic.** In a subgroup-closed class with a simple rank-two
rigidity property, residual weak primitivity forces every parabolic lattice
edge to be maximal. Cyclic and dihedral groups satisfy that rigidity by
elementary subgroup arithmetic. Consequently every dihedral example is built
from prime-index reflection subgroups, with either one rotation subgroup or
one doubled prime. Chinese remainders solve their simultaneous coset equations
and prove flag transitivity. Their geometries are joins of prime-sized sets
and at most one polygon.

For $D_{2n}$ with $n>2$ and $m$ distinct prime divisors, the resulting number
of rank-$r$ group–geometry pairs, modulo group automorphisms and type
permutations, is

$$\binom mr+\binom m{r-1}+m\binom{m-1}{r-2}.$$

The Klein four group is an explicit exception. This recovers the complete
published all-rank theorem, available in a later primary restatement. The
original 2000 full text is unavailable, so a comparison with every printed
statement is still outstanding. The [dihedral note](research/case_study/phase5_dihedral_classification.md)
states the action and source conventions carefully.

**Finite panel actions.** For a fixed chamber stabilizer $B\le G$, let the
normalizer $N_G(B)$ act on the finite set of admissible panel overgroups of
$B$. This is another concrete permutation representation. A geometry is
reconstructed by joining selected panels, checking their exact intersections
and the typed Helly condition, and testing local axioms. RWPRI guarantees a
maximal parabolic in every residue, which gives a complete augmentation rule.
This is a proof of completeness for the enumeration, with a finite subgroup
catalogue as an explicit input.

Applied to $J_2$, the method exhausts all 146 chamber-stabilizer anchors and
recovers the 2002 principal census: eight rank-two, nineteen rank-three and
three rank-four geometries, with no higher ranks. All thirty representatives
pass a separate parabolic verifier. The source geometry lists are not search
inputs. GAP's subgroup catalogue and exact algorithms remain trusted; the
enumeration is not formalized end to end in Lean. See the
[complete reduction and certificate](research/case_study/phase5_j2_theory.md).

The next step removes local two-transitivity as an assumption. The older
J₁ problem allows every primitive panel action. A single nontrivial orbit
test is then insufficient: the rank-two check must consider every relevant
double coset. With that change the same engine exhausts J₁, M₁₁ and M₁₂,
giving respectively 32, 40 and 55 geometries of rank at least two under
group automorphisms and type permutations. All 226 Borel anchors terminate
and every representative passes independent parabolic recognition.

This also recovers the 1998 statement excluding M₁₂ rank at least six.
The [source comparison](research/case_study/phase6_sporadic_source_audit.md)
keeps the old papers' different hypotheses explicit. In particular M₁₁'s
classification based on all maximal element stabilizers is a different
problem. A later M₁₂ numerical table and an inspected supplementary archive
show discrepancies under the documented conventions; these are recorded
without claiming a correction to an unread original article.

**Subfield positions.** The same torsor viewpoint emphasizes relative position:
knowing the isomorphism types of several subgroups does not establish that
they can meet as prescribed. In a Suzuki group, a maximal split dihedral
subgroup determines its overlying subfield group uniquely. Two such dihedral
subgroups in one torus normalizer, sharing a reflection, force the corresponding
subfield groups into their standard simultaneous position. Their intersection
is then the group over the intersection field. A second rigidity argument
uses the center of the unique Sylow 2-subgroup containing an involution.
Together these exclude four candidate intersection patterns from 1999.

There is a complementary constructive argument. The matrices $wz(x)$ have
distinct nonzero traces $x^\theta$, giving a transversal of the nonidentity
odd-order conjugacy classes. Selecting their orders and adjusting torus
parameters supplies all prescribed prime-case patterns, including repeated
prime parameters. The higher-field patterns follow from the same field
intersections, except that one printed lattice fails RWPRI: its central
additive modules have proper invariant subspaces between the purported
maximal intersections. The subgroups do have the printed intersections, so
this is a failure of the extra axiom, not of bare embedding.

Together the two notes give proposed uniform decisions for every displayed
parameter shape. Exact coordinate checks include the intermediate subgroups
over $\mathbf F_{2^{45}}$. The
[complete decision table](research/case_study/phase5_suzuki_higher.md#e-exact-scope-of-the-proposed-resolution)
retains standard Suzuki structure and decides the printed cases individually.
The earlier assumption that the source's candidate list was exhaustive has
now been withdrawn: the following exact example lies outside it.

Choose a binary matrix $M$ with $M^4+M+I=0$ and an order-four binary matrix
$r$ with $r^{-1}Mr=M^2$. The commutative algebra $\mathbf F_2[M]$ is
$\mathbf F_{16}$. Appropriate powers of $M+\lambda I$ over two subfields
give commuting matrices $a,b$ of orders $13,41$ in $\operatorname{Sz}(2^{15})$.
Their common normalizing element $r$ gives $K=\langle a,b,r\rangle=C_{533}:C_4$.
With the standard subfield groups $S=\operatorname{Sz}(8)$ and
$T=\operatorname{Sz}(32)$, exact arithmetic gives

$$|S\cap K|=52,\quad |T\cap K|=164,\quad
|S\cap T|=20,\quad |S\cap T\cap K|=4.$$

These intersections satisfy every RWPRI maximality step, using classical
subfield and torus-normalizer maximality. The applicable printed case
requires the two Suzuki groups to meet in order eight, so it misses this
example. This is a concrete counterexample to the stated exhaustiveness;
it does not depend on assuming that list complete.

There is an especially short geometric certificate:
$K=(K\cap S)(K\cap T)$, since the product has size $52\cdot164/4=2132=|K|$.
For arbitrary subgroups, such a factorization makes every three typed cosets
in a flag share a point. The new
[Lean theorem](research/case_study/formal/RankThreeFactorization.lean)
proves that implication. Thus this example is flag-transitive as well as
firm, residually connected and RWPRI. Its matrices and maximality inputs
remain outside the formal certificate.

The same binary algebra supplies a rank-four subgroup lattice over
$\mathbf F_{2^{105}}$. The
[proof and exact witnesses](research/case_study/phase6_suzuki_realization.md)
separate the rank-three counterexample from this higher construction, whose
flag transitivity remains unproved. A corrected exhaustive classification,
relative embedding classes and publication priority remain separate work.

**Truncation by weighted contraction.** The tree model extends when types
are removed. Contract every omitted edge and give each resulting vertex
the number of original vertices merged into it. The retained edge cuts,
and hence their symmetric-group parabolics, remain exactly the same.
Conversely every positive weighted tree arises in this way, by expanding
each vertex into a tree of the prescribed size.

The weights encode the chamber stabilizer, a product of symmetric groups.
Residues are weighted subtrees. An edge joining weights $a,b$ has
$\binom{a+b}{a}$ panel elements. Three elementary tests now work in all ranks:

| Property | Exact weighted-tree condition |
|---|---|
| RWPRI | Adjacent weights are unequal, or both equal one |
| Local two-transitivity | Every edge has an endpoint of weight one |
| Rank-two intersection | Every nonleaf vertex has weight one |
| Full geometric intersection, rank at least two | The tree is a path and all internal weights equal one |

For the third row, an adjacent pair of edges with weights $a,b,c$ gives
disjointness between $a$- and $c$-subsets of an $(a+b+c)$-set. Two $c$-subsets
differing in one point have $\binom{a+b-1}{a}$ common neighbors. This is at
most one exactly when the middle weight is one. In rank at least two this
condition also forces RWPRI and local two-transitivity; rank one has its
own explicit exceptions.

For full intersection, a weighted branch gives the same kind of obstruction
as the thin claw. A path with internal weights one gives consecutive ranks
of a Boolean lattice. The union/intersection witness still has at most two
vertices, and its ranks remain among those retained. The new
[Lean theorem](research/case_study/formal/ConsecutiveShadow.lean) certifies
that last assertion for every finite universe and arbitrary query family.

For example, a path with weights $2,1,1,3$ is the inclusion geometry on
subset sizes $2,3,4$ of a seven-point set. Its panels have sizes $3,2,4$.
A path with weights $1,2,1$ has locally two-transitive panels but fails
rank-two intersection. These examples distinguish the tests rather than
assuming that one automatically implies all the others.

The [weighted-tree derivation](research/case_study/phase6_weighted_tree.md)
therefore includes every truncation of this family and the advertised
target of the 2003 truncation paper. That original full text remains
unavailable, so an exact whole-paper comparison is still outstanding.
The retained foundational identification of inductively minimal pairs is
the same one used in the unweighted derivation.

## 11. Descent turns compatible field cosets into one chamber

The torsor language becomes especially useful when the subgroups are fixed
groups of field automorphisms. It then connects the incidence problem to
classical nonabelian descent. This supplies a uniform existence argument
in every rank, without enumerating the ambient finite group.

Let $\mathbf H$ be a connected algebraic group with a Steinberg endomorphism
$F$, and put $G=\mathbf H^{F^m}$. For pairwise coprime divisors $b_i$ of
$m$, use the subgroups $S_i=\mathbf H^{F^{m/b_i}}$. The claim is a typed
Helly theorem: pairwise intersecting cosets $g_iS_i$ have a common point.

Here is the mechanism. In the semidirect product of $G$ with its specified
cyclic field action, a coset $g_iS_i$ determines the conjugate of the field
automorphism $f_i=F^{m/b_i}$ by $g_i$. Two incident cosets have a common
representative, so their associated automorphisms commute. Their orders are
coprime. All these commuting automorphisms therefore generate one cyclic
subgroup projecting isomorphically onto the corresponding field-action
subgroup.

Lang–Steinberg descent supplies a common conjugating element in $G$. The
finite-field step is particularly short. If $u\in G$ has norm one for
$\sigma=F^d$, choose $x\in\mathbf H$ with $u=x^{-1}F^d(x)$ by Lang's
theorem. Multiplying the norm factors telescopes to $x^{-1}F^m(x)=1$.
Thus $x$ is already in $G$, rather than merely in the algebraic closure.
The resulting common conjugator belongs to every original coset.

This is an actual use of descent to solve an incidence constraint. Its
substantial input is classical Lang–Steinberg theory, which remains credited
and charged as a dependency. The proof applies to the exceptional Suzuki
endomorphism as well as ordinary Frobenius powers.

One further type can be attached by independent coordinates. Suppose
$K= (V_1\times\cdots\times V_k)\rtimes B$, and
$K\cap S_i=(\prod_{j\ne i}V_j)\rtimes B$. A coset of $K\cap S_i$
inside $K$ specifies just the $V_i$ coordinate. Any tuple of such choices
has a simultaneous representative. Hence any flag containing a $K$-coset
has a common point there. Flags without that type are covered by descent.
The geometry axiom and flag transitivity follow for the enlarged family.
These are coordinates on **coset sets**; the stabilizers need not be normal.
The [Lean attachment theorem](research/case_study/formal/CosetCoordinates.lean)
checks the abstract common-point implication under precisely this coverage
hypothesis.

For Suzuki groups, a single binary four-by-four matrix algebra fixes the
relative positions of all the required tori. Its compatible cyclic torus
orders in odd field degrees are

$$\tau_d=2^d+1-((1+i)^d+(1-i)^d),$$

beginning $1,13,41,113,481$ at degrees $1,3,5,7,9$. The algebraic
centralizer is a two-dimensional torus. On its character lattice the
exceptional endomorphism has eigenvalues $1+i,1-i$; its fixed-point
determinant gives the displayed formula. Exact binary matrices fix the
choice of sign, while classical Suzuki theory supplies cyclicity and
normalizer maximality.

Fix any odd $e\ge3$ and distinct odd primes $a_i$ not dividing $\tau_e$.
Each quotient $\tau_{ea_i}/\tau_e$ has a prime divisor $\ell_i$ that is
absent from $\tau_e$, and these primes are distinct between indices.
The proof uses the fixed-torus intersection formula and an elementary
valuation identity; it does not require infinitely many prime torus orders.
In $\operatorname{Sz}(2^{e\prod a_i})$, take the prime-degree subfields
$S_i=\operatorname{Sz}(2^{e\prod a_j/a_i})$ and
$K=C_{\tau_e\prod\ell_i}:C_4$. Their intersections remove precisely the
corresponding prime coordinates. Descent and coordinate attachment prove
flag transitivity, and classical maximality gives RWPRI in every residue.
The same intersection formulas prove thickness and residual connectedness.

The [full derivation](research/case_study/phase7_suzuki_descent.md) therefore
gives an all-rank family and completes the geometry proof for the earlier
rank-four example over $\mathbb F_{2^{105}}$. A
[companion argument](research/case_study/phase7_suzuki_torus_families.md)
recovers every admissible parameter choice of the older Constructions 8
and 9, using the split torus and both nonsplit torus branches. It also
handles a selected prime dividing the base torus order: the relevant cyclic
quotients still have distinct prime indices, so ordinary CRT supplies the
coset coordinates. Other relative embeddings and a corrected exhaustive
classification remain.

The same descent argument [settles the canonical pure-subfield family](research/case_study/phase8_suzuki_subfields.md).
For distinct selected relative primes $a_1,\ldots,a_k$, put
$e=n/\prod a_i$. The geometry is always thick, residually connected and
flag transitive; it is RWPRI exactly when $e>1$. Thus its sharp rank bound
is $\min(\omega(n),\Omega(n)-1)$, where the two functions count distinct
prime factors and factors with multiplicity. This recovers Construction 11
and includes a repeated-prime boundary omitted by its printed bound.

A second application turns a maximality question into a vector-space
calculation. Inside the mixed parabolic $Q=Z_qU_tH_t$, every relevant
intersection subgroup $H$ surjects onto $Q/Z_q$. Its overgroups are exactly
$Z_VH$, where $V$ ranges over the $\mathbb F_t$-subspaces containing
$H\cap Z_q$. Maximality is therefore equivalent to codimension one.
The prescribed intersections in Construction 10 always have larger
codimension, so none can satisfy the required RWPRI residue condition.
This obstruction applies to every embedding with those intersection types,
although the bare intersection pattern itself is realizable.

## 12. A cyclic extension can obstruct a counterexample

The cyclic-extension idea is useful for lower bounds as well as constructions.
For the hypertope order conjecture, the earlier geometric reduction gives
three cyclic subgroups $A,B,C$ of $P=G'$ with the triple product property:
$abc=1$ forces all three factors to be the identity. The desired inequality
is $|A||B||C|\le |P|$. TPP alone does not make the multiplication map on
$A\times B\times C$ injective; using that shortcut would be an error.

The [metacyclic theorem](research/case_study/phase7_cyclic_tpp.md) proves the
inequality for every finite metacyclic $p$-group, for every prime $p$.
In a smallest counterexample, a central subgroup in one cyclic factor can
be quotiented away. A proper subgroup generated by two factors also reduces
the problem by induction and a coset count. Thus all three factors avoid
the center, and every pair generates the group.

If $P$ has a cyclic normal subgroup $N$ and cyclic quotient, these reductions
force $P=N\rtimes A$. The action of the cyclic complement is faithful;
otherwise its kernel would lie in the center. Write
$N=\langle x\rangle$ of order $p^m$ and $A=\langle y\rangle$ of order
$p^n$, with $yxy^{-1}=x^r$. Faithfulness gives $n\le m-1$.
A generator $x^s y^t$ of another cyclic factor must have $p\nmid s$,
because that factor and $A$ generate $P$. It must also have the same order
as its image in $P/N$, because its intersection with $N$ is trivial.

If that image has order $p^k$, raising the generator to this power requires

$$p^m\mid s(1+r^t+\cdots+r^{(p^k-1)t}).$$

For odd $p$, the geometric sum has valuation exactly $k<m$, which makes
the requirement impossible. For $p=2$, the three distinct Frattini lines
force one of the other two factors to have even $t$. That is precisely the
condition needed for the same valuation argument. A short norm calculation
has excluded an infinite class of potential counterexamples.

This proves the hypertope bound whenever $G'$ is metacyclic. A separate
exhaustion of two-generator groups of order512 extends the finite result to
hypertope groups of order at most $2^{12}$. The universal structural theorem
and the finite certificate have different scopes; neither settles the
unrestricted conjecture.

## 13. The remaining work, and how a living reduction should record it

The framework does not turn every problem into ordinary linear algebra.
Selecting a finite quotient and classifying its marked generators may require
substantial group theory. A faithful small matrix representation must still
be found. Helly conditions, exact generation, rank restrictions, and absence
of unwanted symmetries are real constraints. Cocycle equations are linear
only after the quotient and its action are fixed. Field existence arguments
can require character sums and independently checked exceptional witnesses.
These are the places where a claimed reduction must expose its remaining work.

The repository's long-term object is a living collection of such reductions,
extending through older papers and a broader network of collaborators. A
useful entry records the exact theorem and version, the replacement argument,
the inputs retained, its new consequences, and the checks available. A paper
is not counted as reduced because one lemma fits the language; each principal
result needs a derivation or an explicit remaining dependency. Student or
postdoctoral relationships also require documentation rather than inference
from coauthorship.

The model and coordinated agents can help by comparing statements, proposing
normal forms, deriving equations, finding counterexamples and writing
certificates. The output remains accountable to the same mathematical
distinctions. Internal agent agreement is a review step, not external review
or a replacement for a proof.

The evidence has several layers:

| Layer | What it establishes |
|---|---|
| Written all-parameter proof | A mathematical argument under its stated hypotheses and retained inputs |
| Symbolic identity check | An exact identity in the specified algebra, with interpretation supplied separately |
| Exhaustive finite census | Coverage of a bounded search space, conditional on its catalogue and completeness argument |
| Finite example check | Correctness of the stated instances; useful for finding errors, insufficient for a universal claim |
| Lean certificate | The exact formal theorem and assumptions in the module, with its dependency trust boundary |
| Snapshot or saved-hash check | Agreement of bytes and recorded results; no new mathematical execution |

The [fifteen Lean certificates](research/case_study/formal/README.md) cover
substantial components, including kernel transport, partition reconstruction,
connectivity propagation, field and matrix obstructions, the Suzuki word,
exact Boolean-shadow witnesses including consecutive-rank truncations,
the rank-three factorization and arbitrary-family coordinate-attachment
implications for coset Helly, separation of matrix intertwiners by an
invertible additive commutator, and vanishing of transvection-invariant forms.
They do not formalize every geometric instantiation or classification used
in the notes. [REPRODUCING.md](REPRODUCING.md) separates fresh computations
from historical reports and explains the excluded third-party source cache.

The current [scope table](research/case_study/torsor_compression_overview.md)
is the place to track which targets have complete principal-result reductions,
which have partial reductions, and which remain outside the core. Extending
the project should change those entries through new derivations and review,
with the precise mathematical claims preserved at each step.

The first [matched-proof measurement](research/case_study/phase9_L066_measurement.md)
compares the exact symmetric- and alternating-group commuting-involution
formulas outside degree six. The five orbit multiplicities give one shared
proof, followed by two short adapters to the published floor-sum formulas.
Charging shared material once and excluding an unnecessary source proposition
gives 10,668/3,192, or approximately 3.34, in normalized non-whitespace
characters. This is conditional on common background such as the
automorphisms of symmetric and alternating groups. It measures these two
arguments, and does not estimate the full corpus or the shortest possible
proofs. Rendering and background-cost sensitivity are explicit.

[Measurement](MEASUREMENT.md) specifies this accounting and a separate novelty
assessment for verified solutions of open problems. Its optional infinity
marker denotes a new resolution; an absent known proof does not supply a
literal numerical compression ratio.
