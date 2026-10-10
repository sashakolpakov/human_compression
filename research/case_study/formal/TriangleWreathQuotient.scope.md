# Uniform triangle-wreath quotient: Lean certificate

Date: 2026-10-10. This is a new private formalization. Earlier manuscripts, source files, and certificates are unchanged.

The module `formal/TriangleWreathQuotient.lean` proves the marked quotient construction for every natural parameter `s`, including the exact ten source relators and an explicit subgroup surjection onto the exact triangle group. The final infinitude theorem has the explicit hypothesis `Infinite (Triangle s)`. The module does not assert or assume a global axiom saying that triangle groups are infinite.

## 1. Exact presentation contract

The primary source is Fernandes–Leemans–Ivić Weiss, *Hexagonal extensions of toroidal maps and hypermaps* (2018), section 8, printed page 17. Specializing the displayed eight-parameter rotational presentation to `((3,0),(2,0),(1,1),(s,0))` gives

\[
P_s=\langle x,y,z\mid x^6,y^3,z^2,(zx)^3,(zy)^6,(x^{-1}y)^2,
(y^{-1}x^{-2})^3,(zx^3)^2,
x^{-1}z(y^{-1}z)^2zx(zy)^2,[y(zy)^2]^s\rangle.
\]

The Lean definition `sourceWord` lists exactly these ten words in that order, with the natural-power spelling `(x⁻¹)^2` for `x^{-2}`. `sourceRels` is their range in the free group on `Fin 3`; `Source s` is its actual `PresentedGroup`. This is not a group supplied together with the target relations as unexplained hypotheses.

Likewise, `triangleWord`, `triangleRels`, and `Triangle s` define the exact group

\[
K_s=\langle d,h,q\mid d^2,h^2,q^2,(dh)^2,(dq)^3,(hq)^s\rangle.
\]

`triangle_relations` derives those six identities from membership in the defining relator set. No exact-order or faithfulness claim is required. The source extraction and the frozen written triangle theorem are hash-bound in the manifest. The transcription was checked against the full presentation on the source's page 17, not inferred from its finite-order table.

## 2. What the kernel checks

The outer group is `(Equiv.Perm (Fin 3))ᵐᵒᵖ`. Its precomposition action `rowAction` gives exactly

\[
[A;p][B;r]=[(A_iB_{p(i)})_i;r\circ p].
\]

With `c = ![2,0,1]`, `v=dqd`, the marked rows are

\[
X=[(d,v,v);c],\qquad Y=[(1,1,1);c],\qquad Z=[(h,q,h);1].
\]

The theorem `nine_fixed` evaluates all 27 coordinates of the first nine words. Its short auxiliary identities are all derived from the five fixed triangle relations by `ten_relators`; none is retained as an additional presentation relation. The proof is generic group algebra. It does not rely on numerical matrices, a finite quotient, the finite-factor Python reducer, or a sampled value of `s`.

`parameter_word` proves the exact equality

\[
Y(ZY)^2=[(hq,1,qh);1].
\]

`pure_pow` and `parameter_relator` then prove the tenth relation uniformly from `(hq)^s=1`. `ten_relators` combines the ten identities. `sourceMap` uses the universal property of the actual source `PresentedGroup`; `sourceMap_generator` proves that it sends the three marked generators to `X,Y,Z` in the stated order.

The formal subgroup is slightly more direct than the subgroup of the image in the written note: `pureKernel s` is the kernel of the source map composed with the outer-permutation projection. Its first-coordinate map `coordinateMap` is proved to be a homomorphism, using its defining kernel condition. Three exact image identities are proved:

\[
X^3=[(d,q,d);1],\quad Z=[(h,q,h);1],\quad Y^{-1}ZY=[(q,h,h);1].
\]

`coordinate_generator_preimage` supplies the corresponding source elements and proves their kernel membership. `coordinateMap_surjective` uses generation of the actual triangle presentation by `d,h,q` to prove surjectivity. Consequently `source_infinite_of_triangle` proves

\[
\operatorname{Infinite}(K_s)\Longrightarrow\operatorname{Infinite}(P_s).
\]

The central declarations `ten_relators`, `sourceMap`, `coordinateMap_surjective`, and `source_infinite_of_triangle` have only the standard dependencies `propext`, `Classical.choice`, and `Quot.sound`. There is no `sorryAx`, native-evaluation axiom, unsafe computation, or user-declared axiom in this module. The two three-point permutation checks use `decide +kernel`.

## 3. Explicit limits

The real-matrix proof that `K_s` is infinite for integers `s≥6` is in the independently reviewed written note `phase38_L003_universal_triangle.md`, section 5. Its trigonometric and spectral steps are not formalized here. They remain the mathematical input needed to obtain unconditional all-`s≥6` infinitude from the formal transfer theorem.

This module does not formalize the four-involution group `U_s`, the flip extending the rotational map to that group, the universal hypertope geometry, or the source's published finite baseline at `s=2,3,4,5`. Those have precisely their previously recorded written or computational status. It does not identify the wreath image with the source group. No new source-compression credit or compression ratio is claimed.

## 4. Reproduction and trust boundary

Run with a fresh output directory:

```sh
python3 phase38_triangle_formal_check.py \
  --packages /Users/sasha/bogachev/formal/.lake/packages \
  --lean /Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean \
  --output-dir /private/tmp/triangle-wreath-review-new
```

The runner checks Lean 4.32.2 and every pinned dependency revision and tracked-file cleanliness in `formal/dependency_manifest.json`. It builds missing dependency objects in a fresh overlay, compiles the new module, checks that its bytes did not change during compilation, and requires the four expected axiom reports. Any axiom outside the standard three causes failure. Existing compiled dependency objects are trusted build inputs; the runner does not rebuild all of mathlib or the compiler.

The authored fresh build passed in the report `phase38_triangle_formal_check.json`, with no Lean warnings. The manifest binds the exact Lean module, runner, report, dependency manifest, primary source assets, and written triangle package. This author build and source-transcription check are not described as an independent reviewer replay.
