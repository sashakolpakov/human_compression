# Corrected proof spans for the thirteenth-source candidate

10 October 2026. Root-authored correction prompted by independent phase114
review. The phase110 manuscript and all frozen originals remain unchanged.
The authoritative corrected ledger is
`phase116_commuting_pairs_corrected_ledger.json`; the original phase110
ledger and its structural PASS are historical records with a known defect.
Independent mathematical review and source admission remain separate.

The original builder searched for the next heading in a substring starting
one codepoint after the current final heading began. Removing that first
hash changed `###` into `##`, so the same heading immediately matched the
next-heading expression. All sixteen new L066 proof spans were truncated:
twelve contained only one hash; the four multi-subsection spans omitted
the body of their intended final subsection. In particular the two main
counting formulas lacked the exceptional-degree proof in their bindings.
Their proofs were present in the complete manuscript.

The additive correction first verifies and rebuilds the unchanged phase110
package. It finds all heading positions in the complete manuscript and
selects the first heading strictly after each final subsection heading.
It binds the entire resulting interval, including the final subsection's
body. The four complete intervals, in Unicode codepoints, are:

| Subsection | Start inclusive | End exclusive |
|---|---:|---:|
| 25.1 | 205517 | 207121 |
| 25.2 | 207121 | 211564 |
| 25.3 | 211564 | 214771 |
| 25.4 | 214771 | 217227 |

The original sixteen-item subsection map is preserved. Each corrected
interval must contain designated equations or substantive phrases tied to
that result, including the exceptional classification for Theorems 1.1
and 1.2 and the regular-polyhedron qualification for Theorem 4.4. These
checks establish binding integrity; the independent reviewer must still
judge whether the text actually proves its source contract.

All 120 earlier contract rows remain identical to phase110, and the
351,348-byte manuscript, all eleven full programs and all prior source
inputs are unchanged. No mathematical proof, source count, Lean component,
length denominator or novelty claim is added by this correction.

Replay with distributed nonprimary inputs only:

```text
python3 -B -O phase116_commuting_pairs_correction.py --output NEW-report.json
python3 -B -O phase116_commuting_pairs_controls.py --output-dir NEW-controls
```

To regenerate the corrected ledger in a new directory, use `--build-dir`
instead of `--output`. Verification accepts an optional `--expected-ledger`
for explicit comparison. The controls reject the original defective ledger
and two self-consistent altered span/hash combinations. They also refuse
existing files, directories and dangling symlinks in both output modes.
The portable replay contains only the 27 original exports, three retained
public predecessors, and the correction program and corrected ledger.

The independent reviewer discovered the issue before admission. This record
does not retroactively relabel the original structural checks as detecting
it, and the old verifier must not be used as the sole ledger-admission check.
