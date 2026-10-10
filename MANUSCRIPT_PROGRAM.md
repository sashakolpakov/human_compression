# Topic umbrellas and application papers

The intended unit is a **topic containing several complete papers**:

```text
Topic A:  U_A + A₁ + A₂ + …  →  LA₁, LA₂, …
Topic B:  U_B + B₁ + B₂ + …  →  LB₁, LB₂, …
```

U_A contains the reusable theorems for topic A, with complete proofs.
Each Aᵢ is one of our application manuscripts, corresponding to a named
historical manuscript LAᵢ. It states exactly which main results it derives,
checks the hypotheses of the umbrella theorems, proves the local
constructions and treats the exceptional cases. With those arguments in
place, the historical results should follow as straightforward corollaries.

Application papers should use ordinary academic exposition, at a level
of detail comparable to the source literature. Their length follows the
complete argument. Once U_A is established, some Aᵢ may be very short.
There is no page target for an individual application and no reason to
split one argument into nominally separate papers.

## Rework the proof material already available

The current A–D documents each combine several sources in one reviewed
manuscript. We will reorganize their proofs while preserving every
mathematical qualification. [Topic A now has its complete umbrella and
first application](TOPIC_A.md). The other application papers still need
to be written. The [new projective-line proof](PROJECTIVE_LINE_POLYTOPES.md)
provides two complete principal classifications for topic E. Its
[third application](PROJECTIVE_LINE_MANIPLEXES.md) now recovers the complete
specified PSL₂ maniplex contract with source corrections.

| Topic | Existing reviewed manuscript | Required next structural work |
|---|---|---|
| A: Two-group polytopes and hypertopes | [Complete U_A and L032 application](TOPIC_A.md); [remaining proof material](MODULE_A.md) | Rework the five remaining applications; retain their full presentation, classification and geometric arguments |
| B: Forest coordinates and primitive coset geometries | [Forest coordinates](MODULE_B.md) | Identify its full topic umbrella and preserve the complete recognition, generation and geometric applications |
| C: Halving and Petrial operations on regular geometries | [Operations on regular geometries](MODULE_C.md) | Separate reusable changes of generators and arguments about the objects preserved by these operations from full geometric identifications and censuses |
| D: Marked actions, field orbits and geometry enumeration | [Marked actions and enumeration](MODULE_D.md) | Extract shared theorems about actions and extensions; keep complete field and classification arguments, including correspondence with historical tables, in the application papers |
| E: Projective centralizers, polytopes and maniplexes | [Complete U_E and three applications](PROJECTIVE_LINE_POLYTOPES.md) | Extend the frozen two-application measurement to the new third intake; the 7 + 3 + 2 + 9-page papers are independently reviewed |
| F: Odd kernels and cyclotomic polyhedra | [Complete L014 application](ODD_KERNEL_POLYHEDRA.md) | Develop further applications and extract the full topic umbrella from the character and cyclotomic arguments; the first eight-page paper is independently reviewed |

The [existing U manuscript](UMBRELLA.md) is a source of reusable proofs.
A topic may retain an overlapping part of the same mathematics as another
topic, or need additional theorems. Its full chosen umbrella must be stated
and proved before it can serve as a completed U_A or U_B.

The [current work index](CURRENT_REPORT.md) lists further results that may
inform these choices. Recovering one assertion or proving one equivalence
does not establish all the results promised by an application paper.

## Source papers and results already recovered

These tables describe the existing reviewed proofs that will be reused.
The standalone L032 application and three Topic E applications are complete.
The remaining combined A–D material still needs further application papers.
Each qualification remains part of the result when its proof is moved into
the new structure.

### A. Two-group polytopes and hypertopes

