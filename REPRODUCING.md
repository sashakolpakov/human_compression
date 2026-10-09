# Reproducing the checks

Run these commands from the repository root. Python 3.10 or newer is required
for the public runners. A successful hash check, a fresh computation, and a
Lean compilation establish different things; the commands below keep those
claims separate.

## Snapshot integrity and saved results

```sh
python3 scripts/verify_snapshot.py
python3 research/case_study/formal/verify_lean.py --check-saved
```

The snapshot check compares distributed files with the publication manifest,
checks local documentation links, and checks the ten saved Lean reports
against their source files. The second command checks only those saved Lean
records. Neither command executes Lean or reruns the mathematical computations.
Do not use `--write-manifest` to repair a failed check: that option records a
new publication snapshot rather than verifying the distributed one.

The [provenance note](provenance/README.md) distinguishes original working-file
hashes from the public snapshot. Portability and citation edits can change an
exported file's hash. Historical reports describe their original runs; they
are not relabeled as fresh executions of an edited script.

## Fresh Python computations

```sh
python3 scripts/smoke_check.py --quick
```

This standard-library suite freshly checks all 900 pairs of subgroups of
`S4` in the torsor matrix example, the symbolic Suzuki word identities, and
all eleven exceptional finite-field witnesses. The Suzuki calculation checks
polynomial identities; the other two checks concern the finite inputs stated
in their reports. These are not interchangeable scopes.

For the larger suite, use Python 3.11 or newer and install NumPy in a virtual
environment (the pinned NumPy release requires Python >=3.11):

```sh
python3 -m venv .venv
.venv/bin/python -m pip install numpy==2.4.4
.venv/bin/python scripts/smoke_check.py --full --keep-work-dir
```

The larger suite adds sixteen cyclic-extension congruence systems, 144 small
independent solver checks, and graph counts for `q = 3, 5, 7` using three
constructions and an independent path counter. The modular solver uses exact
integer arithmetic within an explicit overflow guard; NumPy's floating-point
linear algebra is not used. These finite checks corroborate the corresponding
written arguments; they do not alone prove statements for all parameters.

The older-paper checks also use only the standard library:

```sh
python3 scripts/smoke_check.py --older --keep-work-dir
```

This suite checks the semilinear descent example exhaustively over the stated
binary fields, including all 11,811 four-dimensional subspaces containing 1
in `F256`. It compares direct geometric shadow witnesses with the covering
criterion on 682 rank-two structures, all 4,096 structures with three types
of size two, 48 larger examples and 404 induced residues. These are finite
checks of the new 2003/2004 reductions, not a reproduction of the sporadic
classification tables. No end-to-end Lean proof of semilinear descent is
included.

All suites copy their inputs to temporary directories and preserve the
snapshot's reports. `--keep-work-dir` retains fresh reports and logs; a failed
run retains them automatically. Each check has a default 600-second timeout,
adjustable with `--timeout SECONDS`. Do not run certificate scripts with
Python's `-O` option: their mathematical assertions must execute.

Additional scripts beside the notes can be run individually. Several legacy
scripts write JSON or log files beside themselves, so use a disposable copy
when running them directly. Timing fields and environment metadata can differ
between successful runs; compare the mathematical assertions and input hashes,
not just the output-file checksum.

The next older-paper intake adds an independent dihedral subgroup/coset
checker and a tree-cut checker. Run these in a disposable copy because their
JSON reports are written beside the scripts:

```sh
python3 research/case_study/phase5_dihedral_check.py
python3 -m venv .venv
.venv/bin/python -m pip install networkx==3.6.1
.venv/bin/python research/case_study/phase5_tree_check.py
```

Use Python 3.11 or newer for the pinned NetworkX environment. The dihedral
checker uses only Python's standard library and constructs all
subgroups from multiplication for its 18 stated groups. NetworkX supplies
nonisomorphic trees to the second checker; group closure, flag enumeration,
permutation orbits and shadow witnesses are checked separately. The saved
tree run checks 24 trees, 262 generated subgroups, 28,324 flag comparisons
and 1,519,962 Boolean shadow queries. These finite audits accompany the
written all-parameter arguments.

