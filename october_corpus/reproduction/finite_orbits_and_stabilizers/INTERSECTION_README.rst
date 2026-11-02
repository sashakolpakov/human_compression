A word certificate for an intersection obstruction
=================================================

This extension checks the registered exclusion at F004, job 20, position
1099. It uses the four supplied matrices over F11 and preserves the older
seven-case checker.

A word of length 78 in g0, g1 and g2 equals (g1*g2*g3*g2*g3*g2)^2.
Their common value lies outside <g1,g2>, whose order is 10. It therefore
belongs to both end subgroups but not their required intersection. The
argument is given in INTERSECTION_PROOF.rst; the complete matrices and
words are in intersection_cases/position1099.json.

The verifier checks the string involutions, evaluates both words and
computes the complete middle subgroup using full matrix equality. It
requires no subgroup order certificate, discovery search or classification
theorem. The association with the original quartet and the faithful natural
representation remain explicit provenance premises.

Reproduce the result
--------------------

Use Python 3.11 or newer, with psutil installed for the resource guards.
The arithmetic workers use the standard library. From the repository root::

    python3 -E -B -S october_corpus/reproduction/finite_orbits_and_stabilizers/verify_intersection_all.py \
        --output /absolute/path/to/a/fresh/output

The output directory must not exist. Add --python /path/to/python to select
an interpreter. The command runs 24 arithmetic controls, ten input controls
and the case in separate serial processes. Use --role arithmetic,
--role admission or --role 1099 for one role.

Each worker has the existing 128 MiB and 100 second limits. The shared guard
requires 4 GiB available RAM and 10 GiB free disk space. A failed role stops
the command and preserves earlier output.

Validation and scope
--------------------

All controls and the case passed in both private and repository directories.
Their result files agree byte for byte. The case uses 107 matrix products
and 2,113 charged scalar units. INTERSECTION_VALIDATION.json records the
measurements; INTERSECTION_AUDIT.json records the independent review.
Neither the full left subgroup nor its discovery certificate is opened
during this replay.

INTERSECTION_CASES.json identifies the supplied data. The three
INTERSECTION_*SOURCE_MANIFEST.json files identify every loaded worker and
the shared guards. Source and data paths are relative to this package.

This is a new portable proof of an already registered exclusion. It adds
no case, completed manuscript, conjecture resolution, Lean formalization
or compression measurement. Standard facts about word membership,
dihedral groups and the intersection axiom are used; source attribution
and the distinction between discovery and verification are in the proof.
