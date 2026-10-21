Six-layer mass twenty-two and the order-95 diameter bound
========================================================

Status: complete composition submitted for independent mathematical review.
The 27 Boolean refutations used below are already separately acquired.
This note does not change an enumeration ledger, source disposition or
publication counter.  It proves the following two statements from the
explicitly identified handwritten and computational premises.

Theorem A.  In a connected simple four-regular graph of girth at least
five, six consecutive distance layers, each containing at least two
vertices, contain at least 22 vertices in total.

Theorem B.  A connected simple four-regular graph of girth at least five
having a vertex of eccentricity 22 has at least 95 vertices.

Distance layers throughout are the ORIGINAL BFS layers from the fixed
root.  A ball in an induced cap or section will be identified separately.
No assertion that reversed original layers are BFS layers is used.

1. Source question and scope
---------------------------

The retained original is Stijn Cambie, Jan Goedgebeur, Jorik Jooken and
Tibo Van den Eede, ``On the order-diameter ratio of girth-diameter cages'',
arXiv:2511.21144v3, 19 August 2026, DMTCS 28:4, SOFSEM2026 #1.  Its Table 5,
physical page 22, has the row

  k=4, g=5, d=22, M(k;g,d)=87, n(k;g,d)=95, number of cages >=1.

Theorem B supplies the lower-bound side of the claimed minimum order 95:
a diameter-22 graph has a diametral endpoint of eccentricity 22, and exact
girth five implies girth at least five.  In particular it excludes all
order-at-most-94 graphs in the larger eccentricity-22 domain used by the
retained F009 search.  It does not require that all pairs be at distance
at most 22.  A separately checked 95-vertex graph is needed for equality
of the cage order; this composition does not reacquire that positive
witness, enumerate the 95-vertex cages, or prove all other source claims.

The source's Moore-tree and interval bounds and its BFS framework are
reused with attribution.  The contributions here are the composition of
the acquired local exclusions and the mixed-radius two-packing argument
in section 5.  There is no claim of priority for the elementary methods,
and no claim of a Lean or other proof-assistant formalization.

2. Completing the local six-layer theorem
----------------------------------------

The acquired handwritten theorem already gives mass at least 21.  Suppose
for a contradiction that six nonsingleton consecutive layers have total
mass 21, and number them locally 0,...,5.  The first layer is not the root
layer, which is a singleton.  Choose a geodesic across the interval,
with adjacent centres u in layer 2 and v in layer 3.  Name their other
neighbors A1,A2,A3 and B1,B2,B3, with A1 in layer 1 and B1 in layer 4
on the geodesic.

Each radius-two ball has exactly 17 vertices, by degree four and the
absence of triangles and quadrangles.  Both balls lie inside the six
layers.  Their intersection is u,v, the six A/B vertices, and m common
second neighbors Cij.  A vertex Cij is adjacent to Ai and Bj.  There is
at most one for each cell ij, and it has only one A-parent and one
B-parent, by the absence of quadrangles.  No A--B edge exists.  Thus

  |B2(u) union B2(v)| = 26-m.

For each missing cell ij, one private vertex Uij is attached to Ai and
one private vertex Vij is attached to Bj.  These names are distinct;
names within each parent's private set are arbitrary.  There are 9-m
private vertices on each side.  All eight centre/parent vertices already
have their full four distinct neighbors in this displayed union.

Cell 11 is missing: a vertex adjacent to both A1 and B1 would join
original indices differing by three with a path of length two.  Hence
m<=8.  If m<=4 the displayed union already has at least 22 vertices.
The possible equality-21 cases are consequently exactly

  m=8: three vertices outside the union;
  m=7: two vertices outside the union;
  m=6: one vertex outside the union;
  m=5: no vertex outside the union.

For m=8 the acquired eight-cell handwritten theorem excludes equality.
For m=7 the two holes are either in distinct rows and columns or share
a row or column.  The acquired matching-holes and corrected adjacent-
holes handwritten theorems respectively exclude these alternatives.
The corrected adjacent proof is the edition 3fa84896..., not the
preserved earlier edition with an omitted permitted five-cycle case.
Those proofs explicitly justify every reversal they use by support and
degree alone, without reversing the asymmetric BFS predecessor axiom.

