# Centralizer extensions of projective-line maniplexes

The application `phase258_projective_maniplexes.md` recovers the complete
principal PSL results of the eleven-page Leemans–Toledo manuscript dated
15May2023. It reuses the frozen TopicE umbrella and its exact ten-row table,
with a new explicit interface for string markings that need not satisfy
the intersection property. The final PGL conjecture is a separate task.

The packet also corrects three literal claims: an omitted infinite family
with S4 facets, the assertion excluding self-duality in Class1, and the
unqualified maximality assertion for involution centralizers. Exact PSL23,
PSL13 and A5 witnesses accompany full positive proofs. The inconsistent
hemi-icosahedral name following the source's {5,3} construction is corrected
to hemi-dodecahedral. These are corrections, not new open-question claims.

Run from this directory with a nonexistent output path:

```sh
python3 -B -O phase258_check.py \
  --out /private/tmp/phase258_fresh_replay \
  --gap /opt/homebrew/bin/gap \
  --lean /Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean \
  --packages /Users/sasha/bogachev/formal/.lake/packages
```

Add `--verify-primary` to verify the private primary PDF/text bindings.
Without that option all proof and code bindings remain checked; only
primary-source files are optional. The tested environment is GAP4.15.1,
Python3 and Lean4.32.2 with the dependency revisions in the retained
manifest. No network is used during replay.

The driver replays432local sggi markings, the retained10universal groups,
eight projective models, source-convention adapters and relevant negative
controls. It compiles three new all-rank Lean declarations and two reused
centralizer declarations with standard-only axiom reports. Formal scope is
set out separately. Bounded examples are diagnostics; the infinite ranges
and classification are proved in the written manuscript with retained
classical inputs.

All primary results retain their original attribution. Full shared
umbrella and program costs remain chargeable, and no numerical compression
rate or new principal count is awarded before independent review.
