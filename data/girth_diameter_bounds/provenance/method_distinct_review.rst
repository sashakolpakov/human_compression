Distinct review of the six-layer Boolean method
==============================================

Status: DISTINCT_ACCEPTED_F009_FIXED_PATTERN_GRAPH_TO_CNF_METHOD.
This is a mathematical and complete source-code review of the exact files
below. It is not a production certificate, a finite-pattern cover, or a
claim of six-layer mass at least22. No solver, builder, controls, or proof
reader was executed by this reviewer.

Reviewed bytes
--------------

* six_layer_certificates/cnf.py: SHA256
  7631994936654ddc702d436140e6a2ea4a08e6a8b661b18fa8081c7437eb4421.
* six_layer_certificates/proof.rst: SHA256
  4eb762ff947dc3c967d85079b8f14af4f195431de275e9cee1dd7919c6cda08f.
* ../f012/graph_completion_certificate/cnf.py, the actual imported source:
  SHA256 25dcdd98ed0681e02b879bd6d723265a7c80c7396dce74b7b24611b27f91e06c.

Paths in the first two entries are relative to computation/f009; the last
is reached from that directory. The review read the entire new method and
the retained Formula, neg, and graph-builder source. The new method imports
Formula and neg only; it does not call the retained graph builder, whose
additional girth-six constraints would be inappropriate here.

Necessary-domain direction
--------------------------

Take an actual quartic, girth-at-least-five graph and six consecutive
nonsingleton original BFS layers of total21. Their first layer is not the
root layer, since that layer has only one vertex. A geodesic from a vertex
in the last layer back toward the root supplies all six anchors. The
radius-two balls of the middle two vertices lie entirely in the interval.

The accepted adjacent-ball argument gives eight distinct centres/parents,
one vertex for each occupied grid cell, and one private vertex on each side
of each missing cell. Girth at least five makes all these vertices distinct:
a repeated vertex within one parent's side would produce a triangle or
quadrangle, and a common second neighbor across the two sides is precisely
an occupied grid cell. Their union has26-m vertices. Thus m=5 needs exactly
the declared21 names, and m=6 needs those20 names and one extra X.

The geodesic parents A1 and B1 have BFS indices differing by three, so they
cannot have a common neighbor: cell11 is missing. Its geodesic endpoints
are private in their respective parent groups. Labeling those endpoints
U11 and V11 is harmless: the private names for each parent are arbitrary;
the labels do not impose an extra matching or edge between Uij and Vij.
All eight centres/parents have their complete four prescribed neighbors,
so forbidding every other incident edge is necessary.

Use actual adjacency for every remaining edge variable and the actual
local BFS index for every layer variable. Every layer contains at least
two vertices. An edge changes the index by at most one. Interior vertices
have their full degree four inside the interval. A local-layer-zero vertex
has at least one predecessor outside, hence internal degree at most three;
zero is correctly permitted, including for X. The last layer has degree at
most four here, with no required successor. Every vertex at positive local
index has a predecessor in the preceding layer. These are exactly the
asymmetric boundary conditions in the new code; no boundary regularity or
positive internal degree at local index zero has been silently assumed.

Clause implementation
---------------------

Formula.disjunction defines its result by equivalence, including the
constant and singleton cases; conjunction is its De Morgan dual. The
threshold recurrence uses the preceding entire list on the right-hand
side, and therefore computes the intended at-least-j predicates. This
checks the degree thresholds four/five and layer-size threshold two.
Formula.exactly supplies exactly one layer per vertex.

For each pair, the conjunctions describe all its literal common neighbors.
The retained at_most_one method imposes at most one such neighbor AND
returns their disjunction; its name alone would not explain the latter
interface. The new code correctly uses that returned disjunction to forbid
any common neighbor of an adjacent pair. Thus quadrangles and triangles
are excluded, while five-cycles remain allowed. Girth and degree ensure
that an actual section satisfies all these clauses after evaluating the
auxiliary gates. This is the required graph-to-satisfying-assignment
direction; no converse extension to a complete graph is asserted.

Scope still requiring acquisition
---------------------------------

The roster, variables and clause loops are deterministic for a declared
hole set. The checked method accepts only three or four distinct holes
including11. A later request must bind these exact source bytes, its exact
holes, and the actual emitted formula. A separately acquired reconstruction
and checked empty derivation are required before excluding that pattern.
An untrusted UNSAT report, even on identical-looking constraints, gives no
such credit. Covering every m5/m6 hole pattern remains a separate explicit
obligation; this review does not supply that cover or authorize a run.

The root agent authored this method. This distinct review reuses the
previously acquired adjacent-ball argument and Formula semantics, retains
their attribution, and introduces no new mathematical novelty claim.
