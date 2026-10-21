Reproducing the published material
=================================

This guide distinguishes snapshot integrity, selected mathematical checks,
paper rendering and formal compilation.  Passing one does not establish all
the others.  Paths below are relative to the public repository root.  Begin
with ``README.rst``, the selected topic's current guide and source map, and
its admission and distinct review; these define the claim being reproduced.

Obtain the history as well as the files
--------------------------------------

Use a full-history Git clone, without ``--depth`` or ``--single-branch``::

    git clone https://github.com/sashakolpakov/human_compression.git
    cd human_compression
    git fetch origin --tags
    git rev-parse HEAD
    git rev-parse --is-shallow-repository
    git status --short

The shallow-repository answer should be ``false``.  Record the commit you
check.  A ZIP download lacks the required Git objects; a shallow clone can
also lack them.  The archive uses commit-addressed ``git cat-file`` reads,
and registration checks use Git ancestry and diffs.  For example,
``audit/intake.json`` retains tag ``intake-2026-10-11`` and baseline commit
``3b067cc2eba4ac2f2f91248448727639d8ac7c5a``.  Preserve referenced archive
objects and tags.  If a checker reports a missing object, acquire the
required history rather than bypassing that check.

Start with the small checks
--------------------------

Use ordinary Python 3.10 or newer, without optimization.  These entry points
use the Python standard library; the snapshot verifier also invokes Git::

    python3 -E -B scripts/verify_snapshot.py
    python3 -E -B scripts/smoke_check.py --quick --keep-work-dir --timeout 600

The snapshot command checks the current registration and its acquired
predecessor evidence.  It is not a fresh replay of every historical proof,
census or payload.  The quick suite runs three selected checks: torsor
matrices, Suzuki polynomial identities and eleven finite-field witnesses.
It copies inputs to a new temporary directory, checks that protected
snapshot files remain unchanged, and prints the location of fresh reports
and logs.  ``--keep-work-dir`` preserves that directory; a successful run
without it removes its scratch output.  The timeout is per child checker.

Other explicitly selected suites are::

    python3 -E -B scripts/smoke_check.py --older --keep-work-dir --timeout 600
    python3 -E -B scripts/smoke_check.py --full --keep-work-dir --timeout 600

``--older`` uses the standard library for the two 2003/2004 reductions.
``--full`` adds NumPy-dependent cocycle checks and exact graph-construction
checks to the quick suite.  Here “full” names that five-check suite, not a
complete project replay.  Install its dependencies in the chosen Python
environment before invoking it; there is no repository-wide Python lockfile
or fully specified clean-machine environment recipe.

Co2 orbit exclusions
--------------------

The `conditional Co2 component <../papers/sporadic_rank3/co2_nonfree.rst>`_
uses ordinary Python 3.11 or newer and the standard library. Its 52 declared
files contain the proof, normalized orbit data, provenance and checker.
This particular check needs no Git history, native group program or build.
The `admission <../audit/sporadic_rank3/co2_nonfree/admission.json>`_ records
its exact manifest and validation scope.

From the checkout root, select a fresh absolute output directory outside the
checkout, with an existing parent::

    python3 -E -B scripts/sporadic_rank3/check_co2_nonfree.py \
      --manifest-sha256 1f603a4d21c25ea7761d61eeb002d0fc91141d6e502d1feaba5b286852daff32 \
      --out /absolute/external/co2-nonfree-check

Success regenerates all 3,627 nonfree row keys and their canonical digest,
checks all 24,690 rows and leaves 21,063 full-size rows undecided. The
identification of the named group, its centralizers and the complete orbit
partition remain imported premises. This partial certificate does not
complete L026. Generated output belongs outside the checkout.

Paper and topic replay
----------------------

Create a fresh output child outside the checkout; do not overwrite an
archived report or native build::

    repro_scratch=$(mktemp -d "${TMPDIR:-/tmp}/human-compression-repro.XXXXXX")
    python3 -E -B scripts/build_papers.py --paper audit/protocol \
      --output-dir "$repro_scratch/papers" --jobs 1

Select other exact IDs from ``papers/catalogue.json`` with repeated
``--paper`` options.  The builder stages the declared TeX inputs and uses
XeLaTeX by default, or pdfLaTeX when the catalogue specifies it.  Rendering
does not constitute a new mathematical review or length measurement.

Dependencies and replay scope vary by packet.  Concrete retained examples:

* Topic A v3: ``papers/topic-a/v3/README.rst`` separates Python/pypdf and
  XeLaTeX/STIX rendering from the A5/A6 replay requiring an explicit GAP
  executable.  Its retained GAP/NQ and catalogue premises are not installed
  merely by cloning this repository.
* Topic B v2: ``papers/topic-b/v2/README.rst`` requires the pinned Lean
  compiler and package cache; optional rendering also needs pypdf and
  XeLaTeX.  Its written geometry is outside the formal module's scope.
* L027 and L120: their ``papers/recoveries/<ID>/v1/PUBLICATION.rst`` guides
  give portable commands with exact transport, policy and adapter hashes.
  These use ordinary Python, pypdf, pdfLaTeX and Ghostscript.  They restore
  and check retained evidence without repeating the completed group censuses.
  In L027's replay, retained GAP package sources are data, not a required
  implicit system installation.
* L070: ``papers/recoveries/L070/v1/PUBLICATION.rst`` routes its exact
  admission-proposal command and transport pins.  Python/pypdf checks
  selected retained inputs; optional rendering needs TeX and Ghostscript.
  It performs no new group census.

Use each packet's exact command, pins, output rules and documented resource
limits.  Do not infer that all topics share these dependencies, or substitute
a current package version for an explicitly pinned one.  Some individual
commands deliberately test optimized Python; that does not authorize adding
``-O`` to the ordinary-Python commands above.

