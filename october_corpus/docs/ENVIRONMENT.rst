Setting up a reproduction environment
====================================

Use this supplement with `REPRODUCING.rst <REPRODUCING.rst>`_ and the
selected component's guide. It describes the current checker interfaces
without changing their frozen manifests. The installation commands below
are a proposed setup recipe, reviewed against those interfaces; they have
not been tested together on a clean machine. No installation or compilation
was performed for this document. A successful replay from a fresh checkout
using an existing environment is a different test.

Start from the full-history clone described in REPRODUCING.rst. Keep the
checkout, its Git history, source manifests and certificates. Build products
can live outside it. The commands use a POSIX shell, Git and CPython 3.11 or
newer; individual older suites also support Python 3.10. Install those tools
through your operating system's normal distribution, then, from the
repository root::

    repo_root=$(pwd -P)
    repro_env=$(mktemp -d "${TMPDIR:-/tmp}/human-compression-env.XXXXXX")
    repro_env=$(cd "$repro_env" && pwd -P)
    python3 -m venv "$repro_env/venv"
    repro_python="$repro_env/venv/bin/python"
    "$repro_python" --version
    git rev-parse HEAD

The standard `Python venv documentation
<https://docs.python.org/3/library/venv.html>`_ describes virtual-environment
installation. Invoke the chosen interpreter explicitly: installing a package
in this environment does not install it for another ``python3``. Ordinary
checks below use ``-E -B`` and never ``-O``. Select a fresh output child for
each invocation; keep reports and logs until their results have been reviewed.

Python suites and portable components
------------------------------------

The snapshot check, quick smoke suite and older smoke suite use the standard
library; the snapshot check also invokes Git::

    "$repro_python" -E -B scripts/verify_snapshot.py
    "$repro_python" -E -B scripts/smoke_check.py \
      --quick --keep-work-dir --timeout 600
    "$repro_python" -E -B scripts/smoke_check.py \
      --older --keep-work-dir --timeout 600

The five-check ``--full`` smoke suite additionally imports NumPy. Its current
checker does not pin a NumPy release. The installation below uses the
published Topic LCD environment's NumPy 2.4.4 baseline (recorded with Python
3.14.6), rather than selecting an unrecorded latest release::

    "$repro_python" -m pip install numpy==2.4.4
    "$repro_python" -m pip freeze > "$repro_env/python-packages.txt"
    "$repro_python" -E -B scripts/smoke_check.py \
      --full --keep-work-dir --timeout 600

That baseline is bound by `Topic LCD's admission
<../audit/topic-lcd/v1/admission.json>`_ and `environment record
<../audit/topic-lcd/v1/measurement/packet/environment.json>`_, alongside its
passing numerical replay. It is evidence for that retained environment,
not an already executed clean installation or full smoke-suite run using
this recipe. Record the actual interpreter version as well as pip's list.

The O'Nan composition replay uses CPython and Git, with no GAP, NumPy or Lean
installation. Its own guide specifies its disk reserve and exact admission::

    "$repro_python" -E -B scripts/onan_regular_maps/check.py \
      --repo "$repo_root" --out "$repro_env/onan" \
      --admission data/onan_regular_maps/admission.json

The girth-diameter component requires exactly NetworkX 3.6.1 and a C++17
compiler available as ``c++``. Unlike NumPy above, the NetworkX version is
checked by the program. Install your platform's C++ toolchain first, then::

    "$repro_python" -m pip install networkx==3.6.1
    c++ --version
    "$repro_python" -m pip freeze > "$repro_env/python-packages.txt"

The following hash identifies the accepted order95 component published in
commit ``a400bc5fa35126d39c9af0ee75c18776e463c002``. Authenticate that edition
through the publication record or trusted commit; hashing an arbitrary
replacement manifest does not establish trust. Follow `the component guide
<../papers/girth_diameter_bounds/README.rst>`_::

    order95_manifest_sha=aff3401ecd4d39ae30a398502a8cb03d14504c0251001f52e63535b9bd56d27a
    "$repro_python" -E -B scripts/girth_diameter_bounds/check.py \
      --manifest-sha256 "$order95_manifest_sha" --metadata-only
    "$repro_python" -E -B scripts/girth_diameter_bounds/check.py \
      --manifest-sha256 "$order95_manifest_sha" --out "$repro_env/order95"

