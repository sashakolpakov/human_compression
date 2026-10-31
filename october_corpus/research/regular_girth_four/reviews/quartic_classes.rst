Independent hand review: quartic minimum graphs of diameter 4r
=================================================================

Reviewed edition: quartic_classification.tex, 18,666 bytes, SHA-256
15053760411f0e20dcb64968f19fa61aaf33fb3332f601ed3820036414f90ca0.
Verdict: SUPPORTED_MATHEMATICS. No blocking mathematical issue found.
This review concerns finite simple connected quartic graphs, girth exactly
four, diameter exactly 4r, and integer r>=2, at order 8(r+1). It is a
written proof review, not an executed enumeration or formal proof.

1. Equality setup and forced internal chain
------------------------------------------
For a diametral geodesic p_0,...,p_(4r), the r+1 neighborhoods of
z_i=p_(4i) are disjoint independent four-sets and are pairwise
anticomplete. An edge or intersection would shorten a geodesic subpath.
The regular independent-set degree bound therefore gives n>=8(r+1).
At equality the complementary vertex set J is independent too. Every
J vertex meets either just I_i or two consecutive blocks: a pair of
nonconsecutive blocks would give a path of length four between anchors
at distance at least eight. Thus the X_i and F_i types exhaust J.

A single-block vertex meets all of I_i. Hence x_i>=1 and q_i=4-x_i.
Connectedness excludes x_i=4, so 1<=q_i<=3, including the endpoints.
At internal I_i, meeting both adjacent interfaces would give a path of
length six between anchors at distance eight. Both separated parts are
nonempty by connectedness. Consequently their sizes are in {1,2,3}.

The first interface balance is 4|F_0|=4q_0+bq_1. The only multiple of
four among products of two integers in {1,2,3} is 2*2. Thus b=q_1=2.
If an internal index is already forced, the next balance becomes
4|F_i|=4+b'q_(i+1), forcing b'=q_(i+1)=2. This induction covers every
internal index, without imposing q_0=q_r=2. An internal F_i then has
two vertices with all four possible neighbors in I_i^+ union I_(i+1)^-.
All displayed chain incidences are therefore complete, and degree and
type exhaustion preclude hidden edges or additional vertices.

2. Eleven-vertex bases and three ordinary types
-----------------------------------------------
Each endpiece has (4-q_0)+4+(q_0+1)+2=11 vertices. Only the last two
vertices have intrinsic degree two; all other degrees are four. After
choosing an endpoint, the four row vertices each omit exactly one member
of a four-set W. If P,Q are the two port neighborhoods, each a two-set,
the number of row omissions at w must equal beta(w)=1_P(w)+1_Q(w).
This forces the whole row multiset, including multiplicities.

The three possibilities t=|P intersection Q|=0,1,2 exhaust pairs of
two-subsets up to W permutation and port exchange. The four membership
regions have sizes t,2-t,2-t,t. Any such permutation extends to the
forced rows. The ports are intrinsic and their common-neighbor number
is t, so these are distinct as ordinary unrooted halves even when an
endpoint can be moved. The unsupported side vertices and chosen endpoint
are exactly X_0, yielding x_0=1+t and q_0=3-t. Thus all endpoint values
1,2,3 occur and none is omitted. Connectivity and bipartiteness follow
from the stated incidence construction. Every vertex lies within three
of the ports, with an original endpoint at distance exactly three.

3. Extension and exact reversible peeling
------------------------------------------
Each extension adds a new two-set T adjacent completely to the old
ports and a new port two-set Q. All old ports become degree four;
precisely Q has degree two. Its common neighborhood is precisely T.
Deleting Q union T recovers the predecessor half and its two intrinsic
ports. This gives an ordinary-isomorphism invariant inverse; conversely
an isomorphism of predecessors extends because every attachment is
complete and no labeling or matching is retained.

After j=r-2 extensions the order is 11+4j=4r+3. For any old vertex,
distance to the new port set increases by exactly two: a path must
first reach an old port before traversing T. This argument uses the
first old port hit and is unaffected by any new shortcut between old
ports. The new vertices are closer. Thus the maximum port distance is
2r-1, attained by an original endpoint.

The proof correctly stops peeling after exactly r-2 rounds, when the
half has order eleven. It does not assert maximal peeling. This matters
because the base H_2 also has equal port neighborhoods. The stopping
rule is determined by the original order and is preserved by ordinary
isomorphisms, so this coincidence does not collapse two base types.

4. Construction, metrics, and centre for both parities
-------------------------------------------------------
Gluing two extended halves to a new independent pair X gives order
2(4r+3)+2=8(r+1), with every vertex of degree four. Bipartitions extend
across the gluing. X together with any two of its four port neighbors
gives a four-cycle, so girth is exactly four rather than merely at least
four. Every half vertex is within 2r of either X vertex. The original
endpoints in the two components after deleting X have distance exactly
4r because every path between them crosses X. These observations prove
both diameter bounds.

Each X vertex has eccentricity exactly 2r. For z outside X, the
original endpoint e of the other half satisfies
  dist(z,e)=dist(z,X)+2r>2r.
Both X vertices are false twins, which permits the same minimizing
choice at either side of this concatenation. Hence the centre is
intrinsically exactly X, and no additional vertex can join its full
false-twin class.

In the forced chain the two-element port, anchor, and interface sets
have successive geodesic positions beginning at position three. There
is no bypass: each internal anchor or interface separates the ends.
The midpoint position is 2r, so the centre is X_(r/2) for even r and
F_((r-1)/2) for odd r. From position three to the last ports at 2r-1
there are (2r-1-3)/2=r-2 extension steps on each side. Thus both parity
cases give exactly the claimed extended bases, not two different
families of ordinary graphs.

5. Completeness, ordinary disjointness, and count
------------------------------------------------
The equality structure accounts for the full graph, so every graph in
the stated domain is one of the glued pairs. Any ordinary isomorphism
preserves eccentricities and therefore X. It permutes the two connected
components after deleting X. Exact intrinsic peeling then recovers an
unordered pair of the three ordinary base types. Conversely matching
base types extend through every extension and the final complete
attachments. No port alignment or orientation parameter survives.
The ordinary classes are consequently the six multisets of size two
from {H_0,H_1,H_2}. This proves six classes for all r>=2 rather than
extrapolating from a diameter-eight count.

Scope and authority
-------------------
The two precursor editions cited in the proof were independently read
in the preceding review and their whole hashes were rechecked here.
The new proof also restates the ingredients it needs; no finite census
count or unreviewed classification is used as a premise. Its stated
limits on larger orders, other degrees and other diameter congruence
classes are appropriate. No novelty/priority, completed-original,
conjecture, measurement or Lean credit follows from this static review.
Root adoption and any requested formal or computational checking are
separate. No represented Source, graph data, TeX or Lean was executed;
no canonical/public/Git file was changed.
