# L032 + L035 + F013 + F016 → Compress_B: conditional full-body measurement

The four complete primary PDF bodies contain **32,476 NFC whitespace-delimited tokens** under the declared extraction convention. The complete rendered replacement contains **8,267**, giving **32,476 / 8,267 = 3.9283899843**. The replacement includes its substantive scope statement, every section, all source adapters and corrections, the entire Appendix A census algorithm, and the explanation after the code. Nothing mathematical was removed to obtain this number.

This is a **conditional manuscript factor for the reviewed eleven-main-result contract**, under the literal normalized PDF-extraction convention below. It does not say that every assertion of the four source papers has been replaced, or that their retained background has been reproved. The mathematical author and independent/root audits already accept the declared contract; this measurement package was prepared for the root's independent boundary review and fresh replay. This report does not preempt that measurement acceptance. Its bound inputs stay unchanged when a later independent review records acceptance.

## Exact scope and sources

| Input | Frozen primary version | PDF pages | Body-bearing physical pages | NFC tokens | NFC alphanumeric units | NFC nonwhitespace codepoints |
|---|---|---:|---|---:|---:|---:|
| L032, *On regular polytopes of 2-power order* | Author revised PDF, 8 November 2019; journal 2020, DOI 10.1007/s00454-019-00119-5 | 8 | 1–6 | 3,032 | 3,608 | 12,906 |
| L035, *Existence of regular 3-polytopes of order 2^n* | arXiv 1802.08947v2, 22 January 2019; journal catalogue title *2-groups behaving as automorphism groups of regular 3-polytopes* | 22 | 1–20 | 16,721 | 16,352 | 48,156 |
| F013, *String C-groups of 2-power order project onto a common string C-group* | arXiv 2605.20691v1, 20 May 2026; PDF date 21 May 2026 | 11 | 1–10 | 4,540 | 5,117 | 21,985 |
| F016, *Symmetric polytopes whose automorphism groups are 2-groups* | arXiv 2512.15511v1, 17 December 2025; PDF date 18 December 2025 | 19 | 1–17 | 8,183 | 9,261 | 39,335 |
| **Source sum** | Four exact versions; no cross-version substitution | **60** | **53 body-bearing pages** | **32,476** | **34,338** | **122,382** |
| **Compress_B** | `phase37_compress_twogroups_manuscript.md`, SHA-256 `261a9002e7f0394b2ad817b84dbf9a85e8464851c86f9d3ac247048a9fa53751` | **12 rendered** | **All 12** | **8,267** | **8,183** | **36,570** |

L035 physical page 22 is empty. Body-bearing pages can also contain reference or acknowledgment text removed by the exact rules. Page totals are descriptive, because source layout and replacement layout differ. No page-count compression factor is asserted.

The eleven numbered targets are L032 Theorem 1.2; L035 Theorems 1.2 and 1.3 (all three parts, all eight marked presentations, with n ≥ 10); F013 Theorems 1.1 and 1.2; and F016 Theorems 5.1(a–d), 5.3, 6.1(a–b), 7.1, 7.2 and 7.3. The merged ledger has seventeen clause rows. F016's standing input-rank condition d ≥ 3 and its finitely generated infinite-group convention are preserved; the latter permits elements of infinite order. F013's main results concern finite nondegenerate string C-groups of rank at least two.

The exact main-result ledger, author manifest, independent full manuscript audit and fresh census replay, and root mathematical audit are hash-bound in the measurement protocol. This measurement does not conduct another proof audit. It verifies that the complete manuscript accepted by those audits is the manuscript being counted.

The full source numerator includes auxiliary propositions, historical discussion, examples, the unnumbered small-order lists and F016's power-polytope discussion. Those are not additional recovered targets. In particular, F013 v1's false auxiliary Theorem 4.2(c), the specified identification/order assertion in (d), and (e) are corrected in replacement §10 rather than claimed as recovered truths. F016's diagonal-translation and chiral-facet proof repairs remain visible. N009 is excluded entirely.

## Fixed body and counting rules

Each source is freshly extracted from its hash-bound PDF by pypdf 6.13.0 using default `page.extract_text()` on every page. Page strings are joined with exactly one newline. The four fresh extractions produced no warnings and replay the bound whole-file and per-page hashes. The exact original PDF hashes, extraction hashes, page spans, body spans and every exclusion's coordinates/hash/reason are in `phase38_compress_B_measurement_protocol.json`.

A source body starts with its first **Abstract** heading and ends immediately before **References**. Within that interval, the only exclusions are exact keyword/subject-classification metadata, corresponding-author/email notes, date/arXiv/page furniture, running title/author headers, and the terminal acknowledgment/funding paragraph. Each exclusion is replaced with one space. Page numbers are removed by their bound page positions, never by a global numeric-text filter. There is no post-reference mathematical appendix in these sources. The F013 mathematical footnote defining nondegeneracy is retained. Diagram labels/captions and every mathematical expression remain as extracted.

