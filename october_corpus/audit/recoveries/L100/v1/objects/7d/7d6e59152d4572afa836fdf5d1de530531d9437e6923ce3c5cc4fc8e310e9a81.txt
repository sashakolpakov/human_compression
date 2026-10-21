# Independent review of the finite normal-pair representation manuscript

10 October 2026. Author package: `phase177_export.json`, SHA256 `c1032decb72e86aa9f5d56189937b043a6bdbb3478e6de4ec6935463572fb9c9`.

**Verdict: accept the complete written principal-theorem contract for F010, with the three explicit local source qualifications preserved.** The written proofs recover Theorems 3.1, 4.1, 4.2 and A. They also recover the full recursive symmetric-group family, with its base-case qualification, and the intended obstruction of the hexagon example, with its type-preserving group corrected. This is not a claim that every printed statement is true unchanged. In particular, the incorrect completed-hexagon kernel is not admitted as a corollary.

The source is Antonio Díaz Ramos, Rémi Molinier and Antonio Viruel, *Every finite group is represented by a finite incidence geometry*, arXiv:2511.02410v2, 16 December 2025. Its thirteen-page primary PDF has SHA256 `a8ff604a96a57ab8baf20aaa808a90308c01237ab0607a1062207fcb49f736e7`. This is the named 2025 resolution source, inventory F010. The representation theorem and the three gadgets belong to those authors. It is not a newly solved conjecture, and F010 must not silently become a paper from the original L-series intake.

## 1. Review scope and exact theorem

I read the complete primary text, including definitions, all proofs, examples and references; independently inspected the figures on physical pages 5,7,9,10,11,12; and read the entire replacement manuscript `phase177_finite_pair_representation.md`, its contract, scope document and associated certificate sources. All author-export and retained-input bindings were checked before and after the fresh verification. No author file was changed.

The theorem concerns a **normal** subgroup H of a finite group G and an incidence geometry of unrestricted finite rank. Its correlation group consists of graph automorphisms that permute the colour classes; its type-preserving group is the kernel of that palette action. In general a graph automorphism need not be a correlation. The replacement states this distinction correctly.

Normality is necessary, and G/H must embed in the symmetric group on the palette. In rank two its order is at most two. Thus neither arbitrary nonnormal pairs nor arbitrary quotient groups at fixed rank two are being represented. The actual construction for nontrivial G has rank [G:H]+3: the coset colours and three fixed auxiliary colours. Its type action is the regular quotient action on the coset palette. For G=1 the source and replacement use the one-vertex rank-one geometry.

Although Theorem A does not require connectedness in its statement, the constructed graph is connected. Any two original group vertices are joined through their ordered-pair gadget, and all new gadget vertices are attached to those vertices. Chamber completion retains every original edge and attaches each new vertex to its edge chamber, so it preserves connectedness. The trivial one-vertex case is connected as well.

The cleaning theorem, by contrast, begins with an arbitrary nonempty finite properly coloured graph. Its operation preserves the connected-component decomposition rather than joining components: each old edge is replaced by a path through its gadget root, and the other gadgets attach to one old vertex. It therefore does not claim connected output from disconnected input. The recursive symmetric-group examples are connected by their separate inductive construction.

## 2. Restriction and extension

R.Reconstruction is a correct elementary pair-isomorphism criterion. Intrinsic recognition of the retained vertices makes restriction a well-defined homomorphism into the old correlation group. Pointwise rigidity gives injectivity. Explicit extension gives surjectivity and, combined with injectivity, uniqueness and multiplicative compatibility. Its final hypothesis identifies the type-preserving kernels. The manuscript verifies each of these obligations in the applications.

The criterion is fully proved in the manuscript. Its description as an instance of the umbrella action interface is appropriate, but no unproved source theorem is smuggled in through that description. In particular, group action on a gadget is not mistaken for an argument excluding further automorphisms.

## 3. Ordered-pair encoding

The six types of edges in (R1) agree with the primary arrow diagram on p.5. The label k is at least two, so the long chain has at least four edges. Original vertices have degree 4(|G|−1), which is at least four, while all gadget vertices have degree two or three. This recognizes the old vertex set even when |G|=2.

The degree-two neighbours of an old vertex Px are exactly its outgoing T-vertices. Among these, the one at distance two from a specified different old vertex Py is uniquely Txy: the second neighbour of Txz is the terminal chain vertex attached to Pz. The degree-three neighbour of Txy then identifies that terminal vertex. Its chain ending at a degree-three vertex is distinct from the route through Txy ending at a vertex of degree at least four. The chain length recovers k. Thus an uncoloured graph automorphism preserves both the direction and the full label of every ordered pair and fixes all internal vertices once it fixes the old vertices.

