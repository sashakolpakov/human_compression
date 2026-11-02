# Reproducing the October corpus

The corpus formerly occupied the repository root. It now lives in
`october_corpus/`. Its existing tracked manuscripts, programs, manifests and
certificates are preserved with identical Git modes and contents. Their paths
are relative to this directory unless a record explicitly identifies a
historical commit or a private source location.

## Current entry points

Use a full-history clone. From the repository root:

```sh
git clone https://github.com/sashakolpakov/human_compression.git
cd human_compression
git fetch origin --tags
python3 -E -B scripts/check_corpus_layout.py
cd october_corpus
python3 -E -B scripts/smoke_check.py --quick
```

The layout checker reads the fixed migration commit from `../corpora.json`
and verifies it against commit `0466df5e0b0f1c83da3980c4e7b85c69cdca103a`.
At that migration, all 48,690 earlier tracked paths must appear under
`october_corpus/`, with their earlier modes and Git blobs, alongside the
declared new files. It separately checks the current checkout's Git
cleanliness. Later committed corpus additions remain possible. The
precommit `--index` mode also streams every staged working file; the default
historical check does not repeat that full-file scan. These are preservation
checks, separate from mathematical verification.

The quick suite reruns three selected certificates using ordinary Python 3.10
or newer. The [detailed guide](docs/REPRODUCING.rst) covers the other suites,
paper builds, Lean compilation, dependencies and trust boundaries. Interpret
its filesystem commands from `october_corpus/`. For example:

```sh
python3 -E -B scripts/build_papers.py --help
python3 -E -B scripts/check_project_lean.py --help
```

Follow the selected paper's portable reproduction instructions and exact input
pins. Some retained historical programs use earlier paths; their existence in
the archive is not a claim that they are current entry points.

## Current matrix certificates

From the repository root, replay the 2,308 supplied F004 certificates with:

```sh
python3 -E -B -S october_corpus/reproduction/matrix_certificates/verify.py
```

The [package guide](reproduction/matrix_certificates/README.rst) and
[written argument](reproduction/matrix_certificates/THEORY.rst) state the inputs,
provenance and mathematical assumptions. The program uses Python's standard
library, reads six pinned local JSON files and writes its result to standard
output. It needs no private source tree or historical absolute paths.

The expanded guarded replay passed all 2,308 certificates: 2,035 intersection
failures and 273 nongeneration cases. It used 1,391,673 charged input bytes,
145,447 matrix products and 16,989 RREF field operations, including the eight
common prefix sign systems. All 1,595 earlier cases are retained unchanged.
The 943,200 determinant terms remain separately counted under their unchanged
cap. The new graph certificate verifies 8,779 distinct reachable lines and
all 8,778 parent edges.

The program retains its 2 MiB total data-read limit, 1 MiB limit per JSON
file, 400,000 matrix-product limit, 200,000 RREF-operation limit and
100-second internal limit. No counter is reset. Its first expanded replay
finished in 2.915 seconds, with an observed peak of 62,291,968 bytes under
the 128 MiB outer guard.

This replay checks specified exclusions. The original group/model, frame,
membership and orbit associations, the previously accepted full centralizer,
finite Levi structure and maximal subgroup cover remain imported premises.
It adds no Lean verification or completed manuscript. The [current intake
ledger](INTAKE_STATUS.json) records all 3,779 positions in job 24 as resolved:
446 fail generation and 3,333 fail the intersection property. The linked
packages cover different parts of that ledger.
Earlier archives and their
recorded verification scopes remain unchanged.

The [fixed-line certificate](reproduction/fixed_line_orbits/README.rst) reconstructs
original position 59 and verifies its order-19 word, complete one-dimensional
fixed space and 9,241 distinct reachable vectors. Its guide gives all seven
guarded commands. All 56 checks and the complete case passed from both the
private and installed directories; its proof states the imported model and
complete subgroup classification.

The [cubic certificate supplement](reproduction/cubic_certificates/README.rst)
adds 42 intersection failures. Its two commands, from the repository root, are:

```sh
python3 -E -B -S october_corpus/reproduction/cubic_certificates/controls.py --manifest-sha256 f10a3e710a523922c4a4ade238be8d9f408dff3867b0f6b60cbd917b2a0fb4fa
python3 -E -B -S october_corpus/reproduction/cubic_certificates/verify.py --manifest-sha256 f10a3e710a523922c4a4ade238be8d9f408dff3867b0f6b60cbd917b2a0fb4fa
```

