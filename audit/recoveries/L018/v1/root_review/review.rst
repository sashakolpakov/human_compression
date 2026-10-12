Review of the complete L018 recovery
====================================

Root independently read all eleven pages of the bound arXiv2311.02385v1
source, all 36 source dispositions, both complete replacement manuscripts,
the five complete C++ search programs, the whole arithmetic and coloring
certificates, source-example checks, validation oracles and replay driver.
The complete source figures on pages four and six were directly inspected.
All eight final replacement pages were rebuilt and directly viewed. Root did
not author the candidate. The completed fresh exhaustive replay passed all 11,210 unique parameter
cases, with exact node counts. The corrected principal recovery is ACCEPTED.

Written mathematics
-------------------
The seven-piece lower bound treats real axis-parallel lengths. A minimal
counterexample has no spanning piece: either remaining rectangular region
would be a smaller perfect partition, or one piece congruent to the spanning
piece. The four corner pieces are distinct. If every side has two pieces,
the equal-area equations force congruent opposite corners. Otherwise a side
has k>=3 pieces of distinct heights. Their upper-neighbor sets are disjoint,
and the lowest has at least two upper neighbors, giving at least 2k+1 pieces.
The affine normalization is used only in the equal-area equations; the equal
opposite widths and heights imply congruence back in the original rectangle.

A generic transversal gives integral positions from integral side lengths.
The leftmost lowest uncovered cell lies at the bottom-left of its actual
piece. More generally an exposed strict valley forces the same placement
and cannot cross the higher neighboring skyline. Choosing any such valley
by fewest legal choices preserves completeness. Unordered factor-pair
identities enforce noncongruence even when only one orientation fits.
Disconnected open components require area divisible by the common area;
side and valley subset sums use each unused shape once, with rotations as
alternatives. Ordinary square normalization takes a least corner identity
to bottom-left, then uses the remaining diagonal reflection. Repeated corner
identities are allowed. These tests are necessary, not completion oracles.

The row-parity derivative gives the endpoint multigraph used in the hard
840/21 case. All 21 shapes must occur. The four odd-side shapes have even
partners 64 times 7,5,3,1; no proper nonempty signed subset cancels. They
therefore orient along one common axis. The four distinct interval lengths
and even endpoint degrees force a connected four-cycle. Its six exact
patterns, even shifts and two horizontal parity relations are all retained.
Future prescribed placements are tested only by necessary skyline space.
For 840/20, choosing 20 of 22 shapes forces precisely eight of nine odd-side
shapes. Signed sums give 44 configurations, reduced to 26 after the stated
axis normalization. Closure under quarter turns and reflections is explicitly
checked. Both specialized searches correctly remove the earlier diagonal
width<=height normalization after fixing an axis. Thus their symmetries are
compatible; the stronger test is not silently intersected with an unrelated
canonical orientation.

Complete code and finite evidence
---------------------------------
Root reviewed every complete C++ variant, including both specialized copies,
by full base reading and exact deltas. Bounds cover the full executed domain:
W,H<=1000, 17-word side bitsets and at most 63 shape identities. Subset updates
read an old copy per identity, so both rotations cannot reuse one rectangle.
Every placement changes the exact skyline and used mask and is restored on
return. A timeout propagates UNKNOWN and never proves exclusion. The explicit
compile flag '-include array' supplies the omitted historical standard header;
no source bytes are changed to hide this dependency.

The independent cell-cover oracle uses a different state representation and
checks 27 complete small cases, with no unresolved cases. Five relaxed positive
examples have literal tilings which fail only noncongruence, so the controls
also exercise successful completion. The arithmetic roster is reconstructed
from all divisors and unordered fitting shapes, not the source's filtered
list. The full coverage contract has 103 square cases on 49 squares and
11,126 rectangle cases on 6,431 rectangles; their union has 11,210 parameter
triples. Every selected exclusion is tied to an entire program and a completed
receipt. All ten untrimmed historical receipt files are retained. Nine malformed
coverage or geometric controls are rejected. The accompanying root replay
records fresh execution of every unique selected triple and requires the same
exact deterministic node count as its bound receipt. Correct compiler and
native execution remain explicit proof premises; this is not a Lean check.

Source corrections and dispositions
-----------------------------------
The principal nonexistence results are recovered for squares through side
1000 and rectangles with both sides through 400. This does not make every
printed supporting sentence true. The displayed area-1008 factor list contains
transcription errors. A literal five-piece perimeter at side84 uses a spanning
strip; the printed first-perimeter threshold360 requires an additional
no-spanning or recursive convention. It is not a perfect-tiling counterexample.
The printed impossibility of summing216 is false: 72+144 uses two distinct
remaining shapes. The independent containing-hole obstruction for that
perimeter remains valid. The width160 example forces the stated overlap.
Rectangular orientation lists need not be closed under rotation, as the exact
60 by14 example shows. The finite search uses explicit unordered identities
and does not rely on the source's reversal index or halving convention.

All source background, historical timings and implementation-specific filtered
rosters have explicit dispositions. They are not represented as new theorems
or prerequisites of the complete exclusion. The current retrieved Julia
revision is not asserted to be the historical program. General existence of
an integer perfect partition and the logarithmic defect conjecture remain
unanswered. The corrected principal recovery adds one original only upon
publication. It adds no conjecture solution, formal declaration or measured
compression factor. Historical software and external proof-acquisition costs
remain unmeasured.
