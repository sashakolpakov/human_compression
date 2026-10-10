# Recognizable extensions and finite incidence representations

Read the complete [written manuscript](research/case_study/phase177_finite_pair_representation.md)
and its [independent review](research/case_study/phase188_F010_independent_review.md).
This application recovers the principal constructive results of Antonio
Díaz Ramos, Rémi Molinier and Antonio Viruel, *Every finite group is
represented by a finite incidence geometry*,
[arXiv:2511.02410v2](https://arxiv.org/abs/2511.02410v2), 16 December 2025.
This is the independent followup F010 in the intake. The theorem and
constructions belong to those authors; they are not new conjecture
solutions by this project.

    One restriction-and-extension criterion
      + explicit recognition and rigidity proofs for three constructions
        -> F010 Theorems 3.1, 4.1, 4.2 and A;
      + a complete recursive argument
        -> the source's symmetric-group family and its size formulas.

For every finite group G and normal subgroup H, the construction gives a
finite incidence geometry whose correlation group is G and whose
type-preserving automorphism group is H. For nontrivial G, the constructed
geometry is connected and has rank [G:H]+3. The trivial group uses a
one-vertex rank-one geometry. Normality and the freedom to vary rank are
part of the statement.

The common argument recognizes the original vertices inside an enlarged
graph, proves that an automorphism fixing them fixes the entire graph,
and extends every original automorphism uniquely. Tracking the action on
the colour classes identifies the type-preserving kernel. The manuscript
pays these obligations for the ordered-pair encoding, chamber completion
and cleaning construction. The recursive symmetric-group family also
requires recognition of its attached copies, supplied by their connected
interiors and distinct boundaries.

Three local source qualifications remain explicit. In chamber completion,
the degrees are r−1 for new vertices and d(v)(r−1) for original vertices.
The completed hexagon has pair (D12,S3), with D12 of order twelve, rather
than the printed (D12,C3). The recursive family has minimum degree two
from n=3; its n=2 base path needs cleaning before that completion theorem
applies. The four main theorem conclusions are unchanged.

The [source contract](research/case_study/phase177_F010_contract.json),
[root admission](research/case_study/phase193_root_admission.md) and
[current overlay](research/case_study/phase193_F010_overlay.json) record
one additional principal-source contract. This raises that source-library
count to **19**. The fixed editions of Modules A–D still cover sixteen
principal contracts; this separately reviewed application has not been
integrated into their measured or frozen editions.

The written application is 21,870 UTF-8 bytes. Its full public proof and
verification inventory is **42,343 bytes**, or **103,919** with all of U
charged. The local restriction-and-extension lemma is fully proved, so U
is a conceptual reference here; charging it in full is the conservative
project allocation. The [cost ledger](research/case_study/phase193_costs.json)
separates those files from review support. The source's thirteen pages
are not comparable to a byte count. **No matched compression ratio is
assigned.**

The [public replay](research/case_study/phase193_public_replay/report.json)
checks bounded examples of all three constructions and the exact hexagon
groups, freshly compiles the local Lean source, and rejects four altered
conditions. The [formal scope](research/case_study/formal/CompletedHexagonCounterexample.scope.md)
covers an explicit type-preserving reflection of order two and the absence
of a nontrivial involution in C3. The universal constructions remain
reviewed written mathematics, not end-to-end Lean proofs.

```sh
python3 -B -O research/case_study/phase193_public_check.py --output-dir /tmp/NEW-finite-pairs --packages PACKAGES --lean LEAN --gap GAP
```

The output directory must be new. Pinned Lean dependencies and GAP/GRAPE
are required; private primary PDFs and the unrelated L059 census are not.
