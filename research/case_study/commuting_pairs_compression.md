# A complete main-result reduction of the commuting-involutions paper

9 October 2026. This note replaces the proofs of all four stated main results
of Kiefer–Leemans, *On pairs of commuting involutions in Sym(n) and Alt(n)*
(2013), by finite-set orbit decomposition, two rational generating functions,
and a small exact degree-six certificate. [Primary nine-page paper](https://math.uni.lu/kiefer/Publications/Involutions.pdf).
It does not claim that finite-set orbit decomposition or Burnside theory is new.
The elementary framework is standard; the point is the complete reduction and
its extension beyond pairs. This is one paper, not dozens.

## One action decomposition

Let V be a finite elementary abelian 2-group. Every finite V-set decomposes
uniquely, up to equivariant isomorphism, as

    X = disjoint union over K<=V of m_K copies of V/K.

Indeed each transitive orbit is V/K, and, since V is abelian, its stabilizer K
does not depend on the chosen point. The multiplicities m_K therefore give
the complete invariant. The action is faithful exactly when the intersection
of those K with m_K>0 is zero. Relabeling the generators by D<=Aut(V) simply
permutes these multiplicities.

The action lies in the alternating group precisely when

    sum over hyperplanes K of m_K ell_K = 0 in V^*,

where ell_K is the nonzero F2-linear form with kernel K. This follows because
an element acting nontrivially on V/K has |V:K|/2 transpositions: only
index-two orbits contribute odd signs. Thus the alternating condition is one
linear equation, rather than a second cycle-type classification.

This is the usual decomposition of a finite group action into transitive
coset actions, the additive foundation of the Burnside ring; see, for example,
[Webb's Burnside-ring notes](https://www-users.cse.umn.edu/~webb/oldteaching/Year15-16/BurnsideRing.pdf).
The proof above is included so this application does not depend on importing
the whole theory.

## Specialization to two distinct commuting involutions

Write V=<a,b>. Its five transitive actions have stabilizers

    V, <a>, <b>, <ab>, 0,

with respective multiplicities f,x,y,z,t and sizes 1,2,2,2,4. Consequently

    N = f + 2(x+y+z) + 4t.

Two distinct nonidentity commuting involutions give a faithful V-action.
Faithfulness says that t>0 or at least two of x,y,z are positive. Forgetting
the order of a,b exchanges x and y, leaving the other coordinates fixed.
Thus representatives are exactly the nonnegative tuples with x<=y and the
displayed faithfulness condition. This classifies the objects, not only their
number. Both involutions are even exactly when x,y,z have the same parity.

Let s_n and a_n count these classes under conjugation by S_(2n), with the
involutions in S_(2n) and A_(2n), respectively. The same counts hold in degree
2n+1: every nontrivial orbit has even size, so adding or removing one fixed
point is a bijection. A direct product of geometric series gives

    S(v) = sum s_n v^n
         = 1/((1-v)^3(1-v^2)^2) - (1+v)/(1-v)^2,

    A(v) = sum a_n v^n
         = (1+v^3)/((1-v)(1-v^2)^3(1-v^4))
           - (1+v^2)/((1-v)(1-v^2)).

Here is every factor. In S, the unordered pair x<=y contributes
1/((1-v)(1-v^2)), z contributes 1/(1-v), t contributes 1/(1-v^2), and
unused fixed points contribute 1/(1-v). The unfaithful tuples have t=0 and
support of size at most one among x,y,z: they contribute the subtracted term.
In A, write x=2x'+e, y=2y'+e, z=2z'+e, e in {0,1}. The common odd shift
contributes v^3, and the same calculation gives the second formula and its
unfaithful subtraction. These are full all-degree proofs of the counts.

For N>=4, N!=6, automorphisms of S_N are inner and automorphisms of A_N are
induced by S_N. Therefore these counts are exactly the source's isomorphism
counts in Theorems 1.1 and 1.2 outside degree six. The standard automorphism
theorems are retained inputs, just as they are in the source. Small N<4 has
no pair in question. The rational series also show immediately that the two
count sequences are quasipolynomials of degree four, with periods dividing
two and four respectively, and leading terms n^4/96 and n^4/384.

The paper's nested floor sums are another coefficient description of the
same orbit set. In its proof, fixing the cycle count of a means fixing
y+z+2t. Within that support, b has x+z+2t transpositions overall; the regular
orbits account for the paired cross-transpositions. Thus the two
parameterizations are bijective. A separate exact verifier compares both
formulas over a substantial range and all the printed table entries; this is
a check on transcription, while the orbit bijection is the uniform proof.

The [standard-library verifier](commuting_pairs_formula_check.py) matches the
source's floor formulas for every half-degree 2 through 500, direct orbit
multiplicity counts through half-degree 30, and all 13 printed table rows
(with the separately certified degree-six automorphism correction).
Its [hash-bearing result](commuting_pairs_formula_check.json) records PASS.

## Degree six and the two polyhedron statements

The extra outer automorphisms in degree six fuse nine S6-conjugacy classes
to five Aut(S6)-classes, and two S6-conjugacy classes in A6 to one
Aut(A6)-class. The remaining results in the paper are Theorem 3.6 (exactly
two S6 regular polyhedra, up to isomorphism and duality) and Theorem 4.4
(none for A6).

All four finite assertions are certified by the same complete procedure:

1. Enumerate every involution of G and every distinct commuting unordered
   endpoint pair {a,c}.
2. Take the endpoint orbits under Aut(G).
3. For one pair in each orbit, take all involutions b modulo the pair
   stabilizer in Aut(G). Its action includes swapping the endpoints, so
   duality is already incorporated.
4. Retain exactly the triples generating G and satisfying
   <a,b> intersect <b,c> = <b>.

This is complete because any rank-three string C-group has commuting
distinct endpoint involutions, and the stated intersection is the standard
rank-three recognition criterion. Its two adjacent rank-two subgroups are
dihedral C-groups. Conversely every retained triple has the required IP.
The automorphism orbit reductions preserve every condition and exhaust all
possible endpoints and middle generators.

The [exact GAP certificate](commuting_pairs_exception_check.g) and
[saved output](commuting_pairs_exception_check.log) give:

| G | |Aut(G)| | Involutions | Commuting endpoint pairs | Pair orbits | Middle orbits tested | Generating triples retained |
|---|---:|---:|---:|---:|---:|---:|
| S6 | 1440 | 75 | 495 | 5 | 80 | 2 |
| A6 | 1440 | 45 | 90 | 1 | 8 | 0 |

For S6 the resulting types are {5,6} and {6,6}, with representatives

    a=(5,6), b=(2,3)(4,5), c=(1,2)(3,4),
    a=(5,6), b=(2,3)(4,5), c=(1,2)(3,4)(5,6).

Both generating triples pass IP. The certificate uses GAP's exact group and
automorphism machinery, not a floating-point or random search. The finite
case is computationally rederived rather than presented as a computer-free
proof; that change in proof method is part of the cost accounting.

## What has actually been compressed

The two main counting theorems, both exceptional degree-six counts, and both
polyhedron theorems are all recovered. The centralizer propositions follow
from the same orbit decomposition: equivariant permutations of m identical
transitive H-sets form Aut_H(H/K) wreath S_m; for a single involution this is
C2 wreath S_k times S_(N-2k), with its even-permutation subgroup for A_N.
The intermediate floor-sum lemmas are changes of coordinates in the same
classification. This is therefore a reduction of the paper's full principal
result content, rather than just a generic final transport step.

The retained external mathematics is elementary action decomposition,
automorphisms of symmetric/alternating groups, and the standard rank-three
C-group/polyhedron correspondence. The finite certificate is explicit above.
This does not diminish the historical contribution of posing and solving the
counting problem. It establishes a shorter derivation and a generalization.

The [all-rank counting theorem](elementary_action_theorem.md) makes that
generalization explicit: a single Burnside–Möbius formula counts independent
commuting r-tuples in every symmetric degree, with a linear character filter
for even generators. Its computation uses subspaces of F2^r, rather than
enumerating permutations of N points.
