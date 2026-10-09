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
checks local documentation links, and checks the fourteen saved Lean reports
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

The weighted-tree extension uses that same NetworkX environment:

```sh
.venv/bin/python research/case_study/phase6_weighted_tree_check.py
```

Its saved run independently checks 89 weighted models against permutation
flag orbits, 741 residual primitivity tests, 84 rank-two models, 35 weighted
claw obstructions, 2,354,462 consecutive-rank shadow queries and 942 tree
contractions. Primitivity is checked by constructing invariant equivalence
relations from permutation generators, independently of the written weight
criterion. Run in a disposable copy to preserve the saved report.

The complete arbitrary-Borel J2 census is reproduced with GAP and TomLib,
without downloading the original geometry archive. Its
[runner instructions](research/case_study/phase5_j2_theory.md#6-reproduction-and-artifacts)
cover enumeration, automorphism fusion, independent witness recognition and
certificate building. All 146 terminal checkpoints are included. Use a
disposable copy for this pipeline too; the original run used GAP 4.15.1 and
TomLib 1.2.11, and its search took about 124 seconds in that environment.

The generalized engine reproduces the broader J1, M11 and M12 censuses:

```sh
python3 research/case_study/phase6_sporadic_run.py J1
python3 research/case_study/phase6_sporadic_finish.py J1
python3 research/case_study/phase6_sporadic_build_certificate.py J1
```

Replace J1 with M11 or M12. In a disposable copy, remove the copied run
outputs first to start a fresh search; `--resume` verifies existing script
and terminal-checkpoint hashes and searches only unfinished anchors. Keep
the distributed originals for comparison. Search times in the recorded
environment were approximately 224, 12 and 159 seconds respectively, with
fusion/verification recorded separately. The
[common theorem](research/case_study/phase6_sporadic_theory.md) documents
catalogue dependencies and exact class/truncation conventions. Optional
archive comparison requires the separately obtained Cambridge supplement;
the original archive was never an enumeration input.

The same pipeline's next configuration covers M22 and M23 with local
two-transitivity imposed:

```sh
python3 research/case_study/phase7_sporadic_run.py M22
python3 research/case_study/phase7_sporadic_finish.py M22
python3 research/case_study/phase7_sporadic_build_certificate.py M22
```

Replace M22 with M23. Follow the
[fresh-copy instructions](research/case_study/phase7_sporadic_theory.md)
before running these commands, since a fresh run refuses an existing
progress record. The saved searches took approximately 325 and 404 seconds.
All 360 anchors terminate, and a separate recognition pass checks all 105
witnesses. Optional source-archive comparison is performed after enumeration;
its input is neither distributed nor required to reproduce the census.

The explicit missing Suzuki lattice has a standard-library-only checker:

```sh
python3 research/case_study/phase6_suzuki_torus_check.py
```

Run in a disposable copy; it imports the two recorded phase-five arithmetic
modules and writes its own report. The rank-three certificate checks all
2,132 elements of its smaller parabolic, rather than enumerating the huge
ambient Suzuki group. Rank-four intersections use exact field arithmetic
and prime-component extraction. Classical subgroup maximality and the
written interpretation remain explicit inputs. The separate
`RankThreeFactorization.lean` certifies the abstract coset argument.

The all-rank Suzuki extension adds exact polynomial checks of the exceptional
endomorphism in the same matrix coordinates, a twenty-element binary seed,
and finite arithmetic checks of the uniform torus formula:

```sh
python3 research/case_study/phase7_suzuki_seed_check.py
python3 research/case_study/phase7_suzuki_binary_audit.py
python3 research/case_study/phase7_suzuki_families_check.py
```

Use a disposable copy. The all-rank proof uses classical Lang–Steinberg
descent and Suzuki subgroup facts; a small seed computation is not presented
as an enumeration of these infinite families. `CosetCoordinates.lean` checks
the abstract attachment lemma under its explicit coordinate hypothesis.
The independently implemented binary audit searches all 65,536 binary
matrices. The family checker tests complete cyclic coordinate maps in three
examples where a selected prime also divides the base torus order, covering
the split and both nonsplit branches.

The metacyclic TPP arithmetic and the separate order-512 group census are
reproduced from a disposable copy as follows:

```sh
cd research/case_study
python3 phase7_cyclic_tpp_arithmetic.py
gap -q phase7_cyclic_tpp_search.g
```

The arithmetic checker uses only the standard library and checks 3,898
faithful cyclic actions and 1,020,498 generator contexts. The GAP run uses
SmallGroups 1.5.4; the library supplies all 2,043 rank-two groups of order512.
Its exhaustion argument retains the frozen smaller-order result. The
metacyclic theorem itself is a written all-parameter proof with independent
internal review, not an inference from either finite computation.

The modular endpoint reductions for PSL₄ use exact symbolic identities:

```sh
python3 research/case_study/phase7_psl4_check.py --output /tmp/psl4-endpoint-check.json
python3 research/case_study/phase7_psl4_zero_product_check.py --output /tmp/psl4-zero-product-check.json
```

This requires SymPy; the recorded run used version 1.14.0. Its 30 checks
verify the displayed algebraic identities. The written proof supplies the
module classification and coverage in odd characteristic, including
characteristic three. The second script verifies 54 identities for the
remaining zero-product cases, completing the written rank-five exclusion.
An independent Smith-form check confirms that the centralizer ranks used
there do not drop in odd characteristic. Rank six is not excluded by these
arguments. The output option preserves the saved reports.

The separate rank-six continuation and its broader bilinear-form theorem use:

```sh
python3 research/case_study/phase8_psl4_rank6_check.py --output /tmp/psl4-rank6-check.json
```

This checks 33 exact identities and all 12 three-endpoint distinguishing
pairs in the displayed normal forms. The complete proposed maximum-rank
proof combines these written reductions with the preceding rank-five and
higher-rank exclusions and the published rank-four existence theorem.
`IntertwinerSeparation.lean` formalizes the abstract commutator obstruction;
the full representation classification is not formalized.

For the pure-subfield and mixed-center Suzuki extension, run in a disposable
copy, since the checker writes adjacent output:

```sh
python3 research/case_study/phase8_suzuki_subfields_check.py
```

The standard-library checker verifies 49,152 matrix identities and nine
proper intermediate groups in one explicit mixed-parabolic example. The
uniform maximality obstruction and the sharp all-rank subfield criterion
are written proofs, with independent mathematical and primary-source review.

## Fresh Lean compilation

The [formal setup and scope document](research/case_study/formal/README.md)
describes all fourteen certificates and their unformalized boundaries. With Git
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

The fourteen certificates cover intersection transport, field and matrix
obstructions, connectivity and chamber orbits, torsor partitions, coordinate
kernels, the Suzuki matrix word, a local string-intersection obstruction,
exact Boolean-shadow witnesses of at most two vertices, and common-coset-point
theorems from factorization or arbitrary-family coordinate coverage.
The latest module also checks an abstract additive-commutator obstruction
to an intertwiner, with no axioms reported for its two theorems.
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
