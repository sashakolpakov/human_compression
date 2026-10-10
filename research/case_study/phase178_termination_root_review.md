# Independent review of triangular rewriting termination

Date: 2026-10-10. Verdict: admit the two phase172 Lean modules under the
scope below. The root read both complete sources, their imported local
table interface, the author scope, the isolated compiler wrapper and the
negative-control implementation. The root separately rebuilt the four
local modules from the public tree using the repository's generic runner.
This review is independent of the phase172 author.

## Mathematical statement and proof

`TriangularWordTermination` constructs an order on words in natural-number
letters. At each active letter k, a word is split into the blocks between
occurrences of k, retaining empty blocks. These lists of blocks are ordered
by shortlex, using the recursively constructed order on higher letters.
The base relation is empty. Well-foundedness follows by induction from
the retained Mathlib shortlex theorem and inverse images.

The proof establishes compatibility with arbitrary left and right
contexts. Right-context compatibility uses an equal-length lexicographic
lemma; the equal-length hypothesis is present, avoiding the invalid
extension of a proper-prefix comparison by an arbitrary last-block map.
The order need not be total and need not distinguish inert letters outside
the active interval. Neither property is required for termination.

A square aa replaced by a tail of letters strictly greater than a
decreases the number of a-separators at the first relevant level. A swap
ab to ba followed by such a tail, with b < a, decreases the block before
the first b: the empty word is smaller than the one-letter word a. The
tail follows that strict comparison. Both moves therefore decrease the
same well-founded order in any context. The finite bound applies to
letters consumed by a rule; the generic theorem does not require a bound
on tail lengths or tail letters. This stronger statement is consistent:
letters outside the active interval cannot be consumed as redex inputs.

`LabelEightTermination` refines each step of the literal label-eight
table to this generic relation, using the already proved strict tail
inequalities. For every rank d >= 3 and word whose letters are less than
5d-7, alphabet preservation makes every successor satisfy the same
hypothesis. Well-founded induction gives accessibility for the unrestricted
actual step relation starting at that word. A separate theorem gives
well-foundedness on the subtype of bounded words. Finally, induction on
accessibility, using `next_sound` for the literal leftmost collector,
produces some fuel for which the collector reaches a word with no next step.

No termination, confluence or group-theoretic conclusion is smuggled in
as a hypothesis. The sufficient-fuel conclusion is existential; this
package does not supply a numerical fuel bound, all-rank confluence,
unique normal forms, group order, intersection property, or a complete
formalization of the polytope construction.

## Fresh build and trust

The public replay freshly compiled `LabelEightCriticalPairs`,
`LabelEightTriangular`, `TriangularWordTermination` and
`LabelEightTermination` with Lean 4.32.2 and the pinned dependency manifest.
The missing `Mathlib.Data.List.Shortlex` object was rebuilt from pinned
source in a private overlay. No installed dependency files were changed.
Other installed compiled dependencies remain trusted inputs; this is
not a rebuild of the complete Lean/Mathlib toolchain.

All nineteen printed declaration names were matched to their source
`#print axioms` requests. Eleven belong to the two new modules and eight
to retained local dependencies. Every printed dependency is in
`{propext, Classical.choice, Quot.sound}`. There are no native-evaluation
axioms or assumed user theorem axioms in these reports. The two new source
hashes and all twelve author exports plus three retained bindings match
the frozen author manifest. Earlier public build reports are preserved;
the new replay keeps its four fresh reports together in the phase178 record.

The author wrapper additionally enforces source hashes, compiler and
dependency revisions, exact printed axiom reports and fresh output paths.
Its recorded controls include four proved counterexamples, rejected
false decreases and proof mutations, source-change rejection, and occupied
output rejection. The root read those implementations and saved results;
the current independent replay did not rerun the unchanged negative
controls. Rejecting a proposed decrease does not prove that every altered
rewrite system fails to terminate.

## Attribution and accounting

The recursive block-order construction and its application are repository
proofs. They retain Mathlib's shortlex well-foundedness implementation,
attributed to Hannah Fechtner (2024) and Lean community contributors, and
the already published local rule definitions and triangularity proofs.
No historical priority claim is made for the general technique.

This admission adds two scoped Lean components, bringing the public total
to 69: 68 component reports without native-evaluation axioms and one
historical transfer component with four explicitly recorded native axioms.
It adds no source contract, new conjecture-catalogue entry or compression
ratio. Frozen earlier statements that termination was still unformalized
remain historical records and are superseded only on this point.
