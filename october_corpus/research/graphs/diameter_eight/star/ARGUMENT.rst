A star defect is possible
=========================

Source-only mathematical analysis by /root/readme_navigation_audit,
22 October 2026. The companion adjacency list is a new independently
specified example. It is not a current payload, a census-family witness,
an ordinary-class identification or a completeness claim. No graph checker,
project function, group program, resource probe or state transition was run.
The older Source, examples, accepted gates and checkpoint remain unchanged.

1. The missing middle leaf changes the divisibility equation
------------------------------------------------------------

Retain the previous sets A=N(p_0), B=N(p_4), C=N(p_8), the independent
set I of size15 and its five-edge complement F. Suppose F is K1,5,
with center h. Since h has F-degree5, it has no I neighbor and lies in M.
A star has diameter2 and cannot meet both L and R, so interchange the
ends if necessary to put every leaf in L union M. Let t be the number
of leaves in M. Write m=|M|. The bound m<=4 gives0<=t<=m-1<=3.

The t M-leaves each have four B neighbors, omitting one B vertex.
The center h has none. Each of the other m-1-t M vertices meets all
five members of B. For b in B put d_b equal to the number of these
t leaves that omit b; thus sum_b d_b=t. The number of its M neighbors
is exactly m-1-d_b. Besides p_4 it therefore has

                         5-m+d_b

neighbors in L union R. This number is positive, so every B vertex
belongs to exactly one of B_L,B_R. Consequently

   5(|R|-4)=(5-m)|B_R|+sum_{b in B_R}d_b.               (1)

There is an extra term on the right. It need not be divisible by5.
The previous uniform obstruction cannot discard it: an M-leaf has no
F neighbor in L, and its edge to the center is consistent with disjoint
B neighborhoods of sizes4 and0.

For example m=2,t=1,|B_R|=3 and a single omitted B_R vertex give
the right side3*3+1=10, so |R|=6. Since L,R,M partition14 vertices,
|L|=6 as well. This is realized by the explicit graph below.

2. Exact literal construction
------------------------------

Use the32 labels0..31. Keep the original seed, the roots0,10 and
the middle center20. Define

  A={1..5}, B_L={21,22}, B_R={23,24,25}, C={11..15};
  L={6,7,8,9,26,27}, R={16,17,18,19,28,29}, M={30,31}.

Take h=31 and its M-leaf30. Its other leaves are6,7,26,27, so

                    F={6--31,7--31,26--31,27--31,30--31}.

The complete32 adjacency lists are in example.json. The following tables
specify the nontrivial ends independently. Vertex0 meets all A, vertex10
meets all C, and every displayed row has its center neighbor in addition
to the listed four neighbors:

  A vertex    four L neighbors       C vertex    four R neighbors
  1           6,7,8,9                11          16,17,18,19
  2           8,9,26,27              12          18,19,28,29
  3           6,7,9,27               13          16,17,19,29
  4           6,7,8,26               14          16,17,18,28
  5           8,9,26,27              15          18,19,28,29

Vertex20 meets all five members of B=B_L union B_R. Their other
four neighbors are

  21: 7,8,9,30;       22: 6,26,27,30;
  23: 18,28,29,30;    24: 16,17,28,29;    25: 16,17,19,30.

Vertex30 meets21,22,23,25,31. Vertex31 meets6,7,26,27,30.
There are no additional edges. In particular30 omits precisely B vertex24.

3. Full verification by hand
-----------------------------

Degree and simplicity. Every A or C vertex has its center neighbor
and four distinct listed neighbors. Both roots and20 have degree5.
Each B row has20 and its four listed neighbors. In L, vertices6,7,26,27
have three A neighbors, one B neighbor and31; vertices8,9 have four A
neighbors and one B neighbor. In R, vertices16,17,28,29 have three C
neighbors and two B neighbors; vertices18,19 have four C neighbors
and one B neighbor. Vertices30,31 each have the five neighbors specified
above. Every edge has distinct endpoints and is undirected; the complete
adjacency artifact lists both ends. All32 degrees equal five.

Bipartiteness and girth. Put

                   I'=A union B union C union {31}.

It has16 vertices. Every listed edge crosses from I' to its16-point
complement, so no triangle exists. The four-cycle0,1,8,2,0 is present.
The graph therefore has girth exactly four. With the original I not
including31, its induced J-edge set is exactly the stated K1,5.

Seed containment. All25 old seed edges are present: the stars at0,10,20;
the four edges1--6..9; the four edges11--16..19; and the joins9--21
and19--25. Thus the literal original root path

                   0,1,9,21,20,25,19,11,10               (2)

is present, without an assumed isomorphism or a new source embedding.

Connectivity and diameter upper bound. Every L vertex has a B_L neighbor
and every R vertex has a B_R neighbor. Hence each A or C vertex is
within two steps of B, and each root is within three. Vertices20 and30
are within one step of B, and31 is within two through30. Thus every
vertex is within three steps of B. All B vertices meet20, so every pair
of vertices is at distance at most3+2+3=8. This proves connectivity too.

Root distance and exact diameter. The displayed graph has these distance
layers from0:

  {0}; A; L; {21,22,31}; {20,30}; {23,24,25}; R; C; {10}.

Every listed edge joins consecutive displayed layers. Every vertex after
the first layer has a neighbor in the preceding layer, as the tables
show. Its distance from0 is therefore exactly its displayed layer index:
one obtains a path of that length by preceding neighbors, and no path
can cross more than one layer per edge. In particular d(0,10)=8.
Together with the preceding all-pairs upper bound, the diameter is exactly8.

The degree sums in the previous notation are

  |E(A,L)|=20, |E(B_L,L)|=6, sum_L f=4;
  |E(C,R)|=20, |E(B_R,R)|=10, sum_R f=0;
  sum_M f=6, |M|=2, t=1.

Both equations5*6=20+6+4 and5*6=20+10 hold, as does (1).
The center and middle leaf have F-degree5 and1 and B-neighborhood
sizes0 and4, respectively. They are the precise escape from the earlier
one-sided obstruction's hypothesis.

4. Consequence and limit
-------------------------

K1,5 is an attainable defect shape in this seed and target domain. A
general bipartiteness or star exclusion is therefore false. The old
equivalence between a star defect and bipartiteness remains consistent:
moving31 into I gives the explicit balanced bipartition above.

This is an independently specified positive example and a complete manual
proof, awaiting distinct review or a later explicitly granted finite check.
It does not place this graph in a current unfinished family, identify its
ordinary source-list class, alter the25,408 claim or close any family.
The original cage problem, source results and acquired seed/coverage legs
retain their attribution. No historical priority or new-conjecture claim
is made.
