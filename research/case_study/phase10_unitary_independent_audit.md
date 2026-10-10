# Independent review of the PSU4(5) rank-four witness

10 October 2026. **PASS for the exact finite statement.** This is an internal
mathematical and computational review; it is not external peer review or a
uniform construction in the field size.

I inspected the four explicit permutations, the author's deterministic checker,
and the accompanying proof/scope note. I freshly ran the author checker with
GAP 4.15.1 and then ran the independently written
[bitmask checker](phase10_unitary_independent_check.g). The latter indexes
subsets by binary masks, constructs all sixteen subgroups afresh, and checks
all 256 intersections by containment and equal exact orders. It does not use
the author's subset ordering, cached search groups, or parabolic shortcut.
Both runs passed. The [independent run record](phase10_unitary_independent_run.json)
contains the command, output and hashes of the exact inputs.

The tuple consists of four nonidentity involutions, all three distant pairs
commute, and its adjacent product orders are 4, 26 and 10. The generated group
has order 14,742,000,000. GAP reports that it is simple and identifies it as
series 2A, parameter [3,5], namely PSU4(5). Thus, relative to the explicitly
retained exact GAP group algorithms and simple-group recognition, the tuple
is a rank-four string C-group for PSU4(5). This reasoning does not identify
the group from its order alone, and does not identify either rank-three
parabolic from its order alone.

The empty and full generator subsets are included. Containment of the expected
intersection is checked explicitly before comparing orders, so the test is not
an unsupported comparison of subgroup sizes. All permutation computations are
exact. The independent checker uses the same underlying GAP implementation;
it supplies a second program and fresh execution, not an independently
implemented permutation-group engine.

Combining existence with the separate reviewed phase-nine upper bound yields
maximum rank four for this one group. The present certificate neither proves
rank-four existence for every odd PSU4(q) nor establishes historical novelty.
The original ATLAS inputs used during discovery are unnecessary for either
standalone verification. The finite-simple-group recognition remains a
software/theoretical dependency, not a new classification theorem.

Reviewed note snapshot SHA-256:
`296cdec5f51ba2c21525969f9d1ed4a5a37c4028cd588f457b0671d55e462be9`.
The exact witness and checker hashes are in the run record. Later purely
editorial cross-links should be bound in package metadata rather than
misrepresented as new computations.
