# Independent review of the expanded-end odd cover

10 October 2026. **PASS for the exact fixed affine construction and the written uniform Γ2 theorem, including existence of a second minimal regular cover and the stated universal-kernel join equality. No mathematical correction is required.** The conclusion is conditional on the explicitly retained source-family and geometric interfaces. Historical novelty, current openness, the other tight families and the general conjecture are not certified.

The frozen author manifest is SHA256 `f5273849cf506f08aab9180ddbf77a969ea26821604d3ec6e8468bd14bda21b8`; theorem `70bbc104a49bdceec6dc3c3aea623c35d40c0539e1e02857b89feedd77eab030`; program `a347b61ecb82779d490441809dae37dbf2423d9c2bc0f9f4ca1d7d5071827075`; complete certificate `46241387a3ca13b92650390e97cd41e818e5a88c546d87cebd080a8fd26d36c6`. I read the entire theorem, program, six-row ledger and control code, checked all 25 original file bindings plus the manifest, and preserved every author file. No public file was edited.

## 1. Exact result and scope

For the Cunningham–Pellicer Γ2 row, q=2^β, β≥5, and each independent pair of signs, let G be the full reflection group of the smallest regular maniplex. The reviewed predecessor interface gives |G|=256q and a normal cyclic group N=<(r1r2)^4> of order q/4 contained in the medial group. The quotient G/N is the fixed marked group D of order 1024.

The admitted construction gives a finite regular polytopal marked cover H->G of type **{24,q,24}**, kernel **C3^130**, full order **256q·3^130**, two end kernels **C3^17**, and an injective medial projection. A finite polytopal quotient Q of H is a minimal regular cover of the original chiral polytope, with degree **3^d**, **1≤d≤130**, over G. It differs from the retained degree-two minimal cover S. The proof does not specify d or a normal subgroup selecting Q, and does not assert that H itself is minimal.

The two explicit admissible kernels for H and S in the universal marked string group have product equal to the kernel defining G. Thus the join of all finite admissible universal kernels is that kernel for this family. This statement is about the stated normal-kernel lattice; it does not assume their mix is polytopal or identify a join of unrelated quotient groups.

## 2. Affine semantics and finite completeness

The author's right-action convention is `(v,g)(u,h)=(v^h+u,gh)`, with right cosets `<r0>g` and `<r3>g`. The code's permutation composition applies the first permutation and then the second, consistently with that formula. All four shifts agree with the two literal coset differences, and the involution and three nonadjacent commutation equations hold before quotienting. They are not inferred just from projected relations.

The affine kernel lemma is sound. Differences of two lifts over the same base element are actual translations; saturating the complete representative-edge differences under the corresponding base generators therefore remains within the actual kernel. Schreier rewriting supplies the converse. The quotient subspace M is the orbit span of the actual translation of `(h1h2)^4`, which projects to identity. Hence M lies in the full kernel L and is invariant. The dimension subtraction 257−127 is therefore justified.

The intersection proof correctly includes both obligations: exact translation-space intersection after quotienting by M, and incompatibility of affine fibers over every unwanted projected element. In particular, the top projected intersection has order 16 while its medial subgroup has order eight. The author excludes **all eight** extra elements using nonzero remainders; it does not apply a projected-IP shortcut to this nonpolytopal base. Quotient dimensions are computed from sums with M, so no invalid inference from an unquotiented intersection occurs.

The two local rank-three intersection tests, together with the distinct nonidentity projected involutions, establish the endpoint C-groups. The top test then proves full string IP by the recursive theorem. I independently derived a complete subgroup proof of this recursion before reading the mutable construction; that preparation is preserved separately and is consistent with the frozen argument.

## 3. Independent exact recomputation

My checker imports **none** of the author's program. It reconstructs the finite permutation group and module from the bound model, using lexicographic group/coset labels and reversed-generator transversals. Arithmetic uses two integer bit planes for exact F3 addition and highest-coordinate elimination, instead of the author's sparse coefficient dictionaries and lowest-coordinate pivots.

