Orbit intersections and diagonal twistings
=========================================

This author candidate recovers the complete principal contract of N007,
Piedade and Tranchida's twelve-page arXiv:2608.23223v1. It contains a complete
common paper and application, both five pages, and a separate whole-program
appendix. The 32-row source map includes background, both constructions,
quotient variants, exact diagram labels, the finite tree family, both classical
comparisons, the displayed example, and the general existence question with its open status.
Distinct independent mathematical and source review is still required.

The common theorem proves the full finite-rank regular twisting argument:
all flag stabilizers, flag-transitivity, thinness, residual connectivity,
faithfulness and full type-preserving automorphism group. It includes the
orbital-presentation converse used in the earlier Matching paper; no old project
manuscript is an unpaid premise. The result is attributed to the existing
Piedade–Tranchida theory, with a common proof and explicit applications here.
N006 Corollary 3.17 is not an unproved dependency for this application, but
the rest of N006 remains a separate pending principal contract.

Retained classical inputs are declared in contract.json: Coxeter standard
parabolics and their geometry, the string C-group/polytope correspondence,
and the named classical extension descriptions used in N007's Corollaries
3.7 and 3.14. The original McMullen–Schulte book has not been newly read.
Unknown full retained-proof costs are not zero and no ratio is computed.

The displayed complement-subscript error is repaired. Exact doubled labels
are proved, including infinite order. The tree induction preserves the actual
specified tree. Example 3.11's diagrams have four vertices in the first input,
although its prose lists three; the actual two six-vertex output diagrams are
reproduced by complete edge lists. These are explicit source repairs, not a
new open-conjecture claim. The general finite-diagram question stays open.

One complete GAP program is validation, not a uniform finite premise. It builds
the actual semidirect models of orders 48 and 1152 and checks all 320 subset
intersections and all 4,608 coset flag-transitivity triples. Eight new Lean
declarations verify the stated group-coset, type-support and exact-order algebra.
The Helly geometry premise, Coxeter facts and the complete geometric theorem
remain written proofs; no end-to-end formalization is claimed.

Replay in a fresh directory::

  python3 -B -O check.py --out /fresh/path --gap /path/gap \
    --lean /path/lean4.32.2 --packages /path/pinned/.lake/packages \
    --render --xelatex /path/xelatex

Optionally supply --study-root /private/study to verify both primary PDF pins.
No private source text, images, Markdown, compiled Lean objects or cache files
are exported. The code appendix includes the complete raw program literally.
Lean and GAP versions and dependency sources are pinned; precompiled Mathlib
objects and GAP's exact algorithms are explicit computational trust inputs.
Two finite-output mutations and three false Lean conclusions must be rejected.

Suggested independent review priorities are the Cartesian-coordinate proof
of flag-transitivity, each residual-generation case, the chamber-kernel step
in the invariant-quotient lemma, exact doubled orders and the classical named
construction boundary. All statements are finite rank; no infinite-rank
twisting theorem is inferred. No source, question or formal credit is awarded
by the author packet itself.

Additive second edition
-----------------------

The first edition is preserved under its original manifest. This edition repairs
our quotient proof: the source uses intersections of quotient maximal parabolics,
which contain the chamber kernel, rather than arbitrary generated-support images.
The faithful reduction now justifies every quotient parabolic. A separate short
reduction handles flag-transitive unfaithful models of beta. This is not a new
source error or a weakening of its quotient-hypertope hypothesis. See delta.json
and mathematical_delta.diff for the exact changes. Formal and program bytes are
unchanged; no additional formal coverage is claimed for the quotient proof.
