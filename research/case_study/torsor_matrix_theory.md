# Torsors, invariant partitions, and permutation matrices

9 October 2026. The proposed common object is a **regular group torsor with a
marked family of invariant partitions**. Permutation matrices represent the
torsor action; Boolean matrices represent the partitions. Keeping the
distinguished basis is essential. This is a concrete form of established
coset geometry and finite-set action theory, with exact computational and
formal consequences below; it is not a claim to have invented those subjects.

## 0. An intrinsic algebraic object, not just a choice of notation

For a finite nonempty set X, take the split commutative algebra

    A = Q^X, with coordinatewise multiplication.

Its primitive idempotents are exactly the point indicators e_x. Consequently
every Q-algebra automorphism permutes these indicators, and conversely every
permutation of X is an algebra automorphism. Thus

    Aut_Q-algebra(Q^X) = Sym(X).

This makes the permutation basis recoverable from multiplication itself.
The algebra automorphism equations are stronger than invertibility of a
linear map. It is possible to work intrinsically with this algebra instead
of repeatedly stipulating that matrix similarities must preserve the basis.

Unital subalgebras of Q^X are exactly the functions constant on the blocks of
partitions of X. To prove the nontrivial direction, define x~y when every
function in the subalgebra agrees at x and y. For each y outside the block of
x, choose f_y separating x from y. The product over those y of
`(f_y-f_y(y))/(f_y(x)-f_y(y))` is the indicator of x's block. The subalgebra
therefore contains every block indicator and all block-constant functions.
Let G act on functions by pullback, `(g.f)(x)=f(g^(-1)x)`.
G-invariant subalgebras correspond precisely to G-invariant partitions;
larger subalgebras correspond to finer partitions.

Finally, a finite G-action on X is a torsor exactly when

    X x G -> X x X,       (x,g) |-> (x,gx)

is a bijection. Its linearization on the point-indicator bases is then a
permutation matrix. Indeed, bijectivity says that for each ordered pair x,y
there is exactly one g with gx=y: precisely freeness and transitivity.

The common object can therefore be stated as a **split finite commutative
G-algebra satisfying this torsor condition, with marked invariant
subalgebras**. Its based matrix form below supplies the computations. This
algebraic reformulation and its short proofs are not part of the current Lean
certificate; the subgroup/partition theorem is.

## 1. Subgroups are precisely invariant partitions of a torsor

Choose a point in a left G-torsor X and identify X with G. For H<=G define

    A_H[x,y] = 1 if x^(-1)y belongs to H, and 0 otherwise.

This is the equivalence-relation matrix of the left cosets xH. It is invariant
under simultaneous left translation of x and y. Conversely, if an equivalence
relation R on G is left-translation invariant, put

    H = {h : R(1,h)}.

Transitivity, symmetry and invariance give 1 in H, closure under products and
inverses, and R(x,y) iff x^(-1)y in H. Thus this is an exact order-preserving
bijection between subgroups and invariant partitions, not a lossy encoding.
Changing the chosen torsor point conjugates the subgroup description; the
partition diagram itself is intrinsic.

These statements, including reconstruction in both directions, are proved
in [TorsorPartitions.lean](formal/TorsorPartitions.lean). It also checks the
zero-one Hadamard identity below; the ordinary product and rank formulas are
not included in that Lean file.

## 2. Two matrix products encode two different group operations

For any subset S of G use the same definition for A_S. For finite G,

    A_H Hadamard A_K = A_(H intersect K),
    A_H A_K = |H intersect K| A_(HK).                    (1)

The first equation is entrywise conjunction. For the second, the (x,z) entry
counts factorizations x^(-1)z=hk with h in H, k in K. When one factorization
exists, all others are (h t,t^(-1)k), t in H intersect K. Otherwise the entry
is zero. This proves (1) without requiring H and K to commute.

In particular A_H^2=|H|A_H, its row sums are |H|, and

    rank_Q(A_H) = |G|/|H|.

Indeed, ordering the basis by H-cosets gives a block diagonal matrix with
|G:H| all-ones blocks. The normalized matrix A_H/|H| is the orthogonal
averaging projection onto the functions constant on those cosets.

The Boolean transitive closure of A_H OR A_K is A_<H,K>. It therefore
computes subgroup joins, while Hadamard product computes subgroup meets.
Ordinary product records the product set HK and its multiplicity. Treating
ordinary multiplication as though it always produced a subgroup would be
incorrect; HK is a subgroup exactly when HK=KH.

