Fi22 involutions through the three-transposition geometry
========================================================

Author of this route and proofs: /root/readme_final_check. Root proposed
the vertex/edge/triangle route and its application to the unfinished L026
selectors. The Fischer geometry, classical unitary transitivity, Witt
system, maximal subgroups and transporter methods are borrowed named
mathematics. No historical novelty is claimed. This note uses the existing
original intake; reading the cited primary literature adds no manuscript
or Original credit. All new geometric model joins, orbit data and fit are
UNACQUIRED. Only Source/text, primary-source reading and closed metadata
were used; no group, permutation, point, field, worker, helper, guard,
runtime, process or state operation was executed.

1. The exact current input boundary
-----------------------------------

Let G be the retained named simple Fi22 and A=Aut(G). The accepted input
gate is maintenance/intake/l026_fi22_input_acquisition/
root_catalogue_acceptance.json, 272088 bytes, SHA256
425eba68b1a6266fe7767e34f1da7b0d5f277fd503b76bb06f734a7552127153.
It accepts a faithful degree3510 model, normal G in A, three involution
classes in G, their full A-centralizers and35 ordered endpoint orbits.
Its named-Fi22 and Out(G)=2 hypotheses remain attributed. It explicitly
does NOT accept a complete middle partition, generation/duality census
or whole Original.

Its serialized class order is B,C,A in ATLAS notation, not A,B,C:

  block1: class size1216215, |C_A(a)|106168320,12 endpoints;
  block2: class size36486450, |C_A(a)|3538944,18 endpoints;
  block3: class size3510, |C_A(a)|36787322880,5 endpoints.

Thus there are105 potential endpoint/middle-class selectors, not105 paid
partitions. The closed distinct review's endpoint_setup_proposals retain
literal endpoint hashes and borrowed_expected_pointwise_A_order values.
Those expected orders are proposals, not newly acquired H orders here.
The underlying complete local class data provide a future exact route to
their verification. No proposal is promoted to an accepted family result.

The exact old input routine is ambient_input_method_v2/input_blocks.g.
For Q=C_A(a), it stores all Q classes and their membership flags, then
selects precisely c in G of order2 with c!=a. The corresponding Reader
checks full original generator equality, complete model fields, all
serialized block/catalogue joins and the literal endpoint filter. Its
permutations are compact two-byte image strings of length2*3510, not
untyped class names. IsNormal(A,G) means G is normal in A; it does not
mean A is contained in G.

2. Primary geometric inputs, with their precise roles
-----------------------------------------------------

[T] Paul Taylor, Computational Investigation into Finite Groups (2011),
Chapter5, printed pp75--76, identifies the3-transposition class D=2A
and describes2B/2C through products of two/three commuting members of D.
[IW] Ivanov--Wiedorn, More on Geometries of the Fischer Group Fi22,
J. Algebraic Combin.16 (2002), Section3, printed pp119--121, gives the
commuting graph on D, its natural local U6(2) polar action, maximal
22-cliques, their elementary abelian2^10 group and their Witt system.
[B] Brouwer's SRG table gives (3510,693,180,126). [A] ATLAS gives the
orders and centralizers. Full URLs and access qualifications are in
PRIMARY_SOURCES.rst; they are literature premises, not current payloads.

Write Gamma for the graph on D in which distinct vertices commute.
The needed named action fact is that the point stabilizer induces the
natural unitary action on its693 neighbours, with adjacency there being
orthogonality of distinct isotropic points. This is stronger than merely
matching graph parameters. Witt extension gives transitivity on ordered
orthogonal point pairs: a bijection of their two-dimensional totally
isotropic spans is an isometry and extends to the ambient Hermitian
space. The special unitary version also suffices: an extension's
determinant can be adjusted on a nondegenerate complementary plane
while leaving that isotropic span fixed. Hence the named action is
transitive on ordered edges and ordered triangles of Gamma. In particular
it is transitive on their unordered versions. One may use the full
automorphism action; the three G classes are stable in A because their
sizes differ. No arbitrary graph with the same parameters is substituted.

The current faithful3510 permutation model is not identified with these
vertices merely by degree. Section10 gives the still-required actual
same-model correspondence. The following deductions apply to the named
geometric action once that correspondence is supplied.

3. Equivariant products and exact fibers
----------------------------------------

Let E be the unordered edges and T the unordered triangles of Gamma.
Define p2({x,y})=xy and p3({x,y,z})=xyz. The factors commute, so order
does not matter; conjugation and every automorphism commute with these
maps. Transitivity from Section2 makes each image a single class. The
nonempty product descriptions in [T] identify these images with2B and2C.
This explicitly supplies the class assertion before any counting is used.

