# Independent review of the corrected L092 principal-result packet

Phase199, 2026-10-10. Reviewed author freeze: `phase186_export.json`, SHA-256 `cbbb953e5565ef1dd36286fe245c12c81fd1f854be5d887a544361055d97a24b`. All29 exports and10 retained inputs were checked against that manifest. No phase186 or public file was modified.

## Decision

**Accept the corrected principal-result contract, with the exact retained classifications and computational trust boundary below.** The uniform residue/fiber proofs, affine/projective bases, higher-rank classification deduction, literal Witt computations, Figure2 corrections and biplane counterexample are sound within their stated scopes. The conventional four-edge reading of an additional source path claim must be recorded as a correction, not as an unchanged recovered theorem. The author already uses the correct four-vertex/three-edge configuration.

This is not an admission that every assertion in the entire source follows. In particular, the object-level identifications with Pasini's Γ₂₃(4) and Γ₈(4) remain unpaid. Historical priority assertions, referenced earlier constructions and source background are not established merely by matching a group or a diagram. This review does not award a new open-conjecture resolution or a compression rate. Root admission and corpus accounting are separate decisions.

The primary source is D. Leemans, *A Generalization of a Construction due to Van Nypelseer*, Beiträge zur Algebra und Geometrie46(2005),561–574, saved as `sources/older_L092_gwdg.pdf`, SHA-256 `f76a72aeec658ace5d821519a686c3041e455d3a1c5c4276988bd711ba830403`. All14 pages were read in the bound extraction; original images of printed pp566,570,572 were separately inspected for the path wording and both detailed figures. The literal definitions on pp562–565, not the numerical tables, determine the construction.

## 1. Numbered source contract

| Source statement | Reviewed disposition |
|---|---|
| Theorem1 | B.Necessity proves the linear/dual/(4,3,4) conclusion. Chamber transitivity means oriented **three-edge** paths starting at a point. The source's conventional four-edge wording is corrected by the independent counterexample below. |
| Theorem2 | Retained from Buekenhout–Dehaye–Leemans, L102 Theorem6.2, pp42–43; thick spaces exclude its circle case. This external classification is not derived from our elementary recursion. |
| Theorem3 | B.ProjectivePlane proves firmness, all residue types, residual connectivity, diagrams and PSL-containing actions; it also proves q=2, needed by the binary affine branch. |
| Theorem4 | B.AffinePlane and B.SemilinearSixteen prove the stated geometry and group actions, with exact affine residue descriptions and the q=3 exceptional gonality. |
| Theorem5 | B.PointIteration proves the obstruction using an intrinsic ray/anti-flag invariant, without relying on a full-group guess. |
| Theorem6 | Retained corrected theorem: for q>3, firmness and (IP)₂ always; RC iff q>4; FT iff q=4 or8; the A-geometry occurs at q=8. The printed q=4 conjunction is false. The retained literal q=4 disconnection is Lean-certified. |
| Theorems7–8 | B.SpaceObstruction gives the plane-valued component invariant, positive within-plane connectivity and the exact number of components; the projective proof includes q=2. |
| Theorem9 | C.Fiber proves the equivariant chamber bijection and exact ordered-t-tuple stabilizer-fiber criterion, hence the source's staged Property(*) criterion and t-transitivity implication. |
| Theorem10 | Retained Kantor classification, Theorem3 and its proof on p73. The semilinear upper bound in that proof is part of the retained input, not inferred from L092's abbreviated lower bound. |
| Theorem11 | C.Classification correctly derives the same final list after correcting the false intermediate connectivity statements. Full small-Witt automorphism orders and the explicit large-Witt derived planes are paid by the finite computations. |

Thus the result is a **corrected deduction with retained classifications**, not a proof that false printed sentences follow unchanged. L092 Lemma1 is fully recovered; Lemma2 is proved in the retained deleted-line note; the needed local-action parts of Lemma3 are proved directly; the unrestricted equivalence in Lemma3(1) is refuted by the cyclic biplane; Lemma4 is recovered; Lemma5's RC restriction to q=4 is replaced by the already reviewed e=2 criterion. The source's auxiliary affine deleted-line automorphism claim also has the previously established missing factor two. The old Hermitian conjectural statement is handled by the separately retained proof and receives no new credit here.

