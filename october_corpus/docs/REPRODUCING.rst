Reproducing the October corpus
==============================

The `current reproduction guide <../REPRODUCING.md>`_ gives the corpus checks,
selected mathematical replay commands, build instructions and storage guidance.
Paths in corpus packages are relative to ``october_corpus/``.

From the repository root, run::

    python3 -E -B scripts/check_corpus_scope.py

This checks the 102-manuscript catalogue, 101 completed mathematical treatments,
53 measured applications and 19 topics. It executes no numerical searches.

For mathematical reproduction, select a paper from
``papers/latest_catalogue.json`` and follow its publication guide and exact
source edition. Shared theory, local proofs, required programs and retained
inputs belong to the selected proof contract. Formal compilation and paper
rendering have their own declared dependencies and verification scopes.

Keep scratch files outside the checkout. Historical snapshot checkers validate
the exact archived editions named by their records.