The complete arbitrary-Borel J2 census is reproduced with GAP and TomLib,
without downloading the original geometry archive. Its
[runner instructions](research/case_study/phase5_j2_theory.md#6-reproduction-and-artifacts)
cover enumeration, automorphism fusion, independent witness recognition and
certificate building. All 146 terminal checkpoints are included. Use a
disposable copy for this pipeline too; the original run used GAP 4.15.1 and
TomLib 1.2.11, and its search took about 124 seconds in that environment.

## Fresh Lean compilation

The [formal setup and scope document](research/case_study/formal/README.md)
describes all ten certificates and their unformalized boundaries. With Git
and Lean's `elan` toolchain manager installed:

```sh
cd research/case_study/formal
lake exe cache get
python3 verify_lean.py --check-env
python3 verify_lean.py --all
```

The supplied toolchain pins Lean 4.32.2; the Lake manifest pins mathlib commit
`905b95818eb32af7874a58b427f50c1711a5e96c` and all transitive dependencies.
The cache command needs network access. The runner can instead use an existing
built dependency checkout through `--packages PATH` and a compiler through
`--lean PATH`; equivalent environment variables are documented in the formal
README. No original developer's filesystem paths are required.

The runner checks dependency Git revisions and tracked-file cleanliness, then
compiles the selected certificates in dependency order. Fresh reports and
compiled modules go to `formal/.verification/`; historical `.check.json`
files are preserved. The compiled dependency cache and the Lean toolchain are
trusted inputs. Revision checking does not independently authenticate cached
binaries or reproduce a clean build of the toolchain.

The ten certificates cover intersection transport, field and matrix
obstructions, connectivity and chamber orbits, torsor partitions, coordinate
kernels, the Suzuki matrix word, a local string-intersection obstruction,
and exact Boolean-shadow witnesses of at most two vertices.
They formalize the stated components, not the complete geometric
instantiations, all source-group classifications, or every written theorem.
The saved successful runs report no `sorryAx` dependency.

## GAP computations and retained catalogues

GAP runs use exact finite group computations. For example, in a disposable
repository copy, from its root:

```sh
gap -q research/case_study/phase3_256_census.g
gap -q research/case_study/phase3_suzuki_probe.g
```

The first reruns the exhaustive order-256 marked-group census used by the
[eight-family classification](research/case_study/phase3_classification.md).
Its recorded environment is GAP 4.15.1 with SmallGroups 1.5.4; its successful
output has 1,651 eligible groups, 1,641 active groups, and 92 anchored valid
triples in four patterns. Exhaustiveness depends on the completeness of the
SmallGroups catalogue and the reduction proved in the note. It does not
rederive that external catalogue.

The second constructs the Suzuki graph at `q = 8` and checks its 520 vertices,
valency 8, and edge-cycle counts `0, 0, 7` in lengths 3, 4, 5. This is a finite
geometric check separate from the universal symbolic identities and the Lean
word certificate. Other GAP scripts may require additional packages such as
GRAPE or TomLib; their source headers and accompanying reports specify the
inputs used. The `research/leemans` compatibility symlink preserves historical
relative paths in these scripts.

For the 2002 classification track, see the exact commands and source-archive
link in [the J2 note](research/case_study/phase4_old_classification.md). Its
fresh pipeline verifies source representatives, independently enumerates thin
geometries through exhaustion, fuses automorphism/type classes, identifies the
source group explicitly, and checks the generated thin witnesses. Run it in a
disposable copy: it writes intermediate data and reports. The complete subgroup
catalogue is a retained input; this older pipeline does not reprove nonthin
completeness. The arbitrary-Borel phase-five pipeline above now supplies
that exhaustion independently of the source geometry lists.

## External sources and review boundaries

The recovered 2004 publisher archive contains historical maximal-parabolic
data. Its checksum and member hashes are in the source metadata; the archive
is not distributed or executed. Dataset rank labels alone do not establish
that its contents reproduce an earlier classification. The old-paper notes
record any verified differences in scope.

Third-party PDFs, extracted or OCR full texts, publisher-page renderings,
dependency caches, and external GAP library distributions are not bundled.
[Source-asset metadata](research/case_study/sources/source_assets.json) and the
notes retain primary-source links and available checksums. The checks above
use the included mathematical code and witness data; literature retrieval
scripts require separately obtained sources and are not an offline
reproduction of the entire literature search. A source checksum identifies
bytes, not their redistribution rights or the truth of a mathematical claim.

Written proofs, computations, internal agent reviews, and formal certificates
are labeled separately throughout the notes. Internal reviews are not external
peer review. Reproduction verifies the stated checks and their assumptions;
it does not establish research priority or resolve unaddressed conjectures.
