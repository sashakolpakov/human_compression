# The marked parity mix: exact formal scope and proof

Author freeze prepared on 10 October 2026 for independent review. This is the group-theoretic parity-mix construction used in §1 of `phase124_even_label_mix.md`, in the question track **Equal-label polytopes and quadratic symmetries**. The written construction was already reviewed in phase131. This package supplies Lean proofs of its actual generated fibers, component profiles, and full intersection property. It does not replace the written source-specific finite-field arguments.

The package contains twelve new Lean files and fifty explicitly printed declarations. Those are build and audit counts, not counts of new mathematical discoveries. The main result is one construction theorem, with its supporting group, coordinate, and interval interfaces. Six unchanged local dependencies are freshly recompiled and contribute twenty-five existing printed declarations. Every reported dependency is among `propext`, `Classical.choice`, and `Quot.sound`. No target mixed intersection property, parity-profile equality, or interval-forest assertion is accepted as an unproved premise of the final theorem.

## 1. Exact construction theorem

Let (n\geq 0), let (E,G) be groups, and let
\[
 e_i\in E,\qquad g_i\in G\qquad(0\leq i<n).
\]
For a support (S\subseteq\{0,\ldots,n-1\}), write
\[
 E_S=\langle e_i:i\in S\rangle,\quad
 G_S=\langle g_i:i\in S\rangle,\quad
 H_S=\langle(e_i,g_i):i\in S\rangle\leq E\times G,
\]
and let (H=\langle(e_i,g_i):0\leq i<n\rangle). The exact hypotheses of `marked_parity_mix_intersection` are as follows.

1. Every element (x\in E) satisfies (x^{2^k}=1) for some natural number (k), which may depend on (x). This is Mathlib's `IsPGroup 2 E` predicate. A finite two-group satisfies this predicate, but finiteness of either ambient group is not a premise here.
2. (e_i^2=g_i^2=1) for every index. These equations alone allow identity elements; the character hypothesis below rules them out when an index is present.
3. There are actual homomorphisms \(\varepsilon:E\to A\) and \(\delta:G\to A\), where (A) is a commutative group, and an element (t\ne1) such that \(\varepsilon(e_i)=\delta(g_i)=t\) for every (i). Their existence and their values on the generators are hypotheses. When (n>0), the involution equations force (t^2=1); no independent assertion that a desired character exists is hidden in the proof. The usual source application takes (A=C_2).
4. Every adjacent product (g_i g_{i+1}) has odd order. In Lean, this is `Odd (orderOf (g i * g j))` under `i.val + 1 = j.val`. Since Mathlib assigns order zero to an infinite-order element, the oddness premise implies finite odd order.
5. Distant generators commute in each factor: if (i+1<j) or (j+1<i), then (e_i e_j=e_j e_i) and (g_i g_j=g_j g_i).
6. Both factor markings satisfy the full intersection property:
\[
 E_S\cap E_T=E_{S\cap T},\qquad
 G_S\cap G_T=G_{S\cap T}
\]
for all finite supports (S,T).

Then
\[
                         H_S\cap H_T=H_{S\cap T}
\]
for every pair of supports. This is proved for the literal generated subgroups of (E\times G), and then transported through the injective subtype map to the corresponding marked subgroups of (H) itself (`intrinsic_parity_mix_intersection`). Ambient generation of (E) or (G) is not required in this statement: only their distinguished parabolics are used.

Three accompanying statements prove that the literal paired generators generate (H), are nonidentity involutions in (H), and satisfy the string commutation relations. Thus all the group-theoretic marking conditions are established. The package does not define or construct an abstract polytope; that correspondence remains a separate classical input. Empty supports, empty component index types, and (n=0) are included in the formal statements. The nonidentity statement is quantified over actual indices and is consequently vacuous at rank zero.

## 2. Connected fibers are derived from the group hypotheses

The first stage does not use the factor intersection properties. It proves a more general connected-graph statement with a possibly noncommutative character codomain. Suppose the (e_i) generate (E), the (g_i) generate (G), the marker graph is connected from a chosen vertex (i_0), and every edge product (g_i g_j) has odd order. Under the same two-primary, involution and genuine-character hypotheses,
\[
 H=\{(x,y)\in E\times G:\varepsilon(x)=\delta(y)\}.
\]
This is `connected_parity_fiber`. The right-hand subgroup is the existing `fiberProduct` definition; its equality with (H) is proved here.