The supplement includes the original indexed catalogue and frame data. It
checks the cubic relation by nine direct row images, the scalar order by
independent companion-matrix powers, and all eight common-line systems by
exact Gaussian elimination. The original full model and classification
premises remain explicit imports. It does not complete F004.

## A bound from a universal presentation

The [presentation package](reproduction/coxeter_quotients/README.rst) checks
the four original matrices for F004, job 20, position 200. Run:

```sh
python3 -E -B -S october_corpus/reproduction/coxeter_quotients/verify.py --controls
python3 -E -B -S october_corpus/reproduction/coxeter_quotients/verify.py
```

All 24 controls and the complete case passed in private and installed
directories. The case uses 31 matrix products and 392 linear work units.
The written proof applies the attributed finite order of a universal
presentation to conclude nongeneration. The verifier checks the matrix
relations; it does not reprove the published presentation theorem or the
association with the source's indexed case. See the package's
[validation record](reproduction/coxeter_quotients/VALIDATION.json).

## Intersections of end subgroups

The [end subgroup package](reproduction/end_subgroups/README.rst) replays
eleven registered intersection failures from F004, job 20. Run:

```sh
python3 -E -B -S october_corpus/reproduction/end_subgroups/verify.py --controls
python3 -E -B -S october_corpus/reproduction/end_subgroups/verify.py --all
```

All 26 controls and all eleven certificates passed in private and installed
directories, with an independent audit of both executions and the exact
installation. The complete replay uses 782 matrix products, four row images
and 12,440 scalar work units. It checks the supplied prime-order words and,
where applicable, a fixed vector and a generator moving its line. The proof
uses the attributed group, natural module and complete maximal subgroup
cover. These are replays of existing exclusions, not new census results.
The package includes its TeX proof, provenance, explicit imports and
[validation record](reproduction/end_subgroups/VALIDATION.json).

## A word certificate for an intersection obstruction

The [word certificate](reproduction/finite_orbits_and_stabilizers/INTERSECTION_README.rst)
reproduces the registered intersection failure at F004, job 20, position 1099:

```sh
python3 -E -B -S october_corpus/reproduction/finite_orbits_and_stabilizers/verify_intersection_all.py --output /absolute/path/to/a/fresh/output
```

The command runs 24 arithmetic controls, ten input controls and the case in
separate guarded processes. All passed in private and repository directories;
an independent audit checked both runs. The case uses 107 matrix products.
It evaluates a 78-letter word in the left end and a word in the right end
squared, checks equality and excludes the result from the complete middle
subgroup. It needs no subgroup order certificate or classification theorem.
The original marking and faithful representation remain explicit provenance
premises. This replays an existing exclusion and adds no completed manuscript
or compression measurement.

## The singleton middle case

The [singleton middle package](reproduction/single_middle/README.md) contains
the complete producer, proofs, reviews and resource supervisor. Its README
gives commands from the package directory. The retained initial and
installed runs each passed 23 controls and recovered 1,209 ordinary half
graphs, giving 7,254 graphs in this stratum. This package uses relative
functional inputs and does not read the reference census as a target.

## The complete two-centre family

The [two-centre package](reproduction/two_centre/README.rst) enumerates all
ordinary sixteen-vertex halves for this intrinsic centre stratum. It includes
the singleton case and permits the zero endpoint columns required by the
other presentations. All 32 controls and the complete producer passed both
initially and in the installed directory: **1,395 halves**, giving **8,370
graphs** by the reviewed factor-six product. The strict 1,209-class stream is
a subset and is not added again. The complete streams agree byte for byte.

## Ordinary centre halves

The [centre-half package](reproduction/centre_halves/README.rst) gives sequential
commands for 57 controls, fourteen complete raw domains and four ordinary
unions. Initial and installed replays recover **2, 5, 36 and 115** classes,
with complete streams identical to the earlier accepted results. Its README
states all resource limits and distinguishes local file receipts from the
external evidence of execution. Generated jobs, runs and locks are ignored.

## The complete order-32 count