For m=5 and m=6 we use the separately reviewed necessary Boolean model.
Here is the entire interface from a graph to that model.  Keep its
literal 21 vertices, their original local layer indices, and their
induced adjacency.  In the m=6 case call the one extra vertex X.
Choose the geodesic private names U11,V11, so its six vertices are
U11,A1,u,v,B1,V11 at indices 0,...,5.  Set all prescribed edges true,
other edges incident to the saturated eight vertices false, and every
remaining edge variable according to the graph.  Assign one layer per
vertex and evaluate the equivalence-defined Boolean gates.

Every layer has at least two vertices.  Edges change original index by
at most one.  Interior layers 1,...,4 have full degree four inside the
interval.  All vertices have degree at most four there.  A vertex at
local index zero has at most three neighbors inside, since its original
nonroot layer gives it a predecessor outside.  Zero internal degree at
that boundary is allowed.  Every vertex of local index h>0 has a
predecessor at h-1 inside; no successor is required, and no predecessor
inside is required at index zero.  Each unordered pair has at most one
common neighbor; an adjacent pair has none.  These are precisely the
necessary no-quadrangle/no-triangle restrictions used by the model.
In particular five-cycles are allowed.  The old F012 girth-six graph
builder is not called: only its Boolean Formula primitives are reused.
These facts give a satisfying assignment if the graph fragment exists.

Only independent swaps of row labels 2,3 and column labels 2,3 are used
for certificate coverage.  They fix the six geodesic anchors and all
layer indices and map private names with their parents.  They therefore
preserve every degree, predecessor and boundary condition just stated.
No transpose or layer reversal is used in this coverage.  The exact
C2 x C2 action partitions the 28 three-hole sets containing 11 into 10
orbits and the 56 four-hole sets containing 11 into 17 orbits.  The
complete representatives and all orbit members are in the acquired
hole_pattern_partition.json, with its written coverage proof.

For every one of these 27 representatives, a distinct acquisition has
reconstructed the complete deterministic DIMACS formula and primary
variable map from the exact holes and compared all bytes to the retained
producer output.  The accepted RUP kernel then checked the complete
proof and an explicit empty-clause derivation against that formula.
The rectangle m5_03 was acquired first; the other 26 were acquired once
each, with unchanged code, exact cases and terminal successful receipts.
The all_hole_patterns_acceptance.json record binds these actual results.
Its aggregate and the direct small results/receipts were checked again
for the present composition, without executing a solver or proof reader.

The solver's UNSAT answer is not a premise.  The premise is the checked
refutation of each exact necessary formula, under the reviewed Boolean
encoding and RUP implementation.  The checker uses fixed original units,
an active store and a historical RUP fallback; deleting clauses does not
remove the historical consequences.  This composition borrows that
accepted implementation rather than asserting an independent second
implementation.  A satisfying graph assignment would contradict its
representative's checked empty clause.  All m=5,6 cases are excluded.

This exhausts every equality-21 possibility.  Together with the acquired
lower bound 21, it proves Theorem A.

3. Boundary decomposition and the inherited finite reduction
------------------------------------------------------------

Assume now that G has a root o of eccentricity 22 and order at most 94;
write its layers V0,...,V22.  In any internal singleton layer {w}, the
two cuts to earlier and later layers are positive even integers.  They
are even because every degree of G is even; they are positive by the
root paths and the existence of later layers.  They sum to four, so
both equal two.  Prefix and suffix induced subgraphs including w are
connected caps with boundary degree two and every other degree four.
The section between consecutive singletons is connected, has those two
boundary degrees two, and all its other degrees four.  All retain girth
at least five.  The acquired cap theorem gives order at least 20.

The acquired singleton-position arguments, culminating in the mass-21
acceptance, imply the following exhaustive alternative under order<=94:

  no internal singleton; or the complete internal singleton set is
  {4}, {18}, or {4,18}.

This imports the full-set reduction, not a selection of convenient
singletons while silently ignoring others.  The earlier five survivors
were {4},{18},{4,9},{4,18},{13,18}; the accepted mass-21 packing already
excluded the middle two-ended sets {4,9} and {13,18}.  Previously excluded
sets cannot return when a lower bound is increased from 21 to 22.
The end layer V22 is not called an internal singleton.  It may be a
singleton; the radius-two terminal ball used below still has 17 vertices.

We recall exactly the local boundary facts that will be used.  For a
degree-two boundary w whose first three layers meet no other exceptional
vertex, B2(w) has 1+2+6=9 vertices and B3(w) has at least 15 vertices.
The six vertices at distance two split into triples P,Q according to
their two first-layer parents.  Their internal edges form a matching
of size m<=3, and a vertex in the next layer has at most one parent in
each triple.  Thus 18-2m>=12 incidences enter that layer and its size
c is at least six.  The accepted radius-four boundary theorem further
gives |B4(w)|>=19 when all vertices within distance four except w have
degree four, the whole induced graph has even degrees, and a vertex
at distance at least five exists.  These statements apply to the
two-ended section below: its other exceptional boundary is distance14.

