# Independent interval-lifting review

Accepted exact contracts and limitations are in
`phase279_interval_review.md` and its ten-row source contract. Author
manifest: `phase277_export.json`, SHA256
`72e92ed82299be8c658c2f3cb45f75e67f81b0fb48379fb052de05ea3d1007c9`.

With author and review files in their bound relative layout:

```sh
python3 -B -O phase279_check.py --out /fresh/output
```

This verifies all bytes, reconstructs the independent rotation/reflection
model and compares every parabolic order and base intersection failure
with the author's distinct binary-cocycle model. It requires only Python's
standard library. For a fresh full author replay and Lean compilation:

```sh
python3 -B -O phase279_check.py --out /fresh/full-output \
  --author-replay --lean /path/lean --packages /path/.lake/packages
```

Lean 4.32.2 and mathlib revision
`905b95818eb32af7874a58b427f50c1711a5e96c` are required. Optional
`--verify-primary` verifies the two external PDFs recorded in
`phase277_sources.json`; primary PDF bytes are not distributed.

The review allowlist is exactly `phase279_manifest.json`. No primary text,
PDF raster or compiled Lean cache is exported. The three-page interval
paper and two-page obstruction paper were all visually inspected. The
separate rank-five/deletion exploration file is excluded. No whole-source
credit, full all-rank finite theorem, global prime-power claim or complexity
ratio is inferred from this acceptance.
