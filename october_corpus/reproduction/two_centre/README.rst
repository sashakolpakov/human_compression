The complete two-centre family
==============================

This calculation enumerates the ordinary unrooted sixteen-vertex halves
for nonbipartite quintic graphs of order 32, girth 4 and diameter 8 whose
centre is one two-vertex false-twin class. Endpoint columns may be zero.
It covers all four permitted side graphs, all independent row and port
multisets satisfying their margins, and all eligible endpoint choices.
It takes one ordinary union across the four domains.

The structural theorem pairs each half with one of six ordinary left
halves. If the enlarged half count is ``H``, the entire two-centre stratum
has ``6*H`` ordinary graphs. This includes the singleton-middle case and
the exceptional nonisolated middle cases. It is one intrinsic centre
stratum of the full problem. No expected count is an input or stopping
rule.

The original cage problem and published census are due to Cambie,
Goedgebeur, Jooken and Van den Eede, *On the order-diameter ratio of
girth-diameter cages*, arXiv:2511.21144v3, Appendix B, Table 6. The retained
project proofs, the extension to nonnegative columns, and their separate
independent reviews are included in ``proofs/``. The new kernel changes
the four necessary positivity predicates; all finite side domains,
ordinary side isomorphisms and full witnesses retain their proved bounds.

``manifest.json`` pins the scripts and functional mathematical inputs by
relative path, byte length and SHA256. These are identity checks; actual
controls and a complete producer receipt remain separate evidence.

Reproduce
---------

Use Python 3 on Linux or macOS. The producer uses the standard library.
The bundled resource supervisor requires ``psutil==7.2.2``, declared in
``requirements.txt``.

From this directory, choose a fresh result directory beside the bundle:

.. code-block:: sh

    set -eu
    REPRO_BUNDLE="$(pwd -P)"
    python3 -m venv "$HOME/.venvs/human-compression"
    REPRO_PYTHON="$HOME/.venvs/human-compression/bin/python"
    REPRO_RUN="$REPRO_BUNDLE/runs"
    mkdir "$REPRO_RUN"
    "$REPRO_PYTHON" -m pip install -r requirements.txt

    env -u COVERAGE_PROCESS_START -u COVERAGE_PROCESS_CONFIG \
        -u OPENSSL_CONF -u OPENSSL_MODULES \
        "$REPRO_PYTHON" -E -B runtime/supervise_validation.py \
        --volume "$REPRO_BUNDLE" --output "$REPRO_RUN/control-resources" \
        --rss-cap-mib 128 --timeout 150 -- \
        "$REPRO_PYTHON" -E -B -S "$REPRO_BUNDLE/controls.py" \
        --manifest-sha256 27c1d89c56ffdef67ba6a71ab009a0386d6071bd783e5060eddf3385147596ea \
        --out "$REPRO_RUN/controls" --volume "$REPRO_BUNDLE"

    env -u COVERAGE_PROCESS_START -u COVERAGE_PROCESS_CONFIG \
        -u OPENSSL_CONF -u OPENSSL_MODULES \
        "$REPRO_PYTHON" -E -B runtime/supervise_validation.py \
        --volume "$REPRO_BUNDLE" --output "$REPRO_RUN/producer-resources" \
        --rss-cap-mib 128 --timeout 150 -- \
        "$REPRO_PYTHON" -E -B -S "$REPRO_BUNDLE/run.py" \
        --manifest-sha256 27c1d89c56ffdef67ba6a71ab009a0386d6071bd783e5060eddf3385147596ea \
        --out "$REPRO_RUN/codes" --volume "$REPRO_BUNDLE"


The four environment variables above must be absent. The result directory
must be on the monitored volume. The supervisor requires 4 GiB available
RAM and 10 GiB free disk before launch; its sampled floors are 3 GiB and
8 GiB. The outer bounds are 128 MiB RSS and 150 seconds, and the kernel
has a 120-second scientific deadline. The supervisor serializes runs
within this bundle using ``runtime/active.lock``. Different clones have
separate locks.

The supervisor reports sampling, cleanup and reaping of known owned
processes. It does not prove the absence of unseen detached descendants.
Users with their own resource and process supervision may invoke the
child commands directly. Direct execution checks worker RSS, scientific
time and disk space; free-RAM sampling and outer process ownership belong
to the supervisor. These limits are refusal bounds, not a promise of
completion on every machine. A refused or interrupted run supplies no
complete count. Existing result files are never overwritten.

Results and coverage
--------------------

``codes/receipt.json`` records all four complete raw parameter rectangles,
with separate margin, symmetry, compatible-cell and construction counts.
Their cursor accounting must cover every raw cell. Each constructed
marked half receives its ordinary code and a verified isomorphism on all
16 vertices. Every distinct code is then reconstructed and checked as a
canonical fixed point.

The sorted code shards contain one canonical JSON line per ordinary half.
Each shard has at most 4,096 records and 2 MiB. Complete scientific output
is capped at 2 MiB; compatible attempts, marked constructions and distinct
codes are each capped at 4,096. All four domains must finish before a
count is emitted. Source and functional proof files are read and checked
again at closure. Accept a supervised result only after controls pass,
the producer is complete, the resource report passes, and the owned
worker has exited and been reaped.

Concatenating the shards in receipt order gives ``code_set_sha256``, which
is independent of shard boundaries. The receipt distinguishes
``enlarged_half_count`` from ``independent_two_centre_ordinary_graphs``.
The latter is ``6*H``; it is not labelled a singleton-middle count.

The earlier strict positive-column half stream can be compared externally
after complete runs. The proof gives its inclusion in this enlarged
ordinary code set. Equality is not an expected result, and no strict
stream, checksum or published total is a producer input.

The controls compare seven explicit fixtures, including zero columns in
each of the three possible side types, against an independent search over
all eligible endpoints and all ``7!`` side orders. They check full adjacency
witnesses and arbitrary relabeling. Small protocol controls exercise exact
four-domain accounting and union, a missing final block, evaluation and
output limits, path restrictions, duplicate JSON keys, sorted sharding
and checksum verification. These are synthetic checks and are not a
second exhaustive census.

The functional proof roles in ``manifest.json`` are opened and rechecked
by the producer. Additional retained isolation arguments, detailed reviews
and the complete intrinsic-centre formulas are pinned separately in
``DOCUMENTARY_PROOFS.json``; the producer does not open those documentary
files or charge them to its functional input-read counter. The standard
library and the supervisor's installed ``psutil`` dependency have their own
interpreter and library reads outside that artifact counter.

This reproduction by itself asserts no new conjecture solution, Lean
verification, completed manuscript or compression measurement. The other
intrinsic centre families and the remaining ordinary half counts require
their own complete evidence.
