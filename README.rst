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

Common proofs for finite two-groups
----------------------------------

The `common theory <papers/topic-a/v2/umbrella.pdf>`_ proves how separately
supported kernels determine marked subgroup intersections, how to recognize
the resulting presentations, and how a finite quotient bounds a search
through normal kernels. Six complete applications recover the following
principal result sets. Their proofs, retained inputs and corrections have
passed independent mathematical and source review.

.. list-table:: Six source manuscripts and the results recovered
   :header-rows: 1
   :widths: 34 44 22

   * - Source, authors and edition
     - Declared principal results
     - Our application
   * - L032: Hou–Feng–Leemans, *On regular polytopes of 2-power order*;
       revised author manuscript, 8 November 2019
     - Theorem 1.2 for every stated rank, type and order, with the necessary bound
     - `Prescribed orders <papers/topic-a/v2/two-power-orders.pdf>`_
   * - L034: Hou–Feng–Leemans, *Existence of regular 3-hypertopes with 2^n
       chambers*; arXiv:1901.09034v1
     - Lemma 3.1 and Theorem 3.2: presentation, order, structure and geometry;
       explicit corrections
     - `Three-generator hypertopes <papers/topic-a/v2/three-generator-hypertopes.pdf>`_
   * - F016: Cunningham–Feng–Hou–Schulte, *Symmetric polytopes whose
       automorphism groups are 2-groups*; arXiv:2512.15511v1
     - Square classification, section assemblies, presentations and three
       free extensions; stated geometric inputs retained
     - `Square sections and extensions <papers/topic-a/v2/square-sections-and-free-extensions.pdf>`_
   * - F013: Hou–Schulte, *String C-groups of 2-power order project onto a
       common string C-group*; arXiv:2605.20691v1
     - Both principal common-quotient and covering theorems in all ranks;
       auxiliary correction kept separate
     - `Common quotients <papers/topic-a/v2/common-two-group-quotient.pdf>`_
   * - L035: Hou–Feng–Leemans, *Existence of regular 3-polytopes of order
       2^n*; arXiv:1802.08947v2
     - Theorems 1.2–1.3: full existence range and all three high-type
       classifications, with converse and finite seed checks
     - `High-type classifications <papers/topic-a/v2/high-type-two-groups.pdf>`_
   * - N009: Gomi–Loyola–De Las Peñas, *String C-groups of order 1024*;
       Contributions to Discrete Mathematics 13(1) (2018), 1–22
     - Nondegenerate marked classification, all six source tables and
       finite universal orders; explicit literal corrections
     - `Markings of order 1024 <papers/topic-a/v2/order-1024-markings.pdf>`_

The `scope reader <audit/topic-a/v2/SCOPE.rst>`_ states the exact coverage,
exclusions, attribution and formal limits. The `proof admission
<audit/topic-a/v2/admission.json>`_ binds the accepted edition and its
independent reviews. These six existing contracts add no new manuscript
or solved-question credits. The original classifications and constructions
retain their authors' attribution.

The common paper is 17 pages and the six applications total 33 pages.
The `complete computation appendix <papers/topic-a/v2/two-group-computation.pdf>`_
is another 21 pages; all four executable files are in
`required-code <papers/topic-a/v2/required-code>`_. An independent replay
checked the exhaustive census and presentations against all 107 comparison
rows. GAP's exact group algorithms remain an explicit trust boundary.

The `three-page length audit <audit/topic-a/v2/measurement/reader/measurement.pdf>`_ gives
**1.535 times** for the complete written topic and **1.083 times** including
the whole required program. The six source manuscripts total 195,379
characters. Our full theory costs 49,059 and the six applications cost
78,251: together, 127,310. The complete program appendix adds 53,035,
bringing the denominator to 180,345.