Configured Lean compilation
---------------------------

``audit/formal-project/README.rst`` and its ``author/README.rst`` describe
the combined runner.  At the documented edition it covers the canonical
100-source library and the separate one-source Topic B component.  With
the compiler and package cache already supplied, use another fresh child::

    python3 -E -B scripts/check_project_lean.py \
      --lean /path/to/pinned/lean --packages /path/to/pinned/lake/packages \
      --out "$repro_scratch/lean" --jobs 1

The default selects both components.  ``--components legacy`` or
``--components topic-b`` explicitly selects a partial run.  Only a fresh
passing execution of both earns ``PASS_FULL_CONFIGURED_PROJECT``; an old
report is not substituted for a child run.

The retained toolchain is ``leanprover/lean4:v4.32.2``.  The authoritative
package revisions are in ``research/case_study/formal/lake-manifest.json``
and ``dependency_manifest.json``; Topic B retains its own matching
``papers/topic-b/v2/formal/dependency_manifest.json``.  Their exact revisions
are::

    mathlib          905b95818eb32af7874a58b427f50c1711a5e96c
    plausible        e12c1910fe855cbfc38803cd4e55543906d5fa62
    LeanSearchClient c5d5b8fe6e5158def25cd28eb94e4141ad97c843
    importGraph      7e9612bf0b9ee66db3cb5b9988a35afc706f5a12
    proofwidgets     6e311e2a844da9b2cc3971187df2fe0066947b93
    aesop            a7dbf0c63b694e47f425f3dcddbc0e178bb432d3
    Qq               38d591e778f100aec9762bb582f9c7f55f50e9dc
    batteries        023ce7d62a0531e22a5331e20b587817a80d49ff
    Cli              88679d088c9720c27ebdf2ba4dafe17341747f94

The runner does not provision that environment.  Its trust boundary includes
the compiler and cached external objects.  The legacy checker preserves an
explicit historical native-evaluation exception; do not label all its
declarations standard-axiom-only.  These configured components do not
formalize every written result or every experimental Lean source in the
archive.  The combined-runner admission records a real Topic B-only check
and orchestration fixtures, not a fresh all-101-source run.

Sources, historical drafts and cleanup
-------------------------------------

Original scholarly PDFs are not redistributed.  A source recount or primary
source check requires separately acquired originals of the recorded edition
and exact hashes, together with its input policy.  A documentary hash or a
source-free adapter is not a newly acquired original, and it does not remove
the source premise.  Public portable checks explicitly state which such
inputs are excluded from their replay.

Historical author packets, drafts and copied orchestration remain evidence.
Their paths, labels and numerical claims belong to their recorded edition;
some scripts retain obsolete relative or private absolute paths and are not
current executable entry points.  Follow the current guide, admission and
portable adapter instead of executing every archived program.  A candidate
label in a frozen packet is interpreted through its later admission.

Keep new scratch builds outside the checkout.  Unreferenced Python bytecode,
temporary render output and local Lean build objects may be regenerated
from preserved sources and the required environment, once no active process
or accepted record depends on those exact files.  Package source checkouts
are a separate dependency, not automatically disposable build output.

Do not remove a file solely because it ends in ``.log``, ``.aux`` or ``.fls``:
the published provenance manifests bind some such bytes as historical
evidence, and other logs contain mathematical certificates.  A decoded
portable tree can be disposable only when its canonical transport, exact
restore recipe and retained reports suffice, and no active input depends
on the decoded paths.  Preserve unique manuscripts, inputs, source documents,
certificates and hash-bound evidence.  Migrating their interfaces requires
reviewed reference updates; pushing a repository alone does not establish
that unpublished local work is recoverable.

This guide supplies entry points and their limits.  It records no new
scientific execution, clean-machine installation or full-project replay.

F012 package-relative reproduction
----------------------------------

Read ``papers/edge_girth_regular_graphs/reproduction.rst`` before selecting a
route. It gives typed environment generation, complete bounded defaults,
exact payload authentication and restoration of all 53 written sources.
The public registration preserves the full 8e10ebc3 predecessor Git tree and
global manifest; locally sparse unchanged files are retained Git objects,
not deletions. Restore a historical path from Git before invoking a checker
that needs its working-tree bytes. The registration reports inherited Git
identity checks separately from full hashing of all new package exports.
The metadata controls and dense-bounds integration do not replace the
source's borrowed catalogue premises or amount to an all-route fresh replay.


Selected F004 prefix8 certificates
----------------------------------

Read ``audit/f004/prefix8_certificates/PUBLICATION.rst`` and the exact component
manifest before selecting ``scripts/g2_prefix8_certificates/check.py``. Metadata
integrity and the proper230/common118 mathematical modes are separate. The later
Root records acquire a public-only replay of these fixed historical certificates;
old Source-proposal labels remain unchanged as history. The prior3283, natural
full-model/original-frame/catalogue/weights premises stay borrowed. The selected
cutoff is3631 rejected and148 unpaid, regardless of later private studies. This
partial publication leaves102/105 originals and F004/F009/L026 pending unchanged.

``scripts/verify_snapshot.py`` now checks the exact additive layer over full
commit ce9970599fc1e7334f9f3f74ae37929346fbe4ad. The old seven-file checker is
retained byte-for-byte and evaluated only in an explicitly labelled frozen
predecessor Git view; no old CLI pass on the enlarged tree is asserted. A separate
strict current index/delta check allows only the finite exports, one dispatcher
main edit and this append. No old catalogue, paper, archive or proof is retargeted.
See the publication guide for exact replay commands, actual Root evidence and
the inherited Git-history requirement. Keep fresh generated outputs external.