To begin, if ((x,y)\in H), choose (k) with (x^{2^k}=1). If (y) has odd order, then (2^k) is coprime to that order. A power of (y^{2^k}) therefore equals (y), so taking the corresponding powers of ((x,y)) puts ((1,y)) in (H). Applying this to adjacent paired products isolates ((1,g_i g_j)). Along a path these products telescope because (g_j^2=1). Consequently ((1,g_{i_0}g_i)\in H) for every (i), and multiplication by ((e_{i_0},g_{i_0})) gives ((e_{i_0},g_i)\in H).

Closure induction on the actual generating family of (G) now proves that every (y\in G) has a companion (x\in\{1,e_{i_0}\}) with ((x,y)\in H). This two-element set is closed under the necessary multiplication and inversion because (e_{i_0}^2=1). Every element of (H) has equal character values in its two coordinates. If \(\delta(y)=1\), the companion cannot be (e_{i_0}), since \(\varepsilon(e_{i_0})=t\ne1\). Hence ((1,y)\in H) for every (y\in\ker\delta).

Projection of the actual generated group (H) onto (E) is surjective because its projected generators generate (E). Given a pair ((x,y)) with equal character values, choose ((x,v)\in H). Then (v^{-1}y\in\ker\delta), so multiplication by the pure element ((1,v^{-1}y)) produces ((x,y)). The reverse containment follows immediately by applying the characters to the paired generators and closing under the group operations.

For a nonempty interval (C\subseteq\operatorname{Fin}(n)), the local marker families generate the actual groups (E_C,G_C) by definition. The restricted first group is still two-primary. Its consecutive-index graph is explicitly proved connected in `interval_path`; reverse edges preserve the odd-order condition because the reverse product is the inverse of the forward product. The connected theorem therefore gives
\[
 H_C=\{(x,y)\in E_C\times G_C:\varepsilon(x)=\delta(y)\}.
\]
The empty interval is handled directly: all three generated groups are trivial. This yields `interval_support_profile` for every interval, including the empty one.

The isolation argument uses elementary coprime powers, not an assumed common-quotient classification. It is a direct proof of the particular classical subdirect-product consequence needed here; no historical novelty is claimed for that argument.

## 3. Components and their genuine coordinates

`supportComponents S` is defined from the actual order-connected components of (S\subseteq\operatorname{Fin}(n)). The code proves that these finite subsets cover (S), are pairwise disjoint and nonempty, and are order-connected. It also proves that indices belonging to different components are separated by at least one missing index. The source string relations consequently imply commutation of markers in different components.

The assembly map
\[
             \prod_C E_C\longrightarrow E_S
\]
is constructed as a group homomorphism using the commutation of distinct component subgroups. Its range is (E_S), since it contains every distinguished generator on (S). For injectivity, the full input intersection property gives
\[
 E_C\cap\left\langle E_D:D\ne C\right\rangle=1.
\]
This is stronger than mere pairwise trivial intersection; the proof establishes independence from the union of all other supports. Together with commutation it gives the injectivity of the assembly map. The same construction applies to (G). The resulting inverse component maps are actual homomorphisms, not formal coordinate labels.

The mixed group also has a component assembly map. The coordinate projections commute with assembly, as proved in `componentAssembly_map`. Surjectivity of the mixed assembly and uniqueness of the two factor coordinate decompositions prove
\[
 (x,y)\in H_S
 \quad\Longleftrightarrow\quad
 (x_C,y_C)\in H_C\text{ for every component }C,
\]
where (x=\prod_Cx_C\) and (y=\prod_Cy_C\) are their unique component decompositions. Applying the interval fiber theorem to each (C) gives the exact profile
\[
 (x,y)\in H_S
 \quad\Longleftrightarrow\quad
 \varepsilon(x_C)=\delta(y_C)\text{ for every }C.
\]
The theorem `canonical_mixed_parity_profile` supplies this conclusion directly from the original group hypotheses for every finite support. The intermediate `mixed_membership_coordinates` uses the same proved profile with the explicit inverse coordinate homomorphisms.

