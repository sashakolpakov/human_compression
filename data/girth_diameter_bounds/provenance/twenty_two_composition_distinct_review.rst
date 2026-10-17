Distinct review of the six-layer and order-95 composition
========================================================

Status: DISTINCT_ACCEPTED_F009_SIX_LAYER_TWENTY_TWO_AND_ORDER_95.
Reviewer: /root/l070_publication.  Reviewed on 17 October 2026.

The complete 19,531-byte twenty_two_composition.rst, SHA256
695b2d472d58d56fed300ffe48d835941f2f1fb551a9d712d7d8a90dfee54ad4,
and its 9,311-byte twenty_two_composition_inputs.json, SHA256
d24c6aa12267dd540ab3bb3f92bc038956aab4fd005da24411b1db42fb9bdbbd,
were read.  No gap was found.  The accepted conclusions are:

* Six consecutive nonsingleton original BFS layers in a connected simple
  quartic graph of girth at least five have total size at least 22.
* Such a graph with a vertex of eccentricity exactly 22 has order at
  least 95.  This includes the diameter-22 domain of the cited cage row.

This is an independent review of the new composition and mixed-radius
packing, using the explicitly acquired local theorems and computational
certificates as premises.  It is not a new implementation of their proof
checker or a replay of their refutations.

Local equality case and certificate interface
--------------------------------------------

The geodesic across the six original layers places the adjacent centres
at indices 2,3.  Both 17-vertex radius-two balls are contained in the
interval.  Girth gives eight distinct saturated centres/parents, at most
one vertex at each common-parent grid position, and distinct private
neighbors for every missing cell.  Thus their union has 26-m vertices.
The geodesic parents at indices 1,4 cannot have a common neighbor, so
11 is missing and m<=8.  The accepted lower bound 21 reduces failure of
the new bound exactly to m=5,6,7,8, with respectively 0,1,2,3 extras.
There is no omitted smaller-m or smaller-total case.

The acquired m8, matching-hole m7, and corrected adjacent-hole m7 gates
cover their exact alternatives.  In particular the adjacent-hole gate
uses proof 3fa848963cda82a37226da95a86cfac29aeaba0211053acafddc37958e358347;
the earlier incomplete edition is not substituted for it.

For m5/m6, the graph-to-CNF direction preserves all original layer indices.
The geodesic private names U11,V11 can be chosen independently within
their parent sets.  Saturated vertices have exactly their prescribed
neighbors.  Interior degrees are four; at index zero the predecessor
outside gives degree at most three inside, and zero is allowed.  Every
positive local index has its predecessor inside.  No last-layer successor
or reversed-BFS predecessor hypothesis is introduced.  The common-neighbor
clauses forbid triangles and quadrangles and permit five-cycles.

The only coverage symmetries independently exchange labels 2,3 on each
side and keep the six anchors and every BFS index fixed.  They preserve
the asymmetric boundary conditions.  The literal partition was checked:
28 three-hole sets form 10 orbits and 56 four-hole sets form 17 orbits,
with every representative and every orbit member accounted for.  No
transpose or layer reversal is needed.

The exact actual-acquisition premise is all_hole_patterns_acceptance.json,
24,280 bytes, SHA256
62450dccbaffed5811dd2ac976000bb95fe31dc290320a8f6df738c4c384ed32.
The reviewer read verify.py and the accepted encoding/coverage arguments,
then rehashed and joined all 27 small result/receipt pairs to their exact
verification requests, cases and producer hole selectors.  Every result
reports complete DIMACS and variable-map reconstruction, the accepted RUP
refutation status and matching formula dimensions; every receipt is PASS,
unchanged-input, reaped and owned-group-absent.  The rectangle is m5_03,
not an extra or missing representative.  Reported checked additions sum
to 43,029.  These checked refutations, not solver UNSAT messages, exclude
the satisfying assignments supplied by the necessary graph encoding.
The accepted fixed-root/active/historical RUP implementation remains an
explicit software premise.  No formula, solver or proof reader was run.

