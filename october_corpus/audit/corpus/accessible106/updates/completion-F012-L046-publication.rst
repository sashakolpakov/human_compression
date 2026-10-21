Checking the catalogue publication layer
========================================

The F012/L046 catalogue correction is an administrative successor to public
commit ``de0864a7bde3c992239427d3c838fe0fe8ea370d``. The historical F012
registration, its exact checker and reviews, and the previous global
publication manifest are unchanged. Their reviewed publication remains an
acquired premise; this layer does not rerun scientific routes or rehash the
whole inherited publication.

From a full-history checkout, the current entry point remains::

    python3 -E -B scripts/verify_snapshot.py

It verifies the exact two-row catalogue derivation from the already-public
F012 and L046 admissions, all other 104 entries, the unchanged 102/105
partition, both pointer-only edits and the exact dispatcher Source inverse.
It checks every declared new administrative file and preserves inherited
tracked identities through Git. The old reviews still name their original
code and dispatcher; they are not reused as reviews of the new validator.
The new layer has its own noncyclic seven-file publication declaration.

Before registration, a reviewer may check the candidate without staging::

    python3 -E -B scripts/catalogue_completion_registration.py

That command reports ``PASS_CANDIDATE_CATALOGUE_PUBLICATION_LAYER`` and lists
untracked declared files. The advertised entry point requires all of them to
be tracked. Neither command checks the mathematical arguments again, compiles
Lean, repeats group censuses or removes the explicit source/software premises.
A successful metadata check is not a fresh clean-machine scientific replay.
F004, F009 and L026 remain incomplete.
