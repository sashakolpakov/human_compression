# The two projective special linear four-polytopes

## Abstract

We derive the classification of regular polytopes of rank at least four with
full automorphism group $\operatorname{PSL}_2(q)$ from the common projective-line reduction.
The only examples are Grünbaum's 11-cell and Coxeter's 57-cell. The proof
includes uniqueness of the marked groups, their exact universal presentations,
self-duality, face counts and the covering universality of their local maps.
The classification is due to Leemans and Schulte; the purpose of this paper
is its complete application of the shared centralizer and finite-amalgam theory.

## 1. Statement and the common theorem

Let q be a prime power. We use the string C-group convention of the companion
paper [E]: the distinguished generators are nonidentity involutions, they
commute at nonconsecutive positions, and every pair of marked subgroups has
the prescribed intersection. We retain the standard correspondence between
these marked groups and regular abstract polytopes [MS]. Group isomorphisms
preserving the ordered marking give polytope isomorphisms; reversal gives
duality. The automorphism groups below are the full flag-regular groups.

**Theorem 1 (Leemans–Schulte).** A regular abstract polytope of rank at least
four whose full automorphism group is isomorphic to $\operatorname{PSL}_2(q)$ has rank four.
It is precisely one of the following two polytopes:

| q | Polytope | Type | Facets | Vertex figures |
|---:|---|---|---|---|
| 11 | 11-cell | {3, 5, 3} | hemi-icosahedra | hemi-dodecahedra |
| 19 | 57-cell | {5, 3, 5} | hemi-dodecahedra | hemi-icosahedra |

Each row gives one marked-group and polytope isomorphism class. Both polytopes
are self-dual and universal among regular polytopes with the indicated facets
and vertex figures. Their face vectors, from vertices through facets, are
(11, 55, 55, 11) and (57, 171, 171, 57), respectively. The 11-cell has complete
edge graph $K_{11}$. Both full groups equal their even-generator subgroups.

The common theorem [E, Theorem 1] applies to the entire prime-power range.
It gives odd characteristic, rank four, and facet and vertex-figure groups
$S_4$ or $A_5$. It then supplies all six ordered rank-three marking classes and
the ten possible universal presentations, up to reversal. This uses the
retained Dickson subgroup types, the proved centralizer descent and odd-order
normalizer argument, and the exact finite computation of [E, §5]. In
particular, it already supplies the exclusion of small characteristic-two
groups; no unproved rank-three existence assertion is used here.

## 2. Exhaustion of the possible quotients

Suppose that $G=\operatorname{PSL}_2(q)$ has the required marking. The two end parabolics are
proper by IP. We apply the ten-row table of [E, Lemma 11] with its literal
markings. Every possible G is a marked quotient of one of those universal
groups. It is necessary to examine quotients as well as the groups themselves.

The four trivial rows give no marking by nonidentity involutions. In the
rows of order 60 and 24, an end parabolic equals the entire universal group.
Thus the missing endpoint generator is a word in the other three. This
same dependence survives in every quotient, contradicting IP. These two
rows are excluded even before using the ambient projective group.

In the row of order 96, the order of G must divide 96. For odd $q\ge 5$, the
smallest value of $q(q^2-1)/2$ is 60, which does not divide 96; at $q\ge 7$ the order
is already at least 168. The remaining odd value $q=3$ gives $A_4$, which cannot
contain a proper facet $S_4$ or $A_5$. The even values were excluded by the common
rank theorem. Hence the order 96 row contributes nothing.

The row of order 120 is $S_5$. Its normal subgroups are 1, $A_5$, $S_5$, so its only
proper nontrivial quotient is $C_2$. Neither $C_2$ nor $S_5$ is one of the possible
odd-characteristic $\operatorname{PSL}_2(q)$: for $q\ge 5$ the latter is nonabelian simple, and the
remaining small group is $A_4$. Thus this row also gives nothing.

The remaining universal groups are $\operatorname{PSL}_2(11)$, of order 660, and $\operatorname{PSL}_2(19)$,
of order 3420. Both are simple. Any nontrivial marked quotient is therefore
the whole group. For odd q the formula $q(q^2-1)/2$ is strictly increasing,
so the two possibilities force $q=11$ and $q=19$. This proves exhaustion for
every prime power.

Conversely, the exact presentations in those two rows have the displayed
groups and faithful distinguished markings. The common finite proof verifies
all subset-intersection identities, as well as generation and the generator
orders. Their consecutive labels are exactly 3, 5, 3 and 5, 3, 5: the presentation
bounds the orders by these primes, and the distinct involutions prevent
order 1. The correspondence [MS] therefore gives regular rank-four polytopes
with exactly those full automorphism groups and types.

