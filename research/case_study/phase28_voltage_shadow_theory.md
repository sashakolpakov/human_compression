# Graph covers, shadow intersections, and incidence geometries

Private proposed theorem, 10 October 2026. This is a general formulation of the phase27 parity mechanism. Covering-space monodromy, voltage graphs, and their component/coset correspondence are established tools. No novelty or whole-paper claim is made. Existing phase26/27 artifacts are not changed.

## 1. Base geometry and covering data

Let $\Gamma$ be a residually connected incidence geometry of finite rank $n\ge3$, with types $\{0,1\}\cup J$. Every flag extends to a chamber. Assume:

1. Its type-$\{0,1\}$ truncation is the vertex-edge incidence of a simple graph $X$.
2. An edge is incident with a higher object $x$ if and only if both its endpoints are incident with $x$.

These are the usual B1/B2 conditions. A higher flag means a flag with types in $J$. For such a flag $F$, let $X_F$ be the graph of vertices and edges incident with every member of $F$; write $X_x=X_{\{x\}}$ and $X_\varnothing=X$. B2 makes $X_F$ the induced graph on the common vertex shadow. Every $X_F$ has an edge and is connected. The latter follows from the connected-truncation lemma proved below, applied to the residue $\Gamma_F$.

Let $p:Y\to X$ be a connected regular graph cover with deck group $A$, acting freely and transitively on every vertex fiber. Neither the group nor the graphs need be finite. A graph cover means unique lifting of a walk after its initial vertex has been chosen. In voltage coordinates, vertices have the form $(v,g)$, and an oriented edge of voltage $a$ takes $(v,g)$ to $(w,ga)$; deck transformations multiply $g$ on the left.

For $v\in X_F$, choose an $A$-equivariant torsor identification $p^{-1}(v)\cong A$ by choosing a fiber origin. Let $H_F(v)\le A$ be the subgroup of voltages of closed walks based at $v$ and contained in $X_F$. In particular,

$$H_F(v)\le\bigcap_{x\in F}H_x(v).\tag{1}$$

Changing the chosen fiber origin or transporting the base vertex along a path in $X_F$ changes these simultaneous data by the corresponding common coordinate change. All conditions below are invariant under that change. We omit $v$ when fixed.

