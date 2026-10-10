# Independent audit of the complete two-source C length experiment

Date: 2026-10-10. Reviewer: `review_unified_seven`, independent of the author of Compress_C, its lattice bridge, and the phase51 measurement. This is a measurement audit; the complete mathematical contract was independently reviewed earlier in `phase44_operations_recent_audit.md`.

**Admit the measured result, including its negative compression outcome:** under the declared NFC PDF-text convention, the source bodies have **8,382 whitespace tokens**, while the complete replacement has **8,582**. Thus

\[
\frac{|L088|+|N013|}{|\operatorname{Compress_C}+\text{required lattice bridge}|}
=\frac{2512+5870}{8582}
=\frac{4191}{4291}
=0.9766954089955722.
\]

The replacement is **200 tokens, or 2.3860653781913626%, longer** than the source sum. This assembly has a reviewed common proof framework and recovers its declared principal results, but this experiment does **not** demonstrate a length reduction. The distinction is substantive and must remain visible wherever this result is reported.

## Exact intake and replacement

| Intake | Bound version | Included NFC tokens |
|---|---|---:|
| Michael I. Hartley and Dimitri Leemans, *On the thin regular geometries of rank four for the Janko group J1* (2005), L088 | Complete 10-page primary PDF, `sources/catalogue_L088.pdf`, SHA-256 `b3264a0b4d857c8f638656c6ff9c5073134930a4bf965e1836808c85ccc396d6` | 2,512 |
| Antonio Montero and Asia Ivić Weiss, *Locally Spherical Hypertopes from Generalised Cubes* (2020), N013 | 11-page arXiv:2001.11082v1 primary PDF, `sources/phase26_montero_weiss2020.pdf`, SHA-256 `c6f36f7e977696bfada3931b680e74b371de75613c4dfcb1f30c23373991f416` | 5,870 |
| Complete replacement | `phase40_compress_operations_manuscript.md` plus **all** of `phase45_ten_source_toroid_bridge.md`, rendered together | **8,582** |

The mathematical mapping is

**{L088 principal rank-four construction/classification conclusions, N013 principal halving/generalized-cube conclusions} → Compress_C + the full required lattice bridge**, relative to the explicitly retained background.

It covers the 18 principal clause rows in the earlier independent audit, not every statement in the two source documents. The numerator nevertheless includes their complete mathematical bodies under the declared exclusions, including auxiliary discussion, historical text and questions outside that principal contract. It is therefore a conditional principal-result manuscript-length comparison, not an assertion that the replacement implies every sentence in its numerator.

C's SHA-256 is `3e605d2f9ec89324d031bd22e16a7a2d89ae324fa7bd801c2f8e3d8169b49560`; the required bridge's is `6d904c74fc41c8920d325e4e5b625c59be6f3daab0f7a1bbfcdd47009b9b5a09`. The author measurement manifest is `cdaaa194a0842dbf293cb003060e36ff75b4b1c575a8c3317abd625aa5c9e05d`; the protocol is `3109bd2b4e3d6857957b48a0d52ef43f3964a4c2c52d10814bcbfadac1437ad6`. This audit applies only to those frozen objects and the exact render convention below.

## Independent work performed

I read the complete measurement runner, protocol builder, protocol, report and exclusions; reviewed the relevant previously approved metric/render helpers; ran the frozen author runner into the new directory `/private/tmp/phase60-C-independent-replay`; and separately implemented a fresh counter that imports none of those helper or runner modules. The independent counter re-extracts all three PDFs with pypdf 6.13.0, uses independently checked explicit body/exclusion intervals, implements normalization/counting itself, and verifies every metric and normalized-text hash against both the author report and the fresh replay.

All 16 replacement pages were freshly rendered and rasterized at 130 dpi. I opened and inspected every page. I also independently rasterized both primary PDFs at 100 dpi and opened all 10 L088 and all 11 N013 pages. All 37 raster hashes match the author's frozen visual baselines. Matching images supplemented direct inspection; it did not substitute for it. The accompanying independent visual record binds every viewed image and records the boundary/content findings.

