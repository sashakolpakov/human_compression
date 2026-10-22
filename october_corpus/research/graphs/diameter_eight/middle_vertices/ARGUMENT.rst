Two empty current families from a local defect bound
===================================================

Author: /root/readme_navigation_audit, 23 October 2026.

The accepted snapshot at sequence 7696 contains 3960 nodes and 51 pending
representatives. The exact snapshot and acceptance references, all 51 literal
pending records, and their source joins are retained in coverage.json. This
note proves that two of those families have no target completion. It also
gives restrictions on four other current families and a cover by two classes
of extensions for each of two current parents.

These are mathematical proofs and proposals for finite certificates. No
scientific program, project helper, native graph search, guard, state
transition or adoption was invoked in preparing them. All 51 obligations
therefore remain administratively unpaid. In particular, a proof of emptiness
below is not described as an acquired native completion.

Here a small node number denotes its interned key index in this one pinned
snapshot. It does not denote its chronological creation number. The coverage
file retains the permanent family SHA, literal source record and creation
field separately. For example, indices 41 and 42 have creation numbers 55
and 56. Their permanent family identities are

  41: 021e35edf0f5186cedfedc050f06f5ba3c2b2f80a497eb37f495bc12118ddef6
  42: e9440a17723fa8ede243a51669fc01288e72d00e4406482a7760c07a61411bc5

1. The common literal seed
--------------------------

The retained family contract asks for simple 5-regular supergraphs of a
literal graph H on vertices 0,...,31, with girth at least 4 and distance at
least 8 between the marked roots 0 and 10. The final selection additionally
requires connectedness, girth exactly 4 and diameter exactly 8. There are no
further semantic forbidden pairs or conditions on search history. It is
enough to exclude the larger family given by the regularity, triangle and
root-distance conditions.

Each of the 51 pending graphs contains these same 25 edges:

* 0--i for i = 1,...,5, and 10--i for i = 11,...,15;
* 1--j for j = 6,...,9, and 11--j for j = 16,...,19;
* 20--i for i = 21,...,25;
* 9--21 and 19--25.

Thus

                    0,1,9,21,20,25,19,11,10

is an eight-edge root path. It is geodesic in every target completion.
The vertices 0, 20 and 10 already have five neighbors in the seed. Their
full neighborhoods in a completion G are therefore

              A = {1,...,5}, B = {21,...,25}, C = {11,...,15}.

The set I = A union B union C is independent. Within any one of the three
sets an edge would make a triangle. An edge from A to B, or from B to C,
would shorten one of the length-four segments of the displayed geodesic to
length three. An edge from A to C would give a root walk of length three.
Each contradicts the root-distance condition. The three sets are disjoint,
so |I| = 15. Its complement J has 17 vertices.

Let F be the graph consisting of the edges of G with both endpoints in J,
and put f(v) = deg_F(v). Counting degrees on the two sides of the independent
set gives

                 2|E(F)| = 5|J| - 5|I| = 85 - 75 = 10.          (1)

In particular, F has exactly five edges. The three centers 0, 20 and 10
are isolated in F. Write J' = J minus {0,20,10}.

Partition J' into L, R and M: L consists of the vertices meeting A, R of
the vertices meeting C, and M of those meeting neither. No vertex can meet
both A and C, since that would give a root walk of length four. A vertex
of B cannot meet both L and R, since that would give a root walk of length
six. Let B_L and B_R be the vertices of B meeting L and R, respectively.
These sets are disjoint. They are nonempty: 9 belongs to L and meets 21,
whereas 19 belongs to R and meets 25. Consequently

                         21 in B_L, 25 in B_R.                 (2)

A vertex v in M has all its I-neighbors in B, so it has exactly 5-f(v)
neighbors in B. If uv is an edge of F with both endpoints in M, the
B-neighborhoods of u and v are disjoint: a common neighbor would form a
triangle. Since B has five vertices,

                            f(u) + f(v) >= 5.                  (3)

The independent-set identity and this disjoint-neighborhood argument are
also used in the earlier defect notes. They do not assume bipartiteness,
the source census counts or a conjectural shape for F.

2. A vertex meeting both sides
------------------------------

Lemma. Suppose v in J' meets a vertex of B_L and a vertex of B_R. Then
v belongs to M, every F-neighbor of v belongs to M, and f(v) is 0 or 1.

Proof. Let b_R be a B_R neighbor of v, and choose an R neighbor r of b_R.
If v had an A neighbor a, then choosing a C neighbor c of r would give
the root walk 0,a,v,b_R,r,c,10, of length six. This is impossible. The
argument on the other side is identical, so v belongs to M.