A refinement lemma is needed before the overlap argument can use character equations. Suppose pairwise disjoint fine supports (D_a) refine pairwise disjoint coarse supports (C_b), with specified parent (b(a)). A coarse coordinate homomorphism restricts on (E_{D_a}) to the inclusion if its coordinate is (b(a)), and to the trivial homomorphism otherwise. This follows by applying the injective coarse assembly map to a tuple supported on one coordinate. Applying the character to an assembled fine tuple therefore gives
\[
 \varepsilon\bigl(\operatorname{coord}_{b}(\prod_a x_a)\bigr)
       =\prod_{a:b(a)=b}\varepsilon(x_a).
\]
This is `component_coordinate_refinement`. The analogous equality holds for \(\delta\). Commutativity is required of the character codomain at this stage so that the finite products may be collected by their parent. The groups (E) and (G) themselves may be noncommutative.

## 4. The full intersection argument

Take (z=(x,y)\in H_S\cap H_T). Projection and the two factor intersection properties first give (x\in E_{S\cap T}) and (y\in G_{S\cap T}). Let \((L_c)_c\) and \((R_d)_d\) be the interval components of (S) and (T). The sets
\[
                        D_{cd}=L_c\cap R_d
\]
are intervals, are pairwise disjoint, and cover (S\cap T). Empty entries are permitted. Distinct fine supports have commuting generators because their first or second parent differs. The already proved component assembly maps therefore give actual fine coordinates (x_{cd},y_{cd}).

Membership in (H_S), its exact component profile, and the refinement theorem give, for each (c),
\[
              \prod_d\varepsilon(x_{cd})=\prod_d\delta(y_{cd}).
\]
Membership in (H_T) gives the corresponding equality for each fixed (d). These equations are derived in `refined_character_equality`; they are not assumptions of the final intersection theorem.

Regard the commutative group (A) additively and put
\[
 w(c,d)=\operatorname{ofMul}\bigl(\varepsilon(x_{cd})\delta(y_{cd})^{-1}\bigr).
\]
The preceding identities say that every row and every column has sum zero. If (L_c\cap R_d=\varnothing), both fine parabolics are trivial and (w(c,d)=0). The retained theorem `fin_weights_eq_zero` now implies that every weight is zero.

That retained theorem has its own complete Lean proof. It does not accept an interval-forest hypothesis. It considers only nonzero weights, chooses an incident interval of least right endpoint, and proves that its nonzero neighbors must all contain that endpoint. Disjointness within the opposite family leaves a single such neighbor; the row or column equation then contradicts that edge being nonzero. The natural-number interval theorem permits any additive commutative monoid, and the separately proved `Fin n` adapter transports the interval and disjointness conditions, including rank zero.

It follows that \(\varepsilon(x_{cd})=\delta(y_{cd})\) for every fine component. The interval fiber theorem puts each ((x_{cd},y_{cd})) in (H_{D_{cd}}). The mixed assembly profile then puts (z) in (H_{S\cap T}). The opposite containment follows from monotonicity of generated subgroups. This completes `parity_overlap_intersection`; the canonical component construction supplies all its premises in `marked_parity_mix_intersection`.

## 5. Formal interfaces and retained inputs

| File | Explicit reports | Role |
|---|---:|---|
| `ParityMix.lean` | 6 | Actual connected parity fiber by coprime isolation and closure induction |
| `ParityMixComponents.lean` | 6 | Component range, independence, injectivity and homomorphism compatibility |
| `ParityMixLocal.lean` | 3 | Actual local generators, local-to-ambient mix and connected support profile |
| `ParityMixProfile.lean` | 1 | Mixed component membership derived from the two factor decompositions |
| `ParitySupportIntervals.lean` | 9 | Canonical support intervals, coverage, disjointness, paths and separation |
| `ParityMixFiniteProfile.lean` | 5 | Source-hypothesis interval fiber and all-support parity profile |
| `ParityComponentCoordinates.lean` | 4 | Actual inverse coordinate maps and refinement character formula |
| `ParityMixCoordinateProfile.lean` | 1 | Membership expressed using actual inverse coordinates |
| `ParityOverlapGrid.lean` | 4 | Coverage, disjointness, commutation and interval structure of overlaps |
| `ParityRefinementCharacters.lean` | 4 | Derived row/column character equations and additive defects |
| `ParityMixIntersections.lean` | 2 | Projection membership and the overlap intersection theorem |
| `ParityMixTheorem.lean` | 5 | Source-hypothesis ambient/intrinsic IP, generation and marked string involutions |

All new declarations use namespace `MathCompression.ParityMix`. `phase146_parity_mix_dependencies.json` records the exact module imports, explicit report names and original written consumer. A printed report can cover helper declarations through its proof dependencies; fifty is the count explicitly requested from Lean, not a claim that the source contains only fifty declarations.

