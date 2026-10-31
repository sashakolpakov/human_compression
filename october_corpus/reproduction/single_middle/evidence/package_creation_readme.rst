# The singleton middle case

This calculation enumerates the ordinary unrooted right halves in the
singleton middle case for quintic graphs of order 32, girth 4 and
diameter 8. It covers all four permitted side graphs, all incidence
multisets satisfying their column margins, and all changes of the
distinguished endpoint. It takes a single ordinary union across all
four domains. No expected count is an input or a stopping rule.

The retained structural theorem pairs each right half with one of six
ordinary left halves. If the right-half count is `h16`, the corresponding
singleton stratum has `6*h16` ordinary graphs. This is one stratum of the
original problem, rather than a count of all graphs in that problem.
The original problem is due to Cambie, Goedgebeur, Jooken and Van den Eede,
*On the order-diameter ratio of girth-diameter cages*, arXiv:2511.21144v3,
Appendix B, Table 6.

The proofs and their independent reviews are in `proofs/`. The unchanged
mathematical kernel is `half.py`; the complete portable producer is
`run.py`. The manifest pins all functional scripts and runtime mathematical
inputs by relative path, byte length and SHA256. It authenticates their
identities without manufacturing an approval or a runtime result.

## Reproduce

Use Python 3 on Linux or macOS. The producer uses the standard library
only. The optional resource supervisor requires `psutil==7.2.2`, as
declared in `requirements.txt`.

From this directory, choose a fresh result directory beside the bundle:

```sh
set -eu
REPRO_BUNDLE="$(pwd -P)"
REPRO_PYTHON="$(command -v python3)"
REPRO_RUN="${REPRO_BUNDLE%/*}/single-middle-results"
mkdir "$REPRO_RUN"
"$REPRO_PYTHON" -m pip install -r requirements.txt

env -u COVERAGE_PROCESS_START -u COVERAGE_PROCESS_CONFIG \
    -u OPENSSL_CONF -u OPENSSL_MODULES \
    "$REPRO_PYTHON" -E -B runtime/supervise_validation.py \
    --volume "$REPRO_BUNDLE" --output "$REPRO_RUN/control-resources" \
    --rss-cap-mib 128 --timeout 150 -- \
    "$REPRO_PYTHON" -E -B -S "$REPRO_BUNDLE/controls.py" \
    --manifest-sha256 4fa0f78fb78fd5196631f3be85d578dbfde3f1400c0a73455285f72abdc1231c \
    --out "$REPRO_RUN/controls" --volume "$REPRO_BUNDLE"

env -u COVERAGE_PROCESS_START -u COVERAGE_PROCESS_CONFIG \
    -u OPENSSL_CONF -u OPENSSL_MODULES \
    "$REPRO_PYTHON" -E -B runtime/supervise_validation.py \
    --volume "$REPRO_BUNDLE" --output "$REPRO_RUN/producer-resources" \
    --rss-cap-mib 128 --timeout 150 -- \
    "$REPRO_PYTHON" -E -B -S "$REPRO_BUNDLE/run.py" \
    --manifest-sha256 4fa0f78fb78fd5196631f3be85d578dbfde3f1400c0a73455285f72abdc1231c \
    --out "$REPRO_RUN/codes" --volume "$REPRO_BUNDLE"
```

Both entry points require the four variables shown above to be absent.
The result directory must be on the monitored volume. The supervisor
requires 4 GiB of available RAM and 10 GiB of free disk before launch;
its sampled floors are 3 GiB and 8 GiB. The outer limit is 128 MiB RSS
and 150 seconds; the mathematical kernel has a 120-second scientific
deadline. The supervisor uses `runtime/active.lock` to serialize runs
within this bundle. Different clones have separate locks.

The supervisor records its sampled bounds and cleanup of known owned
processes. It claims neither kernel containment nor absence of unseen
detached descendants. Users with their own resource and ownership
supervision may invoke the child commands directly. Direct execution
checks worker RSS, scientific time and disk space, but not free RAM or
outer ownership. These limits are refusal bounds, not a promise that
every machine will complete. A refused or interrupted run has no valid
complete count; existing files are never overwritten.

## Results and coverage

`codes/receipt.json` lists each complete raw domain and its margin,
symmetry and construction counters. Every marked representative receives
the full ordinary code and a verified isomorphism on all 16 vertices.
The producer also rechecks every distinct code as a canonical fixed
point. It never adds counts from different roots or side graphs.

The code shards contain one sorted canonical JSON line per ordinary
half. Each shard has at most 4,096 records and 2 MiB; total scientific
output is at most 2 MiB. Concatenating the shards in receipt order gives
the stream whose digest is `code_set_sha256`. That checksum is independent
of shard boundaries and can be compared with a separate completed run.
The receipt gives `h16` and `singleton_stratum_ordinary_graphs` separately.

The complete producer has explicit caps of 4,096 compatible cells,
marked representatives and ordinary codes. The old private interval
tools retain their separate limits. All four raw domains must finish
before any count is emitted. Source and proof files are read and
authenticated again at closure. Accept a supervised result only after
the controls pass, the producer receipt is complete, the resource report
passes, and the owned worker has exited and been reaped.

The controls compare four explicit fixtures against an independent
search over every eligible endpoint and all seven-factorial side orders.
They check full witnesses, arbitrary relabeling, the positive-column
condition and a toy four-domain orchestration with exact alias counters,
a missing final block, evaluation and byte limits, relative paths,
duplicate JSON keys, and an independent sorted-shard checksum. The fixtures are
not asserted to be distinct ordinary classes. They do not constitute a
second full census.

This reproduction proves no new conjecture and supplies no whole
manuscript, Lean or compression-measurement credit by itself. Completing
the other graph strata and their full ordinary union remains separate.

The singleton theorem imports the separate isolation argument. Its exact
source and independent review are also included in `proofs/`, pinned by
`DOCUMENTARY_PROOFS.json`. These auxiliary proof notes are documentary
mathematical imports: the producer does not open them or count them in
its functional input-read counter. The existing proof and review roles
listed in `manifest.json` are read and rechecked at runtime.