.. list-table:: Each application after acquiring the common theory and program
   :header-rows: 1

   * - Source
     - Source characters
     - Application characters
     - Conditional factor
   * - L032
     - 16,558
     - 8,212
     - 2.016
   * - L034
     - 21,433
     - 5,784
     - 3.706
   * - F016
     - 43,983
     - 15,419
     - 2.853
   * - F013
     - 25,562
     - 6,224
     - 4.107
   * - L035
     - 51,019
     - 14,498
     - 3.519
   * - N009
     - 36,824
     - 28,114
     - 1.310

These use NFC non-whitespace characters in complete-document extracted
PDF text, with exact running furniture excluded. Titles, abstracts and
references remain included. The conditional factors assume the **whole
common theory and complete program** have already been acquired; those
costs remain in the whole-topic comparison.

Source diagrams and some image labels, particularly in L035, are absent
from text extraction. Their costs remain unknown, as do unmeasured outside
proofs and historical programs. These are comparisons of known text costs,
not measurements of all visible content or minimum mathematical complexity.
The `complete numerical ledger <audit/topic-a/v2/measurement/results.json>`_
retains five units, two normalizations and the raw extraction sensitivities.
The `cost graph <audit/topic-a/v2/measurement/reader/costs.svg>`_ shows the
common acquisition followed by all six applications. The `numerical admission
<audit/topic-a/v2/measurement/admission.json>`_ records the independent
recount and exact fraction checks.

The `paired proof graph <audit/topic-a/v2/dag/default_view.svg>`_ shows
the historical arguments and their replacements. Download and open the
`interactive explorer <audit/topic-a/v2/dag/explorer.html>`_ to select any
of the six comparisons, expand a theorem's proof, and inspect its costs,
prerequisites and source references. It works without a network connection;
proof links resolve when it is opened within a repository checkout.

The audit assigns every counted passage to one owner: 341 spans across
14 documents. The 236 argument and reference nodes can share these owners,
so their displayed costs must not be added together. Totals count each
passage once, including the complete program appendix. The `graph review
<audit/topic-a/v2/dag_admission.json>`_ records the independent checks and
the remaining limits, including unknown external costs. Static SVG rendering
and interface checks pass; actual browser layout has not been certified.

Common proofs for projective groups
----------------------------------

The `current common theory <papers/topic-e/v2/umbrella.pdf>`_ proves a
classification of string markings with two proper exceptional end groups.
It derives the intersection property rather than assuming it. A common
centralizer argument and one finite quotient theorem now supply the
classification steps for three applications. Their complete statements,
proofs, borrowed inputs and source corrections are in editable TeX beside
the PDFs.

.. list-table:: Three source manuscripts and the results recovered
   :header-rows: 1
   :widths: 34 44 22

   * - Source and authors
     - Declared principal results
     - Our application
   * - L083: Leemans–Schulte, *Groups of type L2(q) acting on polytopes*
     - PSL classification, complete universal table and stated 11-cell/57-cell geometry
     - `PSL polytopes <papers/topic-e/v2/psl-polytopes.pdf>`_
   * - L079: Leemans–Schulte, *Polytopes with groups of type PGL2(q)*
     - Theorem 10: the unique rank-at-least-four case is the 4-simplex
     - `PGL polytopes <papers/topic-e/v2/pgl-polytopes.pdf>`_
   * - L021: Leemans–Toledo, *Maniplexes with automorphism group PSL(2,q)*
     - Rank and end-group restrictions, extension and infinite constructions; explicit corrections
     - `Projective maniplexes <papers/topic-e/v2/projective-maniplexes.pdf>`_

These contracts do not include every auxiliary assertion. In particular,
L079's semilinear census and the separate PGL conjectures are outside this
comparison. Exact editions, exceptions and retained classical inputs are
bound in the `proof admission <audit/topic-e/v2/admission.json>`_ and
`independent mathematical review <audit/topic-e/v2/independent_proof_review.json>`_.
The prior finite presentations and classifications retain their original
attribution. No historical priority or new solved-question claim is added.

