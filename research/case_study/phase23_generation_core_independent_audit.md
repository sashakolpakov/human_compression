# Independent review of the phase23 generation core

Date: 10 October 2026. **PASS:** no mathematical gap found in the complete written argument at SHA256 `5fcb82d72b937e826bc3bdfe6f7bc5f39f746993fdfc3ae751d98bfb4d4455cf`.

This is a separate mathematical/code review by the survey-audit agent, followed by a fresh scratch execution of the unchanged author's checker. It is not external peer review or a second implementation of the finite diagnostic. The proof and historical report were not edited.

## Mathematical points checked

1. **Kernel versus complement.** In Theorem A, `D∩R` is invariant under the whole projected group because `R` is abelian. A trivial intersection gives a genuinely unique lift for every projected element, hence a cocycle. A full intersection gives the full semidirect product. Coboundary conjugation is by an element of `R`; no finite-group or semisimplicity assumption is hidden here.

2. **Product cohomology, including infinite groups.** Lemma B uses a finite basis of `W` to identify arbitrary cochains into `V⊗W` with the tensor product of cochains. Finite-dimensional `W` is sufficient even if the group and the cohomology space are infinite. The `H` action is on the second tensor factor, and its fixed tensors vanish because `W^H=0`. After subtracting a coboundary, the mixed commuting identity forces the remaining `H` cocycle into `M^G=0`. This proves the stated vanishing for abstract groups over any field.

3. **Additive irreducibility and all-field scope.** The double-root difference in (3.1) isolates one matrix unit without assuming that an invariant additive subgroup is already an `F`-space. Varying a root parameter supplies all its scalar multiples, and determinant-one signed coordinate permutations supply every unit. This also works in characteristic two and over infinite fields. The full product projection remains an explicit hypothesis. A radical conjugate of the block-diagonal complement cannot contain a unipotent with nilpotency index greater than the larger block dimension.

4. **Frobenius-coupled splitting.** I independently recomputed all four equations (4.2) and their weights (4.3). Averaging over the finite torus gives a complement whose two weight sets are disjoint; the Weyl element preserves each set under inversion. The lower-right off-block entry is additive first, then the other entries become additive in the stated order. Uniqueness of linearized-polynomial coordinates justifies the weight test for all additive maps. The integer inequalities establish the exact nonresonance range; the excluded characteristic-three endpoint weights really equal `2p^j`.

5. **Characteristic-three nonsplitting.** The cube subspace of `Sym³` has the claimed Frobenius action. Its quotient is natural after the displayed sign change. The order-three root has Jordan type `(3,1)`, so this extension cannot split into two two-dimensional factors. Duality and the `3^(m−1)` twist produce the precise two exceptional coefficient modules, including their overlap at `m=2`. No complete classification of `H¹` or claim about its dimension is required.

6. **Unitary direct summand.** The skew-Hermitian projection is equivariant and additive; its lack of `E`-linearity does not obstruct applying it to a coboundary. The norm/trace argument establishes additive irreducibility of the Hermitian space, using only repeated prime-field scalar addition, not an unproved full-field closure. Theorem D applies to `(m,f)=(2e,e)` exactly except at `q=3`.

7. **Explicit exceptional complement.** Independently expanding the cubic representation gives diagonal blocks `bar(g)` and `D0*g*D0`, and the stated `D3(g)`. Dualizing, swapping blocks and conjugating the first block by `S0` yields exactly `c0(g)=-g*S0*D3(g)^t`. Projection therefore remains a cocycle. At `x(1)`, the displayed skew part and off-block yield the nonzero square `-E11` in the upper-right block and zero cube. The projection is faithful onto `SL2(9)`, so the image has trivial radical intersection. This is a counterexample to the general parabolic criterion at `q=3`, not to the separate frozen finite rank-three construction.

## Execution and source scope

The full checker was inspected and run from `/private/tmp/phase23-generation-review`, using unchanged source SHA256 `0c0609f634e9509634c406c5fbd7e7d4d9329c3ea55e1c916c40ee26e3abd722`. All 22 check groups passed. The fresh report matches the saved author report in every field except the execution timestamp.

The concrete scope is 5,184 cocycle equations over `F2`, a four-dimensional zero first-cohomology calculation, the cubic identities, every one of the 720 explicit `F9` complement matrices, 2,880 products by a verified generating set, and 2,880 integer parameter triples. Checking products by a generating set suffices to validate the displayed representation on the whole enumerated group. These are finite diagnostics; the all-field and all-parameter results are supported by the written proofs.

I also directly reopened the primary [Grazian–Parker–Semeraro–van Beek manuscript](https://arxiv.org/html/2502.20873v2), reading Lemma2.4 and its proof, Lemma5.6 and its proof, and Proposition5.7 and its proof. Those passages support treating the polynomial extension and adjacent-twist phenomena as established context. I reopened the setup and Theorem5.1 of [Korhonen's paper](https://arxiv.org/html/1712.03861); its algebraic-group extension statement is context, not a replacement for the finite-group proof. I did not read the original Andersen–Jørgensen–Landrock paper or perform an exhaustive priority search.

The note correctly limits compression to the additive-kernel/complement steps in the two prior generation arguments. Diagonal-image surjectivity, the relevant matrix word, ambient root extraction, determinant class, and the intersection property remain separate. No additional whole-paper reduction, new polytope-existence result, or formal proof certificate follows from this review.
