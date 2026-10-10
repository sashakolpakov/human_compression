# All-rank termination of the label-eight presentation

This package proves termination of the actual oriented label-eight presentation for every rank `d >= 3`, on the alphabet of `5*d-7` letters. It also proves that the existing leftmost collector reaches an irreducible word with some finite amount of fuel. These are Lean theorems about the literal presentation table, not tests at selected ranks. They do not yet formalize confluence, the normal-form group-order formula, the intersection property, or the complete polytope construction.

## A reusable order for triangular presentations

Write a word as a list of natural-number letter indices. For a lower index `k`, let `blocks k u` be the list of words obtained by cutting `u` at every occurrence of `k`. Empty blocks are retained. Thus

`blocks 0 [2,0,1,0,0,3] = [[2],[1],[],[3]]`.

The number of blocks is one more than the number of occurrences of the separator. The definition is explicit in `formal/TriangularWordTermination.lean`: prepending the separator inserts an empty first block, while prepending any other letter prepends it to the first block.

Define a relation `BlockOrder k n` recursively. At depth zero it is the empty relation. At depth `n+1`, compare the block lists at separator `k` in shortlex order, using `BlockOrder (k+1) n` to compare their entries. Shortlex first compares the number of blocks. Only when those numbers agree does it compare the block entries lexicographically. This length comparison is essential: unrestricted lexicographic order on arbitrary finite lists of a well-founded alphabet need not be well-founded.

The theorem `blockOrder_wf` proves that this relation is well-founded on all words, by induction on `n`. The successor step is the inverse image of the well-founded shortlex relation under `blocks k`. The finite active interval is `[k,k+n)`. Words may contain other letters, but a strict local decrease below will only be asserted for input letters in the active interval.

The specialized imported well-foundedness result is `List.Shortlex.wf`, from the pinned Mathlib file `Mathlib/Data/List/Shortlex.lean`; standard closure under inverse images and subrelations is also reused. That source credits Hannah Fechtner, 2024. Its proof, including its internal accessibility argument, is reused. The present package supplies the recursive block order, its compatibility with word contexts, the triangular rewriting theorem, and the connection to the actual label-eight table. It does not claim historical novelty for termination of triangular collection processes.

## Why contexts preserve strict decrease

The theorem `blockOrder_context` proves that a strict comparison survives concatenation of the same prefix and suffix on both sides. This is required because the presentation permits a relation to be applied anywhere in a word.

For a prepended separator, both block lists acquire the same empty first entry. For another prepended letter, only the first block changes, and the induction hypothesis supplies strict monotonicity of that modification. The corresponding proof for an appended separator appends an empty last entry. For another appended letter, only the last block changes. The auxiliary `lex_last` lemma explicitly uses equality of block-list lengths, so that modifying the last entry cannot turn a proper-prefix comparison into an invalid one. The proof does not assume a general, unproved monotonicity property of lexicographic order.

Induction over a prefix and reverse induction over a suffix then yield the full two-sided context theorem. These are statements for arbitrary words; they require no rewriting hypothesis.

## Why both kinds of relation decrease

The generic relation `TriangularStep bound` has exactly two constructors:

- A square `a a` may be replaced by any word whose letters strictly exceed `a`, provided `a < bound`.
- A descending pair `a b`, with `b < a < bound`, may be replaced by `b a` followed by any word whose letters strictly exceed `a`.

Both constructors allow arbitrary common prefix and suffix. No bound on tail length occurs. In this generic relation the higher tail letters need not be below `bound`; letters outside the active interval cannot themselves be inputs of a permitted rule.

For the square relation, consider the first relevant separator. When it is `a`, the source has three blocks and the replacement has one, so shortlex decreases by length. At any smaller separator, neither word contains that separator, and the assertion reduces to the next recursive order. This is the theorem `square_decreases`.

For a swap, the first relevant separator is the smaller letter `b`. The source `a b` has blocks `[[a],[]]`, whereas the replacement `b a tail` has blocks `[[],a::tail]`. These lists have equal length. Their first entries compare strictly because the empty word is below the one-letter word `[a]` in the higher-letter order. The possibly long correction tail occurs after this first strict decrease and therefore does not obstruct it. Smaller separators again reduce the assertion recursively. The lemma `nil_lt_letter` supplies the required comparison with the empty word, and `swap_decreases` supplies the swap comparison.

