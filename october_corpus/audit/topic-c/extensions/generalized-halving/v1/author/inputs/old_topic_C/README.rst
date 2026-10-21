Topic C: chamber operations and binary translations
===================================================

This private author edition contains one complete common paper, four complete
applications and a full appendix containing both required Janko programs.
The closed source boundary is L088, N013, L108 and F014.  ``scope.json`` maps
all 35 previously accepted clauses of the first three sources and the five
accepted F014 clauses.  Exclusions and source corrections are preserved.
Independent acceptance of this edition is separate from its author freeze.

The mathematical change is an explicit inverse for the binary translation
presentation.  The graph-generation theorem is used both for generalized
cubes and for polyhedra with equal adjacent parameters.  The latter proof
no longer uses an order sandwich to identify the universal presentation.
The old displacement commutativity argument remains attributed to its
source.  The geometric operation proofs are included in full at this topic's
cost, using previously reviewed arguments.  No historical priority, new
source credit, new question credit or measured compression factor is claimed.

L108's original PDF is unavailable, so its original-manuscript cost remains
unknown.  The Ens notation adapter retains only the prior selected web
reading; no locally acquired Ens primary is implied.  The separate refutation
of F014 Conjecture 3.7 is outside this principal-construction volume.

Reproduction
------------

The ordinary checker verifies the immutable author bindings, all clause and
proof locators, and complete program inclusion in the PDF appendix.  Python
requires ``pypdf``.  Use a fresh output directory::

  python -B -O check.py --out /fresh/output

To check the exact private source and prior-admission bytes, also give
``--study-root`` and ``--public-root``.  The primary PDFs are not redistributed.
To compile all six TeX documents, append ``--render --xelatex /path/to/xelatex``.
The documents require STIXGeneral, STIX Two Math, Menlo and ordinary TeX
packages listed in ``preamble.tex``.  The checker compares every newly rendered
page's extracted text with the frozen PDF; PDF timestamps need not match.

The scoped Lean compilation is separate::

  python -B -O formal/check.py --out /fresh/formal-output \
    --lean /path/to/lean --packages /path/to/pinned/packages

It checks nine new generic inverse declarations and seven unchanged
previous declarations.  It rebuilds missing pinned dependencies in a private
overlay; other pinned compiled objects remain trusted.  It does not formalize
the augmentation basis, source instances, geometric conclusions or Janko
census.  Five concrete finite countermodels check that omitted hypotheses
cannot simply be discarded.

The complete finite classification replay is explicitly optional in the
ordinary binding checker and is run independently by::

  python -B -O programs/phase150_module_C_run.py \
    --output-dir /fresh/janko-output --gap /path/to/gap

This runs both unchanged programs and records GAP/TomLib versions, the actual
Janko data hash, the full construction checks and exhaustive extension census.
Reading a saved record is not described as rerunning that census.

``controls.py --out /fresh/controls.json`` exercises eight boundary and
required-cost mutations.  Operational checkers, formal sources and reports are
inventoried independently of the two required mathematical GAP programs.