Consequently the complete distinguished-subgroup intersection property

    G_I intersect G_J = G_(I intersect J)

is equivalent to the basis-aware matrix identity

    A_(G_I) Hadamard A_(G_J) = A_(G_(I intersect J)).      (2)

The equivalence itself is also checked in the Lean file. Generator relations
are equations in permutation matrices. Generation is a Boolean closure
equal to the all-ones matrix. Local group sizes are row sums, and indices
are ranks. Thus the different tests inhabit one exact matrix calculus.

There is also a computational saving: every left-translation-invariant matrix
is determined by its row at the chosen torsor point. Storing A_H means storing
only H, not |G|^2 entries. Ordinary products become group-algebra convolution,
Hadamard products become support intersection, and joins become reachability.
The matrix language therefore admits compact subgroup and normalizer
implementations; it does not require huge dense matrices for sporadic groups.

## 3. A full coset geometry needs a Helly condition

Let H_i<=G be distinguished maximal parabolics. Vertices of type i are the
blocks of A_(H_i), and vertices of different types are incident when their
blocks meet. The group acts by simultaneous left translation. Put
B=intersection_i H_i.

The following are equivalent:

* every flag is in the G-orbit of the corresponding base flag;
* every collection of pairwise intersecting blocks of distinct types has
  nonempty total intersection.

The second is a typed 2-Helly property. If a collection has common point x,
its blocks are exactly xH_i, proving the forward construction of the orbit.
Conversely every translated base flag has the translating point in all its
blocks. This proves the equivalence directly. The Helly property also makes
the incidence system a geometry, since a common point supplies the missing
types to complete any flag.

When Helly holds, chambers are the cosets G/B. If B=1, the original torsor
is exactly the chamber set. The number of completions of a panel missing
type i is

    |intersection_(j!=i) H_j : B|.

Hence thinness becomes the requirement that each such index be two. This
also explains precisely when the torsor itself, rather than a quotient of
it, parametrizes chambers.

For a base flag of type J, put K_J=intersection_(j in J) H_j. Its residue
is the coset geometry inside K_J with parabolics K_J intersect H_i for
i notin J. Here flag transitivity justifies the identification; without it
there may be additional edges or flags. A coset incidence graph of rank at
least two is connected exactly when its defining parabolics generate the
acting group. Therefore residual connectedness becomes

    K_J = <K_J intersect H_i : i notin J>

for every J whose complement has at least two types. This is again a Boolean
matrix closure test. Thinness, residual connectedness, and the coset Helly
condition are explicit tests; none is silently assumed from (2).

For standard C-group parabolics H_i=<rho_j:j!=i>, IP makes the displayed
residue-generation equalities automatic and makes every panel index two.
The outstanding geometric condition is the typed Helly property. This is
why non-string C-group constructions can fail to give regular hypertopes.

## 4. Symmetries and chirality keep the marking

A type-preserving automorphism of the partition system is a permutation
matrix P satisfying

    P A_(H_i) P^(-1) = A_(H_i) for every i.

Allowing a type permutation pi replaces the right side by A_(H_(pi(i))).
For a thin connected chamber geometry, an automorphism fixing one chamber
fixes its unique adjacent chambers, then all chambers. Thus once a group
acts regularly on chambers, it is the full type-preserving automorphism
group. The generic propagation argument is checked separately in
[ChamberOrbit.lean](formal/ChamberOrbit.lean).

For group markings, allowed generator changes are encoded by automorphisms
of a universal marked group preserving its relation kernel. A missing
reflection is therefore a stabilizer obstruction, not a failure of linear
algebra to identify two arbitrary matrices. A chiral geometry can require
two free chamber orbits; it is then built from two torsors, with the
incidence data linking them. The regular single-torsor statement should not
be incorrectly imposed on every chiral action.

For a regular thin chamber geometry, the classification itself has a precise
normal form. Its marked subgroup tuples are classified under Aut(G), with
allowed type permutations added if the labels are to be forgotten. An
isomorphism between geometries conjugates their full type-preserving groups;
after translating the image base chamber back, it induces an automorphism of
G carrying each H_i to the corresponding parabolic. Conversely any such
automorphism gives an isomorphism of the coset geometries.