The independent recount separately verifies the full denominator assembly, exact code bytes, the unchanged Math/CodeBlock/Table nodes of the two Pandoc trees, every code block's complete ordered appearance in extracted PDF text, and the literal notation probes. All frozen inputs were hash-checked before and after. Deliberate retries against existing output paths were refused; all 46 fresh replay files and the independent count report remained unchanged.

No GAP census or Lean compilation was rerun for this measurement task. Their earlier mathematical/computational reviews are separate evidence; this runner establishes a reproducible representation-length calculation, not a mathematical theorem.

## Source boundaries and extraction qualifications

**L088:** the body starts at `Abstract` (codepoint 176) and runs to EOF (16161), with explicit exclusions for keyword/MSC metadata, page-navigation furniture, acknowledgments, bibliography and affiliations. Its mathematical *Final comments* remain included. Crucially, the two mathematical diagram pages **9 and 10 occur after the bibliography and are included**; page 8 is bibliography/affiliations only. Navigation alone is removed from the final two pages. Every excluded interval is text- and hash-bound, and each is replaced by one ASCII space to avoid fusing adjacent tokens.

The legacy L088 extraction contains non-whitespace control characters and imperfect glyph mappings. These are retained literally: no OCR, glyph repair or hyphen joining was applied. Drawn diagram edges do not become extracted text tokens, although their extractable labels and captions are included. This is an exact count of the selected, normalized extraction, not a claim that the count measures all visual mathematical information in those diagrams.

**N013:** the body starts at `Abstract` (codepoint 131) and ends immediately before `References` on page 10 (28654). The arXiv stamp, title and byline precede that start. The page-1 MSC/keywords/funding footer and repeated running headers/page numbers are excluded. The final mathematical paragraph on page 10, including its all-rank conclusions, is included. Page 11 contains bibliography/affiliations only. Source diagrams within the body remain within the retained extraction; the same limitation on drawn information applies.

Both fresh source text extractions match their frozen full/page hashes and have no pypdf extraction warnings. The N013 Ghostscript rasterization reported two Fontconfig “No writable cache directories” diagnostics and returned success. All its pages were inspected and all its image hashes agree with the frozen baseline; the diagnostics are preserved in the audit evidence rather than suppressed.

## Complete denominator and render changes

C is included from its first substantive paragraph, codepoint 140, through EOF. Only its title and private-version label precede that boundary. There are **no internal exclusions**. In particular, its entire retained-input/reference section is charged because it includes proof-dependency and scope prose. Both complete GAP programs are included once: 4,458 and 4,783 executable bytes, respectively, matching their full manuscript appendices byte for byte.

The bridge is included from BOF through EOF, including its title, date, historical review-status paragraph, full Gray-code/face-poset argument, explicit duality, marked affine group and lattice proof, chamber-halving argument, rank-three basis change, citations and source/proof accounting. C alone previously retained target toroidal identifications; the bridge is essential to the independently approved N8/N12 contract and cannot be silently externalized or subtracted from this denominator.

The assembled Markdown hash is `317ff8db43a9efb0b8178a186f70fe28254f21b7eb45c3720fe6c244f8762a68`. The rendered PDF contains 20 display-math nodes, 14 proof-end marks, two complete tables, and eight complete code blocks: the two GAP programs and six short lattice-coordinate blocks. Their code-block line counts are 106, 124, 1, 3, 2, 1, 1, 1.

The rendering preserves the approved 10-point, letter-paper, one-inch-margin convention. I approve these disclosed presentation extensions **for this exact bound experiment**:

- Use STIXGeneral for prose, Menlo for code, and STIX Two Text for otherwise missing script digits; all six font files were independently hash-checked.
- Disable raw-TeX passthrough so literal set differences such as `E\S` and `E\T` survive.
- In a separate presentation copy, escape prose underscores and duality stars that Markdown would parse as emphasis. Complete code and delimited mathematics remain unchanged.
- Wrap code without decorative continuation arrows, preserving all code tokens in the PDF extraction.

