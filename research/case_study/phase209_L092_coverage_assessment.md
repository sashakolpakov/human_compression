# Coverage assessment for the corrected L092 results

Phase209, 10 October 2026. Private recommendation for the phase208 publication decision.

**Recommendation: record L092 as a source whose specified main results have been recovered with corrections and stated external inputs. Do not record an unchanged recovery of the entire paper.** The missing Pasini identifications do not enter the proofs of the final classification or the new rank-six construction. They remain substantive omitted assertions and must be visible beside the source entry.

This is an author-side reassessment. The agent preparing this note wrote substantial parts of phase186 earlier. It is therefore not a second independent mathematical review. The independent review is phase199, whose conclusion I have compared with the actual written arguments and source statements. No computation was rerun for this note; phase208 handles the fresh execution. This round compared the saved primary text for the construction and numbered statements; visual source checks remain those recorded in phases186 and199.

The primary is D. Leemans, *A Generalization of a Construction due to Van Nypelseer*, Beiträge zur Algebra und Geometrie 46 (2005), 561–574. Source PDF SHA-256: `f76a72aeec658ace5d821519a686c3041e455d3a1c5c4276988bd711ba830403`. The author manifest is `phase186_export.json`, SHA-256 `cbbb953e5565ef1dd36286fe245c12c81fd1f854be5d887a544361055d97a24b`. The independent review manifest is `phase199_export.json`, SHA-256 `8c80fa904dfa730f58bad84c2b83d81250e7626004198849799c7c1467639a3d`.

## What supports the recommendation

The source states two principal objectives on p.561: analyze the rank-three construction, and classify the higher-rank Steiner systems producing the required geometries. It also presents the rank-six M₂₄ construction as a principal result. The actual mathematical statements and their limitations are more precise than the abstract's general wording.

| Source statement | What the replacement establishes | Necessary qualification |
|---|---|---|
| Theorem 1, p.566 | B.Necessity gives the linear-space, dual-linear-space or (4,3,4)-gon alternatives, with the explicit chamber configuration. | The hypothesis is a thick connected **partial linear space**. The transitivity statement concerns four vertices and three edges; the conventional four-edge reading is false. |
| Theorem 2, pp.566–567 | The same classification is available as an explicit external input. | This is the quoted L102 Theorem 6.2, pp.42–43, with the circle case excluded by thickness. Its proof is not rederived. |
| Theorems 3–4, pp.567–568 | B.ProjectivePlane, B.AffinePlane and B.SemilinearSixteen supply the complete projective and affine constructions, residues, diagram parameters and stated group actions. | The projective proof also covers q=2, needed later. The affine q=3 residue has the distinct gonality specified in the proof. |
| Theorem 5, p.568 | B.PointIteration excludes flag transitivity by an incidence invariant with two realized values. | It concerns the type-preserving action and does not depend on an unproved full-group identification. |
| Theorem 6, p.568 | The retained uniform deleted-line theorem gives firmness and (IP)₂ for q>3, residual connectivity exactly for q>4, and flag transitivity exactly for q=4 or 8. Their conjunction selects q=8. | The printed q=4 conjunction is corrected, not recovered as a true statement. |
| Theorems 7–8, p.569 | B.SpaceObstruction gives a plane preserved by every residue path and proves the relevant residue disconnected. | Projective q=2 is also covered; the affine argument uses q≥3. |
| Theorem 9, p.569 | C.Fiber gives an explicit equivariant chamber bijection, the exact stabilizer-fiber criterion and the t-transitivity consequence. | Flag transitivity is a separate condition from residual connectivity. |
| Theorem 10, p.571 | The same classification is available as an explicit external input. | Kantor's Theorem 3 **and its proof on p.73** are retained, including the semilinear upper bound needed in the subline case. |
| Theorem 11, p.573 | C.Classification proves the final list: binary affine planes in dimension three, the GF(4)-subline design on PG(1,16), and the three large Witt designs. It also establishes (IP)₂. | The classification inputs, native Mathieu actions and exact finite group computations remain stated dependencies. False intermediate connectivity claims are not premises. |
| Rank-six M₂₄ construction and Figure 3, pp.572–573 | The construction, all required geometric properties, flag transitivity, object counts and displayed stabilizer structures are established. The two rank-five residues are proved nonisomorphic. | Their identifications with Pasini's named Γ₂₃(4) and Γ₈(4) are not established. |

Thus the proposed addition is substantive. It goes beyond the two already published corrections by supplying the uniform geometry arguments, the local positive and negative cases, the complete final classification and the actual M₂₄ construction. No additional credit should be attached to the two classifications merely because the source itself states them as numbered theorems.

## Checks of the uniform arguments

I reread the residue theorem and its independent phase187 review, the full phase186 fiber and intersection proof, the projective/affine bases, the final classification, and the explanations of the finite Witt inputs. I also reread the Hermitian diameter and numerical arguments and the cyclic-biplane correction, and compared these with phase199. The following are the points on which the classification depends.

