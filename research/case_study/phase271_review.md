# Independent review of the triangle-geometry principal contract

Review date: 11 October 2026. Independent verdict: accepted for the exact corrected principal-source contract below. The frozen author manifest phase265_manifest.json has SHA256 18cd719df0625cbb3d7795bf64072e93bcfaf57e6aec3d1557355be897d1280c. No author file was changed during the final review. The separate cloning result and its question accounting are outside this review; repository admission remains the root editor's action.

## 1. Exact source and coverage

I read the complete final journal source, Delaby–Leemans–Tranchida, *Geometries with trialities arising from linear spaces*, Algebraic Combinatorics 9(2) (2026), 379–402. The bound PDF has twenty-four article pages and one archive cover; its SHA256 is b851c8e5fe1589ce950bb284b75eee1b5f7bc4b3f2256af84565dd6ff2b8f0b0. Printed pages 380–381 (the principal theorems), 390–391 (correlations), 399–400 (all diagrams) and 401 (Table 1 and questions) were also checked visually. The earlier preprint was not substituted for this edition.

Both complete replacement papers, all four GAP programs, all four actual Lean declarations and the source ledger were read. All five pages of the final common-paper PDF and all eight pages of the final application PDF were visually inspected: formulas, tables and text were readable, with no clipping or overlap. The retained Buekenhout–Dehaye–Leemans classification, Theorem 6.2 on printed pp.42–43, was reread from its primary and visually checked. The complete phase210 norm-shell transport supplement and review were reread for the exact written interface used here. This is a review of that interface's use in the new triangle application, not an independent review or admission of this reviewer's earlier phase210 Lean work; the latter requires a different reviewer.

The intended scope is the corrected complete action classification of Theorem 1.1 and the unchanged geometric classification of Theorem 1.2, including necessity and sufficiency, construction, isomorphism and automorphism reconstruction, full correlations, connectivity, all principal diagrams and all Table 1 cases. The square and Desargues examples, the external hypermap-catalogue identification, and the final experimental questions are explicitly excluded. The 2003 classification remains a retained theorem, not an additional source recovered here.

## 2. Literal construction and reconstruction

The directed flag relation is exactly
\[
 (p,L)D(q,M)\quad\Longleftrightarrow\quad p\in M,\quad q\notin L.
\]
For the equality-of-point and equality-of-line matrices its integer factorization is \(D=(A-I)(B-I)\); the only intermediate flag is \((p,M)\), so the product has zero-one entries. A chamber corresponds bijectively to an ordered noncollinear triple. Every panel has exactly \(k-1\) completions in a uniform linear space. Thus firmness means \(k\ge3\), and thinness means \(k=3\). A circle with two-point lines is neither firm nor thin.

Outgoing degree \(v-|L|\) first forces uniform line size under triangle flag transitivity. The identity \(v-1=r_p(k-1)\) then forces constant pencil size. This proves uniformity without presupposing the reconstruction theorem.

For \(r\ge3,k\ge2\), the off-diagonal common-successor maximum \((r-2)(k-1)\) strictly exceeds the possible different-point values \(0,k-2\), and therefore recognizes point fibers, including when \(k=2\). The point labels of successors of \((p,L)\) are precisely \(P\setminus L\). Consequently a triangle isomorphism gives
\[
 M_i(p,L)=f_{i+1}(L).
\]
The image flag condition, intersected over all lines through \(p\), forces \(f_i(p)=f_{i+1}(p)\). This is the essential synchronization step. It shows that the entire map is the diagonal action of one input isomorphism. Applying the same argument to its inverse proves the full bijection of isomorphism sets for two uniform inputs with equal parameters. No line-fiber assertion at \(k=2\) is inferred from a zero predecessor count.