The label equation forces a right translation by evaluating the pair with first entry 1. The replacement uses the inverse in the translation parameter to obtain a homomorphism for the usual composition convention. This removes a possible left/right convention ambiguity without changing the graph construction. Normality of H is used precisely to make these translations permute all coset colour classes; their colour kernel is H.

The minimum-degree, triangle-free and vertex-count arguments are correct. Distinct gadgets meet only at old vertices and there are no old-old edges, so no triangle can cross gadgets. The count of k+4 internal vertices for each ordered pair gives exactly the stated cubic polynomial.

## 4. Chamber completion and cleaning

For chamber completion, each new vertex has its entire neighbourhood inside its assigned edge chamber. Hence any clique containing a new vertex lies there. Triangle-freeness ensures that a clique containing only old vertices has at most two members; positive degree extends singleton cliques, and the graph contains an edge for the empty clique. These observations prove the geometry axiom for all flags, not just edges.

The actual degrees are r−1 for new vertices and d(v)(r−1) for old ones. The minimum-degree hypothesis makes their distinction strict. Old colours are still all represented, so a correlation fixing the old vertices fixes the palette and every new vertex, which is determined by its endpoint pair and colour. The stated extension formula preserves every chamber and identifies the kernels. The case r=2, where nothing is added, is included. The source's p.7 degree bounds are off by one; the replacement corrects them and preserves the required strict inequality.

For cleaning, the two new colour classes have different sizes, each larger than every old colour class. Therefore a correlation fixes them separately and recognizes the old vertices. Two old vertices were adjacent exactly when they share a new neighbour. Deleting the old vertices yields the separate gadgets; their one- or two-vertex old boundaries identify the gadget copies pointwise once the old vertices are fixed.

The rooted-gadget rigidity proof is valid, including M=1. In an isolated-vertex gadget the two attachment vertices have different degrees in the complete graph, so the root is fixed. Along the gadget chain, the first branch has successors of induced-gadget degrees three and two; the next branch has successors of degrees two and three. This determines the remaining vertices. The use of induced-gadget degrees at these branches is essential in the M=1 isolated-vertex case, and the manuscript states it. The normal subgroup information survives because the two added colours are fixed, while the old palette action is unchanged.

All new edges are between opposite gadget parities or between old and new palettes. The isolated attachment joins an old vertex to gadget indices 0 and 2, which are not adjacent. This proves triangle-freeness. The degree calculation includes old isolated vertices and leaves, so the conversion applies to every nonempty finite incidence system, not just connected graphs without isolated elements.

The main finite normal-pair theorem follows directly from ordered-pair encoding followed by chamber completion, with the trivial group handled separately. Cleaning supplies the independent stronger conversion theorem for arbitrary initial systems.

## 5. The recursive symmetric-group family

The written induction proves the actual recursive construction and size formulas, rather than invoking the main existence theorem in place of the smaller example. In the base path the reversal exchanges only colours 0 and 1; its endpoints have degree one. The claimed minimum degree is therefore correctly restricted to n≥3.

The even choices of representatives gj make the local permutations gj'−1 σ gj all have the sign of σ. Thus every local map has the same palette action, the maps agree on shared pair vertices, and their composition law gives the asserted global Sn action. Its kernel on colours is An. This proves the existence of every correlation required by the theorem, including odd permutations, without relying on a picture.

The exclusion of extra correlations is also complete. For n≥4 the top colour class is uniquely smallest. For n=3 it is distinguished by the degree patterns of its neighbours. Once the top vertices are fixed, their two-element neighbour sets distinguish every pair vertex. Removing both layers leaves the interiors of the attached copies, each connected because deleting the top layer from the preceding graph leaves a connected graph. Each interior has a different boundary star in the fixed pair-vertex layer. Hence every copy is preserved, and inductive faithfulness fixes its entire interior. This supplies the component-recognition step needed before applying the induction inside a copy.

The class-size recurrences, triangle-free argument and minimum-degree induction all check. The four-vertex base path must first be cleaned before the general completion theorem can be applied; the manuscript explicitly gives that alternative. No claimed n=2 geometry is inferred by applying the minimum-degree theorem outside its hypotheses.

## 6. The completed hexagon and exact principal coverage

The primary figure on p.10 has alternating tips on three edges initially and tips on all six edges after the depicted completion. Initially the permitted dihedral symmetries form S3 with type kernel C3. After completion the whole dihedral group of order twelve acts; its parity-preserving subgroup consists of three rotations and three reflections and is S3. The explicit reflection in (R4) preserves colours and has order two, so the printed completed kernel C3 cannot be correct.

