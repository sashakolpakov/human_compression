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
proof edition from ten preserved baseline TeX papers. Other topic proofs
remain available in the archive and are material for further common
arguments, not claims of completed compression. The fixed source view is
in `audit/source_registry.json <audit/source_registry.json>`_.

The `completion audit <audit/completion.rst>`_ maps all 27 admitted principal
result sets to their proofs and remaining manuscript work. Its resolved
contracts use later admissions where older registry fields are stale.
Intake remains closed. A new supporting paper on
`normal kernel recognition <papers/formal/normal-kernel-recognition.pdf>`_
replaces two separate finite-order comparisons by one group-theoretic
argument. The full Topic A volume and its measurement are still in preparation.

The complete `finite program <papers/topic-e/v2/required_finite.g>`_ checks
432 local markings, the six local presentations, all ten universal groups,
their required geometry and the literal correction witnesses. The
`validation program <papers/topic-e/v2/validation.g>`_ and five mutation
controls are separate. GAP's group algorithms remain an explicit trust
boundary; uniform infinite-family claims have written proofs.

The `canonical Lean library <research/case_study/formal>`_ has 99 modules.
The new `extension proofs <papers/formal/marked-involution-extension.pdf>`_
verify nine generic declarations about actual marked tuples, their string
relations and generation. They do not formalize the entire projective
classification. Two further modules prove normal-kernel recognition and
construct the explicit direct-product isomorphism, with fourteen declaration
reports. They do not formalize the applications' source presentations or
geometric conclusions. Build evidence combines the prior fresh run of 96
unchanged modules with the separately checked extension module and the two
kernel modules; every module is in the default build. One unchanged legacy
module uses four recorded native-evaluation axioms. The precise scopes are
in the `extension audit <audit/lean_extension.json>`_ and
`kernel audit <audit/normal-kernels/admission.json>`_.

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

Replay the current finite certificate and its mutation controls::

    python3 papers/topic-e/v2/check_common.py --out /tmp/human-compression-finite

Recount the fixed measurement with pypdf 6.13.0 and separately supplied
primary PDFs (their exact paths and hashes are in the protocol)::

    python3 audit/topic-e/v2/measure.py --repo . --sources-root PRIMARY_ROOT --protocol audit/topic-e/v2/protocol.json --out /tmp/human-compression-measurement.json
    python3 audit/topic-e/v2/recount.py --repo . --sources-root PRIMARY_ROOT --out /tmp/human-compression-independent.json

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
