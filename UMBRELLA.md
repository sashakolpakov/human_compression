# Umbrella theory U: Marked groups, kernels and intersections

Read the complete [16-page manuscript](research/case_study/phase138_render_U/application.pdf)
or its [Markdown source](research/case_study/phase138_umbrella_v3.md).
Version 3 contains 30 statements with proofs. All 28 statement/proof pairs
from version 2 are preserved exactly; typed-coset Helly transfer and its
corrected geometric consequence are now integrated.

The principal construction assembles local extensions over sets of
marked generators. Injectivity on every proper local parabolic isolates
each kernel, even with overlapping or nested supports and nonabelian
kernel factors. It proves generation of the compatible group and computes
every parabolic kernel. The resulting intersection property, order,
local recognition, deletion maps and factorization statements serve
several constructions in [Module A](MODULE_A.md).

The coordinate-kernel theorem moves pairwise coset intersections into a
common base fiber, where the remaining constraints fix individual kernel
coordinates. Their compatibility gives a common point. Its geometric
consequence explicitly requires involutory local markers; an involutory
base image alone does not suffice.

Other sections treat quotient intersections, finite nilpotent quotients
and invariant subgroup ladders, marked quotient comparison, faithful
actions, orbit decompositions, relative generation, Frattini coordinates
and amalgamated free products. The latter relative-generation and Frattini
results are also used by [Module B](MODULE_B.md). B's six retained U-v2
statement/proof pairs occur unchanged in this edition.

The [exact contracts](research/case_study/phase138_umbrella_v3_contracts.json)
bind every statement and complete proof. The
[integration and attribution note](research/case_study/phase138_scope.md)
and [publication review](provenance/phase99_review.md) distinguish reused
arguments, new repository steps, retained literature and verification.
Historical priority is not inferred from this reorganization.

Three scoped Lean modules now establish the actual supported-kernel
construction, its order/local/separator/lower-central consequences, and
the complete marked typed-Helly transfer with its supported-kernel
application. Their [exact scopes and fresh reports](research/case_study/formal/README.md)
state every remaining hypothesis. Full geometric recognition, Boolean
deletions in this formal interface and source-application bindings remain
separate formalization tasks. No entire module is certified by a helper.

U's complete body costs 61,576 UTF-8 bytes and is charged once in a combined
comparison. Its 16 rendered pages do not include the four programs required
by Module A. Matched source measurement remains separate from this inventory.
The [previous draft](research/case_study/phase123_umbrella_manuscript_v2.md)
and its [original review](research/case_study/phase127_modular_root_review.md)
remain available for provenance.
