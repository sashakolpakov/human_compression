# Measuring compression and new mathematics

The project has two measurable ambitions: replace existing arguments with a
smaller reusable theory, and obtain verified results beyond the known proofs.
Both belong in the assessment. They require different evidence.

## A finite compression ratio

Fix a set of exact theorem statements $S$, a common background $B$, and a
declared way of measuring proof descriptions. Define

$$R(S\mid B)=\frac{L_{\mathrm{source}}(S\mid B)}
 {L_{\mathrm{core}}(S\mid B)+L_{\mathrm{adapters}}(S\mid B)
  +L_{\mathrm{extra\ dependencies}}(S\mid B)}.$$

The numerator measures the source arguments needed for precisely $S$. The
denominator measures the shared replacement theory, its statement-specific
applications, and any additional dependencies. A dependency already in the
declared background is excluded on both sides. A retained classification
cannot silently become free just because its name fits in one sentence.
Where a dependency is not expanded, report a **conditional ratio** with that
dependency listed explicitly. Count shared arguments once on each side.

Report the theorem set and coverage beside every ratio. The number of
principal-result reductions among the indexed works is a coverage observation,
not a compression ratio; an indexed work is not necessarily read or reduced. A partial theorem
reduction cannot contribute the length of an entire paper to the numerator.
Unreduced statements stay in the remaining-work ledger.

Useful measurements include words in comparable written proofs, bytes in
specified formal proof sources, and the number of independent lemmas reused.
Each captures something different. Keep written exposition, executable
algorithms, formal proofs and numerical certificates in separate columns;
give a bundled byte count only when both bundles have the same declared
contents and output requirements. Record proof checking time and search time
separately from description length. A short exhaustive-search program may
encode a valid finite classification while taking substantial time to run.

For a fixed corpus, record both the total ratio and the marginal cost of
adding another result. This makes reuse visible without repeatedly charging
the shared core. Include an expanded-dependency or sensitivity estimate when
the ratio depends strongly on the chosen background or level of detail.
These are reproducible descriptive measurements, not claims about shortest
possible proofs or the intrinsic value of previous research.

## A separate structural description bound

The [bounded-core classification](research/case_study/phase16_central_join.md)
provides an exact asymptotic encoding result. For fixed excess k>=1, let
a_k(d) count the ordered nondegenerate involutory path markings with
actual IP, of rank d and group order 2^(2d−1+k).
It is eventually a positive degree-k polynomial. Therefore

    log2 a_k(d) = k log2 d + O_k(1).

The [leading-coefficient theorem](research/case_study/phase18_leading_coefficient.md)
now sharpens this to

    a_k(d) = (5^k/k!) d^k + O_k(d^(k−1)),
    log2 a_k(d) = k log2 d + k log2 5 − log2(k!) + O_k(1/d).

The coefficient is derived from the exact canonical-core patterns:
the terms of maximal degree have k separated excess-one components,
each with four edge choices or one triple choice. It is not estimated
by fitting finite counts. Higher nilpotency class contributes only
O_k(d^(k−1)) marked classes.

Conditional on d, k and the specified finite core library, a fixed-length
index identifying one marked class requires exactly ceil(log2 a_k(d))
bits in the worst case. A finite enumeration supplies a decoder; no
efficient enumeration or decoding time is asserted. The canonical
core and its positions also give an explicit structural encoding of
the same asymptotic order. Its library cost is a fixed k-dependent
constant, not a free contribution to an unrelated corpus measurement.

This is a theorem about descriptions of mathematical objects. It is
not a numerical ratio between the literature's proofs and ours. The
finite library multiplicities have not been computed in general.
The leading coefficient is now known. The unrestricted lower coefficients
are also known at excesses one and two, while higher-excess core libraries
remain uncomputed here; no corpus ratio follows.

