# Root admission of the Livingstone-graph reconstruction

Date: 2026-10-10. Accepted scope: one literal principal construction,
one explicitly corrected principal construction, and the finite source
components identified in the 17-row ledger. This is an additional source
with component coverage; it is not an additional complete principal-source
contract.

The source is M. I. Hartley, I. Hubard and D. Leemans, *Regular 4-polytopes
from the Livingstone graph of Janko's first group*, Journal of Algebraic
Combinatorics 35 (2012), 193–214, DOI 10.1007/s10801-011-0300-x, L068.
The exact private primary PDF has SHA256
`e40b3ee73dec3754248a7c9b659fc3015f8ee59c2b98ce46141baae8fe825ad9`.
Its full text is referenced, not distributed.

## What is proved

For a transitive group action on each type, a complete base neighbourhood
equal to a stabilizer orbit identifies the invariant incidence relation
with coset incidence. The proof is the usual orbit–stabilizer argument,
written with the full neighbourhood as an explicit obligation. It cannot
be discharged by counting a selected neighbour orbit alone.

The application constructs the literal graph-face families, verifies their
completeness and transitivity, identifies full object stabilizers, and
compares every base neighbourhood with its required orbit. The retained
Module C marking and geometry-recognition results then apply. The named
degree-266 J1 action and its classical Livingstone-graph identification
remain inputs; the source geometry lists are not inputs to the calculation.

All six literal relations defining P are recovered. The resulting
polytope has type {5,6,5}, face counts (1463,8778,8778,266), and the printed
flag-stabilizer lattice. For Q, five relations agree, but the printed
type-2/type-3 relation gives twelve neighbours. Ten corresponding
pair-flags have no type-1 extension. Thus the literal relation does not
define the claimed geometry. The manuscript supplies an explicit witness.

Adding the induced-quadruple condition motivated by source Proposition3.5
gives a regular polytope of type {5,3,5}, face counts
(1463,8778,8778,2926), and the intended stabilizer lattice. The complete
type-preserving automorphism group of each accepted structure is J1:
thinness and chamber connectedness make chamber stabilizers trivial, so
the already regular J1 action reaches the full-group upper bound.

A second, auxiliary source correction concerns Proposition3.3. The common
distance-two set of an edge has 40 vertices, not ten. The white-pentagon
condition in the preceding source paragraph selects the intended ten.
That condition is credited to the source, not presented as a new idea.

## Review and fresh public execution

The frozen phase184 independent review read all 22 primary pages and
checked the disputed definitions, diagrams and stabilizer lattices
visually. It read the entire replacement manuscript, all new mathematical
programs and Lean source, checked all 17 ledger rows and 24 proof spans,
and inspected all six rendered application pages. Root read the complete
replacement proof, independent review, Lean proof, author GAP program,
independent predicate program and portable drivers. Root verified all
author, retained-input, primary-input and reviewer bindings before copying.
Root does not claim a separate new complete primary-paper reading here.

Fresh execution from the public study directory is saved in
`phase189_public_replay/`. The retained C certificate passed in 1.369s,
the source graph reconstruction in 7.122s, and the Lean compilation in
3.692s. These are observations, not complexity bounds. All three logs
match the independently frozen logs byte for byte.

The independent semantic program re-transcribes all twelve literal
relations, using a distance-based opposite-edge test. It retains the
author's graph and object families; it is not an independent implementation
of those constructions or GAP's group algorithms. For all twelve disputed
neighbours, the counts of type-1 extensions are ten zeros and two fives.
Its separate order-ten stabilizer-orbit criterion selects exactly the
same two neighbours as the proposed graph-based repair.

The fresh semantic replay and both reviewer-designed changes passed their
expected-outcome checks. Replacing P's white-pentagon condition with the
orange condition and deleting Q's repair are rejected. The three
author-designed changes—deleting the repair, changing P's colour, and
altering Q's overlap count—are also rejected. GAP can return process
status zero after an error in batch mode; the controls therefore require
the specified rejection and absence of the successful completion marker.
The saved records are in `phase189_public_semantic/` and
`phase189_public_controls/`.

## Formal scope and retained inputs

`EquivariantIncidence.lean` proves three generic declarations: diagonal
orbit reconstruction, inclusion of the local orbit in the neighbourhood,
and the finite-cardinality criterion. The fresh compile reports `propext`
for the first and `propext`, `Classical.choice`, `Quot.sound` for the
other two. There are no placeholder proofs or native-evaluation axioms.
The canonical formal file is byte-identical to the frozen author file
used by the portable driver.

The driver checks Lean 4.32.2, all pinned dependency revisions and tracked
source cleanliness. Compiled dependency objects remain trusted. The
finite calculation uses GAP 4.15.1, TomLib 1.2.11 and the recorded J1-data
hash. Lean does not verify these group calculations, quotient-set
identification or either full polytope theorem. Those are supported by
the separately reviewed written arguments and finite certificates.

The intended constructions and their ingredients remain attributed to
Hartley–Hubard–Leemans and the earlier graph literature they cite.
The classical local design, named J1 data and subgroup algorithms are
retained. The reusable orbit argument is standard. The present contribution
is its exact source-specific application and the explicit audit and repair;
historical priority for a correction has not been established.

## Coverage and cost

The complete local required inventory is 44,524 UTF-8 bytes, and the full
retained U/C texts and C program add 135,006, for 179,530 bytes. The
six-page application is not the complete denominator. The source's
22 pages are bibliographic metadata, not a normalized numerator. No
compression ratio, fixed-coverage decrease, or new sawtooth step follows
from this admission.

The additive L068 overlay raises encoded sources from55 to56 and
known-result component coverage from40 to41. Full-primary reading moves
from16 to17, with full-text-search-only records decreasing from18 to17.
The indexed161 and retrieved102 remain unchanged. Principal-result
records remain18, and principal contracts in Modules A–D remain16.
One new scoped Lean component brings the total to71:70 have no native
evaluation axioms; the historical transfer component retains its four
explicitly recorded native-evaluation axioms. This is not a count of
fully formalized source papers. No open-question result is added.

The frozen phase179 author's "review pending" fields record its original
state. They are superseded by the phase184 independent acceptance and
this admission, without altering their bytes. Frozen source registries,
manuscripts and earlier measurements likewise remain intact.