The graph parameters give

  |E|=3510*693/2=1216215;
  |T|=3510*693*180/6=72972900.

The ATLAS class sizes are |2B|=1216215 and |2C|=36486450. An equivariant
surjection onto a transitive conjugacy class has equal fibers: conjugation
by an element taking one target to another gives a bijection between
their inverse images. Therefore p2 is a bijection and every p3 fiber
has exactly TWO triangles. This is a proof using image and equivariance,
not an inference from coincident integers alone.

There is consequently a unique fixed-point-free involution tau on T:
tau(U) is the other triangle with the same product. It commutes with A,
because an automorphism carries the two-element fiber bijectively to the
next fiber. This is a two-element equivariant cover of sets. No graph
cover or topological deck group is asserted without a chosen graph on T.

4. The two triangles form complementary triples in a hexad
-----------------------------------------------------------

We first need a general3-transposition observation. If d in D normalizes
a finite commuting clique K, it fixes K pointwise. Its induced permutation
on K is an involution. If it swapped distinct x,y, then x^d=y and
(xd)^2=xx^d=xy would be a nonidentity involution, forcing |xd|=4.
That is forbidden for two3-transpositions. Thus there are no two-cycles.
This argument is for d in D; arbitrary members of A can permute a clique.

Let U,V be the two triangles over t. They are disjoint. Indeed, if x
belonged to both, cancelling x would give equal products for the two
remaining edges, contradicting the injectivity of p2 unless U=V.
For d in V, conjugation by d fixes V pointwise and acts on the two-element
fiber. It therefore also stabilizes U setwise; the preceding observation
then makes it fix U pointwise. Thus all six vertices in U union V commute.
Their product is1, and tau exchanges complementary triples of this6-set.
This six-set is determined by the fiber, not by an arbitrary complement
inside a22-set.

Let K be any maximal commuting clique containing U. Every k in K fixes
U pointwise, hence preserves V setwise, hence fixes V pointwise by the
same observation. Maximality now forces V subset K. Thus every triple
in K has its partner inside K. Define a block to be the union of such
a pair. Every3-subset lies in exactly one such6-block: its partner is
unique; conversely a6-block's complementary3-subsets have equal products.
This constructs S(3,6,22), with77 blocks, directly from the product fibers.
The ambient stabilizer preserves it. This recovers the Witt incidence
used in [IW] without choosing labels by cardinality.

The homomorphism F2^K -> <K> sending a subset to its product has a
12-dimensional kernel since |K|=22 and |<K>|=2^10. No nonzero relation
has weight below6: weights1--3 follow from the involution/product classes;
weight4 contradicts edge injectivity; weight5 equates a2B product with
a2C product. Its weight6 supports are exactly the77 blocks just proved.
Thus the group gives a binary[22,12,6] code. An identification with any
particular Golay encoding or with an existing labelled Witt file still
requires an actual code/design isomorphism. Equal parameters do not
supply that map. The orbit route below does not require naming the code.

5. Deriving H from the existing full C_A(a)
-------------------------------------------

For a fixed accepted endpoint pair (a,c), put Q=C_A(a) and H=C_A(a,c).
The accepted input gives complete Q generators. Positive geometric
decompositions of c reduce the remaining stabilizer problem as follows:

* If c in2A corresponds to x, then H=Q_x.
* If c in2B corresponds to the unique edge e, then H=Q_{e}, setwise.
* If c in2C has fiber {U,tau(U)}, then H is the setwise stabilizer in Q
  of that unordered pair of triangles.

These are equalities, since the products are equivariant and their
fibers have the exact sizes established above. For2B, compute Q_{x,y}
pointwise and test the possible transporter (x,y)->(y,x); the setwise
stabilizer consists of that subgroup and the cosets actually present.
For2C, first compute Q_U. Pointwise stabilization of the three vertices
followed by the six possible orientation transporters gives Q_U exactly.
Then test ONE transporter U->tau(U), allowing all six target orders.
If none exists H=Q_U; if one exists H is its index2 extension. Actual
words, not abstract isomorphic subgroup labels, must certify every coset.

The transporter-coset proof is the standard one retained in
topic_D_L096_volume_v2/sections/transport.tex and the common refinement
theorem in topic_Mix_F007_recovery_v2/relations_and_flags.tex. After a
partial placement, all remaining solutions form a coset of the target's
actual stabilizer. Intersecting with the next condition or finding it
empty is exact; the placed-target stabilizer is reusable. This is the
library-plus-bound-hypotheses method discussed in the old GKM note,
not a new implementation or an inherited Fi22 transporter pass.

6. Exact H-orbits by small fibers
---------------------------------