The equal-parameter wording of the common theorem does not narrow the source's isomorphism conclusion in its stated thick domain. A triangle isomorphism first recovers \(k\) from its panel size \(k-1\). Its outgoing relation degree is \(v-k\), so it then recovers \(v\), and finally \(r=(v-1)/(k-1)\). Thus two isomorphic inputs in this domain necessarily have the same parameters before the reconstruction theorem is applied. The exceptional three-point circle is treated separately, as required by its failure of the pencil hypothesis.

For \(r,k\ge3\), common-predecessor maxima also recognize line fibers. A type reversal exchanges the two recognized partitions and induces an input duality on one type. Removing its global lift leaves an automorphism fixing a whole type, hence the identity. Thus no pointwise kernel is omitted. This proves the full formula
\[
 \operatorname{Cor}(\Delta(S))=C_3\rtimes_\epsilon\operatorname{Cor}(S).
\]
It does not require a polarity. A polarity is equivalent to splitting the *other* sequence, with kernel \(\operatorname{Aut}(S)\) and quotient \(S_3\). The source's qualification is corrected rather than transferred to the wrong sequence.

The constant map on each input type is a valid counterexample to the claimed functor on all forward-incidence morphisms. It preserves input incidence and destroys the negative incidence clause in the triangle relation. The common paper uses only the valid transport of isomorphisms and correlations.

## 3. Complete group classification

Transitivity on ordered noncollinear triples supplies flag transitivity and both local two-transitive actions by choosing two points on a line or on two distinct lines through a point. Thus the exact hypotheses of the retained BDL necessity classification apply. Its exceptional \(A\Gamma L(1,16)\) action on \(AG(2,4)\) is excluded by \(960<2880\).

In a projective space, a map of independent representatives carries the given triple to its target; rescaling one target representative adjusts the determinant without changing a projective point. This proves PSL sufficiency already in projective dimension two. The exceptional \(A_7\) action is a complete bounded obligation and is independently verified below.

For affine dimension at least three, a spare basis vector corrects the determinant of a map between ordered independent pairs. In dimension two, equal determinants are exactly the SL orbits on bases; each fiber is a torsor, with transport \(B^{-1}C\). The semilinear determinant action is
\[
 t\longmapsto \det(A)\sigma(t).
\]
Its transitivity is necessary and sufficient in dimension two. The contained-SL hypothesis is essential: determinant transitivity alone does not saturate the matrix fibers.

Over \(F_9\), the group whose linear half has square determinant and whose Frobenius half has nonsquare determinant is a subgroup, since Frobenius preserves square classes. Its order is 5760 and its linear half has order 2880. It is transitive on all 5760 ordered bases and omits nonsquare-determinant linear matrices. The affine extension is therefore regular on all 466560 ordered noncollinear triples. This is a counterexample within the literal source hypotheses to the GL-containment necessity, together with a uniform repaired criterion.

For a Hermitian unital, normalize an ordered isotropic pair to \(e_1,e_3\). The third point \((x_1,1,x_3)\) has invariant \(z=x_1x_3^q\), where \(z+z^q=-1\). The complete PGU pair stabilizer is the displayed diagonal torus and is regular within each \(z\)-fiber. For odd \(q\), \(-1/2\) is a fixed trace-fiber element. For \(q=2^e,e\ge3\), a Frobenius orbit has size at most \(2e<q\). The fibers for \(q=2,4\) are single orbits of lengths two and four. Hence PΓU is transitive exactly in those two cases. Its order then equals the triple count, excluding every proper subgroup. The argument proves sufficiency and the full-group requirement, not merely a numerical necessary condition.

Circles reduce exactly to three-transitivity, retaining the declared permutation classification and Mathieu actions. The degree-15 \(A_7\) is excluded by order, while its projective action remains valid. The alternating groups require \(v\ge5\). For odd projective-line fields, the two PSL triple orbits are distinguished by determinant square class; Frobenius preserves the classes, so a nonsquare-determinant semilinear element joins them.

