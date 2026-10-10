# Compress_B: source, target and dependency ledger

10 October 2026. Author ledger for the new private manuscript
`phase37_compress_twogroups_manuscript.md`. It does not supersede any frozen
assessment, phase artifact or public registry entry. **Status: integrated
author draft; fresh finite checks passed; assembled independent review
in progress.** No four-paper certification or scalar compression
factor is assigned.

The exact intake contains four named manuscripts, eleven numbered main
theorems, and seventeen clause-level ledger rows below. Counts of rows are
not counts of papers or factors in a compression ratio. N009 is excluded.

## Source bindings and actual reading

| ID and selected manuscript | Primary version | Local retained full text | Main-result pages |
|---|---|---|---|
| L032, Hou–Feng–Leemans, *On regular polytopes of 2-power order* (2020) | [Author revised PDF](https://dipot.ulb.ac.be/dspace/bitstream/2013/292444/3/HRRPR-revised.pdf), header 8 November 2019, journal DOI 10.1007/s00454-019-00119-5 | `sources/catalogue_L032.pdf`, `.txt` | Theorem 1.2, PDF p. 2 |
| L035, Hou–Feng–Leemans, *2-groups behaving as automorphism groups of regular 3-polytopes* (2019); selected preprint title *Existence of regular 3-polytopes of order 2^n* | [arXiv:1802.08947v2](https://arxiv.org/abs/1802.08947v2), 22 January 2019 | `sources/catalogue_L035.pdf`, `.txt` | Theorems 1.2–1.3 and all eight presentations, PDF p. 2 |
| F013, Hou–Schulte, *String C-groups of 2-power order project onto a common string C-group* | [arXiv:2605.20691v1](https://arxiv.org/abs/2605.20691v1), arXiv 20 May 2026; bound PDF header 21 May | `sources/catalogue_F013.pdf`, `.txt` | Theorems 1.1–1.2 p. 2; canonical model pp. 3–4; corrected auxiliary claims pp. 5–8 |
| F016, Cunningham–Feng–Hou–Schulte, *Symmetric polytopes whose automorphism groups are 2-groups* | [arXiv:2512.15511v1](https://arxiv.org/abs/2512.15511v1), arXiv 17 December 2025; bound PDF header 18 December | `sources/symmetric_2groups2025.pdf`, `.txt` | 5.1 p. 8; 5.3 p. 11; 6.1 p. 14; 7.1 p. 15; 7.2 p. 16; 7.3 p. 17 |

This author freshly read the selected source statements, L035 definitions
and retained group-theory inputs, the F013 introduction/canonical-model
passages, and F016's FAP definitions, square-map classification, all six
main statements and surrounding proofs/extension identifications. This is
selected-section primary-text reading, not a claim to have reread every
page of all four papers. The exact F013 auxiliary comparison additionally
uses the previously inspected version-bound definitions and counterexample
calculation, whose mathematics is reprinted and proved in manuscript §10.
The local PDFs and extractions are hash-bound in the machine ledger. No
unexamined later arXiv or journal revision is silently substituted.

The earlier internal mathematical reviews of the individual ingredients
are useful provenance, not independent reviews of this new assembled text.
All necessary mathematical arguments are now in the manuscript, including
the finite census algorithm. It contains no proof obligation discharged
solely by a link to an earlier phase.

## Clause-level main-result contract

Every row currently has status **author proof supplied; assembled review
pending**, subject to the retained inputs listed below. “Supplied” is not
an independent mathematical approval.

| Target | Exact contracted conclusion and boundary | Internal derivation | Source-specific work still charged |
|---|---|---|---|
| L032 1.2 | All d≥3, n≥5, k_i≥2, sum k_i≤n−1: exact order 2^n and prescribed type | §§2–4, Cor. 4.1 | Explicit lattice seed, retractions, cyclic edge kernels and order arithmetic |
| L035 1.2 | All n≥10, s,t≥2, s+t≤n−1: exact rank-three existence | Cor. 4.1 | Same seed and edge inflation, charged once; optional proof-presentation identification also in §4 |
| L035 1.3(1) | All n≥10: exactly marked G1,G2 for type {4,2^(n−3)}; bare presentations have stated order/IP | §§6–7 | Cyclic-core bound, binary twist, model construction and presentation upper bound |
| L035 1.3(2) | All n≥10: exactly marked G3,G4 for type {4,2^(n−4)}; presentation recognition | §§3,6–7 | Unique order-64 square quotient, binary extension, centrality/order argument for bare presentations |
| L035 1.3(3) | All n≥10: exactly marked G5–G8 for type {4,2^(n−5)}; all four parameter pairs and presentation recognition | §§3,6–7, App. A | Order-256 catalogue and exhaustive relation census; exclusion of two seed patterns; order-128 square quotient; four binary models; order bound |
| F013 1.1 | Every finite nondegenerate rank d≥2 two-group string C-group maps by its marking onto G(C_d) | §5 | Graded support, descending factorization and actual-IP argument; explicit canonical quotient identification |
| F013 1.2 | Equivalent regular-polytope covering statement with same finite/nondegenerate/rank scope | Cor. 5.4 | Retained marked quotient/cover correspondence |
| F016 5.1(a) | Every d≥3, n_j≥5: exactly prescribed consecutive square-map sections | §§2–3,8 | All-rank compatible products and square-map recognition |
| F016 5.1(b) | Exact order 2^(sum n_j−3(d−3)) | Eq. (8.1) | Separator orders; no unproved intersection-size multiplication |
| F016 5.1(c) | For d≥4, (d−4,d−1)-flat, hence flat | §8 | Last product factorization and face-stabilizer incidence argument |
| F016 5.1(d) | FAP for co-(d−4)-faces, co-(d−3)-faces and facets | Lemma 2.2 and §8 | Genuine endomorphisms and normal-closure kernels; rank-three trivial cut stated |
| F016 5.3 | The constructed group equals the prescribed universal-type quotient by every displayed four-marker relator | §8, Lemma 8.1 | Boolean maps prove IP of the bare universal local presentation; local gamma3 orders, four-marker centralization, normality and upper/lower order comparison identify its finite quotient |
| F016 6.1(a) | Every d≥4 and allowed parameters: alternating semiregular object with both exact facet types, including square separator for d=4 | §9 | Two-branch compatible product; retained geometric tail-triangle assembly |
| F016 6.1(b) | Exact contracted group order, doubled exactly on equality of final parameters | §9 | Kernel order calculation, facet nonisomorphism by order, retained full-automorphism criterion |
| F016 7.1 | For input rank d≥3, free regular extension has finitely generated infinite group with only two-primary finite torsion, for finite or infinite input two-group | §9, Lemma 9.1 | Retained geometric regular extension and amalgam identification; properness, normal forms, finite generation and torsion proof |
| F016 7.2 | For input rank d≥3, same for oriented chiral input with directly regular facets; free extension remains oriented chiral | §9, Lemma 9.1 | Retained chiral free-extension theorem; only facet rotations embed; index-two torsion transfer proved |
| F016 7.3 | For input rank d≥3, same for universal alternating semiregular extension of two regular inputs sharing a facet, finite or infinite | §9, Lemma 9.1 | Retained universal alternating geometry and full group; optional branch-swap extension |

The printed L035 theorem uses G≅G_i in a marked string-C-group setting.
The contract explicitly preserves the ordered distinguished generators;
it does not interpret arbitrary abstract group isomorphism as fixing an
unrelated marking. The manuscript proves the marked statement and gives
word invariants distinguishing its models.

## Retained inputs, their precise scope and cost

| Input | Exact work imported | Where used | Boundary |
|---|---|---|---|
| Regular-polytope/C-group correspondence | Marked string C-groups define regular polytopes; marked quotients define coverings; faces are appropriate parabolic cosets | §§4–5,8 | Standard geometry is not reproved; Boolean IP and all group constructions are proved |
| Burnside basis theorem and Φ(G)=G' for involution-generated finite two-groups | Irredundancy fixes elementary abelianization and generation from the Frattini quotient | §§3,5–7,10, App. A | No source classification conclusion imported |
| Finite nilpotency and lower-central graded Lie ring | Termination, degree-one generation, bilinear bracket and Jacobi | §5 | The support and descending lift arguments are proved in full |
| Gaussian integer Euclidean algorithm; elementary Euclidean fixed-point/fundamental-domain facts | Two-power-index invariant lattice classification and torsion-kernel argument | §3 | The affine group presentation and all seed calculations are proved |
| Lucchini cyclic-core theorem | For proper cyclic M≤H with core K, |M:K|<|H:M| | §6 | Substantial structural group theory; not presented as elementary linear algebra |
| Complete SmallGroups catalogue at order 256 | A complete set of isomorphism classes of finite groups of this order | §7, App. A | Catalogue completeness is retained. The filtering, marking enumeration, relation tests and lifting proof are charged and independently executable |
| Monson–Schulte 2020, assembly theorem 5.3 in the FAP setting | From two regular facet groups splitting over the common facet, produces alternating semiregular geometry and determines its full group, including swap extension | §9 finite construction | This geometric result is substantial retained background; no claim to derive it from the fiber-product order alone |
| Standard regular free extension | Regular rank increase, universality and Γ(K)*_(Γ(F))(Γ(F)×C2) | §9 | All new two-primary torsion consequences proved |
| Schulte–Weiss 1995 free chiral extension | For oriented chiral K with directly regular F, oriented chiral rank increase/universality and Γ(K)*_(Γ+(F))Γ(F) | §9 | Full Γ(F) embedding in Γ(K) is not assumed |
| Monson–Schulte 2012/2021 universal alternating extension | Universal alternating geometry and factor amalgam, with C2 extension when facets match | §9 | Properness and infinite/torsion conclusions are proved here |
| Amalgam normal-form theorem | Reduced and cyclically reduced normal forms for A*_C B | Lemma 9.1 | The torsion, infinitude and finite-generation corollaries are proved |

The earlier assembly/free-extension sources have not all been freshly
retrieved and reread in this author pass. Their retained forms are stated
explicitly in the manuscript and match the forms recorded in the bound
F016 source and previous independent source audit. Their original-source
attribution should receive particular attention in the independent
assembled review. The universal-local group is now proved to have Boolean
deletions and IP in §8, which constructs its universal regular polytope
using only the ordinary marked C-group correspondence. This boundary
is not hidden under “standard background.”

## Corrections and explicit noncoverage

* **F013 v1 4.2(c), (d), (e):** the source-defined intersection of rotation
  Frattini subgroups is not generally gamma3 and does not have the stated
  order/quotient. Manuscript §10 proves a family of counterexamples at
  every rank d≥4. These assertions are corrections, never recovered
  corollaries. The counterexample leaves the quotient's IP intact and
  does not refute the main common-quotient statements.
* **F016 page 11:** the two perpendicular squared translation cyclic
  subgroups need not intersect trivially in a diagonal torus quotient;
  n=6 already identifies them. Equation (3.2) supplies the exact lattice
  index instead. The resulting main presentation theorem is recovered.
* **F016 chiral extension proof:** only the facet rotation group is known
  to embed. A finite index-two extension supplies the torsion property
  for the full facet group, repairing the proof without strengthening its
  hypotheses.
* L035's unnumbered exceptional n<10 lists, arbitrary types and arbitrary
  groups of order 2^n are excluded; L032's particular higher-rank
  presentation is not itself a main target of the existence theorem.
* F016's previously known power-polytope constructions, examples and
  informal remarks, the other papers' open questions/historical discussion,
  and absolute flag minima among all regular polytopes are outside the
  main-result contract. The manuscript records the immediate conditional
  semidirect-product order calculations for the power constructions.
* N009 *String C-groups of order 1024* and its named presentations/census
  remain outside this intake. No part of their manuscript length may be
  added to a numerator on this evidence.

## Verification, dependency accounting and remaining work

The manuscript's App. A is a complete mathematical specification of the
finite relation-pattern calculation. The executable
`phase37_compress_twogroups_census.g` freshly replays the earlier exact
census, with all output redirected to its new phase37 log. The eight
binary extension models are also freshly replayed at n=10, with output
`phase37_compress_twogroups_models.json`. They check constructions, not
the all-parameter classification proof. These new files do not modify
the older code, reports or frozen proof artifacts.

The machine ledger binds sources, manuscript, executable and outputs.
The new census completed in GAP 4.15.1 with SmallGroups 1.5.4: 1,651
eligible groups, 1,641 with an admissible candidate rotation, 92 anchored
valid triples, and pattern counts [64,4,16,8], in 63.734 CPU seconds.
The eight n=10 binary models also passed fresh exact checks. No
end-to-end formalization of this manuscript
exists. Previously reviewed Lean components establish selected
conditional kernel, Boolean-deletion and four-marker identities, not
this assembled theorem contract; they are not used to excuse a missing
written proof here.

All text in manuscript §§1–10 and App. A belongs in a future replacement
denominator. Any necessary executable/certificate or additional proof
appendix must also be charged under the eventual agreed convention;
diagnostic code and retained-background cost must be reported separately.
The source numerator is not admitted until the main-result coverage and
assembled proof review are closed. Raw whitespace length of the new text
is only an author-side sizing check, not a compression factor.

Remaining work is independent assembled mathematical/source review;
independent reproduction or review of the new bound finite evidence;
resolution of any resulting corrections in a new reviewable version;
and only afterwards a common-rendering manuscript-length experiment.
This draft supplies proofs for every declared target, but does not
declare those review obligations completed.
