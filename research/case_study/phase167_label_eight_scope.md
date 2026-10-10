# A kernel certificate for the finite label-eight rewrite calculation

10 October 2026. This package formalizes the finite calculation used in
*A uniform class-four construction for label eight*. The three Lean
sources prove reachability under the literal presentation rules, finite
critical-pair joinability, reduction of eight particular source words,
and closure of the finite alphabets. They do not formalize the manuscript's
passage from a finite calculation to groups in every rank.

## 1. The statements actually proved

Write a word as a finite list of natural numbers. In rank fourteen the
alphabet is the set of indices less than 63, ordered as

\[
r_0,\ldots,r_{13};\quad x_0,\ldots,x_{12};\quad
y_0,\ldots,y_{11};\quad z_0,\ldots,z_{10};\quad
w_0,\ldots,w_{12}.
\]

Thus the starting indices of these five blocks are 0, 14, 27, 39 and
50. In rank three the corresponding block starts are 0, 3, 5, 6 and 6;
the (z) block is empty, and the alphabet has eight letters. The functions
`decode`, `x`, `y`, `z` and `w` implement exactly these indices. Their
definitions make sense for other natural-number inputs, but no uniform
alphabet theorem is asserted here.

The function `rule d a b` is the right-hand side of the oriented
presentation relation on a nonincreasing pair (a,b). Equal pairs are
removed, except that (x_i x_i) becomes (w_i). A strictly decreasing
pair becomes its reversal followed by the specified correction word.
The definition `correction` is the literal table in the uniform
manuscript, with the same higher-letter-first convention. In particular,
the correction for (x_i r_{i-1}) contains **both** (w_{i-1}) and
(w_i); the corrections for neighboring (x)'s and for (y_i r_{i+1})
are also retained.

`Step d u v` means that one such relation is applied inside an arbitrary
prefix and suffix. `Bounded m u` means every letter of (u) is less than
(m). The relation `AlphabetStep d m` requires a literal `Step` and
boundedness of both endpoints. Consequently its reflexive transitive
closure describes a sequence all of whose intermediate words are on the
finite alphabet. It does not permit an excursion through additional
letters.

The first principal statement is
`rank14_critical_pairs_join_in_alphabet`. For every

\[
0\le c\le b\le a<63,
\]

the words

\[
\operatorname{rule}(14,a,b)\,[c]
\quad\text{and}\quad
[a]\,\operatorname{rule}(14,b,c)
\]

have a common descendant under `AlphabetStep 14 63`. These are the
two one-step reducts of ([a,b,c]). The quantifiers include repeated
indices, and therefore include ambiguities involving square relations.
There are (inom{65}{3}=43,680) such triples.

The second principal statement is
`rank3_source_word_reduces_in_alphabet`. For each integer (k) with
(0\le k<8), the literal word

\[
\bigl([1,2]^k[0,1]^k\bigr)^2
\]

reduces to the empty word under `AlphabetStep 3 8`. Here list powers
denote repeated concatenation. In the marked-group notation this is the
word (((r_1r_2)^k(r_0r_1)^k)^2). This Lean theorem quantifies over
these eight natural exponents. The extension to every integer exponent
uses exact adjacent order eight in the written construction and is not
part of this formal certificate.

## 2. Why the Boolean calculation proves these statements

The normalizer `collect` has an explicit fuel argument. At each step
`next` chooses the first nonincreasing adjacent pair. The theorem
`next_sound` proves that a chosen successor is a literal contextual
presentation rewrite. Induction on fuel then proves
`collect_reachable`: the output of the bounded normalizer is reachable
from its input. If fuel is exhausted, the current word is simply returned.
Neither this lemma nor its consumers assume termination, irreducibility
of the output, confluence, or sufficient fuel.

For a descending triple, `criticalCheck` compares the outputs obtained
from its two one-step reducts. `criticalCheck_sound` turns a true Boolean
comparison into equality of those outputs and uses the two reachability
proofs to obtain a common descendant. `allCritical_sound` discharges
membership in the three finite ranges explicitly. The ranges are
(a<63), (b<a+1) and (c<b+1), so none of the repeated-index cases
is lost.

