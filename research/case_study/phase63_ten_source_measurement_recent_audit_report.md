# Independent audit of the nine-source/full-ten measurement

Reviewer: `/root/review_unified_seven`. Date: 10 October 2026.

**PASS, with an explicitly conditional lower bound.** The complete, independently
reviewed ten-source replacement, including its mandatory reference erratum,
contains **30,957 NFC whitespace tokens** in the declared rendered-PDF
convention. The nine measurable source bodies contain **51,739**. Crediting
the remaining source N001 with zero gives

\[
 \frac{\sum_{i\ne\mathrm{N001}} |X_i|+0}
 {|\operatorname{Compress}_{10}+\text{required erratum}|}
 =\frac{51,739}{30,957}
 =1.6713182801951094.
\]

This is an admissible **lower bound for the ten-source ratio under this
particular convention and the reviewed retained-background contract**. It is
not an exact ten-source ratio; that field remains null. If N001's eventual
faithful body count is any nonnegative number, the numerator can only increase
while this fixed denominator is held unchanged. No guess about N001's length
or damaged extraction is used. The replacement is 20,782 tokens, or about
40.1670%, shorter than even the nine-source subtotal under this convention.

The result measures text, not human effort, importance, historical novelty, or
algorithmic information. It does not establish that every assertion in every
source has been rederived, or that the replacement is Lean verified.

## Named intake and actual replacement

The admitted mathematical relation remains

\[
\begin{aligned}
 (&\mathrm{N001,N003,N008,L032,L035,F013,F016,}\\
  &\mathrm{L088,N013,N016})
 \longrightarrow \operatorname{Compress}_{10}
       +\text{the exact required reference erratum},
\end{aligned}
\]

for the source-specific **principal-result contracts** reviewed in phase52,
relative to their disclosed retained inputs. The body is the continuous
`phase45_ten_source_manuscript.md`, SHA-256
`f7d66e2b0b67da95e1d345fd47cd9e86c03a4309ca38ab9c8b18dd58a0f475fa`,
plus the entire `phase45_ten_source_errata.md`, SHA-256
`bad11f9a405d30cbdefdb0a04eb7750e650e6f1016cf70b805db2a96fcee05aa`.

| ID | Bound source and edition | NFC body tokens |
| --- | --- | ---: |
| N001 | Buekenhout–Cara, *Some properties of inductively minimal geometries* (1998); complete authored browser basis for the mathematical adapter, but no faithful PDF for this measurement | **0 credited** |
| N003 | Cameron–Cara, *Independent generating sets and geometries for symmetric groups* (2002); complete twelve-page author manuscript | 3,941 |
| N008 | Archer–Cara–Krempa, *Using the Frattini Subgroup and Independent Generating Sets to Study RWPRI Geometries* (2005); complete nine-page journal PDF | 3,941 |
| L032 | Hou–Feng–Leemans, *On regular polytopes of 2-power order*; author PDF revised 8 November 2019, published 2020 | 3,032 |
| L035 | Hou–Feng–Leemans, *Existence of regular 3-polytopes of order 2^n*; arXiv:1802.08947v2, 22 January 2019; journal catalogue title *2-groups having automorphism groups of regular 3-polytopes* | 16,721 |
| F013 | Hou–Schulte, *String C-groups of 2-power order project onto a common string C-group*; arXiv:2605.20691v1, PDF dated 21 May 2026 | 4,540 |
| F016 | Cunningham–Feng–Hou–Schulte, *Symmetric polytopes whose automorphism groups are 2-groups*; arXiv:2512.15511v1, PDF dated 18 December 2025 | 8,183 |
| L088 | Hartley–Leemans, *On the thin regular geometries of rank four for the Janko group J1* (2005); ten-page journal PDF | 2,512 |
| N013 | Montero–Ivić Weiss, *Locally Spherical Hypertopes from Generalised Cubes*; arXiv:2001.11082v1, 29 January 2020 | 5,870 |
| N016 | Cunningham, *Chiral polytopes whose smallest regular cover is a polytope*; eight-page author manuscript headed 25 July 2023, associated with the 2024 journal publication | 2,999 |
| | **Nine-source subtotal, with N001 assigned zero** | **51,739** |