This compiles the published C++ checker in the fresh output directory,
checks 27 saved refutations and the positive graph, and uses no solver or
old enumeration cache. The sources, CNFs, proofs and graph are required;
an old compiled checker is not.

Some topic/transport checks additionally import pypdf, especially for PDF
page-text comparisons. Install it only when the selected guide requires it::

    "$repro_python" -m pip install pypdf==6.13.0
    "$repro_python" -m pip freeze > "$repro_env/python-packages.txt"

Pypdf 6.13.0 is recorded in the accepted Topic LCD environment above and
the `locally projective measurement environment
<../audit/topic-locally-projective/v1/measurement/packet/environment.json>`_.
These are documented baseline versions, not one project-wide lockfile or
proof of compatibility with every historical renderer. Preserve any failed
comparison; changing the PDF reader is not a reason to weaken an exact
text check.

Paper rendering
---------------

``scripts/build_papers.py`` itself uses the Python standard library. Install
a TeX distribution providing ``xelatex`` and ``pdflatex`` on PATH, including
the packages named in the selected paper's preamble. Record the actual
distribution/package versions: the current builder pins manuscript inputs,
but not a complete TeX installation or font-file set. Check availability::

    xelatex --version
    pdflatex --version
    kpsewhich geometry.sty
    kpsewhich amsmath.sty
    kpsewhich hyperref.sty

Then select only the desired catalogue entry, for example::

    "$repro_python" -E -B scripts/build_papers.py \
      --paper audit/protocol --output-dir "$repro_env/protocol" --jobs 1

The builder stages declared inputs, uses XeLaTeX unless the catalogue
specifies pdfLaTeX, disables shell escape and checks for unstaged checkout
reads. The checks above are examples of common packages, not an exhaustive
package list for every paper. L027/L120/L070 transport guides can additionally
require Ghostscript (``gs``); that is separate from this paper builder.

Exact Topic A v3 and Topic B v2 preambles require ``STIXGeneral``,
``STIX Two Math`` and ``Menlo``; Topic A also names ``STIX Two Text``.
These fonts are not bundled. In particular a generic TeX installation does
not establish that Menlo is available. Supply fonts with those exact names,
or treat exact rendering of these editions as blocked.
Changing a frozen preamble or substituting a font is a new rendering edition,
not reproduction of the bound one. Mathematical Python/Lean replay does not
require these fonts unless rendering was explicitly selected.

Pinned Lean dependencies
------------------------

The authoritative configuration is under
``research/case_study/formal/``: ``lean-toolchain``, ``lakefile.lean``,
``lake-manifest.json`` and ``dependency_manifest.json``. Topic B's
``papers/topic-b/v2/formal/dependency_manifest.json`` agrees on the nine
package revisions. Use the literal ``rev`` fields, not the branch names in
``inputRev``. Do not run ``lake update`` as part of reproduction.

Install `elan <https://github.com/leanprover/elan#installation>`_ following
its official installation instructions. The proposed setup below copies
only the three Lake configuration files to a fresh external directory,
installs the declared Lean 4.32.2 toolchain, and asks the pinned mathlib cache
tool to obtain its external build artifacts. This requires network access
and can consume multiple gigabytes; it is not part of the small Python
checks and has not been run as part of this documentation change::

    mkdir "$repro_env/lean"
    cp research/case_study/formal/lean-toolchain \
       research/case_study/formal/lakefile.lean \
       research/case_study/formal/lake-manifest.json "$repro_env/lean/"
    repro_toolchain=$(cat "$repro_env/lean/lean-toolchain")
    elan toolchain install "$repro_toolchain"
    (
      cd "$repro_env/lean"
      elan run "$repro_toolchain" lake exe cache get
    )
    cmp research/case_study/formal/lean-toolchain "$repro_env/lean/lean-toolchain"
    cmp research/case_study/formal/lake-manifest.json "$repro_env/lean/lake-manifest.json"
    repro_lean="$(elan run "$repro_toolchain" lean --print-prefix)/bin/lean"
    "$repro_lean" --version

