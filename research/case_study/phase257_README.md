# Four infinite PGL families

The [manuscript](phase257_four_families.md) proves the four-family
conjecture at the end of Section 5 of Leemans and Toledo's May 15, 2023
author manuscript. Each row gives a regular rank-four maniplex with one
full PGL end and the indicated other end:

| Other end | Primes in the construction |
|---|---|
| S4 | p > 5, p congruent to 3 or 5 modulo 8 |
| A5 | p congruent to 9 or 11 modulo 20 |
| PSL2(p) | p congruent to 5 modulo 12 |
| PGL2(p) | p > 3, p congruent to 3 modulo 4 |

Dirichlet gives infinitely many primes in each row. The source asks
for four infinite families, not a complete classification or every q.
The [six-page PDF](phase257_four_families.pdf) contains the complete
written argument relative to the explicitly retained centralizer and
classical subgroup inputs. Publication admission awaits independent
review of this frozen author packet.

The source's centralizer-extension method and normalized matrix family
are attributed explicitly. The additions are the determinant conditions
and the proofs that the opposite end is full in all four cases. A bounded
priority search is recorded separately by the reviewer; no first-proof
claim is inferred from failure to find a later paper. This answers one
recorded question and does not itself recover a historical principal
contract or establish any compression rate.

The GAP certificate constructs 16 actual marked groups using the action
of GL2 on row lines. The separate independent implementation uses
fractional linear maps. The [formal scope](phase257_formal_scope.md)
records the eleven Lean matrix/root-group declarations and all remaining
written obligations. Neither finite samples nor these declarations alone
prove the all-prime theorem.

Replay with a fresh output directory:

```sh
python3 -B -O phase257_check.py --out NEW_OUTPUT --gap GAP_EXECUTABLE \
  --lean LEAN_EXECUTABLE --packages MATHLIB_PACKAGE_DIRECTORY
```

The default checks all public retained inputs. Add `--verify-primary`
only if the privately acquired primary files are present at their bound
paths. Their full texts and page images are not distributed. The runner
pins GAP 4.15.1, Lean 4.32.2 and all Lean package revisions; it replays
all finite samples, compiles the eleven declarations, and requires three
semantic rejection controls to fail as intended.

See `phase257_contract.json`, `phase257_source_ledger.json` and the
frozen `phase257_manifest.json` for the exact statement, dependencies,
proof spans and byte bindings.
