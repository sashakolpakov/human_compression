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

From the repository root, replay the 1,595 supplied F004 certificates with:

```sh
python3 -E -B -S october_corpus/reproduction/matrix_certificates/verify.py
```

The [package guide](reproduction/matrix_certificates/README.rst) and
[written argument](reproduction/matrix_certificates/THEORY.rst) state its inputs,
provenance and mathematical assumptions. The program uses Python's standard
library, reads five pinned JSON files beside it and writes its result to
standard output. It needs no private source tree or historical absolute paths.
Its first guarded replay passed all 1,595 certificates: 1,322 intersection
failures and 273 nongeneration cases. It used 1,245,951 charged input bytes
and 102,923 matrix products, with 5,810 inherited RREF operations and
943,200 separately counted determinant terms. The package contains all
cases of the earlier 285-case edition preserved in Git history.

The new 1,310 intersection certificates use supplied fixed rows and explicit
minors of order six. Their 943,200 determinant terms have a separate counter;
they do not reset or increase the inherited 200,000-operation RREF limit.
The program retains the 2 MiB total data-read limit, 1 MiB limit per JSON
file, 400,000 matrix-product limit and 100-second internal limit.

This replay checks supplied exclusions, not a complete classification.
The original group/model correspondence, frame and orbit associations, and the
maximal subgroup theorem used by the intersection argument remain borrowed.
It adds no Lean verification or completed manuscript. The [current intake
ledger](INTAKE_STATUS.json) separates these 1,595 cases from the historical
1,089 exclusions and the 922 unresolved positions. Earlier archives and their
recorded verification scopes remain unchanged.

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
