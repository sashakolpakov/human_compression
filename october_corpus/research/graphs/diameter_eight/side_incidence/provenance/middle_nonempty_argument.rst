Every target has a vertex in the full middle set
================================================

This proof is by /root/readme_final_check. Root proposed specializing
the existing side and port relation to m=0; the contradiction below arose
in that specialization. Root independently checked the hand argument.
Navigation supplied the earlier missing-hypergraph and cut-parity proof.
The independent-set, seed and boundary reductions are borrowed earlier
project work with their retained attribution. The degree and triangle
arguments used here are elementary; no historical priority is claimed.

This is written mathematics, prepared from Source only. No graph, family,
catalogue, enumerator, checker, solver, project/helper, guard, process or
state operation has been invoked. A separate frozen mathematical review
and any current-family certificate or adoption remain to be acquired.

1. Retained setting
--------------------

Use the exact labelled seed and target hypotheses in
../ARGUMENT.rst and ../side_boundary_decomposition/ARGUMENT.rst. Thus G
is a finite simple triangle-free 5-regular graph on 32 vertices. The
roots 0 and 10 are at distance at least 8, and the seed contains the
path

                   0,1,9,21,20,25,19,11,10.

It is therefore geodesic. The saturated centres have neighborhoods

 A=N(0)={1,...,5}, B=N(20)={21,...,25}, C=N(10)={11,...,15}.

These are disjoint and their union I is independent. Indeed a triangle
would violate neighborhood independence, while a shared neighbor or an
edge between two neighborhoods would shorten a geodesic subpath between
the corresponding centres. Put J=V(G)\I. The regular-degree identity
gives

                    |E(G[J])|=5(32-2*15)/2=5.

The three centres are isolated in G[J]. Among its other 14 vertices,
L consists of those meeting A, R of those meeting C, and M of those
meeting neither. A vertex cannot meet both A and C, since that would
give a root walk of length 4. Thus L,R,M partition those 14 vertices.
All these sets are defined in the FULL graph, not from absent edges
in a partially constructed family.

The seed puts {6,7,8,9} in L and {16,17,18,19} in R. Each A vertex
has four L neighbors besides root 0, giving 20 A--L edges. The forced
9--21 adds one more degree incidence at L, so 5|L|>=21 and |L|>=5.
Likewise |R|>=5 using 19--25. Therefore, writing

                 |L|=4+x, |R|=4+y, |M|=m,

we have x,y>=1 and x+y+m=6. The remaining labels are U={26,...,31},
and M is a subset of U. No L--R edge is possible, since it would give
a root walk of length 5. The centres have no further neighbors.

Theorem. Under these retained hypotheses, M is nonempty.

2. What m=0 would force
------------------------

Suppose for contradiction that M is empty. Each B vertex already has
neighbor 20. Its four other neighbors all lie in L union R: I is
independent, the centres are saturated, and there are no other vertices.
No B vertex meets both sides, since

                    0--a--l--b--r--c--10

would be a root walk of length 6. Partition B into B_L and B_R according
to the side containing its four noncentral neighbors. Both are nonempty
by 9--21 and 19--25. In particular

                         e(B,L)=4|B_L|.

Every L vertex has its five neighbors among A,L,B_L. If D=G[L] and
e=|E(D)|, summing its residual degree after the 20 A incidences gives

                      5x=2e+4|B_L|.                    (1)

Consequently x is even. The symmetric equation makes y even. Positive
x+y=6 leaves only (x,y)=(2,4) or (4,2). Call the side of size 6 the
small side, and for the rest of the proof call it L and its adjacent
root neighborhood A. This is a renaming within the argument, not a
permutation asserted to preserve a particular required graph H. If the
literal small side is on the right, use the symmetric proof with its
near port 25 instead of 21.

For this small side, put b=|B_L|. Equation (1) reads

                           e+2b=5.

