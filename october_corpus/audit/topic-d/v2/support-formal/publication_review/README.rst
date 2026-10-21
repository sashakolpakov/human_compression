Independent publication review: Topic D support formalization
============================================================

Accepted as a bounded publication integration. This review checked exact frozen
copies, retained manuscript inputs, reader-facing scope, relative links, the
standard verifier and rejection controls. It did not repeat the independently
accepted full mathematical/type review or fresh Lean compilation.

The public edition contains 28 declaration reports: the unchanged first module's
12 reports and the global module's 16 reports. The earlier twelve are included
once. These are declarations, including constructions and adapters, not 28
independent mathematical results. The original Topic D ten-declaration packet
and all scientific papers remain unchanged.

The generic orbit decomposition and support formula are formally proved under
the stated action, support and finiteness hypotheses. Source-specific
admissibility, generation, field support, geometric recognition and census
completeness remain outside the supplement. The divisor-poset interpretation
and number-theoretic Mobius bridge are not claimed. The classical incidence
inverse identity and Burnside theorem retain their mathlib attribution.
Existing pinned dependency objects remain trusted; no full mathlib rebuild or
independent kernel implementation is claimed.

The author and early supplement manifests retain their historical pending
status strings. The later independent review and additive public admission
provide the accepted status without altering those frozen bytes. The current
audit reader explicitly supersedes the older frozen publication guide's
pending-supplement sentence.

One verifier hardening request was resolved before acceptance: require the
component counts to be 12 and 16, and require the divisor-bridge flag to remain
false. No author artifact or mathematical statement needed correction.

Reproduce the bounded checks with a fresh output filename::

  python -B -O check.py --public-root /path/to/human_compression \
    --study-root /path/to/private/study --out /fresh/replay.json

The checker compares 48 frozen exports across three packets, 53 admission
bindings and four retained input mappings. It confirms all 24 previous
non-main verifier functions are unchanged, checks 97 relative links and runs
14 rejection controls in memory or temporary files. It makes no public edits
and does not add source, question or compression credit.
