# Independent spectral infinitude certificate audit

10 October 2026. Reviewer: `review_unified_seven`, an internal agent who did not author this certificate or its two formal dependencies.

**PASS: complete source/interface review and fresh pinned Lean replay.** The exact formal triangle group, literal rotational source group and fourteen-relator involutory source group are proved infinite for every natural parameter at least six. The final statements have no remaining infinitude, reflection-identity or numerical-specialization hypothesis. The independent replay printed all twelve requested axiom reports; each contains only `propext`, `Classical.choice` and `Quot.sound`.

The reviewed new source is `formal/TriangleReflection.lean`, SHA-256 `6076538072cbbc3bbcdc1b8eb71cd74d2ae4a50cd8276604579e359e98d36636`. The frozen dependencies are `TriangleWreathQuotient.lean`, SHA-256 `9ff4d19715bd716ce46c1bd284b3070fa44e485e17e0115229f3a971e3f93055`, and `TriangleWreathInvolutory.lean`, SHA-256 `bb1821dab93c385a418c0bf3fd84a2e106766e38f2262e28949e2a9be9baca98`. I read their complete sources, the spectral scope note, runner and manifest, and compared their presentation definitions with the frozen written theorem and the primary extraction's section-eight presentation. I did not modify any frozen source or the prepared repository.

## Exact mathematical interface

The first presented group is exactly

`Triangle s = <d,h,q | d²,h²,q²,(dh)²,(dq)³,(hq)^s>`.

Its relator set is the range of those six words in the free group; there is no omitted additional relation or assumed faithful reflection action. The rotational group has precisely the ten source words

`x^6, y^3, z², (zx)³, (zy)^6, (x⁻¹y)², (y⁻¹x⁻²)³, (zx³)², x⁻¹z(y⁻¹z)²zx(zy)², [y(zy)²]^s`.

Substituting the source parameters `(3,0),(2,0),(1,1),(s,0)` into the inspected primary presentation gives this literal list. The involutory group has four square relations, the six pair powers in order `(01,02,03,12,13,23) = (6,3,2,2,3,6)`, and the last four rotational words under `x=r0*r1`, `y=r0*r2`, `z=r0*r3`. Its `Fin 14` relator range is therefore the exact frozen universal-group presentation.

The wreath coordinate action uses precomposition by **opposite** permutations. This gives the intended row convention `(A,p)(B,q)` with coordinate `A_i B_{p(i)}`. In that group, `X=((d,dqd,dqd),c)`, `Y=(1,c)` and `Z=((h,q,h),1)` satisfy all ten words by identities proved from the six triangle relators. The parameter word is the pure tuple `(hq,1,qh)`. None of the auxiliary braid or involution identities is introduced as an unproved hypothesis in the final source map.

The first-coordinate homomorphism is restricted to the actual kernel of the outer permutation action on the source. The words `x³`, `z` and `y⁻¹zy` belong to this kernel and map to `d,h,q`. Presented-group generation gives surjectivity. This proves infinitude of the source via an infinite subgroup; it does not falsely assert a coordinate homomorphism on the full wreath group.

For the involutory source, the pure permutation `F` reverses X and Y and fixes Z. The four generators `F,FX,FY,FZ` satisfy all fourteen words. A separate source kernel and three explicit rotational witnesses give its coordinate surjection. This proof needs neither a formal embedding of the rotational source into the involutory one nor the separately written semidirect-product identification.

## Reflection representation and the parameter relation

The new module defines actual permutations of `Fin 3 → ℝ` by

`D(v)=(-v0+v2,v1,v2)`,

`H(v)=(v0,-v1+t*v2,v2)`,

`Q(v)=(v0,v1,v0+t*v1-v2)`.

Their inverse functions are the same displayed maps, with both inverse laws proved. Ordinary `Equiv.Perm` multiplication composes column actions: `D*H*Q` means `D(H(Q(v)))`. This is deliberately distinct from the outer row convention, and the represented abstract triangle group connects the two correctly.

