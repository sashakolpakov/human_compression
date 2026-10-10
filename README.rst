Human Compression
=================

Can reusable mathematics and capable language-model agents recover decades
of published results in shorter, complete papers? This project tests that
question through explicit proofs, attribution and measured comparisons.

Intake is closed. The fixed catalogue has 161 works, including 102 retrieved
full texts and 27 previously admitted recoveries of specified principal
results. These are different counts. The next stage audits and reorganizes
the existing mathematics.

Read the `audit protocol <audit/protocol.pdf>`_ and its
`TeX source <audit/protocol.tex>`_. The exact cutoff and the limited
work already in progress are recorded in `audit/intake.json <audit/intake.json>`_.

The first `full-manuscript complexity audit <audit/topic-e/measurement.pdf>`_
compares Topic E's two source papers with the complete shared theory and
two applications: **1.297 times** for written length. Including our required
program gives a **1.131 times** known-cost comparison; historical program
cost is unknown. The former 0.835 figure used selected proof passages.
The `graphs <audit/topic-e/costs.svg>`_,
`fixed protocol <audit/topic-e/protocol.json>`_ and
`independent review <audit/topic-e/independent_review.json>`_ make these
boundaries explicit. The third application is not included yet.

Mathematical papers
-------------------

The first ten complete proof texts have standalone, editable TeX sources
and PDFs. Their newly compiled PDFs have exactly the same extracted text
as their previously reviewed editions. Conversion is not a new proof audit.

* `Topic A <papers/topic-a>`_: supported kernels and two-power orders.
* `Topic E <papers/topic-e>`_: projective centralizers and the PSL/PGL
  polytope classifications.
* `Topic G <papers/topic-g>`_: flag relations and triangle geometries.
* `Separate question results <papers/questions>`_: finite rank-four
  covers, interval lifting, and the coprime obstruction.

The `paper catalogue <papers/catalogue.json>`_ binds these editions to their
sources. Other existing proofs and their dependencies still require the same
migration and audit. The complete source view is in
`audit/source_registry.json <audit/source_registry.json>`_.

There is one `canonical Lean library <research/case_study/formal>`_. Its
96 modules have different scopes: supporting lemmas do not certify entire
papers. The default build now includes every module. One legacy module uses
four explicitly recorded native-evaluation axioms; the others do not.

Build and check
---------------

Compile the papers directly from TeX, using XeLaTeX and the fonts named in
the sources::

    python3 scripts/build_papers.py --output-dir /tmp/human-compression-papers

Use a fresh output directory. Markdown and Pandoc are not build inputs.
For Lean, use the pinned toolchain and dependencies::

    cd research/case_study/formal
    lake build

The portable alternative checks every module against an existing pinned
package cache. Supply the compiler and package paths and use one worker::

    python3 scripts/check_lean.py --lean PATH_TO_LEAN --packages PATH_TO_PACKAGES --out /tmp/human-compression-lean --jobs 1

See ``python3 scripts/check_lean.py --help`` for the path arguments. For
file and archive integrity, from the repository root::

    python3 scripts/verify_snapshot.py

Working notes and the intake archive
-----------------------------------

Markdown stays in local working directories and is not tracked on the
current branch. The 992 previously published notes remain byte-for-byte
recoverable at tag ``intake-2026-10-11``, commit
``3b067cc2eba4ac2f2f91248448727639d8ac7c5a``. The new verifier reads these
bytes from Git objects, never from surviving local notes.

The historical ``research/case_study/phase*`` and ``provenance/phase*``
artifacts document earlier editions. Their original replay scripts require
the complete archived tree. Run a historical replay in a separate checkout::

    git worktree add --detach /tmp/human-compression-intake intake-2026-10-11
    cd /tmp/human-compression-intake
    python3 scripts/verify_snapshot.py

That checkout contains its historical Markdown. Current proofs, measurements
and formalization will develop in TeX, Lean and explicit JSON ledgers.

Compression is charged honestly: each topic pays for its full umbrella once,
then its applications, interfaces and required computations. Overlapping
umbrellas are charged separately in independent topic comparisons. Answers
to open questions have a separate ledger and do not inflate recovery counts.