The [first-excess classification](research/case_study/phase17_k1_classification.md)
now gives the exact special case a₁(d)=5d−10 for every d≥3. An optimal
fixed-length class index therefore has ceil(log₂(5d−10)) bits, conditional
on d and the declared decoder. For example, rank 100 has 490 classes and
requires nine index bits. The rank, decoder, theorem and any proof
certificate are additional information whenever the application has not
already fixed them. This object-index cost is not a source-proof ratio.
The 2018 rank-five source count is a rederivation within this theorem,
not a newly solved conjecture or an infinity-marker entry.

Within nilpotency class at most three, the
[complete transfer formula](research/case_study/phase18_class_three.md)
computes every excess coefficient exactly. Across all excesses its
rank-d count is the Fibonacci number F_(4d−5), giving a conditional
index cost ceil(log₂ F_(4d−5)). That total ranges over different
orders; it must not be substituted for a count at fixed excess.
Neither formula measures the length of a mathematical proof.

The [complete excess-two census](research/case_study/phase19_k2_classification.md)
now gives a₂(d)=(25d²−107d+122)/2 for every d≥3, including all class-four
cases. Its conditional fixed-length class index is exactly
ceil(log₂ a₂(d)) bits. At rank 100 the count is 119,711 and the index
needs 17 bits. The decoder, rank and theorem remain additional information
unless already fixed. The independent rank-three quotient census and
the nested-kernel Lean adapter verify their stated components, rather than
the whole classification. Neither this new formula nor the
[unitary rank-three construction](research/case_study/phase19_unitary_rank3.md)
has a matched source-proof length or established publication priority.
They do not change the two measured ratios or receive an infinity marker.

The [fixed-class transition theorem](research/case_study/phase20_finite_state.md)
gives another exact representation: a finite state graph classifies all
ordered markings at each fixed nilpotency class. Its weighted generating
function counts by rank and excess. At fixed excess k the local windows
have rank k+2 and order at most 2^(3k+3). This bounds the objects in the
library; it is not a proof-length ratio or an efficiency claim. It is
distinct from the earlier bound on the whole canonical support core.

The [all-odd unitary extension theorem](research/case_study/phase20_unitary_rank3.md)
has an internally reviewed proof with a separately computed q=3 base.
A current broad almost-simple classification question is recorded, but
neither complete resolution of that question nor prior openness of this
exact family has been established. The newly retrieved 2025 linear theorem
is retained published input. Both measured ratios and the unassigned
infinity marker remain unchanged.

## The infinity marker

A verified solution to a previously open problem deserves a separate,
prominent entry. We reserve the display **$\infty$ — verified new resolution**
for that qualitative achievement. It means that a previously missing proof
has been supplied; it is **not a measured description-length ratio**.

The source side has no known proof to measure in this case. Its length is
unknown, rather than zero or provably infinite. Absence of a known proof does
not establish that a finite proof did not exist. The infinity marker is an
explicit reporting convention, and must not be averaged into finite ratios
or used to claim that every result in the corpus has been compressed.

Before assigning the marker, record:

1. The exact open question, source version, hypotheses, and requested scope.
2. A dated search of later primary literature, including alternate formulations
   and author followups, supporting the assessment that it remained open.
3. The complete proof and retained mathematical inputs. Disproofs qualify when
   a verified counterexample settles the stated question.
4. The verification actually performed: written proof review, exact symbolic
   computation, exhaustive finite checks, or Lean. State precisely which
   implications and instantiations each certificate checks.
5. An explicit gap audit and the priority/review status. External peer review
   is recorded separately; internal agent agreement is not external review.

A finite-range computation does not settle an all-parameter conjecture.
A Lean lemma for a matrix identity does not by itself formalize the theorem
that connects that identity to the source geometry. A solution already in
the literature is a rederivation, even if we found the proof independently.
Closing an omitted case or obtaining a stronger bound should be reported
with its exact scope; neither automatically settles an entire conjecture.

## Current assessment

