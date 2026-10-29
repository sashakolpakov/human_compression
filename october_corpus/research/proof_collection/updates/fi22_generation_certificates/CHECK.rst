Check the archived files
========================

From the cloned october_corpus directory, run::

    python3 -E -B -S research/proof_collection/check_integrity.py \
      --corpus-root "$PWD" \
      --manifest research/proof_collection/updates/fi22_generation_certificates/manifest.json \
      --manifest-sha256 51723279b40fbed4717283112dee97a8eecd71834ac8dd0d8e89b3755c0ec8be \
      --self-sha256 d84128ef725e52650330c68b31109ded146da00712b96d5a8740d17492af37fb

This whole-file integrity check opens no original machine paths and imports no
scientific Source. It does not verify the group action or repeat the supplied
prime-cycle checks. The manifest and this command file are separately pinned
by the export plan; all other selected files appear in the manifest. The four
base manifests retain their separate original integrity commands and scopes.
