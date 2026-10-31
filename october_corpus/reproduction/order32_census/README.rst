Order-32 quintic census by shared structural composition
=======================================================

This package composes the complete ordinary census of connected simple
5-regular graphs on 32 vertices with girth four and diameter eight.
It uses the existing sibling packages ``bipartite_diameter_eight``,
``two_centre`` and ``centre_halves``. Their mathematical kernels, callers,
controls and limits stay unchanged. They are not embedded again here.

The count 25,408 is a known result of Cambie, Goedgebeur, Jooken and Van den
Eede, ``On the order-diameter ratio of girth-diameter cages``,
arXiv:2511.21144v3, 19 August 2026, Appendix B, Table 6, page 23. This is
recovery of that result, with no priority or open-conjecture claim.
The separate original order-80 census remains unfinished.

What is reused and checked
---------------------------

The bipartite producer exhausts all fourteen proved skeleton products and
checks full 32-vertex witnesses. The two-centre producer exhausts enlarged
ordinary 16-vertex halves H, including zero side incidences. The centre-half
producer supplies the four complete ordinary unions h1..h4. Their all-root
canonicalization and witnesses are checked by those producers. A fresh run
must complete every raw domain and the global ordinary unions.

The common written centre theorem supplies nine disjoint nonbipartite
ordinary strata::

    one twin class, size 2       6H
    one twin class, size 3       h1*h4 + h2*h3
    one twin class, size 4       6
    independent classes 1/2      h4
    independent classes 1/3      6
    independent classes 2/2      4
    centre P3                   6
    centre K2,2                 6
    centre K2,3                 18

The proved postchecks h1=2 and h2=5 simplify their sum to
6H+5h3+3h4+46. The same h4 is reused in two rows; it is enumerated once.
The strict singleton count 1,209 is a subset of enlarged H and is not
added. Bipartiteness separates the bipartite union from all nine rows.

The composer authenticates complete fresh local receipts, their exact
Source/proof context, raw coverage, typed counts and actual whole sorted
code streams. It then applies the written gluing formula. It imports no
graph kernel and performs no second independent graph-isomorphism test.
The ordinary exhaustion, coloured gluing and disjointness proofs remain
explicit mathematical premises, with their complete written reviews.
Local receipt binding creates no Root/SDK authority or independent review.

``PROOF_DEPENDENCIES.json`` retains all 52 exact relative documentary pins:
the original 49 proof/review/provenance legs and the minimum-order theorem,
review and adoption. Some proof-only folders retain historical names
``independent_centre`` and ``centre_halves`` under this directory. They
contain no embedded scientific caller, kernel or controls. Existing exact
``single_middle/proofs`` paths are reused. Absolute references inside old
review bodies are documentary provenance, not runtime paths followed by
the program.

The separately attributed hand minimum theorem in
``proofs/minimum_orders.tex`` gives n(5;4,8)=32 by the prime-k formula
2k(r+1)+2 at k=5,r=2. Its immutable front matter predates later independent
reviews; ``proofs/minimum_review.json`` and ``proofs/minimum_adoption.json``
record that later status. Known census counts were not premises of that
minimum-order proof.

Commands from a fresh clone
---------------------------

Use Python 3 on Linux or macOS. Scientific children and the composer use
only the standard library. The unchanged supervisor needs psutil==7.2.2.
From ``october_corpus/reproduction`` set::

    REPRO_ROOT="$(pwd -P)"
    REPRO_PYTHON="/absolute/path/to/environment/bin/python"
    mkdir -p order32_census/results

Run one bounded child at a time. Before each child, use this common prefix
with a distinct absent guard directory::

    env -u COVERAGE_PROCESS_START -u COVERAGE_PROCESS_CONFIG \
        -u OPENSSL_CONF -u OPENSSL_MODULES \
        "$REPRO_PYTHON" -E -B order32_census/runtime/supervise_validation.py \
        --volume "$REPRO_ROOT" --output ABSOLUTE_FRESH_GUARD_DIRECTORY \
        --rss-cap-mib 128 --timeout 150 --

The supervisor retains 4 GiB RAM/10 GiB disk admission and sampled floors
of 3 GiB/8 GiB. Workers retain 128 MiB and 120 seconds, with 150 seconds
outside. Runtime libraries and known-process sampling are separate from
worker artifact meters. Empty known cleanup does not exclude unseen
detached descendants. Every complete result needs both worker and guard
closure. All output names below must be fresh.