| ID | Source, authors and edition | Main results recovered | Qualifications |
|---|---|---|---|
| N009 | Gomi, Loyola and De Las Peñas, *String C-groups of order 1024* (2018) | Classification of the nondegenerate marked groups; central descent and lifts; explicit presentations and the stated universal group orders | Uses the specified earlier results on square quotients and universal polytopes; corrected diagonal factors and required exhaustive computations remain part of the proof |
| L035 | Hou, Feng and Leemans, *Existence of regular 3-polytopes of order 2^n* (2019 author version, arXiv:1802.08947v2; published as *2-groups behaving as automorphism groups of regular 3-polytopes*) | Existence for the stated orders and types; classification into eight stated families, with explicit presentations and converses | The ranges in Theorems 1.2–1.3 and the cited theorem about cyclic normal subgroups remain in force; this is not a classification of every two-group polytope |
| L032 | Hou, Feng and Leemans, *On regular polytopes of 2-power order* (2020; revised author version dated 8 November 2019) | Theorem 1.2: a string C-group of order 2^n for every stated admissible rank and sequence of adjacent orders | The hypotheses d ≥ 3, n ≥ 5, kᵢ ≥ 2 and Σkᵢ ≤ n − 1 are retained; the broader classification problem is not solved |
| F016 | Cunningham, Feng, Hou and Schulte, *Symmetric polytopes whose automorphism groups are 2-groups* (2025 preprint, arXiv:2512.15511v1) | The stated regular, alternating and free-extension constructions, including their orders, local sections and presentations | Earlier geometric assembly theorems are cited inputs; infinite groups are included only in the extension clauses that allow them |
| F013 | Hou and Schulte, *String C-groups of 2-power order project onto a common string C-group* (2026 preprint, arXiv:2605.20691v1) | The common marked quotient and associated polytope covering results, Theorems 1.1–1.2 | Applies to the stated finite nondegenerate groups; auxiliary source corrections and the standard group/polytope correspondence remain explicit |
| L034 | Hou, Feng and Leemans, *Existence of regular 3-hypertopes with 2^n chambers* (2019 author version, arXiv:1901.09034v1) | The exact group presentation, order, type and regular geometry; the three cyclic kernels and the quotient decomposition | The source's parity assignments and repeated kernel generator are corrected; Conjecture 3.3 is not proved by this construction |

The [complete U_A and first application](TOPIC_A.md) recover L032 through
an explicit supported construction. The [earlier A manuscript](MODULE_A.md)
retains the other proofs and their required computations.

### B. Forest coordinates and primitive coset geometries

| ID | Source, authors and edition | Main results recovered | Qualifications |
|---|---|---|---|
| N001 | Buekenhout and Cara, *Some properties of inductively minimal geometries* (1998; complete authored text) | All four parts of Theorem 1: the stated primitivity, transitivity and intersection properties and the diagram criterion | The earlier 1997 classification and uniqueness theorem remain cited inputs; ambiguous wording about quasi-primitivity is disambiguated. The original PDF is unavailable and the retrieved diagrams are damaged |
| N003 | Cameron and Cara, *Independent generating sets and geometries for symmetric groups* (2002; complete author manuscript) | Extremal generating families, three counting conventions, strong and relative independence, and recognition of the geometries of maximum rank | The symmetric-group classification uses degree at least 7; general numerical statements keep their finite-group scope. Whiston's bound and the separate result about omission subgroups are cited inputs, including their classification dependence |
| N008 | Archer, Cara and Krempa, *Using the Frattini Subgroup and Independent Generating Sets to Study RWPRI Geometries* (2005 journal article) | Containment in geometric stabilizers, quotient and residue results, and the stated classification for finite p-groups | The unrestricted infinite-group converse about relative generators is false and is replaced by its proved finite-group form |
| L030 | García-Colín and Leemans, *An infinite family of locally X graphs based on incidence geometries* (2021; revised institutional manuscript titled *An infinite family of incidence geometries whose incidence graphs are locally X*) | The weighted-star construction, residues, distances, diagram parameters and full graph automorphism groups | Uses the revised manuscript's numbering; three source assertions are corrected, and its identity with the final journal layout is not assumed |

The [B manuscript and review](MODULE_B.md) give the exact theorem ranges,
older dependencies and limits of the available source texts.

