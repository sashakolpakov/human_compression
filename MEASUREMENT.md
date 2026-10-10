# Measuring compression and new mathematics

The project has two measurable ambitions: replace existing arguments with a
smaller reusable theory, and obtain verified results beyond the known proofs.
Both belong in the assessment. They require different evidence.

## The manuscript-level experiment

The requested test is a named intake-to-manuscript reduction:

$$X_1,X_2,\ldots,X_n\longrightarrow C=\operatorname{Compress}(X_1,\ldots,X_n).$$

Each intake manuscript contributes a declared list of its main results.
The replacement manuscript must state a common theory and derive every
listed result through explicit corollaries, with the remaining source-specific
work visible. Reproducing every auxiliary lemma is not required by this test.
A shared vocabulary or a collection of separate long proofs does not yet
establish the intended common-theory reduction.

For a frozen eligible intake and an assembled replacement, report

$$R_{\rm manuscript}=
\frac{\sum_i L(X_i)}{L(C)+L(\text{required adapters outside }C)
+L(\text{additional dependency exposition outside }C)}.$$

The primary manuscript measure should be normalized main-body words, with
the same exclusions for references and acknowledgments on both sides.
Required proof appendices are included. Report page and character measures
as sensitivity checks; retain the exact source versions and counted spans.
Shared replacement material is charged once. A background theorem retained
without proof must be listed explicitly, with the ratio marked conditional
on that background. Executable/formal certificates and checking costs get
their own columns rather than being silently treated as zero-cost prose.

This measure answers how compactly the manuscripts' main results can be
presented together. The proof-span ratios below answer a narrower question
and cannot be substituted for it. An eligible intake paper can contribute
its manuscript length once its entire declared main-result list is recovered;
partial component reductions remain outside that numerator. Corrected
versions and refuted assertions must be labeled separately from literal
corollaries of the replacement.

The repository now has a [reviewed three-paper replacement](COMPRESS_A.md)
with 23 explicit adapters under its declared corrected contract. It has no
three-paper measurement yet. The earlier frozen two-paper version has twelve
reviewed adapters and a separate measurement experiment. Its [first full-body measurement](research/case_study/phase36_compress_forest_measurement.md)
reports source/replacement ratios of 1.362642 by whitespace tokens, 1.168299
by alphanumeric units and 0.941720 by nonwhitespace characters. These are
descriptive sensitivities to mathematical text representation, not one
approved factor. Exact source spans and all necessary manuscript material
are bound. A later [rendered-replacement replay](research/case_study/phase37_rendered_measurement.md)
gives descriptive ratios 1.210121, 1.243398 and 1.059536 in those respective
units, with independently reproduced AST/extraction hashes and counts. The
1998 source still lacks a faithful PDF transcription, so the remaining
representation asymmetry prevents approval of a final factor.
The finite-group qualifications,
excluded unnumbered material and source-rendering limitations accompany the
contract; they cannot be removed by a word-count calculation. The earlier
[independent assessment](INDEPENDENT_ASSESSMENT.md) supplies the wider intake
map and the remaining assembly work for other bundles.

The [second assembled replacement](COMPRESS_B.md) now has a complete
internal review of its four-paper main-result contract and an independent
finite census replay. Its [reviewed whole-body measurement](research/case_study/phase38_compress_B_measurement_root_audit.md)
gives **32,476/8,267 = 3.928390×** under a frozen NFC PDF-extracted token
convention, including the entire proof appendix and census code. The
nonwhitespace-character sensitivity is **122,382/36,570 = 3.346514×**.
The factor is conditional on the named retained background; certificate
and executable bytes are recorded separately. A fresh root rendering and
extraction replay matches all counts and exact source boundaries. The
[named map](MANUSCRIPT_MAP.md) now records those two predecessors and the
subsequent reviewed seven-source integration. The later ten-source assembly
is listed separately, with overlapping intakes counted only once.

The [seven-source measurement audit](research/case_study/phase43_unified_lower_bound_root_audit.md)
admits a **conservative lower bound of 40,358/18,241 = 2.212488×** under the
same NFC PDF-token convention. Six faithful source main bodies contribute
the numerator; N001 is credited zero because its faithful measurement is
unavailable. The denominator is the full integrated replacement, including
all 34 adapters and the complete proof/census appendix. Nonwhitespace characters
give **153,896/82,539 = 1.864525×**. Both bounds remain conditional on retained
background; the exact seven-source factor is unknown. This does not overturn
the separate finding that integration adds 706 raw Markdown tokens over A+B.
Source main bodies include introductions and open-question discussion outside
the target contract, so this is not a minimum theorem-proof-length ratio.

