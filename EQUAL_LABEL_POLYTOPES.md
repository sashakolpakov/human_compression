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
4,\qquad n,\ 2n,\ 4n,
\quad n\in\{3\}\cup\{2^e+1:e\ge2\}\cup\{2^e-1:e\ge3\}.
$$

This includes 3, 4, 5, 6, 7, 9, 10, 12, 14, 15, 17, 18 and 20,
among other labels. Labels 8, 11 and 13 remain outside this argument.

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

The [independent review](research/case_study/phase131_equal_label_root_review.md)
checks all four proofs, their precise source interfaces and three fresh
computational runs. It distinguishes the repository arguments from
retained mathematics and records the source-access limitations. These
are internally reviewed written proofs; historical priority and current
openness have not been established. Complete Lean verification remains
unfinished.

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
outside this formal package; the allowed-label range above is unchanged.

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