The source Markdown is unchanged. Every Math, CodeBlock and Table node remains equal before/after the presentation transformation. That AST check does not by itself prove all prose faithful; the direct page review and literal-notation checks supply the complementary evidence. Both tables retain all rows and columns, proofs and scope qualifications remain visible, and complete code appears in order without clipping.

The final LaTeX diagnostic is exactly one `Underfull \hbox (badness 1490)` at lines 632–642, in the toroidal-notation paragraph on replacement page 6. It causes uneven spacing only. I accept it after viewing that page. There are no final overfull or missing-character diagnostics and no replacement PDF extraction warnings. PDF timestamps can change file bytes; exact text extraction and raster equality are the reproducibility checks used here.

## Arithmetic and sensitivity

The common counting rule is pypdf 6.13.0's default `page.extract_text()`, pages joined by one newline, exact body selection and exclusions, Unicode NFC (primary) or NFKC (sensitivity), and whitespace collapse. The primary tokens are Python whitespace-separated units; the other metrics use the same selected text.

| Metric | NFC source sum / complete replacement | Factor | NFKC source sum / complete replacement | Factor |
|---|---:|---:|---:|---:|
| Whitespace tokens | 8,382 / 8,582 | 0.976695409 | 8,386 / 8,582 | 0.977161501 |
| Alphanumeric units | 8,155 / 10,393 | 0.784662754 | 8,155 / 10,393 | 0.784662754 |
| Non-whitespace characters | 32,926 / 49,419 | 0.666261964 | 33,007 / 49,449 | 0.667495804 |
| Characters after whitespace collapse | 41,306 / 58,000 | 0.712172414 | 41,391 / 58,030 | 0.713268999 |
| UTF-8 bytes after whitespace collapse | 42,805 / 59,392 | 0.720719962 | 42,730 / 58,701 | 0.727926270 |

All ten factors are below one. The difference between the whitespace-token and character-based results illustrates the importance of the declared representation and tokenization; the main finding is not robustly describable as a length reduction under any of these reported measures.

The replacement's full extracted-text SHA-256 is `78c8e0d804b8f4e3180ee69319bc4f640ad2e3b1a004d228e14c8eedd8ebf47c`; its NFC collapsed-text hash is `641970fc47dcb550631bcee40714901915bdb9a18523315f9e4eec53dab74fca`, and NFKC collapsed-text hash is `2c63c3ce44225797af38e370e96d21b01c618b88eefb1bfb0c7a6246d6d46f27`.

## Retained inputs and scope of admission

The mathematical recovery remains conditional on the listed background: the complete TomLib J1 subgroup catalogue/ambient permutation model and GAP algorithms; Danzer's generalized-cube theorem and full group; the classical Coxeter classifications/orders and standard spherical models; and the stated standard geometric facts. It does not assume a catalogue of the target J1 geometries. The bridge removes the formerly retained target toroidal-identification conclusion. The prior mathematical audit's qualifications remain unchanged, including the excluded comparative/auxiliary claims and the rank qualification on non-local-sphericity.

The replacement counts its retained-input interfaces and disclosures, but does not expand the entire external theorem libraries or subgroup catalogue. Eight external certificate/infrastructure/output files are separately bound at **30,390 bytes**. Their total includes the 9,241 bytes of exact executable duplicates already counted inside the manuscript; these should not be charged twice. The remaining wrapper, logs, metadata and outputs are separately disclosed infrastructure, not an uncharged missing proof appendix. This is a manuscript-body comparison, not a complete archive byte-cost comparison or a shortest-proof bound.

Admit the exact conditional **0.976695409** representation factor with the expansion label. Do not transfer an earlier four-source factor or seven-source lower bound to C, and do not transfer this measurement to the later ten-source assembly. This review establishes no new intake source, conjecture resolution, historical priority, or whole-manuscript Lean certificate. It makes no inference about researchers' scientific value or the relative effort of humans and models.

The JSON report and manifest bind the exact evidence and export allowlist. Primary source PDFs, source extractions and source raster images are not exported by this package; the allowlist contains measurement metadata, the replacement PDF, and audit/replay evidence only. Frozen author files and public repository files were not modified.
