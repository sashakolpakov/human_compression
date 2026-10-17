Quartic girth-five graphs of diameter twenty-two
===============================================

This component proves n(4;5,22)=95 and supplies one graph attaining the
bound. It does not enumerate all minimum graphs or complete the other
claims of the cited paper. Read order95.tex and the companion premises/
notes for the mathematics. The original distance-layer and Moore-tree
framework is attributed to Cambie, Goedgebeur, Jooken and Van den Eede,
``On the order-diameter ratio of girth-diameter cages'', arXiv:2511.21144v3,
Table 5, physical page 22. The bibliographic/row record is in
data/girth_diameter_bounds/source.json.

What is checked
---------------

The portable program authenticates every declared component file, checks
the complete 84-pattern cover by 27 distinguished hole representatives,
reconstructs all 27 DIMACS formulas and primary-variable maps exactly,
compiles the unchanged acquired RUP checker, and checks all 27 retained
refutations. It also applies the unchanged accepted graph-property
predicate to the included 750-byte graph6 witness. The expected tuple is
[95,4,4,5,22,0]: order, minimum/maximum degree, girth, diameter and
bipartite indicator. The original graph is connected and nonbipartite.

The hand proofs establish that the formulas are necessary conditions
for the remaining local graph fragments and that their exclusions imply
the global lower bound. Those proofs remain explicit mathematical
premises: the script is not a proof-assistant formalization. The original
solver's UNSAT response is unnecessary. No SAT solver, graph generator,
enumeration checkpoint, private study directory or old platform binary
is used by the replay.

Reproduction from a checkout
----------------------------

Use ordinary Python 3.11 or newer, NetworkX 3.6.1, and a C++17 compiler
available as ``c++``. Python's standard library handles the formula and
manifest work. The compiler and NetworkX are explicit software premises;
their installations are not bundled as research artifacts. Install the
Python dependency in a separate environment, for example::

  python3 -m venv /absolute/external/venv
  /absolute/external/venv/bin/python -m pip install networkx==3.6.1

Obtain the expected manifest SHA256 from the independently accepted
publication record or trusted commit. The checker requires that external
value instead of accepting a modified manifest on its own authority.
From the repository root, first check metadata without writing output::

  python3 -E -B scripts/girth_diameter_bounds/check.py \
      --manifest-sha256 EXPECTED_SHA256 --metadata-only

Then select a fresh absolute output directory outside the checkout::

  python3 -E -B scripts/girth_diameter_bounds/check.py \
      --manifest-sha256 EXPECTED_SHA256 \
      --out /absolute/external/order95-check

The program stops on the first error and does not retry. It preserves any
output already produced. The compiler is allowed 60 seconds and each
saved-proof reader 110 seconds. A caller may impose tighter total runtime,
memory, output and disk-reserve guards; these subprocess deadlines alone
are not an operating-system resource sandbox. Successful output includes
one result.json with all 27 literal checker results and the positive
graph tuple. No PASS report is written after an incomplete child.

The exact compiler command is::

  c++ -std=c++17 -O2 \
      scripts/girth_diameter_bounds/vendor/f012/certificate_backends/rup/root_units_active.cpp \
      -o /absolute/external/order95-check/root_units_active

The vendor tree preserves the original relative source imports/includes.
Only the Boolean Formula primitives of the F012 source are used; its
unrelated graph builder is never called. The positive checker contains
the exact graph_properties function from reference_positive_check.py.
The entrypoint checks their complete syntax-tree equality before use and
never imports or executes that broad historical reference program.

Evidence boundary
-----------------

The canonical formula, proof, map, graph, source and hand-proof files are
bound by data/girth_diameter_bounds/manifest.json. Historical case files,
accepted results, terminal receipts and review records are retained under
data/girth_diameter_bounds/provenance. Their old absolute paths and old
proposal-status labels describe historical executions; the portable
checker never follows those paths. Current mathematical scope is stated
here and in order95.tex, and the exact accepted source-row disposition is
retained in provenance/order95_row_acceptance.json.

Rendering the manuscript is optional for numerical replay. Run pdflatex
with an external output directory if a PDF is desired. The retained
standalone TeX premise documents have their own preambles; they are
separate readable proofs, not inputs to order95.tex. No rendered files,
compiler objects or temporary logs are canonical inputs.

Independent portable-interface review and the actual replay belong to the
publication records. Publication of this component does not turn the
superseded partial enumeration into a complete census. Historical search
material must not be discarded merely because a local package exists:
any cleanup requires a separately checked published replacement and an
exact retained-evidence and restoration boundary.