Here e>=0 and b>=1. Therefore the only possibilities are

                         (e,b)=(1,2) or (3,1).           (2)

This reuses Navigation's cut-parity deduction. It does not assume that
either necessary case is realized. The following local bounds rule out
both.

3. Two elementary bounds on its internal graph
-----------------------------------------------

Lemma 1. Every vertex of D has degree at most 2.

Proof. A vertex v in L has some neighbor a in A. That A vertex has
four distinct neighbors in L, including v. None of the other three can
be adjacent to v, or there would be a triangle through a. Of the five
other L vertices, at least three are therefore forbidden D neighbors.
Thus d_D(v)<=2. This uses |L|=6 and that every L vertex meets A.

Lemma 2. For every edge uv of D,

                        d_D(u)+d_D(v)>=5-b.              (3)

Proof. Triangle-freeness makes N_A(u) and N_A(v) disjoint, so
d_A(u)+d_A(v)<=|A|=5. It also makes N_{B_L}(u) and N_{B_L}(v)
disjoint, giving d_{B_L}(u)+d_{B_L}(v)<=b. There are no other neighbor
classes at u or v in the m=0 case. Summing their two degree-five
equations and subtracting these two upper bounds gives

 d_D(u)+d_D(v)
   =10-[d_A(u)+d_A(v)]-[d_{B_L}(u)+d_{B_L}(v)]
   >=10-5-b.

This proves (3). Neither inequality assumes that the two neighborhoods
exhaust A or B_L, nor that G is bipartite.

4. The contradiction
----------------------

If (e,b)=(1,2), D has just one edge. Its endpoints both have D degree
1, so their sum is 2. Lemma 2 requires at least 3, a contradiction.

If (e,b)=(3,1), Lemma 2 requires degree sum at least 4 on every D edge.
Lemma 1 bounds each endpoint degree by 2. Hence every endpoint of every
edge has degree exactly 2. Each nonisolated component of the finite
simple graph D is therefore a cycle. Triangle-freeness excludes cycles
of length 3, and simplicity excludes loops and two-edge parallel cycles.
Any such component has at least 4 edges. But D has exactly 3 edges,
another contradiction.

These are all cases in (2). Thus M cannot be empty, proving the theorem.
The proof needs no incidence catalogue, Burnside count or enumeration.

5. Exact consequences and family qualifications
-------------------------------------------------

Together with x,y>=1 and x+y+m=6, the theorem gives 1<=m<=4. With a
permitted orientation x<=y the necessary coarse size triples reduce to

       (1,4,1), (2,3,1), (1,3,2), (2,2,2), (1,2,3), (1,1,4).

They are necessary size possibilities only; no existence assertion or
graph-type count is made. The earlier seven-case list remains a true
necessary superset, whose m=0 case has now been excluded by this new leg.
The earlier 51-type unmarked incidence entrypoint is unchanged and still
does not supply complete side, port or gluing libraries.

The theorem is invariant under which literal side is small. It requires
no root-exchanging automorphism of a current H. A family application must
still supply a correct embedding of the retained seed, root marks and
its complete required edge set. In particular absence of an A or C edge
in partial H does NOT establish membership in M.

A sufficient later empty-family certificate would retain that seed
embedding and, for EVERY one of the 14 active J labels, a positive H-edge
witness to A or C. Any target supergraph would then have M empty, which
the theorem forbids. Such a certificate must actually authenticate all
labels, edges and the semantic family before any adoption. No current H
or frontier was read, no such witness was acquired here, and no current
family, reservation, debt or completed-original count is changed.

The m=0 side-port relation is therefore empty for every target under
these hypotheses. There is no need to build its proposed cell generator.
The still open m>=1 port relations, both-side compatibility, all central
choices and final root/girth/diameter/class filters remain separate work.
No stronger exclusion for m=1 is asserted. No native return, census
completion, Lean proof, Original disposition or measured compression
factor is supplied by this written component.
