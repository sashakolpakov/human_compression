# A second minimal cover throughout the Γ2 family

**Every specified Γ2 polytope has at least two finite minimal regular
covers.** The construction allows the end groups to grow. It therefore
complements the [classification with unchanged ends](COVER_COMPLETION.md),
where only the double cover is minimal.

The [complete proof](research/case_study/phase102_expanded_end_covers_theorem.md),
[independent mathematical review](research/case_study/phase104_expanded_end_review_audit.md)
and [root admission with fresh computations](research/case_study/phase111_expanded_end_root_admission.md)
are distributed. This is an internally reviewed result with exact finite
certificates and a written uniform proof. Historical priority remains
unverified.

## Exact family and conclusion

**[B]** The source is Cunningham–Pellicer, *Tight chiral polytopes*,
[arXiv:2009.04566v1](https://arxiv.org/abs/2009.04566v1), Table 2 row Γ2
and Theorem 4.8. Let `q=2^β`, `β≥5`, with either choice of each of the two
signs. The original chiral polytope has type `{8,q,8}`. Its construction,
tightness, orders, normal forms, chirality and intersection property remain
retained source results.

Let G be the full reflection group of its smallest regular maniplex;
`|G|=256q`. The reviewed predecessors supply its nonpolytopality, its
minimal regular double cover S, and the fixed marked quotient
`G/⟨(r1r2)^4⟩=D` of order 1,024. These are required inputs.

**[I]** The repository construction proves:

| Object or conclusion | Exact scope |
|---|---|
| Explicit regular polytopal cover H of G | Type `{24,q,24}`, elementary abelian kernel of order `3^130` |
| Two end projections | Each has kernel of order `3^17` |
| Medial projection | Injective |
| Minimal polytopal descendant Q | Exists with degree `3^d`, `1≤d≤130`, over G; no particular Q or d is selected |
| Comparison with S | Q and the degree-two cover S are distinct minimal regular covers |
| Universal relation kernels | The kernels defining H and S have product equal to the kernel defining G |

The last equality implies that the join of all finite admissible relation
kernels is the kernel of G. It concerns kernels in the same universal
marked string group, not a presumption that arbitrary mixes are polytopal.

## Why finite linear algebra is enough here

**[I]** Start with the permutation module

```text
E = F3[⟨r0⟩\D] ⊕ F3[⟨r3⟩\D].
```

Each summand has 512 coordinates. Four explicit affine lifts satisfy the
involution and string relations. Schreier rewriting computes their entire
translation kernel L. Quotient by the orbit span M of the literal medial
relation `(h1h2)^4`. The exact ranks are `dim L=257`, `dim M=127`.

Subgroup intersections require two checks: intersect the translation
subspaces, and prove the affine fibers are disjoint above every unwanted
base element. Both are checked. This retains the group and incidence
conditions that linear ranks alone would miss.

The changing kernel `N=⟨(r1r2)^4⟩` is a cyclic 2-group. In characteristic
three, cubing an affine lift above n kills its translation. Every element
of N has a cube root, so the generated cover contains the full standard N.
This proves the required pullback description for every parameter. Separate
local intersection arguments then establish the full intersection property.

Choose an inclusion-maximal J inside the finite covering kernel that is
normal in H and for which H/J is polytopal. This gives a minimal descendant.
Its degree is odd and greater than one, while
S has degree two. Coprime indices also prove the universal-kernel product
equality. H itself is not claimed minimal.

## Attribution and certificate boundaries

**[B]** Gabe Cunningham's *Chiral polytopes whose smallest regular cover is
a polytope*, [July 2023 author version](https://gabrielcunningham.com/WhichChiralPolytopes.pdf),
§4, supplies an earlier multiple-minimal-cover example and proposes
multiplicity for the five families in Example 3.5. The cover correspondence,
recursive string C-group recognition and finite group arguments are retained
background. The affine construction and uniform pullback above are
repository derivations; that attribution is not a priority claim.

**[V]** The author checker regenerates the complete certificate. The
independent checker uses different coordinates, transversals and F3 row
arithmetic and checks all 16 parabolics and all 136 unordered subset pairs.
Fresh root runs reproduce both computations. All six changed-input and
three occupied-output controls pass. The 1,024-element base is enumerated;
the enormous affine cover is handled through its exact translation spaces.
The complete code and 1,115,038-byte certificate are required proof data.

**[L]** The separately reviewed
[Lean component](research/case_study/formal/OddCoverSeparation.scope.md)
proves general kernel divisibility, odd-degree separation and finite
admissible maximality. It does not formalize this affine construction,
its intersection property or the geometric correspondence.

The result proves the Γ2 case of the stated multiplicity proposal under
its retained source contract. Current openness and historical novelty
have not been cleared, so no **[O]** sign is assigned. The other two-primary
families, classification of all minimal descendants and the general
conjecture remain outside this result. It adds no manuscript to Compress_12
and changes no compression ratio. See [Reproducing](REPRODUCING.md#covers-with-enlarged-ends)
for the exact replay commands.