**There are two matched-proof ratios: 3.34× for two counting formulas,
and 4/3≈1.33× for eight numbered generator/geometry results from 2002.
No corpus ratio or infinity marker is assigned in this snapshot.** Several proposed resolutions have written
arguments and substantial checks, but their external priority remains
unverified and their formal certificates cover specified components.

The [complete measurement record](research/case_study/phase9_L066_measurement.md)
compares the exact formulas in L066, Theorems 1.1 and 1.2, in degrees
$N\ge4$, $N\ne6$. It excludes both degree-six exceptions and the paper's
polyhedron theorems. Shared spans are counted once. A source centralizer
proposition is recorded but excluded from the conservative primary count,
because its extra order assertion is unnecessary for the target formulas.

| Metric | Source | Replacement | Ratio |
|---|---:|---:|---:|
| Normalized non-whitespace characters | 10,668 | 3,192 | 3.3421 |
| Alphanumeric tokens, extraction-sensitive | 2,534 | 835 | 3.0347 |
| Raw selected-span UTF-8 bytes | 13,722 | 4,080 | 3.3632 |

These are description lengths of particular proofs, conditional on the
declared common background. Typeset-source extraction and plain-text proof
formatting differ, so the figures are reported with sensitivity checks.
The protocol records exact source/replacement spans and hashes; the script
recomputes all counts from the original PDF without distributing its text.
The added cost of the second theorem is reported separately, showing reuse
of the shared proof. This measurement does not assess mathematical importance.

The [second measurement](research/case_study/phase15_N003_measurement.md)
matches N003, Theorems 1.1, 2.1, 3.1 and 3.2 and Corollaries 2.2–2.4 and
3.3, with general bounds restricted to finite groups and the symmetric-group
classification to n≥7. It covers both generator families, all three counts,
the relative bounds and the complete maximum-rank geometry argument.

| Metric | Source | Replacement | Ratio |
|---|---:|---:|---:|
| Normalized non-whitespace characters | 9,680 | 7,260 | 1.333333 |
| Unicode alphanumeric tokens, extraction-sensitive | 2,439 | 1,675 | 1.456119 |
| Raw selected-span UTF-8 bytes | 12,462 | 8,693 | 1.433567 |

The replacement is 25 percent shorter in the primary measure. Whiston's
two specified inputs, including their CFSG dependence, Cayley's count and
the general coset criteria remain common background. Exact source spans,
23 physical-layout exclusions and the replacement blocks are hash-bound;
a second implementation independently recomputes every count and marginal
allocation. Reuse that gives a later corollary zero additional charge is
already-paid proof material, not a new resolution or an infinity marker.
These two measurements are reported separately, without an aggregate ratio.

The [dated status audit](research/case_study/phase6_status_audit.md) searches
later primary literature for four of the strongest proposed resolutions.
It finds a positive 2022 open-status checkpoint for the missing PSL₂ family
and no explicit later settlement of those exact targets in the bounded
search. It does not establish current priority; no infinity marker is
assigned from a negative literature search alone.

The main proposed-resolution targets to assess are:

