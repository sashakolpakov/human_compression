# Independent review of the surface-cover theorem

10 October 2026. **Accepted within the stated scope, with no required
mathematical correction.** This review concerns the frozen phase211
manuscript and certificates. It accepts the uniform construction for
every indicated prime and its application to the four specified
two-primary families. It does not resolve the conjecture for arbitrary
polytopes.

The reviewed author manifest is `phase211_export.json`, SHA256
`636bb448db55668c72d684971eb0d452ef6c3ce415bd11e7d929e5130280a8a4`.
All twelve bound files were checked before and after replay. The complete
manuscript, both Python programs, and the actual definitions and proofs
of all six Lean declarations were read. The frozen phase109 theorem and
phase112 independent review were also read at the exact retained interface.
No original file was edited.

## Source and question boundary

The 2016 Cunningham–Pellicer Problem 5 asks for a polytope whose monodromy
group is not a string C-group but which has a unique minimal regular
polytopal cover, or a proof of nonexistence. Its formulation does not
restrict the question to finite polytopes. Cunningham's 2023 author
edition, *Chiral polytopes whose smallest regular cover is a polytope*,
was read in full. Its Section 4 supplies the general multiplicity
expectation, the earlier two degree-three covers of one 648-flag example,
and the proposed extension to the five specified tight chiral families.
These earlier observations and constructions remain attributed to their
source.

The phase211 result improves the previously reviewed two-prime conclusion
for four of those families to infinitely many finite minimal covers. It
uses every odd prime, for every source parameter and independent sign
pair. It does not newly establish the original chiral families or the
full general conjecture. The Tomotope's infinitely many minimal covers
are already proved in Monson–Pellicer–Williams, Theorem 5.9. The present
application supplies another uniform construction for that example,
not another newly answered question.

For the source-family transport I read the complete relevant frozen
phase109 proof, the phase112 review, the primary Table 2, Proposition 4.2,
and the statements and relevant construction interface of Theorems
4.8–4.10 in *Tight chiral polytopes*. The primary table was also inspected
visually to check its exponents and independent signs. I read the
Tomotope's Definition 3.1, Proposition 3.2, Example 4.3/Definition 4.4,
the literal page-9 permutations, and Theorem 5.9 with its proof. Page 9
was visually inspected. No fresh complete reading of either long primary
paper is implied by these bounded source checks.

## Written mathematical proof

The arbitrary-index kernel argument is correct. The word formulation of
the intersection property is equivalent to the quotient intersection
property when the specified subgroups are the standard word parabolics.
A relation lying in a directed union already lies in one member, which
provides the required common-parabolic representative. Normality and
containment in the target kernel are also preserved. The chain has an
admissible upper bound, and Zorn's lemma gives a maximal admissible
overgroup of any given admissible kernel. Nontriviality of the marked
involutions is supplied separately by containment in a polytope's
flag-action kernel. This is an application premise, not hidden inside
the abstract Lean definition. Uniqueness of a maximal admissible kernel
then implies that it is greatest. No closure assertion for arbitrary
joins is made.

The selected two-color disks form a genuine closed surface. Each
involution edge has two incident disks; the four permitted pairs give
the cyclic vertex link (0,2,1,3). The exact pair orders ensure embedded
polygon boundaries. The Euler count is therefore valid. The equivalence
between orientability and parity of word length follows by propagating
the local colored link orientation across an edge. The computation
checks this again through signed disk adjacency.

The descriptions of the three intersections of marked subcomplexes are
also correct. In the top pair, each component is an entire middle
two-color disk. In either local pair, each component is a single edge.
No intersection component contributes first homology. The union in
each case is connected through the identity, and is a proper subcomplex
because at least one of the other disk types is absent.

The homological intersection lemma handles both obstructions which a
mere projected-intersection test could miss. A loop formed by an
(A)-path and a (B)-path with the same lifted endpoint is null in
(H_1(X)). Injectivity from (H_1(Acup B)) makes it null there as well.
The Mayer–Vietoris boundary detects whether its two endpoints lie in
different components of (Acap B). Once they lie in the same component,
a path in that component supplies a comparison. Since
(H_1(Acap B)=0), the map from (H_1(A)oplus H_1(B)) is injective,
and both comparison loops are null. This excludes additional common
deck transformations as well as additional projected vertices.

The surface criterion in Section 4 is exact. A relative cellular
two-cycle has one free coefficient on each orientable complementary
component in odd characteristic, and none on a nonorientable component.
In characteristic two every complementary component contributes one
coefficient. For an orientable closed surface the absolute fundamental
class has nonzero restriction to every component, yielding the diagonal
line. In the nonorientable odd-characteristic case the absolute
two-homology vanishes. The long exact sequence of the pair gives exactly
the two criteria stated in the manuscript. In particular, connectedness
alone is not substituted for nonorientability of every complementary
component. The separate integral assertion is restricted correctly to
orientable surfaces.

The group of the homology cover is well defined. Paths in the Cayley
graph identify its fundamental group with the kernel of (W(q)	o G).
Backtracking gives the involution relations, and the selected disks
give exactly the nonadjacent commutations and the middle relation.
Using one disk per polygon rather than one per starting vertex changes
neither the normal closure of the boundary words nor the fundamental
group. Asphericity is not required. The mod-prime homology kernel is
characteristic in that fundamental group and hence normal in (W(q)).
The resulting finite group has the asserted elementary abelian kernel.