More explicitly, if D_H is the subgroup of Aut(G) permuting the family of
parabolics, the full type-permuting automorphism group is G semidirect D_H.
Every automorphism has a unique translation taking its image base chamber
back, and its remaining factor fixes that chamber. This proves the splitting.
The map D_H to type permutations is injective because a type-preserving
automorphism fixing a chamber is the identity. Triality without duality is
therefore the concrete case where this permutation stabilizer has a 3-cycle
and no transposition. Computing it still requires the marked partition data.

## 5. Why ordinary linear equivalence loses information

Permutation matrices are linear, but forgetting their basis changes the
classification problem. Take V=C2 x C2 and compare the two six-point V-sets

    X = V disjoint-union two fixed points,
    Y = disjoint-union_(K a line in V) V/K.

Their orbit sizes are respectively 4+1+1 and 2+2+2, so they are not
isomorphic as V-sets. Nevertheless their rational permutation modules are
isomorphic: both have three trivial characters and one copy of each of the
three nontrivial characters.

Explicitly, on X take a=(12)(34), b=(13)(24); on Y take
a'=(34)(56), b'=(12)(56). With permutation matrices acting on column vectors,
the following integer matrix intertwines both pairs:

    T = [[ 2, 2, 0, 0, 0, 0],
         [ 0, 0, 2, 2, 0, 0],
         [ 1,-1, 1,-1, 4, 0],
         [-1, 1,-1, 1, 4, 0],
         [ 1,-1,-1, 1, 0, 4],
         [-1, 1, 1,-1, 0, 4]],

with det(T)=-2048. It is invertible over Q, but is not a permutation matrix.
Thus simultaneous similarity over Q would identify two different actions.
The Hadamard algebra and distinguished basis retain the missing information.
This is also the basic Burnside-ring relation
[V/0]+2[V/V]=sum_(K a line)[V/K] after passage to rational representations.

## 6. An actual normal form, and a whole-paper application

Every finite G-set is a multiset of transitive quotients G/H, indexed by
conjugacy classes of subgroups. This gives a complete normal form for the
action: a vector of nonnegative integer multiplicities, with total size
sum m_H |G:H|. For an abelian G the subgroups themselves index the entries.
The faithful actions are those whose occupied stabilizers have cores with
trivial intersection, where core_G(H)=intersection_g gHg^(-1). For abelian G
the cores are the stabilizers themselves. Relabeling generators acts on this
vector through Aut(G).

For G=F2^r, the sign character of the action is the sum modulo two of the
linear forms belonging to occupied hyperplane quotients, counted with their
multiplicities. This turns alternating-group constraints into linear parity
conditions on the normal form.

For r=2 there are only five orbit types. The resulting five-coordinate
normal form, two geometric-series products, and a degree-six certificate
recover **all principal results** of the 2013 commuting-involutions paper.
The complete [paper reduction](commuting_pairs_compression.md) supplies the
formulas, exceptional automorphism orbits, and both polyhedron classifications.
This is a substantive use of the torsor perspective: the case-by-case
centralizer enumeration is replaced by one finite-set decomposition, and
the same statement immediately covers larger elementary abelian groups.

The [all-rank counting formula](elementary_action_theorem.md) implements that
extension with Möbius inversion on the subspace lattice and a sign-character
filter. Exact counts for ranks three and four are included; the computation
depends on the small acting vector space, not on enumerating S_N.

The independent [matrix checker](torsor_matrix_check.py) verifies the meet,
product and Boolean-join identities for all 900 ordered subgroup pairs of
S4, including 518,400 ordinary-product entries. It also verifies the explicit
linear-equivalence counterexample above and an 18-element C-group whose
coset system fails the Helly condition in nine of its 27 chambers. The latter
checks that the geometric condition is genuinely needed. All checks pass in
the [saved report](torsor_matrix_check.json).

## What is and is not solved by the object

This is a complete exact language and recognition theorem for the indicated
coset structures. It also gives normal forms for finite group actions, which
produce real counting reductions. It does not make every group-specific
generation theorem, subgroup classification, minimality bound or numerical
enumeration automatic. Those inputs can now be isolated, reused and checked.
An actual multi-paper compression must show that the inputs themselves have
been derived or supplied by short independent certificates, rather than
simply placing each original theorem into a matrix hypothesis.