**Established foundation.** The component/coset correspondence is the standard voltage-graph theorem attributed to Gross–Alpert and presented in Gross–Tucker, *Topological Graph Theory*, §2.5. A directly read primary treatment is S. Schluchter, [*Cosets, Voltages, and Derived Embeddings*, arXiv:1411.4358v3](https://arxiv.org/abs/1411.4358v3), §2.2 and Theorem 3.1, with the subgraph/component refinements in §3.1. We use only this elementary covering fact, and prove the required form here; no surface-embedding result is required. Schluchter works with finite graphs and groups; the allowance of infinite covers here is justified by the explicit walk-lifting proof below, not imported from an unstated infinite version of his theorem.

## 2. Two different incidence constructions

Define $\widehat\Gamma$ by retaining the vertex-edge interpretation of the cover:

- type 0 objects are vertices of $Y$;
- type 1 objects are edges of $Y$;
- a higher object over $x$ is a pair $(x,C)$, where $C$ is a connected component of $p^{-1}(X_x)$.

Lower incidence is graph incidence. A vertex or edge is incident with $(x,C)$ precisely when it belongs to $C$. Two higher objects of different types are incident when their base objects are incident in $\Gamma$ and their components share a vertex. Objects of the same type are incident only with themselves. This defines an incidence system; being a geometry will be proved, not assumed.

If $Y$ is bipartite with fixed color classes $Y_0,Y_1$, define a second incidence system $\Delta$ by replacing the lower two types:

- type 0 objects are vertices in $Y_0$;
- type 1 objects are vertices in $Y_1$;
- opposite-color vertices are incident exactly when joined by an edge of $Y$.

The higher objects and their mutual incidence are unchanged. A lower vertex is incident with a higher object when it lies in its component. Thus $\Delta$ compresses the vertex-edge incidence of $Y$ into its bipartite incidence. These constructions should not be conflated: the first has every lifted graph edge as an object; the second does not.

## 3. Exact component and compatibility calculation

Fix a higher flag $F$, a common base vertex $v\in X_F$, and a component $C_x$ over each $x\in F$. The fiber of $C_x$ over $v$ is a left coset

$$C_x\cap p^{-1}(v)=g_xH_x.\tag{2}$$

Indeed, starting at $g_x$, the points reachable over $v$ are exactly the endpoints of lifted closed walks in $X_x$, namely $g_xH_x$. Every component meets this fiber because $X_x$ is connected.

For $x,y\in F$, the components $C_x,C_y$ meet somewhere if and only if the two cosets in (2) meet. The reverse direction is immediate. For the forward direction, project a common lifted vertex to $w\in X_{\{x,y\}}$ and lift a path from $w$ to $v$ inside that connected common graph. The path stays in both components. Thus **pairwise compatibility is exactly pairwise coset intersection in one common fiber**.

If the whole coset intersection is nonempty, choose $g$ in it. Then

$$\bigcap_{x\in F}g_xH_x=gH,\qquad H=\bigcap_{x\in F}H_x.\tag{3}$$

The intersection subgraph $Z=\bigcap_{x\in F}C_x$ lies over $X_F$, and every path in $X_F$ starting at a point of $Z$ lifts entirely within $Z$. Consequently $Z\to X_F$ is a cover, with fiber $gH$ over $v$. Its connected components correspond exactly to the left cosets of $H_F$ in $H$:

$$\#\pi_0(Z)=[H:H_F].\tag{4}$$

Here the equality is an equality of cardinalities when infinite. No normality or commutativity of these subgroups is used. Every component meets the fiber, and two fiber points $gh,gh'$ are connected in $Z$ exactly when $h^{-1}h'\in H_F$, which proves (4).

Two logically distinct obstructions are now visible: the coset intersection can be empty; or it can be nonempty and split into several $H_F$-orbits.

## 4. Recognition theorem for geometry and residual connectedness

Use the following two conditions for every higher flag $F$ of the base geometry and one, equivalently every, vertex $v\in X_F$.

**H — typed coset Helly.** Every choice of cosets $g_xH_x(v)$ indexed by $x\in F$ that intersect pairwise has nonempty total intersection.

**M — common-shadow monodromy.**

$$H_F(v)=\bigcap_{x\in F}H_x(v).\tag{5}$$

The empty flag causes no extra condition: $H_\varnothing=A$ because $Y$ is connected, and the empty subgroup intersection is $A$.

**Theorem A.** The incidence system $\widehat\Gamma$ is a geometry if and only if H holds. Under H, it is residually connected if and only if M holds. If $Y$ is bipartite, exactly the same statements hold for $\Delta$.

**Geometry, necessity.** A pairwise-intersecting coset family gives a flag of higher lifted objects by (2). If the incidence system is a geometry, that flag extends to a chamber, which supplies a common lifted vertex. Transporting that vertex to the selected base vertex inside $X_F$ gives a point in every coset. This applies to either construction.

**Geometry, sufficiency.** A higher-only flag has a common lifted vertex by H. Its base flag together with that vertex extends to a base chamber. Lift its edge at the chosen vertex, and lift every additional higher object to the unique component containing that edge. This gives a chamber of $\widehat\Gamma$ extending the flag. For $\Delta$, the two endpoints of the lifted edge give its two lower objects, regardless of which color the starting vertex has.

If a flag already contains a lower vertex, extend its projected base flag to a chamber and lift at that vertex. If a flag of $\widehat\Gamma$ contains an edge, choose one of its endpoints and do the same. If it contains both vertex and edge, use that edge. A flag of $\Delta$ containing both lower types already specifies an edge of $Y$; project it with either chosen endpoint and lift the remaining base chamber objects. In every case existing higher components contain the resulting edge by unique path lifting. Thus all flags extend.

**Local residues involving lower types.** In $\widehat\Gamma$, the residue at a vertex over $v$ is isomorphic to $\Gamma_v$: each base edge at $v$ lifts uniquely, and each incident higher object has exactly one component containing the chosen vertex. Mutual incidences are preserved because all those components contain the vertex. The analogous statement at an edge is $\widehat\Gamma_{\tilde e}\cong\Gamma_e$. It restricts to any flag containing such an object.

In $\Delta$, the residue at a cover vertex over $v$ is likewise $\Gamma_v$, with its opposite-color neighbors corresponding to the base edges at $v$. This may relabel the remaining lower type. A flag containing both lower colors corresponds to a base vertex-edge flag. Thus all residues involving a lower object are residually connected without using M.

**Residual connectedness, sufficiency.** For a higher-only lifted flag, its lower truncation is the graph incidence of $Z$ in the first construction, or the bipartite graph $Z$ in the second. Formula (4) and M make it connected. Every other object in this residue is incident with some lower object, because the lifted incidence system is already a geometry. Therefore the full residue incidence graph is connected. This includes the empty flag. Together with the preceding local-residue isomorphisms, it proves residual connectedness.

**Residual connectedness, necessity.** Choose every $C_x$ to contain a fixed lift of $v$, so their common fiber is $H=\bigcap H_x$. If the lifted geometry is residually connected, the lower truncation of this flag residue must be connected by the lemma below. Formula (4) forces $[H:H_F]=1$, proving M. One must use connected truncations here: connectivity of the full residue alone would not rule out higher objects joining otherwise disconnected lower pieces.

**Connected-truncation lemma.** In a residually connected finite-rank geometry, the chamber graph is connected, and every truncation retaining at least two types is connected. For the first assertion, induct on rank. Chambers containing a fixed object are connected by galleries because its residue has smaller rank; rank-one chambers are mutually adjacent. A path in the incidence graph between objects in two given chambers, completed to chambers along its edges, joins these connected chamber families. For a retained pair of types, projecting a chamber gallery gives a walk among incident pairs, because changing one chamber object changes at most one member of the pair. Every retained object belongs to a chamber. This proves connectedness of the pair truncation, and adding the other retained types preserves it. The same argument applies inside every residue.

## 5. Firmness and thinness

Assume H, so the constructed systems are geometries. The first construction preserves firmness and thinness in both directions, by its vertex/edge residue isomorphisms and the fact that every base flag has a lift through a chosen lifted chamber.

The bipartite compression does also. Every panel of $\Delta$ contains at least one lower object: there are only $n-2$ higher types, whereas a panel flag has $n-1$ objects. Its rank-one residue is therefore a rank-one residue of the base geometry under the local identification above. Conversely, base panels missing an edge or a higher type are obtained this way by choosing a lift of a containing vertex-edge flag or vertex. Base panels missing a vertex always have exactly two completions by B1. This proves both implications. No flag transitivity is required for these assertions.

## 6. Optional group-action transfer

Suppose a type-preserving group $G$ acts chamber-transitively on $\Gamma$, and every induced graph automorphism of $X$ lifts to an automorphism of the cover. Form the full group of such lifts, retaining the chosen base automorphism as part of its data. It acts naturally on the lifted higher components. Its deck subgroup is $A$.

This group acts chamber-transitively on $\widehat\Gamma$: projected chambers are $G$-equivalent, and deck transformations act transitively on the lifts of a fixed base chamber. This conclusion requires the stated liftability assumption; an arbitrary automorphism need not lift to an arbitrary voltage cover.

For $\Delta$, assume additionally that $X$ is nonbipartite. Then the deck action on the two color classes of connected $Y$ is surjective. Otherwise every fiber would have one color, giving a bipartition of $X$. Its color-preserving subgroup $A^+$ has index two and acts regularly on the points of either color over a fixed base vertex. Every lift of a base automorphism can be made color preserving by composing with a color-swapping deck transformation. The group of color-preserving lifts therefore maps onto $G$ and acts chamber-transitively on $\Delta$. Its chamber fibers over $\Gamma$ are $A^+$-torsors. This is a statement about the given acting group, not a determination of the full automorphism group.

## 7. Exact specialization to parity

Take the canonical bipartite double cover

$$Y=V(X)\times\{0,1\},\qquad (u,i)\sim(v,1-i)\iff u\sim v,$$

with deck group $C_2$. Assume $X$ connected and nonbipartite, so $Y$ is connected. The voltage of every edge is the nonidentity element of $C_2$. For any connected shadow $X_F$,

$$H_F=1\iff X_F\text{ is bipartite},\qquad H_F=C_2\iff X_F\text{ contains an odd cycle}.$$

This assertion is specific to the canonical all-edges-odd voltage assignment; it is false for an arbitrary $C_2$-cover if phrased solely in terms of bipartiteness of the base shadow.

Cosets of subgroups of $C_2$ are either the whole group or singletons, so typed coset Helly is automatic. Condition M is automatic if any $X_x$ is bipartite, since then $H_F\le H_x=1$. In the other case it says exactly:

> For every higher flag $F$, if every individual shadow $X_x$ is nonbipartite, then the common shadow $X_F$ is nonbipartite.

Components over a higher object correspond to its even-walk classes. Their color 0 projection is the chosen class $P_x$, and their color 1 projection is its complementary class in the bipartite case, or the same whole shadow in the nonbipartite case. Higher component intersections can be tested in either color: a common vertex extends along an edge of the connected common shadow. Thus $\Delta$ is precisely the partitioned incidence system of Piedade–Tranchida, Construction 3.6 in [arXiv:2405.19050v1](https://arxiv.org/abs/2405.19050v1). Theorem A recovers the phase27 parity repair. Version-of-record and priority limits remain those in the separate [phase27 status audit](phase27_halving_version_status.md).

For larger deck groups, H is an additional genuine test. Already in $C_2^2$, the cosets $\langle e_1\rangle$, $\langle e_2\rangle$, and $e_1+\langle e_1+e_2\rangle$ meet pairwise but not jointly. This is an algebraic illustration, not a claim that this particular three-coset configuration has been realized by a base geometry here.

## 8. Focused finite diagnostic

The standalone standard-library [checker](phase28_voltage_shadow_check.py) uses a six-element permutation model of $S_3$, a $K_4$ base graph, and an explicit transposition voltage on each edge. Its connected bipartite cover has 24 vertices and 36 edges. It checks 28 component/fiber cosets and 2,350 families of connected induced shadows directly, comparing actual component intersections with (2)–(4).

For the tetrahedron's vertex-edge-face geometry, the same cover gives a graph-incidence lift with 144 chambers and a bipartite compression with 72 chambers. Every flag, every chamber-extension obligation, and every residue is checked in the base and both outputs; all panels have size two. A second connected $S_3$ cover checks a nontrivial index-two intersection: two chosen triangle components have the same order-two monodromy, while their common edge has trivial monodromy, and their intersection consists of two disjoint edges. The report also checks the elementary three-coset obstruction in $C_2^2$. These are bounded examples; they neither replace the universal proof nor assert that the illustrative $C_2^2$ cosets occur in a base geometry satisfying all hypotheses.

Run `python3 phase28_voltage_shadow_check.py --output /tmp/new-voltage-shadow-report.json` with a new output path. No source PDF, group catalogue or other workspace script is needed. The deterministic [report](phase28_voltage_shadow_check.json) binds the checker bytes.

## 9. Scope and review

The proof is self-contained after standard definitions of graph covering and incidence geometry. Its cover components and torsor coordinates are classical; the claim is an exact adapter for these two specified component-lift constructions. It neither states that arbitrary shadow lifts are geometries nor replaces flag completion by subgroup intersection. It does not assert that all regular hypertopes satisfy M automatically, classify covers, determine full automorphism groups, or establish novelty. No numerical experiment is used as a uniform proof. The complete written proof has received an independent internal review; its final hash-bound record is separate. This is not a claim of external peer review.
