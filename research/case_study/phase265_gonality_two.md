# Point cloning and the gonality-two speculation

This is a separate question-track candidate, not part of the principal-source
credit for L009. It has not yet received independent review. Graph blow-ups
and twin fibers are standard constructions; no priority is asserted for
them or for this application.

## Literal source scope

The final journal article of Delaby–Leemans–Tranchida, *Geometries with
trialities arising from linear spaces*, Algebraic Combinatorics 9(2)
(2026), 379–402, says on printed page401, after specifying input gonality
two: “However, experiments suggest that Δ(Γ) will not be residually
connected in that case.” This is an experimental suggestion, not a named
or numbered conjecture. The bound journal PDF and its hash are recorded
in `phase265_intake.md`.

The input of Construction1 is a rank-two geometry under the definitions
on pp381–383. Distinct objects of the same type are not incident. Every
maximal flag must be a chamber. The definitions do not require distinct
objects to have different neighborhoods, nor do they require the input
to be a linear space. The incidence graph is a simple bipartite graph;
simplicity does not exclude twin vertices. The example below deliberately
has twins. It makes no statement about the additional problem in which
one requires distinct point neighborhoods, or about the separate
gonality-three nonlinear question.

## The cloning lemma

Let $S=(P,\mathcal L,\in)$ be a rank-two geometry and let $a\ge2$.
Replace every point $p$ by $a$ distinct points $(p,c)$, $1\le c\le a$,
and retain every line. Put $(p,c)\in L$ if and only if $p\in L$.
Denote the resulting geometry by $S^{[a]}$. It is still a rank-two
geometry: every point and line lies on an incidence, and its maximal
flags are precisely the incident point-line pairs. If some point of $S$
lies on two distinct lines, its two clones and those lines give a
four-cycle. There are no loops or parallel edges, so the input has
gonality exactly two.

The triangle geometry $\Delta(S^{[a]})$ is exactly the independent
vertex blow-up of $\Delta(S)$, replacing each vertex by an independent
set of size $a$. Indeed, a flag of $S^{[a]}$ is $(p,c,L)$, and the two
conditions in Construction1 are

$$p\in L',\qquad p'\notin L,$$

independent of both clone coordinates. Same-type distinct vertices
remain nonincident, as required.

More generally, let $X$ be a finite-rank incidence geometry and replace
every vertex by $a$ clones of the same type, pulling back every
cross-type incidence. Every flag projects to a flag of $X$ and extends
to a chamber by lifting a base chamber, so the blow-up is a geometry.
The residue of any lifted flag is exactly the blow-up of the residue
of its projected flag: the remaining types are unchanged, and their
incidences are pulled back. Every panel size is multiplied by $a$.

If $X$ is residually connected, so is the blow-up. A connected residue
of rank at least two has no isolated vertex, since every vertex extends
to a chamber. A path between distinct base vertices lifts to a path
between any selected clones of its endpoints. Two clones of the same
base vertex can be connected through a clone of a neighboring base
vertex. This proves connectivity of every rank-at-least-two residue,
including the whole geometry. Firmness is likewise preserved.

If $X$ is flag-transitive, so is its blow-up. Lift the base automorphisms
by leaving clone labels fixed, and allow independent permutations of
the clones over every base vertex. These are incidence automorphisms.
First map the projections of two chambers by a base automorphism, then
adjust the clone label separately in each of their distinct type fibers.
The resulting automorphism sends one lifted chamber to the other.

## A literal finite counterexample

Take $S=\operatorname{AG}(2,3)$ and $a=2$. The input $S^{[2]}$ has
eighteen points, twelve lines and seventy-two incidences. Each point
lies on four lines and each line contains six points. Its graph is
simple, connected and has girth four.

The base triangle geometry $\Delta(S)$ has thirty-six vertices per
type and 432 chambers. Its rank-two residues are twelve-cycles, and it
is flag-transitive under the affine group of order432. These facts have
complete proofs in the retained incidence argument. The accompanying
program independently constructs the cloned geometry directly from the
nine-point coordinate plane and checks its asserted properties. The affine group is transitive on ordered noncollinear triples
because its linear part is transitive on ordered bases.

The cloning lemma therefore makes $\Delta(S^{[2]})$ a firm, residually
connected, flag-transitive geometry with seventy-two vertices per type
and $432\cdot2^3=3456$ chambers. Every panel has size four. Every
rank-two residue has twenty-four vertices and degree four. This gives
a counterexample to the unrestricted gonality-two suggestion using
the literal source definitions. It does not claim a counterexample
under a supplementary no-twins hypothesis.

The independent-vertex blow-up viewpoint also gives an infinite family:
every integer $a\ge2$ yields a gonality-two input and preserves the
three properties of its triangle geometry. The proof of this quantifier
is the cloning lemma; no extrapolation from the case $a=2$ is used.

The program `phase265_gonality_two_check.py` constructs the input from
coordinate incidences, implements the source triangle relation directly,
enumerates all chambers and panel sizes, checks the whole graph and
every rank-two residue, and checks a transitive chamber action by actual
permutations. It does not use a precomputed blow-up adjacency matrix as
its definition. No full Lean formalization or present-literature
priority determination is claimed.
