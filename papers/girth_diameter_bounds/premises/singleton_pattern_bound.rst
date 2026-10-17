A restriction on singleton distance layers
==========================================

Claim for independent review
----------------------------

Let G be finite, connected, simple, four-regular and of girth at least five.
Fix a vertex of eccentricity 22, with distance layers V_0,...,V_22 and
n_i=|V_i|. If |G| <= 94, at most three of its internal layers are singletons.
This is a restriction on all target graphs, not an exclusion of all of them.

Premises reused without a new enumeration are singleton_cap_bound.tex
(every connected cap with one vertex of degree two and all others degree
four has at least 19 vertices), singleton_layer_section.tex (four interior
layers between singleton layers five steps apart contain at least 18
vertices), and the elementary common-neighbor pair inequality in
layer_profile_inequalities.tex. All layers below are original BFS layers,
unless a ball is explicitly taken in an induced cap or section.

1. End caps and permitted positions
-----------------------------------

In an internal singleton layer the two adjacent cuts are positive even
numbers summing to four, so each is two. The prefix and suffix, each
including the singleton, are the connected caps in the accepted cap proof.

A cap whose boundary vertex r has a vertex x at distance at least four
has at least 20 vertices: x and its four neighbors have degree four, so
its radius-two ball has exactly 17 vertices, disjoint from r and the two
neighbors of r. If the distance is at least five, this ball is disjoint
from the nine-vertex radius-two ball about r, giving at least 26 vertices.
If the distance is at least six, it is disjoint from the first four layers
about r, which contain at least 1+2+6+6=15 vertices, giving at least 32.
The third-layer lower bound six follows from the parent-matching argument
recalled in section 2. These are lower bounds, not constructions or exact
minimum orders for any cap radius.

There is no internal singleton at index one or two, since n_1=4,n_2=12.
One at index three would make its prefix a cap of order 1+4+12+1=18,
contrary to the cap theorem. Thus the first internal singleton has index
at least four. Any internal singleton has suffix radius at least three:
all suffix distances from that singleton are the original indices minus
its index, and a cap of radius at most two has at most nine vertices.
Consequently the last internal singleton has index at most 19.

Notice the asymmetry: the layer immediately AFTER an internal singleton
has exactly two vertices. The layer immediately BEFORE it need not consist
only of its two backward neighbors. No reversed-layer equality is used.

2. Sections four layers apart
-----------------------------

Consider two internal singleton layers at indices i and i+4, and write the
induced section as u,A,B,C,v. Every section vertex other than u,v has degree
four within the section; u,v have degree two. The original forward BFS
layers give |A|=2 and |B|=6. Split B=P union Q into two triples according
to their A-parent. Edges within B form a matching between P and Q, of size
m <= 3. Every C vertex has one or two B-parents, at most one in each triple.
Put c=|C|. Degree sums give

  e(B,C)=18-2m,       e(C)=2c-10+m,       e(C,v)=2.

The first equality and at most two parents imply c>=6. A C vertex with
two parents has a unique pair label (a,b), for parents p_a,q_b. Labels are
distinct: a repeated label would give a quadrangle. Call these vertices
double-parent and the other C vertices single-parent.

Three elementary restrictions will be used.

* If m=3, number the matching p_a q_a. Double-parent labels are off-diagonal,
  and no two double-parent vertices are adjacent. Indeed an edge between
  labels (a,b),(c,d) requires a!=c,b!=d to avoid triangles and a!=d,b!=c
  to avoid quadrangles through matching edges. Then c,d would both be the
  one index outside {a,b}, contradicting c!=d.
* In any m, a single-parent vertex has at most two double-parent neighbors:
  if its parent is p_a, their first coordinates are different from a and
  from one another, by triangles and quadrangles. The Q-parent case is the
  same. The graph induced by double-parent vertices has only isolated
  vertices, edges and three-vertex paths as components. Its degree is at
  most two by the same coordinate restriction. On a path of four distinct
  double-parent vertices, each coordinate at positions 1,2,3 is distinct,
  and at 2,3,4 is distinct. Thus the fourth label equals the first, which
  is impossible. Triangles are forbidden independently.
* For m=2, number the matching p_0q_0,p_1q_1. The seven possible labels are
  01,10,02,20,12,21,22. The only allowed edges between such labels are
  22--01, 22--10, 02--21, 12--20. This follows by unequal coordinates and
  excluding cross-labels 00 and 11 (the matching-edge quadrangles). Every
  one of the seven labels is incident to at least one of these four edges.

We prove c>=9, including all cases c=6,7,8.

If c=6, then m=3 and every C vertex is double-parent. There are no C edges,
but the degree sum requires five. If c=7, then m=2 or 3. For m=2 all seven
vertices are double-parent; at most the four displayed edges can occur,
whereas six are required. For m=3 there are five double-parent and two
single-parent vertices. Every C edge touches one of the latter, whose
total internal degree is at most six, whereas seven edges are required.