The replacement body is Unicode codepoint interval **130:50790** in its frozen Markdown file. Only the title and bold private-version label precede that interval. The substantive paragraph beginning “This is a new standalone replacement…” remains, as do §§1–10, the Appendix A heading, all 41 code lines, and every explanatory sentence through EOF. There is no separate reference-list exclusion. Internal citations and statements of retained inputs count in full. The Markdown is rendered before comparison; raw Markdown counts are only secondary data in the JSON report.

The primary metric applies Unicode **NFC**, collapses each whitespace run to a single ordinary space and counts whitespace-delimited tokens. Formula identifiers, numerals, punctuation separated by whitespace and code tokens count under this rule. It is a literal PDF-extraction word convention, not a count of English prose words. No discretionary hyphen repair, formula reconstruction, OCR, operator substitution or missing-glyph inference is performed. Nonwhitespace control characters in source font encodings are recorded and retained. Source diagram shapes are not text; their available labels and captions count. This is a limitation of the declared text metric, not an undisclosed deletion.

The same helper also counts alphanumeric runs (`[^\W_]+`), nonwhitespace codepoints, codepoints after whitespace collapse, and UTF-8 bytes after whitespace collapse. **NFKC** is a separately reported sensitivity; it is never silently substituted for NFC. Ratios sum the separately cleaned source counts, then divide by the complete rendered replacement count. No source or metric is selected after observing which ratio is largest.

| Normalization | Unit | Four-source numerator | Complete rendered replacement | Conditional factor |
|---|---|---:|---:|---:|
| NFC | Whitespace tokens, primary | 32,476 | 8,267 | **3.928390** |
| NFKC | Whitespace tokens | 32,513 | 8,267 | 3.932866 |
| NFC | Alphanumeric units | 34,338 | 8,183 | 4.196261 |
| NFKC | Alphanumeric units | 34,338 | 8,183 | 4.196261 |
| NFC | Nonwhitespace codepoints | 122,382 | 36,570 | 3.346514 |
| NFKC | Nonwhitespace codepoints | 122,468 | 36,617 | 3.344567 |
| NFC | Collapsed-whitespace codepoints | 154,854 | 44,836 | 3.453787 |
| NFKC | Collapsed-whitespace codepoints | 154,977 | 44,883 | 3.452911 |
| NFC | Collapsed-whitespace UTF-8 bytes | 164,949 | 51,630 | 3.194829 |
| NFKC | Collapsed-whitespace UTF-8 bytes | 164,920 | 45,934 | 3.590369 |

These are different declared length units. In particular, the primary factor is not a claim that every reasonable mathematical encoding has factor 3.93. Unicode mathematical fonts and ligatures explain much of the byte sensitivity; formula layout and word joining affect token counts. All four originals are nevertheless complete primary PDFs, and the denominator is a complete readable PDF render, so these limitations do not prevent stating the conditional factor under its explicit convention.

## Retained proof inputs and executable costs

| Retained input | Use in the replacement | Cost treatment |
|---|---|---|
| Regular-polytope/string-C-group correspondence, marked quotient/cover correspondence and coset-face construction | Geometric interpretation of the common algebra | Retained standard background; citations and interface explanation count, proof bodies are not rederived |
| Burnside basis theorem, finite two-group nilpotency, lower-central graded Lie facts | Generation and canonical quotient | Retained standard background |
| Gaussian-integer Euclidean algorithm and elementary square-tiling geometry | Square-torus classification | Retained standard background |
| Lucchini's proper cyclic-subgroup core bound | Bounded cyclic descent for L035 classification | Substantial imported theorem; no new proof credit |
| Complete SmallGroups order-256 catalogue, version 1.5.4 | Exhaustive finite seed | Catalogue completeness retained; tested relation implications derived by included Appendix A and bound executable |
| Monson–Schulte 2020 Theorem 5.3 | Alternating semiregular assembly and its full automorphism criterion | Substantial imported geometric theorem; no new proof credit |
| Standard regular free extension; Schulte–Weiss 1995 chiral free extension; Monson–Schulte 2012/2021 universal alternating extension | Geometric existence, universality and amalgam interfaces | Substantial imported geometric theorems; the common torsion/infinitude argument is proved in the replacement |
| Amalgam normal-form theorem | Infinite-order words and finite-order conjugacy | Retained standard theorem |

No main target theorem from these four inputs is itself imported as background. The factor is relative to this stated background, not a compression of those external works.

