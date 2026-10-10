> **Historical reader — archived from `5401cc9`.** This records the earlier
> compilation programme and its dated scope. Its rates, counts and “current”
> wording do not describe the active topic architecture. Use the
> [current programme](../MANUSCRIPT_PROGRAM.md) or the [archive index](README.md).

# Six manuscripts into U and Module A: measured cost

The reviewed comparison gives **1.634× by PDF-extracted whitespace tokens**,
**1.063× by nonwhitespace characters**, and **1.126× by collapsed-whitespace
UTF-8 bytes**. The character saving is much smaller than the token saving;
there is no representation-independent factor or matched page ratio.

The intake is the six exact editions listed in [Module A](../MODULE_A.md):
L032, L035, F013, F016, N009 and L034. Their declared corrected principal
results follow from **Marked groups, kernels and intersections** (U3),
**Construction and classification of two-group polytopes and hypertopes**
(A2), four complete computational proof artifacts and explicitly retained
mathematical/software inputs.

    Six source manuscripts -> U3 + A2 + four complete programs

This arrow describes the compression. The mathematical implication runs
from the replacement and its stated inputs to the source-result contracts.
The [contract and proof review](../provenance/phase99_review.md) establishes
that implication at its stated scope; measuring files alone does not.

| Exact intake | NFC body tokens |
|---|---:|
| L032: *On regular polytopes of 2-power order* | 3,032 |
| L035: *Existence of regular 3-polytopes of order 2^n* | 16,721 |
| F013: *String C-groups of 2-power order project onto a common string C-group* | 4,540 |
| F016: *Symmetric polytopes whose automorphism groups are 2-groups* | 8,183 |
| N009: *String C-groups of order 1024* | 7,897 |
| L034: *Existence of regular 3-hypertopes with 2^n chambers* | 5,692 |
| **Total** | **46,065** |

The **[complete counted replacement](../research/case_study/phase144_render/replacement.pdf)**
has 65 pages, including the full executable appendix. All of U is charged
once, including parts unused by A; all of A, both manuscripts' references,
and all four programs/data files are included. U and A alone have separate
16- and 24-page mathematical renderings. Their sum omits necessary code and
is therefore not the complete denominator.

| NFC metric | Six source bodies | Complete replacement | Factor |
|---|---:|---:|---:|
| Whitespace tokens | 46,065 | 28,192 | **1.633974** |
| Alphanumeric runs | 48,846 | 33,358 | 1.464296 |
| Nonwhitespace characters | 175,580 | 165,244 | **1.062550** |
| Characters with collapsed whitespace | 221,639 | 193,435 | 1.145806 |
| UTF-8 bytes with collapsed whitespace | 236,705 | 210,230 | **1.125934** |

The numerator counts whole cleaned source bodies, including background,
discussion and printed open questions; it excludes bibliographies and
publication furniture. The replacement derives the specified principal
contracts, with source corrections explicit. Counting an open-question
paragraph does not credit A with answering it. This convention measures
whole manuscripts against a replacement of their declared results, rather
than minimum theorem-proof fragments.

Both sides use the same PDF extraction and Unicode rules. Formula layout,
font encodings, ligatures and word splitting still affect the results.
The full [independent review](../research/case_study/phase153_review.md) includes
all NFC/NFKC sensitivities, source boundaries, complete visual inspection,
retained-input costs and the required
[metadata erratum](../research/case_study/phase153_metadata_erratum.md).
The [root admission](../research/case_study/phase152_measurement_root_admission.md)
records a further primary recount and fresh public execution.

This is conditional on the named earlier theorems and trusted GAP/NQ
algorithms. Their transitive implementations are not expanded. The four
application programs themselves are fully charged. Optional Lean validation
and documentary infrastructure are inventoried separately. No new
conjecture solution, source coverage or long-run sawtooth trend is inferred.

With pypdf 6.13.0 installed, a fresh public recount is:

```sh
python3 -B -O research/case_study/phase153_independent_recount.py --output /tmp/NEW-UA-measurement.json
```

It freshly counts the complete own PDF and verifies its manuscript/code
coverage, then uses the bound source measurements. Add `--primary` only
when the six exact primary PDFs are available at the documented paths.
The public repository does not redistribute them.
