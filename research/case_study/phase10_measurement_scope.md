# Phase ten: matched tree-proof measurement scope

10 October 2026. Private source and dependency audit. **The tree-cut theory
supports a genuine cross-paper target, but no cross-paper numerical ratio is
yet justified.** The complete 2002 author manuscript is available. The 1998
source has been read through indexed author-uploaded text in earlier reviews,
but a complete stable extraction of its proof has not been recovered for this
measurement. Its missing spans must not be estimated from the article's page
count or replaced by snippets.

The accounting follows [MEASUREMENT](../../MEASUREMENT.md)
and the [L066 protocol](phase9_L066_measurement_protocol.json): match exact
statements, count each shared argument once, declare retained background,
and keep mathematical proof, finite code and formal certificates separate.
This note does not alter any frozen phase-nine result.

## 1. Exact candidate statements

The main candidate is Buekenhout–Cara, *Some properties of inductively minimal
geometries*, Bulletin of the Belgian Mathematical Society–Simon Stevin 5
(1998), 213–219, DOI [10.36045/bbms/1103409005](https://doi.org/10.36045/bbms/1103409005),
network ID **N001**. Its complete four-part Theorem 1 is mathematically
rederived in [phase5_tree_cuts.md](phase5_tree_cuts.md), with the retained
1997 classification explicit. The exact four targets are:

| ID | Target, for an inductively minimal pair with connected diagram |
|---|---|
| N001.1 | RWPRI, rank-one local two-transitivity, and geometric rank-two intersection property |
| N001.2 | PRI when the rank is even |
| N001.3 | Failure of PRI exactly when the diagram has a middle; in that case QPRI |
| N001.4 | RPRI exactly when the diagram is complete |

Here QPRI means a unique subgroup chain between a type stabilizer and the
whole group. A diagram middle is a cut vertex whose deletion has components
of equal size. The geometric rank-two intersection property is not the
subgroup intersection identity of a C-group. These definitions must be
fixed with the target statements, rather than changed to easier properties.

A suitable second paper is Cameron–Cara, *Independent generating sets and
geometries for symmetric groups* (2002), network ID **N003**. The complete
[twelve-page author manuscript](https://maths.qmul.ac.uk/~pjc/preprints/igsgsn.pdf)
is available privately. The exact eligible additions are components, not the
paper's whole classification:

| ID | Exact selected component | Source location |
|---|---|---|
| N003.T | The edge transpositions of a tree form an independent generating set of the symmetric group | Theorem 2.1, converse, case (a), printed p.4 |
| N003.I | Their generated subgroups have the full subset intersection property | Corollary 2.3, case (a), printed pp.6–7 |
| N003.G | Their standard coset system is a firm, residually connected, flag-transitive, RWPRI geometry | Theorem 3.2, converse, case (a), printed pp.9–10, with the general coset criterion on pp.7–8 |

For literal matching use the manuscript's stated range n≥7, even though the
replacement tree construction works in smaller degrees too. The tree-line-
graph observation on p.11 is an explicitly known additional consequence;
it is not a separate long source proof that can inflate the numerator.

Excluded are Theorem 2.1's classification of all maximum independent sets,
its twisted-generator case (b), Corollary 2.3 for that case, the forward
classification direction of Theorem 3.2, all relative-generator bounds, and
the full maximum-rank coset-geometry classification. The source retains
Whiston's theorem and classification input for those excluded directions.
No source text proving them belongs in this numerator.

## 2. What has actually been recovered

The N003 PDF has twelve readable manuscript pages, beginning with the title
and ending with references. Its SHA-256 is
`43f3f2b1cbb7dacc55f12572ef78a5bb574bcfe745aba6cc0c10291256e611a2`.
Re-extracting it with pypdf 6.13.0, using exactly the phase-nine recipe
(newline, `--- PDF PAGE i ---`, newline, default page text, newline), gives
22,210 Unicode codepoints with SHA-256
`165ef2f20f7b5b3f04021205e002e0f22d2249b035bbc480de10f21986d14310`.
The private extraction is `sources/phase10_N003_extracted.txt`; it is not an
exportable original research artifact.

All N003 pages, including the surrounding classification proof, have been
read to determine the dependencies and excluded branches. The current source
span anchors are:

| Candidate span | Exact extraction locator | Accounting decision |
|---|---|---|
| Tree generation and irredundancy | Codepoint 4810, opening proof of Theorem 2.1; tree claims occur in its first two paragraphs | Mixed sentences also discuss case (b); separate tree clauses or count the entire mixed paragraphs only as an explicit sensitivity variant |
| Forest products and intersection | Corollary 2.3 at 10229; tree proof ends immediately before `Now suppose that case (b)` at 11279 | Includes only the tree proof, not the corollary's full all-case claim |
| General coset criterion | Beginning of §3 at 13390 through the definition of RWPRI | Declare as common background on both sides, or include a self-contained bridge on both sides; never free on just one side |
| Tree coset proof | Tree/converse introduction at 17188, through the case-(a) RWPRI paragraph, ending before `Now let S*` at 18991 | Includes the G1/G2 bridge as well as BH/Helly and RWPRI; exclude the twisted case |

The exact anchor hashes are saved in [phase10_tree_source_scope.json](phase10_tree_source_scope.json).
These are a dependency-audit map, **not yet a frozen counting protocol**.
The final protocol must choose exact half-open boundaries and per-span hashes,
exclude target statements symmetrically, and reject overlapping intervals.
The important source-specific point is that the p.9 assertion that G1/G2
hold uses the strong-independence result already selected from Corollary 2.3;
that result is charged only once. The p.10 BH proof similarly reuses the
forest-product/intersection description.

For N001, the current
[author-uploaded record](https://www.researchgate.net/publication/29655192_Some_properties_of_inductively_minimal_geometries)
exposes the definitions, foundational lemma, Theorem 1, and much of its
proof through search indexing. The available extraction jumps from the
introduction of the disconnected-residue argument to the end of the
maximality argument: central printed-p.217 text, including Lemma 5's full
argument, is absent. The final p.218 argument is also cut in the present
returned record. Earlier mathematical review of indexed text is not a
reproducible complete byte-level source for this measurement.

Fresh retrieval attempts used the publisher's current PDF URL and legacy
`download/pdf_1/euclid.bbms/1103409005` URL. Both returned HTML, not a PDF.
The official
[VUB bibliographic record](https://researchportal.vub.be/en/publications/some-properties-of-inductively-minimal-geometries/)
was retrieved successfully, but supplies metadata rather than an attached
full text. The private response files are named `phase10_N001_*.response`;
they are deliberately not labeled PDFs. No access limitation is converted
into a numerical source length. The five-page N002 counting paper remains
another possible future target, but an indexed citation/abstract and a
failed CiteSeer retrieval do not make its full proof measurable.

## 3. Shared replacement theory that must be charged

The proof should be written as one shared core and small adapters. It must
not count a generic group-torsor encoding as though that supplied the tree
geometry theorem. The actual reusable mathematics is:

1. **Forest subgroups and intersections.** For a tree T on Ω and an edge
   subset I, the corresponding transpositions generate the product of the
   symmetric groups on the components of (Ω,I). Unique paths imply that
   intersecting two component partitions gives the partition for I∩J.
2. **Laminar cuts and flag completion.** Root the tree and orient each edge
   cut away from the root. Cosets of the cut stabilizer are subsets of the
   same size. Pairwise incidence forces the same nesting/disjointness
   relations. The atoms obtained by subtracting maximal selected children
   have matching cardinalities, so one permutation realizes every flag.
3. **Residues and diagram.** A residue is a join of geometries for the
   nontrivial forest components. Panels have two elements; adjacent tree
   edges give a hexagon and disjoint edges a digon. The diagram is the line
   graph L(T), and a connected m-edge residue has group Sym(m+1).
4. **Two-block subgroup test.** A stabilizer Sym(A)×Sym(Ω\A) is maximal
   when the two block sizes differ. If equal and at least two, its only
   proper overgroup is the unordered two-block stabilizer. A cross-block
   transposition proves these claims; N=2 must be handled separately.
5. **Diagram-to-tree reconstruction.** Build a vertex for each maximal
   clique of an allowed diagram, an edge for a diagram vertex in two
   cliques, and a leaf edge for one in a single clique. The diagram's
   clique/cycle conditions make this a tree; its line graph is the
   original diagram. Treat rank one separately.

Items 1–3 deliver N003's selected tree results. Items 4–5, with the retained
1997 classification, extend the same core to *all* N001 inductively minimal
pairs. They must be charged as proofs or explicitly retained as common background
(the two-block option is specified below). A shorter
replacement that simply cites the established tree correspondence would
be measuring a different conditional theorem and must be reported as such.

The N001 adapters are then short but nonempty: a leaf cut in each forest
factor proves RWPRI; odd |Ω| excludes equal cuts; an equal cut is exactly a
diagram middle; and every nonstar tree contains a three-edge path with a
nonprimitive 2+2 cut, whereas every subtree of a star has only leaf cuts.
One must still explicitly connect these tests to the source's definitions,
including disconnected residues and the rank-one exception.

## 4. Retained inputs and fair alternatives

The principal unexpanded input is Buekenhout–Cara–Dehon (1997), as restated
in N001 Lemma 1: the permitted diagrams have the specified clique and cycle
conditions and determine a unique inductively minimal pair. This is a
classification theorem. It is not proved by the finite tree checker and
cannot be silently discarded from the denominator. A combined ratio must
therefore be labeled conditional on this explicit common background.

The replacement does **not** need Whiston's maximum-size classification,
the twisted-generator classification, or a classification of all maximal
subgroups of symmetric groups for the selected tree components. The source
N001 cites maximal-subgroup literature at the two-block step. An honest
protocol has two options:

* Retain the exact two-block maximality statement in the common background
  on both sides, and exclude its expansion from both measured proofs.
* Include the elementary two-block proof in the replacement and retain the
  source's cited implication as an explicitly unexpanded source dependency.
  Report that asymmetry and do not describe the resulting ratio as an
  expanded-dependency comparison.

The first is the clean primary conditional protocol; the second is a useful
conservative replacement-length sensitivity, since it charges extra proof
on the replacement side. Neither justifies using the page count of the
cited classification literature as an estimated numerator.

Likewise, the general coset-geometry criterion can be shared background, or
it can be proved once in each matched bundle. Its elementary proof in terms
of Helly and residue generation is already available in this project, but
including its bytes only on the source side would create artificial reuse.

## 5. Measurement sequence and present conclusion

First freeze the N003-only tree target and a self-contained replacement
core, then rerun the exact extraction/count protocol. This is measurable
now, although it measures selected components of principal statements,
not a whole principal theorem of the 2002 paper. There is no reason to
assume its compression ratio exceeds one: the source tree proofs are
already short, and the laminar argument may cost as much as its BH proof.

If complete N001 text is recovered, add its four targets and the required
reconstruction/maximality adapters. Report both orders of marginal addition:
N003 first (then pay reconstruction and the four property tests), and N001
first (then N003 may be an almost free consequence of the already charged
core). This reveals actual reuse without changing the combined ratio.
Source repetitions that occur in different papers are separate published
arguments; any identical imported lemma that is counted once as common
background must be handled the same way on the replacement side.

The phase-five finite tree tests and formal lemmas are useful validation,
but the all-size results are proved in the written arguments. They do not
supply an absent source proof and do not enter a written-proof length
unless a separate, explicitly comparable certificate metric is defined.

**Current status:** exact matched mathematical targets and the cross-paper
dependency graph are identified; N003 source extraction is reproducible;
N001's complete source numerator is unavailable; no phase-ten ratio is
assigned by this scope audit. The strongest immediate deliverable is a
narrow N003 component measurement, while the full four-part 1998 target
remains ready mathematically but pending complete source access.