The rank-six construction's two displayed rank-five residues have different type-size multisets, so their nonisomorphism is proved. Their actual native stabilizer actions are verified. These facts do not provide the missing maps to Pasini's named objects.

## 2. Uniform proof review

The residue reduction uses complete ordinary chains for necessity. Fixing only the largest ordinary subset produces a join and would not justify connectivity of a factor. The retained proof uses the full chain, whose residue is exactly the derived rank-three construction, so this potential gap is absent. Sufficiency treats every flag containing an ordinary object through the Boolean/derived join and explicitly treats all combinations of the three exceptional types. Parameter inheritance preserves k−t+1 and r. Geometry and firmness are proved by actual flag extensions, not assumed from connectedness.

C.Fiber is a genuine bijection. A full ordinary chain orders T; adjoining the copied point gives an ordered t-tuple. Conversely, the unique block on T together with the copied point intersects any chosen alternative block exactly in T, by the Steiner property. This reconstructs the marked tail and every incidence. The final fiber has r−1 blocks. The usual orbit-fiber implication is proved in the text itself; its U.Orbits name introduces no unstated additional proof. The chamber count (v)_t(r−1), type counts and panel counts follow exactly.

C.Intersections pays the exceptional cases that a blanket Boolean claim could miss. For t=4, fixing all exceptional objects leaves the triangle on the three-set T. For t=3, marked/block and marked/copy flags leave digons, while block/copy leaves point-versus-two-subset incidence on the block. All other cases reduce through the join to the lower rank or to genuine complete-chain Boolean intervals. The rank-three point and line residues are subincidence structures of a linear space, and flag residues are digons. This proves (IP)₂ without assuming a classification.

B.Necessity obtains point-line distance at most three from connected original-point residues and obtains a proper triangle from a path between different lines through a point. Partial linearity then gives gonality three and same-type diameters at most four. The local two-transitivity proof uses the actual four-object configurations. The converse local-action statement correctly rules out repeated or multiply intersecting lines by transporting a singleton intersection.

The projective and affine base proofs account for the entire geometry and every rank-two residue. The determinant-one adjustment preserves the required projective/affine flags. In the affine case it also proves that the chamber stabilizer is trivial. For the exceptional AΓL(1,16) action, the order-five direction quotient and multiplication by2 on its four nonzero exponents give the precise missing transitivity. The point-iteration invariant is preserved by every type-preserving automorphism because the old incidence is recovered as a complement; its two values are realized by extendable flags. The higher-dimensional obstruction is a genuine path invariant, not an inference from parameter counts.

For binary affine designs, the one-point derivative is PG(d−1,2); the q=2 projective base is explicitly paid. The full AGL(d,2) identification follows by reconstructing addition from the fourth point of an affine plane through zero. In the subline branch, the retained proof gives the derivative AG(e,q), RC exactly at e=2, and the full semilinear group. The divisibility q|2f, for q=p^f, correctly leaves only q=4. The q=4 sufficiency is an explicit action, not group-order divisibility alone.

The final classification retains two substantial external classifications. I checked the exact L102 statement and case exclusions, and Kantor's design convention, Theorem3 and proof. No claim is made that their classification proofs have been compressed or formalized by the new local arguments. The native Mathieu actions and their classical identification with those in Kantor are also retained library/classical inputs.

## 3. Hermitian Figure2

The original Figure2 was visually checked. Its entries disagree with the literal construction at the locations stated in the author audit. Object counts are q³+1, q²(q³+1), q²(q²−q+1), and local orders are q−1,q,q²−2. Thus the q=5,8,11 panel entries and the q=16 object counts require correction. The proposed explanation via a smaller group's chamber orbit remains explicitly an inference, not an established account of the source computation.

