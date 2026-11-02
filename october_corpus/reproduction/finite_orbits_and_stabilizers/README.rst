Finite orbits and small stabilizers
==================================

A complete finite orbit and a small stabilizer give short certificates for
subgroup orders. This package checks seven such certificates from F004,
job (20, 4), using the original four marked matrices in each case.

Each left end subgroup has an orbit of 3,080 vectors and a stabilizer of
order 57. The checker verifies the complete Schreier equations, stabilizer
closure and membership words, so its order is 3,080 times 57 = 175,560.
It also checks an element of order 19, its one-dimensional fixed space,
and membership of the fourth marked matrix in the subgroup.

Positions 109, 349, 400 and 502 have positive membership tests. Their four
marks therefore generate a proper subgroup of the imported ambient group.
For positions 877, 1033 and 1099, the fourth mark lies outside that subgroup.
The separate argument in PROOF.tex proves generation using an attributed
maximal subgroup classification and the natural module. These three
rank-four intersection properties remain unresolved.

Reproduce the calculations
-------------------------

Use Python 3.11 or newer, with psutil installed for the resource guards.
The arithmetic workers use only the standard library and run with -S.
From the repository root, run::

    python3 -E -B -S october_corpus/reproduction/finite_orbits_and_stabilizers/verify_all.py \
        --output /absolute/path/to/a/fresh/output

Add --python /path/to/a/venv/bin/python to select the interpreter used by
the guards. The output path must not exist. The command runs 33 arithmetic
controls, eight input controls and seven case checks in separate processes.
Use --role controls or --role 877 to run one role into a fresh output path.

Each worker uses the unchanged 128 MiB, 100 second guard, with admission
requirements of 4 GiB available RAM and 10 GiB free disk space. Its arithmetic
and input budgets are listed in the source manifests. Processes run serially;
a failed role stops the command and preserves the earlier output.

Verification and attribution
----------------------------

The private package and the repository package each passed all 41 controls
and seven cases. Their case results agree byte for byte. VALIDATION.json
records the facts and work counts; AUDIT.json records the independent audit.
Each replay has one captured orchestrator and eight guarded workers.

SOURCE_MANIFEST.json and CONTROL_SOURCE_MANIFEST.json identify every loaded
worker file and the shared guards in ../fixed_line_orbits/runtime/.
CASES.json identifies the supplied case files and binary certificates.
All runtime paths are relative to the package; no private workspace is needed.

Schreier decompositions and orbit-stabilizer counting are standard group
theory. THEORY.rst identifies the borrowed results, and PROOF.tex gives the
written argument and references. The authentic original markings, faithful
named model, membership and maximal subgroup classification are explicit
imported premises. The matrix checker establishes the stated finite matrix
facts. This package adds no full census, completed manuscript, conjecture
solution, Lean formalization or compression measurement.
