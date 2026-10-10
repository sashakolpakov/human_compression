> **Historical reader — archived from `5401cc9`.** This records the earlier
> compilation programme and its dated scope. Its rates, counts and “current”
> wording do not describe the active topic architecture. Use the
> [current programme](../MANUSCRIPT_PROGRAM.md) or the [archive index](README.md).

# Attribution and proof-status annotations

The [annotated ten-source reader](../research/case_study/phase61_ten_source_annotated.md)
places audit signs beside the relevant sections. Its
[attribution ledger](../research/case_study/phase61_ten_source_attribution.md)
and [structured sidecar](../research/case_study/phase61_ten_source_attribution.json)
bind each note to exact spans of the frozen manuscript. The original proof
file remains unchanged; the reader includes the required erratum.

| Sign | Meaning | Evidence needed |
|---|---|---|
| **[B]** | Borrowed result, idea or construction | Original authors/source and precise retained input or source result |
| **[I]** | Repository contribution to the proof or exposition | Description of the contribution and the older ingredients it uses; historical novelty stated separately |
| **[R]** | One shared argument yields multiple earlier results | Named targets and the internal common argument; no numerical saving implied |
| **[C]** | Corrected assertion, scope or reference | Literal issue and exact corrected contract |
| **[V]** | Exact finite computational evidence | Program identity, relevant replay and finite scope |
| **[L]** | Scoped Lean certificate | Exact declaration, source hash and compiler report; an explanation of the unformalized interface |
| **[M]** | Measured compression | Exact numerator, complete denominator, metric, source editions and reviewed measurement |
| **[O]** | Previously open conjecture proved | Exact conjecture/version, accepted proof audit and a separate current-status/priority audit |

“Repository contribution” can mean a shared organization, explicit proof,
correction or new consequence in this exposition. It does not by itself
mean that the idea or theorem is historically new. Elementary group theory,
standard coset constructions and earlier authors' strategies retain their
attribution even when we use new notation or formalize them.

The first annotation pass covers every numbered section and appendix of
Compress_10, its introduction, references and the exact erratum location.
The source authors are credited in the [named intake](../COMPRESS_10.md#exact-intake)
and the manuscript's references. The ledger identifies the principal borrowed
and shared ingredients at each section. Its selected input lists are not
claimed to be complete transitive dependency graphs; the full retained-input
inventory and reviewed contract remain authoritative.

Only the specific K(0) lifting implication receives an **[L]** annotation in
this initial pass. The named Lean declaration proves that algebraic implication
under its explicit image/kernel hypotheses. Geometric recognition, local
mirror compatibility and all applications still require their written proofs.
The repository contains other separately scoped certificates; their presence
does not make the entire section or manuscript formally verified.

There are **no [M] or [O] signs in this edition**. Its ten-source length factor
is still under review, and it claims no newly solved open conjecture. Measured
factors for other frozen manuscripts cannot be transferred to this one.
The general and full five-family cover conjectures remain unproved by this
assembly. Later family results have separate attribution and priority records.

The final audit for each future manuscript should bind four things together:
the exact source/result contract; the complete written proof and borrowed
dependencies; the scoped computational/formal evidence; and the measurement
and novelty decisions. An absent certificate or unfinished priority check
must be recorded as absent. A sign is a compact view of that record, not a
substitute for it.

## Reproduce the annotations

```sh
python3 scripts/annotate_manuscript.py --output-dir /tmp/human-compression-attribution
```

Use a new directory. The script checks the manuscript, every anchor/span,
the review and certificate hashes, and marker prerequisites. It writes an
annotated Markdown reader, a ledger, a Pandoc version with margin-note blocks,
and a report. Removing its recorded annotation insertions must recover the
original manuscript byte for byte. This is an integrity check; the semantic
attribution judgments come from the written reviews and the ledger.

For a typeset margin-sign edition, pass the generated `reader.pandoc.md`
through Pandoc with `scripts/attribution_margins.lua`. The filter places the
short signs in the margin; the full notes remain in the appended ledger.
Typesetting and visual checking are separate from annotation integrity.

The annotated reader is a presentation copy, not a second independent proof.
Its added explanatory bytes are reported separately. No length ratio is
claimed for this annotated edition. An annotation that adds a necessary
argument would have to enter the mathematical denominator; none here adds
a proof step or a mathematical premise.
