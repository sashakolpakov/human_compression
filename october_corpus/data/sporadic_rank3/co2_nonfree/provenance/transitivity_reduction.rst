Co2 generation by certified connectivity in the acquired 2300-point action
========================================================================

Status: SOURCE/math assessment only. No row was parsed, evaluated or assigned
a generation result here. No scientific function, group operation, GAP/helper,
compiler, control or operational mode ran. All existing sources/results remain
unchanged. The new consequence below reuses explicitly attributed maximal-
subgroup classification; it is not a new classification or novelty claim.

Actual remaining domain and acquired work
----------------------------------------

The 169..178 ROOT gate f797da8b completes the accepted top cover 1..178.
There are 24,690 conditional C1\A/S12 rows, not 24,690 generating markings.
The degree 2300 named faithful primitive model has A=G=Co2, order 42,305,421,312,000,
U=C1 of order 1,474,560, pointwise S12 of order 1,280, and setwise T12 of order 2,560.
The old lower algorithm/exhaustive execution supplies disjointness/coverage;
full mass and distinct literal rows alone do not prove it. Its explicit
positive_orbit_bijection_checked=false qualification is retained. The84/87
numeric ledger and generation/marking/duality duties have not changed.

Pair4's accepted source evaluates Size(Group(a,b,c)) and then, for generating
rows only, RepresentativeAction(S,b^swap,b). Its prefix/suffix union covers
all 15,766 S4 rows and yields g=3300,f=10,D=1655. We reuse the accepted endpoint
and IP/count arguments, not that cell's answers. Pair12's reviewed selected
provider source already returns bounded adopted rows without rerunning lower
enumeration, and retains the exact old candidate body. Its future driver must
honor the progress-stream/two-global preamble explicitly required by its
distinct SOURCE peer. This assessment does not silently modify that body.

Existing fixed-point and degree23 character/eigenline obstructions have been
checked already. All three remaining selectors[12,1],[15,1],[16,1] have endpoint
traces(-1,-1,-1), middle trace-1, sign dimensions(5,6,6,6) and(11,12), maximum
sum 18<23. They pass the necessary inequality. Repeating it gives no new zeros,
and no converse generation assertion follows from that pass.

First reuse: reject every nonfree S row without subgroup-order work
-----------------------------------------------------------------

For an adopted row[r,m], b=y^r and its S-orbit length is l=m/|U|. Its
stabilizer is C_S(b)=C_A(a,b,c). If <a,b,c>=G=A, this is Z(G)=1. Therefore

  generating => l=|S|, equivalently m=1474560*1280=1887436800.

The implication already appears as the accepted reader's free-action check
(pointwise_chain/protocol.py, lines68..77). Applying its contrapositive before
a generation calculation is sound under the same acquired orbit-size premise.
It supplies a negative generation flag, not the exact proper subgroup order.
Free rows are not thereby generating. This is reuse of a proved check, not a
new claim that arbitrary row masses certify an orbit partition.

One can bound the possible savings without reading any individual row. Put
N=24690 and M=|G|/|U|=28690200. Every orbit length is a positive divisor of1280;
a nonfull one is at most 640. If k rows have length1280, then

  1280k+(N-k) <= M <= 1280k+640(N-k).

Hence 20139<=k<=22412, so at least 2,278 and at most 4,551 rows have nonfull length
and are certainly nongenerating. These are conditional integer consequences
of the adopted N/mass, not an acquired row distribution or identified row IDs.

Main reusable criterion: transitive is equivalent to generating
--------------------------------------------------------------

Retain the complete maximal-subgroup classification supplied by CTblLib's
stored Co2 Maxes attribute, with the meanings of the named subgroup tables.
Its manual explicitly says a stored Maxes value contains exactly one class
representative for every maximal-subgroup conjugacy class. This classification
premise was already explicitly retained in our independently accepted L045
sporadic-counting component, which includes Co2. That component does not prove
the classification, and we do not turn a software list into a proof of its own
completeness. The exact local source records and their ordinary table orders
are pinned in source_findings.json, with primary definition/manual locators.

The eleven maximal subgroup types and orders are:

====================== =============
U6(2).2                18393661440
2^10:M22:2             908328960
McL                    898128000
2^(1+8):Sp6(2)         743178240
HS.2                   88704000
2^(1+4+6).A8           41287680
U4(3).D8               26127360
2^(4+10)(S5xS3)        11796480
M23                    10200960
3^(1+4):2^(1+4).S5     933120
5^(1+2):4S4            12000
====================== =============

Only M23 has order divisible by 23, and its order has5-adic valuation 1.
Thus no proper maximal subgroup has order divisible by 25*23.

Proposition. For any H<=the acquired G in this precise 2300-point action,
H=G if and only if H is transitive on all 2300 points.

Proof. G is transitive by the acquired primitive-model premise, so H=G
implies transitivity. Conversely, transitivity gives 2300=2^2*5^2*23 dividing
|H| by orbit-stabilizer. If H<G, finiteness puts H inside a maximal M. Then
25*23 divides |M| by Lagrange, contrary to the complete table above. QED.

Faithfulness and degree/order alone would not prove this proposition. Exact
named-group identification, actual transitive action, H<=G, and the complete
maximal classification/orders are essential. H<=G follows for these inputs
from the adopted endpoints and b=y^r with r in A=G, not merely from an
arbitrary permutation's shape. The criterion works for pair16 as well as12;
it does not equate their distinct S-orbit domains.

This is stronger than a positive word-order sieve: a pair of word orders
excluding every maximal would prove generation, but failure to find such
words says nothing. Connectivity gives a complete decision on the finite
2300-point domain for every row. No random word, subgroup-order calculation,
maximal embedding, new character representation or repeated top/lower search
is required. We found no prior application of this converse in the scoped
existing Co2 chain/pointwise/provider notes or original L026 Section5.4; the
old fixed-point argument uses only generation=>transitivity. This is a
scoped reuse finding, not a claim about all unpublished history or novelty.