### C. Halving and Petrial operations on regular geometries

| ID | Source, authors and edition | Main results recovered | Qualifications |
|---|---|---|---|
| L088 | Hartley and Leemans, *On the thin regular geometries of rank four for the Janko group J1* (2005 journal article) | All six constructions and their invariants; exhaustive classification in rank 4 and exclusion of higher ranks for the stated geometries | Thinness, regularity and residual connectivity are required. Two printed figure labels are interchanged; the complete subgroup catalogue and the required J1 computations remain explicit |
| N013 | Montero and Ivić Weiss, *Locally Spherical Hypertopes from Generalised Cubes* (2020, arXiv:2001.11082v1) | Halving and parity groups; polygon parameters; all stated locally spherical cases and exceptional orders; the original and halved toroidal geometries | Preserves the source's lattice-face interpretation of nondegeneracy and dual convention; Danzer's construction and classical Coxeter results are cited inputs |
| L108 | Bonheure, Buekenhout and Leemans, *On the Petrials of thin rank 3 geometries* (2001; complete saved authored text) | Obstruction to thinness, connectivity, faithful regularity and recovery by taking a second Petrial, including the proved infinite cases | Unconditional assertions about action kernels and lengths are corrected. The original PDF is unavailable; the complete authored rendering and its review are the available evidence |
| F014 | Li and Zhang, *Regular 3-polytopes of type {n,n}* (2025, arXiv:2505.09505v1) | Theorems 1.3 and 3.4: all n≥3, exact matrices and universal presentation, self-duality, type and flag count; both parameter corollaries | [Complete new application](EQUAL_LABEL_POLYGONS.md) uses N013’s earlier polygon construction, credits the source presentation argument, corrects the action convention and treats n=2 separately. Five supporting Lean declarations; full theorem remains written. |

The [C manuscript and review](MODULE_C.md) include the geometric
identifications and the complete finite programs; those arguments cannot
be omitted from the new application papers.

### D. Marked actions, field orbits and geometry enumeration

| ID | Source, authors and edition | Main results recovered | Qualifications |
|---|---|---|---|
| L066 | Kiefer and Leemans, *On pairs of commuting involutions in Sym(n) and Alt(n)* (2013; nine-page author PDF) | Both counting formulas in every stated degree, the exceptional degree-six cases, and the complete stated regular-polyhedron classification for S₆ and A₆ | The ambient automorphism theorem and group/polytope correspondence remain cited inputs; the author PDF has not been collated with the publisher's edition |
| L074 | Kiefer and Leemans, *On the number of abstract regular polytopes whose automorphism group is a Suzuki simple group Sz(q)* (author manuscript dated 27 September 2011) | Both counting formulas for every odd exponent, generation, the intersection property, rank restrictions, absence of self-duality and the prime specialization | Classical Suzuki-group structure remains a cited input; the older source L085 is not counted as an additional completed paper |
| L104 | Leemans, *The residually weakly primitive geometries of J₂* (2002 journal article) | The complete census of 8, 19 and 3 classes in ranks 2, 3 and 4, respectively, and exclusion of higher ranks, with the stated identifications under group automorphisms and permutations of types | The complete subgroup catalogue is an input. Further printed diagrams, geometric automorphism and correlation groups, and the doubling relation have not all been recovered |

**Additional result: only part of this paper has been recovered.**

| ID | Source, authors and edition | Results recovered so far | Remaining work |
|---|---|---|---|
| L073 | Leemans and Rowley, *Rank three residually connected geometries for M₂₂, revisited* (2010 journal article) | The 81 rank-two and 431 rank-three classes, explicit witnesses and eight families of geometric shadows | The refined correspondence with the printed table is incomplete. This row is not counted among the three papers whose stated main results are recovered |

The [D manuscript and review](MODULE_D.md) distinguish these results from
the unrecovered parts of the source papers.

### E. Projective centralizers, polytopes and maniplexes