Stop if either comparison fails. Before compilation, check every package's
actual revision and tracked-source cleanliness against the public manifest::

    "$repro_python" -E -B - "$repo_root" "$repro_env/lean/.lake/packages" <<'PY'
    import json, pathlib, subprocess, sys
    root, packages = map(pathlib.Path, sys.argv[1:])
    pins = json.loads((root / 'research/case_study/formal/dependency_manifest.json').read_text())
    for row in pins['packages']:
        path = packages / row['name']
        actual = subprocess.check_output(['git', '-C', str(path), 'rev-parse', 'HEAD'], text=True).strip()
        if actual != row['rev']:
            raise SystemExit('Wrong package revision: ' + row['name'])
        subprocess.run(['git', '-C', str(path), 'diff', '--exit-code', 'HEAD', '--'], check=True)
        print(row['name'], actual)
    PY

Use the actual compiler path and newly supplied package tree explicitly::

    "$repro_python" -E -B scripts/check_project_lean.py \
      --lean "$repro_lean" --packages "$repro_env/lean/.lake/packages" \
      --out "$repro_env/lean-report" --jobs 1

This invokes the current 100-module checker and the separate Topic B module.
It does not substitute cached project reports for compilation. Older
``verify_lean.py --all`` has a smaller fixed selection; use the combined
runner for the current configured pair of components. Pass explicit paths
also when invoking Topic B directly, because its historical defaults name
the author's installation.

Rebuilding dependency objects
-----------------------------

The current checkers admit freshly rebuilt dependency objects. They require
Lean version 4.32.2, the package Git
revisions and clean tracked package sources. They record executable or
generated-object hashes where applicable; they do not compare newly built
external ``.olean`` files to old object hashes. The project sources are
compiled again into fresh output. ``scripts/check_lean.py`` also builds
missing imported dependency modules from the pinned sources into its own
overlay. Topic B instead consumes supplied dependency build directories.
Dependency object contents and the compiler remain explicit trusted inputs.

Consequently a correctly built dependency tree from the declared source
revisions is admitted by these interfaces; keeping the old private package
cache is not a requirement. This interface fact is not a tested, complete
cache-free bootstrap procedure. The pinned Lake accepts ``--no-cache`` and
the target ``@mathlib/Mathlib``, but mathlib's pinned configuration deliberately
rejects an unprepared ProofWidgets JavaScript rebuild. ProofWidgets has its
own Node/npm build and lockfile. A source-only installation must resolve
that upstream build step while retaining the nine exact package revisions
and unchanged tracked sources. Do not silently remove its guard or claim
that bare ``lake --no-cache build`` has been validated here.

The cache-download recipe above trusts the external cache as the existing
checker does. A future successful source-only build would replace that
operational dependency with recorded source-build evidence. Neither route
changes the legacy module's documented native-evaluation exception or
extends formal coverage to every written proof.

Inputs that setup cannot supply
------------------------------

Default combined Lean compilation, the selected smoke suites and the two
current portable components do not require the private study directory.
Optional primary-source audits do: for example Topic B ``--verify-primary``
requires the exact eleven ``private_retained_bindings`` in its manifest,
including source PDFs and ``phase141_module_B_review.json``. They are not
installed by pip, Lake or the default public clone. Supply those independently
with the declared hashes or omit that optional audit and retain its source
premise. Historical absolute provenance paths are not a setup recipe.

After review, newly generated project objects, temporary renders and decoded
copies may be discarded when no active job or retained evidence depends on
them. Preserve their canonical sources, certificates, transport packs,
manifests, required Git history and accepted reports. Installed compilers
and external dependency trees are environment assets: deleting them requires
reinstallation/rebuilding before the next formal check. No file extension
alone establishes that an archived file is unused.
