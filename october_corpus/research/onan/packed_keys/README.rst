Packed conjugacy keys
=====================

This directory contains the permutation kernel and binary I/O code being
developed for the O'Nan computation. Its small examples can be built and
checked from this checkout with Python 3 and a C11 compiler. No downloaded
workspace, prebuilt executable or GAP installation is needed for these tests.

Run the examples
----------------

From this directory::

  python3 -E -B check.py --cc cc

The script verifies the eight source files against ``SourceManifest.json``,
builds two executables in a temporary directory, and runs the unchanged
test suites: eighteen kernel checks and ten I/O checks. It prints their
reports and the freshly built binaries' hashes. Builds, logs and temporary
test data are removed when the script exits.

The entrypoint was successfully run with Clang on macOS under an external
512 MiB memory limit and 150-second time limit. The observed run took
1.48 seconds; its recorded evidence is in ``evidence/reproduction/``.
These timings concern the small examples. They do not establish the cost
of the O'Nan census. The script has a shared 140-second deadline; memory
limits require an external process monitor.

``--cc`` defaults to ``CC`` or ``cc``. Compiler arguments are passed directly,
without a shell. The build commands are::

  CC -std=c11 -O2 -Wall -Wextra -Werror packed_keys.c controls.c -o TEMP/core_controls
  CC -std=c11 -O2 -Wall -Wextra -Werror portable_io/portable_cli.c -o TEMP/packed_portable

The portable translation unit includes ``../packed_keys.c`` and is compiled
alone. The kernel test executable uses ``packed_keys.c`` and ``controls.c``.
Each command log is limited to 64 KiB and each executable to 16 MiB.

What the tests establish
------------------------

The tests use small symmetric groups and finite boundary examples. They
exercise complete permutation keys, supplied certificates, orbit closure,
interrupted updates, binary round trips and rejection of malformed inputs.
They test the actual kernel and I/O implementation; the entrypoint adds
no replacement mathematical tests.

Passing these checks does not complete an O'Nan partition, establish
generation, recover the source manuscript or provide a Lean proof.
The production wrapper ``portable_io/portable.py`` and the GAP export files
are included to preserve the complete source package. The example script
does not invoke them. Production still requires separately verified group
data, runtime evidence and computation results.

Sources and evidence
---------------------

The eight original program files retain their exact bytes and directory
layout. ``SourceManifest.json`` records their hashes, contributor labels
and provenance. Comments describing files as unrun refer to their earlier
source-freeze stage; the later test runs have separate records.

The manifest itself is preserved from initial preparation. Its
``new_public_files`` pins and preparation/status fields describe the earlier
README files and unrun stage, not the current documentation or test status.
Its eight program-file hashes remain current and are the rows checked by
``check.py``. The successful later run is recorded in
``evidence/reproduction/manifest.json``.

``evidence/HistoricalManifest.json`` identifies unchanged earlier reviews,
test reports, captures and logs. ``evidence/README.rst`` explains their
scope and the larger inputs omitted from this package. Historical records
retain their original absolute paths. Copying those records does not make
the entire earlier machine audit replayable from this checkout, and newly
built binaries do not inherit its compiler or production approvals.

The earlier public L026 centralizer package and the separate L046 regular-map
publication remain unchanged. This directory adds reproducible computation
tools and their small tests; it claims no additional completed manuscript.
