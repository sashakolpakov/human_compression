Completed replay of twelve Fi22 certificates
============================================

The corpus-relative checker passed for all twelve adopted invariant-set
certificates. It freshly checked 3,009 supplied points and both rotation
images of each point, for 6,018 closure edges. All original owner identities
and witness hashes agree with the earlier adopted proofs. Nine synthetic
control groups also passed under the final control program's own identity.

Every active proof input came from the repository. There were zero reads from
historical machine paths. The run read 3,172,921 bytes across 30 files, used
6,536,655 metered work units, and reached about 31 MiB of process memory.
The existing input, work, time and memory limits were retained.

The original model, membership, faithful action, geometry and complete maximal
subgroup classification remain stated premises. This replay adds no new
nongenerating case, generation result, completed manuscript, conjecture answer,
Lean proof or compression measurement. The twelve cases were already adopted;
this checks their arithmetic through a reproducible repository interface.

From the october_corpus directory, reproduce the arithmetic with::

    python3 -E -B -S research/fi22/triangle_quotients/invariant_subsets/replay/verify.py \
      --corpus-root "$PWD" \
      --self-sha256 60dad5b29f206150eb4d6f1ede8b653042d67332d69bd9ac1ec9916874fbe3b6 \
      --plan research/fi22/triangle_quotients/invariant_subsets/replay/plan.json \
      --plan-sha256 76bb2d71f2ce9bb2eb49be614083216178fcef8b5a375db7b1356edae31db68b

The full observed result is verification/replay_guard/stdout.log. The actual
execution record, resource guard, independent review and complete source
inverses are retained in verification/. Both the earlier control run and its
later reporting correction retain their exact separate identities.

The complete 70-file packet also passed the relative integrity checker::

    python3 -E -B -S research/proof_collection/check_integrity.py \
      --corpus-root "$PWD" \
      --manifest research/fi22/triangle_quotients/invariant_subsets/replay/manifest.json \
      --manifest-sha256 3b5ee5706ed1267743db28b07e05f5d329e0aa8d5edc84154edd1bb12ca2bf65 \
      --self-sha256 d84128ef725e52650330c68b31109ded146da00712b96d5a8740d17492af37fb

Integrity authenticates the files and mappings. The first command performs
the point arithmetic. Neither command reproves the imported classification
or model identifications.
