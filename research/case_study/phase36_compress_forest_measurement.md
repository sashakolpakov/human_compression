# Compress_A: provisional full-body measurement

10 October 2026. Independent measurement preparation for the two-source assembly. This note does not certify its mathematics or assign a final compression ratio. It measures the exact draft and primary-text representations bound in the companion protocol. No source text has been exported.

The result is sensitive to the representation: the source sum is **1.36264 times** the replacement by whitespace tokens, **1.16830 times** by alphanumeric units, and **0.94172 times** by nonwhitespace characters. Those are descriptive ratios, not interchangeable estimates of semantic or mathematical compression. Under the character convention, the replacement is longer.

## Exact intake and boundaries

The author intake declares twelve targets: N001's four-part Theorem 1, and N003's eight numbered results with the attached strong-independence consequence. Its general group statements are specialized to finite groups; the symmetric-group classifications retain degree at least seven. The shared proof and every adapter are inside the measured replacement. The source and dependency ledger is declared a provenance companion, not an omitted mathematical appendix. Any necessary new argument placed there after review must be charged to the replacement.

The source versions differ. N001 is the complete indexed authored text preserved in a browser record; its original PDF has not been obtained, and its diagram/formula glyphs are damaged. N003 is a complete twelve-page author PDF, whose existing extraction was reproduced byte for byte during this measurement using pypdf 6.13.0. It is not silently identified with journal typesetting. The draft's journal-page endpoint typo is bibliographic and lies outside the measured replacement body.

All intervals below are UTF-8-decoded Python string/codepoint intervals, with the end excluded. They are not byte offsets. Full file and selected-span hashes are in the protocol.

| Document | Selected body interval | Boundary | Internal noncontent exclusions |
|---|---:|---|---:|
| N001 browser record | 10614:26903 | Abstract to immediately before References | 39 intervals, 778 codepoints |
| N003 PDF extraction | 300:20930 | Abstract to immediately before References | 21 intervals, 287 codepoints |
| Compress_A Markdown | 151:35948 | Abstract and scope to immediately before References and source versions | None |

The common policy excludes titles, bylines and affiliations before the abstract; references; funding/editorial metadata; and page or browser furniture. No acknowledgments section was found in these bodies. The removed N001 metadata also contains the journal's keywords and subject classification. These are not proofs or hypotheses. Every running header is identified individually; line labels wholly inside a removed metadata span are not removed twice.

Everything else is retained: abstracts, introductions, definitions, background recitals, displayed formula text, examples, theorem statements, proofs, applications, questions, and the replacement's dependency/coverage discussion. No mathematical paragraph was removed to improve a ratio. In particular, this whole-body numerator includes source material outside the replacement's declared result contract. This is intentionally different from the earlier selected-proof measurement.

## Counts

The main convention applies NFC normalization and collapses whitespace. It does not expand ligatures, repair hyphenation, join broken formulas, translate TeX commands, correct OCR, remove diagram artifacts, or delete nonwhitespace control characters.

| Document | Whitespace tokens | Alphanumeric units | Nonwhitespace characters | Characters with collapsed whitespace |
|---|---:|---:|---:|---:|
| N001 | 3,281 | 3,064 | 12,225 | 15,505 |
| N003 | 3,941 | 4,093 | 16,392 | 20,332 |
| Source sum | **7,222** | **7,157** | **28,617** | **35,837** |
| Compress_A | **5,300** | **6,126** | **30,388** | **35,687** |
| Source sum / replacement | **1.362642** | **1.168299** | **0.941720** | **1.004203** |

“Whitespace tokens” means `len(text.split())`; it includes isolated formula operators and symbols. “Alphanumeric units” means Unicode regex `[^\W_]+`; it includes variables, numbers and TeX command names. Neither is a clean linguistic word count. Character counts are Unicode codepoints, not glyphs or mathematical symbols. UTF-8 byte counts, also saved, are an encoding diagnostic.

Two transparent sensitivities are saved. NFKC expands the 24 compatibility ligatures in N003: its nonwhitespace character ratio becomes 0.942510. Removing only obvious Markdown headings, bold delimiters and backticks from the replacement gives 1.364701 whitespace-token ratio and 0.946329 nonwhitespace-character ratio. Equations and their TeX syntax remain. Neither sensitivity removes the format mismatch or establishes a preferred final ratio.

## Representation effects that matter

