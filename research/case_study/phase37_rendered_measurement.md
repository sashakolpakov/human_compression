# Frozen two-paper replacement: rendering sensitivity

This fresh run renders the fixed Compress_A v1 body, then applies the frozen counting rules to its PDF extraction. Source bodies and exclusions remain unchanged. All quotients below describe these representations; none is an approved compression factor.

Status: `rendering_sensitivity_only_bound_replay_pass`. Output directory: `/private/tmp/mc_phase37_rendered_final`.

| Normalization | Count unit | Source sum | Raw replacement | Rendered replacement | Source/raw | Source/rendered |
|---|---|---:|---:|---:|---:|---:|
| NFC | whitespace_tokens | 7222 | 5300 | 5968 | 1.362642 | 1.210121 |
| NFC | alphanumeric_units | 7157 | 6126 | 5756 | 1.168299 | 1.243398 |
| NFC | characters_without_whitespace | 28617 | 30388 | 27009 | 0.941720 | 1.059536 |
| NFC | characters_with_collapsed_whitespace | 35837 | 35687 | 32976 | 1.004203 | 1.086760 |
| NFC | utf8_bytes_with_collapsed_whitespace | 36700 | 35771 | 36394 | 1.025971 | 1.008408 |
| NFKC | whitespace_tokens | 7222 | 5300 | 5968 | 1.362642 | 1.210121 |
| NFKC | alphanumeric_units | 7157 | 6126 | 5756 | 1.168299 | 1.243398 |
| NFKC | characters_without_whitespace | 28641 | 30388 | 27013 | 0.942510 | 1.060267 |
| NFKC | characters_with_collapsed_whitespace | 35861 | 35687 | 32980 | 1.004876 | 1.087356 |
| NFKC | utf8_bytes_with_collapsed_whitespace | 36676 | 35771 | 33684 | 1.025300 | 1.088826 |

The PDF has 9 pages. Pandoc parses 362 inline and 19 display math expressions. All 21 proof-end marks appear as 21 extracted black squares.

Pandoc/rendering stderr is empty: `True`. Missing-glyph diagnostics: `[]`. The bound exploratory AST and extraction replay exactly: `True`.

N001 remains a damaged browser transcription with control characters and formula/diagram loss, and its original PDF is still unavailable. Rendering the replacement does not make the source representations uniform. Text extraction is sensitive to formula layout, ligatures, font encodings and line boundaries. The run makes no mathematical equivalence claim and does not measure or admit the three-paper manuscript.

The root agent previously inspected pages 2 and 3 of the bound exploratory render. That is a limited visual observation, not a complete visual audit. This runner checks syntax counts, proof-end marks, diagnostics and exact extraction replay; it does not visually inspect pages.

Reproduction requires the private hash-bound primary transcriptions, the frozen body protocol/helper and v1 manuscript. The runner refuses an existing output directory and never writes source bodies or source PDFs. The authored replacement PDF and its extraction stay in the chosen private scratch directory. `report.json` records all input/output hashes, versions, commands, font names, exact counts and normalization hashes.

Run with Python and the bound pypdf/Pandoc/XeLaTeX versions; replace the paths below with the private input directory and a new output directory:

```sh
python3 phase37_rendered_measurement.py \
  --input-root /path/to/private/research/leemans \
  --output-dir /private/tmp/compress-A-v1-render-NEW
```

A toolchain mismatch is refused by default. `--allow-toolchain-drift` permits an explicitly labeled sensitivity run, while preserving all input hashes, body boundaries and counting rules.

PDF bytes can differ through metadata even when the extracted content and AST replay exactly; byte-identical PDF reproducibility is not claimed.
