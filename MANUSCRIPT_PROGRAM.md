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
mathematical qualification. The families of application papers still need
to be written.

| Topic | Existing reviewed manuscript | Required next structural work |
|---|---|---|
| A: Two-group polytopes and hypertopes | [Construction and classification](MODULE_A.md) | Separate the shared theorems about kernels, quotients and local constructions from complete papers devoted to the individual historical results; review the L032 dependency pilot |
| B: Forest coordinates and primitive coset geometries | [Forest coordinates](MODULE_B.md) | Identify its full topic umbrella and preserve the complete recognition, generation and geometric applications |
| C: Halving and Petrial operations on regular geometries | [Operations on regular geometries](MODULE_C.md) | Separate reusable changes of generators and arguments about the objects preserved by these operations from full geometric identifications and censuses |
| D: Marked actions, field orbits and geometry enumeration | [Marked actions and enumeration](MODULE_D.md) | Extract shared theorems about actions and extensions; keep complete field and classification arguments, including correspondence with historical tables, in the application papers |

The [existing U manuscript](UMBRELLA.md) is a source of reusable proofs.
A topic may retain an overlapping part of the same mathematics as another
topic, or need additional theorems. Its full chosen umbrella must be stated
and proved before it can serve as a completed U_A or U_B.

The [current work index](CURRENT_REPORT.md) lists further results that may
inform these choices. Recovering one assertion or proving one equivalence
does not establish all the results promised by an application paper.

## Source papers and results already recovered

These tables describe the existing reviewed proofs that will be reused.
They do not claim that the new families of application papers have already
been written. Each qualification remains part of the result when the
proof is moved into the new structure.

### A. Two-group polytopes and hypertopes

| ID | Source, authors and edition | Main results recovered | Qualifications |
|---|---|---|---|
| N009 | Gomi, Loyola and De Las Peñas, *String C-groups of order 1024* (2018) | Classification of the nondegenerate marked groups; central descent and lifts; explicit presentations and the stated universal group orders | Uses the specified earlier results on square quotients and universal polytopes; corrected diagonal factors and required exhaustive computations remain part of the proof |
| L035 | Hou, Feng and Leemans, *Existence of regular 3-polytopes of order 2^n* (2019 author version, arXiv:1802.08947v2; published as *2-groups behaving as automorphism groups of regular 3-polytopes*) | Existence for the stated orders and types; classification into eight stated families, with explicit presentations and converses | The ranges in Theorems 1.2–1.3 and the cited theorem about cyclic normal subgroups remain in force; this is not a classification of every two-group polytope |
| L032 | Hou, Feng and Leemans, *On regular polytopes of 2-power order* (2020; revised author version dated 8 November 2019) | Theorem 1.2: a string C-group of order 2^n for every stated admissible rank and sequence of adjacent orders | The hypotheses d ≥ 3, n ≥ 5, kᵢ ≥ 2 and Σkᵢ ≤ n − 1 are retained; the broader classification problem is not solved |
| F016 | Cunningham, Feng, Hou and Schulte, *Symmetric polytopes whose automorphism groups are 2-groups* (2025 preprint, arXiv:2512.15511v1) | The stated regular, alternating and free-extension constructions, including their orders, local sections and presentations | Earlier geometric assembly theorems are cited inputs; infinite groups are included only in the extension clauses that allow them |
| F013 | Hou and Schulte, *String C-groups of 2-power order project onto a common string C-group* (2026 preprint, arXiv:2605.20691v1) | The common marked quotient and associated polytope covering results, Theorems 1.1–1.2 | Applies to the stated finite nondegenerate groups; auxiliary source corrections and the standard group/polytope correspondence remain explicit |
| L034 | Hou, Feng and Leemans, *Existence of regular 3-hypertopes with 2^n chambers* (2019 author version, arXiv:1901.09034v1) | The exact group presentation, order, type and regular geometry; the three cyclic kernels and the quotient decomposition | The source's parity assignments and repeated kernel generator are corrected; Conjecture 3.3 is not proved by this construction |

See the [A manuscript and review](MODULE_A.md) for the full statements and
all computations needed by the proofs.

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

## Open questions

Conjecture work continues alongside source compression. The
[question-results catalogue](CONJECTURE_RESULTS.md) keeps statements,
later resolutions, verified cases and open gaps separate. An answered
question needs its own proof and a check of the later literature; it does not
produce a numerical saving against a prior proof that did not exist.