For every one of the **16** marked subsets, I compute the actual Schreier-loop translations `h_g rho_i h_(g rho_i)^(-1)`. Under the right-action convention the representative difference must be acted on by the inverse of the destination base element; the checker explicitly does this. Their span is the entire kernel by direct Schreier generation, so my calculation does not rely on the author's invariant-closure procedure. Invariance is checked separately. The full finite action is verified against every generator edge of the base group.

I then test affine compatibility and translation intersections for **all 136 unordered subset pairs**, including equal and empty subsets. Every pair passes IP. This is stronger finite checking than the three sufficient recursive pairs in the author's program.

| Marked subgroup | Projected order | Raw kernel dimension | Kernel dimension after quotient |
|---|---:|---:|---:|
| 01 | 16 | 1 | 1 |
| 12 | 8 | 1 | 0 |
| 23 | 16 | 1 | 1 |
| 012 | 128 | 33 | 17 |
| 123 | 128 | 33 | 17 |
| 0123 | 1024 | 257 | 130 |

The killed orbit space has dimension 127. Exact adjacent orders are 24,4,24, checked against every smaller positive power. After translating the author's documented coordinates into mine, the full kernel, killed space and every published local basis span exactly the independently computed spaces. All eight published separating remainders are nonzero modulo the independent comparison space and represent the correct defect classes; their base-element list is complete.

The independent computation passed in **1.0043151249410585 seconds**. Its detailed report lists all 16 parabolics and all 136 pair checks. The whole giant affine group is never enumerated. The fixed 1024-element base **is** enumerated; the author's broadly named certificate flag `no_group_order_enumeration_or_floating_point` must be read in the manuscript's stated sense of no enumeration of the enormous affine cover, not as a denial of this finite base enumeration.

## 4. Uniform transport: generation and local IP checked separately

The all-parameter proof is valid and does not interpolate finite examples. Let the changing G act through D on E/M. The generated affine group projects onto G and onto the already certified fixed Hbar. For n in N, any lift `(v,n)` has cube `(0,n^3)` because N acts trivially and the vector group has exponent three. Every element of the cyclic 2-group N has a cube root in N. Thus the marked generated subgroup contains the entire standard copy of N and is the full preimage of Hbar. This establishes the claimed kernel and order, rather than assuming that a generated subgroup equals an ambient fiber product.

The same argument applies to the two ends and the medial subgroup because N lies in all three. Their full-preimage descriptions give the top endpoint intersection and the injective medial projection. The local rank-three checks require an additional step, which the manuscript supplies: the retained old end IP gives N intersect G01 contained in <r1>, and the dihedral rotation/reflection decomposition makes that intersection trivial. Likewise N intersect G23 is trivial. Hence H01 and H23 map isomorphically to their fixed counterparts. Their intersections with H12 then lift the already certified common involutions. This proves local and global IP uniformly.

The pair-group isomorphisms preserve the two endpoint product orders 24, while H12≅G12 gives middle order q. The end kernel dimensions remain 17. Neither this transport nor the finite certificate assumes both end projections are injective: they are expressly not injective, which is why the result is consistent with the earlier local-faithfulness obstruction and classification.

## 5. Minimal descendants and join equality

The finite-descent argument selects an inclusion-maximal normal subgroup J of ker(H->G) whose quotient is polytopal. Identity is admissible and there are finitely many subgroups. Any further regular polytopal cover of the original chiral polytope below H/J maps to its smallest regular maniplex G, by the retained universal property, and therefore corresponds to a larger admissible normal subgroup of H inside that kernel. Maximality excludes it.

The resulting degree is an odd divisor 3^d of 3^130. It cannot be one because G fails IP. The existing cover S has degree two, so the two covers have different group orders; no marked epimorphism from the odd-degree cover onto S over G is possible. This proves the existence of a distinct minimal cover without pretending to have explicitly computed its minimal normal kernel.