Uniqueness follows at the level required by the correspondence. Each local
marking lies in one of the six complete classes in [E, Lemma 10], and each
compatible pair has its exact universal presentation. The only surviving
universal groups are simple, so every admissible quotient map is an isomorphism
preserving all four marked generators. The common reversal automorphisms
identify the two orientations of each local pair. Consequently there is one
polytope in each row, not merely one abstract group. This proves the
classification and uniqueness assertions of Theorem 1.

## 3. Local maps, geometry and universality

For clarity, the two exact presentations consist of the ordinary string
Coxeter relations with type {3, 5, 3} or {5, 3, 5}, together with

\[
 (r_0r_1r_2)^5=(r_1r_2r_3)^5=1.
 \tag{2}
\]

There are no extra relators hidden in this description: these are precisely
the two surviving presentations in the complete common table. Their local
presentations are $[3,5]_5$ and $[5,3]_5$ in the Petrie convention of [E, equation (5)].
The corresponding standard regular maps are the antipodal quotients of the
icosahedron and dodecahedron. This classical identification supplies the
names hemi-icosahedron and hemi-dodecahedron and their projective-plane
interpretation. It is retained from the geometric conventions in [LS, §5]
and [MS]. Thus the polytopes are locally projective, with the facets and
vertex figures stated in the theorem.

Each facet and vertex figure has group $A_5$ of order 60. Hence the numbers of
facets and vertices are 660/60=11 and 3420/60=57. If the common endpoint
label is m, the stabilizer of an edge is $C_2\times D_{2m}$, of order 4m: the isolated
endpoint generator commutes with the opposite adjacent pair, and IP makes
their intersection trivial. The two-face stabilizer has the same order.
Thus there are 660/12=55 edges and triangular two-faces in the first case,
and 3420/20=171 edges and pentagonal two-faces in the second. These are the
face vectors in the theorem. The actual edge-coset calculation of [E,
Lemma 11] identifies 55 distinct unordered endpoint pairs in the first case;
there are exactly 55 pairs on 11 vertices. The edge graph is therefore $K_{11}$,
not an inference from the face numbers alone.

The reversal homomorphisms in [E, Lemma 11] are automorphisms of the actual
marked groups. By [MS] they give the claimed self-dualities. The subgroup
of even-length words in the distinguished generators has index at most two
in any group generated by involutions. Our two groups are nonabelian simple,
so this subgroup is the whole group.

Finally let Q be any regular polytope with one of the stated facet and
vertex-figure pairs. Its distinguished generators satisfy the corresponding
universal presentation above. They therefore receive a marked epimorphism
from the already verified string C-group in the table. The retained
marked-epimorphism/covering theorem [MS] gives a cover from our polytope to Q.
This proves the asserted universality. The argument does not assume that a
general abstract group amalgam satisfies IP; that property was proved for
these exact universal groups. It does not require Q to be assumed finite,
since the epimorphism itself forces its group to be finite. The remaining
assertions of Theorem 1 follow. ∎

## 4. Attribution and verification boundary

The source contract is [LS, Theorems 1, 3, 4], its introductory rank restriction,
its complete ten-row Table 1 and the specified geometric properties in §5.
The 11-cell and 57-cell are the prior constructions of Grünbaum and Coxeter.
The classification belongs to Leemans and Schulte. The present application
uses the common replacement proof of [E] and supplies the complete
projective-special-linear quotient and geometry arguments above.

The exact finite computation and its program belong to the shared paper,
not to an additional computation repeated by this application. Its five
retained Lean declarations certify the abstract odd-order normalizer
obstruction. They do not certify this whole application, the matrix descent,
the finite universal orders, or the polytope correspondence. The required
GAP computation remains an explicit computational dependency.

The historical subfield-intersection lemmas and their multiplicity formulas
are unnecessary to this proof. The source's one-Petrie-relation groups and
its later discussion of two-flag-orbit constructions are outside the present
contract. No new open-question solution or historical-priority claim is made.

## References

[E] *Centralizers, facets and finite amalgams on the projective line*, companion
umbrella paper, especially Theorem 1 and Lemmas 10–11.

[LS] D. Leemans and E. Schulte, *Groups of type $L_2(q)$ acting on polytopes*,
retained arXiv:math/0606660v1 author edition, 14 pages; journal publication
*Advances in Geometry* 7 (2007), 529–539. The exact primary edition is bound
in the accompanying source contract.

[MS] P. McMullen and E. Schulte, *Abstract Regular Polytopes*, Cambridge
University Press, 2002, especially the string C-group and covering correspondence.
