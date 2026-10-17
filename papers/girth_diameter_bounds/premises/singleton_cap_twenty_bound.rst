A cap has at least twenty vertices
=================================

Proposed elementary refinement, pending distinct review. A cap means a
finite connected simple graph H of girth at least five, with one specified
vertex r of degree two and every other vertex of degree four. The acquired
singleton_cap_bound.tex proves |H|>=19. This note excludes equality, hence

  |H| >= 20.                                                   (1)

The new step is a parent-label and distance-two argument for a hypothetical
nineteen-vertex cap. No enumeration, solver, classification of regular
cages, or existence claim for a twenty-vertex cap is used.

The forced layers and parent classes
------------------------------------

Suppose |H|=19. Let a,b be the neighbors of r. Their other neighbors are
disjoint triples P={p0,p1,p2}, Q={q0,q1,q2}. These are the first two
distance layers of r, of sizes two and six. Put B=P union Q and let C be
the remaining ten vertices.

Every x in C has four neighbors of degree four, since x is not adjacent
to r. Its radius-two ball therefore has exactly seventeen vertices: the
nonbacktracking paths of lengths zero, one and two have distinct ends,
by the absence of triangles and quadrangles. If x had distance at least
four from r, this ball would miss r,a,b, leaving at most sixteen vertices.
Thus every member of C has distance exactly three from r.

Each C vertex has one or two B-parents, at most one in P and one in Q.
Call it single or double accordingly. All other neighbors of C lie in C.
There are no edges within P or within Q, and edges between P and Q form
a matching: two sharing an end would give a quadrangle through a or b.
Write m<=3 for its size. A matched B vertex has two C-children; an
unmatched B vertex has three. Consequently

  e(B,C)=18-2m,   d=number of doubles=8-2m,
  s=number of singles=2+2m.                                   (2)

Write D and S for the double and single subsets of C, and F=H[C]. In F,
each double has degree two and each single has degree three. Label a
double ij by its parents pi,qj. Such labels are unique, since repeated
labels would give a quadrangle. A matching edge pi--qi forbids label ii
by a triangle. A single is labelled by its one parent; different singles
may initially have the same label.

Two useful exact restrictions
-----------------------------

First, F[D] has no path on four distinct vertices. Along a three-vertex
path of doubles, the three first coordinates are distinct, as are the
three second coordinates: adjacent equal coordinates give a triangle,
and equal coordinates at distance two give a quadrangle through the
common B-parent. A fourth vertex must therefore have both coordinates
of the first, contradicting label uniqueness. Since double degrees in F
are two and triangles are forbidden, every component of F[D] is a path
on one, two or three vertices. Each such component has exactly two edges
to S, by subtracting its internal degree sum from twice its order.

Second, a single with parent v in B must be within distance two of EVERY
B vertex. Indeed its seventeen-vertex ball misses r and also the opposite
root-neighbor (b for a P-parent, a for a Q-parent). These are its only two
missing vertices. The opposite root-neighbor cannot be reached in two
steps: that would give the single a parent in the opposite triple.

Let delta(v) be one when v is matched in B, zero otherwise. The five B
vertices other than v are reached in two steps either through the matching
mate of v, or through one of the single's three F-neighbors. These paths
have distinct ends, by girth. Each double F-neighbor contributes two
B-parents and each single F-neighbor one. Thus, if k_x is the number of
double neighbors of this single x,

  delta(v)+3+k_x=5,
  k_x=2-delta(v),    number of single neighbors=1+delta(v).     (3)

Their parent sets are pairwise disjoint, avoid v, and, when v is matched,
avoid its matching mate. These assertions also follow directly from the
same triangle/quadrangle restrictions. In particular F[S] has degrees
one or two. If k counts singles whose parent is matched, then

  e(D,S)=2s-k,   0<=k<=s.                                    (4)

Since the total F-degree of D is 2d, (4) gives s<=2d. Formula (2) excludes
m=3. It remains to treat m=0,1,2, entirely by hand.

No matching edges: m=0
---------------------

There are eight doubles and two singles. Every single parent is unmatched,
so (3) gives exactly four D--S edges. Therefore F[D] has exactly two path
components by the first restriction. Each has at most three vertices,
which cannot accommodate eight doubles. This is a contradiction.

One matching edge: m=1
---------------------

Number it p0--q0. There are six doubles and four singles. A simple graph
on these four singles with all degrees one or two and no triangle or
quadrangle is either two disjoint edges or a four-vertex path. In the path
case its two adjacent internal vertices have degree two in F[S]. By (3)
their parents are matched, hence each parent is p0 or q0. Equal parents
give a triangle; parents p0,q0 give a quadrangle using the matching edge.
Thus this case is impossible. F[S] is two edges, and all four single
parents are unmatched.

It follows that p0 and q0 each have two double children, with labels
01,02 and 10,20 respectively. These are four distinct vertices. Each
single must be at distance at most two from p0. It is not adjacent to p0;
a two-step path cannot run through a (whose neighbors are r and P), or
through q0 (which has no single child). It must run through 01 or 02.
Hence the four singles require four incidences with these two doubles.
Each double has F-degree two, so all four available incidences are used,
one for each single. In particular 01 and 02 have no double neighbor.

