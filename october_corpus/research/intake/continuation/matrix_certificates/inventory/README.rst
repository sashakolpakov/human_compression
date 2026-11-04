F004 canonical inventory: opaque byte preservation
==================================================

The chunks form ONE continuous tar.xz stream, split at 32MiB. MEMBERS.json lists
every uncompressed member and compressed-part size/SHA256. LZMA preset 3 is used.
The writer streamed at most 64KiB at a time under 128MiB observed peak RSS.
Every part was rehashed and every member was decompressed and rehashed after
packing. No Original value was parsed and no GAP/project/control function ran.
All originals remain intact. Root alone authorized this finite archive write.

For restoration: first verify every chunk's size/SHA256, concatenate parts in
their zero-padded numeric order, decompress as ONE xz stream, and inspect the tar
member list before extraction. Extract only under a fresh staging directory,
refusing absolute paths, parent traversal, links and unknown/duplicate members.
Recheck all staged member sizes/SHA256 against MEMBERS.json before any explicit
Root-owned restore/rebind. Never execute an archived file merely to unpack it.

This preserves 194 canonical third records, two pair records, the exact model,
global ledgers and selected Source/accepted-reference snapshots. It avoids the
813MB frontier stdout originals. Accepted 127-job certificate closure is not
fully certified by this bank: remaining large refs are explicitly listed.
No manuscript completion, additional census result, permission to delete other
uncovered evidence, or mathematical replay is claimed.
