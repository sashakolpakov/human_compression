# Independent review of the point-cloning counterexample

11 October 2026. **Accepted for the literal journal formulation.** The
construction gives an infinite family of counterexamples to the
gonality-two suggestion in §7 of Delaby–Leemans–Tranchida, *Geometries with
trialities arising from linear spaces*. This is an unnumbered experimental
suggestion, not a named conjecture. It is separate from recovery of the
paper's principal theorems.

## Exact source and permitted inputs

The reviewed source is Algebraic Combinatorics 9(2) (2026), 379–402,
DOI 10.5802/alco.482. The journal PDF has 25 physical pages, including its
archive cover, and SHA256
`b851c8e5fe1589ce950bb284b75eee1b5f7bc4b3f2256af84565dd6ff2b8f0b0`.
Root read printed 381–383 and 400–401, and visually checked printed 382,
383 and 401. This is a selected-source reading record, not a claim to have
reviewed the entire principal source contract here.

The definition permits distinct same-type elements with identical
neighborhoods. Construction 1 takes a rank-two geometry, without assuming
it is a linear space. Its cyclic incidence rule is exactly that the first
point lies on the second line and the second point does not lie on the
first line. The final suggestion concerns input gonality two and residual
connectedness of the resulting triangle geometry. No condition excluding
repeated neighborhoods is imposed. The stronger linear-space hypotheses
of the principal classification cannot be silently added to this final
question. Earlier preprint formulas are not substituted for the bound
journal construction.

## The complete cloning argument

Root read the entire frozen author note and literal checker. Replacing
each point by a nonempty fiber preserves rank-two geometry: every point
and every line still extends to an incidence. For a fiber of size at least
two, two copies of a point together with two distinct lines through that
point form a 4-cycle in the simple bipartite incidence graph. Thus the
input gonality is exactly two.

A triangle vertex is a flag with a type label. Cloning the input point
therefore clones each triangle vertex by the same factor. Both positive
and negative incidence clauses depend only on the projected point and
line. Consequently the claimed blow-up is an exact equality of incidence
relations, not a similarity of vertex counts or local parameters.

Every flag in the blow-up projects to a base flag with distinct types.
Lift a chamber extending that base flag, retaining the already selected
clones. This proves the geometry axiom for every flag. For the residue of
a selected flag, the available vertices are precisely all clones of the
available base vertices. Incidences among them are the same pulled-back
relation, so every residue is the corresponding graph blow-up. A base
residue of rank at least two has a neighbor at every vertex, because it
is a geometry. Paths between distinct base vertices lift. Two clones of
one vertex are joined by the two-edge route through any neighbor. This
proves connectivity of every required residue. Panel multiplicities are
multiplied by the fiber size, proving firmness and, in this application,
thickness.

Base automorphisms lift while preserving clone labels. Arbitrary
permutations within each individual vertex fiber are also automorphisms.
A base automorphism first aligns the projected chambers; independent
fiber permutations then align their clone choices. This establishes
flag transitivity without assuming the full automorphism group has been
classified. The standard graph blow-up construction retains that
attribution; the source authors retain the triangle construction and
the established affine-plane example.

## The affine-plane base and independent computations

For AG(2,3), a triangle chamber corresponds to an ordered noncollinear
triple, with its three lines determined cyclically. There are
9·8·6=432 such triples, and each is the image of the standard affine frame
under a unique affine transformation. The relevant residue can also be
seen directly: the two permitted pencils through a selected line produce
K₃,₃ with a perfect matching removed, hence a 6-cycle; its incidence
subdivision is a 12-cycle. The source's established base example and the
retained incidence proof supply this input with attribution.

The new independent code constructs lines by homogeneous equations over
F₃, rather than the author's slope representation. It defines the
journal triangle relation literally using bitset incidences. It checks
the complete global graph, every rank-two residue, every panel, every
chamber and the projection to affine frames. It verifies the blow-up
identity on every ordered pair of triangle vertices.

| Copies per point | Triangle vertices | Chambers | Residues checked | Panel size |
|---:|---:|---:|---:|---:|
| 1 | 108 | 432 | 108 | 2 |
| 2 | 216 | 3,456 | 216 | 4 |
| 3 | 324 | 11,664 | 324 | 6 |

Together these runs check 648 residues and 163,296 ordered incidence
comparisons. The original literal checker separately verifies actual
incidence automorphisms and their transitive orbit on all 3,456 chambers
in the doubled example. Both programs pass under Python `-O`, using
explicit checks. The all-integer-family conclusion comes from the
written cloning argument, not from extrapolating these three runs.

## Formal component and decision

Root added and compiled four small general Lean proofs for the actual
relation on V×F obtained by ignoring the fiber coordinate. They construct
the lifted path, join arbitrary clones of one vertex, and prove
connectedness transfer. Their statements require symmetry and a neighbor
at every base vertex. The author independently read the four statements
and proofs and confirmed their correspondence to the cloning argument.
All four compile with no axioms. A one-vertex graph and its two isolated
clones demonstrate why the neighbor condition matters.

These statements do not formalize the source incidence construction,
the residue identification, chamber transitivity or the finite example.
Those parts have the written and computational evidence above. No full
Lean counterexample theorem is claimed. The fresh combined replay passed
in 0.645 seconds with the pinned Lean and Mathlib dependencies.

The result answers the unrestricted source suggestion completely. It
does not answer the separate gonality-three nonlinear question, nor a
strengthening that requires distinct point neighborhoods. Those limits
must remain visible in the public question ledger. This admission should
add at most one question entry, explicitly described as a counterexample
to an experimental suggestion, and no principal-source recovery or
compression ratio.

A bounded four-query search on 11 October 2026 used the exact paper title
with gonality, the phrase triangle complex with gonality two, and author
names with cloning/twins. It mostly returned the source and secondary
summaries; no later primary resolution was identified. The publisher's
primary landing page was also read. This weak negative search result
does not establish priority or exclude an earlier observation. No
external peer review is claimed, and no authors were contacted.
