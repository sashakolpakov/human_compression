L046: exact source contract and reusable interfaces
==================================================

The fixed original is Connor--Leemans, Algorithmic enumeration of regular
maps, Ars Mathematica Contemporanea 10 (2016), 211--222, twelve physical
pages. Its PDF SHA256 is
412775233715c6d925377a9588cf98e7af7491c4041789a29dfeb34b7dd36812.
All twelve extracted pages were read. Physical pages 3, 8, 9 and 11 were
also rendered and directly viewed. This is source-contract work, not a
principal recovery or numerical admission.

Principal numerical obligations
-------------------------------

Theorem 1.1(1): O'Nan has generating pairs R,S with RS of order two and
orders p<=q from P={3,4,5,6,7,8,10,11,12,14,15,16,19,20,28,31}, except
the seven types (3,3),(3,4),(3,5),(3,6),(3,7),(3,12),(4,4). These are 129
nonzero types. Complete proof requires both positive generation and the
seven exclusions, not merely nonzero character structure constants.

Theorem 1.1(2), Table 1: every one of the 136 upper-triangular cells, with
sum 796772 Aut(O'Nan)-orbits. The paper's braces are used for an order
type and sometimes for pairs. Formula (2.4) counts ordered generating
pairs under automorphisms, with p<=q selecting type orientation. No extra
quotient by duality at p=q is implicit in that formula. Our comparison
must preserve this convention and distinguish a separate duality quotient.

Theorem 1.1(3): chiral maps exist for exactly the 128 allowed types other
than (3,15). Section 5 strengthens the exceptional case: the six orbits
of type (3,15) split as four with inner and two with outer simultaneous
inversion. The claimed nonexistence of chiral pairs needs exhaustive
coverage of that type, not failure of a search.

Theorem 1.1(4): non-orientable regular maps with full group O'Nan exist
for 95 types. Exclude every allowed type containing 20 or31, together
with (3,10),(4,5),(4,6). The class-inversion obstruction covers the first
family but not the three isolated exceptions. Those require exact pair
classification; positives must have simultaneous INNER inversion.

Theorem 1.1(5): orientably regular reflexible maps with full group ON:2
exist for98 types. Exclude every allowed type containing8 or16. Positives
require simultaneous OUTER inversion; ordinary ON:2 string markings are
not enough unless the actual rotation subgroup is ON.

Additional explicit finite conclusions
-------------------------------------

Section5 records exact chiral/inner/outer splits, respectively:
 (3,10):6/0/1; (4,5):16/0/2; (4,6):42/0/1; (5,5):22/2/2.
The statements for (5,7),(7,7),(6,12) are positive examples of the already
listed types. They are not separate whole-original obligations.

Section7 records complete p=3,4,5 row totals284,5176,7738 and their
chiral/non-orientable subtotals230/39,4906/114,7340/188. The remaining
outer counts would therefore be15,156,210. These exact finite conclusions
should be recovered or explicitly qualified in a whole-source assembly.
Historical running times and the qualitative experimental tendency at
larger p are not mathematical completeness or speed guarantees to reproduce.

The table was extracted into source_table1.json and all136 literal cells
were checked against its native page. The seven zeros, total796772 and
three small-p sums agree internally. This is transcription and arithmetic,
not verification of the generating-pair census. The sentence on physical
page7 simultaneously gives gamma(3,12)=0 and includes12 in a list with
nonzero gamma. That textual inconsistency must not override the explicit
Theorem1.1/Table1 zero or be silently turned into a proved correction of
the referenced external paper.

General algorithm and attribution
---------------------------------

Sections2--3 use Frobenius' character formula, Hall's subgroup inversion
and the free Aut(G) action on generating pairs. They are explicitly old
ideas in the original. A common proof may arrange all order-pair queries
into a single vector calculation and use a common subgroup-incidence
matrix, but it must not claim invention of character counting, Möbius
inversion, or reuse of subgroup data. The source already avoids repeated
subgroup/character calculations within its stated algorithm.

Section6's constructive algorithm covers pairs by fixing a rotation and
using orbits of its cyclic subgroup on involutions. It then explicitly
removes duplicates under the full automorphism group and may stop at the
previously known total. A reusable replacement can instead use complete
Aut(G) rotation orbits and the full stabilizer on involutions; a proof of
both coverage and uniqueness is required. If a census is stopped at an
expected count, that expected count must already have an independently
accepted proof. A timeout is never such a count.

The accepted L071/F006 stabilizer enumeration supplies the general orbit
extension argument and finite software interfaces. Its IP and involution
inventory hypotheses cannot simply be copied onto the rotational problem.
The new objects are generating pairs (R,S) with |RS|=2; choosing S and
tau=RS gives an equivariant bijection R=tau*S^-1. L071's recorded groups
through Held and Co3 do not include an O'Nan map census. All L046 numerical
principal obligations remain pending.

Existing named O'Nan material and its limit
-----------------------------------------

The accepted N006 sporadic packet supplies a concrete named ON:2 model,
its standard generator provenance, character data, and one string marking
of type{8,11}. It does not solve this source's positive case: under the
ON:2/ON character, its three marks (t,a,b) have signs (1,0,0). Thus its
first rotation t*a is outside ON. The existing witness remains useful
as model infrastructure, without map-census credit.

Local GAP contains the ordinary ON and ON.2 character tables and their
stored fusion, but TableOfMarks("ON") returns fail. No local Magma
executable was found. A bounded character probe (~one second) confirms
the exact inversion-class facts used in source Lemmas5.2 and5.3 and
computes every all-pair character count. Four complete small-group
direct-pair controls agree. These are bounded working results awaiting
their own proof/review, not a numerical principal recovery.

The cited subgroup-lattice atlas URL could not be fetched by the browser
or curl in this run; curl reported unresolved hostname. A web search
finds the authors' thesis appendices and the published atlas reference,
but no actual full weighted lattice/character input has yet been acquired.
No new original has been admitted: these are possible cited-premise files
for the already fixed L046. A new huge O'Nan census has not been launched.

Most promising exact routes
--------------------------

For Table1, acquire the complete weighted ON subgroup classification and
actual character data of its subgroup types, then apply a single exact
incidence inversion to the whole order-pair vector. Its external input
cost and provenance must remain explicit. The local character table of
ON alone only gives all-pair upper bounds and cannot certify generation.

For the chirality splits, either acquire actual fixed pair certificates
and complete counts, or develop an exact two-stage orbit census using
full stabilizers with justified bounded execution. The two individual
class obstructions are already very small and suitable for an immediate
bounded component. This plan introduces no unreviewed long search and
does not abandon any principal claim.
