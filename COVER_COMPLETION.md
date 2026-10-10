# Universal completion and an exact cover classification

**One marked group now classifies every regular cover with the prescribed
end groups.** For the specified Γ2 family, its covering kernel is the
Klein-four group. Exactly two covers survive the intersection test: a
degree-four cover and its degree-two quotient. Only the double cover is
minimal. Covers that enlarge either end remain outside this classification.

The [general proof](research/case_study/phase90_universal_complement_bridge.md),
[family proof](research/case_study/phase92_complement_normal_form_theorem.md)
and their separate [general](research/case_study/phase96_universal_complement_review.md)
and [family](research/case_study/phase97_complement_normal_form_review.md)
reviews are distributed in full. The [root admission](research/case_study/phase101_completion_root_admission.md)
records fresh execution from public files. These are internal mathematical
reviews; historical priority remains unverified.

## The reusable object

Let a finite group G have four marked involutions satisfying the string
commutations. Its two end groups
`A=⟨r0,r1,r2⟩` and `B=⟨r1,r2,r3⟩` must already be rank-three string C-groups.
Put `C=⟨r1,r2⟩` and `I=A∩B`. The base G need not satisfy the intersection
property. Form

```text
W = (A *_C B) / <<[r0,r3]>>,       K = ker(W → G).
```

The amalgam includes every local relation of A and B. Every marked cover
whose two end projections are injective is a quotient of W over G. The
two copies of an element `i∈I` need not coincide in W: their difference
`e_i=i_B⁻¹i_A` is the defect that a polytopal quotient must preserve.

The computational presentation U has one generator for each coset `Cg`
and one relation for each translated outer commuting square. Regard those
cosets as edges from `Bg` to `Ag`. A spanning tree separates redundant
edge coordinates from loops, giving the explicit identification

```text
U ≅ F_(|G:A|+|G:B|−1) * K,
δ_i = t_C⁻¹ t_Ci  ↦  e_i.
```

The proof identifies K with the fundamental group of this square complex.
It fixes the paths, orientations and defect words. Killing the actual
tree-edge generators recovers K; matching abstract free ranks alone would
not justify that step.

For any nonempty class of finite groups closed under isomorphisms, subgroups
and finite direct products, a finite cover with kernel in that class and
unchanged ends exists **if and only if, for every coset Ci≠C in C\I, its
defect δ_i survives in a finite quotient of U in that class**. If such a
defect is already trivial in U, existence is obstructed. The proof combines
separating maps and takes a normal core. It needs neither coprimality nor
an abelian kernel.

If one such polytopal cover exists, W itself is polytopal. If K is finite,
every cover in this scope is a finite quotient `W/N`, where

```text
N ◁ W,       N ≤ K,       N ∩ E = {1},
E = {i_B⁻¹i_A : i∈I} = K ∩ BA.
```

Here BA is a set product; E need not be a subgroup. This is the common
normal-subgroup problem behind the separate constructions.

## The Γ2 calculation

The exact source is Cunningham–Pellicer, *Tight chiral polytopes*,
[arXiv:2009.04566v1](https://arxiv.org/abs/2009.04566v1), Table 2 row Γ2
and Theorem 4.8: `q=2^β`, `β≥5`, and either choice of each sign. Its
presentation, existence, tight orders, normal form and intersection property
are retained source inputs. The earlier [two-primary analysis](COVER_TWO_PRIMARY.md)
proves that its smallest regular maniplex G has full group order `256q`
and one common marked action on 128 cosets for every parameter.

For that action the exact certificate proves

```text
128 generators, 1,024 square relations
    → 111 reversible eliminations
    → U ≅ F15 * ⟨X,Y | X²=Y²=[X,Y]=1⟩,
      δ = X.
```

Both directions of the presentation isomorphism are checked. The fifteen
displayed original free generators are actual spanning-tree edges, so
`K≅C2×C2`. An independently constructed affine cover identifies the
extension and its action on K: `r0` and `r3` send X to XY and fix Y;
the middle generators fix both. Thus `⟨Y⟩` is the unique invariant line.

| Marked object over G | Full group order | Conclusion |
|---|---:|---|
| Universal completion W | `1024q` | Degree four; polytopal |
| `W/⟨Y⟩` | `512q` | Degree two; the unique minimum with unchanged ends |
| `W/K=G` | `256q` | Fails the required end intersection |

These are full group orders, unlike the rotation-group orders in the
earlier construction table. Universality proves completeness even for
covers not initially assumed finite. The double cover agrees, as a marked
cover over G, with the earlier construction. A second unrestricted minimal
cover would have to enlarge at least one end.

## Attribution and verification

Universal regular amalgamation is established theory. The
[bounded literature audit](research/case_study/phase100_cover_priority_completion_report.md)
records Cunningham–Pellicer's 2016 attribution to Schulte's 1988 work and
directly read related amalgam constructions of Monson–Schulte. Bass–Serre
theory, van Kampen, free-product normal forms and string C-group recognition
are retained tools. The original Schulte proof was not acquired in that audit.

The repository supplies the displayed complement/defect interface,
finite-class criterion, explicit normal-form maps, kernel action and exact
Γ2 classification. This describes where its arguments enter; it does not
establish historical novelty. The complete 2014 mix paper and relevant
2025 book chapters remain material unread comparisons.

Fresh public checks regenerate the certificate byte for byte, verify all
1,024 original relations and 512 residual relations, and check 4,096 action
edges. A separately implemented verifier enumerates the entire 4,096-element
affine model and its end intersection. Written proofs supply the uniform
parameter transport and completeness. Seven altered-input controls and
three occupied-output controls pass under optimized Python.

Use the commands in [Reproducing](REPRODUCING.md#universal-completion-and-the-exact-two-cover-classification).
No new Lean module formalizes this entire classification. The earlier
[Lean obstruction](research/case_study/formal/OddKernelWord.scope.md) retains
its exact word-identity scope. These standalone results add no manuscript
to Compress_12 and carry no measured length factor or cleared
open-conjecture marker.
