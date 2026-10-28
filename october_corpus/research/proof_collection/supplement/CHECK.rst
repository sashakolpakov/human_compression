Check the supplement's file integrity
======================================

From a clone's october_corpus directory, run::

    python3 -E -B -S research/proof_collection/check_integrity.py \
      --corpus-root "$PWD" \
      --manifest research/proof_collection/supplement/manifest.json \
      --manifest-sha256 8a6a6632ae810179f1f91a253dc140cb81afafa0d0f5089b597013b2bdb95302 \
      --self-sha256 d84128ef725e52650330c68b31109ded146da00712b96d5a8740d17492af37fb

The command checks every whole file listed in the supplemental manifest.
It runs no scientific program and establishes no new arithmetic, Reader,
model or theorem result. Use the separately pinned base manifests for their
complete archived-body integrity checks.

This file and manifest.json are authenticated separately by the publication
plan. Their bytes are outside the manifest's own file list to avoid circular
hashes. Every other selected supplement file is included in that list.
