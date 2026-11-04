F004 accepted-certificate byte preservation
==========================================

One continuous tar.xz stream (LZMA preset 3), split into 32MiB parts. MEMBERS.json
lists 45 unique bodies and all 102 original record/closure aliases for the frozen
baseline 51 accepted rows. Every selected body, including bodies above 1MiB, was
streamed, decompressed and rehashed against its exact accepted pin. No Original
value was parsed and no GAP, project, control or verifier function was executed.
Originals are unchanged. No historical stdout or failed scratch is included.

Verify all compressed-part hashes, concatenate parts in zero-padded order, then
decompress as ONE xz stream. Restore only into fresh safe staging, rejecting
absolute paths, parent traversal, links and unknown/duplicate members. Verify
every staged size/SHA256; materialize the explicit original aliases only after
Root-owned exact restoration/rebinding. This does not authorize code execution.

The paired ../inventory/ packet preserves the canonical model, 194 job records,
current 145 pending list, current 127 global registry snapshots and small accepted
anchors. This certificate packet preserves the actual 51-row baseline result
basis, not just counters. It does not newly revalidate all 127 jobs or claim a
recursively audited proof archive for every later descendant. No case credit,
Git/network mutation, deletion or whole-manuscript completion is inferred.

One writer, 64KiB maximum streaming/decompressed block, observed RSS below 128MiB,
and 1GiB minimum free disk checked at each 32MiB part boundary.
