Graphs of degree five and diameter eight
=======================================

These working proof notes support the unfinished F009 census treatment.
They start with the neighborhoods of three vertices on a geodesic of
length eight. Their union is an independent set of fifteen vertices;
the remaining induced graph has five edges. Degree counts and incidence
matrices then give the following conditional results.

* ``single_middle.tex`` proves that a single middle vertex must be
  isolated in the remaining induced graph. It needs only the fixed
  geodesic. Its final corollary gives sufficient conditions for a partial
  family to have no completion.
* ``side_incidence.tex`` describes every graph whose middle consists of
  exactly two isolated vertices. It gives the five possible side shapes,
  the integer attachment conditions, and an ordinary isomorphism test.
* ``three_isolated_middle.tex`` classifies the case of exactly three
  isolated middle vertices: precisely two ordinary graph classes occur.
  ``three_middle_templates.json`` records their weighted construction.

The manuscripts define “middle” and all additional hypotheses explicitly.
Each has a separate mathematical review in ``reviews/``. ``MANIFEST.json``
binds the reviewed sources, published files and reviews. Editorial changes
cover the titles, author lines and one publication-status paragraph. Every
definition, theorem statement and proof is preserved; the recorded changes
recover every byte of the reviewed sources.

The original problem and reported census belong to Cambie, Goedgebeur,
Jooken and Van den Eede, *On the order-diameter ratio of girth-diameter
cages*, arXiv:2511.21144v3, Appendix B, Table 6. The notes attribute their
earlier neighborhood reductions and standard graph methods. Their present
contribution is the stated collection of conditional deductions.

F009 remains unfinished. Applying these results requires certificates
that the actual pending families satisfy their hypotheses, together with
the required ordinary isomorphism and coverage checks. This publication
adds no completed original, solved open conjecture or measured compression
credit. Lean formalization remains outstanding.

The TeX files are standalone documents. Rendering them requires a TeX
installation with amsmath, amsthm, hyperref and booktabs. Keep the compiler
output in a separate directory. The historical paths in the review
records document provenance; the manuscripts have no private file imports.