The [composition package](reproduction/order32_census/README.rst) gives commands
for the three existing component packages, fresh binding of their six complete
results, and the final scalar calculation. Its 43 controls and complete
installed run passed, recovering **25,408 = 16,467 + 8,941** ordinary classes.
Independent audit verified the complete streams, all 52 imported proof
documents, the nine disjoint contributions and the execution records.

The proof and numerical kernels are shared with the separately accepted
calculations. The composer does not export a new stream of all 25,408 full
graphs or supply a Lean proof of the hand arguments. Its replay record
separates this known-result recovery from F009's unfinished order-80 census.

## Fi22 marking certificates

The [portable Fi22 package](reproduction/fi22_markings/README.rst) adds 18
generation and six nongeneration certificates to the earlier archive. From
the repository root:

```sh
python3 -E -B -S october_corpus/reproduction/fi22_markings/verify.py --controls
python3 -E -B -S october_corpus/reproduction/fi22_markings/verify.py --index 160
python3 -E -B -S october_corpus/reproduction/fi22_markings/verify.py --index 166
```

To replay the whole package, run each index from 160 through 183 in a separate
invocation. Python's standard library and the three pinned repository proof
objects suffice. All 25 controls and 24 case replays passed; the installed
package also passed the controls and the two examples above. The written
generation argument, separate intersection theorem, imported premises and
actual replay records accompany the verifier. These certificates do not
complete the Fi22 classification.

The [following 48 cases](reproduction/fi22_markings/free_0200_0247/README.rst)
cover indices 200 through 247: 36 generation certificates, their separate
intersection proofs, and twelve exclusions. Run:

```sh
python3 -E -B -S october_corpus/reproduction/fi22_markings/free_0200_0247/verify.py --controls
python3 -E -B -S october_corpus/reproduction/fi22_markings/free_0200_0247/verify.py --index 200
python3 -E -B -S october_corpus/reproduction/fi22_markings/free_0200_0247/verify.py --index 203
```

All 25 controls and all 48 individual replays passed for this edition. The
installed package also passed its controls and the two examples above.
[VALIDATION.json](reproduction/fi22_markings/free_0200_0247/VALIDATION.json)
records the input hashes and individual outcomes. Existing proof objects are
shared with the earlier packages. No private working directory is required.

## Fi22 normalizer equations

The [normalizer package](reproduction/fi22_normalizer_equations/README.rst)
contains the complete 3,510-point permutations and two short words. Run:

```sh
python3 -E -B -S october_corpus/reproduction/fi22_normalizer_equations/verify.py --controls
python3 -E -B -S october_corpus/reproduction/fi22_normalizer_equations/verify.py --check
```

All 22 controls and the complete case passed in private and installed
directories. The checker verifies all maps are bijections, the 36
centralizations, and the five equations stated in the supplied lemma.
The full case used 5,363,830 work units under its shared ten-million-unit
limit. Python's standard library suffices; no private directory is read.

The S3 action uses imported membership in the ambient group. The normalizer
order 6,144 is conditional on the earlier identification of the entire
centralizer as a group of order 1,024. The package certifies no action on
the candidate bank and settles no additional bank rows. The
[validation record](reproduction/fi22_normalizer_equations/VALIDATION.json)
separates the equations checked here from those imported premises.

## Historical registration audits

Some integrity checks examine Git diffs and require the corpus to occupy the
old repository root. Their earlier assumptions remain unchanged. In
particular, use an explicit checkout of the last complete root edition to
replay that edition's snapshot registration:

```sh
git worktree add --detach /absolute/external/october-baseline \
  0466df5e0b0f1c83da3980c4e7b85c69cdca103a
cd /absolute/external/october-baseline
python3 -E -B scripts/verify_snapshot.py
```

Choose a fresh external path; the complete baseline tree occupies about
6.75 GiB before Git metadata. After the replay, return to the main checkout
and remove that temporary worktree with `git worktree remove` if no output
needs preserving. The current layout checker establishes preservation of the
baseline; replaying its snapshot verifier checks the historical registration.
Neither command reruns every mathematical computation.

Historical `commit:path` references keep their original, unprefixed paths.
Frozen provenance strings and source hashes are not rewritten to manufacture
agreement with a new location. Existing active private computations retain
their paths until their own inputs and outputs can be migrated safely.
