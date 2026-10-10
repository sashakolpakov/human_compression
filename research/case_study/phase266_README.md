# Formal polynomial steps for the primitive-square proof

This packet adds six Lean declarations to the existing complete written
argument in `psl2_square_proof.md`. The retained proof and all its old
certificates remain unchanged. The exact formal boundary is in
`phase266_formal_scope.md`; a separate independent review of the complete
arithmetic argument is being prepared in phase267.

Use a fresh output directory and the pinned dependencies:

```sh
python3 -B -O phase266_check.py --out /tmp/NEW-polynomial-check --lean LEAN_4_32_2 --packages PINNED_PACKAGES
```

The replay checks package revisions, compiles the actual polynomial and
derivative proofs, inspects their axiom reports, and checks four concrete
counterexamples to omitted hypotheses. The retained arithmetic witnesses
and finite reduction are separate parts of the complete written proof.
The old finite drivers use assertions: run their replays without Python's
`-O` option, in an isolated copy because the witness driver writes its report
beside its own source. The new phase266 driver uses explicit checks and is
valid under `-O`.

No whole-conjecture formalization, historical priority, additional question
entry or source-compression credit is claimed. Frozen files are bound by
`phase266_manifest.json`.
