One command for the configured Lean proofs
=========================================

This runner calls the two existing checkers without changing their mathematical
sources or their checks. By default it runs the canonical library checker and
then the separate Topic B checker. At the bound publication edition these
contain 100 and 1 Lean sources, respectively. Lake's default library remains
the original 100 modules.

From a checkout, with this script either in the checkout or supplied by its
absolute path::

  python3 -B check_project_lean.py \
    --lean /path/to/pinned/lean \
    --packages /path/to/pinned/lake/packages \
    --out /fresh/directory/outside/the/checkout \
    --jobs 2

Pass ``--repo /path/to/human_compression`` when the checkout cannot be found
from the working directory or the script's ancestors. The compiler and package
arguments are shared by both child commands. The legacy checker receives
``--jobs``; Topic B runs serially. The two components run sequentially, keeping
the worker limit explicit. Existing child timeouts remain unchanged.

An intentional partial check is explicit::

  python3 -B check_project_lean.py \
    --repo /path/to/human_compression \
    --lean /path/to/pinned/lean \
    --packages /path/to/pinned/lake/packages \
    --out /fresh/topic-b-check \
    --jobs 2 --components topic-b

``--components legacy`` checks only the canonical library. ``all`` is the
default and must occur alone; explicitly selecting both named components also
checks both. The output must not already exist, even as a dangling symlink,
and must be outside the checkout and the runner packet.

Reports and scope
-----------------

The aggregate ``report.json`` distinguishes the inventoried source set from
the sources checked by this invocation. Each child report remains unchanged
in ``legacy/report.json`` or ``topic-b/report.json``. Child stdout and stderr
are preserved separately. Reports bind the exact checker, Lean source,
dependency-manifest and supporting input hashes. A source change, mismatched
report, missing report, failed process or failed component stops the run.
An earlier passing report is never substituted for a new execution.

``PASS_FULL_CONFIGURED_PROJECT`` means both configured checkers passed afresh.
``PASS_PARTIAL`` means only the explicitly selected components passed. Failure
never acquires the full label, even if a child wrote a purported passing report
before exiting unsuccessfully. Components that passed before a later failure
remain identified as such. Reported declaration counts are printed axiom
reports, not claims about distinct new theorems.

The underlying checkers are ``scripts/check_lean.py`` and
``papers/topic-b/v2/check.py``. Their trust boundaries remain: the pinned Lean
compiler and cached external objects are trusted. The canonical library keeps
its explicitly allowed historical native-evaluation exception; this wrapper
does not describe all legacy reports as standard-axiom-only. Topic B checks six
standard-axiom subgroup-induction declarations and its hypothesis controls.
Its incidence geometry and source applications remain written mathematics.

This command does not discover or certify every archived experimental Lean
file in the repository. It covers the two configured, admitted source sets.
It does not rerender papers, retrieve primary texts, or verify all written
proofs. There is no new theorem, source credit, or change to the canonical
Lake file. No mathematical source is duplicated in this distribution. The
unchanged child checkers create their normal fresh build copies in the output.

Validation of this new runner
-----------------------------

The bundled fixture test can be rerun without Lean or external packages::

  python3 -B test_dispatch.py --out /fresh/fixture-output

Its 14 bounded cases use synthetic child checkers. They test dispatch, jobs
and environment forwarding, exact source coverage, failure propagation,
fresh-output rules and truthful partial labels. They are orchestration tests,
not mathematical certificates.

The archived real run selected only Topic B: one fresh source, six declaration
reports, three rejected weakened hypotheses, and one rejected altered finite
countermodel. All 100 canonical sources are explicitly unselected in that
report. No all-101-source compilation was performed to validate this wrapper.
The default command makes that full fresh run available for the subsequent
independent review; it does not claim the result in advance.

Only reports and logs are archived here. The runner creates no output inside
the paper packets and does not edit the existing checker, source, saved-report
or Lake files.