The further [two-source replacement](COMPRESS_C.md) is admitted only as the
complete C manuscript **plus its required lattice addendum**. Its whole
denominator must include both embedded GAP programs and that entire addendum;
the executable copies are charged once, and runtime/output costs are reported
separately. The declared main-result contract passes independent review,
and the [complete independent measurement audit](research/case_study/phase60_compress_C_measurement_recent_audit_report.md)
now admits **8,382 / 8,582 = 0.976695409×**: the replacement is **200 tokens,
or 2.386%, longer** than the source sum. The nonwhitespace-character factor
is **0.666262×**; all ten reported sensitivity factors are below one. This
experiment demonstrates no length reduction. All 16 replacement and 21 source
pages were independently inspected, including L088's late mathematical diagrams.
The [measured authored PDF](research/case_study/phase51_compress_C_measurement_replacement.pdf)
is distributed; the primary PDFs remain separately acquired inputs.

The [continuous ten-source replacement](COMPRESS_10.md) now passes complete
independent integration review with its exact required reference erratum.
Its denominator must include all 24 sections, every source adapter, the
complete internal lattice bridge, all four embedded programs and that
correction. No ten-source numerical factor is admitted yet. The separate
[annotation reader](ATTRIBUTION.md) adds attribution and verification metadata;
its bytes are reported separately and no ratio for the annotated edition is
implied by a future measurement of the proof manuscript. Annotation text
that adds a necessary argument must enter the proof denominator. None of the
current annotations adds a mathematical premise or proof step.

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
are also known at excesses one, two and three, while higher-excess core
libraries remain uncomputed here; no corpus ratio follows.

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

The principal-result ledger now covers 16 works, including the complete
nondegenerate order-1024 classification and its constructive mechanisms,
the six principal construction theorems from 2005, and the 2001 Petrial
obstruction with its valid conditional structural conclusions.
That increase measures verified coverage. Its 27-item statement ledger,
retained background and literal-source repairs do not supply a new
proof-length ratio; those costs must be measured before another ratio is
reported. The new native Lean arithmetic module is also a verification
component, not evidence of publication priority. The two older-paper additions
retain their explicit completeness and literal-source qualifications. Their
shared ideas and certificates increase coverage; neither has a matched
source/replacement proof-length measurement yet.

The [general endpoint criterion](research/case_study/phase26_halving_core.md)
replaces a full marked-intersection argument by one parabolic-overlap test
and a least-support condition. Its precise S6 counterexample proves that
the extra condition matters. This is a reusable theorem, with bounded
computational diagnostics; it adds no paper count or measured ratio by
itself. The operation and geometric overlap criterion have prior literature,
and the general criterion's priority remains unverified. It receives no
infinity marker.

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
[primary thesis supplement](research/case_study/phase22_linear_priority_supplement.md)
now records an earlier public claim for the q≡5 mod8 range. Its printed
witness has a specific order defect; that does not make the existence
statement false or erase the earlier claim. The thesis quotient at
q≡1 mod8 is a different group, and priority there remains unverified. Neither
a full matched-length comparison nor verified new-resolution status is
established. The measured ratios remain **127/38** and **4/3**, and no
infinity marker is assigned.

The same phase also recovers N009 Theorems 3.6, 3.8 and 5.5 and every
rank-four Table 6 type count, through a uniform central adapter and exact
normal-kernel census. The previously recovered rank-five counts are not
counted again. Phase twenty-two completes the rank-three order-1,024
component and recovers Lemmas 5.2 and 5.4, with all-parameter written
arguments and a fresh finite census. Individual labels and other presentation
claims remain separate, so the principal-result ledger stays at
**twelve works**. A terminating algorithm, a count of 105 classes, and
a short proof of the enumeration mechanism do not by themselves supply
a matched source/replacement proof-length ratio.

The completed third-excess graph now yields the exact cubic count in
every rank at least four, with an explicit rank-three exception. Its
[integer-vector certificate](research/case_study/phase22_excess3_annihilator.md)
proves all later ranks without importing an eventual-polynomiality
theorem. This removes a proof dependency. It does not give a new measured
ratio until the same target and background costs are charged on both
sides. The bounded literature search establishes no verified novelty.

The [common generation theorem](research/case_study/phase23_generation_core.md)
also replaces the additive-kernel/complement steps in two constructions.
Its arbitrary-field extension and exact exceptional boundary are useful
consequences, but the standard cohomological ingredients are credited
and no matched source-length measurement has been made. Neither addition
increases the principal-paper count or receives an infinity marker.
The two measured ratios remain **127/38** and **4/3**.

The geometric parity theorem adds a complete section-level construction
reduction and a source-version-bound counterexample family. It leaves
the fifteen-work principal-result count unchanged: the application sections
of the two newly assessed papers are not covered. Source and replacement
spans have not been matched, so no new finite ratio is assigned. A defect
in a stated theorem is also different from resolving a documented open
conjecture; this finding receives no infinity marker, and correction
priority remains unverified.


Phase thirty-two completes the 2020 source's principal construction/application
scope through nested shadows and an even-coordinate torsor, and recovers two
complete selected presentation families from the 2023 source. The principal
ledger rises to **sixteen works**. Shared theory, retained constructions and
classification inputs still need matched span accounting before a new ratio
can be stated. The two measured ratios remain **127/38** and **4/3**; no
infinity marker is assigned.


