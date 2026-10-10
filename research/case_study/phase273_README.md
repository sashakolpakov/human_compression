# Independent rank-four two-cover review

The exact theorem and limits are in `phase273_rank_four_review.md`; the
16-row source and proof map is `phase273_source_contract.json`. The author
packet remains byte-for-byte frozen at `phase256_export.json`, SHA256
`8d22baec4ddafcbb624300e7c65a23079982be724181b8282fafd512c70503ea`.

The six-model independent cellular check uses only Python's standard
library and imports no author program:

```sh
python3 -B -O phase273_check.py --out /fresh/output
```

With the pinned Lean installation and mathlib packages available, also
repeat the complete author computation and compilation:

```sh
python3 -B -O phase273_check.py --out /fresh/full-output \
  --author-replay --lean /path/to/lean --packages /path/to/.lake/packages
```

Lean version: 4.32.2. Mathlib revision:
`905b95818eb32af7874a58b427f50c1711a5e96c`.
Optional `--verify-primary` verifies the five external primary PDFs listed
in `phase256_sources.json`. Their bytes are not distributed in this review.

The runner requires the 16 frozen author exports and four listed frozen
dependencies in the same relative layout. It first checks their hashes
and all review exports, then requires exact agreement of the independently
reconstructed cellular result. Existing output paths, including dangling
symlinks, are rejected. The result cannot upgrade finite tests to a proof
of the quantified surface theorem; that theorem is accepted by the
complete independent written audit.

Distributed review artifacts are exactly the allowlist in
`phase273_manifest.json`. Primary PDFs, source transcriptions, rendered
page rasters, cached Lean objects and temporary replay directories are
excluded. All seven author PDF pages were read visually. No public file
was edited by this reviewer.
