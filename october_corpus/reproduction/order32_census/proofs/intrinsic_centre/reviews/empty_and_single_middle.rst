Independent mathematical review of the empty and singleton middle cases
======================================================================

Reviewer: /root/status_audit. This reviews the frozen30,222-byte76a5c09c
manuscript. Only written mathematics, ordinary metadata and whole hashes
were inspected. No graph, state, Source, control, TeX or Lean was executed.

Exact assumptions and dependency
-------------------------------

The graph is connected, simple, triangle-free,5-regular and of order32,
with a fixed shortest path of length8. A,B,C are its neighborhoods at
positions0,4,8, and the sides and middle are defined in the COMPLETE graph.
No initial global diameter upper bound is needed. The exact singleton
isolation proof4381b917 and its independently reviewedf13282fd leg are
retained as imports. This note does not replace an unacquired partial
family profile by a full-graph hypothesis.

The setup is consistent: I has15 independent vertices, J has17, K has14,
and F has5 edges. Each endpoint row is an independent4-set in its side.
Positive endpoint incidence gives Delta(D)<=n-4. For an internal edge uv,
the independent rows give alpha(u)+alpha(v)<=5 and beta(u)+beta(v)<=b;
substituting the degree equations gives both displayed row inequalities.
Equality in the total bound indeed makes EVERY row hit exactly one end.

Empty middle
------------

When M is empty, all B ports have4 independent side neighbors and belong
to exactly one nonempty side-port part. The side equation5n=20+4b+2e
forces even side sizes; since both sides have at least5 vertices and
sum14, they must have orders6 and8. The order6 side has (e,b)=(3,1)
or(1,2), and Delta<=2.

For e=1, the edge endpoints need8 external incidences from7 independent
rows, a contradiction. For e=3, the triangle-free maximum-degree2 shapes
are P4+2isolates, P3+K2+1isolate, or3K2. The last has no independent4-set.
In the first shape every independent4-set contains BOTH fixed isolates;
in the second it contains the unique fixed isolate. Thus the same
isolate receives all6 external rows, contradicting degree5. This confirms
the manuscript's retained side obstruction, including its fixed-vertex
quantifier. M0 is impossible under the stated full-graph assumptions.

Singleton structure and the six forms
------------------------------------

The imported isolation theorem gives h isolated in F and N(h)=B. The
two core vertices are nonadjacent false twins. Every port now has3 side
neighbors. The equations on sizes, edges and port counts give only the
initial5/8 and6/7 alternatives. The edge inequality eliminates the5-side
single edge and the6-side matching. Hence the6-side is P3+3isolates and
the7-side is one of the four triangle-free3-edge shapes. The earlier17
patterns are only potential shapes;13 are excluded, with no unsupported
assertion that each remaining right shape is realizable.

On the6-side, equality on each P3 edge forces every external row to meet
the path in its center alone or its two endpoints. If r endpoint rows
contain the center, its degree gives3-r such port rows and r-1 port rows
through the endpoints, so1<=r<=3. The isolate column equations force
exactly beta(q) omissions of each isolate among the endpoint rows. This
gives two orbits for each r, precisely the six stated local forms.
Every form satisfies all vertex degrees and positive endpoint incidence.
The P3 endpoints have identical full neighborhoods, as stated.

The converse construction retains the essential INDIVIDUAL condition
alpha_D(v)=5-d_D(v)-beta_D(v)>=1. Nonnegative columns alone would allow
an extra middle vertex and would not establish exactM1. The construction
with this positive condition is complete and sound: every adjacency is
specified, all degrees are5, row independence forbids triangles, both
regions are connected, and repeated endpoint pairs among30 pair-incidences
give a4-cycle. Removing the core separates the endpoints; each endpoint
is exactly4 from each core vertex. Therefore their distance is exactly8
through the designated middle.

Automatic diameter and intrinsic center
---------------------------------------

The eccentricity proof is valid and uses the stronger feasibility result.
An edge's endpoint degree sum is at most e(D)+1<=4. The first row bound
therefore forces positive port incidence at at least one endpoint, so
port support is a vertex cover. A port-supported side vertex is within2
of the core, an unsupported nonisolated vertex within3, and an unsupported
isolate is a false twin of its endpoint and within4.

On size6 every independent endpoint4-row meets port support of size>=3.
On size7 an endpoint row avoiding support forces that support to be a
3-set equal to every port row. Its4-vertex complement is independent too;
all3 internal edges cross the two sets. That row therefore has a neighbor
within3 of the core, putting the row within4. All other vertex types have
the listed distances. Thus both core vertices have eccentricity4 without
any separate diameter filter.

For a vertex in either region, every path to the opposite endpoint must
meet the core. False twins make its distances to the two core vertices
equal, giving d(v,opposite endpoint)=d(v,core)+4. Every noncore vertex
therefore has eccentricity>=5. The center is EXACTLY the two core
vertices. The same argument for a previously isolated-middle stratum of
diameter8 proves its stated intrinsic center size; the manuscript does
not infer isolation of larger middle sets from this observation.

Ordinary factorization
----------------------

Deleting the intrinsic center leaves connected halves of orders14 and16.
Their ports are precisely their degree3 vertices, and all other half
vertices retain degree5. Thus any uncolored half isomorphism preserves
the port set. The six14-half boundary-distance vectors are, in table order,

    (2,3,7,2), (2,4,7,1), (2,5,5,2),
    (2,6,5,1), (2,3,6,3), (2,4,6,2).

These follow directly from port support, unsupported path vertices,
endpoint rows and zero-port isolates; they agree with independent symbolic
derivation. They are pairwise different, so forgetting the marked endpoint
cannot merge the six covering local forms.

The set H16 is explicitly the unrooted halves admitting a feasible right
presentation, not every graph of its degree sequence. For any pair of
allowed halves, joining two new core twins to all five ports gives a
valid target graph. Conversely an ordinary isomorphism preserves the
center and the components, whose orders distinguish them. All independent
half isomorphisms and the center swap extend. This proves both the
ordinary-class bijection6*H16 and Aut(G)=S2 x Aut(H14) x Aut(H16), with no
root-multiplicity division and no uncomputed port alignment.

No numerical h16 value or complete ordinary count is established. Different
right-side presentations must still be identified as uncolored half
graphs. The nonbipartite conclusion also checks: a bipartite order32
quintic graph has a remaining opposite-color vertex outside A+B+C with
F-degree5, contradicting singleton isolation.

Application boundary
--------------------

There is no mathematical blocker in the frozen edition. Root still needs
an actual universal full-graph profile/required-geodesic certificate before
applying M0 emptiness or this M1 normal form to any pending family. Missing
partial edges do not certify membership in M. Right-incidence coverage,
unrooted half identification and actual ordinary-union joins remain owed.
No checkpoint, reserved transaction, current family, original manuscript,
Lean result, conjecture or compression measurement is credited here.