The residue isomorphism at an ordinary j-subset is a Boolean join with the construction on the j-fold derived design. Necessity uses a **complete ordinary chain**, whose residue is exactly the derived rank-three construction. Connectivity of one join alone would not suffice. Sufficiency treats flags with ordinary objects by induction and treats every combination of the three exceptional types explicitly. Flag extension and the four kinds of panel counts establish the geometry and firmness before connectivity is invoked. The strength-two case is an identity reduction; its connectivity is proved separately in the applications.

C.Fiber is an actual bijection. The ordinary chain orders a (t−1)-set T, and the copied point completes an ordered t-tuple. Conversely, the unique block through that tuple and any alternative block through T meet exactly in T. This reconstructs the marked tail and all incidence conditions. The fiber has r−1 members, yielding both the transitivity test and the chamber count. The orbit argument is written out, so its reference to U.Orbits conceals no additional classification assumption.

C.Intersections handles the exceptional rank-two residues directly. In particular, the t=4 exceptional flag leaves the three-set triangle; the t=3 cases leave digons or point/two-subset incidence. The proof does not substitute an arbitrary Boolean truncation for the actual residue. At strength two, the remaining residues are subincidence structures of the original linear space or generalized digons.

The positive bases supply every group-action assertion, including determinant-one adjustments and the explicit Frobenius action for AΓL(1,16). The point-iteration obstruction is invariant under every type-preserving automorphism because original incidence is recovered by complementing the incidence of the two original types. The higher-dimensional obstruction is a plane preserved along every path, rather than a count of possible components without proof of invariance.

The final classification separates the two decisive conditions. Binary affine designs derive to PG(d−1,2), so the proved projective bases select d=3. Subline designs derive to AG(e,q), so connectivity selects e=2. Only after this step does the full semilinear group and chamber count force q to divide 2f, where q=p^f; q≥3 leaves q=4. The positive q=4 fiber action is explicit. For the small Witt designs, the full computed automorphism groups are too small for the chamber counts. For the three large designs, explicit incidence maps identify the required derivatives with coordinate PG(2,4), and native transitivity transports one derivative to all others. The earlier complete fiber computations supply flag transitivity.

These arguments support phase199's conclusion. They do not obtain the final classification merely from matching parameters, group orders or successful tests at a few field sizes.

## Borrowed classifications and finite computations

Theorems 2 and 10 are substantial external mathematics. Their use is legitimate for this stated comparison because L092 itself explicitly cites them. The replacement must credit Buekenhout–Dehaye–Leemans and Kantor, keep the full hypotheses, and show those dependencies on both sides of any later comparison. It must not say that the residue and fiber arguments prove those classifications or remove their dependence on earlier group theory.

The native Mathieu actions are also retained classical/library inputs. Phase186 identifies the required block systems within those actions by their actual subset or stabilizer orbits before checking the Steiner axioms. Full small-design automorphism orders depend on DESIGN/GRAPE's complete automorphism calculation, not merely on verifying that some generators preserve incidence. Phase199 separately inspected that distinction. The large derived planes have explicit point and line maps checked against GF(4) incidence; this supplies the positive geometric base without inferring a plane isomorphism from parameters alone.

The formal certificates have narrower conclusions. Lean verifies the three displayed finite derived-plane incidence maps, the cyclic-biplane counterexample and the retained q=4 disconnected residue. The link from the original Witt blocks to the displayed derivative tables is checked computationally outside Lean. The uniform residue/fiber theorems, external classifications, full automorphism computations, Hermitian diameter proof and final classification are not formalized in full. A publication label must preserve this distinction.

## Assertions that still cannot be included

The Pasini names on p.573 are not needed to prove that the two rank-five residues exist, have the displayed actions and are nonisomorphic. Those assertions are already proved using the concrete source construction. Nevertheless, agreeing group names and type-size multisets do not identify them with Pasini's earlier incidence geometries. The object maps remain missing, and no assertion of a complete recovery of every construction or identification in the paper is warranted.

There is a second boundary to keep visible. The source abstract speaks of an arbitrary rank-two starting geometry. The numbered Theorem 1 and B.Necessity instead assume partial linearity. This assessment does not supply a new argument removing that hypothesis merely from the assertion that Γ(S) has (IP)₂. The recovered necessity statement must use the numbered theorem's actual hypotheses, rather than a stronger paraphrase of the abstract.

The source's false claims must remain identified as corrections: the deleted-line parameter in Theorem 6; the residual-connectivity restriction in Lemma 5; the unrestricted neighbor-graph equivalence in Lemma 3(1); the conventional four-edge reading of Lemma 3(4) and Theorem 1; and the specified numerical entries in Figure 2. The existing Hermitian-unital question proof is used without a second claim of solving that conjecture. Neither historical priority nor the present external status of every old question is established by this packet.

## Suggested public wording

“L092's specified main results are recovered in a corrected form: the rank-three applications, the complete higher-rank Steiner classification, and the rank-six M₂₄ construction. The two classifications already quoted by the source remain external inputs. Exact finite computations and selected Lean proofs support the written argument. The identifications of two residues with Pasini's named geometries remain unproved here.”

This supports one additional record of recovered main results if phase208's publication checks pass. It supplies no new conjecture count, no claim that every sentence of L092 follows, and no compression ratio. Any future length comparison must include the complete local proofs and necessary computational inputs and state how the borrowed classifications are treated.
