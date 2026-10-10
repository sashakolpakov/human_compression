# The direct involutory triangle-wreath quotient in Lean

Date: 2026-10-10. Additive certificate; the frozen phase38 module and all earlier files are unchanged.

`formal/TriangleWreathInvolutory.lean` constructs the marked map from the exact four-involution group `U_s` into the triangle wreath group. It proves that a specified subgroup of `U_s` surjects onto the exact triangle group `K_s`. Its infinitude conclusion is the explicit transfer

\[
\operatorname{Infinite}(K_s)\Longrightarrow\operatorname{Infinite}(U_s).
\]

The real-matrix proof of the hypothesis for integers `s≥6` remains written mathematics in the reviewed phase38 triangle note. No such hypothesis is inserted as a Lean axiom.

## Exact group and marking

`Universal s` is an actual `PresentedGroup` on `Fin 4`. Its `universalWord` has fourteen entries, in this exact order:

| Zero-based indices | Defining words |
|---|---|
| 0–3 | `r₀²`, `r₁²`, `r₂²`, `r₃²` |
| 4–9 | `(r₀r₁)⁶`, `(r₀r₂)³`, `(r₀r₃)²`, `(r₁r₂)²`, `(r₁r₃)³`, `(r₂r₃)⁶` |
| 10 | `(y⁻¹x⁻²)³` |
| 11 | `(zx³)²` |
| 12 | `x⁻¹z(y⁻¹z)²zx(zy)²` |
| 13 | `[y(zy)²]ˢ` |

The convention is exactly `x=r₀r₁`, `y=r₀r₂`, `z=r₀r₃`. The last four entries call the frozen `sourceWord` at indices 6–9 with these rotations; they therefore reuse the literal already checked expressions, including `(x⁻¹)^2` as the natural-power spelling of `x⁻²`.

This contract matches section 1 of `phase35_L003_all_universal.md` and the direct involutory construction in section 4 of `phase38_L003_universal_triangle.md`. The underlying rotational words were specialized from the primary paper's section 8, printed page 17, as bound in the phase38 formal package. The Lean theorem is algebraically valid for every natural `s`; the geometric identification in the retained manuscript has its stated `s≥2` scope.

## Checked construction

The imported frozen module constructs `K_s`, the row wreath group, and

\[
X=[(d,dqd,dqd);(2,0,1)],\quad
Y=[(1,1,1);(2,0,1)],\quad Z=[(h,q,h);1].
\]

The new module defines `F=[(1,1,1);(2,1,0)]` and checks

\[
F^2=1,\qquad FXF=X^{-1},\qquad FYF=Y^{-1},\qquad FZF=Z.
\]

The marked images are `R₀=F`, `R₁=FX`, `R₂=FY`, `R₃=FZ`. The generic group theorem `universal_relators_of_reversal` proves all fourteen relations from the already proved ten rotational relations and these reversal identities. In particular, the `13` and `23` Coxeter words reduce to powers of `(ZX)⁻¹` and `(ZY)⁻¹`; the four extra words are transported with their exact ordered rotation marking. `universalRows_valid` instantiates this theorem with the explicit wreath rows, and `universalMap` invokes the universal property of the actual fourteen-relator presentation.

`universalMap_rotation` proves that the three source rotations map to `X,Y,Z`. `universalKernel` is the kernel of `universalMap` followed by the outer-permutation projection. `universalCoordinate` is a proved homomorphism from that subgroup to `K_s`, taking the first coordinate.

The preimages of `d,h,q` are respectively the source words `x³`, `z`, and `y⁻¹zy`. Their exact wreath images and their kernel membership are checked. Generation of the actual triangle `PresentedGroup` then proves `universalCoordinate_surjective`, and `universal_infinite_of_triangle` follows.

This proof constructs the direct involutory map. It does not use or assume the separate identification `U_s ≅ P_s ⋊ C₂`, reflection invariance of an orientation-preserving normal closure, or an embedding of `P_s` into `U_s`.

## Verification and remaining boundaries

The four new central declarations `universalRows_valid`, `universalMap`, `universalCoordinate_surjective`, and `universal_infinite_of_triangle` have only `propext`, `Classical.choice`, and `Quot.sound` as axiom dependencies. All displayed group relations and finite permutation identities are kernel checked. There are no unproved placeholders or native-evaluation axioms.

The phase39 runner rebuilds both the unchanged phase38 module and the new module against the pinned Lean 4.32.2 dependencies. It rejects a changed hash for the phase38 source, checks both modules' pre/post compilation hashes and all eight required axiom reports, and writes only to a fresh output directory:

```sh
python3 phase39_triangle_involutory_check.py \
  --packages /Users/sasha/bogachev/formal/.lake/packages \
  --lean /Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean \
  --output-dir /private/tmp/triangle-involutory-review-new
```

Existing compiled dependency objects remain trusted inputs; the runner does not rebuild the entire compiler or mathlib. The authored fresh build report is `phase39_triangle_involutory_check.json`, and the manifest binds the exact source, runner, report, and retained inputs. A successful author replay is not described as an independent reviewer replay.

The real/complex argument proving `K_s` infinite for `s≥6`, universal hypertope geometry, exact local residue orders, and the published finite baseline at `s=2,3,4,5` retain their previously stated written or computational status. No exact order of a marked image, equality between `U_s` and its wreath image, or new compression ratio is asserted by this certificate.
