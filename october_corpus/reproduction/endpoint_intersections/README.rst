An intersection obstruction in G2(11)
=====================================

This package verifies the finite certificates for position 2352 of job 24,
with representative J-index 7302. Write the original generators as
``a, b, c, e``. The certificates establish that ``<a,b,c>`` acts
irreducibly on the natural seven-dimensional space, has order at least
12,100, and contains an element of order four. They also establish
``|<b,c,e>| = 1,742,400`` and ``|<b,c>| <= 24``.

The published subgroup classification then gives ``<a,b,c> = G2(11)``.
Consequently its intersection with ``<b,c,e>`` is larger than ``<b,c>``:
the rank four intersection property fails. The `full proof <PROOF.rst>`_
states the natural-model and membership premises and attributes the
classification and module facts used. The arithmetic program checks the
finite identities; the classification is a cited mathematical input.

The checker uses only the Python standard library. From the repository root::

  cd october_corpus/reproduction/endpoint_intersections
  run_dir=$(mktemp -d)
  python3 -E -B -S verify.py data/case_2352.json \
    --source-sha256 a722ff8f83152c0771a8eae0e7749a616c98d23cb818c87e3d31f5434d8a3303 \
    --case-sha256 3edfcf5cde16dc85fad8905508512ce5e635a60bb27ddfd5ffd0e6531251a898 \
    --out "$run_dir/result"
  python3 -E -B -S controls.py \
    --source-sha256 a722ff8f83152c0771a8eae0e7749a616c98d23cb818c87e3d31f5434d8a3303 \
    --out "$run_dir/controls"

Both commands require fresh output directories. No private working files,
external algebra system, or compiled project dependency is needed.

The finite check covers all 37 relevant projective lines, seven independent
word images for each line, 3,025 distinct reached vectors, the literal word
``(bc)^3`` of order four, and the complete right subgroup calculation.
For the latter it checks all 3,960 orbit edges and Schreier loops and a
closed stabilizer of order 1,320. The stored point prefix on the left is
used only for a lower bound and need not be closed.

`REPLAY.json <REPLAY.json>`_ records successful checks before and after
installation in the repository, together with all 29 component controls.
The complete case replay took about 0.8 seconds and 27 MB on the validation
host. Results on other machines may differ. The external resource guards
used for these recorded runs are shared with
``../fixed_line_orbits/runtime/``; the direct command above has its own
cooperative limits.

The classification is due to Kleidman; Nguyen's proof of Theorem 4.4
records the complete list before the character-degree exclusions. Wilson
provides the natural module descriptions. The projection, cyclic span,
orbit-stabilizer, Schreier and dihedral arguments are standard algebra.
This package contributes the particular certificates and their verification.
See `EVIDENCE.json <EVIDENCE.json>`_ for references and the scope of the
proof. This case adds neither a completed manuscript nor a Lean proof.