For the join, J_H and J_S are normal in the same universal marked group and contained in K0=ker(F->G). The index of their product in K0 divides both 3^130 and 2, hence is one. The universal property ensures every other finite regular-cover relation kernel is also contained in K0. This proves the stated join equality with no assumption that all pairwise mixes or quotients retain IP.

The separately reviewed phase105/107 Lean package formalizes general divisibility and finite-maximality statements relevant to this last reasoning. It is not a proof dependency of the frozen phase102 package and does not formalize the affine construction, its IP or the geometric correspondence.

## 6. Source contract, attribution and retained costs

I freshly checked the retained Γ2 presentation, β≥5 and independent-sign scope against Table2 and the complete Theorem4.8 passage and proof of the bound arXiv:2009.04566v1 extraction. The actual theorem states all four sign pairs and every β≥5. Its atomic-family construction, existence, tight order and normal forms, marked orders, chirality and IP remain borrowed mathematical inputs; phase102 does not reprove that classification.

I reread the needed phase58 mirror-mix, local-end and double-cover derivations and phase66's entire fixed-quotient proof. Their exact phase73/74 independent PASS packages remain retained, including the marked identification of the bound 128-point action. No new source-parameter GAP census was run or needed here: the uniform presentation theorem and the previously reviewed model identification supply the parameter bridge.

I also read the complete relevant §4 and Example3.5 in Cunningham's bound July2023 author extraction. They provide the earlier finite two-minimal-cover example, the prime-degree minimality observation, the five-family multiplicity conjecture and the broader question. The source construction and this earlier question/strategy must keep their attribution. The new affine module and uniform cover argument are repository derivations; that phrase makes no historical-priority claim. No new comprehensive literature search has certified that the stated family result was previously unknown or remains open in all later literature.

The retained geometric background is the marked group/polytope correspondence, recursive string-C recognition, regular-cover/normal-quotient correspondence and smallest-regular-maniplex universal property. The exact program, complete 1,115,038-byte certificate, fixed model and source interfaces are required proof costs. They must not be replaced by the numerical summary alone. This standalone theorem adds no source to a main-result compression assembly and supplies no compression ratio.

Only the stated Γ2 family is covered. No classification of expanded-end covers, explicit selection of Q, multiplicity for Γ3 or Γ4 and its dual, or general-conjecture resolution follows from this audit. The optional edge-chain/surface motivation is not used in the admitted proof.

## 7. Replay, integrity and portability

The author's unchanged optimized-Python checker freshly regenerated its entire certificate byte-for-byte in **0.8467814589384943 seconds**. I also copied only its program, fixed model and expected certificate into a separate isolated directory, then ran from an unrelated working directory. That reproduction passed in **0.932097457931377 seconds**, with the same certificate and empty stderr. The finite author checker requires no private primary PDFs or other study files.

The author's control program was freshly rerun against my fresh successful output: five certificate mutations (shift, medial word, basis, dimension, separating remainder) and one changed-model hash were all rejected before output creation. Existing directory, ordinary file and dangling-symlink outputs were refused; both successful output files were preserved. These are fresh executions of author-written controls, distinct from my independently written mathematical checker.

The author's runner binds its model and compares the expected certificate when that option is supplied; it does not itself validate the complete outer theorem/ledger/source manifest. I separately verified that outer manifest before and after review. My independent checker performs that full binding check, including private source bindings, so its full audit replay needs those private assets; its finite arithmetic itself uses only the model and certificate. None of those source PDFs/fulltexts is in the review export allowlist.

All frozen originals remain unchanged. The separate final audit manifest binds the preparation, independent checker/report, fresh author replay and controls, portability record and this mathematical/source assessment. The conclusion is a finite-computational and written mathematical PASS within the stated retained contract, not a claim of an entirely Lean-verified family theorem or of publication priority.