The newly supplied classical normalizer proof is complete. Normalize a permutation normalizing PSL to fix \(\infty,0,1\) using PGL. The translation subgroup is the unique Sylow-\(p\) subgroup of the infinity stabilizer, so its normalization gives additivity. Normalizing square multipliers gives multiplicativity for square arguments. In even characteristic every element is a square; in odd characteristic every element is a sum of two squares, since two subsets of cardinality \((q+1)/2\) must intersect. Additivity now gives full multiplicativity. The normalized permutation is a field automorphism. This establishes the natural PΓL normalizer, including \(q=2,3\), without an undeclared simplicity or high-dimensional collineation assumption.

## 4. Residues, diagrams and the complete table

The deleted-pencil residue is proved in both directions from the literal relation. Its parts are the points \(Q\notin L\) and the flags \((a,M)\) with \(a\in L\setminus\{p\}\), \(a\in M\ne L\), incident when \(Q\in M\). The otherwise required condition \(a\notin pQ\) is automatic. This is the full Van Nypelseer residue with one pencil actually removed; connectivity is proved after that removal.

In dimension at least three, each edge stays in the plane generated by \(L\) and its outside point, giving distinct residue components. In a projective plane, two allowed parallel classes form a connected affine grid. In an affine plane, two allowed pencils have intersection graph \(K_{q,q}\) minus a matching, connected for \(q\ge3\). These arguments cover the small cases and do not require Desarguesian coordinates for connectivity.

For a unital, the retained outside-point-to-shell identification maps points of \(L\) to isotropic directions. After one direction is deleted, two remain. Choose their representatives as a hyperbolic basis. Their root subgroups become the full upper and lower elementary subgroups of SL2 and generate it, including at \(q=2\). Its regular action on the nonzero shell joins all outside points. This proves connectivity uniformly; it does not assume that arbitrary deletion preserves connectivity.

The projective plane of order two gives an eight-cycle; the affine plane of order three gives a twelve-cycle. For the other planes, the explicit path arguments give both part-diameters four and an actual six-cycle, while unique joining lines exclude four-cycles. The counting arguments remain valid at \(q=4\). In \(U_H(4)\), complete finite computation gives two 60-vertex parts, degree four, girth eight and both diameters six. Distinct complete distance profiles on the two parts exclude every part-interchanging automorphism.

The vertex labels are \(n=vr\), \(s=k-2\). Every source Table 1 row is covered, including field automorphisms in AΓL, the projective-plane polarity action, higher-dimensional projective spaces with unequal point and line counts, and \(U_H(2)=AG(2,3)\). For circles with \(v\ge4\), the nonbacktracking arc relation is strongly connected, and its four-cycle changes the lifted type by one. Each vertex residue is \(v-2\) disjoint edges. Endpoint reversal supplies \(S_3\) commuting with \(S_v\). At \(v=3\), the six disjoint typed chambers give \(S_6\) and \(S_6\times S_3\).

## 5. Independent finite evidence

The independent Python checker uses polynomial arithmetic and a hyperbolic Hermitian form, rather than the author's diagonal form. It obtains secants as spans of pairs of isotropic points rather than by dual-line enumeration. Every nonzero field element is checked to have an inverse before geometry is constructed.

For \(U_H(2)\) and \(U_H(4)\), the checker constructs the literal relation on all flags and checks all panels and all 540910 flag-signature pairs, including 540280 pairs for \(U_H(4)\). The latter gives 62400 panels of one type pair and 249600 chambers. Every residue edge is compared with the deleted-pencil description. Girth is independently computed by deleting each edge and finding a shortest alternate path, rather than the author's BFS back-edge formula. The full part profiles are
\[
 (1,4,12,36,44,20,3),\qquad (1,4,12,36,42,20,5).
\]
The same independent arithmetic enumerates the complete \(F_9\) frame set and its determinant halves, and checks trace-fiber Frobenius orbits at \(q=2,3,4,5,8\). These remain finite diagnostics for the written uniform arguments.

