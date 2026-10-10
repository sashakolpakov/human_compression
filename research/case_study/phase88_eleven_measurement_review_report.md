# Independent review of the eleven-source PDF-length measurement

Reviewer: `/root/compress_twogroups`. Date: 10 October 2026.

**PASS for the stated conditional lower bound, with the metadata correction below.**
The nine measured source bodies contain 51,739 NFC whitespace tokens; the
complete eleven-source replacement contains 34,845. Giving N001 and L108 zero
source credit therefore yields

\[
 \frac{\sum |\text{eleven specified source bodies}|}
 {|\operatorname{Compress}_{11}|}
 \geq \frac{51,739}{34,845}=1.4848328311091978.
\]

The inequality uses the declared editions, extraction convention and retained
background contract. The exact eleven-source factor remains **unavailable**.
This is the measured unannotated phase65 manuscript, not the phase79 annotated
reader. No factor is transferred to an annotated edition.

## Frozen objects and mathematical scope

This review binds the phase84 author manifest
`e1d73fa3845442af52765491ab57794c69d9ec5fbb81e2b378a283c58952976d`,
protocol
`7862cfcaa472b52eb94aeca47f77f47afbf7c33ae2fc47df1a78651e84623962`,
and runner
`48eab4238059d5477164454ba446551ecff7cdd17e02d468902cb6529391880e`.
The measured manuscript is `phase65_petrial_integration_manuscript.md`, SHA256
`6d302a2e7c696c916de97d2deef409c3053879999539be99a3fe72c9506205a1`.
The bound contract ledger is
`15457c4816b5630d23598489660e31bc5c047aacab02f1ee01d2218c756293a5`.

The intake is N001, N003, N008, L032, L035, F013, F016, L088, N013, N016,
and L108. Their specified principal-result contracts follow from the continuous
manuscript relative to the explicitly retained inputs and source corrections,
as established by phase70 and root phase76. This measurement review does not
reprove that implication or infer it from rendering. The 87 ledger rows also
record qualifications and unproved items; they are not a count of 87 theorems.
The mathematical contract does not claim to rederive every assertion in each
source body. Source discussion, examples and open questions remain in those
measured bodies according to the declared main-body convention.

The general multiple-minimal-cover question, complete five-family conjecture,
N013's external all-examples comparison and unused semiregular identification
are outside the proved intake. Later cover-family, nonabelian-obstruction and
N009 work are not silently added. This review makes no historical priority,
novelty, new-conjecture-solution or new Lean claim.

## Independent work

I read the full phase84 method/report, runner, protocol builder, source-status
record, exact source/body-boundary specifications, contract and external-cost
bindings, and the relevant helper functions. I read the earlier phase63
measurement audit and its explicit inherited source-reading boundaries. I
checked the source-selection endpoints and exclusion descriptions, including
the actual N003/N008 funding, page-marker and running-header text. The nine
document specifications are field-for-field identical to phase57.

I executed the frozen author runner in a new directory:

```text
python3 research/leemans/phase84_eleven_measurement.py \
  --output-dir /private/tmp/phase88_eleven_measurement_fresh --rasterize
```

The replay passed every declared check. Its durable byte-identical report is
`phase88_eleven_measurement_review_replay.json`, SHA256
`e98960a3946c70c49b1e6e67b004b3c38001ff1705c8a1f54589a0dc4103b070`.
Every one of the 57 independently produced raster hashes equals the frozen
author baseline. Extracted replacement text also agrees exactly.

I personally opened and inspected **all 57 individual replacement pages**.
The separate visual record gives a page-specific observation for each. No
visible missing glyph, clipped proof, lost continuation, cropped code or
omitted table row was found. The finite-cover table correctly continues from
page 35 to page 36, repeating its header and retaining its last Q-prime row.
The complete Petrial proofs and corrections occupy pages 37–39; their adapter
is on page 43. All five full programs are present, including the Python
appendix on pages 51–56, followed by complete references through page 57.

