# A cyclic counterexample to the unrestricted local-connectivity lemma

This is a correction to the first equivalence of L092 Lemma3, printed p566. The lemma allows an arbitrary thick connected rank-two geometry S. It asserts that connectivity of the proper-triangle neighbor graphs for S and its dual is equivalent to residual connectivity of Construction3. The implication toward Construction3 fails in that generality.

The example below is the classical cyclic 2-(11,5,2) design, given directly by its difference set so that its properties do not depend on recognizing a named biplane. The contribution here is its application to the precise printed claim and the explicit finite proof. It is not presented as a new design or an open-conjecture resolution.

Let the points and line labels both be Z/11Z, put
\[
D=\{1,3,4,5,9\},
\]
and let line a have point set D+a. Thus x is incident with a exactly when x−a∈D.

**Proposition.** This incidence geometry is thick and connected. It and its dual satisfy the source's property (Δ). Nevertheless Γ(S) has no incidence between a flag object and a line object. The residue at the flag object (1,D) consists of four isolated points, so Γ(S) is not residually connected and is not a geometry.

**Proof.** Every point lies on five lines and every line contains five points. Among the20 differences d−e with d,e∈D and d≠e, each nonzero element of Z/11Z occurs exactly twice. Consequently every pair of distinct points is on exactly two lines, and every pair of distinct lines meets in exactly two points. In particular S is connected.

It suffices first to check (Δ) at0. Every other point is collinear with0. The five lines through0, with0 removed, are
\[
\{3,5,6,7\},\quad
\{4,7,9,10\},\quad
\{1,5,8,10\},\quad
\{1,2,6,9\},\quad
\{2,3,4,8\}.
\]
Since every point pair is collinear, an edge {x,y} is near0 exactly when no set in this list contains both x and y. In particular the following nine edges are near0:
\[
13,\ 14,\ 17,\ 39,\ 3\,10,\ 45,\ 46,\ 72,\ 78.
\]
They form a spanning tree on the ten vertices1,…,10: vertices3,4,7 join the root1, and respectively attach9,10;5,6;2,8. Thus the neighbor graph is connected. Translation by any element preserves the incidence relation and takes0 to the corresponding point, so (Δ) holds at every point.

The design is explicitly self-dual. Map a line label a, viewed as a point of the dual, to the point −a; map a point x, viewed as a line of the dual, to the line label −x. The incidence test remains x−a∈D. This is a type-preserving isomorphism from S* to S, proving (Δ) for the dual as well.

In Construction3 a flag object (p,a) is incident with line b only if (D+a)∩(D+b)={p}. The intersection has size5 when a=b and size2 otherwise, so this never happens. For the particular flag (1,0), the remaining point objects are D∖{1}={3,4,5,9}; there are no remaining line objects. Hence its rank-two residue has four isolated vertices and is disconnected. ∎

The point-neighbor graphs are in fact the Petersen graph, but that recognition is unnecessary: the displayed spanning tree proves exactly the needed premise. The original incidence geometry has multiple lines through each point pair, so it is not a partial linear space. Thus this counterexample does not refute the restricted principal classification in L092 Theorem1. The direct proof B.Necessity already establishes that theorem without using the false unrestricted equivalence.

The file formal/CyclicBiplaneDelta.lean uses the literal ZMod11 difference-set incidence relation. It verifies thickness, pairwise collinearity, the line intersection sizes, and paths of length at most two between every pair of vertices in each primal and dual neighbor graph. It then defines the actual Construction3 residue at (1,0), proves that its edge relation is empty, and proves it is disconnected using two distinct residual points. This is a separate certificate from the Witt derivative maps and from the phase182 q=4 correction.

The corrected replacement should retain an exact residue-incidence connectivity test in the unrestricted rank-two setting. It must not substitute neighbor-graph connectivity after collapsing flag objects without controlling the fibers of that collapse. No maximal weakening of the hypotheses, or new unrestricted iff criterion beyond the literal residue test, is claimed here.
