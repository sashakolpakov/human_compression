# Phase-fourteen root review

10 October 2026. Internal mathematical review and fresh execution record.
The complete proposed cyclic-TPP theorem, its nilpotent consequence and
the exact published hypertope conjecture pass this review. This is not
external peer review, a priority determination or a full Lean proof.
The companion JSON binds the exact reviewed bytes.

## Uniform cyclic TPP and the geometric consequence

Root read the complete final [proof](phase14_cyclic_tpp.md), including
all minimum-counterexample reductions, the three action lemmas and both
boundary cases for the third Frattini layer. Two separate internal agents
also read the complete proof and recorded [first](phase14_cyclic_tpp_audit.md)
and [second](phase14_cyclic_tpp_independent_audit.md) reviews. No gap was
found. The historical pending-review footer in the original draft is
preserved; these hash-bound records give its subsequent review status.

The critical checks are the following.

- TPP is used as a unique identity factorization, never as an unexplained
  bijectivity assertion for the whole ordered multiplication map.
- Central quotients preserve the violating ratio after absorption into
  a cyclic factor. Proper pair-generated subgroups give the required
  coset-index bound without assuming normality. A maximal-subgroup
  reduction makes the minimum violating ratio exactly two.
- The weak-embedding induction uses only characteristic power subgroups,
  a central normal subgroup of order two, and the class-two exponent-four
  calculation. It does not assume arbitrary subgroups of powerful groups
  are powerful.
- Powerful ordered factorization is applied to the given marked generating
  list. Bijectivity follows only after the separate equality of orders.
  The top-layer argument uses actual normal elementary abelian subgroups,
  not merely a vector space with an unproved action.
- The first two Frattini layers each have generator rank three. If the
  second layer had smaller rank, weak embedding and the marked top-layer
  argument would contradict center avoidance. This removes the earlier
  isobicyclic classification dependency.
- The third layer is powerful because a binary linear group in dimension
  at most three has 2-subgroups of exponent dividing four. Its trivial
  case is excluded by an equivariant square map; no order-256 census is
  used.
- In the nontrivial case, the two maps
  `S/N -> N/N²` and `K/S -> S/N` are well defined for the explicitly
  proved commutator containments. Equivariance and preservation of the
  marked coordinates suffice. Neither map is assumed to be linear.
  Transport of a fixed marked coordinate gives the contradiction.

The retained structural input is Lubotzky--Mann's powerful-group power
and ordered-factorization theory, with elementary finite-p-group facts.
The [focused primary-source recheck](phase14_powerful_source_recheck.md)
records the exact published statements. No finite catalogue, marked
isobicyclic classification, special order-32 presentation, exact action
matrices, quadratic-map search or exploratory extension probe is an input
to the new written proof.

Root also reread the [odd-prime argument](phase11_odd_nilpotent.md) and
the [geometric adapter](phase3_order_bound.md), sections 1--3. Sylow
decomposition gives the bound for all finite nilpotent groups. For a
regular rank-three hypertope, flag transitivity supplies the typed coset
Helly identity; subgroup intersection alone is insufficient. The three
square-rotation cyclic groups lie in the derived subgroup of index eight.
Their size inequality is exactly `n >= s+t+l`, proving the lower bound
in the published 2019 Conjecture 3.3 under its stated hypotheses.

The [dated literature audit](phase14_cyclic_tpp_status.md) records 24 fresh
queries and the precise later-source reading scope. It found no later
resolution, but its latest explicit open checkpoint remains the 2019
source itself. Current priority is unverified. The theorem is not asserted
for nonnilpotent groups or for arbitrary noncyclic subgroup triples.

## Fresh partial Lean verification

Root wrote [MarkedSquareDescent.lean](formal/MarkedSquareDescent.lean) and
compiled it privately. After byte-identical export, the public runner
freshly compiled both its dependency `BinaryFrattiniActions` and the new
module, in dependency order, using Lean 4.32.2 and the pinned mathlib
revision. The runner checked dependency Git revisions and tracked-file
cleanliness. Both exits were zero; the printed axioms contain no
`sorryAx`. Compiled dependency caches remain trusted build inputs.

The new module verifies the commuting marked-action classification by
kernel-checked finite decisions and proves the abstract equivariant
transport obstruction. The transport lemma itself has no axioms. The
[scope note](formal/MarkedSquareDescent.scope.md) lists the unformalized
steps, including minimum-counterexample reductions, powerful groups,
quotient-square-map construction and the geometric application. The
uniform theorem remains a written proof with formally checked components.
All seventeen earlier saved Lean reports are unchanged.

## Exact PSU4(7) construction

Root read the complete [matrix proof](phase14_unitary_q7.md) and checker,
checked the field coordinates and natural matrix identities, then freshly
ran the original GAP checker in a disposable directory. The report agrees
with the author's on every field except elapsed time: 507 ms versus
553 ms in those recorded runs. This is an independent execution of the
same checker, not a second field-arithmetic implementation.

The action on all 2,752 isotropic planes has order 1,165,572,172,800,
the full projective special-unitary order. All 256 distinguished subgroup
intersections pass and the type is `{4,24,4}`. The group identification
uses containment and an order sandwich, not an unverified recognition
routine. The retained rank upper bound makes the maximum rank four at
q=7. Uniform existence for q congruent to three modulo four, q at least
eleven, remains outside this finite certificate.

## Measurement and export scope

The existing matched-proof ratio, 127/38 approximately 3.34 for the
specified two counting formulas, is unchanged. The nine-work principal
result count is also unchanged. A proposed proof of a conjecture does not
rederive every published theorem of its source paper. No corpus ratio or
verified-new-resolution infinity marker is assigned while priority remains
unverified. The new result is nevertheless recorded prominently with its
complete scope and evidence.

Original proof, review, certificate and fresh-run artifacts are exported
byte for byte. Source publications, exploratory probes and compiled Lean
objects are excluded. Historical artifacts retain their original bytes;
the living introduction, registry and landing documents record the new
uniform theorem and supersede the earlier bounded current-status claims.