Coordinate algebra proves the five fixed relators. The sixth is proved uniformly, not assumed. For angle `a`, an explicit linear map P intertwines HQ with rotation through `2a` in a coordinate plane. Its formula is

`P(u)=((4-t²)u0, t*u0+cos(a)u1−sin(a)u2, 2u0+u1)`, with `t=2cos(a)`.

The code constructs a preimage of every vector using division by `4-t²` and `sin(a)`, with both nonzero hypotheses stated and then proved at `a=π/s`, `s≥6`. Induction proves the power intertwining formula; `s*(2π/s)=2π` and the exact trigonometric rotation identity give `(HQ)^s=1`. `PresentedGroup.toGroup` then constructs the actual representation, with its three generator images proved.

## Infinitude for every parameter

Let C be the represented word dhq. Its coordinate action is proved explicitly. If `s>6`, cosine monotonicity on the specified interval gives `t²>3`. The code constructs a real number `r>1` satisfying `r²−(t²−1)r+1=0`, using the explicit positive quadratic root. The exact orbit of `(r,tr,r+1)` is `r^n(r,tr,r+1)`. Its first coordinates are distinct by strict monotonicity of powers with base greater than one.

At `s=6`, the exact cosine value gives `t²=3`. The code proves the full formula for C², then the orbit `(C²)^n(1,0,0)=(n+1,nt,2n)`. Its first coordinates are distinct. Thus the Euclidean boundary case is covered by an explicit unipotent orbit; it is not inferred from the expanding case.

In both cases, the common orbit lemma turns equality of source-group powers into equality of real first coordinates and hence equality of exponents. This gives an injection from the natural numbers into the actual triangle presentation. No diagonalization theorem, characteristic-polynomial oracle, faithful representation assumption or finite sample argument enters the proof.

The two final corollaries install the proved triangle infinitude instance and invoke the frozen subgroup-surjection theorems. A separate fresh `#check` against the compiled modules produced exactly:

```lean
triangle_infinite (s : ℕ) (hs : 6 ≤ s) : Infinite (Triangle s)
rotational_source_infinite (s : ℕ) (hs : 6 ≤ s) : Infinite (Source s)
universal_source_infinite (s : ℕ) (hs : 6 ≤ s) : Infinite (Universal s)
```

The complete qualified output is saved in `phase42_triangle_spectral_audit_interfaces.txt`.

## Fresh replay and trust boundary

I ran the unchanged pinned runner with a new, previously nonexistent output directory:

```sh
python3 phase40_triangle_spectral_check.py \
  --packages /Users/sasha/bogachev/formal/.lake/packages \
  --lean /Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean \
  --output-dir /private/tmp/mc_phase42_triangle_spectral_independent
```

The runner checked Lean 4.32.2, all nine dependency revisions and tracked-file cleanliness. It built four missing mathlib objects in a private overlay and freshly compiled all three project modules. The project compilations took approximately 13.22, 4.80 and 4.79 seconds, respectively; these figures exclude dependency compilation. All exit codes were zero, stderr was empty and there were no warnings. The copied fresh report is `phase42_triangle_spectral_audit_replay.json`, SHA-256 `b67401787ccece4fa939cf480d8efc26b9d773d4e63210619709d2dad3b88db9`.

Every exact printed axiom report is preserved there and parsed into the companion audit JSON: four declarations from each of the three modules. There are no `sorryAx`, native-evaluation or extra axiom dependencies in those declarations. The runner also checked source hashes before and after each compilation; this audit separately checks all frozen manifest bindings. The Lean kernel/compiler, standard axioms, pinned dependency sources and existing compiled dependency objects remain trusted inputs. The latter are not independently reconstructed by this replay.

This passes the complete formal algebraic infinitude claim for all `s≥6`. The written identification with universal regular hypertopes, exact local residue groups and flag geometry remain outside these Lean modules. The published finite baseline at `s=2,3,4,5`, historical novelty, completeness of a conjecture-intake claim and any manuscript-compression factor are likewise outside this audit. No additional source manuscript is admitted merely because this formal gap has closed.