A second newly written checker imports **none of the author's counting or
rendering helpers**. It independently extracts all nine bound primary PDFs
with pypdf, reconstructs the two legacy page-marker formats, validates every
page and selected/excluded span hash, substitutes one space per exclusion,
normalizes and counts. It freshly extracts the replacement PDF, independently
invokes Pandoc on the selected source and presentation text, compares their
mathematical/code/table nodes, checks full standalone program bytes and finds
every complete code block in the PDF in order while ignoring whitespace only.
All ten metrics agree. Its report is
`phase88_eleven_measurement_review_check.json`, SHA256
`847e98ae4f2df6dc919c8a7a20b4f4ac195b7487d54076c8f73ed1336cb20454`.
All 132 bound inputs checked by it remained unchanged.

Fresh refusal tests rejected an existing renderer output directory and an
existing independent-counter report. All 87 existing replay files and the
counter report remained byte-identical. A separate altered protocol copy was
rejected by its immutable hash before an output directory was created. No
author, source, predecessor or public file was modified.

This review newly inspects replacement pages and freshly verifies primary
extractions/spans. It **inherits** the earlier complete primary-source visual
and boundary audits; it does not claim a new full mathematical reading or
visual examination of every primary PDF page. No GAP census or Lean build was
rerun for this length review.

## Numerator and version boundaries

| ID | Bound edition | NFC tokens |
| --- | --- | ---: |
| N001 | 1998 Buekenhout–Cara; faithful PDF unacquired | 0 |
| N003 | Twelve-page 2002 Cameron–Cara author PDF | 3,941 |
| N008 | Nine-page 2005 Archer–Cara–Krempa journal PDF, pp. 169–177 | 3,941 |
| L032 | Eight-page Hou–Feng–Leemans author revision, 8 November 2019 | 3,032 |
| L035 | Twenty-two-page arXiv:1802.08947v2, 22 January 2019 | 16,721 |
| F013 | Eleven-page arXiv:2605.20691v1, PDF dated 21 May 2026 | 4,540 |
| F016 | Nineteen-page arXiv:2512.15511v1, PDF dated 18 December 2025 | 8,183 |
| L088 | Ten-page 2005 Hartley–Leemans journal PDF, including late diagrams | 2,512 |
| N013 | Eleven-page arXiv:2001.11082v1, 29 January 2020 | 5,870 |
| N016 | Eight-page Cunningham author PDF headed 25 July 2023 | 2,999 |
| L108 | 2001 Bonheure–Buekenhout–Leemans; faithful PDF unacquired | 0 |
| | Nine measured bodies; two zero credits | **51,739** |

The source bodies start at their abstracts and stop before references, with
the explicitly reviewed exception that L088's mathematical diagrams on
pages 9–10 are retained after its bibliography. The bibliography/affiliation
block between that paper's proof and diagrams is excluded by an exact span.
Title/author metadata, keywords, funding/acknowledgments and running furniture
are removed by the inherited explicit intervals. No mathematical table,
auxiliary result, example or conjecture passage inside the selected body is
removed merely because it is outside the principal-result contract.

The two legacy page-wrapper formats contribute no tokens after their exact
exclusions. N003 and N008 really do have equal token counts from distinct
PDFs. The three pre-existing N008 font-dictionary warnings recur exactly.
No OCR, ligature, glyph or hyphen repair is silently introduced; inherited
nonwhitespace control codepoints remain recorded. Diagram edges are not
invented text. These facts limit the interpretation to a reproducible PDF
text representation rather than an abstract-symbol count.

N001 and L108 have complete authored browser bases for their mathematical
adapters, but no bound faithful PDFs for length. Browser counts and estimated
page lengths receive no credit. N016 is the July 2023 author version associated
with the 2024 publication, not an unacquired publisher PDF. Source acquisition
limits mean only that these versions were not acquired; they do not prove
unavailability elsewhere.