If an F-neighbor u of v met A, the same choices would give
0,a,u,v,b_R,r,c,10, now a root walk of length seven. It too is impossible.
The symmetric argument excludes an F-neighbor in R. Thus all F-neighbors
of v are in M.

Put d = f(v). The two known B-neighbors are distinct, so d <= 3. By (3),
each of the d F-neighbors has F-degree at least 5-d. Besides its edge to v,
it therefore has at least 4-d other F-edges. No two F-neighbors of v are
adjacent, because that would form a triangle with v. The edges just counted
are consequently distinct. They can share endpoints outside the neighborhood
of v, but no edge is counted twice. Including the d edges incident with v
gives

                         |E(F)| >= d + d(4-d) = d(5-d).         (4)

For d = 2 or 3 the right side is six, contrary to (1). Hence d is 0 or 1.

The same proof gives a uniform statement for every k >= 5. Take a
triangle-free k-regular graph of order 6k+2 with an eight-edge geodesic,
and take the neighborhoods of its vertices at positions 0, 4 and 8. They
are disjoint independent sets, by the same path-shortening argument. Their
union has size 3k, its complement has size 3k+2, and the analogue of (1)
gives |E(F)| = k. Define L, R, M, B_L and B_R as above. A vertex v meeting
both B_L and B_R, together with all its F-neighbors, lies in M. If
d = f(v), then d <= k-2 and the disjoint B-neighborhood argument gives

                             |E(F)| >= d(k-d).                 (5)

For 2 <= d <= k-2 the right side is at least 2(k-2), which is larger than
k when k >= 5. Thus again d is 0 or 1. No primality assumption is needed.

The bound (5) also applies to any v in the old J whose distances from both
roots are four. Such a vertex cannot meet A or C, and an F-neighbor meeting
either would give a root walk of length at most seven using the other
length-four half. The same edge count follows. To infer d = 0 or 1 one
still needs d <= k-2, for example from two prescribed B-neighbors. Without
that additional condition, the degrees k-1 and k are not excluded by (5).

Corollary. In the fixed seed, the four edges

                        21--v, 25--v, v--u, v--w               (6)

with distinct u,v,w in J' exclude every target completion. Indeed, (2)
shows that v meets both sides, while its two prescribed F-neighbors
contradict the lemma. No further adjacency or degree conditions on u and
w are required.

This is a monotone obstruction: every same-root extension retaining the
seed and (6) has the same contradiction. The argument applies to arbitrary
ancestors or descendants when their literal edges contain this pattern.
It does not show that an ancestor is empty merely because one child is
empty; an ancestor must itself contain a witness, or have an acquired cover
all of whose children have been excluded.

3. The two current empty families
---------------------------------

Node 41 contains

                 21--26, 22--26, 25--26, 26--28, 26--29.

These edges contain (6) with (v,u,w) = (26,28,29). Directly, vertex 26
is saturated, with three B-neighbors and two F-neighbors. Each of the latter
has F-degree at least three. They cannot be adjacent to each other, so
at least 2+2+2 = 6 distinct defect edges would be needed.

Node 42 contains

                 21--26, 25--26, 26--28, 26--29, 26--30.

It contains the same four-edge witness. Alternatively, the three prescribed
F-neighbors each need F-degree at least two, requiring 3+1+1+1 = 6 edges.

The literal records are zero-based record indices 2 and 3, that is, the
third and fourth lines, of order32_queue_result/call_0006.frontier. Their
source pointers in the accepted typed snapshot are [10,2,41] and [10,3,42].
Pin 10 identifies that whole 900-byte file. The coverage retains its pin,
the whole typed values, the raw-line SHA, the creation field and the current
receiver. No canonical-label interpretation or unstated isomorphism is used.

The snapshot records parent 4 as already replaced by [39,40,41,42]. Its
permanent identity is

       95fc82499f35e83a591db9c212837b9fcd04218c3e01cf201ba9251ebd1da90e.

Combining the acquired cover with these proofs leaves only children 39 and
40 as potentially nonempty branches. The historical cover should keep all
four children. New accepted negative certificates would supply the two
additional closed proof legs.

4. The other four current applications
--------------------------------------

The complete literal scan finds a currently forced vertex meeting both
sides in exactly six pending records: 2, 6, 39, 40, 41 and 42. In each it
is vertex 26. The test uses the sets B_L and B_R forced by that particular
literal H. The coverage file retains every forced side set and every
detected witness for all 51 records. This lemma does not exclude any other
current family.

Node 39 prescribes all five B-neighbors of 26, so f(26) = 0. The lemma
does not close this family.