The new all-q diameter proof is sound. In the retained norm-shell coordinates, a determinant-one unitary matrix sends the base point to a collinear point exactly when its trace is2. The Cayley connection set is all nonidentity unipotents. Every nonscalar element is a product of at most two such elements, by choosing a basis with nonzero lower-left entry and adjusting the upper unipotent parameter. In odd characteristic only the antipode −I requires three; in even characteristic all points are within two steps.

A triangle of adjacent group elements is contained in one root coset: the trace equations force the second matrix into the same upper root group. This excludes incidence6-cycles, while upper/lower unipotents give an induced quadrangle and hence an8-cycle. The count of flags within distance3 of a point is q³+1, strictly below the total (q+1)(q²−1) by (q−2)(q+1). Parallel isotropic shell lines with second coordinates b and cb, c≠0,1, have no collinear pair because the difference norm is (c−1)²/c. These arguments establish the exact point/flag diameters, not merely upper bounds.

The original-point residue has a complete multipartite collinearity graph, with classes given by blocks through the deleted point. The separate disjoint-block and proper-triangle arguments prove its exact (4,3,4) labels. The final literal block-residue labels are (5,4,6) in even characteristic and (6,4,6) in odd characteristic.

I independently wrote `phase199_hermitian_literal.g`. It constructs all isotropic projective points in GF(q²)³ with the diagonal Hermitian form, every secant as a linear-form kernel, and the literal source residues. It reads neither the author coset checker nor saved witnesses. Every point pair is checked against the Steiner property, and breadth-first searches start at **every vertex** of the two residue graphs. The results are:

| q | Unital points / blocks | Block-residue type sizes | Block-residue diameters / girth | Point-residue type sizes | Point-residue diameters / girth |
|---:|---:|---:|---|---:|---|
| 3 | 28 / 63 | 24 / 32 | 6,6 / 8 | 27 / 54 | 4,4 / 6 |
| 4 | 65 / 208 | 60 / 75 | 5,6 / 8 | 64 / 192 | 4,4 / 6 |
| 5 | 126 / 525 | 120 / 144 | 6,6 / 8 | 125 / 500 | 4,4 / 6 |

These finite checks independently verify the source-to-residue bridge for the stated small cases, including odd/even characteristic and a printed factor-three discrepancy. They are not an infinite-family proof. The author's root-coset replay additionally checks all nine field orders printed in Figure2. The uniform argument remains written mathematics, outside Lean.

## 4. Witt computation and formal certificates

I read the entire GAP model/stabilizer checker, Python validator, Lean generator, all three compiled Lean files, and the retained Mathieu fiber checker. A fresh complete author replay passed, and the complete new Witt witness is byte-identical to the frozen witness. The retained Mathieu extension-fiber program was also replayed afresh.

The five block models are not selected merely by matching parameters. The two small models have a unique k-subset orbit of the required size and no smaller orbit. The large models have the unique possible size-three tail invariant under the ordered-t-tuple stabilizer. All330,792,1540,8855 and42504 t-subsets, respectively, are checked. This identifies the actual native designs under the explicitly retained Mathieu actions.

The full automorphism call is substantive. The installed DESIGN implementation of `BlockDesign(v,blocks)` creates a bare design without a preassigned automorphism group. `AutGroupBlockDesign` computes the color-preserving automorphism group of its incidence graph through GRAPE and restricts it to the points. The program then verifies preservation by every returned generator and actual equality/inclusion with the native group. Completeness therefore relies on the full DESIGN/GRAPE graph-automorphism implementation, not on the Python check of generator preservation. Full orders are7920,95040,887040,10200960,244823040, as stated.

The three derived-plane maps are verified against coordinate PG(2,4), not against an assumed uniqueness theorem for order-four planes. Python independently reconstructs GF(4) as coefficient bits, all original Steiner incidences, all derivatives and all mapped coordinate lines. The finite Lean declarations verify point/line bijections and all441 incidence equivalences in each displayed table. They do **not** prove within Lean that those displayed tables are derivatives of the original Witt designs; that bridge remains in GAP/Python.