Applying the same argument at q0 shows that 10 and 20 also use all four
of their F-incidences on singles. By (3), the four singles have exactly
eight double neighbors in total, so these eight incidences exhaust all
D--S edges. The other two doubles have no single neighbor and cannot
meet any of 01,02,10,20, whose F-degrees are full. They would both need
F-degree two among just themselves. Simplicity makes that impossible.

Two matching edges: m=2
----------------------

Number them p0--q0 and p1--q1. There are four doubles and six singles.
Equation (4) gives 12-k<=8, hence k>=4. The sum of F[S]-degrees is 6+k,
so k is even. The alternative k=6 would leave both unmatched vertices
p2,q2 without single children. Each needs three double children, and
their child sets have at most one common member (label22); that requires
at least five doubles, whereas there are four. Thus k=4.

Now e(D,S)=8 consumes every F-incidence of the four doubles; D is
independent. F[S] has four vertices of degree two and two of degree one.
Girth at least five forces it to be one path on six vertices: a separate
cycle could only leave either an isolated vertex or a forbidden smaller
cycle. Its endpoints have unmatched parents and its four internal vertices
have matched parents, by (3).

For a single with an unmatched P-parent, its two double neighbors use the
other two P labels and two distinct Q labels. Its sole single neighbor
must have a Q-parent. The analogous assertion holds on interchanging P,Q.
For a single with a matched P-parent, its matching mate already covers
one Q label. Its one double neighbor covers one P and one further Q label;
the remaining two single neighbors must have one P-parent and one Q-parent.
Again the symmetric assertion holds for a matched Q-parent. These facts
are exact consequences of the disjoint coverage used in (3).

Orient the six-vertex path from a P endpoint if it has one. The preceding
rules force its parent sides to be

  P, Q, Q, P, P, Q.

If the chosen endpoint had side Q the symmetric sequence results, so the
endpoints always have opposite sides and the chosen orientation is valid.
Their labels are p2 and q2. The two adjacent internal Q-labelled singles
have different parents, otherwise they form a triangle. They are therefore
q0,q1 in some order. The same holds for the two internal P-labelled singles.
Rename the matching pairs simultaneously so the Q labels occur q0,q1.
The central Q--P edge cannot join parents q1,p1, since that makes a
quadrangle with the matching edge. The full parent sequence is therefore

  p2, q0, q1, p0, p1, q2.                                   (5)

Consider the central q1-single. Its q0-single and p0-single neighbors
cover q0,p0; its parent q1 and matching mate p1 account for the other
already reached labels. Its one double neighbor must have the two
remaining parents p2,q2, hence is double22. The central p0-single likewise
has single neighbors labelled q1,p1 and matching mate q0, and requires
the same double22. Those two central singles are adjacent, producing a
triangle with double22. This final contradiction excludes m=2.

All possibilities for a nineteen-vertex cap are excluded. Together with
the acquired lower bound nineteen, this proves (1).

Application to the retained singleton-position bound
----------------------------------------------------

The prefix and suffix at an internal singleton in the F009 graph are
caps, by the previously accepted even-cut argument. Replace E*(h) in
boundary_radius_four.rst by E**(h)=max(E*(h),20); the section bounds F*
are unchanged. Among its fourteen surviving necessary singleton sets,
only the terminal length-three cap (last singleton19) previously used
the value nineteen. Thus only the following changes occur:

  singleton set     previous bound    new bound
       (19)               92              93
       (4,19)             94              95
       (14,19)            94              95.

The last two sets are excluded at total order at most94. The twelve
remaining necessary sets and bounds are

  (4):91, (8):94, (9):94, (13):94, (14):94, (18):91, (19):93;
  (4,8):94, (4,9):93, (4,18):93, (13,18):93, (14,18):94.

This is substitution into the acquired fourteen-entry table, not a graph
or profile search. The no-singleton stratum and these twelve sets remain
unresolved. No accepted root count, full order94 exclusion or source credit
is asserted. No existence or sharpness claim for order20 caps is made.

Attribution and exact premises
-----------------------------

The radius-two counting and parent restrictions are elementary and use
the prior cap/radius-four proofs. Root supplied the order19 distance-three
lead and requested this proof-only investigation; finite_recoveries derived
the exact single-parent coverage rule and the three contradictions above.
There is no historical novelty claim. Frozen prior files remain unchanged.
Paths are relative to computation/f009:

* singleton_cap_bound.tex,5930B,SHA256
  d99db438805030b2203a08a4d04ff34b23b604c36da65f80196a206a925bf61d.
* singleton_cap_bound_distinct_review.rst,3135B,SHA256
  7732d5fba9394c2866a5b116ce70ba4923c65f628b2cf653dd45445e87538113.
* singleton_cap_bound_root_review.json,2414B,SHA256
  7bd887ba2fe34ea36d5e08b0f8c4a0bfcc3c58d0ada329fcdb5963ff077a3fc0.
* boundary_radius_four.rst,11672B,SHA256
  8f9a2fbbeb527720b78d92593415283b5daeb4e0bbdda607894789271b4c2b68.
* boundary_radius_four_distinct_review.rst,5632B,SHA256
  b7b66196ef7eb2348d8228a0c9fe7afa26918c3b60815e83f1dce931852e90c5.
* boundary_radius_four_acceptance.json,6448B,SHA256
  9e18b21897516cc0632c55bbf6e210eec964b1399cd8df7abb3f15b8a265f0e6.

No scientific process, new executable, solver, enumeration, build, source
registration or CURRENT edit was performed.
