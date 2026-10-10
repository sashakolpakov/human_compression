# All-parameter triangle infinitude in Lean

Date: 2026-10-10. New additive certificate; the phase38 and phase39 group modules remain unchanged.

`formal/TriangleReflection.lean` proves, for every natural `s≥6`,

```lean
triangle_infinite (s : ℕ) (hs : 6 ≤ s) : Infinite (Triangle s)
rotational_source_infinite (s : ℕ) (hs : 6 ≤ s) : Infinite (Source s)
universal_source_infinite (s : ℕ) (hs : 6 ≤ s) : Infinite (Universal s)
```

These are the actual six-, ten-, and fourteen-relator `PresentedGroup` types from the frozen group certificates. The final theorems have no triangle-infinitude hypothesis, no matrix-identity hypothesis, and no unproved axiom. This closes the infinitude input previously left as written mathematics in those two certificates. Their existing conditional theorems are reused without alteration.

## 1. Exact real representation and multiplication convention

Put `θ=π/s` and `t=2 cos θ`. The new module defines the three printed matrices by their column actions on `V = Fin 3 → ℝ`:

\[
D(v)=(-v_0+v_2,v_1,v_2),\qquad
H(v)=(v_0,-v_1+tv_2,v_2),\qquad
Q(v)=(v_0,v_1,v_0+tv_1-v_2).
\]

Each is an actual `Equiv.Perm V`: its displayed action is proved to be its own inverse. Ordinary permutation multiplication composes functions, so `(D*H*Q)(v)=D(H(Q(v)))`, exactly matching matrix multiplication on column vectors. This is separate from the opposite-permutation convention used for the outer row wreath action.

`fixed_relations` proves `D²=H²=Q²=(DH)²=(DQ)³=1` by coordinate algebra. The parameter relation `(HQ)^s=1` is proved as follows, rather than supplied as an assumption.

## 2. Uniform proof of the parameter relation

For a real angle `a`, define

\[
R_a(u_0,u_1,u_2)=
(u_0,\cos(a)u_1-\sin(a)u_2,\sin(a)u_1+\cos(a)u_2).
\]

The module proves `R_a R_b=R_{a+b}`, `R_0=1`, and `R_{2π}=1` from the trigonometric addition formulas. For `t=2 cos a`, define the explicit change of coordinates

\[
P_a(u_0,u_1,u_2)=
((4-t^2)u_0,\;tu_0+\cos(a)u_1-\sin(a)u_2,\;2u_0+u_1).
\]

`HQ_changeCoordinates` proves `HQ(P_a u)=P_a(R_{2a}u)` by coordinate algebra and `sin²a+cos²a=1`. `changeCoordinates_surjective` constructs a preimage using division by `4-t²` and `sin a`, with both nonzero conditions explicit. Induction gives

\[
(HQ)^n(P_a u)=P_a(R_{2na}u).
\]

For `a=π/s` and `s≥6`, the module proves `0<a<π`, hence `sin a>0` and `4-t²>0`; also `s(2a)=2π`. Surjectivity of `P_a` therefore proves the actual permutation equality `(HQ)^s=1` in `parameter_relation`.

`reflection_valid` checks all six triangle relators. `representation` then constructs the homomorphism from the exact `Triangle s` presentation to the real permutation group, with the marked generator images proved explicitly.

## 3. Infinite orbits in both parameter cases

Write `C=DHQ`. Its coordinate formula is proved:

\[
C(v)=(tv_1-v_2,\;tv_0+(t^2-1)v_1-tv_2,\;v_0+tv_1-v_2).
\]

For `s>6`, cosine monotonicity gives `t²>3`. `expanding_root` constructs

\[
\lambda=\frac{t^2-1+\sqrt{(t^2-1)^2-4}}2>1,
\qquad \lambda^2-(t^2-1)\lambda+1=0.
\]

The module directly proves the orbit formula

\[
C^n(\lambda,t\lambda,\lambda+1)
=\lambda^n(\lambda,t\lambda,\lambda+1).
\]

The first coordinates `λⁿλ` are distinct by strict monotonicity of positive powers with base greater than one. This avoids any unproved characteristic-polynomial, diagonalization, or eigenvector-existence step.

At `s=6`, the exact value of `cos(π/6)` proves `t²=3`. The module proves the complete formula for `C²` and then the unipotent orbit

\[
(C^2)^n(1,0,0)=(n+1,nt,2n).
\]

The first coordinates are again distinct. `infinite_of_orbit` lifts either orbit calculation to an injective map from `ℕ` into the source triangle group, using the powers of its actual marked word `dhq`, or its square at parameter six. Thus `triangle_infinite` proves infinitude for every `s≥6`.

The two final source corollaries instantiate the frozen phase38 and phase39 subgroup-surjection theorems with this proved `Infinite (Triangle s)` instance. The four-involution conclusion still uses the direct marked wreath map; it does not require the separate written identification `U_s ≅ P_s ⋊ C₂`.

## 4. Reproduction and scope

Run with a fresh output directory:

```sh
python3 phase40_triangle_spectral_check.py \
  --packages /Users/sasha/bogachev/formal/.lake/packages \
  --lean /Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean \
  --output-dir /private/tmp/triangle-spectral-review-new
```

The runner checks the pinned Lean 4.32.2 and dependency revisions, requires the exact frozen hashes of both group modules, rebuilds all three project modules in a fresh overlay, checks their pre/post source hashes, and requires twelve central axiom reports. Only `propext`, `Classical.choice`, and `Quot.sound` are allowed. The author build report is `phase40_triangle_spectral_check.json`; the manifest binds the exact sources, report, runner, dependency manifest, and mathematical source assets.

The new module uses no finite parameter sampling, native-evaluation axiom, unsafe computation, `sorry`, or declared axiom. Existing compiled dependency objects remain trusted build inputs; neither all of mathlib nor the compiler is rebuilt. An author build is not an independent reviewer replay.

The Lean conclusion is infinitude of the exact presented groups. Identification with the universal regular hypertope geometry and its exact marked local residues retains the prior written proof and dependencies. The source's finite baseline at `s=2,3,4,5`, equality with the wreath image, prior-art priority, and any new compression ratio are outside this certificate.