The source years span 1998–2026. Later journal numbering or unretrieved versions
are not silently substituted. In particular, N016's newly obtained PDF closes
the **author-version measurement gap**, not the gap to its publisher PDF.

The independent phase52 proof review remains the basis for the mathematical
implication. This phase63 audit verifies measurement and presentation; it does
not infer mathematical correctness from a renderer's success. The 79 ledger
rows include qualifications and unproved questions as well as principal
clauses; they are not 79 newly proved theorems.

## Independent work actually performed

I read the complete phase57 runner, protocol builder and prose report, the
measurement specifications and their retained-contract/cost records, and the
new N016 PDF text in full. I compared the latter against the complete frozen
phase41 browser basis and checked all eight original pages visually. I
personally inspected **all 49 pages of the freshly rendered replacement**,
including every table, the complete four GAP appendices and the last-page
erratum. I also inspected N008's title page to resolve the author-name typo.
The visual record has page-specific observations and exact raster hashes.

The no-clobber author runner was freshly executed in a new scratch directory:

```text
/Users/sasha/.venvs/global/bin/python \
  research/leemans/phase57_ten_source_measurement.py \
  --output-dir /private/tmp/phase63-ten-independent-replay --rasterize
```

Its report SHA-256 is
`25cfbcbd10a395a98ac157019fd4b4b6e0ff789787c9418477b831caf825366d`.
All **49 replacement raster hashes** match the frozen author's baseline.
All **eight independently generated N016 raster hashes** also match the
author's source-page baseline. No toolchain drift was reported.

A second, newly written counter imports **none of the author's Python
measurement/render helpers**. It directly extracts all nine primary PDFs with
pypdf 6.13.0, rebuilds the two legacy page-marker formats, checks each page
hash and all exact spans, removes only the approved intervals, independently
normalizes and counts, and freshly extracts the rendered replacement. It also
regenerates the original Pandoc AST independently, checks the unchanged
math/code/table nodes, compares complete GAP program bytes, and locates every
complete code block in the extracted PDF in order, ignoring whitespace only.
The counter's report SHA-256 is
`09368d0aa56e5a3d063277afb575b238044e941fedd3c5680d92ade109a2eab0`.

All ten metric results agree with both the authored result and the fresh
renderer. All **42 bound input files** checked by the counter remained
unchanged before and after its run. Fresh refusal tests confirmed that
reusing the renderer's output directory or the counter's report path fails
without changing the 79 existing scratch files or the independent report.

No GAP census or Lean compilation was rerun during this measurement audit.
The earlier proof, census and formal reviews retain their original scope and
dates. Neither this audit nor its counter is a new theorem-proving result.

## Numerator boundaries and source integrity

The six source specifications from phase43 and the two from phase51 were
compared field by field against their pinned prior protocols. **Every prior
field is identical.** The only additions are a note honestly describing the
inherited reading scope and, for L088/N013, an empty expected-warning list.
No body boundary, excluded interval, PDF version, page hash or extraction
hash changed. The earlier visual/source-boundary reviews are inherited;
phase63 does not claim a fresh complete proof reading of those eight papers.

The six earlier bodies total 40,358 NFC tokens. L088 and N013 add 8,382;
N016 adds 2,999. N003 and N008 each having 3,941 tokens is a verified
coincidence: the independent counter extracts different bound PDFs and
different bodies and obtains those equal counts separately.

The L088 boundary still includes its mathematical diagram pages **9 and 10**,
despite their position after the bibliography. Its bibliography/affiliations,
running navigation and acknowledgments are excluded by the already reviewed
intervals. Diagram labels count as extracted characters; drawn edges do not
become invented text tokens. N013 retains the complete abstract and body to
References, using the original arXiv version and its numbering.

N016's new primary PDF is bound by SHA-256
`d5a53919d17c70f44ef3a6b2761f07e731ce76baf1aeed5548288fe07c6422f0`.
The complete extraction SHA-256 is
`f375764b3854da0fb88ac140c9d6e4196cb564074a42065bd95c8393116fefa8`.
Its body is the exact codepoint interval **[185, 15398)**, beginning at
Abstract and ending immediately before the References heading on page 7.
The only internal exclusions are keyword/AMS metadata **[360,496)** and the
single-character printed footers at **[1958,1959), [4818,4819),
[6551,6552), [9427,9428), [11306,11307), [14003,14004)**.
Each is replaced by one ASCII space. Page 8 is references only. All
mathematical, historical and open-question discussion remains, including all
finite presentations and the concluding conjectures. The source's visible
mirror overbars are not reconstructed in the count when pypdf omits them.