**Metadata correction accompanying this review.** In the frozen
`phase84_eleven_measurement_source_status.json`, the L035 edition sentence
mistypes the journal title as “2-groups having as automorphism groups of
regular 3-polytopes.” Read that phrase as **“2-groups behaving as automorphism
groups of regular 3-polytopes”**, already correctly printed in the measured
phase65 reference [HFLb]. The actual measured edition is the identically bound
author preprint titled *Existence of regular 3-polytopes of order 2^n*. This
report-only bibliographic correction changes no source, proof, boundary,
program or length. The earlier N008 name correction to Krempa is already
incorporated. Neither correction is an omitted mathematical proof cost.

## Complete denominator and presentation

The selected manuscript is exactly codepoints **[161, 228703)**, through EOF,
with **no internal exclusion**: 229,630 UTF-8 bytes before rendering. Only the
title and historical private-status prefix are outside it. The count includes
all common and source-specific proofs, every retained-input interface,
correction and qualification, the full affine/lattice bridge, complete new
K(c)/O0 and infinite-scope Petrial arguments, every adapter, and references.
The old mandatory reference erratum is already incorporated and is not
double-appended.

The five full executable programs are charged once inside the manuscript:
2,455 + 4,458 + 4,783 + 3,725 + 10,533 = **25,954 bytes**. Each appendix body
equals its separately bound executable byte-for-byte, including its final
newline. All eleven code blocks, including the six short mathematical ones,
survive PDF extraction completely and in order. The AST preserves 1,422
inline formulas, 107 displayed formulas and seven tables; all 75 proof-ending
marks survive. Source/code/table AST identity supplements, rather than
replaces, visual inspection.

The common input library remains substantive: older B97/Whiston/Burnside
results, named geometric correspondences and extension theorems, older
classified tight families and chirality input, SmallGroups' complete
order-256 catalogue, TomLib's complete J1 subgroup table and exact GAP
algorithms. Their declared interfaces and citations are counted; their full
proofs and data are not expanded. Five separately inventoried
build/integrity files total 38,978 bytes and supply no omitted mathematical
argument. This is not a full transitive-library or research-history measure.

Rendering uses the pinned Pandoc 3.10, XeTeX/TeX Live 2026, pypdf 6.13.0,
letter paper, one-inch margins, 10-point STIX text and Menlo code. Prose-only
escaping preserves literal underscores/duality stars outside protected
mathematics and code; raw TeX interpretation is disabled. Long code lines
wrap without decorative tokens. The final pass has only the three declared
underfull hbox messages: badness 5862 and 7030 at TeX lines 3948–3955 and
1755 at 4034–4046. Pages 43–44 show loose but legible spacing, without
overfull boxes or missing glyphs. Minor literal reference notation remains
visible. These are presentation qualifications, not proof omissions.

## Sensitivity and admission limit

| Normalization / unit | Numerator | Denominator | Conditional bound |
| --- | ---: | ---: | ---: |
| NFC whitespace tokens | 51,739 | 34,845 | 1.484832831109 |
| NFC alphanumeric runs | 53,349 | 37,486 | 1.423171317292 |
| NFC nonwhitespace codepoints | 198,889 | 176,656 | 1.125854768590 |
| NFC collapsed codepoints | 250,619 | 211,500 | 1.184959810875 |
| NFC collapsed UTF-8 bytes | 264,353 | 227,884 | 1.160033174773 |
| NFKC whitespace tokens | 51,780 | 34,845 | 1.486009470512 |
| NFKC alphanumeric runs | 53,349 | 37,486 | 1.423171317292 |
| NFKC nonwhitespace codepoints | 199,150 | 176,756 | 1.126694426215 |
| NFKC collapsed codepoints | 250,921 | 211,600 | 1.185827032136 |
| NFKC collapsed UTF-8 bytes | 264,159 | 215,288 | 1.227002898443 |

Normalization precedes counting; the same complete bodies are used in all
rows. Their material spread prevents a representation-independent factor
claim. The measurement concerns text length under an explicit conditional
principal-result contract, not research effort, mathematical value, historical
novelty, the shortest possible proof, or a fully formalized development.
The numerical result may be admitted with these boundaries and the metadata
correction. Public export remains the root's separate action; this package's
allowlist contains no primary PDF, primary full text or primary-source raster.
