Bipartite quintic graphs of diameter eight
=========================================

This package reproduces the 16,467 ordinary isomorphism classes of connected
5-regular bipartite graphs on 32 vertices with diameter eight. Their girth
is four. The published census is due to Cambie, Goedgebeur, Jooken and Van
den Eede, ``On the order-diameter ratio of girth-diameter cages``,
`arXiv:2511.21144v3 <https://arxiv.org/abs/2511.21144>`_, Appendix B, Table 6.

The calculation here uses fourteen proved structural forms. It exhausts
the permitted incidence profiles on both sides, constructs every pair,
and identifies ordinary graphs across all choices of roots and structural
forms. The proofs and their reviews are in ``proofs/``. The mathematical
kernel is retained at its reviewed version; ``run.py`` supplies a complete
portable enumeration around that kernel. The published count is an
existing result, and no expected count is supplied to the program.

The reviewed run completed 902 profiles, 3,617 local forms and 34,786 pairs
in 26.53 seconds. Its sampled peak process-tree memory was 64,405,504 bytes
(about 61 MiB). Every pair had a full 32-vertex isomorphism witness checked.
The complete sorted code stream is byte-identical to the separately
audited batch calculation. Both use the same mathematical kernel.

Run the calculation
-------------------

Use Python 3 on Linux or macOS. The producer uses the standard library.
The supplied resource supervisor additionally uses ``psutil==7.2.2``.
From this directory, create an isolated environment and a fresh result
directory on the same volume::

    python3 -m venv .venv
    .venv/bin/python -m pip install -r requirements.txt
    REPRO_BUNDLE="$(pwd -P)"
    REPRO_PYTHON="$REPRO_BUNDLE/.venv/bin/python"
    REPRO_RUN="$(mktemp -d "$REPRO_BUNDLE/../.bipartite-results.XXXXXX")"

Run the small independent checks first::

    env -u COVERAGE_PROCESS_START -u COVERAGE_PROCESS_CONFIG \
        -u OPENSSL_CONF -u OPENSSL_MODULES \
        "$REPRO_PYTHON" -E -B runtime/supervise_validation.py \
        --volume "$REPRO_BUNDLE" --output "$REPRO_RUN/control-resources" \
        --rss-cap-mib 128 --timeout 150 -- \
        "$REPRO_PYTHON" -E -B -S "$REPRO_BUNDLE/controls.py" \
        --manifest-sha256 37f9851f85762437b31818099e1f40abd00bc9825d0c7bc2786a275407034d7d \
        --out "$REPRO_RUN/controls" --volume "$REPRO_BUNDLE"

Then run the complete enumeration::

    env -u COVERAGE_PROCESS_START -u COVERAGE_PROCESS_CONFIG \
        -u OPENSSL_CONF -u OPENSSL_MODULES \
        "$REPRO_PYTHON" -E -B runtime/supervise_validation.py \
        --volume "$REPRO_BUNDLE" --output "$REPRO_RUN/producer-resources" \
        --rss-cap-mib 128 --timeout 150 -- \
        "$REPRO_PYTHON" -E -B -S "$REPRO_BUNDLE/run.py" \
        --manifest-sha256 37f9851f85762437b31818099e1f40abd00bc9825d0c7bc2786a275407034d7d \
        --out "$REPRO_RUN/codes" --volume "$REPRO_BUNDLE"

The supervisor admits a run with at least 4 GiB available RAM and 10 GiB
free disk, and stops at sampled floors of 3 GiB and 8 GiB. The worker limit
is 128 MiB, with 120 seconds for enumeration and 150 seconds outside it.
The shared lock serializes runs within this bundle. A complete result
requires both the worker receipt and its resource report to pass.
Interrupted runs leave provisional outputs and never overwrite old results.

Check the result
----------------

``codes/receipt.json`` records complete coverage of all 28 profile domains
and all 14 products. ``ordinary_classes`` counts their global union.
``reference/`` contains the reviewed result and its five code files.

The code checksum is SHA256 of all canonical JSON lines in sorted order,
including their final line feeds. It is independent of shard boundaries::

    a624df3f52930ff3703fadf9f7352ed9c956e008daa19d7fe9a83ed97e9cfbba

Each code reconstructs a graph using
``theory.graph_from_code(theory.frozen(code))``. Each output shard contains
at most 4,096 records and 2 MiB. The separate complete-enumeration role has
refusal bounds of 65,536 pairs, forms and codes, and 16 MiB total output.
The manifest fixes these limits and every input by relative path, length
and hash. Inputs are authenticated again after the calculation.

``PUBLICATION.json`` records attribution, scope and measured validation.
``evidence/`` contains the static reviews, actual run evidence and
independent audit. This establishes the bipartite branch; F009's
nonbipartite census remains unfinished. No new conjecture, Lean proof or
compression measurement is claimed by this package.
