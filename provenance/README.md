# Provenance and verification scope

The research was developed with an LLM and coordinated agents. Independent
agent checks are internal reviews, not external peer review. The model family
reported by the working session was GPT-6; no claim is made about unrecorded
sampling settings or the exact model assigned to every earlier subtask.

`original_files.json` records the hashes of the internally verified working
artifacts before publication preparation. The public `snapshot_manifest.json`
records the files actually distributed here. Publication edits replace local
source-file links with citations, remove private machine paths, make runners
portable, and update navigation and scope statements.

Generated GAP logs and numerical witnesses retain the bytes bound by their
certificates, including trailing spaces emitted by GAP. `.gitattributes`
exempts that generated output from the trailing-space style check.

The later 2003/2004 intake adds an introduction, a uniform paper registry,
semilinear descent and geometric shadow-IP notes, and two new exact Python
checks. The older classification track adds a fresh GAP thin-geometry census,
source-witness verification, automorphism fusion and explicit group identification.
These additions are not present in the initial `original_files.json`;
their reviewed bytes are included in the current snapshot manifest. The
new [reproduction record](older_intake_reproduction.json) identifies fresh
runs separately from the original quick/full-suite record. The older source archive is represented by metadata
only, including the hashes of its members.

The 1998–2005 network intake adds the complete arbitrary-Borel J2 census,
the uniform dihedral and tree-cut derivations, and the Suzuki realization
audit. Their own records bind the actual executed checker bytes and the
written-proof review scope. The 146 J2 terminal checkpoints are newly
computed output, not copied source geometry lists. The new Boolean-shadow
Lean module has its own successful compiler report; the previous nine
modules and their historical reports remain unchanged.
The [public Boolean-shadow compilation](boolean_shadow_public_compile.json)
is an additional fresh run through the portable runner, including compiler
version and pinned dependency-revision checks.

The weighted-tree extension adds an eleventh certificate, ConsecutiveShadow.
Its saved report records a fresh compilation through the portable runner,
which also freshly compiled its BooleanShadow prerequisite. The previous
ten historical reports remain unchanged. The weighted-tree finite checker
has a separate report binding its source bytes and the explicit finite scope.

The twelfth certificate, RankThreeFactorization, records another fresh
compilation. It proves the abstract coset common-point implication used for
flag transitivity of the Suzuki example. Its theorem prints only `propext`;
the exact matrix and maximal-subgroup inputs remain outside Lean.

The thirteenth certificate, CosetCoordinates, generalizes the attachment
implication to an arbitrary family of cosets, assuming surjectivity onto
their coset coordinates. The fresh compile also rebuilt its prerequisite
without overwriting that prerequisite's historical report. The all-rank
Suzuki descent and torus instantiation remain written mathematics.

The next common-engine runs exhaust M22 and M23 using 360 terminal anchors
and independently recognize 105 witnesses. Archived source lists are used
only for a separate post-hoc comparison. The metacyclic cyclic-TPP theorem
has an independent internal proof audit and arithmetic rerun; its separate
order-512 SmallGroups census extends the hypertope bound through order 2^12.
Their certificates record precise scopes and retained catalogue inputs.
The [phase-seven review record](phase7_review.md) distinguishes fresh
executions, full written-proof reviews and artifact-integrity checks.

The fourteenth certificate, IntertwinerSeparation, proves a general ring
criterion forcing an intertwiner to vanish. Its two theorems report no
axioms. Matrix normal forms and their exhaustive coverage remain separate
written inputs; this is not an end-to-end maximum-rank formalization.
The [phase-eight review record](phase8_review.md) records the complete
proposed rank proof, its broader form alternative and the two additional
older construction analyses.

The [phase-nine review record](phase9_review.md) records the first matched-proof
measurement and new linear/unitary consequences of the same form theorem.
Its fifteenth Lean certificate checks actual transvection invariance of a
matrix. The frozen written application predates that certificate and retains
its original hashes; the separate scope note records the later formalization.

The [phase-ten review record](phase10_review.md) adds the two-coordinate
Suzuki derivation, the uniform small-factor bound and the explicit PSU4(5)
matrix certificate. Its sixteenth Lean module proves the abstract
involution-centralizer rank obstruction. New fresh executions are recorded
separately from historical reports; the source classifications retained by
each argument remain explicit. [Export provenance](phase10_original_files.json)
records the original hashes and the one documentation-link adjustment.

[Measurement](../MEASUREMENT.md) records a conditional 3.34× ratio for two
exact counting formulas and the separate status of new resolutions. No
corpus ratio or infinity marker is assigned by this publication snapshot.

Historical reports retain their original mathematical-source hashes and run
results. Where a script's executable path was made portable, its historical
report describes the original run; it is not relabeled as a fresh execution.
The snapshot checker reports this distinction. The smoke runner and portable
Lean runner keep fresh results separate. Legacy Python/GAP scripts can overwrite
their adjacent reports; run those in a disposable copy as described in
[REPRODUCING.md](../REPRODUCING.md).

The `research/leemans` compatibility symlink points to `research/case_study`.
It preserves the relative paths used by the original GAP scripts without
changing their source or silently rewriting their checksums.

External PDFs, extracted texts and GAP library inputs are identified by source
metadata and checksums. Their absence from the public snapshot is intentional.
A checksum identifies bytes; it is not a proof that the mathematical claim is
correct or that an external catalogue is complete.
