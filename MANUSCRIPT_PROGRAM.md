# Umbrella theory and application manuscripts

The intended mathematical product is

    U + A -> principal results of source bundle S_A
    U + B -> principal results of source bundle S_B
    U + C -> principal results of source bundle S_C.

U contains complete reusable theorems and their proofs. Each application
manuscript is a coherent mathematical paper, normally about 20–25 pages,
which proves all application hypotheses and all source-specific arguments.
The papers do not repeat U's proofs. Source coverage is earned by actual
deductions, not thematic similarity or a shared encoding.

## Umbrella theory U: Marked groups, kernels and intersections

The [complete draft](UMBRELLA.md) has 30 statements with proofs and an
exact attribution, dependency and formal-coverage ledger.

The draft develops exact image/kernel transport, marked parabolic
comparison, compatible extensions with kernels supported on selected
sets of generators, finite actions and relative generation. Existing
proofs and Lean components are reused where their precise hypotheses
match. The support-induction argument and its typed-Helly extension have
independent mathematical reviews and scoped Lean certificates.
Attribution distinguishes re-proved classical results, retained background
and repository arguments. Neither a new universal theory nor historical
priority is presumed from common notation.

## Module A: Construction and classification of two-group polytopes and hypertopes

The [complete application draft](MODULE_A.md) is available as a 24-page
PDF with the full source-contract ledger and required computational inputs.

The coherent source bundle is:

| ID | Source | Declared principal contract |
|---|---|---|
| N009 | Gomi–Loyola–De Las Peñas, *String C-groups of order 1024* (2018) | Complete declared marked classifications, central descent/lifts, exact presentations and universal orders, with source corrections explicit |
| L035 | Hou–Feng–Leemans, *Existence of regular 3-polytopes of order 2^n* (2019 author version) | Existence and eight-presentation classification with converses |
| L032 | Hou–Feng–Leemans, *On regular polytopes of 2-power order* (2020; revised 2019 author version) | Prescribed type and exact-order existence |
| F016 | Cunningham–Feng–Hou–Schulte, *Symmetric polytopes whose automorphism groups are 2-groups* (2025 preprint) | Declared regular, alternating and free-extension clauses, orders and presentations |
| F013 | Hou–Schulte, *String C-groups of 2-power order project onto a common string C-group* (2026 preprint) | Principal common-quotient and covering results |
| L034 | Hou–Feng–Leemans, *Existence of regular 3-hypertopes with 2^n chambers* (2019 author version) | Exact presentation, order, type, regular geometry, cyclic kernels and corrected quotient structure |

These six form the reviewed second edition. They do not constitute a
twelve-paper module. Earlier proofs and certificates have been reworked
into complete construction, classification and geometric arguments. The
hypertope proof now uses the existing edge-inflation theorem and the new
shared coset-intersection theorem. The corrected diagonal factors are
integrated directly. Full Lean formalization and matched measurement
remain incomplete; enlarging the bundle requires further source deductions.

## Module B: Forest coordinates and primitive coset geometries

The [complete 16-page manuscript](MODULE_B.md) connects forest cuts and
compatible partitions with independent generation and Frattini coordinates.
Its reviewed intake is N001 (1998), N003 (2002), N008 (2005) and L030 (2021).
The declared main results follow from U+B with the documented source
corrections and retained inputs. The ledger binds 30 source rows to 22 proof
nodes. Matched length measurement and full Lean formalization remain pending.

Later modules will group related papers around the actual reusable
machinery they need. Their intake will be frozen before a compression
claim. The earlier mixed compilation does not dictate these groupings.
Each module has a descriptive mathematical title; its letter is only an
identifier. Titles for C and later modules will follow their mathematical
scope rather than anticipate an unproved grouping.

## Open questions and formal proofs

A separate paper-by-paper question ledger is in preparation for all 161
indexed works. It distinguishes access gaps, exact historical statements,
later resolutions, repository proofs, partial cases and current-status
uncertainty. Related questions will be attacked together, and a new
consequence may enter an application manuscript with precise attribution.
The existing [question-results catalogue](CONJECTURE_RESULTS.md) collects
recorded answers separately from the compression modules.

The first separately named question-solving track is
**[Equal-label polytopes and quadratic symmetries](EQUAL_LABEL_POLYTOPES.md)**.
Its reviewed cases use path blocks, quadratic identities and parity
fibers. They do not constitute a completed compression module or a
solution of the general all-label conjecture.

Lean statements must correspond to the theorems actually proved in U and
the modules. Existing certificates are mapped to those statements; missing
formal arguments are completed separately. Written proof, finite checking,
complete formalization and historical-priority review are separate statuses.

## Length and complexity

For a module, report the original source sum divided by the complete
module length, explicitly conditional on U. For several modules, divide
the length of the union of source manuscripts by U plus the complete
modules, charging U once. Use the same representation and declared
background; expose overlap, required addenda and certificate costs.
Source pages are not assumed to have a particular length.

The GKM-style record follows the actual evolution of U and its applications:
which theorem was acquired, which old derivations were replaced, what each
new application costs, and whether all existing contracts still follow.
Shared proof bodies, application hypotheses and exceptional arguments all
count. Measurements may show acquisition spikes, cheaper later applications
and reductions after refactoring. We will test for that pattern rather
than manufacture it by changing the intake or moving text into supplements.
