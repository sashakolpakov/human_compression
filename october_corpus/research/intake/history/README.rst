Intake progress history
=======================

The archive preserves cold root-level JSON snapshots as exact opaque bytes.
Every member was checked against its original before removal. Current and active
files, all subdirectories, proofs and scientific case outputs were retained.

To restore the original snapshot names before using a historical consumer::

    mkdir -p /path/to/maintenance/intake/progress
    tar -xJf progress_snapshots.tar.xz -C /path/to/maintenance/intake/progress

The JSON manifest records sizes and SHA256 digests for the archive and members.
This is lossless storage cleanup; it adds no mathematical validation or case credit.