| ID | Source, authors and edition | Main results recovered | Qualifications |
|---|---|---|---|
| L083 | Leemans and Schulte, *Groups of type L₂(q) acting on polytopes*, retained arXiv math/0606660v1 PDF | Rank restriction; Theorems 1, 3 and 4; the complete ten-row universal table; uniqueness and stated geometric properties of the 11-cell and 57-cell | Classical subgroup types and the group–polytope correspondence are retained inputs. Introductory claims about other presentations and chiral constructions remain background. The bound PDF includes a later typesetting date; no different edition is inferred. |
| L079 | Leemans and Schulte, *Polytopes with groups of type PGL₂(q)*, arXiv:0909.1991v1 | Rank restriction and Theorem 10: the unique example in rank at least four is the 4-simplex with PGL₂(5) | The seventeen-case PΣL₂(25) census and Conjecture 11 remain outside this recovery. |
| L021 | Leemans and Toledo, *Maniplexes with automorphism group PSL(2,q)*, May 15, 2023 author manuscript | All-prime-power rank and end-group restrictions, two-proper-end classification, full torus extension theorem and both source families | Natural-subfield distinction and S₄/self-duality/centralizer corrections are explicit. The separate PGL question is not counted here; no complete marking census or full Lean theorem is claimed. |

The [complete common proof and independent review](PROJECTIVE_LINE_POLYTOPES.md)
include exact computation of all ten universal presentations. Five Lean
statements verify the abstract normalizer obstruction. The matrix argument,
classical inputs and complete classifications remain written and computational.
The additional Conjecture 11 is [historically answered](research/case_study/phase240_L079_status.md);
it remains outside our present replacement.
The [separate U_E and both complete applications](PROJECTIVE_LINE_POLYTOPES.md)
are now independently reviewed: seven umbrella pages, three PSL₂ pages and
two PGL₂ pages, with one required shared program. The historical answer to
Conjecture 11 is [recorded separately](research/case_study/phase240_L079_status.md).
The [first topic measurement](TOPIC_E_MEASUREMENT.md) gives conditional local
factors of 1.62× and 2.38×. The full written factor is 0.835×: the two
applications have not yet repaid their umbrella. The complete program is
also charged, with unknown historical artifact cost stated separately.
This phase251/253 measurement is the two-application baseline and excludes
the new nine-page [PSL₂ maniplex application](PROJECTIVE_LINE_MANIPLEXES.md).
The third application retains the full umbrella and adds its actual sggi
interface, torus arguments, local census and three scoped Lean declarations.

### F. Odd kernels and cyclotomic polyhedra

| ID | Source, authors and edition | Main results recovered | Qualifications |
|---|---|---|---|
| L014 | Hou, Feng, Leemans and Qu, *String C-groups of order 4p^m*, arXiv:2407.10388v1 (2024; later journal publication 2025) | Theorems 1.1–1.3 and the marked construction of Theorem 5.1: normal odd kernel, abelian/tight classification and nonabelian family for all stated parameters | The literal v1 marking is corrected. Cunningham–Pellicer's tight classification is a cited input; the introductory census and a classification of all nonabelian kernels are excluded. |

The [complete eight-page application](ODD_KERNEL_POLYHEDRA.md) has independent
review, exact finite checks and five limited Lean declarations. A separate
full U_F and further application papers remain to be completed.

### Affine periods and mixed-prime polyhedra

| ID | Source, authors and edition | Main results recovered | Qualifications |
|---|---|---|---|
| L012 | Hou, Feng and Leemans, *Regular 3-polytopes of order 2^n p*, arXiv:2001.02945v2 (14 July 2024; later journal publication 2025) | Theorems 1.2/3.1, 4.1, 1.3, 4.3 and 5.1, with Corollaries 4.2, 4.4 and 5.2: full type restriction, exact presentations, existence range and all six affine families | Corrected first period sign in Lemma 4.5; Burnside, Lucchini, the complete order-384 catalogue and exact presentation algorithms remain inputs. The general classification problem, full Table 1 census and seed uniqueness are excluded. |