The new PDF's title/date, numbered statements, five classified-family table,
square-torus example, finite presentations and flag counts agree with the
frozen July 2023 author-version basis used by the adapter. The existing
rank-base, nonidentity-power, embedded-local-group and mix/polytopality
qualifications remain in force. This is not a claim that an unread publisher
version has identical statements or corrections, nor a fresh priority search.

N008 produces its three already declared pypdf font-dictionary warnings,
at bytes 0xa69 and 0xa74 for `/F18`, and 0xac6 for `/F45`. No additional
source extraction warnings occurred. Some inherited mathematical PDFs yield
nonwhitespace control codepoints: F013 has 0/1/2, F016 has 2/17, and L088
has 0/2/3/17/18/20/21/22/23/24/27. The counter records them and does not
silently repair or discard them. They underline why this is a reproducible
PDF-text representation metric, not a count of abstract mathematical symbols.

The frozen phase57 report table misspells Krempa as Kemp. The accompanying
**metadata erratum** corrects exactly that occurrence. N008's printed author
name was independently checked. This repair changes no source or proof text,
so it adds no proof-denominator cost. It must not be confused with the
mathematical reference erratum that is included in full below.

## The entire required denominator is charged

The replacement begins at codepoint **161** of the frozen ten-source Markdown,
the first substantive introductory paragraph, and continues to EOF. Only the
title/private-status prefix is outside the measured body. There are **no
internal exclusions**. The entire 638-byte mandatory erratum is then appended
after two newlines, from its own BOF to EOF, including its heading, manuscript
hash, original and corrected sentence, and explanatory metadata.

This charges the whole introduction, common theory, retained-input statements,
all 24 sections and source adapters, qualifications, source-version and
reference list, and all four complete executable programs. It also charges
the full internal Gray-code/face-poset, duality, affine-group and lattice
proof. That proof closes the old C lattice-identification gap inside this
manuscript; the external bridge is not a hidden required proof supplement.

The four appendix programs are exact byte-for-byte copies of their separately
bound executable files, with sizes **2,455 + 4,458 + 4,783 + 3,725 = 15,421
bytes**. They are counted once as part of the rendered manuscript, not charged
again as duplicate files. All four appear completely in the PDF, including
long wrapped records. Six additional short code-format mathematical blocks
are also present in full.

The independent source/final AST comparison preserves **1,424 inline math
nodes, 99 display math nodes, seven tables and ten code blocks**. The PDF
contains all **70 QED marks**. These inventory checks supplement the visual
inspection; they are not substitutes for reading proofs.

The separately listed integrity/review scripts and their reports are
infrastructure rather than omitted mathematical proof steps. Their sizes
remain disclosed: 5,109, 1,485, 8,561 and 11,442 bytes, totaling **26,597**.
The experiment does not price the whole research repository, audit history,
PDF tools, GAP implementations, libraries or hardware.

The approved phase61 attribution reader is a **different representation**.
Its margin notes add provenance explanations and no new proof premises or
steps, as reviewed independently in phase62. It is not the denominator here.
The 1.6713 bound cannot be transferred to the complete annotated reader
without counting that reader separately. The metadata correction in this
phase63 package likewise introduces no mathematical premise.

## Rendering review and diagnostics

The pinned rendering uses Pandoc 3.10, XeTeX/TeX Live 2026, letter paper,
one-inch margins and a 10-point main font. It extends the previously reviewed
C renderer with arbitrary-position code wrapping, splitting long inline-code
strings and six-em emergency paragraph stretch. Decorative code-wrap arrows
are suppressed. Prose underscores and duality stars are escaped outside
protected math/code; raw TeX interpretation is disabled. These are
presentation changes. I approve them for this exact body after checking the
AST invariants, complete extracted code, diagnostics and every page.