| Source target | Current mathematical claim | Verification and scope record |
|---|---|---|
| L025, Conjecture 3.2 | Suzuki graph pentagon count for all stated parameters | [Proof](research/case_study/suzuki_cycle_proof.md); Lean checks the matrix-membership equivalence, with the graph bridge in the written proof |
| L034, Conjecture 3.3 | Complete proposed lower bound n≥s+t+l for regular rank-three hypertopes of type (2ˢ,2ᵗ,2ˡ) and order 2ⁿ in the published source range | [Cyclic-TPP theorem and geometric adapter](research/case_study/phase14_cyclic_tpp.md); independent internal reviews, retained powerful-group theory and an abstract square-descent Lean component. Current priority unverified |
| L043, Conjectures 6.1 and 6.2 | Field/intersection statements and their chiral construction consequence | [Proof chain](research/case_study/psl2_chiral_corollary.md); exact finite-field witnesses and partial formalization |
| L052, Problems 9.3 and 9.4 | Nonexistence under the specified standard parabolic coset construction | [Scope audit](research/case_study/hypertope_questions_independent_audit.md); written proofs and an abstract chamber-orbit certificate |
| L092, Conjecture 1 | Hermitian-unital residue connectivity | [Proof](research/case_study/hermitian_unital_proof.md); finite checks and abstract connectivity formalization |
| L102, §5.1.2 and Theorem 6.1(1) | Desarguesian uniqueness and existence in the specified one-dimensional semilinear case | [Proof and source audit](research/case_study/phase4_old_problem_audit.md); written all-parameter proof and exact small-instance checks |
| L114, final p.61 realization question | Decisions for every displayed parameter shape, distinguishing bare subgroup intersections from RWPRI realization | [Complete decision table](research/case_study/phase5_suzuki_higher.md#e-exact-scope-of-the-proposed-resolution); written uniform proofs, two internal reviews and exact coordinate checks |
| L120, Conjecture 2 in §5.7 | Maximum string C-group rank four for PSL₄(q), every odd q | [Complete dependency map and rank-six proof](research/case_study/phase8_psl4_rank6.md); independent internal reviews, exact symbolic checks, and partial Lean lemmas; rank-four existence retained |

The [central cyclic lift](research/case_study/central_lift_proof.md) also supplies
a proposed omitted existence range. Its source does not have the same status
as a named conjecture. The earlier partial
[hypertope order bound](research/case_study/phase3_order_bound.md) is now
superseded by the complete proposed argument above. Its named-target match
does not itself establish publication priority.

The PSL₄ proof now excludes rank six as well as rank five, completing its
mathematical argument against every rank above four. Its status is therefore
a proposed complete resolution, superseding the earlier partial-progress
entry. Current publication priority remains unverified; its Lean modules
certify specified implications, not the complete proof. No infinity marker
is assigned merely from internal agreement or a negative literature search.
The [separate PSL₄ status audit](research/case_study/phase8_psl4_status_audit.md)
records fifteen primary-source records, reading limits and forty-one
representative searches, including the orthogonal-group formulation.
It located no explicit later resolution and does not certify current priority.

The [metacyclic extension](research/case_study/phase7_cyclic_tpp.md) proves a
uniform cyclic-subgroup inequality and another full structural class of that
order conjecture. Its separate finite certificate increases the verified
hypertope range to order \(2^{12}\). These were partial results, now
subsumed by phase fourteen; neither received the new-resolution marker.

The [small-factor extension](research/case_study/phase10_cyclic_tpp.md) now
proves the same order conjecture whenever a distinguished pair has order at
most eight, without an ambient-order cutoff. It retains the classification
of marked isobicyclic 2-groups. The complete phase-fourteen proof removes
that dependency. The [PSU₄(5) matrix certificate](research/case_study/phase10_unitary_matrix_certificate.md)
settles one finite rank-four existence case, with publication priority
unverified. Neither is assigned an infinity marker.

The [Suzuki marked-field reduction](research/case_study/phase10_suzuki_marked_fields.md)
recovers both principal counting theorems of L074 and the older L085
rank/existence theorem as exactly restated there. This enlarges theorem
coverage but has no matched-length measurement yet. The first 3.34× ratio
is unchanged. The [cross-paper tree scope audit](research/case_study/phase10_measurement_scope.md)
identifies exact 1998/2002 targets and shared dependencies; missing complete
1998 source spans prevent a cross-paper numerator. No page-count proxy or
extrapolation from the existing ratio is used.

The proposed 1999 realization decisions retain classical Suzuki structure.
A subsequent [exact counterexample](research/case_study/phase6_suzuki_realization.md)
shows that the printed candidate list is not exhaustive; the former assumption
of its completeness is withdrawn. Its explicit rank-three geometry is firm,
residually connected, flag-transitive and RWPRI. This deserves a separate
prominent result entry, but a corrected exhaustive classification and
publication priority remain unresolved. No infinity marker is assigned.

The [paper registry](research/case_study/paper_registry.json) records exact
targets, retained inputs and coverage. Further quantitative reports must
extend the same source/replacement span and dependency accounting to other
matched theorem sets. The number of papers indexed, pages downloaded, agents
used, or elapsed research years cannot substitute for those measurements.

The phase-eleven [odd-order nilpotent theorem](research/case_study/phase11_odd_nilpotent.md)
has a short all-parameter proof using a retained 1987 factorization theorem.
It subsumes the odd-prime metacyclic and abelian-Frattini cases. The
[bounded priority audit](research/case_study/phase11_odd_nilpotent_status.md)
does not establish novelty or identify a named open conjecture resolved by
that theorem; it also attributes the known order-21 boundary example. The
[hereditary powerful-Frattini theorem](research/case_study/phase11_powerful_frattini.md)
unifies further 2-group classes. Neither has a matched-length measurement;
both are now subsumed by the complete proposed nilpotent theorem. The
[unitary template](research/case_study/phase11_unitary_intersection.md)
proved a conditional family and certified additional finite examples;
phase thirteen subsequently supplied parameters for every odd q≡1 mod 4.
These are substantive theorem coverage gains, with unverified publication
priority. At that stage the measured ratio stayed **127/38≈3.34**;
phase fifteen adds the separately scoped **4/3** measurement above.
No infinity marker is assigned.

Phase twelve adds a [complete 2002 principal-result reduction](research/case_study/phase12_N003_reduction.md),
raising that coverage ledger to nine works. All eight numbered targets
had exact source-span metadata; phase fifteen now supplies their fully
charged matched-length comparison above. The [class-three bound](research/case_study/phase12_class_three.md)
and [PSU₄(9^e) family](research/case_study/phase12_unitary_parameters.md)
are uniform mathematical gains, with priority unverified; the TPP bound
is now subsumed by phase fourteen. The [2026 correction](research/case_study/phase12_path_cocycle.md)
disproves specified auxiliary assertions, without refuting the paper's
separate main existence claim. None changes the existing numerical ratio
or qualifies here for a verified-new-resolution infinity marker.

Phase thirteen extends the [unitary construction](research/case_study/phase13_unitary_sieve.md)
to every odd q≡1 mod 4, with an independently checked certificate for
all 406 fields left by the uniform sieve. The [cyclic TPP extension](research/case_study/phase13_cyclic_tpp.md)
proves the smallest-factor-eight bound and all 2-groups through order 1024.
A [canonical quotient](research/case_study/phase13_common_quotient_class_three.md)
repairs the common-quotient existence argument through nilpotency class
three, uniformly in rank. At that stage the unrestricted hypertope bound
and the other unitary congruence class were still unresolved. A correction
to a proof is not by itself an open-problem resolution. These results have
no matched-length measurement.
The numerical ratio and nine-work principal-result count remained unchanged
in phase thirteen; no infinity marker was assigned.

The [unitary status audit](research/case_study/phase13_unitary_priority_audit.md)
records thirty primary-literature searches and the exact rank-three
published baseline. It located no matching earlier uniform theorem or
named unitary conjecture, and does not certify novelty. The named survey
conjecture concerns the linear group and must not be attributed to the
unitary companion result.

Phase fourteen supplies a [complete proposed cyclic-TPP theorem](research/case_study/phase14_cyclic_tpp.md)
for finite 2-groups. Combined with the odd-prime argument, it covers every
finite nilpotent group, with no order or class cutoff. The proof retains
published powerful-group structure but removes the earlier isobicyclic
classification and finite catalogues. Its geometric consequence matches
the exact assertion of Hou–Feng–Leemans Conjecture 3.3 (2019); combined
with the source's construction, it gives the parameter criterion in the
stated range. This is a complete proposed resolution, replacing the
earlier partial-progress status.

The [bounded status audit](research/case_study/phase14_cyclic_tpp_status.md)
records 24 fresh searches and exact primary-source reading limits. It
found no later resolution, but the latest explicit open checkpoint located
is the original 2019 paper. Current priority is therefore unverified.
Internal proof agreement and an abstract Lean descent certificate do not
constitute external peer review or full formalization. No infinity marker
is assigned, and no matched proof-length measurement has been made.

The [PSU₄(7) certificate](research/case_study/phase14_unitary_q7.md)
adds one exact rank-four existence case, of type {4,24,4}, with all 16
subset groups and 256 intersections checked. It does not establish a
uniform family for q≡3 mod 4; the range q≥11 in that class was still
unresolved at the end of phase fourteen. It receives no novelty marker
or length ratio. That phase left the **127/38≈3.34** measurement and
nine-work principal-result count unchanged.

Phase fifteen adds the second measured ratio above and an
[all-class forest quotient theorem](research/case_study/phase15_graded_support.md).
Its [source adapter](research/case_study/phase15_graded_support_scope.md)
recovers both principal results of F013, bringing that coverage ledger
to ten works. The earlier counterexamples to its auxiliary kernel formula
remain valid. A replacement proof of an already stated theorem does not
qualify as a new resolution; its proof length has not been measured here.

The [second unitary construction](research/case_study/phase15_unitary_sieve.md)
also completes the proposed maximum-rank-four theorem for every odd q≥5.
The written proof, independent sieve and all exceptional parameter witnesses
are reviewed separately from the earlier priority search. This is a stronger
coverage claim, with current priority unverified; it receives neither a
matched-length ratio nor an infinity marker.

Phase sixteen adds two scoped principal-result reductions: the 2005
Frattini-geometry paper and the six principal construction theorems of
the 2025 two-group paper. The ledger now contains twelve works. The
fixed-excess theorem concentrates all non-class-two data into a bounded
core and gives a sharp Θ_k(d^k) growth order for ordered marked groups.
These are substantive coverage and structural gains. No matched source
and replacement spans have yet been measured for them, so the two existing
ratios remain unchanged. Neither rederiving an existing theorem nor proving
a companion result with unverified priority receives the infinity marker.

The same phase's [linear diagonal construction](research/case_study/phase16_linear_diagonal.md)
proves uniform rank-four existence for every odd-field diagonal index-two
extension. With the retained upper bound, it completes the classification
of maxima within PSL₄(q)≤G≤PGL₄(q). This is a proper part of the broader
survey problem about all almost-simple extensions. The
[dated primary-source audit](research/case_study/phase16_linear_diagonal_status.md)
does not establish current priority, so this result receives neither an
infinity marker nor a finite proof-length ratio.

Phase twenty-one adds the [linear diagonal rank-three construction](research/case_study/phase21_linear_rank3.md), completing the exact rank set
for the index-two diagonal extension at every odd field size. Its proof
uses independent rank-one factors, a Jordan-block obstruction and root
extraction. Some existence cases are already published; the
[bounded priority audit](research/case_study/phase21_linear_rank3_status.md)
records possible further overlap and a 2026 dissertation lead. Neither
a full matched-length comparison nor verified new-resolution status is
established. The measured ratios remain **127/38** and **4/3**, and no
infinity marker is assigned.

The same phase also recovers N009 Theorems 3.6, 3.8 and 5.5 and every
rank-four Table 6 type count, through a uniform central adapter and exact
normal-kernel census. The previously recovered rank-five counts are not
counted again. The rank-three order-1,024 component and other presentation
claims remain outstanding, so the principal-result ledger stays at
**twelve works**. A terminating algorithm, a count of 105 classes, and
a short proof of the enumeration mechanism do not by themselves supply
a matched source/replacement proof-length ratio.