| Artifact or work | Size / observed effort | Included in 8,267-token denominator? |
|---|---:|---|
| Full Appendix A, code and proof explanation | One 41-line GAP code block; exact AST code UTF-8 SHA-256 `d7f259f13c76e19ef3d971645faa2dd33c8d139efcc4c7ec484627a8a209ee33` | **Yes, once**, including surrounding prose |
| Required executable counterpart `phase37_compress_twogroups_census.g` | 2,455 bytes; hash `0a1e993362b263c9ef23e8fca5103c3a2b766a937a2f9af7608fbca8252d2752` | Separately reported; no duplicate manuscript charge |
| Author census output `phase37_compress_twogroups_census.log` | 396 bytes | Separate external output |
| Independent census replay output `phase37_compress_twogroups_recent_check.log` | 396 bytes | Separate external output |
| Prior independent census execution | GAP 4.15.1, SmallGroups 1.5.4; 51.03454 seconds wall time, 48,909 ms reported census CPU time | Separate execution cost; not rerun by the length tool |
| Optional diagnostic models JSON | 2,526 bytes | No proof dependency, separate diagnostic artifact |
| Optional prior `phase3_extension_check.py` | 5,130 bytes | No proof dependency, separate diagnostic artifact |

The independent census examined 1,651 eligible groups, 1,641 active groups and 92 anchored valid triples, with relation-pattern totals [64, 4, 16, 8]. Catalogue completeness and correctness of the exact GAP arithmetic remain retained inputs. The executable-derived implications are not an unexplained extra theorem, because the complete algorithm and exhaustiveness argument are already in the counted manuscript. No computation above group order 256 supports the all-parameter completeness proof.

## Render integrity and reading limits

The fixed renderer uses Pandoc 3.10 with `markdown+tex_math_single_backslash`, XeLaTeX from TeX Live 2026/Homebrew, letter paper, 10-point text, one-inch margins and no page furniture. A bound `newunicodechar` header renders all fourteen proof-end marks as mathematical black squares; `fvextra` permits safe code wrapping. The three tables use Pandoc's nonfloating `longtable` output. No mathematical text or table is manually shortened, deleted or rewritten by the renderer.

The AST contains **669 inline mathematics nodes, 26 display mathematics nodes, 14 proof marks, 3 tables and one complete 41-line code block**. It has no image or figure node. The runner verifies that the code in the AST equals the frozen Markdown code block, and that the PDF extraction retains its exact nonwhitespace token sequence. All fourteen extracted proof marks survive. The entire source/AST/rendered body, code and normalized extraction are hash-bound.

The first direct XeLaTeX pass reports only expected cross-reference/page-label and table-width rerun notices. The second pass has **no LaTeX warning, overfull/underfull box or missing-glyph diagnostic**. Fresh source and replacement PDF extractions have no warnings. Ghostscript 10.07.0 rasterizes the final PDF without errors. The runnable report records program versions/binary hashes, TeX input hashes, embedded font names, exact commands, both direct-pass logs, extraction hashes and counts. PDF metadata can change bytes without changing content; byte-identical PDFs are not promised.

The measurement author read the complete fresh extracted authored bodies of all four sources, including ancillary material, for boundary/exclusion decisions; this was not a new proof verification. References and final pages were checked to rule out an omitted mathematical appendix. This author also viewed every one of the twelve rendered replacement pages at 130 dpi. Formulas, table rows, proof marks, Appendix A's page break and every code line were visible without clipping or missing glyphs. This is a complete page-level visual inspection, not a claim of machine-verified glyph-by-glyph mathematical equivalence. The final runner's twelve PNGs have exactly the same hashes as the twelve visually inspected exploratory pages. The separate visual record binds those observations to the files.

The root independently examined all source body boundaries/exclusions and replacement inclusion, viewed rendered pages 7 and 12, and inspected the clean final log before replay. That is a limited independent sample visual check; the all-page visual observation remains attributed to the measurement author. Mathematical proof acceptance comes from the bound prior full independent manuscript audit and root review, not from page images or token counts.

## Reproduction and files

Run from the private input directory, using a new output directory:

```sh
/Users/sasha/.venvs/global/bin/python phase38_compress_B_measurement.py \
  --input-root /Users/sasha/medusa/research/leemans \
  --output-dir /private/tmp/compress-B-measurement-NEW \
  --rasterize
```

`--rasterize` is optional for numerical replay, and creates every page image for human inspection. The runner refuses an existing output directory. It verifies the exact four primary PDFs, every fresh extraction/page hash, source body/exclusion spans, full replacement hash, all ledger/audit/certificate bindings, complete AST/code, final render diagnostics and expected metrics. It never writes source text or copies source PDFs into the output directory. Its report and authored replacement render remain private. `--allow-toolchain-drift` explicitly labels a sensitivity run; the bound release is required for the exact replay.

The completed author run is `/private/tmp/mc_phase38_B_final2`. The stable structured report is `phase38_compress_B_measurement_report.json`; the body contract is `phase38_compress_B_measurement_protocol.json`; the executable is `phase38_compress_B_measurement.py`; observation bindings are in `phase38_compress_B_measurement_visual.json`; and final file hashes are in `phase38_compress_B_measurement_manifest.json`. The initial span-authoring helper is provenance, not the reproduction entry point. All prior source, manuscript, ledger and review files remain unchanged. Nothing in this package has been publicly exported.