For any subgroup H of A, choose one representative x of each H orbit
on D. For each x, choose representatives y of H_x orbits on N(x).
For each ordered edge (x,y), choose representatives z of H_{x,y}
orbits on N(x) intersect N(y). These local domains have sizes693 and180.
The resulting triples represent exactly the H orbits on ordered triangles.

Proof: move the first coordinate to its representative, then move the
second by its stabilizer, then the third by the next stabilizer. Two
resulting tuples are equivalent precisely when the successive local
choices coincide. The same argument truncated after two coordinates
handles ordered edges. Their stabilizers are the corresponding pointwise
stabilizers. Full stabilizer generators can be certified by the Schreier
generators t_u h t_{u^h}^{-1} from a complete rooted orbit/transition table.
Literal word evaluation, connectivity and every closure edge prove that
table is exactly the orbit; Schreier rewriting proves completeness of
the next stabilizer, not just containment.

The coordinate S2 or S3 action commutes with H on ordered edges or
triangles. Quotient its action on H-orbit records to obtain unordered
objects. The total ordered mass in one such component divided by2 or6
gives its unordered mass. Individual ordered orbits must NOT all be
divided by2 or6: their setwise stabilizers may induce different subgroups
of the coordinate permutation group.

Next apply tau on the UNORDERED triangle-orbit records. If O and tau(O)
are distinct H orbits they merge into one2C orbit of weight |O|. If
O=tau(O), its2C image has weight |O|/2. In the latter case H_t has
index2 over H_U; otherwise H_t=H_U. This follows by restricting the
two-element product fiber to one H orbit. It gives exact weights and
stabilizers without a full2C element list.

Coordinate S3 and H commute on ordered triples, whereas tau is
canonically defined on unordered triangles. A commuting S3-times-C2
action on ordered triples needs an extra equivariant ordering lift;
none is assumed. Sequential S3 then tau quotient, or the equivalent
explicit orbit groupoid, is sufficient and avoids that missing choice.

7. Nonfree and generation certificates reuse existing legs
-----------------------------------------------------------

If a middle orbit has weight w<|H|, its point stabilizer in H is
nontrivial. Such an automorphism fixes a,b,c and cannot fix generators
of all G unless it is the identity. Hence the marking is nongenerating.
This is exactly the previously reviewed marking-stabilizer obstruction.
It works for full Aut pointwise H as well as inner H; the two denominators
must not be interchanged. In particular |H|>|X| makes every middle in
class X nonfree. The closed input review already suggests this cut;
one must acquire exact local-class sizes/H before using its expected
order fields as certificates. Free orbits give no generation or IP result.

There is also a positive11/13 test. The complete ATLAS maximal-order
list has no proper maximal subgroup order divisible by both primes.
Its11-containing families are2.U6(2),2^10:M22 and M12; its13-containing
families are O7(3) and the Tits group. Their orders have no common11/13
case. Kleidman--Wilson's1988 corrigendum preserves the Main Theorem.
Consequently a subgroup of the named G whose order has both divisors
is all G. Distinct closed cycles in supplied words with lengths divisible
by11 and13 suffice, by faithful permutation action and Lagrange. The
two cycles may use different words. Their literal edges/distinctness
still need strict Saved acquisition; a failed search remains UNPAID.

Reuse the existing O'Nan prime-cycle proof mechanism, with a NEW exact
Fi22 source/degree/known-G/maximal-list binding. Its old19/31 Source or
controls gate is not retargeted. Involutions here are certified members
of G, not arbitrary elements of A. For rank3, the existing named-simple
generation-implies-intersection theorem in rank_three_intersections.tex
can then be applied with its exact distinct/string hypotheses. None of
this supplies the remaining full-Aut/reversal/duality count.

8. Why the Witt route may help and what it does not do
-------------------------------------------------------

The accepted Topic G Steiner fiber theorem and the explicit native
S(3,6,22) blocks/coordinate maps/stabilizers are reusable local inputs.
They describe a labelled degree22 design; they do not identify one of
its points with any current Fi22 transposition. A literal incidence
isomorphism and matching action of the actual clique normalizer are
needed before native Mathieu/Golay operations can replace point words.
Maximal22-cliques form a smaller geometric flag domain, but a triangle
can occur in several such cliques. Enumerating flags and counting them
as different middles is wrong; an incidence-owner quotient is required.

The point/neighbor/common-neighbor method avoids building a flat
36-million-element class. It does not prove a universal speedup. It
may produce many local subproblems, and its ordered triangle domain is
larger than2C before quotient. No number of H orbits, time split or
actual Fi22 fit has been acquired. Source diagnosis, local orbit proofs
and genuine measured calls must choose the useful endpoint/batch size.

