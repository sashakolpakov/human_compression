Accepted census checkpoint 11,584
================================

Checkpoint 11,584 has 6,073 nodes, 193 pending families, one reserved debt
and 718,412 selected raw leaf records. From accepted checkpoint 11,519,
the run completed 25 families and refined five, adding 25 node records
and 33,886 selected raw leaves in 65 transactions. Pending families remain
unpaid; the ordinary census is unfinished.

The actual Native run, independent strict Reader and canonical registration
passed. This archive retains their exact Source versions, selected inputs,
raw outputs, reviews, resource records and registration evidence. Existing
public objects are reused by whole byte identity. All 21 named historical
payloads keep their earlier attribution. Their mapping is not a claim that
the complete historical Saved-state dependency cut has been exported.

The successful Native used caller 84a and workspace b348. The later strict
Reader used caller 79f and exporter 1a74 with the explicit policy
F009_CURRENT_REFERENCE_WIRE_QUOTA_V2. The old virtual-only wire admission
was retired; actual raw 64 MiB and packed 8 MiB checks and full mathematical,
typed/order/LF/inverse predicates remain. The separate registration metadata
policy permits up to 3 GiB of aggregate physical reads while retaining a
2 GiB unique input domain. policies.json records the exact Source identities.
Later V2 Native code is not attributed to the successful Native run.

The Reader's observed outer process-tree peak was 534,855,680 bytes under
a 536,870,912-byte cap. Its Owner sampled family peak was 475,774,976 bytes.
The outer headroom was 2,015,232 bytes. These are sampled observations,
without a causal memory-saving claim or promise for a future run.

Reproduction scope
------------------

From october_corpus, use the manifest in the checked-out Git revision::

  census_manifest=research/proof_collection/updates/verified_intake_results/census_checkpoint_11584/manifest.json
  census_manifest_sha256=$(python3 -E -B -c 'import hashlib,sys; print(hashlib.sha256(open(sys.argv[1],"rb").read()).hexdigest())' "$census_manifest")
  python3 -E -B research/proof_collection/check_integrity.py \
    --corpus-root "$PWD" \
    --manifest "$census_manifest" \
    --manifest-sha256 "$census_manifest_sha256" \
    --self-sha256 d84128ef725e52650330c68b31109ded146da00712b96d5a8740d17492af37fb

This checks whole selected bytes and their original-to-relative mappings.
It does not execute Native, Reader, graph or theorem verification. Thus
scientific_replay_status is NOT_ACQUIRED_BY_THIS_EXPORT. A fresh portable
mathematical replay requires a separately reviewed dependency cut and
resolver, followed by an actual semantic Reader run. It is separate work.

Original absolute paths are provenance only. There is no private fallback.
Machine environments, compilation caches and unrelated global registry
images are excluded; imported_boundaries.json states that boundary. Actual
failed, refused, successful and unrun records retain their recorded statuses.
Old archives and objects remain unchanged. Publication adds no completed
manuscript, conjecture proof, Lean result or compression measurement.
