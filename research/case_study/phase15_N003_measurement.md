# A second matched-proof measurement: eight results from 2002

10 October 2026. The [compact forest-and-parity proof](phase15_N003_matched_proof.md)
recovers all eight numbered results of Cameron--Cara, *Independent
generating sets and geometries for symmetric groups* (2002), in the
explicit finite-group and n>=7 scope. Its matched written-proof ratio is
**4/3, approximately 1.33**, conditional on the declared common background.
This is a 25 percent reduction in the chosen character measure. It is
not a ratio for the entire paper, its open questions, or the whole corpus.

| Metric | Source proofs | Replacement proof | Source / replacement |
|---|---:|---:|---:|
| Normalized non-whitespace characters | 9,680 | 7,260 | 4/3 = 1.333333 |
| Unicode alphanumeric tokens | 2,439 | 1,675 | 1.456119 |
| Raw selected-span UTF-8 bytes | 12,462 | 8,693 | 1.433567 |

The token count is extraction-sensitive: the PDF text joins some words.
The raw bytes include physical source layout. Mathematical glyphs in the
source and ASCII/Unicode notation in the replacement are not a canonical
common proof language. The primary normalization removes whitespace,
applies NFKC and removes soft hyphens and only the explicitly located
physical page markers and footers. It does not remove mathematical prose,
equations or difficult steps.

## Exact target and retained inputs

The targets are Theorems 1.1, 2.1, 3.1 and 3.2, and Corollaries 2.2,
2.3, 2.4 and 3.3. Both generator families and all three counts are
included. The geometry result includes the forward classification,
converse existence, uniqueness convention and the arbitrary-parabolic
argument needed to show that every maximum-rank source geometry is RWPRI.
The unnumbered small-degree exceptions, direct-product question and
CFSG-free question are excluded. This is more than the tree-only
component target considered in the earlier measurement-scope audit.

Both sides retain Whiston's independent-family bound W1 and his separate
omission-subgroup trichotomy W2, Cayley's formula, elementary finite
permutation theory, and the source's general coset criteria. W2 retains
its CFSG dependence. The source's explicit recital of W2 is therefore
excluded from its numerator, just as the replacement's background
preamble is excluded. No source lemma is silently imported into the
replacement denominator at zero cost.

The replacement explicitly proves the binary permutation-module bound,
forest subgroup and intersection formulas, the sign-kernel adapter,
two-block overgroup calculation, laminar flag completion and panel
reconstruction. Neither the 1997 inductively minimal classification nor
a classification of all maximal subgroups of S_n is an additional input.
The compact proof has a separate [internal mathematical review](phase15_N003_matched_audit.md).
The measurement script checks lengths and hashes, not validity of the proof.

## Reproducible accounting

The [protocol](phase15_N003_measurement_protocol.json) fixes nine disjoint
source intervals and eight disjoint replacement intervals. Every raw span
has exact codepoint boundaries and a SHA-256 hash. Source Theorem 2.1's
proof is split around the retained W2 recital. Physical source layout
intervals are separately located and hash-bound, avoiding a rule that
might remove mathematical numbers merely because they occupy a line.
Target statements and common definitions are excluded on both sides;
intermediate claims and their explanations remain charged.

Each shared span is charged once. The [report](phase15_N003_measurement.json)
also records which additional proof blocks are first charged as targets
are added in its fixed order. Those are allocations of these particular
proof blocks, not minimal incremental proof costs. In particular the
forest/sign core already proves the intersection property when used
for the generator theorem. Zero further charge for its later corollary
is reuse of paid material, not an infinity marker or a new resolution.

The report shows how the ratio changes if the same illustrative background
cost is added to both sides. Those scenarios are not estimates of the
size of Whiston's proof or the classification of finite simple groups.
It also records unmeasured exposition and measurement-infrastructure
bytes separately. Neither written proof requires a finite enumeration,
so the existing diagnostic and formal artifacts are excluded from this
written-proof metric on both sides. Search time and checker time are
not equated with description length.

To reproduce, obtain the [primary author PDF](https://maths.qmul.ac.uk/~pjc/preprints/igsgsn.pdf)
and install the pinned `pypdf==6.13.0`. From the repository root:

```sh
python3 research/case_study/phase15_N003_measure.py \
  --source-pdf /path/to/igsgsn.pdf \
  --output /tmp/N003-measurement.json
```

The runner reads the PDF bytes once, verifies the exact source hash,
re-extracts all twelve pages, checks the full extraction hash, validates
all interval hashes and recomputes the metrics. It produces metadata and
counts only. The PDF and extracted proof text are not distributed.

## What this changes

There are now two separately scoped matched measurements: this eight-result
2002 bundle at 1.33, and the earlier two-formula counting bundle at 3.34.
The smaller ratio is reported directly; it is not replaced by the larger
one or extrapolated across the bibliography. The common forest/sign
method also supports other papers, but their complete matching source
spans must be measured before assigning a combined reuse ratio.

This work was already in the nine-work principal-result ledger. The
compact proof and measurement improve its evidence; they do not add
another paper to that count. These are established source results,
so no novelty or verified-new-resolution infinity marker is involved.
