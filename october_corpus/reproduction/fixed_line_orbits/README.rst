One fixed line and 9,241 reachable vectors
=========================================

This package reproduces one exclusion from the rank-four census in the
acquired natural model of G2(11): job 24, position 59, representative J136.
The right end generates the whole group, so the original quartet fails
the intersection property. This does not complete the census or manuscript.

The proof is in THEORY.rst and fixed_line_criterion.tex. Its two imported
premises are the named original group, membership and natural frame, and
the complete proper-subgroup cover stated and attributed there. Neither
a matching group order nor a checksum establishes those premises.

What is checked
---------------

The original quartet is reconstructed through the unchanged sibling
matrix_certificates reader. A separate consumer verifies an element of
order 19 and a complete certificate that its fixed space has dimension
one. Another consumer verifies 9,240 parent images, giving 9,241 distinct
reachable vectors from the same fixed seed. The final check requires
both ordered triples, the word and the seed to agree exactly with the
fresh reconstruction.

An invariant rational line would have to be this fixed line and could
contain at most ten reachable nonzero vectors. The other proper-subgroup
alternative has order at most 175,560 and would give an orbit of size
at most 175,560/19 = 9,240. Both contradict the certificate.

All 20 file and consistency checks, 18 word and kernel checks, and 18
reachability checks passed. The original reconstruction, both consumers
and the final check passed in a private directory and in the installed
repository directory. Complete scientific proofs agree after removing
only the recorded manifest-directory path. REPLAY.json records the actual
runs; AUDIT.json records their independent audit. This replays an already
registered exclusion and earns no second case, manuscript, conjecture,
Lean or compression credit.

Reproduce from a clone
---------------------

Keep this directory next to matrix_certificates. Workers use the Python
standard library. The included resource supervisor also needs psutil.
From this directory, choose a fresh absolute output directory::

    CASE_ROOT="$(pwd)"
    CASE_OUT="$(mktemp -d)"
    mkdir "$CASE_OUT/guards"
    run() {
        name="$1"; shift
        python3 -E -B "$CASE_ROOT/runtime/supervise_validation.py" \
            --volume "$CASE_ROOT" --output "$CASE_OUT/guards/$name" \
            --rss-cap-mib 128 --timeout 150 -- "$@"
    }

    run files python3 -E -B -S controls.py 6e0aaf16fa1edfc53e06e04fb6113050613daa2ff3e2c6e55ed53fd5eab5b7a4
    (cd word19 && run word_controls python3 -E -B -S controls.py source_manifest.json e0ecf25940365fca91dc58d43fcef19f7760f801ec05fb370360734cafaa2c70 controls_job.json 64e5fc6e173d4ddaa980b1c0d16cf322bf260e5eb2b7a7e83200c1d6d1d80dd8 "$CASE_OUT/word_controls")
    (cd reachable && run reach_controls python3 -E -B -S controls.py source_manifest.json e134b5987c027e074d18b2d8bceaa85f53b831036ab90eaf60eefb397a2bbdc5 controls_job.json a4fe2ad53beab9023b6b64acbcff57b145a7fba1330862332aea3744c67c3adc "$CASE_OUT/reach_controls")

    run original python3 -E -B -S acquisition/acquire.py data/acquisition.json 56077ea53f49741822c0ed6f9428e0fec4f338fb36e0d180a6ddca84c1aedaa1 "$CASE_OUT/original"
    (cd word19 && run word python3 -E -B -S consume.py source_manifest.json e0ecf25940365fca91dc58d43fcef19f7760f801ec05fb370360734cafaa2c70 ../data/word_job.json d04f637628a387cc7208d9bc8f6cb2c6f5f91bf43f7dae684123c8f625c0a2ad "$CASE_OUT/word")
    (cd reachable && run reach python3 -E -B -S consume.py source_manifest.json e134b5987c027e074d18b2d8bceaa85f53b831036ab90eaf60eefb397a2bbdc5 ../data/reachable_job.json 59ce2da07a2202a58fd8e5298cca7be6647310cb29f5ef7b04e4a0f5611a328c "$CASE_OUT/reachable")
    run conclusion python3 -E -B -S close_replay.py "$CASE_OUT/original/proof.json" "$CASE_OUT/word" "$CASE_OUT/reachable" . "$CASE_OUT/conclusion"

Each process has its own unchanged operation and input limits. The guard
requires 4 GiB available RAM and 10 GiB free disk, with floors of 3 GiB
and 8 GiB. Its memory cap is 128 MiB. Refused admission leaves the case
unrun; it does not justify lowering those limits.

Source is counted separately for each role. Acquisition uses the existing
worker limit: 44,410 bytes plus 23,167 separately disclosed guard bytes.
The word and reachability roles retain combined limits, using 52,557 and
46,456 bytes respectively. The consistency controls use 43,330 bytes
including guards; the final check uses 30,001. These program sizes are
resource accounting, not mathematical compression measurements.

The source and input manifests use relative paths. The adoption record is
historical provenance; its private evidence paths are not clone inputs.
The component headers retain their original preparation provenance.
Actual execution is recorded separately in REPLAY.json.
