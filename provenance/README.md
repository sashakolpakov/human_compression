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