The context theorem extends these local decreases to each literal contextual step. The theorem `triangular_termination` concludes that the reverse of `TriangularStep bound` is well-founded, by inclusion in the constructed well-founded order. Neither termination nor confluence is present among its hypotheses.

## Instantiation with the actual label-eight table

The file `formal/LabelEightTermination.lean` imports the frozen literal definitions from `LabelEightCriticalPairs` through `LabelEightTriangular`, together with the generic termination module. It never replaces the actual table by an assumed terminating relation.

The retained phase174 file proves, by splitting the literal table and checking its index arithmetic, that all square and correction tails are strictly higher than the larger input letter. It also proves that the actual contextual relation preserves the alphabet and any lower alphabet cutoff. These previously proved table facts are paid dependencies of the termination proof.

The theorem `uniform_step_refines_triangular` examines an actual `Step d u v`. The finite-alphabet assumption on `u` bounds the redex letters. Equal letters use `square_tail_triangular`; unequal descending letters use `correction_triangular`. Thus the actual step is an instance of the generic triangular relation, and `uniform_step_decreases` gives its strict decrease.

The theorem `uniform_step_accessible` proves accessibility for the reverse of the actual `Step` relation from every bounded word. The induction hypothesis is applied to each actual successor, after `uniform_step_preserves_range` establishes that the successor remains in the finite alphabet. This proves that no infinite sequence of actual forward rewrites starts at such a word. The companion `uniform_bounded_step_wf` states the same conclusion as a well-founded relation on the subtype of bounded words.

Finally, `collector_terminates_of_accessible` follows the literal `next` function. If it returns `none`, zero fuel suffices. Otherwise `next_sound` supplies a genuine step to its returned word; accessibility supplies sufficient fuel there, and one additional unit suffices for the original word. Consequently, `uniform_collector_terminates` proves

`exists fuel, next d (collect d fuel u) = none`

for every `d >= 3` and every word in the `5*d-7` letter alphabet. This is an existence theorem. It supplies no numerical worst-case fuel bound, and irreducibility alone does not imply uniqueness of the result.

## Formal trust and reproducibility

The two new sources are `formal/TriangularWordTermination.lean` and `formal/LabelEightTermination.lean`. They add eleven printed axiom reports. The complete replay also checks eight retained reports in the literal core and phase174 table module. Every report uses only Lean's standard `propext`, `Classical.choice`, and `Quot.sound`, or a subset of them. No unproved placeholder, user axiom, native evaluation axiom, sufficient-fuel assumption, or confluence assumption occurs.

Run the isolated check from the case-study directory:

```sh
python3 phase172_termination_check.py \
  --packages /path/to/pinned/packages \
  --lean /path/to/lean \
  --output-dir /path/to/fresh/output
```

The runner requires a fresh output directory and verifies the frozen source hashes, compiler version, package revisions, and tracked dependency cleanliness. It recompiles the pinned upstream Shortlex source in a private overlay, then recompiles all four local modules. Other pinned dependency objects remain cached inputs. The overlay only reads those objects through symlinks and does not write the dependency cache. The runner replaces inherited `LEAN_PATH`.

The first isolated author replay passed in 21.11 seconds. Its build report records source and object hashes, logs, individual compilation times, and peak child-process memory. This author replay is separate from the root review and any subsequent public replay.

Negative controls distinguish three boundaries: the hypotheses needed for an order decrease, the exact orientation and strict-tail restrictions in the generic relation, and immutable input/output checks in the runner. Rejecting a false decrease does not prove that every other rewrite system violating these hypotheses is nonterminating.

## What remains outside this package

The finite rank-14 critical-pair certificate is an independent retained result. The present package does not formally transport that certificate to arbitrary rank. Such a transport, followed by a local-confluence argument and the terminating-rewriting theorem, is still needed for formal all-rank confluence. The group construction, normal-form count, intersection property, and source relators beyond the existing finite certificates likewise remain outside these two new modules. Their written proofs are not silently promoted to Lean-verified claims here.

This package adds formal assurance to one part of the label-eight construction. It creates no extra solved-conjecture catalogue entry, whole-paper compression credit, page compression ratio, or historical-priority claim.
