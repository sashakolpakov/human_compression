Independent review of the finite two-block boundary
===================================================

Accepted without a requested correction, within the exact bounded statement.
The root-authored packet e04647d6c40e18d93b2d944d57348acfa6437029560365278b58a36a08e0cdb9
proves the obstruction for the ten specified normalized permutation actions.
It does not classify all possible H, prove their reduction, handle the other
branches of L047, or establish a full original, question or Lean admission.

Roles and reading
-----------------

The manuscript and required search.g/run.g are authored by root.
Enumeration_volume independently read the complete two-page manuscript, all
three executable files and scope metadata, and directly viewed both final
PDF pages. There was no prior authorship contribution by this reviewer to
this finite packet. The source's exact p.6 normalization argument in the
bound L047 PDF/text was consulted for attribution only; its target rank
theorem was not used as a premise.

Enumeration_review separately started and completed a fresh export-only
execution before this review handoff. This review checks the exact twelve
copied files and binds that execution transparently rather than repeating
an identical full run. The mathematical audit and additional oracles below
are independently authored by enumeration_volume and import no author search
code. This review makes no claim to be independent of GAP's finite group
algorithms or the explicitly retained degree-six catalogue.

Why the enumeration is exhaustive
---------------------------------

1. Prefix candidates are precisely order-two elements outside the generated
   prefix which commute with every earlier generator except the adjacent
   last one. Every subfamily of an independent tuple is independent. The
   index bound is valid because each successive strict enlargement has index
   at least two; a remaining index below 2 to the number of remaining entries
   cannot support such a chain. This bound is a necessary condition only.

2. Conjugation by the normalizer of H preserves the candidate conditions.
   Centralizing each chosen generator gives exactly the stabilizer of the
   ordered prefix. Orbit representatives therefore cover all ordered
   markings inductively. Generation and the actual intersection property
   are checked at full length. Skipping nested pairs in AllIP is valid:
   subgroup generation is monotone, so those intersections are automatic.

3. Every character is determined by its values on a generating marking.
   Testing all binary assignments with checked GroupHomomorphismByImages
   enumerates exactly the homomorphisms to C2. The diagonal lift is injective.
   Normalizer conjugation extends diagonally to W, fixes r, and carries a
   character to another enumerated character, so the earlier orbit pruning
   does not lose a lift.

4. Every cut of the ordered C-marking is considered. The cross-cut
   commutation test is exactly required by the larger string, whose two
   C portions are separated by x,r,y. For x, every C member except the last
   left entry is nonadjacent; for y, every C member except the first right
   entry is nonadjacent. The two literal centralizers in W are therefore the
   complete candidate spaces. Order two and noncommutation with r are then
   imposed explicitly. Since x and y are two places apart, they must commute.

5. With rank=|C| and l=|C_L|, the full tuple has rank+3 entries. The distance
   of r from its nearer endpoint is min(l+1,rank+1-l); those of x,y are
   min(l,rank+2-l) and min(l+2,rank-l). The implementation agrees at every
   cut, includes equality, and checks the already fixed C entries as well.
   Within W, the test 1^g>k is exactly the block-exchanging condition.

6. The simultaneous centralizer of C and r preserves both neighbor candidate
   sets, the block-exchange condition, the string relations, transitivity,
   independence and the intersection property. Consequently pruning x by
   this group is valid while retaining every y. These counts are not
   isomorphism-class counts, as the manuscript explicitly states.

7. Deleting each generator and comparing the generated subgroup with the
   full subgroup tests independence exactly. The complete replay verifies
   that all 154 transitive completions already fail this test. The stronger
   statement does not follow merely from zero final C-group solutions;
   the checker explicitly requires the independent-completion column to
   equal zero, and the review includes a control for this distinction.

Independent finite tests
------------------------

The reviewer oracle enumerates eligible ordered markings without the author's
normalizer recursion, index pruning or prefix-independence pruning for four
small specified actions. It obtains 24, 72, 72 and 288 raw markings for S2xS3,
S3xS3, TransitiveGroup(6,9) and TransitiveGroup(6,11), respectively. Their full
normalizer orbits number 4, 1, 1 and 12, exactly matching the author's counts.
For each orbit representative, independent parity propagation on the Cayley
graph checks every binary assignment and agrees with the four characters.

For the entire degree-six wreath product of order 72, literal element
filtering gives the centralizer and neighbor sets, checks their conjugation
invariance, and finds 36 independent transitive positive pairs. The six
pruned pairs cover all 36 up to the permitted conjugations, and each passes
an intersection test over every pair of subsets. The printed positive triple
is checked literally. A redundant three-transposition family fails both
independence and IP. All 196 tuple positions for ranks zero through six
match the endpoint formulas; the 52 equality positions are retained.

These are bounded structural oracles, not a second full large enumeration.
The full fresh copied-author replay supplies the ten-case census: 59
normalized markings, 154 transitive completions, zero independent
completions, and six actual positive-control C-markings. Ten separate review
controls reject changed totals, a hidden independent survivor, omitted
required code or catalogue trust, and improper full-source/formal claims.

Scope and presentation
----------------------

Both rendered pages are readable and all ten table rows match the exact
report. The source's block-swap normalization is explicitly attributed to
Cameron, Fernandes, Leemans and Mixer, Proposition 2.1, Case 3. The new
character/neighbor enumeration is distinguished from that borrowed step.
The required mathematical programs are the full search.g and run.g;
check.py is operational. No source/program length, factor, catalogue credit,
novelty priority, complete L047 proof or Lean claim follows from this review.
