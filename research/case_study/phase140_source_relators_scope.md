# Formal certificates for the equal-label source relations

10 October 2026. Frozen author certificate, pending independent review. This bundle adds two Lean components. Its 28 printed declarations are proof steps, not 28 source results or 28 resolved conjectures. The public repository has not been modified by the author.

## The exact conclusion

The main characteristic-two theorem is an equality of actual linear automorphisms of the entire ambient vector space. Let F be any field of characteristic two, let V be an F-vector space, and let Q be a quadratic form, with polar form B. Neither finite dimension nor nondegeneracy is assumed. Define

\[
\sigma_u(x)=x+B(x,u)u.
\]

If Q(e)=Q(f)=Q(h)=1, B(e,h)=0 and B(e,f)=B(f,h), then the Lean theorem `equal_label_integer_relation` proves

\[
\left((\sigma_f\sigma_h)^k(\sigma_e\sigma_f)^k\right)^2=1
\qquad(k\in\mathbb Z).
\]

Products apply the rightmost map first. The conclusion is not restricted to the span of e,f,h. This matters when that span is degenerate: an identity on the span alone would not establish the source relation on adjacent ambient coordinates. No target power relation, translation subgroup, normalizing action, or quotient calculation is assumed in this final theorem.

The second component proves the exact local equivalence needed in the universal label-four adapter. In any group, let a,b,c have square one and let a commute with c. Then

\[
(ab)^4=(bc)^4=1,\qquad
\big((bc)^k(ab)^k\big)^2=1\quad(1\leq k\leq3)
\]

is equivalent to the two adjacent pairs of nested commutator relations and the cross-commutator relation

\[
[a,[a,b]]=[b,[a,b]]=1,\qquad
[b,[b,c]]=[c,[b,c]]=1,\qquad
[[a,b],[b,c]]=1.
\]

Lean uses `[x,y]=xyx⁻¹y⁻¹` here, exactly as the written adapter does. The equivalence permits identity generators. It does not assert their exact orders or the exact adjacent order four.

## Where the proof comes from

The mathematical arguments being formalized are the existing written arguments in `phase124_equal_label_char2_bridge.md` and `phase124_universal_four_adapter.md`. Their frozen bytes are retained in this bundle's manifest. The formalization reworks those proofs and supplies every algebraic step; it does not restart the literature argument or relabel a retained theorem as a new discovery.

For the characteristic-two proof, the source construction of finite groups with the required intersection property remains Brooksbank–Ferrara–Leemans, *Orthogonal groups in characteristic 2 acting on polytopes of high rank*, arXiv:1709.02219v2, published in *Discrete & Computational Geometry* 63 (2020), 656–669. The exact published inputs and field restrictions are recorded in the written bridge. They are not axioms in either new Lean source: neither source states or invokes their group-generation or intersection theorem. Those results are needed when this local certificate is used to deduce the finite-existence corollary.

For label four, the identification with the unitriangular group remains the presentation theorem of Biss–Dasgupta, *A Presentation for the Unipotent Group over Rings with Identity*, *Journal of Algebra* 237 (2001), 691–707, Theorem 1, specialized to m=2. That paper credits the binary presentation to Biss's 1998 work. This certificate establishes the bidirectional relation adapter, not the retained presentation theorem. Its algebra is valid in every ambient group; there is no extra Lean axiom asserting the presented group's structure.

The local characteristic-two identity and the local label-four conversion are the proof contributions of the existing project notes being certified here. Historical priority of those applications to Li–Zhang's Conjecture 3.7 has not been determined. The formalization makes no new priority claim.

## Characteristic-two proof map

`formal/CharacteristicTwoTranslations.lean` contains the actual definitions and 20 printed declarations in the namespace `MathCompression.CharacteristicTwoTranslations`.

| Declarations | What is proved |
| --- | --- |
| `polar_self_zero`, `vector_add_self`, `quadratic_add` | The alternating polar identity, characteristic-two vector cancellation, and the quadratic addition formula used below. |
| `translation_comp`, `translation_zero`, `translation_involutive` | For the displayed formula T_u, the identities T_u T_v=T_(u+v), T_0=1 and T_u²=1 hold on the whole ambient space whenever B(u,z)=B(v,z)=0. |
| `symmetry_pair` | If Q(u)=1 and B(u,z)=0, the actual maps satisfy σ_u σ_(u+z)=T_u. |
| `symmetry_involutive`, `symmetry_preserves`, `polar_preserves` | The displayed symmetries are involutions; a unit-value symmetry preserves Q; a Q-preserving linear equivalence preserves its polar form. |
| `translation_covariant`, `translation_conjugate` | Linearity, Q preservation, and g(z)=z imply g T_u g⁻¹=T_(g(u)), with the transformed parameter still perpendicular to z. |
| `symmetry_pair_equiv`, `singular_shift` | The pair identity is upgraded to equality of actual linear-equivalence group elements; Q(z)=0 also gives Q(u+z)=1. |
| `translationGroup_square`, `translationGroup_conjugate` | Every element of the explicitly constructed translation subgroup has square one, and each Q-preserving linear equivalence fixing z normalizes it. |
| `integer_power_product_mem`, `integer_power_product_square` | For a subgroup N with ac∈N and conjugation closure by a and a⁻¹, c^k a^k lies in N for every integer k. If every element of N has square one, the product has square one. Both positive and negative induction steps are proved. |
| `triple_singular_radical`, `equal_label_integer_relation` | The hypotheses on e,f,h give the needed singular vector and polar cancellations; the actual symmetries satisfy all of the preceding subgroup theorem's hypotheses, yielding the desired relation for every integer. |

