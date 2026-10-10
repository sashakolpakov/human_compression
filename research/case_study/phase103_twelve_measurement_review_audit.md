# Independent review of the twelve-source manuscript measurement

10 October 2026. **PASS, with no required correction to the frozen author package.** A fresh render, an independently written counter and individual inspection of every replacement page reproduce the conditional NFC/default-PDF-text whitespace-token lower bound

\[
R_{12}\ge 59636/44269 = 1.3471277869389415\ldots.
\]

**This is a lower bound, not the exact twelve-source factor.** N001 and L108 each receive zero numerator credit because faithful PDFs are absent. The complete twelve-source replacement is charged. The exact factor remains unavailable.

**The result depends on the representation and count convention.** The NFC nonwhitespace-character lower bound is **0.9183954868**, and the collapsed NFC UTF-8 byte lower bound is **0.9789236290**. These do not establish compression in those metrics. With two source lengths omitted, they also do not establish expansion for the eventual complete twelve-source comparison. No representation-independent size claim follows.

## Binding and mathematical scope

The reviewed author manifest is `phase98_twelve_measurement_manifest.json`, SHA256 `7477a91be128f4c0fb953e4a7f4b9d422bd70a371367de1fcee2db0cd59b229d`. The exact replacement is the 317,916-byte `phase78_n009_integration_manuscript.md`, SHA256 `15dd00e3845526dc40bb0effa07652e32748958238759eae9a856d901071b801`.

The implication being measured is the corrected, explicitly conditional principal-result contract

`N001, N003, N008, L032, L035, F013, F016, L088, N013, N016, L108, N009 → Compress_12`.

Mathematical acceptance is inherited from frozen phase87 and its unchanged-branch predecessors. This review audits measurement, rendering and coverage; it does not rerun GAP, reprove the mathematics, add Lean coverage, establish historical priority, solve a conjecture, or certify every sentence of every intake paper as a literal corollary. The source corrections remain part of the contract. The exact exceptional infinite decomposition attributed to McMullen–Schulte remains a substantial retained input, as do the declared string-IP criteria, geometry/cover interfaces, B97, Whiston, Burnside, cyclic-core and other named classifications, TomLib and exact GAP/NQ algorithms. No full transitive-background proof-length bound is asserted.

## Independent reproduction and count

I executed the frozen author runner with optimization enabled into the new directory `/private/tmp/phase103-twelve-replay`, including rasterization. It freshly extracted all ten acquired primary PDFs, rebuilt the replacement and reproduced the complete expected extraction and all 83 page-raster hashes. The replay report and diagnostic logs are preserved in `phase103_twelve_measurement_review_replay/`.

I also wrote and executed `phase103_twelve_measurement_review_count.py`. It imports no author measurement or rendering helper. It directly extracts the primary PDFs with pypdf, verifies every bound page and body/exclusion span, replaces each excluded span by one space under the declared convention, and counts by an independent character-state algorithm. Alphanumeric runs are counted by transitions in `str.isalnum()`, independently of the author's regex. Both NFC and NFKC counts, collapsed-text hashes, source sums and exact rational divisions agree. The repeated N003/N008 value 3,941 is independently obtained from two different PDFs.

| Source | NFC body tokens |
|---|---:|
| N001 | 0 credited |
| N003 | 3,941 |
| N008 | 3,941 |
| L032 | 3,032 |
| L035 | 16,721 |
| F013 | 4,540 |
| F016 | 8,183 |
| L088 | 2,512 |
| N013 | 5,870 |
| N016 | 2,999 |
| L108 | 0 credited |
| N009 | 7,897 |
| **Sum** | **59,636** |

All nine inherited source PDF editions, bytes, page extractions, boundaries and exclusions match phase84/88 field for field. The correction to the L035 journal-title metadata and Krempa's name are correctly reflected; neither changes the count. N016 still uses the acquired eight-page author edition headed 25 July 2023, without a claimed equivalence to the unacquired publisher PDF. Browser-rendered N001/L108 source reading does not become PDF-length credit.

## Visual and boundary review

I individually opened **all 83 replacement page rasters** and **all 22 N009 source page rasters**, at full-page readable resolution, as separate images. `phase103_twelve_measurement_review_visual.json` records every page, hash, inspected region and observation. The replacement rasters are byte-identical to my fresh replay. Older nine-source visual readings are explicitly inherited from phase84/88 and its predecessors; their full sets of pages were not all re-viewed in this audit. Their exact primary bytes and every extracted page were freshly checked by the independent counter.

The new N009 source is the complete journal PDF, Contributions to Discrete Mathematics 13(1) (2018), 1–22, SHA256 `0618a57cb5ff35c13587877818a2e77bce442cf2c561f204b6d5e5e095fa2fda`. Its selected extraction span is [151, 43854), Abstract through all concluding remarks. I checked every one of the 21 internal exclusions against the page images and extracted text: the first removes only dates/MSC/keywords/thanks/copyright/footer, and twenty remove running headers. References and the affiliation-only page 22 are after the endpoint. All six tables, their repeated continuation headings and rows, diagram labels/caption, proofs, displayed formulas, examples and quoted background remain counted. Literal table errors remain in the source count; no corrected text is substituted.