The exact header SHA-256 is
`9ea220c41b37f2f2b081864212863ca4c8edd580c470268d018bd046b3f7340c`.
Six bound STIX/Menlo font files were freshly hash checked. The fresh report
also records embedded fonts and TeX inputs. This does not claim byte-identical
PDF metadata across builds; raster and extracted-text identity are the
relevant reproduced outputs.

The first XeLaTeX pass requests the usual second pass for labels and table
widths. The final pass has exactly **three underfull paragraph diagnostics**:
badness 5862 and 7030 at TeX lines 3645–3652, and badness 1755 at lines
3713–3722. On PDF pages 39 and 40 these produce uneven word spacing, with
all text intact. There are no final overfull-box or missing-glyph diagnostics.
The continued finite-cover table retains its final Q-prime row on page 35;
the long code and hash strings on pages 47–49 remain inside the margins;
the complete erratum is visible on page 49. A minor literal reference-list
asterisk is a presentation artifact, not missing mathematical content.

## Sensitivity arithmetic

Normalization precedes splitting. The primary metric is NFC-normalized
whitespace-delimited tokens. The sensitivity counters use Unicode
alphanumeric runs, nonwhitespace characters, characters after collapsing
whitespace to single spaces, and UTF-8 bytes of that collapsed text. NFKC is
reported separately; it is not chosen after seeing a favorable result.

| Normalization and metric | Nine-source numerator | Full-ten denominator | Conditional lower bound |
| --- | ---: | ---: | ---: |
| NFC tokens | 51,739 | 30,957 | 1.671318280 |
| NFC alphanumeric runs | 53,349 | 33,064 | 1.613507138 |
| NFC nonwhitespace characters | 198,889 | 155,487 | 1.279135876 |
| NFC collapsed characters | 250,619 | 186,443 | 1.344212440 |
| NFC collapsed UTF-8 bytes | 264,353 | 202,264 | 1.306970098 |
| NFKC tokens | 51,780 | 30,957 | 1.672642698 |
| NFKC alphanumeric runs | 53,349 | 33,064 | 1.613507138 |
| NFKC nonwhitespace characters | 199,150 | 155,587 | 1.279991259 |
| NFKC collapsed characters | 250,921 | 186,543 | 1.345110779 |
| NFKC collapsed UTF-8 bytes | 264,159 | 189,956 | 1.390632568 |

All ten comparisons exceed one, but their spread is material. There is no
representation-independent compression factor. This result also does not
replace the distinct B factor, the seven-source lower bound, or the C+bridge
expansion result; those use different source sets and denominators.

## Mathematical and attribution limits carried forward

The manuscript supplies a common kernel-transport interface, relative
generation and primitive-coordinate arguments, a shared affine square model,
endpoint recognition, and residue-extension machinery. Source conclusions
are recovered by the reviewed adapter/corollary contracts. Substantial
forest, cyclic-model, marked-intersection, typed-Helly, finite-census and
local-cover proofs still occupy the denominator. This is meaningful reuse,
not a finding that all ten papers contained only a single elementary lemma.

Retained inputs remain substantive: B97 and other older geometric inputs,
Whiston's theorem in its declared degree range, Burnside/Frattini facts,
the SmallGroups order-256 data and GAP algorithms, the complete TomLib J1
subgroup catalogue, and older tight-family/prime-chirality results. The
per-adapter dependency records are selected interfaces, not a complete
transitive library closure. The ratio assumes these same background inputs
are available on both sides and does not count a proof of all of them.

The principal-result implication does not include every auxiliary assertion
or unproved conjecture in the source bodies. In particular, the general
multiple-minimal-cover conjecture, the complete five-family conjecture,
N013's external all-examples comparison and its unused semiregular
identification are not newly solved by this ten-source assembly. Later
kernel and cover-family work is separate and is not retrospectively imported
into this frozen manuscript or its measurement. N009 and L108 are not
additional admitted sources. There is no new priority claim, no new Lean
component and no claim of a wholly formalized manuscript.

This audit changes no source, author freeze or public file. Its manifest
provides an exact export allowlist for the authored measurement package and
the independent evidence, including the metadata correction. Primary source
PDFs, extracted source text and source-page rasters remain private. Root
admission and public export are separate later actions.
