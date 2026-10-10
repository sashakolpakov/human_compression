# Independent review of the public two-primary replay interface

Date: 2026-10-10. Result: **PASS**, for the exact wrapper and mathematical scopes below. This is an additive interface audit; the complete written proof and original program reviews remain phase73 and phase74.

The reviewed wrapper is `phase80_two_primary_verify.py`, SHA-256 `448ca96943d25673fccc2f942f60a728cff68ae87a37c1ce78b8de9a7fdd5df2`. Its private and prepared-public bytes are identical. I read the entire wrapper. Its two hard-coded review-manifest hashes bind all **33** distributed inputs, including the proofs, ledgers, original programs, certificate data, original reports, and independent reviews. The manifest hashes are checked before their content is trusted; conflicting or nested filename bindings are rejected. All 33 public files match their private counterparts and their reviewed hashes.

## Fresh isolated execution

I copied exactly these 33 inputs plus the unchanged wrapper into `/private/tmp/phase81-two-primary-isolated`. The wrapper ran under **optimized Python (`python3 -O`)**, using stock GAP 4.15.1, with a new output directory `/private/tmp/phase81-two-primary-replay`. It invokes no historical Python wrapper, private source PDF, unlisted research seed, or external subgroup catalogue. The three byte-identical GAP copies completed in **51.375268167 seconds** in total: 37.496256583, 9.472618209, and 4.406393375 seconds. All exited zero with empty stderr. This is my fresh run, separate from the root agent's run.

Both complete canonical logs match the independently reviewed historical outputs exactly:

- Construction and extension census: `1f3bba0c157b740812e7a6a3d429c70ec42282466e18893f7a332987d8b7bff2`.
- Coprime obstruction cross-check: `4500327a51a025851187205c0176811666d72475f9c37277d452a5427cc924be`.

Canonicalization changes only CRLF and bare CR to LF. The wrapper's pass criterion requires three successful executions, both whole-log hashes, GAP version 4.15.1, and unchanged original and executed program hashes. Merely printing a success tag would not pass. Raw stdout/stderr, the fresh report, and both canonical logs are retained in this audit's exact export allowlist.

The Python certificate verifier independently reconstructs the supplied permutation action by exact arithmetic: degree 128, group order 1024, medial subgroup order 8 equal to the point stabilizer, and the marked quotient relations. It checks the distinguished defect word, the exact end intersection, literal agreement between the JSON coefficients and embedded GAP coefficients, and all 55 integer terms. Its result is

\[
y=e_1-e_2-e_{39}+e_{77},\qquad d=e_{40}-e_1,
\qquad\sum n_i y w_i=-2e_1+2e_{40}=2d.
\]

This wrapper implementation explicitly adapts my phase74 sparse checker. Its fresh execution is additional reproducibility evidence, **not an independently invented second certificate or second mathematical proof**. Stock GAP's exact group algorithms and Python integer arithmetic remain computational dependencies.

## Rejection and preservation checks

My separate `phase81_two_primary_interfaces_check.py` runs through the optimized command-line interface on isolated copies. All **11** individual mutations were rejected before an output directory was created: each of the two proofs, each of the three GAP programs, both certificate-data JSON files, both independent review manuscripts, and both review manifests. Each mutation appended a newline, so even a mathematically harmless change invalidates the exact reviewed binding.

Three fresh no-clobber tests also passed: an existing directory with a sentinel, an existing ordinary file, and a dangling symlink. Each was preserved and rejected with the documented error. The wrapper uses explicit `require` checks, so optimized Python cannot disable its correctness guards. Its output directory is created with `exist_ok=False`; the initial existence check also recognizes dangling symlinks. These tests establish the tested filesystem interface, not a claim about every conceivable concurrent filesystem modification.

All original private/public inputs were verified unchanged afterward. No public file was edited. Executed copies were checked against their bound hashes after execution. The reviewer checker verifies the raw-stream hashes and both complete log hashes again without rerunning GAP.

## Exact admitted scope

The wrapper accurately separates the written all-parameter proofs from finite computations. Phase58's written theorem concerns every `beta >= 5` and all four signs in the retained Γ2 source family: the two facet/cofacet constructions yield the same minimal double cover after reduction, with uniqueness only inside their proved shared interval. Its **complete degree-two/four census is only at beta 5, signs ++**: one double cover and 29 quartic covers, split as 16 cyclic, two central V4, and 11 noncentral V4; none of the quartic covers supplies a new minimal cover. The eight construction diagnostics are not an all-parameter enumeration.

Phase66's written parameter transport and module argument give the uniform obstruction for **finite covers with odd abelian kernel and injective maps on both end subgroups**. The fixed integer identity and eight source cross-checks support that proof; they do not remove its kernel or local-injectivity hypotheses. The wrapper does not machine-check either written parameter reduction, establish global uniqueness of minimal covers, or resolve the other source families.

No Lean source was compiled in this audit. No new historical-priority claim, current-openness clearance, manuscript-compression factor, or source-count admission follows from this wrapper. Its result is a reproducible public execution interface for the exact already reviewed mathematics, with its retained source inputs and scope limitations intact.