The complete critical-pair calculation uses fuel 32 on each branch. It
is divided into 63 closed row lemmas, each proved with ordinary `decide`.
`allCritical14_verified` combines these lemmas. This division controls
the working set of kernel reduction; it does not replace evaluation by
an external program. The eight source words use fuel 256. Their Boolean
test is also proved with ordinary `decide` and is converted to actual
reachability with `collect_reachable`.

Finally, the two finite `ruleClosureCheck` evaluations prove that every
applicable rule stays inside its alphabet, for ((d,m)=(14,63)) and
((3,8)). `step_preserves_alphabet` handles arbitrary contexts.
`reachable_restrict` inducts over a sequence of rewrites, obtaining a
sequence in `AlphabetStep` and boundedness of its endpoint. The initial
critical branches are bounded by rule closure. `sourceWord_bounded`
proves boundedness of every source word directly, for every natural
(k), without a finite lookup. These facts give the two principal
finite-alphabet theorems.

## 3. Relation to the written proof and attribution

The mathematical input newly encoded here is the complete label-eight
power and commutator table of `phase161_label_eight_uniform.md`.
The Python collector in `phase161_label_eight_collector.py` is useful
for comparison and was the earlier executable calculation. Neither
Python's answers nor a hash of its answers is imported as a Lean premise.
The Lean source independently encodes the table and checks its own
literal rewrite sequences by kernel reduction.

This is a formal implementation and proof of a finite lemma in that
construction, not a separate claim of historical novelty. The general
notion of critical-pair joinability and the closure relation are standard;
the implementation uses Lean and Mathlib's existing list and relation
infrastructure. The source problem and the retained construction inputs
remain attributed in the uniform manuscript and the equal-label question
catalogue. No principal-source replacement or compression credit is
assigned to these three implementation files.

The written manuscript still supplies all of the following deductions:

- termination of collection in arbitrary rank;
- preservation of support, the compression of a triple's support to
  rank fourteen, and preservation of every intermediate rule;
- the passage from critical pairs to all-rank confluence;
- unique normal forms, the presented group, its order, generation,
  exact adjacent label, nilpotency class and intersection property;
- the extension of the eight source words to every integer exponent
  and the regular-polytope correspondence.

In particular, finite joinability is not called an all-rank Lean proof.
It does not identify the universal source group or settle an all-label
conjecture. The later (8n) construction also needs its separately
proved parity-mix and concrete odd-label inputs.

## 4. Replay and trust boundary

The default replay needs only these five project files:

```text
phase167_label_eight_check.py
formal/dependency_manifest.json
formal/LabelEightCriticalPairs.lean
formal/LabelEightFiniteCertificate.lean
formal/LabelEightAlphabet.lean
```

With the pinned package checkouts and installed Lean compiler available,
run

```text
python3 -B -O phase167_label_eight_check.py \
  --packages /PATH/TO/.lake/packages \
  --lean /PATH/TO/lean --output-dir NEW_DIRECTORY
```

The runner refuses occupied outputs, pins all three source hashes and the
dependency manifest, verifies the compiler version and package revisions,
checks tracked dependency cleanliness, and compiles all three sources
into fresh local objects. It replaces the inherited `LEAN_PATH` and
checks all fifteen requested declaration reports against the standard
axiom allowlist. Sixty-three additional row declarations and three small
support lemmas are checked as parts of the same source compilation and
as dependencies of the reported theorems.

The local sources contain no unproved declarations, proof placeholders
or native-evaluation proofs. The compiler and existing compiled package
dependencies remain part of the explicit trust boundary; this runner
does not claim to rebuild all of Mathlib.

`phase167_label_eight_controls.py` supplies separate author controls. It
tests changed inputs and occupied outputs, and deliberately changes four
commutator or power entries. For each mathematical mutation the altered
generic rewrite code must still compile, a specified critical comparison
is kernel-proved false, and the corresponding assertion that it is true
must be rejected. These are sensitivity checks, not an independent
mathematical review and not a substitute for the positive proof.