9. Endpoint decomposition is a positive certificate problem
-------------------------------------------------------------

A supplied one-, two- or three-vertex decomposition must be verified
against the entire original endpoint permutation and current D-action
bridge. For2C, supply both disjoint triangles and check their equal
product c; the two-fiber theorem then proves they are the whole fiber.
No producer search needs replay by Saved.

An optional bounded supplier can search among D elements commuting
with c, because every component does. If the current3510 model's three
involution fixed-point signatures are acquired as694/182/54, their
distinctness classifies any known-G involution after a direct point
count. For2B, test d*c for membership in2A; exactly the two edge
components succeed. For2C, test d*c in2B; exactly the six fiber vertices
succeed, then reduce each such bi-transposition to its edge. For the
latter assertion, an involution d in D centralizing c also stabilizes
the unique edge of d*c; the3-transposition observation fixes that edge
pointwise, producing a commuting triple over c. This proves the converse.

The signatures and the current D point-to-permutation map are additional
finite obligations. They have not been executed here. Alternatively
use exact membership in the complete D dictionary, with its larger
literal map requirement. Neither a character degree nor a token hash
can replace the original permutation comparisons.

10. Smallest concrete acquisition boundary
--------------------------------------------

First acquire ONE reusable current-model D geometry bridge. Use the
accepted block3 representative d0 and its full Q0=C_A(d0), plus all
original A/G generators. Find a point x0 fixed by Q0; verify the
containment and equal orders Q0=A_x0, using transitivity of the actual
degree3510 action and the accepted centralizer order. Then

  x0^g -> d0^g

is well-defined, bijective and A-equivariant: the two stabilizers are
equal. A complete point orbit word DAG/transition table binds every
label to a literal original word. This is an actual same-model proof;
it avoids assuming that matching degrees or graph parameters suffice.
The root neighbourhood comes from a certified commuting2A seed and
its Q0 orbit. Verify its693 entries, full closure and its complement;
transporting it supplies Gamma. A full adjacency artifact should be
symmetric, irreflexive and have the stated local/strongly-regular counts.
Those checks supplement, not replace, its original commutation meaning.

Next select ONE literal accepted (block,endpoint,middle-class) record.
Acquire its endpoint decomposition and H as in Section5. Acquire one
local chain/orbit chunk with whole parent binding and honest unvisited
state. Strict Saved validates supplied point words, edges, stabilizer
Schreier identities, orientation/deck owner joins and weights; it performs
no producer search. Only after complete coverage/quotients may a middle
partition be called complete. Generation certificates follow separately.

Raw models.g, catalogue.g and the three block files total31,017,076 bytes
according to the accepted receipt, below a64MiB data cap before other
inputs. A full D permutation table could occupy24,640,200 bytes as
3510-by3510 unsigned16 images, but need not be retained if words and
local transports suffice. These are raw representation sizes, not RSS
or fit measurements. The existing Reader/typed literal grammar is the
first interface to inspect, not a guessed new model schema.

The old input acquisition used a different2GiB/300s profile. It does
not confer512MiB/150s fit on any new geometry call. New Source/runtime/
controls/Root readsets, bounded work/deadlines, exact original maps,
actual initial frames and physical closure are still required. The
companion ACQUISITION_INTERFACE.rst specifies certificate roles only;
no worker, caller, proof gate or future result pin is manufactured.

References
------------

[A] `ATLAS Fi22 <https://brauer.maths.qmul.ac.uk/Atlas/v3/group/Fi22>`_.

[B] A.E. Brouwer, `Parameters for a few large SRGs
<https://aeb.win.tue.nl/graphs/srgbig.html>`_.

[T] P. Taylor, `Computational Investigation into Finite Groups
<https://pure.manchester.ac.uk/ws/portalfiles/portal/54506542/FULL_TEXT.PDF>`_,
University of Manchester thesis,2011, Chapter5 pp75--76.

[IW] A.A. Ivanov and C. Wiedorn, `More on Geometries of the Fischer
Group Fi22 <https://doi.org/10.1023/A:1021620911639>`_, J. Algebraic
Combin.16(2002),111--150, Section3 pp119--121. Text inspected in the
published-paper PDF mirror named in PRIMARY_SOURCES.rst.

[KW] P.B. Kleidman and R.A. Wilson, `The maximal subgroups of Fi22
<https://doi.org/10.1017/S0305004100067001>`_, Math. Proc. Cambridge
Philos. Soc.102(1987),17--23; `Corrigendum
<https://doi.org/10.1017/S0305004100064963>`_,103(1988),383.
