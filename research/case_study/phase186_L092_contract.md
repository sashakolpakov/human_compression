# L092 principal-result contract after the residue and fiber reductions

This is an intake audit, not an admission of an entire-paper replacement. The complete source is D. Leemans, *A Generalization of a Construction due to Van Nypelseer*, Beiträge zur Algebra und Geometrie46(2005),561–574. The saved original PDF has SHA256 f76a72aeec658ace5d821519a686c3041e455d3a1c5c4276988bd711ba830403.

The source's construction and existing results remain attributed to it and its cited predecessors. The present organization consists of (i) the derived-design residue recursion, (ii) a single ordered-t-tuple chamber fiber, and (iii) the explicitly proved projective and affine rank-three bases. Corrected false statements are recorded as corrections, not as corollaries of a replacement theorem.

## Principal statements

| Source clause | Current deduction or retained input | Exact remaining obligation |
|---|---|---|
| Theorem1: necessary linear/dual/(4,3,4) classification and path transitivity | B.Necessity in phase186_linear_space_bases.md; complete direct proof from literal chamber incidence and residual connectivity | Independent review of this new written proof |
| Theorem2: classification of locally two-transitive flag-transitive finite linear spaces | Retained L102 Theorem6.2 pp42–43, exact hypotheses and exclusion of circles bound in phase186_primary_classification_bindings.md | This is an attributed external classification, not newly proved by the recursion |
| Theorem3: projective-plane family, affine residues and PSL-containing groups | B.ProjectivePlane proves all clauses, and also q=2 needed later | Independent review; any desired formalization remains separate |
| Theorem4: affine-plane family, both residue families, and all stated acting groups | B.AffinePlane, B.SemilinearSixteen, and the exact residue descriptions and parameters | Independently compare all diagram labels with the displayed residue types; written numerical formulas are supplied |
| Theorem5: point-residue iteration not flag-transitive | B.PointIteration gives two intrinsic anti-flag orbits, without assuming a full-group classification | Independent review |
| Theorem6: deleted-line iteration, claimed exceptional q=4 | The printed principal claim is false. Frozen phase182 supplies the corrected uniform theorem: firm+(IP)₂ always, RC iff q>4, FT iff q=4 or8, hence A-geometry iff q=8 | Preserve correction status. Literal q=4 disconnection is Lean-certified; uniform theorem and q=8 are not fully formalized |
| Theorem7: projective dimension≥3 not RC | B.SpaceObstruction, including q=2, gives a plane-valued edge invariant and exact components | Independent review |
| Theorem8: affine dimension≥3 not RC | B.SpaceObstruction for every q≥3 gives the same invariant and exact deleted-line components | Independent review |
| Theorem9: Property(*) iff FT, implies t-transitivity | C.Fiber gives an explicit equivariant chamber bijection and one-fiber iff criterion; source three-stage condition follows from the same orbit-fiber principle | Independent review; bind use of the retained U.Orbits interface |
| Theorem10: Kantor classification of t-transitive Steiner systems | Kantor(1985) Theorem3 and its proof p73, including the semilinear upper bound, bound in phase186_primary_classification_bindings.md | Attributed retained classification; our elementary lemmas do not replace its proof |
| Theorem11: complete higher-rank family classification | C.Classification in phase186_higher_rank_classification.md integrates the common proofs, the reviewed inversive application and retained Mathieu fibers; phase186 Witt checks pay full groups, derived PG(2,4) maps and Figure3 stabilizers | Independent review of the new written proof and finite checks remains required |

## Higher-rank application details

* **Binary affine planes:** fully paid by Section3 of phase186_steiner_fiber_and_intersections.md. Derivation gives PG(d−1,2), residual connectivity holds exactly for d=3, and the explicit AGL(d,2) action satisfies the fiber criterion. The positive d=3 counts and chamber stabilizer order are included.
* **Subline designs:** the one-point derived design is AG(e,q). The shared recursion and bases show RC precisely for e=2, within the firm range q≥3. This corrects L092 Lemma5, which incorrectly restricts RC to q=4. The separate flag-transitivity condition can still select q=4 in the final classification. The exact full automorphism group and fiber action belong to the independently reviewed phase183 inversive application; they must be cited there, not inferred solely from a group order.
* **Small Witt designs:** C.Fiber gives chamber counts three times the full M11/M12 group orders. The full groups are now computed from the literal native incidence models in phase186_witt_derived_check.g; design identification within each retained native action is forced by the complete subset-orbit sizes.
* **Large Witt designs:** explicit coordinate-incidence maps now identify the (t−2)-fold derivatives with PG(2,4). The geometric assertions follow from the recursion and projective base; the existing phase182 stabilizer fibers supply transitivity. Formula(C3) recovers all displayed counts. The phase186 finite checks pay the Figure3 group labels through actual kernels, complements, and conjugated derived-design actions; see phase186_witt_group_identifications.md.

The last M24 construction's ordinary-point and octad residues have different type-size multisets, explicitly computed in the fiber manuscript, so their nonisomorphism is proved. Identifying them with the named earlier rank-five geometries remains part of a strict full-source contract. The subgroup annotations have now been paid by the finite checks.

## Auxiliary and numerical clauses

The retained recursion and phase187 review pay the sufficient direction of Lemma1 and all panel counts; the opening firmness-necessity argument in the phase186 fiber note supplies the converse. C.Intersections pays (IP)₂ at every rank. Lemma2's compatibility with rank-two duality is explicitly proved in the frozen phase182 deleted-line theorem. B.Necessity proves the direction of Lemma3 needed for Theorem1, and B.LocalActions proves its other three local-action/chamber clauses. The unrestricted implication in Lemma3.1 is false: phase186_biplane_delta_correction.md supplies the literal cyclic2-(11,5,2) counterexample, with connected primal/dual neighbor graphs but a four-point edgeless Construction3 residue. This auxiliary correction is separate from the principal partial-linear-space theorem and from conjecture claims.

The source's Hermitian Conjecture1 remains separate from manuscript compression. The existing Hermitian proof is retained without duplication. Figure2 now has a complete numerical audit: phase186_hermitian_figure_audit.md corrects object counts and panel orders, while phase186_hermitian_residue_diameters.md proves all diameter/gonality labels through a common SL(2,q) root-coset graph. The latter new all-q argument is written-only, with a finite root-coset replay for all nine printed field orders; it is not covered by the Lean certificates.

The source's abstract/introduction advertises unification of earlier Mathieu geometries. The explicit construction and the derived-design recursion give a substantive common explanation, but named-isomorphism claims still require object-level correspondences to those earlier sources. A statement that the groups or cardinalities agree is insufficient.

## Current admission boundary

The new phase186 files are written candidate components, pending independent review. C.Classification now gives a complete principal higher-rank classification proof with retained external classifications and explicit finite inputs. The new Lean module WittDerivedPlanes verifies the three concrete derived incidence maps against GF(4) coordinates; it does not certify the general recursion, all-q bases, full group computations, or the full classification proof. The retained phase182 q=4 residue certificate and the new CyclicBiplaneDelta certificate separately concern literal finite corrections. No whole-paper reduction, new conjecture resolution, or compression ratio is claimed by this contract. The remaining historical named-geometry identifications, together with independent review of all new material, prevent a strict all-clause source admission.