Now let c=8. If m=1, all eight vertices are double-parent, so their graph
has at most floor(2*8/3)=5 edges, whereas seven are required. It remains
to consider m=2,3. Let d=18-2m-c be the number of double-parent vertices,
s=2c-18+2m the number of single-parent vertices, and t the number of the
two v-neighbors that are single-parent. Their internal degrees in C are
two or three respectively, reduced by one at either v-neighbor. The
common-neighbor pair inequality for S=C gives exactly the necessary bound

  e(C) + (18-4m) + (d+3s-2-t) + 1 <= binomial(c,2),
  equivalently 7c+m-29-t <= binomial(c,2).

Here 18-4m is the sum of binomial(B-to-C degree,2) over B; the next term
is the internal C contribution, and the last one comes from v. All other
vertices have at most one C-neighbor, or none.

For c=8,m=2 this forces t>=1. There are six double-parent and two
single-parent vertices. Removing any label from the seven-label list
leaves at most three possible double-parent edges. The two single-parent
vertices have at most four edges in total to double-parent vertices. If
they are nonadjacent, there are therefore at most 3+4=7 edges. If they
are adjacent, t>=1 bounds their combined internal degree by five; after
the two incidences of their common edge there are at most three edges
to double-parent vertices, giving at most 3+3+1=7. Both contradict the
required eight edges.

For c=8,m=3 the pair inequality forces t=2. There are four double-parent
and four single-parent vertices. The former are independent, are not
v-neighbors, and have internal C degree two. Thus there are eight edges
between the two sets, and every single-parent vertex must have exactly
two double-parent neighbors. A single-parent vertex attached to p_a or
q_a cannot have a double-parent neighbor containing index a in either
coordinate: one choice gives a triangle and the other a quadrangle through
p_aq_a. Its two double-parent neighbors must consequently be precisely
the labels (b,c),(c,b) on the other two indices. Four single-parent
vertices have only three possible parent indices. Two therefore have the
same two double-parent neighbors, a forbidden quadrangle. This proves c>=9.

Every section four layers apart thus has at least 17 interior vertices.
The proof does not assert that the bound is attained.

3. Longer gaps and the four-singleton partition
-----------------------------------------------

Internal singleton layers cannot be fewer than four steps apart. The next
two forward layers have sizes two and six, and the third has at least six:
the B matching leaves at least twelve outgoing incidences, with at most
two per child. This also excludes a singleton at each of those positions.

For a gap of five, the accepted section theorem gives at least 18 interior
vertices. For a gap of at least six, the first four forward layers contain
at least 15 vertices. The radius-two ball about the other boundary vertex
inside the section contains nine vertices. It is disjoint from those first
four layers, because distance to the first boundary is at least gap minus
two. Thus such a section has at least 24 vertices, or 22 interior vertices.
This argument uses a ball, not equality of backwards and forwards layers.

The singleton indices lie in [4,19] and have separation at least four,
so at most four occur. Suppose that four occur at s_1<s_2<s_3<s_4.
Let D=s_4-s_1; then 12<=D<=15. Put a=s_1>=4 and b=22-s_4>=3,
so a+b=22-D. Write L,R for the orders of the two end caps, including
their boundary singletons, and I for the total number of vertices strictly
between the three consecutive pairs of singleton layers. Exact counting is

  |G| = L + R + I + 2.

The final two count the singleton layers s_2,s_3; the other two singletons
are already included in L,R. All layers are accounted for once.

If D<=13, then a+b>=9 and L+R>=46. Indeed if b>=4, one cap radius is at
least five, giving 26+20; if b=3, a>=6 gives 32+19, a stronger bound.
For D=14 the cap sum is at least 40: the possibilities (a,b)=(4,4),(5,3)
give respectively 20+20 and 26+19. For D=15 it is at least 39, from
(a,b)=(4,3). Combining the section bounds gives this exhaustive small table;
gap orders may be permuted without affecting the bound:

  span D     three gaps       cap sum >=   I >=   |G| >=
  12 or 13   any permitted       46         51      99
  14         4,5,5              40         53      95
  14         4,4,6              40         56      98
  15         5,5,5              39         54      95
  15         4,5,6              39         57      98
  15         4,4,7              39         56      97

In the last line only the weaker gap>=6 bound was used. Every case has
order at least 95, proving the claim.

Scope and remaining obstruction
--------------------------------

This excludes an entire structural family: an order-at-most-94 target has
zero, one, two or three internal singleton layers. The older scalar interval
constraints have not been shown to force four such layers. Thus neither
global nonexistence at order 94 nor completion of F009 follows. The result
can restrict future layer histories and suggests treating singleton-free
long sections and separators of sizes two or three as the remaining issue.
No existing enumerator, cache, frozen request or accepted prefix is changed.

Only seven literal pair labels and the six arithmetic table rows were checked
directly with tiny integer operations; no graph search, solver, compilation,
frontier replay or external classification was used. Root supplied the
c<=7 gap-four argument and independently recognized the distance-sensitive
cap count. The c=8 exclusion and the complete partition above were prepared
here for distinct challenge. The elementary arguments are not claimed novel
in the literature. This note does not supersede the preserved earlier proofs.
