# Large cyclic subgroups in two-group polytopes

The [complete deduction](research/case_study/phase169_cyclic_index_completion.md)
recovers the high-exponent C-group classification in Mark L. Loyola,
[*String C-groups from groups of order 2^m and exponent at least 2^(m−3)*](https://arxiv.org/abs/1607.01457v1),
Theorem 4.1 and the structural content of Proposition 4.2, with an explicit
correction to the checked edition's final product assignment.

    Module A's forest quotient + the cyclic-index argument and complete model proof
        -> Loyola's high-exponent string C-group classification.

The common quotient has order 2^(2d−1) and exponent four. Every cyclic
subgroup therefore has index at least 2^(2d−3). At index eight, the rank
is at most three; equality puts the third lower-central subgroup inside
a cyclic subgroup. The intersection property then forces one adjacent
order to be four. The manuscript constructs and distinguishes the two
remaining families, proves their exact presentations and product
decompositions, and handles every small and disconnected case.

This recovers the classification without the source's exhaustive
abstract-group catalogue. That catalogue, its completeness and its
involution tables are separate source results and are not recovered.
Accordingly this is a **partial source contract**, not a replacement for
the entire 31-page paper or a seventh complete source in Module A.
The auxiliary source is outside the fixed 161-entry registry.

The classification remains attributed to Loyola. Our contribution here
is the deduction through the shared forest quotient and cyclic-index
reduction, with all remaining local arguments supplied. The source's
Theorem 4.1 reverses its final parameter assignment: the inner product is
direct at epsilon=0 and nontrivially semidirect at epsilon=1, as in its
Proposition 4.2. The actual actions establish this correction. No
historical novelty or correction-priority claim is made.

Read the [source ledger](research/case_study/phase169_cyclic_index_ledger.json),
[independent review of the initial argument](research/case_study/phase169_cyclic_index_review.md),
and [separate review of the completed proof](research/case_study/phase175_cyclic_index_root_review.md).
The complete added proof costs 14,968 UTF-8 bytes; the exact retained U
and A inputs and the corroborating programs are recorded separately.
No matched compression ratio or complete Lean certificate is claimed.
This is a deduction of known results, not a solved open conjecture.

Fresh public checks cover 11 coordinate models through M=128, all 704
marked-subset intersections, seven literal presentations through M=32,
both inverse presentation maps and the excluded small boundary case.
They corroborate the written uniform proof. Reproduce them with:

```sh
python3 -B -O research/case_study/phase169_cyclic_index_verify.py --output-dir /tmp/NEW-cyclic-index
```

The runner needs Python and GAP, and accepts `--gap /path/to/gap`.
It needs no primary PDF, private catalogue or earlier computation output.