Run the bipartite controls and producer using its sibling README, with
outputs ``bipartite_diameter_eight/runs/controls`` and
``bipartite_diameter_eight/runs/codes``. The producer child command is::

    "$REPRO_PYTHON" -E -B -S "$REPRO_ROOT/bipartite_diameter_eight/run.py" \
        --manifest-sha256 37f9851f85762437b31818099e1f40abd00bc9825d0c7bc2786a275407034d7d \
        --out "$REPRO_ROOT/bipartite_diameter_eight/runs/codes" \
        --volume "$REPRO_ROOT/bipartite_diameter_eight"

Run the enlarged-H controls and producer using ``two_centre/README.rst``,
with outputs ``two_centre/runs/controls`` and ``two_centre/runs/codes``.
Its producer child is::

    "$REPRO_PYTHON" -E -B -S "$REPRO_ROOT/two_centre/run.py" \
        --manifest-sha256 27c1d89c56ffdef67ba6a71ab009a0386d6071bd783e5060eddf3385147596ea \
        --out "$REPRO_ROOT/two_centre/runs/codes" --volume "$REPRO_ROOT/two_centre"

For both components, controls.py takes the same manifest, --out and
--volume options with its own fresh output. Keep all exact receipts and
code shards, not just displayed scalar counts.

Follow ``centre_halves/README.rst`` for its controls, fourteen raw jobs and
four full ordinary collections. Bind every job to the actual newly
produced receipts. Default complete outputs are
``centre_halves/runs/b1_collect/receipt.json`` through ``b4_collect``.
This frontend has no multi-part merge/seal mode. A full collection over
2,048 selected marked records refuses; do not raise a cap, omit a prefix
or declare a partial family complete. Historical small record totals
are observations, not stopping targets or future-fit guarantees.

Run the 43 synthetic scalar/receipt/stream/path controls under the common
prefix, with this child command::

    "$REPRO_PYTHON" -E -B -S "$REPRO_ROOT/order32_census/composition_controls.py" \
        --program "$REPRO_ROOT/order32_census/compose.py" \
        --sha256 cc12da5d3663e2ded71e5614fda3a347e72b7a16586dfb00af2d0490b77feecd \
        --out "$REPRO_ROOT/order32_census/results/composition_controls.json"

After all six complete receipt locations exist, mechanically bind their
actual whole-file descriptors, again under a fresh guard::

    "$REPRO_PYTHON" -E -B -S "$REPRO_ROOT/order32_census/compose.py" \
        --root "$REPRO_ROOT" --inputs order32_census/COMPOSE_TEMPLATE.json \
        --sha256 1076d9f854e602428ffc9b349e5fc27927eea6a5e38c01ac3f9b4d54f6afaf5f \
        --out order32_census/results/composition_inputs.json --bind

Use the new SHA printed by that binder for the separate composition call::

    "$REPRO_PYTHON" -E -B -S "$REPRO_ROOT/order32_census/compose.py" \
        --root "$REPRO_ROOT" --inputs order32_census/results/composition_inputs.json \
        --sha256 SHA_PRINTED_BY_THE_ACTUAL_BINDER \
        --out order32_census/results/composition.json

Binding grants no approval. It leaves every whole receipt field, timing
and path in the acquired descriptor. No old receipt SHA is transplanted.
The composer requires exact matching manifests, complete coverage and
actual sorted-stream byte counts/SHA identities before it evaluates the
nine-stratum formula.

Compare only after complete production
--------------------------------------

``reference/results.json`` records the earlier accepted comparison values:
H=1,395, (h1,h2,h3,h4)=(2,5,36,115), bipartite=16,467,
nonbipartite=8,941 and total=25,408. Expected final counts do not enter the
producer loops, stopping conditions or feasibility predicates. The small
analytic constants and h1/h2 equalities are stated written theorem inputs.

The composer has its own 8 MiB unique artifact extent, 32 MiB metered reads
including its final whole-input sweep, 256 paths, 2 MiB files, 1,024-byte
code lines and 64 KiB output. Its Source/controls/two runtimes total
55,954 bytes below 65,536. ``IO_INVOICE.json`` separates interpreter Source
reads, bounded output readback and runtime loads. Refusals remain unpaid;
no larger worker or artifact limit is introduced by this layout.

The full claim is count reproduction through complete ordinary halves and
proved gluing; it does not export a new stream of all 25,408 full graphs.
The same mathematical kernels are reused in different orchestration.
It supplies no whole-manuscript completion, Native-family payment, new
conjecture resolution, Lean formalization or compression measurement.
F009 still requires its separate order-80 census and final synthesis.
