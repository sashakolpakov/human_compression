# Independent source-span and measurement review for N003

10 October 2026. **PASS**, for the exact eight-target, common-background
comparison specified by [the protocol](phase15_N003_measurement_protocol.json).
Protocol SHA-256:
`7441c9c1d5130d4b1a9c78f48be8d1d639ef109bb5e0f55471f57faf16391ba0`.
The mathematical review is separate in
[phase15_N003_matched_audit.md](phase15_N003_matched_audit.md).

## Selection and dependency scope

I inspected all nine selected source intervals against the complete primary
manuscript extraction, all eight replacement intervals against their proof
markers, and the full proofs rather than only the interval endpoints. The
source intervals contain the complete proofs of the eight declared results,
with Theorem 2.1 split solely to omit the retained W2 recital. Source Theorem
3.1's stated strong-independence consequence is included. Target statements,
shared definitions, the small-degree remarks, references and unrelated open
questions are outside the selected proof intervals. No required proof step
has been dropped from the source selection.

The interval 5470:5689 contains the W2 trichotomy recital and its transition
sentence. Excluding it agrees with excluding the same retained input from
the replacement's measured preamble. W1, W2, Cayley's formula, source
(G1)–(G4), and elementary finite permutation facts, including natural
alternating-group primitivity, form the same unexpanded background on both
sides. W2's CFSG dependence remains substantial; the comparison does not
measure a CFSG reduction. The replacement pays for the module, forest,
parity, overgroup and arbitrary-parabolic arguments inside its selected
blocks rather than moving those proofs into the background.

Each selected interval is charged once. The marginal order allocates these
fixed blocks and is explicitly not a sequence of shortest incremental proofs.
In particular the full forest/intersection block has already been paid for
before Corollary 2.3 is added; its later zero replacement increment records
reuse. The larger explicit Corollary 3.3 bridge remains charged even though
the source treats that conclusion briefly.

The 23 bound layout exclusions are exclusively the extractor's page markers
and printed page numbers. The independent checker verified their exact text
shapes and hashes. Only their intersections with selected source spans are
removed; no mathematical text is classified as layout.

## Independent numerical recomputation

The [independent checker](phase15_N003_scope_check.py) does not import or
execute the author's runner. It reads the hash-bound extraction and protocol,
removes layout via an absolute-position set, normalizes with NFKC and removes
soft hyphens, and counts alphanumeric runs using a character-state loop. It
verified every span hash, all eight replacement marker boundaries, absence
of selected-span overlaps, every per-span metric, and all marginal allocations.
The [saved report](phase15_N003_scope_check.json) gives:

| Metric | Source | Replacement | Exact source/replacement ratio |
|---|---:|---:|---:|
| Normalized non-whitespace codepoints | 9,680 | 7,260 | 4/3 |
| Unicode alphanumeric runs | 2,439 | 1,675 | 2439/1675 |
| Raw UTF-8 bytes of selected spans | 12,462 | 8,693 | 12462/8693 |

All values match the author's report. This independent run uses the already
bound primary extraction; it did not separately regenerate that extraction
from PDF. The original PDF hash is checked, and the author's runner separately
requires the recorded pypdf version and verifies its regenerated extraction.

## Interpretation and sensitivities

These are descriptive sizes of two specified proof selections conditional
on the declared common background. They are not shortest-proof complexity,
a whole-paper or corpus compression ratio, a search/runtime comparison, or a
measure of mathematical significance. Adding the same expanded background
cost to both sides moves the ratio toward one; no background-length estimate
has been established.

NFKC treats ligatures consistently but does not create a canonical encoding
of mathematics. Source typesetting and replacement plain-text notation still
have different costs. Extracted joined words affect tokenization, so the
alphanumeric measure is not a linguistic word count. Raw bytes intentionally
retain physical layout and are a separate sensitivity measure. These limits
are already stated in the protocol and do not invalidate the exact, narrowly
scoped arithmetic comparison. No numerical correction is needed.