The `three-source measurement <audit/topic-e/v2/measurement.pdf>`_ uses
complete manuscript lengths, measured in normalized non-whitespace
characters:

.. list-table:: Complete topic and conditional application costs
   :header-rows: 1

   * - Comparison
     - Factor
   * - All three source manuscripts / common theory plus all three applications
     - 1.816
   * - Same comparison including our full required finite program
     - 1.523
   * - Also include the complete diagnostic program
     - 1.372
   * - L083 / its application, after acquiring the common theory and program
     - 6.957
   * - L079 / its application, on the same basis
     - 11.271
   * - L021 / its application, on the same basis
     - 2.018

The two headline measures are the whole topic and each application after
acquiring the common theory. Required program costs are shown alongside
them.

The full written denominator is 39,303 characters: the common theory costs
19,790, followed by applications of 3,002, 1,855 and 14,656. The required
program adds 7,565 and diagnostics add 5,173. All three source manuscripts
total 71,375. Our previous proofs of these same results occupied 53,895
written characters; the new proofs remove 14,592. Including diagnostics,
the combined code is slightly longer than before. The gain therefore does
not come from discarding diagnostic code.

The earlier edition at commit ``6d203fd`` gave 1.851 overall. Clearer
explanation adds 735 characters in the current edition, charged under the
same rule. The mathematical results and programs are unchanged.

These are costs of concrete complete proofs under the stated source
contracts, not estimates of minimum mathematical complexity. Historical
program costs and external library proof costs remain unknown. The two
program-inclusive factors are known-cost comparisons. All ten length
coordinates, the fixed boundary and an independent recount are retained.
The `cost graphs <audit/topic-e/v2/costs.svg>`_ show the acquisition and
application stages; `summary.json <audit/topic-e/v2/summary.json>`_ records
the two headline measures.
The earlier `two-source audit <audit/topic-e/measurement.pdf>`_ is a
baseline of the older proofs, not the current result or a limit on what
further common ideas could achieve.

The `paired dependency graphs <audit/topic-e/v2/dag/default_view.svg>`_
show which arguments supply each result. Download and open the
`interactive explorer <audit/topic-e/v2/dag/explorer.html>`_ to switch
between historical and new proofs, inspect individual costs and expand
the branches inside a theorem. It works locally without a network connection.

Every text span has one cost owner. A theorem box sums its branches without
charging them again, and the complete manuscript totals include context
and references. Historical assertions retain their recorded qualifications.
Raw node counts alone are not complexity ratios. Separate topic umbrellas
are each charged in full even when they overlap. The exact accounting and
its limits are in the `graph review <audit/topic-e/v2/dag_admission.json>`_
and the `audit protocol <audit/protocol.pdf>`_.

Papers and verification
-----------------------

The `paper catalogue <papers/catalogue.json>`_ distinguishes the new common
proof editions from ten preserved baseline TeX papers. Other topic proofs
remain available in the archive and are material for further common
arguments, not claims of completed compression. The fixed source view is
in `audit/source_registry.json <audit/source_registry.json>`_.

The `completion audit <audit/completion.rst>`_ maps all 27 admitted principal
result sets to their proofs and remaining manuscript work. Its resolved
contracts use later admissions where older registry fields are stale.
Intake remains closed. A new supporting paper on
`normal kernel recognition <papers/formal/normal-kernel-recognition.pdf>`_
replaces two separate finite-order comparisons by one group-theoretic
argument. These lemmas now serve the complete Topic A applications; their
source-specific hypotheses are checked in the written proofs.

The complete `finite program <papers/topic-e/v2/required_finite.g>`_ checks
432 local markings, the six local presentations, all ten universal groups,
their required geometry and the literal correction witnesses. The
`validation program <papers/topic-e/v2/validation.g>`_ and five mutation
controls are separate. GAP's group algorithms remain an explicit trust
boundary; uniform infinite-family claims have written proofs.