The [separate five-page affine theory and nine-page application](MIXED_PRIME_POLYHEDRA.md)
are independently reviewed. Their required Topic A umbrella, existing cubic
proof and programs remain chargeable; this is not a fourteen-page total
dependency claim. A larger topic of complete applications and its matched
measurement remain to be developed.

## What each paper must supply

1. Name the exact historical editions and main results to recover. State
   any exclusions, corrected assertions and earlier theorems being used.
2. A dependency map separating our proved shared theorems, substantial
   local proofs and borrowed results. The source proof's own reuse must
   also be represented fairly.
3. Complete mathematical arguments, with attribution at the point of use.
4. An exact statement of what the computations and Lean proofs establish.
   Distinguish finite checks, written proofs and complete formal proofs.
5. Independent review of the source comparison and proofs, and a cost
   record including every required appendix and mathematical program.

The [dependency pilot](DEPENDENCY_PILOT.md) tests the comparison on a
specific existence theorem. It is not a certificate that the full source
paper or the whole topic has already been replaced. Graph node counts
are not a complexity metric.

## Independent topic costs and chronological reuse

For topic A, compare the matched historical cost with

```text
c(U_A) + c(A₁) + c(A₂) + …
```

Each application cost includes all required proofs, appendices and programs.
Topic B pays its own full c(U_B), even when U_A and U_B overlap. Do not deduplicate that
overlap in the independent topic statistic. There is no single global U
charged once across all topics in this comparison.

A separate GKM account may track when proofs were developed and reused,
discounting earlier work only under stated conditions. It needs actual
dependencies and complete local costs; it cannot silently replace the
independent topic comparison. The exact definitions and diagram conventions
belong in [TOPIC_COMPLEXITY.md](TOPIC_COMPLEXITY.md).

The [older compilation programme](archive/README.md) has a separate
archive. Its rates and coarse checkpoints do not carry over to these
new papers. The comparison may show an increase in length; an outcome
that has not been measured should be reported as such.

## Conjectures and questions: recorded solutions

Solutions to questions posed in the source literature are a separate
part of the programme. The repository currently records **twelve complete
answers to the stated questions, under their specified hypotheses**, including
the general minimal-cover theorem and the negative answer to F014 in its
cited preprint version and the unnumbered gonality-two experimental
suggestion. One further entry addresses the two readings of
an ambiguously worded question; its limits are listed separately below.
These results belong in the account
of what the project has achieved, alongside
the recovered published theorems. They do not increase a source-length
compression ratio: there was no earlier proof to put in its numerator.