An additional independent construction checks the complete literal triangle graphs of circles on three through six points. It verifies the six disconnected typed chambers at three points, connectedness thereafter, every matching residue, the endpoint/type reversal and triality, and all 6, 24, 120 and 720 diagonal input permutations respectively. It also checks the point-fiber reconstruction signature when there are at least four points. This is not an exhaustive graph-automorphism enumeration: completeness of the full groups is supplied by the written reconstruction and separate six-chamber argument.

The independent GAP checker starts with the primitive degree-15 \(A_7\) action, recovers its 35-line Steiner orbit, and constructs a binary coordinate bijection verifying all projective lines by vector addition. It checks the whole noncollinear ordered orbit of size 2520 and the ordered-pair orbit of size 210. This differs from the author's route through GL4(2) and A8. The primitive-group library and GAP remain ordinary computational dependencies.

Three independently corrupted variants are rejected: replacing negative incidence by positive incidence, removing the nonsquare semilinear half, and using the wrong unital trace fiber. The author packet supplies further live relation, signature, group and Lean controls. Finite checks are not a replacement for the all-parameter proofs.

## 6. Formal and accounting boundary

The four actual Lean declarations prove unique determinant-one matrix transport, literal semilinear determinant transformation, its matrix-fiber equivalence, and subgroup orbit saturation. The last retains its explicit fiber-transitivity hypothesis, supplied in the written application by the matrix result. No declaration is a formal proof of BDL, the full finite geometry, every residue argument, or either complete classification.

The classical classification and full input automorphism identifications remain retained; the complete norm-shell proof and its transport are paid repository dependencies. The common paper is an actual complete manuscript. The application, its mathematical programs and required retained inputs must also be charged. A source-clause count and a principal-contract admission do not establish a matched compression ratio.

The frozen raw inventory contains 44464 UTF-8 bytes and 6790 whitespace words in the two new papers (five plus eight rendered pages), 14138 bytes in the five mathematical program/formal files, and 16466 bytes in the two retained repository proof inputs. The sum of those three categories is 75068 bytes; including the actual author replay driver adds 7794 bytes, giving 82862. These are raw package burdens, not matched compression denominators: the declared opaque classification and classical full-group inputs still require the chosen accounting convention, and no source-side proof-unit measurement has been made. The old incidence_compression.md text is attribution-only here because its reused proof is written in full in the new common paper; the review does not charge it again as an additional logical proof dependency. Rendered certificate pages and this review's evidence are separately identifiable support artifacts. The source's twenty-four article pages divided by the thirteen new pages would therefore not be an admitted compression ratio.

The exact source ledger has 44 dispositions and 13 complete proof spans. The root principal contract may admit one source record with the stated corrections and retained inputs; this is not a whole-paper claim and does not include excluded auxiliary examples or experiments. Source corrections are kept distinct from answering an explicitly posed open question. This review requests no question-count change and makes no historical-priority claim.

## 7. Reproduction and final disposition

The companion phase271_check.py verifies the exact frozen author manifest, all forty exports, and the retained bindings (including private primaries when requested), invokes the complete author replay in a fresh child directory, and then runs both independent programs and all three independent semantic mutations. The bound phase271_replay/report.json records the final execution. It uses Python with optimization enabled, so the required independent checks are explicit runtime predicates rather than removable assert statements. No source PDF, extracted primary text, image or build product is exported by this review.

Accepted: the complete corrected action classification and the unchanged geometry classification, their required source interfaces, full principal diagrams and corrected Table 1. Retained: BDL's classification, the explicitly declared classical full automorphism and three-transitive inputs, and the written norm-shell proof/transport. Excluded: the source's square and Desargues examples, external hypermap-catalogue identification and final questions. Formal boundary: four actual matrix/orbit declarations only; the full principal results remain written proofs with exact finite certificates. No public file has been changed.