The replacement contains 289 literal TeX command occurrences. Its sequences such as a command name, braces and subscripts occupy multiple characters while the source extraction can represent the same mathematical content with one glyph or lose part of its layout. Conversely, N001's spaced formula fragments inflate whitespace-token counts. N003 glues some words to mathematical identifiers and breaks other words at line ends. Eleven ASCII letter-hyphen-space-letter occurrences remain across the two source bodies. They were not automatically joined because the preserved transcription does not always distinguish a layout break from intended notation.

N001 also retains control characters U+0004 and U+0008 in proof/diagram extraction. The protocol does not silently interpret or erase those mathematical artifacts. Its original PDF is unavailable, so no lossless correction or exact visual-word count is claimed. The bound record is reproducible; the completeness and accuracy of every glyph are a separate issue.

These effects explain why whitespace and character metrics give different directions. A reliable comparison of rendered words would require a specified common rendering/transcription convention and inspection of the mathematical layout on both sides. Rendering the replacement through the same PDF extractor would improve comparability to N003, but would not recover N001's missing original layout. Deleting TeX commands alone is not a sound solution: some commands express mathematical content.

## Principal results versus literal whole-document coverage

The user's proposed test concerns all **main results**. Minor commentary, references and open questions need not become replacement theorems merely because the source body is measured in full. The separate `recent_conjectures` and root reviews now pass the twelve declared targets with their retained inputs and finite-group scope. The recent review identifies the degree-at-least-seven classifications as N003's main abstract targets and its excluded small-degree census as auxiliary. This measurement review records that assessment; it is not an additional complete mathematical audit of the manuscript.

There are nevertheless substantive limits to preserve. N003's general statements have been narrowed to finite groups, and its unnumbered small-degree classifications and direct-product consequence are outside the declared target set. The protocol records three mixed source blocks containing those statements, diagram commentary and open questions. Together they contain 351 raw whitespace tokens, but this is **not** a clean count of uncovered mathematics: some sentences are covered, others are questions, and the blocks contain incidental layout. They remain included in the descriptive numerator and must not be silently deleted or all labelled “missing main results.”

The N001 intake uses the earlier inductively minimal classification as retained background, and N003 retains Whiston's two distinct inputs, including their classification dependence. The replacement explicitly states those inputs and their uses. Their recitals are counted on both sides; their underlying proofs are not supplied in either counted manuscript. A later claim must therefore state that the recovery is conditional on this background, rather than claim that the assembly eliminates it.

A literal claim to reproduce every source assertion is presently ineligible. The principal-result reviews support the stated finite-group/degree-at-least-seven contract; the finite specialization still qualifies two general numbered results. A common mathematical rendering/counting convention has not been approved. The report therefore keeps `final_principal_result_compression_ratio` null. The descriptive body ratios remain **text-representation length comparisons**, with each counting convention attached, rather than a representation-independent reduction factor.

## Executable protocol and checks

The standard-library runner reads the protocol's source/body hashes, verifies every exclusion interval, rejects overlaps and out-of-body exclusions, and writes hashes/counts only. It sums both source bodies without deduplicating common background, and counts the integrated replacement body once. Earlier selected-proof ratios are not imported.

Run from this private directory:

```sh
python3 phase36_compress_forest_measurement.py --output /private/tmp/compress_A_measurement.json
```

To reproduce the additional source-PDF integrity/extraction check used here:

```sh
python3 phase36_compress_forest_measurement.py \
  --source-pdf sources/network_independent_generators.pdf \
  --verify-pdf-extraction \
  --output /private/tmp/compress_A_measurement_with_pdf.json
```

That optional replay uses pypdf 6.13.0 and reproduced all twelve pages' bound text exactly. The ordinary count run needs no PDF library. `--n001-text`, `--n003-text`, `--replacement`, and `--input-root` support relocated inputs while retaining exact hash verification. A changed manuscript fails rather than being counted under stale offsets. The runner also refuses an existing output path, including its default saved-report path; use a fresh output for every replay.

The generated counts and body hashes were also checked with a separate temporary deletion-by-codepoint-mask calculation, without importing the runner. That second calculation matched all five main metrics and collapsed-body hashes for all three documents. It is a same-reviewer implementation check, not another person's independent mathematical review.

The protocol, runner, report and this note can be shared without source full texts. Exact replay requires the bound private source transcriptions or independently obtained lawful copies matching their hashes. The public availability of a primary URL does not guarantee that a future indexed rendering will have the same bytes. The files are a provisional measurement snapshot; later manuscript revisions require new bindings and counts.
