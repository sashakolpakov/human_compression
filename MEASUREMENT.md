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

**No numerical corpus compression ratio has been measured. No infinity marker
is assigned in this snapshot.** Several proposed resolutions have written
arguments and substantial checks, but their external priority remains
unverified and their formal certificates cover specified components.

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
| L043, Conjectures 6.1 and 6.2 | Field/intersection statements and their chiral construction consequence | [Proof chain](research/case_study/psl2_chiral_corollary.md); exact finite-field witnesses and partial formalization |
| L052, Problems 9.3 and 9.4 | Nonexistence under the specified standard parabolic coset construction | [Scope audit](research/case_study/hypertope_questions_independent_audit.md); written proofs and an abstract chamber-orbit certificate |
| L092, Conjecture 1 | Hermitian-unital residue connectivity | [Proof](research/case_study/hermitian_unital_proof.md); finite checks and abstract connectivity formalization |
| L102, §5.1.2 and Theorem 6.1(1) | Desarguesian uniqueness and existence in the specified one-dimensional semilinear case | [Proof and source audit](research/case_study/phase4_old_problem_audit.md); written all-parameter proof and exact small-instance checks |
| L114, final p.61 realization question | Decisions for every displayed parameter shape, distinguishing bare subgroup intersections from RWPRI realization | [Complete decision table](research/case_study/phase5_suzuki_higher.md#e-exact-scope-of-the-proposed-resolution); written uniform proofs, two internal reviews and exact coordinate checks |

The [central cyclic lift](research/case_study/central_lift_proof.md) also supplies
a proposed omitted existence range. Its source does not have the same status
as a named conjecture. The improved
[PSL₄ rank bound](research/case_study/phase3_psl4_rank7.md) and partial
[hypertope order bound](research/case_study/phase3_order_bound.md) are progress
with unresolved cases. These distinctions prevent a novelty score from
swallowing the outstanding mathematics.

The proposed 1999 realization decisions retain classical Suzuki structure.
A subsequent [exact counterexample](research/case_study/phase6_suzuki_realization.md)
shows that the printed candidate list is not exhaustive; the former assumption
of its completeness is withdrawn. Its explicit rank-three geometry is firm,
residually connected, flag-transitive and RWPRI. This deserves a separate
prominent result entry, but a corrected exhaustive classification and
publication priority remain unresolved. No infinity marker is assigned.

The [paper registry](research/case_study/paper_registry.json) records exact
targets, retained inputs and coverage. A future quantitative report must
add source and replacement proof spans, the measurement convention, shared
dependency accounting, source hashes and the actual calculation. Until then,
the number of papers indexed, pages downloaded, agents used, or elapsed
research years cannot substitute for a measured ratio.
