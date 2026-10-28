Check the archived files
==========================

From the cloned october_corpus directory, run::

    python3 -E -B -S research/proof_collection/check_integrity.py \
      --corpus-root "$PWD" \
      --manifest research/proof_collection/updates/fi22_invariant_subsets/manifest.json \
      --manifest-sha256 cd206a3f37cf82aa9b769f2871866b813bd1cadc7b2d6ab88db7a78761eaa88f \
      --self-sha256 d84128ef725e52650330c68b31109ded146da00712b96d5a8740d17492af37fb

This checks listed whole files and opens no historical machine paths.
The manifest and this command file are separately authenticated by the copy
plan. Every other selected appendix file is listed in the manifest.
The three prerequisite manifest files have their own archived integrity
commands; run those to inspect their complete proof banks as well.
No mathematical replay of the archived absolute-path worker is claimed.