4. The no-singleton and one-singleton alternatives
-------------------------------------------------

If there is no internal singleton, the original layers 0,...,2 contain
the 17-vertex radius-two ball about o.  Layers 20,...,22 contain the
17-vertex radius-two ball about any vertex in V22.  The 17 middle layers
3,...,19 are all nonsingleton.  Partition them into intervals 3,...,8;
9,...,14; and 15,...,19.  The first two have mass at least 22 by Theorem A;
the third has mass at least 17 by the attributed five-layer Moore bound.
All five sets of layer supports are disjoint, and hence

  |G| >= 17 + 22 + 22 + 17 + 17 = 95.

Suppose the only internal singleton is at index4.  The left cap on
layers 0,...,4 has at least 20 vertices.  Inside the right cap, the
radius-three boundary ball is supported on layers 4,...,7 and has at
least 15 vertices.  A radius-two ball about a vertex in V22 has 17
vertices and is supported on layers 20,...,22.  The remaining whole
layers 8,...,19 are two nonsingleton six-layer intervals.  These four
sets inside the right cap are disjoint, giving right-cap order at
least 15+22+22+17=76.  The two caps overlap in their one boundary vertex:

  |G| >= 20 + 76 - 1 = 95.

For the sole singleton at index18, the same count is obtained without
reversing a BFS predecessor axiom.  In the left cap the regular root
ball has support 0,...,2, the boundary radius-three ball has support
15,...,18, and whole nonsingleton intervals 3,...,8 and 9,...,14 lie
between them.  Its order is at least 17+22+22+15=76.  The right cap has
at least 20 vertices and shares only the singleton, again giving 95.

These support statements need only the elementary Lipschitz property
of original BFS indices along edges: distance at most r from index j
implies original index between j-r and j+r.  Balls are taken in the
indicated cap; the far boundary is too distant to affect their regular
degree counts.  Equality of reversed ball layers and original layers
is nowhere required.

5. A mixed-radius inequality and the last two-singleton case
-----------------------------------------------------------

Here is the needed refinement of the acquired radius-four proof.  Under
its hypotheses, put c=|S3(w)| and d=|S4(w)|.  Then

  |B3(w)| + |B4(w)| >= 35.                              (1)

If c>=7, the two separate acquired bounds give |B3|=9+c>=16
and |B4|>=19, proving (1).  If c=6, the parent incidence count forces
m=3 and every third-layer vertex has two parents.  Number the three
matching edges pi--qi by i=0,1,2.  The six distinct third-layer labels
are exactly the off-diagonal pairs ij.  They are independent, by the
acquired triangle/quadrangle parent argument.  Hence twelve incidences
go from these six vertices to the fourth layer.

A fourth-layer vertex cannot meet two third-layer vertices sharing
either parent coordinate, since this gives a quadrangle.  It has at
most three such neighbors.  The only possible three-neighbor sets are
{01,12,20} and {10,02,21}.  Neither set can occur twice, since two
common neighbors already give a quadrangle.  If d<=4, the fourth layer
can therefore receive at most 3+3+2+2=10 incidences, fewer than twelve.
So d>=5, |B3|=15 and |B4|>=20, proving (1) also in this case.
This uses the c=6 refinement already present in boundary_radius_four.rst;
it is not a claim that every radius-four boundary ball has size twenty.

Now let the complete internal singleton set be {4,18}, with boundary
vertices w in V4 and z in V18.  Let H be the induced section on original
layers 4,...,18 and nH its order, including w and z.  The two boundaries
are distance exactly14 in H: every original edge changes index by at
most one, and a root geodesic to z passes through the unique vertex w
and supplies a length-14 path in H.  All interior vertices have degree
four within H, both boundaries have degree two, and H is connected
and even-degree.  Thus the radius-four hypotheses hold at EACH end,
because the other exceptional vertex is at distance14>4 and also
supplies a vertex at distance at least five.  Define

  Lr=|B_r^H(w)|,  Rr=|B_r^H(z)|,  for r=3,4.

The mixed-radius inequality gives L3+L4>=35 and R3+R4>=35.
Every original layer 5,...,17 is nonsingleton.  There are two useful
packings of H, each separately made of disjoint vertex sets:

* B4^H(w) has support 4,...,8; the six complete layers 9,...,14
  have mass at least22; B3^H(z) has support 15,...,18.  Therefore

    nH >= L4 + 22 + R3.                                  (2)

* B3^H(w) has support 4,...,7; the six complete layers 8,...,13
  have mass at least22; B4^H(z) has support 14,...,18.  Therefore

    nH >= L3 + 22 + R4.                                  (3)

Theorem A is applied to these complete ORIGINAL layer intervals in G,
not to hypothetical reversed distance layers in H.  The support bounds
alone prove the two disjointness assertions.  The two DIFFERENT packings
may overlap each other; that is harmless because we add inequalities
(2) and (3), rather than combine their sets into one purported partition.
We obtain

  2 nH >= (L3+L4) + (R3+R4) + 44 >= 114,
  nH >= 57.

The left cap on layers 0,...,4 and the right cap on 18,...,22 each
have at least20 vertices.  They are disjoint from one another; the
section H overlaps them in w and z respectively and nowhere else.
All original layers are included once after subtracting those two
overlaps.  Consequently

  |G| = |left cap| + nH + |right cap| - 2
      >= 20 + 57 + 20 - 2 = 95.

This is the last alternative under order<=94.  Its contradiction, with
section 4, proves Theorem B.  No universal cap lower bound21 is needed;
indeed the preserved cap_distance_obstruction.rst explains why the
previous proposed eccentricity-four cap exclusion cannot be used.

6. Arithmetic cross-check, evidence and limits
---------------------------------------------

For comparison with the earlier packing tables, let

  P22(r)=max {17a+22b+2(r-5a-6b): a,b>=0, 5a+6b<=r}.

Its values for r=0,...,17 are

  0,2,4,6,8,17,22,24,26,28,34,39,44,46,48,51,56,61.

Substitution into the previously acquired cap/section formulas gives
95,95,96,94,96 for the five old sets {4},{18},{4,9},{4,18},{13,18},
and 95 for the no-singleton alternative.  The 94 in that table uses
separate ball minima; section 5 replaces it by95 using their joint
constraint.  The unchanged twenty_two_packing.json retains this small
integer cross-check.  The direct disjoint packings above are the proof;
the table is not evidence that an extremal graph exists.

The accompanying twenty_two_composition_inputs.json identifies the
exact source and accepted premise records by path, size and SHA256.
It also records the literal check of the 27 acquired result/receipt
joins and the arithmetic just described.  It references the accepted
27-case catalogue rather than copying all its dependency closures.
The principal premise records, with paths relative to computation/f009,
are:

* six_layer_twenty_one_acceptance.json: lower bound21 and the exhaustive
  three surviving nonempty singleton sets under order<=94.
* six_layer_equality_eight_cells_acceptance.json: equality21, m=8.
* six_layer_matching_holes_acceptance.json: equality21, m=7 disjoint holes.
* six_layer_adjacent_holes_acceptance.json: equality21, m=7 adjacent holes,
  using the corrected proof edition.
* six_layer_certificates/method_acceptance.json: necessary CNF encoding.
* six_layer_certificates/hole_pattern_coverage_acceptance.json: the exact
  10+17 representative cover of all28+56 literal m=6/m=5 hole sets.
* six_layer_certificates/all_hole_patterns_acceptance.json: the actual
  27 exact formula/map reconstructions and checked RUP refutations,
  including rectangle/root_acceptance.json for m5_03.
* boundary_radius_four_acceptance.json and boundary_radius_four.rst:
  boundary B4>=19, including its c=6 implies d>=5 refinement.
* singleton_cap_twenty_acceptance.json: each terminal cap has order>=20.
* singleton_free_section_acceptance.json and six_layer_mass_acceptance.json:
  the inherited support/partition arguments and Moore interval premises.

The final local m=5/m=6 exclusions are computationally certified, not
replaced by the unverified Z3 diagnostics that originally guided case
selection.  Those diagnostics and old failed proposals remain separate
historical evidence.  No proof checker, solver, graph generator or
enumeration prefix was rerun for this composition.  The independent
mathematical review of the composition is still a separate step.

Upon acceptance, Theorem B makes any further search for graphs in its
order-at-most-94 domain unnecessary as a proof of that exclusion.  It
does not turn the retained partial enumeration into a completed one:
the accepted literal prefix remains 2030 of14476, and the unprocessed
roots have not been enumerated.  Whole-source recovery and publication
require their separate audit, including positive witnesses and other
claims.  No source-count, current-state, or publication mutation is made
by this document.
