A bipartite graph with a nonsplit action on its parts
===================================================

Private author packet. No public mutation or source-wide admission is made.
Read graph.pdf/graph.tex, then scope.json and certificate.json.

The complete finite construction is graph.json. Its two permutation image
lists and all 896 adjacency lists are literal data, not a search transcript.
Run the REQUIRED elementary certificate from an exported copy::

    python3 -B -O check.py --out /fresh/certificate.json

The optional graph-library cross-check is separate::

    python3 -B -O diagnostic.py --gap /opt/homebrew/bin/gap --out /fresh/diagnostic.json

The elementary proof of full automorphism-group size uses a discrete
neighbour-colour refinement from one ordered star and an explicit subgroup
attaining 896 * 3! = 5376. It does not trust graph-isomorphism software.
The part-preserving subgroup has order2688 and is transitive on all1344
edges. Its other coset has 1024 elements of order4,896 of order12,768 of
order28. These are exhaustive counts, not sampled elements.

The construction is intended as an input to a separate thin rank-three
incidence-geometry argument for L126. This packet proves the graph assertion
only. No claim of historical novelty, source completion, compression factor,
or Lean formalization is made. Both whole required files remain costable;
optional validation is inventoried separately.

The search used GAP/GRAPE and a three-dimensional binary dual-homology
submodule of a112-vertex cubic graph. None of this exploratory search is
required to replay the fixed final graph. Earlier108-vertex half-arc examples
failed part-preserving edge transitivity and are explicitly NOT witnesses.

XeLaTeX builds graph.tex. All three final pages were visually inspected;
render.json records the exact binding and diagnostics.
