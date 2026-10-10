#!/usr/bin/env python3
"""Author a focused application volume from reusable reviewed proof material.

This is an authoring aid, not a retention proof or a size comparison.  The old
manuscript is read solely to avoid retyping established branch arguments.  The
new mathematical architecture is U plus A; the source contract is in A's ledger.
Never changes a frozen predecessor.  Output must not exist.
"""
import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OLD = ROOT / 'phase78_n009_integration_manuscript.md'
EXPECTED = '15dd00e3845526dc40bb0effa07652e32748958238759eae9a856d901071b801'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise SystemExit('Refusing existing output')
    if hashlib.sha256(OLD.read_bytes()).hexdigest() != EXPECTED:
        raise SystemExit('Proof-material binding changed')
    old = OLD.read_text()
    def between(a, b):
        start = old.index(a)
        return old[start:old.index(b, start)]

    front = r'''# Module A: Construction and classification of two-group polytopes

## Application A of the marked-group umbrella theory

Private scientific draft, 10 October 2026. This volume is being independently
challenged and is not an admitted replacement or a measured compression claim.
It cites the companion umbrella manuscript **U** for general algebraic proofs.
The exact U theorem signatures are listed in §1; the companion ledger binds
the complete second author checkpoint of U, not just the cited statements.

The same local data can serve two different purposes: building a group with
prescribed sections, and listing every group of a bounded order. In the first
direction, small kernels are attached to subsets of the generator labels. In
the second, a common nilpotent quotient reduces the search to normal subgroups
of one finite group. This volume develops both directions for two-group
polytopes and connects them through a class-two vertex-and-edge model.

The applications recover the declared principal results of five sources:
Hou–Feng–Leemans on prescribed 2-power orders [HFLa] and on high-type rank-three
groups [HFLb], Hou–Schulte on the common quotient [HS26],
Cunningham–Feng–Hou–Schulte on prescribed square sections and extensions
[CFHS25], and Gomi–Loyola–De Las Peñas on order 1024 [GLP18]. The bundle spans
2018–2026 in its specified editions. Earlier published geometric and cyclic-core
theorems remain explicit inputs. The source results are attributed individually
in §9; no source is credited merely because its terminology occurs here.

The central conclusions are these. Every finite marked two-group with a forest
diagram and the intersection property has the same class-two quotient for that
diagram (§2). The square lattice supplies a single family of local kernels
(§3); U's supported-kernel theorem then gives prescribed edge orders, consecutive
square sections and alternating assembly (§4). A bounded cyclic core reduces
the high-type rank-three classification to eight explicit models (§5). Exact
central descent and one invariant-kernel census complete the order-1024
classification, including presentation recognition and named facets (§§6–7).
The free-extension conclusions use U's amalgam theorem and precisely stated
geometric constructions (§8).

The mathematical text and its complete certificate artifacts form one charged
proof package. The programs and all defining presentation data are external
appendices, rather than repeated source code in the exposition. They are not
unpriced black boxes: Appendix C specifies every input, algorithmic assumption,
exhaustion argument, required check, output and replay command. Acquisition of U
is charged once and every use of it in A has explicit hypothesis obligations.
No page target, eventual twelve-paper bundle, or numerical saving is asserted
before the complete package is rendered and reviewed.

## 1. Markings, geometric inputs and the interface to U

A marking is an ordered generating family of nonidentity involutions
\(r_i\), indexed by a finite set \(I\). Write
\(G_J=\langle r_j:j\in J\rangle\). The intersection property is
\(G_J\cap G_K=G_{J\cap K}\) for every pair of subsets. A string
C-group also has \([r_i,r_j]=1\) for \(|i-j|>1\); nondegeneracy
means that consecutive generators do not commute. The type is their consecutive
product orders. Use \([x,y]=x^{-1}y^{-1}xy\), \(x^y=y^{-1}xy\),
and \(D_8\) for the dihedral group of order eight. Ordered marked
isomorphisms preserve every generator. The [GLP18] census instead identifies
generator sets; for a nondegenerate string this adds precisely reversal.

We retain the regular-polytope/string-C-group correspondence, the marked
epimorphism/cover correspondence and the coset description of faces and
stabilizers. A deletion sends selected markers to themselves and all others
to one. Its geometric interpretation gives the flat amalgamation property
(FAP) at the corresponding initial or final cut. Flatness itself is a separate
incidence conclusion: a factorization of the group by two relevant face
stabilizers makes every face of the first kind incident with every face of the
second kind. It is never inferred merely from IP.

The general facts used from U are listed with provisional exact signatures.
Their complete proofs occur once in U, not in the application proof cost again.

* **U.K**: if a marked epimorphism \(G\to B\) has kernel \(N\)
  and the base has IP, then G has IP exactly when the profiles
  \(N\cap G_J\) have the same subset-intersection property.
* **U.Q**: for a quotient \(q:G\to G/N\),
  \(q(A)\cap q(B)=q(A\cap B)\) holds exactly when
  \(N\cap BA=(N\cap B)(N\cap A)\). In particular
  \(N\cap BA=1\) preserves the
  intersection and embeds both ends; if \(N\le A\), then
  \(q(A)\cap q(B)=q(A\cap B)\). The latter still requires checking
  that the displayed quotient marking on A is valid.
* **U.DEL**: a full Boolean family of genuine deletions implies IP and
  split parabolic retractions, including infinite groups.
* **U.SK**: exact base deletions and epimorphisms \(E_S\to B_S\)
  injective on every proper-support parabolic give the full supported fiber
  group, with kernel profile
  \(\ker\pi\cap H_J=\prod_{S\subseteq J}\ker(E_S\to B_S)\).
  It has IP, inherits Boolean deletions, and has the resulting parabolic
  order formula. Antichain supports embed their full local groups. If every
  local kernel is \(\gamma_c(E_S)\) and B has class below c, the
  global kernel is \(\gamma_c(H)\). A supported separator gives
  \(H=H_JH_K\) when \(B=B_JB_K\).
* **U.FQ/LAD**: for an involutory finitely generated presentation F with
  deletions, its class-two quotient Q inherits deletions and IP. Finite marked quotients with
  that same Q and order \(|Q|2^k\) are classified by suitable kernels
  inside \(\gamma_3(F/\gamma_{k+3}(F))\). Their IP is the exact
  all-parabolic kernel-profile condition. Every invariant index-two step is
  a hyperplane preimage in \(M/(\Phi(M)[M,U])\), and iterating k
  steps exhausts every index-\(2^k\) invariant kernel.
* **U.PHI**: an irredundant generating marking of a finite two-group maps to
  a basis of its Frattini quotient; every binary coordinate assignment gives
  a character. All marked parabolics have the corresponding coordinate images.
* **U.TOR**: p-primary finite torsion is preserved by subgroups, finite
  p-group extensions and amalgamated free products. Proper embeddings in both
  factors make an amalgam infinite; finitely generated factors generate it.
* **U.Order**: finite normal factors and a finite quotient-index bound give
  the product upper bound; a marked finite quotient attaining that bound
  identifies the complete presentation.

U retains Burnside's basis theorem, lower-central graded Lie theory, finite
nilpotency of finite two-groups and amalgam normal forms. Here we additionally
retain the Gaussian-integer Euclidean algorithm, the precise cyclic-core theorem
in §5 and the geometric assembly/extension theorems in §§4 and8. The standard
low-rank string-IP criteria, smooth square-quotient classification, universal
geometric interpretation and exceptional infinite decomposition quoted by
[GLP18] are stated where used. Exact GAP group and coset algorithms and NQ's
universal nilpotent quotient algorithm are computational inputs. No finite
classification catalogue supplies search completeness.

## 2. A canonical quotient and one finite classification problem

The application-specific bridge to U is a rigidity statement: a forest diagram
forces independent edge commutators in degree two. Its proof uses actual IP in
G; no intermediate quotient is presumed to retain IP.

'''
    forest = between('**Lemma Q5.1 (descending lift).**', '### A single finite-kernel classification')
    forest = forest.replace('Theorem S', 'U.PHI').replace('Theorem Q5.3', 'Theorem A2.3').replace('Corollary Q5.4', 'Corollary A2.4')
    forest = forest.replace('Lemma Q5.1', 'Lemma A2.1').replace('Lemma Q5.2', 'Lemma A2.2')
    forest = forest.replace('**Theorem Q5.3', '**Theorem A2.3').replace('**Corollary Q5.4', '**Corollary A2.4')
    forest = forest.replace('(Q5.1)', '(A-F)')
    finite_interface = r'''
**Corollary A2.5 (rank and excess classify the finite search).** Let T be a
specified forest on d vertices and m edges, and let k≥0. Set

\[
 F_T=\langle x_i\mid x_i^2=1,\ [x_i,x_j]=1\text{ for nonedges}\rangle,
 \quad U_{T,k}=F_T/\gamma_{k+3}(F_T),\quad K=\gamma_3(U_{T,k}).
\]

The ordered IP markings with graph T and order \(2^{d+m+k}\) are exactly
the quotients \(U_{T,k}/N\), where N is normal, contained in K,
\([K:N]=2^k\), and the images
\((N(K\cap(U_{T,k})_J))/N\) have IP for every pair J,L.
Generator-set equivalence is exactly the action of Aut(T) on these kernels.

*Proof.* Killing any set of generators preserves every defining relator of
F_T. Collection in its class-two quotient gives at most d+m binary
coordinates, and (A-F) realizes all of them, so this quotient is precisely
the marked model Q_T. Every target has that same quotient by A2.3.
These are exactly U.FQ's hypotheses. Its all-parabolic condition and U.LAD
give the stated bijection and exhaustive search. An ordered isomorphism must
commute with the generating map, hence has the same kernel. A permutation
of the generator set preserves the noncommutation graph and extends to an
automorphism of F_T and U_{T,k}; this proves the last claim. ∎

This is used twice below: the order-256 seed has (d,k)=(3,3), while all
nondegenerate order-1024 markings have (d,k)=(3,5),(4,3),(5,1). Their actual
terminal counts require the complete computation in Appendix C. The parameter
theorem proves exhaustion and termination, not those output values.

## 3. The affine square seed

'''
    square = between('Let\n\\[\n a(x,y)=(-x,y)', '### An oriented square model')
    square = square.replace('Theorem S', 'U.PHI').replace('Lemma Q2.2', 'U.DEL')
    square = square.replace('Lemma Q3.1', 'Lemma A3.1').replace('(Q3.1)', '(A-S1)').replace('(Q3.2)', '(A-S2)')
    # The rank-two local injectivity is an actual U.SK obligation.
    square += r'''
The quotient \(q_n:H_n\to H_5\) fixes the three named generators.
Its kernel is \(\gamma_3(H_n)\). Every proper marked parabolic has
at most two generators, and its type is respectively 4,4 or2 both upstairs
and downstairs. Each is the identical dihedral or order-four group; singleton
and empty parabolics likewise embed. This verifies U.SK's full proper-support
condition, rather than merely checking three involutions.

## 4. Prescribed local sections from supported kernels

**Theorem A4.1 (edge inflation and exact orders).** Let B have Boolean
deletions and select pairs S={i,j} whose product orders q_S are even. For
m_S divisible by q_S, attach the marked dihedral map
\(D_{2m_S}\to B_S=D_{2q_S}\). The resulting supported fiber group
has IP, all deletions and

\[
 |H_J|=|B_J|\prod_{S\subseteq J}(m_S/q_S).
\]

Every selected pair has product order m_S and every unselected pair retains
its old order.

*Proof.* The dihedral quotient is injective on its proper parabolics, which
are trivial or a single reflection. U.SK applies and its antichain clause
identifies each selected local group. On an unselected pair every extra
coordinate is a reflection or one; a base pair of odd order cannot have a
single-reflection deletion. Thus the extra coordinates do not increase its
base product order. ∎

For d≥3, n≥5, k_i≥2 and \(\sum k_i\le n-1\), set
\(\delta=n-1-\sum k_i\) and
\(B=C_2^{d-3}\times H_{\delta+5}\), with the elementary factors first.
Its initial d−3 consecutive pair orders are2 and its final two are4.
Attach \(m_i=2^{k_i}\). The seed supplies all deletions, so A4.1 gives

\[
 |H|=2^{d-3+\delta+5}
       \prod_{i\le d-3}2^{k_i-1}
       \prod_{i>d-3}2^{k_i-2}=2^n.
\]

Distant markers commute in every coordinate, so the marking is string.
The geometric correspondence proves **[HFLa] Theorem1.2**. Taking d=3
proves **[HFLb] Theorem1.2**, including its stated n≥10 range, without
another construction. These existence results do not imply the classification
of §5.

**Theorem A4.2 (square kernels on a forest).** Let T be a forest and choose
distinct induced three-vertex paths S, with parameters n_S≥5. Attach
\(H_{n_S}\to H_5=(Q_T)_S\) to the model (A-F). Then

\[
 |H_J|=2^{|J|+|E(T[J])|+\sum_{S\subseteq J}(n_S-5)},\qquad
 \gamma_3(H)=\prod_S\gamma_3(H_{n_S}),\qquad H/\gamma_3(H)=Q_T.
 \tag{A-P}
\]

It has Boolean deletions and IP, and each selected triple is exactly H_n_S.

*Proof.* Deleting coordinates in (A-F) gives all base deletions and its
parabolic order \(2^{|J|+|E(T[J])|}\). Section3 verifies every
proper-support injection and the local γ3 kernel. U.SK, including its
antichain and lower-central clauses, gives every assertion. ∎

For the d-vertex path, take all consecutive triples with parameters
n_3,…,n_d. Equation (A-P) gives the exact group order
\(2^{\sum n_j-3(d-3)}\), all prescribed square sections and all FAP
cuts. To prove flatness when d≥4, let L={0,…,d−2} and
M={d−3,d−2,d−1}. Every support lies on one side. The vertex-and-edge
counts in (A-F), together with IP, give \(Q_T=(Q_T)_L(Q_T)_M\).
U.SK therefore gives H=H_LH_M. The stabilizer of the base (d−4)-face
contains H_M, while H_L is a facet stabilizer; taking inverses also gives
H=H_MH_L. The coset face criterion proves (d−4,d−1)-flatness and hence
flatness. The co-(−1)-face cut at d=3 is the tautological whole-polytope
cut; the other two cuts are genuine seed deletions. This proves all clauses
of **[CFHS25] Theorem5.1**.

### The universal presentation is a separate conclusion

Write G for the group H constructed in the path case above. The supported
fiber group is not an arbitrary amalgam. To prove the source's
universal-presentation claim, a further local normalization argument is needed.

'''
    universal = between('**Lemma Q8.1 (four-marker centralization).**', '## 15. Alternating assembly')
    universal = universal.replace('Lemma Q8.1', 'Lemma A4.3').replace('Lemma Q2.2', 'U.DEL')
    universal = universal.replace('§9', '§3').replace('(Q3.2)', '(A-S2)').replace('(Q8.3)', '(A-U)')
    universal = universal.replace('(Q8.2)', '(A-P)')
    universal = universal.replace('the same\nlocal-to-global centralization argument used for (A-P) makes', 'each edge commutator commutes with its endpoints and nearest outside markers,\nand with farther markers by string commutation. Thus')
    universal = universal.replace('Thus \\(Q/K\\)\nclass two.', 'Thus \\(Q/K\\) is\nclass two.')
    universal = universal.replace('The order comparison principle identifies', 'U.Order, applied to the finite normal factors and the displayed quotient bound, identifies')
    universal += r'''
This proves **[CFHS25] Theorem5.3**. No assertion about the order of the
universal group P_0 itself is required.

### Alternating assembly

We retain the following precise FAP case of Monson–Schulte's assembly theorem.
If regular (d−1)-polytopes P,Q have a common facet K and FAP retractions
\(\Gamma(P)=N_P\rtimes\Gamma(K)\) and
\(\Gamma(Q)=N_Q\rtimes\Gamma(K)\), the tail-triangle group
\((N_P\times N_Q)\rtimes\Gamma(K)\), with distinct final markers,
gives an alternating semiregular d-polytope with these facets. Its full
automorphism group is that group if P and Q are not isomorphic, and its
extension by branch-swapping C2 when P=Q; in that case the polytope is regular.
This is a retained geometric theorem, not a consequence of IP alone.

Apply A4.2 to the tree with common prefix and two final leaves, attaching the
two lists \((n_3,\ldots,n_{d-2},n_{d-1})\) and
\((n_3,\ldots,n_{d-2},m_{d-1})\). Write L,M for the facet label sets
and C=L∩M. The two deletions map H into \(H_L\times_{H_C}H_M\).
They are jointly injective: every vertex coordinate, edge coordinate and
supported kernel coordinate lies on one side and is detected there. Their
image is the full fiber product, since (A-P) gives its order
\(|H_L||H_M|/|H_C|\). Split deletions identify it with the exact
tail-triangle group in the retained theorem. For d=4 the common facet is a
square; otherwise it has list \((n_3,\ldots,n_{d-2})\). Its order is
\(2^{\sum_{j=3}^{d-2}n_j-3(d-5)}\), including8 for the empty list.
The two facet kernels have orders \(2^{n_{d-1}-3}\) and
\(2^{m_{d-1}-3}\). Thus the full automorphism order is

\[
 2^{\sum_{j=3}^{d-2}n_j+n_{d-1}+m_{d-1}-3(d-3)}
\]

when the final parameters differ, and twice that order when they agree.
Unequal parameters give unequal facet orders and rule out an interchange;
equal parameters give identical marked facets and their branch swap.
These are exactly **[CFHS25] Theorem6.1(a–b)**. No additional mixed
co-(d−4)-section is prescribed.

## 5. Bounded cyclic cores and the eight high-type families

The supported constructions solve existence. Completeness at the high
dihedral boundary needs a different local invariant, the cyclic core. Its
bounded quotient is nevertheless recognized by the same square model, and
its only finite seed is generated by the same U.FQ/U.LAD search as order1024.

'''
    cyclic = between('The retained **cyclic core theorem', '## 14. Prescribed square sections')
    cyclic = cyclic.replace('## 13. Completeness and exact presentation recognition','### Completeness and bare presentation recognition')
    cyclic = cyclic.replace('Theorem S','U.PHI').replace('§12','§5').replace('Lemma Q3.1','Lemma A3.1')
    cyclic = cyclic.replace('Theorems Q5.5–Q5.6', 'U.FQ and U.LAD, as specialized in A2.5')
    cyclic = cyclic.replace('Section 24.3', 'Section 7').replace('Appendix A', 'Appendix C')
    cyclic = cyclic.replace('Theorem Q6.1','Theorem A5.1').replace('Theorem Q7.1','Theorem A5.2')
    cyclic = cyclic.replace('**Theorem Q6.1','**Theorem A5.1').replace('**Theorem Q7.1','**Theorem A5.2')
    cyclic = cyclic.replace('(Q6.1)','(A-C1)').replace('(Q6.2)','(A-C2)').replace('(Q6.3)','(A-C3)').replace('(Q6.4)','(A-C4)')
    cyclic = cyclic.replace('The former SmallGroups identifiers and anchored multiplicities remain historical records in the unchanged predecessor, and are unnecessary for the relation implications used below.', 'No SmallGroups identifier or catalogue multiplicity enters these relation implications.')
    central = '\n## 6. Central descent and complete binary lifts\n\n'
    central += between('This branch concerns the principal nondegenerate classification', '### 24.3. One exhaustive computation')
    central = central.replace('§24.6','§7').replace('### 24.1.','### 6.1.').replace('### 24.2.','### 6.2.')
    central = central.replace('Theorem K(d)','U.Q').replace('K(d)','U.Q')
    central = central.replace('Appendix G','the defining-data appendix').replace('Appendix F','the presentation checker')
    census = '\n## 7. Exhaustive bounded classification and named objects\n\n'
    census += between('Apply Theorems Q5.5–Q5.6 to the path', '## 25. Source-by-source') if '## 25. Source-by-source' in old else between('Apply Theorems Q5.5–Q5.6 to the path', '## 25.')
    census = census.replace('Theorems Q5.5–Q5.6', 'A2.5 (U.FQ/U.LAD)').replace('Appendix A', 'the census program of Appendix C')
    census = census.replace('Appendix F', 'the presentation checker of Appendix C').replace('Appendix G', 'the complete defining-data artifact of Appendix C')
    census = census.replace('§13','§5').replace('§24.3','§7').replace('§24.6','§7.4')
    census = census.replace('### 24.4.', '### 7.2.').replace('### 24.5.', '### 7.3.').replace('### 24.6.', '### 7.4.')
    census = census.replace('§9','§3').replace('The §9','The §3')
    census = census.replace('All code and mathematical data are printed.', 'All code and mathematical data are included as complete external appendices with the bindings in Appendix C.')
    census = census.replace('| Terminal kernels | Ordered IP markings | Reversal-fixed | Classes | Direct IP meets |',
                            '| Kernels | IP | Fixed | Classes | Meets |')
    census = census.replace('The ladder sizes are respectively',
        'Here Kernels counts terminal normal subgroups, IP counts ordered markings satisfying every intersection test, Fixed counts reversal-fixed markings, and Meets counts actual subgroup-intersection checks. The ladder sizes are respectively')
    free = '\n## 8. Free extensions and two-primary torsion\n\n'
    free += between('For the infinite statements we retain', '**Lemma Q9.1 (torsion and amalgams).**')
    free += between('In each of the three free-extension identifications', '## 16. Corrections')
    free = free.replace('Lemma Q9.1','U.TOR').replace('and, when needed, its finite-extension clause','and, when needed, its finite-extension clause')
    corrections = '\n## 9. Source contracts, corrections and attribution\n\n'
    corrections += between('The F013 common-quotient theorem', 'Outside the declared main-result contract')
    corrections = corrections.replace('(Q5.1)','(A-F)').replace('(Q3.2)','(A-S2)').replace('§15','§8')
    corrections += r'''
The exact intake is the five specified editions in the references. The following
is the principal-result map; the companion ledger expands every normalized
statement, multipart clause and all33 [GLP18] numbered/table records.

| Source | Target contract | Derivation and actual U call |
|---|---|---|
| [HFLa], Theorem1.2 | Every admissible rank, order and sequence of 2-power adjacent orders | A4.1; square seed; U.SK with two-generator proper-parabolic checks |
| [HFLb], Theorem1.2 | Rank-three existence in the stated n≥10 range | d=3 specialization of A4.1 |
| [HFLb], Theorem1.3 | All2+2+4 high-type families; completeness, bare orders/IP and marking distinction | §5; A3.1; cyclic-core input; A2.5/U.FQ/U.LAD seed and exact relation checks |
| [HS26], Theorems1.1–1.2 | Canonical marked quotient and geometric cover for every finite nondegenerate rank | A2.1–A2.4; U.PHI; retained cover correspondence |
| [CFHS25], Theorem5.1(a–d) | Exact prescribed sections/order, flatness and all required FAP cuts | A4.2 path binding; U.SK antichain, γ3, separator and deletion clauses |
| [CFHS25], Theorem5.3 | Exact quotient of the universal local presentation | A4.3 normalization, actual local embeddings and finite order bound |
| [CFHS25], Theorem6.1(a–b) | Alternating semiregular assembly and exact full automorphism order | A4.2 fork binding; two-deletion fiber isomorphism; retained assembly theorem |
| [CFHS25], Theorems7.1–7.3 | Regular, chiral and alternating free extensions, including infinite input | §8; all geometric embeddings/properness checked; U.TOR |
| [GLP18], §§2–3/Table1 | Marked quotient criteria, central descent and all binary lift patterns | §6; U.Q/U.PHI; explicit center-in-product argument |
| [GLP18], Example3.9/Tables2–4 | Every stated raw presentation and intended named target; diagnosed literal discrepancies | §7.2; complete coset tables and generator-preserving isomorphisms |
| [GLP18], Examples4.3–4.5 | Exact universals and their order1024 smooth quotients | §7.3; complete raw presentation orders/IP and all central involutions |
| [GLP18], Lemmas5.1–5.4/Theorem5.5 | Lattice centers, retained infinite decomposition, kernel location and exactly two exceptional targets | §7.4; A3.1 affine model; U.PHI; exact census and presentations |
| [GLP18], Tables5–6 | All125 rank3,105 rank4 and8 rank5 reversal classes; all107 facet rows and universal orders | A2.5/U.FQ/U.LAD plus all-parabolic census and exact named-object recognition |

The [HS26] auxiliary kernel assertions are corrected above; its two principal
existence conclusions remain recovered. The [CFHS25] diagonal-translation and
chiral-facet proof steps use the corrected arguments stated here. In [GLP18],
Corollary3.7 stops at order8, Table4's literal rows remain distinguished from
their repaired targets, and reversed facet markings in Table6 are explicit.
The retained inputs are part of the contract, not silently counted as newly
proved results. No open question, historical novelty claim, unnumbered small-n
classification or separate census of degenerate products is included. The
power-polytope recollections in [CFHS25] are not extra source targets.

This scientific organization and the supported-kernel applications are repository
work, with the support-inclusion simplification credited to independent reviewer
122. The source authors receive credit for the original results and
constructions. The classical ingredients of U and the new assembly carry no
historical-priority claim. Removing one declared U dependency only invalidates
the recorded derivation; it does not show that the conclusion has no other proof.

## Appendix C. Complete computational proof interface

There are four complete external artifacts, all part of this volume's proof
cost: `phase78_n009_integration_census.g`,
`phase78_n009_integration_finite.g`,
`phase78_n009_integration_data.g` and
`phase78_n009_integration_run.py`. Their legacy filenames identify established
reusable artifacts; no surrounding manuscript is imported by those filenames.
The first three contain every executed mathematical instruction and all72 named
Atlas presentations,107 Table6 rows and source relators. The fourth is the
complete no-clobber orchestration and output checker. Source editions and
artifacts are hash-bound in the companion ledger before independent review.

The exact algorithms assumed are GAP's finite permutation/pc group arithmetic,
subgroup intersection and complete Todd–Coxeter enumeration, and NQ's universal
nilpotent quotient algorithm. A completed coset table at the trivial subgroup
establishes the raw presentation order; a finite image alone would not suffice.
No source count is used to prune candidate generation, and no saved certificate,
private primary file, permutation-array atlas or SmallGroups catalogue is read.

For every (d,k), the census constructs U_(T,k) from its original marked
nilpotent quotient map, transports those same generators, and enumerates every
U-normal index-two hyperplane preimage k times. Only equal subgroups are
deduplicated. Its binary subgroup key is used only after checking that every
ambient relative pc order is two. A2.5 supplies completeness. Every terminal
candidate is subjected both to the kernel-profile test and to all4^d actual
marked subgroup meets, including rejected candidates. Reversal is computed on
the markings; the observed fixed count and the two-element orbit formula give
the generator-set classes. The order256 seed evaluates the four distinct word
patterns on each oriented type-{4,8} marking, so its use in §5 is an explicit
finite implication with no hidden classification assumption.

The presentation checker constructs all raw groups from complete relators,
finishes the trivial-subgroup coset table, evaluates all defining relations,
checks generation, exact involution/product orders and all subset intersections.
It verifies each facet name by an actual generator-preserving isomorphism.
Dual names are computed using reversed generators. It enumerates all central
involutions in the order2048 example and checks every quotient. For each finite
Table6 row it combines both complete facet presentations and distant-end
commutation, proves the raw universal order and verifies both facet embeddings.
The one infinite row invokes the precisely stated retained decomposition; it
is never sent to an unbounded finite-order computation.

The complete run requires539264 census meets,214 raw presentations and43840
additional meets,428 exact facet identifications and all107 Table6 rows. These
are expected results checked after exhaustive generation, not assumptions
proving it. Successful replay establishes the finite conditional obligations,
not a Lean formalization or a substitute for the parameter proofs.

From the research directory's parent, run:

```sh
python3 -B -O research/leemans/phase78_n009_integration_run.py --output-dir /private/tmp/NEW-two-group-certificate
```

The output path must not exist. The artifact manifest records source/program
hashes, installed versions, complete logs and all generated mathematical data.
The application ledger charges the four source files in full, plus the actual
U dependency closure and all written hypotheses in A. Rendered mathematical
pages, certificate bytes and any cumulative multi-volume accounting will be
reported separately after complete review; the supported-kernel acquisition
cost is not waived because it has several users.

## References and source-version boundary

'''
    refs = between('[HFLa]', '### Operations and covers')
    refs += '\n'+old[old.index('[GLP18] Y.'):]
    refs = refs.replace('§24','§7').replace('Appendix G','the complete defining-data artifact').replace('Existing software/background inputs for the other branches are unchanged.', '')
    refs += r'''

The retained cyclic-core result is Lucchini's theorem in the form recorded by
Isaacs, *Finite Group Theory*, Theorem2.20. The retained alternating assembly
is Monson–Schulte, *The assembly problem for alternating semiregular polytopes*
(2020), Theorem5.3 in its FAP case. The chiral free-extension theorem is
Schulte–Weiss, *Free extensions of chiral polytopes* (1995); the universal
alternating construction is Monson–Schulte (2012,2021), in the exact forms
stated in §8. These prior proofs are retained rather than included as additional
compressed sources. The regular-polytope and marked-cover correspondences are
the standard McMullen–Schulte framework, with the scopes stated in §1.
'''
    out = ''.join([front, forest, finite_interface, square, universal, cyclic, central, census, free, corrections, refs])
    # Give equations stable identifiers matching the new exposition's calls.
    for old_tag, new_tag in {'Q5.1':'A-F','Q3.1':'A-S1','Q3.2':'A-S2','Q8.3':'A-U',
                             'Q6.1':'A-C1','Q6.2':'A-C2','Q6.3':'A-C3','Q6.4':'A-C4',
                             'Q10.1':'A-X1','Q10.2':'A-X2'}.items():
        out = out.replace('\\tag{'+old_tag+'}', '\\tag{'+new_tag+'}')
        out = out.replace('('+old_tag+')','('+new_tag+')')
    for a,b in [('and8','and 8'),('order1024','order 1024'),('order256','order 256'),
                ('order2048','order 2048'),('all33','all 33'),('all72','all 72'),
                ('all107','all 107'),('all4^d','all 4^d'),('all2+2+4','all 2+2+4'),
                ('All2+2+4','All 2+2+4'),('All125','All 125'),('rank3','rank 3'),
                ('rank4','rank 4'),('rank5','rank 5'),('rank2','rank 2'),
                ('two-group-certificate','two-group-certificate'),
                ('requires539264','requires 539264'),('and43840','and 43840'),
                ('are2','are 2'),('are4','are 4'),('including8','including 8'),
                ('. the census program','. The census program')]:
        out = out.replace(a,b)
    import re
    out = re.sub(r'\b(Theorem|Theorems|Lemma|Lemmas|Corollary|Example|Examples|Table|Tables)(\d)',r'\1 \2',out)
    out = out.replace('Appendix C evaluates every displayed word', 'The census program in Appendix C evaluates every displayed word')
    out = out.replace('all printed in the defining-data appendix', 'all included in the defining-data appendix')
    for a,b in [('U.FQ/LAD','U.Nilpotent/U.Ladder'),('U.FQ','U.Nilpotent'),
                ('U.LAD','U.Ladder'),('U.PHI','U.Phi'),('U.DEL','U.D'),('U.TOR','U.Amalgam')]:
        out=out.replace(a,b)
    # These are mathematical variables, not literal underscored prose. Keep
    # existing math/code untouched and typeset the new exposition normally.
    protected=re.compile(r'```[^\n]*\n.*?\n```|`[^`\n]+`|\\\[.*?\\\]|\\\(.*?\\\)',re.S)
    def prose_math(s):
        special={'U_(T,k)':r'\(U_{T,k}\)','U_{T,k}':r'\(U_{T,k}\)','H_n_S':r'\(H_{n_S}\)',
                 'H=H_LH_M':r'\(H=H_LH_M\)','H=H_MH_L':r'\(H=H_MH_L\)'}
        s=re.sub(r'(?<=\})\*(?=\d)',r'\\*',s)
        # Normalize literal exponent/index notation inherited from the prose
        # proofs, without changing words or mathematical expressions.
        def power(m):
            base=m.group(1); exponent=m.group(2) or m.group(3)
            exponent=exponent.replace('−','-').replace('ε','\\epsilon ').replace('ᵢ','_i')
            exponent=re.sub('[₀₁₂₃₄₅₆₇₈₉]',lambda x:'_'+str('₀₁₂₃₄₅₆₇₈₉'.index(x.group())),exponent)
            return r'\('+base+'^{'+exponent+r'}\)'
        s=re.sub(r'(\([a-zA-Z]+\)|\b[0-9a-zA-Z]+)\^(?:\(([^()\n]+)\)|([0-9a-zA-Z]+))',power,s)
        s=re.sub(r'(?<![A-Za-z_\\])(?:[qmn]_S|Q_T|F_T|H_[LM]|n_[3d])\b',
                 lambda m:r'\('+m.group()+r'\)',s)
        return re.sub('|'.join(re.escape(x) for x in special),lambda m:special[m.group()],s)
    chunks=[];cursor=0
    for m in protected.finditer(out):
        chunks += [prose_math(out[cursor:m.start()]),m.group()];cursor=m.end()
    chunks.append(prose_math(out[cursor:]));out=''.join(chunks)
    args.output.write_text(out)
    print(f'Author draft: {len(out.encode())} UTF-8 bytes; {len(out.split())} plain whitespace tokens (not rendered measurement)')


if __name__ == '__main__':
    main()