The intermediate linear maps, linear equivalences, and `translationGroup` are definitions with proved structure fields. For example, closure of the subgroup under multiplication invokes `translation_comp`; it is not inserted as an assumption. The translation formula is

\[
T_u(x)=x+B(x,z)u+\bigl(B(x,u)+Q(u)B(x,z)\bigr)z.
\]

In the final attachment z=e+h. The proof obtains B(e,z)=B(f,z)=0, proves that A=σ_eσ_f preserves Q and fixes z, and also proves those properties for A⁻¹. It then establishes

\[
AC=\sigma_e\sigma_h=T_e\in T,
\qquad C=\sigma_f\sigma_h,
\]

and invokes the already proved all-integer subgroup lemma. In the formalization, T uses every parameter in z-perp rather than only parameters in span(e,f,h). This removes a separate subspace-invariance obligation while proving the same ambient relation. Its membership and normalizing identities are still derived from the actual quadratic form. The algebraic composition and conjugation statements happen not to require Q(z)=0; singularity is nevertheless proved for z=e+h and retained in the exact source attachment.

## Label-four proof map

`formal/LabelFourRelations.lean` contains eight printed declarations in the namespace `MathCompression.LabelFourRelations`.

| Declaration | What is proved |
| --- | --- |
| `commutator_eq_square` | For a²=b²=1, [a,b]=(ab)². |
| `nested_commutators` | Both adjacent nested commutators equal ((ab)⁴)⁻¹. |
| `adjacent_relations_iff` | Their vanishing is equivalent to (ab)⁴=1. |
| `commutator_iff_reversed_square` | For u²=v²=1, [u,v]=1 exactly when (vu)²=1. |
| `cross_relation_iff` | Under the adjacent fourth powers, the cross-commutator relation is exactly the source k=2 relation. |
| `first_power_relation` | The source k=1 relation follows from involutivity and distant commutation. |
| `third_power_relation` | The source k=3 relation follows as well once the adjacent fourth powers hold. |
| `label_four_relations_iff` | Both directions of the complete consecutive-triple relation adapter. |

The last theorem is a local relation equivalence. Passing from this theorem for every consecutive triple to equality of the two presentation kernels is a written application in the retained adapter. This bundle does not construct a Lean `PresentedGroup`, prove its marking-preserving isomorphism, count a unitriangular group, or prove its matrix-parabolic intersection property.

## Reproduction and trust boundary

From a directory containing this bundle and `formal/dependency_manifest.json`, run:

```sh
python3 -B -O phase140_source_relators_check.py \
  --packages /path/to/pinned/.lake/packages \
  --lean /path/to/lean \
  --output-dir /fresh/output/directory
```

The manifest pins Lean 4.32.2 and every package revision, including Mathlib revision `905b95818eb32af7874a58b427f50c1711a5e96c`. The runner checks those revisions and tracked-file cleanliness, the dependency-manifest hash, and both complete source hashes. It freshly compiles both local modules. It also freshly compiles the two required pinned Mathlib modules `Mathlib.LinearAlgebra.SesquilinearForm.Orthogonal` and `Mathlib.LinearAlgebra.QuadraticForm.Basic` in a private namespace overlay. Other cached package objects and the installed compiler remain in the trust boundary. No package checkout or cached object is overwritten.

The runner requires all 28 expected axiom reports, rejects duplicate or missing reports, and rejects warnings, errors, unproved placeholders, `sorryAx`, and native-evaluation trust. The actual reports use only `propext` and `Quot.sound`; the label-four component uses only `propext`. The author fresh build passed in 22.89 seconds. A complete Lean check supplies the universal proof; finite computations are not substitutes for it.

The companion `phase140_source_relators_controls.py` runs seven rejection cases: a changed copy of each Lean source, a changed dependency manifest, an occupied regular output file, an occupied directory, a live symlink, and a dangling symlink. Every case fails for the intended reason while preserving the occupied target and the original inputs. It can be invoked with the same `--packages`, `--lean`, and fresh `--output-dir` arguments. These are author checks, not independent review.

The older finite matrix diagnostics were not rerun: this work adds symbolic proofs, and their scope is established by reading and rebuilding the actual statements. No new finite-experiment count is claimed.

## What is still outside the certificate

Neither file formally proves the finite-field parameter selection, the retained orthogonal-group generation and intersection theorem, the general string-C-group/polytope correspondence, the unitriangular presentation theorem, or the source-level finite-existence and universal-label-four conclusions. In particular, the all-label universal-group conjecture has not been solved by this bundle. A finite image satisfying relations still need not be the universal group.

The checkpoint records acquisition cost for these two formal proof bodies and their actual written consumers. It claims no measured source-level compression ratio, no removed duplication in the original papers, and no already achieved formal reuse payoff. A later consumer should cite and discharge the exact interfaces rather than copy these proofs.