Figure3's groups are paid by actual homomorphisms, kernels and complements. Block kernels are elementary abelian of order16, their images are the actual A_k actions, and complements are constructed. Marked stabilizers are parity-matched subset stabilizers. In the M22 marked case, the code separately verifies the central2², elementary-abelian quotient2⁴, S3 quotient and outer complement; it does not assume that the central extension splits. Ordinary stabilizers are transported by explicit derived-design maps and compared as actual permutation groups. The projective semilinear S3 complement is supplied by a diagonal order-three element and Frobenius. Source labels refer to the native action, even when the full design group is larger, as at degree22.

The biplane Lean file uses the literal ZMod11 difference set, literal primal/dual proper-triangle predicates, singleton line-intersection rule, and actual residue vertex types. It proves both neighbor graphs connected and the four-point flag residue disconnected. Its statement does not smuggle disconnection into the adjacency definition. This refutes the unrestricted implication in Lemma3(1); the example is not a partial linear space and does not refute B.Necessity.

Fresh Lean checks give15 new axiom reports:9 for the three explicit derived-plane isomorphisms and6 for the biplane correction. The retained GF(4) residue module gives7 further reports. They use standard Lean axioms only; no sorry, admit, new axiom or native_decide is present. The all-rank recursion, uniform classification, full finite-group completeness, H.Labels and the new path-wording counterexample remain outside Lean. Four semantic Lean mutations and two Python witness mutations are rejected by the author replay.

## 5. Additional path-wording qualification

The source's Lemma3(4) and Theorem1 say paths of length four. The author correctly uses P–M–x–L, with four vertices and three edges. Under the usual edge-count meaning, the stronger assertion is false. In AG(2,3), ASL(2,3) has216 elements, is flag-transitive on the affine plane, and acts regularly on the216 chambers of Construction3. The plane has432 oriented four-edge paths beginning at a point. No group of order216 can be transitive on that set.

The independent `phase199_path_length.py` verifies the entire57-object geometry, all216 chambers, panel sizes2/3, all58 required connected graphs, all57 rank-two intersection tests, the216 explicit affine determinant-one actions and the432 paths. Its observed four-edge orbit size is216. The full written correction is `phase199_path_length_correction.md`. This is an additional precise source correction, not a claim about author intent or a new open problem.

## 6. Reproduction, costs and remaining boundary

Run `python3 -B phase199_review.py --output-dir /private/tmp/fresh_phase199`. It verifies every frozen author binding before and after execution, reruns the author packet, the independent literal Hermitian checks, the independent path check and the retained Mathieu fibers, and rejects an altered literal flag incidence. The fresh output directory is mandatory. The report records GAP/DESIGN/GRAPE and mathlib versions, all Lean controls and exact witness identity. The exported manifest binds this review and its evidence. Scientific and public source files remain untouched.

The author's exported packet contains224,913 bytes. Its ten new prose files account for75,724; new computational programs/drivers for27,842; new Lean files for9,810; other evidence for111,537. Retained non-primary inputs total66,439 bytes:58,658 prose,2,330 GAP and5,451 Lean. The three retained primary PDFs total973,187 bytes and are not republished by this review. These are exact artifact inventories, **not a minimal proof-length denominator or a compression ratio**. The complete new-plus-retained prose/program inventory is164,554 bytes; with the Lean sources it is179,815. That inventory deliberately includes scope and review prose and does not establish a source-matched manuscript measurement.

The independent review adds its own separately itemized programs, prose and replay support. It does not re-charge or re-claim the earlier Hermitian conjectural statement, deleted-line theorem or inversive correction as new discoveries. Construction1/2/3, classical designs, projective/affine linear algebra, classification inputs and software libraries remain attributed retained material.

No mathematical defect remains in the corrected principal-result packet after the path convention is made explicit. Strict all-clause source replacement is still unestablished: most visibly the two named Pasini isomorphisms lack object maps, and historical/background identifications have not received a blanket admission. Any corpus update should say **corrected principal contract with retained classifications**, preserve the source's false statements as corrections, and keep a whole-manuscript compression claim separate.