Singleton reduction and end support
----------------------------------

six_layer_twenty_one_acceptance.json (1befdd15630d78611b38c904e86322d0a2234e483f78e1995b048b123e040121)
already gives the exhaustive nonempty surviving COMPLETE singleton sets
{4}, {18}, {4,18}, under order<=94 and eccentricity22.  The empty set is
handled separately.  This composition does not silently select just some
singleton positions or reinstate sets excluded by weaker bounds.

At an internal singleton, the two nonempty even cuts sum to four and
therefore each have size two.  Root paths show that the two induced caps
and intervening sections are connected, with exactly their stated
degree-two boundaries and full other degrees.  The acquired cap bound
20 applies.  All ball supports used in the new proof follow from the
one-step Lipschitz property of ORIGINAL BFS indices.  Reversed original
layers are never assumed to be BFS layers in a cap.

For no internal singleton the disjoint supports give
17+22+22+17+17=95.  For the sole singleton at 4 or 18, the long cap has
the disjoint regular/boundary balls and two six-layer intervals giving
76; with the other cap and their one-vertex overlap this is 20+76-1=95.
The last layer may itself be a singleton without changing these counts.

Mixed-radius bound and the last section
--------------------------------------

At either boundary of the 14-step section, its other exceptional vertex
is beyond radius four.  All local degree/girth/even-cut hypotheses of
boundary_radius_four.rst (8f9a2fbbeb527720b78d92593415283b5daeb4e0bbdda607894789271b4c2b68)
hold.  Write c=|S3|.  For c>=7, B3>=16 and the acquired B4>=19 give
B3+B4>=35.  For c=6, all six labels are the off-diagonal double-parent
labels, independent, with twelve incidences to S4.  Any fourth-layer
neighbor set has disjoint parent coordinates.  The only triples are
the two derangements; neither can repeat, by a quadrangle.  Four
fourth-layer vertices could therefore receive at most 3+3+2+2=10 of
the twelve incidences.  Thus |S4|>=5, B3=15, B4>=20, and the same
joint bound 35 follows.  This does not assert the false universal B4>=20.

The section 4..18 has boundary distance exactly14: original indices give
the lower bound and a geodesic through the unique V4 vertex gives equality.
Its two packings are separately disjoint by supports 4..8/9..14/15..18
and 4..7/8..13/14..18.  Hence nH>=L4+22+R3 and nH>=L3+22+R4.  Adding
these inequalities is valid although the two packings overlap each other.
The two joint bounds give 2*nH>=35+35+44=114, hence nH>=57.  The two
20-vertex caps meet this section only at its respective boundaries,
giving 20+57+20-2=95.  This closes the final alternative.

Checks, attribution and limits
------------------------------

The 31 declared direct input pins and all foregoing small execution joins
were checked: 167 unique files, 2,023,334 bytes in that bounded check.
Literal integer substitution independently gives
P22(0..17)=0,2,4,6,8,17,22,24,26,28,34,39,44,46,48,51,56,61.
The direct support inequalities above, rather than realizability of a
scalar profile, establish the final bound.

The pinned source extraction's physical page22, Table5, directly contains
the row 4 5 22 87 95 >=1.  Thus the theorem supplies its lower-order
exclusion, but not the separately required positive 95-vertex witness,
the number of cages or unrelated source claims.  Moore/interval methods
and BFS framework retain the stated source attribution.  The reviewer
previously contributed some imported cap/section and m7 work; those
already accepted components are disclosed premises, not newly independent
discoveries in this review.  The new composition is by /root/finite_recoveries.

No graph enumeration, solver, RUP replay, compilation, source registration,
CURRENT edit or publication was performed.  The old literal enumeration
prefix remains 2030/14476; a proof superseding the need to extend that
search does not make its unfinished roots enumerated.  Whole-source credit,
positive-witness acquisition and portable public reproduction remain
separate obligations.  No old checkpoint may be discarded merely on
the strength of this local review before the replacement proof package
is safely published and checked from a checkout.