The previous L088 convention, including mathematical diagrams after its references, is unchanged. No OCR, hyphenation, ligature, lost graphical placement or control-character repair is made. The three inherited N008 font-dictionary warnings recur exactly. Default extraction is a declared imperfect representation of mathematical typesetting; graphics with no extractable text receive no separate area charge.

## Complete denominator

The measured body starts at codepoint 161 and runs through EOF. Only the initial title/historical-status heading is omitted. All **26 numbered sections**, full references, retained-input interfaces, source corrections, final adapters, and **eight full code/data blocks totaling 79,874 bytes** are included. The independent counter checks each appendix byte for byte against its standalone file. It also checks every one of the 14 Pandoc code blocks in the PDF extraction, in order, after whitespace removal.

Appendices A–H contain the complete shared census, both J1 certificates, chiral-cover certificate, optional Petrial controls, N009 presentation recognition, all named presentations and 107 Table 6 data rows, and the full mathematical replay runner. The optional controls and orchestration are charged. Standalone duplicate files are counted once, inside the manuscript. No necessary external proof addendum is omitted. The historical Section 16 exclusion of N009 is preserved and counted as an earlier four-source-branch boundary; current Section 24 and Corollary N7 supply the admitted N009 contract.

The renderer's presentation transformations preserve every Math, CodeBlock and Table AST node. All 1,405 inline and 120 display math nodes, 12 tables and 85 proof-ending squares remain represented. I found no clipping or omitted table/code continuation. The added Unicode fallback displays the new symbols; it changes no mathematical AST or source byte. The accepted four underfull warnings on pages 6, 50 and 51 affect spacing only. There are no accepted missing-glyph or overfull warnings.

The denominator is **44,269 rendered-PDF tokens**, not the smaller 39,768 raw-Markdown count. The complete independent sensitivity results are:

| Convention | Source sum | Denominator | Lower bound |
|---|---:|---:|---:|
| NFC whitespace tokens | 59,636 | 44,269 | 1.3471277869 |
| NFKC whitespace tokens | 59,677 | 44,269 | 1.3480539429 |
| NFC/NFKC alphanumeric runs | 62,537 | 51,526 | 1.2136979389 |
| NFC nonwhitespace characters | 233,120 | 253,834 | 0.9183954868 |
| NFC collapsed characters | 292,746 | 298,102 | 0.9820329954 |
| NFC collapsed UTF-8 bytes | 309,055 | 315,709 | 0.9789236290 |
| NFKC nonwhitespace characters | 233,471 | 253,948 | 0.9193653819 |
| NFKC collapsed characters | 293,138 | 298,216 | 0.9829720739 |
| NFKC collapsed UTF-8 bytes | 308,777 | 302,440 | 1.0209529163 |

The denominator is 15,367 tokens, or 25.76799249%, smaller than the conservative ten-body numerator under the primary convention. Later standalone results and attribution-note readers are outside this measured text and receive no credit. Review/render infrastructure and logs are separately bound artifacts, not disguised missing mathematical proofs. The author's 38,317-byte reconstruction/review infrastructure is separately disclosed; its necessary mathematical programs are already in the denominator.

## Portability, controls and publication boundary

The author's 132-file allowlist plus its manifest and retained inputs form an exact **158-file nonprimary union**. I copied that union to an isolated directory with no primary PDFs and successfully ran the independent counter in `--replacement-only` mode. All retained dependencies not in the new allowlist already have exact matching public copies. The portability record lists these matches and every exact image/PDF binding. My checker reads every one of the 132 manifest-bound files; they cannot silently be omitted from export.

The new imagery consists of exactly `phase98_twelve_measurement_render/page-01.png` through `page-83.png`, and the single `replacement.pdf`, SHA256 `a9736e98b5eaa49386a0a7c40afb337872e033cb3826db1ae4a49d090b52662c`. These are repository-authored replacement renderings, confirmed by regeneration and individual inspection. No primary PDF, extracted source body or primary-page raster is on the allowlist. Root may therefore add an explicit exception for these exact paths and hashes to its public snapshot policy; a wildcard exception is unnecessary.

My own three existing-output controls and five isolated mutations (protocol, manuscript, data, replacement PDF, final page raster) all reject without changing originals or creating a claimed result. The author-defined three refusal/eight mutation controls were also freshly executed independently against my replay; their separate report preserves their author-defined scope. No frozen author, earlier review or public file was changed.

Portable replacement-only check, from the directory holding the exact exported originals and retained bindings:

```sh
python -O phase103_twelve_measurement_review_count.py --replacement-only --output /tmp/NEW-independent-count.json
```

Omit `--replacement-only` when the private primary PDFs have been placed at the protocol's exact paths. Full rendering additionally uses the frozen phase98 runner and its declared toolchain. Results and output directories must not already exist. This review adds no new source-count admission or mathematical theorem; it approves the stated measurement and its explicit limits.
