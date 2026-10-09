# Leemans literature audit, version 2

Audit cutoff: **9 October 2026**. This is a literature-status record, not an assertion that an unpublished proof developed in this workspace has been accepted by the mathematical community.

Subsequent workspace progress is recorded separately in
[workspace_proof_audits.json](workspace_proof_audits.json) and merged into the
inventory's `followup_proof_audit_2026_10_09` fields on every rebuild. It now
includes a proposed all-q proof of the Suzuki pentagon-count conjecture, a
complete reduction of both L035 principal theorems, partial uniform L034
order bounds, and further PSL4 exclusions. The
[Wenger audit](phase3_egr_conjecture_audit.md) identifies a discrepancy in a
later preprint's claimed partial solution of L025 Conjecture 4.5; that
existence conjecture remains unresolved here. These updates do not convert
the baseline full-text searches below into claims of complete paper reading.

The archived [author catalogue](https://leemans.dimitri.web.ulb.be/papers.html) contains **134 entries: 128 mathematical works and six nonmathematical publications**. All 128 mathematical records now have either an identified full-text audit or an explicit retrieval limitation. The machine-readable [JSON](literature_inventory.json) and [CSV](literature_inventory.csv) preserve every entry. Identifiers L001–L134 refer to positions in the archived HTML. Seventeen directly relevant followups or proof dependencies have identifiers F001–F017.

| Catalogue coverage | Number | What was actually checked |
|---|---:|---|
| Identified full texts |73|Every indexed available text searched for explicit conjectures, questions and future-work statements; candidate contexts and selected main results read. This includes one two-page editorial.|
| Primary abstracts only |46|Author, publisher or institutional abstracts read; article-level open-problem contents remain unknown.|
| Metadata and access attempts only |9|Exact work identity checked, retrieval attempts recorded; no readable primary abstract/full text obtained.|
| Mathematical entries with no recorded retrieval attempt |0|All 128 records have a documented outcome.|

The nine access-only entries are **L001, L005, L049, L058, L067, L080, L084, L089 and L127**. The other 46 inaccessible works have primary-abstract readings. All 55 full-text limitations are explicitly indexed below. This is completed *attempted catalogue coverage*, not a claim to have read every proof, exhausted every library, or audited every paper ever written by every collaborator.

Together with the 17 external followups, **90 indexed full texts** have reproducible lexical searches in [fulltext_open_problem_hits.json](fulltext_open_problem_hits.json). The current search records 406 candidate contexts, including resolved statements and bibliography hits. Only **two short mathematical papers** and **one short editorial** are marked completely read; long papers have explicit section-level or search-level scopes. The selected priority corpus is 37 works: 36 full texts and the 2016 PSL4 institutional abstract. Downloads, abstract archives where available, and alternate valid PDFs carry SHA-256 hashes. Hashes identify the bytes checked; they do not certify mathematical correctness.

Files returned as login pages or publisher HTML with a `.pdf` suffix were rejected. Near-title mismatches were excluded, including J2 PDFs mistakenly returned for older J3/M22/M23 records and the original `{5,3,5}` paper substituted for its separate erratum. OCR was required for L091 and L114 and can miss text. The [older sweep](older_literature_scan.md) records its particular limitations.

## Highest-priority unresolved statements located

| Statement | Exact mathematical scope | Literature status and importance |
|---|---|---|
| Brooksbank–Leemans, 2019, Conjecture 5.1; 2021 survey Conjecture 3 | Among finite simple groups, A11 is the unique group whose string C-group rank spectrum has a gap. A11 has spectrum {3,6}. | No general resolution located. The 2025 degree 11 paper still identifies A11 as the unique known example. This is a broad structural conjecture about simple groups and regular polytopes. |
| Leemans 2021 survey Conjecture 2 | For every odd prime power q, the maximum string C-group rank of PSL(4,q) is 4. | No general upper-bound proof located. Rank 4 existence is established in 2016; checking individual q does not settle the infinite family. |
| Leemans–Moerenhout–O'Reilly-Regueiro, 2017, Conjecture 6.1 | For odd prime p and odd e1,e2>1, choose multiplicatively primitive ji in F_(p^ei). With wi=ji+ji^(-1), some choices make w1²w2²−4(w1²+w2²) a square in F_(p^lcm(e1,e2)). | No published resolution located. This arithmetic obstruction feeds directly into the remaining PSL2 chiral-polytope classification. Coprimality is **not** a hypothesis of this conjecture. |
| Same paper, Conjecture 6.2 | For its Section 6 matrices alpha,beta,gamma, with d=e1e2 and coprime odd e1,e2>1, the required equality is <alpha,beta> intersection <beta,gamma> = <beta>. | No published resolution located. It is a separate intersection-property obstruction; a square-existence argument alone does not prove it. |
| Leemans–Vandenschrick, 2022, Section 7 | Determine which PSU(3,q), q>17, admit a chiral polytope. | Still open in the final manuscript, with no later resolution found in this audit. Possible ranks are only 4 or 5. The final text has examples q=11 and 17; the older arXiv version omits the latter. |
| 2021 survey Problem 9 | Determine maximum ranks for O^±(2m,2^k) and Sp(2m,2^k), k>=2. | Known constructions give every rank 3 through 2m and 2m+1 respectively. They do not establish the proposed maxima in every dimension. |

Primary texts: [rank reduction](https://arxiv.org/pdf/1812.01055), [2021 survey](https://arxiv.org/pdf/1910.08843), [degree 11 followup](https://arxiv.org/pdf/2302.11943), [PSL2 chiral classification](https://arxiv.org/pdf/1606.08017), [final PSL3/PSU3 paper](https://dipot.ulb.ac.be/dspace/bitstream/2013/333283/3/psl3-final.pdf), [characteristic-two constructions](https://arxiv.org/pdf/1709.02219).

For the first two conjectures, significance comes from determining which dimensions of highly symmetric abstract polytopes a finite simple group can support. For Conjectures 6.1/6.2, it comes from completing a precise classification, rather than from the technical appearance of an isolated field identity. None of these is being described here as a universally famous conjecture.

### Dependency check for the PSL2 target

The unresolved family identified in the 2017 paper is q=p^d congruent to 3 modulo 4, where d>1 is not a prime power. Such an odd d has a factorization d=e1e2 with coprime odd e1,e2>1. Thus the coprime part of Conjecture 6.1, together with Conjecture 6.2 and the other verifications in Section 6, is enough for this remaining classification family. The first case is q=3^15.

Write u=w1, v=w2 and Delta²=u²v²−4(u²+v²). The determinant-one representatives used for the construction are

```
alpha = (1/2) [[u, u+2], [u-2, u]]
beta  = (1/2) [[2+u, u], [-u, 2-u]]
gamma = (1/(2u)) [[v(u-2), Delta], [Delta, v(u+2)]]
```

Changing Delta to −Delta gives the other sign. The source's final display suppresses the scalar in gamma; retaining it matters when doing SL2 matrix calculations. The statement is projective.

The final 2022 PSL3 paper, Section 7, explicitly retains this same PSL2 family among the unresolved chiral existence cases. Exact-title and exact-conjecture searches through the cutoff located no later proof. This is evidence about the searched literature, not a guarantee that no unpublished or poorly indexed proof exists. This workspace's new candidate proofs must be tracked separately from the historical status.

## Statements that should not be called open

| Former target | Resolution checked |
|---|---|
| High-rank symmetric-group counting stability, survey Conjecture 1 | Cameron–Fernandes–Leemans, *Advances in Mathematics* 453 (2024), 109832, Theorem 1.1: for fixed kappa>=1 the count, up to isomorphism and duality, of rank n−kappa representations of S_n is constant for n>=2kappa+3. [Text](https://arxiv.org/pdf/2212.12723). |
| Candidate graph list in Table 6 of that counting paper | Leemans–Mulpas, 2026, Proposition 4.8 supplies a counterexample. The stability theorem itself survives. [Gluing paper](https://arxiv.org/pdf/2504.17535). |
| Alternating-group existence at all intermediate ranks | Fernandes–Leemans, 2019, Theorem 1.1 supplies ranks 3 through floor((n−1)/2) for all n>=12. [Text](https://arxiv.org/pdf/1810.12450). |
| Suzuki chiral polytopes have rank 3 | Spiga, 2021, Theorem 1.1 proves this for the relevant almost simple groups. [Text](https://arxiv.org/pdf/2010.04080). |
| O'Nan rank 3 enumeration, survey Problem 10 | The **published** Leemans–Mulpas 2022 paper, Section 5.3, gives 6536 rank 3 representations, 16 rank 4, and none higher. Its old arXiv preprint covers only Suzuki and Rudvalis and is insufficient for this update. [Published PDF](https://adam-journal.eu/index.php/ADAM/article/download/1405/1405). |
| A group-theoretic chirality test for hypertopes | Zhang–Leemans, 2026, Theorem 1.1 gives necessary and sufficient conditions without building the entire incidence graph. [Text](https://arxiv.org/pdf/2511.14562). |
| Unrestricted finite-group incidence representation existence | Díaz Ramos–Molinier–Viruel, arXiv:2511.02410v2, Theorem A realizes every finite pair H normal in G as the type-preserving/full automorphism pair of a finite incidence geometry. This answers the unrestricted finite existence direction raised by Leemans–Stokes–Tranchida 2025; additional regularity constraints are separate. [Text](https://arxiv.org/pdf/2511.02410). |
| Realizing every finite diagram-symmetry group by a regular hypertope | Leemans–Spiga–Tranchida, arXiv:2610.09711, Theorem 1.1, submitted **7 October 2026**, proves this. The date was checked directly; it is within the audit cutoff. [Text](https://arxiv.org/pdf/2610.09711). |
| Type (2) regular 3-polytope existence for every odd prime, Hou–Feng–Leemans 2025, §5 | Li–Zhang, arXiv:2505.09505v1, Theorem 1.3 constructs a self-dual regular 3-polytope of type `{n,n}` with `2^n n` flags for every integer `n>=3`; Corollary 3.6 explicitly answers the earlier question. Our augmentation-module construction independently rediscovered this result. [Primary preprint](https://arxiv.org/pdf/2505.09505). |
| Araujo-Pardo–Leemans edge-girth extremality conjecture | Goedgebeur–Jooken 2025, §4 proves `n(3,8,8)=40<54` and `n(3,12,32)<=162<486`, disproving arXiv Conjecture 4.6/published Conjecture 4.4. This does not by itself settle the separate Suzuki lambda or general existence conjectures. [Primary preprint](https://arxiv.org/pdf/2401.08271). |
| Monson's real-Schur-index 2 existence problem and its polytopal-character variant | Cameron–Herman–Leemans 2022 answer both affirmatively; PSU(5,3) supplies the explicit example. Their final informal suggestion concerning all members of an infinite family is a different statement. [Primary paper](https://arxiv.org/pdf/2201.01313). |
| Earlier PSL2/PGL2 chiral rank/existence conjectures, Elliott–Leemans–O'Reilly-Regueiro 2015, Conjectures 3.2–3.3 | The 2017 paper Theorem 1(1)(2) gives rank<=4 and PGL2(q) rank 4 existence exactly when q>=5. Even q is included, since PSL2(q)=PGL2(q). [Primary paper](https://arxiv.org/pdf/1606.08017). |

## Complete index of the survey's numbered problems

The problem wording below is compressed. “Not resolved in corpus” records a limited status check, not an exhaustive negative literature theorem. [Source](https://arxiv.org/pdf/1910.08843).

| Number | Scope | Audit result |
|---|---|---|
|1|S_n enumeration by rank|High-rank stability solved; general enumeration not resolved in corpus.|
|2|A_n enumeration by rank|Not resolved in corpus.|
|3|PSL2 with Baer involution: ranks 3,4 enumeration|Not resolved in corpus.|
|4|PGL2 with Baer involution: rank 3 enumeration|Not resolved in corpus.|
|5|Almost simple PSL3 socle: maximum rank|Not resolved in corpus.|
|6|Same socle: rank 3 enumeration|Not resolved in corpus.|
|7|Almost simple PSL4 socle: maximum rank|Not resolved in corpus.|
|8|Small Ree rank 3 enumeration|Not resolved in corpus.|
|9|Characteristic-two orthogonal/symplectic maximum rank|See priority table.|
|10|O'Nan rank 3 count|Solved in 2022: 6536.|
|11|Further sporadic computation|Progress: Co2 rank 3=60370; Fi22 rank 3=25052, published 2022.|
|12|Suzuki unrestricted C-group enumeration|Not resolved in corpus.|
|13|Almost simple PSL2 unrestricted C-group classification|Not resolved in corpus.|
|14|Same family: unrestricted enumeration|Not resolved in corpus.|
|15|Small Ree unrestricted C-group maximum rank|Not resolved in corpus; string rank 3 theorem does not settle it.|

## Recent followups and additional live questions

**G2 rank spectra.** Chen's [September 2026 paper](https://arxiv.org/pdf/2609.25004) constructs rank 5 regular polytopes for every even q>2 and obtains ranks 4 and 3 by reduction. Question 4.1 asks whether {3,4,5} is the complete spectrum in even characteristic. Question 4.2 asks whether odd-characteristic G2(q) can have ranks 5 or 6. The paper's census covers prime powers 3<=q<=11. It explicitly acknowledges a different recent Gvozdev–Nuzhin construction. That [published August 2026 paper](https://doi.org/10.1007/s10469-026-09844-2) also treats triality groups; its full proof has not been read here, so its abstract's exceptional parameter range is not promoted to a verified nonexistence theorem.

**Coxeter families.** Chen–Rowley 2025 determine all intermediate ranks for D_n and the rank maxima of exceptional finite irreducible Coxeter groups. Their [Theorems 1–3](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v32i4p18/pdf/) do not automatically imply statements about their finite simple quotients.

**Mondrian partitions.** The [August 2026 Lebowitz-Lockard–Tenenbaum manuscript](https://tenenb.perso.math.cnrs.fr/PPP/Mondrian.pdf) explicitly retains nonexistence of Mondrian integers as Conjecture 1.1. It proves that a positive proportion of side lengths are impossible. This strengthens, but does not finish, the problem studied computationally by Leemans and collaborators below 1001. Its scaling observation makes a density-zero result for possible side lengths equivalent to full nonexistence.

**Girth–diameter cages.** The [original paper](https://arxiv.org/pdf/2401.15539) asks for further constructions attaining order k²+k+2 at girth 5 and diameter 4; it does not state a numbered conjecture asserting attainment for all k. The [2026 Cambie et al. followup](https://arxiv.org/pdf/2511.21144) settles 107 parameter triples and supplies an exhaustive generator. Table 6 confirms exactly two (6;5,4)-cages and does not resolve (7;5,4). Its Question 1 asks whether every even-girth (k;g,d)-cage with d<=g is bipartite, a strengthening connected to the longstanding even-girth cage conjecture.

**Mixing and faithfulness.** Cunningham–Hubard 2025 [final Problems 1–3](https://arxiv.org/pdf/2506.19334) ask for polytopality criteria for admissible covers, preservation of a two-orbit class under mixing, and smallest regular covers. Cunningham–Mochán–Montero–Potočnik–Toledo 2026 [Section 8](https://dirros.openscience.si/Dokument.php?id=49623&lang=eng) asks about two-facet faithfulness, polytopes appearing as posets of unfaithful maniplexes, and connectivity needed for poset reconstruction. These are explicitly stated research problems rather than yes/no conjectures. The latter paper announces a sequel on rotary rank 4 maniplexes; no sequel was verified in this audit.

## Additional explicit statements recovered in the catalogue sweep

“Historical statement; no resolution located” is weaker than a verified current consensus that a problem is open. The latter status requires stronger recent corroboration, as supplied above for the major rank and PSL2 questions. New workspace arguments are separate from published status.

| Source | Exact scope recovered | Status after this audit |
|---|---|---|
|L003 §9 Conjecture 9.1|Table 3 exhausts finite **universal chiral** 4-polytopes of type `{6,3,6}`.|No later resolution located. Universal groups are essential; an arbitrary finite quotient is not a counterexample.|
|L003 §9 Conjecture 9.2–9.3|No finite universal chiral hypertope for the square-cycle diagram with consecutive labels `(6,3,4,3)`; no finite universal regular or chiral hypertope for `(6,3,5,3)`.|Diagrams visually checked on PDF p. 19. No later resolution located.|
|L003 Problem 9.2|Extend Table 8 lines 5–8 to an infinite family with parameters `((3,0),(2,0),(1,1),(s,0))`, integer `s>=2`.|No resolution located in the checked locally toroidal followups.|
|L003 Problem 9.1|Extend McMullen–Schulte quotient criterion Theorem 2E17 to regular/chiral hypertopes.|Partial published answer: L033 §3 Theorem 3.1 lifts the C-group intersection property when the quotient homomorphism is injective on **all** maximal parabolics. Flag transitivity remains a separate geometric condition; no general chiral answer verified.|
|L034 Conjecture 3.3|For `n>=10,s,t>=2,l>=1,n<s+t+l`, no regular 3-hypertope of type `(2^s,2^t,2^l)` has automorphism group order `2^n`.|Final 2019 manuscript retains the conjecture. The `l=1` case and `n<=10` computations are known. No later resolution located, including the 2025/2026 group-order followups.|
|L021 §5 unnumbered conjecture|Infinitely many rank 4 maniplexes with automorphism group PGL2(q), full facet group PGL2(q), and vertex group respectively S4,A5,PSL2(q),PGL2(q).|No subsequent resolution located. The main paper title concerns PSL2, but this final conjecture concerns PGL2.|
|L025 Conjecture 3.2|Suzuki graphs `G_q` are edge-girth-regular with parameters `(q(q^2+1),q,5,q−1)`.|Checked q=8 in original; no general lambda=q−1 proof located. Separate from its refuted extremality conjecture.|
|L025 Conjecture 4.5|For prime powers `q>=3`, `g in {8,12}`, an edge-girth-regular graph with parameters `(2q^((g−2)/2),q,g,(q−1)^((g−2)/2)(q−2))` exists.|Historical existence claim not settled by the extremality counterexamples; no complete resolution verified here.|
|L052 Problem 9.1|Find a minimal set of conditions for IC+ (called IP+ in the earlier preprint).|No general minimal criterion verified. The 2026 chirality test addresses recognition but is not automatically a minimality theorem.|
|L052 Problem 9.2|Classify finite locally toroidal geometries of type `{(3,3,3);p}` for `p=3,4,5`.|Accepted version makes the parameter restriction explicit. No complete classification located.|
|L052 Problems 9.3–9.4|Find a thin residually connected non-flag-transitive standard C-group geometry in rank >=4; find a rank 3 standard C-group geometry lacking thinness, residual connectedness and flag transitivity.|The two requested examples are ruled out by short elementary arguments drafted and independently checked in this workspace: see [coset_geometry_obstructions.md](coset_geometry_obstructions.md). No claim of established publication novelty.|
|L059 Problems 1–2|Classify cubic/quartic flag-transitive cyclic configurations; classify semisymmetric graphs with large vertex stabilizers and corresponding core-free rank 2 coset geometries.|Broad historical classification programmes; current completeness not established by this audit.|
|L092 Conjecture 1, §4.6, p. 569|The construction Γ(U_H(q)) from the Hermitian unital is firm, residually connected and flag-transitive for every prime power q>2.|Original checked q<=16. No later resolution located by two independent targeted searches; OpenAlex had zero indexed forward citations, which is weak negative evidence. Workspace proof and computations are separate, in [hermitian_unital_proof.md](hermitian_unital_proof.md).|
|L102 §5.1.2|Are the flag-transitive RWPRI spread spaces in the one-dimensional affine semilinear case `G<=AΓL(1,p^d)` necessarily Desarguesian?|Exact contextual restriction matters. Present external resolution status unverified.|
|L110 final section; L114 final paragraph|Determine which listed Suzuki RWPRI pregeometries/candidate subgroup configurations are realized by flag-transitive geometries.|Historical realization gap, not the solved string-C-group rank problem. Current completeness unverified.|
|F014 Conjecture 3.7|For every d,n>=3, the stated Coxeter quotient with the additional adjacent-pair relations yields a regular d-polytope of type `{n,...,n}`.|Read in May 2025 v1. No later version or resolution located. The wording does not explicitly assert that every resulting group is finite.|

Additional directions are less definite: L009 §7 reports experiments about gonality 2 inputs and asks for non-linear-space gonality 3 inputs producing well-behaved triality geometries; L024's final remark suggests certain unitary-group characters are always polytopal; L036 proposes extending a rank 2 classification algorithm to higher ranks. These should not be promoted to precise numbered conjectures without specifying the missing quantifiers.

L050 §6 asks whether a graph code whose complementary graph code equals its dual must be LCD, and conversely. [Key–Rodrigues 2018, Proposition 1(2)](https://www.math.clemson.edu/~keyj/Key/LCD_KeyRod.pdf) already proves the forward implication for regular graphs. A short unrestricted matrix argument is available, but its scope and novelty should be distinguished from that prior result. L050 §6.3 also mentions uniqueness of the strongly regular graph with parameters `(253,140,87,65)` as unknown; no later uniqueness theorem was located, but this audit has not reconstructed the entire SRG literature.

The 2025 [symmetric 2-group paper](https://arxiv.org/pdf/2512.15511) supplies constructions and universal extensions; the 2026 [common-quotient theorem](https://arxiv.org/pdf/2605.20691) shows every finite regular 2-power polytope covers Conder's minimal polytope of its rank. Neither is a classification of all 2-power groups/polytopes or a resolution of L034 Conjecture 3.3. The 2023 [central-symmetry/halving construction](https://www.combinatorics.org/ojs/index.php/eljc/article/download/v30i2p20/pdf/) provides further infinite hypertope families but does not state a solution to L003's universal square-diagram conjectures.

## Exact coverage limitations

No mathematical catalogue entry is now untouched. **55 full texts remain unavailable after the recorded searches**, so absence of an open statement in those papers has not been established. Their IDs and titles are listed below; the JSON carries primary URLs, reading scope and retrieval outcomes. Authors have not been contacted, institutional credentials have not been used, and unavailable papers have not been replaced by similarly titled works.

|ID|Title|Available evidence|
|---|---|---|
|L001|Residually weakly primitive and locally two-transitive geometries for sporadic groups|Metadata/access attempts|
|L002|An Atlas of Residually Weakly Primitive Geometries for Small Groups|Primary abstract|
|L004|Chiral polytopes and Suzuki simple groups|Primary abstract|
|L005|Residually weakly primitive geometries of small sporadic and almost simple groups : a synthesis|Metadata/access attempts|
|L006|Incidence Geometry|Primary abstract|
|L048|Polytopes of large rank for PSL(4,q)|Primary abstract|
|L049|Two-transitive pairs in PSL(2,q)|Metadata/access attempts|
|L051|Chiral polyhedra arising from almost simple groups with socle PSL(2,q)|Primary abstract|
|L053|Almost simple groups with socle PSL(2,q) acting on abstract regular polytopes|Primary abstract|
|L055|C-groups of PSL(2,q) and PGL(2,q)|Primary abstract|
|L057|C-groups of Suzuki type|Primary abstract|
|L058|Abstract regular polytopes for the O'Nan group|Metadata/access attempts|
|L060|Locally 2-arc-transitive complete bipartite graphs|Primary abstract|
|L061|Binary codes of some strongly regular graphs of the McLaughlin graph|Primary abstract|
|L062|Corrigendum to "Polytopes of high rank for the symmetric groups"|Primary abstract|
|L065|A new algorithm to find apartments in coset geometries|Primary abstract|
|L067|Polytopes of high rank for the alternating groups|Metadata/access attempts|
|L069|All alternating groups A n with n ≥ 12 have polytopes of rank ⌊ (n-1)/2 ⌋|Primary abstract|
|L072|Polytopes of high rank for the symmetric groups|Primary abstract|
|L075|On the geometry of O'N|Primary abstract|
|L077|On locally spherical polytopes of type {5,3,5}|Primary abstract|
|L078|Locally s-arc-transitive graphs related to sporadic simple groups|Primary abstract|
|L080|On apartments in incidence geometry|Metadata/access attempts|
|L081|A new Petrie-like construction for abstract polytopes|Primary abstract|
|L082|A rank six geometry related to the McLaughlin sporadic simple group|Primary abstract|
|L084|Errata : "Quotients of a universal locally projective polytope of type {5,3,5}"|Metadata/access attempts|
|L085|Almost simple groups of Suzuki type acting on polytopes|Primary abstract|
|L086|An atlas of abstract regular polytopes for small groups|Primary abstract|
|L087|Two rank six geometries for the Higman-Sims sporadic group|Primary abstract|
|L089|On inductively minimal geometries that satisfy the intersection property|Metadata/access attempts|
|L090|A family of geometries related to the Suzuki tower|Primary abstract|
|L093|Constructions of rank five geometries for the Mathieu group M_22|Primary abstract|
|L094|The residually weakly primitive geometries of PSL(3,q) with q < 8|Primary abstract|
|L097|The residually weakly primitive geometries of J_3|Primary abstract|
|L098|The residually weakly primitive geometries of M_23|Primary abstract|
|L099|On a rank four geometry for the Hall-Janko sporadic group|Primary abstract|
|L100|Geometries for the group PSL(3,4)|Primary abstract|
|L101|The residually weakly primitive geometries of M_22|Primary abstract|
|L103|The RWPRI geometries of Sym(5) x 2|Primary abstract|
|L105|Constructing coset geometries with Magma : An application to the sporadic groups M(12) and J(1)|Primary abstract|
|L106|On a rank five geometry of Meixner for the Mathieu group M(12)|Primary abstract|
|L107|Some rank five geometries related to the Mathieu group M(23)|Primary abstract|
|L108|On the Petrials of thin regular rank three geometries|Primary abstract|
|L109|The residually weakly primitive geometries of the Dihedral Groups|Primary abstract|
|L111|New geometries for finite groups and polytopes|Primary abstract|
|L112|On a geometry of Ivanov and Shpectorov for the O'Nan sporadic simple group|Primary abstract|
|L113|An Atlas of regular thin geometries for small groups|Primary abstract|
|L116|Thin geometries for the Suzuki simple group Sz(8)|Primary abstract|
|L117|Two Nearly Isomorphic Groups|Primary abstract|
|L118|On the List of Finite Primitive Permutation Groups of Degree Less Than 50|Primary abstract|
|L119|All Geometries of the Mathieu Group M(11) Based on Maximal Subgroups|Primary abstract|
|L123|The residually weakly primitive geometries of the Suzuki simple group Sz(8)|Primary abstract|
|L124|On Flag-Transitive Incidence Geometries of Rank 6 for the Mathieu Group M(12)|Primary abstract|
|L125|The Residually Weakly Primitive Geometries of the Janko Group J(1)|Primary abstract|
|L127|Tight chiral polyhedra of order 2p m|Metadata/access attempts|

The catalogue is an author-maintained list, not a mathematical guarantee of complete bibliography. OpenAlex and arXiv metadata were used to find alternate versions and followups, with identities checked against titles, authors and publication details. The 17 external works form a targeted followup corpus, not an exhaustive catalogue of all collaborators' publications. Three additional focused checks for the two hypertope questions are recorded separately in [hypertope_prior_art_audit.json](hypertope_prior_art_audit.json); they do not change the indexed corpus counts above.

Rebuild with `python3 research/leemans/build_literature_inventory.py`, then repeat the lexical audit with `python3 research/leemans/scan_open_problem_contexts.py`. Both commands operate locally. The source text and exact hypotheses must still be read before using a theorem as a dependency. In particular, a keyword search finding no numbered conjecture is not evidence that a paper contains no unresolved mathematical issue.