The local retained build dependencies are `CoprimePullback.lean`, `LiftCertificate.lean`, `CoordinateKernels.lean`, `SupportedKernelGeneration.lean`, `IntervalOverlapCancellation.lean`, and `FinIntervalOverlapCancellation.lean`. The actual new proof uses the existing fiber-product definition, the marked-subgroup definition and its monotonicity/map lemmas, and the proved interval cancellation. It does **not** invoke the coprime-kernel pullback theorem or the supported-kernel construction theorem. The larger imported files, including their transitive dependencies, are nevertheless charged and rebuilt in full. Their old statements are not counted as new parity-mix results.

Mathlib supplies the standard group closure, order-of-element and coprime-power machinery, two-primary subgroup inheritance, commuting subgroup products and their independence criterion, finite products, and order-connected components. These are retained library inputs, with versions pinned by `formal/dependency_manifest.json`. The dependency cache and installed Lean compiler remain in the trust boundary; this replay is not a from-source rebuild of all Mathlib.

The present package reworks the already written parity-mix proof rather than presenting that written argument as a new discovery made by the compiler. The interval cancellation and its finite-index adapter were authored and checked separately in phases149 and154, then admitted by the root review in phase155. Their exact frozen sources are retained unchanged. Independent review of those components does not by itself review this consumer's bindings; phase146 still requires its own independent review.

## 6. Verification and portability

From a directory containing this package and its declared retained formal sources, run:

```sh
python3 -B -O phase146_parity_mix_check.py \
  --packages /path/to/pinned/.lake/packages \
  --lean /path/to/lean \
  --output-dir /path/to/new/parity-build

python3 -B -O phase146_parity_mix_controls.py \
  --packages /path/to/pinned/.lake/packages \
  --lean /path/to/lean \
  --output-dir /path/to/new/parity-controls
```

The wrapper checks exact local source and dependency-manifest hashes, the pinned compiler version, dependency revisions and tracked cleanliness. It then freshly compiles all eighteen local sources in dependency order, verifies all seventy-five expected report names, rejects unexpected diagnostics or nonstandard proof dependencies, and records source, object and log hashes. Outputs must be new: existing regular files, directories, live symlinks and dangling symlinks are rejected. The control program mutates each of the eighteen local sources and the dependency manifest separately, and checks those four occupied-output cases. These twenty-three controls test the wrapper's integrity and preservation behavior; the mathematical proofs are checked by the compiler run, not by the mutation controls.

The author run passed all seventy-five reports in 46.73 seconds of recorded compiler time. The twenty-three rejection controls passed. A second fresh build from an isolated twenty-one-file replay tree passed in 43.61 seconds; no manuscript or private study file was present in that tree. These are author checks, pending independent review.

The default replay needs only the two executable wrappers, the eighteen enumerated local Lean sources, `formal/dependency_manifest.json`, and the pinned external compiler/packages. It does not read private source PDFs, the historical source bank, manuscript registries, GitHub, GKM experiments, or the prose provenance documents. The exact public allowlist and recorded run outputs are frozen in the manifest after successful replay.

## 7. What this certificate does not claim

The source's finite parabolic order formula \(|H_S|=|E_S||G_S|/2^{c(S)}\) and its exact adjacent-product least-common-multiple orders are not formalized in this package. The all-support group profile needed to derive the former is formalized; the numerical conclusion must still be proved and separately checked before it can be advertised as a Lean result.

Application-specific assertions remain external: the chosen finite-field parameters, the BFL generation and intersection results for a concrete symmetry group, the existence and marker values of its Dickson character, any chosen unitriangular or permutation parity character, and the group-to-polytope correspondence. Neither this package nor the earlier local quadratic-relator certificate proves the full source theorem without those inputs. The all-label universal-group conjecture is not proved here. There is no source-level compression ratio, historical priority claim, or additional whole-paper replacement credit.

The proof-library accounting follows the GKM methodology of reusing retained interfaces before adding proof bodies and recording the full acquisition cost. This is methodological attribution, not an import of GKM experimental results. The checkpoint records the first frozen version of every new body, all charged local dependencies, and actual consumer edges. It has no matched alternative formal proof and no previous frozen version of these twelve new bodies: consequently removed duplication, measured payback, a sawtooth trend, and a compression ratio are unmeasured. Later changes must distinguish gross additions, removals and signed net change, while retaining exact body versions and consumer bindings.
