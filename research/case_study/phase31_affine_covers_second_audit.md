# Independent written review of the affine cover theorem

10 October 2026. Internal mathematical review by the recent-conjectures agent; not external peer review, a priority determination, or a new execution of the author's checker.

Reviewed the final `phase31_affine_covers.md`, SHA-256 `ecd97b2a3eb5fc64f1b790f39ceff291c0c439e3ff7a01d7abf8ad9b797e7b64`, in full. **No mathematical gap found in the stated theorem and scope.** The accompanying JSON binds the exact retained inputs. I had previously reviewed the full phase30 affine construction and its explicit finite seed; that earlier review is retained rather than claimed as a new source audit here.

## Checks that matter to the uniform argument

1. The seed's flag triangulation has circular links, and its exchange-of-6-and-7 character reverses on every adjacent flag. The resulting orientable closed surface has Euler characteristic −6 and genus four. The distinction between a vertex star and its circular link is correct in the final text.
2. A characteristic fundamental-group subgroup is preserved by orientation-reversing homeomorphisms as well as orientation-preserving ones. Hence all seed symmetries lift. One must keep the full group of lifts; neither a chosen splitting nor conformal lifting alone is sufficient. Its free and transitive action on lifted flags follows from the base action and the deck action.
3. Every lifted five-edge block maps bijectively to its base block. Its column span has dimension at most four because of the five-term relation and at least four because it surjects onto the certified base span. The resulting isomorphism proves the asserted local relations without computing the entire lifted code.
4. At an incident lifted vertex-face pair, the intersection injects into the base two-dimensional intersection. The two common lifted edges are independent by their images. Both inclusions and the dimension equality follow. This does not presume subgroup IP or flag transitivity of the eventual affine construction.
5. The vertex-row family and face-row family each have their own zero-sum relation. Their individual rank upper bounds add even if the two row spaces overlap. Therefore the lower bound is (6t+2), not merely (6t).
6. A same-fiber column collision gives a nontrivial deck stabilizer of that column. For a p-group this stabilizer has order at least p. Lifted edge transitivity conjugates such stabilizers, so every base-edge fiber has at most (t/p) distinct columns. The dimension of a vector space spanned by these columns cannot exceed their number. This contradicts the preceding lower bound for p≥5. The argument does not require the deck group to be abelian.
7. Once all columns are distinct, the local span isomorphism proves B2 exactly: a column in a lifted block span must equal the unique column in that block over its base edge. Nonzero columns and different-base-edge separation already follow from the quotient map.
8. The subgroup ([\Pi,\Pi]\Pi^p) is characteristic, and the genus-four abelianization gives deck group (C_p^8). The subsequent affine extension is a specified semidirect product; the preceding lift extension need not split. Their roles are correctly separated.
9. The surviving odd five-term local dependence and the even common square give the same local halving defect as the finite seed. Neither global chamber disconnection nor failure of the narrower source coset-isomorphism claim is inferred. The object counts and odd-part distinction (15p^8) are consistent for every p≥5.

The stated more general numerical criterion retains all necessary seed assumptions, including embedded face boundaries, two common edges at an incident vertex-face pair, local code spans, and the incidence-span conditions. Its inequality is sufficient by the same count. It is not asserted for arbitrary regular maps.

## Trust and reading boundary

This review retains standard surface covering classification and lifting results, explicitly named in the author's note, rather than re-proving topology. The focused finite checker diagnoses the seed only; it does not construct a homology cover or establish the all-prime result by sampling. I read the final evidence description but did not rerun that checker in this review. Other agents' executions remain separate evidence.

The exact statement is a construction theorem from the previously certified finite seed and standard topology. Its comparison with Zhang's inaccessible 2024 covering theorems remains undetermined; see [the bounded intake](phase31_cover_prior_art.md). The source-version restriction to the inspected halving preprint is preserved. This review does not establish novelty, current priority, or the wording of the revised journal article.
