# Scope and source adapter for the graded-support proof

10 October 2026. The frozen author proof is
[phase15_graded_support.md](phase15_graded_support.md), SHA256
`831faf9b27d0f0b1596e278ae0ac5cc87baa8a3d7f1975bdb9e4c24ff923c9c3`.
Its historical pending-review footer is preserved; completed review
records are bound separately by the certificate.

The exact source target is Hou–Schulte, *String C-groups of 2-power order
project onto a common string C-group*,
[arXiv:2605.20691v1](https://arxiv.org/abs/2605.20691v1), dated May 2026.
The primary full text's pages 1–4 were read for this adapter. Theorem 1.1
asserts the marked common quotient for every finite nondegenerate string
C-group of two-power order and rank at least two. The definition of
nondegenerate on page 2 excludes type entries equal to two. Section 3,
page 4, defines the target by adjacent products of order four, distant
commutation, and central squares of adjacent products. These are exactly
the class-two path presentation identified in the replacement proof.

The replacement therefore rederives the source's complete group-theoretic
principal statement. Its canonical kernel is γ₃(G). The source's
Theorem 1.2 is the equivalent polytope-covering statement, using the
standard marked C-group/regular-polytope correspondence recalled in its
Section 2. That correspondence is retained background, not reconstructed
in this note. The forest extension in the replacement has a wider
commutation-diagram hypothesis than the path statement; priority for
that extension has not been established.

This is a new proposed proof of an already stated theorem. It should not
be described as resolving a conjecture that the cited paper leaves open.
The independently checked counterexamples to the paper's specified
Frattini-intersection kernel remain valid; the present argument neither
uses that kernel formula nor repairs it. No claim of external peer
review or of formalizing the full proof in Lean is made.

The all-class argument uses the graded-support and finite counting
lemmas proved within its own note. The earlier
[class-four proof](phase15_common_quotient_class_four.md) and
[last-central quotient-IP counterexample](phase15_quotient_ip.md) are
historical and diagnostic supplements, not dependencies of the uniform
theorem. The uniform theorem has no finite-census, software-computation
or classification-by-nilpotency-class input.
