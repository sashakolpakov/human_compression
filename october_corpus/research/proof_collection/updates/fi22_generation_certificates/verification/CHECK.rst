Check the actual publication evidence
=====================================

From the cloned october_corpus directory, run::

    python3 -E -B -S research/proof_collection/check_integrity.py \
      --corpus-root "$PWD" \
      --manifest research/proof_collection/updates/fi22_generation_certificates/verification/manifest.json \
      --manifest-sha256 b3a104cd54eee75e02935066f5737f11942f85731956d225cc9751f63fa6631c \
      --self-sha256 d84128ef725e52650330c68b31109ded146da00712b96d5a8740d17492af37fb

This checks the completed archive's publication evidence and aliases as files.
It performs no mathematical replay. The separate original archive CHECK.rst
checks the unchanged342-file snapshot. This command and its manifest are
separately pinned by the new copy plan; every other selected file is listed.
