# First finite matched-proof measurement

10 October 2026. Private measurement with completed internal review. This is a result for
**two precisely restricted theorem statements in one paper**, not a
corpus ratio or a measurement of the whole paper.

For the nonexceptional portions of Kiefer–Leemans Theorems 1.1 and 1.2,
the selected original proof spans contain **10,668 normalized characters**.
The replacement shared core and both adapters contain **3,192**. The
conditional proof-description ratio is therefore

    R(S | B) = 10,668 / 3,192 = 3.34211.

Here a character means a non-whitespace Unicode codepoint after NFKC
normalization and removal of PDF running headers and page markers.
The supplementary alphanumeric-token ratio is 2,534 / 835 = 3.03473.
Because PDF extraction glues some words, the latter is not presented as
a clean linguistic word count. Neither metric measures mathematical
difficulty, novelty, shortest possible proof length, or historical value.

## Exact matched targets and background

S consists of the exact floor-sum counting formulas in Theorems 1.1
and 1.2 of *On pairs of commuting involutions in Sym(n) and Alt(n)*,
for permutation degrees N≥4, N≠6. The equivalence relation is the
source's group-automorphism equivalence on unordered pairs of distinct
involutions. Degree six, its exceptional automorphisms, and Theorems
3.6 and 4.4 on regular polyhedra are excluded.

The [replacement proof](phase9_L066_matched_proof.md) gives an explicit
bijection between orbit multiplicities and the source's cycle-count
parameters. It derives the published floor sums directly. Agreement
of two numerical sequences over finitely many degrees is not used as
a substitute for this all-degree equivalence.

The common retained background B consists of elementary finite group
and permutation facts, orbit-stabilizer and coset actions, cycle-type
conjugacy, permutation parity, the usual symmetric-group centralizer of
an involution, and the standard automorphism theorems for S_N and A_N
outside degree six. The source also retains these general facts. The
replacement proves the finite V-set classification and all application
counting steps within the measured spans. No source counting lemma or
classification database is made free background.

The general automorphism and centralizer theorems are not expanded on
either side. This is consequently a **conditional** ratio relative to
B, not an unconditional comparison of complete foundations.

## Source ranges and shared accounting

The source is the author's nine-page primary PDF:
[Kiefer–Leemans manuscript](https://math.uni.lu/kiefer/Publications/Involutions.pdf).
Its PDF hash, extraction hash, exact half-open character ranges, and
individual span hashes are recorded in the
[protocol](phase9_L066_measurement_protocol.json). I read the complete
selected proof text and checked the two target formulas against the
page images. No original proof text or page images are bundled.

| Selected proof component | Source characters | Replacement characters |
|---|---:|---:|
| Shared counting arguments: pp3–5, Lemmas 3.2–3.3; pp5–6, equal-cycle calculation | 7,470 | 2,001 |
| Symmetric-group final adapter, p6 | 285 | 332 |
| Alternating-group adapter, pp7–8 | 2,913 | 859 |
| Total, shared spans counted once | 10,668 | 3,192 |

The source's Proposition 4.1 statement and proof contribute another
599 characters. Its centralizer order is not needed for these targets,
and Lemma 4.2 already repeats the necessary even-part characterization.
The conservative primary numerator excludes this whole optional span.
Including it as part of the original explanatory presentation gives
11,267 / 3,192≈3.52976, reported as a separate sensitivity result.

The replacement's symmetric adapter is **longer** than the corresponding
source adapter: its ratio is 285/332≈0.858. Most savings occur in the
shared counting argument. This local reversal is retained in the report.

The selected source ranges exclude the abstract, introduction, target
statements and table on pp1–2, references, Remark 3.4 about polytopes,
the degree-six section, and both polyhedron proofs. Internal lemma
statements and displayed calculations inside the selected arguments are
counted. The replacement uses the same rule: all three marked proof
spans count, while the surrounding target/background declarations and
measurement exposition do not. Displayed equations inside the proofs
are included, not treated as free labels.

Adding the symmetric formula first costs 7,755 source characters versus
2,333 replacement characters: ratio 3.32405. Adding the alternating
formula then costs only the previously uncharged spans, 2,913 versus
859: marginal ratio 3.39115. The shared core is not charged again.
These marginal figures depend on the declared ordering; the total does
not.

## Sensitivity and separate costs

Using raw UTF-8 bytes of those proof spans gives 13,722 / 4,080≈3.36324.
This is a supplementary formatting-sensitive metric, not a bundle of
proofs, code, libraries and certificates. The agreement in direction
between character, token and byte metrics does not remove their limits.
In particular, the source is extracted from typeset mathematical glyphs,
whereas the replacement uses plain Unicode/ASCII equations and English
summation descriptions. The measured replacement spans contain no LaTeX
commands to be mistaken for rendered mathematics, but these two formats
are still not a canonical common mathematical encoding. Missing spaces,
line-wrap hyphens and formula layout also affect the metrics differently.
This is a comparison of the specified descriptions, not a claim that
their typography or level of exposition has been made identical.

If an identical expanded background of length b is charged to each side,
the character ratio becomes (10,668+b)/(3,192+b). For illustrative added
costs b=1,000, 10,000, and 100,000, it is 2.7834, 1.5667, and 1.0724.
Those are sensitivity scenarios, **not measurements or estimates of B**.
No claim about the true expanded-background ratio is made.

The replacement file has 5,651 UTF-8 bytes, of which 4,080 belong to the
measured proof spans and 1,571 to surrounding exposition and declarations.
No executable mathematical search or numerical certificate is required
by either of these target proofs. Existing GAP and formula-comparison
files are outside this measurement. The measurement script and protocol
are separately recorded as measurement infrastructure, including the
pypdf extraction dependency; they are not smuggled into, or omitted
from, a purported executable-proof bundle. Runtime and search cost are
not compared here.

## Reproduction and review scope

With Python 3 and `pypdf==6.13.0`, obtain the primary PDF independently
and run:

```sh
python3 phase9_L066_measure.py --source-pdf /path/to/Involutions.pdf
```

The [script](phase9_L066_measure.py) verifies the PDF, extracted text,
replacement, and every span hash; rejects overlapping ranges; and
regenerates the [machine-readable report](phase9_L066_measurement.json).
It outputs counts and hashes, never the copyrighted source text. A
different PDF version or extraction result is rejected rather than
silently measured against stale offsets.

This specimen establishes an actual, reproducible reduction in the
description length of this matched proof set under the declared B.
It makes no claim that two entire papers, every result of L066, or the
larger literature corpus have been compressed by this factor. The root
and recent_conjectures agents independently checked the all-parameter
replacement proof. The survey_audit agent additionally read the exact
source spans and adjacent exclusions, checked the target-formula page
images, and independently reran the measurement with the same result.
These are internal reviews, not external peer review; methodological
criticism remains separate from arithmetic reproducibility.
