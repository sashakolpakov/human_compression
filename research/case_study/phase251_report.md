# Measured reuse in the projective-line topic

The complete shared theory and two applications recover the specified
principal classifications of Leemans and Schulte: PSL2(q), L083, followed
by PGL2(q), L079. **Their total written replacement is currently longer on
the designated character metric.** Each local application is shorter once
the shared theory has been paid for. This is a measured pilot with two
applications, not evidence for a twenty-year trend or a repeated sawtooth.

The exact transformation is

```text
L083 principal proof + L079 principal proof
    <- U_E + complete required finite program + A1 + A2.
```

Here the arrow means recovery of the accepted principal conclusions. The
source papers also contain separate chiral, one-Petrie and semilinear
material outside these contracts. They are not claimed wholly replaced.
The mathematical scope and attribution were independently accepted in
phases234 and243. This measurement adds no principal source, no theorem and
no answer to an open question.

## Acquisition and local costs

The fixed primary proxy is the number of NFC-normalized non-whitespace
characters extracted from the PDFs. It is a reproducible representation
length, not minimum mathematical complexity.

| Historical passage | Cost | Complete local replacement | Cost | Conditional factor |
|---|---:|---|---:|---:|
| L083: PSL2 principal proof | 13,279 | A1: classification and geometry | 8,213 | 1.616827 |
| L079: PGL2 principal proof | 13,627 | A2: classification and simplex | 5,737 | 2.375283 |

The complete umbrella costs **18,264**, and the complete required finite
program appendix costs **4,754**. Their acquisition cost is **23,018**.
The local factors above assume this has already been paid; they do not
include it a second time. Every other topic still pays its own full
umbrella, without an overlap discount.

For the written papers alone,

$$R_{text}=\frac{13,279+13,627}{18,264+8,213+5,737}
          =\frac{26,906}{32,214}\simeq0.835227.$$

With our full required program, the corresponding conservative lower bound
on an artifact-inclusive factor is

$$R_{artifacts}\ge\frac{26,906}{32,214+4,754}
                  =\frac{26,906}{36,968}\simeq0.727819.$$

A historical supporting program, if any, is unavailable; its cost is
unknown, not zero. This inequality therefore does not determine the exact
artifact-inclusive factor or prove it is less than one. The original
protocol overstated the evidence for historical software use; the dated
[clarification](phase251_clarification.md) corrects that statement while
preserving the premeasurement protocol bytes.

![Acquisition, individual applications and cumulative costs](phase251_complexity.svg)

This graph orders the PSL2 source before the PGL2 source. It displays one
acquisition followed by two applications. Connecting the cumulative points
is only a visual aid; no intermediate work or future saving is inferred.
The historical supporting-artifact cost is unknown and is not plotted.

## All fixed coordinates

Both normalizations and all five proxies were fixed before computing the
comparison. They are reported even when they disagree about small savings.

| Normalization | Proxy | Historical writing | Our writing | Ours with program | Written factor | Artifact lower bound |
|---|---|---:|---:|---:|---:|---:|
| NFC | Whitespace tokens | 6,578 | 6,371 | 6,849 | 1.032491 | 0.960432 |
| NFC | Alphanumeric runs | 6,768 | 6,458 | 7,441 | 1.048002 | 0.909555 |
| NFC | Characters without whitespace | 26,906 | 32,214 | 36,968 | 0.835227 | 0.727819 |
| NFC | Characters with collapsed whitespace | 33,482 | 38,582 | 43,813 | 0.867814 | 0.764202 |
| NFC | UTF-8 bytes with collapsed whitespace | 34,714 | 40,686 | 45,917 | 0.853217 | 0.756016 |
| NFKC | Whitespace tokens | 6,579 | 6,371 | 6,849 | 1.032648 | 0.960578 |
| NFKC | Alphanumeric runs | 6,768 | 6,458 | 7,441 | 1.048002 | 0.909555 |
| NFKC | Characters without whitespace | 26,950 | 32,216 | 36,970 | 0.836541 | 0.728969 |
| NFKC | Characters with collapsed whitespace | 33,527 | 38,584 | 43,815 | 0.868935 | 0.765195 |
| NFKC | UTF-8 bytes with collapsed whitespace | 34,673 | 38,907 | 44,138 | 0.891176 | 0.785559 |

Whitespace-token and alphanumeric-run counts give small written savings;
character and byte counts do not. The designated primary coordinate is
unchanged. Font encodings, formula layout and PDF extraction affect these
proxies even under the same extraction procedure. Physical page counts
are an inventory only: historical editions have 14 and 9 pages, the complete
U_E/A1/A2 have 7/3/2 pages, and the program appendix has 3 pages. Those
numbers are not a common-format page ratio.

## What is shared and what is borrowed

The [two theorem dependency graphs](phase251_dependency_dags.md), with
[explicit edge reasons](phase251_dependency_dags.json), show the actual
historical reuse. L079 invokes L083 to exclude characteristic two, repeats
its subfield counting argument, and directly reuses its finite table.
The historical cost counts each printed passage once. It does not charge
a fictitious second table or a second program.

Our common argument uses dihedral centralizer descent, an odd-order
normalizer lemma and one finite computation. Both full application papers
use this theory; A2 does not depend on A1. Named lemmas and connected proof
blocks are diagrammed, but they do not carry separate numerical weights.
The graph is a proof map, not a minimal dependency DAG or a ratio of nodes.

Both sides retain the named classical background: Dickson's subgroup
results, elementary projective group structure, and the group–polytope,
coset and covering correspondences. The historical PSL2 rank bound is a
separate retained theorem of Leemans–Vauthier; our rank bound is proved in
U_E. This comparison conditions on that common available library. It does
not assign a zero unconditional proof cost to it, and it does not assert
that both arguments use every retained item.

The classifications remain attributed to Leemans and Schulte. The six
local map classes and ten universal groups are earlier mathematics; the
replacement provides a new organization and exact replay of their use.
No historical priority claim is made for the centralizer method. Optional
Lean verification checks specific normalizer and matrix statements; it
is not a complete formalization of either classification. Its files and
the replay/review machinery are recorded separately from proof acquisition.

## Reproduction and limits

[Boundaries and hashes](phase251_boundaries.json) specify every included
source interval, every removed page header or number, and all six PDFs.
Every word of our three complete papers and every non-whitespace character
of the required program are counted. The primary publication PDFs, extracted
text and page images remain private. To reproduce, obtain the exact bound
editions in `sources/` and use pypdf 6.13.0 with a new output file:

```sh
python3 -B -O phase251_measure.py --root . --out /tmp/NEW-topic-E.json
python3 -B -O phase251_controls.py --root . --out /tmp/NEW-topic-E-controls.json
python3 -B -O phase251_make_graphs.py --root .
```

The three rejection controls alter a source PDF, a selected interval and
the required program. They test measurement integrity, not the mathematics.
The separately written phase252 implementation independently recomputes all
ten coordinate rows and their document hashes. The primary mathematical
proofs retain their existing reviews and computational trust boundaries.
The phase251 author manifest freezes this packet; acceptance requires the
separate phase252 review.