Small exact certificates and bounded next method
-----------------------------------------------

For a row, take the three actual permutation generators(a,b,c). A BFS starting
at point1, using these three involutions, visits at most 2300 points and scans
at most 6900 generator edges. No subgroup or Schreier-Sims order is needed.

* Positive: provide discovery-order point IDs q[1..2300], parent positions p,
  and labels e in1..3. Require q to be exactly a permutation of1..2300,
  q[1]=1,p[1]=e[1]=0, and for each j>1 require1<=p[j]<j and
  q[p[j]]^generator[e[j]]=q[j]. Every point is then reachable, proving
  transitivity, and the proposition proves generation. No trusted BFS count
  or claimed Size(H) replaces these checks.
* Negative: provide a nonempty proper subset O containing1 and check that
  all three generators send every point of O back into O. Then O is invariant
  (the generators are involutions), so H is intransitive and cannot equal G.
  This negative certificate needs no maximal-subgroup classification. A cap
  or partial BFS with an unclosed frontier is not such a certificate.

A separate small saved validator can check these edge/tree/subset conditions
using the acquired exact 2300-point permutation representation/parsing and
conjugation helpers. It must authenticate the selected lower row, endpoints,
canonical model and full source/runtime/25-gap/84-cell boundary first.
Execution of those checks is saved scientific validation, not metadata.

The smallest production change would be a separately named generation variant
of the reviewed selected-interval middle, replacing only the two generation
lines with this certified decision and a typed certificate output. The old
body/parser must remain byte-unchanged. Exact generated_order for a proper
subgroup is not supplied by a closed orbit or a nonfree-row obstruction: it
must be explicitly unavailable in the new result schema, rather than0 or a
fabricated divisor. A positive certificate proves the actual order equals
the acquired |G| but must distinguish that deduction from a Size(H) call.
The old journal/parser insists on a positive exact order for every negative
row, so a genuinely reviewed new protocol is necessary. No existing reader
is asserted to accept the changed result unchanged.

Use the existing provider's immutable source keys and bounded selections;
do not re-emit/re-enumerate all 178 lower blocks. All candidate certificates
and negative records are serialized immediately. The fixed finite operation
count per row is2300 points/6900 transitions; it is not a wall-time or RSS
fit guarantee. Existing 300s/2GiB native/512MiB output, outer 600s/3GiB and6/10
admission3/8 floors remain prospective stopping limits. Larger selections
than the reviewed 256 require their own explicit source-bound change; none
is authorized here. Every unknown/partial outcome stays unpaid. Genuine
SOURCE/math review, tiny positive/negative/damaged certificate controls,
concrete binding, full fresh admission and a ROOT release are still owed.

Intersection property and reversal: what is already paid and what is not
------------------------------------------------------------------------

The accepted endpoint_method.tex explicitly imports the Conder--Oliveros
rank-three lemma via L011: an involution triple generating a nonabelian simple
G, with distinct commuting ends, has full intersection property. Thus a
certified generation decision pays IP under that acquired theorem. There is
no need to add 24,690 independent dihedral-intersection computations. This is
attributed reuse; the present note does not independently reprove L011.

For each generating row, keep the existing exact reversal test with S12,
the actual swap in T12\S12, and the full 2300-point positive witness equation.
Generation/connectivity does not decide self-duality. A useful consistency
consequence is that any reversing witness w satisfies w^2=1: w^2 centralizes
all three generators and hence lies in Z(G)=1. This can restrict a separately
reviewed search to involutions of the actual swap coset, but no such coset
inventory or universal zero-fixed result has been acquired here. The existing
exhaustive RepresentativeAction(S,b^swap,b) method is already sound and remains
the smallest acquired choice; no unproved graph-isomorphism shortcut is used.

S12 has order 1,280, T12 order 2,560. Count g generating S-orbits and f reversal-
fixed S-orbits; only the complete disjoint selected-row union may apply
(ordered,self_dual,dual)=(g,f,(g+f)/2). A partial interval need not satisfy
global parity because its reversal partners can be in another interval.
Do not count the T-action as the original S inventory or infer f from a swap.

Finite route for the last three Co2 selectors
-------------------------------------------

1. For the already adopted 24,690 pair12 rows, acquire all certified generation
   flags and actual reversal outcomes with exact disjoint source-key coverage.
   Compose the full g12/f12 and global parity, then ROOT may adopt[12,1].
2. Reuse the already accepted178-row C1\A/C1 top for pair16. Its separate
   S16 has order 1024, T16 order 2048 and lower index 1440. The prepared
   pair16_saved_top_pointwise_lower source/old chain may reuse the top, but
   cannot reuse pair12's 1152 lower index or its lower representatives. The
   differing full centralizer orders 1280 vs 1024 even rule out an ambient
   conjugacy of the two Klein groups. Pair16 lower refinement remains unpaid.
   Apply the same universal connectivity generation criterion and acquired
   IP/reversal method to its own complete rows; compose g16/f16.
3. The already acquired word [4,2,-4] and full literal checks in gate0f8e6333
   give K16 conjugate K15. Only after actual complete 16 may the accepted
   theorem give[15,1]=(2*g16,0,g16). No separate15 enumeration is needed.

The full 87-cell union and original L026 claim still require their real
source-level joins and exact aggregate comparison. The printed 60370 target
is never an input to a candidate decision or stop rule. Completion of this
Co2 leg does not pay the separate Fi22/O'Nan principal obligations or make
102/105 into105/105. All historical failures and borrowed model/action/IP/
partition/maximal-classification premises remain explicit.