Node 40 prescribes B-neighbors 21, 22, 23, 25 and the single F-neighbor 28
of 26. Thus f(26) = 1, and (3) forces f(28) >= 4. The lemma also places
28 in M. Triangles exclude its four possible B-neighbors already adjacent
to 26. Its only possible I-neighbor is therefore 24. Its crossing edges
are either absent or consist of the single edge 28--24. This is a necessary
restriction, not an emptiness proof. The earlier valid star construction
rules out a general assertion that this configuration is impossible.

Nodes 2 and 6 prescribe only 21 and 25 as neighbors of 26. In every
completion its final B-neighborhood has size four or five. At least two
of 26--22, 26--23 and 26--24 must therefore be present. If exactly two are
present, its remaining neighbor lies in M, has F-degree at least four,
and can meet I only at the omitted B vertex.

5. Covers by two classes of extensions
--------------------------------------

For both literal parents 2 and 6, vertices 22, 23 and 24 have no fixed
neighbor other than 20. The isolated vertices of H are 27,...,31 in node 2
and 29,...,31 in node 6. Permuting each of these two cells preserves H and
fixes the marked roots.

Define two extensions by adding these edges:

  A: 26--22, 26--23, 26--24;
  B: 26--22, 26--23, 26--w0,

where w0 = 27 for node 2 and w0 = 29 for node 6. The two extensions cover
the ordinary isomorphism classes of target completions of H. This is not
an assertion that every labelled completion contains one of these two
labelled extensions without relabelling.

Proof. If f(26) = 0, every B-neighbor is present and the completion contains
A. Otherwise let b be the unique omitted B vertex, which belongs to
{22,23,24}, and let w be the unique F-neighbor of 26. Every vertex of J'
outside {26} and the specified isolated cell either already meets A or C,
or already meets 25. The former cannot be w because w belongs to M; the
latter cannot be w because it would form a triangle with 25 and 26. Thus
w lies in the isolated cell.

Apply the transposition interchanging b and 24, and the transposition
interchanging w and w0, omitting either when its endpoints coincide. They
have disjoint supports, preserve H, and fix both roots. The resulting graph
contains B. These explicit permutations give the required class cover.
Conversely, a target completion of either extension is a target completion
of H. Every historical final condition is preserved under the permutations.

Without quotienting, the corresponding labelled cover has 1+3|X| extensions,
where X is the isolated cell: one with all B-neighbors, and one for every
choice of omitted B vertex and F-neighbor in X. No orbit size is obtained
by division by an assumed free group action. Parent 4 has the same cover
with w0 = 28. Its two acquired representatives are precisely nodes 39 and
40: their literal edge sets equal H_4 with the respective three edges
added. These are class covers; their surviving child families are unpaid.

6. Finite certificates and remaining obligations
------------------------------------------------

The emptiness theorem is proved above, subject to independent mathematical
review. The mechanical obligations are finite: authenticate the accepted
snapshot and family contract; preserve the exact list of 51 pending records;
check the seed and four-edge witnesses in nodes 41 and 42; and verify the
literal parent 4 links and the side and permutation facts for nodes 2, 6
and 40. No new ordinary-class census or completed-leaf decoding is needed.

check_bridge.py is a separate, uninvoked standard-library checker for these
literal joins. It checks the whole snapshot and all 51 original records,
not only the two favorable examples. Its output is a mathematical certificate
result, not a Root gate or a replacement census checkpoint. The proof of
the general lemma remains written mathematics, not a Lean certification.

The separate persistence.json joins the six applications to the accepted
sequence-7727 snapshot by permanent SHA and complete literal record. All six
remain pending with the same values and creation fields; in particular the
two empty families persist. It retains the identities and order of all 51
current pending records. This is a persistence check, not a repeated theorem
scan of the later frontier. The checker validates it separately and does not
replace or modify the original sequence-7696 coverage file.

The current native/Saved grammar and the smallest honest adoption route
are described in TRANSITIONS.rst. A new algebraic proof needs an explicitly
reviewed proof kind and transition. It cannot be labelled as an old native
complete-return PASS. Until such a rule is adopted, the pending count stays
51 and the accepted snapshot, aliases and original credit stay unchanged.
No number of eliminated native cases or compression factor is claimed.

Attribution
-----------

The source authors own the original problem and census claims. The literal
seed, restoration contract, acquired typed snapshot, coverage invariant and
parent 4 replacement are borrowed acquired work. The independent-neighborhood
identity and disjoint-neighborhood count are elementary arguments also proved
in the preceding defect notes. This note contributes the local bound d(k-d),
its rooted forbidden pattern, its exact current witnesses and two explicit
class covers within this project. It makes no claim of historical priority,
Lean completion, a newly solved source conjecture or a finished census.
