Topic D proof dependencies
==========================

This is a logical graph proposal for the three already accepted Topic D
contracts, awaiting independent semantic review. It preserves all 37 source
rows, 19 accepted proof contexts, the exact published edition, five required
programs, three diagnostics and two execution drivers. There are no weights,
exclusive cost partitions, ratios or new result credits.

``reader.pdf`` explains the shared arguments, local obligations and exclusions.
``logical_graph.json`` records actual typed prerequisites and exact locators.
``coverage.json`` maps each unchanged source record to historical outputs,
current proved outputs, retained inputs and qualification context separately.
The historical graph documents assertions used by the source; it does not
retroactively validate a faulty proof. Comparison and attribution arrows are
not unpriced proof dependencies on the old manuscript.

Both original and later scoped Lean layers are evidence only. The later 28
reports already include the first 12; they are not 12 plus 28 independent
results. The source-specific field, generation, geometry and catalogue
obligations remain explicit.

Supply the exact primary PDFs and their existing private page extractions
locally under ``--study-root``; they are not exports. The public proof edition
is supplied under ``--public-root``. Run::

  python -B -O check.py --study-root /path/to/private/study \
    --public-root /path/to/human_compression --out /fresh/report.json

To reproduce the graph construction in a fresh directory::

  python -B build.py --study-root /path/to/private/study \
    --public-root /path/to/human_compression --out /fresh/graph

The numerical measurement protocol is a separate packet. This graph neither
imports its counts nor derives a factor from the number of nodes. External
proofs, catalogue construction and graphics are unknown costs, not zero.