This changes the example's second group, not its intended demonstration that naive completion can enlarge the correlation group. The example does not establish the source's informal assertion that every hypothesis is optimal in every possible formulation. The replacement correctly avoids that stronger inference.

| Primary result | Accepted scope |
|---|---|
| Theorem 3.1 | Complete written ordered-pair construction and exact normal pair |
| Theorem 4.1 | Complete written chamber completion; degree formula corrected in its proof |
| Theorem 4.2 | Complete written cleaning operation, including isolated and singleton inputs |
| Theorem A | Complete written deduction for every finite normal pair, including G=1 |
| Example 5.1 | Intended obstruction recovered; completed pair corrected to (D12,S3) |
| Example 5.2 | Full recursive family and colour sizes; minimum degree asserted from n=3 |

The four named theorems are recovered without changing their mathematical conclusions. The local example corrections must remain visible in any whole-source intake statement. This supports one F010 principal-theorem intake, subject to root admission, but not an assertion that all literal assertions in the paper follow unchanged.

## 7. Independent finite and formal verification

The fresh reviewer program implements all three constructions independently from the stated edge lists. It checks every properly coloured graph on at most three labelled vertices, up to relabelling the colour names: 25 cases. Cleaning followed by chamber completion preserves both groups under the actual restriction maps in every case. This includes isolated vertices, leaves, a triangle and multiple connected components.

The ordered-pair encoder is checked for every normal subgroup of C2, C3 and S3: seven pairs. Besides graph counts, connectivity, minimum degree and triangle-freeness, the full uncoloured automorphism group is computed. Restricting correlations and their type-preserving kernels to the original group vertices gives exactly the prescribed right-regular groups. Chamber completion is additionally checked for the four C2/C3 pairs. It is not claimed computationally checked for the S3 pairs. The general completion theorem rests on the written proof; a slower exploratory larger completion computation is not part of the accepted replay.

The recursive family is independently constructed for n=2,3,4,5. Its vertex counts are 4,12,46,225; its colour counts, exact Sn/An top actions, connectivity and triangle-freeness agree with the universal proof. These finite cases provide diagnostics and do not substitute for the induction.

The author's hexagon computation was freshly rerun and its local Lean source freshly compiled. Their accepted logs are byte-identical to the author evidence. Lean verifies an explicit adjacency- and colour-preserving nonidentity involution and the impossibility of a nontrivial involution in C3. It does not count the entire graph group or formalize the universal constructions. The full two finite group orders are checked by GAP/GRAPE.

Four meaningful controls reject: deleting the asymmetric cleaning-tail chord; collapsing the arrow labels, with only the vertex-count expectation bypassed so that rejection tests actual rigidity; imposing the incorrect printed completed-hexagon kernel; and using the wrong image of the tips in the Lean reflection. GAP error exit codes alone are not treated as evidence; the driver requires the rejection message and absence of the positive completion marker.

The verification uses pinned Lean 4.32.2 and records all pinned dependency revisions and tracked-source cleanliness. Cached library objects remain trusted. GAP/GRAPE supply exact finite graph and group algorithms. The mathematical universal proofs are independently reviewed written arguments, not end-to-end Lean certificates. No L059 census was rerun or newly admitted by this review.

## 8. Attribution and accounting

The finite normal-pair theorem, explicit gadgets and symmetric-family construction are borrowed from Díaz Ramos–Molinier–Viruel. Their source credits the earlier graph-representation tradition of Frucht and König. The new manuscript organizes the proofs through a single explicit restriction-extension criterion, pays for the component-boundary recognition, and records the three local source qualifications. It makes no historical-priority claim for that elementary criterion or for a correction.

The self-contained written mathematical application is 21,870 UTF-8 bytes. Its local completed-hexagon evidence additionally uses the 1,239-byte GAP source and 2,390-byte Lean source. The actual driver, independent bounded programs, replay records and review evidence are itemized separately in the review cost ledger. Retained library infrastructure is an explicit trust dependency. The manuscript's proof of R.Reconstruction is complete, so a reference to the umbrella interface is not an uncharged theorem needed to make the argument work.

No matched compression ratio is computed. The source's thirteen pages and the manuscript's bytes are different units and do not by themselves define one. This intake adds no newly solved open conjecture: it reconstructs a theorem already proved by the source authors in 2025. Broader source-count changes and public admission remain root decisions, with the F010 provenance and local-correction flags preserved.
