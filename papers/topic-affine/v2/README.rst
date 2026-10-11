Affine groups and period quotients
=================================

This author edition presents one existing corrected principal source contract:
Hou, Feng and Leemans, Regular 3-polytopes of order 2^n p, arXiv:2001.02945v2,
14 July 2024. It preserves all 33 detailed rows of the admitted ledger and does
not change the project's 27 principal contracts. Independent review is required
before public adoption. No new source, question or numerical compression claim
is made.

Read ``umbrella.pdf`` and ``mixed-prime-polyhedra.pdf`` in that order. The full
six required programs are printed in ``required-programs.pdf``. ``scope.json``
binds the source edition, retained theorems, all old rows and current proof
regions; ``lineage.json`` identifies reused proof material and identical program
bytes. All used supported-kernel and square proofs are included in this topic,
not treated as free imports from Topic A. The original programs' cost is unknown.

Reproduction
------------

Use Python with pypdf and SymPy, GAP with SmallGroups 1.5.4, Lean 4.32.2 and the
exact packages in ``formal/dependency_manifest.json``. The proof programs use
exact integer/group computations. The legacy Python program contains assertions;
the driver explicitly enables them, ignoring inherited PYTHONOPTIMIZE. XeLaTeX
with the declared fonts is required only for ``--render``.

From this directory, run::

  python -B -O check.py --out /fresh/output/path \
    --gap /path/to/gap --lean /path/to/lean \
    --packages /path/to/pinned/packages \
    --sources-root /path/to/private/study --render

The output path must not already exist. The optional source root verifies the
six exact previously acquired primary artifacts listed in scope.json. Those
copyrighted PDFs are not redistributed; omitting this option does not verify
their bytes. The rest of the packet is self-contained. ``--xelatex`` overrides
the default /opt/homebrew/bin/xelatex path when necessary.

Verification limits
-------------------

Nine Lean declarations cover seven reused quotient/sign lemmas and two generic
statements about smaller normal periods. They do not formalize the affine
coordinates, lattice bases, Reidemeister--Schreier/Tietze algorithms, SmallGroups
catalogue or the complete geometric classification. Exact finite executions
support these written proofs; no finite sample is substituted for their uniform
arguments. Burnside, Lucchini's stated proposition and the regular-polytope
correspondence are retained and attributed at their points of use.

The fixed arXiv edition's literal period-sign defect is kept distinct from the
corrected presentation. The broader Problem 1.1, a complete independent census
for Table 1, and ancillary uniqueness assertions about the order-384 seeds are
outside the already admitted principal boundary. The known equal-label answer
is proved and attributed, with no new question credit.