Applying the homological lemma to all three pairs proves both local
rank-three intersections and the top rank-four intersection. Recursive
string C-group recognition is therefore applicable; only the top
intersection has not been checked in isolation. The middle product
has exact order because the defining relation holds above and its
order is attained below.

The passage from all primes to infinitely many minimal descendants is
sound. Each constructed cover is finite, so a maximal normal subgroup
within its covering kernel whose quotient is still polytopal exists by
finite descent. Any further regular polytopal quotient over the original
polytope would also be such a finite quotient, proving global minimality.
Its degree over the nonpolytopal monodromy group cannot be one, and must
be a positive prime power dividing the constructed degree. Distinct
primes give distinct orders and thus nonisomorphic regular polytopes.
A common regular polytopal quotient would have degree dividing two
coprime powers, which is impossible. The product-of-kernels argument
uses normal subgroups and coprime finite indices; it does not assume
that arbitrary mixes or arbitrary joins preserve polytopality.

## The four-family application

The finite common group (D) and its exact markings agree with the
frozen phase109 model. Its orientable surface has Euler characteristic
(-32), so the homology kernel has dimension 34 for every prime.
Each end has 64 vertices, 96 edges, 24 disks, and eight boundary circles.
Its first Betti number is nine. Injectivity of its first homology into
the whole surface follows from the accepted top-union injection and
Mayer–Vietoris. The middle subcomplex is a disk and contributes no kernel.

Each end is an orientable surface with at least two boundary components.
An individual boundary class is primitive and nonzero; the only relation
among all oriented boundary classes is their sum. It remains nonzero
over every prime field. Consequently the outer product order is
(4ell), whereas the middle order remains four. This proves the
uniform type of the constructed cover of (D), without extrapolating
from the fields of orders three and five.

The nonsplit coprime pullback argument is valid. For an element in the
base kernel, choose an (ell)-th root inside its cyclic subgroup and
lift it to the generated parabolic. Its first coordinate lies in the
elementary abelian covering kernel, so its (ell)-th power has trivial
first coordinate and the required second coordinate. Thus every
generated parabolic is the full fiber product. Removing a lift from
the common parabolic gives the precise remaining kernel intersection.
No splitting or centrality assumption is needed.

The retained phase109 bridge proves the full monodromy order (4pqr),
polytopality of both ends, and a quotient to (D) whose two-primary
kernel detects the entire unwanted top-intersection coset. Its uniform
proof uses the exact source presentations; it does not depend on a
sample of values of (eta). The primary statements include every
(etageq5) and all four choices of the two independent signs. Rank
reversal gives the fourth, dual row without asserting self-duality.
The new theorem can therefore be transported for every odd prime.
The degree, end degrees, and type are exactly those stated in phase211.

These are retained substantial source and proof inputs. This review
does not reclassify the atomic chiral polytopes or attribute their
existence and chirality to the present construction.

## Independent finite reconstruction and formal scope

`phase218_independent.g` imports no author computation. It uses native
GAP permutation groups and reconstructs the Tomotope from the printed
twelve-point automorphisms and the primary Wythoff cosets. It checks
the primary diagram orders, both additional relations, and all
intersection pairs of its sixteen distinguished parabolics. It then
enumerates every pairwise-incident face tuple, obtaining exactly 192
flags. This is a separate route from the author's enumeration of the
two flag orbits. Flag adjacency yields a monodromy group of order 18,432.

For both models the program builds the regular Cayley cells directly.
Complement orientation is computed by signed union-find, independently
of the author's breadth-first dual-graph propagation. The results are:

| Model | ((V,E,F)) | Surface orientation | Complement disk counts | Complement orientation |
|---|---|---|---|---|
| (D) | ((256,512,224)) | orientable | (178,223,223) | all orientable |
| Tomotope | ((18432,36864,14592)) | nonorientable | (14090,14591,14591) | all nonorientable |

Every displayed complement is connected. The independent program also
checks both end cell counts and all eight boundary cycles for (D),
and all six reduced source relators at the common quotient. Their
common involution is central in the rotation image and lies outside
the middle parabolic, as required for the retained quotient bridge.

The three additional native controls reject an identity marking, a
single altered disk-orientation constraint, and omission of the second
Tomotope facet type. The original optimized-Python replay and its two
finite controls also pass. The frozen evidence records exact bindings
and outputs rather than relying on a matching summary count.

All six Lean declarations compile afresh under the pinned toolchain and
library with only the reported standard axioms. Their statements
match the intended directed-union, chain, maximal-kernel, greatest-kernel,
and coprime-power interfaces. They do not assert a correspondence with
polytopes or formalize surface topology. The negative control which
replaces coprimality by an inequality is correctly rejected. The
weakened mathematical assertion is false: in a cyclic group of order
two, the nonidentity element has its second and fourth powers in the
trivial subgroup, although the element itself is not in it.

The replay command is:

```sh
python3 -B -O phase218_check.py --out /tmp/phase218-fresh-review
```

The driver accepts explicit GAP, Lean, and package paths. It checks all
frozen author bindings, reruns the author packet, runs the independent
GAP construction and three native controls, and verifies that no frozen
input changed.

## Remaining boundary

The automatic validity of the complement criterion for every genuine
polytope monodromy group is not proved. Nor is a higher-rank replacement
for the four-color surface construction supplied. The three exploratory
bad quotients and the claim that no polytopal flag action was found in
them are outside this acceptance. No complete arbitrary-polytope
conjecture resolution, priority determination, whole-manuscript
compression credit, or fully Lean-verified topological theorem follows
from this review.
