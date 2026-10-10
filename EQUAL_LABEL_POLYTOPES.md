# Equal-label polytopes and quadratic symmetries

This question-solving track proves specified cases of Li–Zhang,
*Regular 3-polytopes of type {n,n}*,
[Conjecture 3.7](https://arxiv.org/html/2505.09505v1).
It is separate from the modules recovering known published results.
The full conjecture remains unresolved.

For **every rank d ≥ 3**, the reviewed written proofs give finite regular
polytopes satisfying all the source's additional power relations at
labels

$$
4,\ 8,\qquad n,\ 2n,\ 4n,\ 8n,
\quad n\in\{3\}\cup\{2^e+1:e\ge2\}\cup\{2^e-1:e\ge3\}.
$$

This includes 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 17, 18, 20,
24, 40, 56 and 72, among other labels. Labels 11, 13 and 16 remain
outside this all-rank range.

The source asks for a quotient with the required relations and exact
type. The stronger assertion about the entire universal presentation
is proved here only for labels **3 and 4**, giving S_(d+1) and
UT_(d+1)(F₂). At label four its order is 2^(d(d+1)/2).

## Proofs and retained inputs

| Argument | Role |
|---|---|
| [Path blocks and elementary matrices](research/case_study/phase124_equal_label_partial.md) | All-rank constructions at labels 3 and 4, with every parabolic intersection |
| [Quadratic symmetries and a singular vector](research/case_study/phase124_equal_label_char2_bridge.md) | The extra source relations hold on the whole ambient space; the published Brooksbank–Ferrara–Leemans theorem supplies IP for the stated q±1 labels |
| [Parity fibers and interval forests](research/case_study/phase124_even_label_mix.md) | Exact parabolic descriptions preserve IP while doubling or quadrupling an allowed odd label; Dickson parity is a retained classical input |
| [Universal label-four presentation](research/case_study/phase124_universal_four_adapter.md) | A bidirectional relator calculation identifies the source presentation with the retained Biss–Dasgupta presentation |
| [Class-four normal forms and finite support](research/case_study/phase168_label_eight_reader.md) | A finite critical-pair certificate and an all-rank support-transfer proof give label eight, exact group and parabolic orders, full IP and genuine parity |
| [The 8n consequence](research/case_study/phase168_label_eight_mix.md) | The new two-group factor and the earlier orientable odd-label construction discharge the actual parity-mix hypotheses |

The [independent review](research/case_study/phase131_equal_label_root_review.md)
checks all four proofs, their precise source interfaces and three fresh
computational runs. It distinguishes the repository arguments from
retained mathematics and records the source-access limitations. These
are internally reviewed written proofs; historical priority and current
openness have not been established. Complete Lean verification remains
unfinished.

The [label-eight review](research/case_study/phase168_label_eight_review.md)
checks the complete terminating presentation and its support-transfer proof,
with a separately implemented collector. In rank d, the constructed group
has order **2^(5d−7)** and class exactly four. Its normal forms describe
every parabolic, so IP follows uniformly rather than from sampled ranks.
Class at most three is impossible under the label-eight hypotheses.
This constructs a finite image of the source presentation; it does not
identify the universal group.

Four scoped Lean components now verify specific parts of these written
arguments. [Characteristic-two translations](research/case_study/formal/CharacteristicTwoTranslations.scope.md)
prove the power relation on the whole ambient space for every integer
exponent, with no nondegeneracy assumption.
[Label-four relations](research/case_study/formal/LabelFourRelations.scope.md)
prove the local relator equivalence in both directions.
[Interval-overlap cancellation](research/case_study/formal/IntervalOverlapCancellation.scope.md)
and its [finite-marker adapter](research/case_study/formal/FinIntervalOverlapCancellation.scope.md)
prove the complete combinatorial cancellation theorem used by the mixing
argument. Retained presentation and generation theorems and complete
polytope conclusions remain separate formal obligations.
The [publication review](provenance/phase100_review.md) records fresh pinned
compilations and the precise trust boundary.

The [parity-mix construction](PARITY_MIX.md) now also has a complete Lean
proof of its general group-theoretic intersection property. Twelve
supporting modules derive the actual fibers, component coordinates and
character equations before applying interval cancellation. The theorem
requires genuine input characters and both factor intersection properties.
Its [independent review](research/case_study/phase157_parity_mix_review.md)
and fresh public build cover these precise hypotheses and conclusions.
Concrete finite-field applications and numerical order formulas remain
outside this formal package. The new label-eight factor expands the written
application range above; the complete concrete mix is still not formalized.

Three further Lean modules now prove the finite rewriting lemma used by
the label-eight construction. All **43,680** descending triples in its
63-letter rank-fourteen alphabet have joining rewrite paths, and all eight
rank-three source words reduce to the empty word. Every intermediate word
stays in the stated finite alphabet. The [formal review and fresh public
build](research/case_study/phase171_label_eight_formal_review.md) cover the
actual contextual rewrite relation. The 63 row proofs use ordinary kernel
evaluation, with no native-evaluation axioms. Support transfer, confluence
and the resulting all-rank group theorem remain written proofs.

The [uniform table certificate](research/case_study/phase174_label_eight_scope.md)
now proves that every square and swap correction lies strictly later in
the generator order, and that every rewrite preserves the allowed
alphabet, for all ranks. Its five declarations were independently read
and freshly compiled with standard axioms.

The [termination certificate](research/case_study/phase172_termination_scope.md)
now proves a general well-founded order for triangular word rewriting
and applies it to the actual label-eight table for every rank d ≥ 3.
Every word in the allowed alphabet is accessible, and the implemented
collector has sufficient fuel for termination. The [independent reading
and fresh public build](provenance/phase107_review.md) cover all eleven
new printed declarations using standard axioms. This proves neither a
numerical fuel bound nor confluence, unique normal forms, group order or IP.

Finite checks include all parabolics of fifteen explicit groups or mixes,
42 quadratic markings, 2,310 quadratic power words and 8,448 translation
parameter pairs. They support the written arguments without replacing
their all-rank proofs. The distinction from universal presentations is
visible already at label nine: the matrix image has order 1,152, while
the source rank-three group has order 4,608.

## Reproduction

The [export manifest](research/case_study/phase131_equal_label_export.json)
preserves the author notes and reports unchanged. Their earlier scope
statements are extended only by the separately dated additive notes.
Primary publication PDFs are not redistributed.

Use a fresh output path:

```sh
python3 -B -O research/case_study/phase131_equal_label_verify.py --output /tmp/NEW-equal-label-check.json --replay
```

This checks the frozen inputs and reruns all three bounded computations.
It does not certify the general written proofs or establish priority.
No completed source replacement or compression ratio is assigned to
this partial conjecture result.

For the new construction, the [separate export record](research/case_study/phase168_label_eight_export.json)
preserves the frozen proof, its delimiter-only reader and fresh review
reports. Run the author or independent finite collector with a new path:

```sh
python3 -B -O research/case_study/phase161_label_eight_collector.py --report /tmp/NEW-label-eight-author.json
python3 -B -O research/case_study/phase168_label_eight_independent.py --report /tmp/NEW-label-eight-independent.json
```

To freshly compile all three formal sources with the pinned compiler and
dependencies, allow several minutes and several GB of memory:

```sh
python3 -B research/case_study/formal/verify_lean.py LabelEightAlphabet.lean --packages PACKAGES --lean LEAN --timeout 900 --output-dir /tmp/NEW-label-eight-Lean
```