Phase thirty-three strengthens the version-bound counterexample to an actual
regular input, using an invariant binary code and a uniform affine theorem.
The independent computations and kernel-decide data certificate check stated
components; they do not give a matched proof-length ratio. A false theorem
consequence is not itself a documented open conjecture. No infinity marker,
new principal-work credit or correction-priority claim is assigned.


Phase thirty-four replaces the isolated regular example with a proved
infinite family at one rank and diagram. Its integer-degree corollary uses
every n≥2 coprime to6. This is additional mathematical scope, not an extra
principal-paper reduction or a measured source/replacement length. The
relevant abelian-cover and coset-twisting prior art is recorded with exact
access limits. Both finite ratios remain unchanged and no infinity marker
is assigned.


Phase thirty-five recovers one complete 2000 construction theorem and proves
an algebraic obstruction for an exact2018 presentation. The latter is an
infinite-group theorem with a finite certificate; it is not an infinite
compression ratio. It does not settle the source's broader geometric
question. The ledger has52 encoded works,38 with specified existing
components rederived, and16 with principal-result coverage. Those are
coverage counts. The two measured ratios remain127/38 and4/3, with no
corpus-wide ratio or infinity marker assigned.


Phase thirty-six strengthens the L003 algebraic result to an actual infinite
universal regular hypertope at parameter six, with infinitely many finite
quotients preserving its residues. Its quotient criterion is formally
verified. The source parameter remains fixed; the broader Problem9.2 and
priority remain unresolved here. This addition changes no existing-result
coverage count, matched ratio or infinity marker.


Phase thirty-seven adds further statement-level reductions within the 2000
construction paper and two counterexamples to assertions in the accessed
version. It also formally proves quotient transport allowing one exceptional
maximal parabolic. These additions change neither existing paper counts nor
the two measured ratios. Published-statement counterexamples are tracked
separately from previously open problems; no infinity marker is assigned.


Phase thirty-eight proves finite regular existence for infinitely many
distinct exact parameters in the 2018 family: every even s>=2. It also
establishes the marked regular universal objects at those parameters,
infinite whenever6|s. This is recorded as substantive partial progress on
the source problem, separately from compression of published proofs.
Uniform odd-parameter existence and priority remain undetermined; unread
2024 main theorems are a material comparison gap. No corpus ratio or
infinity marker is inferred, and the two matched-proof ratios are unchanged.


Phase thirty-nine determines |G_m|=1296m^6 for the specified even-parameter
quotients and formally checks the generic integral-reduction step. A group
order is not a proof-compression ratio. The two matched-proof ratios and
the unassigned infinity marker are unchanged.


Phase forty adds finite regular existence at every source parameter divisible
by three. Combined with the even family, it covers parameters divisible by
two or three; the uniform cases coprime to six and current priority remain
undetermined. Parameter coverage is not a proof-compression ratio. No
existing-paper count or infinity marker changes.


Phase forty-one replaces the even-family 1,296-coordinate action by four
affine maps in six coordinates, with an exact marked comparison and a
standalone certificate. This measures a representation-size reduction;
source and replacement proof spans have not been matched. Neither measured
proof ratio, paper coverage nor the unassigned infinity marker changes.


Phase forty-two proves a free quotient of an index-648 subgroup in the
unfilled rotational presentation and constructs its actual universal
regular geometry. This also proves the compact affine image is a proper
quotient. These are new structural consequences in the stated scope,
with priority unverified; they do not close every finite parameter case.
The two matched ratios, existing-paper coverage and infinity marker stay
unchanged.


Phase forty-three identifies every specified even-family group as a split
extension C_m^6 semidirect Q, with one fixed integral action of the order-1296
group Q. This short structural consequence has not been matched against
source proof spans. It changes no existing-paper count, measured ratio or
infinity marker.


Phase forty-four supplies an eight-dimensional tensor quotient with every
exact parameter s>=3 and every required local group for s>=4. The Fibonacci
scalar-power argument is formally verified for every parameter. Global
intersection and coset Helly remain pending, so no complete open-problem
resolution or infinity marker is assigned. Existing-paper counts and both
matched ratios remain unchanged.


Phase forty-five completes finite regular existence at every integer s>=2
in the specified 2018 toroidal family. Its global geometry follows from a
uniform bounded-product argument with exact finite certificates. The result
is recorded separately from rederiving existing proofs and from finiteness
of universal groups. Current priority remains unverified, so no infinity
marker is assigned. Both earlier proof-span ratios and the sixteen principal
intake candidates remain unchanged; there is still no manuscript-level ratio.


Phase forty-six establishes actual universal marked regular geometries for
every integer parameter in that family, with finite local-preserving quotients.
The historical problem's finite-existence reading is now explicitly matched.
Its universal groups are infinite at multiples of six. The bounded priority
comparison still has a material unread2024 theorem, so novelty and any optional
infinity marker remain unverified. This is separate from manuscript compression.
