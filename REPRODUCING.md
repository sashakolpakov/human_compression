# Reproducing the checks

The current mathematical writing target is [U plus application modules](MANUSCRIPT_PROGRAM.md).
Existing exact computations and Lean components below are reusable proof
material. The latest public-only replays are documented in the
[five-family cover result](COVER_FIVE_FAMILIES.md#attribution-and-reproduction)
and [commuting-pair source compilation](COMPRESS_13.md#correction-verification-and-cost).
A certificate applies only to its stated theorem and hypotheses.

Run these commands from the repository root. Python 3.10 or newer is required
for the public runners. A successful hash check, a fresh computation, and a
Lean compilation establish different things; the commands below keep those
claims separate.

## Covers with enlarged ends

The [Γ2 theorem](COVER_ENLARGED_ENDS.md) has a standard-library finite
checker. Use new output directories:

```sh
python3 -O research/case_study/phase102_expanded_end_covers_check.py --expected-certificate research/case_study/phase102_expanded_end_covers_certificate.json --output-dir /tmp/enlarged-cover-replay
python3 -O research/case_study/phase102_expanded_end_covers_controls.py --successful-replay-dir /tmp/enlarged-cover-replay --output-dir /tmp/enlarged-cover-controls
```

The first command rebuilds the fixed group, affine action, complete kernel
spaces and all necessary recursive intersections, then compares the
generated certificate byte for byte. The second checks six altered inputs
and refuses three occupied outputs. Both work from distributed files.

The [independent checker](research/case_study/phase104_expanded_end_review_check.py)
uses different finite-field arithmetic and checks all 136 subset pairs.
Its outer manifest also verifies the original private primary sources and
one unexported context-only note. A complete replay therefore requires the
recorded original study tree, supplied explicitly:

```sh
python3 -O research/case_study/phase104_expanded_end_review_check.py --study-root /path/to/original-study --output-dir /tmp/enlarged-cover-independent
```

The saved independent report and [fresh root rerun](research/case_study/phase111_expanded_end_root_admission.md)
are public. Neither finite checker proves the all-parameter pullback,
minimal-descendant interpretation or historical novelty; those boundaries
are stated in the written theorem and independent review. The separate
OddCoverSeparation Lean component formalizes only its general algebraic
statements.

## Snapshot integrity and saved results

```sh
python3 scripts/verify_snapshot.py
python3 research/case_study/formal/verify_lean.py --check-saved
```

The snapshot check compares distributed files with the publication manifest,
checks local documentation links, and checks the forty-three saved Lean reports
against their source files. The second command checks only those saved Lean
records. Neither command executes Lean or reruns the mathematical computations.
Do not use `--write-manifest` to repair a failed check: that option records a
new publication snapshot rather than verifying the distributed one.

The [provenance note](provenance/README.md) distinguishes original working-file
hashes from the public snapshot. Portability and citation edits can change an
exported file's hash. Historical reports describe their original runs; they
are not relabeled as fresh executions of an edited script.

## Continuous twelve-source replacement

The latest [twelve-source edition](COMPRESS_12.md) has a public structural
verifier and complete new mathematical replay:

```sh
python3 research/case_study/phase78_n009_integration_verify.py \
  --output /tmp/human-compression-twelve-structure.json \
  --run-new-gap /tmp/human-compression-twelve-mathematics
```

Both output paths must be new. The verifier checks 120 proof spans,
preservation of 87 previous adapters and 19 complete sections, and all eight
printed program/data blocks. The new computation uses GAP 4.15.1 and NQ
2.5.11 in the recorded run. Its complete kernel census and raw-presentation
recognition use only public inputs and took 88.6 seconds in the root replay.
The optional `--primary-check` needs private primary snapshots and is omitted
above. The independent review's separate checker additionally reparses those
snapshots; they are not distributed. The assembly builder writes output files
and should be run only in an isolated copy. Old programs are not rerun by this
command. None of these executions constitutes a Lean proof of the manuscript.

The [twelve-source annotation edition](ATTRIBUTION_12.md) has a separate
public regeneration and independent proof-byte recovery check:

```sh
python3 -O research/case_study/phase91_n009_annotations_controls.py \
  --output-dir /tmp/human-compression-twelve-annotation-controls
python3 -O research/case_study/phase94_twelve_annotations_review_check.py \
  --output /tmp/human-compression-twelve-annotation-check.json
```

Use new paths. Python and Pandoc suffice; no primary captures are needed.
The complete controls regenerate both readers, reject altered inputs and
existing outputs, and check 41 Lua margin commands. The separate checker
imports no author annotation code. The exact historical planning file is
distributed because the frozen checker validates that manifest binding too.
These are annotation integrity checks, without a new census, Lean build or
PDF layout review.

## Earlier continuous replacements

The successor [eleven-source edition](COMPRESS_11.md) has a standalone runner:

```sh
python3 research/case_study/phase75_eleven_source_verify.py \
  --output-dir /tmp/human-compression-eleven-new --run-petrial
```

Python's standard library is sufficient. The runner validates all 87 proof
spans, the 73 unchanged and six citation-corrected predecessor spans, 19
unchanged sections and all five complete programs. The optional flag runs
seven exact Petrial controls with assertions enabled. It preserves the
executed program, raw logs and results in the new directory. Private source
captures are not required; mathematical and primary-source review remain
the separate [independent audit](research/case_study/phase70_petrial_integration_recent_audit.md).
The [wrapper review](research/case_study/phase77_eleven_wrapper_recent_audit.md)
checks an isolated public-input tree, no-clobber and altered-input rejection.
The unchanged earlier GAP programs are not rerun by this command.

The following command reproduces the preceding ten-source edition:

```sh
python3 research/case_study/phase45_ten_source_verify.py --output-dir /tmp/human-compression-ten-structure
```

Choose an output directory that does not exist. This verifies the 79 contract
spans, unique equation labels and exact extraction of all four embedded GAP
programs. It does not check mathematical proofs or execute GAP. The
[independent full-text review](research/case_study/phase52_ten_source_recent_audit.md)
and [root admission](research/case_study/phase56_ten_source_root_audit.md)
record the written proof review and previous exact computational evidence.
Read the [required erratum](research/case_study/phase45_ten_source_errata.md)
with the original manuscript.

For a fresh execution of all four programs, use another new output directory
and add `--run --gap gap`. The original runs used GAP 4.15.1, SmallGroups and
TomLib; the full exhaustive J1 stage can take several minutes. All extracted
programs and logs are retained in that new directory. The independent
`phase52_ten_source_recent_audit_check.py` is a historical source-continuity
checker that also requires the private primary captures identified by hash;
it is not the public reproduction entry point.

The [eleven-source attribution reader](ATTRIBUTION_11.md) reproduces with:

```sh
python3 -O research/case_study/phase79_eleven_attribution_generate.py \
  --output-dir /tmp/human-compression-eleven-reader-new
```

It preserves all proof bytes and checks the 35 notes and their evidence
bindings. Its [independent review](research/case_study/phase85_eleven_attribution_recent_audit.md)
separately assesses the meanings of those notes. No new PDF or mathematical
proof check is performed by this presentation command.

The earlier [ten-source attribution reader](ATTRIBUTION.md) has its own standard-library generator
and [independent semantic/integrity audit](research/case_study/phase62_attribution_recent_audit.md).
Its signs do not add proof premises or broaden any certificate's scope.

The [complete C measurement](research/case_study/phase60_compress_C_measurement_recent_audit_report.md)
is distributed with its exact authored replacement PDF and independent recount
program. Its full rerun requires separately acquired primary PDFs at the bound
hashes, plus pypdf 6.13.0, Pandoc, XeLaTeX and the recorded fonts. The original
protocol builder also expects private source-extraction files. The report gives
the exact render/count commands and exclusion intervals; no standalone public
remeasurement without those primary inputs is implied. The approved outcome
is 2.386% expansion, with the entire required lattice bridge charged.

The [ten-source measurement](research/case_study/phase63_ten_source_measurement_recent_audit_report.md)
has a separate 49-page authored PDF and independent recount program. Its
full replay likewise requires the exact primary PDFs, prior bound protocols,
pypdf 6.13.0 and the recorded rendering tools and fonts. The approved
lower bound is 51,739/30,957, with N001 credited zero and the full required
reference erratum included. It does not measure the annotated reader.

The [eleven-source measurement review](research/case_study/phase88_eleven_measurement_review_report.md)
adds a 57-page authored PDF and a separate independent recount program,
`research/case_study/phase88_eleven_measurement_review_check.py`. Its full
replay requires the exact privately acquired primary PDFs, bound earlier
protocols and all 57 replacement rasters, together with the pinned tools.
These primary captures and rasters are not distributed. The public report
records a fresh root replay of all 132 input bindings, extraction and
counting checks. The approved bound is 51,739/34,845, with N001 and L108
credited zero. It measures all five programs and the complete unannotated
proof; the accompanying metadata erratum changes no count.

The [twelve-source measurement](research/case_study/phase103_twelve_measurement_review_audit.md)
has a portable independent check that needs only the public tree and pypdf:

```sh
python3 -O research/case_study/phase103_twelve_measurement_review_count.py \
  --replacement-only --output /tmp/human-compression-twelve-count-new.json
```

It validates all frozen export/dependency bindings and recounts the exact
83-page authored PDF, checking all 26 sections, eight full programs, all
14 rendered code blocks and unchanged math/table nodes. Omit
`--replacement-only` only after acquiring the ten primary PDFs at the exact
protocol paths; that mode independently re-extracts the numerator and
reproduces all sensitivities. Full rendering is separately available via
`phase98_twelve_measurement.py --output-dir NEW --rasterize` with its declared
toolchain and primary inputs. Existing outputs are refused. The
[root admission](research/case_study/phase106_twelve_measurement_root_admission.md)
records fresh public-only and full-primary counter runs; it does not claim
a third complete visual/render review.

## Two-primary covers and exact integer obstruction

```sh
python3 research/case_study/phase80_two_primary_verify.py \
  --gap /path/to/gap --output-dir /tmp/human-compression-two-primary-new
```

This public runner needs Python and stock GAP 4.15.1. It verifies the 128-point
model and all 55 integer terms, then runs the three unchanged GAP programs:
eight construction checks, the complete degree-two/four census at β=5 with
signs (+,+), and eight source-binding checks for the integral obstruction.
It checks all 33 distributed input bindings before and after execution, keeps
the three executed programs and raw logs, and compares both combined logs
with the reviewed originals. Existing output paths are refused. Primary
captures and historical wrappers are unnecessary. The uniform parameter
reduction remains a separately reviewed written proof; this is no Lean build.
See [the exact theorem scopes](COVER_TWO_PRIMARY.md).

The stronger obstruction for arbitrary finite odd kernels has a separate
replay, using the pinned Lean packages:

```sh
python3 -O research/case_study/phase83_nonabelian_cover_check.py \
  --packages /path/to/pinned/packages --lean /path/to/lean-4.32.2 \
  --output-dir /tmp/human-compression-odd-kernel-new
```

It verifies the actual cell orbit, regenerates the elementary elimination
trace and exact Lean source, then compiles both word/cardinality theorems.
The independent review supplies separate implementations of the complete
111-step trace and the 35-cell subproof. The written family transport and
geometric recognition remain necessary; read the manuscript with its
[required correction](research/case_study/phase83_nonabelian_cover_erratum.md).

## Universal completion and the exact two-cover classification

The [completion theorem](COVER_COMPLETION.md) has three public checks using
only Python's standard library. Choose new output paths for every command:

```sh
python3 -O research/case_study/phase92_complement_normal_form.py \
  --expected-certificate research/case_study/phase92_complement_normal_form_certificate.json \
  --output-dir /tmp/human-compression-completion-new
python3 -O research/case_study/phase96_universal_complement_review_check.py \
  --output /tmp/human-compression-bridge-new.json
python3 -O research/case_study/phase97_complement_normal_form_review_check.py \
  --output /tmp/human-compression-completion-independent-new.json
python3 -O research/case_study/phase92_complement_normal_form_controls.py \
  --successful-replay-dir /tmp/human-compression-completion-new \
  --output-dir /tmp/human-compression-completion-controls-new
```

The first regenerates the exact free-product isomorphism, marked action,
tree and binary affine certificate. The second independently checks graph
and square conventions on two finite models. The third independently
checks the normal form and explicitly enumerates the whole 4,096-element
affine group, its ends and unique invariant kernel line. The controls reject
seven altered inputs and refuse three occupied output paths. The
[root replay](research/case_study/phase101_completion_root_admission.md) passed
all four commands from these public files. Uniform parameter transport and
the complete cover classification require the separately reviewed written
proofs. This adds no full-theorem Lean claim and needs no primary PDF.

## Odd-degree quotient separation in Lean

The [scoped separation certificate](research/case_study/formal/OddCoverSeparation.scope.md)
has a public independent replay with pinned compilation and interface controls:

```sh
python3 -O research/case_study/phase107_odd_cover_formal_review_check.py \
  --packages /path/to/pinned/packages --lean /path/to/lean-4.32.2 \
  --output-dir /tmp/human-compression-odd-cover-separation-new
```

It copies only the exact author wrapper, Lean source and dependency manifest
to an isolated directory, compiles all six statements, compares complete
axiom logs, rejects three occupied outputs and two altered inputs, and
rechecks every original binding. It requires no family construction or
primary publication. The general kernel and finite-maximality conclusions
do not formalize a polytope predicate or prove a specific cover exists.

## Odd-prime cover-family diagnostics and formal separation

```sh
python3 research/case_study/phase67_cover_family_verify.py \
  --gap /path/to/gap --output-dir /tmp/human-compression-cover-family-new
python3 research/case_study/formal/verify_lean.py CoverCharacterSeparation.lean \
  --packages /path/to/pinned/packages --lean /path/to/lean \
  --output-dir /tmp/human-compression-cover-character-new
```

The first command uses stock GAP 4.15.1 and the distributed program, theorem
and independent review. It rebuilds eight finite examples from exact
presentations and preserves raw logs. An existing output directory is rejected.
The public replay completed in about 71 seconds. The all-parameter theorem
is a separately reviewed written proof; these are finite diagnostics.

The second compiles three algebraic declarations using pinned Lean 4.32.2
and mathlib. It verifies the inversion-versus-fixed kernel obstruction to a
marked isomorphism, including the odd-prime-order specialization. Family
existence, kernel actions and geometry remain written inputs; see the
[exact scope](research/case_study/formal/CoverCharacterSeparation.scope.md).

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

The subsequent linear/unitary application has two independent standard-library
checkers. Both accept fresh output paths:

```sh
python3 research/case_study/phase9_linear_unitary_check.py --output /tmp/linear-unitary.json
python3 research/case_study/phase9_torus_character_audit.py --output /tmp/torus-characters.json
```

The 45 integer character comparisons certify separation for every torus
exponent at least three. The finite matrix-unit checks verify universal
entry identities. The written proof supplies the group-theoretic deductions;
`TransvectionForms.lean` independently checks actual transvection matrix
invariance, without formalizing the full rank theorem.

For the first proof-length measurement, obtain the primary PDF linked in
[the measurement protocol](research/case_study/phase9_L066_measurement_protocol.json)
and use its declared extractor version `pypdf==6.13.0`:

```sh
python3 research/case_study/phase9_L066_measure.py \
  --source-pdf /path/to/Involutions.pdf --output /tmp/L066-measurement.json
```

The script checks the PDF, extracted-text and selected-span hashes before
counting. It reproduces the matched two-formula comparison, its optional
source-span sensitivity and marginal costs. It outputs counts and hashes,
not the source text. This is a measurement, not a proof checker; the
replacement argument and independent source-span review are separate files.

For the pure-subfield and mixed-center Suzuki extension, run in a disposable
copy, since the checker writes adjacent output:

```sh
python3 research/case_study/phase8_suzuki_subfields_check.py
```

The standard-library checker verifies 49,152 matrix identities and nine
proper intermediate groups in one explicit mixed-parabolic example. The
uniform maximality obstruction and the sharp all-rank subfield criterion
are written proofs, with independent mathematical and primary-source review.

The marked-field Suzuki derivation has two complementary checks:

```sh
python3 research/case_study/phase10_suzuki_marked_fields_check.py --output /tmp/suzuki-fields.json
gap -q -T research/case_study/phase10_suzuki_marked_groups_check.g
```

The Python checker compares both counting formulas in 49 odd degrees and
exhausts the normalized coordinate pairs over fields of sizes 8, 32 and 512.
The GAP checker uses actual Suzuki matrices at q=8: all 42 normalized triples
generate the group, all 2,688 ordered subgroup intersections hold, and all
42 duality identities hold by diagonal conjugation. The all-parameter
generation and counting arguments remain written proofs with explicit
classical group-theoretic inputs.

The new small-factor cyclic-TPP check uses only the standard library:

```sh
python3 research/case_study/phase10_cyclic_tpp_check.py --output /tmp/cyclic-tpp.json
```

Its 48 normal-form models have ambient orders through 8,192. It checks 48,336
elements in the specified Frattini classes, 386,688 swap equations and
1,966,080 associativity equations. Full associativity is exhausted only for
n≤8; larger parameters use generator-local equations. This is neither a
census of all groups through order 8,192 nor a proof of the retained marked
isobicyclic classification. The written argument proves the small-factor
case uniformly; it is now subsumed by the complete proposed phase-fourteen
theorem below.

For the finite unitary example, run from the artifact directory:

```sh
cd research/case_study
gap -q -T phase10_unitary_matrix_check.g
```

This checker reads only the four explicit matrices in the accompanying
witness file. It verifies the field convention, determinant-one Hermitian
isometries, isotropic-plane orbit, exact projective order, string relations,
type {4,26,10} and all 256 subgroup intersections. Identification uses
unitary containment and the standard order formula. No ATLAS file or
simple-group recognition is required. The older permutation certificate
and its independently implemented bitmask check are also retained, with
their different identification dependencies recorded.

## Frattini actions and the unitary template

The phase-eleven finite action checks use Python's standard library. From
the repository root, write fresh reports outside the saved artifact names:

```sh
python3 research/case_study/phase11_binary_action_check.py --output /tmp/binary_action.json
python3 research/case_study/phase11_abelian_frattini_independent_check.py --output /tmp/frattini_independent.json
python3 research/case_study/phase11_odd_norm_independent_check.py --output /tmp/odd_norm.json
python3 research/case_study/phase11_cyclic_tpp_check.py --output /tmp/cyclic_structure.json
```

The first two independently encode the binary lemma; the second also checks
bounded unequal-exponent lifting. The third exhausts the F3 norm equations:
2,187 solutions in 81 action pairs. The last checks 46 retained normal-form
models and 96,640 outside elements. None enumerates all finite p-groups or
formalizes the group-theoretic induction. The shorter all-odd-prime proof
does not depend on these finite action checks.

Three standalone GAP witnesses make the limitations concrete:

```sh
gap -q -T research/case_study/phase11_tpp_equality_witness.g
gap -q -T research/case_study/phase11_rank3_equality_witness.g
gap -q -T research/case_study/phase11_odd_nonnilpotent_witness.g
```

These require SmallGrp. The first two show that TPP and equality of the
factor-order product with group order do not imply an injective global
product map. The third gives a cyclic TPP triple of orders 3,3,3 in a
nonnilpotent group of order 21. These are individual witnesses, not censuses.

For the unitary matrices, run the two Python scripts in a **disposable copy**
of the artifact directory: they require SymPy and write adjacent JSON reports.
Then run the GAP checker from that copy:

```sh
python3 phase11_unitary_template_check.py
python3 phase11_unitary_intersection_check.py
gap -q -T phase11_unitary_examples_check.g
```

The Python scripts verify 33 generation identities and 14 intersection-proof
identities or checks. They do not certify the retained rank-one subgroup
theorem or the complete group argument. GAP constructs the natural action
on isotropic two-spaces and verifies the full projective-unitary order,
all 16 subset groups and all 256 intersections for each of four markings.
Three give C-groups at q=5,9,13; the negative control at q=9 has exactly two
failed ordered intersection checks. No external group-generator database
or simple-group recognition is used. Compare mathematical fields in the
saved reports; timestamps and runtimes vary.

## Phase-twelve uniform proofs and focused checks

The following commands run the new original diagnostics. As with the
earlier commands, use a disposable repository copy to preserve the
distributed reports. Python checks use the standard library except the
unitary arithmetic script, which also uses SymPy. The two presentation
checks and the class-three collection check need GAP with NQ.

```sh
python3 research/case_study/phase12_path_cocycle_check.py
gap -q research/case_study/phase12_hou_schulte_independent.g
gap -q research/case_study/phase12_class_three_check.g
python3 research/case_study/phase12_power_layers_check.py
gap -q research/case_study/phase12_rank32_check.g
python3 research/case_study/phase12_N003_check.py --output phase12_N003_fresh.json
python3 research/case_study/phase12_unitary_parameters_check.py
gap -q research/case_study/phase12_unitary_parameters_check.g
```

The path checker exhausts ranks 2–6: 299,584 cocycle comparisons and
5,456 standard subgroup intersections. The independently constructed
rank-four NQ witness gives order 128 and Frattini orders 4,8,4, exposing
the exact 2026 kernel discrepancy. The adjoining written proof establishes
the all-rank family and states which source claims it contradicts.

The class-three script checks the collection identities in the free
torsion-free nilpotent group, plus the order-4096 boundary example. The
power-layer scripts check the small linear action lemma, the order-32
presentation and an explicit failed shortcut. Their uniform group
conclusions rely on the separately reviewed proofs and retained inputs.

The 2002 checker constructs actual permutation closures and cosets. It
checks 716 markings, 11,124 subset groups, 182,672 intersections and
369,093 typed partial flags. It also verifies the three counting formulas
for n=3,…,6 and 44,696 permutation-module triples. This is a diagnostic
for the forest/parity proof, not verification of Whiston's inputs or an
exhaustion of the all-n classification.

The unitary arithmetic check proves the seven small-exponent inequalities
and the uniform divisor-bound constant by exact integers, alongside the
symbolic identities. GAP tests every one of 7,376 nonzero parameters in
four sample fields, obtaining counts 8,64,456,4800, and directly checks
a chosen middle matrix's order and square field in each. The character
bound proving existence for all q=9^e remains a written argument with
precise retained cohomological inputs.

Fresh root outputs are separate files. Deterministic reports match their
frozen counterparts; the unitary arithmetic timestamp differs, and its
raw GAP log differs only in the initial blank line's CRLF/LF encoding.
[The phase-twelve review](provenance/phase12_review.md) binds the exact
review and execution scopes. All seventeen earlier Lean reports are
preserved; this phase does not add a Lean module.

## Phase-thirteen field and structural certificates

The independent unitary checker requires only Python's standard library.
It reads the included polynomial-coordinate witnesses and writes a new report
at the specified output path, preserving the saved report:

```sh
python3 research/case_study/phase13_unitary_independent_check.py --output phase13_unitary_fresh.json
python3 research/case_study/phase13_cyclic_tpp_check.py > phase13_cyclic_tpp_fresh.json
python3 research/case_study/phase13_cyclic_tpp_top_action_check.py > phase13_top_action_fresh.json
gap -q research/case_study/phase13_common_quotient_check.g > phase13_common_quotient_fresh.log
```

The first command independently reconstructs all 4,795 eligible fields
below 98,660 and the exact 406-field exception list. It verifies every
field polynomial's irreducibility, all coordinate and order conditions,
and the actual special-unitary matrix and its projective order. The
large-field curve and character-sum estimates remain written arguments;
the checker does not replace the retained generation or intersection
proofs. The q=5 witness correctly has a nonidentity scalar at its
projective order.

The second checks the one- and two-dimensional action lemma, its
three-dimensional boundary, and the retained order-256 input hashes.
It does not rerun the historical SmallGroups census. The new bound
through order 1024 follows from the structural theorem. The separate
top-action check exhausts 100 two-group image pairs and 38 third-coset
cases in GL₃(F₂), finding the single surviving marked action. This
necessary condition does not exclude a counterexample.

The GAP/NQ command checks 70 collection formulas at ranks two through
six, and all 1,344 subset intersections in the complete stated
rank-three quotient diagnostic. Root's fresh transcript matches the
saved log after newline normalization; only its initial CR/LF differs.
The all-rank support proof is independent of this finite diagnostic.

To rerun the author unitary checks, use a disposable copy of the repository:

```sh
python3 research/case_study/phase13_unitary_elliptic_check.py
python3 research/case_study/phase13_unitary_sieve_check.py
gap -q -T research/case_study/phase13_unitary_witnesses.g
```

The first requires SymPy; the second uses the standard library. These
scripts preserve their original report-writing behavior, so a disposable
copy avoids replacing historical reports. The GAP script prints the
coordinate witnesses and per-field checks to standard output; the included
JSON is the recorded coordinate package checked by the independent runner. The [phase-thirteen review](provenance/phase13_review.md)
separates author checks, fresh independent arithmetic, written reviews,
and retained mathematical inputs. No new Lean module is added.

## The complete cyclic-TPP proof and the q=7 witness

The [phase-fourteen theorem](research/case_study/phase14_cyclic_tpp.md)
is an all-parameter written proof, with two independent internal reviews.
It uses the specified powerful-group theorems and elementary group facts;
there is no new finite census to run. Its partial formal component can be
freshly compiled using the pinned setup below:

```sh
python3 research/case_study/formal/verify_lean.py MarkedSquareDescent.lean
```

The runner first compiles its `BinaryFrattiniActions` dependency. The new
module checks the finite action classification and the final abstract
fixed-coordinate obstruction. It does not formalize the entire group or
geometric proof. The two fresh public compilation reports and their
review boundaries are linked from the [phase-fourteen review](provenance/phase14_review.md).

The independent q=7 unitary witness has a short exact GAP check. From a
disposable directory, copy the checker and execute it there:

```sh
mkdir -p /tmp/math-compression-q7
cp research/case_study/phase14_unitary_q7_check.g /tmp/math-compression-q7/
cd /tmp/math-compression-q7
gap -q -T phase14_unitary_q7_check.g
```

It writes `phase14_unitary_q7_check.json` in the working directory.

## Graded support and the second matched measurement

The [all-class forest theorem](research/case_study/phase15_graded_support.md)
is a written proof, with two complete internal reviews bound by its
[certificate](research/case_study/phase15_graded_support_certificate.json).
Its graded Lie and descending-factorization steps do not depend on the
earlier class-four diagnostics or a finite census.

The separate permutation witness shows that a last lower-central quotient
can lose the intersection property. Its standard-library verifier closes
the supplied permutations, constructs actual commutators and checks every
original and relevant quotient subgroup intersection:

```sh
python3 research/case_study/phase15_quotient_ip_verify.py \
  --output /tmp/quotient-ip-fresh.json
```

The [N003 measurement](research/case_study/phase15_N003_measurement.md)
uses the exact twelve-page primary PDF identified by the protocol. Obtain
it separately and use `pypdf==6.13.0`:

```sh
python3 research/case_study/phase15_N003_measure.py \
  --source-pdf /path/to/igsgsn.pdf \
  --output /tmp/N003-measurement-fresh.json
```

This freshly extracts the PDF, verifies the full text and every selected
span hash, and recomputes 9,680/7,260=4/3. It does not verify mathematical
correctness; that has a separate complete written review. A second
[accounting implementation](research/case_study/phase15_N003_scope_check.py)
uses the bound extraction, without importing the first runner. To reproduce
it, copy the `phase15_N003_*` files into a scratch directory and
put the exact PDF at `sources/network_independent_generators.pdf` and its
page-labelled extraction at `sources/phase10_N003_extracted.txt` there.
The extraction convention is specified in the first runner. Then run
the second script with `--directory /path/to/scratch --output /tmp/N003-scope.json`.
Neither primary source nor extracted publication text is redistributed.

The optional historical class-four diagnostics need GAP with NQ. Copy
`phase15_common_quotient_check.g` to scratch space and run it with
`gap -q -T phase15_common_quotient_check.g`. It checks universal collection
in ranks two through six and all relevant quotients of the computed
rank-three group. The separate uniform forest proof supersedes that
class restriction and uses none of these finite checks as a premise.

## Completing the second unitary family

The [uniform proof](research/case_study/phase15_unitary_sieve.md) combines
written generation/intersection and curve bounds with complete finite
arithmetic. The [independent audit](research/case_study/phase15_unitary_independent_audit.md)
and [author manifest](research/case_study/phase15_unitary_manifest.json)
record their different trust boundaries. Run the two independent
standard-library checks directly from the public copy:

```sh
python3 research/case_study/phase15_unitary_sieve_independent_check.py \
  --output /tmp/unitary-sieve-fresh.json
python3 research/case_study/phase15_unitary_witnesses_independent_check.py \
  --output /tmp/unitary-witnesses-fresh.json
gap -q -T research/case_study/phase15_unitary_example_check.g > /tmp/unitary-q11-fresh.log
```

The first recomputes the three cutoff bounds, all 40,389 field sizes,
80,778 factorizations and the complete set of 1,699 exceptions. The second
checks that same exception list using the saved, hash-bound independent
sieve record, then rebuilds every polynomial field and verifies all 1,697
primitive norm witnesses and the direct q=19,23,43 parameters. It imports
neither GAP nor an author checker. The final command separately constructs
the full q=11 projective group and checks all 256 subset intersections;
it uses GAP's exact arithmetic and retains the unitary order formula.

The q=7 full group certificate is retained from phase fourteen. The uniform
generation, intersection and character-sum bounds remain written proofs;
the finite checks establish their parameter instances and coverage, not
those universal statements. To rerun the 37 symbolic identities with SymPy,
copy `phase15_unitary_symbolic_check.py` into scratch space before executing
it: that author script writes its adjacent report. The other author search
scripts likewise belong in a disposable copy. Preserve the saved originals.

The nineteenth Lean component can be freshly compiled with the pinned setup
described below:

```sh
python3 research/case_study/formal/verify_lean.py GradedSupport.lean
```

It verifies the explicitly documented group-factorization lemmas. It does
not formalize either the full forest theorem or the unitary theorem.
The recorded fresh run verifies the full group order, type `{4,24,4}`,
and all 256 subgroup intersections. This is a finite q=7 certificate,
not a uniform existence proof for its congruence class. Use a fresh
scratch directory to preserve any previous local run reports.

## Fresh Lean compilation

The [formal setup and scope document](research/case_study/formal/README.md)
describes all forty-three certificates and their unformalized boundaries. With Git
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

The first twenty-two certificates cover intersection transport, field and matrix
obstructions, connectivity and chamber orbits, torsor partitions, coordinate
kernels, the Suzuki matrix word, a local string-intersection obstruction,
exact Boolean-shadow witnesses of at most two vertices, and common-coset-point
theorems from factorization or arbitrary-family coordinate coverage.
Further modules check an abstract additive-commutator obstruction to an
intertwiner, vanishing of transvection-invariant forms, and the rank-three
obstruction from involution centralizers. That module uses actual subgroup
closure for generation; it does not formalize Suzuki structure or existence.
The seventeenth module, BinaryFrattiniActions, proves the exact four-case
binary action classification and its coordinate-support consequence using
kernel-checked finite decisions. The full p-group theorem remains a written
proof; its source/report boundary is specified in the accompanying scope note.
The eighteenth module, MarkedSquareDescent, adds marked action rigidity and
the equivariant transport obstruction with its stated assumptions.
They formalize the stated components, not the complete geometric
instantiations, all source-group classifications, or every written theorem.
The saved successful runs report no `sorryAx` dependency.

## Fixed excess, fiber products and the 2005 Frattini reduction

From the repository root, use a scratch output directory to preserve the
saved reports:

```sh
mkdir -p scratch/phase16
python3 research/case_study/phase16_frattini_coordinate_check.py --output scratch/phase16/frattini.json
python3 research/case_study/phase16_fiber_products_check.py --output scratch/phase16/fibers.json
python3 research/case_study/phase16_central_join_check.py --output scratch/phase16/joins.json
gap -q research/case_study/phase16_fixed_excess_check.g > scratch/phase16/core.log
gap -q research/case_study/phase16_hidden_kernel_check.g > scratch/phase16/hidden_kernel.log
python3 research/case_study/formal/verify_lean.py BooleanRetractions.lean
```

The first checker uses only the Python standard library. It examines
774,039 subspace families and verifies 1,801 coordinate bijections.
Its optional `--source-pdf` verifies separately supplied primary bytes;
the mathematical diagnostic does not require that PDF.

The second requires GAP and constructs the eight presented groups before
checking their orders, 136 deletion maps, all 3,008 subgroup intersections
and their local kernel products. Its runner checks the complete case list
and binds the output. The fixed-excess scripts additionally require GAP's
NQ package. Their six examples check 23,616 meets and 296 kernel restrictions;
the separate class-four example checks 256 meets and exhibits an extra
kernel element produced only by normal closure. These are finite diagnostics
for the uniform written proofs, not an exhaustive classification at every
excess.

The standard-library central-join checker builds its order-64 torus seed
from affine coordinates and checks its multiplication. Its four joins
have orders 128, 256, 4,096 and 32,768; it constructs 224 parabolics,
tests 20,992 meets, and computes the derived and lower central subgroups.
The fresh exported run is byte-identical to the saved deterministic report,
recorded in [the public check](provenance/phase16_join_public_check.json).
This tests actual cocycle groups, including two separated nonabelian cores;
it is not a finite census proving the counting polynomial.

The twentieth Lean module proves exactly the Boolean-image intersection
and four-marker centralization statements. The public runner was freshly
executed against the pinned dependencies; its report is
[saved separately](provenance/phase16_boolean_public_compile.json).
The preceding nineteen source files and historical compiler reports are
unchanged. The geometric bridges and full constructions remain written
arguments with the retained inputs listed in their notes.

For the linear diagonal construction, preserve the timestamped symbolic
report by running a scratch copy:

```sh
mkdir -p scratch/phase16_linear
cp research/case_study/phase16_linear_diagonal_symbolic.py scratch/phase16_linear/
python3 scratch/phase16_linear/phase16_linear_diagonal_symbolic.py
gap -q -T research/case_study/phase16_linear_diagonal_check.g > scratch/phase16_linear/finite.log
```

The symbolic checker requires SymPy (recorded version 1.14.0) and verifies
89 exact identities, including the root chains and all form-elimination
sign cases. The GAP check constructs the projective groups over q=3,5,7,9
and checks every one of their 16 marked subgroups and 256 meets. Root and
independent agent executions agree on all mathematical outputs. This
supports the written all-field proof; there is no new Lean formalization
of this matrix-family theorem or certification of publication priority.

## First-excess and diagonal unitary checks

The first-excess [classification](research/case_study/phase17_k1_classification.md)
has a uniform written proof and separate finite diagnostics:

```sh
mkdir -p scratch/phase17
gap -q -T research/case_study/phase17_k1_check.g > scratch/phase17/k1.log
gap -q -T research/case_study/phase17_unitary_diagonal_check.g > scratch/phase17/unitary_one.log
gap -q -T research/case_study/phase17_unitary_twisted_check.g > scratch/phase17/unitary_three.log
python3 research/case_study/phase17_unitary_diagonal_independent_check.py --output scratch/phase17/symbolic_one.json
python3 research/case_study/phase17_unitary_twisted_independent_check.py --output scratch/phase17/symbolic_three.json
```

The k1 script requires GAP's NQ package (recorded versions GAP 4.15.1 and
NQ 2.5.11). It tests all 165 nonzero parameter vectors at ranks 3–5:
4,616 parabolic orders and 138,432 exact meets, with 5, 10 and 15 accepted
markings. It also verifies every rejected vector against the support
criterion. These are bounded checks; the proof establishes all ranks.

The unitary scripts construct natural permutation actions and check
generation, orders and all marked subgroup intersections. The first uses
q=5,9,13,17 and the second q=3,7,11, totaling 112 subgroup closures and
1,792 meets. Their independently authored symbolic checkers pass 32
identities each using SymPy 1.14.0, with the correct field conjugation
in each branch. The author's separate symbolic checks pass 86 identities.
The [standalone q=3 script](research/case_study/phase17_unitary_q3_check.g)
also constructs the exceptional base using explicit field coordinates.
Generation at q=3 is a finite proof input; generation at the other fields
and the all-field intersection argument remain written proofs.

Compile the new narrow formal component through the existing runner:

```sh
python3 research/case_study/formal/verify_lean.py PrincipalKernelIntersections.lean
```

Supply `--packages` and `--lean` as above if using an existing pinned
checkout. The [fresh exported-source report](provenance/phase17_kernel_public_compile.json)
records successful compilation. The earlier twenty source files and
historical reports remain unchanged. The Lake target and portable runner
now both list all twenty-one modules. This corrects the older Lake target's
omission of `GradedSupport` and `BooleanRetractions`; their historical
certificates and explicit runner verification were already present.

## All-excess class-three checks

The [class-three classification](research/case_study/phase18_class_three.md)
has a written all-rank proof. Its bounded diagnostics deliberately test
two different objects: actual finite groups and the vector-space model
of central kernel quotients. These commands preserve the saved reports:

```sh
mkdir -p scratch/phase18
gap -q -T research/case_study/phase18_class_three_check.g > scratch/phase18/groups.log
python3 research/case_study/phase18_class_three_linear_check.py --output scratch/phase18/rank_two.json
python3 research/case_study/phase18_class_three_independent_linear_check.py --output scratch/phase18/all_subspaces.json
```

The GAP/NQ run constructs every rank-two kernel quotient at ranks
three and four, and the 81 predicted accepted ones at rank five.
It checks 243 groups, 5,128 parabolic orders and 123,072 subgroup
intersections. It does not construct the predicted rejected rank-five
groups. The first Python script tests all 2,829 rank-two quotient
maps up to change of basis. The independent script instead enumerates
all 29,602 kernel subspaces in these ranks, at every excess, without
using the proposed classification to select candidates. It performs
4,320,898 intersections, stopping early on rejected candidates.

Root freshly reproduced the group run and the independent subspace
run from their frozen scripts; the
[review record](research/case_study/phase18_class_three_root_audit.json)
binds those outputs. The transfer formula, Fibonacci identity and
fixed-excess leading coefficient are written derivations, not fitted
finite data. No new Lean module is claimed for them; the existing
twenty-one modules retain their stated partial scopes.

The [rank-three form diagnostic](research/case_study/phase18_rank3_forms_check.py)
uses SymPy for exact integer Smith forms and matrix identities. In a
disposable directory, copy that script and `phase18_rank3_forms.md`,
then run the script with a Python environment containing SymPy. It
writes its report beside itself. The saved check covers all 35 joint
endpoint multiplicity patterns, the middle-involution dimensions and
the specified fold identities. Its Smith factors are only one and two,
so the dimension systems lose no rank in odd characteristic. This
is a linear-algebra diagnostic, not a group-generation certificate.

## Complete excess two and unitary rank three

The excess-two proof classifies every rank d>=3 at order 2^(2d+1).
Its independent rank-three diagnostic starts with the universal class-four
quotient, enumerates all 207 normal subgroups and tests all 23 eligible
quotients. The 13 accepted markings split as six central, four noncentral
cyclic and three noncentral elementary-abelian kernels. The affine seed
has a separate 128-element check using only Python's standard library.

```sh
mkdir -p scratch/phase19
gap -q -T research/case_study/phase19_k2_independent_census.g > scratch/phase19/k2_census.log
python3 research/case_study/phase19_k2_affine_check.py --output scratch/phase19/affine.json
gap -q -T research/case_study/phase19_k2_check.g > scratch/phase19/noncentral_groups.log
```

The first run checks 184 parabolics and all 1,472 meets. The third
constructs the 48 proposed noncentral groups at ranks three through
five and checks 1,112 parabolic kernels/orders and 30,144 meets; it is
not an independent exhaustive search at those three ranks. The
[root review](research/case_study/phase19_k2_root_audit.json) records fresh
runs of the independent census and affine checker. The source-census
parser needs the separately obtained primary text identified in its
saved report; that full text is not bundled.

The unitary rank-three proof has both independent symbolic checks
and exact finite-group diagnostics. The Python command needs SymPy.

```sh
python3 research/case_study/phase19_unitary_rank3_independent_symbolic.py --output scratch/phase19/unitary_symbolic.json
gap -q -T research/case_study/phase19_unitary_rank3_check.g > scratch/phase19/unitary_groups.log
```

These check 24 identities and six markings, respectively: q=5,7,9,11,13
and a second q=7 parameter. Every computed projective group has the
predicted order, and all 48 subgroup closures and 384 meets pass.
The [root review](research/case_study/phase19_unitary_rank3_root_audit.json)
binds fresh runs from the frozen scripts. Full-field generation is proved
in the written argument; the finite examples alone do not establish it.

The new nested-kernel Lean adapter can be freshly compiled with the
same pinned environment described above:

```sh
python3 research/case_study/formal/verify_lean.py NestedKernelIntersections.lean --packages /path/to/pinned/.lake/packages --output-dir scratch/phase19/lean
```

The runner compiles its principal-kernel dependency first. The
[public-run report](provenance/phase19_nested_kernel_public_compile.json)
records Lean 4.32.2, checked dependency revisions, exit zero and the
five theorem axiom lists. The exact parabolic kernel profile remains
a formal hypothesis. All twenty-one older source/report pairs remain
unchanged; there are now twenty-two partial certificates.

## Finite boundary states and all odd unitary extensions

The fixed-class theorem has two bounded transition diagnostics:

```sh
mkdir -p scratch/phase20
gap -q -T research/case_study/phase20_finite_state_check.g > scratch/phase20/class_three.log
gap -q -T research/case_study/phase20_finite_state_class4_check.g > scratch/phase20/class_four.log
```

The first builds the complete rank-three class-three alphabet from all
16 kernel subgroups of the universal group. Its 13 states and 89 transitions
construct all 89 corresponding rank-four groups. It checks orders, class,
factor embeddings, actual IP and the deletion-kernel update. Weighted
counts through rank ten agree with the earlier two-state formula. It
also checks the unique class-two boundary state.

The second repeats the class-three pool construction, adds the 16
noncentral excess-two rank-four windows, and filters to excess at most
two. Its 58 states and 258 transitions yield 258 checked rank-five
constructions. This run performs 9,808 parabolic closures and 288,000
meets cumulatively, including the repeated pool work. The walk coefficients
through rank twelve agree with the earlier exact excess-zero/one/two
formulas. Completeness of this restricted alphabet retains the previous
classifications. No genuine extra compatibility rejection or noncentral
diagonal is exhibited; the general cases rely on the written proof.
The [root record](research/case_study/phase20_finite_state_root_audit.json)
binds a fresh run of the second script. Its cumulative count should not
be added to the repeated pool's count as if they were disjoint tests.

The new unitary template covers every odd q>=3. The general proof applies
at q>=5, and the q=3 base is verified separately:

```sh
python3 research/case_study/phase20_unitary_q3_independent_check.py --output scratch/phase20/q3_independent.json
python3 research/case_study/phase20_unitary_q3_root_check.py --output scratch/phase20/q3_root.json
gap -q -T research/case_study/phase20_unitary_rank3_check.g > scratch/phase20/unitary_groups.log
```

Both Python implementations need SymPy and construct their own field
arithmetic and plane permutations from the literal matrices. They retain
SymPy's Schreier-Sims group-order algorithm. Each finds order 6,531,840
on 112 planes and verifies all 64 marked meets. They are independent
implementations of the same finite base, not extra parameter cases.
The GAP script checks six fields, including q=3, with 384 total meets.

For the symbolic identities, copy
`research/case_study/phase20_unitary_rank3_symbolic.py` into the scratch
directory and run that copy with SymPy installed. It writes its report
beside itself and verifies 31 identities, including the q=3 polynomial
coordinates. Root freshly ran this symbolic check and the root q=3
implementation; the author six-field GAP run is retained as a saved record.
No new Lean module is claimed in this phase. The 22 existing formal
certificates keep their previous source and report bytes and partial scopes.

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

## Phase twenty-one: linear rank-three generation

The [standalone proof](research/case_study/phase21_linear_rank3.md) covers
all odd q≥5; the exact rank-set corollary retains the published q=3 case
and earlier rank-four and upper-bound results. To reproduce its diagnostics:

```sh
mkdir -p scratch/phase21
cp research/case_study/phase21_linear_rank3_symbolic.py scratch/phase21/
python3 scratch/phase21/phase21_linear_rank3_symbolic.py
gap -q -T research/case_study/phase21_linear_rank3_check.g > scratch/phase21/linear_groups.log
```

The symbolic script writes beside its own copy; running it in scratch
preserves the historical report. It needs SymPy (recorded version 1.14.0).
Expected results are 34 exact symbolic checks and six fields
q=5,7,9,13,17,25, with 48 marked subgroup closures and 384 exact meets.
The checker also verifies both rank-one projection orders and the exact
projective ambient-order sandwich. The [root record](research/case_study/phase21_linear_rank3_root_audit.json)
binds fresh executions of the unchanged scripts. Reproducing those cases
does not add new parameter coverage. The group argument and retained
classification inputs remain written mathematics; no new Lean module
is included in this phase.

The independent-kernel census requires GAP with NQ (recorded versions
4.15.1 and 2.5.11). Set the rank before reading the unchanged script.
This example preserves fresh raw kernel checkpoints in scratch:

```sh
mkdir -p scratch/phase21
gap -q -T > scratch/phase21/rank4.log <<'GAP'
rank21 := 4;;
checkpoint21 := "scratch/phase21/rank4";;
Read("research/case_study/phase21_kernel_census.g");
GAP
gap -q -T research/case_study/phase21_N009_presentations_check.g > scratch/phase21/presentations.log
python3 research/case_study/phase21_N009_source_compare.py --accepted scratch/phase21/rank4.accepted.json --output scratch/phase21/source_comparison.json
```

The rank-four expected result is 1,483 candidate kernels, 199 accepted
ordered markings, 11 fixed by reversal and 105 reversal classes. It checks
73,880 small-kernel meets and all 50,944 full marked meets in the accepted
groups. The source comparison checks all thirteen type counts and the two
specified oriented facet cases. The separate raw-presentation run uses
Todd–Coxeter without NQ or added class relations; each presented group has
order 1,024 and their combined 512 marked intersections pass.

The [report packager](research/case_study/phase21_build_census_report.py)
checks completed logs, all kernel checkpoints, accepted witness metadata
and executed-source hashes. It does not rerun GAP or prove the census
independently. The compressed checkpoints are original mathematical data,
not third-party group catalogues. Historical reports and compressed files
remain unchanged when rerunning into scratch.

Setting `rank21` to 3 or 5 runs the corresponding completed third-excess
census. Expected ordered totals are 37 and 584, respectively. The rank-five
run exhausts 35,971 kernels, checks 3,072,608 small-kernel comparisons and
598,016 full meets on accepted groups. Its recorded runtime was about
12 minutes; this is an observation, not a performance guarantee. These
finite totals alone do not establish an all-rank counting formula.

## Rank-three order-1,024 census, auxiliary lemmas and priority audit

The [phase22 root review](research/case_study/phase22_root_audit.md)
records fresh executions separate from the frozen authored reports. To
repeat the complete nonabelian-kernel census, use a fresh directory:

```sh
mkdir -p scratch/phase22
cp research/case_study/phase22_N009_rank3_census.g scratch/phase22/
cp research/case_study/phase22_N009_rank3_universal.g scratch/phase22/
cp research/case_study/phase22_N009_rank3_build_report.py scratch/phase22/
cd scratch/phase22
gap -q -T phase22_N009_rank3_census.g > phase22_N009_rank3_census.log
gap -q -T phase22_N009_rank3_universal.g > phase22_N009_rank3_universal.log
python3 phase22_N009_rank3_build_report.py --directory . --output fresh_certificate.json
cd ../..
```

Expected totals are 401 candidate kernels, 235 ordered markings, 15
reversal-fixed markings and 125 classes. All 25,664 actual subgroup meets
are tested, including rejected candidates. The five complete kernel
levels contain 7, 23, 61, 147 and 401 entries. The universal kernel is
nonabelian, with derived subgroup of order 512. GAP/NQ's exact universal
quotient and subgroup operations remain explicit computational inputs.
The builder checks data and all twelve source type totals; it does not
regenerate the groups itself.

The affine-center and priority diagnostics use only Python's standard
library. Copy the priority checker because it writes its report beside
its script:

```sh
python3 research/case_study/phase22_N009_centers_check.py --output scratch/phase22/centers.json
cp research/case_study/phase22_linear_priority_check.py scratch/phase22/
python3 scratch/phase22/phase22_linear_priority_check.py
```

These check all 4,080 elements in eight affine models, and five integer
matrix identities plus eight scalar-quotient cases. The uniform center
and kernel-location arguments are written proofs. The source supplement
attributes the earlier thesis claim, records a specific printed-witness
defect and preserves the limits of its selected-section reading. These
checks do not audit the complete thesis or establish publication novelty.

## Third-excess transition graph and exact all-rank certificate

This run reconstructs all 706 windows from the immutable kernel data,
verifies their actual intersections, executes both compatibility tests,
builds the complete budget-three graph and constructs its two additional
deletion states:

```sh
python3 research/case_study/phase22_excess3_run.py --output-prefix scratch/excess3/phase22_excess3_final
python3 research/case_study/phase22_excess3_check.py --prefix scratch/excess3/phase22_excess3_final --output scratch/excess3/recount.json
cp research/case_study/phase21_rank[345]_census.json scratch/excess3/
python3 research/case_study/phase22_excess3_annihilator.py --inputs scratch/excess3 --output scratch/excess3/annihilator.json
```

The first command requires GAP with NQ; the two Python checkers use only
the standard library. The fresh root run took about 104 seconds and
reproduced graph, windows and gluings byte for byte. It checked 722,944
actual window meets and 8,192 meets in the two additional groups. Both
general compatibility rejection counts are zero in this bounded run,
and both extra examples have trivial diagonal gluing intersection;
the general theorem retains its written proof for the other cases.

The separate integer-vector checker verifies `(T-I)^3 v7=125e` and
`Te=e` in all 2,832 coordinates. The binomial operator theorem then
gives the all-rank cubic; ranks four through six are handled separately
and rank three remains exceptional. This is independent arithmetic on
the exact graph, not an independent implementation of GAP's group
algorithms. See the [root audit](research/case_study/phase22_excess3_root_audit.md).

## Common generation theorem and its exceptional complement

Copy both the checker and its proof input, since the checker binds the
proof hash when writing its new report:

```sh
mkdir -p scratch/generation
cp research/case_study/phase23_generation_core_check.py scratch/generation/
cp research/case_study/phase23_generation_core.md scratch/generation/
python3 scratch/generation/phase23_generation_core_check.py
```

Python with SymPy is required. Expected output is 22 passing check groups,
including all 5,184 cocycle equations for the characteristic-two product,
all 720 explicit unitary-complement matrices over F9 and 2,880 products
by a verified generating set. The nilpotent ranks are 2,1,0, certifying
the exceptional Jordan type (3,1). Another 2,880 integer parameter cases
corroborate the all-parameter weight argument. The universal mathematical
proof remains in the [note](research/case_study/phase23_generation_core.md);
the [independent review](research/case_study/phase23_generation_core_independent_audit.md)
and [root technical review](research/case_study/phase23_generation_core_root_audit.md)
have distinct roles. These additions supply no new Lean module in this snapshot.


## Exact Table 6 labels and finite universal presentations

The [independent replay checker](research/case_study/phase22_N009_labels_rank_check.py)
runs all four GAP scripts in a disposable directory and compares the resulting
eight data files with the saved outputs. It verifies the frozen input hashes
and the complete table comparison. This command leaves historical files intact:

```sh
mkdir -p scratch/labels
python3 research/case_study/phase22_N009_labels_rank_check.py --gap gap --output scratch/labels/replay.json
```

Expected results are 428 marked facet identifications, all 107 source rows,
and all 106 finite universal orders. The rank-five search checks all 127
hyperplanes and 130,048 actual subgroup intersections. The original
[review](research/case_study/phase22_N009_labels_rank_audit.md) additionally
parsed 67 primary Atlas pages, their actual permutations and relator words,
and re-extracted the source table. Those primary files are not distributed.
The optional `--primary-sources` flag requires the hash-matching private
snapshots at the paths in the manifest. Without it, the mathematical reruns
and comparison of distributed numerical data still execute.

Rank-four completeness comes from the earlier kernel census; the infinite
universal row retains the cited decomposition. The Atlas assigns names to
exact marked objects and is not used as a candidate-completeness oracle.

## Lean transfer arithmetic with native evaluation

```sh
mkdir -p scratch/transfer
python3 research/case_study/formal/verify_lean.py Phase23TransferAnnihilator.lean --output-dir scratch/transfer
python3 research/case_study/phase23_transfer_lean_data_check.py --compile-report scratch/transfer/Phase23TransferAnnihilator.check.json --output scratch/transfer/data_check.json
python3 research/case_study/phase23_transfer_lean_generate.py --output scratch/transfer/Phase23TransferAnnihilator.lean
```

Use the pinned dependency setup above, or provide `--packages` and `--lean`.
Fresh compilation verifies the literal integer transfer identities; its output
prints four generated native-evaluation axioms. It therefore trusts Lean's
compiler/interpreter for these arithmetic decisions. The data checker binds
the embedded rows and edges to the frozen graph and to the successful compile
report; it does not itself run Lean. Regeneration should reproduce SHA256
`0ee15f12f7cb9583380cf49ff5467da3001fb184ca912002487e6d35044f198f`.
The [scope](research/case_study/formal/Phase23TransferAnnihilator.scope.md)
excludes the group-to-graph correspondence and general all-rank algebra.
The earlier 22 source/report pairs remain unchanged.


## Complete N009 statement ledger and remaining finite examples

```sh
mkdir -p scratch/N009-examples
python3 research/case_study/phase24_N009_examples_run.py --gap gap --output-dir scratch/N009-examples
python3 research/case_study/phase24_N009_rank_audit.py --gap gap --output scratch/N009-examples/review.json
```

The first command runs the 34 raw presentations in isolation and saves its
log, five mathematical outputs and execution report. The second additionally
checks the frozen manifest, complete 27-item/six-table ledger, numerical data
transport and agreement with the authored outputs, then independently reruns
the same GAP checker. Either is sufficient for a mathematical replay; running
both is optional. The recorded root and agent reviews used separate runs.

Expected output is 3,328 actual IP meets, all twelve Table 3 assignments,
eight distinct type-{4,8} markings matched to the unfiltered census, and all
three central-involution quotient kernels in Example 4.5. The literal Table 4
map sends e/f/h to c/a/c. The
[coverage note](research/case_study/phase24_N009_coverage.md) explains the
verified repairs and the quoted inputs that remain. The independent audit's
optional `--primary-sources` mode needs the excluded hash-matching snapshots.
A successful finite replay does not independently rerun the earlier censuses
or prove the quoted infinite decomposition.


## The six 2005 constructions and the 2001 Petrial obstruction

```sh
python3 research/case_study/phase24_L088_run.py --gap gap --output-dir scratch/L088-fresh
python3 research/case_study/phase25_L108_check.py --output scratch/L108-fresh.json
python3 research/case_study/formal/verify_lean.py EndpointDoublingIntersections.lean --output-dir scratch/endpoint-lean
```

The L088 runner requires a new empty output directory, GAP and TomLib. It
copies its four inputs into a temporary directory and leaves historical
reports unchanged. Expected output is six verified markings, 1,536 full
subgroup meets, 168 typed Helly equalities, 66 residue-generation tests,
and the raw source presentation's completed index of 1,463. The group
order sandwich retains the correctness of that completed Todd–Coxeter
calculation; checking a transitive coset table alone is insufficient for
an upper bound. The independent integer checker tests the explicit
permutations and table actions. The exhaustive six-only classification
is outside this replay.

The L108 checker needs only Python's standard library. It constructs all
the incidences and chamber flips of seven examples (188 original chambers),
deduplicates Petrie faces as actual vertex-edge sets, and checks both
nonfaithful actions and all four thin-case bidualities. Its finite scope
is separate from the written proof for arbitrary groups. Use a new output
filename to preserve earlier results. The Lean command verifies only the
fixed-overlap mixed-subgroup lemma, under the pinned dependencies above.


## General endpoint changes and the isolated support obstruction

```sh
python3 research/case_study/phase26_halving_check.py --output scratch/halving-fresh.json
mkdir -p scratch/halving-S6
cp research/case_study/phase26_halving_filter_check.py scratch/halving-S6/
python3 scratch/halving-S6/phase26_halving_filter_check.py
```

Both use only Python's standard library. The first refuses an existing
output file and checks nine named examples plus all168 eligible S4 triples,
for21,888 actual ordered subgroup meets. It verifies the full iff criterion
in every qualifying finite example; the arbitrary-group result remains
the written proof. The independent S6 checker writes beside its own source,
so run the scratch copy as above. It checks all32 complete subgroup element
sets, all512 old/new meets and the actual set-stabilizer identifications.
Its two changed-meet failures are the intended negative certificate.

The frozen example note's command `python 3` is a typographical error;
the invocation above uses `python3`. Its original bytes and hash are
preserved. No source catalogue or external group package is required.

The separate formal supplement for the support obstruction is checked by:

```sh
python3 research/case_study/formal/verify_lean.py TwoCosetIntersection.lean --output-dir scratch/two-coset-lean
```

It proves the iff statement for a general two-coset interval and the
excess-witness implication. The printed axioms are only `propext` and
`Quot.sound`; it does not derive the interval hypotheses from an arbitrary
marked group or formalize the complete geometric construction.


## Why the S6 input is not a geometry

```sh
python3 research/case_study/phase26_s6_geometry_check.py --output scratch/S6-geometry-fresh.json
```

This independent diagnostic builds every typed coset flag of the old S6
marking and checks its common intersection and actual chamber extensions.
It finds 720 full chambers and 90 unextendible flags, all of type {0,2,3}.
The two local graph conditions B1 and B2 pass. Thus the old subgroup-IP
and these graph conditions do not supply the original geometry hypothesis
of the cited halving theorem. The source adapter also gives an explicit
Johnson-graph/partition witness. Python standard library only; the output
path must be new. Source PDF reading and the general source theorems are
separate from this exact finite diagnostic.

## The actual geometric parity obstruction

```sh
mkdir -p scratch/parity-author
cp research/case_study/phase27_parity_shadow_check.py scratch/parity-author/
python3 scratch/parity-author/phase27_parity_shadow_check.py
python3 research/case_study/phase27_parity_shadow_rank_check.py --output scratch/parity-independent.json
```

Both checkers use only Python's standard library. The first writes beside
its source, so run the scratch copy to preserve the frozen report. It
checks part sizes one and two. The independent bitset implementation
computes the even-walk classes and reconstructs the published construction
for part size two. Expected output is 801 original flags and 192 chambers,
with panel counts 336 of size two and 24 of size four. Every original
residue is connected. Every transformed flag still extends to a chamber,
but exactly twelve transformed residues split into two components of size
four. These are the intended negative results. The all-part-size family,
the exact iff theorem and the lattice-polytope reduction are written proofs;
these finite checks do not formalize them or establish publication priority.

## Arbitrary deck-group torsors

```sh
python3 research/case_study/phase28_voltage_shadow_check.py --output scratch/voltage-shadow-fresh.json
python3 research/case_study/formal/verify_lean.py Phase29CosetMonodromy.lean --output-dir scratch/monodromy-lean
```

The first command needs only Python's standard library and a new output
filename. Expected counts are 28 component cosets and 2,350 shadow
families in an explicit S₃-cover of K₄. The tetrahedral graph-incidence
lift has 144 chambers; its bipartite compression has 72. Every flag,
extension and residue of these rank-three examples is checked. A second
cover verifies a common-shadow intersection splitting into two components.
The C₂² three-coset Helly failure is an algebraic illustration; the
checker does not realize it inside a higher-rank base geometry.

The Lean command uses the pinned dependencies described above and writes
fresh results outside the historical reports. It certifies five algebraic
lemmas about nonempty common fibers, equivalence classes and the subgroup
equality criterion. It does not formalize graph lifting or the complete
geometric theorem. All five printed axiom lists contain standard axioms
only, with no native evaluation.

## The exact lift-extension identification

```sh
python3 research/case_study/phase30_torsor_cover_check.py --output scratch/torsor-cover-fresh.json
```

Python standard library only; use a new output filename. This checks the
tetrahedral parity cover and the identity cover of the triangular dihedron.
The latter has a graph-action kernel of order two and a faithful incidence
action, testing why both the base and cover automorphism must be retained.
Expected totals are 192 exact subgroup meets, with 145 and 39 flags and
48 and 12 chambers in the two graph-incidence examples. All base-subflag
stabilizer formulas and the object/coset correspondence are checked. These
rank-three examples do not test higher flags with multiple objects; the
arbitrary-rank equivalence is the separate written proof.


## Nested-shadow applications and complete presentations

```sh
python3 research/case_study/phase30_source_geometry_check.py --output scratch/source-geometry-fresh.json
gap -q research/case_study/phase30_source_presentations_check.g > scratch/source-presentations-fresh.log
```

Use a new Python output filename. The standard-library coordinate checker
verifies 10,580 flags, 3,060 residues, 4,896 thin panels and 132 nested higher
component pairs. GAP checks six raw presentations, of orders 64,144,384,1296,
1536,5184, including every indicated involution/product order and all 768
subgroup meets. It prints `PHASE30_SOURCE_PRESENTATIONS_PASS`; inspect the
log for errors as well as the process exit. Neither script modifies historical
reports. These are finite diagnostics of separate uniform written arguments.


## Actual regular affine counterexample

```sh
python3 research/case_study/phase30_affine_map_check.py --output scratch/affine-author-fresh.json
python3 research/case_study/phase30_regular_halving_root_check.py --output scratch/affine-independent-fresh.json
python3 research/case_study/phase30_affine_formal_data_check.py --output scratch/affine-transcription-fresh.json
python3 research/case_study/formal/verify_lean.py Phase30AffineData.lean --output-dir scratch/affine-lean
```

Use new output names. The two standard-library implementations use different
seed coordinates and import neither one another nor external group data.
They check the 120-element seed, its 355 flags, code rank17/quotient dimension13,
all 720 memberships and 60 span intersections, and local changed groups of
orders160,160 with intersection8 instead of4. The global 983,040-chamber
geometry and 122,880 failed transformed residues follow from the written
affine theorem; a full global enumeration is not performed.

The transcription check binds four Lean arrays to the authored JSON.
The fresh pinned Lean compile checks six literal predicates using kernel
`decide`, with no native-evaluation axioms. See the scope document for the
unformalized code, seed and geometric adapters. Historical reports are
preserved by every command above.


## Seed surface for the infinite cover family

```sh
python3 research/case_study/phase31_seed_surface_check.py \
  --seed research/case_study/phase30_affine_map_check.json \
  --output scratch/seed-surface-fresh.json
```

Python standard library only; use a new output filename. The seed report is
hash-bound before the literal group is reconstructed. Expected results are12
embedded pentagons,54 circular barycentric links,180 panels, genus4, integral
boundary composition zero and first-homology dimension8 at primes2,3,5,7,11.
The sign character is checked on all14,400 group products and every flag
adjacency. The uniform surface-cover theorem and integer-degree corollary
are written proofs, not consequences of sampling these primes. No lifted
code, enormous affine group or new Lean module is generated by this command.


## Infinite presentation and older neighbourhood theorem

```sh
python3 research/case_study/phase32_L003_root_check.py \
  --data research/case_study/phase32_L003_voltage.json \
  --output scratch/L003-image-fresh.json
python3 research/case_study/phase32_L111_check.py \
  --output scratch/L111-neighbourhood-fresh.json
python3 research/case_study/phase32_L003_formal_data_check.py \
  --data research/case_study/phase32_L003_voltage.json \
  --lean research/case_study/formal/Phase32L003Infinitude.lean \
  --output scratch/L003-formal-alignment-fresh.json
```

These standard-library commands use new output filenames. Expected results:
2,160 exact relator/state checks, a nonzero translation, permutation-image
order216 and translation rank6; and316 finite neighbourhood inputs with
12,628 residue isomorphisms and26,802 flags. The formal transcription check
matches literal arrays and all ten words; it does not compile Lean.

Compile both new formal modules with the dedicated pinned-dependency runner:

```sh
python3 research/case_study/phase32_L003_formal_check.py \
  --packages /path/to/pinned/.lake/packages \
  --lean /path/to/lean-4.32.2 \
  --output-dir scratch/L003-lean-fresh
```

The output directory must be new. Missing PresentedGroup dependency objects
are compiled from pinned sources into a private overlay, leaving the
installed packages unchanged. Both certificates are compiled afresh. The
formal theorem proves infinitude of the displayed s6 presentation; the
all-multiples extension, source identification, image-rank computation and
neighbourhood theorem are written arguments with separate evidence.


## Fixed-parameter geometry and quotient transport

```sh
python3 research/case_study/phase32_L003_geometry_check.py \
  --output scratch/L003-geometry-fresh.json
python3 research/case_study/formal/verify_lean.py ParabolicQuotientTransport.lean \
  --packages /path/to/pinned/.lake/packages \
  --lean /path/to/lean-4.32.2 \
  --output-dir scratch/quotient-transport-fresh
```

The standard-library geometry checker closes all15 proper integer-action
subgroups, computes the full modulus-two order27,648 from432 permutations
and1,728 binary Schreier generators, and verifies all256 marked meets and16
nonautomatic typed-Helly counts. A fresh report path is required. The
all-even-modulus and universal-group conclusions are separate written
proofs. The Lean module checks the abstract quotient criterion, with its
explicit hypotheses; it does not execute the geometric census.


## Merging, parity and one exceptional parabolic

```sh
python3 research/case_study/phase32_L111_section6_check.py \
  --output scratch/L111-section6-fresh.json
python3 research/case_study/formal/verify_lean.py OneExceptionalParabolic.lean \
  --packages /path/to/pinned/.lake/packages \
  --lean /path/to/lean-4.32.2 \
  --output-dir scratch/one-exceptional-fresh
```

The standard-library checker validates the merging/splitting maps, the exact
128/512 symmetry groups, and all flag, residue, weak-shadow and group claims
for the odd square torus at modulus five. The all-odd-modulus argument and
arbitrary-rank construction are written proofs. Lean independently checks
the generic one-exceptional-parabolic transport theorem and imports the
previous transport module. It does not certify either geometric example.


## Every even source parameter

```sh
python3 research/case_study/phase33_L003_even_check.py \
  --output scratch/L003-even-fresh.json
python3 research/case_study/phase33_L003_even_base_root_check.py \
  --output scratch/L003-even-base-independent-fresh.json
```

The first standard-library checker verifies11,664 literal integer
relator/state equalities, three finite injective parabolics, a unit
translation minor and the base group's IP and typed Helly. The second
implementation independently builds Cayley components and checks all5,287
pairwise-incident coset flags, including1,296 chambers with unique common
representatives. Both require a new output path. The all-even theorem
uses these finite data, the separately Lean-checked one-exceptional
transport theorem, and retained toroidal presentation/order bounds.
Universal-even existence and infinitude for6|s are written corollaries.


## Exact even-family orders and integral reduction

```sh
python3 research/case_study/phase34_L003_even_order_check.py \
  --output scratch/L003-even-order-fresh.json
python3 research/case_study/formal/verify_lean.py SplitLatticeReduction.lean \
  --packages /path/to/pinned/.lake/packages \
  --lean /path/to/lean-4.32.2 \
  --output-dir scratch/split-lattice-fresh
```

The first checks every Schreier translation against six integral basis
vectors, their unit minor and literal words. Its written uniform argument
gives kernel mL and order1296m^6 at every modulus. Lean certifies the
abstract additive-left-inverse reduction and the literal matrix inverse;
it does not run the full Schreier enumeration.


## Source parameters divisible by three

```sh
python3 research/case_study/phase34_L003_triple_check.py \
  --output scratch/L003-triple-fresh.json
python3 research/case_study/phase34_L003_triple_base_root_check.py \
  --output scratch/L003-triple-base-independent-fresh.json
```

These standard-library checks verify the literal integral action and its
modulus-two base. The first uses finite subgroup meets and flag-orbit
counts; the second independently constructs Cayley components and checks
all56225 flags, including13824 singleton-intersection chambers. Both
require a new output path. The all-m argument uses twice-integral local
translations, exact toroidal order bounds and the existing quotient theorem.


## Compact affine model and literal Lean matrices

```sh
python3 research/case_study/phase35_L003_affine_check.py \
  --output scratch/L003-affine-fresh.json
python3 research/case_study/phase35_L003_affine_compare.py \
  --data research/case_study/phase33_L003_even_voltage.json \
  --output scratch/L003-affine-comparison-fresh.json
python3 research/case_study/formal/verify_lean.py CompactAffineData.lean \
  --packages /path/to/pinned/.lake/packages \
  --lean /path/to/lean-4.32.2 \
  --output-dir scratch/compact-affine-lean-fresh
```

The standalone standard-library check requires no input data. It closes the
six-dimensional linear group, checks all Schreier translations, three fixed
parabolics and all 5,287 base coset flags. The second proves the literal
generator intertwiner with the older voltage model. Each requires a fresh
output path. Lean checks the homogeneous integer matrix identities and
specified translation words; it does not repeat the finite geometry census.


## Free quotient of the unfilled presentation

```sh
python3 research/case_study/phase34_L003_free_voltage_check.py \
  --output scratch/L003-free-words-fresh.json
```

Python's standard library checks all 5,832 free-word relator/state equalities,
the transitive 648-state action and every listed surjectivity witness. The
output must be new. The universal geometry and Euclidean local-group
identification are separate written consequences of the compact family.
The retained GAP finder and log record discovery only and are unnecessary
for verification. Run that finder only from a fresh scratch directory:
it writes its data filename in the current directory.


## Splitting the compact family

```sh
python3 research/case_study/phase35_L003_affine_split_check.py \
  --output scratch/L003-affine-split-fresh.json
```

This checks the 24 integer coordinates of the change of origin and scale.
The short written splitting proof retains the earlier full translation
kernel calculation. The exact abstract group Q is preserved at every modulus.


## Tensor parameters and uniform Fibonacci arithmetic

```sh
python3 research/case_study/phase35_L003_tensor_model_check.py \
  --output scratch/L003-tensor-fresh.json
python3 research/case_study/formal/verify_lean.py FibonacciModulus.lean \
  --packages /path/to/pinned/.lake/packages \
  --lean /path/to/lean-4.32.2 \
  --output-dir scratch/fibonacci-lean-fresh
```

The Python checker needs only the standard library and its literal matrices.
It verifies all fixed integer relations, local closures, reductions and 23
sample parameters. The all-parameter argument is written; Lean independently
checks its uniform Fibonacci matrix arithmetic. Neither command proves the
pending global intersection/incidence assertions.


## Complete tensor geometry at every parameter

```sh
python3 research/case_study/phase35_L003_tensor_geometry_check.py \
  --output scratch/L003-tensor-geometry-fresh.json
```

This standard-library checker has no data-file or discovery-script input.
It uses literal tensor matrices, completes the three fixed groups, checks
all 1,928 bounded products and 52 membership witnesses, and verifies every
proper-subgroup meet and typed-Helly count at moduli three and five. The
all-modulus transfer and source geometry adapter are written proofs. The
output must be new; the checker does not enumerate either full ambient group.


## General parabolic-product comparison

```sh
python3 research/case_study/formal/verify_lean.py ParabolicProductComparison.lean \
  --packages /path/to/pinned/packages --lean /path/to/lean \
  --output-dir scratch/parabolic-product-fresh
```

The runner computes transitive local imports and compiles the two earlier
transport modules before this certificate. The formal theorem includes both
typed-Helly directions. The subsequent marked comparison module below adds
full subgroup IP; the matrix/geometric adapter remains a written proof.
The Lake root list also includes all
41 modules; no frozen historical reports are overwritten by the scratch run.


## Full-body measurement of Compress_A

```sh
python3 research/case_study/phase36_compress_forest_measurement.py \
  --n001-text /path/to/bound/N001-browser-record.txt \
  --n003-text /path/to/bound/N003-extraction.txt \
  --output scratch/compress-A-lengths.json
```

The exact third-party source transcriptions are intentionally excluded from
the repository. Their hashes and body/exclusion intervals are in the protocol;
changed source bytes fail verification. The public replacement is found next
to the runner. Add `--source-pdf /path/to/N003.pdf --verify-pdf-extraction`
to repeat the optional pypdf extraction check. The output path must be new.
The runner measures representations; it does not approve theorem coverage
or turn the divergent token/character metrics into a single factor.


## Full marked comparison

```sh
python3 research/case_study/formal/verify_lean.py ParabolicMarkedComparison.lean \
  --packages /path/to/pinned/packages --lean /path/to/lean \
  --output-dir scratch/parabolic-marked-fresh
```

This selects the complete four-module import chain. Both abstract IP and
typed-Helly equivalences are formalized for actual markings; concrete matrix
hypotheses and geometry identifications remain separate. See the
[root interface review](research/case_study/phase37_parabolic_marked_root_audit.md).


## Integrated three-paper manuscript

The [manuscript and contract](COMPRESS_A.md) have a complete internal written
review. To replay the read-only provenance check, use a private source root
containing the exact source assets and component artifacts bound in its intake:

```sh
python3 research/case_study/phase37_compress_forest_recent_check.py \
  --root /path/to/complete/private/intake --output scratch/forest-v2-check.json
```

The output path must be new. The check binds 23 source/replacement spans,
ten N008 numbered anchors and the source files; it does not verify the proof
or measure length. The author assembler/binder are preserved as construction
provenance and write generated files; run them only on an isolated copy.


## Rendered two-paper body sensitivity

Use Python with pypdf 6.13.0, Pandoc 3.10 and the XeLaTeX release recorded in
the [protocol](research/case_study/phase37_rendered_measurement_protocol.json):

```sh
python3 research/case_study/phase37_rendered_measurement.py \
  --input-root /path/to/complete/private/intake \
  --output-dir /tmp/compress-A-render-NEW
```

The output directory must not exist. The tool binds the source files and
body spans, renders only the earlier authored replacement, and compares
AST/extraction hashes and all NFC/NFKC metrics. Renderer drift requires
the explicit `--allow-toolchain-drift` option and is reported as such.
PDFs and extracted replacement text remain in scratch; source bodies are
never written. The [root replay review](research/case_study/phase37_rendered_measurement_root_audit.md)
states the exact validation and the remaining source-representation limit.


## Four-paper replacement and its charged finite census

The [Compress_B review](COMPRESS_B.md) separates the written all-parameter
arguments from the bounded exact calculation. With GAP and SmallGroups:

```sh
python3 research/case_study/phase37_compress_twogroups_recent_check.py \
  --gap /path/to/gap --output scratch/compress-B-census.json \
  --log scratch/compress-B-census.log
```

Both output paths must be new. The wrapper checks the unchanged source hash,
runs in a temporary directory, and asserts 1,651 eligible groups, 1,641 active
groups, 92 anchored triples, all four relation counts and every group/row hit.
The recorded run uses GAP 4.15.1 and SmallGroups 1.5.4. It retains the catalogue
and exact group arithmetic; it does not prove the infinite-parameter lifting
argument or the imported geometric assembly results.


## Primitive saturation and parabolic-kernel diagnostics

```sh
gap -q research/case_study/phase38_primitive_saturation_check.g
```

The finite diagnostic builds eight compatible-square groups from their
presentations and checks 136 parabolic kernels/orders and 292 induced-residue
indices. It also checks the general Frattini restriction and unique maximal
overgroups on five further p-groups. This uses exact GAP arithmetic and
the SmallGroups catalogue for those five examples. The all-parameter
[theorem and review](research/case_study/phase38_primitive_saturation_root_audit.md)
are separate written evidence; no higher lower-central restriction is claimed.


## Triangle quotient and universal infinitude

```sh
python3 research/case_study/phase38_L003_universal_triangle_check.py \
  --output /tmp/triangle-check-new.json
```

The output path must be new. This standard-library checker verifies the
nine fixed relators in an abstract amalgam, the tenth word's uniform
formula, the subgroup projection witnesses, the involutory lift and the
exact polynomial reflection identities. The all-parameter spectral and
infinitude arguments are [written and reviewed](research/case_study/phase38_L003_universal_triangle_root_audit.md).
It does not recompute universal finiteness at parameters 2–5 or establish
historical novelty.


## Four-paper Compress_B manuscript factor

```sh
python3 research/case_study/phase38_compress_B_measurement.py \
  --input-root /path/to/verified-inputs \
  --output-dir /tmp/compress-b-measurement-new
```

Use Python with pypdf 6.13.0, Pandoc 3.10 and the recorded XeLaTeX toolchain.
The input root needs the bound authored artifacts/helper and the four primary
PDFs at their protocol paths. PDFs and full extracted source texts are not
redistributed. The output directory must be new. Add `--rasterize` with
Ghostscript to produce page images for a separate visual review. The runner
checks full-body spans, the complete proof/census appendix, exact extraction,
render diagnostics and every reported count. It does not reprove the
mathematics, rerun the group census or establish bibliographic priority.


## Exact triangle-wreath maps for both presentations

```sh
python3 research/case_study/formal/verify_lean.py TriangleWreathInvolutory.lean \
  --packages /path/to/pinned/packages \
  --lean /path/to/lean-4.32.2 \
  --output-dir /tmp/triangle-wreath-new
```

The runner includes the unchanged rotational module automatically and builds
absent mathlib objects in a private output overlay. It compiles the exact
ten-relator and fourteen-relator maps and their subgroup-surjection proofs.
Both infinitude transfers retain `Infinite (Triangle s)` as a hypothesis;
the spectral proof and universal geometry are outside these formal modules.
See the [fresh root replay and interface review](research/case_study/phase40_triangle_quotients_root_audit.md).

## Complete triangle and source infinitude

```sh
python3 research/case_study/formal/verify_lean.py TriangleReflection.lean \
  --packages /path/to/pinned/packages \
  --lean /path/to/lean-4.32.2 \
  --output-dir /tmp/triangle-reflection-new
```

The dependency closure includes both triangle-wreath modules. This proves
infinitude of all three exact presented groups for every natural parameter at
least six, with no remaining infinitude hypothesis. The [independent review](research/case_study/phase42_triangle_spectral_audit.md)
records its separate full source/interface reading and pinned replay; the root
also freshly rebuilt the three public modules. All twelve central axiom reports
use only `propext`, `Classical.choice` and `Quot.sound`. Universal hypertope
geometry and historical priority remain separate from this formal theorem.


## Conservative seven-source manuscript bound

```sh
python3 research/case_study/phase43_unified_lower_bound_measure.py \
  --input-root /path/to/verified-inputs \
  --output-dir /tmp/compress-unified-measurement-new --rasterize
python3 research/case_study/phase43_unified_lower_bound_root_recount.py \
  --input-root /path/to/verified-inputs \
  --render-dir /tmp/compress-unified-measurement-new \
  --output /tmp/compress-unified-recount-new.json
```

The bound input root needs the public protocol/helper/manuscript artifacts
and the six privately acquired primary PDFs and exact extractions listed
in the protocol. Use pypdf 6.13.0, Pandoc 3.10, the recorded XeLaTeX 2026
and Ghostscript toolchain. The first command freshly extracts and renders;
the second independently selects the source bodies and recounts all ten
metrics without importing the first command's counting helpers. Both refuse
to overwrite their outputs. Raster hashes bind a separate full visual review;
the commands do not perform visual judgment or reprove the mathematics.

The frozen runner's report retains its original pending-review label. The
[subsequent root audit](research/case_study/phase43_unified_lower_bound_root_audit.md)
admits only a conditional lower bound, with N001 credited zero. Neither
command estimates N001's length or supplies an exact seven-source factor.

## Chiral-cover finite certificate

```sh
python3 research/case_study/phase43_chiral_cover_verify.py \
  --gap /path/to/gap --output-dir /tmp/chiral-cover-new
```

Use stock GAP 4.15.1. The no-clobber runner checks six literal presentations
and mixes, actual subgroup intersections, mirror/cover/dual maps and a word
distinguishing the two minimal covers. It binds the entire output after the
historical universal-newline conversion and saves raw logs separately. No
source PDF, finite catalogue or RAMP is needed. GAP's exact algorithms are
trusted; this is not a Lean certificate. The [root proof review](research/case_study/phase43_chiral_cover_root_audit.md)
supplies the mathematical interfaces and minimality argument. The author's
old in-place Python runner and primary fulltexts are intentionally not exported.

## Two-source operations census

```sh
python3 research/case_study/phase40_compress_operations_verify.py \
  --gap /path/to/gap --output-dir /tmp/compress-c-new
```

The recorded run uses GAP 4.15.1 and TomLib 1.2.11, with the J1 data hash
bound in the reports. The output directory must be new. The runner first
checks that both full programs match the manuscript's code blocks, then runs
the construction and exhaustive classification, saving logs and class data.
The independent census took about 279 seconds; it reads a complete subgroup
catalogue, not a geometry catalogue. Its rank-five stage includes proper
subgroups and supports the written all-higher-rank exclusion.

The [independent mathematical review](research/case_study/phase44_operations_recent_audit.md)
also checks the general endpoint/geometry proofs and the complete required
lattice addendum. Running finite code does not prove those all-parameter
theorems or supply a C compression ratio. No source PDF is needed to rerun
the finite programs, but the bound primary sources are required for an
independent literature and statement audit.

## Exact quotient-intersection criterion

```sh
python3 research/case_study/formal/verify_lean.py QuotientIntersectionCriterion.lean \
  --packages /path/to/project/.lake/packages \
  --lean /path/to/lean --output-dir /tmp/quotient-intersection-new
```

This compiles the actual image-intersection/kernel-product equivalence and its
quotient and locally injective specializations. The [root audit](research/case_study/phase53_cover_kernel_root_audit.md)
records two fresh builds with pinned Lean 4.32.2 and all nine dependency
revisions. Four theorem axiom reports use only standard axioms. Geometry,
module classification, cover minimality and source-specific finite code are
outside the [formal scope](research/case_study/formal/QuotientIntersectionCriterion.scope.md).

## Complete finite cover interval

```sh
python3 research/case_study/phase54_cover_interval_verify.py \
  --gap /path/to/gap --output-dir /tmp/cover-interval-new
```

Stock GAP 4.15.1 reconstructs the literal source groups and the rotation group
of order 8,748. The program checks the order-nine kernel, exact defect, every
subspace, every invariant quotient, and both maximal admissible axes. It also
checks the scoped tetrahedral counterexample. The directory must be new;
raw and canonical logs are saved and the entire canonical output is bound.
The complete program matches the assembly in the
[independent review](research/case_study/phase50_cover_recent_audit.md).

No private primary capture or older manifest tree is needed by this command.
The preserved phase46 author runner has those private dependencies and is
not the public entry point. The [root admission](research/case_study/phase54_cover_interval_root_audit.md)
records the new runner and fresh replay. The support and central-kernel
theorems are written proofs; the finite program does not establish the
general cover conjecture or classify covers outside the specified interval.
