One fixed line argument for 161 original quartets
===============================================

This package reproduces 161 additional exclusions in F004, q11 job 24:
138 use the right end and 23 use the left end. Each original quartet fails
the intersection property because the indicated end generates the whole
acquired group G2(11).

The common proof and its attributions are retained in
`the shared theory <../fixed_line_orbits/THEORY.rst>`_ and
`the TeX proof <../fixed_line_orbits/fixed_line_criterion.tex>`_. The earlier
certificate for position 59 remains in its original directory. Here the
same argument is applied to 161 further quartets; the theory and numerical
verification routines are reused.

For each case, the program reconstructs the original quartet from the
indexed catalogue. Separate consumers verify an element of order 19 with
a fixed space of dimension one and 9,241 distinct vectors reachable from
the same fixed seed. A final check binds both certificates to the same
ordered triple in the reconstructed quartet.

A proper end subgroup preserving a rational line would have at most ten
reachable nonzero vectors on that line. The other alternative in the
attributed subgroup cover lies in J1, whose order gives an orbit bound of
175,560/19 = 9,240. The verified tree excludes both alternatives. The named
group, its faithful natural representation, catalogue membership and the
complete subgroup cover remain explicit imported premises.

Verification
------------

All 138 cases passed all four stages in a private directory and again in
the repository directory: 1,104 separate successful guarded stages.
The 23 left-end cases passed the same four stages in both locations:
184 further successful guarded stages. A separate run of one earlier
right-end case also checked the dispatcher's unchanged default selection.
Sixteen checks of case identity, ordered ends and certificate consistency
passed in each location before the left-end extension. These checks already
cover both ordered ends; their unchanged results are reused here.
The existing word, kernel and reachability
verifiers retain their earlier control suites and exact source manifests.

Closing checks covered all 161 original case associations. Original
reconstruction proofs and results agree byte for byte between locations.
Word and reachability proofs agree after removing only the recorded
manifest directory path. Their results agree after the corresponding
input path relocation and removal of observed time and memory metadata.
All other answers and operation counts agree. REPLAY.json and CASES.json
retain the original 138 right-end comparisons and input hashes unchanged.
REPLAY_LEFT.json and CASES_LEFT.json record the 23 left-end cases.
AUDIT.json and AUDIT_LEFT.json record the separate closing audits and
their scope. The original dispatcher and source manifest remain available
at commit e8ab1e6; the current dispatcher adds an explicit end selector.

These are replays of already registered exclusions. They add no second
case credit, completed original, conjecture, Lean proof or compression
measurement. Job 24 still has one unresolved position, 2352; the wider q11
classification and the manuscript remain incomplete.

Reproduce from a clone
---------------------

Keep this directory beside fixed_line_orbits and matrix_certificates.
The workers use the Python standard library. The resource supervisor
needs psutil installed in the same Python interpreter. The reference
runs used macOS.

From this directory, choose a fresh canonical output parent and run
successive windows of at most eight cases::

    REPLAY_ROOT="$(pwd -P)"
    OUTPUT_PARENT="$(cd "$(mktemp -d)" && pwd -P)"
    for start in $(seq 0 8 136); do
        stop=$((start + 8))
        if [ "$stop" -gt 138 ]; then stop=138; fi
        env -u COVERAGE_PROCESS_CONFIG -u COVERAGE_CONFIG \
            -u COVERAGE_PROCESS_START -u OPENSSL_CONF -u OPENSSL_MODULES \
            python3 -E -B -S "$REPLAY_ROOT/run.py" "$REPLAY_ROOT" \
            "$OUTPUT_PARENT/right_${start}_${stop}" "$start" "$stop" \
            --end right || break
    done

Use the same roots and separate fresh output directories for the left end::

    for start in 0 8 16; do
        stop=$((start + 8))
        if [ "$stop" -gt 23 ]; then stop=23; fi
        env -u COVERAGE_PROCESS_CONFIG -u COVERAGE_CONFIG \
            -u COVERAGE_PROCESS_START -u OPENSSL_CONF -u OPENSSL_MODULES \
            python3 -E -B -S "$REPLAY_ROOT/run.py" "$REPLAY_ROOT" \
            "$OUTPUT_PARENT/left_${start}_${stop}" "$start" "$stop" \
            --end left || break
    done

Run the sixteen consistency checks separately::

    python3 -E -B -S controls.py close_replay.py \
        efddb6ed0e50e4e04a098382ea7e3a1541d83a726b36e1affc4b6bd968c567b2

The dispatcher runs each scientific stage under its own unchanged
128 MiB / 150 second supervisor. Admission requires 4 GiB available RAM
and 10 GiB free disk; the operational floors are 3 GiB and 8 GiB.
Each stage retains its own operation, input and output counters. The
dispatcher has separate limits of 256 MiB, 64 MiB of metadata reads,
512 paths and 16 MiB of metadata outputs per window. A refusal or failure
stops the window and preserves its partial outputs; no failed stage is
automatically retried.

Source sizes are recorded separately from mathematical compression.
Original acquisition uses 44,686 worker bytes plus 23,167 guard bytes.
The unchanged word and reachability roles use 52,557 and 46,456 bytes
including guards. The final join uses 31,004; the new dispatcher adds
9,619 bytes of coordination code. No common verifier or theorem is
republished for each case.

Only source, compact inputs and verification records belong in this
directory. Runtime logs, locks and generated proof/result files are
written to the chosen output parent.
