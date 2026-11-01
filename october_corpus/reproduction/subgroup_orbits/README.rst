Two certificates from subgroup orbits
====================================

This package supplies the parent certificates for original job 24,
positions 2570 and 3017, in the acquired natural matrix model of G2(11).
It reconstructs each original quartet, checks that the LEFT end has no
rational invariant line, and verifies 9,241 distinct vectors reached by
supplied parent edges. The retained order 19 overgroup classification then
proves that the LEFT end is the full group. The omitted nonidentity mark
gives an explicit failure of the rank-four intersection property.

From a fresh clone, with Python 3.9 or later on Linux or macOS, run::

    python3 -E -B -S october_corpus/reproduction/subgroup_orbits/controls.py --output /tmp/subgroup_orbits_controls
    python3 -E -B -S october_corpus/reproduction/subgroup_orbits/verify.py --output /tmp/subgroup_orbits_replay

Use fresh output directory names. Each command writes proof.json and
result.json, then prints their hashes and the charged read counters.
The standard library is sufficient. The programs require -E -B -S and
retain the shared reader's prohibition of -O.

The sibling matrix_certificates directory supplies the pinned reader and
its existing domain.json, prefix.json and ambient_frame.json. Those bytes
are shared. The 2,308-case verifier and its data remain unchanged. This
package's scope is the two positions above. The older primitive 19/order 4
pair 1677/3611 has its own verification method; its portable replay remains
separate.

Checks and premises
-------------------

All original marks, their involution and string relations, the frame
identities, the same LEFT word of exact order 19, the fixed seed, and every
parent image are checked directly. Eight sign systems per case are
reduced over F_11; full rank excludes every common invariant rational
line. The field-operation counter accumulates through all sixteen systems.

The named faithful G2(11) model, the original indexed catalogue/member
association, and the complete order 19 overgroup/J1 classification remain
borrowed mathematical premises. THEORY.rst states exactly how they enter.
The canonical adoption is retained byte for byte in data/adoption.json;
its historical absolute references are inert provenance. The verifier
opens only its local files and the explicitly selected shared directory.
A successful arithmetic replay does not create Root SDK provenance,
mathematical priority, Lean formalization or a completed original paper.

The bounds are 400,000 total matrix products, 200,000 row images, 200,000
linear field units, 8 MiB of charged project reads, 96 paths, 128 MiB RSS and
100 seconds. The inherited 112 MiB/90 second soft stop also remains. Each
output is bounded by 128 KiB. Root's external replay uses the unchanged
128 MiB/150 second guard. No orbit search or full group enumeration occurs.

All 19 controls and both certificates passed in the private and installed
directories. Their proof and result files agree byte for byte. The installed
certificate run took 0.240 seconds and reported a peak resident memory of
38,174,720 bytes. REPLAY.json retains the outputs, execution records,
resource observations and independent reviews. These are replays of two
already accepted cases; they add no further classification cases.
