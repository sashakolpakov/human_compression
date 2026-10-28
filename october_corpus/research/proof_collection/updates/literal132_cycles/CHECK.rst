Check this appendix's file integrity
====================================

From a clone's october_corpus directory, run::

    python3 -E -B -S research/proof_collection/check_integrity.py \
      --corpus-root "$PWD" \
      --manifest research/proof_collection/updates/literal132_cycles/manifest.json \
      --manifest-sha256 19eddc0bb1a848c7cc3a86caa4f85fb75883ffeb02ad6d65fb6f605185ef97b6 \
      --self-sha256 d84128ef725e52650330c68b31109ded146da00712b96d5a8740d17492af37fb

This checks listed whole files only and runs no scientific Source. The
manifest and this command file are separately authenticated by the copy plan
to avoid circular hashes. Every other selected appendix file is listed.