| Source question | Recorded answer | Proof and verification |
|---|---|---|
| L043, Conjecture 6.1 | For every stated odd prime and pair of odd extension degrees greater than one, suitable primitive elements make the specified expression a nonzero square. | [Complete arithmetic proof and independent review](PRIMITIVE_SQUARES.md), exact exceptional-case computations and six polynomial Lean declarations. The character-sum argument and full theorem remain written. |
| L009, §7, final 2026 journal | Point cloning refutes the experimental gonality-two suggestion for every multiplicity a ≥ 2. | [Complete proof and independent review](POINT_CLONING.md); exact finite checks and four axiom-free Lean path proofs. Twin points are allowed by the stated definitions; the variant excluding them remains unanswered. |
| L043, Conjecture 6.2 | For the specified matrices and coprime odd extension degrees, the middle parabolics intersect exactly in their common cyclic subgroup. | [Intersection proof](research/case_study/psl2_intersection_proof.md); Lean verifies field and entrywise intersection components, with the source-group and geometry identifications remaining written. |
| L025, Conjecture 3.2 | The specified Suzuki graphs have girth five and exactly q−1 pentagons through each edge. | [Cycle proof](research/case_study/suzuki_cycle_proof.md) and dedicated mathematical review; Lean verifies the matrix membership component. |
| L092, Conjecture 1 | The Hermitian-unital construction is firm, residually connected and flag-transitive for every prime power q>2. | [Complete proof and independent review](HERMITIAN_UNITALS.md); thirteen additional Lean declarations verify actual unitary transport and root moves. The full geometric theorem remains written. |
| L102, §5.1.2 | In the stated affine semilinear case, the spread is Desarguesian; the specified existence and uniqueness conclusions follow. | [Written argument](research/case_study/phase4_old_problem_audit.md) and [descent review](research/case_study/phase4_spread_descent_audit.md); both local primitivity assumptions are essential. No complete Lean proof. |
| L007, §7 | Non-tight chiral polyhedra exist throughout the omitted even-exponent range. | [Construction](research/case_study/central_lift_proof.md) and dedicated review; Lean verifies conditional transfer, with the actual group construction and order calculation remaining written. |
| L052, Problem 9.3 | The requested thin, residually connected but non-flag-transitive example cannot occur for the standard parabolic coset construction. | [Coset argument](research/case_study/coset_geometry_obstructions.md) and dedicated review; Lean verifies propagation of a chamber orbit. |
| L052, Problem 9.4 | A rank-three standard parabolic coset system is residually connected, excluding the requested simultaneous failure. | [Coset argument](research/case_study/coset_geometry_obstructions.md) and dedicated review; the complete geometric theorem remains written. |
| F014, Conjecture 3.7, arXiv v1 | **False:** no regular d-polytope satisfying all the stated relations at label 11 exists for any d≥5. Every quotient retaining the adjacent order is excluded. | [Complete proof and certificates](LABEL_ELEVEN_OBSTRUCTION.md), independently reviewed. Nine general Lean declarations support the quotient argument; [coset bounds through rank three](COSET_CERTIFICATES.md) are now kernel-checked. The larger computations and full theorem remain outside Lean. The 2026 journal formulation and priority are unverified. |
| Cunningham–Pellicer, Problem 5; N016, §4 | Every finite-rank abstract polytope has a minimal regular polytopal cover, unique exactly when its distinguished monodromy group is a string C-group. | [Full general proof and independent review](MINIMAL_REGULAR_COVERS.md). Covers may be infinite. Five new and six retained Lean declarations verify algebraic steps; the geometry and full theorem remain written. [Infinitely many finite covers](INFINITE_MINIMAL_COVERS.md) are proved separately in four families, and the [uniform square-torus application](SQUARE_TORUS_COVERS.md) adds every odd square-torus pyramid. The general finite version remains unresolved. |
| L021, final conjecture of §5, May 2023 author edition | Four infinite regular rank-four PGL₂ families with one full end and other end S₄, A₅, PSL₂(p), or PGL₂(p). | [Complete proof and independent review](PGL_MANIPLEX_FAMILIES.md). Eleven Lean matrix/root-group declarations; the full existence theorem remains written. The bounded priority search does not establish a first-proof claim. |

### The remaining ambiguous formulation

| Source question | Result obtained | Remaining scope |
|---|---|---|
| L003, Problem 9.2 | Finite examples exist for every s≥2; the exact universal groups are infinite for every s≥6. | [The two readings explained](TOROIDAL_QUESTION.md). Lean proves infinitude of the exact presentations; the geometric identification remains written. Universal-group structure and priority are separate questions. |

The [question-results catalogue](CONJECTURE_RESULTS.md) gives the full
parameter ranges, original attribution, borrowed results, review records
and precise Lean coverage. Historical priority has not been established
for these answers. A recorded solution, a complete formal proof and a
verified first solution to a still-open problem are distinct claims.
F014 moves from a partial result to a complete negative answer for the
bound source version. The minimal-cover result now answers the unrestricted
question, beyond the earlier five families. The four-family PGL answer
adds one entry. The total is now twelve distinct question entries.

The [locally faithful cover criterion](LOCALLY_FAITHFUL_COVERS.md) is a
separate proved tool for the remaining finite-cover problem. It includes a
complete classification of Tomotope covers with abelian kernel preserving
both ends, and an obstruction for every odd-primary kernel under that
condition. Its rational-homology multiplicity theorem has explicit
hypotheses; no additional complete-answer count is assigned.