The `canonical Lean library <research/case_study/formal>`_ has 100 modules.
The new `extension proofs <papers/formal/marked-involution-extension.pdf>`_
verify nine generic declarations about actual marked tuples, their string
relations and generation. They do not formalize the entire projective
classification. Two further modules prove normal-kernel recognition and
construct the explicit direct-product isomorphism, with fourteen declaration
reports. They do not formalize the applications' source presentations or
geometric conclusions. Build evidence combines the prior fresh run of 96
unchanged modules with the separately checked extension module and the two
kernel modules, followed by the separately checked commuting-retraction
module; every module is in the default build. One unchanged legacy
module uses four recorded native-evaluation axioms. The precise scopes are
in the `extension audit <audit/lean_extension.json>`_,
`kernel audit <audit/normal-kernels/admission.json>`_ and
`commuting-retraction audit <audit/commuting-retractions/admission.json>`_.
The last module proves the compatible-pair inverse for two commuting
retractions, with four checked definitions and seven checked theorems.
Application-specific deletion maps and their joint faithfulness remain
written obligations.

Build and check
---------------

Compile the papers directly from TeX, using XeLaTeX and the fonts named in
the sources::

    python3 scripts/build_papers.py --output-dir /tmp/human-compression-papers

Use a fresh output directory. Markdown and Pandoc are not build inputs.
To build particular documents, repeat ``--paper`` with their exact IDs
from ``papers/catalogue.json`` (or ``audit/protocol``). Shared TeX inputs
must be listed explicitly in the catalogue's ``tex_inputs`` field and
bound in the same proof review. The builder copies only those sources
and records their hashes; a whole source directory is never copied.
The `build review <audit/tex-build/tex_inputs_design_review.rst>`_ records
the checks and the external TeX dependency boundary.

For Lean, use the pinned toolchain and dependencies::

    cd research/case_study/formal
    lake build

The portable alternative checks every module against an existing pinned
package cache. Supply the compiler and package paths and use one worker::

    python3 scripts/check_lean.py --lean PATH_TO_LEAN --packages PATH_TO_PACKAGES --out /tmp/human-compression-lean --jobs 1

See ``python3 scripts/check_lean.py --help`` for the path arguments. For
file and archive integrity, from the repository root::

    python3 scripts/verify_snapshot.py

Replay the current finite certificate and its mutation controls::

    python3 papers/topic-e/v2/check_common.py --out /tmp/human-compression-finite

Recount the fixed measurement with pypdf 6.13.0 and separately supplied
primary PDFs (their exact paths and hashes are in the protocol)::

    python3 audit/topic-e/v2/measure.py --repo . --sources-root PRIMARY_ROOT --protocol audit/topic-e/v2/protocol.json --out /tmp/human-compression-measurement.json
    python3 audit/topic-e/v2/recount.py --repo . --sources-root PRIMARY_ROOT --out /tmp/human-compression-independent.json

Recount Topic A with the same pypdf version and its separately supplied
primary PDFs::

    python3 -B -O audit/topic-a/v2/measurement/recount.py --sources-root PRIMARY_ROOT --public-root . --out /tmp/human-compression-topic-a-counts

To rebuild its measurement reader and cost graph, use the dependencies
listed in the reader manifest and a fresh output directory::

    python3 -B -O audit/topic-a/v2/measurement/reader/build_reader.py --author-pdf audit/topic-a/v2/measurement/reader/measurement.pdf --out /tmp/human-compression-topic-a-reader

Replay Topic A's proof-cost partition against the same primary PDFs and
the current published manuscripts::

    python3 -B -O audit/topic-a/v2/dag/check.py --sources-root PRIMARY_ROOT --artifacts-root . --out /tmp/human-compression-topic-a-dag

The `graph instructions <audit/topic-a/v2/dag/README.rst>`_ also describe
how to regenerate the explorer and check its controls without the primary PDFs.

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
